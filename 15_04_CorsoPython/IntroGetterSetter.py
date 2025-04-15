class Computer:
    def __init__(self):
        self.__processore = "Intel i5" # Attributo privato
        
    def get_processore(self):
        return self.__processore
    
    def set_processore(self, processore):
        self.__processore = processore
        
pc = Computer()
print(pc)
print(pc.get_processore()) # Per stampare devo usare il getter altrimenti non posso accedere al dato poiché dichirato privato
pc.set_processore("AMD Ryzen 5") # Setter per modificare l'attributo processore
print(pc.get_processore())