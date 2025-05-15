#Ciclo matematico
conteggio = 0

while conteggio < 5:
    print(conteggio)
    conteggio += 1
    

#Ciclo booleano
attivo = True

while attivo:
    risposta = input("Vuoi continuare? (s/n): ").lower()
    
    if risposta == 'n':
        attivo = False
    elif risposta != 's':
        print("Input non valido, inserisci 's' o 'n'")