from random import randint
import sqlite3

class DatabaseManager:
    def __init__(self, db_name="partita.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS squadra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            citta TEXT NOT NULL,
            anno_fondazione INTEGER
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS membrosquadra (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            nome TEXT NOT NULL,
            eta INTEGER NOT NULL,
            id_squadra INTEGER,
            FOREIGN KEY (id_squadra) REFERENCES squadra(id) ON DELETE SET NULL
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS giocatore (
            id_membro INTEGER PRIMARY KEY,
            numero INTEGER NOT NULL,
            overall INTEGER NOT NULL CHECK(overall BETWEEN 1 AND 99),
            FOREIGN KEY (id_membro) REFERENCES membrosquadra(id) ON DELETE CASCADE
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS allenatore (
            id_membro INTEGER PRIMARY KEY,
            atteggiamento INTEGER NOT NULL CHECK(atteggiamento BETWEEN 1 AND 3),
            FOREIGN KEY (id_membro) REFERENCES membrosquadra(id) ON DELETE CASCADE
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS assistente (
            id_membro INTEGER PRIMARY KEY,
            ruolo INTEGER NOT NULL CHECK(ruolo BETWEEN 1 AND 3),
            FOREIGN KEY (id_membro) REFERENCES membrosquadra(id) ON DELETE CASCADE
        );
        """)

        self.conn.commit()

    
    def crea_squadra(self, nome, citta, anno_fondazione):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO squadra (nome, citta, anno_fondazione) VALUES (?, ?, ?)", 
                      (nome, citta, anno_fondazione))
        self.conn.commit()
        return cursor.lastrowid    
    
    def salva_membro(self, tipo, nome, eta, id_squadra=None):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO membrosquadra (tipo, nome, eta, id_squadra) VALUES (?, ?, ?, ?)", 
                      (tipo, nome, eta, id_squadra))
        self.conn.commit()
        return cursor.lastrowid
    
    def salva_giocatore(self, id_membro, numero, overall):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO giocatore (id_membro, numero, overall) VALUES (?, ?, ?)",
                      (id_membro, numero, overall))
        self.conn.commit()
    
    def salva_allenatore(self, id_membro, atteggiamento):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO allenatore (id_membro, atteggiamento) VALUES (?, ?)",
                      (id_membro, atteggiamento))
        self.conn.commit()
    
    def salva_assistente(self, id_membro, ruolo):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO assistente (id_membro, ruolo) VALUES (?, ?)",
                      (id_membro, ruolo))
        self.conn.commit()
    
    def get_squadre(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, nome FROM squadra")
        return cursor.fetchall()
    
    def get_giocatori_squadra(self, id_squadra):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT g.numero, g.overall 
                          FROM giocatore g
                          JOIN membrosquadra m ON g.id_membro = m.id
                          WHERE m.id_squadra = ?""", (id_squadra,))
        return cursor.fetchall()
    
    def get_allenatore_squadra(self, id_squadra):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT a.atteggiamento 
                          FROM allenatore a
                          JOIN membrosquadra m ON a.id_membro = m.id
                          WHERE m.id_squadra = ?""", (id_squadra,))
        return cursor.fetchone()
    
    def get_assistente_squadra(self, id_squadra):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT a.ruolo 
                          FROM assistente a
                          JOIN membrosquadra m ON a.id_membro = m.id
                          WHERE m.id_squadra = ?""", (id_squadra,))
        return cursor.fetchone()

class Squadra:
    def __init__(self, nome, citta, anno_fondazione):
        self.nome = nome
        self.citta = citta
        self.anno_fondazione = anno_fondazione
        self.id = None

class MembroSquadra:
    def __init__(self, nome, eta):
        self.nome = nome
        self.eta = eta
        self.id = None
        
    def descrivi(self):
        print(f"{self.nome} di eta {self.eta}")

class Giocatore(MembroSquadra):
    def __init__(self, nome, eta, numero, overall):
        super().__init__(nome, eta)
        self.numero = numero
        self.overall = overall

class Allenatore(MembroSquadra):
    def __init__(self, nome, eta, atteggiamento):
        super().__init__(nome, eta)
        self.atteggiamento = atteggiamento

class Assistente(MembroSquadra):
    def __init__(self, nome, eta, ruolo):
        super().__init__(nome, eta)
        self.ruolo = ruolo

def aggiungi_squadra(db):
    nome = input("Inserisci nome squadra: ")
    citta = input("Inserisci nome citta: ")
    anno_fond = int(input("Inserisci anno fondazione: "))
    id_squadra = db.crea_squadra(nome, citta, anno_fond)
    
    print("Aggiungi 5 giocatori:")
    for i in range(5):
        print(f"\nGiocatore {i+1}:")
        nome = input("Nome: ")
        eta = int(input("Età: "))
        numero = int(input("Numero: "))
        overall = int(input("Overall (70-94): "))
        
        id_membro = db.salva_membro("giocatore", nome, eta, id_squadra)
        db.salva_giocatore(id_membro, numero, overall)
    
    print("\nAggiungi allenatore:")
    nome = input("Nome: ")
    eta = int(input("Età: "))
    atteggiamento = int(input("Atteggiamento (1-3): "))
    id_membro = db.salva_membro("allenatore", nome, eta, id_squadra)
    db.salva_allenatore(id_membro, atteggiamento)
    
    print("\nAggiungi assistente:")
    nome = input("Nome: ")
    eta = int(input("Età: "))
    ruolo = int(input("Ruolo (1-3): "))
    id_membro = db.salva_membro("assistente", nome, eta, id_squadra)
    db.salva_assistente(id_membro, ruolo)
    
    # INSERISCI QUESTO BLOCCO NEL FILE principale dopo l'inizializzazione del database

    # ==========================
    # Squadra 1: AC Milan
    # ==========================
    id_milan = db.crea_squadra("AC Milan", "Milano", 1899)

    giocatori_milan = [
        ("Mike Maignan", 28, 16, 88),
        ("Fikayo Tomori", 26, 23, 83),
        ("Theo Hernández", 26, 19, 85),
        ("Ismaël Bennacer", 26, 4, 82),
        ("Rafael Leão", 24, 10, 86)
    ]

    for nome, eta, numero, overall in giocatori_milan:
        id_membro = db.salva_membro("giocatore", nome, eta, id_milan)
        db.salva_giocatore(id_membro, numero, overall)

    # Allenatore AC Milan
    id_membro = db.salva_membro("allenatore", "Stefano Pioli", 58, id_milan)
    db.salva_allenatore(id_membro, atteggiamento=2)  # 1=off, 2=eq, 3=def

    # Assistente AC Milan
    id_membro = db.salva_membro("assistente", "Daniele Bonera", 42, id_milan)
    db.salva_assistente(id_membro, ruolo=1)

    # ==========================
    # Squadra 2: Juventus
    # ==========================
    id_juve = db.crea_squadra("Juventus", "Torino", 1897)

    giocatori_juve = [
        ("Wojciech Szczęsny", 33, 1, 86),
        ("Gleison Bremer", 27, 3, 84),
        ("Federico Chiesa", 26, 7, 85),
        ("Adrien Rabiot", 29, 25, 83),
        ("Dusan Vlahović", 24, 9, 84)
    ]

    for nome, eta, numero, overall in giocatori_juve:
        id_membro = db.salva_membro("giocatore", nome, eta, id_juve)
        db.salva_giocatore(id_membro, numero, overall)

    # Allenatore Juventus
    id_membro = db.salva_membro("allenatore", "Massimiliano Allegri", 56, id_juve)
    db.salva_allenatore(id_membro, atteggiamento=3)

    # Assistente Juventus
    id_membro = db.salva_membro("assistente", "Marco Landucci", 59, id_juve)
    db.salva_assistente(id_membro, ruolo=2)

def simula_partita(db):
    squadre = db.get_squadre()
    if len(squadre) < 2:
        print("Creare almeno 2 squadre prima di simulare una partita!")
        return
    
    print("\nSquadre disponibili:")
    for id_squadra, nome in squadre:
        print(f"ID: {id_squadra} - {nome}")
    
    squadraUno = int(input("\nInserisci id squadra 1: "))
    squadraDue = int(input("Inserisci id squadra 2: "))
    
    # Calcola forza squadra 1
    giocatori1 = db.get_giocatori_squadra(squadraUno)
    overall1 = sum(g[1] for g in giocatori1)
    allenatore1 = db.get_allenatore_squadra(squadraUno)
    bonus_allenatore1 = 5 if allenatore1[0] == 1 else 10 if allenatore1[0] == 2 else 0
    assistente1 = db.get_assistente_squadra(squadraUno)
    bonus_assistente1 = 5 if assistente1[0] == 1 else 10 if assistente1[0] == 2 else 0
    forza1 = overall1 + bonus_allenatore1 + bonus_assistente1
    
    # Calcola forza squadra 2
    giocatori2 = db.get_giocatori_squadra(squadraDue)
    overall2 = sum(g[1] for g in giocatori2)
    allenatore2 = db.get_allenatore_squadra(squadraDue)
    bonus_allenatore2 = 5 if allenatore2[0] == 1 else 10 if allenatore2[0] == 2 else 0
    assistente2 = db.get_assistente_squadra(squadraDue)
    bonus_assistente2 = 5 if assistente2[0] == 1 else 10 if assistente2[0] == 2 else 0
    forza2 = overall2 + bonus_allenatore2 + bonus_assistente2
    
    # Simula risultato
    differenza = abs(forza1 - forza2)
    gol1 = randint(0, 5) if differenza < 100 else randint(0, 3) if forza1 > forza2 else randint(0, 1)
    gol2 = randint(0, 5) if differenza < 100 else randint(0, 3) if forza2 > forza1 else randint(0, 1)
    
    # Aggiusta risultato in base alla forza
    if forza1 > forza2:
        gol1 += differenza // 100
    else:
        gol2 += differenza // 100
    
    # Stampa risultato
    print("\n=== RISULTATO FINALE ===")
    print(f"Squadra 1: {gol1} - Squadra 2: {gol2}")
    if gol1 > gol2:
        print("Squadra 1 vince!")
    elif gol2 > gol1:
        print("Squadra 2 vince!")
    else:
        print("Pareggio!")

def popola_esempio(db):
        # INSERISCI QUESTO BLOCCO NEL FILE principale dopo l'inizializzazione del database

    # ==========================
    # Squadra 1: AC Milan
    # ==========================
    id_milan = db.crea_squadra("AC Milan", "Milano", 1899)

    giocatori_milan = [
        ("Mike Maignan", 28, 16, 88),
        ("Fikayo Tomori", 26, 23, 83),
        ("Theo Hernández", 26, 19, 85),
        ("Ismaël Bennacer", 26, 4, 82),
        ("Rafael Leão", 24, 10, 86)
    ]

    for nome, eta, numero, overall in giocatori_milan:
        id_membro = db.salva_membro("giocatore", nome, eta, id_milan)
        db.salva_giocatore(id_membro, numero, overall)

    # Allenatore AC Milan
    id_membro = db.salva_membro("allenatore", "Stefano Pioli", 58, id_milan)
    db.salva_allenatore(id_membro, atteggiamento=2)  # 1=off, 2=eq, 3=def

    # Assistente AC Milan
    id_membro = db.salva_membro("assistente", "Daniele Bonera", 42, id_milan)
    db.salva_assistente(id_membro, ruolo=1)

    # ==========================
    # Squadra 2: Juventus
    # ==========================
    id_juve = db.crea_squadra("Juventus", "Torino", 1897)

    giocatori_juve = [
        ("Wojciech Szczęsny", 33, 1, 86),
        ("Gleison Bremer", 27, 3, 84),
        ("Federico Chiesa", 26, 7, 85),
        ("Adrien Rabiot", 29, 25, 83),
        ("Dusan Vlahović", 24, 9, 84)
    ]

    for nome, eta, numero, overall in giocatori_juve:
        id_membro = db.salva_membro("giocatore", nome, eta, id_juve)
        db.salva_giocatore(id_membro, numero, overall)

    # Allenatore Juventus
    id_membro = db.salva_membro("allenatore", "Massimiliano Allegri", 56, id_juve)
    db.salva_allenatore(id_membro, atteggiamento=3)

    # Assistente Juventus
    id_membro = db.salva_membro("assistente", "Marco Landucci", 59, id_juve)
    db.salva_assistente(id_membro, ruolo=2)

def main():
    db = DatabaseManager()
    
    while True:
        print("\nBenvenuto allo Stadio Simone Arena! Cosa desideri fare? : ")
        print("1. Aggiungi squadra")
        print("2. Simula partita")
        print("3. Esci")
        print("4. esempio")
        
        scelta = input("Scegli un'opzione (1-3): ")
        
        if scelta == "1":
            aggiungi_squadra(db)
        elif scelta == "2":
            simula_partita(db)
        elif scelta == "3":
            print("Arrivederci!")
            break
        elif scelta == "4":
            popola_esempio(db)
        else:
            print("Scelta non valida. Riprova.")

if __name__ == "__main__":
    main()