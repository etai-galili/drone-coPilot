#!/usr/bin/env bash
set -euo pipefail

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║         AVATA CO-PILOT — SETUP           ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Python version check
PYTHON=$(command -v python3 || command -v python || echo "")
if [ -z "$PYTHON" ]; then
  echo "[ERR] Python 3.10+ is required but not found."
  exit 1
fi
PY_VER=$("$PYTHON" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "[OK] Python $PY_VER"

# Virtual environment
if [ ! -d "venv" ]; then
  echo "[1/5] Creating virtual environment..."
  "$PYTHON" -m venv venv
else
  echo "[1/5] Virtual environment already exists."
fi

# Activate
# shellcheck disable=SC1091
source venv/bin/activate

echo "[2/5] Installing dependencies..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo "      Dependencies installed."

echo "[3/5] Fetching documentation..."
python scripts/fetch_docs.py

echo "[4/5] Chunking documents..."
python scripts/chunk_docs.py

echo "[5/5] Building vector index..."
python scripts/build_index.py

echo ""
echo "[6/6] Downloading LLM model..."
python scripts/setup_model.py

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║         SETUP COMPLETE                   ║"
echo "╠══════════════════════════════════════════╣"
echo "║  Run:  ./run.sh                          ║"
echo "║  Then open: http://127.0.0.1:7860        ║"
echo "╚══════════════════════════════════════════╝"
echo ""
