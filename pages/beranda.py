import streamlit as st
from fungsi import *

url='https://api.themoviedb.org/3'
api=st.secrets['TMDB_API_KEY']
st.header('Filmku')
st.subheader('Film yang trending minggu ini')
try:
    trend=trending(url,api)
except requests.RequestException:
    st.error('Gagal Mengambil Data Dari TMDB')

halaman(trend,'beranda',4)