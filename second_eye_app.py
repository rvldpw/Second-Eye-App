import streamlit as st
import time
import io
from datetime import datetime
from PIL import Image
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SecondEye",
    page_icon="👁",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, .stApp { background: #08080f !important; color: #e2e2f0; font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* top bar */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 14px 28px;
    background: #0c0c18;
    border-bottom: 1px solid #1c1c30;
}
.topbar-logo { font-family: 'JetBrains Mono', monospace; font-size: 18px; font-weight: 500; color: #fff; }
.topbar-logo b { color: #6390f5; }
.topbar-right { display: flex; align-items: center; gap: 16px; }
.status-pill {
    display: flex; align-items: center; gap: 6px;
    background: #0d1f12; border: 1px solid #2ecf8044;
    border-radius: 20px; padding: 4px 12px;
    font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #2ecf80;
}
.pulse-dot { width: 6px; height: 6px; border-radius: 50%; background: #2ecf80; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:.3} }
.time-tag { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #4b5563; }

/* section label */
.sec-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px; letter-spacing: 2.5px; text-transform: uppercase;
    color: #3b5bdb; margin-bottom: 8px; margin-top: 18px;
}
.sec-label:first-child { margin-top: 0; }

/* cards */
.card { background: #111120; border: 1px solid #1e1e32; border-radius: 12px; padding: 14px 16px; margin-bottom: 10px; }
.card-danger { border-color: #ef444466; background: #1a0808; }
.card-warn   { border-color: #f59e0b66; background: #150f00; }
.card-ok     { border-color: #2ecf8040; background: #0a1810; }

/* alert */
.alert-row { display: flex; align-items: flex-start; gap: 12px; }
.alert-icon { font-size: 22px; flex-shrink: 0; }
.alert-title { font-size: 14px; font-weight: 600; margin-bottom: 3px; }
.alert-sub   { font-size: 11px; opacity: .75; line-height: 1.4; }
.col-danger { color: #fca5a5; }
.col-warn   { color: #fcd34d; }
.col-ok     { color: #6ee7b7; }

/* nav */
.nav-arrow { font-size: 38px; font-weight: 700; color: #fff; line-height: 1; }
.nav-step  { font-size: 16px; font-weight: 600; color: #fff; margin-top: 4px; }
.nav-sub   { font-size: 12px; color: #6b7280; margin-top: 3px; }

/* progress */
.dest-name { font-size: 15px; font-weight: 600; color: #fff; }
.dest-dist { font-size: 11px; color: #6b7280; margin: 3px 0 10px; }
.prog-track { height: 6px; background: #1c1c30; border-radius: 4px; overflow: hidden; }
.prog-fill  { height: 100%; border-radius: 4px; background: linear-gradient(90deg,#3b5bdb,#2ecf80); }

/* haptic */
.haptic-row { display: flex; justify-content: space-between; align-items: center; }
.haptic-dots { font-family: 'JetBrains Mono', monospace; font-size: 18px; letter-spacing: 5px; }
.haptic-lbl  { font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #4b5563; letter-spacing: 1.5px; text-transform: uppercase; }

/* chips */
.chips-wrap { display: flex; flex-wrap: wrap; gap: 5px; }
.chip   { border-radius: 20px; padding: 3px 10px; font-family: 'JetBrains Mono', monospace; font-size: 10px; }
.chip-d { background:#240a0a; border:1px solid #ef444455; color:#fca5a5; }
.chip-w { background:#1a1100; border:1px solid #f59e0b55; color:#fcd34d; }
.chip-n { background:#141428; border:1px solid #2a2a48; color:#a5b4fc; }

/* stats */
.stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.stat-card  { background:#111120; border:1px solid #1e1e32; border-radius:10px; padding:10px; text-align:center; }
.stat-val   { font-family:'JetBrains Mono',monospace; font-size:20px; font-weight:500; color:#fff; }
.stat-lbl   { font-family:'JetBrains Mono',monospace; font-size:8px; color:#4b5563; text-transform:uppercase; letter-spacing:1px; margin-top:3px; }

/* camera wrapper */
.cam-header {
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 16px;
    background: #0e0e1c;
    border: 1px solid #1c1c30;
    border-radius: 12px 12px 0 0;
}
.cam-title { font-family:'JetBrains Mono',monospace; font-size:10px; color:#6390f5; letter-spacing:2px; text-transform:uppercase; }
.cam-rec   { display:flex; align-items:center; gap:5px; font-family:'JetBrains Mono',monospace; font-size:10px; color:#ef4444; }
.cam-dot   { width:6px; height:6px; border-radius:50%; background:#ef4444; animation:blink 1s infinite; }
.cam-body  { border:1px solid #1c1c30; border-top:none; border-radius:0 0 12px 12px; overflow:hidden; background:#08080f; }

/* detection bar */
.det-bar {
    display:flex; align-items:center; gap:10px; flex-wrap:wrap;
    background:#0e0e1c; border:1px solid #1c1c30; border-radius:10px;
    padding:10px 16px; margin-top:12px;
}
.det-count { font-family:'JetBrains Mono',monospace; font-size:11px; color:#6b7280; }
.det-count b { color:#e2e2f0; }

/* log */
.log-item { font-family:'JetBrains Mono',monospace; font-size:10px; padding:5px 0; border-bottom:1px solid #14142a; display:flex; gap:8px; }
.log-item:last-child { border-bottom:none; }
.log-ts  { color:#2a2a4a; flex-shrink:0; }
.log-msg { color:#6b7280; }
.log-empty { font-family:'JetBrains Mono',monospace; font-size:10px; color:#1e1e38; padding:6px 0; }

/* phases / principles */
.row-item { padding:6px 0; border-bottom:1px solid #14142a; }
.row-item:last-child { border-bottom:none; }
.row-title  { font-size:11px; font-weight:500; color:#6390f5; margin-bottom:2px; }
.row-desc   { font-size:10px; color:#374151; line-height:1.4; }
.phase-badge { font-family:'JetBrains Mono',monospace; font-size:9px; padding:2px 9px; border-radius:20px; }
.ph-on  { background:#0a1f14; color:#2ecf80; border:1px solid #2ecf8040; }
.ph-off { background:#111120; color:#2a2a4a; border:1px solid #1e1e32; }
.phase-row { display:flex; align-items:center; gap:10px; padding:6px 0; border-bottom:1px solid #14142a; }
.phase-row:last-child { border-bottom:none; }
.phase-desc { font-size:11px; color:#4b5563; }

/* controls */
.stButton>button {
    background:#3b5bdb !important; color:#fff !important; border:none !important;
    border-radius:8px !important; font-family:'JetBrains Mono',monospace !important;
    font-size:11px !important; padding:8px 0 !important; width:100% !important;
}
.stButton>button:hover { background:#2f4ac7 !important; }
div[data-testid="stSelectbox"] label { color:#6b7280 !important; font-size:11px !important; }
div[data-testid="stCameraInput"]>label { display:none !important; }
div[data-testid="stCameraInput"] { margin:0 !important; }
div[data-testid="stFileUploader"]>label { color:#6b7280 !important; font-size:11px !important; }
div[data-testid="stImage"] { margin:0 !important; }
div[data-testid="stRadio"]>label { color:#6b7280 !important; font-size:11px !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
DEFAULTS = {
    "tick": 0, "alerts": [], "destination": "Blok M Station",
    "detections": [], "cam_mode": "webcam", "last_frame_id": None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Model ─────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    try:
        from ultralytics import YOLO
        return YOLO("yolov8n.pt"), None
    except Exception as e:
        return None, str(e)

DANGER_CLS = {"person","bicycle","car","motorbike","bus","truck","traffic light","stop sign"}
WARN_CLS   = {"chair","bench","potted plant","suitcase","backpack","umbrella","dog","cat","bird"}

def cls_level(label):
    if label in DANGER_CLS: return "danger"
    if label in WARN_CLS:   return "warn"
    return "default"

def run_yolo(model, pil_img):
    arr     = np.array(pil_img)
    results = model(arr, verbose=False, conf=0.35)[0]
    ann_rgb = results.plot()[:, :, ::-1]
    dets    = [{"label": model.names[int(b.cls[0])], "conf": float(b.conf[0]),
                "level": cls_level(model.names[int(b.cls[0])])} for b in results.boxes]
    return Image.fromarray(ann_rgb), dets

def top_obstacle(dets):
    for lv in ("danger","warn"):
        pool = [d for d in dets if d["level"] == lv]
        if pool:
            d = max(pool, key=lambda x: x["conf"])
            return {"level": lv,
                    "icon":  "🚨" if lv=="danger" else "⚠️",
                    "name":  d["label"].title() + " detected",
                    "action": (f"Stop! {d['label'].title()} ahead — reroute."
                               if lv=="danger" else
                               f"Slow down — {d['label'].title()} nearby.")}
    return None

# ── Static data ───────────────────────────────────────────────────────────────
NAV_STEPS = [
    ("↑","Walk straight","120m to next intersection"),
    ("→","Turn right","At Jl. Sudirman"),
    ("⇥","Cross lane","Wait for green signal"),
    ("↑","Walk straight","80m, destination ahead"),
    ("✓","Arrived","Main entrance on your left"),
]
HAPTIC = {
    "danger": ("● ● ●","#ef4444","TRIPLE PULSE"),
    "warn":   ("● ○ ●","#f59e0b","DOUBLE PULSE"),
    "ok":     ("○ ○ ○","#2ecf80","IDLE"),
}

def nav_state():
    t   = st.session_state.tick
    step     = NAV_STEPS[min(t // 12, len(NAV_STEPS)-1)]
    distance = max(200 - t * 6, 0)
    battery  = max(97 - t // 3, 20)
    progress = min(int((200 - distance) / 2), 100)
    steps_done = min(t // 12, len(NAV_STEPS)-1) + 1
    return step, distance, battery, progress, steps_done

# ═════════════════════════════════════════════════════════════════════════════
# LOAD
# ═════════════════════════════════════════════════════════════════════════════
with st.spinner("Loading YOLOv8n…"):
    model, model_err = load_model()

# ── Top bar ───────────────────────────────────────────────────────────────────
now = datetime.now().strftime("%H:%M:%S")
status_text = "YOLOv8 · LIVE" if not model_err else "MODEL ERROR"
st.markdown(f"""
<div class="topbar">
  <div class="topbar-logo"><b>Second</b>Eye
    <span style="font-weight:300;font-size:13px;color:#374151;margin-left:8px;">Navigation System</span>
  </div>
  <div class="topbar-right">
    <div class="status-pill"><div class="pulse-dot"></div>{status_text}</div>
    <div class="time-tag">{now}</div>
  </div>
</div>
""", unsafe_allow_html=True)

if model_err:
    st.error(f"YOLOv8 failed: {model_err}")
    st.stop()

# ── Columns ───────────────────────────────────────────────────────────────────
col_left, col_center, col_right = st.columns([1.1, 2.1, 0.95], gap="small")

step, distance, battery, progress, steps_done = nav_state()
dets     = st.session_state.detections
obstacle = top_obstacle(dets)
hap_key  = obstacle["level"] if obstacle else "ok"
hap_dots, hap_col, hap_lbl = HAPTIC[hap_key]

# ─────────────────────── LEFT ─────────────────────────────────────────────────
with col_left:
    # Alert card
    if obstacle:
        card_cls = "card-danger" if obstacle["level"]=="danger" else "card-warn"
        col_cls  = "col-danger"  if obstacle["level"]=="danger" else "col-warn"
    else:
        card_cls, col_cls = "card-ok", "col-ok"

    icon  = obstacle["icon"]   if obstacle else "✅"
    title = obstacle["name"]   if obstacle else "Path clear"
    sub   = obstacle["action"] if obstacle else "No obstacles detected"

    st.markdown(f"""
<div class="sec-label">Alert</div>
<div class="card {card_cls}">
  <div class="alert-row">
    <div class="alert-icon">{icon}</div>
    <div>
      <div class="alert-title {col_cls}">{title}</div>
      <div class="alert-sub {col_cls}">{sub}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

    # Nav card
    arr, sname, sdetail = step
    st.markdown(f"""
<div class="sec-label">Next action</div>
<div class="card">
  <div class="nav-arrow">{arr}</div>
  <div class="nav-step">{sname}</div>
  <div class="nav-sub">{sdetail}</div>
</div>""", unsafe_allow_html=True)

    # Destination
    est = max(1, distance // 60)
    st.markdown(f"""
<div class="sec-label">Destination</div>
<div class="card">
  <div class="dest-name">{st.session_state.destination}</div>
  <div class="dest-dist">{distance}m · est. {est} min</div>
  <div class="prog-track"><div class="prog-fill" style="width:{progress}%"></div></div>
</div>""", unsafe_allow_html=True)

    # Haptic
    st.markdown(f"""
<div class="sec-label">Haptic</div>
<div class="card">
  <div class="haptic-row">
    <div class="haptic-dots" style="color:{hap_col}">{hap_dots}</div>
    <div class="haptic-lbl">{hap_lbl}</div>
  </div>
</div>""", unsafe_allow_html=True)

    # Scene chips
    chips_html = ""
    for d in dets[:8]:
        cm = {"danger":"chip-d","warn":"chip-w","default":"chip-n"}
        chips_html += f'<span class="chip {cm[d["level"]]}">{d["label"]} {d["conf"]:.0%}</span>'
    if not chips_html:
        chips_html = '<span class="chip chip-n">awaiting frame…</span>'

    st.markdown(f"""
<div class="sec-label">Scene objects</div>
<div class="card">
  <div class="chips-wrap">{chips_html}</div>
</div>""", unsafe_allow_html=True)

    # Stats
    st.markdown(f"""
<div class="sec-label">Stats</div>
<div class="stats-grid">
  <div class="stat-card"><div class="stat-val">{battery}%</div><div class="stat-lbl">Battery</div></div>
  <div class="stat-card"><div class="stat-val">{steps_done}/{len(NAV_STEPS)}</div><div class="stat-lbl">Steps</div></div>
  <div class="stat-card"><div class="stat-val">{len(dets)}</div><div class="stat-lbl">Objects</div></div>
  <div class="stat-card"><div class="stat-val">{len(st.session_state.alerts)}</div><div class="stat-lbl">Alerts</div></div>
</div>""", unsafe_allow_html=True)

# ─────────────────────── CENTER ───────────────────────────────────────────────
with col_center:
    st.markdown('<div class="sec-label">Live Camera · AI Detection</div>', unsafe_allow_html=True)

    cam_mode = st.radio(
        "Input", ["📷  Webcam", "🖼  Upload image"],
        horizontal=True, label_visibility="collapsed",
    )
    use_webcam = "Webcam" in cam_mode

    ts_str = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
<div class="cam-header">
  <div class="cam-title">👁 SecondEye · CAM-01 · Phase 1</div>
  <div class="cam-rec"><div class="cam-dot"></div>REC {ts_str}</div>
</div>
<div class="cam-body">""", unsafe_allow_html=True)

    frame_slot     = st.empty()
    annotated_slot = st.empty()

    st.markdown("</div>", unsafe_allow_html=True)

    # Detection summary
    d_n = sum(1 for d in dets if d["level"]=="danger")
    w_n = sum(1 for d in dets if d["level"]=="warn")
    o_n = sum(1 for d in dets if d["level"]=="default")
    bar = ""
    if d_n: bar += f'<span class="chip chip-d">🚨 {d_n} danger</span>'
    if w_n: bar += f'<span class="chip chip-w">⚠️ {w_n} caution</span>'
    if o_n: bar += f'<span class="chip chip-n">{o_n} other</span>'
    if not dets: bar = '<span class="chip chip-n">No detections yet</span>'

    st.markdown(f"""
<div class="det-bar">
  <div class="det-count">YOLOv8n · <b>{len(dets)}</b> objects detected</div>
  {bar}
</div>""", unsafe_allow_html=True)

    # ── Camera logic (no auto-rerun loop — only reruns on new frame) ──────
    if use_webcam:
        with frame_slot:
            captured = st.camera_input("cam", label_visibility="collapsed")

        if captured is not None:
            fid = hash(captured.getvalue())
            if fid != st.session_state.last_frame_id:
                pil_img = Image.open(io.BytesIO(captured.getvalue())).convert("RGB")
                ann_pil, new_dets = run_yolo(model, pil_img)
                st.session_state.detections    = new_dets
                st.session_state.last_frame_id = fid
                st.session_state.tick         += 1
                obs = top_obstacle(new_dets)
                if obs:
                    ts    = datetime.now().strftime("%H:%M:%S")
                    entry = f"[{ts}] {obs['icon']} {obs['name']}"
                    logs  = st.session_state.alerts
                    if not logs or logs[-1] != entry:
                        logs.append(entry)
                        if len(logs) > 20: logs.pop(0)
                with annotated_slot:
                    st.image(ann_pil, use_container_width=True)
                st.rerun()
        else:
            with annotated_slot:
                st.markdown("""
<div style="text-align:center;padding:60px 20px;color:#2a2a4a;font-family:'JetBrains Mono',monospace;font-size:12px;">
  📷 Click the shutter button above<br>to capture a frame for AI detection
</div>""", unsafe_allow_html=True)

    else:
        with frame_slot:
            uploaded = st.file_uploader(
                "Image", type=["jpg","jpeg","png","bmp","webp"],
                label_visibility="collapsed",
            )
        if uploaded:
            pil_img = Image.open(uploaded).convert("RGB")
            ann_pil, new_dets = run_yolo(model, pil_img)
            st.session_state.detections = new_dets
            st.session_state.tick      += 1
            obs = top_obstacle(new_dets)
            if obs:
                ts    = datetime.now().strftime("%H:%M:%S")
                entry = f"[{ts}] {obs['icon']} {obs['name']}"
                st.session_state.alerts.append(entry)
                if len(st.session_state.alerts) > 20:
                    st.session_state.alerts.pop(0)
            with annotated_slot:
                st.image(ann_pil, use_container_width=True)
        else:
            with annotated_slot:
                st.markdown("""
<div style="text-align:center;padding:60px 20px;color:#2a2a4a;font-family:'JetBrains Mono',monospace;font-size:12px;">
  🖼 Upload an image to run detection
</div>""", unsafe_allow_html=True)

# ─────────────────────── RIGHT ────────────────────────────────────────────────
with col_right:
    st.markdown('<div class="sec-label">Destination</div>', unsafe_allow_html=True)
    dest = st.selectbox(
        "dest",
        ["Blok M Station","Monas","Grand Indonesia","Kota Tua","Bundaran HI","Stasiun Sudirman"],
        label_visibility="collapsed",
    )
    st.session_state.destination = dest

    if st.button("↺  Reset session"):
        for k, v in DEFAULTS.items():
            st.session_state[k] = v
        st.rerun()

    # Alert log
    st.markdown('<div class="sec-label" style="margin-top:16px;">Alert log</div>', unsafe_allow_html=True)
    st.markdown('<div class="card" style="padding:10px 14px;">', unsafe_allow_html=True)
    if st.session_state.alerts:
        log_html = ""
        for item in reversed(st.session_state.alerts[-10:]):
            parts = item.split("] ", 1)
            ts_p  = parts[0] + "]" if len(parts) > 1 else ""
            msg_p = parts[1] if len(parts) > 1 else item
            log_html += f'<div class="log-item"><span class="log-ts">{ts_p}</span><span class="log-msg">{msg_p}</span></div>'
        st.markdown(log_html, unsafe_allow_html=True)
    else:
        st.markdown('<div class="log-empty">No alerts yet.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Phases
    st.markdown('<div class="sec-label" style="margin-top:16px;">System phases</div>', unsafe_allow_html=True)
    phases_html = '<div class="card" style="padding:10px 14px;">'
    for ph, desc, active in [
        ("Phase 1","Obstacle + GPS",True),
        ("Phase 2","Scene understanding",False),
        ("Phase 3","Predictive AI",False),
    ]:
        c = "ph-on" if active else "ph-off"
        phases_html += f'<div class="phase-row"><span class="phase-badge {c}">{ph}</span><span class="phase-desc">{desc}</span></div>'
    st.markdown(phases_html + '</div>', unsafe_allow_html=True)

    # Principles
    st.markdown('<div class="sec-label" style="margin-top:16px;">Design principles</div>', unsafe_allow_html=True)
    prins = [
        ("Event-triggered AI","Runs only when needed"),
        ("Decision guidance","Tells you where to go"),
        ("Vibration first","Audio only for critical"),
        ("Phone as brain","Glasses stay minimal"),
        ("Offline-capable","No cloud required"),
    ]
    pr_html = '<div class="card" style="padding:10px 14px;">'
    for t, d in prins:
        pr_html += f'<div class="row-item"><div class="row-title">{t}</div><div class="row-desc">{d}</div></div>'
    st.markdown(pr_html + '</div>', unsafe_allow_html=True)

    # Architecture
    st.markdown('<div class="sec-label" style="margin-top:16px;">Architecture</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="card" style="padding:10px 14px;">
  <div class="row-item">
    <div class="row-title">Glasses layer</div>
    <div class="row-desc">Camera · bone speaker · vibration · BLE · MCU</div>
  </div>
  <div class="row-item">
    <div class="row-title">Phone layer</div>
    <div class="row-desc">YOLOv8n · GPS route · scene AI (Ph.2) · offline maps</div>
  </div>
</div>""", unsafe_allow_html=True)
