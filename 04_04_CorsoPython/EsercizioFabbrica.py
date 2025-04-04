# Esercizio fabbrica che produce vende vari tipi di prodotto

class Prodotto: # Definisco la classe prodotto con tutti gli attributi da traccia
    
    def __init__(self, nome, costo_produzione, prezzo_vendita):
        self.nome = nome
        self.costo_produzione = costo_produzione
        self.prezzo_vendita = prezzo_vendita
        self.venduto = False

    def calcolca_profitto(self): # Metodo che verrà utilizzato per il calcolo del profitto
        profitto = self.prezzo_vendita - self.costo_produzione
        return profitto
    
class Fabbrica: # Definisco la classe fabbrica
        
    def __init__(self):
        self.inventario = {} # Dizionario creato per contenere i prodotti
        self.prox_id = 1 # Variabile utilizzata per id dei prodotti
    
    def stampa_inv(self): # Metodo per stampare i prodotti presenti e controllo se il prodotto è disponibile
        
        if not self.inventario:
            print("\nMi dispiace, al momento non sono disponibili prodotti nell'inventario.")
            return
        
        for id_prodotto, prodotto in self.inventario.items():
            if prodotto.venduto:
                stato = "Venduto"
            else:
                stato = "Disponibile"
            print(f"\nID: {id_prodotto}\nNome: {prodotto.nome}\nCosto: {prodotto.costo_produzione}\nPrezzo Vendita: {prodotto.prezzo_vendita} euro\nStato: {stato}")
        
    def aggiungi_prodotto(self): # Metodo per aggiungere il prodotto all'inventario
        nome = input("Inserisci nome prodotto: ")
        costoP = int(input("Inserisci costo produzione: "))
        prezzoV = int(input("Inserisci prezzo vendita: "))
        id_prodotto = self.prox_id # Assegno id al prodotto
        self.inventario[id_prodotto] = Prodotto(nome,costoP,prezzoV) # Aggiungo il prodotto al dizionario
        self.prox_id += 1
        
    def vendi_prodotto(self): # Metodo per segnare una vendita di un prodotto
        self.stampa_inv()
        ins = int(input("\nQuale prodotto hai venduto? (inserisci id):"))
        
        if ins in self.inventario:
            if not self.inventario[ins].venduto:
                self.inventario[ins].venduto = True
                print(f"Prodotto {ins} venduto con successo!")
            else:
                print("Prodotto già venduto!")
        else:
            print("ID prodotto non valido!")
            
    def resi_prodotto(self): # Metodo per fare reso di un prodotto con controllo sulla vendita del prodotto 
        self.stampa_inv()
        reso = int(input("\nDi quale prodotto vuoi fare il reso? (inserisci id)"))
        
        if reso in self.inventario:
            if self.inventario[reso].venduto:
                self.inventario[reso].venduto == False
                print(f"\nReso del prodotto {reso} registrato con successo!\nRiceverai i soldi entro 3-4 giorni lavorativi.")
            else:
                print(f"Non è questo il prodotto di cui vuoi fare il reso!")
        else:
            print("ID prodotto non valido!")
    
fabbrica = Fabbrica()

print("\nBenvenuto nella fabbrica di Simone!\n")
while True: # Menu creato per richiamare le varie funzionalità
    print("\nCosa vuoi fare? ")
    print("1. Aggiungi prodotto")
    print("2. Visualizza inventario")
    print("3. Vendi prodotto")
    print("4. Registra reso")
    print("5. Esci")
        
    scelta = input("Scegli un'opzione (1-5): ")
        
    if scelta == "1":
        fabbrica.aggiungi_prodotto()
    elif scelta == "2":
        fabbrica.stampa_inv()
    elif scelta == "3":
        fabbrica.vendi_prodotto()
    elif scelta == "4":
        fabbrica.resi_prodotto()
    elif scelta == "5":
        print("\nGrazie per aver usato il sistema!")
        break
    else:
        print("\nScelta non valida! Riprova")
                