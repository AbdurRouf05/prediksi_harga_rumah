# 🏡 Prediksi Harga Rumah (Jakarta, Surabaya, Lumajang)

Aplikasi web berbasis Machine Learning untuk memprediksi harga rumah di 3 kota: Jakarta, Surabaya, dan Lumajang. Aplikasi ini menggunakan data historis properti untuk melatih model dan memberikan estimasi harga berdasarkan spesifikasi rumah (luas tanah, jumlah kamar, dll).

## 🚀 Fitur Utama

- **Prediksi Harga Cepat**: Dapatkan estimasi harga rumah hanya dengan memasukkan beberapa spesifikasi (luas tanah, kamar tidur, kamar mandi, sertifikat, dll).
- **Tiga Kota Tersedia**: Mendukung prediksi untuk wilayah Jakarta, Surabaya, dan Lumajang.
- **Multiple Models**: Menggunakan 3 algoritma Machine Learning terbaik:
  - **Random Forest** (Akurasi Tinggi, Feature Importance)
  - **Linear Regression** (Sederhana, Cepat)
  - **Neural Network / Deep Learning** (Menangkap pola kompleks)
- **Dashboard Interaktif**: Dibangun menggunakan Streamlit untuk antarmuka yang bersih dan mudah digunakan.
- **Visualisasi Data (EDA)**: Lihat langsung grafik dan sebaran data dari dataset yang digunakan.
- **Web Scraper Bawaan**: Dilengkapi dengan bot Selenium untuk mengambil data rumah secara otomatis dari Rumah123.

## 🛠️ Teknologi yang Digunakan

- **Bahasa Utama**: Python 3
- **Web Framework**: Streamlit
- **Machine Learning**: Scikit-Learn, TensorFlow/Keras
- **Data Processing**: Pandas, NumPy
- **Visualisasi**: Plotly, Matplotlib, Seaborn
- **Web Scraping**: Selenium

## 📂 Struktur Direktori Utama

- `app.py`: File utama untuk menjalankan dashboard Streamlit.
- `scraper_lumajang.py`: Script bot Selenium untuk mengambil data rumah area Lumajang.
- `dataset/`: Berisi dataset mentah dan bersih untuk masing-masing kota.
- `notebook/`: Berisi Jupyter Notebook untuk proses pembersihan data, eksplorasi (EDA), dan pelatihan model di Google Colab.
- `models/`: Folder untuk menyimpan hasil model yang sudah dilatih (`.pkl` dan `.h5`).
- `penjelasan/`: Dokumentasi lengkap mengenai struktur folder, cara kerja frontend/backend, dataset, dll.

## ⚙️ Cara Menjalankan Project

### 1. Prasyarat
- Python 3.8+
- (Opsional) Google Chrome & ChromeDriver jika ingin menjalankan scraper.

### 2. Instalasi
Buka terminal di folder project dan jalankan:
```bash
pip install -r requirements.txt
```

### 3. Menjalankan Dashboard
```bash
streamlit run app.py
```
Website akan terbuka secara otomatis di `http://localhost:8501`.

*(Catatan: Pastikan model `.pkl` dan `.h5` sudah ada di folder `models/`. Jika belum, Anda harus melatih model menggunakan notebook yang disediakan.)*

## 📚 Penjelasan Lengkap (Dokumentasi)

Jika Anda ingin memahami project ini lebih dalam, silakan baca dokumentasi di folder `penjelasan/`:
- [01. Gambaran Umum Project](penjelasan/01_GAMBARAN_UMUM_PROJECT.md)
- [02. Struktur Folder](penjelasan/02_STRUKTUR_FOLDER.md)
- [03. Penjelasan Kode Backend](penjelasan/03_PENJELASAN_KODE_BACKEND.md)
- [04. Penjelasan Kode Frontend](penjelasan/04_PENJELASAN_KODE_FRONTEND.md)
- [05. Penjelasan Notebook](penjelasan/05_PENJELASAN_NOTEBOOK.md)
- [06. Penjelasan Dataset](penjelasan/06_PENJELASAN_DATASET.md)
- [07. Cara Menjalankan](penjelasan/07_CARA_MENJALANKAN.md)
- [08. Penjelasan Scraper](penjelasan/08_PENJELASAN_SCRAPER.md)
- [09. Glosarium & Tips Sidang](penjelasan/09_GLOSARIUM_DAN_TIPS_SIDANG.md)
