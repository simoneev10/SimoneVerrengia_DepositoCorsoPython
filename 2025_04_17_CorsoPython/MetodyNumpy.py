import numpy as np

arr = np.array([1,2,3,4,5])

arr2d = np.array([[1,2,3],[4,5,6]])

# Metodi degli array

print("Forma dell'array: ", arr.shape)
print("Dimensioni dell'array: ", arr.ndim)
print("Tipo di dati: ", arr.dtype)
print("Numero di elementi: ",arr.size)
print("Somma degli elementi: ",arr.sum())
print("Media degli elementi: ",arr.mean())
print("Valore massimo: ", arr.max())
print("Indice del valore massimo: ", arr.argmax())

# arra = np.arange(10)
# print(arra)

arra = np.arange(6)
reshaped_arra = arra.reshape((2,3))
print("Uso del reshape: \n",reshaped_arra)