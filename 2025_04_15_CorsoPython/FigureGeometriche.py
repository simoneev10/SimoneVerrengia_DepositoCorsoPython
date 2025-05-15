class Cerchio:
    def disegna(self):
        print("Disegno un cerchio")

class Rettangolo:
    def disegna(self):
        print("Disegno un rettangolo")

def disegna_figura(figura):
# Anche qui, basta che 'figura' abbia il metodo 'disegna'
    figura.disegna()

figure = [Cerchio(), Rettangolo()]
# figure[0]=Cerchio() / figure[1]=Rettagolo()

# Iteriamo e disegniamo ogni figura
for figura in figure:
    disegna_figura(figura)