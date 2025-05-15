from abc import ABC, abstractmethod

class Impiegato(ABC):
    @abstractmethod
    def __init__(self, nome, cognome, stipendioBase):
        pass
    
    @abstractmethod
    def calcola_stipendio(self):
        pass
    
class ImpiegatoFisso(Impiegato):
    def __init__(self, nome, cognome, stipendioBase):
        super().__init__(nome, cognome, stipendioBase)
        self.__admin = False
        
    def get_admin(self):
        return self.__admin
    
    def set_admin(self, admin):
        self.__admin = admin
        
class ImpiegatoAProvvigione(Impiegato):
    def __init__(self, nome, cognome, stipendioBase, bonus):
        super().__init__(nome, cognome, stipendioBase)
        self.__bonus = bonus
        
    def get_bonus(self):
        return self.__bonus
    
    def set_bonus(self, bonus):
        self.__bonus = bonus
    
    def imposta_bonus(self):
        bonusVendite = int(input(f"Quante vendite ha effettuato {self.nome}"))
        for i in range(bonusVendite):
            self.set_bonus += 10

def crea_admin(ImpiegatoFisso):
    admin = ImpiegatoFisso.get_admin()
    
    if not admin:
        ImpiegatoFisso.set_admin(True)
        
def aggiungi_impiegato(self, ImpiegatoFisso):
    admin = ImpiegatoFisso.get_admin()
    
    if not admin:
        print("\nNon sei l'admin non puoi aggiungere impiegati!")
        return
    else:
        scelta = int(input("Che tipologia di impiegato vuoi aggiungere?"))
        nome = input("nome")
        cognome = input("cognome")
        stipendiobase = 1500
        match scelta:
            case "1":
                impbase = ImpiegatoFisso(nome, cognome, stipendiobase)
            case "2":
                vendite = input("Quante vendite ha fatto?")
                impAprovv = ImpiegatoAProvvigione(nome, cognome, stipendioBase, vendite)
            # case _:
            #     break
            


                
    