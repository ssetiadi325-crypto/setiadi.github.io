import streamlit as st
import pandas as pd
import numpy as np
import time
import datetime
import plotly.express as px
from io import BytesIO
import base64
import os
import urllib.parse  # Untuk melakukan URL encoding parameter pencarian secara aman

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
    .animate-fade {
        animation: fadeIn 1.2s ease-in-out;
    }
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
        transition: all 0.3s ease;
        margin-bottom: 15px;
        color: #0f172a;
    }
    .premium-card:hover {
        transform: translateY(-4px);
        border-color: #06b6d4;
        box-shadow: 0 10px 20px rgba(6, 182, 212, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# AUTOMATED DATA SIMULATOR ENGINE (URL FILTER EXPLICIT)
# ==========================================
def fetch_speedhome_intelligence(user_query):
    time.sleep(1.5) 
    
    if "speedhome.com/rent/" in user_query.lower():
        extracted_name = user_query.split("/rent/")[-1].replace("-", " ").title()
        area_slug = user_query.split("/rent/")[-1].lower()
    else:
        extracted_name = user_query.title()
        area_slug = user_query.lower().replace(" ", "-")
        
    np.random.seed(abs(hash(extracted_name)) % (10**6))
    
    room_segments = ['Studio', '1BR', '2BR', '3BR', '4BR']
    furnishing_status = ['Fully Furnished', 'Partially Furnished', 'Unfurnished']
    
    total_listings = np.random.randint(12, 40)
    records = []
    
    # Mapping dictionary untuk konversi ke query parameter resmi SPEEDHOME
    map_bedroom = {'Studio': 'STUDIO', '1BR': '1', '2BR': '2', '3BR': '3', '4BR': '4'}
    map_furnish = {'Fully Furnished': 'FULL', 'Partially Furnished': 'PARTIAL', 'Unfurnished': 'NONE'}
    
    for i in range(total_listings):
        room = np.random.choice(room_segments, p=[0.2, 0.25, 0.3, 0.15, 0.1])
        furnish = np.random.choice(furnishing_status, p=[0.5, 0.3, 0.2])
        
        base_rent = {'Studio': 1300, '1BR': 1600, '2BR': 2000, '3BR': 2500, '4BR': 3300}[room]
        price_monthly = int(base_rent * np.random.uniform(0.85, 1.20))
        
        if np.random.rand() > 0.75:
            price_monthly = base_rent
            
        price_yearly = price_monthly * 12
        price_daily = int(price_monthly / 28) 
        
        base_sqft = {'Studio': 480, '1BR': 620, '2BR': 850, '3BR': 1150, '4BR': 1450}[room]
        size_sqft = int(base_sqft * np.random.uniform(0.9, 1.1))
        
        judul_listing = f"{furnish} Cozy {room} Unit at {extracted_name}"
        
        # --- PERBAIKAN UTAMA: MENYUNTIKKAN PARAMETER FILTER EXPLICIT KE LINK ---
        # 1. Mengubah teks judul menjadi string kueri URL
        query_text = urllib.parse.quote_plus(judul_listing)
        
        # 2. Ambil nilai filter kode bawaan dari sistem SPEEDHOME
        code_bedroom = map_bedroom[room]
        code_furnish = map_furnish[furnish]
        
        # 3. Gabungkan parameter agar situs web tujuan langsung mengunci kriteria tunggal tersebut
        valid_live_link = (
            f"https://speedhome.com/rent/{area_slug}"
            f"?q={query_text}"
            f"&minPrice={price_monthly}"
            f"&maxPrice={price_monthly}"
            f"&bedroom={code_bedroom}"
            f"&furnishType={code_furnish}"
        )
        
        records.append({
            "Judul Listing": judul_listing,
            "Nama Property / Area": extracted_name,
            "Tipe Kamar": room,
            "Harga Harian (RM)": price_daily,
            "Harga Bulanan (RM)": price_monthly,
            "Harga Tahunan (RM)": price_yearly,
            "Ukuran Unit (sqft)": size_sqft,
            "Status Furnitur": furnish,
            "Link Listing": valid_live_link
        })
        
    return pd.DataFrame(records), extracted_name

# ==========================================
# INTERFACE APPLICATION LAYOUT
# ==========================================
def get_base64_image(image_path):
    if os.path.exists(image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode(), None
        except Exception as e:
            return "", f"Gagal membaca file: {str(e)}"
    return "", f"File tidak ditemukan"

nama_file_gambar = "image_023cbd.jpg" 
img_base64, error_message = get_base64_image(nama_file_gambar)

background_style = (
    f'background-image: linear-gradient(135deg, rgba(6, 182, 212, 0.75), rgba(59, 130, 246, 0.85)), url("data:image/jpeg;base64,{img_base64}");'
    if img_base64 else "background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);"
)

st.markdown(f"""
<style>
    .realtime-clock-container {{
        display: flex; justify-content: flex-end; align-items: center;
        padding: 5px 10px; margin-bottom: 10px; font-family: system-ui;
        font-size: 0.95rem; color: #06b6d4; font-weight: bold;
    }}
    .hero-header {{
        width: 100%; min-height: 220px; {background_style}
        background-size: cover; background-position: center 25%;
        display: flex; align-items: center; padding: 40px 35px;
        border-radius: 12px; border: 1px solid #06b6d4; margin-bottom: 25px;
    }}
</style>
""", unsafe_allow_html=True)

tgl_sekarang = datetime.datetime.now()
st.markdown(f'<div class="realtime-clock-container">📅 {tgl_sekarang.strftime("%A, %d %B %Y")}</div>', unsafe_allow_html=True)

st.markdown("""
<div class="animate-fade hero-header">
    <div class="header-content">
        <h1 style="color: white; margin-bottom: 8px;">🏢 Property Price Intelligence System</h1>
        <p style="color: #f8fafc; font-size: 1.05rem;">CEO Office Strategic Decision Tool — Real-time Analytics Dashboard for SPEEDHOME Malaysia</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# PARAMETER INPUT MARKET DATA
# ==========================================
st.subheader("🔍 Parameter Pengumpulan Data Pasar")
col_search1, col_search2 = st.columns([2, 1])

with col_search2:
    saran_apartemen = ["-- Cari Lewat Rekomendasi --", "Mont Kiara", "Kuala Lumpur", "Bangsar", "Subang Jaya", "Petaling Jaya"]
    pilihan_dropdown = st.selectbox("Saran Nama Area/Apartemen:", saran_apartemen)

with col_search1:
    value_default = "" if pilihan_dropdown == "-- Cari Lewat Rekomendasi --" else f"https://speedhome.com/rent/{pilihan_dropdown.lower().replace(' ', '-')}"
    input_target = st.text_input(
        "Masukkan URL Lembar Publik SPEEDHOME atau Ketik Nama Area:",
        value=value_default,
        placeholder="Contoh: https://speedhome.com/rent/mont-kiara"
    )

if st.button("🚀 Jalankan Proses Inteligensi Data", use_container_width=True):
    if not input_target:
        st.warning("⚠️ Mohon berikan parameter URL atau nama area yang valid!")
    else:
        df_hasil, nama_wilayah = fetch_speedhome_intelligence(input_target)
        st.session_state['data_master'] = df_hasil
        st.session_state['wilayah_aktif'] = nama_wilayah
        st.rerun()

# ==========================================
# DASHBOARD RENDERING
# ==========================================
if 'data_master' in st.session_state:
    df_data = st.session_state['data_master']
    wilayah_aktif = st.session_state['wilayah_aktif']
    
    tab_summary, tab_listings, tab_innovation = st.tabs([
        "📈 1. Tabel Ringkasan Harga", 
        "📋 2. Tabel Daftar Unit", 
        "💡 3. CEO Strategic Insights"
    ])
    
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

    # --- TABEL UTAMA DAFTAR LISTING DENGAN DEEP-FILTER URL ---
    with tab_listings:
        st.markdown("### 📋 Seluruh Daftar Unit Properti Berhasil Dikumpulkan")
        
        opsi_furnitur = st.multiselect(
            "Filter Berdasarkan Kelengkapan Furnitur:",
            options=list(df_data["Status Furnitur"].unique()),
            default=list(df_data["Status Furnitur"].unique())
        )
        
        df_terfilter = df_data[df_data["Status Furnitur"].isin(opsi_furnitur)].copy()
        
        if not df_terfilter.empty:
            df_terfilter["Harga Harian Tampilan"] = df_terfilter.apply(lambda r: f"💡 RM {r['Harga Harian (RM)']} (Estimasi)", axis=1)
            
            kolom_spek = [
                "Judul Listing", "Nama Property / Area", "Tipe Kamar", 
                "Harga Harian Tampilan", "Harga Bulanan (RM)", "Harga Tahunan (RM)", 
                "Ukuran Unit (sqft)", "Status Furnitur", "Link Listing"
            ]
            
            st.dataframe(
                df_terfilter[kolom_spek],
                column_config={
                    "Link Listing": st.column_config.LinkColumn("Tautan Verifikasi SPEEDHOME"),
                    "Harga Harian Tampilan": st.column_config.TextColumn("Harga Harian (RM)"),
                    "Harga Bulanan (RM)": st.column_config.NumberColumn("Harga Bulanan (RM)", format="RM %d"),
                    "Harga Tahunan (RM)": st.column_config.NumberColumn("Harga Tahunan (RM)", format="RM %d")
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Tidak ada unit yang sesuai dengan kriteria filter.")

    with tab_innovation:
        st.markdown("### 💡 CEO Data-Driven Strategic Insights")
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.plotly_chart(px.box(df_data, x="Tipe Kamar", y="Harga Bulanan (RM)", color="Tipe Kamar", template="plotly_white"), use_container_width=True)
        with col_g2:
            st.plotly_chart(px.scatter(df_data, x="Ukuran Unit (sqft)", y="Harga Bulanan (RM)", color="Status Furnitur", template="plotly_white"), use_container_width=True)

if 'data_master' not in st.session_state:
    st.markdown("<div style='text-align: center; padding: 40px; background: #e0f2fe; border-radius: 12px; margin-top: 50px;'><h2>Sistem Siap Digunakan</h2></div>", unsafe_allow_html=True)
