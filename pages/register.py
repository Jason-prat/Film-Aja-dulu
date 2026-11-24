import streamlit as st
from readwrite import *

st.title("Filmku🎬")
st.subheader("Buat Akun")
with st.form("form daftar"):
    username = st.text_input("Username",placeholder="Masukkan Username")
    password = st.text_input("Kata Sandi",placeholder="Masukkan Kata Sandi",type='password')
    konfirmasi = st.text_input("Konfirmasi Kata Sandi", placeholder="Masukkan Kata Sandi",type='password')
    tekan = st.form_submit_button("Daftar",type="primary")

if tekan:
    username = username.strip()
    low = username.lower()
    user = baca_usn()
    if username== "" or password=='' or konfirmasi=='':
        st.error("Semua Kolom Wajib Diisi")
    elif len(username)<2:
        st.error("Username Minimal Terdiri dari 2 Kata")
    elif len(password)<8:
        st.error("Kata Sandi Minimal Terdiri dari 8 Kata")
    elif password != konfirmasi:
        st.error("Kata Sandi Tidak Sama Dengan Perulangan")
    elif low in user:
        st.error("Username Telah Digunakan")
    else:
        user[low] = {"username":username,"password":password}
        tulis_usn(user)
        st.session_state['sukses'] = ("Akun Berhasil Dibuat")
        st.switch_page("pages/login.py")

st.caption("Sudah punya akun?")
if st.button("Masuk Sekarang"):
    st.switch_page("pages/login.py")