import streamlit as st
from readwrite import *

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
            with kanan1:
                tekan = st.form_submit_button("Simpan Kata Sandi",type='primary')
    if batal:
        st.switch_page("pages/beranda.py")
    if tekan:
        sup = ambildb()
        data = profile(sup,username)
        if lama != data[0]['password'] :
            st.error("Kata Sandi Lama Salah")
        elif 8 > len(baru):
            st.error("Kata Sandi Minimal Terdiri dari 8 Kata")
        elif baru != konfirm:
            st.error("Kata Sandi Baru Tidak Sama Dengan Perulangan")
        elif baru == lama:
            st.error("Kata Sandi Baru Harus Berbeda Dengan Sandi Lama")
        else:
            sup.table("users").update({"password":baru}).eq("username",username).execute()
            st.success("Password Telah Berhasil Diganti")

