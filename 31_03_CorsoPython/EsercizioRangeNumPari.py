# #Chiedi all'utente di inserire un numero e far partire un conto alla rovescia

# ins = int(input("Inserire un numero dal quale far parire il conto alla rovescia: "))

# for numero in range(ins,0,-1):
#     print(numero)
    

#Numeri pari     
#Creo Lista per contenere i 5 numeri pari
numeriPari = []
#Setto questo while in modo che non si fermi finchè non completo la mia lista da 5
while len(numeriPari) < 5 :
        numero = int(input("Inserire un numero: "))
        if numero % 2 == 0: #Controllo se il numero è pari
            print("il numero", numero, "è pari!")
            numeriPari.append(numero)
        else:
            print(numero, "non è un numero pari. Riprova:")
        print(numeriPari)
        
print("Complimenti hai inserito 5 numeri pari!")