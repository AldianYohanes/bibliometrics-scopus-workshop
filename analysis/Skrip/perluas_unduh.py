"""Unduh paper tambahan (29 Okt 2026): string lama blok A/C yang belum pernah disaring + blok C dengan sinonim baru.

Tidak menyentuh data lama. Hasil: Data/perluasan_baru.csv (kolom sama dengan dataset_gabungan, tanpa Zenodo, tanpa judul ganda).
Kunci API dibaca dari ~/Tools/openalex.key. Jalankan: python -I perluas_unduh.py
"""
import csv, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from unduh_openalex import BLOCKS, fetch, abstract  # noqa: E402

DATA = os.path.join(os.path.dirname(HERE), "Data")
L2X = '("large language model" OR "large language models" OR LLM OR LLMs OR "generative AI" OR "generative artificial intelligence" OR ChatGPT OR "GPT-4" OR "small language model" OR SLM)'
CTXX = '(retail OR SME OR SMEs OR "small business" OR "small businesses" OR MSME OR warehouse OR "supply chain" OR procurement OR "demand forecasting" OR "sales forecasting" OR replenishment OR "point of sale" OR e-commerce OR "order management" OR "restaurant" OR "food and beverage")'
INVX = '(inventory OR "stock management" OR "stock control" OR "stock level" OR "stock levels")'
SAHAM = '("stock market" OR "stock price" OR "stock prices" OR "stock exchange" OR "stock trading" OR "stock returns")'
EXTRA = {
    "A": BLOCKS["A"],  # string lama; hanya yang belum pernah disaring yang dipakai
    "C": BLOCKS["C"],
    "C_sinonim": f"{L2X} AND {INVX} AND {CTXX} NOT {SAHAM}",
}
PERLU = {"A": "A", "C": "C", "C_sinonim": "C"}  # kolom blok di data akhir

known = {r["id"] for r in csv.DictReader(open(os.path.join(DATA, "penyaringan_gabungan.csv"), encoding="utf-8-sig"))}
# judul ganda & Zenodo yang sudah dibuang sebelumnya tidak dimasukkan lagi
norm = lambda t: re.sub(r"\W+", " ", (t or "").lower()).strip()
known_titles = {norm(r["title"]) for r in csv.DictReader(open(os.path.join(DATA, "penyaringan_gabungan.csv"), encoding="utf-8-sig"))}

found = {}
for name, s in EXTRA.items():
    for w in fetch(s):
        if w["id"] in known:
            continue
        found.setdefault(w["id"], {"w": w, "asal": set()})["asal"].add(name)

rows, seen_titles, dropped = [], set(), {"zenodo": 0, "judul_ganda": 0}
for v in found.values():
    w = v["w"]
    src = ((w.get("primary_location") or {}).get("source") or {})
    name = src.get("display_name") or ""
    if "zenodo" in name.lower():
        dropped["zenodo"] += 1
        continue
    t = norm(w.get("title"))
    if t in known_titles or t in seen_titles:
        dropped["judul_ganda"] += 1
        continue
    seen_titles.add(t)
    auth = w.get("authorships") or []
    rows.append({
        "id": w["id"], "doi": w.get("doi") or "", "title": w.get("title") or "",
        "year": w.get("publication_year"), "cited_by": w.get("cited_by_count"),
        "source": name,
        "authors": "; ".join((a.get("author") or {}).get("display_name") or "" for a in auth),
        "countries": "; ".join(sorted({c for a in auth for c in (a.get("countries") or [])})),
        "keywords": "; ".join(k.get("display_name", "") for k in (w.get("keywords") or [])),
        "topics": "; ".join(t_.get("display_name", "") for t_ in (w.get("topics") or [])),
        "n_refs": w.get("referenced_works_count") or 0,
        "referenced_works": "|".join(w.get("referenced_works") or []),
        "abstract": abstract(w), "blok": "+".join(sorted({PERLU[a] for a in v["asal"]})),
        "asal_pencarian": "+".join(sorted(v["asal"])),
    })
with open(os.path.join(DATA, "perluasan_baru.csv"), "w", encoding="utf-8-sig", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0]))
    wr.writeheader(); wr.writerows(rows)
print("belum pernah disaring:", len(found), "dibuang:", dropped, "tersimpan:", len(rows))
from collections import Counter
print(Counter(r["asal_pencarian"] for r in rows), Counter(bool(r["abstract"]) for r in rows))
