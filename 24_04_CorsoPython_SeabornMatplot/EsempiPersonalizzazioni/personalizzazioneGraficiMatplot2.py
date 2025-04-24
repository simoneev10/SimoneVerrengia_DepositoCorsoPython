import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(0, 2*np.pi, 200)

# Creiamo una figura con 2 righe e 1 colonna di subplot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

# Primo subplot: seno
ax1.plot(t, np.sin(t), color='purple')
ax1.set_title("Funzione seno")
ax1.grid(True)

# Secondo subplot: coseno
ax2.plot(t, np.cos(t), color='green')
ax2.set_title("Funzione coseno")
ax2.set_xlabel("Angolo (rad)")
ax2.grid(True)

plt.tight_layout()
plt.show()