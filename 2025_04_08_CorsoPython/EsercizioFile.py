# Esercizio: scrivere 5 numeri random e provare ad indovinare

from random import randint

numeri = []
for i in range(5):
    numeri.append(str(randint(1,100)))
    
numeri_salvati = ",".join(numeri)

def scrittura(stringa):
    with open("prova.txt","w") as file:
        file.write(stringa)

def lettura(stringa):
    with open("prova.txt","r") as file:
        return file.read(stringa)
        

testo = scrittura(numeri_salvati)
letto = lettura(testo)
num_letti = letto.split(",")


print(num_letti)
for num in range(2):
    scelta = input("Inserisci un numero: ")
    if scelta in num_letti:
        print("Hai indovinato!")
    else:
        print("Hai sbagliato!")

