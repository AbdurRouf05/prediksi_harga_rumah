# Penjelasan Kode Frontend (Folder frontend)

Folder `frontend/` berisi **tampilan web** yang dilihat pengguna di browser.
Menggunakan Streamlit sebagai framework.

## 1. styles.py — CSS Styling

### Apa Tugasnya

Menyuntikkan CSS kustom ke dalam halaman Streamlit agar tampilannya terlihat 
premium dan modern (bukan tampilan default Streamlit yang polos).

Elemen-elemen yang di-style:
- **KPI Card:** Kotak dengan bayangan dan gradien untuk menampilkan angka statistik
- **Title Gradient:** Judul halaman dengan efek gradient warna biru-hijau
- **Info Box:** Kotak penjelasan dengan border biru
- **Metric Card:** Card untuk menampilkan skor model

## 2. page_predict.py — Halaman Prediksi Harga

### Tugas Halaman Prediksi

Menampilkan form input dan hasil prediksi harga rumah.

### Alur Kerja Halaman Prediksi

```text
1. Ambil schema dari metadata model
2. Render form input secara DINAMIS:
   - Fitur numerik → st.number_input()
   - Fitur kategorikal → st.selectbox() dengan pilihan dari LabelEncoder
3. Saat tombol "Prediksi" ditekan:
   - Kumpulkan input ke dictionary
   - Panggil predictor.predict_price()
   - Tampilkan hasil dengan format rupiah yang cantik
   - Tampilkan perbandingan 3 model dalam bar chart
```

### Kenapa Form-nya Dinamis

Karena setiap kota memiliki fitur yang BERBEDA:
- Jakarta: LB, LT, KT, KM, GRS (5 fitur)
- Surabaya: Luas Tanah, Luas Bangunan, Kamar, Sertifikat, dll (8 fitur)
- Lumajang: Luas Tanah, Luas Bangunan, Sertifikat, Daya Listrik, dll (6 fitur)

System membaca `metadata.pkl` → `schema` untuk tahu fitur apa saja yang perlu 
ditampilkan. Jadi tidak perlu coding ulang halaman untuk setiap kota baru!

## 3. page_explore.py — Halaman Eksplorasi Data (EDA)

### Tugas Halaman Eksplorasi

Menampilkan visualisasi interaktif dari dataset asli setiap kota.

### Visualisasi yang Ditampilkan

1. **Informasi Dataset:** Jumlah baris, kolom, missing values, outlier
2. **Pratinjau Data:** Tabel 10 baris pertama
3. **Feature Selection:** Perbandingan fitur berguna vs tidak berguna
4. **Tab Distribusi Harga:** Histogram harga rumah
5. **Tab Korelasi:** Scatter plot + Heatmap korelasi antar fitur numerik
6. **Tab Outlier:** Box plot dengan statistik IQR (Q1, Q3, Batas)
7. **Tab Kategorikal:** Bar chart distribusi fitur non-angka

### Load Dataset

Fungsi `load_dataset()` mencari file CSV di folder `dataset/<kota>/`.
Urutan pencarian:
1. `DATA_RUMAH_FULL.csv`
2. `DATA_RUMAH.csv`
3. `DATA_RUMAH_LUMAJANG_DEEP.csv`
4. `DATA_RUMAH.xlsx` (fallback)

## 4. page_model_info.py — Halaman Info Model dan Bobot

### Tugas Halaman Info Model

Menampilkan "jeroan" model ML yang sudah dilatih.
Halaman ini sangat penting untuk **presentasi/sidang** karena menunjukkan 
bahwa Anda benar-benar memahami apa yang terjadi di balik layar.

### Informasi yang Ditampilkan

1. **Statistik Pelatihan:**
   - Jumlah data training vs testing
   - Data yang dihapus karena outlier
   - Model terbaik dan skor R2

2. **Perbandingan 3 Model:**
   - Bar chart skor R2 untuk RF, LR, dan NN
   - Rekomendasi model mana yang terbaik

3. **Feature Importance (Random Forest):**
   - Grafik batang horizontal yang menunjukkan fitur mana yang 
     paling berpengaruh terhadap harga rumah
   - Misal: Luas Tanah = 45%, Luas Bangunan = 30%, Kamar = 10%

4. **Koefisien Linear Regression:**
   - Menunjukkan seberapa besar perubahan harga jika fitur naik 1 satuan
   - Koefisien positif = fitur membuat harga naik
   - Koefisien negatif = fitur membuat harga turun

5. **Arsitektur Neural Network:**
   - Diagram layer: Input → 128 → 64 → 32 → 1
   - Jumlah parameter yang dipelajari
   - Activation function yang digunakan

## 5. app.py — Entry Point Utama

### Tugas Entry Point

File utama yang "menggabungkan" semua komponen.

### Alur Eksekusi

```python
1. st.set_page_config()           # Konfigurasi judul & layout
2. inject_css()                   # Suntik CSS dari styles.py
3. Sidebar:
   - Tampilkan logo & judul
   - Radio button pilih kota (Jakarta/Surabaya/Lumajang)
   - Status model (aktif/belum)
   - Menu navigasi (Prediksi/EDA/Model Info)
4. Load model:
   - Jika kota berubah → load ulang model dari folder
   - Simpan di st.session_state agar tidak load berulang
5. Render halaman sesuai menu yang dipilih
```

### Session State

Streamlit me-re-run SELURUH kode setiap kali ada interaksi (klik tombol, 
pindah halaman, dll). Untuk menghindari load model berulang kali, 
kita menyimpan model di `st.session_state` (memori browser).
