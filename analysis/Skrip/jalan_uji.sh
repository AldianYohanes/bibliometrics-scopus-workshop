#!/bin/bash
# Jalankan analisis untuk data uji kepekaan (Data/dataset_lolos_N.csv, autor_sumber_N.csv, referensi_tambahan_N.csv)
# dengan menukar sementara file data utama, lalu kembalikan. Pakai: bash jalan_uji.sh 720  -> hasil di analysis/Hasil_uji720
set -e
A=$(cd "$(dirname "$0")/.." && pwd)
S=${TMPDIR:-/tmp}/bibliometrik_uji  # cadangan sementara dan log
N=$1
export PYTHONIOENCODING=utf-8
rm -rf $S/tukar && mkdir -p $S/tukar
cp $A/Data/dataset_lolos.csv $A/Data/autor_sumber.csv $A/Data/referensi_tambahan.csv $S/tukar/
cp -r $A/Hasil $S/tukar/Hasil
cp -r $A/../paper/tables $S/tukar/tables
cp -r $A/../paper/figures $S/tukar/figures
pulihkan() {
  cp $S/tukar/dataset_lolos.csv $S/tukar/autor_sumber.csv $S/tukar/referensi_tambahan.csv $A/Data/
  rm -rf $A/Hasil && cp -r $S/tukar/Hasil $A/Hasil
  rm -rf $A/../paper/tables && cp -r $S/tukar/tables $A/../paper/tables
  rm -rf $A/../paper/figures && cp -r $S/tukar/figures $A/../paper/figures
  echo dipulihkan
}
trap pulihkan EXIT
cp $A/Data/dataset_lolos_$N.csv $A/Data/dataset_lolos.csv
cp $A/Data/autor_sumber_$N.csv $A/Data/autor_sumber.csv
cp $A/Data/referensi_tambahan_$N.csv $A/Data/referensi_tambahan.csv
cd $A/Skrip
python -I kinerja_id.py > $S/loguji_kinerja.txt 2>&1
for f in analisis_awal analisis_tambahan uji_ketahanan tabel_template sapu_ambang gambar_ringkasan; do
  python -I $f.py > $S/loguji_$f.txt 2>&1
done
rm -rf $A/Hasil_uji$N && mkdir -p $A/Hasil_uji$N
for f in sapu_ambang.csv ketahanan.csv ketahanan_cocitation.csv ketahanan_coupling.csv kinerja_tahun.csv ringkasan_sitasi.csv kinerja_negara.csv kinerja_id_sumber.csv coword_kluster.csv cocitation_kluster.csv coupling_v3_kluster.csv tabel_artikel.md; do
  cp $A/Hasil/$f $A/Hasil_uji$N/
done
echo selesai $N, log di $S
