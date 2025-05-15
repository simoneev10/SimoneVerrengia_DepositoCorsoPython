class Libro():
    isbn = 0
    def __init__(self, titolo, autore):
        self.titolo = titolo
        self.autore = autore
        
    def descrizione(self):
        print(f"Il libro [{self.isbn}] è {self.titolo} ed è stato scritto da {self.autore}")