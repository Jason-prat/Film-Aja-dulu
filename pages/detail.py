import streamlit as st
from fungsi import *
import requests
from datetime import datetime
data=detail()
if st.button(f'Kembali ke {st.session_state['asal'].split('_')[0].capitalize()}'):
    st.switch_page(f'pages/{st.session_state['asal'].split('_')[0]}.py')
a,b=st.columns([3,11])
with a:
    if data['poster']:
        st.image("https://image.tmdb.org/t/p/w500"+data['poster'])
    if st.button('Tambah Film',use_container_width=True,type='primary'):
        st.switch_page('pages/tambah.py')
with b:
    st.header(f'{data['judul']} ({data['tahun']})')
    st.write(f'Sutradara: {data['direktor']} | Durasi: {data['durasi']} Menit | Genre: {data['genre']}')
    st.write(f'Rilis: {data['rilis']}')
    kol=st.columns(5,gap='small',border=True,width=768)
    for i in range(5):
        with kol[i]:
            pass
            if data['pemeran']:
                   try:
                    st.image("https://image.tmdb.org/t/p/w185"+data['pemeran'][i][1])
                   except:
                       st.image('https://www.google.com/imgres?q=foto%20profile%20kosong&imgurl=https%3A%2F%2Fi.pinimg.com%2Foriginals%2F8a%2Fe9%2Fe9%2F8ae9e92fa4e69967aa61bf2bda967b7b.jpg&imgrefurl=https%3A%2F%2Fwww.pinterest.com%2Fpin%2F1050746156848281266%2F&docid=cG3u9g48aBv5vM&tbnid=L0oFsHYt8bCsZM&vet=12ahUKEwjU0uawjaCYAxUCzDgGHTdHFScQnPAOegQIQBAA..i&w=736&h=736&hcb=2&ved=2ahUKEwjU0uawjaCYAxUCzDgGHTdHFScQnPAOegQIQBAA')
            st.write(f'**{data['pemeran'][i][0]}**')
            st.write(data['pemeran'][i][2])

            
    st.subheader('Sinopsis')
    st.write(data['sinopsis'])
    if data['trailer'].split('v=')[1]=='':
        st.video(data['trailer'],width=900)
    else:
        st.caption("Trailer belum tersedia.")