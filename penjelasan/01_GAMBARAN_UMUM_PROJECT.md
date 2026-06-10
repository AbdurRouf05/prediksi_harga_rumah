# Gambaran Umum Project

## Apa Itu Project Ini

Project ini adalah sebuah **aplikasi web berbasis Machine Learning** yang mampu
**memprediksi harga rumah** di 3 kota: **Jakarta**, **Surabaya**, dan **Lumajang**.

Bayangkan Anda ingin membeli rumah. Anda tahu luas tanahnya 150m2, ada 3 kamar tidur,
2 kamar mandi, dan sertifikatnya SHM. Berapa kira-kira harganya?

**Itulah yang dijawab oleh aplikasi ini!**

Komputer "belajar" dari ratusan/ribuan data rumah yang sudah dijual sebelumnya,
lalu menggunakan pola yang dipelajari untuk menebak harga rumah baru.

## Teknologi yang Digunakan

| Komponen | Teknologi | Fungsi |
| --- | --- | --- |
| Bahasa | Python 3 | Bahasa utama |
| Web Framework | Streamlit | Membuat dashboard interaktif |
| Machine Learning | Scikit-Learn | Random Forest dan Linear Regression |
| Deep Learning | TensorFlow/Keras | Neural Network |
| Visualisasi | Plotly, Matplotlib, Seaborn | Grafik interaktif |
| Data | Pandas, NumPy | Olah data tabular |
| Scraping | Selenium | Mengambil data dari website properti |
| Training | Google Colab | Melatih model di cloud gratis |

## Alur Kerja Project (End-to-End Pipeline)

```text
PENGUMPULAN DATA --> PEMBERSIHAN DATA --> EKSPLORASI DATA (EDA)
(Scraping/CSV)      (Data Cleaning)      (Visualisasi)
                                              |
                                              v
DEPLOYMENT      <-- EVALUASI          <-- TRAINING MODEL
(Website/App)       (Skor R2, MAE)        (RF, LR, NN)
(Streamlit)         Feature Importance
```

### Penjelasan Setiap Tahap

1. **Pengumpulan Data:** Data rumah diambil dari website properti (rumah123.com)
   menggunakan web scraping (Selenium), atau dari dataset CSV yang sudah tersedia.

2. **Pembersihan Data (Data Cleaning):** Data mentah biasanya kotor (ada kolom kosong,
   format tidak konsisten, teks tercampur angka). Tahap ini membersihkan semuanya.

3. **Eksplorasi Data (EDA):** Kita memvisualisasikan data menggunakan grafik
   (histogram, heatmap, scatter plot) untuk memahami pola dan distribusi.

4. **Training Model:** Data yang sudah bersih dimasukkan ke 3 algoritma ML.
   Komputer "belajar" pola dari data ini. Hasilnya disimpan ke file .pkl dan .h5.

5. **Evaluasi:** Kita menguji keakuratan model menggunakan data yang tidak pernah
   dilihat model sebelumnya (test set). Skor R2 mendekati 1.0 artinya sangat bagus.

6. **Deployment:** Model yang sudah pintar di-deploy ke website Streamlit agar
   pengguna bisa langsung memprediksi harga rumah lewat browser.

## Algoritma Machine Learning yang Digunakan

### 1. Linear Regression

Model paling sederhana. Ia berasumsi bahwa harga rumah memiliki hubungan linear
(garis lurus) dengan fitur-fiturnya.

- Kelebihan: Cepat, mudah diintepretasi.
- Kekurangan: Tidak bisa menangkap hubungan non-linear (kurva).

### 2. Random Forest

Kumpulan dari ratusan Decision Tree (pohon keputusan) yang memilih keputusan
secara bersama-sama (voting). Ini seperti bertanya ke 100 orang ahli lalu
mengambil jawaban mayoritas.

- Kelebihan: Sangat akurat, tahan terhadap overfitting, bisa menunjukkan
  fitur mana yang paling penting (Feature Importance).
- Kekurangan: Lebih lambat dari Linear Regression.

### 3. Neural Network (Deep Learning)

Meniru cara kerja otak manusia dengan lapisan-lapisan neuron buatan.
Arsitektur yang digunakan: 128 lalu 64 lalu 32 lalu 1 neuron.

- Kelebihan: Bisa menangkap pola yang sangat kompleks.
- Kekurangan: Butuh data banyak, sulit diintepretasi ("black box").

## Metrik Evaluasi

### R2 Score (R-Squared / Koefisien Determinasi)

- Mengukur seberapa baik model menjelaskan variasi data.
- R2 = 1.000 berarti Prediksi sempurna (mustahil di dunia nyata).
- R2 = 0.800 berarti Model menjelaskan 80% variasi harga (bagus).
- R2 = 0.000 berarti Model tidak berguna sama sekali.

### MAE (Mean Absolute Error)

- Rata-rata selisih antara harga prediksi dan harga asli.
- Semakin kecil nilainya, semakin baik modelnya.
