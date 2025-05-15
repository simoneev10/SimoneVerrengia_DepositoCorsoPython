class Ristorante:
    
    # menu = {"Carbonara":10}
    aperto = False
    
    def __init__(self, nomeRistorante, tipoCucina, menu):
        self.nomeRistorante = nomeRistorante
        self.tipoCucina = tipoCucina
        self.menu = menu
    
    def descrivi_ristorante(self): # Metodo che stampa le info del ristorante
        if self.aperto == True:# Traduco il flag
            tipo = "aperto"
        else:
            tipo ="chiuso"
        
        print(f"\nIl ristorante è il {self.nomeRistorante}, ha una cucina di tipo {self.tipoCucina} ed è {tipo}!")
        
    def stato_apertura(self): # Metodo che stampa se il ristorante è chiuso o aperto
        if self.aperto == False:
            print("\nIl ristorante è chiuso!")        
        else:
            print("\nIl ristorante è aperto!")
            
    def apri_ristorante(self): # Metodo che cambia lo stato del ristorante da chiuso ad aperto
        if self.aperto == False:
            self.aperto == True
            print("\nAdesso il ristorante è aperto!")        
        else:
            print("\nIl ristorante è già aperto!")
            
    def chiudi_ristorante(self): # Metodo che cambia lo stato del ristorante da aperto a chiuso
        if self.aperto == True:
            self.aperto == False        
        else:
            print("\nIl ristorante è già chiuso!")
    
    def aggiungi_al_menu(self): # Metodo per aggiungere al dizionario un piatto
        piatto = input("Inserisci il nome: ")
        prezzo = input("Inserisci il prezzo: ")
        self.menu[piatto] = prezzo # Aggiungo il prezzo alla key piatto

    def rimuovi_dal_menu(self): # Metodo per rimuovere un piatto dal menu
        print("Ecco i piatti disponibili nel menu:")
        for i, piatto in enumerate(self.menu.keys(), start=1): # Stampo i piatti con un indice
            print(f"{i}) {piatto}")
        
        scelta = int(input("Seleziona il numero del piatto da rimuovere: "))
        if 1 <= scelta <= len(self.menu):
            piatto_da_rimuovere = list(self.menu.keys())[scelta - 1]
            del self.menu[piatto_da_rimuovere] # Rimuovo il piatto selezionato
            print(f"Il piatto '{piatto_da_rimuovere}' è stato rimosso dal menu.")
        else:
            print("Scelta non valida.")
        
    def stampa_menu(self):
        for piatto, prezzo in self.menu.items(): # Scorro i piatti presenti nel menu e li stampo
            print(f"{piatto}: {prezzo}€")
        
Ristorante1 = Ristorante("Taverna di Pippo", "Italiana", {"Spaghetto allo scoglio": 12})

while True: # Ciclo per avere un menu di selezione
    print("\nMenu:")
    print("1) Visualizzare il ristorante")
    print("2) Verificare se il ristorante è aperto o chiuso")
    print("3) Aprire il ristorante")
    print("4) Chiudere il ristorante")
    print("5) Aggiungere un piatto al menu")
    print("6) Rimuovere un piatto dal menu")
    print("7) Visualizzare il menu")
    print("8) Uscire")
    
    scelta = int(input("Scegli un'opzione: "))
    
    if scelta == 1:
        Ristorante1.descrivi_ristorante()
    elif scelta == 2:
        Ristorante1.stato_apertura()
    elif scelta == 3:
        Ristorante1.aperto = True
        print("\nIl ristorante è stato aperto!")
    elif scelta == 4:
        Ristorante1.aperto = False
        print("\nIl ristorante è stato chiuso!")
    elif scelta == 5:
        Ristorante1.aggiungi_al_menu()
        print("\nPiatto aggiunto al menu con successo!")
    elif scelta == 6:
        Ristorante1.rimuovi_dal_menu()
    elif scelta == 7:
        print("\nEcco il menu del ristorante:")
        Ristorante1.stampa_menu()
    elif scelta == 8:
        print("\nArrivederci!\n")
        break
    else:
        print("Scelta non valida. Riprova.")
