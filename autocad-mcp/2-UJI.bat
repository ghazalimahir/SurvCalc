@echo off
chcp 65001 >nul 2>&1
setlocal
title 2 - Uji sambungan AutoCAD
cd /d "%~dp0"

echo ============================================================
echo   LANGKAH 2 - UJI SAMBUNGAN ^(BACA SAHAJA^)
echo ============================================================
echo.
echo   Fail ini TIDAK mengubah gambar anda. Ia hanya membaca.
echo.
echo   Pastikan dahulu:
echo     - AutoCAD sudah dibuka
echo     - Ada satu gambar terbuka ^(bukan skrin mula sahaja^)
echo     - Tiada dialog atau command sedang berjalan ^(tekan ESC^)
echo.
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

%PYCMD% probe_acad.py

echo.
echo ============================================================
echo   Salin SEMUA teks di atas dan tunjuk kepada Claude,
echo   sama ada ia berjaya atau gagal.
echo.
echo   Kalau berjaya, cuba pula  3-UJI-LUKIS.bat
echo ============================================================

:habis
echo.
pause
