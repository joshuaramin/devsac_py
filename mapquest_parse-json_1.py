import os
import urllib.parse
import requests
from dotenv import load_dotenv

load_dotenv()

main_api = "https://www.mapquestapi.com/directions/v2/route?"
orig = "Rome, Italy"
dest = "Frascati, Italy"
key = os.getenv("MAPQUEST_API_KEY")  

url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})

json_data = requests.get(url).json()
print(json_data)
