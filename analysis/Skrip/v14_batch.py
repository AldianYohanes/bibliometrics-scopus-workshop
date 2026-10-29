"""Pecah Data/perluasan_v14.csv jadi 8 berkas batch untuk penyaringan judul+abstrak (tahap 1).

Hasil: Data/Penyaringan_v14/batch_{1..8}.md. Hasil penyaringan ditulis penyaring ke hasil_{1..8}.csv
(kolom id,label,topik,keyakinan,alasan; sama dengan Penyaringan_perluasan). Jalankan: python -I v14_batch.py
"""
import csv, os, sys
sys.stdout.reconfigure(encoding="utf-8")
DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Data")
OUT = os.path.join(DATA, "Penyaringan_v14")
os.makedirs(OUT, exist_ok=True)
rows = list(csv.DictReader(open(os.path.join(DATA, "perluasan_v14.csv"), encoding="utf-8-sig")))
n = 8
for i in range(n):
    with open(os.path.join(OUT, f"batch_{i + 1}.md"), "w", encoding="utf-8") as f:
        for r in rows[i::n]:
            f.write(f"### {r['id'].rsplit('/', 1)[-1]}\nTitle: {r['title']}\nKeywords: {r['keywords']}\n"
                    f"Abstract: {(r['abstract'] or '(no abstract)')[:1500]}\n\n")
print(len(rows), "rekaman ->", n, "batch")
