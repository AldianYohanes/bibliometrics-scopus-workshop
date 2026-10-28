"""Kinerja penulis, sumber, institusi, negara memakai ID OpenAlex (bukan nama), supaya nama ganda tidak menggandakan penghitungan.

Langkah 1 (sekali, butuh data mentah): python -I kinerja_id.py <folder_raw_json>   -> membuat Data/autor_sumber.csv
Langkah 2 (selanjutnya):               python -I kinerja_id.py                     -> tabel di Hasil/kinerja_id_*.csv
Hanya dokumen di Data/dataset_lolos.csv yang dihitung.
"""
import csv, glob, json, os, sys
from collections import Counter, defaultdict

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = f"{ROOT}/Data/autor_sumber.csv"
lolos = set(pd.read_csv(f"{ROOT}/Data/dataset_lolos.csv", encoding="utf-8-sig").id)

if len(sys.argv) > 1:
    seen, rows = set(), []
    for f in sorted(glob.glob(os.path.join(sys.argv[1], "raw_blok_*.json"))):
        for w in json.load(open(f, encoding="utf-8")):
            if w["id"] not in lolos or w["id"] in seen:
                continue
            seen.add(w["id"])
            src = (w.get("primary_location") or {}).get("source") or {}
            auts = w.get("authorships") or []
            rows.append({"id": w["id"], "cited_by": w.get("cited_by_count") or 0, "year": w.get("publication_year"),
                         "source_id": src.get("id") or "", "source": src.get("display_name") or "", "issn_l": src.get("issn_l") or "",
                         "authors": json.dumps([[(a.get("author") or {}).get("id") or "", (a.get("author") or {}).get("display_name") or ""] for a in auts], ensure_ascii=False),
                         "institutions": json.dumps(sorted({(i.get("id") or "", i.get("display_name") or "", i.get("country_code") or "") for a in auts for i in (a.get("institutions") or [])}), ensure_ascii=False),
                         "countries": "; ".join(sorted({c for a in auts for c in (a.get("countries") or [])}))})
    with open(CSV, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    print("autor_sumber.csv:", len(rows), "dokumen")

d = pd.read_csv(CSV, encoding="utf-8-sig").fillna("")
H = f"{ROOT}/Hasil"
doc_cit = dict(zip(d.id, d.cited_by))

# penulis (ID)
a_docs, a_name = defaultdict(set), {}
for r in d.itertuples():
    for aid, name in json.loads(r.authors):
        if aid:
            a_docs[aid].add(r.id); a_name[aid] = name
names = [n for r in d.itertuples() for _, n in json.loads(r.authors)]
print(f"penulis: {len(a_docs)} ID unik vs {len(set(names))} nama unik (selisih {len(set(names)) - len(a_docs)})")
rows = sorted(({"penulis": a_name[a], "id": a.split("/")[-1], "dokumen": len(s), "sitasi": sum(doc_cit[i] for i in s)} for a, s in a_docs.items()), key=lambda x: (-x["dokumen"], -x["sitasi"]))
pd.DataFrame(rows[:15]).to_csv(f"{H}/kinerja_id_penulis.csv", index=False, encoding="utf-8-sig")
print("penulis dengan >=3 dokumen:", sum(1 for r in rows if r["dokumen"] >= 3), "| >=2:", sum(1 for r in rows if r["dokumen"] >= 2), "| teratas:", [(r["penulis"], r["dokumen"]) for r in rows[:5]])

# sumber (ID)
s_docs, s_name = defaultdict(set), {}
for r in d.itertuples():
    if r.source_id:
        s_docs[r.source_id].add(r.id); s_name[r.source_id] = r.source
rows = sorted(({"sumber": s_name[s], "id": s.split("/")[-1], "dokumen": len(v), "sitasi": sum(doc_cit[i] for i in v)} for s, v in s_docs.items()), key=lambda x: (-x["dokumen"], -x["sitasi"]))
pd.DataFrame(rows[:15]).to_csv(f"{H}/kinerja_id_sumber.csv", index=False, encoding="utf-8-sig")
print("sumber unik:", len(s_docs), "| tanpa sumber:", int((d.source_id == '').sum()), "| teratas:", [(r["sumber"][:40], r["dokumen"]) for r in rows[:4]])

# institusi (ID)
i_docs, i_name, i_cty = defaultdict(set), {}, {}
for r in d.itertuples():
    for iid, name, cty in json.loads(r.institutions):
        if iid:
            i_docs[iid].add(r.id); i_name[iid] = name; i_cty[iid] = cty
rows = sorted(({"institusi": i_name[i], "negara": i_cty[i], "dokumen": len(s), "sitasi": sum(doc_cit[x] for x in s)} for i, s in i_docs.items()), key=lambda x: (-x["dokumen"], -x["sitasi"]))
pd.DataFrame(rows[:15]).to_csv(f"{H}/kinerja_id_institusi.csv", index=False, encoding="utf-8-sig")
print("institusi unik:", len(i_docs), "| tanpa institusi:", int((d.institutions == '[]').sum()), "| teratas:", [(r["institusi"][:35], r["dokumen"]) for r in rows[:4]])

# negara
c = Counter(x for s in d.countries for x in s.split("; ") if x)
pd.DataFrame(c.most_common(15), columns=["negara", "dokumen"]).to_csv(f"{H}/kinerja_id_negara.csv", index=False, encoding="utf-8-sig")
print("dokumen tanpa data negara:", int((d.countries == "").sum()), "| teratas:", c.most_common(5))
