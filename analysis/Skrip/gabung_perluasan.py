"""Gabungkan hasil penyaringan perluasan (29 Okt 2026) ke dataset.

Masukan : Data/perluasan_baru.csv + hasil penyaringan (ID,label,topik,keyakinan,alasan) di Data/Penyaringan_perluasan/hasil_*.csv
Keluaran: Data/dataset_lolos_540.csv (485 + 'ya', hanya uji kepekaan; dataset_lolos.csv tidak disentuh),
          Data/penyaringan_perluasan.csv (semua 127 + label), Data/daftar_ragu_perluasan.csv (tidak masuk dataset).
Jalankan: python -I gabung_perluasan.py
"""
import csv, glob, os, shutil, sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Data")
rd = lambda p: list(csv.DictReader(open(p, encoding="utf-8-sig")))

lolos_p = os.path.join(DATA, "dataset_lolos_540.csv")  # dataset utama (485) tidak diubah; 540 hanya untuk uji kepekaan
lama = rd(os.path.join(DATA, "dataset_lolos.csv"))
cols = list(lama[0])

hasil = {}
for p in sorted(glob.glob(os.path.join(DATA, "Penyaringan_perluasan", "hasil_*.csv"))):
    for r in rd(p):
        hasil["https://openalex.org/" + r["id"]] = r
baru = rd(os.path.join(DATA, "perluasan_baru.csv"))
assert set(hasil) == {r["id"] for r in baru}, "id hasil tidak cocok dengan perluasan_baru"
assert not ({r["id"] for r in baru} & {r["id"] for r in lama}), "ada id ganda dengan dataset lama"

masuk, semua, ragu = [], [], []
for r in baru:
    h = hasil[r["id"]]
    row = {c: r.get(c, "") for c in cols}
    row.update(label=h["label"], topik_label=h["topik"], alasan=h["alasan"], label_akhir=h["label"],
               keyakinan2=h["keyakinan"], sumber_label="perluasan", sumber_perlu_dicek="")
    semua.append({**row, "asal_pencarian": r["asal_pencarian"]})
    if h["label"] == "ya":
        masuk.append(row)
    elif h["label"] == "ragu":
        ragu.append(row)

def tulis(p, rows, fields):
    with open(p, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

tulis(lolos_p, lama + masuk, cols)
tulis(os.path.join(DATA, "penyaringan_perluasan.csv"), semua, cols + ["asal_pencarian"])
tulis(os.path.join(DATA, "daftar_ragu_perluasan.csv"), ragu, cols)
print("perluasan:", Counter(h["label"] for h in hasil.values()))
print("dataset_lolos:", len(lama), "+", len(masuk), "=", len(lama) + len(masuk))
print("blok tambahan:", Counter(r["blok"] for r in masuk), "| keyakinan 'ya':", Counter(r["keyakinan2"] for r in masuk))
print("tahun:", Counter(r["year"] for r in masuk))
