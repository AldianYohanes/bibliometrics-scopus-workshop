"""Tabel dan gambar sesuai format template workshop (Template Bibliographic coupling/co-word dan Template citation/co-citation/co-word).

Keluaran: Hasil/tabel_artikel.md (tabel siap tempel) + Hasil/gambar1_tren_publikasi.png.
Rumus sama dengan analisis_tambahan.py (seed 42, ambang sama), jadi nomor kluster cocok dengan peta VOSviewer yang dibuka.
Jalankan: python -I tabel_template.py
"""
import itertools, json, os, sys, time, urllib.parse, urllib.request
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Hasil")
KEY = open(os.path.expanduser("~/Tools/openalex.key")).read().strip()
SEED = 42
WARNA = {1: "merah", 2: "hijau", 3: "biru", 4: "kuning", 5: "ungu", 6: "cyan", 7: "oranye"}
CURIGA = {"https://openalex.org/W4385245566"}
d = pd.read_csv(os.path.join(ROOT, "Data", "dataset_lolos.csv"), encoding="utf-8-sig").fillna("")
ex = pd.read_csv(os.path.join(ROOT, "Data", "referensi_tambahan.csv"), encoding="utf-8-sig").fillna("")
e = dict(zip(ex.id, ex.referenced_works))
d["refs_all"] = [r if r else e.get(i, "") for i, r in zip(d.id, d.referenced_works)]
tt = d.set_index("id")


def louvain(G):
    return sorted(nx.community.louvain_communities(G, weight="weight", seed=SEED), key=len, reverse=True)


def kuat(G):
    return dict(G.degree(weight="weight"))


def cut(s, n):
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "..."


def pub(i):
    r = tt.loc[i]
    a = (r.authors.split("; ")[0].split()[-1] if r.authors else "?")
    return f"{a} et al. ({r.year}), {cut(r.title, 80)}"


def md(df):
    cols = list(df.columns)
    s = "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n"
    for _, r in df.iterrows():
        s += "| " + " | ".join(str(x).replace("|", "/") for x in r) + " |\n"
    return s


teks = ["# Tabel dan gambar artikel (format template workshop)\n",
        "Dibuat otomatis oleh `Skrip/tabel_template.py` dari `Data/dataset_lolos.csv` (485 paper). Nama kluster **belum diberi**: harus dari membaca dokumen inti (aturan template: interpretasi induktif). TLS = total link strength.\n"]

# ---------- Gambar 1: publikasi dan sitasi per tahun ----------
g = d.groupby("year").agg(dokumen=("id", "size"), sitasi=("cited_by", "sum"))
fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(g.index.astype(str), g.dokumen, color="#2b8cbe"); ax.set_ylabel("Jumlah publikasi")
for x, y in zip(g.index.astype(str), g.dokumen):
    ax.text(x, y, str(y), ha="center", va="bottom", fontsize=8)
ax2 = ax.twinx(); ax2.plot(g.index.astype(str), g.sitasi, color="#e6550d", marker="o"); ax2.set_ylabel("Jumlah sitasi")
ax.set_title("Publikasi dan sitasi per tahun (OpenAlex, artikel; 2026 belum selesai)", fontsize=9)
fig.tight_layout(); fig.savefig(f"{OUT}/gambar1_tren_publikasi.png", dpi=150); plt.close(fig)
teks += ["## Gambar 1. Publikasi dan sitasi per tahun\n", "File: `Hasil/gambar1_tren_publikasi.png`\n", md(g.reset_index().rename(columns={"year": "tahun"})), ""]

# ---------- Tabel: dokumen teratas menurut sitasi (analisis sitasi) ----------
top = d.sort_values("cited_by", ascending=False).head(10)
t = pd.DataFrame({"Peringkat": range(1, 11), "Penulis": [x.split("; ")[0] + " et al." for x in top.authors],
                  "Judul": [cut(x, 95) for x in top.title], "Tahun": top.year, "Sitasi": top.cited_by})
teks += ["## Tabel A. Top 10 dokumen berdasarkan sitasi (analisis sitasi)\n", "Sitasi dari OpenAlex (angka global, bukan hanya dari dataset ini).\n", md(t), ""]

# ---------- Bibliographic coupling ----------
refs = {r.id: set(r.refs_all.split("|")) for r in d[d.refs_all != ""].itertuples()}
B = nx.Graph(); B.add_nodes_from(refs)
for a, b in itertools.combinations(list(refs), 2):
    s = len(refs[a] & refs[b])
    if s >= 2:
        B.add_edge(a, b, weight=s)
B.remove_nodes_from([n for n in list(B) if B.degree(n) == 0])
bc = louvain(B); tls = kuat(B)
lab = {n: i for i, c in enumerate(bc, 1) for n in c}
teks += [f"## Bibliographic coupling\n", f"Dari {len(d)} dokumen, {len(refs)} punya data referensi; {B.number_of_nodes()} terhubung (≥2 referensi sama) dan membentuk {len(bc)} kluster (ukuran: {[len(c) for c in bc]}).\n"]
tb = sorted(B, key=lambda n: -tls[n])[:10]
t = pd.DataFrame({"Peringkat": range(1, 11), "Publikasi": [pub(n) for n in tb], "Sitasi": [tt.loc[n, "cited_by"] for n in tb], "TLS": [tls[n] for n in tb], "Kluster": [lab[n] for n in tb]})
teks += ["### Tabel B. Top 10 dokumen dalam analisis bibliographic coupling (menurut TLS)\n", md(t), ""]
rows = []
for i, c in enumerate(bc, 1):
    if len(c) < 5:
        continue
    rep = sorted(c, key=lambda n: -tls[n])[:2]
    rows.append({"Kluster (warna)": f"{i} ({WARNA.get(i, '?')})", "Label kluster": "[BELUM DIBERI NAMA]", "Jumlah publikasi": len(c),
                 "Blok asal": dict(Counter(tt.loc[n, 'blok'] for n in c)), "Publikasi representatif": "; ".join(pub(n) for n in rep)})
teks += ["### Tabel C. Ringkasan kluster bibliographic coupling (kluster ≥5 dokumen)\n", md(pd.DataFrame(rows)), ""]

# ---------- Co-citation ----------
cit = Counter(r for s in refs.values() for r in s)
keep = {r for r, c in cit.items() if c >= 3}
tipe = {}
ids = list(keep)
for i in range(0, len(ids), 50):
    q = {"filter": "openalex_id:" + "|".join(ids[i:i + 50]), "per-page": 50, "select": "id,display_name,publication_year,authorships,type,cited_by_count", "api_key": KEY}
    with urllib.request.urlopen("https://api.openalex.org/works?" + urllib.parse.urlencode(q), timeout=60) as r:
        for w in json.load(r)["results"]:
            a = ((w.get("authorships") or [{}])[0].get("author") or {}).get("display_name", "?")
            tipe[w["id"]] = {"tipe": w.get("type") or "", "judul": w.get("display_name") or "", "tahun": w.get("publication_year"), "pen": a, "cit": w.get("cited_by_count")}
    time.sleep(0.1)
bad = {r for r in keep if r in CURIGA or tipe.get(r, {}).get("tipe") == "proceedings" or tipe.get(r, {}).get("judul", "").lower().startswith(("proceedings of", "findings of"))}
keep -= bad
C = nx.Graph(); C.add_nodes_from(sorted(keep))
for s in refs.values():
    for a, b in itertools.combinations(sorted(s & keep), 2):
        C.add_edge(a, b, weight=C.get_edge_data(a, b, {"weight": 0})["weight"] + 1)
C.remove_nodes_from([n for n in list(C) if C.degree(n) == 0])
cc = louvain(C); ctl = kuat(C)
clab = {n: i for i, c in enumerate(cc, 1) for n in c}


def rf(n):
    x = tipe.get(n, {})
    return f"{x.get('pen', '?').split()[-1]} ({x.get('tahun')}), {cut(x.get('judul', n), 80)}"


teks += ["## Co-citation\n", f"Dari {len(cit)} referensi unik, {len(keep)} memenuhi ambang 3 sitasi oleh dokumen kita (setelah {len(bad)} artefak dibuang), membentuk {len(cc)} kluster (ukuran: {[len(c) for c in cc]}).\n"]
tc = sorted(C, key=lambda n: -ctl[n])[:10]
t = pd.DataFrame({"Peringkat": range(1, 11), "Dokumen": [rf(n) for n in tc], "Sitasi (oleh dokumen kita)": [cit[n] for n in tc], "TLS": [ctl[n] for n in tc], "Kluster": [clab[n] for n in tc]})
teks += ["### Tabel D. Top 10 dokumen dengan co-citation dan TLS tertinggi\n", md(t), ""]
rows = []
for i, c in enumerate(cc, 1):
    rep = sorted(c, key=lambda n: -cit[n])[:2]
    rows.append({"Kluster (warna)": f"{i} ({WARNA.get(i, '?')})", "Label kluster": "[BELUM DIBERI NAMA]", "Jumlah artikel": len(c), "Publikasi representatif": "; ".join(rf(n) for n in rep)})
teks += ["### Tabel E. Kluster co-citation\n", md(pd.DataFrame(rows)), ""]

# ---------- Co-word ----------
SIN = {"llm": "large language model", "llms": "large language model", "large language models": "large language model", "language model": "large language model", "language models": "large language model", "ai": "artificial intelligence"}
BUANG = {"large language model", "artificial intelligence"}
kws = [sorted({SIN.get(k.strip().lower(), k.strip().lower()) for k in s.split(";") if k.strip()} - BUANG) for s in d.keywords]
cnt = Counter(k for ks in kws for k in ks)
keepk = {k for k, c in cnt.items() if c >= 8}
G = nx.Graph(); G.add_nodes_from(sorted(keepk))
for ks in kws:
    for a, b in itertools.combinations([k for k in ks if k in keepk], 2):
        G.add_edge(a, b, weight=G.get_edge_data(a, b, {"weight": 0})["weight"] + 1)
G.remove_nodes_from([n for n in list(G) if G.degree(n) == 0])
kc = louvain(G); ktl = kuat(G)
klab = {n: i for i, c in enumerate(kc, 1) for n in c}
teks += ["## Co-word\n", f"Dari {len(cnt)} kata kunci unik (setelah penggabungan sinonim dan membuang 'large language model' serta 'artificial intelligence'), {G.number_of_nodes()} memenuhi ambang 8 kemunculan, membentuk {len(kc)} kluster (ukuran: {[len(c) for c in kc]}).\n"]
tk = sorted(G, key=lambda n: -cnt[n])[:15]
t = pd.DataFrame({"Peringkat": range(1, 16), "Kata kunci": tk, "Kemunculan": [cnt[k] for k in tk], "TLS": [ktl[k] for k in tk], "Kluster": [klab[k] for k in tk]})
teks += ["### Tabel F. Top 15 kata kunci dalam analisis co-occurrence\n", md(t), ""]
rows = []
for i, c in enumerate(kc, 1):
    rep = sorted(c, key=lambda k: -cnt[k])[:8]
    rows.append({"Kluster (warna)": f"{i} ({WARNA.get(i, '?')})", "Label kluster": "[BELUM DIBERI NAMA]", "Jumlah kata kunci": len(c), "Kata kunci representatif": ", ".join(rep)})
teks += ["### Tabel G. Ringkasan analisis co-word\n", md(pd.DataFrame(rows)), "",
         "Catatan: warna kluster mengikuti urutan standar VOSviewer (1 merah, 2 hijau, 3 biru, 4 kuning, 5 ungu); cocokkan dengan gambar yang kamu ekspor.\n"]
open(f"{OUT}/tabel_artikel.md", "w", encoding="utf-8").write("\n".join(teks))
print("ok | coupling", [len(c) for c in bc][:9], "| cocit", [len(c) for c in cc], "| coword", [len(c) for c in kc], "| kata unik", len(cnt))
