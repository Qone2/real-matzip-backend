import requests
import json
from urllib.parse import quote_plus

resp1 = requests.get("http://localhost:8000/matzip").json()

for re in resp1:
    de = requests.delete("http://localhost:8000/matzip/" + str(re["id"]))
