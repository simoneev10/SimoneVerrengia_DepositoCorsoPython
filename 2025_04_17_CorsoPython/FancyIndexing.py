import numpy as np

arr = np.arange(10,60,10)

print(arr)

# Utilizzo un array di indici
indices = np.array([1,3])
print(arr[indices])
# Utilizzo una lista di indici
indiceSec = [0,2,4]
print(arr[indiceSec])