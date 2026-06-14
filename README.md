# AVATA CO-PILOT

**Offline AI field assistant for DJI Avata drone operators.**  
Runs 100% locally — no internet, no cloud, no Docker.

---

## Quick Start

### macOS / Linux
```bash
chmod +x setup.sh run.sh
./setup.sh      # one-time setup (~5 min)
./run.sh        # launch the UI
```

### Windows
```
setup.bat
run.bat
```

Then open **http://127.0.0.1:7860** in your browser.

---

## What setup.sh does

| Step | Action |
|------|--------|
| 1 | Creates Python virtual environment |
| 2 | Installs all dependencies from requirements.txt |
| 3 | Builds the knowledge base from curated, verified **DJI Avata 2** docs in `data/seed/` |
| 4 | Chunks text (400 tokens, 80 token overlap) |
| 5 | Builds ChromaDB vector index |
| 6 | Downloads Qwen2.5-1.5B-Instruct Q4_K_M (~1 GB) |

> The knowledge base is built from a **curated, version-controlled set of verified
> DJI Avata 2 documents** (`data/seed/`) covering system familiarization, the operating
> manual, operator instructions, the electrical/power system, the camera/imaging system,
> the mechanical/propulsion system, known faults & troubleshooting, emergency procedures,
> and a full specifications reference. This makes answers deterministic and trustworthy.
> Web scraping is optional and **off by default** — run `python scripts/fetch_docs.py --web`
> to pull supplementary online sources.

---

## Features

| Tab | Function |
|-----|----------|
| Ask Co-Pilot | Free-form Q&A with RAG pipeline + severity tagging |
| Pre-Flight | Mission-specific checklist generator with progress tracking |
| Anomaly Diagnosis | Symptom + telemetry diagnosis with severity/abort decision |
| Quick Reference | Static specs, emergency procedures, modes, LED codes |
| System Status | Live model/KB/RAM status + self-test runner |

---

## Architecture

```
User Question
     │
     ▼
Embed (MiniLM-L6-v2)
     │
     ▼
ChromaDB vector search → top-4 chunks
     │
     ▼
Build ChatML prompt (SYSTEM + context + question)
     │
     ▼
Qwen2.5-1.5B Instruct Q4_K_M (llama-cpp-python)
     │
     ▼
Answer + severity tag + sources + latency_ms
```

---

## Requirements

- Python 3.10+
- ~2 GB disk (model + index)
- ~2.5 GB RAM minimum
- No GPU required (CPU inference)

---

## Updating or Adding Documentation

The authoritative knowledge base lives in `data/seed/` as plain `.txt` files
(version-controlled). To update facts or add a new model:

1. Edit or add `.txt` files in `data/seed/` (keep specs verified and accurate).
2. Re-run: `python scripts/fetch_docs.py && python scripts/chunk_docs.py && python scripts/build_index.py`
3. Restart the app — no code changes needed.

(`fetch_docs.py` copies the verified seed docs into `data/raw/`; add `--web` to also
pull supplementary online sources.)

---

## Running the Benchmark

```bash
source venv/bin/activate
python -m pytest tests/test_pipeline.py -v
```

Pass threshold: 8/10 benchmark questions.

---

## Project Structure

```
drone-co-pilot/
├── data/
│   ├── seed/          # Curated, verified Avata 2 docs (version-controlled)
│   ├── raw/           # Built knowledge base (.txt, from seed + optional web)
│   ├── chunks/        # all_chunks.jsonl
│   └── chroma_db/     # ChromaDB vector store
├── models/            # GGUF model file (gitignored)
├── engine/
│   ├── llm_client.py  # LocalLLMClient (llama-cpp)
│   ├── rag_pipeline.py # DroneCoPilot RAG logic
│   └── prompts.py     # ChatML prompt builder
├── ui/
│   └── app.py         # Gradio tactical UI (5 tabs)
├── scripts/
│   ├── fetch_docs.py  # Web scraper
│   ├── chunk_docs.py  # Tiktoken chunker
│   ├── build_index.py # ChromaDB indexer
│   └── setup_model.py # Model downloader
├── tests/
│   └── test_pipeline.py
├── setup.sh / setup.bat
├── run.sh / run.bat
└── requirements.txt
```

---

All code, UI, and responses are in **English only**.  
Offline after initial setup. No Docker. No cloud.
