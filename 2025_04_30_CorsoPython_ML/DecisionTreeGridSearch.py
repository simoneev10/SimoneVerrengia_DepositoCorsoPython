import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score

# Carichiamo il dataset degli iris
iris = load_iris()
X = iris.data
y = iris.target

# Dividiamo in training e test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=73)

# Visualizzo bene quali sono i dati di Iris
df_iris = pd.DataFrame(iris.data, columns=iris.feature_names)
print(df_iris.head(5))

# Definiamo i parametri da cercare
param_grid = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [2, 3, 4, 5, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [2, 3, 4, 6, 8]
}

# Creiamo il classificatore base
dt = DecisionTreeClassifier(random_state=73)

# Applichiamo la GridSearch con cross-validation
grid_search = GridSearchCV(estimator=dt, param_grid=param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Miglior modello
best_tree = grid_search.best_estimator_

# Valutiamo sul test set
y_pred = best_tree.predict(X_test)
print("Best Parameters:", grid_search.best_params_)
print("Test Accuracy:", accuracy_score(y_test, y_pred))

# Visualizziamo l'albero decisionale ottimizzato
plt.figure(figsize=(12, 6))
plot_tree(best_tree, 
          feature_names=iris.feature_names, 
          class_names=iris.target_names, 
          filled=True)
plt.title("Decision Tree Classifier - Miglior modello con GridSearch")
plt.show()
