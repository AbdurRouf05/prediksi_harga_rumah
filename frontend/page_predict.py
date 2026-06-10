"""
Page: Prediksi Harga Rumah
==========================
Halaman utama dimana user menginput fitur rumah dan mendapatkan
prediksi harga dari model ML yang sudah dilatih.
Mendukung input dinamis berdasarkan skema fitur masing-masing kota.
"""

import streamlit as st
import pandas as pd
from engine.data_preprocessing import get_schema, get_feature_names, format_rupiah
from engine.predictor import predict_price

def render_predict(models: dict, nama_kota: str):
    """Render halaman prediksi harga rumah"""
    
    st.markdown(f"<div class='title-gradient'>Prediksi Harga Rumah {nama_kota}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>Masukkan spesifikasi rumah di bawah ini. Model Machine Learning yang sudah belajar dari ribuan data rumah asli {nama_kota} akan memprediksi harganya.</div>", unsafe_allow_html=True)
    
    if models.get('scaler') is None:
        st.error("❌ **Model belum dimuat!** Pastikan Anda sudah menjalankan training dan menaruh file `.pkl` di folder `models/`.")
        st.info("📖 Lihat halaman **Info Model** untuk panduan lengkap.")
        return
    
    st.markdown("### 🏠 Spesifikasi Rumah")
    
    schema = get_schema(models)
    
    # Generate form secara dinamis
    input_data = {}
    
    # Kita bagi fitur ke dalam baris dengan 3 kolom
    cols = st.columns(3)
    
    for i, feature in enumerate(schema):
        name = feature['name']
        ftype = feature['type']
        
        with cols[i % 3]:
            label = feature.get('label', name)
            if ftype == 'numeric':
                min_val = float(feature.get('min', 0))
                max_val = float(feature.get('max', 10000))
                default_val = float(feature.get('default', min_val))
                
                # Jika fitur adalah luasan (LT, LB), gunakan step 10, sisanya step 1
                if name in ['LT', 'LB']:
                    val = st.number_input(f"{label}", min_value=int(min_val), max_value=int(max_val)*2, value=int(default_val), step=10)
                else:
                    val = st.number_input(f"{label}", min_value=int(min_val), max_value=int(max_val), value=int(default_val), step=1)
                input_data[name] = val
                
            elif ftype == 'categorical':
                options = feature.get('options', [])
                val = st.selectbox(f"{label}", options)
                input_data[name] = val
    
    # Pilih model
    st.write("---")
    model_options = {'🤖 Otomatis (Model Terbaik)': 'auto'}
    if models.get('model_lr'):
        model_options['📊 Linear Regression'] = 'lr'
    if models.get('model_rf'):
        model_options['🌲 Random Forest'] = 'rf'
    if models.get('model_nn'):
        model_options['🧠 Neural Network'] = 'nn'
    
    selected_model = st.selectbox("🔧 Pilih Model ML", list(model_options.keys()), index=0)
    model_key = model_options[selected_model]
    
    st.write("---")
    
    # Tombol prediksi
    predict_button = st.button("🔮 Prediksi Harga Rumah", use_container_width=True, type="primary")
    
    if predict_button:
        with st.spinner("Model sedang memprediksi..."):
            result = predict_price(input_data, models, model_key)
        
        if 'error' in result:
            st.error(result['error'])
            return
        
        harga = result['harga_prediksi']
        model_used = result['model_digunakan']
        semua = result['semua_prediksi']
        
        # Tampilkan hasil
        st.markdown(f"""
            <div class='prediction-card'>
                <div class='prediction-label'>Estimasi Harga Rumah (Model: {model_used})</div>
                <div class='prediction-price'>{format_rupiah(harga)}</div>
                <div class='prediction-label'>= Rp {harga:,.0f}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        
        # Perbandingan semua model
        if len(semua) > 1:
            st.markdown("### 📊 Perbandingan Prediksi Semua Model")
            cols2 = st.columns(len(semua))
            
            for i, (name, price) in enumerate(semua.items()):
                with cols2[i]:
                    is_winner = (name == model_used)
                    winner_class = "winner" if is_winner else ""
                    badge = "🏆 Model Terbaik" if is_winner else ""
                    
                    st.markdown(f"""
                        <div class='model-card {winner_class}'>
                            <div class='kpi-label'>{name}</div>
                            <div class='kpi-value' style='font-size:1.2rem;'>{format_rupiah(price)}</div>
                            <div class='kpi-badge' style='background-color:#10b98120; color:#10b981;'>{badge}</div>
                        </div>
                    """, unsafe_allow_html=True)
        
        # Penjelasan
        metadata = models.get('metadata', {})
        st.markdown(f"""
            <div class='info-box'>
                <b>💡 Bagaimana model ini bekerja?</b><br>
                Model <b>{model_used}</b> sudah <b>belajar pola</b> dari {metadata.get('train_size', '800+')} data rumah asli {nama_kota} saat proses training.
                Semua "pemahaman" ini tersimpan dalam <b>bobot (weights)</b> di file model <code>.pkl</code> / <code>.h5</code>.
            </div>
        """, unsafe_allow_html=True)
