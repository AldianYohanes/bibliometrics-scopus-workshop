"""Unduh rekaman tambahan dari variasi string V1 (istilah LLM lebih luas) dan V4 (sinonim perangkat lebih luas).

Yang sudah pernah disaring (708 hasil dasar, 127 perluasan) tidak diambil lagi; Zenodo dan judul ganda dibuang.
Hasil: Data/perluasan_v14.csv (kolom sama dengan perluasan_baru.csv). Data lama tidak disentuh.
Kunci API dibaca dari ~/Tools/openalex.key. Jalankan: python -I v14_unduh.py
"""
import csv, os, re, sys
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import json, time, urllib.parse, urllib.request  # noqa: E402
from unduh_openalex import AG, BR, BZ, CTX, FIELDS, KEY, L, L2, SAHAM, abstract  # noqa: E402


def fetch(search):
    # halaman 200 dengan daftar rujukan sering terputus di tengah; pakai 100 per halaman dan coba ulang
    flt = f"title_and_abstract.search:{search},publication_year:2023-2026,type:article"
    cursor, out = "*", []
    while cursor:
        q = {"filter": flt, "per-page": 100, "cursor": cursor, "select": FIELDS, "api_key": KEY}
        for coba in range(5):
            try:
                with urllib.request.urlopen("https://api.openalex.org/works?" + urllib.parse.urlencode(q), timeout=120) as r:
                    d = json.load(r)
                break
            except Exception:
                if coba == 4:
                    raise
                time.sleep(5 * (coba + 1))
        out += d["results"]
        cursor = d["meta"].get("next_cursor")
        time.sleep(0.2)
    return out

DATA = os.path.join(os.path.dirname(HERE), "Data")
# sama persis dengan VARIAN V1 dan V4 di sensibilitas_string.py
GEN = '("large language model" OR LLM OR LLMs OR "generative AI" OR GPT OR ChatGPT OR "foundation model" OR "foundation models")'
GEN2 = GEN[:-1] + ' OR "small language model" OR SLM)'
BR2 = BR[:-1] + ' OR TinyML OR "local LLM" OR "local inference" OR smartphone OR smartphones OR "mobile device" OR "mobile devices")'
STRING = {
    "V1_A": (f"{GEN} AND {AG} AND {BZ}", "A"),
    "V1_B": (f"{GEN2} AND {BR}", "B"),
    "V1_C": (f"{GEN2} AND (inventory OR stock) AND {CTX} NOT {SAHAM}", "C"),
    "V4_B": (f"{L2} AND {BR2}", "B"),
}

rd = lambda p: list(csv.DictReader(open(os.path.join(DATA, p), encoding="utf-8-sig")))
norm = lambda t: re.sub(r"\W+", " ", (t or "").lower()).strip()
# 708 yang disaring + 127 perluasan; 93 sisanya (judul ganda, Zenodo) tersaring lagi lewat judul dan sumber
lama = rd("penyaringan_gabungan.csv") + rd("perluasan_baru.csv")
known, known_titles = {r["id"] for r in lama}, {norm(r["title"]) for r in lama}

found = {}
for name, (s, blok) in STRING.items():
    for w in fetch(s):
        if w["id"] not in known:
            v = found.setdefault(w["id"], {"w": w, "asal": set(), "blok": set()})
            v["asal"].add(name); v["blok"].add(blok)

rows, seen, dropped = [], set(), Counter()
for v in found.values():
    w = v["w"]
    name = (((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "")
    if "zenodo" in name.lower():
        dropped["zenodo"] += 1; continue
    t = norm(w.get("title"))
    if t in known_titles or t in seen:
        dropped["judul_ganda"] += 1; continue
    seen.add(t)
    auth = w.get("authorships") or []
    rows.append({
        "id": w["id"], "doi": w.get("doi") or "", "title": w.get("title") or "",
        "year": w.get("publication_year"), "cited_by": w.get("cited_by_count"), "source": name,
        "authors": "; ".join((a.get("author") or {}).get("display_name") or "" for a in auth),
        "countries": "; ".join(sorted({c for a in auth for c in (a.get("countries") or [])})),
        "keywords": "; ".join(k.get("display_name", "") for k in (w.get("keywords") or [])),
        "topics": "; ".join(x.get("display_name", "") for x in (w.get("topics") or [])),
        "n_refs": w.get("referenced_works_count") or 0,
        "referenced_works": "|".join(w.get("referenced_works") or []),
        "abstract": abstract(w), "blok": "+".join(sorted(v["blok"])),
        "asal_pencarian": "+".join(sorted(v["asal"])),
    })
with open(os.path.join(DATA, "perluasan_v14.csv"), "w", encoding="utf-8-sig", newline="") as f:
    wr = csv.DictWriter(f, fieldnames=list(rows[0]))
    wr.writeheader(); wr.writerows(rows)
print("baru:", len(found), "dibuang:", dict(dropped), "tersimpan:", len(rows))
print(Counter(r["asal_pencarian"] for r in rows), "ada abstrak:", sum(bool(r["abstract"]) for r in rows))
