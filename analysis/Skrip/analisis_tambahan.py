"""Analisis tambahan: co-citation, coupling dengan referensi lengkap (OpenAlex + Crossref), peta tren, kolaborasi.

Masukan: Data/dataset_lolos.csv, Data/referensi_tambahan.csv. Keluaran: Hasil/ (tabel, PNG, file VOSviewer).
Kunci OpenAlex dibaca dari ~/Tools/openalex.key (dipakai hanya untuk memberi judul pada referensi teratas).
Jalankan: python -I analisis_tambahan.py
"""
import csv, itertools, json, os, sys, time, urllib.parse, urllib.request
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
d = pd.read_csv(os.path.join(ROOT, "Data", "dataset_lolos.csv"), encoding="utf-8-sig").fillna("")
extra = pd.read_csv(os.path.join(ROOT, "Data", "referensi_tambahan.csv"), encoding="utf-8-sig").fillna("")
ex = dict(zip(extra.id, extra.referenced_works))
d["refs_all"] = [r if r else ex.get(i, "") for i, r in zip(d.id, d.referenced_works)]
withref = d[d.refs_all != ""].copy()
print(f"dokumen: {len(d)} | punya referensi (OpenAlex + Crossref): {len(withref)} ({100*len(withref)/len(d):.1f}%)")
refs = {r.id: set(r.refs_all.split("|")) for r in withref.itertuples()}


def louvain(G):
    return sorted(nx.community.louvain_communities(G, weight="weight", seed=SEED), key=len, reverse=True)


# Referensi yang dibuang dari co-citation karena diduga artefak data (bukan karya yang sebenarnya dikutip):
# - W4385245566 dikutip 22 dokumen edge-LLM padahal judulnya tentang sistem tutor cerdas; dugaan salah tautan OpenAlex.
# - jilid prosiding ("Proceedings of ...", tipe proceedings) bukan satu karya.
CURIGA = {"https://openalex.org/W4385245566", "https://openalex.org/W4292779060", "https://openalex.org/W4384918448"}
TIPE = {}


def judul(ids):
    """ID OpenAlex -> 'Penulis Tahun, Judul' (batch 50)."""
    out, ids = {}, list(ids)
    for i in range(0, len(ids), 50):
        q = {"filter": "openalex_id:" + "|".join(ids[i:i + 50]), "per-page": 50, "select": "id,display_name,publication_year,authorships,type", "api_key": KEY}
        with urllib.request.urlopen("https://api.openalex.org/works?" + urllib.parse.urlencode(q), timeout=60) as r:
            for w in json.load(r)["results"]:
                a = ((w.get("authorships") or [{}])[0].get("author") or {}).get("display_name", "?")
                out[w["id"]] = f"{a.split()[-1] if a else '?'} {w.get('publication_year')}, {(w.get('display_name') or '')[:70]}"
                TIPE[w["id"]] = (w.get("type") or "", w.get("display_name") or "")
        time.sleep(0.1)
    return out


# ---------- bibliographic coupling (referensi lengkap) ----------
B = nx.Graph()
ids = list(refs)
B.add_nodes_from(ids)
for a, b in itertools.combinations(ids, 2):
    s = len(refs[a] & refs[b])
    if s >= 2:
        B.add_edge(a, b, weight=s)
B.remove_nodes_from([n for n in list(B) if B.degree(n) == 0])
bc = louvain(B)
tt = d.set_index("id")
rows = []
for i, c in enumerate(bc, 1):
    top = sorted(c, key=lambda n: -tt.loc[n, "cited_by"])[:3]
    rows.append({"kluster": i, "jumlah_dokumen": len(c), "blok": str(dict(Counter(tt.loc[n, "blok"] for n in c))),
                 "contoh_judul": " || ".join(tt.loc[n, "title"][:70] for n in top)})
pd.DataFrame(rows).to_csv(f"{OUT}/coupling_v3_kluster.csv", index=False, encoding="utf-8-sig")
print(f"coupling v3: {B.number_of_nodes()} dokumen terhubung, {B.number_of_edges()} garis, {len(bc)} kluster; ukuran: {[len(c) for c in bc][:9]}")

# ---------- co-citation ----------
cit = Counter(r for s in refs.values() for r in s)
dist = Counter(min(c, 10) for c in cit.values())
print("referensi unik:", len(cit), "| dikutip >=2 dokumen:", sum(1 for c in cit.values() if c >= 2), "| >=3:", sum(1 for c in cit.values() if c >= 3), "| >=5:", sum(1 for c in cit.values() if c >= 5))
MIN_CIT = 3
keep = {r for r, c in cit.items() if c >= MIN_CIT}
judul(keep)
buang = {r for r in keep if r in CURIGA or TIPE.get(r, ("", ""))[0] == "proceedings" or TIPE.get(r, ("", ""))[1].lower().startswith(("proceedings of", "findings of"))}
print("referensi dibuang dari co-citation (artefak):", len(buang))
keep -= buang
C = nx.Graph()
for r in sorted(keep):
    C.add_node(r, n=cit[r])
for s in refs.values():
    for a, b in itertools.combinations(sorted(s & keep), 2):
        C.add_edge(a, b, weight=C.get_edge_data(a, b, {"weight": 0})["weight"] + 1)
C.remove_nodes_from([n for n in list(C) if C.degree(n) == 0])
cc = louvain(C)
lab = judul(C.nodes)
for i, c in enumerate(cc, 1):
    for n in c:
        C.nodes[n]["cluster"] = i
rows = []
for i, c in enumerate(cc, 1):
    top = sorted(c, key=lambda n: -cit[n])[:6]
    rows.append({"kluster": i, "jumlah_referensi": len(c), "referensi_teratas": " || ".join(f"{lab.get(n, n)} (x{cit[n]})" for n in top)})
pd.DataFrame(rows).to_csv(f"{OUT}/cocitation_kluster.csv", index=False, encoding="utf-8-sig")
pd.DataFrame([{"referensi": lab.get(n, n), "dikutip_oleh_dokumen": cit[n], "kluster": C.nodes[n]["cluster"]} for n in sorted(C, key=lambda n: -cit[n])[:30]]).to_csv(f"{OUT}/cocitation_teratas.csv", index=False, encoding="utf-8-sig")
print(f"co-citation (min {MIN_CIT} sitasi): {C.number_of_nodes()} referensi, {C.number_of_edges()} garis, {len(cc)} kluster; ukuran: {[len(c) for c in cc]}")
pos = nx.spring_layout(C, weight="weight", seed=SEED, k=0.8)
fig, ax = plt.subplots(figsize=(13, 9))
cm = plt.get_cmap("tab10")
nx.draw_networkx_edges(C, pos, alpha=0.1, width=0.4, ax=ax)
nx.draw_networkx_nodes(C, pos, node_size=[30 + 14 * cit[n] for n in C], node_color=[cm((C.nodes[n]["cluster"] - 1) % 10) for n in C], alpha=0.85, ax=ax)
nx.draw_networkx_labels(C, pos, labels={n: lab.get(n, "")[:28] for n in sorted(C, key=lambda n: -cit[n])[:25]}, font_size=6.5, ax=ax)
ax.set_title("Co-citation map (references co-cited by at least 3 articles)"); ax.axis("off")
fig.tight_layout(); fig.savefig(f"{OUT}/peta_cocitation.png", dpi=130); plt.close(fig)
idx = {n: i for i, n in enumerate(C, 1)}
with open(f"{OUT}/vos_cocitation_map.txt", "w", encoding="utf-8") as f:
    f.write("id\tlabel\tx\ty\tcluster\tweight<Citations>\n")
    for n in C:
        f.write(f"{idx[n]}\t{lab.get(n, n)[:60].replace(chr(9), ' ')}\t{pos[n][0]:.4f}\t{pos[n][1]:.4f}\t{C.nodes[n]['cluster']}\t{cit[n]}\n")
with open(f"{OUT}/vos_cocitation_network.txt", "w", encoding="utf-8") as f:
    for a, b, w in C.edges(data="weight"):
        f.write(f"{idx[a]}\t{idx[b]}\t{w}\n")

# ---------- peta tren (rata-rata tahun per kata kunci) ----------
SIN = {"llm": "large language model", "llms": "large language model", "large language models": "large language model",
       "language model": "large language model", "language models": "large language model", "ai": "artificial intelligence"}
BUANG = {"large language model", "artificial intelligence"}
kws = [sorted({SIN.get(k.strip().lower(), k.strip().lower()) for k in s.split(";") if k.strip()} - BUANG) for s in d.keywords]
yrs = d.year.tolist()
cnt, ysum = Counter(), Counter()
for ks, y in zip(kws, yrs):
    for k in ks:
        cnt[k] += 1
        ysum[k] += int(y)
keep = {k for k, c in cnt.items() if c >= 8}
G = nx.Graph()
for k in sorted(keep):
    G.add_node(k, n=cnt[k], y=ysum[k] / cnt[k])
for ks in kws:
    for a, b in itertools.combinations([k for k in ks if k in keep], 2):
        G.add_edge(a, b, weight=G.get_edge_data(a, b, {"weight": 0})["weight"] + 1)
G.remove_nodes_from([n for n in list(G) if G.degree(n) == 0])
tr = pd.DataFrame([{"kata": k, "dokumen": cnt[k], "rata_rata_tahun": round(ysum[k] / cnt[k], 2)} for k in G]).sort_values("rata_rata_tahun")
tr.to_csv(f"{OUT}/tren_kata_kunci.csv", index=False, encoding="utf-8-sig")
print("kata tertua (rata-rata tahun):", tr.head(5).kata.tolist(), "| terbaru:", tr.tail(5).kata.tolist())
pos = nx.spring_layout(G, weight="weight", seed=SEED, k=0.9)
fig, ax = plt.subplots(figsize=(13, 9))
nx.draw_networkx_edges(G, pos, alpha=0.1, width=0.4, ax=ax)
sc = nx.draw_networkx_nodes(G, pos, node_size=[40 + 14 * G.nodes[n]["n"] for n in G], node_color=[G.nodes[n]["y"] for n in G], cmap="viridis", alpha=0.9, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=7, ax=ax)
plt.colorbar(sc, ax=ax, shrink=0.6, label="mean publication year")
ax.set_title("Co-word map, colour = mean publication year (yellow = more recent)"); ax.axis("off")
fig.tight_layout(); fig.savefig(f"{OUT}/peta_tren.png", dpi=130); plt.close(fig)
idx = {k: i for i, k in enumerate(G, 1)}
com = {k: i for i, c in enumerate(louvain(G), 1) for k in c}
with open(f"{OUT}/vos_tren_map.txt", "w", encoding="utf-8") as f:
    f.write("id\tlabel\tx\ty\tcluster\tweight<Occurrences>\tscore<Avg. pub. year>\n")
    for k in G:
        f.write(f"{idx[k]}\t{k}\t{pos[k][0]:.4f}\t{pos[k][1]:.4f}\t{com[k]}\t{G.nodes[k]['n']}\t{G.nodes[k]['y']:.2f}\n")
with open(f"{OUT}/vos_tren_network.txt", "w", encoding="utf-8") as f:
    for a, b, w in G.edges(data="weight"):
        f.write(f"{idx[a]}\t{idx[b]}\t{w}\n")

# ---------- kolaborasi negara dan penulis ----------
cs = [sorted(set(x for x in s.split("; ") if x)) for s in d.countries]
cc_cnt = Counter(c for s in cs for c in s)
CG = nx.Graph()
for c, n in cc_cnt.items():
    if n >= 8:
        CG.add_node(c, n=n)
for s in cs:
    for a, b in itertools.combinations([c for c in s if c in CG], 2):
        CG.add_edge(a, b, weight=CG.get_edge_data(a, b, {"weight": 0})["weight"] + 1)
pairs = sorted(((a, b, w) for a, b, w in CG.edges(data="weight")), key=lambda x: -x[2])
pd.DataFrame(pairs, columns=["negara_1", "negara_2", "paper_bersama"]).head(20).to_csv(f"{OUT}/kolaborasi_negara.csv", index=False, encoding="utf-8-sig")
multi = sum(1 for s in cs if len(s) >= 2)
print(f"kolaborasi negara: {multi} dari {len(d)} paper ({100*multi/len(d):.0f}%) punya >=2 negara; pasangan teratas: {pairs[:3]}")
pos = nx.spring_layout(CG, weight="weight", seed=SEED, k=1.2)
fig, ax = plt.subplots(figsize=(9, 7))
nx.draw_networkx_edges(CG, pos, width=[0.3 + 0.35 * CG[u][v]["weight"] for u, v in CG.edges], alpha=0.35, ax=ax)
nx.draw_networkx_nodes(CG, pos, node_size=[60 + 9 * CG.nodes[n]["n"] for n in CG], node_color="#2b8cbe", alpha=0.85, ax=ax)
nx.draw_networkx_labels(CG, pos, font_size=8, ax=ax)
ax.set_title("Collaboration between countries (countries with at least 8 articles)"); ax.axis("off")
fig.tight_layout(); fig.savefig(f"{OUT}/peta_kolaborasi_negara.png", dpi=130); plt.close(fig)

au = [[x for x in s.split("; ") if x] for s in d.authors]
ac = Counter(a for s in au for a in s)
ap = Counter(p for s in au for p in itertools.combinations(sorted(s), 2) if ac[p[0]] >= 2 and ac[p[1]] >= 2)
pd.DataFrame([{"penulis": a, "dokumen": n} for a, n in ac.most_common(15)]).to_csv(f"{OUT}/kolaborasi_penulis_teratas.csv", index=False, encoding="utf-8-sig")
pd.DataFrame([{"penulis_1": a, "penulis_2": b, "paper_bersama": w} for (a, b), w in ap.most_common(15)]).to_csv(f"{OUT}/kolaborasi_penulis_pasangan.csv", index=False, encoding="utf-8-sig")
solo = sum(1 for s in au if len(s) == 1)
print(f"penulis: {len(ac)} unik; paper satu penulis: {solo}; rata-rata penulis/paper: {sum(len(s) for s in au)/len(au):.2f}; penulis dgn >=3 paper: {sum(1 for n in ac.values() if n>=3)}")
