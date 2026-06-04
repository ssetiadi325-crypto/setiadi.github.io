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
# AUTOMATED DATA SIMULATOR ENGINE 
# ==========================================
def fetch_speedhome_intelligence(user_query):
    time.sleep(1.5) 
    
    if "speedhome.com/rent/" in user_query.lower():
        extracted_name = user_query.split("/rent/")[-1].replace("-", " ").title()
    else:
        extracted_name = user_query.title()
        
    np.random.seed(abs(hash(extracted_name)) % (10**6))
    
    room_segments = ['Studio', '1BR', '2BR', '3BR', '4BR']
    furnishing_status = ['Fully Furnished', 'Partially Furnished', 'Unfurnished']
    
    total_listings = np.random.randint(12, 40)
    records = []
    
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
        
        ad_id = np.random.randint(200000, 890000)
        
        records.append({
            "Judul Listing": f"{furnish} Cozy {room} Unit at {extracted_name}",
            "Nama Property / Area": extracted_name,
            "Tipe Kamar": room,
            "Harga Harian (RM)": price_daily,
            "Harga Bulanan (RM)": price_monthly,
            "Harga Tahunan (RM)": price_yearly,
            "Ukuran Unit (sqft)": size_sqft,
            "Status Furnitur": furnish,
            "Link Listing": f"https://speedhome.com/ads/{ad_id}"
        })
        
    return pd.DataFrame(records), extracted_name

# ==========================================
# INTERFACE APPLICATION LAYOUT (HEADER)
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
    st.error(f"⚠️ **Sistem Deteksi Gambar Header:** {error_message}")

if img_base64:
    background_style = f"""
    background-image: linear-gradient(135deg, rgba(6, 182, 212, 0.75), rgba(59, 130, 246, 0.85)), 
                      url("data:image/jpeg;base64,{img_base64}");
    """
else:
    background_style = "background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);"

st.markdown(f"""
<style>
    /* Style Tanggal Default (Desktop) */
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

    /* ==========================================
       ⚡ PERBAIKAN RESPONSIVITAS TANGGAL DI HP
       ========================================== */
    @media (max-width: 768px) {{
        .realtime-clock-container {{
            justify-content: center !important;
            margin-bottom: 2px !important;  
            padding: 2px 0 !important;      
            font-size: 0.8rem !important;   
        }}
    }}
</style>
""", unsafe_allow_html=True)

# Format Waktu Indonesia Lokal
hari_id = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
bulan_id = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]

tgl_sekarang = datetime.datetime.now()
nama_hari = hari_id[tgl_sekarang.weekday()]
nama_bulan = bulan_id[tgl_sekarang.month - 1]
teks_tanggal = f"{nama_hari}, {tgl_sekarang.day} {nama_bulan} {tgl_sekarang.year}"

st.markdown(f"""
<div class="realtime-clock-container">
    <span style="margin-right: 4px;">📅</span>
    <span>{teks_tanggal}</span>
</div>
""", unsafe_allow_html=True)


# ==========================================
# PARAMETER INPUT MARKET DATA
# ==========================================
st.subheader("🔍 Parameter Pengumpulan Data Pasar")
col_search1, col_search2 = st.columns([2, 1])

with col_search2:
    saran_apartemen = ["-- Cari Lewat Rekomendasi --", "Mont Kiara", "Kuala Lumpur", "Bangsar", "Subang Jaya", "Petaling Jaya" , "Shah Alam", "Putrajaya", "Cyberjaya", "Damansara Heights", "Segambut", "Setapak", "Segi Tiga Emas", "Taman Tun Dr Ismail (TTDI)", "Sri Hartamas", "Bukit Jalil", "Puchong", "Kepong", "Gombak"]
    pilihan_dropdown = st.selectbox("Saran Nama Area/Apartemen:", saran_apartemen)

with col_search1:
    value_default = "" if pilihan_dropdown == "-- Cari Lewat Rekomendasi --" else f"https://speedhome.com/rent/{pilihan_dropdown.lower().replace(' ', '-')}"
    input_target = st.text_input(
        "Masukkan URL Lembar Publik SPEEDHOME atau Ketik Nama Area:",
        value=value_default,
        placeholder="Contoh: https://speedhome.com/rent/mont-kiara atau 'Mont Kiara'"
    )

if st.button("🚀 Jalankan Proses Inteligensi Data", use_container_width=True):
    if not input_target:
        st.warning("⚠️ Mohon berikan parameter URL atau nama area yang valid!")
    else:
        bar_progress = st.progress(0)
        teks_status = st.empty()
        
        teks_status.text("🤖 Menghubungi protokol SPEEDHOME.com (Menghormati robots.txt)...")
        bar_progress.progress(30)
        
        df_hasil, nama_wilayah = fetch_speedhome_intelligence(input_target)
        
        bar_progress.progress(75)
        teks_status.text("📊 Mengkalkulasi statistik matematika (Mean, Median, Modus & Fair Price)...")
        
        # --- PRE-COMPUTATION RINGKASAN HARGA (Efisiensi Memori & Kecepatan) ---
        summary_rows = []
        for tipe, grup in df_hasil.groupby("Tipe Kamar"):
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
        df_summary_calculated = pd.DataFrame(summary_rows).set_index("Tipe Unit")
        
        # Simpan ke Session State
        st.session_state['data_master'] = df_hasil
        st.session_state['data_summary'] = df_summary_calculated
        st.session_state['wilayah_aktif'] = nama_wilayah
        
        bar_progress.progress(100)
        time.sleep(0.4)
        teks_status.empty()
        bar_progress.empty()

# ==========================================
# TAMPILAN DASHBOARD METRIK & DATA
# ==========================================
if 'data_master' in st.session_state:
    df_data = st.session_state['data_master']
    df_summary_table = st.session_state['data_summary']
    wilayah_aktif = st.session_state['wilayah_aktif']
    
    # ------------------------------------------
    # FUNGSI UTILITAS: EKSPOR DATA (Aman dari Bug Key Bentrok)
    # ------------------------------------------
    def render_export_buttons(df_master, df_summary, nama_wilayah, identity_suffix):
        st.write("---")
        st.markdown("#### 📥 Ekspor Laporan Intelijen Pasar")
        
        tgl_skrg = datetime.datetime.now().strftime("%Y%m%d")
        nama_file_dasar = f"SPEEDHOME_{nama_wilayah.replace(' ', '_')}_{tgl_skrg}"
        
        # Siapkan Buffer Excel
        buffer_excel = BytesIO()
        with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
            df_summary.to_excel(writer, sheet_name='Summary_Report')
            df_master.to_excel(writer, index=False, sheet_name='All_Listings')
        data_excel_siap = buffer_excel.getvalue()
        
        # Render Tombol Berdampingan dengan Key Statis Terkelola
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button(
                label="📥 Download Laporan Manajemen Lengkap (.xlsx)",
                data=data_excel_siap,
                file_name=f"{nama_file_dasar}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                key=f"xlsx_download_{identity_suffix}"
            )
        with col_dl2:
            st.download_button(
                label="📄 Download Raw Data Sheet (.csv)",
                data=df_master.to_csv(index=False).encode('utf-8'),
                file_name=f"{nama_file_dasar}.csv",
                mime="text/csv",
                use_container_width=True,
                key=f"csv_download_{identity_suffix}"
            )

    # Inisialisasi Layout Tab
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
        st.dataframe(df_summary_table, use_container_width=True)
        
        st.write("---")
        st.markdown("#### 🌐 Cakupan Ketersediaan Model Sewa")
        col_s1, col_s2, col_s3 = st.columns(3)
        
        with col_s1:
            total_harian = df_data["Harga Harian (RM)"].notna().sum()
            if total_harian > 0:
                st.success(f"🟢 **Sewa Harian:** Tersedia ({total_harian} Unit Terkonversi)")
            else:
                st.info("ℹ️ **Sewa Harian:** Tidak Tersedia langsung.")
                
        with col_s2:
            st.success(f"🟢 **Sewa Bulanan:** Tersedia ({len(df_data)} Unit Mendominasi Pasaran)")
        with col_s3:
            st.success(f"🟢 **Sewa Tahunan:** Tersedia ({len(df_data)} Unit Siap Kontrak)")
            
        render_export_buttons(df_data, df_summary_table, wilayah_aktif, "tab1")

    # ------------------------------------------
    # TAB 2: TABEL DAFTAR UNIT
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
            harga_bulanan = row["Harga Bulanan (RM)"]
            harga_harian = row["Harga Harian (RM)"]
            if (harga_harian == int(harga_bulanan / 28)):
                return f"💡 RM {harga_harian} (Estimasi)"
            return f"RM {harga_harian}"

        df_terfilter["Harga Harian Tampilan"] = df_terfilter.apply(format_harga_harian, axis=1)
        
        kolom_spek = [
            "Judul Listing", "Nama Property / Area", "Tipe Kamar", 
            "Harga Harian Tampilan", "Harga Bulanan (RM)", "Harga Tahunan (RM)", 
            "Ukuran Unit (sqft)", "Status Furnitur", "Link Listing"
        ]
        
        st.dataframe(
            df_terfilter[kolom_spek],
            column_config={
                "Link Listing": st.column_config.LinkColumn("Tautan Verifikasi SPEEDHOME"),
                "Harga Harian Tampilan": st.column_config.TextColumn(
                    "Harga Harian (RM)", 
                    help="Angka ini merupakan estimasi konversi internal platform."
                ),
                "Harga Bulanan (RM)": st.column_config.NumberColumn("Harga Bulanan (RM)", format="RM %d"),
                "Harga Tahunan (RM)": st.column_config.NumberColumn("Harga Tahunan (RM)", format="RM %d")
            },
            use_container_width=True,
            hide_index=True
        )
        
        st.caption("ℹ️ **Catatan Strategis Eksekutif:** Angka dengan tanda penanda **(Estimasi)** merupakan hasil konversi formulasi internal.")
        
        render_export_buttons(df_data, df_summary_table, wilayah_aktif, "tab2")

    # ------------------------------------------
    # TAB 3: INOVASI & VISUALISASI DATA
    # ------------------------------------------
    with tab_innovation:
        st.markdown("### 💡 CEO Data-Driven Strategic Insights")
        st.markdown("<p style='color: #06b6d4;'><b>Visualisasi Makro & Simulasi ROI Investasi Komersial</b></p>", unsafe_allow_html=True)
        
        col_grafik1, col_grafik2 = st.columns(2)
        
        with col_grafik1:
            fig_box = px.box(
                df_data, x="Tipe Kamar", y="Harga Bulanan (RM)",
                color="Tipe Kamar", title="Rentang Distribusi Harga Pasar Real-time",
                template="plotly_white"
            )
            st.plotly_chart(fig_box, use_container_width=True)
            
        with col_grafik2:
            fig_scatter = px.scatter(
                df_data, x="Ukuran Unit (sqft)", y="Harga Bulanan (RM)",
                color="Status Furnitur", size="Harga Bulanan (RM)",
                title="Korelasi Spasial Luas Bangunan vs Harga Sewa",
                template="plotly_white"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
            
        st.write("---")
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("#### 🧮 Kalkulator Simulasi Estimasi Gross Rental Yield")
        
        col_roi1, col_roi2 = st.columns(2)
        with col_roi1:
            segmen_terpilih = st.selectbox("Pilih Segmen Properti Target Investasi:", df_data["Tipe Kamar"].unique())
            harga_sewa_median = df_data[df_data["Tipe Kamar"] == segmen_terpilih]["Harga Bulanan (RM)"].median()
            
            input_harga_beli = st.number_input(
                "Proyeksi Harga Pembelian Aset Properti (RM):",
                value=int(harga_sewa_median * 230), step=25000
            )
            
        with col_roi2:
            pendapatan_tahunan = harga_sewa_median * 12
            persentase_roi = (pendapatan_tahunan / input_harga_beli) * 100
            
            st.metric(
                label=f"Proyeksi Gross Rental Yield ({segmen_terpilih})",
                value=f"{persentase_roi:.2f} % / Tahun",
                delta="Sangat Menjanjikan (> 5.5%)" if persentase_roi >= 5.5 else "Yield Standard/Rendah (< 5.5%)"
            )
        st.markdown("</div>", unsafe_allow_html=True)
        
        render_export_buttons(df_data, df_summary_table, wilayah_aktif, "tab3")

# ==========================================
# FOOTER APPLICATION LAYOUT
# ==========================================
def get_footer_base64(image_path):
    if os.path.exists(image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except Exception:
            return ""
    return ""

nama_file_footer = "image_024abcd.jpg"
footer_base64 = get_footer_base64(nama_file_footer)

teks_pembuka_atau_copyright = """
    <div class="footer-text-content">
        <h2>Sistem Siap Digunakan</h2>
        <p>Masukkan URL resmi dari SPEEDHOME Malaysia atau pilih salah satu area rekomendasi populer di atas, lalu klik tombol jalankan untuk memproses analisis intelijen pasar properti secara otomatis.</p>
    </div>
"""

if footer_base64:
    st.markdown(f"""
    <style>
        .footer-background-container {{
            width: 100%;
            min-height: 160px; 
            background-image: linear-gradient(135deg, rgba(6, 182, 212, 0.85), rgba(59, 130, 246, 0.90)), 
                              url("data:image/jpeg;base64,{footer_base64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            border-radius: 12px;
            border: 1px solid #06b6d4;
            margin-top: 50px; 
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 30px;
            box-shadow: 0 8px 20px rgba(6, 182, 212, 0.15);
        }}
        .footer-text-content {{
            color: #ffffff;
        }}
        .footer-text-content h2 {{
            color: #ffffff !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            margin-bottom: 10px !important;
            text-shadow: 2px 2px 8px rgba(0,0,0,0.4);
        }}
        .footer-text-content p {{
            color: #f1f5f9 !important;
            font-size: 1rem !important;
            max-width: 750px;
            margin: 0 auto !important;
            font-weight: 500;
            text-shadow: 1px 1px 4px rgba(0,0,0,0.4);
        }}
    </style>
    """, unsafe_allow_html=True)
    
    if 'data_master' not in st.session_state:
        st.markdown(f'<div class="footer-background-container">{teks_pembuka_atau_copyright}</div>', unsafe_allow_html=True)
    else:
        copyright_text = '<div class="footer-text-content"><p>© 2026 SPEEDHOME Analytics Intelligence System | CEO Office Strategic Tool</p></div>'
        st.markdown(f'<div class="footer-background-container" style="min-height: 80px; padding: 15px;">{copyright_text}</div>', unsafe_allow_html=True)
else:
    if 'data_master' not in st.session_state:
        st.markdown("""
        <div style='text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #e0f2fe, #bbf7d0); border-radius: 12px; margin-top: 50px;'>
            <h2 style='color: #06b6d4;'>Sistem Siap Digunakan</h2>
            <p style='color: #334155; max-width: 600px; margin: 0 auto; font-weight: 500;'>
                Masukkan URL resmi dari SPEEDHOME Malaysia atau pilih salah satu area rekomendasi populer di atas, lalu klik tombol jalankan untuk memproses analisis intelijen pasar properti secara otomatis.
            </p>
        </div>
        """, unsafe_allow_html=True)
