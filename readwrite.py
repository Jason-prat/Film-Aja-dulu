#ini halamannya buat baca file sama write ke json
import json

file = "dbuser.json"

def baca_usn ():
   try:
        with open (file,encoding="utf-8") as fl:
            return json.load(fl)
   except FileNotFoundError:
        return {}
   
def tulis_usn(data):
    with open (file,'w',encoding='utf-8') as tulis:
        return json.dump(data,tulis,indent=2)
