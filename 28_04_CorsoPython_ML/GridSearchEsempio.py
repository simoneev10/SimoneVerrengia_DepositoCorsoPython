from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier

# Carico il dataset Wine come un DataFrame di Pandas per una facile manipolazione
wine = load_wine()

# Estraggo le caratteristiche (X) e la variabile target (y) dal DataFrame
X = wine.data
y = wine.target

# Divido il dataset in set di training e test. Il 70% dei dati sarà usato per l'allenamento e il 30% per la valutazione.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

param_grid = {'max_depth':[3,5,7], 'criterion':['gini','entropy']}
# grid_search = GridSearchCV(DecisionTreeClassifier(), param_grid, cv=5) base
grid_search = GridSearchCV(DecisionTreeClassifier(), param_grid,cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42))
# la seconda grid_search sevre per "standardizzare", se per esemoio vogliamo gli stessi ris nel gruppo di lavoro
grid_search.fit(X_train, y_train)
print(f"Migliori parametri: {grid_search.best_params_}")
