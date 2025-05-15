import numpy as np

#Creazione array casuale di numeri compresi tra 1 e 100
arr = np.random.randint(1,101,15)
print("Array casuale di numeri compresi tra 1 e 100: \n", arr)

#Calcolo la somma degli elementi presenti nell'array 
somma = arr.sum()
print("La somma degli elementi presenti nell'array è: ",somma)

#Calolo la media degli elementi presenti nell'array 
media = arr.mean()
print("La media degli elementi presenti nell'array è: ",media)