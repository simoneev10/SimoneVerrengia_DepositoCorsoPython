class Animale: # classe genitore da cui i figli ereditano 
    def __init__(self, nome, eta, verso):
        self.nome = nome
        self.eta = eta
        self.verso = verso
    
    def fai_suono(self):
        print("L'animale fa un suono.")

class Coccodrillo(Animale): # classe figlia di Animale
    def __init__(self, nome, eta, verso):
        super().__init__(nome, eta, verso)
        
    def fai_suono(self): # riscrittura del metodo della classe padre
        print(f"Che verso fa il coccodrillo non si sa: {self.verso}")
        
    def attivita(self):
        print("Il coccodrillo nuota nel lago")
        
class Zebra(Animale):  # classe figlia di Animale
    def __init__(self, nome, eta, verso):
        super().__init__(nome, eta, verso)
        
    def fai_suono(self):  # riscrittura del metodo della classe padre
        print(f"La zebra nitrisce:{self.verso}")
        
    def attivita(self):
        print("La zebra sta scappando da una iena")

class Iena(Animale):  # classe figlia di Animale
    def __init__(self, nome, eta, verso):
        super().__init__(nome, eta, verso)
        
    def fai_suono(self):  # riscrittura del metodo della classe padre
        print(f"La iena ringhia: {self.verso}")
        
    def attivita(self):
        print("La iena sta cacciando la zebra")

# creazione oggetti 
cocco = Coccodrillo("Croccone", 10, "TATATATATTAAA")
zebra = Zebra("Giuvents", 12, "HIIHIII")
iena = Iena("Clementino", 5, "GRRRROO")

animali = [cocco, zebra, iena]

for animale in animali:
    print(f"--- {animale.nome} ---")
    animale.fai_suono()
    animale.attivita()
    print()
