# LAPORAN PROYEK AKHIR: SISTEM PREDIKSI HARGA RUMAH BERBASIS MACHINE LEARNING

---

## BAB 1: PENDAHULUAN

### 1.1 Latar Belakang
Menentukan harga jual atau beli sebuah properti (rumah) sering kali menjadi proses yang rumit dan sangat subjektif. Tanpa pemahaman mendalam tentang harga pasar, penjual berisiko menjual rumahnya terlalu murah, sementara pembeli berisiko membeli dengan harga yang terlalu mahal. Penilaian harga rumah yang dilakukan secara manual biasanya dipengaruhi oleh emosi atau perkiraan kasar yang tidak selalu mencerminkan nilai wajar dari spesifikasi fisik rumah tersebut.

Di era digital, data harga rumah sebenarnya sangat berlimpah di internet. Dengan memanfaatkan teknologi *Machine Learning* (Kecerdasan Buatan), kita dapat membuat sistem yang mampu mengenali pola dari ribuan data historis harga rumah, dan menggunakannya untuk memberikan estimasi harga yang lebih objektif, adil, dan berbasis data (*data-driven*).

### 1.2 Tujuan
Proyek ini bertujuan untuk membangun sebuah sistem prediksi harga rumah menggunakan *Machine Learning* yang dapat mengestimasi harga berdasarkan spesifikasi fisik bangunan. Sistem ini dirancang untuk memprediksi harga rumah di tiga area spesifik, yaitu: **Jakarta**, **Surabaya**, dan **Lumajang**. Selain membangun model prediksi, proyek ini juga bertujuan untuk mengimplementasikan model tersebut ke dalam sebuah *dashboard* antarmuka (website) interaktif agar mudah digunakan oleh masyarakat awam.

### 1.3 Batasan Masalah
Untuk menjaga fokus pengembangan, proyek ini dibatasi pada spesifikasi fisik utama. Model hanya berlaku secara akurat pada rentang harga normal yang ada di dalam dataset (bukan untuk rumah subsidi yang sangat murah atau rumah super mewah/istana).

---

## BAB 2: PENGUMPULAN & PENJELASAN DATASET

### 2.1 Sumber Data
1. **Data Sekunder (Jakarta & Surabaya):** Data untuk kota besar ini didapatkan melalui sumber *open source* di GitHub. Datanya sudah cukup rapi karena telah dikumpulkan oleh komunitas.
2. **Data Primer / Web Scraping (Lumajang):** Karena data properti kota kecil sangat langka, kami membangun *bot web scraper* menggunakan *library* Selenium untuk mengambil data langsung dari web Rumah123 secara otomatis.

**💡 Potongan Kode Scraping (`scraper_lumajang.py`):**
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

# 1. Menginisiasi browser otomatis (Bot)
driver = webdriver.Chrome()
driver.get("https://www.rumah123.com/jual/lumajang/rumah/")

# 2. Mencari semua kotak iklan rumah di halaman tersebut
listings = driver.find_elements(By.CSS_SELECTOR, ".ui-organism-intersection__element")
for listing in listings:
    # 3. Mengambil URL (link) untuk masing-masing rumah
    url = listing.find_element(By.TAG_NAME, "a").get_attribute("href")
    # Setelah dapat link-nya, bot akan masuk ke halaman tersebut untuk mencatat spesifikasinya
```
*Penjelasan:* Kode di atas bertugas membuka browser Google Chrome secara otomatis, mengetikkan alamat web properti area Lumajang, mencari semua kotak iklan rumah, lalu mencatat link satu per satu agar bot bisa membaca isi spesifikasi lengkapnya di halaman selanjutnya.

### 2.2 Penjelasan Fitur Dataset
Data rumah awal yang kami miliki berupa tabel (CSV) dengan berbagai macam kolom. Namun, tidak semua kolom digunakan. Berikut rinciannya:

*   **Fitur yang Dipakai (Variabel Prediktor):** `LB` (Luas Bangunan), `LT` (Luas Tanah), `KT` (Kamar Tidur), `KM` (Kamar Mandi), dan `GRS` (Garasi). Kelima fitur ini dipilih karena wujudnya berupa angka murni yang punya kaitan logis dan matematis terhadap harga fisik bangunan.
*   **Target Prediksi:** `HARGA` (Ini adalah nilai akhir yang ingin kita tebak).
*   **Fitur yang Dibuang beserta Alasannya:**
    1.  `NO` (Nomor Urut / ID): Dibuang karena hanya urutan tabel biasa. Jika tidak dibuang, sistem akan salah paham dan mengira rumah nomor urut 1 lebih murah daripada rumah nomor urut 1000.
    2.  `NAMA RUMAH` (Deskripsi Iklan, misal: *"Rumah Murah Hook Tebet"*): Dibuang karena berupa teks kalimat promosi yang tidak beraturan. Mengubah kalimat promosi ini menjadi angka akan sangat memperumit hitungan model, padahal intisari dari nilai rumah tersebut sesungguhnya sudah terwakili oleh kelima angka spesifikasi di atas.

### 2.3 Dataset Mana yang Paling Optimal?
Jika ditinjau dari sisi akurasi model, dataset untuk kota **Jakarta** adalah yang paling optimal dan cerdas dalam melakukan prediksi. Hal ini dikarenakan dataset Jakarta memiliki jumlah baris data riwayat rumah yang paling banyak (lebih dari 1.000 rumah) dan variasinya sangat kaya. 
Dalam *Machine Learning*, semakin banyak contoh kasus yang dipelajari dari dataset, maka algoritma akan semakin presisi. Sebaliknya, data Lumajang hasil *scraping* jumlahnya lebih terbatas, sehingga variasi pola prediksinya tidak sekompleks model Jakarta.

---

## BAB 3: PEMBERSIHAN DATA (*DATA PREPROCESSING*)

Data mentah, terutama hasil *scraping*, pasti banyak yang kotor (kosong atau salah ketik).

**💡 Potongan Kode Preprocessing (Notebook):**
```python
# 1. Menghapus Outlier (Data Pencilan tak masuk akal) dengan metode IQR
Q1 = df['HARGA'].quantile(0.25)
Q3 = df['HARGA'].quantile(0.75)
IQR = Q3 - Q1
# Membuang rumah yang harganya terlampau murah atau terlampau mahal secara tak wajar
df = df[~((df['HARGA'] < (Q1 - 1.5 * IQR)) | (df['HARGA'] > (Q3 + 1.5 * IQR)))]

# 2. Menyamakan Skala Angka (Scaling)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
# Luas Tanah/Bangunan distandarisasi agar tidak kalah dengan angka Harga
X_scaled = scaler.fit_transform(X)
```
*Penjelasan:* Jika ada rumah dengan luas 10m² tapi tertulis harganya 10 Miliar, itu sangat mungkin merupakan kesalahan ketik (Outlier). Kode pertama di atas bertugas membuang data-data pencilan tersebut agar mesin tidak ikut sesat saat menganalisis.
Kode kedua (Scaling) bertugas menyeragamkan skala angka. Sebagai contoh, Luas Tanah (misal: 150) jika disandingkan langsung dengan Harga (Rp 1.000.000.000) tanpa di-scale akan membuat mesin menganggap Harga jauh lebih dominan dalam perhitungan hanya karena nominal nol-nya banyak.

---

## BAB 4: PROSES NOTEBOOK DAN PEMBUATAN FILE MODEL (.pkl)

Proses pelatihan model dilakukan sepenuhnya di dalam lingkungan Jupyter Notebook / Google Colab.

**💡 Potongan Kode Training & Export .pkl (Notebook):**
```python
from sklearn.ensemble import RandomForestRegressor
import joblib

# 1. Melatih model dari data latih (Training)
rf_model = RandomForestRegressor(n_estimators=100)
rf_model.fit(X_train_scaled, y_train)

# 2. Menyimpan model yang sudah dilatih ke dalam file .pkl (Pickle)
joblib.dump(rf_model, 'models/jakarta/model_rf.pkl')
joblib.dump(scaler, 'models/jakarta/scaler.pkl')
```
*Penjelasan:*
*   Perintah `fit()` adalah instruksi utama di mana kita memberikan matriks fitur (`X_train`) dan target harga (`y_train`) agar mesin mencari pola hubungannya secara mandiri.
*   Setelah berhasil memetakan pola tersebut, algoritma harus disimpan agar tidak perlu dilakukan *training* ulang setiap kali aplikasi dijalankan. Perintah `joblib.dump()` bertugas mengekspor pemahaman mesin tersebut ke dalam sebuah file berakhiran `.pkl`. File ini ibarat *flashdisk* yang memuat sistem cerdas tersebut sehingga bisa langsung dihubungkan ke platform web.

---

## BAB 5: PEMODELAN MACHINE LEARNING

Dalam proyek ini, kami sengaja menggunakan dua algoritma yang berbeda secara bersamaan untuk melihat perbandingannya. Kami membutuhkan satu model dasar sebagai tolok ukur awal, dan satu model canggih sebagai solusi akhir.

### 5.1 Linear Regression (Model Dasar)
*   **Apa itu?** Ini adalah rumus matematika klasik yang menganggap bahwa pergerakan harga properti selalu berwujud "garis lurus" yang konstan.
*   **Analogi:** Seperti aturan kaku: *"Setiap 1 meter persegi, harganya pasti Rp 10 Juta"*. Jadi jika 10 meter adalah Rp 100 Juta, maka 100 meter pasti Rp 1 Miliar. 
*   **Kenapa Dipakai?** Kami menggunakannya sebagai *baseline* (tolok ukur paling dasar). Kami ingin melihat seberapa tinggi akurasi yang didapat jika fluktuasi harga rumah hanya ditebak memakai logika matematika linier sederhana.
*   **Kelemahan:** Di dunia nyata, harga rumah sangat dinamis. Rumah seluas 1000m² belum tentu harganya persis 10 kali lipat dari rumah 100m² (terdapat faktor nilai per kawasan dan *diminishing returns*). Sifat kaku "garis lurus" ini sering kali membuatnya gagal menebak pergerakan harga pasar yang rumit.

### 5.2 Random Forest (Model Andalan)
*   **Apa itu?** *Random Forest* adalah sekumpulan besar "Pohon Keputusan" (*Decision Trees*). Model ini tidak berpegang pada aturan garis lurus, melainkan memprediksi harga melalui ratusan rantai kondisi/syarat yang berbeda-beda.
*   **Analogi:** Daripada bertanya pada 1 orang penilai (seperti Linear Regression), model ini ibarat mengumpulkan **100 agen properti independen**.
    *   Agen 1 memprediksi: *"Luas di atas 100m² dan kamar ada 3? Estimasi Rp 1,2 Miliar."*
    *   Agen 2 memprediksi dari sudut pandang lain: *"Garasi muat 2 mobil dan Luas Tanah lebih besar dari Bangunan? Estimasi Rp 1,3 Miliar."*
    *   Hasil akhirnya adalah **nilai rata-rata** dari 100 tebakan agen tersebut.
*   **Kenapa Dipakai?** Keputusan yang diambil secara kolektif terbukti jauh lebih stabil dan akurat. Model ini sangat adaptif dan pintar dalam membaca pola harga properti yang bersifat non-linear (acak). Model ini menjadi algoritma utama yang diimplementasikan ke *dashboard* web karena keakuratannya yang superior.

---

## BAB 6: EVALUASI MODEL

Skor metrik statistik **R-Squared (R²)** digunakan untuk mengukur kinerja akurasi model regresi yang telah dibuat.

**💡 Potongan Kode Evaluasi (Notebook):**
```python
from sklearn.metrics import r2_score

# 1. Memerintahkan model menebak data uji (data yang belum pernah ia lihat)
y_prediksi = rf_model.predict(X_test_scaled)

# 2. Menghitung kecocokan tebakan mesin (y_prediksi) dengan harga riil (y_test)
akurasi = r2_score(y_test, y_prediksi)
print(f"Skor Akurasi R-Squared: {akurasi * 100}%")
```
*Penjelasan:* Perintah `r2_score` berfungsi untuk membandingkan seberapa presisi angka tebakan model terhadap data riil pasar. 
Jika didapatkan skor R² sebesar **78%**, ini berarti sistem kita berhasil mengidentifikasi dan memetakan 78% faktor yang membuat harga rumah tersebut naik atau turun (hanya dengan bermodalkan data luas dan kamar). Sisa deviasi 22% terjadi karena adanya pengaruh dari faktor eksternal di luar dataset (contoh: renovasi arsitektur, kelayakan struktur atap, atau lokasi spesifik di suatu perumahan). Akurasi di atas 70% sudah tergolong sangat ideal untuk estimasi harga berbasis dimensi fisik semata.

---

## BAB 7: IMPLEMENTASI DASHBOARD WEB (STREAMLIT)

Bagaimana aplikasi web bisa terhubung dengan sistem prediktor secara instan? Jawabannya ada pada metode pemanggilan file `.pkl`.

### 7.1 Proses Memanggil (Load) Model .pkl
**💡 Potongan Kode Load Model (`engine/model_loader.py`):**
```python
import joblib
import os

def load_all_models(kota, models_dir):
    # Mengarah ke jalur direktori tempat file model (pkl) tersimpan
    rf_path = os.path.join(models_dir, 'model_rf.pkl')
    
    # Memuat algoritma kembali ke dalam memori komputer
    result = {}
    result['model_rf'] = joblib.load(rf_path)
    return result
```
*Penjelasan:* Aplikasi web didesain agar tidak perlu melakukan proses *training* ulang yang memakan waktu berjam-jam. Server web cukup mengeksekusi file `.pkl` (`joblib.load()`) ke dalam memorinya sekali saja saat dijalankan. Hal ini membuat aplikasi bersifat ringan dan mampu merespons kalkulasi dalam hitungan milidetik.

### 7.2 Proses Melakukan Prediksi
**💡 Potongan Kode Prediksi (`engine/predictor.py`):**
```python
def predict_price(input_data, models, model_key):
    model = models['model_rf']
    scaler = models['scaler']
    
    # 1. Menyamakan skala angka dari inputan pengguna
    input_scaled = scaler.transform(input_df)
    
    # 2. Mesin melakukan eksekusi prediksi dan mengeluarkan output harga
    harga = model.predict(input_scaled)[0]
    
    return harga
```
*Penjelasan:* Sewaktu pengguna mengisi kolom Luas (misalnya 150) dan menekan tombol prediksi, data 150 tersebut langsung dinormalisasi ukurannya terlebih dahulu (`transform`), untuk kemudian diumpankan kepada algoritma prediksi (`predict()`) yang seketika itu juga mengembalikan angka akhir.

### 7.3 Tampilan (User Interface) Dashboard
*(Tambahkan Screenshot Web Anda di bawah ini)*
> *Catatan: Anda bisa menempelkan Screenshot Dashboard Web Streamlit Anda yang menunjukkan Halaman Input Spesifikasi dan Halaman Grafik Eksplorasi Data di posisi ini untuk melengkapi dokumentasi laporan Anda.*

<div align="center">
    <img src="https://via.placeholder.com/800x400.png?text=+-+SCREENSHOT+DASHBOARD+PREDIKSI+ANDA+DISINI+-+" alt="Screenshot Dashboard Streamlit">
    <br>
    <i>Gambar 1: Tampilan Dashboard Prediksi Harga Rumah berbasis Streamlit.</i>
</div>

---

## BAB 8: KESIMPULAN DAN SARAN

Sistem prediktor terbukti mampu memberikan estimasi harga wajar sebuah properti secara otomatis dan *data-driven*. Penggunaan algoritma Random Forest, dibantu tahapan pembersihan pencilan (outlier), menghasilkan tingkat akurasi (R²) yang memuaskan. Ke depannya, akurasi sistem masih bisa diimprovisasi dengan menyuntikkan fitur tambahan seperti data titik koordinat (GPS) secara detail serta pengaplikasian *Computer Vision* untuk menilai tingkat kemewahan desain bangunan melalui citra visual (foto).
