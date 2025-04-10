import mysql.connector

myDB = mysql.connector.connect(
    host = "localhost",
    user = 'root',
    password = "",
    database = "corsopython"
)
"""
# Per interfarciarci bisogna creare un cursore

myCursor = myDB.cursor()

queryCreazioneDB = "CREATE DATABASE CorsoPython"

#myCursor.execute(queryCreazioneDB)

# Query per vedere i database

QueryVisualizzazioneDB = "SHOW DATABASES"

myCursor.execute(QueryVisualizzazioneDB)
for db in myCursor: # per vedere tutti i db dobbiamo inserirla in un ciclo
    print(db)

# Il cursore dopo un for "si scarica", dovrei ricaricare il cursore

# inserimento prima tabella
myCursor = myDB.cursor()
queryUtenti = "CREATE TABLE utenti(ID int PRIMARY KEY, NOME VARCHAR(50), INDIRIZZO VARCHAR(50))"
myCursor.execute(queryUtenti)


myCursor = myDB.cursor()
queryUtenti = "INSERT INTO utenti(NOME, INDIRIZZO) VALUES(%s,%s)"
val = ("Simone","Via Roma") #Inserimento prima tupla

myCursor.execute(queryUtenti,val)

myDB.commit()

print(myCursor.rowcount, "righe inserite!")

myCursor = myDB.cursor()
queryUtenti = "ALTER TABLE utenti MODIFY ID INT AUTO_INCREMENT" #Modifico la primary key in modo che incrementa sempre l'id per ogni inserimento
myCursor.execute(queryUtenti)

#Metodo inserimento più righe
myCursor = myDB.cursor()
val = [("Filippo","Via Napoli"),("Giacomo","Via Cassino")]

queryUtenti = "INSERT INTO utenti(NOME, INDIRIZZO) VALUES(%s,%s)"
myCursor.executemany(queryUtenti, val)
myDB.commit()
print(myCursor.rowcount, "righe inserite!")
print("Ultimo id inserito: ", myCursor.lastrowid)
"""

#Creo funzioni per le varie operazioni
def InsertManyRow(dati):
    myCursor = myDB.cursor()

    queryUtenti = "INSERT INTO utenti(NOME, INDIRIZZO) VALUES(%s,%s)"
    
    myCursor.executemany(queryUtenti, dati)
    myDB.commit()
    
    print(myCursor.rowcount, "righe inserite!")
    print("Ultimo id inserito: ", myCursor.lastrowid)

myCursor = myDB.cursor()

def readRows():
    query = "select * from utenti"
    myCursor.execute(query)
    result = myCursor.fetchall()
    for row in result:
        print(row)
        
def readRow():
    query = "select * from utenti"
    myCursor.execute(query)
    result = myCursor.fetchone()
    print(result)
    
#readRow()
#readRows()

#myDB.close() per chiudere la connessione con il DB