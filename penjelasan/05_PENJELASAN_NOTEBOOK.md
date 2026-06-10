# Penjelasan Notebook Training

Setiap kota memiliki 1 file `.ipynb` (Jupyter Notebook) yang dijalankan di **Google Colab**. Struktur ketiga notebook IDENTIK, hanya berbeda di:

- Nama file dataset yang di-upload
- Kolom yang dibuang (berbeda tiap kota)
- Parsing harga (Lumajang perlu dikonversi dari teks)

## Struktur Umum Setiap Notebook (9 Tahap)

### Tahap 1: Import Library

Memanggil semua library yang dibutuhkan:

- `pandas` (olah data tabel)
- `numpy` (matematika)
- `matplotlib` + `seaborn` (grafik)
- `scikit-learn` (ML: RF, LR, Scaler, LabelEncoder)
- `tensorflow.keras` (Neural Network)
- `google.colab.files` (upload/download file di Colab)

### Tahap 2: Upload Dataset

Mengunggah file CSV dari komputer ke Colab.

### Tahap 3: Data Cleaning

- Menghapus kolom identitas (NO, Link, IMG Link, ID Iklan)
- Mengisi nilai kosong ("-") dengan "Tidak Diketahui"
- Mengubah tipe data yang salah (teks → angka)

### Tahap 4: EDA (Exploratory Data Analysis)

- Histogram distribusi harga
- Heatmap korelasi antar fitur numerik

### Tahap 5: Feature Selection (Seleksi Fitur)

Membuang kolom yang TIDAK BERGUNA.
**(Sudah diisi otomatis, tidak perlu diubah!)**

### Tahap 6: Hapus Outlier & Encoding

- **Outlier:** Data ekstrem dihapus pakai rumus IQR
- **Label Encoding:** Teks seperti "SHM" diubah ke angka (0, 1, 2)

### Tahap 7: Training Model

- Split data 80% training : 20% testing
- StandardScaler untuk normalisasi
- Latih 3 model (RF, LR, NN)

### Tahap 8: Evaluasi

- Scatter plot Prediksi vs Aktual
- Bar chart Feature Importance

### Tahap 9: Export

- Simpan semua model ke folder
- Bungkus jadi ZIP dan download otomatis

## Detail Per Kota

### Training_Jakarta.ipynb

**Dataset:** `DATA_RUMAH.csv` (1011 baris, 8 kolom)
**Target:** Kolom `HARGA`

**Kolom yang dibuang di Cleaning:** `NO`
**Kolom yang dibuang di Feature Selection:** `NAMA RUMAH`

**Fitur yang dipakai model (5 fitur):**

| Fitur | Tipe | Penjelasan |
| --- | --- | --- |
| LB | Numerik | Luas Bangunan (m2) |
| LT | Numerik | Luas Tanah (m2) |
| KT | Numerik | Jumlah Kamar Tidur |
| KM | Numerik | Jumlah Kamar Mandi |
| GRS | Numerik | Jumlah Garasi |

### Training_Surabaya.ipynb

**Dataset:** `Dataset rumah123 CLEAN.csv` (11497 baris, 21 kolom)
**Target:** Kolom `Harga`

**Kolom yang dibuang di Cleaning (4 kolom identitas):**

| Kolom | Alasan Dibuang |
| --- | --- |
| index | Nomor urut |
| Link | URL iklan (unik per baris, bukan spesifikasi rumah) |
| IMG Link | URL gambar (bukan spesifikasi rumah) |
| ID Iklan | Kode unik iklan |

**Kolom yang dibuang di Feature Selection (8 kolom noise):**

| Kolom | Alasan | Persentase Kosong |
| --- | --- | --- |
| Alamat | Hanya 7 nilai unik, terlalu sedikit variasi | 0% tapi tidak informatif |
| Tipe Properti | Isinya 100% "Rumah", tidak ada variasi | 0% tapi hanya 1 nilai |
| Kondisi Properti | 66% berisi "-" | 66% kosong |
| Dilengkapi Perabotan | 76% berisi "-" | 76% kosong |
| Hadap | 80% berisi "-" | 80% kosong |
| Carport | 91% berisi "-" | 91% kosong |
| Umur Bangunan | 50% berisi "-" | 50% kosong |
| Kamar Pembantu | 61% berisi "-" | 61% kosong |

**Fitur yang dipakai model (8 fitur):**

| Fitur | Tipe | Penjelasan |
| --- | --- | --- |
| Luas Tanah | Numerik | Luas tanah dalam m2 |
| Luas Bangunan | Numerik | Luas bangunan dalam m2 |
| Kamar | Numerik | Jumlah kamar tidur |
| Kamar Mandi | Numerik | Jumlah kamar mandi |
| Sertifikat | Kategorikal | SHM / HGB / PPJB / dll |
| Jumlah Lantai | Numerik | 1, 2, 3 lantai |
| Daya Listrik | Kategorikal | 900, 1300, 2200 Watt |
| Garasi | Numerik | Jumlah slot garasi |

### Training_Lumajang.ipynb

**Dataset:** `DATA_RUMAH_LUMAJANG_DEEP.csv` (91 baris, 17 kolom)
**Target:** Kolom `Harga`

**Proses Khusus Lumajang:**

- Harga berformat teks ("RP 2,85 MILIAR") → harus dikonversi ke angka
- Luas berformat "430 M2" → harus dihapus satuan "M2"-nya
- Kamar Tidur/Mandi berformat teks → harus dikonversi ke angka

**Kolom yang dibuang di Cleaning:** `Link`

**Kolom yang dibuang di Feature Selection (9 kolom noise):**

| Kolom | Alasan | Persentase Kosong |
| --- | --- | --- |
| Lokasi | Hampir semuanya "Lumajang" (2 nilai) | 0% tapi tidak informatif |
| Tipe Properti | 85% berisi "-" | 85% kosong |
| Kondisi Properti | 100% berisi "-" | 100% KOSONG! |
| Dilengkapi Perabotan | 100% berisi "-" | 100% KOSONG! |
| Kamar Pembantu | 100% berisi "-" | 100% KOSONG! |
| Hadap | 100% berisi "-" | 100% KOSONG! |
| Garasi | 91% berisi "-" | 91% kosong |
| Carport | 84% berisi "-" | 84% kosong |
| Jumlah Lantai | 48% berisi "-" | 48% kosong |

**Fitur yang dipakai model (6 fitur):**

| Fitur | Tipe | Penjelasan |
| --- | --- | --- |
| Luas Tanah | Numerik | Luas tanah dalam m2 |
| Luas Bangunan | Numerik | Luas bangunan dalam m2 |
| Kamar Tidur | Numerik | Jumlah kamar tidur |
| Kamar Mandi | Numerik | Jumlah kamar mandi |
| Sertifikat | Kategorikal | SHM / HGB |
| Daya Listrik | Kategorikal | 900Watt, 1300Watt, dll |

## Kenapa Fitur Tertentu Dibuang

### Prinsip Utama

Ketika seseorang mencari rumah, mereka bertanya:

- "Berapa **luas** tanahnya?" ✅ → Dipakai
- "Ada **berapa kamar**?" ✅ → Dipakai
- "**Sertifikat**-nya apa?" ✅ → Dipakai
- "**Daya listrik**-nya berapa?" ✅ → Dipakai

Mereka **TIDAK** bertanya:

- "Berapa **ID iklan**-nya?" ❌ → Dibuang
- "Apa **link URL** iklannya?" ❌ → Dibuang
- "Apa **URL gambar**-nya?" ❌ → Dibuang
- "**Nomor urut** datanya berapa?" ❌ → Dibuang

### Prinsip Kelengkapan Data

- Jika lebih dari 50% baris kosong ("-"), kolom tersebut DIBUANG
- Karena mengisi "-" dengan tebakan akan merusak pola data asli
- Lebih baik hilangkan daripada mengotori model
