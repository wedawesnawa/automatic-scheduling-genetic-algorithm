import streamlit as st
import pandas as pd
import numpy as np

@st.dialog("Tambah Mata Kuliah")
def vote():
    st.text_input("Nama MK")
    st.text_input("Semester")
    st.text_input("SKS")
    st.text_input("Kelas")
    st.text_input("ID Dosen")
    if st.button("Submit"):
        st.rerun()

left, = st.columns(1, vertical_alignment="bottom")
if left.button("Tambah Mata Kuliah"):
    vote() 

csv_path = r"dataset\courses.csv"
try:
    df = pd.read_csv(csv_path)
    st.table(df)  # atau st.dataframe(df) untuk fitur interaktif
except FileNotFoundError:
    st.error(f"File tidak ditemukan di: {csv_path}")
except Exception as e:
    st.error(f"Terjadi kesalahan saat membaca file CSV: {e}")
