import requests

# note to self, always lat before long

# api from ipinfo.io
resp = requests.get("https://ipinfo.io/json")
loc = resp.json()["loc"]
print(f"Ipinfo: {loc}")

# api from ip-api.com
resp = requests.get("http://ip-api.com/json")
data = resp.json()
latitude = data["lat"]
longitude = data["lon"]
print(f"ip-api: {latitude}, {longitude}")

# api from ipapi.co
resp = requests.get("https://ipapi.co/json")
data = resp.json()
papi_latitude = data["latitude"]
papi_longitude = data["longitude"]
print(f"ipapi: {papi_latitude}, {papi_longitude}")