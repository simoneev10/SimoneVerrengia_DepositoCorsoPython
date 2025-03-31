#Esercizio scelta operazione
#Inserimento
numA = int(input("Inserire primo numero: "))
numB = int(input("Inserire secondo numero: "))
#scelta dell'operazione
operazione = input("Che operazione vuoi svolgere?\n 1)Addizione\n2) Sottrazione\n3) Moltiplicazione\n4) Divisione\n: ")
#Utilizzo lo switch per la selezione dell'operazione
match operazione:
    case "1":
        ris = numA + numB
        print("Il risultato è: ", ris)
    case "2":
        ris = numA - numB
        print("Il risultato è: ", ris)
    case "3":
        ris = numB * numA
        print("Il risultato è: ", ris)
    case "4":
        if numA == 0 or numB == 0:
            print("Operazione non valida")
        else:
            ris = numA / numB
            print("Il risultato è: ", ris)
    case _:
        print("Operazione non consentita")