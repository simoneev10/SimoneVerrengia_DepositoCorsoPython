numeri = []

#Funzione che ritorna il quadrato dei numeri presi in input
def quadrato(lista):
    return [numero*numero for numero in lista]

#Somma dei quadrati
def sommaQuadrato(inserimento):
    somma = 0
    for num in inserimento:
        somma += num
    return somma

#Scelta di quanti e quali numeri da inserire 
def inserimento():
    ins = int(input("\nQuanti numeri vuoi inserire?: "))
    #Chiedo all'utente quanti numeri vuole inserire
    while ins > 0:
        num = int(input("Inserisci numero: "))
        numeri.append(num)
        ins -= 1

def molt(lista):
    sommamolt = 1
    for num in lista:
        sommamolt *= num
    return sommamolt

#Inizio dall 'inserimento dei dati
inserimento()
#Richiamo le funzioni e salvo i risultati
quadrati = quadrato(numeri)
somma = sommaQuadrato(quadrati)

print(f"\nI numeri inseriti sono: {numeri}")
print(f"I quadrati dei numeri inserirti sono: {quadrati}\n")

#Ciclo per simulare le scelte
while True:
    scelta = input("Vuoi inserire un'altra lista di numeri? (s/n): ").lower()
    if scelta == "s":
        inserimento()
        scelta2 = input("Vuoi moltiplicare tutti i numeri inseriti? (s/n): ").lower()
        if scelta2 == "s":
            ris = molt(numeri)
            print(f"\nLa moltiplicazione di tutti i numeri inseriti è: {ris}")
            break
        else:
            break
    else:
        break
                            
print(f"\nLa somma dei quadrati è: {somma}\n")


