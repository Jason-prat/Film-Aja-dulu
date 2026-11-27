
from fungsi import *
from readwrite import *
OPSI=[3,4,5]
st.title('Riwayat Tontonan')
db=ambildb()
user=ambil_riwayat(db,st.session_state.user)
data_film=ambil_data_film(user)
kolom=st.columns([65,40],vertical_alignment='bottom',gap='xxsmall')
if 'ukuran' not in st.session_state:
    st.session_state['ukuran']=4
with kolom[0]:
    q=st.text_input('Cari',placeholder='Cari judul, genre, tahun, atau rating')
with kolom[1]:
    with st.container(horizontal=True,vertical_alignment='bottom'):
        kol=st.columns(2,vertical_alignment='bottom')
        urut=st.selectbox(label='Urutkan',options=['Judul','Rating','Tahun','Tanggal Ditonton'])
        desc=st.toggle('Descending',value=False)

        stats=st.selectbox(label='Status',options=['Semua Status','Sudah Ditonton','Sedang Ditonton','Ingin Ditonton'])

        favorit=st.checkbox('Favorit') 

        ukuran=st.selectbox('Ukuran Grid',options=OPSI,index=OPSI.index(st.session_state['ukuran']),width=150)
        st.session_state['ukuran']=ukuran
if urut == 'Rating':
    data_film=sorting(data_film, key_rating,desc)
elif urut =='Judul':
    data_film=sorting(data_film,key_judul,desc)
elif urut=='Tahun':
    data_film=sorting(data_film,key_tahun,desc)
else:
    data_film=sorting(data_film,key_tanggal,desc)
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
    halaman(data_film,'riwayat',ukuran)