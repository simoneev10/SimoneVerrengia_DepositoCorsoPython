import mysql.connector

def creazioneDB(dbName): # Funzione per accedere al server MySQL
    connessione = mysql.connector.connect(
        host = "localhost",
        user = 'root',
        password = ""
    )
    
    cursor = connessione.cursor()
    
    # Crea il database solo se non esiste già
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbName}")
    
    # Terminate le operazioni iniziali chiudo cursore e connessione al DB    
    cursor.close()
    connessione.close()
    
    myDB = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = dbName
    )
    
    print(f"Connesso al Database {dbName}!")
    return myDB