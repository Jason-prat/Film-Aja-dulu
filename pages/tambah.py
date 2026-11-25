import streamlit as st
from fungsi import *

#belum lengkap, aku cuma nambah UI, belum insert ke json buat hasil inputnya

data=detail(st.session_state['id'])

kiri,kanan=st.columns([3,11])
with kiri:
        st.header("Tambah Ke Filmku")
        st.caption("Isi catatan untuk film yang kamu ingin tonton")
        if st.button(f'Kembali ke {st.session_state['asal'].split('_')[0].capitalize()}'):
            st.switch_page(f'pages/{st.session_state['asal'].split('_')[0]}.py')    
        if data['poster']:
            st.image("https://image.tmdb.org/t/p/w500"+data['poster'])
        st.subheader(f'{data['judul']} ({data['tahun']})')
        st.write(f'Sutradara: {data['direktor']} | Durasi: {data['durasi']} Menit | Genre: {data['genre']}')
        st.write(f'Rilis: {data['rilis']}')
with kanan:
     with st.container(border=True):
        st.write("Status Tontonan")
        sdh,sdg,ingin=st.columns(3)
        if 'status' not in st.session_state:
             st.session_state['status']=''
        simpan_status=st.session_state['status']
        with sdh:
            if st.button("Sudah Ditonton",type='primary' if st.session_state['status']=="Sudah Ditonton" else 'secondary',use_container_width=True):
                st.session_state['status'] = 'Sudah Ditonton'
                simpan_status = st.session_state['status']
                st.rerun()
        with sdg:
            if st.button("Sedang Ditonton",type='primary' if st.session_state['status']=="Sedang Ditonton" else 'secondary',use_container_width=True):
                st.session_state['status'] = 'Sedang Ditonton'
                simpan_status = st.session_state['status'] 
                st.rerun()
        with ingin:
            if st.button("Ingin Ditonton",type='primary' if st.session_state['status']=="Ingin Ditonton" else 'secondary',use_container_width=True):
                st.session_state['status'] = 'Ingin Ditonton'
                simpan_status = st.session_state['status'] 
                st.rerun()
        if simpan_status == 'Sudah Ditonton':
            ki,t,ka=st.columns(3)
            with ki:
                sdh_tgl= st.date_input("Tanggal Ditonton")
            with t:
                pntn = st.selectbox("Tempat Menonton",['Netflix',"Disney+","Youtube","Lainnya"])
            with ka:
                rate = st.slider('Rating pribadi 1-10' , 0,10,0)
            fav= st.checkbox("Tanda Favorit")
            komen = st.text_area("Catatan Pribadi",placeholder="Masukkan Komentar Anda Disini")

            _,batal,simpan=st.columns([4,1,2])
            with batal:
                if st.button("Batal"):
                            st.switch_page(f'pages/{st.session_state['asal'].split('_')[0]}.py')    
            with simpan:
                if st.button("Simpan ke Filmku",type='primary'):
                           st.success("Data Berhasiil Disimpan")
        elif simpan_status == 'Sedang Ditonton':
             ki,t,ka=st.columns(3)
             with ki:
                 sdg_tgl = st.date_input("Tanggal Mulai Menonton")
             with t:
                 terakhir = st.text_input("Durasi Nonton Terakhir",placeholder="Contoh : 00.00.00 / 45 menit")
             with ka:
                 pntn = st.selectbox("Tempat Menonton",['Netflix',"Disney+","Youtube","Lainnya"]) 
             target = st.date_input("Target Selesai Menonton")
             komen = st.text_area("Catatan pribadi saat ini",placeholder="Masukkan Komentar Anda Disini, Apakah sejauh ini ada yang menarik?")
             _,batal,simpan=st.columns([4,1,2])
             with batal:
                if st.button("Batal"):
                    st.switch_page(f'pages/{st.session_state['asal'].split('_')[0]}.py')    
             with simpan:
                if st.button("Simpan ke Filmku",type='primary'):
                    st.success("Data Berhasiil Disimpan")
        elif simpan_status == 'Ingin Ditonton':
             st.warning("Rating dan tanggal diisi nanti, setelah filmnya selesai ditonton.")
             ki,t,ka=st.columns(3)
             with ki :
                  pntn = st.selectbox("Rencana Tempat Menonton",['Netflix',"Disney+","Youtube","Lainnya"]) 
             with t: 
                  ingin_tgl = st.date_input("Tanggal Rencana Menonton")
             with ka:
                  prioritas = st.selectbox("Prioritas Menonton",['Tinggi','Sedang','Rendah'])
             ingat = st.checkbox("Ingatkan saya saat tanggal target tiba")
             komen= st.text_area("Alasan ingin menonton / note ",placeholder="Direkomendasikan teman, tertarik dengan sutradara/aktornya..")
             _,batal,simpan=st.columns([4,1,2])
             with batal:
                if st.button("Batal"):
                    st.switch_page(f'pages/{st.session_state['asal'].split('_')[0]}.py')    
             with simpan:
                if st.button("Simpan ke Filmku",type='primary'):
                    st.success("Data Berhasiil Disimpan")