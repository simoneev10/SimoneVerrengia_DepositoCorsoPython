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