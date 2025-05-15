class Animale:
    def emetti_suono(self):
        print("Animale emette suono")
        
class Cane:
    def emetti_suono(self):
        return "BAU!"
        
class Gatto:
    def emetti_suono(self):
        return "MIAO!"
        
def fai_parlare(animale):
    # Non importa di che tipo sia l'animale
    print(animale.emetti_suono())
    
cane = Cane()
gatto = Gatto()

fai_parlare(cane)
fai_parlare(gatto)