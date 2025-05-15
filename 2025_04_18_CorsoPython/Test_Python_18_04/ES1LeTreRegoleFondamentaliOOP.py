# #ES 1: Le tre regole fondamentali dell’OOP

# Implementa in Python un piccolo sistema di gestione di veicoli che dimostri incapsulamento, ereditarietà e polimorfismo.

#  Obiettivi: 
#  Definire una classe base Veicolo con attributi protetti(Marca[Str], Anno di immatricolazione[Int], Targa [Str] e Revisione[Bool]  ) e metodi getter/setter. 
#  Creare tre sottoclassi (Auto, Moto, Camion) che ereditano da Veicolo e sovrascrivono un metodo comune (descrivi())che riporti tutti i dati dell'oggetto reale, ogni classe figlia deve avere un attributo unico . 
#  Nel menu, permettere all’utente di creare istanze diverse specifiche dei veicoli e previo controllo di tutti gli inserimenti chiamare descrivi() in un metodo polimorfico polimorfo. 

class Veicolo: # Creazione classe veicolo con attributi protetti
    def __init__(self, marca, anno_immatricolazione, targa):
        self._marca = marca
        self._anno_immatricolazione = anno_immatricolazione
        self._targa = targa
        self._revisione = False # la imposto inizialmente a False

    # Getter e Setter
    def get_marca(self):
        return self._marca

    def set_marca(self, marca):
        self._marca = marca

    def get_anno_immatricolazione(self):
        return self._anno_immatricolazione

    def set_anno_immatricolazione(self, anno):
        self._anno_immatricolazione = anno

    def get_targa(self):
        return self._targa

    def set_targa(self, targa):
        self._targa = targa

    def is_revisionato(self):
        return self._revisione

    def set_revisione(self, stato):
        self._revisione = stato

    def descrivi(self):
        return f"Marca: {self._marca}\nAnno: {self._anno_immatricolazione}\nTarga: {self._targa}\nRevisione: {'Sì' if self._revisione else 'No'}"

class Auto(Veicolo):
    def __init__(self, marca, anno_immatricolazione, targa, modello):
        super().__init__(marca, anno_immatricolazione, targa)
        self.modello = modello
        
    def descrivi(self):
        return f"\nMarca: {self._marca}\nModello: {self.modello}\nAnno: {self._anno_immatricolazione}\nTarga: {self._targa}\nRevisione: {'Sì' if self._revisione else 'No'}"

class Moto(Veicolo):
    def __init__(self, marca, anno, targa, carena):
        super().__init__(marca, anno, targa)
        self.carena = carena

    def descrivi(self):
        return f"\nMarca: {self._marca}\nCarena: {self.carena}\nAnno: {self._anno_immatricolazione}\nTarga: {self._targa}\nRevisione: {'Sì' if self._revisione else 'No'}"

class Camion(Veicolo):
    def __init__(self, marca, anno, targa, capacita_carico):
        super().__init__(marca, anno, targa)
        self.capacita_carico = capacita_carico  # in tonnellate

    def descrivi(self):
        return f"\nMarca: {self._marca}\nCapacita di carico: {self.capacita_carico}\nAnno: {self._anno_immatricolazione}\nTarga: {self._targa}\nRevisione: {'Sì' if self._revisione else 'No'}"

def crea_veicolo():
    print("Scegli il tipo di veicolo:\n1) Auto\n2) Moto\n3) Camion")
    scelta = input("Inserisci numero: ")
    
    marca = input("Marca: ")
    anno = int(input("Anno immatricolazione: "))
    targa = input("Targa: ")
    revisione = input("Revisione effettuata? (s/n): ").lower() == "s"

    if scelta == "1":
        modello = input("Modello: ")
        veicolo = Auto(marca, anno, targa, modello)
    elif scelta == "2":
        carena = input("Tipo carena: ")
        veicolo = Moto(marca, anno, targa, carena)
    elif scelta == "3":
        carico = float(input("Capacità carico (tonnellate): "))
        veicolo = Camion(marca, anno, targa, carico)
    else:
        print("Scelta non valida.")
        return None

    veicolo.set_revisione(revisione)
    return veicolo

def main():
    lista_veicoli = []

    while True:
        print("\n1) Aggiungi veicolo\n2) Mostra veicoli\n3) Esci")
        scelta = input("Scelta: ")
        
        if scelta == "1":
            veicolo = crea_veicolo()
            if veicolo:
                lista_veicoli.append(veicolo)
        elif scelta == "2":
            for v in lista_veicoli:
                print(v.descrivi())
        elif scelta == "3":
            print("Uscita...")
            break
        else:
            print("Scelta non valida.")

if __name__ == "__main__":
    main()


