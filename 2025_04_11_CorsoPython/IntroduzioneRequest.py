import requests

url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,rain,visibility"
response = requests.get(url)
dizionario = response.json()

print(dizionario["hourly"]["rain"])