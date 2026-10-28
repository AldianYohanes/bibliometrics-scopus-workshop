"""Unduh tiga blok pencarian dari OpenAlex ke folder Data/.

Kunci API dibaca dari ~/Tools/openalex.key (di luar vault, jangan dipindah ke sini).
Hasil: Data/raw_blok_{A,B,C}.json (mentah), Data/dataset_gabungan.csv (tanpa duplikat, ada kolom blok).
Jalankan: python -I unduh_openalex.py
"""
import csv, json, os, sys, time, urllib.parse, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "Data")
KEY = open(os.path.expanduser("~/Tools/openalex.key")).read().strip()

L  = '("large language model" OR LLM OR LLMs)'
L2 = '("large language model" OR LLM OR LLMs OR "small language model" OR SLM)'
AG = '("multi-agent" OR "multiagent" OR agentic OR "LLM agent" OR "LLM agents")'
BZ = '("inventory management" OR "inventory control" OR "supply chain management" OR SME OR SMEs OR "small business" OR "small businesses" OR retail OR MSME OR "business process")'
BR = '(WebLLM OR WebGPU OR "in-browser" OR "browser-based" OR "on-device" OR "edge device" OR "edge devices")'
CTX = '(retail OR SME OR SMEs OR "small business" OR "small businesses" OR MSME OR warehouse OR "supply chain management" OR procurement OR "demand forecasting" OR "sales forecasting" OR replenishment OR "point of sale" OR e-commerce)'
SAHAM = '("stock market" OR "stock price" OR "stock prices" OR "stock exchange" OR "stock trading" OR "stock returns")'
BLOCKS = {
    "A": f"{L} AND {AG} AND {BZ}",
    "B": f"{L2} AND {BR}",
    "C": f"{L2} AND (inventory OR stock) AND {CTX} NOT {SAHAM}",
}
FIELDS = ("id,doi,title,publication_year,type,language,cited_by_count,abstract_inverted_index,"
          "authorships,primary_location,keywords,topics,referenced_works,referenced_works_count")


def fetch(search):
    flt = f"title_and_abstract.search:{search},publication_year:2023-2026,type:article"
    cursor, out = "*", []
    while cursor:
        q = {"filter": flt, "per-page": 200, "cursor": cursor, "select": FIELDS, "api_key": KEY}
        with urllib.request.urlopen("https://api.openalex.org/works?" + urllib.parse.urlencode(q), timeout=120) as r:
            d = json.load(r)
        out += d["results"]
        cursor = d["meta"].get("next_cursor")
        time.sleep(0.2)
    return out


def abstract(w):
    inv = w.get("abstract_inverted_index") or {}
    pos = {p: word for word, ps in inv.items() for p in ps}
    return " ".join(pos[i] for i in sorted(pos))


def main():
    os.makedirs(DATA, exist_ok=True)
    merged = {}
    for b, s in BLOCKS.items():
        works = fetch(s)
        json.dump(works, open(os.path.join(DATA, f"raw_blok_{b}.json"), "w", encoding="utf-8"), ensure_ascii=False)
        print(f"blok {b}: {len(works)}")
        for w in works:
            merged.setdefault(w["id"], {"w": w, "blok": set()})["blok"].add(b)
    rows = []
    for v in merged.values():
        w = v["w"]
        src = ((w.get("primary_location") or {}).get("source") or {})
        auth = w.get("authorships") or []
        rows.append({
            "id": w["id"], "doi": w.get("doi") or "", "title": w.get("title") or "",
            "year": w.get("publication_year"), "cited_by": w.get("cited_by_count"),
            "source": src.get("display_name") or "",
            "authors": "; ".join((a.get("author") or {}).get("display_name") or "" for a in auth),
            "countries": "; ".join(sorted({c for a in auth for c in (a.get("countries") or [])})),
            "keywords": "; ".join(k.get("display_name", "") for k in (w.get("keywords") or [])),
            "topics": "; ".join(t.get("display_name", "") for t in (w.get("topics") or [])),
            "n_refs": w.get("referenced_works_count") or 0,
            "referenced_works": "|".join(w.get("referenced_works") or []),
            "abstract": abstract(w), "blok": "+".join(sorted(v["blok"])),
        })
    with open(os.path.join(DATA, "dataset_gabungan.csv"), "w", encoding="utf-8-sig", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]))
        wr.writeheader(); wr.writerows(rows)
    print("gabungan tanpa duplikat:", len(rows))


if __name__ == "__main__":
    main()
