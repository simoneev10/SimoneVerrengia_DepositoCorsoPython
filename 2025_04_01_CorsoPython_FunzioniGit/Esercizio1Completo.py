#Imposto un ciclo fino a quando la condizione di inserimento di un positivo è soddisfatta
while True:
    numero = int(input("Inserisci un intero positivo: "))
    if numero <= 0:
        print("Riprova: ")
    else:
        scelta = input("Verrà creato un intervallo da 1 al numero inserito.\nVuoi fare la somma dei numeri pari o stampare tutti i numeri dispari? (p/d): ").lower()
        match scelta:
            case "p": #Caso somma pari
                #Creo un var di appoggio per la somma ed il mio range con il numero inserito
                sommaPari = 0
                numeri = [*range(1,numero+1)]
                for num in range(1,numero+1,1):
                    if num % 2 == 0:
                        sommaPari += num
                print(f"La somma dei numeri pari a 1 a {numero} è {sommaPari}")
                #Controllo se il numero è primo
                isPrimo = True
                for i in range(2, int(numero**0.5) + 1):
                    if numero  % i == 0:
                        isPrimo = False
                if isPrimo: 
                    print(f"il numero {numero} inserito è primo!")
            
                else:
                    print(f"il numero {numero} inserito non è primo!")
            case "d":#Caso stampa numeri dispari
                numeri = [*range(1,numero+1)]
                print(f"I numeri dispari da 1 a {numero} sono:")
                for num in range(1,numero+1,1):
                    if num % 2 != 0:
                        print(f"{num}")
                #Controllo se il numero è primo
                isPrimo = True
                for i in range(2, int(numero**0.5) + 1):
                    if numero  % i == 0:
                        isPrimo = False
                if isPrimo: 
                    print(f"il numero {numero} inserito è primo!")
            
                else:
                    print(f"il numero {numero} inserito non è primo!")
                
        break        

print("Sei uscito")