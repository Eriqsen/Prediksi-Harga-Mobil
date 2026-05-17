import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
import os

st.set_page_config(
    page_title="AutoPrice AI 🏎️",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimal CSS - hanya styling dasar yang aman di Streamlit
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #0e0e16; }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; }
section[data-testid="stSidebar"] { display: none; }
div[data-testid="stMetric"] {
    background: #161625;
    border: 1px solid #252540;
    border-radius: 12px;
    padding: 16px 20px;
}
div[data-testid="stMetricLabel"] > div { color: #7070a0; font-size: 0.75rem; }
div[data-testid="stMetricValue"] > div { color: #ffffff; font-size: 1.6rem; font-weight: 700; }
.stButton > button {
    background: linear-gradient(135deg, #cc3300, #ff5500, #ff8800) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 16px !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    width: 100% !important;
    box-shadow: 0 6px 24px rgba(255,80,0,0.4) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 10px 32px rgba(255,80,0,0.55) !important;
}
div[data-testid="stSlider"] > div > div > div > div {
    background: #ff5500 !important;
}
</style>
""", unsafe_allow_html=True)


# ── LOAD MODEL ────────────────────────────────────────────────
@st.cache_resource
def load_model():
    if not os.path.exists("model_prediksi_harga_mobil.pkl"):
        st.error("❌ File **model_prediksi_harga_mobil.pkl** tidak ditemukan!\n\n"
                 "Jalankan notebook Google Colab terlebih dahulu dan download file model-nya.")
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

# ── HEADER ───────────────────────────────────────────────────
st.markdown("# 🏎️ AutoPrice Intelligence")
st.markdown("##### Sistem Prediksi Harga Mobil berbasis Machine Learning — CRISP-DM Framework")
st.divider()

# ── KPI ROW ──────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("🎯 Akurasi Model (R²)", f"{R2*100:.1f}%")
k2.metric("📦 Total Data Training", "157 record")
k3.metric("🔢 Jumlah Fitur Input", "7 fitur")
k4.metric("📏 Margin Error (RMSE)", f"±${RMSE*1000:,.0f}")

st.divider()

# ── MAIN LAYOUT ───────────────────────────────────────────────
left, right = st.columns([1, 1], gap="large")

CONF = {
    "__year_resale_value": ("💲 Nilai Jual Kembali (4 Thn)",  "Ribu USD"),
    "Engine_size":         ("⚙️ Kapasitas Mesin",             "Liter"),
    "Horsepower":          ("🔥 Tenaga Mesin",                 "HP"),
    "Curb_weight":         ("⚖️ Berat Kendaraan",              "Ribu Lbs"),
    "Wheelbase":           ("📐 Jarak Sumbu Roda",             "Inch"),
    "Fuel_capacity":       ("⛽ Kapasitas Tangki",             "Galon"),
    "Power_perf_factor":   ("⚡ Faktor Performa Daya",         "—"),
}

# ── LEFT: INPUT ───────────────────────────────────────────────
with left:
    st.markdown("### 🔧 Spesifikasi Kendaraan")
    st.caption("Atur nilai setiap spesifikasi menggunakan slider di bawah ini.")
    st.markdown("")

    inputs = {}
    for feat in FEATURES:
        label, unit = CONF[feat]
        s = STATS[feat]
        step = 0.1 if s["max"] < 20 else (1.0 if s["max"] < 200 else 5.0)

        col_lbl, col_val = st.columns([3, 1])
        with col_lbl:
            st.markdown(f"**{label}**")
        with col_val:
            st.markdown(f"<p style='color:#ff5500;text-align:right;margin:0;font-weight:700;font-size:0.85rem'>{unit}</p>",
                        unsafe_allow_html=True)

        inputs[feat] = st.slider(
            label=feat,
            min_value=float(s["min"]),
            max_value=float(s["max"]),
            value=float(s["median"]),
            step=step,
            label_visibility="collapsed",
            help=f"Min: {s['min']} | Max: {s['max']} | Median: {s['median']}"
        )
        st.markdown("---")

    st.markdown("")
    hitung = st.button("⚡  HITUNG HARGA MOBIL", use_container_width=True)

# ── RIGHT: OUTPUT ─────────────────────────────────────────────
with right:
    st.markdown("### 💰 Estimasi Harga Pasar")
    st.caption("Hasil prediksi berdasarkan spesifikasi yang diinput.")
    st.markdown("")

    if hitung:
        pred      = model.predict(pd.DataFrame([inputs]))[0]
        price_usd = pred * 1000
        price_idr = price_usd * 16_000
        lower     = max(0, (pred - RMSE) * 1000)
        upper     = (pred + RMSE) * 1000

        # ── PRICE DISPLAY ──
        st.success(f"### 💵 Estimasi Harga: **${price_usd:,.0f}**")
        st.markdown(f"""
> **≈ Rp {price_idr:,.0f}** *(kurs Rp 16.000)*
>
> 📊 Rentang estimasi: **${lower:,.0f}** — **${upper:,.0f}**
        """)

        # ── ACCURACY BAR ──
        st.markdown("**🎯 Akurasi Model:**")
        st.progress(R2, text=f"R² Score: {R2*100:.1f}%")
        st.markdown("")

        # ── SPEC SUMMARY ──
        st.markdown("**📋 Ringkasan Spesifikasi yang Diinput:**")
        c1, c2 = st.columns(2)

        feat_list = list(FEATURES)
        for i, feat in enumerate(feat_list):
            label, unit = CONF[feat]
            val = inputs[feat]
            clean_label = label.split(" ", 1)[1]
            target = c1 if i % 2 == 0 else c2
            target.metric(label=clean_label, value=f"{val:.1f} {unit}")

        st.markdown("")
        st.divider()

        # ── CREDIT ──
        st.markdown("""
        <div style='
            background:#161625;
            border:1px solid #252540;
            border-radius:10px;
            padding:14px 20px;
            display:flex;
            justify-content:space-between;
        '>
            <span style='color:#44446a;font-size:0.78rem'>SISTEM INI DIBUAT OLEH:</span>
            <span style='color:#8080c0;font-weight:600'>Alariq Aria Mustafa &nbsp;·&nbsp; <span style='color:#44446a'>NIM 237006166</span></span>
        </div>
        """, unsafe_allow_html=True)

    else:
        # ── IDLE STATE ──
        st.markdown("")
        st.markdown("")
        st.markdown("""
        <div style='
            text-align:center;
            padding:60px 20px;
            color:#44446a;
        '>
            <div style='font-size:4.5rem;margin-bottom:20px'>🏎️</div>
            <h3 style='color:#30305a;letter-spacing:2px'>SIAP KALKULASI</h3>
            <p style='color:#252538;font-size:0.9rem;margin-top:8px'>
                Atur spesifikasi kendaraan di panel kiri<br>
                lalu tekan tombol <b>HITUNG HARGA MOBIL</b>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.markdown("""
        <div style='
            background:#161625;
            border:1px solid #252540;
            border-radius:10px;
            padding:14px 20px;
        '>
            <span style='color:#44446a;font-size:0.78rem'>SISTEM INI DIBUAT OLEH: &nbsp;</span>
            <span style='color:#8080c0;font-weight:600'>Alariq Aria Mustafa &nbsp;·&nbsp; </span>
        </div>
        """, unsafe_allow_html=True)
