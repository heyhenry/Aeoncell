import requests

# note to self, always lat before long

resp = requests.get("https://ipinfo.io/json")
loc = resp.json()["loc"]
print(f"Ipinfo: {loc}")

resp = requests.get("http://ip-api.com/json")
data = resp.json()
latitude = data["lat"]
longitude = data["lon"]
print(f"ip-api: Lat: {latitude}, Lon: {longitude}")
