import numpy as np

# Crea la matrice 6x6 con numeri tra 1 e 100
arr2d = np.random.randint(1, 101, size=(6, 6))

# Stampa la matrice
print("Matrice 6x6 con valori casuali tra 1 e 100:")
print(arr2d,"\n")
# Sotto-matrice centrale 4x4
print("Sotto-matrice centrale 4x4:\n",arr2d[1:5,1:5],"\n")
# Diagonale principale della matrice invertita
# Inverto per prima cosa la matrice
arr2d_invertita = np.fliplr(arr2d) 
print("Matrice invertita:")
print(arr2d_invertita,"\n")
# Estraggo la diagonale
diagonale = np.diag(arr2d_invertita)
print("\nDiagonale principale della matrice invertita:")
print(diagonale,"\n")

# Sostituisci tutti i valori multipli di 3 della matrice invertita con -1
# for i in range(len(arr2d_invertita)):
#     for j in range(len(arr2d_invertita[0])):
#         if arr2d_invertita[i][j] % 3 == 0:
#             arr2d_invertita[i][j] = -1
# Metodo Numpy
arr2d_invertita[arr2d_invertita % 3 == 0] = -1

print("Matrice Invertita con multipli di 3 sostituiti con -1:\n",arr2d_invertita,"\n")
