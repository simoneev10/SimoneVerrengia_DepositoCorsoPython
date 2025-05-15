# Variabile globale
numero = 10

def funzione_esterna():
    numero = 5
    print(f"Numero dentro funzione esterna (locale): {numero}")
    
    def funzione_interna():
        nonlocal numero
        numero = 3
        print(f"Numero dentro funzione interna (non locale): {numero}")
        
    funzione_interna()
    
print(f"Numero nel main (globale): {numero}")
funzione_esterna()
print(f"Numero nel main dopo chiamata (globale non cambiato): {numero}")