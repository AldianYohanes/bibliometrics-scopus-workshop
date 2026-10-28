"""Uji sensitivitas string pencarian: variasi kata kunci dibandingkan dengan pencarian dasar.

Untuk tiap variasi: jumlah hasil, berapa dari 485 paper lolos yang tetap tertangkap (recall terhadap data akhir),
berapa paper baru di luar hasil dasar yang sudah dibersihkan (708), dan contoh judul paper baru untuk dinilai relevansinya.
Jalankan: python -I sensibilitas_string.py   (butuh ~/Tools/openalex.key)
"""
import json, os, random, sys, time, urllib.parse, urllib.request

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from unduh_openalex import AG, BR, BZ, CTX, KEY, L, L2, SAHAM  # noqa: E402  (hanya konstanta; main tidak jalan saat impor)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
base_all = set(pd.read_csv(f"{ROOT}/Data/penyaringan_gabungan.csv", encoding="utf-8-sig").id)
incl = set(pd.read_csv(f"{ROOT}/Data/dataset_lolos.csv", encoding="utf-8-sig").id)
CAP = 3000


def fetch(search, field="title_and_abstract"):
    flt = f"{field}.search:{search},publication_year:2023-2026,type:article"
    cursor, out, total = "*", {}, 0
    while cursor and len(out) < CAP:
        q = {"filter": flt, "per-page": 200, "cursor": cursor, "select": "id,title", "api_key": KEY}
        with urllib.request.urlopen("https://api.openalex.org/works?" + urllib.parse.urlencode(q), timeout=120) as r:
            d = json.load(r)
        total = d["meta"]["count"]
        out.update({w["id"]: w["title"] for w in d["results"]})
        cursor = d["meta"].get("next_cursor")
        time.sleep(0.2)
    return total, out


GEN = '("large language model" OR LLM OR LLMs OR "generative AI" OR GPT OR ChatGPT OR "foundation model" OR "foundation models")'
GEN2 = GEN[:-1] + ' OR "small language model" OR SLM)'
BR2 = BR[:-1] + ' OR TinyML OR "local LLM" OR "local inference" OR smartphone OR smartphones OR "mobile device" OR "mobile devices")'
IN2 = '(inventory OR stock OR stockout OR "stock-out" OR SKU OR "warehouse management" OR "stock keeping")'
A = lambda l: f"{l} AND {AG} AND {BZ}"
B = lambda l, br: f"{l} AND {br}"
C = lambda l, i, ex: f"{l} AND {i} AND {CTX}" + (f" NOT {SAHAM}" if ex else "")
VARIAN = {
    "dasar": ([A(L), B(L2, BR), C(L2, "(inventory OR stock)", True)], "title_and_abstract"),
    "V1 istilah LLM lebih luas (+generative AI, GPT, ChatGPT, foundation model)": ([A(GEN), B(GEN2, BR), C(GEN2, "(inventory OR stock)", True)], "title_and_abstract"),
    "V2 blok C tanpa pengecualian saham": ([A(L), B(L2, BR), C(L2, "(inventory OR stock)", False)], "title_and_abstract"),
    "V3 hanya judul (bukan abstrak)": ([A(L), B(L2, BR), C(L2, "(inventory OR stock)", True)], "title"),
    "V4 sinonim perangkat lebih luas (+TinyML, local LLM, smartphone, mobile device)": ([A(L), B(L2, BR2), C(L2, "(inventory OR stock)", True)], "title_and_abstract"),
    "V5 sinonim inventori lebih luas (+SKU, stockout, warehouse management)": ([A(L), B(L2, BR), C(L2, IN2, True)], "title_and_abstract"),
}
random.seed(7)
rows, contoh = [], {}
for nama, (blok, field) in VARIAN.items():
    ids, titles = set(), {}
    for s in blok:
        _, t = fetch(s, field)
        titles.update(t)
    ids = set(titles)
    baru = ids - base_all
    rows.append({"varian": nama, "hasil_unik": len(ids), "recall_data_akhir_485": f"{len(ids & incl)} dari {len(incl)} ({100*len(ids & incl)/len(incl):.0f}%)",
                 "irisan_dengan_dasar_708": len(ids & base_all), "paper_baru_di_luar_dasar": len(baru)})
    contoh[nama] = [titles[i] for i in random.sample(sorted(baru), min(8, len(baru)))]
    print(rows[-1], flush=True)
pd.DataFrame(rows).to_csv(f"{ROOT}/Hasil/sensibilitas_string.csv", index=False, encoding="utf-8-sig")
json.dump(contoh, open(f"{ROOT}/Hasil/sensibilitas_contoh_baru.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
