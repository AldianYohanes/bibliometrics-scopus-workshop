"""Menyapu ambang sitasi/kemunculan dan melaporkan apakah peta memenuhi aturan pembimbing: 3-5 kluster, tiap kluster minimal 6 item.

Hanya melaporkan; tidak mengubah tabel, gambar, atau naskah. Rumus graf sama dengan tabel_template.py (Louvain, seed 42, simpul diurutkan).
Keluaran: Hasil/sapu_ambang.csv. Jalankan: python -I sapu_ambang.py
"""
import itertools, json, os, sys, time, urllib.parse, urllib.request
from collections import Counter

import networkx as nx
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = open(os.path.expanduser("~/Tools/openalex.key")).read().strip()
SEED, MIN_ITEM, K_MIN, K_MAX = 42, 6, 3, 5
CURIGA = {"https://openalex.org/W4385245566", "https://openalex.org/W4292779060", "https://openalex.org/W4384918448"}
d = pd.read_csv(f"{ROOT}/Data/dataset_lolos.csv", encoding="utf-8-sig").fillna("")
ex = dict(zip(*pd.read_csv(f"{ROOT}/Data/referensi_tambahan.csv", encoding="utf-8-sig").fillna("")[["id", "referenced_works"]].T.values))
refs = {i: set((r or ex.get(i, "")).split("|")) - {""} for i, r in zip(d.id, d.referenced_works)}
refs = {i: s for i, s in refs.items() if s}
cit = Counter(r for s in refs.values() for r in s)
rows = []


def louvain(G):
    return sorted(nx.community.louvain_communities(G, weight="weight", seed=SEED), key=len, reverse=True)


def lapor(peta, ambang, G):
    G.remove_nodes_from([n for n in list(G) if G.degree(n) == 0])
    if G.number_of_nodes() == 0:
        return
    ks = [len(c) for c in louvain(G)]
    kecil = sum(1 for k in ks if k < MIN_ITEM)
    ok = K_MIN <= len(ks) <= K_MAX and kecil == 0
    rows.append({"peta": peta, "ambang": ambang, "item": G.number_of_nodes(), "kluster": len(ks), "ukuran": ks[:10], "kluster_<6": kecil, "memenuhi_aturan": ok})


# co-citation: tipe dokumen diambil dari OpenAlex untuk membuang prosiding/artefak, sama seperti tabel_template.py
kandidat = [r for r, c in cit.items() if c >= 2]
tipe = {}
for i in range(0, len(kandidat), 50):
    q = {"filter": "openalex_id:" + "|".join(kandidat[i:i + 50]), "per-page": 50, "select": "id,display_name,type", "api_key": KEY}
    with urllib.request.urlopen("https://api.openalex.org/works?" + urllib.parse.urlencode(q), timeout=60) as r:
        for w in json.load(r)["results"]:
            tipe[w["id"]] = (w.get("type") or "", (w.get("display_name") or "").lower())
    time.sleep(0.1)
bad = {r for r in kandidat if r in CURIGA or tipe.get(r, ("", ""))[0] == "proceedings" or tipe.get(r, ("", ""))[1].startswith(("proceedings of", "findings of"))}
for k in range(2, 9):
    keep = {r for r, c in cit.items() if c >= k} - bad
    C = nx.Graph(); C.add_nodes_from(sorted(keep))
    for s in refs.values():
        for a, b in itertools.combinations(sorted(s & keep), 2):
            C.add_edge(a, b, weight=C.get_edge_data(a, b, {"weight": 0})["weight"] + 1)
    lapor("co-citation (min. sitasi referensi)", k, C)

# co-word
SIN = {"llm": "large language model", "llms": "large language model", "large language models": "large language model", "language model": "large language model", "language models": "large language model", "ai": "artificial intelligence"}
BUANG = {"large language model", "artificial intelligence"}
kws = [sorted({SIN.get(k.strip().lower(), k.strip().lower()) for k in s.split(";") if k.strip()} - BUANG) for s in d.keywords]
cnt = Counter(k for ks in kws for k in ks)
for k in range(5, 16):
    kk = {w for w, c in cnt.items() if c >= k}
    G = nx.Graph(); G.add_nodes_from(sorted(kk))
    for ks in kws:
        for a, b in itertools.combinations([w for w in ks if w in kk], 2):
            G.add_edge(a, b, weight=G.get_edge_data(a, b, {"weight": 0})["weight"] + 1)
    lapor("co-word (min. kemunculan kata kunci)", k, G)

# bibliographic coupling: simpul disaring menurut sitasi dokumen (cited_by), tepi minimal 2 referensi sama (seperti tabel_template.py)
cb = dict(zip(d.id, d.cited_by.astype(int)))
for k in (0, 1, 2, 3, 5, 8, 10, 15, 20):
    ids = sorted(i for i in refs if cb[i] >= k)
    B = nx.Graph(); B.add_nodes_from(ids)
    for a, b in itertools.combinations(ids, 2):
        s = len(refs[a] & refs[b])
        if s >= 2:
            B.add_edge(a, b, weight=s)
    lapor("bibliographic coupling (min. sitasi dokumen)", k, B)

out = pd.DataFrame(rows)
out.to_csv(f"{ROOT}/Hasil/sapu_ambang.csv", index=False, encoding="utf-8-sig")
pd.set_option("display.width", 250, "display.max_colwidth", 70)
print(out.to_string(index=False))
