@echo off
chcp 65001 >nul 2>&1
setlocal
title 3 - Uji melukis dalam AutoCAD
cd /d "%~dp0"

echo ============================================================
echo   LANGKAH 3 - UJI MELUKIS
echo ============================================================
echo.
echo   Fail ini AKAN menambah bentuk pada gambar yang terbuka:
echo     - satu garisan, satu bulatan, satu teks
echo     - semuanya pada layer  CLAUDE_UJIAN  ^(warna merah^)
echo.
echo   Senang dipadam selepas itu, dan ia TIDAK menyimpan gambar.
echo   Sebaiknya guna gambar kosong dahulu.
echo.
echo   Tekan CTRL+C untuk berhenti, atau...
pause
echo.

set "PYCMD="
py -3 --version >nul 2>&1
if not errorlevel 1 set "PYCMD=py -3"
if not defined PYCMD (
    python --version >nul 2>&1
    if not errorlevel 1 set "PYCMD=python"
)
if not defined PYCMD (
    echo   [TIADA PYTHON] Klik dua kali 1-PASANG.bat dahulu.
    goto habis
)

%PYCMD% probe_acad.py --draw

echo.
echo ============================================================
echo   Lihat AutoCAD sekarang - ada garisan, bulatan dan teks?
echo.
echo   Untuk padam:  taip  LAYER  pilih CLAUDE_UJIAN, atau
echo                 taip  ERASE  kemudian pilih bentuk itu
echo.
echo   Salin teks di atas dan tunjuk kepada Claude.
echo ============================================================

:habis
echo.
pause
