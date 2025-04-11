# L'utente potrà scegliere se visionarle dei prossimi 1, 3 o 7 giorni e se
# visionare oltre che le temperature anche la velocità del vento e le
# probabili precipitazioni.
import requests

import requests

# Funzione per ottenere latitudine e longitudine della città inserita
def get_coordinates(citta):
    urlCitta = f"https://geocoding-api.open-meteo.com/v1/search?name={citta}&count=1&language=it&format=json"
    response = requests.get(urlCitta)
    data = response.json()
    location = data["results"][0]
    return location["latitude"], location["longitude"]

# Funzione per ottenere le previsioni meteo in base a latitudine, longitudine e giorni
def get_forecast(lat, lon, giorni):
    urlGiorni = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,wind_speed_10m_max,precipitation_sum&forecast_days={giorni}"
    response = requests.get(urlGiorni)
    return response.json()

# Funzione per stampare i dati delle previsioni meteo
def stampa_previsioni(diz, citta, giorni):
    temp_max = diz["daily"]["temperature_2m_max"]
    temp_min = diz["daily"]["temperature_2m_min"]
    vento = diz["daily"]["wind_speed_10m_max"]
    precipitazioni = diz["daily"]["precipitation_sum"]

    print(f"\nSalve! Qui a {citta} per i prossimi {giorni} giorni:")
    for i in range(giorni):
        print(f"\nGiorno {i+1}:")
        print(f"  Temperatura massima: {temp_max[i]}°C")
        print(f"  Temperatura minima: {temp_min[i]}°C")
        print(f"  Velocità massima del vento: {vento[i]} km/h")
        print(f"  Precipitazioni totali: {precipitazioni[i]} mm")

# Funzione che gestisce il menu usando match-case
def menu():
    print("\n1. Visualizza previsioni\n2. Esci")
    scelta = input("Cosa desideri fare: ")

    match scelta:
        case "1":
            citta = input("Inserire la città di cui si vogliono le previsioni: ")
            lat, lon = get_coordinates(citta)

            giorni = int(input("Di quanti giorni vuoi vedere (1, 3 o 7): "))
            while giorni not in [1, 3, 7]:
                print("Inserisci un valore valido (1, 3 o 7)")
                giorni = int(input("Di quanti giorni vuoi vedere (1, 3 o 7): "))

            dati = get_forecast(lat, lon, giorni)
            stampa_previsioni(dati, citta, giorni)
            menu()  # Richiamo ricorsivo per tornare al menu

        case "2":
            print("Uscita dal programma.")
            return

        case _:
            print("Scelta non valida.")
            menu()  # Richiamo ricorsivo per tentare di nuovo

# Punto di ingresso del programma
def main():
    menu()

# Avvio del programma
if __name__ == "__main__":
    main()
