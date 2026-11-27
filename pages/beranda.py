import streamlit as st
from fungsi import *

url='https://api.themoviedb.org/3'
api=st.secrets['TMDB_API_KEY']
st.header('Filmku')
if 'ukuran' not in st.session_state:
    st.session_state['ukuran']=4
OPSI=[3,4,5]
try:
    trend=trending(url,api)
    akan_rilis=upcoming(url,api)
    kol = st.columns(2)
    with kol[0]:
        st.subheader('Trending Minggu Ini')
    with kol[1]:
        with st.container(horizontal_alignment='right'):
            ukuran=st.selectbox('Ukuran Grid',options=OPSI,index=OPSI.index(st.session_state['ukuran']),width=150)
            st.session_state['ukuran']=ukuran
    halaman(trend,'beranda_trending',ukuran)
    st.divider()
    st.subheader('Akan Rilis')
    halaman(akan_rilis,'beranda_upcoming',ukuran)
except requests.RequestException:
    st.error('Gagal Mengambil Data Dari TMDB, Silahkan Coba Lagi')
