import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
import os

# ─── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="Prediksi Harga Mobil",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #f0f4f8; }
    .stApp { font-family: 'Segoe UI', sans-serif; }

    .title-box {
        background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #1565c0 100%);
        color: white;
        padding: 30px 35px;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(26,35,126,0.3);
    }
    .title-box h1 { margin: 0; font-size: 2rem; font-weight: 700; }
    .title-box p  { margin: 8px 0 0 0; opacity: 0.85; font-size: 1rem; }

    .result-card {
        background: linear-gradient(135deg, #e65100 0%, #ff6f00 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 6px 25px rgba(230,81,0,0.35);
        margin: 15px 0;
    }
    .result-card .label { font-size: 0.95rem; opacity: 0.9; font-weight: 500; letter-spacing: 1px; text-transform: uppercase; }
    .result-card .price { font-size: 3rem; font-weight: 800; margin: 8px 0; }
    .result-card .sub   { font-size: 0.9rem; opacity: 0.85; }

    .spec-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        border-left: 5px solid #1565c0;
        margin: 8px 0;
    }
    .spec-row { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px dashed #e0e0e0; font-size: 0.92rem; }
    .spec-row:last-child { border-bottom: none; }
    .spec-label { color: #555; }
    .spec-value { font-weight: 600; color: #1a237e; }

    .metric-card {
        background: white;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
    }
    .metric-card .m-val { font-size: 1.8rem; font-weight: 700; color: #1565c0; }
    .metric-card .m-lbl { font-size: 0.8rem; color: #777; margin-top: 4px; }

    .credit-box {
        background: linear-gradient(135deg, #0d47a1 0%, #1565c0 100%);
        color: white;
        padding: 18px 22px;
        border-radius: 12px;
        margin-top: 20px;
        font-size: 0.88rem;
    }
    .credit-box b { font-size: 1rem; }

    .stButton > button {
        background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 14px 0;
        font-size: 1.05rem;
        font-weight: 600;
        width: 100%;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(21,101,192,0.35);
        transition: all 0.2s;
    }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(21,101,192,0.45); }

    .sidebar-title {
        background: linear-gradient(135deg, #1a237e, #1565c0);
        color: white;
        padding: 12px 16px;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 15px;
        text-align: center;
    }
    div[data-testid="stSlider"] > div { padding-top: 4px; }
</style>
""", unsafe_allow_html=True)


# ─── LOAD MODEL ───────────────────────────────────────────────
@st.cache_resource
def load_model():
    model_path    = "model_prediksi_harga_mobil.pkl"
    metadata_path = "model_metadata.json"

    if not os.path.exists(model_path):
        st.error("❌ File `model_prediksi_harga_mobil.pkl` tidak ditemukan! "
                 "Jalankan notebook Colab terlebih dahulu dan download model-nya.")
        st.stop()

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    with open(metadata_path, "r") as f:
        meta = json.load(f)

    return model, meta


model, meta = load_model()
FEATURES = meta["features"]
STATS    = meta["feature_stats"]
R2       = meta["r2"]
RMSE     = meta["rmse"]

# ─── HEADER ───────────────────────────────────────────────────
st.markdown("""
<div class="title-box">
    <h1>🚗 Sistem Prediksi Harga Mobil</h1>
    <p>Masukkan spesifikasi teknis kendaraan untuk mendapatkan estimasi harga pasar secara otomatis</p>
</div>
""", unsafe_allow_html=True)

# ─── LAYOUT ───────────────────────────────────────────────────
left_col, right_col = st.columns([1, 1], gap="large")

# ── SIDEBAR INFO ──
with st.sidebar:
    st.markdown('<div class="sidebar-title">📊 Info Model</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-val">{R2*100:.1f}%</div>
            <div class="m-lbl">R² Score</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="m-val">±${RMSE*1000:,.0f}</div>
            <div class="m-lbl">Rata-rata Error</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📖 Panduan Penggunaan")
    st.info("""
1. Atur nilai setiap spesifikasi mobil menggunakan slider di panel kiri.
2. Klik tombol **"Hitung Harga Mobil"**.
3. Estimasi harga akan tampil di panel kanan.
    """)

    st.markdown("---")
    st.markdown("#### 📌 Tentang Dataset")
    st.write("Dataset: **Car Sales** | 157 data kendaraan dari berbagai merek.")

    st.markdown("""
    <div class="credit-box">
        <b>Sistem ini dibuat oleh:</b><br>
        👤 Alariq Aria Mustafa<br>
        🎓 NIM: 237006166<br>
        🏫 Teknik Informatika<br>
        🏛️ Universitas Siliwangi
    </div>
    """, unsafe_allow_html=True)


# ── INPUT PANEL ──
with left_col:
    st.markdown("### 🔧 Spesifikasi Kendaraan")
    st.markdown("Sesuaikan nilai berikut sesuai mobil yang ingin diproduksi:")

    label_map = {
        "__year_resale_value": ("💲 Nilai Jual Kembali (4 thn)", "ribu USD"),
        "Engine_size":         ("⚙️ Kapasitas Mesin",            "Liter"),
        "Horsepower":          ("🔥 Tenaga Mesin",               "HP"),
        "Curb_weight":         ("⚖️ Berat Kendaraan",            "ribu lbs"),
        "Wheelbase":           ("📏 Jarak Sumbu Roda",           "inch"),
        "Fuel_capacity":       ("⛽ Kapasitas Tangki",           "galon"),
        "Power_perf_factor":   ("⚡ Faktor Performa Daya",       ""),
    }

    inputs = {}
    for feat in FEATURES:
        label, unit = label_map[feat]
        s = STATS[feat]
        step = 0.1 if s["max"] < 20 else (1.0 if s["max"] < 200 else 5.0)
        full_label = f"{label} ({unit})" if unit else label
        inputs[feat] = st.slider(
            full_label,
            min_value=float(s["min"]),
            max_value=float(s["max"]),
            value=float(s["median"]),
            step=step,
            help=f"Rentang data: {s['min']} – {s['max']} | Median: {s['median']}"
        )

    st.markdown("<br>", unsafe_allow_html=True)
    hitung = st.button("🚗 Hitung Harga Mobil", use_container_width=True)


# ── RESULT PANEL ──
with right_col:
    st.markdown("### 💰 Perkiraan Harga Mobil")

    if hitung:
        input_df = pd.DataFrame([inputs])
        predicted_price = model.predict(input_df)[0]
        price_usd = predicted_price * 1_000

        # Price card
        st.markdown(f"""
        <div class="result-card">
            <div class="label">Estimasi Harga Pasar</div>
            <div class="price">${price_usd:,.0f}</div>
            <div class="sub">≈ Rp {price_usd * 16_000:,.0f} <small>(kurs ~Rp 16.000)</small></div>
        </div>
        """, unsafe_allow_html=True)

        # Spec summary
        st.markdown("**📋 Spesifikasi yang Diinput:**")
        rows_html = ""
        for feat, val in inputs.items():
            label, unit = label_map[feat]
            label_clean = label.split(" ", 1)[1]
            rows_html += f'<div class="spec-row"><span class="spec-label">{label_clean}</span><span class="spec-value">{val:.1f} {unit}</span></div>'

        st.markdown(f'<div class="spec-card">{rows_html}</div>', unsafe_allow_html=True)

        # Confidence note
        lower = price_usd - (RMSE * 1_000)
        upper = price_usd + (RMSE * 1_000)
        st.success(f"📊 Rentang estimasi: **${lower:,.0f}** – **${upper:,.0f}**  \n"
                   f"Akurasi model: **{R2*100:.1f}%** (R² Score)")

        # Credit
        st.markdown("""
        <div class="credit-box">
            SISTEM INI DIBUAT OLEH:<br>
            <b>NAMA  : Alariq Aria Mustafa</b><br>
            <b>NIM   : 237006166</b>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="background:white; border-radius:15px; padding:40px; text-align:center;
                    box-shadow:0 2px 12px rgba(0,0,0,0.08); color:#888; margin-top:20px;">
            <div style="font-size:4rem;">🚗</div>
            <h3 style="color:#555;">Siap Menghitung Harga</h3>
            <p>Atur spesifikasi kendaraan di panel kiri,<br>lalu klik <b>Hitung Harga Mobil</b>.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="credit-box" style="margin-top:30px;">
            SISTEM INI DIBUAT OLEH:<br>
            <b>NAMA  : Alariq Aria Mustafa</b><br>
            <b>NIM   : 237006166</b>
        </div>
        """, unsafe_allow_html=True)
