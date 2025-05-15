print("Ciao! Sono il sistema di login del corso Python.")
#Inserimento dati
nome = input("Inserire nome: ")
passw = input("Inserire pass: ")
utente_p = [nome,passw]
utenti = [["admin","123"]]
#prima controllo se presente e utenza e pass corrispondono
if utente_p in utenti:
    print("Ancora un attimo.")
    colore = input("Qual è il tuo colore preferito?")
    #ulteriore controllo di sicurezza
    if colore != "nero":
        print("Risposta alla domanda segreta non corretta!")
        print("Uscita in corso...")
    else:
        print("Benvenuto ", utente_p[0])
    
else:
    print("Utente non esistente!")
    


#Versione con lo switch

print("Ciao! Sono il sistema di login del corso Python.")
com = input("Vuoi Loggare o creare un nuovo account? (l/c)")
utenti = [["admin","123"]]

match com:
    case "l":
        nome = input("Inserire nome: ")
        passw = input("Inserire pass: ")
        utente_p = [nome,passw]
        
        #prima controllo se presente e utenza e pass corrispondono
        if utente_p in utenti:
            print("Ancora un attimo.")
            colore = input("Qual è il tuo colore preferito?")
            #ulteriore controllo di sicurezza
            if colore != "nero":
                print("Risposta alla domanda segreta non corretta!")
                print("Uscita in corso...")
            else:
                print("Benvenuto ", utente_p[0])
    
        else:
            print("Utente non esistente!")
    case "c":
        nome = input("Inserire nome: ")
        passw = input("Inserire pass: ")
        utente_p1 = [nome,passw]
        if utente_p1 in utenti:
            print("Nome utente già presente!")
        else:
            print("Benvenuto ", utente_p1[0])