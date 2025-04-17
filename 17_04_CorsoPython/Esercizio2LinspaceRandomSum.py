import numpy as np

class GestioneArray:
    def __init__(self):
        self.arr_equi = None
        self.arr_rand = None
        self.arr_somma = None
        self.somma_totale = None
        self.somma_magg5 = None

    def crea_array_equidistante(self): # Dentro la funzione sfrutto il metodo linspace per creare l'array equidistante
        inizio = int(input("Inserisci inizio: "))
        fine = int(input("Inserisci fine: "))
        dim = int(input("Inserisci dimensione: "))
        self.arr_equi = np.linspace(inizio, fine, dim)
        print("Array equidistante creato:\n", self.arr_equi)

    def crea_array_casuale(self): # Dentro la funzione sfrutto il metodo random.rand per creare l'array di numeri tra 0 ed 1
        dim = int(input("Inserisci dimensione: "))
        self.arr_rand = np.random.rand(dim)
        print("Array casuale di numeri tra 0 ed 1 creato:\n", self.arr_rand)

    def somma_array(self):  # Dentro la funzione sfrutto il metodo sum per effettuare la somma dei due array
        if self.arr_equi is not None and self.arr_rand is not None: # Controllo per vedere se si può effettuare la somma
            if len(self.arr_equi) != len(self.arr_rand):
                print("Errore: gli  devarrayono avere la stessa dimensione.")
                return
            self.arr_somma = self.arr_equi + self.arr_rand
            self.somma_totale = np.sum(self.arr_somma)
            print("Somma completata.")
        else:
            print("Devi prima creare entrambi gli array.")

    def somma_maggiore_di_5(self): # Dentro la funzione sfrutto il metodo sum per effettuare la somma ed in più la potenza di numpy dentro le []
        if self.arr_somma is not None:
            self.somma_magg5 = np.sum(self.arr_somma[self.arr_somma > 5])
            print("Somma degli elementi > 5 calcolata.")
        else:
            print("Calcola prima la somma degli array.")

    def somma_elementi_array(self): # Menu per vedere quale degli array creati si vuole sommare
        print("\nScegli l'array da sommare:")
        print("1. Array equidistante")
        print("2. Array casuale")
        print("3. Array somma")

        scelta = input("Inserisci scelta (1-3): ")
        match scelta:
            case "1":
                if self.arr_equi is not None:
                    print("Somma degli elementi (equidistante):", np.sum(self.arr_equi))
                else:
                    print("Array equidistante non disponibile.")
            case "2":
                if self.arr_rand is not None:
                    print("Somma degli elementi (casuale):", np.sum(self.arr_rand))
                else:
                    print("Array casuale non disponibile.")
            case "3":
                if self.arr_somma is not None:
                    print("Somma degli elementi (somma):", np.sum(self.arr_somma))
                else:
                    print("Array somma non disponibile.")
            case _:
                print("Scelta non valida.")

    def stampa_risultati(self): # Stampa totale
        print("\nRisultati: ")
        print("Array equidistante:", self.arr_equi)
        print("Array casuale di numeri tra 0 ed 1:", self.arr_rand)
        print("Array somma:", self.arr_somma)
        print("Somma totale:", self.somma_totale)
        print("Somma elementi > 5:", self.somma_magg5)

    def menu(self): # Menu per la gestione completa
        while True:
            print("\n--- Menu ---")
            print("1. Crea array equidistante")
            print("2. Array casuale di numeri tra 0 ed 1")
            print("3. Somma gli array")
            print("4. Somma elementi > 5")
            print("5. Stampa risultati")
            print("6. Somma elementi in un singolo array")
            print("7. Esci")

            scelta = input("Scegli un'opzione: ")

            match scelta:
                case "1":
                    self.crea_array_equidistante()
                case "2":
                    self.crea_array_casuale()
                case "3":
                    self.somma_array()
                case "4":
                    self.somma_maggiore_di_5()
                case "5":
                    self.stampa_risultati()
                case "6":
                    self.somma_elementi_array()
                case "7":
                    print("Uscita dal programma.")
                    break
                case _:
                    print("Scelta non valida.")

# Avvio del programma
if __name__ == "__main__":
    app = GestioneArray()
    app.menu()
