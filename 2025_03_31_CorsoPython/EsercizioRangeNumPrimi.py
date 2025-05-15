#Numeri primi     
#Creo Lista per contenere i 5 numeri primi
numeriPrimi = []
#Setto questo while in modo che non si fermi finchè non completo la mia lista da 5
while len(numeriPrimi) < 5 :
        numero = int(input("Inserire un numero: "))
        isPrimo = True
        for i in range(2, int(numero**0.5) + 1):
            if numero  % i == 0:
                isPrimo = False
        if isPrimo: #Controllo se il numero è primo
            print("il numero", numero, "è primo!")
            numeriPrimi.append(numero)
        else:
            print(numero, "non è un numero primo. Riprova:")
        print(numeriPrimi)
        
print("Complimenti hai inserito 5 numeri primi!")