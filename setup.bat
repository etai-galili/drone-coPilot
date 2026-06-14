@echo off
setlocal enabledelayedexpansion

echo.
echo ╔══════════════════════════════════════════╗
echo ║         AVATA CO-PILOT — SETUP           ║
echo ╚══════════════════════════════════════════╝
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo [ERR] Python not found. Install Python 3.10+ and add it to PATH.
    pause
    exit /b 1
)

if not exist "venv\" (
    echo [1/6] Creating virtual environment...
    python -m venv venv
) else (
    echo [1/6] Virtual environment already exists.
)

call venv\Scripts\activate.bat

echo [2/6] Installing dependencies...
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo       Dependencies installed.

echo [3/6] Fetching documentation...
python scripts\fetch_docs.py

echo [4/6] Chunking documents...
python scripts\chunk_docs.py

echo [5/6] Building vector index...
python scripts\build_index.py

echo [6/6] Downloading LLM model...
python scripts\setup_model.py

echo.
echo ╔══════════════════════════════════════════╗
echo ║         SETUP COMPLETE                   ║
echo ╠══════════════════════════════════════════╣
echo ║  Run:  run.bat                           ║
echo ║  Then open: http://127.0.0.1:7860        ║
echo ╚══════════════════════════════════════════╝
echo.
pause
