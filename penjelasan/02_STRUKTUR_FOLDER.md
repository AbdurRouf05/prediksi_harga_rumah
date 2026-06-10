# Struktur Folder Project

Berikut penjelasan setiap file dan folder dalam project ini.

```text
prediksi_harga_rumah/
│
├── app.py                          ← FILE UTAMA (Entry Point)
│                                      Jalankan: streamlit run app.py
│                                      Berisi konfigurasi halaman, sidebar, 
│                                      pemilihan kota, dan routing menu.
│
├── requirements.txt                ← Daftar library yang harus diinstal
│                                      (pip install -r requirements.txt)
│
├── scraper_lumajang.py             ← Robot Web Scraping untuk Lumajang
│                                      Menggunakan Selenium untuk membuka
│                                      website rumah123.com dan menambang
│                                      data properti satu per satu.
│
├── engine/                         ← MESIN INTI (Backend Logic)
│   ├── __init__.py                    Package initializer
│   ├── model_loader.py                Memuat file .pkl dan .h5 dari disk
│   ├── data_preprocessing.py          Mengolah input user → format model
│   └── predictor.py                   Menjalankan prediksi harga
│
├── frontend/                       ← TAMPILAN WEB (UI)
│   ├── __init__.py                    Package initializer
│   ├── styles.py                      CSS styling untuk tampilan premium
│   ├── page_predict.py                Halaman Prediksi Harga
│   ├── page_explore.py                Halaman Eksplorasi Data (EDA)
│   └── page_model_info.py             Halaman Info Model & Bobot
│
├── models/                         ← OTAK AI (Hasil Training dari Colab)
│   ├── jakarta/
│   │   ├── model_rf.pkl               Random Forest model
│   │   ├── model_lr.pkl               Linear Regression model
│   │   ├── model_nn.h5                Neural Network model
│   │   ├── scaler.pkl                 StandardScaler (normalisasi)
│   │   ├── encoders.pkl               LabelEncoder (teks→angka)
│   │   └── metadata.pkl               Info model (R2, fitur, schema)
│   ├── surabaya/
│   │   └── (sama seperti jakarta)
│   └── lumajang/
│       └── (sama seperti jakarta)
│
├── dataset/                        ← DATA MENTAH
│   ├── jakarta/
│   │   └── DATA_RUMAH.csv             1011 data rumah Jakarta
│   ├── surabaya/
│   │   └── Dataset rumah123 CLEAN.csv 11497 data rumah Surabaya
│   └── lumajang/
│       └── DATA_RUMAH_LUMAJANG_DEEP.csv 91 data rumah Lumajang
│
├── notebook/                       ← NOTEBOOK COLAB (Training)
│   ├── Training_Jakarta.ipynb         Pipeline training Jakarta
│   ├── Training_Surabaya.ipynb        Pipeline training Surabaya
│   └── Training_Lumajang.ipynb        Pipeline training Lumajang
│
└── penjelasan/                     ← DOKUMENTASI (Anda sedang membacanya!)
    ├── 01_GAMBARAN_UMUM_PROJECT.md
    ├── 02_STRUKTUR_FOLDER.md
    ├── 03_PENJELASAN_KODE_BACKEND.md
    ├── 04_PENJELASAN_KODE_FRONTEND.md
    ├── 05_PENJELASAN_NOTEBOOK.md
    ├── 06_PENJELASAN_DATASET.md
    └── 07_CARA_MENJALANKAN.md
```

## Alur Data dalam Sistem

```text
  [Dataset CSV]
       │
       ▼
  [Notebook Colab]  →  Training  →  Export .pkl/.h5
       │
       ▼
  [Folder models/]  ←  Upload dari Colab (file ZIP)
       │
       ▼
  [app.py]  →  model_loader.py  →  Load .pkl/.h5 ke RAM
       │
       ▼
  [User klik "Prediksi"]
       │
       ▼
  [page_predict.py]  →  data_preprocessing.py  →  predictor.py
       │
       ▼
  [Hasil: "Rp 2.5 Miliar"]
```
