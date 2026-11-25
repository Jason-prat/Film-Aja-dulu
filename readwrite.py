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
# def tambah(data_tambah):

@st.cache_resource
def ambildb():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
 
