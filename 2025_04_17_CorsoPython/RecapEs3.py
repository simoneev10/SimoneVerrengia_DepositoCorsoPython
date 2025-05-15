import numpy as np

# 1) Creare un array 4x4 con numeri interi casuali tra 10 e 50
arr = np.random.randint(10, 51, size=(4, 4))
print("\nArray 4x4 :\n", arr)

# 2) Fancy indexing: selezionare e stampare elementi agli indici (0,1), (1,3), (2,2), (3,0)
righe = [0, 1, 2, 3]
colonne = [1, 3, 2, 0]
elementi_selezionati = arr[righe, colonne]
print("\nElementi selezionati con fancy indexing:\n", elementi_selezionati)

# 3) Fancy indexing: selezionare tutte le righe dispari
righe_dispari = arr[0::2]
print("\nRighe dispari della matrice:\n", righe_dispari)

# 4) Modificare gli elementi selezionati nel punto 2 aggiungendo 10
arr[righe, colonne] += 10
print("\nArray dopo aver aggiunto il valore 10 agli elementi selezionati:\n", arr)
