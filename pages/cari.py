import streamlit as st
from fungsi import *
import requests
from datetime import datetime
#nanti jangan lupa nambahin status sudah nntn dll, kalau halaman tambah dah beres
st.header("Cari & Tambah Film")
st.caption("Cari di TMDB (Tidak perlu lengkap)")
if 'ukuran' not in st.session_state:
    st.session_state['ukuran']=4
OPSI=[3,4,5]
with st.container(horizontal=True,vertical_alignment='bottom'):
    query = st.text_input("Cari Film",placeholder="Inception",value=st.session_state.get('query',''),key='input',on_change=simpan_query,)
    ukuran=st.selectbox('Ukuran Grid',options=OPSI,index=OPSI.index(st.session_state['ukuran']),width=150)
    st.session_state['ukuran']=ukuran

url='https://api.themoviedb.org/3'
api=st.secrets['TMDB_API_KEY']
cari = cari_film(url,api,query)
# st.write(cari)

if cari:
    st.caption(f'{len(cari)} hasil untuk {query}')
    halaman(cari,'cari_film',ukuran)
elif not query:
    st.caption('Silahkan masukkan nama film')
else:
    st.caption(f'0 hasil untuk {query}')




