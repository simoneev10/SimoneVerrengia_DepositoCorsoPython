#Tuple
punto = (3,4)
colore_rgb = (255, 128, 0)
informazioni_persona = ("Simone", 27, "Maschio")
print(informazioni_persona)
informazioni_persona = ("Franco", 30, "Maschio")
print(informazioni_persona)

#Insiemi
set1 = set([1, 2, 3, 4, 5])
set2 = {4, 5, 6, 7, 8}
#Non contengono elementi duplicati
set3 = {9, 10, 1, 2, 3, 4, 4, 4, 5, 6, 7, 8} #Attenzione non ordina secondo l'inserimento ma tramite grandezza
print(set3)

#Operazioni sui set
print(set1.union(set2))
print(set1.intersection(set2))
print(set1.difference(set2))
print(set1.symmetric_difference(set2))