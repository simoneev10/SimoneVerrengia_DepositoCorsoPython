class ContoBancario: # Classe ContoBancario con attributi privati
    def __init__(self, titolare, saldo):
        self.__titolare = titolare
        self.__saldo = saldo
    
    def get_saldo(self): # Getter - Metodo per accedere alle variabile privata [saldo]
        return self.__saldo
    
    def set_saldo(self, saldo): # Setter - Metodo per modifcare la variabile privata [saldo]
        self.__saldo = saldo
        
    def get_titolare(self): # Getter - Metodo per accedere alle variabile privata [titolare]
        return self.__titolare
    
    def set_titolare(self, titolare): # Setter - Metodo per modifcare la variabile privata [titolare]
        self.__titolare = titolare
    
    def deposita(self): # metodo che serve a depositare denaro nel conto sfruttando i getter ed i setter
        try:    
            importoIns = int(input("Quanti soldi vuoi depositare?: "))
            nuovoImporto = self.get_saldo() + importoIns
            self.set_saldo(nuovoImporto)
        except ValueError:
            print("Inserisci numero valido!")
            return
            
    def preleva(self): # metodo che serve a prelevare denaro nel conto sfruttando i getter ed i setter
        try: 
            importoPrelievo = int(input("Quanti soldi vuoi prelevare?: "))
            soldiRestanti = self.get_saldo()
            if importoPrelievo > soldiRestanti:
                print("Non possiedi abbastanza fondi!")
            else:
                ris = soldiRestanti - importoPrelievo 
                self.set_saldo(ris)
        except ValueError:
            print("Inserisci numero valido!")
            return
                
        
if __name__ == "__main__":
    conto = ContoBancario("Simone", 1000)
    print(f"Conto di {conto.get_titolare()}")
    
    while True: # Menu per simulare tutte le funnzionalità
        print(f"\nSaldo attuale: €{conto.get_saldo()}")
        scelta = input("[D]eposita, [P]releva, [E]sci: ").upper()
        
        if scelta == "D":
            conto.deposita()
        elif scelta == "P":
            conto.preleva()
        elif scelta == "E":
            break
        else:
            print("Scelta non valida")