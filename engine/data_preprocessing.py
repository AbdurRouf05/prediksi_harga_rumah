"""
Data Preprocessing Module
=========================
Fungsi untuk menyiapkan input data pengguna agar bisa diproses
oleh model ML yang sudah dilatih. Mendukung UI dinamis.
"""

import pandas as pd
import numpy as np

# Fallback schema untuk model Jakarta (yang tidak punya schema dinamis di metadata)
DEFAULT_SCHEMA = [
    {'name': 'LB', 'label': 'Luas Bangunan (m²)', 'type': 'numeric', 'min': 20, 'max': 1500, 'default': 100},
    {'name': 'LT', 'label': 'Luas Tanah (m²)', 'type': 'numeric', 'min': 20, 'max': 2000, 'default': 150},
    {'name': 'KT', 'label': 'Kamar Tidur', 'type': 'numeric', 'min': 1, 'max': 10, 'default': 3},
    {'name': 'KM', 'label': 'Kamar Mandi', 'type': 'numeric', 'min': 1, 'max': 10, 'default': 2},
    {'name': 'GRS', 'label': 'Garasi (Mobil)', 'type': 'numeric', 'min': 0, 'max': 10, 'default': 1},
]

def get_schema(models: dict):
    """Mendapatkan schema fitur dari metadata model"""
    meta = models.get('metadata', {})
    if 'schema' in meta:
        return meta['schema']
    return DEFAULT_SCHEMA

def get_feature_names(models: dict):
    """Mendapatkan daftar urutan fitur"""
    schema = get_schema(models)
    return [f['name'] for f in schema]

def preprocess_input(input_dict: dict, models: dict) -> np.ndarray:
    """
    Preprocessing input dari user menjadi format siap prediksi.
    
    1. Loop semua fitur di schema
    2. Jika kategorikal, encode menggunakan LabelEncoder (dari models['encoders'])
    3. Susun array dan transform pakai scaler
    """
    schema = get_schema(models)
    feature_names = get_feature_names(models)
    encoders = models.get('encoders', {})
    scaler = models.get('scaler')
    
    processed_values = []
    
    for feature in schema:
        name = feature['name']
        val = input_dict.get(name)
        
        if feature['type'] == 'categorical':
            # Encode
            le = encoders.get(name)
            if le is not None:
                try:
                    encoded_val = le.transform([str(val)])[0]
                except ValueError:
                    encoded_val = 0 # Fallback jika tidak dikenal
                processed_values.append(encoded_val)
            else:
                processed_values.append(0)
        else:
            # Numeric
            if val is None:
                val = feature.get('default', 0)
            processed_values.append(float(val))
            
    input_df = pd.DataFrame([processed_values], columns=feature_names)
    input_scaled = scaler.transform(input_df)
    return input_scaled

def format_rupiah(value):
    """Format angka ke format Rupiah Indonesia"""
    if value >= 1e12:
        return f"Rp {value/1e12:,.2f} Triliun"
    elif value >= 1e9:
        return f"Rp {value/1e9:,.2f} Miliar"
    elif value >= 1e6:
        return f"Rp {value/1e6:,.0f} Juta"
    else:
        return f"Rp {value:,.0f}"
