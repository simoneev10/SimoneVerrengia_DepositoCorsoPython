# Esercizio per la gestione di una classe con scrittura su file

def calcola_media(voti): # Funzione per il calcolo della media
    somma = 0
    for voto in voti:
        somma += voto
    return round(somma / len(voti), 2)

def crea_file_csv():
    try:
        # Prova ad aprire il file in lettura per vedere se esiste
        with open("alunni.csv", "r"):
            pass
    except:
        # Se il file non esiste, lo crea con intestazione
        with open("alunni.csv", "w") as file:
            file.write("Nome,Cognome,Voti,Media")

def aggiungi_alunno(): # Funzione per aggiungere un alunno alla classe (alunni.csv)
    
    nome = input("Nome: ").strip()
    cognome = input("Cognome: ").strip()
    
    with open("alunni.csv", "r") as file:
        contenuto = file.read()

    righe = contenuto.splitlines()

    alunno_presente = False # Flag utilizzato per verificare la presenza

    for riga in righe:
        dati = riga.strip().split(",") # Utilizzo dati per vedere se in righe è presente l'alunno
        if dati[0] == nome and dati[1] == cognome:
            alunno_presente = True
            break
    
    if alunno_presente:
        print("Alunno già presente nel registro.\n")
        return  # oppure: continua, se vuoi che possa riprovare
    else:
        numero_voti = int(input("Quanti voti vuoi inserire? "))
        voti = []
        for i in range(numero_voti): # For per inserire il numero di voti selezionato
            voto = int(input(f"Inserisci voto {i+1}: "))
            voti.append(voto)

        voti_str = "-".join([str(v) for v in voti]) # Li salvo in questo modo: 6-7-8
        media = calcola_media(voti)

        with open("alunni.csv", "a") as file:
            file.write(f"\n{nome},{cognome},{voti_str},{media}")
        print("Alunno aggiunto!\n")

def mostra_alunni(): # Funzione per mostrare tutti gli alunni
    try:
        with open("alunni.csv", "r") as file:
            righe = file.read()
        righe_lista = righe.split("\n")
        if len(righe_lista) <= 1: # Controllo se non ci sono alunni inseriti
            print("Nessun alunno nel registro.\n")
        else:
            print("\n--- Registro Alunni ---")
            for riga in righe_lista: # scorro tutte le righe e le stampo
                print(riga.strip())
    except:
        print("Errore nella lettura del file.")

def modifica_alunno(): # Funzione per modificare i dati dell'alunno
    nome = input("Nome dell'alunno da modificare: ").strip()
    cognome = input("Cognome: ").strip()
    trovato = False
    nuove_righe = []

    with open("alunni.csv", "r") as file:
        contenuto = file.read()
    
    righe = contenuto.splitlines()

    for riga in righe:
        dati = riga.strip().split(",")
        if dati[0] == nome and dati[1] == cognome: # Scorro le righe e uso dati per vedere se i dati corrispondono
            trovato = True
            print("Alunno trovato. Inserisci i nuovi voti.")
            nuovi_voti = []
            numero = int(input("Quanti voti vuoi inserire? "))
            for i in range(numero):
                voto = int(input(f"Voto {i+1}: "))
                nuovi_voti.append(voto)
            media = calcola_media(nuovi_voti)
            voti_str = "-".join(str(v) for v in nuovi_voti) # carico i voti in questo modo: 6-7-8
            nuove_righe.append(f"{nome},{cognome},{voti_str},{media}")
        else:
            nuove_righe.append(riga)
    if trovato:
        with open("alunni.csv", "w") as file:
            file.write("\n".join(nuove_righe))
        print("Alunno modificato!\n")
    else:
        print("Alunno non trovato.\n")

def elimina_alunno():
    nome = input("Nome dell'alunno da eliminare: ").strip()
    cognome = input("Cognome: ").strip()
    trovato = False
    nuove_righe = []

    with open("alunni.csv", "r") as file:
        righe = file.read().splitlines()

    for riga in righe:
        dati = riga.strip().split(",")
        if dati[0] == nome and dati[1] == cognome: # Scorro le righe e uso dati per vedere se i dati corrispondono
            trovato = True
            print(f"Alunno {nome} {cognome} eliminato.\n")
            continue # salta l'append della riga dove nome e cognome corrispondono
        nuove_righe.append(riga)

    if trovato:
        with open("alunni.csv", "w") as file:
            file.write("\n".join(nuove_righe))
    else:
        print("Alunno non trovato.\n")

def modifica_nomi_alunno():
    nome = input("Nome attuale dell'alunno: ").strip()
    cognome = input("Cognome attuale: ").strip()
    trovato = False
    nuove_righe = []

    with open("alunni.csv", "r") as file:
        righe = file.read().splitlines()

    for riga in righe:
        dati = riga.strip().split(",")
        if dati[0] == nome and dati[1] == cognome:  # Scorro le righe e uso dati per vedere se i dati corrispondono
            trovato = True
            nuovo_nome = input("Nuovo nome: ").strip()
            nuovo_cognome = input("Nuovo cognome: ").strip()
            nuove_righe.append(f"{nuovo_nome},{nuovo_cognome},{dati[2]},{dati[3]}")
            print("Nome e cognome modificati!\n")
        else:
            nuove_righe.append(riga)

    if trovato:
        with open("alunni.csv", "w") as file:
            file.write("\n".join(nuove_righe))
    else:
        print("Alunno non trovato.\n")


crea_file_csv()
# Menu per la gestione del registro elettronico
print("\nBenvenuto nel registro elettronico!")
while True:
    print("1. Aggiungi alunno")
    print("2. Mostra registro")
    print("3. Modifica voti alunno")
    print("4. Elimina alunno")
    print("5. Modifica nome/cognome")
    print("6. Esci")
    
    scelta = input("Scegli un'opzione: ")
    
    if scelta == "1":
        aggiungi_alunno()
    elif scelta == "2":
        mostra_alunni()
    elif scelta == "3":
        modifica_alunno()
    elif scelta == "4":
        elimina_alunno()
    elif scelta == "5":
        modifica_nomi_alunno()
    elif scelta == "6":
        print("\nArrivederci!\n")
        break
    else:
        print("Scelta non valida.\n")