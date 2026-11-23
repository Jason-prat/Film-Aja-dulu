import streamlit as st
import json
from readwrite import *
st.set_page_config(page_title='Filmku',page_icon="🎬",layout="wide")

def logout():
    st.session_state.clear()
    st.rerun()
beranda=st.Page('pages/beranda.py',title='Beranda',default=True)
cari=st.Page('pages/cari.py',title='Cari Film')
riwayat=st.Page('pages/riwayat.py',title='Riwayat')
login=st.Page('pages/login.py',title='Login',default=True)
register=st.Page('pages/register.py',title='Register')
detail=st.Page('pages/detail.py',title='Detail',visibility='hidden')
rekomendasi=st.Page('pages/rekomendasi.py',title='Rekomendasi')
statistik=st.Page('pages/statistik.py',title='Statistik')
tambah=st.Page('pages/tambah.py',title='Tambah',visibility='hidden')
keluar=st.Page(logout,title='Keluar',icon=':material/logout:')
data=baca_usn()
if st.session_state.get('user'):
    profile=st.Page('pages/profile.py',title=data[st.session_state['user']]['username'])
    pg= st.navigation([beranda,riwayat,cari,statistik,rekomendasi,profile,keluar,detail,tambah],position='top')
else:
    pg= st.navigation([login,register],position='hidden')

pg.run()