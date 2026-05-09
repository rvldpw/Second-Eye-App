import streamlit as st
import time
import math
from datetime import datetime
import numpy as np
import io
from PIL import Image

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SecondEye — Navigation System",
    page_icon="👁",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;700&display=swap');

*, html, body { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif;
    background-color: #070710 !important;
    color: #e8e8f0;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem !important; max-width: 100% !important; }

.page-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 16px;
    border-bottom: 1px solid #1a1a2e;
    margin-bottom: 28px;
}
.logo { font-family: 'DM Mono', monospace; font-size: 20px; font-weight: 500; color: #fff; letter-spacing: -0.5px; }
.logo b { color: #5b8dee; }
.live-badge { display: flex; align-items: center; gap: 6px; font-size: 12px; color: #6b7280; font-family: 'DM Mono', monospace; }
.dot-live { width: 7px; height: 7px; border-radius: 50%; background: #3ecf8e; animation: blink 1.8s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

.phone-shell-wrap { display: flex; justify-content: center; align-items: flex-start; }
.phone-shell {
    width: 340px;
    background: #111118;
    border-radius: 42px;
    border: 2px solid #2a2a3e;
    box-shadow: 0 0 0 6px #0d0d18, 0 30px 80px rgba(0,0,0,0.7), inset 0 0 0 1px #1e1e2e;
    padding: 16px 10px 20px 10px;
    position: relative;
}
.phone-notch {
    width: 100px; height: 26px;
    background: #0d0d18;
    border-radius: 0 0 18px 18px;
    margin: 0 auto 10px auto;
    display: flex; align-items: center; justify-content: center; gap: 6px;
}
.notch-cam { width: 8px; height: 8px; border-radius: 50%; background: #1e1e2e; border: 1px solid #2a2a42; }
.notch-speaker { width: 40px; height: 4px; border-radius: 3px; background: #1e1e2e; }
.phone-screen { background: #0a0a14; border-radius: 28px; overflow: hidden; min-height: 680px; }
.phone-status-bar {
    display: flex; justify-content: space-between; align-items: center;
    padding: 6px 16px;
    background: #0a0a14;
    font-family: 'DM Mono', monospace; font-size: 10px; color: #6b7280;
}
.phone-home-btn { width: 100px; height: 4px; border-radius: 3px; background: #2a2a3e; margin: 12px auto 0 auto; }
.phone-side-btn { position: absolute; right: -8px; top: 100px; width: 4px; height: 50px; background: #1e1e2e; border-radius: 0 3px 3px 0; }
.phone-vol-btn  { position: absolute; left: -8px; top: 90px;  width: 4px; height: 35px; background: #1e1e2e; border-radius: 3px 0 0 3px; }
.phone-vol-btn2 { position: absolute; left: -8px; top: 135px; width: 4px; height: 35px; background: #1e1e2e; border-radius: 3px 0 0 3px; }

.app-topbar { display: flex; justify-content: space-between; align-items: center; padding: 10px 14px 6px 14px; border-bottom: 1px solid #1a1a2a; }
.app-logo { font-family: 'DM Mono', monospace; font-size: 14px; font-weight: 500; color: #fff; }
.app-logo span { color: #5b8dee; }
.app-status-chip { font-family: 'DM Mono', monospace; font-size: 9px; color: #3ecf8e; background: #0a1f14; border: 1px solid #3ecf8e44; border-radius: 20px; padding: 2px 8px; letter-spacing: 0.5px; }

.cam-section { position: relative; margin: 10px 12px; border-radius: 16px; overflow: hidden; border: 1px solid #1e1e2e; }

.alert-banner { margin: 8px 12px; border-radius: 12px; padding: 10px 14px; display: flex; align-items: center; gap: 10px; font-family: 'DM Mono', monospace; font-size: 11px; }
.ab-clear  { background: #0a1f14; border: 1px solid #3ecf8e33; color: #6ee7b7; }
.ab-warn   { background: #1f1500; border: 1px solid #f59e0b55; color: #fcd34d; }
.ab-danger { background: #2a0a0a; border: 1px solid #ef444455; color: #fca5a5; }
.ab-icon   { font-size: 18px; line-height: 1; }
.ab-title  { font-weight: 500; font-size: 12px; }
.ab-sub    { font-size: 10px; opacity: 0.7; margin-top: 1px; }

.nav-card  { margin: 8px 12px; background: #0f0f1e; border: 1px solid #1e1e2e; border-radius: 14px; padding: 12px 14px; }
.nav-label { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 2px; text-transform: uppercase; color: #5b8dee; margin-bottom: 6px; }
.nav-action { font-size: 22px; font-weight: 700; color: #fff; line-height: 1.1; }
.nav-detail { font-size: 11px; color: #6b7280; margin-top: 3px; }

.dest-card { margin: 8px 12px; background: #0f0f1e; border: 1px solid #1e1e2e; border-radius: 14px; padding: 12px 14px; }
.dest-name { font-size: 14px; font-weight: 600; color: #fff; margin-bottom: 2px; }
.dest-sub  { font-size: 10px; color: #6b7280; margin-bottom: 8px; }
.progress-track { background: #1a1a2e; border-radius: 4px; height: 5px; overflow: hidden; }
.progress-fill  { height: 100%; border-radius: 4px; background: linear-gradient(to right, #5b8dee, #3ecf8e); }

.haptic-row { margin: 8px 12px; background: #0f0f1e; border: 1px solid #1e1e2e; border-radius: 14px; padding: 10px 14px; display: flex; align-items: center; justify-content: space-between; }
.haptic-pattern { font-family: 'DM Mono', monospace; font-size: 13px; letter-spacing: 2px; }
.haptic-label   { font-family: 'DM Mono', monospace; font-size: 9px; color: #4b5563; text-transform: uppercase; letter-spacing: 1px; text-align: right; }

.scene-row   { margin: 6px 12px 4px 12px; }
.scene-label { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 2px; text-transform: uppercase; color: #4b5563; margin-bottom: 5px; }
.chip         { display: inline-block; border-radius: 20px; padding: 3px 10px; font-family: 'DM Mono', monospace; font-size: 10px; margin: 2px; }
.chip-default { background: #1a1a2e; border: 1px solid #2a2a42; color: #a5b4fc; }
.chip-warn    { background: #1f1500; border: 1px solid #f59e0b44; color: #fcd34d; }
.chip-danger  { background: #2a0a0a; border: 1px solid #ef444444; color: #fca5a5; }

.stats-row { display: flex; gap: 6px; margin: 6px 12px; }
.stat-box  { flex: 1; background: #0f0f1e; border: 1px solid #1e1e2e; border-radius: 12px; padding: 8px 10px; text-align: center; }
.stat-val  { font-family: 'DM Mono', monospace; font-size: 16px; font-weight: 500; color: #fff; }
.stat-lbl  { font-family: 'DM Mono', monospace; font-size: 8px; color: #4b5563; text-transform: uppercase; letter-spacing: 1px; margin-top: 1px; }

.panel-title { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: #5b8dee; margin-bottom: 14px; }
.info-card   { background: #0f0f1e; border: 1px solid #1e1e2e; border-radius: 12px; padding: 16px; margin-bottom: 12px; }
.info-card-title { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 2px; text-transform: uppercase; color: #4b5563; margin-bottom: 8px; }

.alert-log-item { font-family: 'DM Mono', monospace; font-size: 11px; color: #4b5563; padding: 4px 0; border-bottom: 1px solid #1a1a2a; }
.alert-log-item:last-child { border-bottom: none; }

.phase-row { display: flex; align-items: center; gap: 10px; margin: 6px 0; }
.phase-badge { font-family: 'DM Mono', monospace; font-size: 10px; padding: 2px 10px; border-radius: 20px; white-space: nowrap; }
.pb-on  { background: #0a1f14; color: #3ecf8e; border: 1px solid #3ecf8e44; }
.pb-off { background: #141420; color: #374151; border: 1px solid #1e1e2e; }
.phase-desc { font-size: 11px; color: #4b5563; }
.divider { border: none; border-top: 1px solid #1a1a2a; margin: 12px 0; }

.stButton > button { background: #5b8dee !important; color: white !important; border: none !important; border-radius: 8px !important; font-family: 'DM Mono', monospace !important; font-size: 12px !important; width: 100% !important; padding: 8px 0 !important; }
.stButton > button:hover { background: #4a7dde !important; }
div[data-testid="stSelectbox"] label { color: #6b7280 !important; font-size: 11px !important; }

/* Camera feed overlay styling */
.cam-overlay-img { width: 100%; border-radius: 16px; display: block; }
.loading-box { background: #060614; padding: 40px 20px; text-align: center; border-radius: 16px; font-family: 'DM Mono', monospace; font-size: 11px; color: #3ecf8e; }
</style>
""", unsafe_allow_html=True)

# ─── Load YOLOv8 (cached so it only downloads once) ──────────────────────────
@st.cache_resource
def load_model():
    """Download and cache YOLOv8n model (~6MB nano, fast inference)."""
    try:
        from ultralytics import YOLO
        model = YOLO("yolov8n.pt")   # downloads ~6MB on first run
        return model, None
    except Exception as e:
        return None, str(e)

# ─── DANGER classes in COCO dataset ──────────────────────────────────────────
DANGER_CLASSES  = {"person", "bicycle", "car", "motorbike", "bus", "truck",
                   "traffic light", "stop sign", "fire hydrant"}
WARN_CLASSES    = {"chair", "bench", "potted plant", "suitcase",
                   "backpack", "umbrella", "handbag", "bottle", "bowl",
                   "dog", "cat", "bird"}

def classify_detection(label: str):
    if label in DANGER_CLASSES:
        return "danger"
    if label in WARN_CLASSES:
        return "warn"
    return "default"

def run_yolo(model, pil_image: Image.Image):
    """Run YOLOv8 inference on a PIL image; return (annotated PIL image, detections list)."""
    img_array = np.array(pil_image)
    results   = model(img_array, verbose=False, conf=0.35)[0]
    # results.plot() returns BGR numpy array — convert via PIL
    annotated_bgr = results.plot()
    annotated_rgb = annotated_bgr[:, :, ::-1]   # BGR → RGB
    annotated_pil = Image.fromarray(annotated_rgb)

    detections = []
    for box in results.boxes:
        cls_id = int(box.cls[0])
        label  = model.names[cls_id]
        conf   = float(box.conf[0])
        level  = classify_detection(label)
        detections.append({"label": label, "conf": conf, "level": level})

    return annotated_pil, detections

# ─── Session State ────────────────────────────────────────────────────────────
defaults = {
    "running": False,
    "tick": 0,
    "alerts": [],
    "destination": "Blok M Station",
    "detections": [],          # from YOLO
    "last_obstacle": None,
    "model_loaded": False,
    "cam_mode": "webcam",      # "webcam" | "upload"
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── Static navigation data ───────────────────────────────────────────────────
NAV_STEPS = [
    ("Walk straight",  "~120m to intersection",   "↑"),
    ("Turn right",     "At Jl. Sudirman",          "→"),
    ("Cross lane",     "Wait for green signal",    "⇥"),
    ("Walk straight",  "~80m, destination close",  "↑"),
    ("Arrived",        "Main entrance on your left","✓"),
]

HAPTIC = {
    "danger": ("●  ●  ●", "#ef4444", "DOUBLE PULSE"),
    "warn":   ("●  ○  ●", "#f59e0b", "SINGLE PULSE"),
    "ok":     ("○  ○  ○", "#3ecf8e", "IDLE"),
}

def get_nav_state():
    t         = st.session_state.tick
    step      = NAV_STEPS[min(t // 10, len(NAV_STEPS) - 1)]
    distance  = max(200 - t * 5, 0)
    battery   = max(95 - t // 2, 20)
    progress  = max(0, 100 - distance // 2)
    steps_done= min(t // 10, len(NAV_STEPS) - 1) + 1
    return step, distance, battery, progress, steps_done

# ─── Helper: determine obstacle from detections ───────────────────────────────
def top_obstacle(detections):
    dangers = [d for d in detections if d["level"] == "danger"]
    warns   = [d for d in detections if d["level"] == "warn"]
    if dangers:
        d = max(dangers, key=lambda x: x["conf"])
        return {
            "name":   d["label"].title() + " detected",
            "level":  "danger",
            "icon":   "🚨",
            "action": f"Caution! {d['label'].title()} ahead — stop or reroute.",
        }
    if warns:
        d = max(warns, key=lambda x: x["conf"])
        return {
            "name":   d["label"].title() + " nearby",
            "level":  "warn",
            "icon":   "⚠️",
            "action": f"Slow down. {d['label'].title()} on path.",
        }
    return None

# ─── Page Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div class="logo"><b>Second</b>Eye &nbsp;<span style="font-weight:300;color:#4b5563;font-size:13px;">Navigation System</span></div>
    <div class="live-badge"><span class="dot-live"></span>Live Camera + YOLOv8 &nbsp;&middot;&nbsp; Phase 1</div>
</div>
""", unsafe_allow_html=True)

# ─── Model load status ────────────────────────────────────────────────────────
with st.spinner("Loading YOLOv8 model (first run ~6MB download)…"):
    model, model_err = load_model()

if model_err:
    st.error(f"YOLOv8 load failed: {model_err}")
    st.stop()

# ─── Main Layout ──────────────────────────────────────────────────────────────
col_phone, col_info, col_ctrl = st.columns([1.1, 1.1, 0.9])

# ══════════════════════════════════════════════════════════════════════════════
# LEFT  — Phone mockup with LIVE camera
# ══════════════════════════════════════════════════════════════════════════════
with col_phone:

    nav_step, distance, battery, progress, steps_done = get_nav_state()
    t        = st.session_state.tick
    now_str  = datetime.now().strftime("%H:%M")

    detections  = st.session_state.detections
    obstacle    = top_obstacle(detections)

    if obstacle:
        a_cls = "ab-danger" if obstacle["level"] == "danger" else "ab-warn"
        a_ico, a_ttl, a_sub = obstacle["icon"], obstacle["name"], obstacle["action"]
    else:
        a_cls, a_ico, a_ttl, a_sub = "ab-clear", "✅", "Path clear", "No obstacles detected"

    hap_key                    = obstacle["level"] if obstacle else "ok"
    hap_pat, hap_col, hap_lbl = HAPTIC[hap_key]

    nav_label, nav_det, nav_arrow = nav_step
    est_min = max(1, distance // 60)

    # chips from YOLO detections
    chips_html = ""
    if detections:
        for d in detections[:6]:
            chips_html += f'<span class="chip chip-{d["level"]}">{d["label"]} {d["conf"]:.0%}</span>'
    else:
        chips_html = '<span class="chip chip-default">awaiting camera…</span>'

    # Phone shell open
    phone_top = (
        '<div class="phone-shell-wrap">'
        '<div class="phone-shell">'
        '<div class="phone-vol-btn"></div>'
        '<div class="phone-vol-btn2"></div>'
        '<div class="phone-side-btn"></div>'
        '<div class="phone-notch">'
        '<div class="notch-cam"></div>'
        '<div class="notch-speaker"></div>'
        '<div class="notch-cam"></div>'
        '</div>'
        '<div class="phone-screen">'
        '<div class="phone-status-bar">'
        '<span>' + now_str + '</span>'
        '<span>&#9679;&#9679;&#9679; &nbsp;' + str(battery) + '%</span>'
        '</div>'
        '<div class="app-topbar">'
        '<div class="app-logo"><span>Second</span>Eye</div>'
        '<div class="app-status-chip">&#9679; LIVE</div>'
        '</div>'
        '<div class="cam-section">'   # camera slot — closed below after st widget
    )
    st.markdown(phone_top, unsafe_allow_html=True)

    # ── Camera frame slot (native Streamlit widget, inside phone shell) ────
    cam_placeholder  = st.empty()
    frame_placeholder= st.empty()

    # Phone shell close
    phone_bottom = (
        '</div>'  # .cam-section

        '<div class="alert-banner ' + a_cls + '">'
        '<div class="ab-icon">' + a_ico + '</div>'
        '<div>'
        '<div class="ab-title">' + a_ttl + '</div>'
        '<div class="ab-sub">' + a_sub + '</div>'
        '</div>'
        '</div>'

        '<div class="nav-card">'
        '<div class="nav-label">Next action</div>'
        '<div class="nav-action">' + nav_arrow + ' ' + nav_label + '</div>'
        '<div class="nav-detail">' + nav_det + '</div>'
        '</div>'

        '<div class="dest-card">'
        '<div class="nav-label">Destination</div>'
        '<div class="dest-name">' + st.session_state.destination + '</div>'
        '<div class="dest-sub">' + str(distance) + 'm remaining &middot; est. ' + str(est_min) + ' min</div>'
        '<div class="progress-track"><div class="progress-fill" style="width:' + str(progress) + '%"></div></div>'
        '</div>'

        '<div class="haptic-row">'
        '<div>'
        '<div class="nav-label">Haptic feedback</div>'
        '<div class="haptic-pattern" style="color:' + hap_col + '">' + hap_pat + '</div>'
        '</div>'
        '<div class="haptic-label">' + hap_lbl + '</div>'
        '</div>'

        '<div class="scene-row">'
        '<div class="scene-label">Detected in scene</div>'
        + chips_html +
        '</div>'

        '<div class="stats-row">'
        '<div class="stat-box"><div class="stat-val">' + str(battery) + '%</div><div class="stat-lbl">Battery</div></div>'
        '<div class="stat-box"><div class="stat-val">' + ("ON" if st.session_state.running else "OFF") + '</div><div class="stat-lbl">AI Active</div></div>'
        '<div class="stat-box"><div class="stat-val">' + str(steps_done) + '/' + str(len(NAV_STEPS)) + '</div><div class="stat-lbl">Steps</div></div>'
        '<div class="stat-box"><div class="stat-val">' + str(len(st.session_state.alerts)) + '</div><div class="stat-lbl">Alerts</div></div>'
        '</div>'

        '</div>'   # .phone-screen
        '<div class="phone-home-btn"></div>'
        '</div>'   # .phone-shell
        '</div>'   # .phone-shell-wrap
    )
    st.markdown(phone_bottom, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MIDDLE — Alert log + architecture
# ══════════════════════════════════════════════════════════════════════════════
with col_info:
    st.markdown("<div class='panel-title'>Alert History</div>", unsafe_allow_html=True)

    if obstacle:
        ts    = datetime.now().strftime("%H:%M:%S")
        entry = "[" + ts + "]  " + obstacle["icon"] + "  " + obstacle["name"]
        if not st.session_state.alerts or st.session_state.alerts[-1] != entry:
            st.session_state.alerts.append(entry)
            if len(st.session_state.alerts) > 10:
                st.session_state.alerts.pop(0)

    log_html = ""
    for item in reversed(st.session_state.alerts[-6:]):
        log_html += '<div class="alert-log-item">' + item + '</div>'
    if not log_html:
        log_html = '<div class="alert-log-item" style="color:#2a2a42;">No alerts yet &mdash; start camera</div>'

    st.markdown(
        '<div class="info-card"><div class="info-card-title">Recent Events</div>' + log_html + '</div>',
        unsafe_allow_html=True
    )

    st.markdown("<div class='panel-title' style='margin-top:16px;'>System Architecture</div>", unsafe_allow_html=True)
    st.markdown("""
<div class="info-card">
  <div class="info-card-title">Device Layer (Glasses)</div>
  <div style="font-size:12px;color:#6b7280;line-height:1.8;">
    &#9679; Small camera module<br>
    &#9679; Bone conduction speaker<br>
    &#9679; Dual vibration motors<br>
    &#9679; Bluetooth Low Energy<br>
    &#9679; Low-power MCU only
  </div>
</div>
<div class="info-card">
  <div class="info-card-title">Phone Layer (AI Brain)</div>
  <div style="font-size:12px;color:#6b7280;line-height:1.8;">
    &#9679; YOLOv8n obstacle detection<br>
    &#9679; GPS + route planning<br>
    &#9679; Scene understanding (Ph.2)<br>
    &#9679; Event-triggered, not streaming<br>
    &#9679; Offline-capable navigation
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# RIGHT — Controls
# ══════════════════════════════════════════════════════════════════════════════
with col_ctrl:
    st.markdown("<div class='panel-title'>Controls</div>", unsafe_allow_html=True)

    dest = st.selectbox(
        "Destination",
        ["Blok M Station", "Monas", "Grand Indonesia", "Kota Tua", "Bundaran HI", "Stasiun Sudirman"],
    )
    st.session_state.destination = dest

    st.selectbox(
        "Active Phase",
        ["Phase 1 — Obstacle + GPS", "Phase 2 — Scene Understanding", "Phase 3 — Full Second Eye"],
    )

    cam_mode = st.radio(
        "Camera input",
        ["Webcam (live)", "Upload image/video"],
        horizontal=True,
        label_visibility="visible",
    )
    st.session_state.cam_mode = "webcam" if "Webcam" in cam_mode else "upload"

    c1, c2 = st.columns(2)
    with c1:
        lbl = "⏸ Pause" if st.session_state.running else "▶ Start"
        if st.button(lbl, key="btn_start"):
            st.session_state.running = not st.session_state.running
    with c2:
        if st.button("↺ Reset", key="btn_reset"):
            st.session_state.tick     = 0
            st.session_state.alerts   = []
            st.session_state.running  = False
            st.session_state.detections = []

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-title'>System Phases</div>", unsafe_allow_html=True)

    phase_html = ""
    for ph, desc, active in [
        ("Phase 1", "Obstacle + GPS guidance",        True),
        ("Phase 2", "Scene understanding",             False),
        ("Phase 3", "Spatial memory + predictive AI",  False),
    ]:
        cls = "pb-on" if active else "pb-off"
        phase_html += (
            '<div class="phase-row">'
            '<span class="phase-badge ' + cls + '">' + ph + '</span>'
            '<span class="phase-desc">' + desc + '</span>'
            '</div>'
        )
    st.markdown('<div class="info-card">' + phase_html + '</div>', unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("<div class='panel-title'>Design Principles</div>", unsafe_allow_html=True)

    pr_html = ""
    for title, desc in [
        ("Event-triggered AI",  "Wakes only when needed"),
        ("Decision guidance",   "Move right, not object list"),
        ("Vibration first",     "Voice only when critical"),
        ("Phone as brain",      "Glasses stay light + cheap"),
        ("Offline-capable",     "No cloud dependency"),
    ]:
        pr_html += (
            '<div style="margin:8px 0;">'
            '<div style="font-family:\'DM Mono\',monospace;font-size:10px;color:#5b8dee;">' + title + '</div>'
            '<div style="font-size:11px;color:#4b5563;">' + desc + '</div>'
            '</div>'
        )
    st.markdown('<div class="info-card">' + pr_html + '</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CAMERA PROCESSING  (runs after layout is drawn)
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.cam_mode == "upload":
    # ── Upload mode ──────────────────────────────────────────────────────────
    uploaded = st.file_uploader(
        "Upload an image to analyse",
        type=["jpg", "jpeg", "png", "bmp", "webp"],
        key="uploader",
    )
    if uploaded:
        pil_img = Image.open(uploaded).convert("RGB")
        annotated_pil, dets = run_yolo(model, pil_img)
        st.session_state.detections = dets
        with cam_placeholder:
            st.image(annotated_pil, use_container_width=True, caption="YOLOv8 detections")
        if st.session_state.running:
            st.session_state.tick += 1
        st.rerun()
    else:
        with cam_placeholder:
            st.markdown(
                '<div class="loading-box">📁 Upload an image to run detection</div>',
                unsafe_allow_html=True,
            )

else:
    # ── Webcam mode ──────────────────────────────────────────────────────────
    with cam_placeholder:
        frame_data = st.camera_input(
            "Camera feed (allow camera access when prompted)",
            key=f"cam_{st.session_state.tick}",
            label_visibility="collapsed",
        )

    if frame_data is not None:
        pil_img = Image.open(io.BytesIO(frame_data.getvalue())).convert("RGB")
        annotated_pil, dets = run_yolo(model, pil_img)
        st.session_state.detections = dets

        with frame_placeholder:
            st.image(annotated_pil, use_container_width=True, caption="YOLOv8 live detections")

        if st.session_state.running:
            time.sleep(0.5)
            st.session_state.tick += 1
            st.rerun()
    else:
        with cam_placeholder:
            st.markdown(
                '<div class="loading-box">📷 Click the camera button above to capture a frame for AI analysis</div>',
                unsafe_allow_html=True,
            )
