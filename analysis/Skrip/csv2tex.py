"""Tabel LaTeX bergaya template dari CSV hasil analisis tambahan (penulis, sumber, sensitivitas, porsi kata kunci, peta tema).

Keluaran: paper/tables/tabel_H.tex ... tabel_L.tex dan paper/figures/peta_tema.png.
Jalankan setelah kinerja_id.py, sensibilitas_string.py, peta_tema.py: python -I csv2tex.py
"""
import os, shutil, sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texlib import grid_table  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER = os.path.join(os.path.dirname(ROOT), "paper")
H = f"{ROOT}/Hasil"
SRC_A = r"Source: Authors' analysis of OpenAlex data."


def tulis(letter, header, rows, caption, wide=False, source=SRC_A):
    grid_table(f"{PAPER}/tables/tabel_{letter}.tex", f"tab:{letter}", caption, header, [[str(x) for x in r] for r in rows], source=source, wide=wide)


a = pd.read_csv(f"{H}/kinerja_id_penulis.csv").head(10)
tulis("H", ["Rank", "Author (OpenAlex author ID)", "Articles", "Citation"], [(i + 1, r.penulis, r.dokumen, r.sitasi) for i, r in enumerate(a.itertuples())],
      "Top 10 authors, counted by OpenAlex author identifier")
s = pd.read_csv(f"{H}/kinerja_id_sumber.csv").head(10)
tulis("I", ["Rank", "Source (OpenAlex source ID)", "Articles", "Citation"], [(i + 1, r.sumber, r.dokumen, r.sitasi) for i, r in enumerate(s.itertuples())],
      "Top 10 sources, counted by OpenAlex source identifier")
v = pd.read_csv(f"{H}/sensibilitas_string.csv")
ren = {"dasar": "Baseline", "V1": "V1: broader LLM terms (+generative AI, GPT, ChatGPT, foundation model)", "V2": "V2: block C without the stock-market exclusion",
       "V3": "V3: title only instead of title and abstract", "V4": "V4: broader device terms (+TinyML, local LLM, smartphone, mobile device)", "V5": "V5: broader inventory terms (+SKU, stockout, warehouse management)"}
tulis("J", ["Variant", "Unique results", "Final 485 retained", "New outside the cleaned baseline"],
      [(ren[r.varian.split()[0]], r.hasil_unik, r.recall_data_akhir_485.replace(" dari ", " of "), r.paper_baru_di_luar_dasar) for r in v.itertuples()],
      "Sensitivity of the search strings (``new'' includes the 93 records removed in the baseline as duplicates or Zenodo items)")
p = pd.read_csv(f"{H}/perubahan_porsi_kata.csv")
sel = pd.concat([p.head(5), p.tail(5)[::-1]])
tulis("K", ["Keyword", "Articles 2025", "Articles 2026", "Share 2025 (%)", "Share 2026 (%)", "Change (points)"],
      [(r.kata, r.n_2025, r.n_2026, r.porsi_2025_persen, r.porsi_2026_persen, r.selisih_poin) for r in sel.itertuples()],
      "Keywords with the largest falling (first five rows) and rising (last five rows) share of articles, 2025 (n = 151) and 2026 (n = 293)")
t = pd.read_csv(f"{H}/peta_tema.csv")
t = t[t.ambang == 8]
tulis("L", ["Cluster", "Number of keywords", "Centrality", "Density", "Leading keywords"], [(r.kluster, r.kata, r.centrality, r.density, r.kata_teratas) for r in t.itertuples()],
      "Thematic map values for the three co-word clusters (minimum eight occurrences)")
shutil.copy(f"{H}/peta_tema.png", f"{PAPER}/figures/peta_tema.png")
print("tabel H-L dan gambar peta_tema dibuat")
