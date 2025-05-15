# def decoratore(funzione):
#     def wrapper():
#         print("Prima dell'esecuzione della funzione")
#         funzione()
#         print("Dopo l'esecuzione della funzione")
#     return wrapper

# @decoratore
# def saluta():
#     print("Ciao!")


# saluta()

def decoratore_con_argomenti(funzione):
    def wrapper(*args, **kwargs):
        print("Prima")
        risultato = funzione(*args,**kwargs)
        print("Dopo")
        return risultato + 2
    return wrapper

@decoratore_con_argomenti
def somma(a,b):
    print(a+b)
    return a + b

print("Il risultato è:", somma(3,4))



def logger(funzione):
    def wrapper(*args, **kwargs):
        print(f"Chiamata a {funzione.__name__} con argomenti: {args} e {kwargs}")
        risultato = funzione(*args, **kwargs)
        print(f"Risultato di {funzione.__name__}: {risultato}")
        return risultato
    return wrapper

@logger
def moltiplica(a, b):
    return a * b

# Chiamata alla funzione decorata
print(moltiplica(3, 4))