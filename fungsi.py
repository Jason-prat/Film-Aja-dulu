import json
import streamlit as st
import requests
import math
from datetime import date

url='https://api.themoviedb.org/3'
api=st.secrets['TMDB_API_KEY']
def buka(hal,id):
    st.session_state['id']=id
    st.session_state['asal']=hal
def trending(url,api):
    path='/trending/movie/week'
    r=requests.get(url+path,params={'api_key':api,'language':'id-ID'})
    trending=r.json()['results']
    return trending

def upcoming(url,api,hal=4):
    sekarang=date.today().isoformat()
    film=[]
    for i in range(1,hal+1):
        r=requests.get(f'{url}/discover/movie',params={'api_key':api,'sort_by':'popularity.desc','page':i,'primary_release_date.gte':sekarang,'region':'ID'})
        film+=r.json()['results']
    return film

def cari_film(url,api,query,hal=4):
    path= '/search/movie'
    film =[]
    for i in range(1,hal+1):
        r= requests.get(f"{url}{path}",params={'api_key':api,'query':query,'page':i,'region':'ID'})
        film+=r.json()['results']
    return film
def kartu(f:dict,asal,offset):
    foto=f.get('poster_path')
    tahun = (f.get("release_date") or f.get("first_air_date") or "")[:4]
    skor=f'·⭐ {f.get('vote_average'):.1f}' if f.get('vote_average') else ""
    judul=f.get('original_title') or f.get('name')
    judul_bersih=judul if len(judul)<25 else judul[:23]+'...'
    with st.container(border=True,height='stretch'):
        if foto:
            st.image("https://image.tmdb.org/t/p/w342"+foto)
        st.markdown(f'**{judul}**')
        kunci=f'{asal}_{f.get('id')}_{offset}'
        st.caption(f'{tahun} {skor} ')
        col1,col2=st.columns(2)
        with col1:
            if st.button('Detail',key=f'detail{kunci}',type='secondary',use_container_width=True):
                buka(asal,f['id'])
                st.switch_page('pages/detail.py')
        with col2:
            if st.button('Tambah Film',key=f'tambah_{kunci}',type='primary',use_container_width=True):
                buka(asal,f['id'])
                st.switch_page('pages/tambah.py')
def grid(film,asal,n=4,offset=0):
    for i,item in enumerate(film):
        if i%n==0:
            kolom=st.columns(n,gap='medium')
        with kolom[i%n]:
            kartu(item,asal,offset+i)

def ganti_hal(kunci,ganti):
    st.session_state[kunci]+=ganti
def halaman(film,asal,hal=4):
    kunci=f'hal_{asal}'
    total=max(1, math.ceil(len(film)/hal))
    st.session_state.setdefault(kunci,1)
    
    st.session_state[kunci] = min(max(st.session_state[kunci],1),total)
    
    halaman=st.session_state[kunci]
    mulai = (halaman-1)*hal
    grid(film[mulai:mulai + hal],asal,4,mulai)

    kiri,tengah,kanan=st.columns(3)
    with kiri:
        st.button('Prev',key=f'prev_{asal}',disabled=halaman<=1,on_click=ganti_hal,args=(kunci,-1),use_container_width=True)
    with tengah:
        st.markdown(f'Halaman {halaman} dari {total}',text_alignment='center')
    with kanan:
        st.button('Next',key=f'next_{asal}',disabled=halaman>=total,on_click=ganti_hal,args=(kunci,1),use_container_width=True)
