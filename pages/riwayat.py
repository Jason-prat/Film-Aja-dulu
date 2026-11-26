
from fungsi import *
from readwrite import *

st.title('Riwayat Tontonan')
db=ambildb()
user=ambil_riwayat(db,st.session_state.user)
data_film=ambil_data_film(user)
kolom=st.columns([68,12,10,10],vertical_alignment='bottom')
with kolom[0]:
    q=st.text_input('Cari',placeholder='Cari judul, genre, tahun, atau rating')
with kolom[1]:
    kol=st.columns(2,vertical_alignment='bottom')
    with kol[0]:
        urut=st.selectbox(label='Urutkan',options=['Rating','Judul','Tahun'])
    with kol[1]:
        desc=st.toggle('Descending',value=True)
with kolom[2]:
    stats=st.selectbox(label='Status',options=['Semua Status','Sudah Ditonton','Sedang Ditonton','Ingin Ditonton'])
with kolom[3]:
    favorit=st.checkbox('Favorit') 
if urut == 'Rating':
    data_film=sorting(data_film, key_rating,desc)
elif urut =='Judul':
    data_film=sorting(data_film,key_judul,desc)
elif urut=='Tahun':
    data_film=sorting(data_film,key_tahun,desc)
if stats in ['Sudah Ditonton','Sedang Ditonton','Ingin Ditonton']:
    data_film=status(data_film,stats)
if favorit:
    data_film=key_favorit(data_film)
# st.write(st.session_state)
if q.strip():
    query = q.strip().lower()
    film=[]
    for i in data_film:
        if cari(i,query):
            film.append(i)
    data_film=film
if len(data_film)==0:
    st.info('Tidak ada film ditemukan')
else:
    halaman(data_film,'riwayat',4)