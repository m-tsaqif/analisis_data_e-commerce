import streamlit as st
from PIL import Image

def local_css():
    """
    Menerapkan tema kustom.
    
    Fungsi ini menambahkan CSS kustom untuk:
    - Header dan judul
    - Kartu profil dan penelitian
    - Tombol dan elemen UI lainnya
    - Warna aksen dan border
    """
    st.markdown("""
    <style>
        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        
        .profile-card {
            background-color: #ffffff;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            border: 2px solid #FFD700;
        }
        
        .profile-img {
            border-radius: 50%;
            width: 150px;
            height: 150px;
            object-fit: cover;
            margin-right: 2rem;
            border: 5px solid #1e3c72;
        }
        
        .research-card {
            background-color: #f8f9fa;
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border-left: 5px solid #FFD700;
        }
        
        .research-card h3 {
            color: #1e3c72;
            margin-top: 0;
        }
        
        .footer {
            text-align: center;
            margin-top: 2rem;
            padding: 1rem;
            color: #1e3c72;
            border-top: 1px solid #FFD700;
        }
        
        .ecommerce-bg {
            background: linear-gradient(rgba(30, 60, 114, 0.8), rgba(30, 60, 114, 0.8)), 
                        url('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTatmCOYtH1oyCaySYCRSdz8xdx18Gb2Araxw&s');
            background-size: cover;
            background-position: center;
            padding: 3rem;
            border-radius: 10px;
            color: white;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
            margin-bottom: 2rem;
        }
        
        .stButton>button {
            background-color: #1a5fb4;
            color: white;
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
        }
        
        .stButton>button:hover {
            background-color: #0d47a1;
            color: white;
            transform: scale(1.05);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
        }
        
        .stButton>button:focus:not(:active) {
            background-color: #1a5fb4;
            color: white;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
        }
        
        .highlight-blue {
            color: #1e3c72;
            font-weight: bold;
        }
        
        .highlight-yellow {
            color: #FFD700;
            font-weight: bold;
        }
        
        .border-yellow {
            border: 1px solid #FFD700;
            border-radius: 5px;
            padding: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

def show_header():
    """
    Menampilkan header aplikasi dengan background e-commerce.
    """
    st.markdown("""
    <div class="ecommerce-bg">
        <h1 style="margin:0; font-size:2.5rem;">Proyek Analisis Data: E-Commerce Datasets</h1>
        <p style="margin:0; font-size:1.2rem; opacity:0.9;">Analisis Tren dan Pola Pembelian Pelanggan</p>
    </div>
    """, unsafe_allow_html=True)

def show_profile_section():
    """
    Menampilkan bagian profil pengguna dengan foto dan informasi kontak.
    """
    with st.container():
        col1, col2 = st.columns([1, 4])
        
        with col1:
            try:
                profile_img = Image.open("img/foto_tsaqif.png")
                st.image(profile_img, 
                         caption='Muhammad Tsaqif', 
                         use_container_width=False, 
                         width=180)
            except FileNotFoundError:
                st.error("Foto tidak ditemukan di img/foto_tsaqif.png")
            except Exception as e:
                st.error(f"Error saat memuat gambar: {str(e)}")
        
        with col2:
            st.markdown(
                """
                <div>
                    <h2 style="color:#1e3c72;">Muhammad Tsaqif</h2>
                    <p><strong>Email:</strong> mtsaqif08@gmail.com</p>
                    <p><strong>ID Dicoding:</strong> MC004D5Y2062</p>
                    <p>Data Analyst dengan spesialisasi dalam analisis data e-commerce dan perilaku konsumen.</p>
                </div>
                """,
                unsafe_allow_html=True
            )

def show_research_questions():
    """
    Menampilkan pertanyaan penelitian dalam bentuk kartu.
    """
    st.markdown("## 🎯 Pertanyaan Bisnis")

    st.markdown("""
    <div class="research-card">
        <h3>📈 Membuat Prediksi (Visual Tren)</h3>
        <p><i>"Bagaimana perubahan nilai rata-rata pembayaran pelanggan dari waktu ke waktu selama 12 bulan terakhir, 
        dan adakah periode tertentu yang menunjukkan tren kenaikan atau penurunan signifikan?"</i></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="research-card">
        <h3>🔗 Menemukan Hubungan</h3>
        <p><i>"Bagaimana hubungan antara harga produk dan biaya pengiriman dalam data pesanan?"</i></p>
    </div>
    """, unsafe_allow_html=True)

def show_footer():
    """
    Menampilkan footer aplikasi.
    """
    st.markdown("""
    <div class="footer">
        <p>© 2023 Muhammad Tsaqif - Proyek Analisis Data E-Commerce</p>
    </div>
    """, unsafe_allow_html=True)

def app():

    # Menerapkan tema kustom
    local_css()
    
    # Menampilkan header
    show_header()
    
    # Menampilkan bagian profil
    show_profile_section()
    
    # Menampilkan pertanyaan penelitian
    show_research_questions()
    
    # Menampilkan footer
    show_footer()

if __name__ == "__main__":
    app()