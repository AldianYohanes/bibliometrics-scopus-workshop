# Ekspor gambar peta dari VOSviewer lewat parameter baris perintah (manual VOSviewer 1.6.21, bab 5.1: save_screenshot_png).
# Tiap ekspor butuh sekitar 1 menit (layout dan render), lalu proses VOSviewer milik skrip ini dihentikan.
# Proses VOSviewer lain yang sedang dibuka (mis. jendela yang dipakai penulis) tidak disentuh: hanya proses yang baris perintahnya memuat nama berkas keluaran.
# Jalankan: powershell -File vos_export.ps1   (ubah $Vos jika VOSviewer ada di folder lain)
param(
  [string]$Vos = 'C:\Users\aldia\Tools\VOSviewer\VOSviewer.exe',
  [string]$Hasil = (Join-Path (Split-Path -Parent $PSScriptRoot) 'Hasil'),
  [string]$Keluar = (Join-Path (Split-Path -Parent $PSScriptRoot) 'Hasil\vos_full')
)
# Setelah ini jalankan: python -I redimensi_vos.py  (memotong tepi putih dan mengecilkan ke paper/figures)
# Catatan: tunggu ukuran berkas stabil sebelum menghentikan VOSviewer, kalau tidak PNG terpotong (pernah terjadi pada percobaan pertama).
New-Item -ItemType Directory -Force $Keluar | Out-Null

function Export-Peta($nama, $peta, $jaringan, $tambahan) {
  $png = Join-Path $Keluar $nama
  if (Test-Path $png) { Remove-Item $png -Force }
  $argumen = @('-map', (Join-Path $Hasil $peta), '-network', (Join-Path $Hasil $jaringan), '-save_screenshot_png', $png, '-white_background', 'true') + $tambahan
  $p = Start-Process -FilePath $Vos -ArgumentList $argumen -PassThru
  $selesai = $false; $terakhir = -1; $stabil = 0
  for ($i = 0; $i -lt 150; $i++) {
    Start-Sleep -Seconds 2
    if (Test-Path $png) {
      $len = (Get-Item $png).Length
      if ($len -gt 100000 -and $len -eq $terakhir) { $stabil++ } else { $stabil = 0 }
      $terakhir = $len
      if ($stabil -ge 4) { $selesai = $true; break }
    }
  }
  # hentikan hanya proses yang membawa nama berkas keluaran ini
  Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -and $_.CommandLine.Contains($nama) } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
  if ($selesai) { "{0}: {1:N1} MB" -f $nama, ((Get-Item $png).Length / 1MB) } else { "${nama}: GAGAL (tidak ada berkas)" }
}

Export-Peta 'vos_coword.png' 'vos_coword_map.txt' 'vos_coword_network.txt' @()
Export-Peta 'vos_cocitation.png' 'vos_cocitation_map.txt' 'vos_cocitation_network.txt' @()
Export-Peta 'vos_tren.png' 'vos_tren_map.txt' 'vos_tren_network.txt' @('-overlay_visualization')
