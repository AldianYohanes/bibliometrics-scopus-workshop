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
CURIGA = {"https://openalex.org/W4385245566", "https://openalex.org/W4292779060", "https://openalex.org/W4384918448"}
d = pd.read_csv(os.path.join(ROOT, "Data", "dataset_lolos.csv"), encoding="utf-8-sig").fillna("")
ex = pd.read_csv(os.path.join(ROOT, "Data", "referensi_tambahan.csv"), encoding="utf-8-sig").fillna("")
e = dict(zip(ex.id, ex.referenced_works))
d["refs_all"] = [r if r else e.get(i, "") for i, r in zip(d.id, d.referenced_works)]
tt = d.set_index("id")



# Label kluster usulan (pembacaan abstrak artikel representatif oleh model, lalu diperiksa; HARUS disetujui penulis).
# Kunci = tuple ukuran kluster; jika ukuran berubah (data atau algoritma berubah) label tidak dipakai lagi supaya tidak salah tempel.
LABEL = {
    # coupling (ambang sitasi dokumen >=3, kluster >=6): label dari judul 9 dokumen dengan TLS tertinggi per kluster (lebih tipis daripada pembacaan abstrak sebelumnya)
    "coupling": {(19, 18, 18, 14): [
        "Edge-cloud collaborative inference and surveys of edge LLM deployment", "Edge intelligence surveys, collaborative inference, and hardware acceleration",
        "On-device deployment, inference optimisation, and small language models", "Pruning and on-device (federated) fine-tuning"]},
    "cocit": {(128, 95, 58, 57, 6): [
        "Edge LLM surveys, collaborative serving, and NLP benchmarks", "Quantisation, pruning, and serving efficiency, with foundation models",
        "Mixed background: efficient inference, federated and parameter-efficient tuning, early applications", "General background: reasoning, edge computing visions, LLM agents, compression basics",
        "Generative AI in supply chain and operations management"]},
    "coword": {(24, 23, 21): [
        "Agentic AI and RAG for enterprise applications (with an inventory sub-theme)", "Compression and optimisation for edge LLM deployment",
        "Small language models and privacy-preserving on-device learning"]},
}


def nama_kluster(kind, comms, i):
    sizes = tuple(len(c) for c in comms)
    for key, names in LABEL[kind].items():
        if sizes[:len(key)] == key and i <= len(names):
            return names[i - 1]
    return "[BELUM DIBERI NAMA]"


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
ax.bar(g.index.astype(str), g.dokumen, color="#2b8cbe"); ax.set_ylabel("Publications")
for x, y in zip(g.index.astype(str), g.dokumen):
    ax.text(x, y, str(y), ha="center", va="bottom", fontsize=8)
ax2 = ax.twinx(); ax2.plot(g.index.astype(str), g.sitasi, color="#e6550d", marker="o"); ax2.set_ylabel("Citations")
ax.set_title("Publications and citations per year (OpenAlex articles; 2026 is incomplete)", fontsize=9)
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
B0 = B.copy()  # graf penuh tanpa ambang sitasi dokumen; dipakai uji ketahanan dan keterangan bagian yang dibuang
bc0 = louvain(B0)
# Aturan pembimbing: 3-5 kluster, tiap kluster >=6 item. Ambang sitasi dokumen >=3 (OpenAlex), lalu kluster <6 dokumen dibuang (lihat sapu_ambang.py).
DOK_MIN_SITASI, KLUSTER_MIN = 3, 6
pilih = sorted(n for n in B0 if tt.loc[n, "cited_by"] >= DOK_MIN_SITASI)
B = nx.Graph(); B.add_nodes_from(pilih)  # simpul dan garis diurutkan supaya hasil Louvain tetap sama (sama dengan sapu_ambang.py)
for a, b in itertools.combinations(pilih, 2):
    if B0.has_edge(a, b):
        B.add_edge(a, b, weight=B0[a][b]["weight"])
B.remove_nodes_from([n for n in list(B) if B.degree(n) == 0])
bc_semua = louvain(B)
bc = [c for c in bc_semua if len(c) >= KLUSTER_MIN]
B = B.subgraph(set().union(*bc)).copy(); tls = kuat(B)
lab = {n: i for i, c in enumerate(bc, 1) for n in c}
teks += [f"## Bibliographic coupling\n", f"Dari {len(d)} dokumen, {len(refs)} punya data referensi; {B0.number_of_nodes()} terhubung (≥2 referensi sama) dan membentuk {len(bc0)} kluster (ukuran: {[len(c) for c in bc0]}) tanpa ambang. "
         f"Dengan ambang sitasi dokumen ≥{DOK_MIN_SITASI}: {len(bc_semua)} kluster (ukuran: {[len(c) for c in bc_semua]}); kluster <{KLUSTER_MIN} dokumen dibuang, sisa {B.number_of_nodes()} dokumen dalam {len(bc)} kluster (ukuran: {[len(c) for c in bc]}).\n"]
tb = sorted(B, key=lambda n: -tls[n])[:10]
t = pd.DataFrame({"Peringkat": range(1, 11), "Publikasi": [pub(n) for n in tb], "Sitasi": [tt.loc[n, "cited_by"] for n in tb], "TLS": [tls[n] for n in tb], "Kluster": [lab[n] for n in tb]})
teks += ["### Tabel B. Top 10 dokumen dalam analisis bibliographic coupling (menurut TLS)\n", md(t), ""]
rows = []
for i, c in enumerate(bc, 1):
    rep = sorted(c, key=lambda n: -tls[n])[:2]
    rows.append({"Kluster (warna)": f"{i} ({WARNA.get(i, '?')})", "Label kluster": nama_kluster("coupling", bc, i), "Jumlah publikasi": len(c),
                 "Blok asal": dict(Counter(tt.loc[n, 'blok'] for n in c)), "Publikasi representatif": "; ".join(pub(n) for n in rep)})
teks += ["### Tabel C. Ringkasan kluster bibliographic coupling (kluster ≥6 dokumen)\n", md(pd.DataFrame(rows)), ""]

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


def nama_belakang(nama):
    bagian = nama.replace(",", " ").split()
    return next((b for b in reversed(bagian) if len(b.rstrip(".")) > 1), bagian[-1] if bagian else "?")


# Koreksi manual atas nama penulis pertama yang terpotong di OpenAlex ("Tom B." untuk Brown dkk., NeurIPS 2020).
PENULIS_KOREKSI = {"Language Models are Few-Shot Learners": "Brown"}
TAHUN_KOREKSI = {"Attention Is All You Need": 2017}  # OpenAlex mencatat 2025 (rekaman ulang); terbit NeurIPS 2017


def rf(n):
    x = tipe.get(n, {})
    judul_ = x.get("judul", n)
    nama = next((v for k, v in PENULIS_KOREKSI.items() if judul_.startswith(k)), nama_belakang(x.get("pen", "?")))
    tahun = next((v for k, v in TAHUN_KOREKSI.items() if judul_.startswith(k)), x.get("tahun"))
    return f"{nama} ({tahun}), {cut(judul_, 80)}"


teks += ["## Co-citation\n", f"Dari {len(cit)} referensi unik, {len(keep)} memenuhi ambang 3 sitasi oleh dokumen kita (setelah {len(bad)} artefak dibuang), membentuk {len(cc)} kluster (ukuran: {[len(c) for c in cc]}).\n"]
tc = sorted(C, key=lambda n: -ctl[n])[:10]
t = pd.DataFrame({"Peringkat": range(1, 11), "Dokumen": [rf(n) for n in tc], "Sitasi (oleh dokumen kita)": [cit[n] for n in tc], "TLS": [ctl[n] for n in tc], "Kluster": [clab[n] for n in tc]})
teks += ["### Tabel D. Top 10 dokumen dengan co-citation dan TLS tertinggi\n", md(t), ""]
rows = []
for i, c in enumerate(cc, 1):
    rep = sorted(c, key=lambda n: -cit[n])[:2]
    rows.append({"Kluster (warna)": f"{i} ({WARNA.get(i, '?')})", "Label kluster": nama_kluster("cocit", cc, i), "Jumlah artikel": len(c), "Publikasi representatif": "; ".join(rf(n) for n in rep)})
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
    rows.append({"Kluster (warna)": f"{i} ({WARNA.get(i, '?')})", "Label kluster": nama_kluster("coword", kc, i), "Jumlah kata kunci": len(c), "Kata kunci representatif": ", ".join(rep)})
teks += ["### Tabel G. Ringkasan analisis co-word\n", md(pd.DataFrame(rows)), "",
         "Catatan: warna kluster mengikuti urutan standar VOSviewer (1 merah, 2 hijau, 3 biru, 4 kuning, 5 ungu); cocokkan dengan gambar yang kamu ekspor.\n"]
open(f"{OUT}/tabel_artikel.md", "w", encoding="utf-8").write("\n".join(teks))
print("ok | coupling", [len(c) for c in bc][:9], "| cocit", [len(c) for c in cc], "| coword", [len(c) for c in kc], "| kata unik", len(cnt))

# ---------- anggota kluster (untuk penamaan kluster dan pengecekan) ----------
json.dump({
    "coupling": [{"kluster": i, "docs": sorted(c, key=lambda n: -tls[n])} for i, c in enumerate(bc, 1)],
    "cocitation": [{"kluster": i, "refs": [{"id": n, "label": rf(n), "cit": cit[n]} for n in sorted(c, key=lambda n: -cit[n])]} for i, c in enumerate(cc, 1)],
    "coword": [{"kluster": i, "kw": sorted(c, key=lambda k: -cnt[k]), "cnt": {k: cnt[k] for k in c}} for i, c in enumerate(kc, 1)],
}, open(f"{OUT}/kluster_anggota.json", "w", encoding="utf-8"), ensure_ascii=False)

# ---------- ketahanan co-citation: 20 seed Louvain + greedy; apakah referensi rantai pasok tetap satu kelompok terpisah? ----------
SUPPLY = {n for n in C if any(k in rf(n) for k in ("Jackson", "Wamba", "AlMahri")) and "supply" in rf(n).lower() + tipe.get(n, {}).get("judul", "").lower() or (n in C and "supply chain" in tipe.get(n, {}).get("judul", "").lower())}
hasil = []
for seed in list(range(20)) + ["greedy"]:
    parts = list(nx.community.greedy_modularity_communities(C, weight="weight")) if seed == "greedy" else nx.community.louvain_communities(C, weight="weight", seed=seed)
    parts = sorted(parts, key=len, reverse=True)
    where = Counter(next(i for i, p in enumerate(parts) if n in p) for n in SUPPLY)
    k, jumlah = where.most_common(1)[0]
    kelompok = parts[k]
    hasil.append({"seed": seed, "jumlah_kluster": len(parts), "ukuran": str([len(p) for p in parts]), "ref_rantai_pasok": len(SUPPLY), "dalam_satu_kluster": jumlah,
                  "ukuran_kluster_itu": len(kelompok), "persen_rantai_pasok_di_kluster": round(100 * len(SUPPLY & kelompok) / len(kelompok), 1)})
pd.DataFrame(hasil).to_csv(f"{OUT}/ketahanan_cocitation.csv", index=False, encoding="utf-8-sig")
hh = pd.DataFrame(hasil)
print("co-citation ketahanan | referensi rantai pasok:", sorted(rf(n)[:45] for n in SUPPLY))
print(hh.groupby("jumlah_kluster").size().to_dict(), "| semua rantai pasok satu kluster di", int((hh.dalam_satu_kluster == hh.ref_rantai_pasok).sum()), "dari", len(hh), "| ukuran kluster rantai pasok:", sorted(hh.ukuran_kluster_itu.unique()))

# ---------- ketahanan coupling: dokumen blok A/C (bisnis) tetap berkelompok sendiri? ----------
bis = {n for n in B0 if tt.loc[n, "blok"] in ("A", "C", "A+C")}
hasil = []
for seed in list(range(20)) + ["greedy"]:  # graf penuh B0 (tanpa ambang sitasi dokumen)
    parts = list(nx.community.greedy_modularity_communities(B0, weight="weight")) if seed == "greedy" else nx.community.louvain_communities(B0, weight="weight", seed=seed)
    di_bisnis = sum(len(bis & p) for p in parts if len(bis & p) / len(p) >= 0.5)
    hasil.append({"seed": seed, "jumlah_kluster": len(parts), "dokumen_bisnis": len(bis), "di_kluster_bisnis": di_bisnis,
                  "persen": round(100 * di_bisnis / len(bis), 1), "kluster_terbesar": len(max(parts, key=len))})
hb = pd.DataFrame(hasil)
hb.to_csv(f"{OUT}/ketahanan_coupling.csv", index=False, encoding="utf-8-sig")
print(f"coupling ketahanan | dokumen bisnis terhubung: {len(bis)} dari {B0.number_of_nodes()} (graf penuh) | dokumen bisnis yang lolos ambang sitasi dan kluster >=6: {len({n for n in B if tt.loc[n, 'blok'] in ('A', 'C', 'A+C')})} | persen di kluster bisnis: min {hb.persen.min()}, median {hb.persen.median()}, maks {hb.persen.max()} | jumlah kluster: {sorted(hb.jumlah_kluster.unique())}")

# ---------- graf untuk gambar peta (dibaca peta_gambar.py) ----------
json.dump({
    "coword": {"nodes": [{"id": k, "n": cnt[k], "cluster": klab[k]} for k in G], "edges": [[a, b, w] for a, b, w in G.edges(data="weight")],
               "names": [nama_kluster("coword", kc, i) for i in range(1, len(kc) + 1)]},
    "cocit": {"nodes": [{"id": n, "label": rf(n), "n": cit[n], "cluster": clab[n]} for n in C], "edges": [[a, b, w] for a, b, w in C.edges(data="weight")],
              "names": [nama_kluster("cocit", cc, i) for i in range(1, len(cc) + 1)]},
}, open(f"{OUT}/graf.json", "w", encoding="utf-8"), ensure_ascii=False)
