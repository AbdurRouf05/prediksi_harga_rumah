# Penjelasan Kode Backend (Folder engine)

Folder `engine/` berisi **otak logika** aplikasi. Ia tidak memiliki tampilan — tugasnya murni memproses data di belakang layar.

## 1. model_loader.py — Pemuat Model

### Apa Tugasnya

Membaca file-file model ML (.pkl, .h5) dari disk ke dalam memori komputer.
Tanpa modul ini, semua model hanya "tidur" di dalam file dan tidak bisa digunakan.

### Daftar Fungsi model_loader

#### `load_all_models(kota, models_dir)`

```python
Input:  kota = 'jakarta' / 'surabaya' / 'lumajang'
Output: Dictionary berisi model_lr, model_rf, model_nn, scaler, 
        metadata, encoders
```

- Membuka folder `models/<kota>/`
- Membaca setiap file `.pkl` menggunakan `joblib.load()`
- Membaca `model_nn.h5` menggunakan `keras.models.load_model()`
- Jika file tidak ada, isi-nya `None` (tidak error)
- Mengembalikan semua ke dalam satu dictionary

#### `check_models_exist(kota, models_dir)`

```python
Input:  kota = 'jakarta'
Output: True / False
```

- Mengecek apakah file `scaler.pkl` ada (WAJIB ada)
- Mengecek apakah minimal 1 dari 3 model ada
- Digunakan di `app.py` sebelum mencoba load model

## 2. data_preprocessing.py — Pengolah Input User

### Apa Tugas Modul Ini

Mengubah input mentah dari pengguna (misal: LT=150, KM=2, Sertifikat="SHM") menjadi format numerik yang bisa dipahami model ML.

### Kenapa Perlu Diproses

Model ML hanya mengerti ANGKA. Jadi:

- Teks "SHM" harus diubah ke angka (misal: 2) menggunakan LabelEncoder
- Semua angka harus dinormalisasi (StandardScaler) agar skala seimbang

### Daftar Fungsi data_preprocessing

#### `get_schema(models)`

```python
Input:  models = dictionary dari model_loader
Output: List schema fitur (nama, tipe, min, max, options)
```

- Mengambil `schema` dari `metadata.pkl`
- Jika tidak ada, gunakan `DEFAULT_SCHEMA` (fallback Jakarta lama)
- Schema menentukan form input apa yang muncul di halaman web

#### `get_feature_names(models)`

- Mengembalikan daftar nama fitur saja (tanpa detail lain)

#### `preprocess_input(input_dict, models)`

```python
Input:  input_dict = {'LT': 150, 'KM': 2, 'Sertifikat': 'SHM'}
        models = dictionary model
Output: numpy array yang sudah di-scale, siap masuk model
```

Langkah-langkah:

1. Loop setiap fitur di schema
2. Jika tipe = `categorical` → encode pakai LabelEncoder
3. Jika tipe = `numeric` → langsung ambil angkanya
4. Susun menjadi DataFrame
5. Transform dengan StandardScaler
6. Return array

#### `format_rupiah(value)`

```python
Input:  2500000000
Output: "Rp 2.50 Miliar"
```

- Mengubah angka menjadi format rupiah yang mudah dibaca
- Otomatis memilih satuan (Juta, Miliar, Triliun)

## 3. predictor.py — Mesin Prediksi

### Tugas Utama Predictor

Menjalankan prediksi harga menggunakan model yang sudah dimuat.

### Daftar Fungsi predictor

#### `predict_price(input_dict, models, model_name)`

```python
Input:  input_dict = {'LT': 150, 'KM': 2}
        models = dictionary model
        model_name = 'auto' / 'lr' / 'rf' / 'nn'
Output: {
          'harga_prediksi': 2500000000,
          'harga_formatted': 'Rp 2.50 Miliar',
          'model_digunakan': 'Random Forest',
          'semua_prediksi': {
              'Linear Regression': 2200000000,
              'Random Forest': 2500000000,
              'Neural Network': 2400000000
          }
        }
```

Langkah-langkah:

1. Panggil `preprocess_input()` untuk mengolah input
2. Prediksi dengan SEMUA model yang tersedia (LR, RF, NN)
3. Untuk Neural Network: karena dilatih pakai sigmoid (0-1), hasilnya dikalikan kembali dengan `y_max_nn`
4. Jika `model_name='auto'`, pilih model terbaik dari metadata
5. Kembalikan semua hasil prediksi

## Alur Pemanggilan Antar File

```text
User klik "Prediksi" di browser
    │
    ▼
page_predict.py
    │ input_dict = {'LT': 150, 'KM': 2}
    ▼
predictor.py  →  predict_price(input_dict, models)
    │
    ▼
data_preprocessing.py  →  preprocess_input(input_dict, models)
    │ 1. LabelEncode teks
    │ 2. StandardScale angka
    ▼
model.predict(input_scaled)  ← Model RF/LR/NN yang sudah di-load
    │
    ▼
return {'harga': 2500000000, 'formatted': 'Rp 2.50 Miliar'}
```
