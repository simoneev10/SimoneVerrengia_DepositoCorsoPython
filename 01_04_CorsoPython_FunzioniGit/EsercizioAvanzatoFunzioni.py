def fibonacci(num):
    if num <= 0:
        return []
    elif num == 1:
        return [0]
    elif num == 2:
        return [0,1]
    seq = [0,1]
    #Ciclo per generare la sequenza di fibonacci
    for i in range(2,num):
        seq.append(seq[i-1] + seq[i-2])
    return seq
    
inserimento = int(input("\nInserisci un numero: "))
#Richiamo la funzione e la salvo in sequenza
sequenza = fibonacci(inserimento)
print(f"La sequenza di Fibonacci con il limite da te inserito [{inserimento}] è: {sequenza}")