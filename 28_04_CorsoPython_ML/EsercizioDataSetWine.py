from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Carico il dataset Wine
data_wine = load_wine()
X = data_wine.data
y = data_wine.target
feature_names = data_wine.feature_names
target_names = data_wine.target_names

# Creo un DataFrame per una migliore gestione
df_wine = pd.DataFrame(X, columns=feature_names)
df_wine['target'] = y

df_wine.info()
print(df_wine.head())

print("\nNumero di campioni per ciascuna classe: ")
print(df_wine['target'].value_counts())

# Calcola le statistiche di base delle feature
print("\nStatistiche di base delle feature:")
print(df_wine.describe())

# Grafico a barre per vedere distribuzione delle classi
plt.figure(figsize=(8,6))
sns.countplot(x='target', data=df_wine, palette='viridis')
plt.title('Distribuzione delle Classi nel Dataset Wine')
plt.xlabel('Classi')
plt.ylabel('Numero Campioni')
plt.show()

# Adesso riduco la dimensionalità tramite PCA
# prima però applico standardizzazione

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Creo DataFrame per i dati PCA
df_pca = pd.DataFrame(data=X_pca, columns=['PC1','PC2'])
df_pca['target'] = y

print("\nPrime 5 righe dei dati dopo PCA:")
print(df_pca.head())

print("\nVarianza spiegata da ciascun componente principale:")
print(pca.explained_variance_ratio_)

# Visualizzazione grafico Scatter 2D
plt.figure(figsize=(8,6))
scatter = plt.scatter(df_pca['PC1'], df_pca['PC2'], c=df_pca['target'])
plt.xlabel('Componente principale PC1')
plt.ylabel('Componente principale PC2')
plt.title('Rappresentazione 2D dei dati dopo PCA')
plt.grid(True)
plt.show()

# Suddivido dati in training e test set
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=73)

# Applico random forest
rf_classifier = RandomForestClassifier()
rf_classifier.fit(X_train, y_train)
predizioniTree = rf_classifier.predict(X_test)

# Valuta la performance del modello
print("\nValutazione della Performance del Modello RandomForest:")
print(f"Accuracy: {accuracy_score(y_test, predizioniTree):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, predizioniTree, target_names=target_names))

# Visualizza la matrice di confusione
cm = confusion_matrix(y_test, predizioniTree)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=target_names, yticklabels=target_names)
plt.xlabel('Etichetta Predetta')
plt.ylabel('Etichetta Reale')
plt.title('Matrice di Confusione - RandomForestClassifier')
plt.show()

# Visualizzo importanza features
importanza = rf_classifier.feature_importances_
indici = np.argsort(importanza)[::-1]

plt.figure(figsize=(10, 6))
plt.title("Importanza delle Feature secondo RandomForest")
plt.bar(range(X_train.shape[1]), importanza[indici],
        color="y", align="center")
plt.xticks(range(X_train.shape[1]), [feature_names[i] for i in indici], rotation=90)
plt.xlim([-1, X_train.shape[1]])
plt.tight_layout()
plt.show()

# Ottimizza l'algoritmo utilizzando GridSearchCV
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 5, 10],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 3, 5]
}

grid_search = GridSearchCV(estimator=rf_classifier, param_grid=param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Migliori parametri trovati
print("\nMigliori Parametri trovati con GridSearchCV:")
print(grid_search.best_params_)

# Miglior modello
best_rf_classifier = grid_search.best_estimator_

# Valuta il miglior modello sul set di test
y_pred_best = best_rf_classifier.predict(X_test)

print("\nValutazione della Performance del Modello RandomForest Ottimizzato:")
print(f"Accuracy (Miglior Modello): {accuracy_score(y_test, y_pred_best):.4f}")
print("\nClassification Report (Miglior Modello):")
print(classification_report(y_test, y_pred_best, target_names=target_names))

# Visualizza la matrice di confusione per il miglior modello
cm_best = confusion_matrix(y_test, y_pred_best)
plt.figure(figsize=(8, 6))
sns.heatmap(cm_best, annot=True, fmt='d', cmap='Greens',
            xticklabels=target_names, yticklabels=target_names)
plt.xlabel('Etichetta Predetta')
plt.ylabel('Etichetta Reale')
plt.title('Matrice di Confusione - RandomForestClassifier (Ottimizzato)')
plt.show()

# Visualizza l'importanza delle feature per il miglior modello
importances_best = best_rf_classifier.feature_importances_
indices_best = np.argsort(importances_best)[::-1]

plt.figure(figsize=(10, 6))
plt.title("Importanza delle Feature secondo RandomForest (Ottimizzato)")
plt.bar(range(X_train.shape[1]), importances_best[indices_best],
        color="g", align="center")
plt.xticks(range(X_train.shape[1]), [feature_names[i] for i in indices_best], rotation=90)
plt.xlim([-1, X_train.shape[1]])
plt.tight_layout()
plt.show()