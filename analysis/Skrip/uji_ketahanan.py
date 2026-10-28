"""Uji ketahanan co-word: apakah kata-kata 'bisnis/agen/inventori' tetap terpisah dari kata-kata 'edge'?

Variasi: ambang kemunculan kata (5, 8, 12), algoritma (Louvain 20 seed, greedy modularity), dan tanpa blok B
(buang paper yang hanya dari blok B). Hasil: Hasil/ketahanan.csv. Jalankan: python -I uji_ketahanan.py
"""
import itertools, os, sys
from collections import Counter

import networkx as nx
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = pd.read_csv(os.path.join(ROOT, "Data", "dataset_lolos.csv"), encoding="utf-8-sig").fillna("")
SIN = {"llm": "large language model", "llms": "large language model", "large language models": "large language model",
       "language model": "large language model", "language models": "large language model", "ai": "artificial intelligence"}
BUANG = {"large language model", "artificial intelligence"}
BISNIS = {"inventory management", "demand forecasting", "multi-agent systems", "agentic ai", "llm agents", "supply chain management", "small and medium-sized enterprises", "business process automation"}
EDGE = {"edge computing", "model compression", "edge deployment", "on-device inference", "edge devices", "resource-constrained devices", "inference latency", "energy efficiency"}


def kw_list(frame):
    return [sorted({SIN.get(k.strip().lower(), k.strip().lower()) for k in s.split(";") if k.strip()} - BUANG) for s in frame.keywords]


def graf(docs_kw, min_kw):
    cnt = Counter(k for ks in docs_kw for k in ks)
    keep = {k for k, c in cnt.items() if c >= min_kw}
    G = nx.Graph()
    for k in sorted(keep):
        G.add_node(k)
    for ks in docs_kw:
        for a, b in itertools.combinations([k for k in ks if k in keep], 2):
            G.add_edge(a, b, weight=G.get_edge_data(a, b, {"weight": 0})["weight"] + 1)
    G.remove_nodes_from([n for n in list(G) if G.degree(n) == 0])
    return G


def ukur(G, comm):
    lab = {k: i for i, c in enumerate(comm) for k in c}
    b = [lab[k] for k in G if k in BISNIS]
    e = [lab[k] for k in G if k in EDGE]
    if len(b) < 3 or len(e) < 3:
        return None
    dom_b = Counter(b).most_common(1)[0]
    dom_e = Counter(e).most_common(1)[0]
    mod = nx.community.modularity(G, comm, weight="weight")
    # 'terpisah' = kata bisnis mayoritas (>=60%) dalam satu kluster yang bukan kluster dominan kata edge
    terpisah = dom_b[1] / len(b) >= 0.6 and dom_b[0] != dom_e[0] and dom_e[1] / len(e) >= 0.6
    tw = sum(w for u, v, w in G.edges(data="weight") if lab[u] != lab[v])
    return {"kata": G.number_of_nodes(), "kluster": len(comm), "modularitas": round(mod, 3), "terpisah": terpisah,
            "bisnis_dalam_1_kluster": round(dom_b[1] / len(b), 2), "garis_antar_kluster_persen": round(100 * tw / G.size(weight="weight"), 1)}


rows = []
skenario = {"semua": d, "tanpa_B_saja": d[d.blok != "B"]}
for nama, frame in skenario.items():
    dk = kw_list(frame)
    for mk in (5, 8, 12):
        if nama == "tanpa_B_saja" and mk > 5:
            continue
        G = graf(dk, mk)
        if G.number_of_nodes() < 10:
            continue
        for seed in range(20):
            r = ukur(G, nx.community.louvain_communities(G, weight="weight", seed=seed))
            if r:
                rows.append({"skenario": nama, "min_kata": mk, "algoritma": "louvain", "seed": seed, **r})
        r = ukur(G, list(nx.community.greedy_modularity_communities(G, weight="weight")))
        if r:
            rows.append({"skenario": nama, "min_kata": mk, "algoritma": "greedy", "seed": 0, **r})
df = pd.DataFrame(rows)
df.to_csv(os.path.join(ROOT, "Hasil", "ketahanan.csv"), index=False, encoding="utf-8-sig")
ring = df.groupby(["skenario", "min_kata", "algoritma"]).agg(percobaan=("seed", "size"), terpisah=("terpisah", "sum"),
                                                              kata=("kata", "median"), kluster=("kluster", "median"),
                                                              modularitas=("modularitas", "median"),
                                                              antar_persen=("garis_antar_kluster_persen", "median"))
print(ring.to_string())
