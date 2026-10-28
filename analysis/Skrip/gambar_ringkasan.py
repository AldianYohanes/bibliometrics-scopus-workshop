"""Gambar 1 bergaya template (ringkasan publikasi dan sitasi): jumlah publikasi, total sitasi, rata-rata per artikel, h-index, dan publikasi per tahun.

Sitasi = hitungan global OpenAlex untuk artikel di dataset. h-index = h terbesar sehingga ada h artikel dengan minimal h sitasi.
Keluaran: paper/figures/gambar1_ringkasan.png dan Hasil/ringkasan_sitasi.csv. Jalankan: python -I gambar_ringkasan.py
"""
import os, sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER = os.path.join(os.path.dirname(ROOT), "paper")
d = pd.read_csv(f"{ROOT}/Data/dataset_lolos.csv", encoding="utf-8-sig")
c = sorted(d.cited_by.astype(int), reverse=True)
h = max(i + 1 for i, x in enumerate(c) if x >= i + 1)
tot, n = sum(c), len(c)
sem = d.groupby("year").agg(dokumen=("id", "size"), sitasi=("cited_by", "sum"))
pd.DataFrame({"publikasi": [n], "total_sitasi": [tot], "rata_rata_per_artikel": [round(tot / n, 2)], "h_index": [h]}).to_csv(f"{ROOT}/Hasil/ringkasan_sitasi.csv", index=False)
print(f"publikasi {n} | total sitasi {tot} | rata-rata {tot/n:.2f} | h-index {h}")

fig = plt.figure(figsize=(10, 4.6))
tiles = [("Publications", f"{n:,}", "total"), ("Times cited", f"{tot:,}", "total"), ("Average citations", f"{tot/n:.2f}", "per article"), ("h-index", f"{h}", "of the dataset")]
for i, (t, v, s) in enumerate(tiles):
    ax = fig.add_axes([0.02 + i * 0.245, 0.62, 0.225, 0.33]); ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, fill=False, ec="#999999", lw=1, transform=ax.transAxes))
    ax.text(0.06, 0.78, t, fontsize=11, transform=ax.transAxes)
    ax.text(0.06, 0.38, v, fontsize=22, transform=ax.transAxes)
    ax.text(0.06, 0.12, s, fontsize=9, color="#555555", transform=ax.transAxes)
ax = fig.add_axes([0.08, 0.12, 0.84, 0.38])
ax.bar(sem.index.astype(str), sem.dokumen, color="#2b8cbe")
for x, y in zip(sem.index.astype(str), sem.dokumen):
    ax.text(x, y, str(y), ha="center", va="bottom", fontsize=8)
ax.set_ylabel("Publications")
ax2 = ax.twinx(); ax2.plot(sem.index.astype(str), sem.sitasi, color="#e6550d", marker="o"); ax2.set_ylabel("Citations")
ax.set_title("Publications and citations per year (2026 is incomplete)", fontsize=9)
fig.savefig(f"{PAPER}/figures/gambar1_ringkasan.png", dpi=150); plt.close(fig)
