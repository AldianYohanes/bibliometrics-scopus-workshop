"""Lengkapi daftar pustaka paper yang kosong di OpenAlex dengan data Crossref (lewat DOI).

Alur: dataset_lolos.csv (n_refs = 0 dan ada DOI) -> Crossref /works/{doi} -> daftar DOI referensi
-> cocokkan DOI itu ke ID OpenAlex (batch 50) -> Data/referensi_tambahan.csv.
Kunci OpenAlex dibaca dari ~/Tools/openalex.key. Crossref dipanggil tanpa email (kolam publik, lebih lambat).
Jalankan: python -I lengkapi_referensi.py
"""
import csv, json, os, sys, time, urllib.parse, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = open(os.path.expanduser("~/Tools/openalex.key")).read().strip()
UA = {"User-Agent": "bibliometrics-student-project/1.0"}


def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.load(r)
        except Exception as e:  # 404 untuk DOI yang tidak ada di Crossref itu normal
            if "404" in str(e):
                return None
            time.sleep(1.5 * (i + 1))
    return None


def norm_doi(s):
    return s.lower().replace("https://doi.org/", "").replace("http://dx.doi.org/", "").strip()


rows = list(csv.DictReader(open(os.path.join(ROOT, "Data", "dataset_lolos.csv"), encoding="utf-8-sig")))
todo = [r for r in rows if int(r["n_refs"] or 0) == 0 and r["doi"]]
print(f"dokumen lolos: {len(rows)} | tanpa referensi OpenAlex tapi punya DOI: {len(todo)}")

per_doc, all_dois = {}, set()
stat = {"crossref_ada": 0, "crossref_ada_referensi": 0, "total_ref": 0, "ref_ber_doi": 0}
for i, r in enumerate(todo, 1):
    d = norm_doi(r["doi"])
    j = get("https://api.crossref.org/works/" + urllib.parse.quote(d, safe="/"))
    time.sleep(0.15)
    if not j:
        continue
    stat["crossref_ada"] += 1
    refs = (j.get("message") or {}).get("reference") or []
    if refs:
        stat["crossref_ada_referensi"] += 1
    dois = [norm_doi(x["DOI"]) for x in refs if x.get("DOI")]
    stat["total_ref"] += len(refs)
    stat["ref_ber_doi"] += len(dois)
    per_doc[r["id"]] = {"n_total": len(refs), "dois": dois}
    all_dois.update(dois)
    if i % 50 == 0:
        print("  diproses", i, "/", len(todo))
print(stat, "| DOI referensi unik:", len(all_dois))

# DOI -> ID OpenAlex
doi2id, lst = {}, sorted(all_dois)
for i in range(0, len(lst), 50):
    chunk = lst[i:i + 50]
    q = {"filter": "doi:" + "|".join("https://doi.org/" + d for d in chunk), "per-page": 50, "select": "id,doi", "api_key": KEY}
    j = get("https://api.openalex.org/works?" + urllib.parse.urlencode(q))
    for w in (j or {}).get("results", []):
        doi2id[norm_doi(w["doi"])] = w["id"]
    time.sleep(0.1)
print(f"DOI referensi dikenali di OpenAlex: {len(doi2id)} dari {len(lst)}")

out = os.path.join(ROOT, "Data", "referensi_tambahan.csv")
with open(out, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "sumber", "n_ref_crossref_total", "n_ref_dikenali", "referenced_works"])
    gained = 0
    for id_, v in per_doc.items():
        ids = sorted({doi2id[d] for d in v["dois"] if d in doi2id})
        if ids:
            gained += 1
        w.writerow([id_, "crossref", v["n_total"], len(ids), "|".join(ids)])
print(f"dokumen yang mendapat >=1 referensi baru: {gained} dari {len(todo)}")
