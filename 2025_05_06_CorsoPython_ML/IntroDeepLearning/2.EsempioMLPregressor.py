from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import numpy as np

# Caricamento del dataset
housing = fetch_california_housing()
X = housing.data
y = housing.target

# Suddivisione in training, validation e test
X_train_full, X_test, y_train_full, y_test = train_test_split(X, y, random_state=42)
X_train, X_valid, y_train, y_valid = train_test_split(X_train_full, y_train_full, random_state=42)

# Definizione del modello: 3 hidden layer con 50 neuroni ciascuno
mlp_reg = MLPRegressor(hidden_layer_sizes=[50, 50, 50], 
                       activation='relu', 
                       solver='adam', 
                       alpha=0.0001,
                       max_iter=500,
                       random_state=42)

# Creazione della pipeline con normalizzazione
pipeline = make_pipeline(StandardScaler(), mlp_reg)

# Addestramento del modello
pipeline.fit(X_train, y_train)

# Predizione e valutazione su validation set
y_pred = pipeline.predict(X_valid)
rmse = np.sqrt(mean_squared_error(y_valid,y_pred))

print(f"Root Mean Squared Error (Validation): {rmse:.3f}")