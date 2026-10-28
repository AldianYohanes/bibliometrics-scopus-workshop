"""Gambar peta yang rapi (mirip tampilan VOSviewer): co-word, co-citation, dan co-word berwarna tahun rata-rata.

Masukan: Hasil/graf.json (dari tabel_template.py) dan Data/dataset_lolos.csv.
Keluaran: Hasil/fig_cocitation.png, fig_coword.png, fig_tren.png. Tata letak dari Python (spring layout, seed tetap), jadi bukan tata letak VOSviewer.
Jalankan: python -I peta_gambar.py
"""
import json, os, sys
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from adjustText import adjust_text
from matplotlib.lines import Line2D

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = f"{ROOT}/Hasil"
plt.rcParams["font.family"] = ["Times New Roman", "DejaVu Serif"]
WARNA = {1: "#e15759", 2: "#59a14f", 3: "#4e79a7", 4: "#edc948", 5: "#b07aa1", 6: "#76b7b2", 7: "#f28e2b"}
NAMA_WARNA = {1: "red", 2: "green", 3: "blue", 4: "yellow", 5: "purple"}
J = json.load(open(f"{H}/graf.json", encoding="utf-8"))


def graf(d):
    G = nx.Graph()
    for n in d["nodes"]:
        G.add_node(n["id"], **n)
    G.add_weighted_edges_from(d["edges"])
    return G


def gambar(G, names, judul_legenda, file, label_fn, top_labels=None, edge_pct=70, warna_fn=None, size_scale=22, cbar=None, figsize=(11, 8.4), kfac=1.6):
    pos = nx.spring_layout(G, weight="weight", seed=7, k=kfac / np.sqrt(len(G)), iterations=600)
    fig, ax = plt.subplots(figsize=figsize)
    w = np.array([d["weight"] for _, _, d in G.edges(data=True)])
    cut = np.percentile(w, edge_pct)
    keep = [(u, v) for u, v, d in G.edges(data=True) if d["weight"] >= cut]
    nx.draw_networkx_edges(G, pos, edgelist=keep, edge_color="#9a9a9a", alpha=0.18, width=0.5, ax=ax)
    nodes = list(G)
    size = [size_scale + size_scale * 2.2 * G.nodes[n]["n"] ** 0.5 for n in nodes]
    col = [warna_fn(n) if warna_fn else WARNA.get(G.nodes[n]["cluster"], "#999999") for n in nodes]
    sc = nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_size=size, node_color=col, alpha=0.9, linewidths=0.4, edgecolors="white", ax=ax, cmap=cbar[0] if cbar else None,
                                vmin=cbar[1] if cbar else None, vmax=cbar[2] if cbar else None)
    lab_nodes = nodes if top_labels is None else sorted(nodes, key=lambda n: -G.nodes[n]["n"])[:top_labels]
    texts = [ax.text(pos[n][0], pos[n][1], label_fn(G, n), fontsize=7.5, color="#222222") for n in lab_nodes]
    adjust_text(texts, ax=ax, expand=(1.2, 1.4), arrowprops=dict(arrowstyle="-", color="#777777", lw=0.4))
    ax.axis("off")
    if cbar:
        cb = fig.colorbar(sc, ax=ax, shrink=0.55, pad=0.01); cb.set_label("Mean publication year", fontsize=9)
    else:
        h = [Line2D([0], [0], marker="o", color="w", markerfacecolor=WARNA[i], markersize=9, label=f"Cluster {i} ({NAMA_WARNA.get(i, '')}): {names[i - 1]}") for i in range(1, len(names) + 1)]
        ax.legend(handles=h, title=judul_legenda, loc="lower center", bbox_to_anchor=(0.5, -0.09), ncol=1, fontsize=8, title_fontsize=8.5, frameon=False)
    fig.savefig(f"{H}/{file}", dpi=200, bbox_inches="tight"); plt.close(fig)
    print(file, "ok:", len(G), "simpul,", len(keep), "garis digambar dari", G.number_of_edges())


cw = graf(J["coword"])
gambar(cw, J["coword"]["names"], "Clusters", "fig_coword.png", lambda G, n: n)

cc = graf(J["cocit"])
gambar(cc, J["cocit"]["names"], "Clusters", "fig_cocitation.png", lambda G, n: G.nodes[n]["label"].split(",")[0], top_labels=30, edge_pct=96, size_scale=8, kfac=0.45)

# co-word berwarna rata-rata tahun terbit
d = pd.read_csv(f"{ROOT}/Data/dataset_lolos.csv", encoding="utf-8-sig").fillna("")
SIN = {"llm": "large language model", "llms": "large language model", "large language models": "large language model", "language model": "large language model", "language models": "large language model", "ai": "artificial intelligence"}
BUANG = {"large language model", "artificial intelligence"}
ys = Counter(); ns = Counter()
for s, y in zip(d.keywords, d.year):
    for k in {SIN.get(k.strip().lower(), k.strip().lower()) for k in s.split(";") if k.strip()} - BUANG:
        ys[k] += int(y); ns[k] += 1
yr = {n["id"]: ys[n["id"]] / ns[n["id"]] for n in J["coword"]["nodes"]}
lo, hi = min(yr.values()), max(yr.values())
gambar(cw, [], "", "fig_tren.png", lambda G, n: n, warna_fn=lambda n: yr[n], cbar=("viridis", lo, hi))
