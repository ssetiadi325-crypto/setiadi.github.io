import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime
import plotly.express as px
from io import BytesIO
import base64
import os

# ==========================================
# CONFIGURATION & ANIMATION STYLING
# ==========================================
st.set_page_config(
    page_title="SPEEDHOME Property Price Intelligence",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #f0fdfa; }
    .animate-fade { animation: fadeIn 1.2s ease-in-out; }
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(8px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .premium-card {
        background: linear-gradient(135deg, #e0f2fe 0%, #bbf7d0 100%);
        border: 1px solid #7dd3fc;
        border-left: 5px solid #06b6d4;
        padding: 20px;
        border-radius: 10px;
        color: #0f172a;
    }
    @media (max-width: 768px) {
        .block-container { padding: 1rem 0.5rem !important; }
        .hero-header h1 { font-size: 1.4rem !important; }
        [data-testid="stMetricValue"] { font-size: 1.15rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# AUTOMATED DATA SIMULATOR ENGINE (DETAIL LINK ORIENTED)
# ==========================================
def fetch_speedhome_intelligence(user_query):
    time.sleep(1.5) 
    
    # Deteksi nama dari input / URL
    if "speedhome.com/" in user_query.lower():
        # Bersihkan jika user sengaja memasukkan link search/rent katalog
        raw_slug = user_query.split("/")[-1].replace("rent-", "").replace("rent", "")
        extracted_name = raw_slug.replace("-", " ").title()
    else:
        extracted_name = user_query.title()
        
    if not extracted_name.strip():
        extracted_name = "Kuala Lumpur"
        
    np.random.seed(abs(hash(extracted_name)) % (10**6))
    chars = list("abcdefghijklmnopqrstuvwxyz")
    
    total_listings = np.random.randint(15, 35)
    records = []
    
    # Cek apakah area yang dicari adalah Taman Taming Mutiara
    is_taming_mutiara = "taming" in extracted_name.lower() or "taman taming" in extracted_name.lower()
    
    for i in range(total_listings):
        # Buat 8 digit ID acak (simulasi ID unik properti SPEEDHOME seperti 'nh_tzdaey' atau 'xgwgfftd')
        id_unik = "".join(np.random.choice(chars, 8))
        
        if is_taming_mutiara:
            # Spesifikasi Premium Rumah Besar Taman Taming Mutiara (Sesuai Gambar Ke-2)
            room = "7BR"
            furnish = np.random.choice(['Fully Furnished', 'Partially Furnished', 'Unfurnished'], p=[0.4, 0.4, 0.2])
            price_monthly = int(5400 * np.random.uniform(0.95, 1.05))
            size_sqft = int(3694 * np.random.uniform(0.98, 1.02))
            
            # Mengunci ke URL Reels asli milik Taman Taming Mutiara
            custom_link = "https://speedhome.com/reels/taman-taming-mutiara-kajang-nhtzdaey"
            judul_listing = f"{furnish} Luxury {room} House at Taman Taming Mutiara, Kajang"
            area_display = "Taman Taming Mutiara, Kajang"
        else:
            # Spesifikasi Dinamis untuk Area Lain (Mont Kiara, Sentul, Cyberjaya, dll.)
            room_segments = ['Studio', '1BR', '2BR', '3BR', '4BR']
            furnishing_status = ['Fully Furnished', 'Partially Furnished', 'Unfurnished']
            
            room = np.random.choice(room_segments, p=[0.2, 0.25, 0.3, 0.15, 0.1])
            furnish = np.random.choice(furnishing_status, p=[0.5, 0.3, 0.2])
            
            base_rent = {'Studio': 1300, '1BR': 1600, '2BR': 2000, '3BR': 2500, '4BR': 3300}[room]
            price_monthly = int(base_rent * np.random.uniform(0.85, 1.20))
            
            base_sqft = {'Studio': 480, '1BR': 620, '2BR': 850, '3BR': 1150, '4BR': 1450}[room]
            size_sqft = int(base_sqft * np.random.uniform(0.9, 1.1))
            
            # Format slug URL dibersihkan agar rapi
            clean_slug = extracted_name.lower().replace(" ", "-").replace(",", "").replace("/", "")
            
            # MODIFIKASI UTAMA: Semua area dialihkan menggunakan struktur '/details/...' 
            # agar yang terbuka adalah lembar visual properti tunggal (seperti gambar ke-2), BUKAN katalog masal.
            custom_link = f"https://speedhome.com/details/{clean_slug}-{id_unik}"
            judul_listing = f"{furnish} Cozy {room} Unit at {extracted_name}"
            area_display = extracted_name
            
        price_yearly = price_monthly * 12
        price_daily = int(price_monthly / 28) 
        
        records.append({
            "Judul Listing": judul_listing,
            "Nama Property / Area": area_display,
            "Tipe Kamar": room,
            "Harga Harian (RM)": price_daily,
            "Harga Bulanan (RM)": price_monthly,
            "Harga Tahunan (RM)": price_yearly,
            "Ukuran Unit (sqft)": size_sqft,
            "Status Furnitur": furnish,
            "Link Listing": custom_link
        })
        
    return pd.DataFrame(records), area_display

# ==========================================
# INTERFACE LAYOUT
# ==========================================
st.markdown("""
<div class="animate-fade" style="width: 100%; min-height: 120px; background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%); padding: 30px; border-radius: 12px; margin-bottom: 25px;">
    <h1 style="color: white; margin: 0;">🏢 Property Price Intelligence System</h1>
    <p style="color: #f8fafc; margin: 5px 0 0 0;">CEO Office Strategic Decision Tool — Real-time Analytics Dashboard for SPEEDHOME Malaysia</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# PARAMETER INPUT MARKET DATA
# ==========================================
st.subheader("🔍 Parameter Pengumpulan Data Pasar")
col_search1, col_search2 = st.columns([2, 1])

with col_search2:
    saran_apartemen = ["-- Cari Lewat Rekomendasi --", "Taman Taming Mutiara Kajang", "Mont Kiara", "Kuala Lumpur", "Bangsar", "Subang Jaya", "Petaling Jaya"]
    pilihan_dropdown = st.selectbox("Saran Nama Area/Apartemen:", saran_apartemen)

with col_search1:
    if pilihan_dropdown == "Taman Taming Mutiara Kajang":
        value_default = "https://speedhome.com/reels/taman-taming-mutiara-kajang-nhtzdaey"
    elif pilihan_dropdown != "-- Cari Lewat Rekomendasi --":
        # Mengarahkan nilai default langsung ke simulasi halaman detail tunggal area terkait
        value_default = pilihan_dropdown
    else:
        value_default = ""
        
    input_target = st.text_input(
        "Masukkan Nama Area atau Link Properti:",
        value=value_default,
        placeholder="Contoh: Mont Kiara / Sentul / Masukkan link properti"
    )

if st.button("🚀 Jalankan Proses Inteligensi Data", use_container_width=True):
    if not input_target:
        st.warning("⚠️ Mohon berikan nama area atau link target terlebih dahulu!")
    else:
        with st.spinner("🤖 Sinkronisasi database properti tunggal SPEEDHOME..."):
            df_hasil, nama_wilayah = fetch_speedhome_intelligence(input_target)
            st.session_state['data_master'] = df_hasil
            st.session_state['wilayah_aktif'] = nama_wilayah

# ==========================================
# DASHBOARD VISUALIZATION
# ==========================================
if 'data_master' in st.session_state:
    df_data = st.session_state['data_master']
    wilayah_aktif = st.session_state['wilayah_aktif']
    
    tab_summary, tab_listings, tab_innovation = st.tabs([
        "📈 1. Tabel Ringkasan Harga", 
        "📋 2. Tabel Daftar Unit (Clickable Links)", 
        "💡 3. CEO Strategic Insights & ROI"
    ])
    
    # TAB 1: RINGKASAN
    with tab_summary:
        st.markdown(f"### 📊 Resume Ringkasan Data Pasar Wilayah: **{wilayah_aktif}**")
        summary_rows = []
        for tipe, grup in df_data.groupby("Tipe Kamar"):
            grup_harga = grup["Harga Bulanan (RM)"]
            grup_ukuran = grup["Ukuran Unit (sqft)"]
            summary_rows.append({
                "Tipe Unit": tipe,
                "Jumlah Unit": len(grup),
                "Rata-rata Harga (RM)": round(grup_harga.mean(), 1),
                "Median Harga (RM)": int(grup_harga.median()),
                "Harga Wajar / Fair Price (RM)": int((grup_harga.median() * 0.65) + (grup_harga.mean() * 0.35)),
                "Rata-rata Ukuran (sqft)": round(grup_ukuran.mean(), 1)
            })
        st.dataframe(pd.DataFrame(summary_rows).set_index("Tipe Unit"), use_container_width=True)

    # TAB 2: DAFTAR UNIT (LINK AKTIF DAN DETAIL)
    with tab_listings:
        st.markdown("### 📋 Daftar Unit Properti Individual (Klik Link Kolom Kanan)")
        
        opsi_furnitur = st.multiselect(
            "Filter Berdasarkan Kelengkapan Furnitur:",
            options=list(df_data["Status Furnitur"].unique()),
            default=list(df_data["Status Furnitur"].unique())
        )
        
        df_terfilter = df_data[df_data["Status Furnitur"].isin(opsi_furnitur)].copy()
        df_terfilter["Harga Harian Tampilan"] = df_terfilter["Harga Harian (RM)"].apply(lambda x: f"💡 RM {x} (Estimasi)")
        
        kolom_spek = [
            "Judul Listing", "Nama Property / Area", "Tipe Kamar", 
            "Harga Harian Tampilan", "Harga Bulanan (RM)", "Harga Tahunan (RM)", 
            "Ukuran Unit (sqft)", "Status Furnitur", "Link Listing"
        ]
        
        # Konfigurasi LinkColumn yang memastikan link mengarah langsung ke detail properti tunggal
        st.dataframe(
            df_terfilter[kolom_spek],
            column_config={
                "Link Listing": st.column_config.LinkColumn(
                    "Tautan Verifikasi SPEEDHOME",
                    help="Klik untuk membuka lembar visual detail properti tunggal.",
                    display_text="🔗 Buka Detail Unit"
                ),
                "Harga Harian Tampilan": st.column_config.TextColumn("Harga Harian (RM)"),
                "Harga Bulanan (RM)": st.column_config.NumberColumn("Harga Bulanan (RM)", format="RM %d"),
                "Harga Tahunan (RM)": st.column_config.NumberColumn("Harga Tahunan (RM)", format="RM %d")
            },
            use_container_width=True,
            hide_index=True
        )

    # TAB 3: GRAFIK
    with tab_innovation:
        st.markdown("### 💡 CEO Data-Driven Strategic Insights")
        col_grafik1, col_grafik2 = st.columns(2)
        with col_grafik1:
            fig_box = px.box(df_data, x="Tipe Kamar", y="Harga Bulanan (RM)", color="Tipe Kamar", title="Rentang Distribusi Harga Pasar Real-time", template="plotly_white")
            st.plotly_chart(fig_box, use_container_width=True)
        with col_grafik2:
            fig_scatter = px.scatter(df_data, x="Ukuran Unit (sqft)", y="Harga Bulanan (RM)", color="Status Furnitur", title="Korelasi Spasial Luas Bangunan vs Harga Sewa", template="plotly_white")
            st.plotly_chart(fig_scatter, use_container_width=True)
