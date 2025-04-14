from libro import Libro

class Libreria:
    catalogo = {}
    
    def __init__(self):
        pass
    
    def aggiungi_libro(self): # Funzione per aggiungere un oggetto libro
        titolo = input("Inserisci il titolo del libro: ")
        autore = input("Inserisci nome dell'autore: ")
        libro = Libro(titolo,autore)
        self.catalogo[Libro.isbn] = (libro) # Inserisco l'oggetto libro nel catalogo
        Libro.isbn += 1
        print(f"Libro aggiunto con ISBN: {Libro.isbn - 1}")
        
    def rimuovi_libro(self): # Funzione per rimuovere libro
        isbn = int(input("Inserisci identificativo del libro da eliminare: "))
        if isbn in self.catalogo: # Lo cerco nel catalogo
            del self.catalogo[isbn]
            print(f"Il libro con identificativo {isbn} è stato eliminato")
        else:
            print(f"Il libro con identificativo {isbn} non è presente nella libreria")
    
    def mostra_catalogo(self): # Funzione per rimuovere libro
        if  not self.catalogo:
            print("Nessun Libro presente in catalogo!")
        else:   
            for isbn, libro in self.catalogo.items():
                print(f"ISBN: {isbn} - Titolo: {libro.titolo} - Autore: {libro.autore}")
    
    def cerca_per_titolo(self, titolo_ricercato): # Restituisce una lista di libri che corrispondono al titolo ricercato
        risultati = []
        for libro in self.catalogo.values():
            if libro.titolo.lower() == titolo_ricercato.lower():
                risultati.append(libro)
        return risultati             
            