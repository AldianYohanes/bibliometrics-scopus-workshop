# bibliometrics-scopus-workshop

Artikel bibliometrik (LaTeX) tentang penelitian LLM di tiga arus: agen multi-agent, LLM di browser/perangkat, dan inventori usaha kecil. Data dari OpenAlex (artikel jurnal 2023-2026, dicari 28 Okt 2026). Proyek dari workshop publikasi Scopus dengan bibliometrik.

Format mengikuti `Template Bibliometric_citation, co-citation, co-word.docx` dari workshop (A4, margin 2,54 cm, Times New Roman 12 pt, tabel kisi penuh, keterangan tabel di atas, keterangan gambar di bawah, APA 7). Bagian tambahan di luar template: Methodology 3.3-3.4, Result 4.4-4.6, Limitations, Future research, Conclusion, Declarations.

Status: **draf awal**. Yang selesai: metode, hasil dengan angka dari skrip, tabel. Yang belum: konfirmasi label kluster oleh penulis, validasi manusia atas penyaringan, cek ulang di Scopus/WoS, dan baca penuh semua rujukan. Semua yang belum selesai ditandai `\todo{...}` (merah di PDF).

## Struktur
```
paper/       naskah LaTeX (main.tex, sections/, tables/, figures/, refs.bib)
analysis/    skrip Python, data, dan hasil analisis
  Skrip/     unduh_openalex.py, lengkapi_referensi.py, analisis_awal.py, analisis_tambahan.py,
             uji_ketahanan.py, tabel_template.py, md2tex.py
  Data/      dataset_lolos.csv (485 paper), referensi_tambahan.csv, penyaringan_gabungan.csv
  Hasil/     tabel, gambar, dan file masukan VOSviewer
```

## Kompilasi
Pakai XeLaTeX + biber (MiKTeX); daftar pustaka APA 7 lewat biblatex. Jika `latexmk` gagal karena PATH memuat `claude.exe`, saring PATH dulu.
```bash
cd paper
xelatex main && biber main && xelatex main && xelatex main
```

## Mengulang analisis
Dari folder `analysis/Skrip`:
```bash
python -I tabel_template.py   # tabel dan gambar dari dataset_lolos.csv
python -I md2tex.py           # tabel ke LaTeX di paper/tables (gaya template), gambar ke paper/figures
python -I csv2tex.py          # tabel penulis, sumber, sensitivitas, tren, peta tema
python -I gambar_ringkasan.py # Gambar 1 (ringkasan publikasi, sitasi, h-index)
python -I peta_gambar.py      # gambar peta co-word, co-citation, tren (dari Hasil/graf.json)
python -I ambil_rujukan.py    # paper/refs_tambahan.bib dari OpenAlex
```
`unduh_openalex.py` dan `lengkapi_referensi.py` butuh kunci API OpenAlex di `~/Tools/openalex.key` (jangan dimasukkan ke repo).
Hasil pengelompokan diulang dengan urutan simpul yang diurutkan dan seed tetap, jadi sama antar jalankan.

## Catatan
- Catatan kerja lengkap (keputusan, angka, masalah) ada di vault Obsidian, folder `SCOPUS Bibliometrics`.
- Rujukan: `paper/refs.bib` (metode) dan `paper/refs_tambahan.bib` (Introduction dan Literature Review, dibuat dari OpenAlex; daftar penulis dipotong 6 + others, lengkapi sebelum submit). Baru dicek ada (judul, penulis pertama, DOI), belum dicek volume dan halaman.
- Gambar peta di `paper/figures` dibuat dengan Python; ganti dengan ekspor VOSviewer sebelum submit.
- Penyaringan dibantu model bahasa (Claude); pengungkapan AI ada di bagian Declarations.
