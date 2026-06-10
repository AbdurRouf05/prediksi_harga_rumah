"""
Page: Info Model & Bobot
========================
Halaman yang menampilkan detail teknis model ML:
- Bobot (weights/coefficients) 
- Feature importance
- Performa model (MAE, RMSE, R²)
- Perbandingan model
- Pipeline Data Science
Mendukung info dinamis per kota.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from engine.data_preprocessing import format_rupiah, get_schema


def render_model_info(models: dict, nama_kota: str):
    """Render halaman info model dan bobot"""
    
    st.markdown(f"<div class='title-gradient'>Info Model & Bobot ({nama_kota})</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>Halaman ini menjelaskan BAGAIMANA model Machine Learning bekerja untuk data {nama_kota}, apa saja BOBOT yang dipelajari, dan seberapa AKURAT prediksinya.</div>", unsafe_allow_html=True)
    
    metadata = models.get('metadata', {})
    
    if not metadata:
        st.warning("⚠️ Metadata model belum dimuat. Jalankan training terlebih dahulu.")
        _render_pipeline_info(metadata, nama_kota)
        return
        
    schema = get_schema(models)
    
    # ---- Pipeline Data Science ----
    st.markdown("### 🔬 Pipeline Data Science yang Digunakan")
    st.markdown("""
        <div class='info-box'>
            <b>Ini bukan kalkulator!</b> Berikut adalah pipeline Machine Learning lengkap yang dijalankan:
        </div>
    """, unsafe_allow_html=True)
    
    total_data = metadata.get('total_data', 'Ribuan')
    clean_data = metadata.get('clean_data', 'Semua data bersih')
    outliers = metadata.get('outliers_removed', 'Beberapa')
    train_size = metadata.get('train_size', '80%')
    test_size = metadata.get('test_size', '20%')
    
    steps = [
        ("1. Kumpulkan Dataset", f"Kumpulan data rumah asli dari {nama_kota}.", "#3b82f6"),
        ("2. Feature Selection", f"Memilih {len(schema)} fitur terpenting dan membuang ID/data yang tidak relevan.", "#8b5cf6"),
        ("3. Deteksi Outlier (IQR)", f"Menghapus data yang menyimpang terlalu jauh (outliers).", "#f59e0b"),
        ("4. Analisis Korelasi", "Mencari fitur mana yang paling berpengaruh secara statistik ke harga.", "#ec4899"),
        ("5. Train/Test Split", f"Membagi data latih ({train_size}) dan uji ({test_size}).", "#10b981"),
        ("6. Scaling & Encoding", "Normalisasi rentang angka (StandardScaler) dan mengubah teks ke angka (LabelEncoder).", "#06b6d4"),
        ("7. Training (model.fit)", "Model belajar pola dari data latih: Linear Regression, Random Forest, Neural Network.", "#ef4444"),
        ("8. Evaluasi", "Ukur akurasi di data uji → pilih model terbaik.", "#f97316"),
        ("9. Export Model", "Simpan ke .pkl dan .h5 → dimuat secara dinamis oleh web app.", "#a855f7"),
    ]
    
    for title, desc, color in steps:
        st.markdown(f"""
            <div class='pipeline-step' style='border-left-color: {color};'>
                <b style='color: {color};'>{title}</b><br>
                <span style='color: #94a3b8; font-size: 0.85rem;'>{desc}</span>
            </div>
        """, unsafe_allow_html=True)
    
    # ---- Perbandingan Model ----
    st.write("---")
    st.markdown("### 🏆 Perbandingan Performa Model")
    
    comparison = metadata.get('comparison', {})
    if comparison:
        comp_df = pd.DataFrame(comparison)
        
        best_model = metadata.get('best_model', 'Unknown')
        best_r2 = metadata.get('best_r2', 0)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-label'>Model Terbaik</div>
                    <div class='kpi-value' style='font-size:1.5rem; color:#10b981;'>{best_model}</div>
                    <div class='kpi-badge' style='background-color:#10b98120;color:#10b981;'>🏆 Winner</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-label'>Akurasi (R² Score)</div>
                    <div class='kpi-value' style='color:#3b82f6;'>{best_r2:.1%}</div>
                    <div class='kpi-badge' style='background-color:#3b82f620;color:#3b82f6;'>Skor 0-100%</div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-label'>Fitur Dipakai</div>
                    <div class='kpi-value' style='color:#f59e0b;'>{len(schema)} Fitur</div>
                    <div class='kpi-badge' style='background-color:#f59e0b20;color:#f59e0b;'>Sangat Dinamis</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.write("")
        
        # Format tabel perbandingan
        if 'MAE (Rp)' in comp_df.columns:
            display_df = comp_df.copy()
            display_df['MAE'] = display_df['MAE (Rp)'].apply(lambda x: format_rupiah(x))
            display_df['RMSE'] = display_df['RMSE (Rp)'].apply(lambda x: format_rupiah(x))
            display_df['R²'] = display_df['R² Score'].apply(lambda x: f"{x:.4f} ({x*100:.1f}%)")
            st.dataframe(display_df[['Model', 'MAE', 'RMSE', 'R²']], use_container_width=True, hide_index=True)
        else:
            st.dataframe(comp_df, use_container_width=True, hide_index=True)
        
        # Grafik R²
        if 'R² Score' in comp_df.columns and 'Model' in comp_df.columns:
            fig = go.Figure()
            colors = ['#3b82f6', '#10b981', '#f59e0b']
            for i, (_, row) in enumerate(comp_df.iterrows()):
                fig.add_trace(go.Bar(
                    x=[row['Model']],
                    y=[row['R² Score']],
                    name=row['Model'],
                    marker_color=colors[i % 3],
                    opacity=0.85,
                    text=f"{row['R² Score']:.4f}",
                    textposition='outside'
                ))
            fig.update_layout(
                title='Perbandingan R² Score (Semakin Tinggi = Semakin Akurat)',
                yaxis_title='R² Score',
                yaxis_range=[0, 1],
                template='plotly_dark',
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        # Fallback jika comparison dict tidak disave, tapi best_r2 ada (seperti di surabaya)
        best_model = metadata.get('best_model', 'Unknown')
        best_r2 = metadata.get('best_r2', 0)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-label'>Model Terbaik</div>
                    <div class='kpi-value' style='font-size:1.5rem; color:#10b981;'>{best_model}</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class='kpi-card'>
                    <div class='kpi-label'>Akurasi (R² Score)</div>
                    <div class='kpi-value' style='color:#3b82f6;'>{best_r2:.1%}</div>
                </div>
            """, unsafe_allow_html=True)
    
    # ---- Bobot Model ----
    st.write("---")
    st.markdown("### ⚖️ Bobot (Weights) — Fitur Mana yang Paling Berpengaruh?")
    
    tab1, tab2 = st.tabs(["🌲 Random Forest (Feature Importance)", "📊 Linear Regression (Coefficients)"])
    
    with tab1:
        rf_importance = metadata.get('feature_importances', metadata.get('rf_importance', {}))
        if rf_importance:
            st.markdown("""
                <div class='info-box'>
                    <b>Feature Importance</b> menunjukkan seberapa besar kontribusi setiap fitur dalam prediksi.
                    Semakin tinggi nilainya, semakin berpengaruh fitur tersebut terhadap harga rumah.
                    Ini adalah <b>BOBOT</b> yang dipelajari model dari data.
                </div>
            """, unsafe_allow_html=True)
            
            # Map nama fitur ke label untuk UI yang lebih baik
            label_dict = {f['name']: f.get('label', f['name']) for f in schema}
            
            imp_df = pd.DataFrame({
                'Fitur Asli': list(rf_importance.keys()),
                'Importance': list(rf_importance.values())
            })
            imp_df['Fitur'] = imp_df['Fitur Asli'].apply(lambda x: label_dict.get(x, x))
            imp_df = imp_df.sort_values('Importance', ascending=True)
            
            fig_imp = go.Figure()
            fig_imp.add_trace(go.Bar(
                y=imp_df['Fitur'],
                x=imp_df['Importance'],
                orientation='h',
                marker_color='#10b981',
                opacity=0.85,
                text=[f"{v:.4f}" for v in imp_df['Importance']],
                textposition='outside'
            ))
            fig_imp.update_layout(
                title='Feature Importance — Random Forest',
                xaxis_title='Importance Score (Bobot Pengaruh)',
                template='plotly_dark',
                height=max(400, len(imp_df)*40) # Dinamis tinggi grafik
            )
            st.plotly_chart(fig_imp, use_container_width=True)
        else:
            st.info("Data feature importance belum tersedia.")
    
    with tab2:
        lr_coef = metadata.get('lr_coef', {})
        lr_intercept = metadata.get('lr_intercept', 0)
        if lr_coef:
            st.markdown("""
                <div class='info-box'>
                    <b>Coefficients (Koefisien)</b> menunjukkan BOBOT setiap fitur dalam rumus Linear Regression.<br>
                    Bobot positif (+) = meningkatkan harga. Bobot negatif (-) = menurunkan harga.
                </div>
            """, unsafe_allow_html=True)
            
            # Map nama fitur ke label
            label_dict = {f['name']: f.get('label', f['name']) for f in schema}
            
            coef_df = pd.DataFrame({
                'Fitur Asli': list(lr_coef.keys()),
                'Bobot (Coefficient)': list(lr_coef.values())
            })
            coef_df['Fitur'] = coef_df['Fitur Asli'].apply(lambda x: label_dict.get(x, x))
            coef_df = coef_df.sort_values('Bobot (Coefficient)', ascending=True)
            
            colors_coef = ['#ef4444' if v < 0 else '#10b981' for v in coef_df['Bobot (Coefficient)']]
            
            fig_coef = go.Figure()
            fig_coef.add_trace(go.Bar(
                y=coef_df['Fitur'],
                x=coef_df['Bobot (Coefficient)'],
                orientation='h',
                marker_color=colors_coef,
                opacity=0.85,
                text=[f"{v:,.0f}" for v in coef_df['Bobot (Coefficient)']],
                textposition='outside'
            ))
            fig_coef.update_layout(
                title=f'Bobot (Coefficients) — Linear Regression | Bias = {format_rupiah(lr_intercept)}',
                xaxis_title='Bobot (Coefficient dalam Rupiah)',
                template='plotly_dark',
                height=max(400, len(coef_df)*40)
            )
            st.plotly_chart(fig_coef, use_container_width=True)
            
            st.markdown(f"**Bias (Intercept):** {format_rupiah(lr_intercept)} — ini adalah harga dasar sebelum ditambah pengaruh fitur.")
        else:
            st.info("Data coefficients belum disimpan oleh model ini.")
    
    # ---- Penjelasan Sidang ----
    st.write("---")
    _render_pipeline_info(metadata, nama_kota)


def _render_pipeline_info(metadata: dict, nama_kota: str):
    """Render penjelasan untuk sidang"""
    st.markdown("###  Penjelasan Konsep")
    
    train_size = metadata.get('train_size', '800+') if metadata else '800+'
    
    qa = [
        ("Apa bedanya dengan kalkulator biasa?",
         f"Kalkulator hanya menjalankan rumus tetap (input → rumus → output). "
         f"Model ML ini sudah BELAJAR dari {train_size} data rumah asli di wilayah {nama_kota}. Ia menemukan POLA dan menyimpannya "
         "sebagai BOBOT (weights) di dalam file .pkl/.h5. Saat memprediksi, ia menggunakan bobot "
         "yang sudah dipelajari, bukan rumus buatan manusia."),
        
        ("Apa itu bobot (weights)?",
         "Bobot adalah angka-angka yang dipelajari model dari data training. "
         "Contoh: model belajar bahwa setiap 1 m² luas tanah menambah harga ~Rp X. "
         "Nilai X inilah yang disebut bobot. Di Linear Regression disebut coefficient, "
         "di Neural Network disebut weight, di Random Forest disebut feature importance."),
        
        ("Dimana sigmoid digunakan?",
         "Sigmoid digunakan sebagai fungsi aktivasi di Neural Network (file .h5). "
         "Fungsi sigmoid mengubah nilai apapun menjadi angka antara 0 dan 1, "
         "membantu neuron dalam jaringan untuk 'memutuskan' seberapa kuat sinyal yang diteruskan."),
        
        ("Apa itu deteksi outlier (IQR)?",
         "Outlier adalah data yang nilainya sangat jauh dari mayoritas data. "
         "Metode IQR menghitung Q1 (kuartil 25%) dan Q3 (kuartil 75%), lalu menentukan batas normal. "
         "Data di luar batas dianggap outlier dan dihapus agar model tidak belajar dari data yang menyimpang."),
        
        ("Kenapa harus train/test split?",
         "Agar kita bisa mengukur seberapa baik model belajar. Data training untuk belajar, "
         "data testing untuk ujian. Jika model akurat di data testing (yang belum pernah dilihat), "
         "berarti model benar-benar memahami pola, bukan sekedar menghafal."),
        
        ("Apa itu R² Score?",
         "R² Score (R-squared) mengukur seberapa baik model menjelaskan variasi data. "
         "Nilainya 0 sampai 1. R²=0.8 berarti model bisa menjelaskan 80% variasi harga rumah. "
         "Semakin mendekati 1, semakin akurat model."),
    ]
    
    for question, answer in qa:
        with st.expander(f"❓ {question}"):
            st.write(answer)
