class Punto:
    def __init__(self):
        self.x = 0
        self.y = 0

    def muovi(self): # Definisco funzione per muovermi
        muoviX = int(input("Inserisci di quanto ti vuoi muovere per x: "))
        muoviY = int(input("Inserisci di quanto ti vuoi muovere per y: "))
        self.x += muoviX
        self.y += muoviY

    def distanza_da_origine(self): # Definisco la funzione per stampare
        print(f"La distanza dall'origine è:\nx = {self.x}, y = {self.y}")
        
# Creo oggetto Punto1
Punto1 = Punto()
Punto1.muovi()
Punto1.distanza_da_origine()