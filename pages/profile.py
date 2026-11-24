import streamlit as st
from readwrite import *
#ini halaman kalau mau buat ganti pw gez
username = st.session_state['user']
if st.button("← Kembali Ke Beranda"):
    st.switch_page("pages/beranda.py")
st.header("Akun Saya")
st.caption("Kelola data akun dan ganti kata sandi.")
kiri,kanan,empt = st.columns([1,1.3,1.2],gap='medium')
with kiri:
    with st.container(border=True):
        st.subheader("Informasi Akun")
        st.text_input("Username",value=username,disabled=True)

with kanan: 
    with st.container(border=True):
        st.subheader("Ganti Kata Sandi")
        with st.form("form ganti sandi"):
            lama = st.text_input("Kata Sandi Lama",placeholder='Masukkan Kata Sandi Lama',type='password')
            baru = st.text_input("Kata Sandi Baru",placeholder='Masukkan Kata Sandi Baru',type='password')
            st.caption("Kata Sandi Minimal 8 Karakter")
            konfirm = st.text_input("Konfirmasi Kata Sandi Baru",placeholder='Masukkan Kata Sandi Baru',type="password")
            empt1,kiri1,kanan1 = st.columns([3,1,2])
            with kiri1:
                batal = st.form_submit_button("Batal")
                #langsung ku direct ke beranda
            with kanan1:
                tekan = st.form_submit_button("Simpan Kata Sandi",type='primary')
    if batal:
        st.switch_page("pages/beranda.py")

#tambah syaratnya sama json buat ubah pwnya