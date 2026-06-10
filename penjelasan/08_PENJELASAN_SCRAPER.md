# 🕷️ PENJELASAN SCRAPER LUMAJANG

## File: `scraper_lumajang.py`

### Apa Itu Web Scraping?
Web scraping adalah teknik mengambil data dari website secara otomatis 
menggunakan robot/bot. Kita menggunakan **Selenium** karena website 
rumah123.com menggunakan JavaScript dinamis (React/Next.js) yang tidak 
bisa diambil dengan `requests` biasa.

### Kenapa Butuh Selenium?
Website modern (seperti rumah123.com) me-render kontennya di browser 
menggunakan JavaScript. Jika kita hanya mengunduh HTML mentahnya 
(dengan `requests`), isinya kosong! Selenium membuka Chrome sungguhan 
dan menunggu JavaScript selesai berjalan.


---

## Arsitektur Deep Scraping (2 Fase)

### Fase 1: Kumpulkan URL
```
Browser membuka halaman pencarian
    → Scroll ke bawah
    → Ambil semua <a href="..."> yang mengarah ke halaman detail rumah
    → Klik "Halaman Berikutnya"
    → Ulangi sampai habis
    → Simpan semua URL unik ke dalam set()
```

### Fase 2: Gali Detail
```
Untuk setiap URL yang dikumpulkan:
    → Buka halaman detail rumah tersebut
    → Cari elemen-elemen spesifik:
        - Luas Tanah, Luas Bangunan
        - Kamar Tidur, Kamar Mandi
        - Sertifikat, Daya Listrik
        - Kondisi, Perabotan, dll
    → Simpan ke dalam list
    → Tunggu 4 detik (agar tidak diblokir)
```

### Kenapa 2 Fase?
Karena halaman pencarian (list) hanya menampilkan info dasar (harga + foto). 
Detail lengkap (sertifikat, daya listrik, garasi) hanya tersedia di 
halaman masing-masing rumah. Inilah yang disebut **"Deep Scraping"**.


---

## Anti-Detection (Agar Tidak Diblokir)

1. **Jeda 4 detik** antar request (`time.sleep(4)`)
2. **Chrome Options:**
   - `--disable-blink-features=AutomationControlled` (Menyamarkan bot)
   - `--start-maximized` (Tampak seperti user biasa)
3. **Menggunakan `set()`** untuk menghindari URL duplikat


---

## Output

File: `dataset/lumajang/DATA_RUMAH_LUMAJANG_DEEP.csv`

Kolom yang dihasilkan:
```
Link, Lokasi, Tipe Properti, Luas Tanah, Luas Bangunan, 
Kamar Tidur, Kamar Mandi, Sertifikat, Jumlah Lantai, 
Kondisi Properti, Dilengkapi Perabotan, Daya Listrik, 
Kamar Pembantu, Garasi, Carport, Hadap, Harga
```
