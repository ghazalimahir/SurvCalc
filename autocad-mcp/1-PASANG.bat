@echo off
chcp 65001 >nul 2>&1
setlocal
title 1 - Pasang autocad-mcp
cd /d "%~dp0"

echo ============================================================
echo   LANGKAH 1 - PASANG KEPERLUAN
echo ============================================================
echo.

set "PYCMD="
py -3 --version >nul 2>&1
if not errorlevel 1 set "PYCMD=py -3"
if not defined PYCMD (
    python --version >nul 2>&1
    if not errorlevel 1 set "PYCMD=python"
)

if not defined PYCMD (
    echo   [TIADA PYTHON]
    echo.
    echo   Python belum dipasang. Buat sekali sahaja:
    echo.
    echo     1. Buka  https://www.python.org/downloads/windows/
    echo     2. Muat turun "Windows installer ^(64-bit^)"
    echo     3. SEMASA PASANG, tandakan kotak di bawah skrin:
    echo.
    echo            [x]  Add python.exe to PATH
    echo.
    echo        ^(kotak ini PENTING - kalau terlepas, ulang pemasangan^)
    echo     4. Klik "Install Now", tunggu siap
    echo     5. Klik dua kali fail ini semula
    echo.
    goto habis
)

echo   Python dijumpai: %PYCMD%
%PYCMD% --version
echo.
echo   Memasang pywin32 dan mcp. Tunggu sebentar...
echo.

%PYCMD% -m pip install --upgrade pip
%PYCMD% -m pip install -r requirements.txt

echo.
if errorlevel 1 (
    echo   [GAGAL] Pemasangan tidak berjaya.
    echo   Salin mesej merah di atas dan tunjuk kepada Claude.
) else (
    echo   ============================================================
    echo     SIAP. Seterusnya:
    echo.
    echo       1. Buka AutoCAD, buka satu gambar
    echo       2. Klik dua kali  2-UJI.bat
    echo   ============================================================
)

:habis
echo.
pause
