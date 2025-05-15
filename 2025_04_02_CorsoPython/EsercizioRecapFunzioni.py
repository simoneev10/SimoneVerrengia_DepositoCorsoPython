#Funzione che ritorna il quadrato dei numeri presi in input
def quadrato(lista):
    return [numero*numero for numero in lista]

#Somma dei quadrati
def sommaQuadrato(inserimento):
    somma = 0
    for num in inserimento:
        somma += num
    return somma


ins = int(input("Quanti numeri vuoi inserire?: "))
numeri = []
#Chiedo all'utente quanti numeri vuole inserire
while ins > 0:
    num = int(input("Inserisci numero: "))
    numeri.append(num)
    ins -= 1

#Richiamo le funzioni e salvo i risultati
quadrati = quadrato(numeri)
somma = sommaQuadrato(quadrati)

print(f"\nI numeri inseriti sono: {numeri}")
print(f"I quadrati dei numeri inserirti sono: {quadrati}")
print(f"La somma dei quadrati è: {somma}\n")

