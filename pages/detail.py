import streamlit as st
from fungsi import *
import requests
from datetime import datetime
with st.spinner("Memuat detail film..."):
    api=st.secrets['TMDB_API_KEY']
    r=requests.get(f'https://api.themoviedb.org/3/movie/{st.session_state['id']}',params={'api_key':api,"append_to_response": "credits,videos"})
    data_film=r.json()
poster=data_film.get('poster_path')
cast=[]
kru=data_film.get('credits',{}).get('crew',[])
# st.write(data_film['credits'].get('cast'))
for i in range(len(data_film['credits'].get('cast')[:5])):
    detail=[]
    detail.append(data_film['credits'].get('cast')[i]['name'])
    detail.append(data_film['credits'].get('cast')[i]['profile_path'])
    detail.append(data_film['credits'].get('cast')[i]['character'])
    cast.append(detail)
direktor=[i['name'] for i in kru if i['job']=='Director']
foto_cast=[i.get('profile_path') for i in data_film['credits'].get('cast')][:5]
pemeran=[i.get('name') for i in data_film['credits'].get('cast')][:5]


pemerans =', '.join(pemeran)
karakter=[i.get('character') for i in data_film['credits'].get('cast')]
genres=data_film.get('genres')
genre=[i.get('name') for i in genres]
videos=data_film.get('videos').get('results')
skor=f'·⭐ {data_film.get('vote_average'):.1f}' if data_film.get('vote_average') else ""
trailer=None
trailer=[i['key'] for i in videos if i.get('type')=='Trailer' and i.get('site')=='YouTube' and 'fan' not in i.get('name','').lower()]
tanggal=datetime.strptime(data_film['release_date'], "%Y-%m-%d").date()
rilis=tanggal.strftime("%d %B %Y")
# st.write(data_film['credits'])
if st.button(f'Kembali ke {st.session_state['asal'].split('_')[0].capitalize()}'):
    st.switch_page(f'pages/{st.session_state['asal'].split('_')[0]}.py')
a,b=st.columns([3,11])
with a:

    if poster:
        st.image("https://image.tmdb.org/t/p/w500"+poster)
    if st.button('Tambah Film',use_container_width=True,type='primary'):
        st.switch_page('pages/tambah.py')
with b:
    st.header(f'{data_film.get('original_title')} ({data_film.get('release_date')[:4]})')
    st.write(f'Sutradara: {', '.join(direktor)} | Durasi: {data_film.get('runtime')} Menit | Genre: {', '.join(genre)}')
    st.write(f'Rilis: {rilis} {skor}')
    kol=st.columns(5,gap='small',border=True,width=660)
    for i in range(5):
        with kol[i]:
            pass
            if cast:
                try:
                    st.image("https://image.tmdb.org/t/p/w185"+cast[i][1])
                except:
                    st.image('https://www.google.com/imgres?q=foto%20profile%20kosong&imgurl=https%3A%2F%2Fi.pinimg.com%2Foriginals%2F8a%2Fe9%2Fe9%2F8ae9e92fa4e69967aa61bf2bda967b7b.jpg&imgrefurl=https%3A%2F%2Fwww.pinterest.com%2Fpin%2F1050746156848281266%2F&docid=cG3u9g48aBv5vM&tbnid=L0oFsHYt8bCsZM&vet=12ahUKEwjU0uawjaCYAxUCzDgGHTdHFScQnPAOegQIQBAA..i&w=736&h=736&hcb=2&ved=2ahUKEwjU0uawjaCYAxUCzDgGHTdHFScQnPAOegQIQBAA')
            st.write(f'**{cast[i][0]}**')
            st.write(cast[i][2])

    
    st.subheader('Sinopsis')
    st.write(data_film.get('overview'))
    if trailer:
        st.video(f"https://www.youtube.com/watch?v={trailer[0]}",width=900)
    else:
        st.caption("Trailer belum tersedia.")
