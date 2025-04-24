import matplotlib.pyplot as plt
import numpy as np

# Modifichiamo i parametri globali di matplotlib
plt.rcParams['font.size'] = 12         # dimensione font di default
plt.rcParams['font.family'] = 'serif'  # famiglia di font
plt.rcParams['axes.titlesize'] = 14    # dimensione del titolo degli assi
plt.rcParams['axes.labelsize'] = 12    # dimensione delle etichette degli assi
plt.rcParams['lines.linewidth'] = 2    # spessore linea di default
plt.rcParams['lines.markersize'] = 8   # dimensione marker di default

# Dati di esempio
x = np.linspace(0, 4*np.pi, 100)
y = np.sin(x) * np.exp(-x/10)

plt.figure(figsize=(7,4))
plt.plot(x, y, marker='D', label='sin(x)·exp(-x/10)')
plt.title("Damping della sinusoide")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()
