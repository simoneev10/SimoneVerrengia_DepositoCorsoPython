import numpy as np

def reshape(val):
    appo = np.array(val)
    righe = int(input("Inserire righe: "))
    colonne = int(input("Inserire colonne: "))
    if righe * colonne != len(appo):  # era: len(arr)
        print(f"Errore: {righe}x{colonne} = {righe*colonne} elementi, ma l'array ne ha {len(appo)}")
        return appo
    return appo.reshape(righe, colonne)

while True:
    scelta = input("Vuoi creare un numpy array (s/n)?: ").lower()
    match scelta:
        case "s":
            tipo = input("Vuoi usare SIZE (numero elementi) o STEP (passo)? (s/t): ").lower()
            inizio = int(input("Inserire inizio: "))
            fine = int(input("Inserire fine: "))

            if tipo == "s":
                dim = int(input("Inserisci numero elementi (size): "))
                arr = np.linspace(inizio, fine, num=dim, dtype=int)
                print("\nArray creato con size (elementi equidistanti):")
                secscelta = input("Vuoi usare usare il reshape? (s/t): ").lower()
                if secscelta == "s":
                    resharr = reshape(arr)
                    print(resharr)

            elif tipo == "t":
                step = int(input("Inserisci passo (step): "))
                arr = np.arange(inizio, fine, step)
                print("\nArray creato con step:")
            else:
                print("Scelta non valida. Usa 's' per size o 't' per step.")
                continue

            franco = np.array(arr)
            print(arr)
            print(franco)

        case "n":
            print("Bye bye brother!")
            break
        case _:
            print("Scelta non valida. Inserisci 's' o 'n'.")
