# Definizione della classe Automobile
class Automobile:
    # Attributo di classe che rappresenta il numero di ruote di un'automobile
    numero_di_ruote = 4

    # Metodo costruttore per inizializzare gli attributi di un'istanza
    def __init__(self, marca, modello): # Il self sta ad indicare per esempio che sia auto1
        self.marca = marca  # Attributo di istanza per la marca dell'automobile
        self.modello = modello  # Attributo di istanza per il modello dell'automobile
        
    # Metodo per stampare le informazioni dell'automobile
    def stampa_info(self):
        print("L'automobile è una", self.marca, self.modello)  # Stampa marca e modello dell'automobile
        
# Creazione di un'istanza della classe Automobile con marca "Fiat" e modello "500"
Auto1 = Automobile("Fiat", "500") 

# Creazione di un'altra istanza della classe Automobile con marca "BMW" e modello "Serie 1"
Auto2 = Automobile("BMW", "Serie 1")

# Stampa delle informazioni delle automobili create
Auto1.stampa_info()
Auto2.stampa_info()

# Stampa del numero di ruote dell'automobile
print("Il numero di ruote dell'automobile è:", Auto1.numero_di_ruote)

# Creazione della classe Persona

class Persona:
    def __init__(self, nome, eta):
        self.nome = nome # Attributo per memorizzare il nome
        self.eta = eta # Attributo per memorizzare l'età

# Creazione di un oggetto Persona
p = Persona("Simone", 27)

# Stampo l'oggetto creato
print(p.nome)
print(p.eta)

print(p.eta - 1)