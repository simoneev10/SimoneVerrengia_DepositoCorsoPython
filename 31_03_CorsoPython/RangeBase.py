#Esercizio base inserimento

cond = True
listone = []
while cond:
    #Chiedo all'utente cosa vuole fare
    scelta = input(("Vuoi inserire una Stringa, un Numero o stampare? (s/n/p): "))
    match scelta:
        case "s":
            #Caso inserimento stringa, controllo se è pari o dispari
            parola = input("Inserisci stringa: ")
            if len(parola) % 2 == 0:
                listone.append(parola)
                print(f"La stringa {parola} è pari!")
            else:
                listone.append(parola)
                print(f"La stringa {parola} è dispari!")
        case "n":
            #Caso inserimento numero, controllo se è pari o dispari
            num= int(input("Inserisci numero: "))
            if num % 2 == 0:
                listone.append(num)
                print(f"Il numero {num} è pari!")
            else:
                listone.append(num)
                print(f"Il numero {num} è dispari!")
        case "p":
            #Caso in cui stampo la lista con controllo
            if len(listone) <= 0:
                print("La lista è vuota!")
            else:
                print(listone)
        case _:
            #Uscita dal programma
            cond = False
            print("Non si vuole inserire nulla. Uscita dal programma")
            