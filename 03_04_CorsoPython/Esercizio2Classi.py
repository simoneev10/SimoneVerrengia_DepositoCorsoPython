class Libro:
    def __init__(self, titolo, autore, npagine):
        self.titolo = titolo
        self.autore = autore
        self.npagine = npagine
        
    def descrizione(self): # Metodo per stampare le info del libro
        print(f"Il titolo del libro è {self.titolo} è stato scritto da {self.autore} ed ha {self.npagine} pagine.")

# Creazione di oggetto di tipo Libro        
Libro1 = Libro("Franco il contadino","Franco FF", "540")
Libro1.descrizione()