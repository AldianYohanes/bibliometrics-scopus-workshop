"""Grafik jumlah item yang lolos pada tiap ambang: referensi menurut ambang sitasi (co-citation) dan kata kunci menurut ambang kemunculan (co-word).

Dasar pemilihan ambang di naskah: ambang 3 sitasi untuk referensi dan 8 kemunculan untuk kata kunci (ditandai garis putus).
Jumlah referensi memakai hitungan mentah sebelum 10 artefak dibuang (pada ambang 3: 354 mentah, 344 sesudah dibuang).
Keluaran: Hasil/ambang.csv, Hasil/fig_ambang.png, paper/figures/fig_ambang.png. Jalankan: python -I ambang.py
"""
import os, shutil, sys
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER = os.path.join(os.path.dirname(ROOT), "paper")
plt.rcParams["font.family"] = ["Times New Roman", "DejaVu Serif"]
d = pd.read_csv(f"{ROOT}/Data/dataset_lolos.csv", encoding="utf-8-sig").fillna("")
ex = dict(zip(*pd.read_csv(f"{ROOT}/Data/referensi_tambahan.csv", encoding="utf-8-sig").fillna("")[["id", "referenced_works"]].T.values))

# referensi: berapa artikel di dataset yang mengutip tiap referensi
cit = Counter()
for i, r in zip(d.id, d.referenced_works):
    refs = r or ex.get(i, "")
    cit.update(set(refs.split("|")) - {""})
ref_k = list(range(1, 16))
ref_n = [sum(1 for c in cit.values() if c >= k) for k in ref_k]

# kata kunci: berapa kata kunci muncul di minimal k artikel (setelah penggabungan sinonim)
SIN = {"llm": "large language model", "llms": "large language model", "large language models": "large language model", "language model": "large language model", "language models": "large language model", "ai": "artificial intelligence"}
BUANG = {"large language model", "artificial intelligence"}
kw = Counter()
for s in d.keywords:
    kw.update({SIN.get(k.strip().lower(), k.strip().lower()) for k in s.split(";") if k.strip()} - BUANG)
kw_k = list(range(1, 21))
kw_n = [sum(1 for c in kw.values() if c >= k) for k in kw_k]

pd.concat([pd.DataFrame({"jenis": "referensi (min. sitasi)", "ambang": ref_k, "item_lolos": ref_n}),
           pd.DataFrame({"jenis": "kata kunci (min. kemunculan)", "ambang": kw_k, "item_lolos": kw_n})]).to_csv(f"{ROOT}/Hasil/ambang.csv", index=False)
print("referensi unik:", len(cit), "| lolos ambang 2/3/5:", ref_n[1], ref_n[2], ref_n[4])
print("kata kunci unik:", len(kw), "| lolos ambang 5/8/12:", kw_n[4], kw_n[7], kw_n[11])

fig, ax = plt.subplots(1, 2, figsize=(10, 3.9))
for a, k, n, pilih, judul, xl in ((ax[0], ref_k, ref_n, 3, "Co-citation: cited references", "Minimum number of citing articles (threshold)"),
                                  (ax[1], kw_k, kw_n, 8, "Co-word: keywords", "Minimum number of occurrences (threshold)")):
    a.plot(k, n, marker="o", color="#2b8cbe", ms=4)
    a.set_yscale("log"); a.set_xlabel(xl); a.set_ylabel("Items meeting the threshold"); a.set_title(judul, fontsize=10)
    a.axvline(pilih, color="#e6550d", ls="--", lw=1)
    a.annotate(f"threshold {pilih}: {n[pilih - 1]} items", (pilih, n[pilih - 1]), textcoords="offset points", xytext=(8, 8), fontsize=9, color="#e6550d")
    a.set_xticks(k[::2] if len(k) > 12 else k)
fig.tight_layout()
fig.savefig(f"{ROOT}/Hasil/fig_ambang.png", dpi=200)
shutil.copy(f"{ROOT}/Hasil/fig_ambang.png", f"{PAPER}/figures/fig_ambang.png")
