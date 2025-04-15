import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="esercito"
    )

def crea_tabelle():
    conn = get_connection()
    c = conn.cursor()

    # Tabella dei tipi di esercito (es: fanteria, cavalleria, ecc.)
    c.execute("""
        CREATE TABLE IF NOT EXISTS tipi_esercito (
            id_tipo INT AUTO_INCREMENT PRIMARY KEY,
            nome_tipo VARCHAR(50) UNIQUE NOT NULL,
            soldati_totali INT DEFAULT 0
        )
    """)

    # Tabella generale delle unità militari
    c.execute("""
        CREATE TABLE IF NOT EXISTS unita_militari (
            id_unita INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            numero_soldati INT NOT NULL,
            id_tipo INT NOT NULL,
            FOREIGN KEY (id_tipo) REFERENCES tipi_esercito(id_tipo)
        )
    """)

    # Fanteria
    c.execute("""
        CREATE TABLE IF NOT EXISTS fanteria (
            id_unita INT PRIMARY KEY,
            posizione_trincea VARCHAR(100),
            FOREIGN KEY (id_unita) REFERENCES unita_militari(id_unita) ON DELETE CASCADE
        )
    """)

    # Cavalleria
    c.execute("""
        CREATE TABLE IF NOT EXISTS cavalleria (
            id_unita INT PRIMARY KEY,
            terreno_target VARCHAR(100),
            FOREIGN KEY (id_unita) REFERENCES unita_militari(id_unita) ON DELETE CASCADE
        )
    """)

    # Artiglieria
    c.execute("""
        CREATE TABLE IF NOT EXISTS artiglieria (
            id_unita INT PRIMARY KEY,
            numero_razzi INT,
            target VARCHAR(100),
            FOREIGN KEY (id_unita) REFERENCES unita_militari(id_unita) ON DELETE CASCADE
        )
    """)

    # Supporto logistico
    c.execute("""
        CREATE TABLE IF NOT EXISTS supporto_logistico (
            id_unita INT PRIMARY KEY,
            risorse VARCHAR(100),
            FOREIGN KEY (id_unita) REFERENCES unita_militari(id_unita) ON DELETE CASCADE
        )
    """)

    # Ricognizione
    c.execute("""
        CREATE TABLE IF NOT EXISTS ricognizione (
            id_unita INT PRIMARY KEY,
            target VARCHAR(100),
            FOREIGN KEY (id_unita) REFERENCES unita_militari(id_unita) ON DELETE CASCADE
        )
    """)

    conn.commit()
    c.close()
    conn.close()

def inserisci_unita(nome, numero_soldati, tipo, dettaglio):
    conn = get_connection()
    c = conn.cursor()

    # 1. Inserisci tipo in tipi_esercito (se non esiste)
    c.execute("INSERT IGNORE INTO tipi_esercito (nome_tipo) VALUES (%s)", (tipo,))
    conn.commit()

    # 2. Ottieni id_tipo
    c.execute("SELECT id_tipo FROM tipi_esercito WHERE nome_tipo = %s", (tipo,))
    id_tipo = c.fetchone()[0]

    # 3. Inserisci in unita_militari
    c.execute("""
        INSERT INTO unita_militari (nome, numero_soldati, id_tipo)
        VALUES (%s, %s, %s)
    """, (nome, numero_soldati, id_tipo))
    conn.commit()

    # 4. Ottieni id_unita appena inserito
    id_unita = c.lastrowid

    # 5. Inserisci nella tabella specifica
    match tipo:
        case "Fanteria":
            c.execute("INSERT INTO fanteria (id_unita, posizione_trincea) VALUES (%s, %s)", (id_unita, dettaglio))
        case "Cavalleria":
            c.execute("INSERT INTO cavalleria (id_unita, terreno_target) VALUES (%s, %s)", (id_unita, dettaglio))
        case "Artiglieria":
            c.execute("INSERT INTO artiglieria (id_unita, numero_razzi, target) VALUES (%s, %s, %s)",
                      (id_unita, dettaglio["numero_razzi"], dettaglio["target"]))
        case "Supporto Logistico":
            c.execute("INSERT INTO supporto_logistico (id_unita, risorse) VALUES (%s, %s)", (id_unita, dettaglio))
        case "Ricognizione":
            c.execute("INSERT INTO ricognizione (id_unita, target) VALUES (%s, %s)", (id_unita, dettaglio))
    
    # 6. Aggiorna il totale dei soldati per tipo
    c.execute("UPDATE tipi_esercito SET soldati_totali = soldati_totali + %s WHERE id_tipo = %s", (numero_soldati, id_tipo))
    conn.commit()

    c.close()
    conn.close()

    return id_unita  # utile per registrazione locale

def riepilogo_soldati():
    conn = get_connection()
    c = conn.cursor()

    # Seleziona i totali dei soldati per ogni tipo di esercito
    c.execute("SELECT nome_tipo, soldati_totali FROM tipi_esercito")
    result = c.fetchall()

    # Output estetico
    print("\n" + "="*40)
    print(f"{'Riepilogo Soldati per Tipo di Esercito':^40}")
    print("="*40)
    print(f"{'Tipo di Esercito':<25}{'Soldati Totali':>15}")
    print("-"*40)

    for nome, soldati in result:
        print(f"{nome:<25}{soldati:>15}")

    print("="*40)
    c.close()
    conn.close()