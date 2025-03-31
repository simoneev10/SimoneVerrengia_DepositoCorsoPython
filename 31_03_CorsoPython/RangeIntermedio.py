num1 = int(input("Inserisci il primo numero dell'intervallo: "))
num2 = int(input("Inserisci il secondo numero dell'intervallo: "))
#Tramite l'operatore splat creo la mia lista con l'intervallo inserito
numeriPrimi = [*range(num1,num2+1)]
i = 0
#Itero tutto l'intervallo servendomi di un ciclatore i
while i < len(numeriPrimi):
    numero = numeriPrimi[i]
    if numero <= 1:
        #Se la condizione è verificata non è primo e lo rimuovo dalla lista
        numeriPrimi.pop(i)
        continue
    
    isPrimo = True
    #Tramite questo ciclo e la condizione impostata su isPrimo controllo che gli altri numeri dell'intervallo siano primi
    for n in range(2,int(numero**0.5) + 1):
        if numero % n == 0:
            isPrimo = False
            break
    #Vado avanti nel ciclo
    if isPrimo:
        i = i+1
    else:
        numeriPrimi.pop(i)
#Stampo tutti i numeri primi dell'intervallo        
print(f"Numeri primi nell'intervallo [{num1},{num2}]: ", numeriPrimi)
            