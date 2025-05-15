import numpy as np

arr = np.arange(1,26)
matrice = arr.reshape(5,5)
print("La matrice 5x5 dei numeri squenziali da 1 a 25 è:\n", matrice)

terzaRiga = matrice[2:3]
print("La terza riga estratta dalla matrice è: \n",terzaRiga)

diagonalePrincipale = np.diag(matrice)
print("La diagonale principale è: \n", diagonalePrincipale)

sommaDiag = diagonalePrincipale.sum()
print("La somma degli elementi sulla diagonale principale è: ", sommaDiag)