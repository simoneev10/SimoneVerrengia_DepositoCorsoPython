import numpy as np

arr_2d = np.array([[1,2,3,4],
                  [5,6,7,8],
                  [9,10,11,12]])

# Slicing sulle righe
print(arr_2d[1:3]) # Prendo solo la seconda e terza riga

# Slicing sulle colonne 
print(arr_2d[:,1:3]) # prendo tutte le righe, ma le colonne da posizione 1 a 3

# Slicing misto
print(arr_2d[1:,1:3]) # dalla riga 1 in poi, e collonne dalla 1 alla 3 (sempre come posizioni)

print("----------------------------------------------")
arrone = np.arange(0,10)
print(arrone)

# Slicing base
print(arrone[2:7])

# Slicing con passo
print(arrone[1:8:2])

# Omettere start and stop
print(arrone[:5])
print(arrone[5:])

# Utilizza indici negativi
print("print(arrone[-5:])\n",arrone[-5:])
print("print(arrone[:-5])\n",arrone[:-5])