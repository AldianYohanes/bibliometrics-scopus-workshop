"""Buat berkas 'dosir' per kelompok kluster untuk dibaca penilai (judul + abstrak artikel representatif).

Masukan: Hasil/kluster_anggota.json (dari tabel_template.py) dan Data/dataset_lolos.csv.
Keluaran: tiga berkas teks di folder yang diberikan: dosir_coword.txt, dosir_coupling.txt, dosir_cocitation.txt.
Jalankan: python -I dosir_kluster.py <folder_keluaran>
"""
import json, os, sys
from collections import Counter

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
K = json.load(open(f"{ROOT}/Hasil/kluster_anggota.json", encoding="utf-8"))
d = pd.read_csv(f"{ROOT}/Data/dataset_lolos.csv", encoding="utf-8-sig").fillna("").set_index("id")
SIN = {"llm": "large language model", "llms": "large language model", "large language models": "large language model",
       "language model": "large language model", "language models": "large language model", "ai": "artificial intelligence"}


def doc(i, extra=""):
    r = d.loc[i]
    ab = r.abstract[:900] if r.abstract else "(tidak ada abstrak)"
    return f"- [{i.split('/')[-1]}] ({r.year}, blok {r.blok}{extra}) {r.title}\n  Abstrak: {ab}\n"


# co-word: tiap dokumen masuk kluster dengan kata kunci terbanyak
with open(f"{out}/dosir_coword.txt", "w", encoding="utf-8") as f:
    kwcl = {k: c["kluster"] for c in K["coword"] for k in c["kw"]}
    score = {c["kluster"]: [] for c in K["coword"]}
    for i, r in d.iterrows():
        ks = {SIN.get(k.strip().lower(), k.strip().lower()) for k in r.keywords.split(";") if k.strip()}
        cnt = Counter(kwcl[k] for k in ks if k in kwcl)
        if cnt:
            kl, n = cnt.most_common(1)[0]
            score[kl].append((n, r.cited_by, i))
    for c in K["coword"]:
        f.write(f"\n===== KLUSTER CO-WORD {c['kluster']} =====\nJumlah kata kunci: {len(c['kw'])}\nKata kunci (jumlah dokumen): " + ", ".join(f"{k} ({c['cnt'][k]})" for k in c["kw"]) + "\n\nArtikel representatif (paling banyak kata kunci kluster ini, lalu paling banyak dikutip):\n")
        for n, cb, i in sorted(score[c["kluster"]], reverse=True)[:10]:
            f.write(doc(i, f", {n} kata kunci kluster"))

# coupling: kluster >=5 dokumen, 8 dokumen dengan TLS tertinggi
with open(f"{out}/dosir_coupling.txt", "w", encoding="utf-8") as f:
    for c in K["coupling"]:
        if len(c["docs"]) < 5:
            continue
        f.write(f"\n===== KLUSTER COUPLING {c['kluster']} =====\nJumlah artikel: {len(c['docs'])}\nBlok asal: {dict(Counter(d.loc[i, 'blok'] for i in c['docs']))}\n\nArtikel dengan total link strength tertinggi:\n")
        for i in c["docs"][:8]:
            f.write(doc(i))

# co-citation: 25 referensi paling sering dikutip per kluster (hanya judul; abstrak referensi tidak ada)
with open(f"{out}/dosir_cocitation.txt", "w", encoding="utf-8") as f:
    for c in K["cocitation"]:
        f.write(f"\n===== KLUSTER CO-CITATION {c['kluster']} =====\nJumlah referensi: {len(c['refs'])}\nReferensi yang paling sering dikutip oleh artikel kita (penulis pertama, tahun, judul; jumlah artikel yang mengutip):\n")
        for r in c["refs"][:25]:
            f.write(f"- {r['label']} (x{r['cit']})\n")
print("ok")
