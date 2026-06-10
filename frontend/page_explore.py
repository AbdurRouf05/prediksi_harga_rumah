"""
Page: Eksplorasi Data (EDA)
===========================
Halaman yang menampilkan visualisasi eksplorasi data dari dataset.
Mendukung dataset dinamis untuk tiap kota.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os

from engine.data_preprocessing import format_rupiah, get_schema


def load_dataset(kota_aktif: str):
    """Load dataset dari folder dataset/<kota_aktif>/"""
    # Coba cari full data CSV dulu (seperti surabaya)
    dataset_path_full = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'dataset', kota_aktif, 'DATA_RUMAH_FULL.csv'
    )
    if os.path.exists(dataset_path_full):
        return pd.read_csv(dataset_path_full)
        
    dataset_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'dataset', kota_aktif, 'DATA_RUMAH.csv'
    )
    if os.path.exists(dataset_path):
        return pd.read_csv(dataset_path)
        
    dataset_path_deep = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'dataset', kota_aktif, 'DATA_RUMAH_LUMAJANG_DEEP.csv'
    )
    if os.path.exists(dataset_path_deep):
        return pd.read_csv(dataset_path_deep)
    
    # Fallback ke xlsx jika ada (seperti jakarta)
    xlsx_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'dataset', kota_aktif, 'DATA_RUMAH.xlsx'
    )
    if os.path.exists(xlsx_path):
        return pd.read_excel(xlsx_path)
        
    return None


def render_explore(models: dict, kota_aktif: str, nama_kota: str):
    """Render halaman eksplorasi data"""
    
    st.markdown(f"<div class='title-gradient'>Eksplorasi Data (EDA) — {nama_kota}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>Melihat dan memahami dataset asli rumah {nama_kota}. Tahap EDA adalah fondasi penting dalam Data Science — sebelum membangun model, kita harus MEMAHAMI data.</div>", unsafe_allow_html=True)
    
    df = load_dataset(kota_aktif)
    if df is None:
        st.error(f"❌ Dataset tidak ditemukan untuk kota {nama_kota}!")
        return
        
    # Standardize column target
    target_col = 'HARGA' if 'HARGA' in df.columns else 'Harga'
    if target_col not in df.columns:
        st.error("❌ Kolom harga (target) tidak ditemukan di dataset ini.")
        return
        
    # Pastikan target numerik (kasus Lumajang yang masih teks "RP 2,85 MILIAR")
    if df[target_col].dtype == object:
        df_target = df[target_col].astype(str).str.upper().str.replace('RP ', '', regex=False)
        df_target = df_target.str.replace(',', '.', regex=False)
        
        def parse_harga(x):
            try:
                if 'MILIAR' in x:
                    return float(x.replace(' MILIAR', '').strip()) * 1e9
                elif 'JUTA' in x:
                    return float(x.replace(' JUTA', '').strip()) * 1e6
                return float(x.strip())
            except:
                return np.nan
                
        df[target_col] = df_target.apply(parse_harga)
        df = df.dropna(subset=[target_col])
    
    metadata = models.get('metadata', {})
    schema = get_schema(models)
    
    fitur_dipakai = [f['name'] for f in schema]
    
    # ---- Info Dasar ----
    st.markdown("### 📊 Informasi Dataset")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>Total Baris Data</div>
                <div class='kpi-value' style='color:#3b82f6;'>{len(df):,}</div>
                <div class='kpi-badge' style='background-color:#3b82f620;color:#3b82f6;'>Data Asli {nama_kota}</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>Total Kolom</div>
                <div class='kpi-value' style='color:#10b981;'>{len(df.columns)}</div>
                <div class='kpi-badge' style='background-color:#10b98120;color:#10b981;'>{len(fitur_dipakai)} fitur dipakai</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        missing_total = df.isnull().sum().sum()
        st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>Data Kosong (Missing)</div>
                <div class='kpi-value' style='color:#f59e0b;'>{missing_total}</div>
                <div class='kpi-badge' style='background-color:#f59e0b20;color:#f59e0b;'>{'✅ Lengkap' if missing_total == 0 else '⚠️ Ada yang kosong'}</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        outliers_removed = metadata.get('outliers_removed', 'Dibersihkan')
        st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-label'>Outlier</div>
                <div class='kpi-value' style='color:#ef4444; font-size:1.5rem;'>{outliers_removed}</div>
                <div class='kpi-badge' style='background-color:#ef444420;color:#ef4444;'>Metode IQR</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    
    # ---- Pratinjau Data ----
    with st.expander("📋 Pratinjau Data Mentah (10 Baris Pertama)", expanded=False):
        st.dataframe(df.head(10), use_container_width=True, height=300)
    
    # ---- Feature Selection ----
    st.write("---")
    st.markdown("### 🗑️ Feature Selection — Fitur Berguna vs Tidak Berguna")
    st.markdown("""
        <div class='info-box'>
            <b>Konsep penting dalam Data Science:</b> Tidak semua kolom berguna untuk prediksi. 
            Kita harus <b>memilih fitur yang penting</b> dan <b>membuang yang tidak berguna</b>.
        </div>
    """, unsafe_allow_html=True)
    
    col_good, col_bad = st.columns(2)
    with col_good:
        st.markdown("**✅ Fitur BERGUNA (digunakan model)**")
        for f in schema:
            st.markdown(f"- ✅ `{f['name']}` — {f.get('label', f['name'])}")
    
    with col_bad:
        st.markdown("**❌ Fitur TIDAK BERGUNA (dibuang)**")
        useless_cols = [c for c in df.columns if c not in fitur_dipakai and c != target_col]
        if useless_cols:
            for c in useless_cols:
                st.markdown(f"- ❌ `{c}` — Berpotensi menjadi noise atau tidak berkorelasi.")
        else:
            st.markdown("- *Semua fitur mentah telah difilter di tahap awal dataset.*")
    
    # ---- Visualisasi ----
    st.write("---")
    st.markdown("### 📈 Visualisasi Data")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Distribusi Harga", "Korelasi Fitur Numerik", "Deteksi Outlier", "Distribusi Fitur Tambahan"])
    
    with tab1:
        # Distribusi Harga
        harga_miliar = df[target_col] / 1e9
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=harga_miliar, nbinsx=50,
            marker_color='#3b82f6', opacity=0.8,
            name='Distribusi Harga'
        ))
        fig.update_layout(
            title=f'Distribusi Harga Rumah {nama_kota}',
            xaxis_title='Harga (Miliar Rp)',
            yaxis_title='Frekuensi',
            template='plotly_dark',
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
            **📊 Statistik Harga:**
            - Termurah: {format_rupiah(df[target_col].min())}
            - Termahal: {format_rupiah(df[target_col].max())}
            - Rata-rata: {format_rupiah(df[target_col].mean())}
            - Median: {format_rupiah(df[target_col].median())}
        """)
    
    with tab2:
        # Scatter plots korelasi
        # Coba ambil 'LT' atau kolom numerik pertama
        numeric_features = [f['name'] for f in schema if f['type'] == 'numeric']
        if numeric_features:
            x_col = numeric_features[0] if 'LT' not in numeric_features else 'LT'
            
            # Extract numbers in case the raw data is string like "430 M2" (Lumajang case)
            x_data = df[x_col]
            if x_data.dtype == object:
                x_data = pd.to_numeric(x_data.astype(str).str.extract(r'(\d+)', expand=False), errors='coerce')
                
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=x_data, y=harga_miliar,
                mode='markers',
                marker=dict(color='#f59e0b', size=5, opacity=0.4),
                name='Data Rumah'
            ))
            fig2.update_layout(
                title=f'Korelasi: {x_col} vs Harga Rumah',
                xaxis_title=x_col,
                yaxis_title='Harga (Miliar Rp)',
                template='plotly_dark',
                height=450
            )
            st.plotly_chart(fig2, use_container_width=True)
            
            st.info("📝 Terlihat pola: semakin besar luas tanah/bangunan, semakin tinggi harga. Ini adalah **korelasi positif**.")
            
            # Heatmap korelasi numerik
            df_num = df[numeric_features + [target_col]].copy()
            # pastikan numerik
            for c in df_num.columns:
                df_num[c] = pd.to_numeric(df_num[c], errors='coerce')
                
            corr_matrix = df_num.corr()
            
            fig3 = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdYlBu_r',
                zmid=0,
                text=corr_matrix.values.round(2),
                texttemplate='%{text}',
                textfont=dict(size=14),
            ))
            fig3.update_layout(
                title='Heatmap Korelasi Antar Fitur',
                template='plotly_dark',
                height=500,
                width=600,
            )
            st.plotly_chart(fig3, use_container_width=True)
    
    with tab3:
        st.markdown("### 🔍 Deteksi Outlier (Metode IQR)")
        st.markdown("""
            <div class='info-box'>
                <b>Metode IQR (Interquartile Range)</b> adalah cara standar mendeteksi outlier:<br>
                <code>Q1 = kuartil 25% | Q3 = kuartil 75% | IQR = Q3 - Q1</code><br>
                <code>Batas bawah = Q1 - 1.5×IQR | Batas atas = Q3 + 1.5×IQR</code><br>
                Data di luar batas → <b>OUTLIER</b> → dihapus sebelum training.
            </div>
        """, unsafe_allow_html=True)
        
        fitur_outlier = st.selectbox("Pilih fitur:", [target_col] + numeric_features)
        
        col_data = pd.to_numeric(df[fitur_outlier], errors='coerce').dropna()
        Q1 = col_data.quantile(0.25)
        Q3 = col_data.quantile(0.75)
        IQR = Q3 - Q1
        batas_bawah = Q1 - 1.5 * IQR
        batas_atas = Q3 + 1.5 * IQR
        outlier_count = ((col_data < batas_bawah) | (col_data > batas_atas)).sum()
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Q1 (25%)", f"{Q1:,.0f}")
            st.metric("Batas Bawah", f"{batas_bawah:,.0f}")
        with col_b:
            st.metric("Q3 (75%)", f"{Q3:,.0f}")
            st.metric("Batas Atas", f"{batas_atas:,.0f}")
        with col_c:
            st.metric("IQR", f"{IQR:,.0f}")
            st.metric("Outlier Ditemukan", f"{outlier_count}")
        
        fig4 = go.Figure()
        fig4.add_trace(go.Box(
            y=col_data, name=fitur_outlier,
            marker_color='#3b82f6',
            boxpoints='outliers',
        ))
        fig4.update_layout(
            title=f'Boxplot {fitur_outlier} — Deteksi Outlier',
            template='plotly_dark',
            height=400
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    with tab4:
        st.markdown("### 📊 Distribusi Fitur Kategorikal / Hitungan")
        
        categorical_or_counts = [f['name'] for f in schema if f['type'] == 'categorical' or f['name'] in ['KT', 'KM', 'Garasi', 'Lantai']]
        
        if not categorical_or_counts:
            st.info("Tidak ada fitur kategorikal untuk ditampilkan.")
        else:
            col_1, col_2 = st.columns(2)
            
            with col_1:
                f1 = categorical_or_counts[0]
                dist1 = df[f1].value_counts().sort_index() if df[f1].dtype in ['int64', 'float64'] else df[f1].value_counts()
                fig5 = go.Figure()
                fig5.add_trace(go.Bar(
                    x=dist1.index.astype(str), y=dist1.values,
                    marker_color='#ec4899', opacity=0.85
                ))
                fig5.update_layout(
                    title=f'Distribusi {f1}',
                    template='plotly_dark', height=350
                )
                st.plotly_chart(fig5, use_container_width=True)
            
            if len(categorical_or_counts) > 1:
                with col_2:
                    f2 = categorical_or_counts[1]
                    dist2 = df[f2].value_counts().sort_index() if df[f2].dtype in ['int64', 'float64'] else df[f2].value_counts()
                    fig6 = go.Figure()
                    fig6.add_trace(go.Bar(
                        x=dist2.index.astype(str), y=dist2.values,
                        marker_color='#06b6d4', opacity=0.85
                    ))
                    fig6.update_layout(
                        title=f'Distribusi {f2}',
                        template='plotly_dark', height=350
                    )
                    st.plotly_chart(fig6, use_container_width=True)
