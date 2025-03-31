#Punto 1: Utilizzo di if
numero = int(input("Inserisci un numero: "))
#controllo se il numero è pari
if numero % 2 == 0:
    print("Il numero", numero, "è pari!")
else:
    print("Il numero", numero, " è dispari!")
    


#Punto 2: Utilizzo di while e range
numero = int(input("Inserisci un numero: "))
#Finche la condizione è vera diminuisco di un'unità il mio numero
while numero >= 0:
    print(numero)
    numero = numero - 1

#Punto 3: Utilizzo di for
numeri = []
size = int(input("Quanti numeri vuoi inserire? "))
#Inserimento da tastiera dei numeri
for n in range(size):
    num= int(input("Inserisci numero: "))
    numeri.append(num)
#Stampa dei numeri inseriti e dei numeri al quadrato
print("Numeri inseriti: ", numeri)
for n in numeri:
    print("Numeri al quadrato: ", n**2)