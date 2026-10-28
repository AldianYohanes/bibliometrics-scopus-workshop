"""Tabel LaTeX dari CSV hasil analisis tambahan (penulis, sumber, sensitivitas string, porsi kata kunci, peta tema).

Keluaran: paper/tables/tabel_H.tex ... tabel_L.tex dan paper/figures/peta_tema.png.
Jalankan setelah kinerja_id.py, sensibilitas_string.py, peta_tema.py: python -I csv2tex.py
"""
import os, re, shutil, sys

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER = os.path.join(os.path.dirname(ROOT), "paper")
H = f"{ROOT}/Hasil"
SPECIAL = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}


def esc(s):
    return "".join(SPECIAL.get(c, c) for c in str(s))


def tulis(letter, df, caption, label_cols=None):
    """df sudah berisi judul kolom bahasa Inggris."""
    num = [bool(re.fullmatch(r"-?[\d.,]+", str(df.iloc[:, i].astype(str).iloc[0]).strip())) and df.iloc[:, i].astype(str).str.fullmatch(r"-?[\d.,]+").all() for i in range(df.shape[1])]
    spec = "".join("r" if n else ("Y" if df.iloc[:, i].astype(str).str.len().max() > 24 else "l") for i, n in enumerate(num))
    if "Y" not in spec:
        spec = "Y" + spec[1:]
    out = [r"\begin{table}[htbp]", r"\centering", r"\small", rf"\caption{{{caption}}}", rf"\label{{tab:{letter}}}", rf"\begin{{tabularx}}{{\textwidth}}{{{spec}}}", r"\toprule",
           " & ".join(rf"\textbf{{{esc(c)}}}" for c in df.columns) + r" \\", r"\midrule"]
    out += [" & ".join(esc(x) for x in row) + r" \\" for row in df.itertuples(index=False)]
    out += [r"\bottomrule", r"\end{tabularx}", r"\end{table}", ""]
    open(f"{PAPER}/tables/tabel_{letter}.tex", "w", encoding="utf-8").write("\n".join(out))


a = pd.read_csv(f"{H}/kinerja_id_penulis.csv").head(10)
tulis("H", pd.DataFrame({"Rank": range(1, 11), "Author (OpenAlex author ID)": a.penulis, "Articles": a.dokumen, "Citations": a.sitasi}),
      "Most productive authors, counted by OpenAlex author ID (so that name variants are not counted twice); citations are global OpenAlex counts of the authors' articles in the dataset.")
s = pd.read_csv(f"{H}/kinerja_id_sumber.csv").head(10)
tulis("I", pd.DataFrame({"Rank": range(1, 11), "Source (OpenAlex source ID)": s.sumber, "Articles": s.dokumen, "Citations": s.sitasi}),
      "Most frequent sources, counted by OpenAlex source ID.")
v = pd.read_csv(f"{H}/sensibilitas_string.csv")
ren = {"dasar": "Baseline", "V1": "V1: broader LLM terms (+generative AI, GPT, ChatGPT, foundation model)", "V2": "V2: block C without the stock-market exclusion",
       "V3": "V3: title only instead of title and abstract", "V4": "V4: broader device terms (+TinyML, local LLM, smartphone, mobile device)", "V5": "V5: broader inventory terms (+SKU, stockout, warehouse management)"}
v["Variant"] = [ren[k.split()[0]] for k in v.varian]
v["recall"] = v.recall_data_akhir_485.str.replace(" dari ", " of ")
tulis("J", pd.DataFrame({"Variant": v.Variant, "Unique results": v.hasil_unik, "Final 485 retained": v.recall, "New outside the cleaned baseline": v.paper_baru_di_luar_dasar}),
      "Sensitivity of the search strings. ``New'' counts records not in the cleaned baseline of 708 (it includes the 93 records that were removed as duplicates or Zenodo items in the baseline run).")
p = pd.read_csv(f"{H}/perubahan_porsi_kata.csv")
sel = pd.concat([p.head(5), p.tail(5)[::-1]])
tulis("K", pd.DataFrame({"Keyword": sel.kata, "Articles 2025 (n=151)": sel.n_2025, "Articles 2026 (n=293)": sel.n_2026, "Share 2025 (%)": sel.porsi_2025_persen, "Share 2026 (%)": sel.porsi_2026_persen, "Change (points)": sel.selisih_poin}),
      "Keywords with the largest falling (first five rows) and rising (last five rows) share of articles between 2025 and 2026 (keywords with at least eight occurrences). 2026 is a partial year.")
t = pd.read_csv(f"{H}/peta_tema.csv")
t = t[t.ambang == 8]
tulis("L", pd.DataFrame({"Cluster": t.kluster, "Keywords": t.kata, "Centrality": t.centrality, "Density": t.density, "Leading keywords": t.kata_teratas}),
      "Thematic map values for the three co-word clusters (minimum eight occurrences): centrality is the weight of links to other clusters; density is 100 times the internal link weight per keyword.")
shutil.copy(f"{H}/peta_tema.png", f"{PAPER}/figures/peta_tema.png")
print("tabel H-L dan gambar peta_tema dibuat")
