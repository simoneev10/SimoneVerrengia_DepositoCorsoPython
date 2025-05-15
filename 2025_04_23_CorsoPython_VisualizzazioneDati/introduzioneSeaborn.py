import matplotlib.pyplot as plt
import seaborn as sns

# Dati di esempio
tips = sns.load_dataset("tips")

# Creare un grafico a barre
sns.barplot(x="day", y="total_bill", data=tips)
plt.title('Conto totale per giorno')
plt.show()