import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import re

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="SPEEDHOME Market Data Automated Aggregator",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================================
# KUNCI JAWABAN: CSS Khusus Penyesuaian Ukuran Otomatis Tanpa Ubah Susunan
# =============================================================================
st.markdown("""
<style>
    /* Mengatur lebar maksimal kontainer utama di laptop */
    .reportview-container .main .block-container{ max-width: 1200px; }
    .stDataFrame { width: 100%; }
    
    /* 📱 MEDIA QUERY: Otomatis aktif HANYA di layar HP (Lebar Maksimal 768px) */
    @media (max-width: 768px) {
        /* Mengecilkan ukuran font teks Judul Utama agar tidak pecah/hilang */
        .stHeading h1 { font-size: 1.6rem !important; }
        .stHeading h2 { font-size: 1.2rem !important; }
        .stHeading h3 { font-size: 1.0rem !important; }
        
        /* Mengecilkan ukuran komponen metrik kotak sewa agar muat sebaris */
        [data-testid="stMetricValue"] {
            font-size: 1.3rem !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
        }
        
        /* Memaksa area tabel luar memiliki scrollbar horizontal bawaan HP yang lancar */
        div[data-testid="stDataFrame"] {
            overflow-x: auto !important;
        }
        
        /* Mengurangi space kosong (padding) di kanan-kiri layar HP agar teks tidak terbuang */
        .block-container {
            padding-left: 0.4rem !important;
            padding-right: 0.4rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# FUNGSI-FUNGSI HELPER & API FETCHING (SUSUNAN ASLI)
# -----------------------------------------------------------------------------

def extract_slug_from_url(url):
    match = re.search(r"rent/([^/?]+)", url)
    if match:
        return match.group(1).replace("-", " ")
    match_ads = re.search(r"ads/([^/?]+)", url)
    if match_ads:
        slug_clean = re.sub(r"-[a-f0-9\-]+$", "", match_ads.group(1))
        return slug_clean.replace("-", " ")
    return None

def get_suggestions(query):
    if not query or len(query) < 3:
        return []
    if "speedhome.com" in query:
        extracted = extract_slug_from_url(query)
        if extracted: return [extracted.title()]

    url = f"https://api.speedhome.com/v1/internal/search/suggest?q={query}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            suggestions = [item.get('name') for item in data.get('suggestions', []) if item.get('name')]
            return list(set(suggestions))[:5]
    except:
        pass
    return []

def fetch_speedhome_data(location_query):
    if "speedhome.com" in location_query:
        extracted = extract_slug_from_url(location_query)
        if extracted: location_query = extracted

    formatted_query = location_query.lower().strip().replace(" ", "-")
    url = f"https://api.speedhome.com/v1/internal/search?q={formatted_query}&pageSize=100&page=0"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://speedhome.com/",
        "Origin": "https://speedhome.com"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            return response.json().get('results', [])
        return None
    except:
        return None

def process_data(raw_listings):
    cleaned_data = []
    
    for item in raw_listings:
        beds = item.get('bedrooms', 0)
        is_studio = item.get('propertyType') == 'STUDIO'
        
        if is_studio:
            room_type = "Studio"
        elif beds > 0:
            room_type = f"{beds} BR"
        else:
            room_type = "Lainnya"
            
        furnish_raw = item.get('furnishType', 'UNFURNISHED').upper()
        if furnish_raw == 'FULL':
            furnish = "Fully Furnished"
        elif furnish_raw == 'PARTIAL':
            furnish = "Partially Furnished"
        else:
            furnish = "Unfurnished"
            
        price_monthly = item.get('price', 0)
        price_yearly = price_monthly * 12 if price_monthly else 0
        
        is_daily_available = item.get('shortTermRental', False)
        price_daily = f"RM {round(price_monthly / 30)}" if is_daily_available else "Tidak Tersedia"

        prop_id = item.get('id', '')
        slug = item.get('urlSlug', '')
        link = f"https://speedhome.com/ads/{slug}-{prop_id}" if slug else f"https://speedhome.com/ads/{prop_id}"

        # SUSUNAN INPUT UTAMA DIKEMBALIKAN UTUH SEPERTI REKUES AWAL ANDA
        cleaned_data.append({
            "Judul Listing": item.get('title', 'No Title'),
            "Nama Property / Area": item.get('name', 'N/A'),
            "Tipe Kamar": room_type,
            "Harga Bulanan (RM)": price_monthly,
            "Harga Tahunan (RM)": price_yearly,
            "Sewa Harian": price_daily,
            "Ukuran (sqft)": item.get('sqft', 0),
            "Status Furnitur": furnish,
            "Link": link
        })
        
    return pd.DataFrame(cleaned_data)

def calculate_summary(df):
    summary_rows = []
    grouped = df.groupby('Tipe Kamar')
    
    for name, group in grouped:
        prices = group['Harga Bulanan (RM)'].dropna()
        sizes = group['Ukuran (sqft)'].dropna()
        
        if prices.empty:
            continue
            
        mode_val = prices.mode()
        mode_str = f"RM {int(mode_val.iloc[0])}" if not mode_val.empty else "N/A"
        fair_price = prices.median()
        
        # SUSUNAN FORMULIR RESUME DIKEMBALIKAN UTUH SPERTI AWAL
        summary_rows.append({
            "Tipe Unit": name,
            "Jumlah Unit": len(group),
            "Rata-rata Harga": f"RM {round(prices.mean())}",
            "Median Harga": f"RM {round(prices.median())}",
            "Modus Harga": mode_str,
            "Harga Wajar (Fair Price)": f"RM {round(fair_price)}",
            "Rata-rata Ukuran (sqft)": f"{round(sizes.mean())} sqft" if not sizes.empty else "N/A"
        })
        
    return pd.DataFrame(summary_rows)

# -----------------------------------------------------------------------------
# INTERFACE APLIKASI WEB (SUSUNAN STRUKTUR TETAP / FIX SIZING)
# -----------------------------------------------------------------------------

st.title("🏢 SPEEDHOME Market Data Automated Aggregator")
st.caption("Aplikasi otomatis pengumpul dan penganalisis data sewa properti real-time dari SPEEDHOME Malaysia.")
st.write("---")

st.subheader("🔍 Parameter Pencarian")
input_mode = st.radio("Pilih Metode Input:", ["Ketik Nama Area / Apartemen", "Masukkan URL Langsung"], horizontal=True)

search_keyword = ""

if input_mode == "Ketik Nama Area / Apartemen":
    typed_input = st.text_input("Kawasan Ketik Nama (Contoh: 'Mont Kiara', 'Cyberjaya'):", placeholder="Ketik minimal 3 huruf...")
    
    if len(typed_input) >= 3:
        if "speedhome.com" in typed_input:
            extracted = extract_slug_from_url(typed_input)
            if extracted: search_keyword = extracted
        else:
            suggestions = get_suggestions(typed_input)
            if suggestions:
                search_keyword = st.selectbox("Saran area ditemukan (Pilih salah satu):", ["-- Pilih Area --"] + suggestions)
                if search_keyword == "-- Pilih Area --":
                    search_keyword = ""
            else:
                search_keyword = typed_input
    else:
        search_keyword = typed_input

else:
    url_input = st.text_input("Masukkan URL Halaman Publik SPEEDHOME:", placeholder="https://speedhome.com/rent/mont-kiara")
    if url_input:
        extracted = extract_slug_from_url(url_input)
        if extracted: search_keyword = extracted

# Tombol menyesuaikan lebar kontainer secara elegan di HP
if st.button("🚀 Kumpulkan dan Proses Data", type="primary", use_container_width=True):
    if not search_keyword:
        st.error("Silakan masukkan nama area atau URL yang valid terlebih dahulu!")
    else:
        with st.spinner(f"Sedang menarik data otomatis untuk '{search_keyword}' dari SPEEDHOME..."):
            raw_data = fetch_speedhome_data(search_keyword)
            
            if not raw_data:
                st.error("Tidak ada data yang ditemukan atau koneksi diblokir.")
            else:
                df_listings = process_data(raw_data)
                if df_listings.empty:
                    st.warning("Data wilayah tersebut kosong setelah diproses.")
                else:
                    st.session_state['df_listings'] = df_listings
                    st.session_state['search_area'] = search_keyword.replace(" ", "_")

if 'df_listings' in st.session_state:
    df_listings = st.session_state['df_listings']
    area_name = st.session_state['search_area']
    current_date = datetime.now().strftime("%Y%m%d")
    
    # OUTPUT 4: Tipe Sewa yang Dicakup (Susunan kolom horizontal laptop, bertumpuk aman di HP)
    st.write("---")
    st.subheader("📅 Cakupan Tipe Sewa di Area Ini")
    col1, col2, col3 = st.columns(3)
    
    has_daily = df_listings['Sewa Harian'].loc[df_listings['Sewa Harian'] != "Tidak Tersedia"].count()
    
    with col1:
        st.metric(label="Sewa Bulanan", value="Tersedia (Dominan)", delta="Aktif")
    with col2:
        st.metric(label="Sewa Tahunan (Kalkulasi 12bln)", value="Tersedia", delta="Aktif")
    with col3:
        if has_daily > 0:
            st.metric(label="Sewa Harian (Short-term)", value=f"Tersedia ({has_daily} Unit)", delta="Terbatas")
        else:
            st.metric(label="Sewa Harian (Short-term)", value="Tidak Tersedia", delta="Kosong", delta_color="inverse")

    # OUTPUT 2: Tabel Ringkasan Harga (Price Summary)
    st.write("---")
    st.subheader("📊 Tabel Ringkasan Harga (Price Summary)")
    df_summary = calculate_summary(df_listings)
    st.dataframe(df_summary, use_container_width=True, hide_index=True)
    
    # OUTPUT 5: Fitur Download Data
    st.write("---")
    st.subheader("💾 Unduh Data Hasil Scraper")
    
    import io
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_summary.to_excel(writer, sheet_name='Summary Harga', index=False)
        df_listings.to_excel(writer, sheet_name='Daftar Unit Lengkap', index=False)
        
    st.download_button(
        label="📥 Download Hasil Format Excel (.xlsx)",
        data=buffer.getvalue(),
        file_name=f"SPEEDHOME_{area_name}_{current_date}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    # OUTPUT 3: Tabel Daftar Unit (Unit Listings)
    st.write("---")
    st.subheader("📋 Tabel Daftar Unit Lengkap (Unit Listings)")
    st.write("*(Gunakan scroll horizontal jika layar HP Anda vertikal untuk melihat seluruh kolom)*")
    
    st.dataframe(
        df_listings, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Link": st.column_config.LinkColumn("Link Listing", display_text="Buka Halaman SPEEDHOME")
        }
    )
