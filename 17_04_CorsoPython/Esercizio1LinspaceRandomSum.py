import numpy as np

arr = np.linspace(0,1,12)
arr2d = arr.reshape(3,4)
sommaMatLin = arr2d.sum()
matriceCasuale = np.random.rand(3, 4)
sommaMatCasuale = matriceCasuale.sum()

while True:
    print("\nMENU ARRAYGIANTE")
    print("1. Stampa array lineare (0-1 con 12 elementi)")
    print("2. Stampa array con reshape (3x4)")
    print("3. Stampa somma primo array")
    print("4. Stampa matrice casuale 3x4")
    print("5. Stampa somma matrice casuale")
    print("0. Esci")

    scelta = input("Scegli un'opzione (0-5): ")

    if scelta == "1":
        print("\nArray lineare:")
        print(arr)
    elif scelta == "2":
        print("\nArray con Reshape(3x4):")
        print(arr2d)
    elif scelta == "3":
        print("\nSomma primo array: ")
        print(arr2d.sum())
    elif scelta == "4":
        print("\nMatrice casuale 3x4:")
        print(matriceCasuale)
    elif scelta == "5":
        print("\nSomma matrice casuale:")
        print(matriceCasuale.sum())
    elif scelta == "0":
        print("Programma terminato.")
        break
    else:
        print("Scelta non valida. Riprova.")