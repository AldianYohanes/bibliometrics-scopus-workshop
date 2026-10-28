"""Peta tema (centrality-density, gaya Callon) dan perubahan porsi kata kunci per tahun.

Co-word: kluster Louvain pada ambang kemunculan 5 dan 8. Centrality = jumlah bobot garis keluar kluster; density = 100 x rata-rata bobot garis dalam kluster
per kata (definisi Callon yang dipakai Biblioshiny; pembulatan beda dari Biblioshiny mungkin). Data hanya 2023-2026, jadi bukan deteksi lonjakan (burst)
dengan algoritma Kleinberg: kami hanya membandingkan porsi kata kunci 2025 dan 2026.
Jalankan: python -I peta_tema.py
"""
import itertools, os, sys
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = f"{ROOT}/Hasil"
d = pd.read_csv(f"{ROOT}/Data/dataset_lolos.csv", encoding="utf-8-sig").fillna("")
SIN = {"llm": "large language model", "llms": "large language model", "large language models": "large language model",
       "language model": "large language model", "language models": "large language model", "ai": "artificial intelligence"}
BUANG = {"large language model", "artificial intelligence"}
kws = [sorted({SIN.get(k.strip().lower(), k.strip().lower()) for k in s.split(";") if k.strip()} - BUANG) for s in d.keywords]
cnt = Counter(k for ks in kws for k in ks)


def graf(min_kw):
    keep = {k for k, c in cnt.items() if c >= min_kw}
    G = nx.Graph(); G.add_nodes_from(sorted(keep))
    for ks in kws:
        for a, b in itertools.combinations([k for k in ks if k in keep], 2):
            G.add_edge(a, b, weight=G.get_edge_data(a, b, {"weight": 0})["weight"] + 1)
    G.remove_nodes_from([n for n in list(G) if G.degree(n) == 0])
    return G


rows = []
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for ax, mk in zip(axes, (8, 5)):
    G = graf(mk)
    com = sorted(nx.community.louvain_communities(G, weight="weight", seed=42), key=len, reverse=True)
    lab = {n: i for i, c in enumerate(com, 1) for n in c}
    for i, c in enumerate(com, 1):
        inn = sum(w for u, v, w in G.edges(c, data="weight") if u in c and v in c)
        out = sum(w for u, v, w in G.edges(c, data="weight") if (u in c) != (v in c))
        dens, cen = 100 * inn / len(c), out
        top = ", ".join(sorted(c, key=lambda k: -cnt[k])[:4])
        rows.append({"ambang": mk, "kluster": i, "kata": len(c), "centrality": cen, "density": round(dens, 1), "kata_teratas": top})
        ax.scatter(cen, dens, s=40 + 12 * len(c), alpha=0.7)
        ax.annotate(f"{i}: {top.split(',')[0]}", (cen, dens), fontsize=8)
    ax.set_xlabel("Centrality (weight of links to other clusters)"); ax.set_ylabel("Density"); ax.set_title(f"Thematic map, minimum {mk} occurrences ({len(com)} clusters)")
fig.tight_layout(); fig.savefig(f"{H}/peta_tema.png", dpi=130); plt.close(fig)
pd.DataFrame(rows).to_csv(f"{H}/peta_tema.csv", index=False, encoding="utf-8-sig")
print(pd.DataFrame(rows).to_string(index=False))

# porsi kata kunci 2025 vs 2026
ny = Counter(d.year)
by = {y: Counter() for y in (2025, 2026)}
for ks, y in zip(kws, d.year):
    if y in by:
        for k in ks:
            by[y][k] += 1
out = []
for k in cnt:
    if cnt[k] >= 8:
        p25, p26 = by[2025][k] / ny[2025], by[2026][k] / ny[2026]
        out.append({"kata": k, "dokumen_total": cnt[k], "n_2025": by[2025][k], "n_2026": by[2026][k], "porsi_2025_persen": round(100 * p25, 1), "porsi_2026_persen": round(100 * p26, 1), "selisih_poin": round(100 * (p26 - p25), 1)})
df = pd.DataFrame(out).sort_values("selisih_poin")
df.to_csv(f"{H}/perubahan_porsi_kata.csv", index=False, encoding="utf-8-sig")
print("\nporsi turun terbanyak:\n", df.head(6).to_string(index=False))
print("\nporsi naik terbanyak:\n", df.tail(6).to_string(index=False))
print("\ndokumen 2025:", ny[2025], "| 2026:", ny[2026])
