import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# Dati 2D di esempio
X, Y = np.meshgrid(np.linspace(0, 1, 30), np.linspace(0, 1, 30))
Z = np.sin(X * np.pi) * np.cos(Y * np.pi)

sns.set_theme(style="dark")
plt.figure(figsize=(6, 5))
# Creiamo una heatmap con barra colore integrata
sns.heatmap(Z, 
            cmap="viridis",      # mappa dei colori
            cbar_kws={"label": "Intensità"},
            square=True,         # caselle quadrate
            xticklabels=5,       # mostra un tick ogni 5
            yticklabels=5)
plt.title("Heatmap di esempio con seaborn")
plt.xlabel("Asse X")
plt.ylabel("Asse Y")
plt.show()