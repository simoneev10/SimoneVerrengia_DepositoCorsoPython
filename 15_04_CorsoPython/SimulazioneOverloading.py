class Stampa:
    def mostra(self, a=None, b=None):
        if a is not None and b is not None:
            print(a + b)
        elif a is not None:
            print(a)
        else:
            print("Niente da mostrare")

s = Stampa()
s.mostra(5)
s.mostra(7,8)