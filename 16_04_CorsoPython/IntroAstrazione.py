from abc import ABC, abstractmethod

class Animale(ABC):
    @abstractmethod
    def muovi(self):
        pass
    
class Cane(Animale):
    def muovi(self):
        print("Corrooo!")
        
class Pesce(Animale):
    def muovi(self):
        print("Nuotooo!")
        
c = Cane()
c.muovi()
p = Pesce()
p.muovi()