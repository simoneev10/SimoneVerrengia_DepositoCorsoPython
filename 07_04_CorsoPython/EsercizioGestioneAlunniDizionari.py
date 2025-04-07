# Sistema gestionale sugli alunni, con inserimento nome e voti (funzionalità media voto) Scegliere una chiave 
from statistics import mean

class Alunno(): # Creo una classe di tipo alunno
    
    def __init__(self, nome, cognome): # Attributi come da traccia
        self.nome = nome
        self.cognome = cognome
        self.voti = []
        
class Aula(): # Classe aula dove gestisco gli oggetti di tipo alunno
    
    def __init__(self):
        self.registro = {}
        self.proxId = 0
        
    def inserimentoAlunni(self): # Metodo per inserire gli alunnoi nel dizionario
        nome = input("Inserisci un nome: ")
        cognome = input("Inserisci cognome: ")
        alunno = Alunno(nome, cognome)
        
        nvoti = int(input("Quanti voti vuoi inserire: "))
        for _ in range(nvoti):
            appoggio = int(input("Inserisci voto: "))
            alunno.voti.append(appoggio) # Aggiugno voti 
        idAlunno = self.proxId
        self.registro[idAlunno] = alunno
        self.proxId += 1 # Aumento l'id ad ogni inserimento
        print(f"{self.proxId}")
        
    def visualizzaAula(self):
        
        if not self.registro:
            print("\nNessun alunno presente nel registro!")
        else:
            for key, value in self.registro.items(): # Scorro il dizionario per stampare a schermo
                print(f"\nID: {value.proxId} \nNome: {value.nome} \nCognome: {value.cognome} \nVoti: {value.voti}")
                
    def mediaVoti(self):
        
        if not self.registro:
            print("\nNessun alunno presente nel registro!")
        else:
            for key, value in self.registro.items(): 
                media = mean(value.voti) # Funzione per media importata da statistics
                print(f"\nID: {value.proxId} \nNome: {value.nome} \nCognome: {value.cognome} \nMedia: {media}")
                
                
aula = Aula() # Istanzio l'aula

while True: # Menu per selezionare cosa fare
    print("\nMENU GESTIONE ALUNNI")
    print("1. Inserisci nuovo alunno")
    print("2. Visualizza registro alunni")
    print("3. Calcola medie voti")
    print("4. Esci\n")
        
    scelta = input("Seleziona un'opzione: ")
        
    match scelta:
        case "1":
            aula.inserimentoAlunni()
        case "2":
            aula.visualizzaAula()
        case "3":
            aula.mediaVoti()
        case "4":
            print("Programma terminato.")
            break
        case _:
            print("Scelta non valida. Riprova.")
