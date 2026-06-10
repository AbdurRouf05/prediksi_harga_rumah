"""
Styles Module - CSS Premium untuk Dashboard Prediksi Harga Rumah
"""

import streamlit as st


def inject_css():
    """Menyuntikkan stylesheet CSS premium ke dalam aplikasi Streamlit"""
    st.markdown("""
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');
        
        /* Root variables */
        :root {
            --primary: #3b82f6;
            --primary-dark: #2563eb;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --purple: #8b5cf6;
            --bg-dark: #0f172a;
            --bg-card: #1e293b;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --border: #334155;
        }
        
        /* Global styles */
        .stApp {
            font-family: 'Outfit', sans-serif;
        }
        
        /* Title gradient */
        .title-gradient {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            font-weight: 800;
            font-family: 'Outfit', sans-serif;
            margin-bottom: 0.3rem;
            letter-spacing: -0.02em;
        }
        
        .subtitle {
            font-size: 1rem;
            color: #94a3b8;
            margin-bottom: 1.5rem;
            font-weight: 300;
        }
        
        /* KPI Cards */
        .kpi-card {
            background: linear-gradient(145deg, #1e293b, #0f172a);
            border-radius: 16px;
            padding: 1.5rem;
            border: 1px solid #334155;
            text-align: center;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3);
        }
        
        .kpi-card:hover {
            transform: translateY(-2px);
            border-color: #3b82f6;
            box-shadow: 0 8px 25px -5px rgba(59, 130, 246, 0.2);
        }
        
        .kpi-label {
            font-size: 0.8rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }
        
        .kpi-value {
            font-size: 2rem;
            font-weight: 700;
            color: #f1f5f9;
            font-family: 'Outfit', sans-serif;
            line-height: 1.2;
            margin-bottom: 0.5rem;
        }
        
        .kpi-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        
        /* Prediction result card */
        .prediction-card {
            background: linear-gradient(145deg, #1e293b, #0f172a);
            border-radius: 20px;
            padding: 2.5rem;
            border: 2px solid #3b82f6;
            text-align: center;
            box-shadow: 0 0 40px rgba(59, 130, 246, 0.15);
        }
        
        .prediction-price {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, #3b82f6, #10b981);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Outfit', sans-serif;
            line-height: 1.2;
            margin: 0.5rem 0;
        }
        
        .prediction-label {
            font-size: 0.9rem;
            color: #94a3b8;
            margin-bottom: 0.5rem;
        }
        
        /* Feature importance bar */
        .feature-bar {
            background: #1e293b;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            margin-bottom: 0.3rem;
            border: 1px solid #334155;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .feature-name {
            font-size: 0.85rem;
            color: #f1f5f9;
            min-width: 180px;
            font-weight: 500;
        }
        
        .feature-value {
            font-size: 0.8rem;
            color: #94a3b8;
            font-family: 'JetBrains Mono', monospace;
        }
        
        /* Section headers */
        .section-header {
            font-size: 1.3rem;
            font-weight: 700;
            color: #f1f5f9;
            margin: 1.5rem 0 0.8rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #334155;
        }
        
        /* Info boxes */
        .info-box {
            background: linear-gradient(145deg, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05));
            border-radius: 12px;
            padding: 1rem 1.5rem;
            border-left: 4px solid #3b82f6;
            margin: 1rem 0;
            font-size: 0.9rem;
            color: #cbd5e1;
        }
        
        /* Model comparison cards */
        .model-card {
            background: linear-gradient(145deg, #1e293b, #0f172a);
            border-radius: 12px;
            padding: 1.2rem;
            border: 1px solid #334155;
            transition: all 0.3s ease;
        }
        
        .model-card.winner {
            border-color: #10b981;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.15);
        }
        
        /* Welcome card */
        .welcome-card {
            background: linear-gradient(145deg, rgba(59, 130, 246, 0.08), rgba(139, 92, 246, 0.05));
            border-radius: 20px;
            padding: 3rem;
            text-align: center;
            border: 1px dashed rgba(59, 130, 246, 0.3);
            margin-top: 2rem;
        }
        
        .welcome-card h3 {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 1.8rem;
            margin-bottom: 1rem;
        }
        
        /* Pipeline step */
        .pipeline-step {
            background: #1e293b;
            border-radius: 10px;
            padding: 0.8rem 1rem;
            margin-bottom: 0.5rem;
            border-left: 3px solid;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)
