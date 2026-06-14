from __future__ import annotations

import chromadb
from sentence_transformers import SentenceTransformer

from engine.llm_client import LocalLLMClient
from engine.prompts import SYSTEM_PROMPT, PREFLIGHT_PROMPTS, build_prompt

CRITICAL_KW = {"emergency", "fail", "crash", "critical", "malfunct", "fire", "flyaway", "fly away"}
CAUTION_KW = {"warning", "low battery", "signal loss", "gps", "obstacle", "caution", "wind"}

COLLECTION_NAME = "avata_copilot_v1"


def _severity(text: str) -> str:
    lower = text.lower()
    if any(k in lower for k in CRITICAL_KW):
        return "critical"
    if any(k in lower for k in CAUTION_KW):
        return "caution"
    return "info"


class DroneCoPilot:
    def __init__(self, chroma_path: str, model_path: str, n_gpu_layers: int = 0):
        self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        chroma_client = chromadb.PersistentClient(path=chroma_path)
        self.collection = chroma_client.get_collection(COLLECTION_NAME)
        self.llm = LocalLLMClient(model_path, n_gpu_layers=n_gpu_layers)
        self._latency_history: list[int] = []

    # ------------------------------------------------------------------
    def _retrieve(self, query: str, n: int = 4) -> tuple[str, list[str]]:
        emb = self.embedder.encode(query).tolist()
        results = self.collection.query(query_embeddings=[emb], n_results=n)
        docs: list[str] = results["documents"][0]
        metas: list[dict] = results["metadatas"][0]
        sources = [m.get("source", "unknown") for m in metas]
        context = "\n\n---\n\n".join(docs)
        return context, sources

    def _record_latency(self, ms: int) -> None:
        self._latency_history = (self._latency_history + [ms])[-5:]

    # ------------------------------------------------------------------
    def ask(self, question: str) -> dict:
        context, sources = self._retrieve(question)
        prompt = build_prompt(SYSTEM_PROMPT, question, context)
        answer, latency_ms = self.llm.generate(prompt)
        self._record_latency(latency_ms)
        severity = _severity(question + " " + answer)
        return {
            "answer": answer,
            "sources": sorted(set(sources)),
            "latency_ms": latency_ms,
            "severity": severity,
        }

    # ------------------------------------------------------------------
    def get_preflight_checklist(self, mission_type: str) -> list[str]:
        mission_q = PREFLIGHT_PROMPTS.get(mission_type, PREFLIGHT_PROMPTS["Outdoor Recon"])
        context, _ = self._retrieve(f"pre-flight checklist {mission_type} DJI Avata")
        prompt = build_prompt(SYSTEM_PROMPT, mission_q, context)
        answer, _ = self.llm.generate(prompt, max_tokens=500)

        checklist: list[str] = []
        for line in answer.split("\n"):
            line = line.strip()
            if not line:
                continue
            # Strip leading numbering: "1.", "1)", "-", "*"
            stripped = line.lstrip("0123456789.-)*• ").strip()
            if stripped and len(stripped) > 4:
                checklist.append(stripped)

        if not checklist:
            checklist = [
                "Check battery charge is above 80%",
                "Inspect all propellers for damage or debris",
                "Confirm GPS lock with 8+ satellites",
                "Set Return-to-Home altitude (minimum 30 m)",
                "Verify video transmission and goggle link",
                "Enable obstacle avoidance if environment permits",
                "Check SD card is inserted and has free space",
                "Confirm wind speed is within operating limits (< 10.7 m/s)",
            ]
        return checklist

    # ------------------------------------------------------------------
    def diagnose(self, symptom: str, telemetry: dict) -> dict:
        tel_lines = "\n".join(f"  {k}: {v}" for k, v in telemetry.items() if v is not None)
        user_msg = (
            f"Diagnose this anomaly:\n"
            f"Symptom: {symptom}\n"
            f"Telemetry:\n{tel_lines}\n\n"
            "Provide: severity (LOW/MEDIUM/HIGH/CRITICAL), recommended action, "
            "and whether to abort the mission (yes/no)."
        )
        context, _ = self._retrieve(symptom)
        prompt = build_prompt(SYSTEM_PROMPT, user_msg, context)
        answer, latency_ms = self.llm.generate(prompt, max_tokens=350)
        self._record_latency(latency_ms)

        lower = answer.lower()
        if any(k in lower for k in ["critical", "land immediately", "flyaway", "fly away", "fire"]):
            severity, abort = "CRITICAL", True
        elif any(k in lower for k in ["high", "return to home", "activate rth", "danger"]):
            severity, abort = "HIGH", True
        elif any(k in lower for k in ["medium", "caution", "monitor closely"]):
            severity, abort = "MEDIUM", False
        else:
            severity, abort = "LOW", False

        first_line = answer.split("\n")[0].strip() if answer else "Monitor the situation."
        return {
            "severity": severity,
            "recommended_action": first_line,
            "explanation": answer,
            "abort_mission": abort,
            "latency_ms": latency_ms,
        }

    # ------------------------------------------------------------------
    def avg_latency_ms(self) -> int:
        if not self._latency_history:
            return 0
        return int(sum(self._latency_history) / len(self._latency_history))

    def chunk_count(self) -> int:
        return self.collection.count()
