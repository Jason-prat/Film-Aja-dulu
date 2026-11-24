import streamlit as st
from readwrite import *

st.title("Filmku🎬")
st.subheader("Masuk")
with st.form("form masuk"):
    username = st.text_input("Username",placeholder="Masukkan Username")
    password = st.text_input("Kata Sandi",placeholder="Masukkan Kata Sandi",type='password')
    tekan = st.form_submit_button("Masuk",type="primary")

if tekan:
    username = username.strip().lower()
    user = baca_usn()
    if username not in user:
        st.error("Username atau Sandi Salah")
    elif user[username]['password'] != password:
        st.error("Username atau Sandi Salah")
    else:
        st.session_state['user'] = username
        st.success("Berhasil Masuk")
        st.rerun()

if 'sukses' in st.session_state:
    st.success(st.session_state.pop('sukses'))

st.caption("Belum punya akun?")
if st.button("Buat Sekarang"):
    st.switch_page("pages/register.py")