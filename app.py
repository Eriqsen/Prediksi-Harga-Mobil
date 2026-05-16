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
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">

<style>
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background: #080810 !important;
    font-family: 'DM Sans', sans-serif;
    color: #e0e0f0;
}

#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none !important; }
[data-testid="stAppViewContainer"] { padding: 0; }

/* ─── HERO ─── */
.hero {
    position: relative;
    overflow: hidden;
    padding: 52px 64px 40px;
    background: #080810;
    border-bottom: 1px solid #141428;
}
.hero-glow-a {
    position: absolute; top: -100px; right: -40px;
    width: 480px; height: 480px;
    background: radial-gradient(circle, rgba(255,55,0,0.16) 0%, transparent 68%);
    pointer-events: none;
}
.hero-glow-b {
    position: absolute; bottom: -120px; left: 25%;
    width: 360px; height: 360px;
    background: radial-gradient(circle, rgba(255,150,0,0.08) 0%, transparent 68%);
    pointer-events: none;
}
.hero-tag {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(255,55,0,0.1);
    border: 1px solid rgba(255,55,0,0.35);
    color: #ff5522;
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem; letter-spacing: 3px; text-transform: uppercase;
    padding: 5px 14px; border-radius: 2px; margin-bottom: 20px;
}
.hero-dot { width: 6px; height: 6px; border-radius: 50%; background: #ff5522; animation: blink 1.4s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

.hero h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3.8rem, 7.5vw, 7rem);
    letter-spacing: 4px; line-height: 0.88;
    color: #ffffff; margin-bottom: 20px;
}
.hero h1 .accent { color: #ff4400; }
.hero p { font-size: 0.95rem; color: #60608a; max-width: 460px; line-height: 1.7; font-weight: 300; }

.hero-kpi { display: flex; gap: 48px; margin-top: 32px; }
.kpi-val { font-family: 'Bebas Neue', sans-serif; font-size: 2.2rem; color: #ff4400; letter-spacing: 2px; }
.kpi-lbl { font-family: 'Space Mono', monospace; font-size: 0.6rem; color: #40405a; letter-spacing: 2px; text-transform: uppercase; margin-top: 3px; }

/* ─── COLUMNS LAYOUT ─── */
.col-left {
    padding: 44px 52px;
    background: #0b0b18;
    border-right: 1px solid #141428;
    min-height: calc(100vh - 230px);
}
.col-right {
    padding: 44px 52px;
    background: #070710;
    min-height: calc(100vh - 230px);
    display: flex; flex-direction: column;
}

.section-tag {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem; letter-spacing: 4px; text-transform: uppercase;
    color: #ff4400; margin-bottom: 10px;
}
.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem; letter-spacing: 3px; color: #fff;
    line-height: 1; margin-bottom: 36px;
}

/* ─── SPEC CARDS ─── */
.spec-card {
    background: rgba(255,255,255,0.022);
    border: 1px solid rgba(255,255,255,0.055);
    border-left: 3px solid transparent;
    border-radius: 8px;
    padding: 18px 20px 10px;
    margin-bottom: 14px;
    transition: border-color 0.2s, background 0.2s;
}
.spec-card:hover {
    border-left-color: #ff4400;
    background: rgba(255,68,0,0.04);
}
.spec-top {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 12px;
}
.spec-name {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem; letter-spacing: 2px; text-transform: uppercase;
    color: #9090b8;
}
.spec-badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem; color: #30305a;
    background: rgba(255,255,255,0.03);
    padding: 2px 8px; border-radius: 2px;
}

/* Slider overrides */
div[data-testid="stSlider"] { padding: 0 !important; margin-bottom: 4px !important; }
div[data-testid="stSlider"] > label { display: none !important; }
div[data-testid="stSlider"] div[role="slider"] {
    background: #ff4400 !important;
    border: 2px solid #ff4400 !important;
    box-shadow: 0 0 12px rgba(255,68,0,0.5) !important;
}
div[data-testid="stSlider"] > div > div > div:nth-child(1) {
    background: rgba(255,68,0,0.2) !important;
}

/* ─── BUTTON ─── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #cc3300 0%, #ff5500 50%, #ff7700 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 18px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.3rem !important;
    letter-spacing: 5px !important;
    cursor: pointer !important;
    box-shadow: 0 6px 28px rgba(255,68,0,0.4) !important;
    transition: all 0.25s !important;
    margin-top: 16px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 36px rgba(255,68,0,0.55) !important;
}

/* ─── PRICE CARD ─── */
.price-card {
    background: linear-gradient(145deg, #180800, #250f00, #180800);
    border: 1px solid rgba(255,68,0,0.25);
    border-radius: 12px;
    padding: 36px 40px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}
.price-card::before {
    content:'';
    position: absolute; top: -80px; right: -80px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(255,80,0,0.18) 0%, transparent 70%);
}
.pc-tag { font-family: 'Space Mono', monospace; font-size: 0.6rem; letter-spacing: 4px; text-transform: uppercase; color: #ff4400; margin-bottom: 16px; }
.pc-price {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3rem, 5.5vw, 4.8rem);
    letter-spacing: 2px; color: #fff; line-height: 1;
}
.pc-idr { font-size: 0.85rem; color: #40405a; margin-top: 8px; font-weight: 300; }
.pc-range {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem; color: #40405a; margin-top: 14px;
}
.pc-range b { color: #ff6030; }

/* ─── ACCURACY BAR ─── */
.acc-wrap {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.055);
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 16px;
}
.acc-top { display: flex; justify-content: space-between; margin-bottom: 10px; }
.acc-lbl { font-family: 'Space Mono', monospace; font-size: 0.6rem; color: #30304a; letter-spacing: 2px; text-transform: uppercase; }
.acc-val { font-family: 'Bebas Neue', sans-serif; font-size: 1.2rem; color: #ff4400; letter-spacing: 1px; }
.acc-bg { height: 3px; background: rgba(255,255,255,0.05); border-radius: 2px; }
.acc-fill { height: 3px; border-radius: 2px; background: linear-gradient(90deg, #ff3300, #ffaa00); }

/* ─── SPEC RESULT GRID ─── */
.res-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 16px; }
.res-item {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 6px;
    padding: 12px 14px;
}
.res-lbl { font-family: 'Space Mono', monospace; font-size: 0.55rem; color: #30304a; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 5px; }
.res-val { font-size: 0.92rem; font-weight: 600; color: #c0c0e0; }
.res-val small { font-size: 0.68rem; color: #40405a; margin-left: 3px; font-weight: 400; }

/* ─── CREDIT ─── */
.credit {
    margin-top: auto;
    background: rgba(255,255,255,0.015);
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 8px;
    padding: 14px 20px;
    display: flex; justify-content: space-between; align-items: center;
}
.cr-left { font-family: 'Space Mono', monospace; font-size: 0.55rem; color: #20203a; letter-spacing: 2px; text-transform: uppercase; line-height: 1.8; }
.cr-name { font-size: 0.88rem; color: #40406a; font-weight: 500; }
.cr-nim { font-family: 'Space Mono', monospace; font-size: 0.62rem; color: #25253a; margin-top: 2px; }

/* ─── IDLE ─── */
.idle {
    flex: 1; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center; padding: 40px 0;
}
.idle-ring {
    width: 100px; height: 100px; border-radius: 50%;
    border: 2px solid #141428;
    display: flex; align-items: center; justify-content: center;
    font-size: 2.5rem; margin-bottom: 24px;
    background: rgba(255,68,0,0.04);
    box-shadow: 0 0 40px rgba(255,68,0,0.08);
}
.idle-title { font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; letter-spacing: 4px; color: #20203a; margin-bottom: 8px; }
.idle-sub { font-size: 0.78rem; color: #18182a; line-height: 1.7; }
</style>
""", unsafe_allow_html=True)


# ── LOAD MODEL
@st.cache_resource
def load_model():
    if not os.path.exists("model_prediksi_harga_mobil.pkl"):
        st.error("❌ model_prediksi_harga_mobil.pkl tidak ditemukan. Jalankan notebook Colab dulu!")
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

# ── HERO
st.markdown(f"""
<div class="hero">
    <div class="hero-glow-a"></div>
    <div class="hero-glow-b"></div>
    <div class="hero-tag"><span class="hero-dot"></span> LIVE · AI-Powered Prediction Engine</div>
    <h1>AUTO<span class="accent">PRICE</span><br>INTELLIGENCE</h1>
    <p>Sistem prediksi harga kendaraan berbasis Machine Learning dengan metode CRISP-DM. Input spesifikasi, dapatkan estimasi harga instan.</p>
    <div class="hero-kpi">
        <div><div class="kpi-val">{R2*100:.1f}%</div><div class="kpi-lbl">Akurasi R²</div></div>
        <div><div class="kpi-val">157</div><div class="kpi-lbl">Data Record</div></div>
        <div><div class="kpi-val">7</div><div class="kpi-lbl">Fitur Input</div></div>
        <div><div class="kpi-val">±${RMSE*1000:,.0f}</div><div class="kpi-lbl">Margin Error</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── COLUMNS
col_l, col_r = st.columns([1, 1], gap="small")

CONF = {
    "__year_resale_value": ("NILAI JUAL KEMBALI",  "Ribu USD"),
    "Engine_size":         ("KAPASITAS MESIN",      "Liter"),
    "Horsepower":          ("TENAGA MESIN",          "HP"),
    "Curb_weight":         ("BERAT KENDARAAN",       "Ribu Lbs"),
    "Wheelbase":           ("JARAK SUMBU RODA",      "Inch"),
    "Fuel_capacity":       ("KAPASITAS TANGKI",      "Galon"),
    "Power_perf_factor":   ("FAKTOR PERFORMA DAYA",  "—"),
}
ICONS = ["💲","⚙️","🔥","⚖️","📐","⛽","⚡"]

with col_l:
    st.markdown("""
    <div class="col-left">
        <div class="section-tag">// Konfigurasi Kendaraan</div>
        <div class="section-title">SPESIFIKASI<br>TEKNIS</div>
    </div>""", unsafe_allow_html=True)

    inputs = {}
    for i, feat in enumerate(FEATURES):
        name, unit = CONF[feat]
        icon = ICONS[i]
        s = STATS[feat]
        step = 0.1 if s["max"] < 20 else (1.0 if s["max"] < 200 else 5.0)
        st.markdown(f"""
        <div class="spec-card">
            <div class="spec-top">
                <span class="spec-name">{icon} &nbsp;{name}</span>
                <span class="spec-badge">{unit}</span>
            </div>
        </div>""", unsafe_allow_html=True)
        inputs[feat] = st.slider(
            feat, float(s["min"]), float(s["max"]),
            float(s["median"]), step, label_visibility="collapsed"
        )

    hitung = st.button("⚡  KALKULASI HARGA SEKARANG")

with col_r:
    if hitung:
        pred      = model.predict(pd.DataFrame([inputs]))[0]
        price_usd = pred * 1000
        price_idr = price_usd * 16000
        lower     = (pred - RMSE) * 1000
        upper     = (pred + RMSE) * 1000
        fill      = int(R2 * 100)

        res_items = ""
        for i, feat in enumerate(FEATURES):
            name, unit = CONF[feat]
            val = inputs[feat]
            res_items += f"""
            <div class="res-item">
                <div class="res-lbl">{name}</div>
                <div class="res-val">{val:.1f}<small>{unit}</small></div>
            </div>"""

        st.markdown(f"""
        <div class="col-right">
            <div class="section-tag">// Output Kalkulasi</div>
            <div class="section-title">ESTIMASI<br>HARGA PASAR</div>

            <div class="price-card">
                <div class="pc-tag">// Harga Prediksi</div>
                <div class="pc-price">${price_usd:,.0f}</div>
                <div class="pc-idr">≈ Rp {price_idr:,.0f} <span style="font-size:0.75rem">(kurs Rp 16.000)</span></div>
                <div class="pc-range">Rentang estimasi &nbsp;·&nbsp; <b>${lower:,.0f}</b> &nbsp;—&nbsp; <b>${upper:,.0f}</b></div>
            </div>

            <div class="acc-wrap">
                <div class="acc-top">
                    <span class="acc-lbl">Akurasi Model (R² Score)</span>
                    <span class="acc-val">{fill}%</span>
                </div>
                <div class="acc-bg"><div class="acc-fill" style="width:{fill}%"></div></div>
            </div>

            <div class="res-grid">{res_items}</div>

            <div class="credit">
                <div class="cr-left">SISTEM INI<br>DIBUAT OLEH</div>
                <div>
                    <div class="cr-name">Alariq Aria Mustafa</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="col-right">
            <div class="idle">
                <div class="idle-ring">🏎️</div>
                <div class="idle-title">SIAP KALKULASI</div>
                <div class="idle-sub">Atur spesifikasi kendaraan di panel kiri<br>lalu tekan tombol kalkulasi</div>
            </div>
            <div class="credit">
                <div class="cr-left">SISTEM INI<br>DIBUAT OLEH</div>
                <div>
                    <div class="cr-name">Alariq Aria Mustafa</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
