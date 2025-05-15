#Esercizio Completo     
        
numeri = []
cond = True
#Gestisco l'inserimento e riempio la lista        
while cond:
    ins = input("Vuoi continuare ad inserire: (s/n): ")
    match ins:
        case "s":
            num= int(input("Inserisci numero: "))
            #Aggiungo i numeri alla lista
            numeri.append(num)
        case "n":
            #Uscita dal ciclo
            cond = False
        case _:
            print("Input non valido. Usa 's' o 'n'.")
        
size = len(numeri)
#Simulo un conteggio 
while  size > 0:
        print("Conteggio in corso...\nCi sono", size, "valori")
        size = size - 1
#Controllo e stampo il più grande   
if len(numeri) < 1:
    print("\nLista vuota")
else:
    print("\nIl numero più grande della lista è:", max(numeri))