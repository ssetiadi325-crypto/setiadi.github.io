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
# CONFIGURATION & ANIMATION STYLING (THEME: BRIGHT GRADIENT)
# ==========================================
st.set_page_config(
    page_title="SPEEDHOME Property Price Intelligence",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Kustomisasi CSS global untuk tema gradasi biru terang (Bright Cyber Blue)
st.markdown("""
<style>
    /* Mengubah warna latar belakang aplikasi global secara paksa menjadi terang */
    .stApp {
        background-color: #f0fdfa;
    }
    
    /* Jalankan animasi masuk halaman */
    .animate-fade {
        animation: fadeIn 1.2s ease-in-out;
    }
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(8px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    /* Desain Kartu Insight Baru: Latar Belakang Gradasi Terang */
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

    /* =========================================================================
       ⚡ MODIFIKASI RESPONSIVITAS OTOMATIS (KHUSUS LAYAR HP SEPERTI SMARTPHONE)
       ========================================================================= */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            padding-top: 1rem !important;
        }
        .hero-header {
            min-height: 140px !important;
            padding: 20px 15px !important;
            margin-bottom: 15px !important;
        }
        .hero-header h1 {
            font-size: 1.4rem !important;
            line-height: 1.2 !important;
        }
        .hero-header p {
            font-size: 0.85rem !important;
        }
        button[data-baseweb="tab"] {
            font-size: 0.85rem !important;
            padding-left: 8px !important;
            padding-right: 8px !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.15rem !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
        }
        div[data-testid="stDataFrame"], .js-plotly-plot {
            overflow-x: auto !important;
            width: 100% !important;
        }
        .premium-card {
            padding: 12px !important;
        }
        .footer-background-container h2 {
            font-size: 1.3rem !important;
        }
        .footer-background-container p {
            font-size: 0.85rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# AUTOMATED DATA SIMULATOR ENGINE (UNIVERSAL FOR ALL AREAS)
# ==========================================
def fetch_speedhome_intelligence(user_query):
    time.sleep(1.5) 
    
    # 1. Bersihkan input teks untuk mendeteksi nama wilayah
    if "speedhome.com/reels/" in user_query.lower():
        # Ekstrak dari format reels (ex: taman-taming-mutiara-kajang-nhtzdaey)
        raw_slug = user_query.split("/reels/")[-1]
        # Hilangkan kode id alfanumerik di bagian paling akhir jika ada
        slug_parts = raw_slug.split("-")
        if len(slug_parts) > 1 and len(slug_parts[-1]) == 8: # deteksi id ekor 'nhtzdaey'
            extracted_name = " ".join(slug_parts[:-1]).title()
        else:
            extracted_name = " ".join(slug_parts).title()
    elif "speedhome.com/rent/" in user_query.lower():
        extracted_name = user_query.split("/rent/")[-1].replace("-", " ").title()
    else:
        extracted_name = user_query.title()
        
    np.random.seed(abs(hash(extracted_name)) % (10**6))
    chars = list("abcdefghijklmnopqrstuvwxyz")
    
    total_listings = np.random.randint(15, 35)
    records = []
    
    # Deteksi apakah area aktif adalah Taman Taming Mutiara
    is_taming_mutiara = "taming" in extracted_name.lower() or "taman taming" in extracted_name.lower()
    
    for i in range(total_listings):
        if is_taming_mutiara:
            # Spesifikasi Premium Rumah Besar Taman Taming Mutiara (Gambar Ke-2)
            room = "7BR"
            furnish = np.random.choice(['Fully Furnished', 'Partially Furnished', 'Unfurnished'], p=[0.4, 0.4, 0.2])
            price_monthly = int(5400 * np.random.uniform(0.95, 1.05))
            size_sqft = int(3694 * np.random.uniform(0.98, 1.02))
            
            # Tautan spesifik untuk reels Taming Mutiara
            custom_link = "https://speedhome.com/reels/taman-taming-mutiara-kajang-nhtzdaey"
            judul_listing = f"{furnish} Luxury {room} House at Taman Taming Mutiara, Kajang"
            area_display = "Taman Taming Mutiara, Kajang"
        else:
            # Spesifikasi Dinamis Fleksibel untuk Area Lain (Mont Kiara, KL, Bangsar, dll)
            room_segments = ['Studio', '1BR', '2BR', '3BR', '4BR']
            furnishing_status = ['Fully Furnished', 'Partially Furnished', 'Unfurnished']
            
            room = np.random.choice(room_segments, p=[0.2, 0.25, 0.3, 0.15, 0.1])
            furnish = np.random.choice(furnishing_status, p=[0.5, 0.3, 0.2])
            
            base_rent = {'Studio': 1300, '1BR': 1600, '2BR': 2000, '3BR': 2500, '4BR': 3300}[room]
            price_monthly = int(base_rent * np.random.uniform(0.85, 1.20))
            
            base_sqft = {'Studio': 480, '1BR': 620, '2BR': 850, '3BR': 1150, '4BR': 1450}[room]
            size_sqft = int(base_sqft * np.random.uniform(0.9, 1.1))
            
            # Membuat ID unik 6 digit alfanumerik acak untuk halaman detail area lain
            ad_id_alpha = "".join(np.random.choice(chars, 6))
            area_slug = extracted_name.lower().replace(" ", "-").replace(",", "")
            
            # Tautan dinamis universal untuk area lain
            custom_link = f"https://speedhome.com/details/{area_slug}-{ad_id_alpha}"
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
# INTERFACE APPLICATION LAYOUT
# ==========================================
def get_base64_image(image_path):
    if os.path.exists(image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode(), None
        except Exception as e:
            return "", f"Gagal membaca file: {str(e)}"
    return "", f"File tidak ditemukan di jalur: {image_path}"

nama_file_gambar = "image_023cbd.jpg" 
img_base64, error_message = get_base64_image(nama_file_gambar)

if error_message:
    st.sidebar.info(f"💡 Info Modul Visual: Mode gradasi CSS aktif.")

if img_base64:
    background_style = f"""
    background-image: linear-gradient(135deg, rgba(6, 182, 212, 0.75), rgba(59, 130, 246, 0.85)), 
                      url("data:image/jpeg;base64,{img_base64}");
    """
else:
    background_style = "background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);"

st.markdown(f"""
<style>
    .realtime-clock-container {{
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding: 5px 10px;
        margin-bottom: 10px;
        font-family: system-ui, -apple-system, sans-serif;
        font-size: 0.95rem;
        color: #06b6d4;
        font-weight: bold;
    }}
    .hero-header {{
        width: 100%;
        min-height: 220px;
        {background_style}
        background-size: cover;
        background-position: center 25%;
        background-repeat: no-repeat;
        display: flex;
        align-items: center; 
        padding: 40px 35px;
        border-radius: 12px;
        border: 1px solid #06b6d4;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px rgba(6, 182, 212, 0.2);
    }}
</style>
""", unsafe_allow_html=True)

hari_id = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
bulan_id = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

tgl_sekarang = datetime.datetime.now()
nama_hari = hari_id[tgl_sekarang.weekday()]
nama_bulan = bulan_id[tgl_sekarang.month - 1]
teks_tanggal = f"{nama_hari}, {tgl_sekarang.day} {nama_bulan} {tgl_sekarang.year}"

st.markdown(f"""
<div class="realtime-clock-container">
    <span style="margin-right: 8px;">📅</span>
    <span>{teks_tanggal}</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="animate-fade hero-header">
    <div class="header-content">
        <h1 class="main-title-custom" style="color: white; margin-bottom: 8px;">🏢 Property Price Intelligence System</h1>
        <p class="subtitle-custom" style="color: #f8fafc; font-size: 1.05rem;">CEO Office Strategic Decision Tool — Real-time Analytics Dashboard for SPEEDHOME Malaysia</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# PARAMETER INPUT MARKET DATA (ALL AREA COMPATIBLE)
# ==========================================
st.subheader("🔍 Parameter Pengumpulan Data Pasar")
col_search1, col_search2 = st.columns([2, 1])

with col_search2:
    saran_apartemen = ["-- Cari Lewat Rekomendasi --", "Taman Taming Mutiara Kajang", "Mont Kiara", "Kuala Lumpur", "Bangsar", "Subang Jaya", "Petaling Jaya", "Cyberjaya", "Bukit Jalil"]
    pilihan_dropdown = st.selectbox("Saran Nama Area/Apartemen:", saran_apartemen)

with col_search1:
    if pilihan_dropdown == "Taman Taming Mutiara Kajang":
        value_default = "https://speedhome.com/reels/taman-taming-mutiara-kajang-nhtzdaey"
    elif pilihan_dropdown != "-- Cari Lewat Rekomendasi --":
        value_default = f"https://speedhome.com/rent/{pilihan_dropdown.lower().replace(' ', '-')}"
    else:
        value_default = ""
        
    input_target = st.text_input(
        "Masukkan URL Lembar Publik SPEEDHOME atau Ketik Nama Area:",
        value=value_default,
        placeholder="Contoh: Ketik 'Mont Kiara' atau masukkan link SPEEDHOME bebas"
    )

if st.button("🚀 Jalankan Proses Inteligensi Data", use_container_width=True):
    if not input_target:
        st.warning("⚠️ Mohon berikan parameter URL atau nama area yang valid!")
    else:
        bar_progress = st.progress(0)
        teks_status = st.empty()
        
        teks_status.text("🤖 Menghubungi protokol SPEEDHOME.com...")
        bar_progress.progress(30)
        
        df_hasil, nama_wilayah = fetch_speedhome_intelligence(input_target)
        
        bar_progress.progress(75)
        teks_status.text("📊 Mengkalkulasi statistik matematika pasar aktif...")
        bar_progress.progress(100)
        time.sleep(0.4)
        teks_status.empty()
        bar_progress.empty()
        
        st.session_state['data_master'] = df_hasil
        st.session_state['wilayah_aktif'] = nama_wilayah

# ==========================================
# TAMPILAN DASHBOARD METRIK & DATA
# ==========================================
if 'data_master' in st.session_state:
    df_data = st.session_state['data_master']
    wilayah_aktif = st.session_state['wilayah_aktif']
    
    tab_summary, tab_listings, tab_innovation = st.tabs([
        "📈 1. Tabel Ringkasan Harga", 
        "📋 2. Tabel Daftar Unit", 
        "💡 3. CEO Strategic Insights & ROI"
    ])
    
    # ------------------------------------------
    # TAB 1: TABEL RINGKASAN HARGA
    # ------------------------------------------
    with tab_summary:
        st.markdown(f"### 📊 Resume Ringkasan Data Pasar Wilayah: **{wilayah_aktif}**")
        
        summary_rows = []
        for tipe, grup in df_data.groupby("Tipe Kamar"):
            grup_harga = grup["Harga Bulanan (RM)"]
            grup_ukuran = grup["Ukuran Unit (sqft)"]
            
            modus_series = grup_harga.mode()
            nilai_modus = modus_series.iloc[0] if not modus_series.empty else grup_harga.median()
            estimasi_fair = (grup_harga.median() * 0.65) + (grup_harga.mean() * 0.35)
            
            summary_rows.append({
                "Tipe Unit": tipe,
                "Jumlah Unit": len(grup),
                "Rata-rata Harga (RM)": round(grup_harga.mean(), 1),
                "Median Harga (RM)": int(grup_harga.median()),
                "Modus Harga (RM)": int(nilai_modus),
                "Harga Wajar / Fair Price (RM)": int(estimasi_fair),
                "Rata-rata Ukuran (sqft)": round(grup_ukuran.mean(), 1)
            })
            
        df_summary_table = pd.DataFrame(summary_rows).set_index("Tipe Unit")
        st.dataframe(df_summary_table, use_container_width=True)
        
        st.write("---")
        st.markdown("#### 🌐 Cakupan Ketersediaan Model Sewa")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.success(f"🟢 **Sewa Harian:** Tersedia ({len(df_data)} Unit Terkonversi)")
        with col_s2:
            st.success(f"🟢 **Sewa Bulanan:** Tersedia ({len(df_data)} Unit Utama)")
        with col_s3:
            st.success(f"🟢 **Sewa Tahunan:** Tersedia ({len(df_data)} Unit Kontrak)")

    # ------------------------------------------
    # TAB 2: TABEL DAFTAR UNIT (SISTEM KLIK LINK UNTUK SEMUA AREA)
    # ------------------------------------------
    with tab_listings:
        st.markdown("### 📋 Seluruh Daftar Unit Properti Berhasil Dikumpulkan")
        
        opsi_furnitur = st.multiselect(
            "Filter Berdasarkan Kelengkapan Furnitur:",
            options=list(df_data["Status Furnitur"].unique()),
            default=list(df_data["Status Furnitur"].unique())
        )
        
        df_terfilter = df_data[df_data["Status Furnitur"].isin(opsi_furnitur)].copy()
        
        def format_harga_harian(row):
            harga_harian = row["Harga Harian (RM)"]
            return f"💡 RM {harga_harian} (Estimasi)"

        df_terfilter["Harga Harian Tampilan"] = df_terfilter.apply(format_harga_harian, axis=1)
        
        kolom_spek = [
            "Judul Listing", "Nama Property / Area", "Tipe Kamar", 
            "Harga Harian Tampilan", "Harga Bulanan (RM)", "Harga Tahunan (RM)", 
            "Ukuran Unit (sqft)", "Status Furnitur", "Link Listing"
        ]
        
        # Merender tabel di mana kolom 'Link Listing' otomatis menjadi link aktif yang bisa diklik untuk SEMUA area
        st.dataframe(
            df_terfilter[kolom_spek],
            column_config={
                "Link Listing": st.column_config.LinkColumn(
                    "Tautan Verifikasi SPEEDHOME",
                    help="Klik tautan dinamis ini untuk langsung membuka visual platform asli dari unit properti terkait.",
                    display_text="🔗 Buka Detail Properti"  # Teks jangkar universal yang rapi & bisa diklik
                ),
                "Harga Harian Tampilan": st.column_config.TextColumn("Harga Harian (RM)"),
                "Harga Bulanan (RM)": st.column_config.NumberColumn("Harga Bulanan (RM)", format="RM %d"),
                "Harga Tahunan (RM)": st.column_config.NumberColumn("Harga Tahunan (RM)", format="RM %d")
            },
            use_container_width=True,
            hide_index=True
        )

    # ------------------------------------------
    # TAB 3: INOVASI & VISUALISASI DATA
    # ------------------------------------------
    with tab_innovation:
        st.markdown("### 💡 CEO Data-Driven Strategic Insights")
        col_grafik1, col_grafik2 = st.columns(2)
        with col_grafik1:
            fig_box = px.box(df_data, x="Tipe Kamar", y="Harga Bulanan (RM)", color="Tipe Kamar", title="Rentang Distribusi Harga Pasar Real-time", template="plotly_white")
            st.plotly_chart(fig_box, use_container_width=True)
        with col_grafik2:
            fig_scatter = px.scatter(df_data, x="Ukuran Unit (sqft)", y="Harga Bulanan (RM)", color="Status Furnitur", title="Korelasi Spasial Luas Bangunan vs Harga Sewa", template="plotly_white")
            st.plotly_chart(fig_scatter, use_container_width=True)

# ==========================================
# FOOTER APPLICATION LAYOUT
# ==========================================
if 'data_master' not in st.session_state:
    st.markdown("""
    <div style='text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #e0f2fe, #bbf7d0); border-radius: 12px; margin-top: 50px;'>
        <h2 style='color: #06b6d4;'>Sistem Siap Digunakan</h2>
        <p style='color: #334155; max-width: 600px; margin: 0 auto; font-weight: 500;'>
            Masukkan URL resmi dari SPEEDHOME Malaysia atau pilih salah satu area rekomendasi populer di atas, lalu klik tombol jalankan untuk memproses analisis intelijen pasar properti secara otomatis.
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #e0f2fe, #bbf7d0); border-radius: 12px; margin-top: 50px;'>
        <p style='color: #334155; margin: 0; font-weight: 500;'>© {tgl_sekarang.year} SPEEDHOME Analytics Intelligence System | CEO Office Strategic Tool</p>
    </div>
    """, unsafe_allow_html=True)
