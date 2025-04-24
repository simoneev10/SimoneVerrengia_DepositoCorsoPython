import seaborn as sns
import matplotlib.pyplot as plt

# Dati di esempio
x = [1, 2, 3, 4, 5]
y1 = [2, 3, 5, 7, 11]
y2 = [1, 4, 6, 8, 9]

sns.set_theme(style="whitegrid", palette="muted")

plt.figure(figsize=(6, 4))
# Tracciamo entrambe le serie specificando un'etichetta e uno stile di marker
sns.lineplot(x=x, y=y1, marker="o", label="Serie 1")
sns.lineplot(x=x, y=y2, marker="s", label="Serie 2")

plt.title("Confronto Serie 1 e Serie 2 con seaborn")
plt.xlabel("Indice")
plt.ylabel("Valore")
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()
