#ini halamannya buat baca file sama write ke json
import json
from supabase import create_client
import streamlit as st


def login(db,username,password):
    cek=db.table('users').select('*').eq('username',username).execute()
    if cek.data[0]['password']==password:
        return True
    else:
        return False
    # return False
def register(db,username,password):
    cek=db.table('users').select('id').eq('username',username).execute()
    if cek.data:
        return False
    
    db.table('users').insert({
        'username':username,
        'password':password
    }).execute()
    return True

def profile(db,username):
    cek= db.table('users').select('*').eq('username',username).execute()
    return cek.data


def tambah(db,username,tmdb_id,status,tempat,tgl_tonton,catatan=None,rating_pribadi=None,favorit=None,durasi_terakhir=None,target_selesai=None,prioritas=None):
    data = {
        'username':username,
        'tmdb_id':tmdb_id,
        'status':status,
        'tempat': tempat,
        'tgl_tonton':tgl_tonton.isoformat(),
        'catatan':catatan or None,
        'rating_pribadi':rating_pribadi,
        'favorit': favorit,
        'durasi_terakhir':durasi_terakhir or None,
        'target_selesai':target_selesai.isoformat() if target_selesai else None,
        'prioritas':prioritas
    }
    try:
        db.table('film').insert(data).execute()
        return True, "Data Berhasil Diambil"
    except Exception as kecuali:
        if '23505' in str(kecuali) or "duplicate" in str(kecuali).lower():
            return False, "Film ini sudah ada di Filmku"
        return False, f"Gagal menyimpan: {kecuali}"

def status_tonton(username):
    db=ambildb()
    dats = db.table("film").select("tmdb_id,status").eq("username",username).execute()
    return {datas["tmdb_id"]:datas['status'] for datas in dats.data}

@st.cache_resource
def ambildb():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def ambil_riwayat(db, username):
    return db.table('film').select('*').eq('username', username).execute().data
 
