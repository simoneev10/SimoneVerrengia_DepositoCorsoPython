# Costruisci un sistema per gestire forme geometriche usando classi astratte

# Obiettivi:
#  Definire una classe astratta Forma con metodi astratti area() e perimetro(). 
#  Creare classi concrete (Cerchio, Rettangolo, Triangolo) che implementino i metodi. 
#  Fornire un menu per scegliere il tipo di forma, richiedere i parametri e stampare area/perimetro.
# Salva almeno 4 forme geometriche in lista di oggetti. 
# Creare un metodo poliformico che si occupi di paragonare la lista di forme geometriche e rispondere quale ha l'area maggiore e/o il perimetro.
from abc import ABC, abstractmethod
import math

class Forma(ABC): # Creo classe astratta forma come da punto 1
    @abstractmethod
    def area(self): # Non definisco i metodi poichè verranno ereditati e definiti lì
        pass
    
    @abstractmethod
    def perimetro(self):
        pass
    
    @abstractmethod
    def descrivi(self):
        pass
    
class Cerchio(Forma): # Cerchio che eredita da forma
    def __init__(self, raggio):
        self.raggio = raggio
    
    def area(self): # Metodo per l'area
        areaCerchio = math.pi * self.raggio ** 2
        return areaCerchio
    
    def perimetro(self): # Metodo per perimetro
        perimetroCerchio = math.pi * self.raggio * 2
        return perimetroCerchio
    
    def descrivi(self): # Metodo per stampare
        return f"Cerchio: [Raggio: {self.raggio}, Area: {self.area():.2f}, Perimetro: {self.perimetro():.2f}]"
   
class Rettangolo(Forma): # Rettangolo che eredita da forma
    def __init__(self, base, altezza):
        self.base = base
        self.altezza = altezza
        
    def area(self): # Metodo per l'area
        areaRettangolo = self.base * self.altezza
        return areaRettangolo
    
    def perimetro(self): # Metodo per perimetro
        perimetroRettangolo = (self.base * self.altezza)/2
        return perimetroRettangolo
    
    def descrivi(self): # Metodo per stampare
        return f"Rettangolo: [Base: {self.base}, Altezza: {self.altezza}, Area: {self.area():.2f}, Perimetro: {self.perimetro():.2f}]"
    
class Triangolo(Forma): # Triangolo che eredita da forma
    def __init__(self, lato1, lato2, lato3):
        self.lato1 = lato1
        self.lato2 = lato2
        self.lato3 = lato3
        
    def area(self): # Metodo per l'area
        # Utilizzo la Formula di Erone e non la classica ((bxh)/2) poiché ho solamente i 3 lati
        semiPerimetro = self.perimetro() / 2
        return math.sqrt(semiPerimetro * (semiPerimetro - self.lato1) * (semiPerimetro - self.lato2) * (semiPerimetro - self.lato3))

    def perimetro(self): # Metodo per perimetro
        perimetro = self.lato1 + self.lato2 + self.lato3
        return perimetro
    
    def descrivi(self): # Metodo per stampare
        return f"Triangolo: [Lati: {self.lato1}, {self.lato2}, {self.lato3}, Area: {self.area():.2f}, Perimetro: {self.perimetro():.2f}]"
    
def crea_forma(): # Metodo per scegliere quale tipo di figura istanziare
    print("Scegli una forma:\n1) Cerchio\n2) Rettangolo\n3) Triangolo")
    scelta = input("Scelta: ")

    try: # Utilizzo questo costrutto per convalidare la scelta
        if scelta == "1": # In base alla scelta ogni figura ha bisogno di dati diversi e quindi vengono chiesti all'utente
            raggio = float(input("Inserisci raggio: "))
            return Cerchio(raggio)
        elif scelta == "2":
            base = float(input("Inserisci base: "))
            altezza = float(input("Inserisci altezza: "))
            return Rettangolo(base, altezza)
        elif scelta == "3":
            lato1 = float(input("Lato 1: "))
            lato2 = float(input("Lato 2: "))
            lato3 = float(input("Lato 3: "))
            if lato1 + lato2 > lato3 and lato1 + lato3 > lato2 and lato2 + lato3 > lato1:
                return Triangolo(lato1, lato2, lato3)
            else:
                print("Triangolo non valido.")
                return None
        else:
            print("Scelta non valida.")
            return None
    except ValueError:
        print("Inserimento non valido.")
        return None

def confronta_forme(forme): # Metodo per confrontare area e perimetro come da traccia
    if not forme: # Controllo se ci sono forme
        print("Nessuna forma da confrontare.")
        return

    # Inizializzo la forma con area e perimetro massimi
    forma_max_area = forme[0]
    forma_max_perimetro = forme[0]

    for forma in forme[1:]: # Scorro tutte le forme presenti e confronto aree e perimetri
        if forma.area() > forma_max_area.area():
            forma_max_area = forma
        if forma.perimetro() > forma_max_perimetro.perimetro():
            forma_max_perimetro = forma

    print("\nForma con AREA maggiore:")
    print(forma_max_area.descrivi())

    print("\nForma con PERIMETRO maggiore:")
    print(forma_max_perimetro.descrivi())


def main():
    forme = []

    while True: # Menu per selezionare cosa fare
        print("\nMENU:")
        print("1) Crea una nuova forma")
        print("2) Mostra tutte le forme")
        print("3) Confronta forme (area e perimetro)")
        print("4) Esci")
        scelta = input("Scelta: ")

        if scelta == "1":
            forma = crea_forma()
            if forma:
                forme.append(forma)
                print("Forma aggiunta con successo.")
        elif scelta == "2":
            if forme:
                print("\nElenco forme")
                for f in forme:
                    print(f.descrivi())
            else:
                print("Nessuna forma salvata.")
        elif scelta == "3":
            if len(forme) >= 2:
                confronta_forme(forme)
            else:
                print("Inserisci almeno 2 forme per confrontarle.")
        elif scelta == "4":
            print("Chiusura programma...")
            break
        else:
            print("Scelta non valida.")

if __name__ == "__main__":
    main()


