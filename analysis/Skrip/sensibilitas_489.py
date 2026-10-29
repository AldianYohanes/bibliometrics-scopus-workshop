"""Perbarui kolom recall di Hasil/sensibilitas_string.csv dari 485 ke dataset utama sekarang (489), tanpa mengulang pencarian.

Pencarian 28 Okt tidak diulang supaya tanggal data tetap sama. Dasarnya:
- varian yang irisannya dengan hasil dasar = 708 menangkap semua rekaman dasar, jadi juga 4 paper tambahan (semuanya dari 708);
- untuk V3 (hanya judul), query OpenAlex 29 Okt yang dibatasi ke 4 ID itu tidak menangkap satu pun, jadi recall tetap 61.
Jalankan: python -I sensibilitas_489.py, lalu python -I csv2tex.py
"""
import os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = f"{ROOT}/Hasil/sensibilitas_string.csv"
v = pd.read_csv(H, encoding="utf-8-sig")
n = len(pd.read_csv(f"{ROOT}/Data/dataset_lolos.csv", encoding="utf-8-sig"))
lama = "recall_data_akhir_485" if "recall_data_akhir_485" in v else "recall_data_akhir"
TAMBAH_V3 = 0  # dari 4 paper tambahan yang tertangkap V3 (cek 29 Okt)
out = []
for r in v.itertuples():
    k = int(getattr(r, lama).split()[0])
    if r.irisan_dengan_dasar_708 == 708:
        k = n
    elif r.varian.startswith("V3"):
        k = 61 + TAMBAH_V3
    out.append(f"{k} dari {n} ({100 * k / n:.0f}%)")
v = v.drop(columns=[lama])
v.insert(2, "recall_data_akhir", out)
v.to_csv(H, index=False, encoding="utf-8-sig")
print(v[["varian", "recall_data_akhir"]].to_string())
