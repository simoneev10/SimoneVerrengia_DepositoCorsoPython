from abc import ABC, abstractmethod

class Forma(ABC):
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimetro(self):
        pass
    
class Rettangolo(Forma):
    def __init__(self, larghezza, altezza):
        self.larghezza = larghezza
        self.altezza = altezza
        
    def area(self):
        return self.larghezza * self.altezza
    
    def perimetro(self):
        return 2 * (self.larghezza + self.altezza)
    
# f = Forma() - TypeError: Can't instantiate abstract class Forma without an implementation for abstract methods 'area', 'perimetro'
r = Rettangolo(5,10)
print(r.area())
print(r.perimetro())
        
    