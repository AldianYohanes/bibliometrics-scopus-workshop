"""Gabungkan hasil penyaringan V1/V4 (tahap 1 Haiku + tahap 2 Sonnet untuk yang ragu) menjadi data uji kepekaan.

Masukan : Data/perluasan_v14.csv, Data/Penyaringan_v14/hasil_{1..8}.csv, hasil_ragu_{1..3}.csv
Keluaran: Data/penyaringan_v14.csv (711 + label), Data/dataset_lolos_<N>.csv (489 + 'ya'),
          Data/autor_sumber_<N>.csv, Data/referensi_tambahan_<N>.csv (Crossref untuk yang tanpa referensi).
Dataset utama (dataset_lolos.csv) tidak disentuh. Jalankan: python -I v14_gabung.py
"""
import csv, glob, json, os, sys, time, urllib.parse, urllib.request
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Data")
P = os.path.join(DATA, "Penyaringan_v14")
KEY = open(os.path.expanduser("~/Tools/openalex.key")).read().strip()
UA = {"User-Agent": "bibliometrics-student-project/1.0"}


def baca(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


def tulis(p, kolom, rows):
    with open(p, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=kolom)
        w.writeheader(); w.writerows(rows)


def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return json.load(r)
        except Exception as e:  # 404 dari Crossref berarti DOI tidak terdaftar
            if "404" in str(e):
                return None
            time.sleep(2 * (i + 1))
    return None


norm_doi = lambda s: s.lower().replace("https://doi.org/", "").replace("http://dx.doi.org/", "").strip()

_, rec = baca(os.path.join(DATA, "perluasan_v14.csv"))
h1 = {r["id"].strip(): r for p in sorted(glob.glob(os.path.join(P, "hasil_[0-9].csv"))) for r in baca(p)[1]}
h2 = {r["id"].strip(): r for p in sorted(glob.glob(os.path.join(P, "hasil_ragu_*.csv"))) for r in baca(p)[1]}
ragu1 = {k for k, v in h1.items() if v["label"] == "ragu"}
assert set(h2) == ragu1, (len(h2), len(ragu1), ragu1 ^ set(h2))

kol_l, lolos = baca(os.path.join(DATA, "dataset_lolos.csv"))
semua, masuk = [], []
for r in rec:
    k = r["id"].rsplit("/", 1)[-1]
    a, b = h1[k], h2.get(k)
    akhir = b or a
    row = {c: r.get(c, "") for c in kol_l}
    row.update(label=a["label"], topik_label=a["topik"], alasan=a["alasan"],
               label2=b["label"] if b else "", topik2=b["topik"] if b else "", keyakinan2=akhir["keyakinan"],
               alasan2=b["alasan"] if b else "", label_akhir=akhir["label"],
               sumber_label="v14_pass2" if b else "v14_pass1", sumber_perlu_dicek="")
    semua.append({**row, "asal_pencarian": r["asal_pencarian"]})
    if akhir["label"] == "ya":
        masuk.append(row)
tulis(os.path.join(DATA, "penyaringan_v14.csv"), kol_l + ["asal_pencarian"], semua)
uji = lolos + masuk
assert len(uji) == len({r["id"] for r in uji})
n = len(uji)
tulis(os.path.join(DATA, f"dataset_lolos_{n}.csv"), kol_l, uji)
print("tahap 1:", Counter(v["label"] for v in h1.values()), "| tahap 2:", Counter(v["label"] for v in h2.values()),
      "| tahap 2 keyakinan:", Counter(v["keyakinan"] for v in h2.values()))
print("akhir:", Counter(r["label_akhir"] for r in semua), "| masuk:", len(masuk), "| dataset uji:", n)
print("asal yang masuk:", Counter(r["asal_pencarian"] for r in semua if r["label_akhir"] == "ya"))

# penulis/sumber untuk rekaman baru (kolom sama dengan kinerja_id.py langkah 1)
ids = [r["id"].rsplit("/", 1)[-1] for r in masuk]
raw = []
for i in range(0, len(ids), 50):
    q = {"filter": "openalex:" + "|".join(ids[i:i + 50]), "per-page": 50, "api_key": KEY,
         "select": "id,cited_by_count,publication_year,primary_location,authorships"}
    raw += get("https://api.openalex.org/works?" + urllib.parse.urlencode(q))["results"]
assert len(raw) == len(ids), (len(raw), len(ids))
kol_a, aut = baca(os.path.join(DATA, "autor_sumber.csv"))
for w in raw:
    src = (w.get("primary_location") or {}).get("source") or {}
    auts = w.get("authorships") or []
    aut.append({"id": w["id"], "cited_by": w.get("cited_by_count") or 0, "year": w.get("publication_year"),
                "source_id": src.get("id") or "", "source": src.get("display_name") or "", "issn_l": src.get("issn_l") or "",
                "authors": json.dumps([[(a.get("author") or {}).get("id") or "", (a.get("author") or {}).get("display_name") or ""] for a in auts], ensure_ascii=False),
                "institutions": json.dumps(sorted({(i.get("id") or "", i.get("display_name") or "", i.get("country_code") or "") for a in auts for i in (a.get("institutions") or [])}), ensure_ascii=False),
                "countries": "; ".join(sorted({c for a in auts for c in (a.get("countries") or [])}))})
tulis(os.path.join(DATA, f"autor_sumber_{n}.csv"), kol_a, aut)

# referensi Crossref untuk rekaman baru tanpa daftar referensi di OpenAlex (logika sama dengan lengkapi_referensi.py)
todo = [r for r in masuk if int(r["n_refs"] or 0) == 0 and r["doi"]]
per_doc, all_dois = {}, set()
for r in todo:
    j = get("https://api.crossref.org/works/" + urllib.parse.quote(norm_doi(r["doi"]), safe="/"))
    time.sleep(0.15)
    if not j:
        continue
    refs = (j.get("message") or {}).get("reference") or []
    dois = [norm_doi(x["DOI"]) for x in refs if x.get("DOI")]
    per_doc[r["id"]] = {"n_total": len(refs), "dois": dois}
    all_dois.update(dois)
doi2id, lst = {}, sorted(all_dois)
for i in range(0, len(lst), 50):
    q = {"filter": "doi:" + "|".join("https://doi.org/" + d for d in lst[i:i + 50]), "per-page": 50, "select": "id,doi", "api_key": KEY}
    for w in (get("https://api.openalex.org/works?" + urllib.parse.urlencode(q)) or {}).get("results", []):
        doi2id[norm_doi(w["doi"])] = w["id"]
kol_r, ref = baca(os.path.join(DATA, "referensi_tambahan.csv"))
dapat = 0
for id_, v in per_doc.items():
    got = sorted({doi2id[d] for d in v["dois"] if d in doi2id})
    dapat += bool(got)
    ref.append({"id": id_, "sumber": "crossref", "n_ref_crossref_total": v["n_total"], "n_ref_dikenali": len(got), "referenced_works": "|".join(got)})
tulis(os.path.join(DATA, f"referensi_tambahan_{n}.csv"), kol_r, ref)
print(f"tanpa referensi OpenAlex: {len(todo)} | dapat dari Crossref: {dapat} | N = {n}")
