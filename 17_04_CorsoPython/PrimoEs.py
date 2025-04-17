# Crea un array NumPy utilizzando arange e
# verifica il tipo di dato (dtype) e la forma
# (shape) dell'array. Utilizza arange, dtype, shape, arange

import numpy as np

arr = np.arange(10,49) # Tramite arange creo un array con una seqenza di valori compresi tra 10 e 49

print(arr)
print(arr.dtype)
print(arr.shape)

arr = np.arange(10,49, dtype='float64') # Cambio il tipo in float64
print(arr)
print(arr.dtype)
print(arr.shape)