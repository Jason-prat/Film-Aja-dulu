import streamlit as st
from fungsi import *
from readwrite import *
#belum lengkap, aku cuma nambah UI, belum insert ke json buat hasil inputnya

sup = ambildb()
film=ambil_satu_film(sup,st.session_state['user'],st.session_state['id'])
LIST_TEMPAT=['Netflix',"Disney+","Youtube","Bioskop","Lainnya"]
LIST_PRIO=['Tinggi','Sedang','Rendah']
if film:
    TEMPAT_NONTON=[film['tempat']]
    TEMPAT_NONTON.extend([i for i in LIST_TEMPAT if i != film['tempat']])
    # st.write(TEMPAT_NONTON)
    if film['prioritas']:
        PRIORITAS=[film['prioritas']]
        PRIORITAS.extend([i for i in LIST_TEMPAT if i != film['prioritas']])
    else:
        PRIORITAS=LIST_PRIO
    if st.session_state['status']!=film['status']:
         st.session_state['status']=film['status']
else:
    TEMPAT_NONTON=['Netflix',"Disney+","Youtube","Bioskop","Lainnya"]
    PRIORITAS=['Tinggi','Sedang','Rendah']
data=detail(st.session_state['id'])
if 'status' not in st.session_state:
     st.session_state['status']= film['status'] if film else 'Sudah Ditonton'


simpan_status=st.session_state['status']
# st.write(simpan_status)
st.header("Tambah Ke Filmku")
st.caption("Isi catatan untuk film yang kamu ingin tonton")
if st.button(f'Kembali ke {st.session_state['asal'].split('_')[0].capitalize()}'):
    st.switch_page(f'pages/{st.session_state['asal'].split('_')[0]}.py')    
kiri,kanan=st.columns([3,11])
with kiri:


        if data['poster']:
            st.image("https://image.tmdb.org/t/p/w500"+data['poster'])
        st.subheader(f'{data['judul']} ({data['tahun']})')
        st.write(f'Sutradara: {data['direktor']} | Durasi: {data['durasi']} Menit | Genre: {data['genre']}')
        st.write(f'Rilis: {data['rilis']}')
with kanan:
     with st.container(border=True):
        st.write("Status Tontonan")
        @st.fragment(key='button')
        def button():
            simpan_status=st.session_state['status']
            sdh,sdg,ingin=st.columns(3)
            with sdh:
                if st.button("Sudah Ditonton",type='primary' if st.session_state['status']=="Sudah Ditonton" else 'secondary',use_container_width=True):
                    ingin="Sudah Ditonton"
                    st.session_state['status'] = 'Sudah Ditonton'
                    simpan_status = st.session_state['status']
                    st.rerun(scope='fragment')
            with sdg:

                if st.button("Sedang Ditonton",type='primary' if st.session_state['status']=="Sedang Ditonton" else 'secondary',use_container_width=True):
                    ingin="Sedang Ditonton"
                    st.session_state['status'] = 'Sedang Ditonton'
                    simpan_status = st.session_state['status'] 
                    st.rerun(scope='fragment')
            with ingin:
                if st.button("Ingin Ditonton",type='primary' if st.session_state['status']=="Ingin Ditonton" else 'secondary',use_container_width=True):
                    ingin="Ingin Ditonton"
                    st.session_state['status'] = 'Ingin Ditonton'
                    simpan_status = st.session_state['status']
                    st.rerun(scope='fragment')
        
            if simpan_status == 'Sudah Ditonton':
                ki,t,ka=st.columns(3)
                with ki:
                    tgl_tonton= st.date_input("Tanggal Ditonton",value=film['tgl_tonton'] if film else None )#
                with t:
                    pntn = st.selectbox("Tempat Menonton",options=TEMPAT_NONTON)#
                with ka:
                    rate = st.slider('Rating pribadi 1-10' , 0,10,value=film['rating_pribadi'] if film else None)#
                fav= st.checkbox("Tanda Favorit",value=film['favorit'] if film else None)#
                komen = st.text_area("Catatan Pribadi",placeholder="Masukkan Komentar Anda Disini",value=film['catatan'] if film else None)#

                _,simpan=st.columns(2)
                with _:
                     if film:
                        if st.button('Hapus dari Filmku'):
                            hapus(data)
                              
                with simpan:
                    with st.container(horizontal=True,horizontal_alignment='right'):
                        if st.button("Batal"):
                                    st.switch_page(f'pages/{st.session_state['asal'].split('_')[0]}.py')    
                        if st.button("Simpan ke Filmku",type='primary'):
                                indikator, pesan = tambah(
                                        sup,
                                        username = st.session_state['user'],
                                        tmdb_id= st.session_state['id'],
                                        status= "Sudah Ditonton",
                                        tempat=pntn,
                                        tgl_tonton=tgl_tonton,
                                        catatan=komen,
                                        rating_pribadi=rate,
                                        favorit=fav)                                                                                                                     
                                if indikator: 
                                    st.success(pesan)
                                    
                                else: 
                                    st.error(pesan)

            elif simpan_status == 'Sedang Ditonton':
                ki,t,ka=st.columns(3)
                with ki:
                    tgl_tonton = st.date_input("Tanggal Mulai Menonton",value=film['tgl_tonton'] if film else None)#
                with t:
                    terakhir = st.text_input("Durasi Nonton Terakhir",placeholder="Contoh : 00.00.00 / 45 menit",value=film['durasi_terakhir'] if film else None)#
                with ka:
                    pntn = st.selectbox("Tempat Menonton",options=TEMPAT_NONTON) #
                target = st.date_input("Target Selesai Menonton",value=film['target_selesai'] if film else None)#
                komen = st.text_area("Catatan pribadi saat ini",placeholder="Masukkan Komentar Anda Disini, Apakah sejauh ini ada yang menarik?",value=film['catatan'] if film else None)#
                _,simpan=st.columns(2)
                with _:
                     if film:
                        if st.button('Hapus dari Filmku'):
                            hapus(data)
                with simpan:
                    with st.container(horizontal=True,horizontal_alignment='right'):
                        if st.button("Batal"):
                            st.switch_page(f'pages/{st.session_state['asal'].split('_')[0]}.py')    
                        if st.button("Simpan ke Filmku",type='primary'):
                                indikator, pesan = tambah(
                                        sup,
                                        username = st.session_state['user'],
                                        tmdb_id= st.session_state['id'],
                                        status= "Sedang Ditonton",
                                        tempat=pntn,
                                        tgl_tonton=tgl_tonton,
                                        catatan=komen,
                                        durasi_terakhir=terakhir,
                                        target_selesai=target)                                                                                                                     
                                if indikator: 
                                    st.success(pesan) 
                                else: 
                                        st.error(pesan)
                        
            elif simpan_status == 'Ingin Ditonton':
                st.warning("Rating dan tanggal diisi nanti, setelah filmnya selesai ditonton.")
                ki,t,ka=st.columns(3)
                with ki :
                    pntn = st.selectbox("Rencana Tempat Menonton",options=TEMPAT_NONTON) #
                with t: 
                    tgl_tonton = st.date_input("Tanggal Rencana Menonton",value=film['tgl_tonton'] if film else None)#
                with ka:
                    prioritas = st.selectbox("Prioritas Menonton",PRIORITAS)#
                komen= st.text_area("Alasan ingin menonton / note ",placeholder="Direkomendasikan teman, tertarik dengan sutradara/aktornya..",value=film['catatan'] if film else None)#
                _,simpan=st.columns(2)
                with _:
                     if film:
                        if st.button('Hapus dari Filmku'):
                            hapus(data)
                with simpan:
                    with st.container(horizontal=True,horizontal_alignment='right'):
                        if st.button("Batal"):
                            st.switch_page(f'pages/{st.session_state['asal'].split('_')[0]}.py')    
                        if st.button("Simpan ke Filmku",type='primary'):
                                indikator, pesan = tambah(
                                        sup,
                                        username = st.session_state['user'],
                                        tmdb_id= st.session_state['id'],
                                        status= "Ingin Ditonton",
                                        tempat=pntn,
                                        tgl_tonton=tgl_tonton,
                                        catatan=komen,
                                        prioritas=prioritas)                                                                                                                 
                                if indikator: 
                                    st.success(pesan) 
                                else: 
                                        st.error(pesan)
        button()