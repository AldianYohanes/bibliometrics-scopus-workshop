"""Buat paper/refs_tambahan.bib dari daftar ID OpenAlex (metadata diambil dari OpenAlex, bukan diketik).

Tiap rujukan dipilih karena muncul dalam data kita atau pencarian judul; keberadaannya = ada di OpenAlex dengan judul, penulis pertama, dan tahun yang dicek.
Volume dan halaman diambil dari OpenAlex bila ada; hasil tetap perlu dicek ke situs penerbit sebelum submit.
Jalankan: python -I ambil_rujukan.py   (butuh ~/Tools/openalex.key)
"""
import json, os, re, sys, urllib.parse, urllib.request

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(os.path.dirname(ROOT), "paper", "refs_tambahan.bib")
KEY = open(os.path.expanduser("~/Tools/openalex.key")).read().strip()

IDS = {  # kunci bibtex: ID OpenAlex
    "brown2020": "W3030163527", "touvron2023": "W4322718191", "wei2022": "W7133224126",
    "wang2024agents": "W4393065402", "friha2024": "W4402350363", "qu2025": "W4406207083", "zheng2025": "W4407881031", "wang2025slm": "W4414320956",
    "ruan2024webllm": "W4405715435", "jackson2024": "W4391403992", "wamba2023": "W4390055472", "kosasih2023": "W4388971978",
    "almahri2025": "W7104176434", "nakhost2025": "W4416956871", "jannelli2025": "W7116783479",
    "fan2024": "W4396870811", "olujimi2025": "W7117245693", "hassan2025": "W4412445032", "gencer2025": "W7203589611",
}
IDS.pop("gencer2025")  # W7203589611 adalah artikel di jurnal yang kualitasnya meragukan; tidak dipakai


def esc(s):
    return s.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#").replace("_", r"\_")


q = {"filter": "openalex_id:" + "|".join(IDS.values()), "per-page": 50, "api_key": KEY,
     "select": "id,display_name,publication_year,type,doi,authorships,biblio,primary_location,abstract_inverted_index"}
works = {w["id"].split("/")[-1]: w for w in json.load(urllib.request.urlopen("https://api.openalex.org/works?" + urllib.parse.urlencode(q)))["results"]}
out, info = [], {}
for key, wid in IDS.items():
    w = works[wid]
    nama = [re.sub(r"\s+[A-Z]$", "", a["author"]["display_name"]) for a in w["authorships"]]  # buang inisial lepas ("Jared Kaplan A")
    au = " and ".join(nama[:6]) + (" and others" if len(nama) > 6 else "")  # daftar penulis dipotong; lengkapi sebelum submit
    doi = (w.get("doi") or "").replace("https://doi.org/", "")
    src = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
    b = w.get("biblio") or {}
    pages = "--".join(x for x in (b.get("first_page"), b.get("last_page")) if x)
    f = [f"  author = {{{esc(au)}}}", f"  title = {{{{{esc(w['display_name'])}}}}}", f"  year = {{{w['publication_year']}}}"]
    m = re.match(r"10\.48550/arxiv\.(.+)", doi, re.I)
    if m or w["type"] == "preprint":
        typ = "online"
        f += [f"  eprint = {{{m.group(1) if m else ''}}}", "  eprinttype = {arxiv}"]
        if not m:
            f += [f"  doi = {{{doi}}}"]
    elif w["type"] == "conference-paper":
        typ = "inproceedings"
        f += ["  booktitle = {Advances in Neural Information Processing Systems}"] + ([f"  doi = {{{doi}}}"] if doi else [])
    else:
        typ = "article"
        f += [f"  journal = {{{esc(src)}}}"] + ([f"  volume = {{{b['volume']}}}"] if b.get("volume") else []) + ([f"  number = {{{b['issue']}}}"] if b.get("issue") else []) \
            + ([f"  pages = {{{pages}}}"] if pages else []) + ([f"  doi = {{{doi}}}"] if doi else [])
    out.append(f"@{typ}{{{key},\n" + ",\n".join(f) + "\n}\n")
    inv = w.get("abstract_inverted_index") or {}
    pos = {p: t for t, ps in inv.items() for p in ps}
    info[key] = " ".join(pos[i] for i in sorted(pos))
head = "% Dibuat oleh analysis/Skrip/ambil_rujukan.py dari OpenAlex (metadata tidak diketik). Cek volume/halaman ke situs penerbit sebelum submit.\n% Vaswani 2017 ditambah manual di refs.bib (NeurIPS 30, arXiv 1706.03762).\n\n"
open(OUT, "w", encoding="utf-8").write(head + "\n".join(out))
json.dump(info, open(os.path.join(ROOT, "Hasil", "abstrak_rujukan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ditulis", len(out), "entri ->", OUT)
for k in ("fan2024", "olujimi2025", "hassan2025"):
    print("\n##", k, "|", info[k][:1100])
