#Terzo Esercizio
#dati pre-inseriti per seconda condizione
idAcc = 0
account = [["mirko","pippo",idAcc]]
#momento della scelta, se "s" si va alla creazione
#altrimenti si verifica se è già presente
risposta = input("Vuoi creare un account? (s/n): ")

if risposta == "s": #creazione account
    
    nome = input("Inserisci il nome: ")
    passw = input("Inserisci la password: ")
    #creo una listra contenente il nuovo account
    nnuovo_account = [nome,passw,idAcc+1]
    #e lo aggiungo agli account
    account.append(nnuovo_account)
    
    if nome in account:
        print("Account già presente!")
        account.remove(nnuovo_account)
    else:
        print("Account creato!")
        print(account)   
    
else: #controllo l'accesso
    print("Ottimo, allora effettuiamo l'accesso!")
    nome = input("Inserisci il nome: ")
    passw = input("Inserisci la password: ")
    
    if nome in account and passw in account:
        print("Account trovato!")
    else:
        print("Account non trovato!")