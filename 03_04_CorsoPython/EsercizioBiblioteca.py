class Libro: # Creo classe libro con Titolo, Autore e Numero di pagine
    def __init__(self, titolo, autore, npagine):
        self.titolo = titolo
        self.autore = autore
        self.npagine = npagine
        
    def descrizione(self): # Metodo per stampare le info del libro
        print(f"Il titolo del libro è {self.titolo} è stato scritto da {self.autore} ed ha {self.npagine} pagine.")

class Biblioteca: # Creo la classe libro dove contenere le istanze di libro
    def __init__(self):
        self.libreria = []
        
    def crea_libro(self): # Funzione per l'inserimento del libro
        titolo = input("Inserisci titolo: ")
        autore = input("Inserisci autore: ")
        npagine = int(input("Inserisci numero pagine: "))
        nuovo_libro = Libro(titolo, autore, npagine) # Creazione del nuovo libro con costruttore
        self.libreria.append(nuovo_libro) # Aggiungo alla libreria
    
    def stampa_libreria(self): # Funzione per stampare la libreria
        for libro in self.libreria:
            libro.descrizione()

biblio1 = Biblioteca()
print("Benvenuto nella biblioteca!")

while True: # Creazione di menù interattivo per l'utente con le varie opzioni disponibili per l'utente
    scelta = int(input("\n1) Aggiungere un libro\n2) Visualizzare i libri\n3) Uscire\n: "))
    if scelta == 1:
        biblio1.crea_libro()
        print("Libro aggiunto con successo!")
    elif scelta == 2:
        if not biblio1.libreria:
            print("Nessun libro presente nella libreria.")
        else:
            print("Ecco i libri presenti nella libreria:")
            biblio1.stampa_libreria()
    elif scelta == 3:
        print("Arrivederci!")
        break
    else:
        print("Scelta non valida. Riprova.")


