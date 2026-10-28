"""Ubah tabel di Hasil/tabel_artikel.md menjadi file LaTeX (paper/tables/tabel_X.tex) dan salin gambar ke paper/figures/.

Jalankan setelah tabel_template.py: python -I md2tex.py
Judul kolom dan keterangan diterjemahkan ke bahasa Inggris (artikel berbahasa Inggris).
"""
import os, re, shutil, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # analysis/
PAPER = os.path.join(os.path.dirname(ROOT), "paper")
os.makedirs(f"{PAPER}/tables", exist_ok=True)
os.makedirs(f"{PAPER}/figures", exist_ok=True)

HEADER = {"Peringkat": "Rank", "Penulis": "Author", "Judul": "Title", "Tahun": "Year", "Sitasi": "Citations", "Publikasi": "Publication",
          "Kluster": "Cluster", "Kluster (warna)": "Cluster (colour)", "Label kluster": "Cluster label", "Jumlah publikasi": "No. of publications",
          "Blok asal": "Source block", "Publikasi representatif": "Representative publications", "Dokumen": "Document",
          "Sitasi (oleh dokumen kita)": "Citations (within dataset)", "Jumlah artikel": "No. of articles", "Kata kunci": "Keyword",
          "Kemunculan": "Occurrences", "Jumlah kata kunci": "No. of keywords", "Kata kunci representatif": "Representative keywords", "TLS": "TLS"}
WARNA = {"merah": "red", "hijau": "green", "biru": "blue", "kuning": "yellow", "ungu": "purple", "cyan": "cyan", "oranye": "orange"}
CAPTION = {
    "A": "Top 10 documents by citations (global OpenAlex citation counts).",
    "B": "Top 10 documents in the bibliographic coupling analysis, ranked by total link strength (TLS).",
    "C": "Summary of bibliographic coupling clusters (clusters with at least five documents).",
    "D": "Top 10 documents by co-citation total link strength (TLS); citations are counted within the dataset.",
    "E": "Co-citation clusters.",
    "F": "Top 15 keywords in the co-occurrence analysis.",
    "G": "Summary of the co-word analysis.",
}
SPECIAL = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}


def esc(s):
    s = s.strip()
    if s == "[BELUM DIBERI NAMA]":
        return r"\todo{to be labelled}"
    s = re.sub(r"^\{(.*)\}$", r"\1", s)  # {'B': 3} -> 'B': 3
    s = s.replace("'", "")
    for k, v in WARNA.items():
        s = s.replace(f"({k})", f"({v})")
    return "".join(SPECIAL.get(c, c) for c in s)


def table(letter, rows):
    head = [HEADER.get(h.strip(), h.strip()) for h in rows[0]]
    body = rows[2:]
    num = [all(re.fullmatch(r"[\d.,]+", r[i].strip()) for r in body) for i in range(len(head))]
    spec = "".join("r" if n else ("l" if max(len(r[i]) for r in body) < 22 else "Y") for i, n in enumerate(num))
    if "Y" not in spec:
        spec = spec[:-1] + "Y"
    out = [r"\begin{table}[htbp]", r"\centering", r"\small", rf"\caption{{{CAPTION[letter]}}}", rf"\label{{tab:{letter}}}",
           rf"\begin{{tabularx}}{{\textwidth}}{{{spec}}}", r"\toprule", " & ".join(rf"\textbf{{{esc(h)}}}" for h in head) + r" \\", r"\midrule"]
    out += [" & ".join(esc(c) for c in r) + r" \\" for r in body]
    out += [r"\bottomrule", r"\end{tabularx}", r"\end{table}", ""]
    open(f"{PAPER}/tables/tabel_{letter}.tex", "w", encoding="utf-8").write("\n".join(out))


lines = open(f"{ROOT}/Hasil/tabel_artikel.md", encoding="utf-8").read().splitlines()
letter, buf, made = None, [], []
for ln in lines + [""]:
    m = re.match(r"^#+ Tabel ([A-G])\.", ln)
    if m:
        letter = m.group(1)
        continue
    if ln.startswith("|") and letter:
        buf.append([c for c in ln.strip().strip("|").split("|")])
    elif buf:
        if letter:
            table(letter, buf)
            made.append(letter)
        buf, letter = [], None
print("tabel dibuat:", made)
for f in ["gambar1_tren_publikasi.png", "peta_coword.png", "peta_cocitation.png", "peta_tren.png", "peta_kolaborasi_negara.png"]:
    shutil.copy(f"{ROOT}/Hasil/{f}", f"{PAPER}/figures/{f}")
print("gambar disalin ke paper/figures")
