"""Potong tepi putih lalu perkecil ekspor VOSviewer beresolusi penuh (4284 x 2854) ke 3000 px lebar untuk naskah (paper/figures).

Masukan: analysis/Hasil/vos_full/vos_*.png (dari vos_export.ps1, tidak ikut git). Keluaran: paper/figures/vos_*.png. Jalankan: python -I redimensi_vos.py
"""
import glob, os, sys
from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(os.path.dirname(ROOT), "paper", "figures")
for f in sorted(glob.glob(f"{ROOT}/Hasil/vos_full/vos_*.png")):
    im = Image.open(f).convert("RGB")
    bbox = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).getbbox()  # buang tepi putih
    if bbox:
        m = 40
        im = im.crop((max(bbox[0] - m, 0), max(bbox[1] - m, 0), min(bbox[2] + m, im.width), min(bbox[3] + m, im.height)))
    im = im.resize((3000, round(im.height * 3000 / im.width)), Image.LANCZOS)
    out = os.path.join(FIG, os.path.basename(f))
    im.save(out, optimize=True)
    print(os.path.basename(f), im.size, f"{os.path.getsize(out)/1e6:.1f} MB")
