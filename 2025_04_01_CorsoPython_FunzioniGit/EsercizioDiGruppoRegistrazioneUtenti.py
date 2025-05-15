# Lista per memorizzare gli utenti registrati (nome utente, password)
utenti_registrati = []

# Lista per memorizzare i concerti registrati, ogni concerto è un dizionario con nome e posti disponibili
concerti_registrati = []  

# Lista per memorizzare le prenotazioni effettuate, ogni prenotazione è una tupla (utente, concerto)
prenotazioni_effettuate = []  

# Funzione per registrare un nuovo utente
def registra_utente():
    nome = input("Inserisci nome utente: ")
    for utente in utenti_registrati:
        if utente[0] == nome:  # Controlla se l'utente è già registrato
            print("Utente già registrato.")
            return
    password = input("Inserisci password: ")
    utenti_registrati.append((nome, password))  # Aggiunge l'utente
    print("Registrazione completata.")

# Funzione per effettuare il login di un utente
def login():
    tentativi = 0
    while tentativi < 3:  # Limita i tentativi di login a 3
        nome = input("Nome utente: ")
        password = input("Password: ")
        for utente in utenti_registrati:
            if utente[0] == nome and utente[1] == password:  # Verifica le credenziali
                print("Login riuscito!")
                return nome
        print("Credenziali errate.")
        tentativi += 1
    print("Troppi tentativi falliti. Login bloccato.")
    return None

# Funzione per aggiungere un nuovo concerto
def aggiungi_concerto():
    if len(concerti_registrati) >= 3:  # Controlla il limite massimo di concerti
        print("Limite massimo di concerti raggiunto.")
        return
    password2 = input("Inserisci password segreta per aggiungere concerti: ")
    if password2 != "GHIBLI":  # Verifica la password segreta
        print("Password segreta errata!")
        return
    nome_concerto = input("Nome del concerto: ")
    # Aggiunge il concerto con il numero di posti disponibili
    concerti_registrati.append({"nome": nome_concerto, "posti": 10})
    print(f"Concerto '{nome_concerto}' aggiunto con successo.")

# Funzione per prenotare un concerto
def prenota_concerto(utente):
    if not concerti_registrati:  # Controlla se ci sono concerti disponibili
        print("Nessun concerto disponibile.")
        return
    print("Concerti disponibili:")
    # Mostra l'elenco dei concerti disponibili
    for i in range(len(concerti_registrati)):
        c = concerti_registrati[i]
        print(f"{i + 1}. {c['nome']} (Posti: {c['posti']})")
    scelta = int(input("Seleziona il numero del concerto da prenotare: ")) - 1
    if 0 <= scelta < len(concerti_registrati):  # Controlla se la scelta è valida
        concerto = concerti_registrati[scelta]
        if concerto['posti'] > 0:  # Controlla se ci sono posti disponibili
            concerto['posti'] -= 1  # Riduce il numero di posti disponibili
            prenotazioni_effettuate.append((utente, concerto['nome']))  # Registra la prenotazione
            print("Prenotazione effettuata!")
        else:
            print("Posti esauriti per questo concerto.")
    else:
        print("Scelta non valida.")

# Funzione principale che gestisce il menu e il flusso del programma
def main():
    while True:
        print("\n1. Registrati\n2. Login\n3. Esci")
        scelta = input("Seleziona un'opzione: ")

        if scelta == "1":
            registra_utente()  # Opzione per registrare un nuovo utente
        elif scelta == "2":
            utente = login()  # Opzione per effettuare il login
            if utente:
                while True:
                    print("\n1. Prenota Concerto\n2. Aggiungi Concerto\n3. Logout")
                    scelta2 = input("Seleziona un'opzione: ")
                    if scelta2 == "1":
                        prenota_concerto(utente)  # Opzione per prenotare un concerto
                    elif scelta2 == "2":
                        aggiungi_concerto()  # Opzione per aggiungere un concerto
                    elif scelta2 == "3":
                        break  # Logout
        elif scelta == "3":
            print("Uscita dal programma.")  # Esce dal programma
            break
        else:
            print("Scelta non valida.")  # Gestisce scelte non valide

# Punto di ingresso del programma
if __name__ == "__main__":
    main()