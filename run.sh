#!/usr/bin/env bash
set -euo pipefail

if [ ! -f "venv/bin/activate" ]; then
  echo "[ERR] Virtual environment not found. Run ./setup.sh first."
  exit 1
fi

if [ ! -f "config.json" ]; then
  echo "[ERR] config.json not found. Run ./setup.sh first."
  exit 1
fi

# shellcheck disable=SC1091
source venv/bin/activate

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║        PROFWORXML v.1 — LAUNCH           ║"
echo "╠══════════════════════════════════════════╣"
echo "║  URL: http://127.0.0.1:7860              ║"
echo "║  Press Ctrl+C to stop                    ║"
echo "╚══════════════════════════════════════════╝"
echo ""

python ui/app.py
