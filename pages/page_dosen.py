import streamlit as st
import pandas as pd
import numpy as np

@st.dialog("Tambah Dosen")
def vote():
    st.text_input("Nama Dosen")
    st.text_input("Maks SKS per-hari")
    st.text_input("Maks SKS per week")
    if st.button("Submit"):
        st.rerun()

left, = st.columns(1, vertical_alignment="bottom")
if left.button("Tambah Dosen"):
    vote() 

csv_path = r"dataset\lecturers.csv"
try:
    df = pd.read_csv(csv_path)
    st.table(df)  # atau st.dataframe(df) untuk fitur interaktif
except FileNotFoundError:
    st.error(f"File tidak ditemukan di: {csv_path}")
except Exception as e:
    st.error(f"Terjadi kesalahan saat membaca file CSV: {e}")
