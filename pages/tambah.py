import streamlit as st
from fungsi import *

with st.spinner("Memuat detail film..."):
    api=st.secrets['TMDB_API_KEY']
    r=requests.get(f'https://api.themoviedb.org/3/movie/{st.session_state['id']}',params={'api_key':api,"append_to_response": "credits,videos"})
    data_film=r.json()
if st.button(f'Kembali ke {st.session_state['asal'].split('_')[0].capitalize()}'):
    st.switch_page(f'pages/{st.session_state['asal'].split('_')[0]}.py')
kiri,kanan=st.columns([3,11])
