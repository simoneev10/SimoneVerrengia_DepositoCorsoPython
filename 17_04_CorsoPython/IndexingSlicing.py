import numpy as np

arr = np.array([1,2,3,4,5])

print("Array completo: ",arr)
print("Prove di Indexing e Sliding: ")

#Indexing
print(arr[0])

#Slicing
print(arr[2:4])

#Boolean Indexing
print(arr[arr>2])