import streamlit as st
from fungsi import *

url='https://api.themoviedb.org/3'
api=st.secrets['TMDB_API_KEY']
st.header('Filmku')

try:
    with st.spinner("Memuat film..."):
        trend=trending(url,api)
        akan_rilis=upcoming(url,api)
except requests.RequestException:
    st.error('Gagal Mengambil Data Dari TMDB')
st.subheader('Trending Minggu Ini')
halaman(trend,'beranda_trending',4)
st.divider()
st.subheader('Akan Rilis')
halaman(akan_rilis,'beranda_upcoming',4)