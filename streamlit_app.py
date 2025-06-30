import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

# Konfigurasi halaman
st.set_page_config(
    page_title="Prediksi Curah Hujan Jawa Timur",
    layout="wide"
)

# Gaya CSS kustom
st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #cc66cc;
            padding: 0px;
        }
        .sidebar .css-1d391kg {
            padding-top: 0rem;
        }
        .sidebar .stButton>button {
            width: 100%;
            margin-bottom: 10px;
            background-color: white;
            color: black;
            border-radius: 20px;
        }
        .main-header {
            background-color: #ff66cc;
            color: black;
            font-size: 26px;
            text-align: center;
            padding: 20px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar dengan menu navigasi
st.sidebar.markdown("## ")
menu = st.sidebar.radio("Navigasi", ["Home", "Upload Data", "Preprocessing Data", "Pemodelan", "Visualisasi"])

# Header utama
st.markdown('<div class="main-header">Selamat Datang di Web Prediksi Curah Hujan Jawa Timur</div>', unsafe_allow_html=True)

# Konten berdasarkan pilihan menu
if menu == "Home":
    st.write("Ini adalah halaman beranda. Silakan gunakan menu di sebelah kiri untuk navigasi.")

elif menu == "Upload Data":
    uploaded_file = st.file_uploader("Unggah dataset curah hujan (CSV)", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("File berhasil diunggah!")
        st.dataframe(df)

elif menu == "Preprocessing Data":
    st.write("Halaman untuk preprocessing data, seperti normalisasi dan cek missing values.")

elif menu == "Pemodelan":
    st.write("Halaman pemodelan menggunakan algoritma GA-LSTM akan ditampilkan di sini.")

elif menu == "Visualisasi":
    st.write("Halaman visualisasi data dan prediksi curah hujan.")
