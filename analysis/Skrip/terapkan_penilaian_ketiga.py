"""Terapkan penilaian ketiga (Data/penilaian_ketiga.csv) ke data penyaringan.

- 72 rekaman yang dikeluarkan putaran kedua: yang dinilai 'ya' masuk dataset utama (Data/dataset_lolos.csv).
- 14 paper perluasan berkeyakinan rendah: yang dinilai 'tidak' diubah labelnya di Data/penyaringan_perluasan.csv.
Label lama tetap ada di kolom label/label2; label_akhir dan sumber_label diperbarui ('pass3').
Jalankan: python -I terapkan_penilaian_ketiga.py
"""
import csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "Data")


def baca(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


def tulis(p, kolom, rows):
    with open(p, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=kolom)
        w.writeheader()
        w.writerows(rows)


nilai = {x["id"]: x for x in csv.DictReader(open(os.path.join(D, "penilaian_ketiga.csv"), encoding="utf-8"))}

kol, gab = baca(os.path.join(D, "penyaringan_gabungan.csv"))
ubah = 0
for r in gab:
    v = nilai.get(r["id"])
    if v and v["asal"] == "72":
        assert r["label2"] == "tidak", r["id"]
        r["label_akhir"], r["sumber_label"] = v["label3"], "pass3"
        ubah += 1
assert ubah == 72, ubah
tulis(os.path.join(D, "penyaringan_gabungan.csv"), kol, gab)

kol_l, lama = baca(os.path.join(D, "dataset_lolos.csv"))
ada = {r["id"] for r in lama}
baru = [r for r in gab if r["sumber_label"] == "pass3" and r["label_akhir"] == "ya" and r["id"] not in ada]
lolos = lama + [{k: r.get(k, "") for k in kol_l} for r in baru]
assert len(lolos) == len({r["id"] for r in lolos})
assert len(lolos) == sum(1 for r in gab if r["label_akhir"] == "ya"), "dataset_lolos harus sama dengan label_akhir ya"
tulis(os.path.join(D, "dataset_lolos.csv"), kol_l, lolos)

kol_p, per = baca(os.path.join(D, "penyaringan_perluasan.csv"))
ubah_p = 0
for r in per:
    v = nilai.get(r["id"])
    if v and v["asal"] == "55":
        assert r["label"] == "ya", r["id"]
        r["label_akhir"], r["sumber_label"] = v["label3"], "pass3"
        ubah_p += 1
assert ubah_p == 14, ubah_p
tulis(os.path.join(D, "penyaringan_perluasan.csv"), kol_p, per)

print("dataset_lolos:", len(lama), "+", len(baru), "=", len(lolos))

# Data uji perluasan (hanya uji kepekaan): dataset utama + paper perluasan yang tetap 'ya'
masuk = [{k: r.get(k, "") for k in kol_l} for r in per if r["label_akhir"] == "ya"]
uji = lolos + masuk
n = len(uji)
tulis(os.path.join(D, f"dataset_lolos_{n}.csv"), kol_l, uji)
ids = {r["id"] for r in uji}
# penulis/sumber dan referensi Crossref: gabung file utama dengan file uji sebelumnya (dari gabung_perluasan.py), saring ke dataset uji
for nama in ["autor_sumber", "referensi_tambahan"]:
    rows, kol_x, seen = [], None, set()
    for p in [os.path.join(D, f"{nama}.csv"), os.path.join(D, f"{nama}_540.csv")]:
        k, rr = baca(p)
        kol_x = kol_x or k
        for r in rr:
            if r["id"] in ids and r["id"] not in seen:
                seen.add(r["id"]); rows.append(r)
    tulis(os.path.join(D, f"{nama}_{n}.csv"), kol_x, rows)
    print(f"{nama}_{n}.csv:", len(rows))
print("perluasan ya:", len(masuk), "| dataset uji:", n)
