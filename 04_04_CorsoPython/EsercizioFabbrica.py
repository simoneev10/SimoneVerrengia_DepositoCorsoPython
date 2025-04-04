# Esercizio fabbrica che produce vende vari tipi di prodotto

class Prodotto:
    
    # id = 0
    
    def __init__(self, nome, costo_produzione, prezzo_vendita):
        self.nome = nome
        self.costo_produzione = costo_produzione
        self.prezzo_vendita = prezzo_vendita
        self.venduto = False
        # self.id += 1
        
    def calcolca_profitto(self):
        profitto = self.prezzo_vendita - self.costo_produzione
        return profitto
    
 
class Fabbrica:
        
    def __init__(self):
        self.inventario = {}
        self.prox_id = 1
    
    def stampa_inv(self):
        for id_prodotto, prodotto in self.inventario.items():
            if prodotto.venduto:
                stato = "Venduto"
            else:
                stato = "Disponibile"
            print(f"\nID: {id_prodotto}\nNome: {prodotto.nome}\nCosto: {prodotto.costo_produzione}\nPrezzo Vendita: {prodotto.prezzo_vendita} euro\nStato: {stato}")
        
    def aggiungi_prodotto(self):
        nome = input("Inserisci nome prodotto: ")
        costoP = int(input("Inserisci costo produzione: "))
        prezzoV = int(input("Inserisci prezzo vendita: "))
        id_prodotto = self.prox_id
        self.inventario[id_prodotto] = Prodotto(nome,costoP,prezzoV)
        self.prox_id += 1
        
    def vendi_prodotto(self):
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
            
    def resi_prodotto(self):
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
while True:
    print("\nBenvenuto nella fabbrica di Simone!\nCosa vuoi fare? ")
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
                