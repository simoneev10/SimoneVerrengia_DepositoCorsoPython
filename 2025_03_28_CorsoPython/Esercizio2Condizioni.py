#Secondo esercizio
#lista pre inserita
elementi = ["Cane","Gatto","Pesce","Serpente"]
print("Data la lista \n",elementi, "\nPuoi effettuare una delle operazioni CRUD con la lettera minuscola appropriata")
lettera = input("inserisci l'operazione che vuoi svolgere: ")
#varie scelte
if lettera.lower() == "c":
    elementi.append("Lupo")
    print(elementi)
elif lettera.lower() == "r":
    print(elementi)
elif lettera.lower() == "u":
    elementi[-1] = "Basilisco"
    print(elementi)
else:
    elementi.remove(elementi[1])
    print(elementi)