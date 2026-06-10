# 📊 PENJELASAN DATASET

## Sumber Data

| Kota | Sumber | Metode | Jumlah Data |
|------|--------|--------|-------------|
| Jakarta | Dataset akademik | CSV langsung | 1.011 rumah |
| Surabaya | rumah123.com | Scraping (sudah di-clean) | 11.497 rumah |
| Lumajang | rumah123.com | Deep Scraping (Selenium) | 91 rumah |


---

## Jakarta: `DATA_RUMAH.csv`

**Jumlah:** 1.011 baris × 8 kolom
**Kondisi:** Sangat bersih. Semua data lengkap, tidak ada yang kosong.

| Kolom | Tipe | Contoh | Deskripsi |
|-------|------|--------|-----------|
| NO | int | 1 | Nomor urut (DIBUANG) |
| NAMA RUMAH | text | "Rumah Mewah di Tebet..." | Nama iklan (DIBUANG) |
| HARGA | int | 3800000000 | Harga rumah (TARGET) |
| LB | int | 220 | Luas Bangunan dalam m² |
| LT | int | 220 | Luas Tanah dalam m² |
| KT | int | 3 | Jumlah Kamar Tidur |
| KM | int | 3 | Jumlah Kamar Mandi |
| GRS | int | 0 | Jumlah Garasi |


---

## Surabaya: `Dataset rumah123 CLEAN.csv`

**Jumlah:** 11.497 baris × 21 kolom
**Kondisi:** Cukup bersih tapi banyak kolom yang mayoritas kosong ("-").

| Kolom | Tipe | Unik | Kosong ("-") | Status |
|-------|------|------|-------------|--------|
| index | int | 2000 | 0 | ❌ BUANG (identitas) |
| Link | text | 11496 | 0 | ❌ BUANG (URL) |
| Alamat | text | 7 | 0 | ❌ BUANG (sedikit variasi) |
| IMG Link | text | 11496 | 0 | ❌ BUANG (URL gambar) |
| ID Iklan | text | 11496 | 0 | ❌ BUANG (kode unik) |
| Tipe Properti | text | 1 | 0 | ❌ BUANG (100% "Rumah") |
| Luas Tanah | int | 575 | 0 | ✅ PAKAI |
| Luas Bangunan | int | 455 | 0 | ✅ PAKAI |
| Kamar | int | 44 | 0 | ✅ PAKAI |
| Kamar Mandi | int | 41 | 0 | ✅ PAKAI |
| Sertifikat | text | 6 | 508 (4%) | ✅ PAKAI |
| Jumlah Lantai | int | 9 | 0 | ✅ PAKAI |
| Kondisi Properti | text | 6 | 7582 (66%) | ❌ BUANG |
| Dilengkapi Perabotan | text | 4 | 8745 (76%) | ❌ BUANG |
| Daya Listrik | text | 29 | 3304 (29%) | ✅ PAKAI |
| Hadap | text | 9 | 9154 (80%) | ❌ BUANG |
| Garasi | int | 12 | 0 | ✅ PAKAI |
| Carport | text | 9 | 10424 (91%) | ❌ BUANG |
| Umur Bangunan | text | 40 | 5788 (50%) | ❌ BUANG |
| Kamar Pembantu | text | 11 | 7048 (61%) | ❌ BUANG |
| Harga | int | 548 | 0 | 🎯 TARGET |


---

## Lumajang: `DATA_RUMAH_LUMAJANG_DEEP.csv`

**Jumlah:** 91 baris × 17 kolom
**Kondisi:** Data masih mentah (perlu parsing harga dan luas dari teks).
**Metode Pengambilan:** Deep Scraping — bot Selenium membuka setiap halaman 
rumah satu per satu untuk mendapatkan detail tersembunyi.

| Kolom | Tipe | Unik | Kosong ("-") | Status |
|-------|------|------|-------------|--------|
| Link | text | 91 | 0 | ❌ BUANG (URL) |
| Lokasi | text | 2 | 0 | ❌ BUANG (hampir semua "Lumajang") |
| Tipe Properti | text | 4 | 77 (85%) | ❌ BUANG |
| Luas Tanah | text | 47 | 17 (19%) | ✅ PAKAI (perlu parsing "M²") |
| Luas Bangunan | text | 46 | 17 (19%) | ✅ PAKAI (perlu parsing "M²") |
| Kamar Tidur | text | 8 | 18 (20%) | ✅ PAKAI |
| Kamar Mandi | text | 6 | 17 (19%) | ✅ PAKAI |
| Sertifikat | text | 4 | 3 (3%) | ✅ PAKAI |
| Jumlah Lantai | text | 3 | 44 (48%) | ❌ BUANG |
| Kondisi Properti | text | 1 | 91 (100%) | ❌ BUANG (SEMUA KOSONG!) |
| Dilengkapi Perabotan | text | 1 | 91 (100%) | ❌ BUANG (SEMUA KOSONG!) |
| Daya Listrik | text | 10 | 17 (19%) | ✅ PAKAI |
| Kamar Pembantu | text | 1 | 91 (100%) | ❌ BUANG (SEMUA KOSONG!) |
| Garasi | text | 5 | 83 (91%) | ❌ BUANG |
| Carport | text | 5 | 76 (84%) | ❌ BUANG |
| Hadap | text | 1 | 91 (100%) | ❌ BUANG (SEMUA KOSONG!) |
| Harga | text | 57 | 0 | 🎯 TARGET (perlu parsing "RP 2,85 MILIAR") |


---

## Catatan tentang Data Lumajang

Data Lumajang hanya **91 baris** (jauh lebih sedikit dari Jakarta dan Surabaya). 
Ini karena Lumajang adalah kota kecil sehingga iklan properti online-nya terbatas.

**Dampak terhadap model:**
- Model mungkin kurang akurat karena data terlalu sedikit
- Overfitting lebih mungkin terjadi
- Sangat bergantung pada kualitas data

**Cara menjelaskan ke dosen:**
"Dataset Lumajang hanya 91 baris karena keterbatasan listing properti online 
di kota kecil. Kami menyadari ini adalah limitasi, namun kami tetap menjalankan 
pipeline yang sama untuk menunjukkan bahwa sistem kami scalable dan bisa 
diterapkan di kota manapun."
