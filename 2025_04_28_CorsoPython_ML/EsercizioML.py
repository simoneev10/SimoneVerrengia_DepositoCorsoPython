import pandas as pd
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Inizio caricando il famoso dataset Iris come un pratico DataFrame
iris_data = load_iris(as_frame=True)
df_iris = iris_data.frame
features = iris_data.data
target = iris_data.target

# Ora mi occupo di rendere le caratteristiche comparabili tra loro, standardizzandole
standardizzatore = StandardScaler()
features_standardizzate = standardizzatore.fit_transform(features)
features_standardizzate_df = pd.DataFrame(features_standardizzate, columns=features.columns)

# Adesso è il momento di separare i dati in due gruppi distinti: uno per l'train del modello e l'altro per verificarne l'efficacia
X_train, X_test, y_train, y_test = train_test_split(features_standardizzate_df, target, test_size=0.3, random_state=69)

# Con i dati pronti, posso istruire il mio classificatore ad albero decisionale
classificatore_albero = DecisionTreeClassifier(random_state=69)
classificatore_albero.fit(X_train, y_train)
previsioni = classificatore_albero.predict(X_test)

# Voglio capire quanto bene il mio modello ha imparato, quindi genero un report di classificazione
print("Ecco il resoconto delle performance del mio modello:")
print(classification_report(y_test, previsioni, target_names=iris_data.target_names))

# Infine, per avere una visione chiara di dove il modello ha fatto centro e dove ha sbagliato, visualizzo la matrice di confusione
matrice_confusione = confusion_matrix(y_test, previsioni)
plt.figure(figsize=(8, 6))
sns.heatmap(matrice_confusione, annot=True, fmt='d', cmap='Blues',
            xticklabels=iris_data.target_names, yticklabels=iris_data.target_names)
plt.xlabel('Etichetta Predetta')
plt.ylabel('Etichetta Reale')
plt.title('Come si è comportato il mio classificatore?')
plt.show()