import streamlit as st
import pandas as pd
import os
from pathlib import Path

def local_css():
    """
    Menerapkan tema kustom dengan CSS.
    
    Fungsi ini menambahkan styling untuk:
    - Background utama
    - Tombol dan elemen interaktif
    - Kartu dataset dan insight
    - Header dan typography
    - Tabel dan expander
    """
    st.markdown(f"""
    <style>
        .main {{
            background-color: #f5f9ff;
        }}
        
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
        
        .stSelectbox, .stDataFrame, .stTextInput, .stNumberInput {{
            border: 1px solid #4a90e2;
            border-radius: 5px;
        }}
        
        .dataset-card {{
            padding: 15px;
            border-radius: 10px;
            background: linear-gradient(145deg, #e6f0ff, #ffffff);
            border-left: 4px solid #ffd700;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        }}
        
        .insight-card {{
            padding: 15px;
            border-radius: 10px;
            background: #fff9e6;
            border-left: 4px solid #1e3c72;
            margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .dataset-card h5 {{
            color: #1a5fb4;
            margin-bottom: 8px !important;
        }}
        
        .dataset-card p {{
            color: #333333;
            margin: 5px 0 !important;
        }}
        
        .stHeader {{
            color: #1e3c72 !important;
            font-weight: bold !important;
        }}
        
        .st-expander {{
            border: 1px solid #4a90e2;
            border-radius: 5px;
        }}
        
        .st-expander-header {{
            background-color: #e6f0ff !important;
            color: #1e3c72 !important;
            font-weight: bold !important;
        }}
        
        hr {{
            border-top: 2px dashed #ffd700;
            margin: 20px 0;
        }}
        
        .highlight-blue {{
            color: #1e3c72;
            font-weight: bold;
        }}
        
        .highlight-yellow {{
            color: #FFD700;
            font-weight: bold;
        }}
        
        .stDataFrame {{
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
    </style>
    """, unsafe_allow_html=True)

def get_filenames(folder_path):
    """
    Mengambil daftar nama file dalam sebuah folder.
    
    Parameters:
        folder_path (str): Path menuju folder yang ingin dipindai
        
    Returns:
        list: Daftar nama file dalam folder tersebut
    """
    try:
        return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    except FileNotFoundError:
        st.error(f"Folder '{folder_path}' tidak ditemukan.")
        return []

def read_csv_datasets(file_list, folder_path="datasets"):
    """
    Membaca file CSV dari daftar nama file dan mengembalikan dictionary of DataFrames.
    
    Parameters:
        file_list (list): Daftar nama file
        folder_path (str): Path folder tempat file-file disimpan (default: 'datasets')
        
    Returns:
        dict: Dictionary dengan format {nama_file: DataFrame}
    """
    datasets = {}
    for file in file_list:
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            try:
                dataset_name = os.path.splitext(file)[0]
                datasets[dataset_name] = pd.read_csv(file_path)
            except Exception as e:
                st.error(f"Gagal membaca file {file}: {str(e)}")
    return datasets

def show_dataset_card(selected_dataset, df):
    """
    Menampilkan kartu informasi dataset dalam format yang rapi.
    
    Parameters:
        selected_dataset (str): Nama dataset yang dipilih
        df (DataFrame): Dataframe yang berisi data dataset
    """
    st.markdown(f"""
        <div class='dataset-card'>
            <h5>📁 Dataset: {selected_dataset}</h5>
            <p>🔢 Jumlah Baris: {df.shape[0]:,}</p>
            <p>📊 Jumlah Kolom: {df.shape[1]}</p>
            <p>💾 Ukuran Memori: {df.memory_usage(deep=True).sum()/1024/1024:.2f} MB</p>
        </div>
    """, unsafe_allow_html=True)

def show_dataset_overview(datasets):
    """
    Menampilkan overview dataset yang telah dimuat dalam bentuk interaktif.
    
    Parameters:
        datasets (dict): Dictionary berisi dataset yang telah dimuat
    """
    st.header("📂 Dataset Loaded", divider='blue')
    
    if not datasets:
        st.warning("Belum ada dataset yang dimuat.")
        return
    
    selected_dataset = st.selectbox(
        "Pilih Dataset",
        list(datasets.keys()),
        help="Pilih dataset yang ingin Anda lihat"
    )
    
    if selected_dataset:
        df = datasets[selected_dataset]
        show_dataset_card(selected_dataset, df)
        
        with st.expander(f"🔍 Lihat isi dataset {selected_dataset}", expanded=False):
            st.dataframe(df, use_container_width=True)
        
        with st.expander(f"📊 Statistik Deskriptif {selected_dataset}", expanded=False):
            st.write(df.describe())

def show_insight_card(title, datasets, description):
    """
    Menampilkan kartu insight analitik dengan format yang konsisten.
    
    Parameters:
        title (str): Judul insight
        datasets (list): Daftar dataset yang relevan
        description (str): Deskripsi insight
    """
    st.markdown(f"""
    <div class='insight-card'>
        <h3 style='color: #1a5fb4; margin-top: 0;'>{title}</h3>
        <p><strong>Dataset yang relevan:</strong></p>
        <ul>
            {''.join([f"<li><span style='color: #1a5fb4;'>{dataset}</span></li>" for dataset in datasets])}
        </ul>
        <p style='color: #666; font-style: italic;'>{description}</p>
    </div>
    """, unsafe_allow_html=True)

def show_analytical_insights():
    """
    Menampilkan bagian insight analitik dengan kartu-kartu yang informatif.
    """
    st.header("💡 Insight Analitik", divider='blue')
    
    show_insight_card(
        "1. Membuat Prediksi (Visual Tren)",
        ["order_payments_dataset", "orders_dataset"],
        "Dataset ini digunakan untuk menganalisis tren penjualan."
    )
    
    show_insight_card(
        "2. Menemukan Hubungan",
        ["order_items_dataset"],
        "Analisis hubungan antara harga produk dengan biaya pengiriman untuk menemukan pola menarik."
    )
    
    st.success("✨ Insight ini akan digunakan untuk membuat visualisasi tren dan menemukan hubungan pada tahap selanjutnya.")

def show_main_header():
    """
    Menampilkan header utama aplikasi dengan gradient biru.
    """
    st.markdown("""
    <div style='background: linear-gradient(90deg, #1a5fb4, #3584e4); padding: 15px; border-radius: 10px; margin-bottom: 25px;'>
        <h1 style='color: white; margin: 0;'>📈 Dataset Overview</h1>
    </div>
    """, unsafe_allow_html=True)

def app():

    # Menerapkan CSS kustom untuk seluruh aplikasi
    local_css()
    
    # Menampilkan header utama aplikasi
    show_main_header()
    
    # Mendapatkan path folder datasets
    folder_path = Path(__file__).parent.parent / 'datasets'
    
    # Mengambil daftar file dan membaca dataset
    file_list = get_filenames(folder_path)
    datasets = read_csv_datasets(file_list, folder_path)
    
    # Menampilkan overview dataset yang telah dimuat
    show_dataset_overview(datasets)
    
    # Menambahkan divider visual
    st.markdown("---")
    
    # Menampilkan insight analitik
    show_analytical_insights()

if __name__ == "__main__":
    app()