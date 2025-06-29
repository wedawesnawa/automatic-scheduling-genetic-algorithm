import streamlit as st
import pandas as pd
import numpy as np
import datetime

@st.dialog("Tambah Waktu")
def vote():
    st.text_input("Hari")
    st.time_input("Mulai", value=None)
    st.time_input("Selesai", value=None)
    if st.button("Submit"):
        st.rerun()

left, = st.columns(1, vertical_alignment="bottom")
if left.button("Tambah Waktu"):
    vote() 

csv_path = r"dataset\timeslots.csv"
try:
    df = pd.read_csv(csv_path)
    st.table(df)  # atau st.dataframe(df) untuk fitur interaktif
except FileNotFoundError:
    st.error(f"File tidak ditemukan di: {csv_path}")
except Exception as e:
    st.error(f"Terjadi kesalahan saat membaca file CSV: {e}")