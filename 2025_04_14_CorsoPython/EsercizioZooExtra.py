import sqlite3

class DatabaseManager:
    def __init__(self, db_name="zoo.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS animali (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            nome TEXT NOT NULL,
            eta INTEGER NOT NULL
        )
        """)
        self.conn.commit()
    
    def salva_animale(self, tipo, nome, eta):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO animali (tipo, nome, eta) VALUES (?, ?, ?)", 
                      (tipo, nome, eta))
        self.conn.commit()
        return cursor.lastrowid
    
    def carica_animali(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, tipo, nome, eta FROM animali")
        return cursor.fetchall()
    
    def elimina_animale(self, id_animale):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM animali WHERE id = ?", (id_animale,))
        self.conn.commit()
        return cursor.rowcount > 0
    
class Animale:
    db = DatabaseManager()
    
    def __init__(self, nome, eta):
        self.nome = nome
        self.eta = eta
        self.id = None
    
    def salva(self):
        tipo = self.__class__.__name__
        self.id = self.db.salva_animale(tipo, self.nome, self.eta)
        print(f"{tipo} {self.nome} salvato nel database con ID {self.id}")
        
    def fai_suono(self):
        print("Suono generico")

class Leone(Animale):
    def fai_suono(self):
        print(f"{self.nome} ruggisce!")
    
    def caccia(self):
        print(f"Il leone {self.nome} sta cacciando!")

class Giraffa(Animale):
    def fai_suono(self):
        print(f"{self.nome} landiscee!")
        
    def mangia(self):
        print(f"La giraffa {self.nome} mangia le foglie dall'albero!")

class Pinguino(Animale):
    def fai_suono(self):
        print(f"{self.nome} garrisce!")
    
    def scivola(self):
        print(f"Il pinguino {self.nome} scivolaaa!")

def crea_animale():
    print("\nTipi di animali disponibili:")
    print("1. Leone")
    print("2. Giraffa")
    print("3. Pinguino")
    
    scelta = input("Scegli il tipo di animale (1-3): ")
    nome = input("Inserisci il nome dell'animale: ")
    eta = int(input("Inserisci l'età dell'animale: "))
    
    if scelta == "1":
        animale = Leone(nome, eta)
    elif scelta == "2":
        animale = Giraffa(nome, eta)
    elif scelta == "3":
        animale = Pinguino(nome, eta)
    else:
        print("Scelta non valida!")
        return None
    
    animale.salva()
    return animale

def mostra_animali():
    db = DatabaseManager()
    animali = db.carica_animali()
    
    if not animali:
        print("\nNessun animale presente nel database!")
        return
    
    print("\nElenco animali nello zoo:")
    for id_animale, tipo, nome, eta in animali:
        print(f"ID: {id_animale} - {tipo}: {nome}, {eta} anni")

def elimina_animale():
    mostra_animali()
    id_animale = input("\nInserisci l'ID dell'animale da eliminare (0 per annullare): ")
    
    if id_animale == "0":
        return
    
    db = DatabaseManager()
    if db.elimina_animale(int(id_animale)):
        print("Animale eliminato con successo!")
    else:
        print("Nessun animale trovato con questo ID")

def interagisci_animale():
    mostra_animali()
    id_animale = input("\nInserisci l'ID dell'animale con cui interagire (0 per annullare): ")
    
    if id_animale == "0":
        return
    
    db = DatabaseManager()
    animali = db.carica_animali()
    animale_selezionato = None
    
    for id_a, tipo, nome, eta in animali:
        if str(id_a) == id_animale:
            if tipo == "Leone":
                animale_selezionato = Leone(nome, eta)
            elif tipo == "Giraffa":
                animale_selezionato = Giraffa(nome, eta)
            elif tipo == "Pinguino":
                animale_selezionato = Pinguino(nome, eta)
            animale_selezionato.id = id_a
            break
    
    if not animale_selezionato:
        print("Animale non trovato!")
        return
    
    print(f"\nInteragisci con {animale_selezionato.nome} ({animale_selezionato.__class__.__name__}):")
    
    if isinstance(animale_selezionato, Leone):
        print("1. Fai ruggire")
        print("2. Fai cacciare")
    elif isinstance(animale_selezionato, Giraffa):
        print("1. Fai landire")
        print("2. Fai mangiare")
    elif isinstance(animale_selezionato, Pinguino):
        print("1. Fai garrire")
        print("2. Fai scivolare")
    
    azione = input("Scegli un'azione (1-2): ")
    
    if azione == "1":
        animale_selezionato.fai_suono()
    elif azione == "2":
        if isinstance(animale_selezionato, Leone):
            animale_selezionato.caccia()
        elif isinstance(animale_selezionato, Giraffa):
            animale_selezionato.mangia()
        elif isinstance(animale_selezionato, Pinguino):
            animale_selezionato.scivola()
    else:
        print("Azione non valida!")

def menu_principale():
    while True:
        print("\n=== MENU GESTIONE ZOO ===")
        print("1. Aggiungi un nuovo animale")
        print("2. Mostra tutti gli animali")
        print("3. Elimina un animale")
        print("4. Interagisci con un animale")
        print("5. Esci")
        
        scelta = input("Scegli un'opzione (1-5): ")
        
        if scelta == "1":
            crea_animale()
        elif scelta == "2":
            mostra_animali()
        elif scelta == "3":
            elimina_animale()
        elif scelta == "4":
            interagisci_animale()
        elif scelta == "5":
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida. Riprova.")

if __name__ == "__main__":
    menu_principale()