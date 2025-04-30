import streamlit as st
import importlib

PAGES = {
    "🏠 Home": "home",
    "📄 Datasets": "datasets",
    "📊 EDA": "eda",
    "📑 Conclusion": "conclusion"
}

st.set_page_config(page_title="Multi-Page App", layout="wide")

if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"

def render_sidebar():
    st.sidebar.markdown("""
    <style>
        .sidebar-title {
            color: #1e3c72 !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            margin-bottom: 1.5rem !important;
            padding-bottom: 0.75rem;
            position: relative;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            text-align: center;
        }
        
        .sidebar-title:after {
            content: "";
            position: absolute;
            bottom: 0;
            left: 25%;
            width: 50%;
            height: 3px;
            background: linear-gradient(90deg, #ffd700, #1a5fb4);
            border-radius: 3px;
        }
        
        .sidebar-title:hover {
            text-shadow: 0 0 8px rgba(26, 95, 180, 0.3);
            transition: text-shadow 0.3s ease;
        }
        
        .sidebar .stButton>button {
            background-color: #1a5fb4 !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            margin: 8px 0 !important;
            font-weight: bold !important;
            font-size: 1rem !important;
            cursor: pointer !important;
            text-align: center !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
            transition: all 0.3s ease !important;
            border: none !important;
            width: 100% !important;
        }
        
        .sidebar .stButton>button:hover {
            background-color: #0d47a1 !important;
            color: white !important;
            transform: scale(1.02) !important;
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15) !important;
        }
        
        .sidebar .stButton>button:focus:not(:active) {
            background-color: #1a5fb4 !important;
            color: white !important;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
        }
        
        .sidebar .stButton>button[aria-pressed="true"] {
            background-color: #0d47a1 !important;
            border-left: 4px solid #ffd700 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown('<div class="sidebar-title">📚 Navigation</div>', unsafe_allow_html=True)
    
    for label in PAGES:
        if st.sidebar.button(label, key=f"nav_{label}"):
            st.session_state.current_page = label
            st.rerun()

render_sidebar()

st.markdown("""
<style>
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

try:
    module_name = f"pages.{PAGES[st.session_state.current_page]}"
    module = importlib.import_module(module_name)
    
    with st.container():
        st.markdown('<div class="main">', unsafe_allow_html=True)
        module.app()
        st.markdown('</div>', unsafe_allow_html=True)
        
except ImportError as e:
    st.error(f"Failed to load page module: {e}")
    st.error("Please make sure you have the following files in your directory under 'pages/' folder:")
    for page in PAGES.values():
        st.error(f"- pages/{page}.py")