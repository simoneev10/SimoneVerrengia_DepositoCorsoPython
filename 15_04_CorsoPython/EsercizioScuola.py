class Persona: # Classe Padre da specializzare poi in studente e professore
    def __init__(self, nome, eta):
        self.__nome = nome 
        self.__eta = eta
    # Prosegue poi con getter e setter    
    def get_nome(self):
        return self.__nome
    
    def get_eta(self):
        return self.__eta
    
    def set_nome(self, nome):
        self.__nome = nome
    
    def set_eta(self, eta):
        self.__eta = eta
    # Metodo per la presentazione poi da modificarne il comportamento per studente e prof    
    def presentazione(self):
        print(f"\nCiao sono {self.get_nome()} ed ho {self.get_eta()} anni!")

class Studente(Persona):
    def __init__(self, nome, eta, voti=None):
        super().__init__(nome, eta)
        self.voti = voti if voti else {}
    
    def calcola_media(self):
        if not self.voti:
            return 0
        return sum(self.voti.values()) / len(self.voti)
    
    def aggiungi_voto(self, materia, voto):
        self.voti[materia] = voto
    
    def presentazione(self):
        print(f"\nCiao sono {self.get_nome()} ed ho {self.get_eta()} anni!")
        print(f"La mia media è: {self.calcola_media():.2f}")
        print("Voti per materia:")
        for materia, voto in self.voti.items():
            print(f"- {materia}: {voto}")

class Professore(Persona):
    def __init__(self, nome, eta, materia):
        super().__init__(nome, eta)
        self.materia = materia
    
    def cambia_materia(self, nuova_materia):
        self.materia = nuova_materia
    
    def presentazione(self):
        print(f"\nCiao sono {self.get_nome()} ed ho {self.get_eta()} anni!")
        print(f"Insegno: {self.materia}")

# Funzioni di creazione
def crea_studente():
    nome = input("Inserisci nome studente: ")
    eta = int(input("Inserisci età studente: "))
    voti = {}
    nmat = int(input("Quante materie vuoi inserire?: "))
    for i in range(nmat):
        materia = input("Inserisci materia: ")
        if not materia:
            break
        voto = int(input(f"Inserisci voto per {materia}: "))
        voti[materia] = voto
    return Studente(nome, eta, voti)

def crea_professore():
    nome = input("Inserisci nome professore: ")
    eta = int(input("Inserisci età professore: "))
    materia = input("Inserisci materia insegnata: ")
    return Professore(nome, eta, materia)

# Funzioni di visualizzazione
def visualizza_studenti(studenti):
    print("\n=== STUDENTI ===")
    if not studenti:
        print("Nessuno studente registrato!")
        return
    for id_studente, studente in studenti.items():
        print(f"\nID: {id_studente}")
        studente.presentazione()

def visualizza_professori(professori):
    print("\n=== PROFESSORI ===")
    if not professori:
        print("Nessun professore registrato!")
        return
    for id_professore, professore in professori.items():
        print(f"\nID: {id_professore}")
        professore.presentazione()

# Funzioni di modifica
def aggiungi_voto_studente(studenti):
    visualizza_studenti(studenti)
    if not studenti:
        return
    id_studente = input("\nInserisci ID studente: ")
    if id_studente not in studenti:
        print("ID studente non valido!")
        return
    materia = input("Inserisci materia: ")
    voto = int(input("Inserisci voto: "))
    studenti[id_studente].aggiungi_voto(materia, voto)
    print("Voto aggiunto con successo!")

def cambia_materia_professore(professori):
    visualizza_professori(professori)
    if not professori:
        return
    id_professore = input("\nInserisci ID professore: ")
    if id_professore not in professori:
        print("ID professore non valido!")
        return
    nuova_materia = input("Inserisci nuova materia: ")
    professori[id_professore].cambia_materia(nuova_materia)
    print("Materia cambiata con successo!")

# Menu principale
def menu():
    studenti = {}
    professori = {}
    id_counter_studenti = 1
    id_counter_professori = 1
    
    while True:
        print("\nBenvenuto nella Scuola del Pitone!\nCosa vuoi fare?")
        print("1. Aggiungi studente")
        print("2. Aggiungi professore")
        print("3. Visualizza studenti")
        print("4. Visualizza professori")
        print("5. Aggiungi voto a studente")
        print("6. Cambia materia professore")
        print("0. Esci")
        
        scelta = input("\nScelta: ")
        
        if scelta == "1":
            studenti[f"S{id_counter_studenti}"] = crea_studente()
            print(f"Studente creato con ID: S{id_counter_studenti}")
            id_counter_studenti += 1
        elif scelta == "2":
            professori[f"P{id_counter_professori}"] = crea_professore()
            print(f"Professore creato con ID: P{id_counter_professori}")
            id_counter_professori += 1
        elif scelta == "3":
            visualizza_studenti(studenti)
        elif scelta == "4":
            visualizza_professori(professori)
        elif scelta == "5":
            aggiungi_voto_studente(studenti)
        elif scelta == "6":
            cambia_materia_professore(professori)
        elif scelta == "0":
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida!")

if __name__ == "__main__":
    menu()