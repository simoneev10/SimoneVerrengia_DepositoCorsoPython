class Pasticceria():
    def __init__(self, nome, guadagnoStimato):
        self.nome = nome
        self.__inventario = {}
        self.__guadagnoStimato = guadagnoStimato

    # Getter per inventario
    def get_inventario(self):
        return self.__inventario

    # Setter per inventario
    def set_inventario(self, nuovo_inventario):
        self.__inventario = nuovo_inventario

    # Getter per guadagno stimato
    def get_guadagno_stimato(self):
        return self.__guadagnoStimato

    # Setter per guadagno stimato
    def set_guadagno_stimato(self, nuovo_guadagno):
        self.__guadagnoStimato = nuovo_guadagno
        
    def crea_torta(self, peso, nome):
        #nome = input("Inserisci nome: ")
        inventarioApp = self.get_inventario()
        for key,values in inventarioApp.items():
            if key == inventarioApp[nome]:
                print("La torta è già presente nell'inventario!")
                del inventarioApp[nome]
                self.set_inventario(inventarioApp)
                return
            else:
                peso = input("Inserisci il peso (in Kg): ")
                match nome:
                    case "TortaFrutta":
                        torta = TortaFrutta(peso)
                        print(f"Print torta {self.nome} è stata aggiunta all'inventario")
                    case "TortaMela":
                        torta = TortaMela(peso)
                        print(f"Print torta {self.nome} è stata aggiunta all'inventario")
                    case "TortaCioccolato":
                        torta = TortaCioccolato(peso)
                        print(f"Print torta {self.nome} è stata aggiunta all'inventario")
                
                inventarioApp[nome] = peso
                #torta(nome)
    
    
    def prezzo_torta(self, peso, nome):
        #inventarioApp = self.get_inventario()
        # for key,values in inventarioApp.items():
        prezzo = nome.calcola_prezzo(peso)
        return prezzo
         
        
                
    def ordina_torta(self, peso, nome):
        #nome = input("Inserisci nome: ")
        inventarioApp = self.get_inventario()
        for key,values in inventarioApp.items():
            if key == inventarioApp[nome]:
                print("La torta è già presente nell'inventario!")
                del inventarioApp[nome]
                self.set_inventario(inventarioApp)
                return
            else:
                peso = input("Inserisci il peso (in Kg): ")
                match nome:
                    case "TortaFrutta":
                        torta = TortaFrutta(peso)
                        print(f"La torta {self.nome} è stata ordinata")
                    case "TortaMela":
                        torta = TortaMela(peso)
                        print(f"La torta {self.nome} è stata ordinata")
                    case "TortaCioccolato":
                        torta = TortaCioccolato(peso)
                        print(f"La torta {self.nome} è stata ordinata")
                    case _:
                        print("Scelta non valida")
                        return False
        return True
         
    def calcola_guadagno(self):
        inventarioApp = self.get_inventario()
        totValore = 0
        for key,values in self.inventarioApp.items():
            prezzo = key.calcola_prezzo(inventarioApp[key])
            totValore += prezzo
        print(f"Il guadagno stimato è: {totValore}")
        
past = Pasticceria()

class Cliente():
    def __init__(self, nome, budget):
        self.nome = nome
        self.__budget = budget
    
    # getter per inventario    
    def get_budget(self):
        return self.__budget

    # Setter per inventario
    def set_budget(self, budget):
        self.__budget = budget
         
    def prenota_torta(self):
        peso = float(input("Inserisci il peso: "))
        nome_torta = input("Inserisci nome: ")
        cliente_budget = self.get_budget()
        prezzo = past.ordina_torta(peso, nome_torta)
        if cliente_budget >= prezzo:
            cliente_budget -= prezzo
            self.set_budget(cliente_budget)
            print("La torta è stata acquistata!")
        else:
            print("Budget non abbastanza alto")
        