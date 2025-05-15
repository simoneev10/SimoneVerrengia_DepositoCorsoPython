import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split

# Carichiamo il dataset degli iris
iris = load_iris()
X = iris.data#[:, :2]  # Usiamo solo le prime due feature per semplicità di visualizzazione
y = iris.target

# X, y = make_classification(n_samples=100, n_features=2, 
#                            n_informative=2, n_redundant=0, 
#                            n_repeated=0, n_classes=2, random_state=42)

# Dividiamo in training e test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=73)

# Creiamo il modello Decision Tree
tree = DecisionTreeClassifier(max_depth=3, criterion="gini", random_state=73)
tree.fit(X_train, y_train)

# Visualizziamo l'albero decisionale
plt.figure(figsize=(12, 6))
plot_tree(tree, 
          feature_names=iris.feature_names,#[:2], 
          class_names=iris.target_names, 
          filled=True)
plt.title("Decision Tree Classifier (Gini Impurity) - Dataset Iris")
plt.show()

#plot_tree(tree, feature_names=iris.feature_names, class_names=["Setosa", "Versicolor", "Virginica"], filled=True)
