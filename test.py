import requests

# api from geojs.io
resp = requests.get("https://get.geojs.io/v1/ip/geo.json")
data = resp.json()
latitude = data["latitude"]
longitude = data["longitude"]
print(f"geojs.io: {latitude}, {longitude}")

response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,precipitation,weather_code&timezone=auto")
data = response.json()
current_units = data["current_units"]
current_values = data["current"]

timezone = f"Location: {data["timezone"]}"
last_updated_time = f" Last Updated: {current_values["time"][11:]}"
temperature = f"Temp: {current_values["temperature_2m"]} {current_units["temperature_2m"]}"
precipitation = f"Precip: {current_values["precipitation"]} {current_units["precipitation"]}"
weather_code = f"WMO: {current_values["weather_code"]}"

print(timezone)
print(last_updated_time)
print(temperature)
print(precipitation)
print(weather_code)