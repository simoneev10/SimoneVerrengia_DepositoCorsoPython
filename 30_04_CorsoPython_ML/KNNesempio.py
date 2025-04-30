from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Carica il dataset
iris = load_iris()
X, y = iris.data, iris.target
target_names = iris.target_names

# 2. Suddivisione train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 3. Ciclo su diversi valori di k
neighbors_list = [1, 3, 7, 9]

for k in neighbors_list:
    print(f"\n K = {k}")
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    print("Accuracy:", acc)
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Matrice di confusione
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, cmap='Blues', xticklabels=target_names, yticklabels=target_names)
    plt.title(f'Confusion Matrix (k={k})')
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.show()

# 4. Visualizzazione finale (usando l'ultimo modello KNN)
pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

plt.figure(figsize=(8,6))
for i, target_name in enumerate(target_names):
    plt.scatter(X_reduced[y == i, 0], X_reduced[y == i, 1], label=target_name)

plt.title(f'Iris Dataset - PCA Projection (final model k={k})')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.legend()
plt.grid(True)
plt.show()
