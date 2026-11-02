@echo off
chcp 65001 >nul 2>&1
setlocal
title 4 - Daftar AutoCAD kepada Claude Code
cd /d "%~dp0"

echo ============================================================
echo   LANGKAH 4 - SAMBUNG KE CLAUDE CODE
echo ============================================================
echo.
echo   Buat ini SELEPAS 2-UJI.bat berjaya.
echo   Laluan fail dikira sendiri - anda tidak perlu taip apa-apa.
echo.

where claude >nul 2>&1
if errorlevel 1 (
    echo   [TIADA CLAUDE CODE]
    echo.
    echo   Claude Code belum dipasang di PC ini, atau belum masuk PATH.
    echo   Pasang dari:  https://claude.ai/download
    echo.
    echo   Ingat: Claude di laman web ^(claude.ai/code^) TIDAK boleh
    echo   guna ini. Ia berjalan di awan dan tidak nampak PC anda.
    echo   Claude mesti berjalan DI PC INI.
    echo.
    goto habis
)

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

echo   Mendaftar server "autocad"...
echo.
call claude mcp add autocad -- %PYCMD% "%~dp0acad_mcp.py"

echo.
if errorlevel 1 (
    echo   [GAGAL] Salin mesej di atas dan tunjuk kepada Claude.
) else (
    echo   ============================================================
    echo     SIAP. Cara guna:
    echo.
    echo       1. Buka AutoCAD dengan satu gambar
    echo       2. Buka Claude Code di PC ini
    echo       3. Taip  /mcp   untuk pastikan "autocad" tersenarai
    echo       4. Minta sahaja, contoh:
    echo            "periksa status autocad"
    echo            "lukis garisan dari 0,0 ke 100,50"
    echo            "plot titik traverse ini dan labelkan"
    echo   ============================================================
)

:habis
echo.
pause
