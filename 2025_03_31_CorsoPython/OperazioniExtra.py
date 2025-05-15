#Esercizio scelta operazione
#Inserimento
numA = int(input("Inserire primo numero: "))
numB = int(input("Inserire secondo numero: "))
#scelta dell'operazione
operazione = input("Che operazione vuoi svolgere?\n 1)Addizione\n2) Sottrazione\n3) Moltiplicazione\n4) Divisione\n5)Operazione multipla\n: ")
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
    case "5":
        operatore1 = input("Inserisci il primo operatore (+, -, *, /): ")
        operatore2 = input("Inserisci il secondo operatore (+, -, *, /): ")
            # applico il primo operatore
        if operatore1 == "+":
                risultato = numA + numB
        elif operatore1 == "-":
                risultato = numA - numB
        elif operatore1 == "*":
                risultato = numA * numB
        elif operatore1 == "/":
            if numB != 0:
                    risultato = numA / numB
            else:
                    risultato = "Impossibile dividere per zero"
        else:
            risultato = "Operatore non valido"
            # ora applico il secondo operatore   
        if operatore2 == "+":
            risultato += numB
            print("Il risultato della combinazione di operazioni è:", risultato)
        elif operatore2 == "-":
            risultato -= numB
            print("Il risultato della combinazione di operazioni è:", risultato)
        elif operatore2 == "*":
            risultato *= numB
            print("Il risultato della combinazione di operazioni è:", risultato)
        elif operatore2 == "/":
            if numB != 0:
                risultato /= numB
                print("Il risultato della combinazione di operazioni è:", risultato)
            else:
                risultato = "Impossibile dividere per zero"
        else:
                risultato = "Operatore non valido"
    case _:
        print("Operazione non consentita")