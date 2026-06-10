# 📚 ISTILAH-ISTILAH PENTING (GLOSARIUM)

Panduan cepat istilah-istilah yang mungkin ditanyakan dosen saat sidang/presentasi.


## Machine Learning

| Istilah | Penjelasan Sederhana |
|---------|---------------------|
| **Machine Learning** | Komputer yang belajar dari data, bukan diprogram manual |
| **Training** | Proses komputer "belajar" dari data historis |
| **Testing** | Ujian bagi model menggunakan data yang belum pernah dilihat |
| **Model** | "Otak" AI yang sudah belajar dan bisa menebak |
| **Prediksi** | Tebakan model terhadap data baru |
| **Overfitting** | Model terlalu menghafal data training, buruk di data baru |
| **Underfitting** | Model terlalu bodoh, tidak bisa menangkap pola |


## Data Science

| Istilah | Penjelasan Sederhana |
|---------|---------------------|
| **Dataset** | Kumpulan data dalam bentuk tabel (baris × kolom) |
| **Fitur (Feature)** | Kolom yang menjadi input (misal: Luas Tanah) |
| **Target** | Kolom yang ingin diprediksi (Harga) |
| **EDA** | Exploratory Data Analysis — melihat pola data lewat grafik |
| **Data Cleaning** | Membersihkan data kotor (kosong, format salah) |
| **Feature Selection** | Memilih fitur yang berguna, membuang yang noise |
| **Outlier** | Data yang jauh menyimpang dari rata-rata (anomali) |
| **IQR** | Interquartile Range — metode deteksi outlier menggunakan Q1 dan Q3 |
| **Missing Value** | Data yang kosong/hilang dalam dataset |
| **Encoding** | Mengubah teks menjadi angka (misal: "SHM" → 2) |
| **Scaling** | Menyamakan skala angka agar model tidak bias |


## Metrik & Evaluasi

| Istilah | Penjelasan Sederhana |
|---------|---------------------|
| **R² (R-Squared)** | Skor 0-1 yang mengukur seberapa bagus model. 1 = sempurna |
| **MAE** | Mean Absolute Error — rata-rata selisih prediksi vs aktual |
| **MSE** | Mean Squared Error — seperti MAE tapi lebih sensitif ke error besar |
| **Feature Importance** | Ranking fitur berdasarkan kontribusinya ke prediksi |
| **Koefisien** | Bobot fitur di Linear Regression (+ = naikkan harga, - = turunkan) |


## Algoritma

| Istilah | Penjelasan Sederhana |
|---------|---------------------|
| **Linear Regression** | Cari garis lurus terbaik yang menghubungkan fitur ke target |
| **Random Forest** | 100 pohon keputusan yang voting bersama (akurat tapi lambat) |
| **Neural Network** | Jaringan neuron buatan yang meniru otak manusia |
| **Decision Tree** | Pohon keputusan: "Jika LT > 200 DAN KT > 3, maka harga..." |
| **Ensemble** | Gabungan banyak model kecil menjadi 1 model besar (Random Forest) |
| **Deep Learning** | Neural Network dengan banyak layer (lebih dalam = lebih pintar) |
| **Activation Function** | Fungsi di neuron yang menentukan apakah sinyal diteruskan |
| **Dropout** | Teknik "matikan" sebagian neuron saat training untuk cegah overfitting |


## Teknologi

| Istilah | Penjelasan Sederhana |
|---------|---------------------|
| **Streamlit** | Framework Python untuk membuat website/dashboard tanpa HTML/CSS |
| **Selenium** | Library untuk mengendalikan browser (Chrome) secara otomatis |
| **Scikit-Learn** | Library Python untuk Machine Learning (RF, LR, Scaler) |
| **TensorFlow/Keras** | Library untuk Deep Learning (Neural Network) |
| **Pandas** | Library Python untuk mengolah data tabel |
| **Plotly** | Library untuk grafik interaktif (bisa di-hover, zoom) |
| **Google Colab** | Jupyter Notebook gratis di cloud milik Google |
| **Web Scraping** | Teknik mengambil data dari website secara otomatis |
| **ChromeDriver** | Penghubung antara Selenium dan browser Chrome |
| **Joblib** | Library untuk menyimpan/memuat objek Python (model, scaler) |
| **StandardScaler** | Mengubah data agar mean=0 dan std=1 (normalisasi) |
| **LabelEncoder** | Mengubah teks kategori ke angka berurutan (0, 1, 2, ...) |


## Contoh Jawaban Sidang

**"Kenapa pakai Random Forest?"**
> "Karena Random Forest unggul dalam menangkap pola non-linear. 
> Harga rumah tidak selalu naik secara garis lurus — ada interaksi 
> antar fitur yang kompleks. RF juga memberikan Feature Importance 
> sehingga kita bisa tahu fitur mana yang paling berpengaruh."

**"Kenapa fitur X dibuang?"**
> "Karena setelah analisis, kolom tersebut memiliki [X]% data kosong. 
> Memasukkan kolom dengan banyak missing value akan merusak kualitas 
> prediksi model. Prinsip Garbage In = Garbage Out."

**"Kenapa data Lumajang sedikit?"**
> "Lumajang adalah kota kecil dengan listing properti online yang 
> terbatas. Ini adalah limitasi dari penelitian ini. Namun, kami 
> menunjukkan bahwa pipeline yang kami bangun bersifat scalable — 
> bisa diterapkan ke kota manapun selama ada datanya."
