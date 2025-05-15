class Posto:
    def __init__(self, numero, fila):
        self.__numero = numero
        self.__fila = fila
        self.__occupato = False

    def prenota(self):
        if not self.__occupato:
            self.__occupato = True
            print(f"Posto {self.__fila}{self.__numero} prenotato con successo.")
        else:
            print(f"Posto {self.__fila}{self.__numero} è già occupato.")

    def libera(self):
        if self.__occupato:
            self.__occupato = False
            print(f"Posto {self.__fila}{self.__numero} liberato.")
        else:
            print(f"Posto {self.__fila}{self.__numero} non era occupato.")

    def get_numero(self):
        return self.__numero

    def get_fila(self):
        return self.__fila

    def is_occupato(self):
        return self.__occupato

    def __str__(self):
        stato = "Occupato" if self.__occupato else "Libero"
        return f"Posto {self.__fila}{self.__numero} - {stato}"



class PostoVIP(Posto):
    def __init__(self, numero, fila, servizi_extra):
        super().__init__(numero, fila)
        self.__servizi_extra = servizi_extra

    def prenota(self):
        if not self.is_occupato():
            super().prenota()
            print(f"Servizi VIP attivati: {', '.join(self.__servizi_extra)}")
        else:
            print(f"Posto VIP {self.get_fila()}{self.get_numero()} è già occupato.")




class PostoStandard(Posto):
    def __init__(self, numero, fila, costo):
        super().__init__(numero, fila)
        self.__costo = costo

    def prenota(self):
        if not self.is_occupato():
            print(f"Il costo della prenotazione è di €{self.__costo}")
            super().prenota()
        else:
            print(f"Posto Standard {self.get_fila()}{self.get_numero()} è già occupato.")


class Teatro:
    def __init__(self):
        self.__posti = []

    def aggiungi_posto(self, posto):
        self.__posti.append(posto)

    def prenota_posto(self, numero, fila):
        for posto in self.__posti:
            if posto.get_numero() == numero and posto.get_fila() == fila:
                posto.prenota()
                return
        print(f"Nessun posto trovato per fila {fila} numero {numero}.")

    def stampa_posti_occupati(self):
        print("Posti occupati:")
        trovati = False
        for posto in self.__posti:
            if posto.is_occupato():
                print(posto)
                trovati = True
        if not trovati:
            print("Nessun posto è attualmente occupato.")


def menu_teatro():
    teatro = Teatro()

    while True:
        print("\n--- Menu Teatro ---")
        print("1. Aggiungi Posto Standard")
        print("2. Aggiungi Posto VIP")
        print("3. Prenota un posto")
        print("4. Libera un posto")
        print("5. Visualizza posti occupati")
        print("6. Esci")

        scelta = input("Scegli un'opzione (1-6): ").strip()

        match scelta:
            case "1":
                try:
                    numero = int(input("Numero del posto: "))
                    fila = input("Fila del posto: ").upper().strip()
                    costo = float(input("Costo del posto: "))
                    posto = PostoStandard(numero, fila, costo)
                    teatro.aggiungi_posto(posto)
                    print("Posto Standard aggiunto.")
                except:
                    print("Errore nell'inserimento dei dati.")
            
            case "2":
                try:
                    numero = int(input("Numero del posto: "))
                    fila = input("Fila del posto: ").upper().strip()
                    servizi = input("Servizi extra (separati da virgola): ").split(",")
                    servizi = [s.strip() for s in servizi if s.strip()]
                    posto = PostoVIP(numero, fila, servizi)
                    teatro.aggiungi_posto(posto)
                    print("Posto VIP aggiunto.")
                except:
                    print("Errore nell'inserimento dei dati.")
            
            case "3":
                numero = int(input("Numero del posto da prenotare: "))
                fila = input("Fila del posto da prenotare: ").upper().strip()
                teatro.prenota_posto(numero, fila)

            case "4":
                numero = int(input("Numero del posto da liberare: "))
                fila = input("Fila del posto da liberare: ").upper().strip()
                for posto in teatro._Teatro__posti:
                    if posto.get_numero() == numero and posto.get_fila() == fila:
                        posto.libera()
                        break
                else:
                    print("Posto non trovato.")

            case "5":
                teatro.stampa_posti_occupati()

            case "6":
                print("Chiusura programma. Arrivederci!")
                break

            case _:
                print("Scelta non valida. Riprova.")

if __name__ == "__main__":
    menu_teatro()