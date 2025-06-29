import streamlit as st
import pandas as pd
import numpy as np

@st.dialog("Tambah Ruangan")
def vote():
    st.text_input("Nama Ruangan")
    st.text_input("Kapasitas")
    st.selectbox("Tipe Ruangan", ("Teori", "Labs"),)
    if st.button("Submit"):
        st.rerun()

left, = st.columns(1, vertical_alignment="bottom")
if left.button("Tambah Ruangan"):
    vote() 

csv_path = r"dataset\rooms.csv"
try:
    df = pd.read_csv(csv_path)
    st.table(df)  # atau st.dataframe(df) untuk fitur interaktif
except FileNotFoundError:
    st.error(f"File tidak ditemukan di: {csv_path}")
except Exception as e:
    st.error(f"Terjadi kesalahan saat membaca file CSV: {e}")
