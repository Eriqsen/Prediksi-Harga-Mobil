import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
import os

st.set_page_config(
    page_title="AutoPrice AI",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>

/* ══ RESET & BASE ══ */
html, body, .stApp { background: #0e0e16 !important; font-family: 'Outfit', sans-serif; }
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1400px !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ══ HERO BANNER ══ */
.hero-wrap {
    background: linear-gradient(120deg, #12122a 0%, #1a0a00 50%, #0e0e16 100%);
    border: 1px solid #2a2a45;
    border-radius: 16px;
    padding: 44px 52px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content:''; position:absolute; top:-80px; right:-60px;
    width:350px; height:350px;
    background: radial-gradient(circle, rgba(255,80,0,0.22) 0%, transparent 65%);
}
.hero-wrap::after {
    content:''; position:absolute; bottom:-60px; left:35%;
    width:280px; height:280px;
    background: radial-gradient(circle, rgba(255,160,0,0.10) 0%, transparent 65%);
}
.hero-badge {
    display:inline-flex; align-items:center; gap:8px;
    background: rgba(255,80,0,0.15); border: 1px solid rgba(255,80,0,0.4);
    color:#ff6633; font-family:'Space Mono',monospace;
    font-size:0.62rem; letter-spacing:3px; text-transform:uppercase;
    padding:5px 14px; border-radius:3px; margin-bottom:16px;
}
.live-dot { width:7px; height:7px; border-radius:50%; background:#ff5500; animation: pulse 1.3s infinite; }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.3;transform:scale(0.8)} }

.hero-title {
    font-family:'Bebas Neue',sans-serif;
    font-size: clamp(3.2rem,6vw,5.8rem);
    letter-spacing:4px; line-height:0.9; color:#fff; margin-bottom:14px;
}
.hero-title .fire { color:#ff4400; }
.hero-desc { font-size:0.95rem; color:#7878a8; max-width:500px; line-height:1.7; font-weight:300; margin-bottom:28px; }
.kpi-row { display:flex; gap:48px; flex-wrap:wrap; }
.kpi-item .val { font-family:'Bebas Neue',sans-serif; font-size:2rem; color:#ff5500; letter-spacing:2px; }
.kpi-item .lbl { font-family:'Space Mono',monospace; font-size:0.58rem; color:#44446a; letter-spacing:2px; text-transform:uppercase; margin-top:2px; }

/* ══ PANEL HEADERS ══ */
.panel-head {
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid #1e1e38;
}
.panel-tag { font-family:'Space Mono',monospace; font-size:0.6rem; letter-spacing:4px; text-transform:uppercase; color:#ff4400; margin-bottom:8px; }
.panel-title { font-family:'Bebas Neue',sans-serif; font-size:1.8rem; letter-spacing:3px; color:#ffffff; line-height:1; }

/* ══ SPEC SLIDERS ══ */
.spec-wrap {
    background: #161625;
    border: 1px solid #252540;
    border-left: 3px solid #1e1e38;
    border-radius: 10px;
    padding: 16px 20px 4px;
    margin-bottom: 12px;
    transition: border-left-color 0.2s;
}
.spec-wrap:hover { border-left-color: #ff4400; }
.spec-label-row {
    display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;
}
.spec-name-txt {
    font-family:'Space Mono',monospace; font-size:0.62rem;
    letter-spacing:2px; text-transform:uppercase; color:#a0a0cc;
}
.spec-unit-txt {
    font-family:'Space Mono',monospace; font-size:0.58rem;
    color:#44446a; background:#0e0e1e; padding:2px 8px; border-radius:3px;
}

/* Streamlit slider styling */
div[data-testid="stSlider"] { padding:0 !important; }
div[data-testid="stSlider"] label { display:none !important; }
div[data-testid="stSlider"] [role="slider"] {
    background:#ff4400 !important;
    border:2px solid #ff6633 !important;
    box-shadow: 0 0 14px rgba(255,68,0,0.6) !important;
}

/* ══ BUTTON ══ */
.stButton > button {
    width:100% !important;
    background: linear-gradient(135deg, #c43000 0%, #ff5500 55%, #ff8800 100%) !important;
    color:#fff !important; border:none !important;
    border-radius:10px !important; padding:17px !important;
    font-family:'Bebas Neue',sans-serif !important;
    font-size:1.25rem !important; letter-spacing:5px !important;
    box-shadow: 0 8px 32px rgba(255,68,0,0.45) !important;
    transition: all 0.25s !important; margin-top:12px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 14px 40px rgba(255,68,0,0.6) !important;
}

/* ══ RESULT PRICE CARD ══ */
.price-big-card {
    background: linear-gradient(145deg, #200e00, #2d1200, #1e0c00);
    border: 1px solid rgba(255,80,0,0.3);
    border-radius: 14px;
    padding: 34px 38px;
    margin-bottom: 16px;
    position:relative; overflow:hidden;
}
.price-big-card::before {
    content:''; position:absolute; top:-70px; right:-70px;
    width:200px; height:200px;
    background:radial-gradient(circle,rgba(255,90,0,0.2) 0%,transparent 70%);
}
.pbc-label { font-family:'Space Mono',monospace; font-size:0.6rem; letter-spacing:4px; text-transform:uppercase; color:#ff5500; margin-bottom:14px; }
.pbc-usd { font-family:'Bebas Neue',sans-serif; font-size:clamp(2.8rem,5vw,4.5rem); letter-spacing:2px; color:#ffffff; line-height:1; }
.pbc-idr { font-size:0.85rem; color:#5a5a80; margin-top:8px; font-weight:300; }
.pbc-range { font-family:'Space Mono',monospace; font-size:0.63rem; color:#44446a; margin-top:14px; }
.pbc-range b { color:#ff6030; font-weight:700; }

/* ══ ACCURACY BAR ══ */
.acc-card {
    background:#161625; border:1px solid #252540;
    border-radius:10px; padding:16px 20px; margin-bottom:14px;
}
.acc-row { display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
.acc-label-txt { font-family:'Space Mono',monospace; font-size:0.6rem; color:#44446a; letter-spacing:2px; text-transform:uppercase; }
.acc-pct { font-family:'Bebas Neue',sans-serif; font-size:1.3rem; color:#ff5500; letter-spacing:1px; }
.acc-track { height:4px; background:rgba(255,255,255,0.06); border-radius:2px; overflow:hidden; }
.acc-bar { height:4px; border-radius:2px; background:linear-gradient(90deg,#ff3300,#ffaa00); transition:width 0.6s ease; }

/* ══ SPEC RESULT GRID ══ */
.res-cards {
    display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:16px;
}
.res-card {
    background:#161625; border:1px solid #252540;
    border-radius:8px; padding:14px 16px;
}
.res-card-lbl { font-family:'Space Mono',monospace; font-size:0.55rem; color:#35355a; letter-spacing:2px; text-transform:uppercase; margin-bottom:6px; }
.res-card-val { font-size:1rem; font-weight:600; color:#d0d0f8; }
.res-card-val small { font-size:0.68rem; color:#44446a; margin-left:4px; font-weight:400; }

/* ══ CREDIT CARD ══ */
.credit-card {
    background:#111120; border:1px solid #1e1e35;
    border-radius:10px; padding:16px 22px;
    display:flex; justify-content:space-between; align-items:center;
    margin-top:8px;
}
.credit-label { font-family:'Space Mono',monospace; font-size:0.56rem; color:#28283a; letter-spacing:2px; text-transform:uppercase; line-height:1.9; }
.credit-name { font-size:0.9rem; color:#6060a0; font-weight:600; text-align:right; }
.credit-nim { font-family:'Space Mono',monospace; font-size:0.62rem; color:#28283a; text-align:right; margin-top:2px; }

/* ══ IDLE STATE ══ */
.idle-container {
    display:flex; flex-direction:column; align-items:center;
    justify-content:center; padding:60px 0; text-align:center;
}
.idle-ring {
    width:110px; height:110px; border-radius:50%;
    border:2px solid #1e1e38;
    background:rgba(255,68,0,0.05);
    box-shadow:0 0 50px rgba(255,68,0,0.07);
    display:flex; align-items:center; justify-content:center;
    font-size:2.8rem; margin-bottom:22px;
}
.idle-title { font-family:'Bebas Neue',sans-serif; font-size:1.6rem; letter-spacing:4px; color:#25253a; margin-bottom:10px; }
.idle-sub { font-size:0.8rem; color:#1c1c2e; line-height:1.8; }

/* ══ METRIC OVERRIDES ══ */
[data-testid="stMetric"] {
    background:#161625 !important; border:1px solid #252540 !important;
    border-radius:10px !important; padding:16px 20px !important;
}
[data-testid="stMetricLabel"] { color:#44446a !important; font-family:'Space Mono',monospace !important; font-size:0.6rem !important; }
[data-testid="stMetricValue"] { color:#ffffff !important; font-family:'Bebas Neue',sans-serif !important; font-size:1.8rem !important; letter-spacing:2px !important; }

/* Divider */
hr { border-color:#1e1e38 !important; margin: 8px 0 20px !important; }
</style>
""", unsafe_allow_html=True)


# ── LOAD MODEL ────────────────────────────────────────────────
@st.cache_resource
def load_model():
    if not os.path.exists("model_prediksi_harga_mobil.pkl"):
        st.error("❌ **model_prediksi_harga_mobil.pkl** tidak ditemukan!\n\nJalankan notebook Colab terlebih dahulu lalu download file model-nya.")
        st.stop()
    with open("model_prediksi_harga_mobil.pkl", "rb") as f:
        model = pickle.load(f)
    with open("model_metadata.json", "r") as f:
        meta = json.load(f)
    return model, meta

model, meta = load_model()
FEATURES = meta["features"]
STATS    = meta["feature_stats"]
R2       = meta["r2"]
RMSE     = meta["rmse"]

# ── HERO ─────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-badge"><span class="live-dot"></span>LIVE · AI-Powered · CRISP-DM</div>
    <div class="hero-title">AUTO<span class="fire">PRICE</span><br>INTELLIGENCE</div>
    <div class="hero-desc">Sistem prediksi harga kendaraan berbasis Machine Learning. Input spesifikasi teknis, dapatkan estimasi harga pasar secara instan dan akurat.</div>
    <div class="kpi-row">
        <div class="kpi-item"><div class="val">{R2*100:.1f}%</div><div class="lbl">Akurasi R²</div></div>
        <div class="kpi-item"><div class="val">157</div><div class="lbl">Data Record</div></div>
        <div class="kpi-item"><div class="val">7</div><div class="lbl">Fitur Input</div></div>
        <div class="kpi-item"><div class="val">±${RMSE*1000:,.0f}</div><div class="lbl">Margin Error</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── MAIN LAYOUT ───────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

CONF = {
    "__year_resale_value": ("💲 NILAI JUAL KEMBALI",  "Ribu USD"),
    "Engine_size":         ("⚙️ KAPASITAS MESIN",      "Liter"),
    "Horsepower":          ("🔥 TENAGA MESIN",          "HP"),
    "Curb_weight":         ("⚖️ BERAT KENDARAAN",       "Ribu Lbs"),
    "Wheelbase":           ("📐 JARAK SUMBU RODA",      "Inch"),
    "Fuel_capacity":       ("⛽ KAPASITAS TANGKI",      "Galon"),
    "Power_perf_factor":   ("⚡ FAKTOR PERFORMA",       "—"),
}

# ── LEFT: INPUT ───────────────────────────────────────────────
with left:
    st.markdown("""
    <div class="panel-head">
        <div class="panel-tag">// Konfigurasi Kendaraan</div>
        <div class="panel-title">SPESIFIKASI TEKNIS</div>
    </div>""", unsafe_allow_html=True)

    inputs = {}
    for feat in FEATURES:
        name, unit = CONF[feat]
        s = STATS[feat]
        step = 0.1 if s["max"] < 20 else (1.0 if s["max"] < 200 else 5.0)

        st.markdown(f"""
        <div class="spec-wrap">
            <div class="spec-label-row">
                <span class="spec-name-txt">{name}</span>
                <span class="spec-unit-txt">{unit}</span>
            </div>
        </div>""", unsafe_allow_html=True)

        inputs[feat] = st.slider(
            feat,
            min_value=float(s["min"]),
            max_value=float(s["max"]),
            value=float(s["median"]),
            step=step,
            label_visibility="collapsed"
        )

    st.markdown("<br>", unsafe_allow_html=True)
    hitung = st.button("⚡  KALKULASI HARGA SEKARANG")

# ── RIGHT: OUTPUT ─────────────────────────────────────────────
with right:
    st.markdown("""
    <div class="panel-head">
        <div class="panel-tag">// Output Kalkulasi</div>
        <div class="panel-title">ESTIMASI HARGA PASAR</div>
    </div>""", unsafe_allow_html=True)

    if hitung:
        pred      = model.predict(pd.DataFrame([inputs]))[0]
        price_usd = pred * 1000
        price_idr = price_usd * 16000
        lower     = max(0, (pred - RMSE) * 1000)
        upper     = (pred + RMSE) * 1000
        fill_pct  = int(R2 * 100)

        # Price card via markdown (safe, above column content)
        st.markdown(f"""
        <div class="price-big-card">
            <div class="pbc-label">// Perkiraan Harga Jual</div>
            <div class="pbc-usd">${price_usd:,.0f}</div>
            <div class="pbc-idr">≈ Rp {price_idr:,.0f} &nbsp;<span style="font-size:0.75rem">(kurs Rp 16.000)</span></div>
            <div class="pbc-range">Rentang estimasi &nbsp;·&nbsp; <b>${lower:,.0f}</b> — <b>${upper:,.0f}</b></div>
        </div>
        """, unsafe_allow_html=True)

        # Accuracy bar
        st.markdown(f"""
        <div class="acc-card">
            <div class="acc-row">
                <span class="acc-label-txt">Akurasi Model (R² Score)</span>
                <span class="acc-pct">{fill_pct}%</span>
            </div>
            <div class="acc-track">
                <div class="acc-bar" style="width:{fill_pct}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Spec grid — use native st.columns to avoid HTML rendering issues
        st.markdown("**📋 Spesifikasi yang Diinput:**")
        cols_a = st.columns(2)
        cols_b = st.columns(2)
        all_cols = list(cols_a) + list(cols_b)

        feat_pairs = [(f, CONF[f][0].split(" ", 1)[1], CONF[f][1], inputs[f]) for f in FEATURES]
        # Fill 4 per row, 2 rows → 7 items across 4+3
        col_idx = 0
        for i, (feat, name, unit, val) in enumerate(feat_pairs):
            row = i // 2
            col = i % 2
            target_cols = cols_a if row == 0 else cols_b if row == 1 else None

            # Fallback: just use 4 columns cycling
            c_idx = i % 4
            if i < 4:
                with cols_a[i % 2] if i < 2 else cols_b[i % 2 - (0 if i%2 else 0)]:
                    pass

        # Simpler: just iterate with columns(2)
        feat_list = [(f, CONF[f][0].split(" ",1)[1], CONF[f][1], inputs[f]) for f in FEATURES]
        for i in range(0, len(feat_list), 2):
            c1, c2 = st.columns(2)
            f1_name, f1_unit, f1_val = feat_list[i][1], feat_list[i][2], feat_list[i][3]
            with c1:
                st.markdown(f"""
                <div class="res-card">
                    <div class="res-card-lbl">{f1_name}</div>
                    <div class="res-card-val">{f1_val:.1f}<small>{f1_unit}</small></div>
                </div>""", unsafe_allow_html=True)
            if i + 1 < len(feat_list):
                f2_name, f2_unit, f2_val = feat_list[i+1][1], feat_list[i+1][2], feat_list[i+1][3]
                with c2:
                    st.markdown(f"""
                    <div class="res-card">
                        <div class="res-card-lbl">{f2_name}</div>
                        <div class="res-card-val">{f2_val:.1f}<small>{f2_unit}</small></div>
                    </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class="credit-card">
            <div class="credit-label">SISTEM INI<br>DIBUAT OLEH</div>
            <div>
                <div class="credit-name">Alariq Aria Mustafa</div>
                <div class="credit-nim">NIM · 237006166</div>
            </div>
        </div>""", unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="idle-container">
            <div class="idle-ring">🏎️</div>
            <div class="idle-title">SIAP KALKULASI</div>
            <div class="idle-sub">Atur spesifikasi kendaraan<br>di panel kiri, lalu tekan<br>tombol kalkulasi</div>
        </div>
        <div class="credit-card">
            <div class="credit-label">SISTEM INI<br>DIBUAT OLEH</div>
            <div>
                <div class="credit-name">Alariq Aria Mustafa</div>
                <div class="credit-nim">NIM · 237006166</div>
            </div>
        </div>""", unsafe_allow_html=True)
