
from fungsi import *
from readwrite import *

st.title('Riwayat Tontonan')
db=ambildb()
user=ambil_riwayat(db,st.session_state.user)
data_film=ambil_data_film(user)
kolom=st.columns([70,10,10,10])
with kolom[0]:
    cari=st.text_input('Cari',placeholder='Cari judul, genre, tahun, atau rating')
with kolom[1]:
    kol=st.columns(2)
    with kol[0]:
        urut=st.selectbox(label='Urutkan',options=['Rating','Judul','Tahun'])
    with kol[1]:
        ascending=st.toggle('Descending')
with kolom[2]:
    status=st.selectbox(label='Status',options=['Semua status','Sudah ditonton','Sedang ditonton','Ingin ditonton'])
with kolom[3]:
    favorit=st.checkbox('Favorit') 
if urut == 'Rating':
    data_film=sorting(data_film, key_rating,ascending)
elif urut =='Judul':
    data_film=sorting(data_film,key_judul,ascending)
elif urut=='Tahun':
    data_film=sorting(data_film,key_tahun,ascending)


halaman(data_film,'riwayat',4)