import json
import streamlit as st
import requests
import math
from datetime import date
from datetime import datetime
from readwrite import *

url='https://api.themoviedb.org/3'
api=st.secrets['TMDB_API_KEY']
def buka(hal,id):
    st.session_state['id']=id
    st.session_state['asal']=hal

@st.cache_data(ttl=3600,show_spinner='Memuat trending...')
def trending(url,api):
    path='/trending/movie/week'
    r=requests.get(url+path,params={'api_key':api,'language':'id-ID'})
    trending=r.json()['results']
    return trending

@st.cache_data(ttl=3600,show_spinner='Memuat akan rilis...')
def upcoming(url,api,hal=4):
    sekarang=date.today().isoformat()
    film=[]
    for i in range(1,hal+1):
        r=requests.get(f'{url}/discover/movie',params={'api_key':api,'sort_by':'popularity.desc','page':i,'primary_release_date.gte':sekarang,'region':'ID'})
        film+=r.json()['results']
    return film

@st.cache_data(ttl=3600,show_spinner='Memuat cari film...')
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
    judul=f.get('title') or f.get('original_title')
    with st.container(border=True,height='stretch'):
        if foto:
            st.image("https://image.tmdb.org/t/p/w342"+foto)
        st.markdown(f'**{judul}**')
        kunci=f'{asal}_{f.get('id')}_{offset}'
        
        stat= status_tonton(st.session_state['user']).get(f.get('id'))
        if asal.split('_')[0] in ['cari','riwayat']:
            if stat == "Sudah Ditonton":
                st.success(stat)
            elif stat == "Sedang Ditonton":
                st.warning(stat)
            elif stat == "Ingin Ditonton":
                st.error(stat)
        if f.get('pribadi'):
            genre=', '.join(i['name'] for i in f['genres'])
            kol=st.columns([70,30])
            with kol[0]:
                st.caption(f'{tahun} · {genre}')
            with kol[1]:
                if f.get('rating_pribadi') != None:
                    st.caption(f'Rating Pribadi: ⭐{f.get('rating_pribadi')}')
                else:
                    st.caption(f'Rating Pribadi: ⭐0')
                    f['rating_pribadi']=0
        else:
            st.caption(f'{tahun} {skor} ')
        col1,col2=st.columns(2)
        with col1:
            if st.button('Detail',key=f'detail{kunci}',type='secondary',use_container_width=True):
                buka(asal,f['id'])
                st.switch_page('pages/detail.py')
        with col2:
            if stat:
                if st.button('Edit Status Film',key=f'tambah_{kunci}',type='primary',use_container_width=True):
                    st.session_state['status']=stat
                    buka(asal,f['id'])
                    st.switch_page('pages/tambah.py') 
            else:
                if st.button('Tambah Film',key=f'tambah_{kunci}',type='primary',use_container_width=True):
                    buka(asal,f['id'])
                    st.switch_page('pages/tambah.py')

def grid(film,asal,n=4,offset=0): #buat jumlah kolom
    for i,item in enumerate(film):
        if i%n==0:
            kolom=st.columns(n,gap='medium')
        with kolom[i%n]:
            kartu(item,asal,offset+i)

def ganti_hal(kunci,ganti): #buat menambah kunci halaman
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

@st.cache_data(ttl=3600,show_spinner='Memuat data film...')
def detail(id):
    api=st.secrets['TMDB_API_KEY']
    r=requests.get(f'https://api.themoviedb.org/3/movie/{id}',params={'api_key':api,"append_to_response": "credits,videos"})
    data_film=r.json()
    poster=data_film.get('poster_path')
    cast=[]
    kru=data_film.get('credits',{}).get('crew',[])
    for i in range(len(data_film['credits'].get('cast')[:5])):
        detail=[]
        detail.append(data_film['credits'].get('cast')[i]['name'])
        detail.append(data_film['credits'].get('cast')[i]['profile_path'])
        detail.append(data_film['credits'].get('cast')[i]['character'])
        cast.append(detail)
    direktor=[i['name'] for i in kru if i['job']=='Director']
    direktor=', '.join(direktor)
    genres=data_film.get('genres')
    genre=[i.get('name') for i in genres]
    genres=', '.join(genre)
    videos=data_film.get('videos').get('results')
    skor=f' ·⭐ {data_film.get('vote_average'):.1f}' if data_film.get('vote_average') else ""
    trailer=[i['key'] for i in videos if i.get('type')=='Trailer' and i.get('site')=='YouTube' and 'fan' not in i.get('name','').lower()]
    tanggal=datetime.strptime(data_film['release_date'], "%Y-%m-%d").date()
    rilis=tanggal.strftime("%d %B %Y") if tanggal else 'Belum Tersedia Tanggal Rilis'
    return {'poster':poster,'direktor':direktor,'durasi':data_film.get('runtime'),'genre':genres,'rilis':rilis+skor,'pemeran':cast,'sinopsis':data_film.get('overview'),'trailer':trailer,'judul':data_film.get('title'),'tahun':data_film.get('release_date')[:4],'tmdb_id':id}

def simpan_query():
    st.session_state['query']=st.session_state['input']

@st.cache_data(ttl=3600,show_spinner='Memuat Riwayat...')
def ambil_data_film(film):
    url='https://api.themoviedb.org/3'
    api=st.secrets['TMDB_API_KEY']
    data=[]
    for i in film:
        r=requests.get(f'{url}/movie/{str(i['tmdb_id'])}',params={'api_key':api})
        data.append({**r.json(),'pribadi':i,'rating_pribadi':i['rating_pribadi']})

    return data

def sorting(film,key,asc=True):
    hasil = film[:]                      
    n = len(hasil)
    for i in range(n - 1):
        tukar = False
        for j in range(n - 1 - i):
            a = key(hasil[j])
            b = key(hasil[j + 1])
            salah_urut = (a < b) if asc else (a > b)
            if salah_urut:
                hasil[j], hasil[j + 1] = hasil[j + 1], hasil[j]
                tukar = True
        if not tukar:                    
            break
    return hasil

def key_rating(film):
    rating = film.get('rating_pribadi') or 0 
    return rating

def key_judul(film):
    return film.get('original_title').lower()

def key_tahun(film):
    return (film.get('release_date') or '')[:4]

def key_favorit(film):
    return [i for i in film if i.get('pribadi').get('favorit')]

def status(film,status):
    return [i for i in film if i.get('pribadi').get('status')==status]

def cari(film,query):
    judul=(film.get('title') or '').lower()
    genre = ' '.join(i['name'] for i in film.get('genres',[])).lower()
    tahun = (film.get('release_date') or '')[:4]
    rating = film.get('rating_pribadi')
    rating = str(rating) if rating is not None else ''
    teks = judul + ' ' + genre
    for i in query.split():
        if i in teks:
            continue
        if i == tahun or i == rating:
            continue
        return False
    return True

@st.dialog('Hapus film?')
def popup_hapus(film):
    st.write(f'**Hapus {film['judul']}** dari riwayat?')
    kol=st.columns(2)
    if kol[0].button('Batal',use_container_width=True):
        st.rerun()
    if kol[1].button('Hapus',use_container_width=True):
        hapus_film(film)
        st.switch_page(f'pages/{st.session_state['asal'].split('_')[0]}.py')