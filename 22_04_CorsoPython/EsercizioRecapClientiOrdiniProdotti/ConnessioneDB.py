import mysql.connector
import numpy as np
import random
import string

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="negozio"
        )
        return conn
    except mysql.connector.Error as err:
        print("Errore di connessione al database:", err)
        return None

def crea_database(nome_db):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {nome_db}")
        print(f"Database '{nome_db}' verificato/creato.")
    except mysql.connector.Error as err:
        print("Errore durante la creazione del database:", err)
    finally:
        conn.close()

def crea_tabelle():
    conn = get_connection()
    if conn is None:
        return
    try:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ordini (
                ordini_id INT AUTO_INCREMENT PRIMARY KEY
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cliente (
                cliente_id INT PRIMARY KEY,
                ordini_id INT,
                name VARCHAR(50),
                cf VARCHAR(16),
                FOREIGN KEY (ordini_id) REFERENCES ordini(ordini_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prodotto (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50),
                barcode BIGINT,
                prezzo FLOAT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ordine_prodotto (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ordini_id INT,
                prodotto_id INT,
                FOREIGN KEY (ordini_id) REFERENCES ordini(ordini_id),
                FOREIGN KEY (prodotto_id) REFERENCES prodotto(id)
            )
        ''')

        conn.commit()
        print("Tabelle aggiornate con successo.")
    except mysql.connector.Error as err:
        print("Errore durante la creazione delle tabelle:", err)
    finally:
        conn.close()

def genera_cf():
    lettere = ''.join(random.choices(string.ascii_uppercase, k=6))
    numeri = ''.join(random.choices(string.digits, k=10))
    return lettere + numeri

def inserisci_cliente(cliente_id, ordini_id, nome):
    cf = genera_cf()
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cliente (cliente_id, ordini_id, name, cf) VALUES (%s, %s, %s, %s)",
                       (cliente_id, ordini_id, nome, cf))
        conn.commit()
    except mysql.connector.Error as err:
        print("Errore inserimento cliente:", err)
    finally:
        conn.close()

def crea_ordine_e_restituisci_id():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ordini () VALUES ()")
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as err:
        print("Errore creazione ordine:", err)
        return None
    finally:
        conn.close()

def inserisci_ordine(ordini_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ordini (ordini_id) VALUES (%s)", (ordini_id,))
        conn.commit()
    except mysql.connector.Error as err:
        print("Errore inserimento ordine:", err)
    finally:
        conn.close()

def inserisci_prodotto(nome, prezzo):
    cifre = np.random.randint(0, 10, 12)
    barcode = int("".join(map(str, cifre)))
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO prodotto (name, barcode, prezzo) VALUES (%s, %s, %s)", (nome, barcode, prezzo))
        conn.commit()
    except mysql.connector.Error as err:
        print("Errore inserimento prodotto:", err)
    finally:
        conn.close()

def inserisci_prodotto_in_ordine(ordini_id, prodotto_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ordine_prodotto (ordini_id, prodotto_id) VALUES (%s, %s)", (ordini_id, prodotto_id))
        conn.commit()
    except mysql.connector.Error as err:
        print("Errore associazione ordine-prodotto:", err)
    finally:
        conn.close()

def leggi_clienti():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cliente")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print("Errore lettura clienti:", err)
        return []
    finally:
        conn.close()

def leggi_prodotti():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM prodotto")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print("Errore lettura prodotti:", err)
        return []
    finally:
        conn.close()

def leggi_ordini():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT ordini_id FROM ordini")
        results = cursor.fetchall()
        return np.array([r[0] for r in results])
    except mysql.connector.Error as err:
        print("Errore lettura ordini:", err)
        return np.array([])
    finally:
        conn.close()

def prezzi_prodotti_ordinati():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.prezzo
            FROM prodotto p
            JOIN ordine_prodotto op ON p.id = op.prodotto_id
        ''')
        prezzi = [row[0] for row in cursor.fetchall()]
        return np.array(prezzi)
    except mysql.connector.Error as err:
        print("Errore recupero prezzi:", err)
        return np.array([])
    finally:
        conn.close()
