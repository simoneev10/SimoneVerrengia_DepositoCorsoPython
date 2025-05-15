#Primo esercizio
print("Procediamo con il gioco delle scale")
numero = int(input("Inserici un numero: "))
if numero > 15:
    numero = int(input("Ottimo! Inserici un altro numero: "))
    if numero > 30:
        numero = int(input("Okay, adesso prova ad indovinare. Inserici un numero: "))
        if numero == 50:
            print("Grande, gioco concluso!")
            