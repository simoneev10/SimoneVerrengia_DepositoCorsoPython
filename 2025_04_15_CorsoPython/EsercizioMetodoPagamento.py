class MetodoPagamento:
    def effettua_pagamento(self, importo):
        print("Si pagaaa!")
        
class CartaDiCredito:
    def effettua_pagamento(self, importo):
        #pin = int(input("Inserisci PIN: "))
        print(f"Pagamento di {importo} tramite carta di credito in esecuzione . . .")

class Paypal:
    def effettua_pagamento(self, importo):
        print(f"Pagamento di {importo} tramite PayPal in esecuzione . . .")
        
class BonificoBancario:
    def effettua_pagamento(self, importo):
        print(f"Pagamento di {importo} tramite Bonifico Bancario in esecuzione . . .")
        
class GestorePagamenti:
    def fai_pagare(self, metodo_pagamento,importo):
        metodo_pagamento.effettua_pagamento(importo)

gp = GestorePagamenti()        
cdc = CartaDiCredito()
pp = Paypal()
bb = BonificoBancario()

gp.fai_pagare(cdc, 10)
gp.fai_pagare(pp, 20)
gp.fai_pagare(bb, 100)