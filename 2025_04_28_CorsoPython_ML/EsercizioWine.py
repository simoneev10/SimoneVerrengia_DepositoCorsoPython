import pandas as pd
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Carico il dataset Wine come un DataFrame di Pandas per una facile manipolazione
wine = load_wine()

# Estraggo le caratteristiche (X) e la variabile target (y) dal DataFrame
X = wine.data
y = wine.target

df = pd.DataFrame(wine.data, columns=wine.feature_names)
df['target'] = wine.target
df.info()
print(df.head())

# Inizializzo lo StandardScaler per standardizzare le caratteristiche
standardizzazione = StandardScaler()
features_standardizzate = standardizzazione.fit_transform(X)

# Divido il dataset in set di training e test. Il 70% dei dati sarà usato per l'allenamento e il 30% per la valutazione.
X_train, X_test, y_train, y_test = train_test_split(features_standardizzate, y, test_size=0.3, random_state=73)

# Creo un'istanza del classificatore ad albero decisionale
tree_class = DecisionTreeClassifier(random_state=73) # 'random_state' qui assicura la riproducibilità dell'albero

# Addestro il modello utilizzando i dati di training
tree_class.fit(X_train, y_train)

# Eseguo le previsioni sul set di test
previsione = tree_class.predict(X_test)

# Stampo il report di classificazione per valutare le prestazioni del modello
# Il report include precisione, recall, F1-score e supporto per ciascuna classe di vino
print("Il mio classification report: ")
print(classification_report(y_test, previsione, target_names=wine.target_names))

# Calcolo la matrice di confusione per visualizzare le prestazioni del classificatore
# La matrice mostra il numero di previsioni corrette e scorrette per ogni classe
matrice_confusione = confusion_matrix(y_test, previsione)

# Visualizzo la matrice di confusione utilizzando una heatmap di seaborn
plt.figure(figsize=(8, 6))
sns.heatmap(matrice_confusione, annot=True, fmt='d', cmap='Blues',
            xticklabels=wine.target_names, yticklabels=wine.target_names)
plt.xlabel('Etichetta Predetta')
plt.ylabel('Etichetta Reale')
plt.title('Come si è comportato il mio classificatore?')
plt.show()