import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import datetime
import re

# Konfigurasi Halaman Streamlit (Optimasi Penuh Mobile)
st.set_page_config(
    page_title="SPEEDHOME Analyser",
    page_icon="🏢",
    layout="wide", # Tetap menggunakan wide agar tabel memiliki ruang di desktop
    initial_sidebar_state="collapsed"
)

# Custom CSS Agresif untuk Layar HP (Mencegah Teks Terpotong / Hilang)
st.markdown("""
<style>
    /* Mengurangi padding default Streamlit agar muat di layar HP */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }
    
    /* Memastikan teks metrik tidak terpotong di layar kecil */
    [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        word-break: break-word !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
    }
    
    /* Membuat container tabel responsif */
    .stDataFrame div {
        width: 100% !important;
    }
    
    /* Menghilangkan margin berlebih pada perangkat mobile */
    @media (max-width: 640px) {
        .stHeading h1 { font-size: 1.8rem !important; }
        .stHeading h2 { font-size: 1.4rem !important; }
        .stHeading h3 { font-size: 1.1rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# FUNGSI-FUNGSI UTAMA (TETAP SAMA & STABIL)
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
        
        room_type = "Studio" if is_studio else (f"{beds} BR" if beds > 0 else "Lainnya")
        
        furnish_raw = item.get('furnishType', 'UNFURNISHED').upper()
        furnish = "Fully" if furnish_raw == 'FULL' else ("Partially" if furnish_raw == 'PARTIAL' else "Unfurnished")
            
        price_monthly = item.get('price', 0)
        price_yearly = price_monthly * 12 if price_monthly else 0
        
        is_daily_available = item.get('shortTermRental', False)
        price_daily = f"RM {round(price_monthly / 30)}" if is_daily_available else "N/A"

        prop_id = item.get('id', '')
        slug = item.get('urlSlug', '')
        link = f"https://speedhome.com/ads/{slug}-{prop_id}" if slug else f"https://speedhome.com/ads/{prop_id}"

        cleaned_data.append({
            "Listing": item.get('title', 'No Title')[:30] + "...", # Potong judul agar hemat ruang di HP
            "Property": item.get('name', 'N/A'),
            "Tipe": room_type,
            "Bulanan": price_monthly,
            "Tahunan": price_yearly,
            "Harian": price_daily,
            "Size": item.get('sqft', 0),
            "Furnitur": furnish,
            "Link": link
        })
    return pd.DataFrame(cleaned_data)

def calculate_summary(df):
    summary_rows = []
    grouped = df.groupby('Tipe')
    for name, group in grouped:
        prices = group['Bulanan'].dropna()
        sizes = group['Size'].dropna()
        if prices.empty: continue
            
        mode_val = prices.mode()
        mode_str = f"RM {int(mode_val.iloc[0])}" if not mode_val.empty else "N/A"
        
        summary_rows.append({
            "Tipe Unit": name,
            "Unit": len(group),
            "Avg (RM)": round(prices.mean()),
            "Median (RM)": round(prices.median()),
            "Modus": mode_str,
            "Fair Price": f"RM {round(prices.median())}",
            "Avg Size": f"{round(sizes.mean())} sqft" if not sizes.empty else "N/A"
        })
    return pd.DataFrame(summary_rows)

# -----------------------------------------------------------------------------
# INTERFACE APLIKASI WEB (STREAMLIT)
# -----------------------------------------------------------------------------

st.title("🏢 SPEEDHOME Analyser")
st.caption("Automated property data aggregator.")

st.subheader("🔍 Parameter Pencarian")
input_mode = st.radio("Metode Input:", ["Ketik Nama", "URL Langsung"], horizontal=True)

search_keyword = ""

if input_mode == "Ketik Nama":
    typed_input = st.text_input("Nama Area / Apartemen:", placeholder="Contoh: Mont Kiara...")
    if len(typed_input) >= 3:
        if "speedhome.com" in typed_input:
            extracted = extract_slug_from_url(typed_input)
            if extracted: search_keyword = extracted
        else:
            suggestions = get_suggestions(typed_input)
            if suggestions:
                search_keyword = st.selectbox("Pilih Area Terdekat:", suggestions)
            else:
                search_keyword = typed_input
    else:
        search_keyword = typed_input
else:
    url_input = st.text_input("Paste URL SPEEDHOME:", placeholder="https://speedhome.com/rent/...")
    if url_input:
        extracted = extract_slug_from_url(url_input)
        if extracted: search_keyword = extracted

if st.button("🚀 Ambil Data", type="primary", use_container_width=True): # Gunakan container width agar tombol penuh di HP
    if not search_keyword:
        st.error("Input tidak boleh kosong!")
    else:
        with st.spinner("Mengunduh data..."):
            raw_data = fetch_speedhome_data(search_keyword)
            if not raw_data:
                st.error("Gagal mengambil data atau koneksi diblokir.")
            else:
                df_listings = process_data(raw_data)
                if df_listings.empty:
                    st.warning("Data tidak ditemukan.")
                else:
                    st.session_state['df_listings'] = df_listings
                    st.session_state['search_area'] = search_keyword.replace(" ", "_")

# MENAMPILKAN HASIL DATA
if 'df_listings' in st.session_state:
    df_listings = st.session_state['df_listings']
    area_name = st.session_state['search_area']
    
    # 1. Tipe Sewa (Metrik dibuat Vertikal/Horizontal cerdas)
    st.write("---")
    st.subheader("📅 Tipe Sewa Tersedia")
    
    has_daily = df_listings['Harian'].loc[df_listings['Harian'] != "N/A"].count()
    
    # Menggunakan container agar rapi di HP
    st.metric(label="Sewa Bulanan & Tahunan", value="Tersedia (Aktif)")
    st.metric(label="Sewa Jangka Pendek (Harian)", value=f"{has_daily} Unit" if has_daily > 0 else "Tidak Tersedia")

    # 2. Summary Table
    st.write("---")
    st.subheader("📊 Summary Harga")
    df_summary = calculate_summary(df_listings)
    
    # Menggunakan st.dataframe dengan configurasi penyesuaian lebar otomatis
    st.dataframe(df_summary, use_container_width=True, hide_index=True)
    
    # 3. Download Button
    st.write("---")
    import io
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_summary.to_excel(writer, sheet_name='Summary Harga', index=False)
        df_listings.to_excel(writer, sheet_name='Daftar Unit', index=False)
        
    st.download_button(
        label="📥 Download File Excel (.xlsx)",
        data=buffer.getvalue(),
        file_name=f"SPEEDHOME_{area_name}_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True # Tombol penuh di layar HP
    )

    # 4. Detailed Unit Listings
    st.write("---")
    st.subheader("📋 Daftar Unit Lengkap")
    st.write("*(Geser tabel ke kanan untuk melihat kolom harga/link)*")
    
    st.dataframe(
        df_listings, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "Link": st.column_config.LinkColumn("Buka", display_text="Link")
        }
    )
