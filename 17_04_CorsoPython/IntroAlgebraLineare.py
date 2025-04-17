import numpy as np

#Creazione matrice quadrata
A = np.array([[1,2], [3,4]])
print("Matrice A: \n",A)
#Calcolo inversa della matrice
A_inv = np.linalg.inv(A)
print("Inversa di A: \n",A_inv)

#Creazione di un vettore
v = np.array([3,4])
print("Vettore v: \n",v)

#Calcolo della norma del vettore
norm_v = np.linalg.norm(v)
print("Norma di v: \n", norm_v)