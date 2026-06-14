@echo off
setlocal

if not exist "venv\Scripts\activate.bat" (
    echo [ERR] Virtual environment not found. Run setup.bat first.
    pause
    exit /b 1
)

if not exist "config.json" (
    echo [ERR] config.json not found. Run setup.bat first.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo.
echo ╔══════════════════════════════════════════╗
echo ║         AVATA CO-PILOT — LAUNCH          ║
echo ╠══════════════════════════════════════════╣
echo ║  URL: http://127.0.0.1:7860              ║
echo ║  Press Ctrl+C to stop                    ║
echo ╚══════════════════════════════════════════╝
echo.

python ui\app.py
