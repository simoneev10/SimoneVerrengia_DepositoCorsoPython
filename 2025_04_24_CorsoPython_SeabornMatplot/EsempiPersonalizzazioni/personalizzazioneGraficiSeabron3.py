import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# Definiamo tema, font e palette
sns.set_theme(
    context="talk",            # dimensione del font pensata per presentazioni
    style="whitegrid",         # griglia chiara
    palette="coolwarm",        # palette dei colori
    font="serif",              # famiglia di font
    rc={                        # parametri rc aggiuntivi
        "axes.titlesize": 16,
        "axes.labelsize": 14,
        "lines.linewidth": 2,
        "lines.markersize": 8
    }
)

# Dati di esempio
x = np.linspace(0, 4*np.pi, 100)
y = np.sin(x) * np.exp(-x/10)

plt.figure(figsize=(7, 4))
sns.lineplot(x=x, y=y, marker="D", label="sin(x)·exp(-x/10)")
plt.title("Damping della sinusoide con seaborn")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()
