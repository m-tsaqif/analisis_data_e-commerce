import streamlit as st

def local_css():
    """
    Menerapkan CSS kustom untuk aplikasi Streamlit.
    
    Fungsi ini menambahkan styling untuk:
    - Tombol utama dan sidebar
    - Header dan subheader
    - Blok pertanyaan, kesimpulan, dan rekomendasi
    - Highlight teks dan gradient header
    """
    st.markdown(f"""
        <style>
            .stButton>button {{
                background-color: #1a5fb4;
                color: white !important;
                border-radius: 5px;
                padding: 12px 16px;
                margin: 8px 0;
                font-weight: bold;
                cursor: pointer;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                border: none;
                width: 100%;
            }}
            
            .stButton>button:hover {{
                background-color: #0d47a1;
                color: white !important;
                transform: scale(1.05);
                box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
            }}
            
            .sidebar .stButton>button {{
                color: white !important;
                background-color: #1a5fb4;
            }}
            
            .sidebar .stButton>button:hover {{
                color: white !important;
                background-color: #0d47a1;
            }}

            .main h1 {{
                color: #1e3c72 !important;
                border-bottom: 3px solid #ffd700;
                padding-bottom: 8px;
                margin-bottom: 1.5rem !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            .main h2 {{
                color: #1a5fb4 !important;
                margin-top: 1.8rem !important;
                padding-left: 10px;
                border-left: 4px solid #ffd700;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            .pertanyaan {{
                background-color: #e6f0ff;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #1a5fb4;
                margin: 15px 0;
                font-style: italic;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            .kesimpulan {{
                background-color: white;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #ffd700;
                margin: 15px 0;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            .rekomendasi {{
                background-color: #fff9e6;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #1e3c72;
                margin: 15px 0;
                font-weight: bold;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            .main ul {{
                padding-left: 20px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            .main li {{
                margin-bottom: 8px;
            }}
            
            .highlight {{
                color: #1e3c72;
                font-weight: bold;
            }}
            
            .gradient-header {{
                background: linear-gradient(90deg, #1a5fb4, #3584e4);
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 25px;
            }}
            
            .gradient-header h1 {{
                color: white !important;
                margin: 0;
                border-bottom: none !important;
            }}
        </style>
        """, unsafe_allow_html=True)

def show_main_header():
    """
    Menampilkan header utama dengan gradient background.
    """
    st.markdown("""
    <div style='background: linear-gradient(90deg, #1a5fb4, #3584e4); padding: 15px; border-radius: 10px; margin-bottom: 25px;'>
        <h1 style='color: white; margin: 0;'>💡 Kesimpulan Analisis</h1>
    </div>
    """, unsafe_allow_html=True)

def show_question1_section():
    """
    Menampilkan bagian untuk pertanyaan pertama tentang prediksi visual tren.
    """
    st.markdown("""
    #### Pertanyaan 1: Membuat Prediksi (Visual Tren)
    """)
    
    st.markdown("""
    <div class="pertanyaan">
    <strong>Bagaimana perubahan nilai rata-rata pembayaran pelanggan dari waktu ke waktu selama 12 bulan terakhir, dan adakah periode tertentu yang menunjukkan tren kenaikan atau penurunan signifikan?</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="kesimpulan">
    <strong>Kesimpulan:</strong>
    <ul>
        <li><span class="highlight">Tren nilai rata-rata pembayaran pelanggan relatif stabil</span> selama 12 bulan terakhir, dengan <span class="highlight">fluktuasi kecil antar bulan</span>.</li>
        <li>Terlihat <span class="highlight">ada kenaikan yang lebih menonjol menjelang akhir tahun</span> (mungkin dipicu oleh musim belanja seperti promo akhir tahun, Harbolnas, atau libur panjang).</li>
        <li><span class="highlight">Tidak terdapat penurunan signifikan yang konsisten</span>, meskipun ada sedikit penurunan sesaat di bulan-bulan tengah tahun.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="rekomendasi">
    <strong>Rekomendasi:</strong> Perusahaan dapat mempertimbangkan meningkatkan aktivitas promosi di kuartal akhir karena respons positif pasar terhadap harga dan belanja.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

def show_question2_section():
    """
    Menampilkan bagian untuk pertanyaan kedua tentang menemukan hubungan.
    """
    st.markdown("""
    #### Pertanyaan 2: Menemukan Hubungan
    """)
    
    st.markdown("""
    <div class="pertanyaan">
    <strong>Bagaimana hubungan antara harga produk dan biaya pengiriman dalam data pesanan?</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="kesimpulan">
    <strong>Kesimpulan:</strong>
    <ul>
        <li>Terdapat <span class="highlight">korelasi positif lemah</span> antara harga produk dan ongkos kirim (~0.41), yang menunjukkan bahwa <span class="highlight">produk mahal cenderung memiliki ongkir lebih tinggi</span>, tapi <span class="highlight">tidak selalu</span>.</li>
        <li>Berdasarkan analisis distribusi:
        <ul>
            <li><span class="highlight">Mayoritas ongkir tidak proporsional terhadap harga</span>; rasio ongkir/harga produk cenderung rendah, banyak di bawah 0.25.</li>
            <li><span class="highlight">Produk sangat mahal</span> justru menunjukkan <span class="highlight">variasi ongkir yang lebih besar</span>, terlihat dari sebaran outlier yang tinggi di boxplot kelompok harga.</li>
            <li>Ada indikasi bahwa <span class="highlight">berat atau dimensi fisik produk</span> mungkin lebih menentukan ongkir dibanding harganya.</li>
        </ul>
        </li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="rekomendasi">
    <strong>Rekomendasi:</strong> Perlu dilakukan analisis lebih lanjut berdasarkan fitur seperti berat produk atau lokasi pengiriman untuk memahami faktor penentu utama ongkir.
    </div>
    """, unsafe_allow_html=True)

def app():
    """
    Fungsi utama untuk menjalankan aplikasi Streamlit.
    Mengatur tata letak dan alur aplikasi analisis data.
    """
    
    # Menerapkan CSS kustom
    local_css()
    
    # Menampilkan header utama
    show_main_header()
    
    # Menampilkan bagian pertanyaan pertama
    show_question1_section()
    
    # Menampilkan bagian pertanyaan kedua
    show_question2_section()

if __name__ == "__main__":
    app()