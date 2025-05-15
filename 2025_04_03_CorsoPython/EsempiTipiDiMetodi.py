# Esempio metodo statico
class Calcolatrice:
    
    @staticmethod
    def somma(a, b):
        return a + b

# Uso del metodo statico senza creare un'istanza    
risultato = Calcolatrice.somma(3, 7)
print(risultato)

# Esempio metodo decorato
class Contatore:
    numero_istanze = 0 # Attributo di classe
    
    def __init__(self):
        Contatore.numero_istanze += 1
        
    @classmethod
    def mostra_numero_istanze(cls):
        print(f"Sono state create {cls.numero_istanze} istanze.")
        
# Creazione di alcune istanze
C1 = Contatore()
C2 = Contatore()

Contatore.mostra_numero_istanze()