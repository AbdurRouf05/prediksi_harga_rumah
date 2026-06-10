"""
=============================================================================
 PREDIKSI HARGA RUMAH — Machine Learning Dashboard
=============================================================================
 Aplikasi web berbasis Streamlit yang MEMUAT model ML yang sudah dilatih
 dan menggunakannya untuk prediksi harga rumah di Jakarta, Surabaya,
 dan Lumajang.

 PENTING: Ini BUKAN kalkulator sederhana!
 Model sudah BELAJAR dari ratusan/ribuan data rumah asli dan menyimpan
 BOBOT-nya di file .pkl (scikit-learn) dan .h5 (Keras/TensorFlow).

 Cara Menjalankan:
   streamlit run app.py
=============================================================================
"""

import streamlit as st
import os
import sys

# Setup path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from frontend.styles import inject_css
from frontend.page_predict import render_predict
from frontend.page_explore import render_explore
from frontend.page_model_info import render_model_info
from engine.model_loader import load_all_models, check_models_exist

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================
st.set_page_config(
    page_title="Prediksi Harga Rumah — ML Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_css()

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
        <div style='text-align:center; padding: 1rem 0;'>
            <div style='font-size: 2.5rem;'>🏠</div>
            <div style='font-size: 1.2rem; font-weight: 700; 
                        background: linear-gradient(135deg, #3b82f6, #10b981);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                Prediksi Harga Rumah
            </div>
            <div style='font-size: 0.75rem; color: #64748b; margin-top: 4px;'>
                Machine Learning Dashboard
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # PILIH KOTA (3 pilihan: Jakarta, Surabaya, Lumajang)
    st.markdown("**📍 PILIH LOKASI PREDIKSI:**")
    pilihan_kota = st.radio(
        "Kota",
        ["🏙️ Jakarta", "🦈 Surabaya", "🌋 Lumajang"],
        label_visibility="collapsed"
    )
    
    # Mapping pilihan kota ke folder dan nama tampilan
    if 'Jakarta' in pilihan_kota:
        kota_aktif, nama_kota = 'jakarta', 'Jakarta'
    elif 'Surabaya' in pilihan_kota:
        kota_aktif, nama_kota = 'surabaya', 'Surabaya'
    else:
        kota_aktif, nama_kota = 'lumajang', 'Lumajang'
    
    st.write("---")

# ============================================================
# LOAD MODEL (DINAMIS SESUAI KOTA)
# ============================================================
# Kita simpan state kota agar jika berubah, model diload ulang
if 'current_kota' not in st.session_state or st.session_state['current_kota'] != kota_aktif:
    st.session_state['current_kota'] = kota_aktif
    
    models_dir = os.path.join(BASE_DIR, 'models', kota_aktif)
    
    if check_models_exist(kota_aktif, models_dir):
        with st.spinner(f"Memuat model Machine Learning untuk {nama_kota}..."):
            st.session_state['models'] = load_all_models(kota_aktif, models_dir)
            st.session_state['models_loaded'] = True
    else:
        st.session_state['models'] = {
            'model_lr': None, 'model_rf': None, 'model_nn': None,
            'scaler': None, 'metadata': {}
        }
        st.session_state['models_loaded'] = False

models = st.session_state['models']

with st.sidebar:
    if st.session_state.get('models_loaded', False):
        st.success(f"✅ Model {nama_kota} aktif")
        meta = models.get('metadata', {})
        if meta:
            st.caption(f"Model terbaik: **{meta.get('best_model', '?')}**")
            st.caption(f"Akurasi R²: **{meta.get('best_r2', 0):.1%}**")
    else:
        st.error(f"❌ Model {nama_kota} belum ada")
        st.caption(f"Jalankan training untuk {nama_kota} dulu!")
    
    st.write("---")
    
    menu = st.radio(
        "📑 Navigasi",
        ["🔮 Prediksi Harga", "📊 Eksplorasi Data", "🧠 Info Model & Bobot"],
        index=0,
        label_visibility="collapsed"
    )

# ============================================================
# RENDER HALAMAN
# ============================================================
if "Prediksi Harga" in menu:
    render_predict(models, nama_kota)
elif "Eksplorasi Data" in menu:
    render_explore(models, kota_aktif, nama_kota)
elif "Info Model" in menu:
    render_model_info(models, nama_kota)
