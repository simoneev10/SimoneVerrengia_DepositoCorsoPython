def scrittura(stringa,metodo):
    with open("prova.txt",metodo) as file:
        file.write(stringa)

scrittura("nuova","w")