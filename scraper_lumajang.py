"""
Script Deep Scraper Data Rumah Lumajang (SELENIUM)
==================================================
Script ini mengambil data dari situs properti (Rumah123) secara MENDALAM.
Pertama-tama ia akan mengambil semua URL rumah di halaman pencarian,
lalu ia akan MEMBUKA SATU PER SATU halaman rumah tersebut untuk mendapatkan
fitur spesifik (Sertifikat, Listrik, Kondisi, dll).
"""

import time
import os
import random
import re
import pandas as pd
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

TARGET_URL = 'https://www.rumah123.com/jual/lumajang/rumah/?page='
MAX_PAGES = 5 # Berapa halaman list pencarian yang ingin diambil

def setup_driver():
    """Menyiapkan dan membuka browser Chrome"""
    chrome_options = Options()
    # chrome_options.add_argument("--headless") # Jalankan tanpa membuka jendela (bisa lebih rentan diblokir)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def scrape_lumajang():
    print("Menjalankan Deep Scraper... (Proses ini akan memakan waktu lama)")
    
    try:
        driver = setup_driver()
    except Exception as e:
        print(f"Gagal membuka Chrome. Error: {e}")
        return

    # FASE 1: Mengumpulkan semua URL Rumah
    property_urls = set()
    
    for page in range(1, MAX_PAGES + 1):
        print(f"\n[FASE 1] Memuat Halaman Pencarian ke-{page}...")
        url = f"{TARGET_URL}{page}"
        
        try:
            driver.get(url)
            time.sleep(random.uniform(4.0, 6.0))
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
            time.sleep(2)
            
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Cari semua link properti
            links = soup.find_all('a', href=re.compile(r'/properti/'))
            for link in links:
                href = link['href']
                if 'rumah123.com' not in href:
                    href = 'https://www.rumah123.com' + href
                property_urls.add(href)
                
            print(f"Total URL unik dikumpulkan sementara: {len(property_urls)}")
            
        except Exception as e:
            print(f"Error halaman {page}: {e}")
            
    print(f"\n✅ Selesai Fase 1! Mendapatkan {len(property_urls)} URL Properti untuk digali lebih dalam.")
    
    # FASE 2: Membuka Setiap URL dan Ekstrak Fitur Lengkap
    all_data = []
    
    for idx, prop_url in enumerate(list(property_urls)):
        print(f"[{idx+1}/{len(property_urls)}] Menggali data dari: {prop_url.split('/')[-2][:20]}...")
        
        try:
            driver.get(prop_url)
            time.sleep(random.uniform(3.0, 5.0)) # JEDA SANGAT PENTING AGAR TIDAK DIBLOKIR
            
            driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(1)
            
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            text_content = soup.get_text(separator=' | ', strip=True).lower()
            
            # Ekstrak data menggunakan pola Teks yang umum ada di halaman detail Rumah123
            # Kami menggunakan regex untuk mencari "Label | Nilai" 
            
            # Harga
            harga_match = re.search(r'rp\s*([0-9.,]+)\s*(juta|miliar|triliun)?', text_content)
            harga = harga_match.group(0).upper() if harga_match else "0"
            
            # Lokasi (Title halaman biasanya memuat lokasi)
            title = soup.title.string if soup.title else ""
            lokasi_match = re.search(r'di\s+(.+?),', title, re.IGNORECASE)
            lokasi = lokasi_match.group(1).title() if lokasi_match else "Lumajang"
            
            # Fitur dasar
            def cari_nilai(label, text_source):
                # Mencari kata kunci, lalu mengambil kata setelah pemisah ' | '
                pattern = rf'{label}\s*\|\s*([^|]+)'
                match = re.search(pattern, text_source)
                return match.group(1).strip().title() if match else "-"
            
            data_rumah = {
                'Link': prop_url,
                'Lokasi': lokasi,
                'Tipe Properti': cari_nilai('tipe properti', text_content),
                'Luas Tanah': cari_nilai('luas tanah', text_content).replace('m²', '').strip(),
                'Luas Bangunan': cari_nilai('luas bangunan', text_content).replace('m²', '').strip(),
                'Kamar Tidur': cari_nilai('kamar tidur', text_content),
                'Kamar Mandi': cari_nilai('kamar mandi', text_content),
                'Sertifikat': cari_nilai('sertifikat', text_content),
                'Jumlah Lantai': cari_nilai('jumlah lantai', text_content),
                'Kondisi Properti': cari_nilai('kondisi properti', text_content),
                'Dilengkapi Perabotan': cari_nilai('dilengkapi perabotan', text_content),
                'Daya Listrik': cari_nilai('daya listrik', text_content).replace('watt', '').replace(' ', ''),
                'Kamar Pembantu': cari_nilai('kamar pembantu', text_content),
                'Garasi': cari_nilai('garasi', text_content),
                'Carport': cari_nilai('carport', text_content),
                'Hadap': cari_nilai('hadap', text_content),
                'Harga': harga
            }
            
            all_data.append(data_rumah)
            
        except Exception as e:
            print(f"Error parsing detail: {e}")
            
    print("\nMenutup browser Chrome...")
    driver.quit()
            
    if all_data:
        df = pd.DataFrame(all_data)
        out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dataset', 'lumajang')
        os.makedirs(out_dir, exist_ok=True)
        
        out_path = os.path.join(out_dir, 'DATA_RUMAH_LUMAJANG_DEEP.csv')
        df.to_csv(out_path, index=False)
        print(f"\n✅ Scraping Selesai! Berhasil menambang {len(df)} data SECARA MENDALAM.")
        print(f"📁 Data disimpan di: {out_path}")
    else:
        print("\n❌ Gagal mendapatkan data sama sekali.")

if __name__ == '__main__':
    scrape_lumajang()
