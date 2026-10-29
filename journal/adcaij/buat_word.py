"""Buat versi Word naskah untuk ADCAIJ dari LaTeX (paper/main.tex) dengan pandoc.

- Acuan gaya: template resmi ADCAIJ_Template_2026_V6.dotx, diubah jadi reference.docx (ukuran halaman, margin, gaya heading/body/caption).
- Sitasi: biblatex -> citeproc dengan apa.csl (APA 7, dari repositori Citation Style Language).
- Keluaran: journal/adcaij/naskah_adcaij.docx. Tata letak halaman pertama (logo, kotak abstrak/kata kunci) tetap dirapikan manual di template resmi.
Jalankan: python -I buat_word.py   (butuh pandoc 3.x di C:\\Program Files\\Pandoc)
"""
import os, re, shutil, subprocess, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.join(os.path.dirname(os.path.dirname(HERE)), "paper")
PANDOC = shutil.which("pandoc") or r"C:\Program Files\Pandoc\pandoc.exe"
DOTX = os.path.join(HERE, "template", "ADCAIJ_template", "ADCAIJ_Template_2026_V6.dotx")
REF = os.path.join(HERE, "reference.docx")
OUT = os.path.join(HERE, "naskah_adcaij.docx")

# .dotx -> .docx: hanya tipe konten dokumen utama yang berbeda
with zipfile.ZipFile(DOTX) as zin, zipfile.ZipFile(REF, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "[Content_Types].xml":
            data = data.replace(b"wordprocessingml.template.main+xml", b"wordprocessingml.document.main+xml")
        zout.writestr(item, data)

# Gabung \input jadi satu berkas dan ganti \ref dengan nomor dari main.aux (kompilasi XeLaTeX terakhir),
# supaya nomor tabel/gambar di Word sama dengan PDF. Pandoc sendiri tidak memberi nomor pada keterangan dari LaTeX.
aux = open(os.path.join(PAPER, "main.aux"), encoding="utf-8", errors="replace").read()
NOMOR = dict(re.findall(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}", aux))


def gabung(path):
    s = open(path, encoding="utf-8").read()
    return re.sub(r"\\input\{([^}]+)\}", lambda m: gabung(os.path.join(PAPER, m.group(1) if m.group(1).endswith(".tex") else m.group(1) + ".tex")), s)


def beri_nomor(m):
    blok, jenis = m.group(0), ("Table" if m.group(1) == "table" else "Figure")
    lab = re.search(r"\\label\{([^}]+)\}", blok)
    if not lab:
        return blok
    return blok.replace(r"\caption{", r"\caption{" + f"{jenis} {NOMOR[lab.group(1)]}. ", 1)


src = gabung(os.path.join(PAPER, "main.tex"))
src = re.sub(r"\\begin\{(table|figure)\}.*?\\end\{\1\}", beri_nomor, src, flags=re.S)
src = re.sub(r"\\ref\{([^}]+)\}", lambda m: NOMOR[m.group(1)], src)
# pandoc tidak mengenal kolom buatan "Y" di tabularx: ubah ke tabular biasa (lebar kolom diatur Word)
src = re.sub(r"\\begin\{tabularx\}\{\\textwidth\}\{((?:[^{}]|\{[^{}]*\})*)\}",
             lambda m: r"\begin{tabular}{" + re.sub(r"p\{[^}]*\}", "l", m.group(1)).replace("Y", "l").replace("X", "l") + "}", src)
src = src.replace(r"\end{tabularx}", r"\end{tabular}")
assert "\\input{" not in src and "\\ref{" not in src
TMP = os.path.join(PAPER, "_naskah_word.tex")
open(TMP, "w", encoding="utf-8").write(src)

cmd = [PANDOC, "_naskah_word.tex", "-f", "latex", "-t", "docx", "-o", OUT,
       "--reference-doc", REF, "--citeproc", "--csl", os.path.join(HERE, "apa.csl"),
       "--bibliography", "refs.bib", "--bibliography", "refs_tambahan.bib",
       "--resource-path", ".", "--number-sections", "--metadata", "link-citations=false"]
r = subprocess.run(cmd, cwd=PAPER, capture_output=True, text=True, encoding="utf-8", errors="replace")
os.remove(TMP)
print(r.stderr.strip()[-3000:] or "pandoc: tanpa peringatan")
if r.returncode:
    sys.exit(r.returncode)
print("dibuat:", OUT, round(os.path.getsize(OUT) / 1e6, 2), "MB")
