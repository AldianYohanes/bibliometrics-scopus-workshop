"""Gambar terpisah untuk ADCAIJ: TIFF 300 dpi berwarna dan versi hitam-putih, plus berkas keterangan gambar.

Nomor gambar dan keterangan diambil dari paper/main.aux (kompilasi XeLaTeX terakhir), urutan sama dengan naskah.
Keluaran: journal/adcaij/gambar/Figure_N.tif, Figure_N_bw.tif, figure_captions.txt. Jalankan: python -I ekspor_gambar.py
"""
import os, re
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.join(os.path.dirname(os.path.dirname(HERE)), "paper")
OUT = os.path.join(HERE, "gambar")
os.makedirs(OUT, exist_ok=True)
aux = open(os.path.join(PAPER, "main.aux"), encoding="utf-8", errors="replace").read()
label = {k: (int(n), cap) for k, n, cap in re.findall(r"\\newlabel\{(fig:[^}]+)\}\{\{(\d+)\}\{[^}]*\}\{((?:[^{}]|\{[^{}]*\})*)\}", aux)}

src = ""
for f in sorted(os.listdir(os.path.join(PAPER, "sections"))):
    src += open(os.path.join(PAPER, "sections", f), encoding="utf-8").read()
gambar = {}
for blok in re.findall(r"\\begin\{figure\}.*?\\end\{figure\}", src, flags=re.S):
    g = re.search(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", blok).group(1)
    lab = re.search(r"\\label\{([^}]+)\}", blok).group(1)
    gambar[label[lab][0]] = (g, label[lab][1])
assert sorted(gambar) == list(range(1, len(gambar) + 1)), gambar.keys()

baris = []
for n, (g, cap) in sorted(gambar.items()):
    im = Image.open(os.path.join(PAPER, g)).convert("RGB")
    im.save(os.path.join(OUT, f"Figure_{n}.tif"), dpi=(300, 300), compression="tiff_lzw")
    im.convert("L").save(os.path.join(OUT, f"Figure_{n}_bw.tif"), dpi=(300, 300), compression="tiff_lzw")
    lebar_cm = im.width / 300 * 2.54
    baris.append(f"Figure {n}. {cap}")
    print(f"Figure {n}: {g} {im.width}x{im.height} px (lebar {lebar_cm:.1f} cm pada 300 dpi)")
open(os.path.join(OUT, "figure_captions.txt"), "w", encoding="utf-8").write("\n\n".join(baris) + "\n")
