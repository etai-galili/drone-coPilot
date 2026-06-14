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
  echo "[1/6] Creating virtual environment..."
  "$PYTHON" -m venv venv
else
  echo "[1/6] Virtual environment already exists."
fi

# Activate
# shellcheck disable=SC1091
source venv/bin/activate

echo "[2/6] Installing dependencies..."
pip install --upgrade pip --quiet
# On Apple Silicon, build llama-cpp-python with Metal GPU support for fast inference
if [ "$(uname -s)" = "Darwin" ] && [ "$(uname -m)" = "arm64" ]; then
  echo "      Detected Apple Silicon — enabling Metal GPU for llama-cpp-python..."
  CMAKE_ARGS="-DGGML_METAL=on" pip install llama-cpp-python --quiet --force-reinstall --no-cache-dir 2>/dev/null || \
  pip install llama-cpp-python --quiet
fi
pip install -r requirements.txt --quiet
echo "      Dependencies installed."

echo "[3/6] Fetching documentation..."
python scripts/fetch_docs.py

echo "[4/6] Chunking documents..."
python scripts/chunk_docs.py

echo "[5/6] Building vector index..."
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
