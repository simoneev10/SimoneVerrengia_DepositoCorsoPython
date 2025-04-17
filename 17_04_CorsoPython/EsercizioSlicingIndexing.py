import numpy as np


# 1. Crea un array NumPy 1D di 20 numeri interi casuali compresitra 10 e 50.
arr = np.random.randint(10,50,20)
print(arr)
# 2. Utilizza lo slicing per estrarre i primi 10 elementidell'array.
print(arr[:10])
# 3. Utilizza lo slicing per estrarre gli ultimi 5 elementidell'array.
print(arr[-5:])
# 4. Utilizza lo slicing per estrarre gli elementi dall'indice 5all'indice 15 (escluso).
print(arr[5:15])
# 5. Utilizza lo slicing per estrarre ogni terzo elemento dell'array.
print(arr[::3])
# 6. Modifica, tramite slicing, gli elementi dall'indice 5all'indice 10 (escluso) assegnando loro il valore 99.
arr[5:10] = 99
print(arr)


