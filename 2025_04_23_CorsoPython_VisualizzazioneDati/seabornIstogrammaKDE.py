import seaborn as sns
import matplotlib.pyplot as plt

# Generare dati casuali
data = sns.load_dataset("penguins")

# Creare un istogramma con KDE
sns.histplot(data=data, x="flipper_length_mm", kde=True)
plt.title("Distribuzione Lunghezza Pinne dei Pinguini")
plt.show()