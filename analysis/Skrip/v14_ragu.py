"""Periksa hasil tahap 1 penyaringan V1/V4 dan siapkan berkas rekaman 'ragu' untuk tahap 2.

Masukan : Data/perluasan_v14.csv, Data/Penyaringan_v14/hasil_{1..8}.csv
Keluaran: Data/Penyaringan_v14/ragu_{1..3}.md (abstrak lebih panjang). Jalankan: python -I v14_ragu.py
"""
import csv, glob, os, sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Data")
OUT = os.path.join(DATA, "Penyaringan_v14")
rec = {r["id"].rsplit("/", 1)[-1]: r for r in csv.DictReader(open(os.path.join(DATA, "perluasan_v14.csv"), encoding="utf-8-sig"))}
hasil = []
for p in sorted(glob.glob(os.path.join(OUT, "hasil_[0-9].csv"))):
    hasil += list(csv.DictReader(open(p, encoding="utf-8-sig")))
ids = [h["id"].strip() for h in hasil]
assert len(ids) == len(set(ids)) == len(rec) and set(ids) == set(rec), (len(ids), len(set(ids)), len(rec), set(rec) - set(ids))
assert {h["label"] for h in hasil} <= {"ya", "tidak", "ragu"}, Counter(h["label"] for h in hasil)
print("tahap 1:", Counter(h["label"] for h in hasil))
ragu = [h["id"].strip() for h in hasil if h["label"] == "ragu"]
n = 3
for i in range(n):
    with open(os.path.join(OUT, f"ragu_{i + 1}.md"), "w", encoding="utf-8") as f:
        for k in ragu[i::n]:
            r = rec[k]
            f.write(f"### {k}\nTitle: {r['title']}\nKeywords: {r['keywords']}\nTopics: {r['topics']}\n"
                    f"Abstract: {(r['abstract'] or '(no abstract)')[:3500]}\n\n")
print(len(ragu), "ragu ->", n, "berkas")
