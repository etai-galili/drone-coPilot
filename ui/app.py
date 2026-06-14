from __future__ import annotations

import json
import sys
from pathlib import Path

import gradio as gr
import psutil

# Project root on path so engine imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

CONFIG_PATH = Path("config.json")

# Branded model name shown across the UI (overrides the underlying GGUF label)
MODEL_DISPLAY_NAME = "ProfWorxML v.1"

# ---------------------------------------------------------------------------
# Tactical CSS
# ---------------------------------------------------------------------------
TACTICAL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg-base:       #0A0D11;
  --bg-surface:    #0F141A;
  --bg-card:       #151B22;
  --bg-card-hover: #1C2530;
  --border:        #283039;
  --border-accent: #A6CE39;
  --text-primary:  #EDF1F3;
  --text-secondary:#93A0A8;
  --text-muted:    #5A636C;
  --accent-green:  #A6CE39;
  --accent-amber:  #F0B53A;
  --danger:        #F0524A;
  --warning:       #F08A2E;
  --success:       #A6CE39;
  --font-mono:     'JetBrains Mono', monospace;
  --font-ui:       'Inter', sans-serif;
  --radius:        6px;
  --radius-card:   10px;
}

*, *::before, *::after { box-sizing: border-box; }

body, .gradio-container, #root {
  background: var(--bg-base) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-ui) !important;
  margin: 0 !important;
}

/* Tabs */
.tab-nav { border-bottom: 1px solid var(--border) !important; }
.tab-nav button {
  background: transparent !important;
  color: var(--text-secondary) !important;
  border: none !important;
  border-bottom: 2px solid transparent !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  font-family: var(--font-ui) !important;
  padding: 10px 16px !important;
  transition: color 0.15s !important;
}
.tab-nav button:hover { color: var(--text-primary) !important; }
.tab-nav button.selected {
  color: var(--accent-green) !important;
  border-bottom: 2px solid var(--accent-green) !important;
}

/* Panels / blocks */
.block, .panel, .form, .gap, div[class*="block"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-card) !important;
}
.gradio-container > .gap { background: var(--bg-base) !important; border: none !important; }

/* Inputs */
input[type="text"], input[type="number"], textarea, .input-wrap textarea {
  background: var(--bg-surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-ui) !important;
  font-size: 14px !important;
  padding: 10px 12px !important;
  min-height: 44px !important;
  transition: border-color 0.15s !important;
}
input:focus, textarea:focus {
  border-color: var(--border-accent) !important;
  outline: none !important;
  box-shadow: 0 0 0 3px rgba(166,206,57,0.08) !important;
}

/* Primary buttons */
button.primary, .btn-primary, button[class*="primary"] {
  background: transparent !important;
  border: 1px solid var(--accent-green) !important;
  color: var(--accent-green) !important;
  text-transform: uppercase !important;
  letter-spacing: 0.1em !important;
  font-weight: 700 !important;
  font-size: 12px !important;
  border-radius: var(--radius) !important;
  min-height: 44px !important;
  cursor: pointer !important;
  transition: background 0.15s, box-shadow 0.15s !important;
}
button.primary:hover, .btn-primary:hover {
  background: rgba(166,206,57,0.08) !important;
  box-shadow: 0 0 12px rgba(166,206,57,0.2) !important;
}

/* Secondary buttons */
button.secondary, button[class*="secondary"] {
  background: transparent !important;
  border: 1px solid var(--border) !important;
  color: var(--text-secondary) !important;
  border-radius: var(--radius) !important;
  min-height: 44px !important;
  font-size: 12px !important;
  text-transform: uppercase !important;
  letter-spacing: 0.08em !important;
}
button.secondary:hover { border-color: var(--text-secondary) !important; color: var(--text-primary) !important; }

/* Labels */
label, .label-wrap span, span.svelte-1b6s6s {
  color: var(--text-secondary) !important;
  font-size: 11px !important;
  text-transform: uppercase !important;
  letter-spacing: 0.06em !important;
  font-weight: 600 !important;
}

/* Dropdowns / selects */
select, .select-wrap select {
  background: var(--bg-surface) !important;
  border: 1px solid var(--border) !important;
  color: var(--text-primary) !important;
  border-radius: var(--radius) !important;
  font-family: var(--font-ui) !important;
}

/* Sliders */
input[type="range"] { accent-color: var(--accent-green) !important; }

/* Radio buttons */
input[type="radio"] { accent-color: var(--accent-green) !important; }

/* Checkboxes */
input[type="checkbox"] { accent-color: var(--accent-green) !important; }

/* Accordion */
details, .accordion { background: var(--bg-surface) !important; border: 1px solid var(--border) !important; border-radius: var(--radius) !important; }
summary { color: var(--text-secondary) !important; font-size: 12px !important; padding: 8px 12px !important; cursor: pointer !important; }

/* Scrollbars */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* Utility classes used in HTML components */
.tac-header {
  font-family: var(--font-mono);
  color: var(--accent-green);
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 4px;
}
.tac-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-card);
  padding: 16px;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.tac-card:hover {
  border-color: rgba(166,206,57,0.35);
  box-shadow: 0 0 16px rgba(166,206,57,0.06);
}
.tac-card h3 {
  font-family: var(--font-mono);
  color: var(--accent-green);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin: 0 0 12px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border);
}
.tac-card p { color: var(--text-secondary); font-size: 13px; margin: 4px 0; line-height: 1.6; }
.tac-card strong { color: var(--text-primary); }
.tac-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
@media (max-width: 640px) { .tac-grid { grid-template-columns: 1fr; } }

.badge-info     { border-left: 3px solid var(--accent-green); padding-left: 12px; }
.badge-caution  { border-left: 3px solid var(--accent-amber); padding-left: 12px; }
.badge-critical { border-left: 3px solid var(--danger); padding-left: 12px; box-shadow: -4px 0 12px rgba(255,68,68,0.25); }

.status-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }
.dot-green  { background: var(--accent-green); box-shadow: 0 0 6px var(--accent-green); }
.dot-amber  { background: var(--accent-amber); box-shadow: 0 0 6px var(--accent-amber); }
.dot-red    { background: var(--danger); box-shadow: 0 0 6px var(--danger); }
.dot-grey   { background: var(--text-muted); }

.severity-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
}
.sev-low      { background: rgba(166,206,57,0.15); color: var(--accent-green); border: 1px solid var(--accent-green); }
.sev-medium   { background: rgba(255,184,0,0.12); color: var(--accent-amber); border: 1px solid var(--accent-amber); }
.sev-high     { background: rgba(255,140,0,0.12); color: var(--warning); border: 1px solid var(--warning); }
.sev-critical { background: rgba(255,68,68,0.15); color: var(--danger); border: 1px solid var(--danger); }

.footer-bar {
  color: var(--text-muted);
  font-family: var(--font-mono);
  font-size: 10px;
  letter-spacing: 0.08em;
  text-align: center;
  padding: 6px 0;
  border-top: 1px solid var(--border);
  margin-top: 4px;
}
"""

# ---------------------------------------------------------------------------
# Load pilot (lazy — first query initialises the LLM)
# ---------------------------------------------------------------------------
_pilot = None
_config: dict = {}
_load_error: str = ""


def _get_pilot():
    global _pilot, _config, _load_error
    if _pilot is not None:
        return _pilot

    if not CONFIG_PATH.exists():
        _load_error = "config.json not found — run ./setup.sh first."
        return None

    try:
        _config = json.loads(CONFIG_PATH.read_text())
        from engine.rag_pipeline import DroneCoPilot
        _pilot = DroneCoPilot(
            chroma_path=_config["chroma_path"],
            model_path=_config["model_path"],
            n_gpu_layers=_config.get("n_gpu_layers", 0),
        )
        return _pilot
    except Exception as exc:
        _load_error = f"Failed to load pipeline: {exc}"
        return None


# ---------------------------------------------------------------------------
# Helper — severity-coloured HTML answer card
# ---------------------------------------------------------------------------
def _answer_html(answer: str, severity: str, latency_ms: int, sources: list[str], model_label: str) -> str:
    sev_class = {
        "info": "badge-info",
        "caution": "badge-caution",
        "critical": "badge-critical",
    }.get(severity, "badge-info")

    sources_html = ""
    if sources:
        items = "".join(f"<li>{s}</li>" for s in sources)
        sources_html = f"<ul style='margin:8px 0 0 0;padding-left:18px;color:var(--text-muted);font-size:12px;font-family:var(--font-mono)'>{items}</ul>"

    return f"""
<div class='tac-card {sev_class}' style='margin:0'>
  <div style='font-size:14px;line-height:1.7;color:var(--text-primary);white-space:pre-wrap'>{answer}</div>
  {sources_html}
  <div class='footer-bar' style='margin-top:12px'>
    LATENCY: {latency_ms}ms &nbsp;|&nbsp; MODEL: {MODEL_DISPLAY_NAME}
    &nbsp;|&nbsp; SEVERITY: {severity.upper()}
  </div>
</div>
"""


# ---------------------------------------------------------------------------
# Tab 1 — Ask Co-Pilot
# ---------------------------------------------------------------------------
def ask_copilot(question: str) -> str:
    if not question.strip():
        return "<div class='tac-card badge-caution'>Enter a question first.</div>"
    pilot = _get_pilot()
    if pilot is None:
        return f"<div class='tac-card badge-critical'>{_load_error}</div>"
    result = pilot.ask(question)
    return _answer_html(
        result["answer"],
        result["severity"],
        result["latency_ms"],
        result["sources"],
        _config.get("model_label", ""),
    )


# ---------------------------------------------------------------------------
# Tab 2 — Pre-flight Checklist
# ---------------------------------------------------------------------------
def generate_checklist(mission_type: str) -> tuple[list[str], str, str]:
    pilot = _get_pilot()
    if pilot is None:
        return [], "0 / 0 items confirmed", _not_ready_html()
    items = pilot.get_preflight_checklist(mission_type)
    return items, _progress_html(0, len(items)), _status_badge("NOT READY")


def update_checklist_progress(checked: list[str], all_items: list[str]) -> tuple[str, str]:
    n = len(checked)
    total = len(all_items) if all_items else 1
    ready = n == total and total > 0
    return _progress_html(n, total), _status_badge("READY TO FLY" if ready else "NOT READY")


def reset_checklist() -> tuple[list[str], str, str]:
    return [], _progress_html(0, 0), _status_badge("NOT READY")


def _progress_html(done: int, total: int) -> str:
    pct = int(done / total * 100) if total else 0
    color = "var(--accent-green)" if pct == 100 else "var(--accent-amber)"
    return f"""
<div style='padding:8px 0'>
  <div style='font-family:var(--font-mono);font-size:11px;color:var(--text-secondary);margin-bottom:6px;letter-spacing:0.08em'>
    PROGRESS &nbsp;·&nbsp; {done} / {total} ITEMS CONFIRMED
  </div>
  <div style='background:var(--bg-surface);border:1px solid var(--border);border-radius:4px;height:6px;overflow:hidden'>
    <div style='height:100%;width:{pct}%;background:{color};transition:width 0.3s;border-radius:4px'></div>
  </div>
</div>
"""


def _status_badge(label: str) -> str:
    is_ready = label == "READY TO FLY"
    color = "var(--accent-green)" if is_ready else "var(--danger)"
    dot = "dot-green" if is_ready else "dot-red"
    return f"""
<div style='display:inline-flex;align-items:center;gap:8px;padding:8px 16px;
            border:1px solid {color};border-radius:6px;
            background:rgba({"166,206,57" if is_ready else "255,68,68"},0.06)'>
  <span class='status-dot {dot}'></span>
  <span style='font-family:var(--font-mono);font-size:12px;font-weight:700;
               letter-spacing:0.12em;color:{color}'>{label}</span>
</div>
"""


def _not_ready_html() -> str:
    return _status_badge("NOT READY")


# ---------------------------------------------------------------------------
# Tab 3 — Anomaly Diagnosis
# ---------------------------------------------------------------------------
def diagnose_anomaly(
    symptom: str,
    battery: int,
    gps_sats: int,
    signal: int,
    wind: str,
) -> str:
    if not symptom.strip():
        return "<div class='tac-card badge-caution'>Describe the anomaly first.</div>"
    pilot = _get_pilot()
    if pilot is None:
        return f"<div class='tac-card badge-critical'>{_load_error}</div>"

    telemetry = {
        "Battery %": battery,
        "GPS Satellites": gps_sats,
        "Signal Strength %": signal,
        "Wind Condition": wind,
    }
    result = pilot.diagnose(symptom, telemetry)
    sev = result["severity"]
    sev_map = {"LOW": "sev-low", "MEDIUM": "sev-medium", "HIGH": "sev-high", "CRITICAL": "sev-critical"}
    sev_class = sev_map.get(sev, "sev-low")
    abort_html = ""
    if result["abort_mission"]:
        abort_html = """
<div style='margin-top:12px;padding:10px 14px;background:rgba(255,68,68,0.12);
            border:1px solid var(--danger);border-radius:6px;
            font-family:var(--font-mono);font-size:12px;font-weight:700;
            color:var(--danger);letter-spacing:0.1em;text-align:center'>
  ⚠ ABORT MISSION — LAND IMMEDIATELY
</div>
"""
    return f"""
<div class='tac-card' style='margin:0'>
  <div style='display:flex;align-items:center;gap:12px;margin-bottom:12px'>
    <span class='severity-badge {sev_class}'>{sev}</span>
    <span style='font-family:var(--font-mono);font-size:10px;color:var(--text-muted);letter-spacing:0.08em'>
      SEVERITY ASSESSMENT
    </span>
  </div>
  <div style='font-size:15px;font-weight:600;color:var(--text-primary);margin-bottom:8px'>
    {result["recommended_action"]}
  </div>
  <div style='font-size:13px;color:var(--text-secondary);line-height:1.7;white-space:pre-wrap'>
    {result["explanation"]}
  </div>
  {abort_html}
  <div class='footer-bar' style='margin-top:12px'>LATENCY: {result["latency_ms"]}ms</div>
</div>
"""


# ---------------------------------------------------------------------------
# Tab 4 — Quick Reference (static HTML)
# ---------------------------------------------------------------------------
QUICK_REF_HTML = """
<div class='tac-grid'>

  <div class='tac-card'>
    <h3>// Flight Specs</h3>
    <p><strong>Max flight time</strong> · ~18 min (Avata 1) / ~23 min (Avata 2)</p>
    <p><strong>Max range</strong> · 10 km (CE) / 13 km (FCC)</p>
    <p><strong>Max altitude</strong> · 500 m AGL</p>
    <p><strong>Max wind resistance</strong> · 10.7 m/s (Level 5)</p>
    <p><strong>Max speed (Sport)</strong> · 97.2 km/h</p>
    <p><strong>Video transmission</strong> · O3+ up to 1080p/100fps</p>
  </div>

  <div class='tac-card'>
    <h3>// Emergency Procedures</h3>
    <p><strong>RTH</strong> · Press and hold RTH button 2 sec</p>
    <p><strong>Emergency Stop</strong> · Toggle arm switch 3× in 1 sec</p>
    <p><strong>Turtle Mode</strong> · Activated via goggles when inverted</p>
    <p><strong>Signal Loss</strong> · Auto-RTH after 11 sec</p>
    <p><strong>Low Battery</strong> · Auto-land at critical level</p>
    <p><strong>Obstacle</strong> · Hover/brake in N-Mode</p>
  </div>

  <div class='tac-card'>
    <h3>// Flight Modes</h3>
    <p><strong>N-Mode</strong> · GNSS + Vision System, stable, beginner-safe</p>
    <p><strong>S-Mode</strong> · Sport, faster, reduced obstacle sensing</p>
    <p><strong>M-Mode</strong> · Manual, no stabilisation, expert only</p>
    <p><strong>Brake Mode</strong> · Altitude hold, emergency stop</p>
  </div>

  <div class='tac-card'>
    <h3>// LED Status Codes</h3>
    <p><span style='color:var(--accent-green)'>●</span> <strong>Solid Green</strong> · Ready to fly</p>
    <p><span style='color:var(--accent-amber)'>●</span> <strong>Blinking Yellow</strong> · GPS calibration in progress</p>
    <p><span style='color:var(--danger)'>●</span> <strong>Blinking Red</strong> · Low battery warning</p>
    <p><span style='color:var(--danger)'>●</span>/<span style='color:var(--accent-amber)'>●</span> <strong>Alternating Red/Yellow</strong> · IMU error — do not fly</p>
    <p><span style='color:#6fa8dc'>●</span> <strong>Solid Blue</strong> · Connecting / initialising</p>
  </div>

</div>
"""


# ---------------------------------------------------------------------------
# Tab 5 — System Status
# ---------------------------------------------------------------------------
def _system_status_html() -> str:
    mem = psutil.virtual_memory()
    ram_used = mem.used / (1024 ** 3)
    ram_total = mem.total / (1024 ** 3)

    if CONFIG_PATH.exists():
        try:
            cfg = json.loads(CONFIG_PATH.read_text())
            backend = cfg.get("backend", "CPU")
            model_path = cfg.get("model_path", "")
            model_size = ""
            if model_path and Path(model_path).exists():
                size_mb = Path(model_path).stat().st_size / (1024 ** 2)
                model_size = f"{size_mb:.0f} MB"
            llm_dot = "dot-green"
            llm_status = f"Loaded: {MODEL_DISPLAY_NAME} | {model_size} | {backend}"
        except Exception as e:
            llm_dot = "dot-amber"
            llm_status = f"Config error: {e}"
    else:
        llm_dot = "dot-red"
        llm_status = "Not configured — run ./setup.sh"

    from pathlib import Path as _P
    chroma_ok = _P("data/chroma_db").exists()
    chunks_path = _P("data/chunks/all_chunks.jsonl")
    chunk_count = 0
    if chunks_path.exists():
        with chunks_path.open() as f:
            chunk_count = sum(1 for l in f if l.strip())
    kb_dot = "dot-green" if (chroma_ok and chunk_count > 0) else "dot-red"
    kb_status = f"{chunk_count} chunks indexed | ChromaDB: {'OK' if chroma_ok else 'MISSING'}"

    pilot = _pilot
    avg_lat = pilot.avg_latency_ms() if pilot else 0
    lat_str = f"{avg_lat} ms (last 5 queries)" if avg_lat else "No queries yet"

    def row(dot: str, label: str, value: str) -> str:
        return f"""
<div style='display:flex;align-items:flex-start;gap:12px;padding:12px 0;border-bottom:1px solid var(--border)'>
  <span class='status-dot {dot}' style='margin-top:5px;flex-shrink:0'></span>
  <div>
    <div style='font-family:var(--font-mono);font-size:11px;color:var(--text-secondary);
                letter-spacing:0.08em;text-transform:uppercase'>{label}</div>
    <div style='font-size:13px;color:var(--text-primary);margin-top:3px'>{value}</div>
  </div>
</div>
"""
    return f"""
<div class='tac-card' style='margin:0'>
  {row(llm_dot, "LLM Model", llm_status)}
  {row(kb_dot, "Knowledge Base", kb_status)}
  {row("dot-green", "RAM Usage", f"{ram_used:.1f} GB used / {ram_total:.1f} GB total")}
  {row("dot-green" if avg_lat else "dot-grey", "Avg Latency", lat_str)}
  <div class='footer-bar' style='margin-top:8px'>
    PROFWORXML v.1 &nbsp;|&nbsp; OFFLINE &nbsp;|&nbsp; DJI AVATA KNOWLEDGE BASE
  </div>
</div>
"""


def run_self_test() -> str:
    TEST_QUESTIONS = [
        "What is the maximum flight time of the DJI Avata?",
        "How do I activate Return to Home on the DJI Avata?",
        "What does alternating red and yellow LED mean?",
    ]
    pilot = _get_pilot()
    if pilot is None:
        return f"<div class='tac-card badge-critical'>{_load_error}</div>"

    rows = ""
    all_pass = True
    for q in TEST_QUESTIONS:
        try:
            result = pilot.ask(q)
            answer_preview = result["answer"][:120].replace("<", "&lt;").replace(">", "&gt;")
            rows += f"""
<div style='padding:10px 0;border-bottom:1px solid var(--border)'>
  <div style='display:flex;align-items:center;gap:8px;margin-bottom:4px'>
    <span style='color:var(--accent-green);font-family:var(--font-mono);font-size:11px'>PASS</span>
    <span style='color:var(--text-muted);font-family:var(--font-mono);font-size:10px'>{result["latency_ms"]}ms</span>
  </div>
  <div style='font-size:12px;color:var(--text-secondary);margin-bottom:3px'>{q}</div>
  <div style='font-size:13px;color:var(--text-primary)'>{answer_preview}{"..." if len(result["answer"]) > 120 else ""}</div>
</div>
"""
        except Exception as e:
            all_pass = False
            rows += f"""
<div style='padding:10px 0;border-bottom:1px solid var(--border)'>
  <div style='color:var(--danger);font-family:var(--font-mono);font-size:11px;margin-bottom:4px'>FAIL</div>
  <div style='font-size:12px;color:var(--text-secondary)'>{q}</div>
  <div style='font-size:13px;color:var(--danger)'>{e}</div>
</div>
"""

    overall = "dot-green" if all_pass else "dot-amber"
    label = "ALL TESTS PASSED" if all_pass else "SOME TESTS FAILED"
    color = "var(--accent-green)" if all_pass else "var(--accent-amber)"

    return f"""
<div class='tac-card' style='margin:0'>
  <div style='display:flex;align-items:center;gap:8px;margin-bottom:12px'>
    <span class='status-dot {overall}'></span>
    <span style='font-family:var(--font-mono);font-size:11px;font-weight:700;
                 letter-spacing:0.1em;color:{color}'>{label}</span>
  </div>
  {rows}
</div>
"""


# ---------------------------------------------------------------------------
# Build the Gradio interface
# ---------------------------------------------------------------------------
def build_ui() -> gr.Blocks:
    with gr.Blocks(css=TACTICAL_CSS, title="ProfWorxML v.1") as demo:

        # ── Header ──────────────────────────────────────────────────────
        gr.HTML("""
<div style='padding:20px 24px 14px;border-bottom:1px solid var(--border);
            display:flex;align-items:center;gap:16px'>
  <div style='display:flex;align-items:baseline;gap:10px'>
    <span style='font-family:var(--font-ui);font-size:22px;font-weight:800;
                 color:var(--text-primary);letter-spacing:0.04em;text-transform:uppercase'>ProfWorx</span>
    <span style='font-family:var(--font-mono);font-size:13px;font-weight:600;
                 color:var(--accent-green);letter-spacing:0.1em'>ML v.1</span>
  </div>
  <div style='margin-left:auto;display:flex;gap:6px;align-items:center'>
    <span class='status-dot dot-green'></span>
    <span style='font-family:var(--font-mono);font-size:10px;color:var(--accent-green);
                 letter-spacing:0.08em'>SYSTEM ONLINE</span>
  </div>
</div>
""")

        with gr.Tabs():

            # ── TAB 1: ASK CO-PILOT ─────────────────────────────────────
            with gr.Tab("// Ask Co-Pilot"):
                gr.HTML("<div class='tac-header' style='padding:16px 0 8px'>"
                        "// ASK CO-PILOT</div>")
                question_in = gr.Textbox(
                    placeholder="Enter your operational question...",
                    label="Question",
                    lines=3,
                )
                ask_btn = gr.Button("ASK", variant="primary")
                answer_out = gr.HTML(label="Response")

                ask_btn.click(fn=ask_copilot, inputs=question_in, outputs=answer_out)
                question_in.submit(fn=ask_copilot, inputs=question_in, outputs=answer_out)

            # ── TAB 2: PRE-FLIGHT CHECKLIST ─────────────────────────────
            with gr.Tab("// Pre-Flight"):
                gr.HTML("<div class='tac-header' style='padding:16px 0 8px'>"
                        "// PRE-FLIGHT CHECKLIST</div>")
                mission_dd = gr.Dropdown(
                    choices=["Indoor Recon", "Outdoor Recon", "FPV Freestyle", "Mapping", "SAR"],
                    value="Outdoor Recon",
                    label="Mission Type",
                )
                gen_btn = gr.Button("GENERATE CHECKLIST", variant="primary")

                checklist_state = gr.State([])
                checklist_box = gr.CheckboxGroup(choices=[], label="Checklist Items", interactive=True)
                progress_html = gr.HTML()
                status_html = gr.HTML()

                with gr.Row():
                    reset_btn = gr.Button("RESET", variant="secondary")

                def _gen(mission: str):
                    from engine.rag_pipeline import DroneCoPilot  # noqa: F401
                    pilot = _get_pilot()
                    if pilot is None:
                        return [], [], _progress_html(0, 0), _not_ready_html()
                    items = pilot.get_preflight_checklist(mission)
                    return items, gr.CheckboxGroup(choices=items, value=[]), _progress_html(0, len(items)), _status_badge("NOT READY")

                def _progress(checked: list[str], state: list[str]):
                    total = len(state)
                    n = len(checked)
                    ready = n == total and total > 0
                    return _progress_html(n, total), _status_badge("READY TO FLY" if ready else "NOT READY")

                def _reset(state: list[str]):
                    return gr.CheckboxGroup(choices=state, value=[]), _progress_html(0, len(state)), _status_badge("NOT READY")

                gen_btn.click(
                    fn=_gen,
                    inputs=mission_dd,
                    outputs=[checklist_state, checklist_box, progress_html, status_html],
                )
                checklist_box.change(
                    fn=_progress,
                    inputs=[checklist_box, checklist_state],
                    outputs=[progress_html, status_html],
                )
                reset_btn.click(
                    fn=_reset,
                    inputs=checklist_state,
                    outputs=[checklist_box, progress_html, status_html],
                )

            # ── TAB 3: ANOMALY DIAGNOSIS ─────────────────────────────────
            with gr.Tab("// Diagnosis"):
                gr.HTML("<div class='tac-header' style='padding:16px 0 8px'>"
                        "// ANOMALY DIAGNOSIS</div>")
                symptom_in = gr.Textbox(
                    placeholder="Describe the anomaly or symptom...",
                    label="Symptom",
                    lines=3,
                )
                gr.HTML("<div style='color:var(--text-muted);font-size:11px;font-family:var(--font-mono);"
                        "letter-spacing:0.06em;margin:8px 0 4px'>TELEMETRY (optional)</div>")
                with gr.Row():
                    battery_sl = gr.Slider(0, 100, value=100, step=1, label="Battery %")
                    gps_num = gr.Number(value=12, minimum=0, maximum=20, label="GPS Satellites")
                with gr.Row():
                    signal_sl = gr.Slider(0, 100, value=90, step=1, label="Signal Strength %")
                    wind_radio = gr.Radio(
                        choices=["Calm", "Light", "Moderate", "Strong"],
                        value="Calm",
                        label="Wind Condition",
                    )
                diag_btn = gr.Button("DIAGNOSE", variant="primary")
                diag_out = gr.HTML(label="Diagnosis")

                diag_btn.click(
                    fn=diagnose_anomaly,
                    inputs=[symptom_in, battery_sl, gps_num, signal_sl, wind_radio],
                    outputs=diag_out,
                )

            # ── TAB 4: QUICK REFERENCE ──────────────────────────────────
            with gr.Tab("// Quick Ref"):
                gr.HTML("<div class='tac-header' style='padding:16px 0 8px'>"
                        "// QUICK REFERENCE</div>")
                gr.HTML(QUICK_REF_HTML)

            # ── TAB 5: SYSTEM STATUS ─────────────────────────────────────
            with gr.Tab("// Status"):
                gr.HTML("<div class='tac-header' style='padding:16px 0 8px'>"
                        "// SYSTEM STATUS</div>")
                status_panel = gr.HTML()
                with gr.Row():
                    refresh_btn = gr.Button("REFRESH STATUS", variant="secondary")
                    test_btn = gr.Button("RUN SELF-TEST", variant="primary")
                test_out = gr.HTML(label="Self-Test Results")

                demo.load(fn=_system_status_html, inputs=None, outputs=status_panel)
                refresh_btn.click(fn=_system_status_html, inputs=None, outputs=status_panel)
                test_btn.click(fn=run_self_test, inputs=None, outputs=test_out)

    return demo


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app = build_ui()
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_api=False,
        inbrowser=True,
    )
