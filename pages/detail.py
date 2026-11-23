import streamlit as st
from fungsi import *
import requests
with st.spinner("Memuat data film..."):

    api=st.secrets['TMDB_API_KEY']
    r=requests.get(f'https://api.themoviedb.org/3/movie/{st.session_state['id']}',params={'api_key':api,"append_to_response": "credits,videos"})
    data_film=r.json()
poster=data_film.get('poster_path')
a,b=st.columns([3,11])

kru=data_film.get('credits',{}).get('crew',[])
direktor=[i['name'] for i in kru if i['job']=='Director']
pemeran=[i.get('name') for i in data_film['credits'].get('cast')][:5]
pemerans =', '.join(pemeran)
genres=data_film.get('genres')
genre=[i.get('name') for i in genres]
videos=data_film.get('videos').get('results')

trailer=None
trailer=[i['key'] for i in videos if i.get('type')=='Trailer' and i.get('site')=='YouTube' and 'fan' not in i.get('name','').lower()]

with a:
    if poster:
        st.image("https://image.tmdb.org/t/p/w500"+poster)
    if st.button('Tambah Film',use_container_width=True,type='primary'):
        st.switch_page('pages/tambah.py')
with b:
    st.header(f'{data_film.get('original_title')} ({data_film.get('release_date')[:4]})')
    st.write(f'Sutradara: {''.join(direktor)} | Durasi: {data_film.get('runtime')} Menit | Genre: {', '.join(genre)}')
    st.write(f"Pemeran: {pemerans}")
    st.subheader('Sinopsis')
    st.write(data_film.get('overview'))
    if trailer:
        st.video(f"https://www.youtube.com/watch?v={trailer[0]}",width=900)
    else:
        st.caption("Trailer belum tersedia.")
