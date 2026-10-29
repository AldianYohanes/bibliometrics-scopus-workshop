"""Pembuat tabel LaTeX gaya ADCAIJ (tanpa garis vertikal; garis di atas, di bawah judul kolom, dan di bawah tabel), dipakai md2tex.py dan csv2tex.py."""
import re

SPECIAL = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}


def esc(s):
    return "".join(SPECIAL.get(c, c) for c in str(s).strip())


def grid_table(path, label, caption, header, rows, source=None, wide=False):
    """Tabel tanpa garis vertikal. Kolom yang semuanya angka dipusatkan; kolom teks memakai lebar sisa (Y)."""
    n = len(header)
    num = [all(re.fullmatch(r"-?[\d.,]+", str(r[i]).strip()) for r in rows) for i in range(n)]
    long_ = [max(len(str(r[i])) for r in rows) > 26 for i in range(n)]
    spec = "".join("c" if num[i] else ("Y" if long_[i] else "l") for i in range(n))
    if "Y" not in spec:  # pastikan satu kolom menyerap sisa lebar
        k = max(range(n), key=lambda i: max(len(str(r[i])) for r in rows))
        spec = spec[:k] + "Y" + spec[k + 1:]
    size = r"\footnotesize" if wide else r"\small"
    out = [r"\begin{table}[htbp]", r"\centering", size, rf"\caption{{{caption}}}", rf"\label{{{label}}}",
           rf"\begin{{tabularx}}{{\textwidth}}{{{spec}}}", r"\hline",
           " & ".join(rf"\textbf{{{esc(h)}}}" for h in header) + r" \\ \hline"]
    out += [" & ".join(esc(c) for c in r) + (r" \\ \hline" if i == len(rows) - 1 else r" \\") for i, r in enumerate(rows)]
    out += [r"\end{tabularx}"]
    if source:
        out += [r"\par\vspace{2pt}{\normalsize " + source + "}"]
    out += [r"\end{table}", ""]
    open(path, "w", encoding="utf-8").write("\n".join(out))
