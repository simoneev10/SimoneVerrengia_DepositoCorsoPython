import numpy as np

#La funzione linspace genera un array di numeri equidistanti tra un valore iniziale e uno finale
arr = np.linspace(0,1,5)
print(arr,"\n")

# Serve per generare una matrice casuale 3x3
random_arr = np.random.rand(3,3)
print(random_arr)

arra = np.array([1, 2, 3, 4, 5])

sum_value = np.sum(arra)
mean_value = np.mean(arra)
std_value = np.std(arra)

print("Sum: ", sum_value)
print("Mean: ", mean_value)
print("Standard Deviation: ", std_value)