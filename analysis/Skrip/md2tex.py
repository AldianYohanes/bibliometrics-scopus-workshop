"""Ubah tabel di Hasil/tabel_artikel.md menjadi file LaTeX bergaya template (paper/tables/tabel_X.tex) dan salin gambar ke paper/figures/.

Kolom dipilih dan diberi judul mengikuti template workshop. Jalankan setelah tabel_template.py: python -I md2tex.py
"""
import os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texlib import grid_table  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # analysis/
PAPER = os.path.join(os.path.dirname(ROOT), "paper")
os.makedirs(f"{PAPER}/tables", exist_ok=True)
os.makedirs(f"{PAPER}/figures", exist_ok=True)

WARNA = {"merah": "red", "hijau": "green", "biru": "blue", "kuning": "yellow", "ungu": "purple", "cyan": "cyan", "oranye": "orange"}
# letter: (caption, [(kolom sumber, judul baru)], sumber/keterangan di bawah tabel)
SRC_V = r"Source: Author interpretation based on VOSviewer analysis."
SRC_A = r"Source: Authors' analysis of OpenAlex data."
SPEC = {
    "A": ("Top 10 document citation analysis", [("Peringkat", "Rank"), ("Penulis", "Author"), ("Judul", "Title"), ("Sitasi", "Citation")], SRC_A),
    "B": ("Top 10 documents in the bibliographic coupling analysis", [("Peringkat", "Rank"), ("Publikasi", "Publication"), ("Sitasi", "Citation"), ("TLS", "Total link strength")], SRC_V),
    "C": ("Bibliographic coupling analysis (clusters with at least five documents)", [("Kluster (warna)", "Cluster No and colour"), ("Label kluster", "Cluster label"), ("Jumlah publikasi", "Number of publications"), ("Publikasi representatif", "Representative publication")], SRC_V),
    "D": ("Top 10 documents with the highest co-citation and total link strength", [("Dokumen", "Documents"), ("Sitasi (oleh dokumen kita)", "Citation"), ("TLS", "Total link strength")], SRC_V),
    "E": ("Co-citation clusters on LLM research", [("Kluster (warna)", "Cluster No and colour"), ("Label kluster", "Cluster label"), ("Jumlah artikel", "Number of articles"), ("Publikasi representatif", "Representative publication")], SRC_V),
    "F": ("Top 15 keywords in the co-occurrence of keywords analysis", [("Peringkat", "Rank"), ("Kata kunci", "Keyword"), ("Kemunculan", "Occurrences"), ("TLS", "Total link strength")], SRC_V),
    "G": ("Co-word analysis on LLM research", [("Kluster (warna)", "Cluster No and colour"), ("Label kluster", "Cluster label"), ("Jumlah kata kunci", "Number of keywords"), ("Kata kunci representatif", "Representative keywords")], SRC_V),
}


def cell(s):
    s = s.strip()
    s = re.sub(r"^\{(.*)\}$", r"\1", s).replace("'", "")
    for k, v in WARNA.items():
        s = s.replace(f"({k})", f"({v})")
    return s


def make(letter, rows):
    caption, cols, src = SPEC[letter]
    head = [h.strip() for h in rows[0]]
    idx = [head.index(c) for c, _ in cols]
    body = [[cell(r[i]) for i in idx] for r in rows[2:]]
    # tabel 12 pt harus muat: satu publikasi representatif (C, E) dan lima kata kunci (G)
    for r in body:
        for j, (c_, _) in enumerate(cols):
            if c_ == "Publikasi representatif":
                r[j] = r[j].split("; ")[0]
            if c_ == "Kata kunci representatif":
                r[j] = ", ".join(r[j].split(", ")[:5])
    grid_table(f"{PAPER}/tables/tabel_{letter}.tex", f"tab:{letter}", caption, [n for _, n in cols], body, source=src, wide=letter in "CEG")


lines = open(f"{ROOT}/Hasil/tabel_artikel.md", encoding="utf-8").read().splitlines()
letter, buf, made = None, [], []
for ln in lines + [""]:
    m = re.match(r"^#+ Tabel ([A-G])\.", ln)
    if m:
        letter = m.group(1)
        continue
    if ln.startswith("|") and letter:
        buf.append(ln.strip().strip("|").split("|"))
    elif buf:
        if letter:
            make(letter, buf)
            made.append(letter)
        buf, letter = [], None
print("tabel dibuat:", made)
for f in ["fig_coword.png", "fig_cocitation.png", "fig_tren.png"]:
    shutil.copy(f"{ROOT}/Hasil/{f}", f"{PAPER}/figures/{f}")
print("gambar disalin ke paper/figures")
