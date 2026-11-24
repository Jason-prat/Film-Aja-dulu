import streamlit as st
from fungsi import *
import requests
from datetime import datetime

st.header("Cari & Tambah Film")
st.caption("Cari di TMDB (Tidak perlu lengkap)")
query = st.text_input("Cari Film",placeholder="Inception",value=st.session_state.get('query',''),key='input',on_change=simpan_query,)

url='https://api.themoviedb.org/3'
api=st.secrets['TMDB_API_KEY']
cari = cari_film(url,api,query)

if cari:
    st.caption(f'{len(cari)} hasil untuk {query}')
    halaman(cari,'cari_film',4)
elif not query:
    st.caption('Silahkan masukkan nama film')
else:
    st.caption(f'0 hasil untuk {query}')




