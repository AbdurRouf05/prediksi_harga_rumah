"""
Model Loader Module
===================
Fungsi untuk memuat model ML yang sudah dilatih (.pkl / .h5)
beserta scaler dan metadata pendukung dari folder sesuai kota.
"""

import os
import joblib

try:
    from tensorflow.keras.models import load_model as keras_load_model
    HAS_TENSORFLOW = True
except ImportError:
    HAS_TENSORFLOW = False


def load_all_models(kota: str = 'jakarta', models_dir: str = None) -> dict:
    """
    Memuat semua model, scaler, dan metadata dari folder models/<kota>/.
    
    Parameters:
        kota: 'jakarta' atau 'surabaya'
        
    Returns:
        dict berisi model_lr, model_rf, model_nn, scaler, metadata
    """
    if models_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        models_dir = os.path.join(base_dir, 'models', kota)
    
    result = {}
    
    # 1. Load Linear Regression
    lr_path = os.path.join(models_dir, 'model_lr.pkl')
    if os.path.exists(lr_path):
        result['model_lr'] = joblib.load(lr_path)
        print(f"  [LOADER] [OK] Linear Regression ({kota}) dimuat")
    else:
        result['model_lr'] = None
    
    # 2. Load Random Forest
    rf_path = os.path.join(models_dir, 'model_rf.pkl')
    if os.path.exists(rf_path):
        result['model_rf'] = joblib.load(rf_path)
        print(f"  [LOADER] [OK] Random Forest ({kota}) dimuat")
    else:
        result['model_rf'] = None
    
    # 3. Load Neural Network
    nn_path = os.path.join(models_dir, 'model_nn.h5')
    if os.path.exists(nn_path) and HAS_TENSORFLOW:
        result['model_nn'] = keras_load_model(nn_path)
        print(f"  [LOADER] [OK] Neural Network ({kota}) dimuat")
    else:
        result['model_nn'] = None
    
    # 4. Load Scaler
    scaler_path = os.path.join(models_dir, 'scaler.pkl')
    if os.path.exists(scaler_path):
        result['scaler'] = joblib.load(scaler_path)
        print(f"  [LOADER] [OK] Scaler ({kota}) dimuat")
    else:
        result['scaler'] = None
        print(f"  [LOADER] [ERROR] scaler.pkl ({kota}) tidak ditemukan!")
    
    # 5. Load Metadata
    meta_path = os.path.join(models_dir, 'metadata.pkl')
    if os.path.exists(meta_path):
        result['metadata'] = joblib.load(meta_path)
        print(f"  [LOADER] [OK] Metadata ({kota}) dimuat")
    else:
        result['metadata'] = {}
        
    # 6. Load Encoders (jika ada, untuk UI dinamis)
    encoders_path = os.path.join(models_dir, 'encoders.pkl')
    if os.path.exists(encoders_path):
        result['encoders'] = joblib.load(encoders_path)
        print(f"  [LOADER] [OK] Encoders ({kota}) dimuat")
    else:
        result['encoders'] = {}
    
    return result


def check_models_exist(kota: str = 'jakarta', models_dir: str = None) -> bool:
    """Cek apakah file model minimum sudah ada untuk kota tertentu."""
    if models_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        models_dir = os.path.join(base_dir, 'models', kota)
    
    # Wajib: scaler
    if not os.path.exists(os.path.join(models_dir, 'scaler.pkl')):
        return False
    
    # Minimal 1 model
    model_files = ['model_lr.pkl', 'model_rf.pkl', 'model_nn.h5']
    return any(os.path.exists(os.path.join(models_dir, f)) for f in model_files)
