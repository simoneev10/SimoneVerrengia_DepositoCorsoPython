import random

#creo la funzione per creare un numero casuale da 1 a 100
def numcas():
    return random.randint(1,100)
#Salvo il numero casuale in una variabile   
numeroCasuale = numcas()
print(f"numcas", numeroCasuale) #Stampo il numero per indovinare :')

while True:
    scelta = int(input("Prova ad indovinare che numero ho scelta tra 1 e 100!\nLa tua scelta: "))
    #Vedo se il numero scelto è più grande o più piccolo
    if scelta < numeroCasuale:
        print(f"Peccato! {scelta} è più piccolo")
    elif scelta > numeroCasuale:
        print(f"Peccato! {scelta} è più grande")
    else:
        print("Complimenti, hai indovinato!")
        break
        