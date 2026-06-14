"""
10-question benchmark for the DroneCoPilot RAG pipeline.
Run after setup is complete: python -m pytest tests/test_pipeline.py -v
"""

import json
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

CONFIG_PATH = Path("config.json")

BENCHMARK: list[tuple[str, list[str]]] = [
    ("What is the maximum flight time of the DJI Avata?", ["18", "min"]),
    ("What is the maximum speed in Sport mode?", ["97", "km"]),
    ("How do I activate Return to Home on the DJI Avata?", ["rth", "button", "return"]),
    ("What does a blinking red LED indicate?", ["battery", "low"]),
    ("What is the maximum video transmission range?", ["10", "km", "range"]),
    ("What is M-Mode on the DJI Avata?", ["manual", "stabiliz"]),
    ("How many GPS satellites are needed for stable flight?", ["satellite", "gps"]),
    ("What is the emergency stop procedure?", ["switch", "stop", "arm"]),
    ("What is the maximum wind resistance of the DJI Avata?", ["10.7", "wind", "level"]),
    ("What is Turtle Mode?", ["upside", "inverted", "turtle"]),
]

PASS_THRESHOLD = 8


@pytest.fixture(scope="module")
def pilot():
    if not CONFIG_PATH.exists():
        pytest.skip("config.json not found — run ./setup.sh first")
    cfg = json.loads(CONFIG_PATH.read_text())
    from engine.rag_pipeline import DroneCoPilot
    return DroneCoPilot(
        chroma_path=cfg["chroma_path"],
        model_path=cfg["model_path"],
        n_gpu_layers=cfg.get("n_gpu_layers", 0),
    )


@pytest.mark.parametrize("question,keywords", BENCHMARK)
def test_answer_contains_keyword(pilot, question: str, keywords: list[str]):
    result = pilot.ask(question)
    answer_lower = result["answer"].lower()
    matched = any(kw.lower() in answer_lower for kw in keywords)
    assert matched, (
        f"Expected one of {keywords} in answer.\n"
        f"Question: {question}\n"
        f"Answer:   {result['answer']}"
    )


def test_answer_latency(pilot):
    result = pilot.ask("What is the max altitude for the DJI Avata?")
    assert result["latency_ms"] < 30_000, (
        f"Response too slow: {result['latency_ms']}ms (limit 30s)"
    )


def test_severity_classification_critical(pilot):
    result = pilot.ask("Emergency: the drone is crashing — what do I do?")
    assert result["severity"] in ("critical", "caution"), (
        f"Expected critical/caution severity, got: {result['severity']}"
    )


def test_severity_classification_info(pilot):
    result = pilot.ask("What is the maximum flight time?")
    assert result["severity"] in ("info", "caution"), (
        f"Expected info/caution severity, got: {result['severity']}"
    )


def test_sources_returned(pilot):
    result = pilot.ask("What are the LED status codes?")
    assert isinstance(result["sources"], list) and len(result["sources"]) > 0, (
        "No sources returned"
    )


def test_preflight_checklist_not_empty(pilot):
    items = pilot.get_preflight_checklist("Outdoor Recon")
    assert len(items) >= 4, f"Checklist too short: {len(items)} items"


def test_diagnose_returns_severity(pilot):
    result = pilot.diagnose("Drone drifting uncontrollably", {"Battery %": 80, "GPS Satellites": 10})
    assert result["severity"] in ("LOW", "MEDIUM", "HIGH", "CRITICAL")


def test_benchmark_pass_rate(pilot):
    passed = 0
    for question, keywords in BENCHMARK:
        result = pilot.ask(question)
        answer_lower = result["answer"].lower()
        if any(kw.lower() in answer_lower for kw in keywords):
            passed += 1
    rate = passed / len(BENCHMARK)
    assert passed >= PASS_THRESHOLD, (
        f"Benchmark pass rate {passed}/{len(BENCHMARK)} ({rate:.0%}) "
        f"below threshold {PASS_THRESHOLD}/{len(BENCHMARK)}"
    )
