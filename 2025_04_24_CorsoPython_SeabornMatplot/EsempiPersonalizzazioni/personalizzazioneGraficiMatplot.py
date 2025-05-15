import matplotlib.pyplot as plt

# Dati di esempio
x = [1, 2, 3, 4, 5]
y1 = [2, 3, 5, 7, 11]    # serie 1
y2 = [1, 4, 6, 8, 9]     # serie 2

plt.figure(figsize=(6, 4))

# Serie 1: linea rossa tratteggiata con marker a cerchio
plt.plot(x, y1,
         color='red',          # colore linea
         linestyle='--',       # stile linea (tratteggiata)
         marker='o',           # marker a cerchio
         label='Serie 1')      # etichetta per la legenda

# Serie 2: linea blu continua con marker a quadrato
plt.plot(x, y2,
         color='blue',
         linestyle='-',
         marker='s',           # marker a quadrato
         label='Serie 2')

plt.title("Confronto Serie 1 e Serie 2")
plt.xlabel("Indice")
plt.ylabel("Valore")
plt.legend(loc='upper left')   # posiziona la legenda in alto a sinistra
plt.grid(linestyle=':')         # griglia punteggiata
plt.tight_layout()              # ottimizza spaziatura
plt.show()