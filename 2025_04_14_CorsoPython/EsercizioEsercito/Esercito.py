import unitaMilitareDB

# Classe base per un'unità militare
class UnitaMilitare:
    def __init__(self, nome, numero_soldati):
        self.nome = nome
        self.numero_soldati = numero_soldati
    
    # Metodo per muovere l'unità verso una zona target
    def muovi(self, zona_target):
        print(f"\n🔻 L'unità militare '{self.nome}' sta marciando verso {zona_target}.")
    
    # Metodo per eseguire un attacco
    def attacca(self, target):
        print(f"\n💥 Avvio dell'attacco verso {target} da parte dell'unità '{self.nome}'.")
    
    # Metodo per ordinare una ritirata
    def ritirata(self, verso_dove):
        print(f"\n🚶‍♂️ L'unità militare '{self.nome}' si ritira verso {verso_dove}.")
    

# Classe per la Fanteria, una sottoclasse di UnitaMilitare
class Fanteria(UnitaMilitare):
    def __init__(self, nome, numero_soldati, posizione_trincea):
        super().__init__(nome, numero_soldati)
        self.posizione_trincea = posizione_trincea

    # Metodo per costruire una trincea
    def costruisci_trincea(self):
        print(f"\n🔨 La squadra Fanteria '{self.nome}' costruisce una trincea a {self.posizione_trincea}.")
    
    # Metodo per ottenere il tipo di unità
    def get_tipo(self):
        return "Fanteria"

# Classe per la Cavalleria, una sottoclasse di UnitaMilitare
class Cavalleria(UnitaMilitare):
    def __init__(self, nome, numero_soldati, terreno_target):
        super().__init__(nome, numero_soldati)
        self.terreno_target = terreno_target

    # Metodo per esplorare il terreno
    def esplora_terreno(self):
        print(f"\n🐎 La squadra Cavalleria '{self.nome}' avvia l'esplorazione verso {self.terreno_target}.")
    
    # Metodo per ottenere il tipo di unità
    def get_tipo(self):
        return "Cavalleria"

# Classe per l'Artiglieria, una sottoclasse di UnitaMilitare
class Artiglieria(UnitaMilitare):
    def __init__(self, nome, numero_soldati, numero_razzi, target):
        super().__init__(nome, numero_soldati)
        self.numero_razzi = numero_razzi
        self.target = target

    # Metodo per calibrare l'artiglieria
    def calibra_artiglieria(self):
        print(f"\n🎯 La squadra Artiglieria '{self.nome}' calibra {self.numero_razzi} razzi verso {self.target}.")
    
    # Metodo per ottenere il tipo di unità
    def get_tipo(self):
        return "Artiglieria"

# Classe per il Supporto Logistico, una sottoclasse di UnitaMilitare
class SupportoLogistico(UnitaMilitare):
    def __init__(self, nome, numero_soldati, risorse):
        super().__init__(nome, numero_soldati)
        self.risorse = risorse

    # Metodo per distribuire risorse
    def distribuisci_risorse(self):
        print(f"\n🚚 La squadra Supporto Logistico '{self.nome}' distribuisce {self.risorse} alle truppe.")
    
    # Metodo per ottenere il tipo di unità
    def get_tipo(self):
        return "Supporto Logistico"

# Classe per la Ricognizione, una sottoclasse di UnitaMilitare
class Ricognizione(UnitaMilitare):
    def __init__(self, nome, numero_soldati, target):
        super().__init__(nome, numero_soldati)
        self.target = target

    # Metodo per condurre la ricognizione
    def conduci_ricognizione(self):
        print(f"\n🕵️‍♂️ La squadra Ricognizione '{self.nome}' sta sorvegliando {self.target}.")
    
    # Metodo per ottenere il tipo di unità
    def get_tipo(self):
        return "Ricognizione"

# Classe per gestire il controllo delle unità militari
class ControlloMilitare(UnitaMilitare):
    unita_registrate = {}  # Dizionario per tenere traccia delle unità
    id_counter = 1  # Contatore per assegnare ID univoci alle unità

    def __init__(self, nome="Comando Centrale", numero_soldati=0):
        super().__init__(nome, numero_soldati)

    # Metodo per mostrare tutte le unità registrate
    def mostra_unita(self):
        if not self.unita_registrate:
            print("\n⚠️ Nessuna unità registrata!")
            return
        print("\n📋 ELENCO UNITÀ:")
        for id_unita, unita in self.unita_registrate.items():
            print(f"ID: {id_unita} - Tipo: {unita.get_tipo()} - Nome: {unita.nome} - Soldati: {unita.numero_soldati}")

    # Metodo per registrare una nuova unità
    def registra_unita(self):
        print("\n📌 REGISTRAZIONE NUOVA UNITÀ")
        print("1. Fanteria\n2. Cavalleria\n3. Artiglieria\n4. Supporto Logistico\n5. Ricognizione")
        tipo_unita = input("Tipo (1-5): ")
        nome = input("Nome unità: ")
        numero_soldati = int(input("Numero soldati: "))

        nuova_unita = None
        dettaglio = None

        # Gestione della scelta del tipo di unità
        match tipo_unita:
            case "1":
                posizione_trincea = input("Posizione trincea: ")
                nuova_unita = Fanteria(nome, numero_soldati, posizione_trincea)
                dettaglio = posizione_trincea
            case "2":
                terreno_target = input("Terreno da esplorare: ")
                nuova_unita = Cavalleria(nome, numero_soldati, terreno_target)
                dettaglio = terreno_target
            case "3":
                numero_razzi = int(input("Numero razzi: "))
                target = input("Target artiglieria: ")
                nuova_unita = Artiglieria(nome, numero_soldati, numero_razzi, target)
                dettaglio = {"numero_razzi": numero_razzi, "target": target}
            case "4":
                risorse = input("Tipo di risorse: ")
                nuova_unita = SupportoLogistico(nome, numero_soldati, risorse)
                dettaglio = risorse
            case "5":
                target = input("Target ricognizione: ")
                nuova_unita = Ricognizione(nome, numero_soldati, target)
                dettaglio = target
            case _:
                print("\n❌ Tipo non valido.")
                return

        # Aggiungi l'unità nel database e nell'elenco
        tipo = nuova_unita.get_tipo()
        id_unita_db = unitaMilitareDB.inserisci_unita(nome, numero_soldati, tipo, dettaglio)

        # Salva l'unità nell'elenco delle unità registrate
        self.unita_registrate[self.id_counter] = nuova_unita
        print(f"\n✅ Unità '{nome}' registrata con ID {self.id_counter} (ID DB: {id_unita_db})")
        self.id_counter += 1

    # Metodo per eseguire operazioni su una specifica unità
    def operazioni_unita(self):
        if not self.unita_registrate:
            print("\n⚠️ Nessuna unità registrata!")
            return

        self.mostra_unita()
        try:
            id_unita = int(input("\nID dell'unità da comandare: "))
            unita = self.unita_registrate.get(id_unita)

            if not unita:
                print("\n❌ ID non valido.")
                return

            print(f"\n⚔️ Comando unità: {unita.nome} ({unita.get_tipo()})")
            print("1. Muovi\n2. Attacca\n3. Ritirata\n4. Azione speciale")

            scelta = input("Scelta: ")

            # Esegui l'operazione scelta
            match scelta:
                case "1":
                    zona = input("Destinazione: ")
                    unita.muovi(zona)
                case "2":
                    target = input("Target: ")
                    unita.attacca(target)
                case "3":
                    direzione = input("Verso dove? ")
                    unita.ritirata(direzione)
                case "4":
                    match unita:
                        case Fanteria():
                            unita.costruisci_trincea()
                        case Cavalleria():
                            unita.esplora_terreno()
                        case Artiglieria():
                            unita.calibra_artiglieria()
                        case SupportoLogistico():
                            unita.distribuisci_risorse()
                        case Ricognizione():
                            unita.conduci_ricognizione()
                        case _:
                            print("\n❌ Operazione non disponibile.")
                case _:
                    print("\n❌ Scelta non valida.")
        except ValueError:
            print("\n⚠️ Errore: inserire un numero valido.")

# Funzione principale per interagire con il sistema di controllo
def menu_controllo_militare():
    unitaMilitareDB.crea_tabelle()
    sistema = ControlloMilitare()

    while True:
        print("\n📡 SISTEMA DI CONTROLLO MILITARE")
        print("1. Registra nuova unità")
        print("2. Mostra tutte le unità")
        print("3. Comanda un'unità")
        print("4. Riepilogo Soldati per Tipo di Esercito")
        print("5. Esci")

        scelta = input("Scelta: ")

        match scelta:
            case "1":
                sistema.registra_unita()
            case "2":
                sistema.mostra_unita()
            case "3":
                sistema.operazioni_unita()
            case "4":
                unitaMilitareDB.riepilogo_soldati()
            case "5":
                print("\n💼 Chiusura sistema...")
                break
            case _:
                print("\n❌ Scelta non valida.")

if __name__ == "__main__":
    menu_controllo_militare()

