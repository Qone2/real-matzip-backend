import requests
import json
from urllib.parse import quote_plus

resp1 = requests.get("http://127.0.0.1:8000/matzip").json()

for re in resp1:
    de = requests.delete("http://127.0.0.1:8000/matzip/" + str(re["id"]))
