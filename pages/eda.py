import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import os
from pathlib import Path

BLUE_PALETTE = ["#1f77b4", "#4e79a7", "#5c8ab8", "#7eb0d5", "#a5c8e0"]
YELLOW_PALETTE = ["#ffbb00", "#ffcc33", "#ffdd66", "#ffee99", "#fff6cc"]
BACKGROUND_COLOR = "#f8f9fa"

def get_base_dir():
    """
    Mengembalikan path absolut ke direktori utama proyek.
    
    Returns:
        Path: Objek Path yang menunjuk ke direktori utama proyek
    """
    return Path(__file__).parent.parent  # Naik dua tingkat dari pages/

def get_dataset_paths():
    """
    Mendefinisikan path ke dataset yang digunakan dalam aplikasi.
    
    Returns:
        tuple: Tuple berisi path untuk (payments, orders, order_items)
    """
    BASE_DIR = get_base_dir()
    return (
        os.path.join(BASE_DIR, 'datasets', 'order_payments_dataset.csv'),
        os.path.join(BASE_DIR, 'datasets', 'orders_dataset.csv'),
        os.path.join(BASE_DIR, 'datasets', 'order_items_dataset.csv')
    )

def local_css():
    """
    Menerapkan tema kustom CSS.
    
    Menambahkan CSS untuk:
    - Warna dan tata letak utama
    - Tombol dan elemen interaktif
    - Kartu dataset dan insight
    - Tipografi dan highlight
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

def load_payments_data():
    """
    Memuat dataset pembayaran dan pesanan dari file CSV.
    
    Returns:
        tuple: (payments_df, orders_dataset) - DataFrame pembayaran dan pesanan
        
    Raises:
        st.error: Menampilkan pesan error jika file tidak ditemukan
    """
    PAYMENTS_PATH, ORDERS_PATH, _ = get_dataset_paths()
    try:
        payments_df = pd.read_csv(PAYMENTS_PATH)
        orders_dataset = pd.read_csv(ORDERS_PATH)
        return payments_df, orders_dataset
    except FileNotFoundError as e:
        st.error(f"File dataset tidak ditemukan: {e}")
        st.error(f"Memeriksa path: {PAYMENTS_PATH}")
        st.stop()

def load_order_items():
    """
    Memuat dataset item pesanan dari file CSV.
    
    Returns:
        pd.DataFrame: DataFrame item pesanan
        
    Raises:
        st.error: Menampilkan pesan error jika file tidak ditemukan
    """
    _, _, ORDER_ITEMS_PATH = get_dataset_paths()
    try:
        return pd.read_csv(ORDER_ITEMS_PATH)
    except FileNotFoundError as e:
        st.error(f"File dataset tidak ditemukan: {e}")
        st.error(f"Memeriksa path: {ORDER_ITEMS_PATH}")
        st.stop()

def preprocess_payments_data(payments_df, orders_dataset):
    """
    Melakukan preprocessing data pembayaran dan pesanan.
    
    Parameters:
        payments_df (pd.DataFrame): Data pembayaran
        orders_dataset (pd.DataFrame): Data pesanan
        
    Returns:
        pd.DataFrame: Data yang sudah diproses dengan kolom tambahan
    """
    processed_df = pd.merge(
        payments_df[['order_id', 'payment_value']],
        orders_dataset[['order_id', 'order_purchase_timestamp']],
        on='order_id',
        how='inner'
    )
    processed_df['order_purchase_timestamp'] = pd.to_datetime(processed_df['order_purchase_timestamp'])

    latest_date = processed_df['order_purchase_timestamp'].max()
    start_date = latest_date - pd.DateOffset(months=12)
    filtered_df = processed_df[
        (processed_df['order_purchase_timestamp'] >= start_date) &
        (processed_df['order_purchase_timestamp'] <= latest_date)
    ].copy()
    
    filtered_df['month_year'] = filtered_df['order_purchase_timestamp'].dt.to_period('M')
    
    return filtered_df

def calculate_monthly_stats(filtered_df):
    """
    Menghitung statistik bulanan dari data pembayaran.
    
    Parameters:
        filtered_df (pd.DataFrame): Data pembayaran yang sudah difilter
        
    Returns:
        pd.DataFrame: Data statistik bulanan
    """
    monthly_stats = filtered_df.groupby('month_year')['payment_value'].agg(['count', 'mean', 'median', 'sum']).reset_index()
    monthly_stats.columns = ['Bulan', 'Jumlah Transaksi', 'Rata-rata Pembayaran', 'Median Pembayaran', 'Total Pembayaran']
    monthly_stats['Bulan'] = monthly_stats['Bulan'].astype(str)
    return monthly_stats

def create_payment_trend_chart(monthly_stats):
    """
    Membuat visualisasi tren pembayaran dan transaksi.
    
    Parameters:
        monthly_stats (pd.DataFrame): Data statistik bulanan
        
    Returns:
        plotly.graph_objects.Figure: Figure Plotly yang sudah dikonfigurasi
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(
        x=monthly_stats['Bulan'],
        y=monthly_stats['Total Pembayaran'],
        mode='lines+markers',
        name='Total Pembayaran',
        line=dict(color=BLUE_PALETTE[0], width=3),
        marker=dict(color=BLUE_PALETTE[0], size=8),
        hovertemplate='Bulan: %{x}<br>Rp%{y:,.0f}<extra></extra>'
    ), secondary_y=False)

    fig.add_trace(go.Bar(
        x=monthly_stats['Bulan'],
        y=monthly_stats['Jumlah Transaksi'],
        name='Jumlah Transaksi',
        marker_color=YELLOW_PALETTE[0],
        opacity=0.7,
        hovertemplate='Bulan: %{x}<br>%{y:,} transaksi<extra></extra>'
    ), secondary_y=True)

    fig.update_layout(
        title='<b>Tren Pembayaran dan Volume Transaksi</b>',
        title_font=dict(size=18, color=BLUE_PALETTE[0], family="Arial"),
        xaxis=dict(
            title='Bulan',
            title_font=dict(size=14, color=BLUE_PALETTE[0]),
            tickfont=dict(size=12),
            gridcolor='rgba(0,0,0,0.05)',
            showline=True,
            linecolor=BLUE_PALETTE[0],
            linewidth=1
        ),
        yaxis=dict(
            title='Total Pembayaran (Rp)',
            title_font=dict(size=14, color=BLUE_PALETTE[0]),
            tickfont=dict(size=12),
            gridcolor='rgba(0,0,0,0.05)',
            showline=True,
            linecolor=BLUE_PALETTE[0],
            linewidth=1
        ),
        yaxis2=dict(
            title='Jumlah Transaksi',
            title_font=dict(size=14, color=YELLOW_PALETTE[0]),
            tickfont=dict(size=12),
            gridcolor='rgba(0,0,0,0.05)',
            showline=True,
            linecolor=YELLOW_PALETTE[0],
            linewidth=1
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=12)
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=50, r=50, b=50, t=80, pad=4),
        height=500
    )
    
    return fig

def show_key_insights():
    """
    Menampilkan kartu insight utama dalam layout kolom.
    """
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div style="background-color:{BLUE_PALETTE[4]};padding:15px;border-radius:10px;margin-bottom:20px;">
            <h4 style="color:{BLUE_PALETTE[0]};margin-top:0;">📈 Tren Pembayaran</h4>
            <ul style="color:#333;">
                <li>Total pembayaran stabil meski jumlah transaksi bervariasi, menandakan rata-rata nilai transaksi konsisten.</li>
                <li>Kenaikan kecil pada pembayaran April–Juli 2018 mengindikasikan peningkatan rata-rata nilai transaksi.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background-color:{YELLOW_PALETTE[4]};padding:15px;border-radius:10px;margin-bottom:20px;">
            <h4 style="color:{YELLOW_PALETTE[0]};margin-top:0;">📊 Volume Transaksi</h4>
            <ul style="color:#333;">
                <li>Lonjakan transaksi dari Oktober ke November 2017, mengindikasikan kampanye atau promosi yang efektif.</li>
                <li>Stabil tinggi Desember 2017–Agustus 2018, dengan puncak transaksi pada Maret–Mei 2018.</li>
                <li>Penurunan drastis pada September–Oktober 2018 kemungkinan disebabkan oleh data yang tidak lengkap.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_price_shipping_analysis(order_items_dataset):
    """
    Menampilkan analisis harga dan biaya pengiriman dalam bentuk tab.
    
    Parameters:
        order_items_dataset (pd.DataFrame): Data item pesanan
    """
    st.subheader('📦 Analisis Harga dan Biaya Pengiriman')
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Statistik Dasar", 
        "📈 Korelasi", 
        "📦 Distribusi Ongkir", 
        "📉 Rasio Ongkir"
    ])
    
    with tab1:
        show_basic_stats(order_items_dataset)
    
    with tab2:
        show_correlation_analysis(order_items_dataset)
    
    with tab3:
        show_shipping_distribution(order_items_dataset)
    
    with tab4:
        show_shipping_ratio_analysis(order_items_dataset)

def show_basic_stats(order_items_dataset):
    """
    Menampilkan statistik dasar harga dan biaya pengiriman.
    
    Parameters:
        order_items_dataset (pd.DataFrame): Data item pesanan
    """
    st.markdown(f"""
    <div style="background-color:{BLUE_PALETTE[0]};padding:15px;border-radius:10px;margin-bottom:20px;box-shadow:0 4px 6px rgba(0,0,0,0.1);">
        <h4 style="color:white;margin:0;text-align:center;">Ringkasan Statistik Harga dan Biaya Pengiriman</h4>
    </div>
    """, unsafe_allow_html=True)
    
    stats = order_items_dataset[['price', 'freight_value']].describe().loc[['mean', 'std', 'min', '25%', '50%', '75%', 'max']]
    st.dataframe(
        stats.style.format("{:.2f}")
        .background_gradient(cmap='Blues', subset=['price'])
        .background_gradient(cmap='YlOrBr', subset=['freight_value'])
        .set_properties(**{
            'font-family': 'Arial',
            'border': '1px solid #f0f0f0'
        }),
        use_container_width=True
    )
    
    st.markdown(f"""
    <div style="background-color:#f8f9fa;padding:15px;border-radius:10px;border-left:4px solid {BLUE_PALETTE[0]};margin-top:20px;">
        <h5 style="color:{BLUE_PALETTE[0]};margin-top:0;">📊 Insights:</h5>
        <ul style="margin-bottom:0;">
            <li><b>Harga rata-rata produk:</b> Rp120.65 (standar deviasi Rp183.63)</li>
            <li><b>Ongkir rata-rata:</b> Rp19.99 (standar deviasi Rp15.81)</li>
            <li>Penyebaran sangat besar pada kedua variabel (terdapat outlier ekstrem)</li>
            <li>75% produk memiliki harga di bawah Rp139.90 dan ongkir di bawah Rp28.89</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def show_correlation_analysis(order_items_dataset):
    """
    Menampilkan analisis korelasi antara harga dan biaya pengiriman.
    
    Parameters:
        order_items_dataset (pd.DataFrame): Data item pesanan
    """
    st.markdown(f"""
    <div style="background-color:{BLUE_PALETTE[0]};padding:15px;border-radius:10px;margin-bottom:20px;box-shadow:0 4px 6px rgba(0,0,0,0.1);">
        <h4 style="color:white;margin:0;text-align:center;">Hubungan Harga Produk dan Biaya Pengiriman</h4>
    </div>
    """, unsafe_allow_html=True)
    
    correlation = order_items_dataset[['price', 'freight_value']].corr().iloc[0, 1]
    
    fig_corr = px.scatter(
        order_items_dataset.sample(frac=0.1),
        x='price',
        y='freight_value',
        color_discrete_sequence=[BLUE_PALETTE[1]],
        opacity=0.6,
        trendline="lowess",
        trendline_color_override=YELLOW_PALETTE[1],
        labels={
            'price': 'Harga Produk (Rp)',
            'freight_value': 'Biaya Pengiriman (Rp)'
        }
    )
    
    fig_corr.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        margin=dict(l=20, r=20, t=60, b=20),
        title={
            'text': f"<b>Korelasi: {correlation:.2f} (Hubungan Positif Sedang)</b>",
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="<b>Harga Produk (Rp)</b>",
        yaxis_title="<b>Biaya Pengiriman (Rp)</b>"
    )
    fig_corr.update_traces(
        marker=dict(size=5, line=dict(width=0.5, color='DarkSlateGrey'))
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    st.markdown(f"""
    <div style="background-color:#f8f9fa;padding:15px;border-radius:10px;border-left:4px solid {BLUE_PALETTE[0]};margin-top:20px;">
        <h5 style="color:{BLUE_PALETTE[0]};margin-top:0;">📊 Insights:</h5>
        <ul style="margin-bottom:0;">
            <li><b>Korelasi Pearson:</b> {correlation:.2f} (hubungan positif sedang)</li>
            <li>Produk lebih mahal cenderung memiliki biaya pengiriman lebih tinggi</li>
            <li>Hubungan tidak terlalu kuat - terdapat banyak variasi dalam pola</li>
            <li>Tren LOWESS menunjukkan hubungan non-linear yang menarik</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def show_shipping_distribution(order_items_dataset):
    """
    Menampilkan distribusi biaya pengiriman berdasarkan kelompok harga.
    
    Parameters:
        order_items_dataset (pd.DataFrame): Data item pesanan
    """
    st.markdown(f"""
    <div style="background-color:{BLUE_PALETTE[0]};padding:15px;border-radius:10px;margin-bottom:20px;box-shadow:0 4px 6px rgba(0,0,0,0.1);">
        <h4 style="color:white;margin:0;text-align:center;">Distribusi Biaya Pengiriman Berdasarkan Kelompok Harga</h4>
    </div>
    """, unsafe_allow_html=True)

    order_items_dataset['price_group'] = pd.qcut(
        order_items_dataset['price'],
        q=4,
        labels=['Murah', 'Sedang', 'Mahal', 'Sangat Mahal']
    )

    order_items_dataset['price_group'] = pd.Categorical(
        order_items_dataset['price_group'],
        categories=['Murah', 'Sedang', 'Mahal', 'Sangat Mahal'],
        ordered=True
    )

    color_sequence = [BLUE_PALETTE[1], BLUE_PALETTE[2], BLUE_PALETTE[3], BLUE_PALETTE[4]]

    fig_box = px.box(
        order_items_dataset,
        x='price_group',
        y='freight_value',
        color='price_group',
        color_discrete_sequence=color_sequence,
        points='all',
        hover_data=['price'],
        labels={
            'price_group': 'Kelompok Harga',
            'freight_value': 'Biaya Pengiriman (Rp)',
            'price': 'Harga Produk (Rp)'
        }
    )
    
    fig_box.update_layout(
        xaxis_title="<b>Kelompok Harga</b>",
        yaxis_title="<b>Biaya Pengiriman (Rp)</b>",
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        margin=dict(l=20, r=20, t=30, b=20),
        boxgap=0.3,
        boxgroupgap=0.3,
        xaxis=dict(
            categoryorder='array',
            categoryarray=['Murah', 'Sedang', 'Mahal', 'Sangat Mahal']
        )
    )
    
    fig_box.update_traces(
        hovertemplate="<br>".join([
            "Kelompok: %{x}",
            "Biaya Pengiriman: Rp%{y:,.2f}",
            "Harga Produk: Rp%{customdata[0]:,.2f}"
        ])
    )
    
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("""
        <div style="background-color:#f8f9fa;padding:15px;border-radius:10px;border-left:4px solid {};margin-top:20px;">
            <h5 style="color:{};margin-top:0;">📊 Insights:</h5>
            <ul style="margin-bottom:0;">
                <li><b>Semakin tinggi kelompok harga</b>, distribusi ongkir cenderung meningkat, baik dari sisi median maupun rentang interkuartilnya.</li>
                <li>Namun, distribusi ongkir masih menumpuk di nilai rendah, terutama di kelompok <b>Murah</b> dan <b>Sedang</b>.</li>
                <li>Kelompok <b>Sangat Mahal</b> memiliki outlier ongkir yang sangat tinggi, mengindikasikan produk mahal belum tentu ongkirnya rendah secara proporsional.</li>
                <li>Terdapat banyak <b>outlier</b> di semua kelompok harga, menunjukkan ketidakseimbangan dan potensi ketidaksesuaian biaya pengiriman.</li>
            </ul>
        </div>
    """.format(BLUE_PALETTE[0], BLUE_PALETTE[0]), unsafe_allow_html=True)

def show_shipping_ratio_analysis(order_items_dataset):
    """
    Menampilkan analisis rasio biaya pengiriman terhadap harga produk.
    
    Parameters:
        order_items_dataset (pd.DataFrame): Data item pesanan
    """
    st.markdown(f"""
    <div style="background-color:{BLUE_PALETTE[0]};padding:15px;border-radius:10px;margin-bottom:20px;box-shadow:0 4px 6px rgba(0,0,0,0.1);">
        <h4 style="color:white;margin:0;text-align:center;">Distribusi Rasio Biaya Pengiriman terhadap Harga Produk</h4>
    </div>
    """, unsafe_allow_html=True)
    
    order_items_dataset['shipping_ratio'] = order_items_dataset['freight_value'] / order_items_dataset['price']
    
    fig_hist = px.histogram(
        order_items_dataset,
        x='shipping_ratio',
        nbins=150,
        color_discrete_sequence=[YELLOW_PALETTE[1]],
        marginal='box',
        opacity=0.8,
        labels={
            'shipping_ratio': 'Rasio (Biaya Pengiriman/Harga)',
            'count': 'Jumlah Produk'
        }
    )
    fig_hist.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="<b>Rasio (Biaya Pengiriman/Harga)</b>",
        yaxis_title="<b>Jumlah Produk</b>",
        xaxis_range=[0, 2]
    )
    fig_hist.update_traces(
        marker=dict(line=dict(width=0.5, color='DarkSlateGrey'))
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    
    st.markdown(f"""
        <div style="background-color:#f8f9fa;padding:15px;border-radius:10px;border-left:4px solid {BLUE_PALETTE[0]};margin-top:20px;">
            <h5 style="color:{BLUE_PALETTE[0]};margin-top:0;">📊 Insights:</h5>
            <ul style="margin-bottom:0;">
                <li><b>Rasio ongkir terhadap harga produk</b> berdistribusi miring ke kanan (right-skewed), dengan mayoritas produk memiliki ongkir < 50% dari harga produk.</li>
                <li><b>75%</b> produk memiliki rasio ongkir < 0.39 (Q3).</li>
                <li>Terdapat <b>kasus ekstrem</b> dengan rasio > 1 (biaya pengiriman lebih tinggi dari harga produk), meskipun jumlahnya kecil.</li>
                <li>Pola ini mengindikasikan bahwa secara umum, <b>ongkir tidak terlalu membebani harga produk</b> untuk sebagian besar item.</li>
                <li><b>Modus rasio</b> berada di rentang 0.1-0.2.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

def app():
    
    # Menerapkan tema kustom
    local_css()
    
    # Header utama dengan gradient
    st.markdown("""
    <div style='background: linear-gradient(90deg, #1a5fb4, #3584e4); padding: 15px; border-radius: 10px; margin-bottom: 25px;'>
        <h1 style='color: white; margin: 0;'>📊 Exploratory Data Analysis</h1>
    </div>
    """, unsafe_allow_html=True)

    # Muat dataset
    payments_df, orders_dataset = load_payments_data()
    order_items_dataset = load_order_items()

    # Preprocessing data pembayaran
    filtered_df = preprocess_payments_data(payments_df, orders_dataset)
    
    # Hitung statistik bulanan
    monthly_stats = calculate_monthly_stats(filtered_df)

    # Tampilkan tabel statistik
    st.subheader('📈 Summary Statistik per Bulan')
    st.markdown("""
    <div style="background-color:#f8f9fa;padding:15px;border-radius:10px;margin-bottom:20px;">
    <h4 style="color:#1f77b4;">Statistik Pembayaran 12 Bulan Terakhir</h4>
    </div>
    """, unsafe_allow_html=True)
    
    st.dataframe(
        monthly_stats.style.format({
            'Jumlah Transaksi': '{:,}',
            'Rata-rata Pembayaran': 'Rp{:,.2f}',
            'Median Pembayaran': 'Rp{:,.2f}',
            'Total Pembayaran': 'Rp{:,.0f}'
        }).background_gradient(cmap='Blues', subset=['Jumlah Transaksi', 'Total Pembayaran'])
        .applymap(lambda x: f"color: {BLUE_PALETTE[0]};", subset=['Rata-rata Pembayaran', 'Median Pembayaran']),
        use_container_width=True,
        height=(monthly_stats.shape[0] + 1) * 35 + 3
    )

    # Tampilkan visualisasi tren pembayaran
    st.subheader('📊 Tren Total Pembayaran dan Jumlah Transaksi per Bulan')
    fig = create_payment_trend_chart(monthly_stats)
    st.plotly_chart(fig, use_container_width=True)

    # Tampilkan insight utama
    st.subheader('🔍 Insight Utama')
    show_key_insights()
    
    # Tampilkan analisis harga dan biaya pengiriman
    show_price_shipping_analysis(order_items_dataset)

if __name__ == "__main__":
    app()