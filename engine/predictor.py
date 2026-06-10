"""
Predictor Module
================
Fungsi untuk melakukan prediksi harga rumah menggunakan model yang sudah dimuat.
"""

import numpy as np
import pandas as pd
from .data_preprocessing import preprocess_input, format_rupiah


def predict_price(input_dict: dict, models: dict, model_name: str = 'auto') -> dict:
    """
    Prediksi harga satu rumah berdasarkan fitur-fiturnya.
    
    Parameters:
        input_dict: Dictionary berisi fitur rumah (LB, LT, KT, KM, GRS)
        models: Dictionary model yang dimuat dari load_all_models()
        model_name: 'lr', 'rf', 'nn', atau 'auto' untuk terbaik
    
    Returns:
        dict berisi harga_prediksi, model_digunakan, semua_prediksi
    """
    scaler = models.get('scaler')
    metadata = models.get('metadata', {})
    
    if scaler is None:
        return {'error': 'Scaler belum dimuat. Pastikan file .pkl sudah ada.'}
    
    # Preprocessing input
    input_scaled = preprocess_input(input_dict, models)
    
    # Prediksi dengan semua model yang tersedia
    semua_prediksi = {}
    
    if models.get('model_lr') is not None:
        pred_lr = models['model_lr'].predict(input_scaled)[0]
        semua_prediksi['Linear Regression'] = max(0, round(pred_lr))
    
    if models.get('model_rf') is not None:
        pred_rf = models['model_rf'].predict(input_scaled)[0]
        semua_prediksi['Random Forest'] = max(0, round(pred_rf))
    
    if models.get('model_nn') is not None:
        pred_nn = models['model_nn'].predict(input_scaled, verbose=0).flatten()[0]
        # Jika NN di-train dengan normalisasi (sigmoid), kembalikan ke skala harga asli
        y_max = metadata.get('y_max_nn')
        if y_max is not None and pred_nn <= 1.0:
            pred_nn = pred_nn * float(y_max)
        semua_prediksi['Neural Network'] = max(0, round(float(pred_nn)))
    
    if not semua_prediksi:
        return {'error': 'Tidak ada model yang tersedia untuk prediksi.'}
    
    # Pilih model
    if model_name == 'auto':
        best = metadata.get('best_model', 'Random Forest')
        if best in semua_prediksi:
            harga = semua_prediksi[best]
            model_used = best
        else:
            model_used = list(semua_prediksi.keys())[0]
            harga = semua_prediksi[model_used]
    elif model_name == 'lr' and 'Linear Regression' in semua_prediksi:
        harga = semua_prediksi['Linear Regression']
        model_used = 'Linear Regression'
    elif model_name == 'rf' and 'Random Forest' in semua_prediksi:
        harga = semua_prediksi['Random Forest']
        model_used = 'Random Forest'
    elif model_name == 'nn' and 'Neural Network' in semua_prediksi:
        harga = semua_prediksi['Neural Network']
        model_used = 'Neural Network'
    else:
        model_used = list(semua_prediksi.keys())[0]
        harga = semua_prediksi[model_used]
    
    return {
        'harga_prediksi': harga,
        'harga_formatted': format_rupiah(harga),
        'model_digunakan': model_used,
        'semua_prediksi': semua_prediksi,
    }
