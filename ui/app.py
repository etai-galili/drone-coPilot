from __future__ import annotations

import json
import sys
from pathlib import Path

import gradio as gr
import psutil

# Project root on path so engine imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

CONFIG_PATH = Path("config.json")

# ---------------------------------------------------------------------------
# Tactical CSS
# ---------------------------------------------------------------------------
TACTICAL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg-base:       #080C10;
  --bg-surface:    #0D1117;
  --bg-card:       #161B22;
  --bg-card-hover: #1C2330;
  --border:        #30363D;
  --border-accent: #00FF94;
  --text-primary:  #E6EDF3;
  --text-secondary:#8B949E;
  --text-muted:    #484F58;
  --accent-green:  #00FF94;
  --accent-amber:  #FFB800;
  --danger:        #FF4444;
  --warning:       #FF8C00;
  --success:       #00FF94;
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
  box-shadow: 0 0 0 3px rgba(0,255,148,0.08) !important;
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
  background: rgba(0,255,148,0.08) !important;
  box-shadow: 0 0 12px rgba(0,255,148,0.2) !important;
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
  border-color: rgba(0,255,148,0.35);
  box-shadow: 0 0 16px rgba(0,255,148,0.06);
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
.sev-low      { background: rgba(0,255,148,0.15); color: var(--accent-green); border: 1px solid var(--accent-green); }
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
    LATENCY: {latency_ms}ms &nbsp;|&nbsp; MODEL: {model_label or 'N/A'}
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
            background:rgba({"0,255,148" if is_ready else "255,68,68"},0.06)'>
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
            model_label = cfg.get("model_label", "Unknown")
            backend = cfg.get("backend", "CPU")
            model_path = cfg.get("model_path", "")
            model_size = ""
            if model_path and Path(model_path).exists():
                size_mb = Path(model_path).stat().st_size / (1024 ** 2)
                model_size = f"{size_mb:.0f} MB"
            llm_dot = "dot-green"
            llm_status = f"Loaded: {model_label} | {model_size} | {backend}"
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
    AVATA CO-PILOT v1.0 &nbsp;|&nbsp; OFFLINE &nbsp;|&nbsp; DJI AVATA KNOWLEDGE BASE
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
# Tab 5 — Drone Explorer (interactive SVG)
# ---------------------------------------------------------------------------
DRONE_EXPLORER_HTML = """
<style>
#de-wrap { display:flex; gap:0; height:620px; background:#080C10; border-radius:10px; overflow:hidden; border:1px solid #30363D; font-family:'JetBrains Mono',monospace; }
#de-svg-panel { flex:1; position:relative; display:flex; flex-direction:column; align-items:center; justify-content:center; background:#080C10; min-width:0; }
#de-hint { position:absolute; top:14px; left:50%; transform:translateX(-50%); font-size:10px; color:#484F58; letter-spacing:.1em; text-transform:uppercase; white-space:nowrap; pointer-events:none; }
#de-zoom-wrap { width:100%; height:100%; display:flex; align-items:center; justify-content:center; overflow:hidden; cursor:default; }
#de-svg { transition: transform .45s cubic-bezier(.4,0,.2,1); transform-origin: center center; }
#de-info { width:310px; flex-shrink:0; background:#0D1117; border-left:1px solid #30363D; display:flex; flex-direction:column; overflow:hidden; }
#de-info-header { padding:16px 18px 12px; border-bottom:1px solid #30363D; }
#de-info-title { font-size:14px; font-weight:700; color:#E6EDF3; letter-spacing:.06em; margin:0 0 2px; }
#de-info-sub { font-size:10px; color:#8B949E; letter-spacing:.1em; text-transform:uppercase; }
#de-info-body { flex:1; overflow-y:auto; padding:0 18px 16px; }
#de-info-body::-webkit-scrollbar { width:4px; } #de-info-body::-webkit-scrollbar-track { background:#0D1117; } #de-info-body::-webkit-scrollbar-thumb { background:#30363D; border-radius:2px; }
.de-spec-table { width:100%; border-collapse:collapse; margin-top:14px; }
.de-spec-table tr { border-bottom:1px solid #1C2330; }
.de-spec-table td { padding:7px 4px; font-size:12px; line-height:1.4; }
.de-spec-table td:first-child { color:#8B949E; width:45%; padding-right:8px; }
.de-spec-table td:last-child { color:#E6EDF3; font-weight:500; }
.de-desc { font-size:12px; color:#8B949E; line-height:1.6; margin-top:12px; padding-top:12px; border-top:1px solid #1C2330; }
.de-badge { display:inline-block; padding:2px 8px; border-radius:3px; font-size:10px; font-weight:700; letter-spacing:.08em; margin-top:12px; }
#de-reset { position:absolute; bottom:14px; right:14px; background:transparent; border:1px solid #30363D; color:#8B949E; font-size:10px; font-family:'JetBrains Mono',monospace; letter-spacing:.08em; text-transform:uppercase; padding:5px 12px; border-radius:4px; cursor:pointer; transition:all .15s; }
#de-reset:hover { border-color:#00FF94; color:#00FF94; }
/* hotspot pulse animation */
@keyframes de-pulse { 0%,100%{opacity:.6} 50%{opacity:1} }
.de-hs { cursor:pointer; transition:opacity .2s; }
.de-hs:hover .de-hs-ring { animation: de-pulse .9s ease-in-out infinite; }
</style>

<div id="de-wrap">
  <!-- SVG panel -->
  <div id="de-svg-panel">
    <div id="de-hint">לחץ על חלק לפרטים &nbsp;·&nbsp; CLICK A PART TO INSPECT</div>
    <div id="de-zoom-wrap">
      <svg id="de-svg" viewBox="0 0 500 520" xmlns="http://www.w3.org/2000/svg" width="480" height="500">
        <defs>
          <filter id="de-glow-g"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
          <filter id="de-glow-c"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
          <filter id="de-glow-o"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
          <radialGradient id="de-bg-grad" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#0d1929" stop-opacity="1"/>
            <stop offset="100%" stop-color="#080C10" stop-opacity="1"/>
          </radialGradient>
        </defs>

        <!-- Background -->
        <rect width="500" height="520" fill="url(#de-bg-grad)"/>
        <!-- Grid -->
        <g stroke="#1a2535" stroke-width=".5" opacity=".6">
          <line x1="0" y1="130" x2="500" y2="130"/><line x1="0" y1="260" x2="500" y2="260"/>
          <line x1="0" y1="390" x2="500" y2="390"/>
          <line x1="125" y1="0" x2="125" y2="520"/><line x1="250" y1="0" x2="250" y2="520"/>
          <line x1="375" y1="0" x2="375" y2="520"/>
        </g>
        <!-- Crosshair center -->
        <g stroke="#1a2535" stroke-width=".8">
          <line x1="240" y1="258" x2="260" y2="258"/><line x1="250" y1="248" x2="250" y2="268"/>
        </g>

        <!-- ═══ PROP GUARDS (outer rings) ═══ -->
        <!-- FL guard -->
        <circle cx="132" cy="132" r="82" fill="#0a1020" stroke="#2a4a7a" stroke-width="2.2" id="de-guard-fl"/>
        <circle cx="132" cy="132" r="64" fill="none" stroke="#1e3560" stroke-width="1" opacity=".5"/>
        <!-- FR guard -->
        <circle cx="368" cy="132" r="82" fill="#0a1020" stroke="#2a4a7a" stroke-width="2.2" id="de-guard-fr"/>
        <circle cx="368" cy="132" r="64" fill="none" stroke="#1e3560" stroke-width="1" opacity=".5"/>
        <!-- RL guard -->
        <circle cx="132" cy="388" r="82" fill="#0a1020" stroke="#2a4a7a" stroke-width="2.2" id="de-guard-rl"/>
        <circle cx="132" cy="388" r="64" fill="none" stroke="#1e3560" stroke-width="1" opacity=".5"/>
        <!-- RR guard -->
        <circle cx="368" cy="388" r="82" fill="#0a1020" stroke="#2a4a7a" stroke-width="2.2" id="de-guard-rr"/>
        <circle cx="368" cy="388" r="64" fill="none" stroke="#1e3560" stroke-width="1" opacity=".5"/>

        <!-- Guard spoke crosses -->
        <g stroke="#1e3560" stroke-width=".8" opacity=".6">
          <line x1="132" y1="54" x2="132" y2="210"/><line x1="54" y1="132" x2="210" y2="132"/>
          <line x1="368" y1="54" x2="368" y2="210"/><line x1="290" y1="132" x2="446" y2="132"/>
          <line x1="132" y1="310" x2="132" y2="466"/><line x1="54" y1="388" x2="210" y2="388"/>
          <line x1="368" y1="310" x2="368" y2="466"/><line x1="290" y1="388" x2="446" y2="388"/>
        </g>

        <!-- ═══ ARMS ═══ -->
        <!-- FL arm -->
        <polygon points="132,152 168,178 188,162 178,138" fill="#0d1929" stroke="#2a4a7a" stroke-width="1.5"/>
        <!-- FR arm -->
        <polygon points="368,152 332,178 312,162 322,138" fill="#0d1929" stroke="#2a4a7a" stroke-width="1.5"/>
        <!-- RL arm -->
        <polygon points="132,368 168,342 188,358 178,382" fill="#0d1929" stroke="#2a4a7a" stroke-width="1.5"/>
        <!-- RR arm -->
        <polygon points="368,368 332,342 312,358 322,382" fill="#0d1929" stroke="#2a4a7a" stroke-width="1.5"/>

        <!-- ═══ MAIN BODY ═══ -->
        <polygon points="188,162 220,148 280,148 312,162 320,200 320,320 312,358 280,372 220,372 188,358 180,320 180,200"
          fill="#0d1929" stroke="#3a6aaa" stroke-width="2"/>

        <!-- Body interior detail lines -->
        <line x1="250" y1="160" x2="250" y2="370" stroke="#1e3560" stroke-width=".8" opacity=".5"/>
        <line x1="185" y1="260" x2="315" y2="260" stroke="#1e3560" stroke-width=".8" opacity=".5"/>

        <!-- ═══ BATTERY COVER ═══ -->
        <rect id="de-battery-shape" x="210" y="190" width="80" height="120" rx="6"
          fill="#111c2e" stroke="#3a6aaa" stroke-width="1.8"/>
        <!-- Battery grip lines -->
        <line x1="218" y1="210" x2="282" y2="210" stroke="#1e3560" stroke-width=".8"/>
        <line x1="218" y1="220" x2="282" y2="220" stroke="#1e3560" stroke-width=".8"/>
        <!-- DJI logo placeholder -->
        <text x="250" y="263" fill="#2a4a7a" font-family="monospace" font-size="11" font-weight="bold" text-anchor="middle" letter-spacing="2">DJI</text>
        <!-- AVATA text -->
        <text x="250" y="278" fill="#1e3560" font-family="monospace" font-size="8" text-anchor="middle" letter-spacing="3">AVATA</text>
        <!-- Battery level bar -->
        <rect x="218" y="290" width="64" height="8" rx="2" fill="#0a0f1a" stroke="#1e3560" stroke-width="1"/>
        <rect x="219" y="291" width="48" height="6" rx="1.5" fill="#00FF94" opacity=".6"/>

        <!-- ═══ FLIGHT CONTROLLER (ESC area) ═══ -->
        <rect id="de-fc-shape" x="215" y="320" width="70" height="45" rx="4"
          fill="#0a1420" stroke="#2a4a7a" stroke-width="1.2"/>
        <!-- PCB detail -->
        <rect x="222" y="327" width="56" height="31" rx="2" fill="#070e18" stroke="#1e3560" stroke-width=".8"/>
        <circle cx="229" cy="343" r="3" fill="#1e3560"/><circle cx="271" cy="343" r="3" fill="#1e3560"/>
        <line x1="234" y1="335" x2="266" y2="335" stroke="#1e3560" stroke-width=".6"/>
        <line x1="234" y1="343" x2="266" y2="343" stroke="#1e3560" stroke-width=".6"/>
        <line x1="234" y1="351" x2="266" y2="351" stroke="#1e3560" stroke-width=".6"/>

        <!-- ═══ CAMERA ═══ -->
        <!-- Camera housing -->
        <ellipse cx="250" cy="175" rx="22" ry="14" fill="#070d18" stroke="#00ffcc" stroke-width="1.8" filter="url(#de-glow-c)"/>
        <circle cx="250" cy="175" r="10" fill="#0a1520" stroke="#00ffcc" stroke-width="1.5"/>
        <circle cx="250" cy="175" r="5.5" fill="#00ffcc" opacity=".2"/>
        <circle cx="250" cy="175" r="2.5" fill="#00ffcc" opacity=".4"/>
        <!-- Camera reflection dot -->
        <circle cx="253" cy="172" r="1.2" fill="white" opacity=".5"/>

        <!-- ═══ VIDEO TX ANTENNA ═══ -->
        <!-- O3+ antenna represented as a small element top of body -->
        <rect x="241" y="150" width="18" height="8" rx="2" fill="#111c2e" stroke="#4a9eff" stroke-width="1.2"/>
        <line x1="250" y1="150" x2="250" y2="143" stroke="#4a9eff" stroke-width="1.5"/>
        <circle cx="250" cy="141" r="3" fill="none" stroke="#4a9eff" stroke-width="1.2" opacity=".7"/>

        <!-- ═══ MOTORS ═══ -->
        <!-- FL motor -->
        <circle cx="132" cy="132" r="24" fill="#0d1929" stroke="#4a9eff" stroke-width="2" filter="url(#de-glow-g)"/>
        <circle cx="132" cy="132" r="14" fill="#0a1020" stroke="#4a9eff" stroke-width="1.5"/>
        <circle cx="132" cy="132" r="5" fill="#4a9eff" opacity=".6"/>
        <!-- FR motor -->
        <circle cx="368" cy="132" r="24" fill="#0d1929" stroke="#4a9eff" stroke-width="2" filter="url(#de-glow-g)"/>
        <circle cx="368" cy="132" r="14" fill="#0a1020" stroke="#4a9eff" stroke-width="1.5"/>
        <circle cx="368" cy="132" r="5" fill="#4a9eff" opacity=".6"/>
        <!-- RL motor -->
        <circle cx="132" cy="388" r="24" fill="#0d1929" stroke="#4a9eff" stroke-width="2" filter="url(#de-glow-g)"/>
        <circle cx="132" cy="388" r="14" fill="#0a1020" stroke="#4a9eff" stroke-width="1.5"/>
        <circle cx="132" cy="388" r="5" fill="#4a9eff" opacity=".6"/>
        <!-- RR motor -->
        <circle cx="368" cy="388" r="24" fill="#0d1929" stroke="#4a9eff" stroke-width="2" filter="url(#de-glow-g)"/>
        <circle cx="368" cy="388" r="14" fill="#0a1020" stroke="#4a9eff" stroke-width="1.5"/>
        <circle cx="368" cy="388" r="5" fill="#4a9eff" opacity=".6"/>

        <!-- ═══ PROPELLERS ═══ -->
        <!-- FL props (CW - 2 blades shown as ellipses) -->
        <ellipse cx="132" cy="132" rx="52" ry="7" fill="rgba(74,158,255,.12)" stroke="#4a9eff" stroke-width="1" opacity=".7" transform="rotate(20,132,132)"/>
        <ellipse cx="132" cy="132" rx="52" ry="7" fill="rgba(74,158,255,.12)" stroke="#4a9eff" stroke-width="1" opacity=".7" transform="rotate(110,132,132)"/>
        <!-- FR props (CCW) -->
        <ellipse cx="368" cy="132" rx="52" ry="7" fill="rgba(74,158,255,.12)" stroke="#4a9eff" stroke-width="1" opacity=".7" transform="rotate(-20,368,132)"/>
        <ellipse cx="368" cy="132" rx="52" ry="7" fill="rgba(74,158,255,.12)" stroke="#4a9eff" stroke-width="1" opacity=".7" transform="rotate(70,368,132)"/>
        <!-- RL props (CCW) -->
        <ellipse cx="132" cy="388" rx="52" ry="7" fill="rgba(74,158,255,.12)" stroke="#4a9eff" stroke-width="1" opacity=".7" transform="rotate(-20,132,388)"/>
        <ellipse cx="132" cy="388" rx="52" ry="7" fill="rgba(74,158,255,.12)" stroke="#4a9eff" stroke-width="1" opacity=".7" transform="rotate(70,132,388)"/>
        <!-- RR props (CW) -->
        <ellipse cx="368" cy="388" rx="52" ry="7" fill="rgba(74,158,255,.12)" stroke="#4a9eff" stroke-width="1" opacity=".7" transform="rotate(20,368,388)"/>
        <ellipse cx="368" cy="388" rx="52" ry="7" fill="rgba(74,158,255,.12)" stroke="#4a9eff" stroke-width="1" opacity=".7" transform="rotate(110,368,388)"/>

        <!-- ═══ LED INDICATORS ═══ -->
        <circle cx="195" cy="165" r="3" fill="#00FF94" opacity=".8" filter="url(#de-glow-g)"/>
        <circle cx="305" cy="165" r="3" fill="#00FF94" opacity=".8" filter="url(#de-glow-g)"/>
        <circle cx="195" cy="355" r="3" fill="#ff4444" opacity=".8"/>
        <circle cx="305" cy="355" r="3" fill="#ff4444" opacity=".8"/>

        <!-- ═══ PART LABELS ═══ -->
        <g font-family="monospace" font-size="8.5" fill="#484F58" letter-spacing=".06em">
          <text x="250" y="510" text-anchor="middle">DJI AVATA · TOP VIEW · 1:1 SCALE REFERENCE</text>
        </g>

        <!-- ═══ INTERACTIVE HOTSPOTS ═══ -->
        <!-- Camera hotspot -->
        <g class="de-hs" data-part="camera" onclick="deSelect('camera')">
          <circle class="de-hs-ring" cx="250" cy="175" r="28" fill="rgba(0,255,204,.04)" stroke="#00ffcc" stroke-width="1.5" stroke-dasharray="4,3" opacity=".0"/>
          <circle cx="250" cy="175" r="28" fill="transparent"/>
          <text x="250" y="208" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#00ffcc" opacity=".7" letter-spacing=".05em" pointer-events="none">CAMERA</text>
        </g>

        <!-- Battery hotspot -->
        <g class="de-hs" data-part="battery" onclick="deSelect('battery')">
          <rect class="de-hs-ring" x="205" y="185" width="90" height="130" rx="8" fill="rgba(255,149,0,.04)" stroke="#ff9500" stroke-width="1.5" stroke-dasharray="4,3" opacity=".0"/>
          <rect x="205" y="185" width="90" height="130" rx="8" fill="transparent"/>
          <text x="250" y="328" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#ff9500" opacity=".7" letter-spacing=".05em" pointer-events="none">BATTERY</text>
        </g>

        <!-- FL Motor hotspot -->
        <g class="de-hs" data-part="motor-fl" onclick="deSelect('motor-fl')">
          <circle class="de-hs-ring" cx="132" cy="132" r="40" fill="rgba(74,158,255,.04)" stroke="#4a9eff" stroke-width="1.5" stroke-dasharray="4,3" opacity=".0"/>
          <circle cx="132" cy="132" r="40" fill="transparent"/>
          <text x="132" y="88" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#4a9eff" opacity=".7" pointer-events="none">FL MOTOR</text>
        </g>

        <!-- FR Motor hotspot -->
        <g class="de-hs" data-part="motor-fr" onclick="deSelect('motor-fr')">
          <circle class="de-hs-ring" cx="368" cy="132" r="40" fill="rgba(74,158,255,.04)" stroke="#4a9eff" stroke-width="1.5" stroke-dasharray="4,3" opacity=".0"/>
          <circle cx="368" cy="132" r="40" fill="transparent"/>
          <text x="368" y="88" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#4a9eff" opacity=".7" pointer-events="none">FR MOTOR</text>
        </g>

        <!-- RL Motor hotspot -->
        <g class="de-hs" data-part="motor-rl" onclick="deSelect('motor-rl')">
          <circle class="de-hs-ring" cx="132" cy="388" r="40" fill="rgba(74,158,255,.04)" stroke="#4a9eff" stroke-width="1.5" stroke-dasharray="4,3" opacity=".0"/>
          <circle cx="132" cy="388" r="40" fill="transparent"/>
          <text x="132" y="442" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#4a9eff" opacity=".7" pointer-events="none">RL MOTOR</text>
        </g>

        <!-- RR Motor hotspot -->
        <g class="de-hs" data-part="motor-rr" onclick="deSelect('motor-rr')">
          <circle class="de-hs-ring" cx="368" cy="388" r="40" fill="rgba(74,158,255,.04)" stroke="#4a9eff" stroke-width="1.5" stroke-dasharray="4,3" opacity=".0"/>
          <circle cx="368" cy="388" r="40" fill="transparent"/>
          <text x="368" y="442" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#4a9eff" opacity=".7" pointer-events="none">RR MOTOR</text>
        </g>

        <!-- Frame / Guards hotspot (arm area) -->
        <g class="de-hs" data-part="frame" onclick="deSelect('frame')">
          <polygon class="de-hs-ring" points="140,152 170,175 185,160 160,135" fill="rgba(0,255,148,.04)" stroke="#00FF94" stroke-width="1.5" stroke-dasharray="4,3" opacity=".0"/>
          <polygon points="140,152 170,175 185,160 160,135" fill="transparent"/>
          <text x="105" y="165" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#00FF94" opacity=".7" pointer-events="none">FRAME</text>
        </g>

        <!-- FC / ESC hotspot -->
        <g class="de-hs" data-part="fc" onclick="deSelect('fc')">
          <rect class="de-hs-ring" x="210" y="315" width="80" height="55" rx="5" fill="rgba(180,100,255,.04)" stroke="#b464ff" stroke-width="1.5" stroke-dasharray="4,3" opacity=".0"/>
          <rect x="210" y="315" width="80" height="55" rx="5" fill="transparent"/>
          <text x="250" y="382" text-anchor="middle" font-family="monospace" font-size="7.5" fill="#b464ff" opacity=".7" pointer-events="none">FC / ESC</text>
        </g>

        <!-- Video TX hotspot -->
        <g class="de-hs" data-part="vtx" onclick="deSelect('vtx')">
          <rect class="de-hs-ring" x="236" y="136" width="28" height="22" rx="4" fill="rgba(74,158,255,.04)" stroke="#4a9eff" stroke-width="1.5" stroke-dasharray="4,3" opacity=".0"/>
          <rect x="236" y="136" width="28" height="22" rx="4" fill="transparent"/>
        </g>
      </svg>
    </div>
    <button id="de-reset" onclick="deReset()">↩ RESET VIEW</button>
  </div>

  <!-- Info panel -->
  <div id="de-info">
    <div id="de-info-header">
      <p id="de-info-title">DJI AVATA</p>
      <p id="de-info-sub">Select a part to inspect</p>
    </div>
    <div id="de-info-body">
      <table class="de-spec-table" id="de-spec-tbl">
        <tr><td>Weight</td><td>410 g (with battery)</td></tr>
        <tr><td>Dimensions</td><td>180 × 232 × 80 mm</td></tr>
        <tr><td>Max Speed</td><td>97.2 km/h (S-Mode)</td></tr>
        <tr><td>Flight Time</td><td>~18 min</td></tr>
        <tr><td>Range</td><td>10 km (O3+)</td></tr>
        <tr><td>Video</td><td>4K / 60fps</td></tr>
        <tr><td>Prop Size</td><td>4-inch ducted</td></tr>
        <tr><td>Battery</td><td>2420mAh 4S LiPo</td></tr>
      </table>
      <p class="de-desc">לחץ על כל חלק ברחפן לקבלת מידע מפורט. הצבע ועל החלקים לגילוי.<br><br>Click any component on the drone to zoom in and see detailed technical specifications.</p>
    </div>
  </div>
</div>

<script>
const DE_PARTS = {
  camera: {
    title: 'מצלמה + ג׳ימבל',
    sub: 'Camera & Stabilization System',
    color: '#00ffcc',
    zoom: { x: 250, y: 175, scale: 2.8 },
    specs: [
      ['Sensor','1/1.7" CMOS'],
      ['Resolution','4K @ 60fps'],
      ['Slow Motion','2.7K@120fps / 1080p@120fps'],
      ['FOV','155° Ultra-Wide'],
      ['Aperture','f/2.8 fixed'],
      ['ISO (Video)','100 – 6400'],
      ['Shutter','1/8000s max'],
      ['Stabilization','RockSteady 3.0 EIS'],
      ['Horizon Steady','±35° correction'],
      ['Format','MP4 / MOV (H.264/H.265)'],
      ['Max Bitrate','150 Mbps'],
    ],
    desc: 'מצלמת 4K עם חיישן 1/1.7 אינץ׳ ועדשה 155 מעלות. מערכת RockSteady 3.0 מספקת ייצוב וידאו חלק גם במעוף מהיר.',
  },
  battery: {
    title: 'סוללה חכמה',
    sub: 'Intelligent Flight Battery',
    color: '#ff9500',
    zoom: { x: 250, y: 250, scale: 2.4 },
    specs: [
      ['Capacity','2420 mAh'],
      ['Voltage','14.8V (4S LiPo)'],
      ['Max Charge Power','38W'],
      ['Charging Time','~70 min (18W charger)'],
      ['Flight Time','~18 minutes'],
      ['Weight','95.5 g'],
      ['Energy','35.84 Wh'],
      ['Operating Temp','5°C to 40°C'],
      ['Discharge Temp','-10°C to 45°C'],
    ],
    desc: 'סוללת LiPo 4S עם ניהול חכם. מתריאה על מתח נמוך ומבצעת נחיתת חירום אוטומטית בסוללה קריטית.',
  },
  'motor-fl': {
    title: 'מנוע קדמי-שמאל (FL)',
    sub: 'Front-Left Brushless Motor — CW',
    color: '#4a9eff',
    zoom: { x: 132, y: 132, scale: 3.2 },
    specs: [
      ['KV Rating','~1700 KV'],
      ['Type','Brushless DC 3-phase'],
      ['Direction','CW (clockwise)'],
      ['Motor Size','2306 equivalent'],
      ['Voltage','14.8V (4S)'],
      ['Est. Max Thrust','~600 g per motor'],
      ['Bearing','Dual ball bearing'],
      ['Cooling','Integrated duct airflow'],
    ],
    desc: 'מנוע ללא מברשות (brushless) עם כיוון סיבוב CW. עובד עם מדחף 4 אינץ׳ בתוך מגן דקטד לבטיחות ויעילות אוירודינמית.',
  },
  'motor-fr': {
    title: 'מנוע קדמי-ימין (FR)',
    sub: 'Front-Right Brushless Motor — CCW',
    color: '#4a9eff',
    zoom: { x: 368, y: 132, scale: 3.2 },
    specs: [
      ['KV Rating','~1700 KV'],
      ['Type','Brushless DC 3-phase'],
      ['Direction','CCW (counter-clockwise)'],
      ['Motor Size','2306 equivalent'],
      ['Voltage','14.8V (4S)'],
      ['Est. Max Thrust','~600 g per motor'],
      ['Bearing','Dual ball bearing'],
      ['Cooling','Integrated duct airflow'],
    ],
    desc: 'מנוע ללא מברשות עם כיוון CCW. מנוע הקדמי-ימין פועל הפוך ממנוע הקדמי-שמאל לאיזון מומנט הכלי.',
  },
  'motor-rl': {
    title: 'מנוע אחורי-שמאל (RL)',
    sub: 'Rear-Left Brushless Motor — CCW',
    color: '#4a9eff',
    zoom: { x: 132, y: 388, scale: 3.2 },
    specs: [
      ['KV Rating','~1700 KV'],
      ['Type','Brushless DC 3-phase'],
      ['Direction','CCW (counter-clockwise)'],
      ['Motor Size','2306 equivalent'],
      ['Voltage','14.8V (4S)'],
      ['Est. Max Thrust','~600 g per motor'],
      ['Diagonal','163 mm motor-to-motor'],
    ],
    desc: 'מנוע אחורי-שמאל, כיוון CCW. ארבעת המנועים יחד מייצרים דחף כולל של ~2.4 ק"ג לרחפן שמשקלו 410 גרם.',
  },
  'motor-rr': {
    title: 'מנוע אחורי-ימין (RR)',
    sub: 'Rear-Right Brushless Motor — CW',
    color: '#4a9eff',
    zoom: { x: 368, y: 388, scale: 3.2 },
    specs: [
      ['KV Rating','~1700 KV'],
      ['Type','Brushless DC 3-phase'],
      ['Direction','CW (clockwise)'],
      ['Motor Size','2306 equivalent'],
      ['Voltage','14.8V (4S)'],
      ['Est. Max Thrust','~600 g per motor'],
      ['Diagonal','163 mm motor-to-motor'],
    ],
    desc: 'מנוע אחורי-ימין, כיוון CW. פריסת X-frame קלאסית: FL+RR = CW, FR+RL = CCW לאיזון הצינגל.',
  },
  frame: {
    title: 'שלדה + מגני מדחפים',
    sub: 'Frame & Ducted Prop Guards',
    color: '#00FF94',
    zoom: { x: 155, y: 152, scale: 2.5 },
    specs: [
      ['Material','Carbon fiber + polypropylene'],
      ['Guard Diameter','~147 mm per guard'],
      ['Frame Type','Integrated ducted X-frame'],
      ['Total Weight (bare)','314 g'],
      ['Duct Function','Efficiency + safety + thrust'],
      ['Wind Resistance','Level 5 (10.7 m/s)'],
      ['IP Rating','Not waterproof'],
      ['Arm Count','4 integrated arms'],
    ],
    desc: 'שלדה מקארבון פחמן עם מגני מדחפים משולבים מפוליפרופילן. המגנים הדקטדים מגבירים יעילות ומאפשרים טיסה בתוך מבנים.',
  },
  fc: {
    title: 'בקר טיסה + ESC',
    sub: 'Flight Controller & 4-in-1 ESC',
    color: '#b464ff',
    zoom: { x: 250, y: 345, scale: 2.8 },
    specs: [
      ['FC','DJI proprietary FC'],
      ['ESC Type','4-in-1 integrated'],
      ['ESC Protocol','DSHOT600'],
      ['Current Rating','35A continuous'],
      ['Sensors','IMU + Barometer + Vision'],
      ['GNSS','GPS + GLONASS (goggles mode)'],
      ['Max Ascent','6 m/s'],
      ['Max Descent','6 m/s'],
      ['Flight Modes','N / S / M (Normal/Sport/Manual)'],
    ],
    desc: 'בקר טיסה בעל קוד DJI קנייני. מסנכרן בין ה-ESC, ה-IMU והחיישנים לטיסה יציבה. ה-ESC 4in1 מפשט את הרכבה ומשקל.',
  },
  vtx: {
    title: 'משדר וידאו O3+',
    sub: 'DJI O3+ Video Transmission',
    color: '#4a9eff',
    zoom: { x: 250, y: 148, scale: 3.0 },
    specs: [
      ['System','DJI O3+ (OcuSync 3+)'],
      ['Max Range','10 km (CE) / 13 km (FCC)'],
      ['Frequencies','2.4 GHz / 5.8 GHz auto'],
      ['Max Video Bitrate','50 Mbps'],
      ['Live Feed Res','1080p / 100fps'],
      ['Latency','< 100 ms (with goggles)'],
      ['Channel Bandwidth','10 / 20 / 40 MHz'],
      ['Encryption','AES-256'],
    ],
    desc: 'מערכת O3+ מספקת שידור וידאו חי ב-1080p עם השהייה של פחות מ-100 אלפיות שנייה לגוגלס DJI. תומך ב-2.4 ו-5.8 GHz ועובר אוטומטית בין הערוצים.',
  },
};

let deActive = null;

function deSelect(partId) {
  const part = DE_PARTS[partId];
  if (!part) return;

  // Highlight ring
  document.querySelectorAll('.de-hs-ring').forEach(el => {
    el.style.opacity = '0';
    el.style.animation = 'none';
  });
  const parent = document.querySelector('[data-part="' + partId + '"]');
  if (parent) {
    const ring = parent.querySelector('.de-hs-ring');
    if (ring) {
      ring.style.opacity = '1';
      ring.style.stroke = part.color;
      ring.style.fill = 'rgba(' + hexToRgb(part.color) + ',.06)';
      ring.style.animation = 'de-pulse .9s ease-in-out infinite';
    }
  }

  // Zoom
  const svg = document.getElementById('de-svg');
  const wrap = document.getElementById('de-zoom-wrap');
  const wW = wrap.offsetWidth || 480;
  const wH = wrap.offsetHeight || 500;
  const z = part.zoom;
  const tx = wW/2 - z.x * z.scale;
  const ty = wH/2 - z.y * z.scale;
  svg.style.transform = 'translate(' + tx + 'px,' + ty + 'px) scale(' + z.scale + ')';

  // Info panel
  document.getElementById('de-info-title').textContent = part.title;
  document.getElementById('de-info-sub').textContent = part.sub;
  document.getElementById('de-info-sub').style.color = part.color;

  const tbl = document.getElementById('de-spec-tbl');
  tbl.innerHTML = part.specs.map(([k,v]) =>
    '<tr><td>' + k + '</td><td style="color:' + part.color + '">' + v + '</td></tr>'
  ).join('');

  let desc = document.getElementById('de-desc-p');
  if (!desc) {
    desc = document.createElement('p');
    desc.id = 'de-desc-p';
    desc.className = 'de-desc';
    tbl.parentNode.appendChild(desc);
  }
  desc.textContent = part.desc;

  deActive = partId;
}

function deReset() {
  const svg = document.getElementById('de-svg');
  svg.style.transform = 'translate(0,0) scale(1)';
  document.querySelectorAll('.de-hs-ring').forEach(el => {
    el.style.opacity = '0';
    el.style.animation = 'none';
  });
  document.getElementById('de-info-title').textContent = 'DJI AVATA';
  document.getElementById('de-info-sub').textContent = 'Select a part to inspect';
  document.getElementById('de-info-sub').style.color = '#8B949E';
  document.getElementById('de-spec-tbl').innerHTML = `
    <tr><td>Weight</td><td>410 g (with battery)</td></tr>
    <tr><td>Dimensions</td><td>180 × 232 × 80 mm</td></tr>
    <tr><td>Max Speed</td><td>97.2 km/h (S-Mode)</td></tr>
    <tr><td>Flight Time</td><td>~18 min</td></tr>
    <tr><td>Range</td><td>10 km (O3+)</td></tr>
    <tr><td>Video</td><td>4K / 60fps</td></tr>
    <tr><td>Prop Size</td><td>4-inch ducted</td></tr>
    <tr><td>Battery</td><td>2420mAh 4S LiPo</td></tr>
  `;
  const d = document.getElementById('de-desc-p');
  if (d) d.textContent = 'לחץ על כל חלק ברחפן לקבלת מידע מפורט.\\n\\nClick any component on the drone to zoom in and see detailed technical specifications.';
  deActive = null;
}

function hexToRgb(hex) {
  const r = parseInt(hex.slice(1,3),16);
  const g = parseInt(hex.slice(3,5),16);
  const b = parseInt(hex.slice(5,7),16);
  return r+','+g+','+b;
}

// Hover effects
document.querySelectorAll('.de-hs').forEach(el => {
  el.addEventListener('mouseenter', () => {
    const ring = el.querySelector('.de-hs-ring');
    if (ring && el.dataset.part !== deActive) {
      ring.style.opacity = '.5';
    }
  });
  el.addEventListener('mouseleave', () => {
    const ring = el.querySelector('.de-hs-ring');
    if (ring && el.dataset.part !== deActive) {
      ring.style.opacity = '0';
    }
  });
});
</script>
"""

# ---------------------------------------------------------------------------
# Build the Gradio interface
# ---------------------------------------------------------------------------
def build_ui() -> gr.Blocks:
    with gr.Blocks(css=TACTICAL_CSS, title="AVATA CO-PILOT") as demo:

        # ── Header ──────────────────────────────────────────────────────
        gr.HTML("""
<div style='padding:20px 24px 12px;border-bottom:1px solid var(--border);
            display:flex;align-items:center;gap:16px'>
  <div>
    <div style='font-family:var(--font-mono);font-size:18px;font-weight:500;
                color:var(--accent-green);letter-spacing:0.12em'>AVATA CO-PILOT</div>
    <div style='font-family:var(--font-mono);font-size:10px;color:var(--text-muted);
                letter-spacing:0.1em;margin-top:2px'>
      DJI AVATA FIELD ASSISTANT &nbsp;|&nbsp; OFFLINE &nbsp;|&nbsp; v1.0
    </div>
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

            # ── TAB 5: DRONE EXPLORER ───────────────────────────────────
            with gr.Tab("// Drone Explorer"):
                gr.HTML(DRONE_EXPLORER_HTML)

            # ── TAB 6: SYSTEM STATUS ─────────────────────────────────────
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
