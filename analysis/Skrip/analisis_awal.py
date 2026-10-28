"""Peta pertama dari Data/dataset_lolos.csv: co-word, bibliographic coupling, tabel kinerja.

Hasil ke Hasil/ (tabel CSV, PNG, dan file masukan VOSviewer). Acak diberi seed supaya bisa diulang.
Jalankan: python -I analisis_awal.py
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
OUT = os.path.join(ROOT, "Hasil")
os.makedirs(OUT, exist_ok=True)
d = pd.read_csv(os.path.join(ROOT, "Data", "dataset_lolos.csv"), encoding="utf-8-sig").fillna("")
SEED = 42
print("dokumen:", len(d))

# ---------- kinerja ----------
d["tahun"] = d.year
d.groupby("tahun").size().rename("dokumen").to_csv(f"{OUT}/kinerja_tahun.csv")
d.groupby("source").agg(dokumen=("id", "size"), sitasi=("cited_by", "sum")).sort_values("dokumen", ascending=False).head(20).to_csv(f"{OUT}/kinerja_sumber.csv")
cs = d.countries.str.split("; ").explode()
cs[cs != ""].value_counts().head(20).rename("dokumen").to_csv(f"{OUT}/kinerja_negara.csv")
au = d.authors.str.split("; ").explode()
au[au != ""].value_counts().head(20).rename("dokumen").to_csv(f"{OUT}/kinerja_penulis.csv")
d.sort_values("cited_by", ascending=False)[["title", "year", "source", "cited_by", "blok"]].head(15).to_csv(f"{OUT}/kinerja_sitasi_teratas.csv", index=False)

# ---------- co-word ----------
SINONIM = {"llm": "large language model", "llms": "large language model", "large language models": "large language model",
           "language model": "large language model", "language models": "large language model", "ai": "artificial intelligence"}
BUANG = {"large language model", "artificial intelligence"}  # ada di hampir semua dokumen, tidak membedakan
docs_kw = []
for s in d.keywords:
    ks = {SINONIM.get(k.strip().lower(), k.strip().lower()) for k in s.split(";") if k.strip()}
    docs_kw.append(sorted(ks - BUANG))
cnt = Counter(k for ks in docs_kw for k in ks)
MIN_KW = 8
keep = {k for k, c in cnt.items() if c >= MIN_KW}
G = nx.Graph()
for k in sorted(keep):
    G.add_node(k, n=cnt[k])
for ks in docs_kw:
    for a, b in itertools.combinations([k for k in ks if k in keep], 2):
        w = G.get_edge_data(a, b, {"weight": 0})["weight"] + 1
        G.add_edge(a, b, weight=w)
G.remove_nodes_from([n for n in list(G) if G.degree(n) == 0])
com = nx.community.louvain_communities(G, weight="weight", seed=SEED)
com = sorted(com, key=len, reverse=True)
rows = []
for i, c in enumerate(com, 1):
    for k in c:
        G.nodes[k]["cluster"] = i
    top = sorted(c, key=lambda k: -cnt[k])[:8]
    rows.append({"kluster": i, "jumlah_kata": len(c), "kata_teratas": "; ".join(f"{k} ({cnt[k]})" for k in top)})
pd.DataFrame(rows).to_csv(f"{OUT}/coword_kluster.csv", index=False, encoding="utf-8-sig")
print(f"co-word: {G.number_of_nodes()} kata (min {MIN_KW} kemunculan), {G.number_of_edges()} garis, {len(com)} kluster")
pos = nx.spring_layout(G, weight="weight", seed=SEED, k=0.9)
fig, ax = plt.subplots(figsize=(13, 9))
cmap = plt.get_cmap("tab10")
nx.draw_networkx_edges(G, pos, alpha=0.12, width=[0.3 + 0.15 * G[u][v]["weight"] ** 0.5 for u, v in G.edges], ax=ax)
nx.draw_networkx_nodes(G, pos, node_size=[40 + 14 * G.nodes[n]["n"] for n in G], node_color=[cmap((G.nodes[n]["cluster"] - 1) % 10) for n in G], alpha=0.85, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=7, ax=ax)
ax.set_title("Peta co-word (kata kunci OpenAlex), warna = kluster"); ax.axis("off")
fig.tight_layout(); fig.savefig(f"{OUT}/peta_coword.png", dpi=130); plt.close(fig)
# masukan VOSviewer: file peta + file jaringan (tab)
idx = {k: i for i, k in enumerate(G, 1)}
with open(f"{OUT}/vos_coword_map.txt", "w", encoding="utf-8") as f:
    f.write("id\tlabel\tx\ty\tcluster\tweight<Occurrences>\n")
    for k in G:
        f.write(f"{idx[k]}\t{k}\t{pos[k][0]:.4f}\t{pos[k][1]:.4f}\t{G.nodes[k]['cluster']}\t{G.nodes[k]['n']}\n")
with open(f"{OUT}/vos_coword_network.txt", "w", encoding="utf-8") as f:
    for a, b, w in G.edges(data="weight"):
        f.write(f"{idx[a]}\t{idx[b]}\t{w}\n")

# ---------- bibliographic coupling (hanya dokumen yang punya referensi) ----------
r = d[d.referenced_works != ""].copy()
refs = {row.id: set(row.referenced_works.split("|")) for row in r.itertuples()}
ids = list(refs)
B = nx.Graph()
B.add_nodes_from(ids)
for a, b in itertools.combinations(ids, 2):
    s = len(refs[a] & refs[b])
    if s >= 2:
        B.add_edge(a, b, weight=s)
B.remove_nodes_from([n for n in list(B) if B.degree(n) == 0])
bc = sorted(nx.community.louvain_communities(B, weight="weight", seed=SEED), key=len, reverse=True)
tt = d.set_index("id")
rows = []
for i, c in enumerate(bc, 1):
    kw = Counter(k for n in c for k in docs_kw[d.index[d.id == n][0]])
    top_doc = sorted(c, key=lambda n: -tt.loc[n, "cited_by"])[:3]
    rows.append({"kluster": i, "jumlah_dokumen": len(c),
                 "kata_teratas": "; ".join(k for k, _ in kw.most_common(6)),
                 "blok": dict(Counter(tt.loc[n, "blok"] for n in c)).__str__(),
                 "contoh_judul": " || ".join(tt.loc[n, "title"][:70] for n in top_doc)})
pd.DataFrame(rows).to_csv(f"{OUT}/coupling_kluster.csv", index=False, encoding="utf-8-sig")
print(f"coupling: {len(r)} dokumen punya referensi, {B.number_of_nodes()} terhubung (>=2 referensi sama), {B.number_of_edges()} garis, {len(bc)} kluster")
