# stringa = input("Inserisci una stringa: ")
# cont = {}

# for carattere in stringa: #Scorro la lista per carattere
#     if carattere in cont: #Se presente aumento il conteggio di ogni carattere
#         cont[carattere] += 1
#     else:
#         cont[carattere] = 1 #Altrimenti crea l'occorrenza 

# print(cont)  
    
stringa = "banana"
lista = list(stringa)
dizi = {}

for i in lista:
    dizi.setdefault(i, lista.count(i))

print(dizi)