class UnitaMilitare:
    def __init__(self, nome, numero_soldati):
       self.nome = nome
       self.numero_soldati = numero_soldati
       self.id = 1
    
    def muovi(self, zona_target):
        print(f"L'unità militare {self.nome} è in marcia verso {zona_target}")
        
    def attacca(self, target):
        print(f"Avvio dell'attacco verso {target}")
    
    def ritirata(self, verso_dove):
        print(f"L'unità militare {self.nome} si ritira verso {verso_dove} ")
        
class Fanteria(UnitaMilitare):
    def __init__(self, nome, numero_soldati, posizione_trincea):
        super().__init__(nome, numero_soldati)
        self.posizione_trincea = posizione_trincea
        
    def costruisci_trincea(self):
        print(f"La squadra fanteria {self.nome} costruisce una trincea a {self.posizione_trincea}")
    
    def get_tipo(self):
        return "Fanteria"
        
class Cavalleria(UnitaMilitare):
    def __init__(self, nome, numero_soldati, terreno_target):
        super().__init__(nome, numero_soldati)
        self.terreno_target = terreno_target
        
    def esplora_terreno(self):
        print(f"La squadra cavalleria {self.nome} avvia l'esplorazione verso {self.terreno_target}")

    def get_tipo(self):
        return "Cavalleria"
        
class Artiglieria(UnitaMilitare):
    def __init__(self, nome, numero_soldati, numero_razzi, target):
        super().__init__(nome, numero_soldati)
        self.numero_razzi = numero_razzi
        self.target = target
        
    def calibra_artiglieria(self):
        print(f"La squadra artiglieria {self.nome} impiega {self.numero_soldati} soldati per calibrare {self.numero_razzi} razzi, verso {self.target}")
    
    def get_tipo(self):
        return "Artiglieria"
    
class SupportoLogistico(UnitaMilitare):
    def __init__(self, nome, numero_soldati, risorse):
        super().__init__(nome, numero_soldati)
        self.risorse = risorse
        
    def distribuisci_risorse(self):
        print(f"La squadra supporto logistico {self.nome} distribuisce {self.risorse} alle truppe")
    
    def get_tipo(self):
        return "Supporto Logistico"

class Ricognizione(UnitaMilitare):
    def __init__(self, nome, numero_soldati, target):
        super().__init__(nome, numero_soldati)
        self.target = target
        
    def conduci_ricognizione(self):
        print(f"La squadra ricognizione {self.nome} impiega {self.numero_soldati} soldati per sorvegliare {self.target}")

    def get_tipo(self):
        return "Ricognizione"

class ControlloMilitare(UnitaMilitare):
    unita_registrate = {}
    id_counter = 1  # Contatore per gli ID univoci
    
    def __init__(self, nome="Comando Centrale", numero_soldati=0):
        super().__init__(nome, numero_soldati)
        
    def mostra_unita(self):
        if not self.unita_registrate:
            print("Nessuna unità registrata!")
            return
        
        print("\nELENCO UNITÀ MILITARI")
        for id_unita, unita in self.unita_registrate.items():
            print(f"ID: {id_unita} - Tipo: {unita.get_tipo()} - Nome: {unita.nome} - Soldati: {unita.numero_soldati}")
        
    def registra_unita(self):
        print("\nREGISTRAZIONE NUOVA UNITÀ")
        print("Tipi di unità disponibili:")
        print("1. Fanteria")
        print("2. Cavalleria")
        print("3. Artiglieria")
        print("4. Supporto Logistico")
        print("5. Ricognizione")
        
        tipo_unita = input("Seleziona tipo di unità (1-6): ")
        nome = input("Nome unità: ")
        numero_soldati = int(input("Numero soldati: "))
        
        nuova_unita = None
        

        if tipo_unita == "1":
            posizione_trincea = input("Posizione trincea: ")
            nuova_unita = Fanteria(nome, numero_soldati, posizione_trincea)
        elif tipo_unita == "2":
            terreno_target = input("Terreno target per esplorazione: ")
            nuova_unita = Cavalleria(nome, numero_soldati, terreno_target)
        elif tipo_unita == "3":
            numero_razzi = int(input("Numero razzi: "))
            target = input("Target: ")
            nuova_unita = Artiglieria(nome, numero_soldati, numero_razzi, target)
        elif tipo_unita == "4":
            risorse = input("Risorse da gestire: ")
            nuova_unita = SupportoLogistico(nome, numero_soldati, risorse)
        elif tipo_unita == "5":
            target = input("Target per ricognizione: ")
            nuova_unita = Ricognizione(nome, numero_soldati, target)
        else:
            print("Tipo non valido, creazione unità generica.")
            nuova_unita = UnitaMilitare(nome, numero_soldati)
        
        self.unita_registrate[self.id_counter] = nuova_unita
        print(f"Unità '{nome}' registrata con ID {self.id_counter}")
        self.id_counter += 1
    
    def dettagli_unita(self):
        if not self.unita_registrate:
            print("Nessuna unità registrata!")
            return
            
        self.mostra_unita()
        try:
            id_unita = int(input("\nInserisci ID unità da visualizzare: "))
            unita = self.unita_registrate.get(id_unita)
            
            if unita:
                print("\nSCHEDA UNITÀ")
                print(f"Tipo: {unita.get_tipo()}")
                print(f"Nome: {unita.nome}")
                print(f"Numero soldati: {unita.numero_soldati}")
                print(f"ID registro: {id_unita}")
                
                # Mostra proprietà specifiche in base al tipo di unità
                if isinstance(unita, Fanteria):
                    print(f"Posizione trincea: {unita.posizione_trincea}")
                elif isinstance(unita, Cavalleria):
                    print(f"Terreno target: {unita.terreno_target}")
                elif isinstance(unita, Artiglieria):
                    print(f"Numero razzi: {unita.numero_razzi}")
                    print(f"Target: {unita.target}")
                elif isinstance(unita, SupportoLogistico):
                    print(f"Risorse: {unita.risorse}")
                elif isinstance(unita, Ricognizione):
                    print(f"Target ricognizione: {unita.target}")
            else:
                print("ID unità non valido!")
        except ValueError:
            print("Errore: Inserire un numero valido")

    def operazioni_unita(self):
        if not self.unita_registrate:
            print("Nessuna unità registrata!")
            return
            
        self.mostra_unita()
        try:
            id_unita = int(input("\nInserisci ID unità da comandare: "))
            unita = self.unita_registrate.get(id_unita)
            
            if unita:
                print(f"\nCOMANDO UNITÀ: {unita.nome} ({unita.get_tipo()})")
                print("Operazioni disponibili:")
                print("1. Muovi")
                print("2. Attacca")
                print("3. Ritirata")
                
                # Operazioni specifiche per tipo
                if isinstance(unita, Fanteria):
                    print("4. Costruisci trincea")
                elif isinstance(unita, Cavalleria):
                    print("4. Esplora terreno")
                elif isinstance(unita, Artiglieria):
                    print("4. Calibra artiglieria")
                elif isinstance(unita, SupportoLogistico):
                    print("4. Distribuisci risorse")
                elif isinstance(unita, Ricognizione):
                    print("4. Conduci ricognizione")
                
                scelta = input("Selezione operazione: ")
                
                if scelta == "1":
                    zona = input("Destinazione: ")
                    unita.muovi(zona)
                elif scelta == "2":
                    target = input("Target da attaccare: ")
                    unita.attacca(target)
                elif scelta == "3":
                    verso_dove = input("Destinazione ritirata: ")
                    unita.ritirata(verso_dove)
                elif scelta == "4":
                    if isinstance(unita, Fanteria):
                        unita.costruisci_trincea()
                    elif isinstance(unita, Cavalleria):
                        unita.esplora_terreno()
                    elif isinstance(unita, Artiglieria):
                        unita.calibra_artiglieria()
                    elif isinstance(unita, SupportoLogistico):
                        unita.distribuisci_risorse()
                    elif isinstance(unita, Ricognizione):
                        unita.conduci_ricognizione()
                    else:
                        print("Operazione non disponibile per questo tipo di unità.")
                else:
                    print("Operazione non valida.")
            else:
                print("ID unità non valido!")
        except ValueError:
            print("Errore: Inserire un numero valido")

def menu_controllo_militare():
    sistema = ControlloMilitare()
    
    while True:
        print("\nSISTEMA DI CONTROLLO MILITARE")
        print("1. Registra nuova unità")
        print("2. Mostra tutte le unità")
        print("3. Visualizza dettagli unità")
        print("4. Comanda un'unità")
        print("5. Torna al menu principale")
        
        scelta = input("Selezione: ")
        
        if scelta == "1":
            sistema.registra_unita()
        elif scelta == "2":
            sistema.mostra_unita()
        elif scelta == "3":
            sistema.dettagli_unita()
        elif scelta == "4":
            sistema.operazioni_unita()
        elif scelta == "5":
            print("Uscita dal sistema di controllo...")
            break
        else:
            print("Scelta non valida. Riprovare.")

# Per testare direttamente questo modulo
if __name__ == "__main__":
    menu_controllo_militare()