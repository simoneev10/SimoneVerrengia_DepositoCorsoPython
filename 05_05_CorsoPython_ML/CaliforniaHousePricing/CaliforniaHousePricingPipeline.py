import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error, r2_score
from pandas.plotting import scatter_matrix
from sklearn.cluster import KMeans

# 1. Caricamento del Dataset
california = fetch_california_housing(as_frame=True)
housing = california.frame.copy()
housing.columns = [col.capitalize() for col in housing.columns]

# 2. Esplorazione Iniziale dei Dati (ridotta)
print("="*30)
print("Esplorazione Iniziale dei Dati (ridotta)")
print("="*30)

print("\nPrime 5 righe del dataset:")
print(housing.head())

print("\nInformazioni sul dataset:")
housing.info()

# Visualizzazione della distribuzione del reddito mediano
plt.figure(figsize=(8, 4))
housing["Medinc"].hist(bins=30)
plt.title("Distribuzione del Reddito Mediano")
plt.xlabel("Reddito Mediano")
plt.ylabel("Frequenza")
plt.show()

# Visualizzazione geografica con densità evidenziata (ridotta alpha)
plt.figure(figsize=(8, 6))
plt.scatter(housing["Longitude"], housing["Latitude"], alpha=0.1)
plt.title("Distribuzione geografica con densità evidenziata")
plt.xlabel("Longitudine")
plt.ylabel("Latitudine")
plt.grid(True)
plt.show()

# Calcolo della matrice di correlazione
corr_matrix = housing.corr(numeric_only=True)
print("\nCorrelazione con MedHouseVal (ordinata):")
print(corr_matrix["Medhouseval"].sort_values(ascending=False))

# Scatter matrix tra variabili selezionate (ridotta)
attribs = ["Medhouseval", "Medinc", "Averooms"]
scatter_matrix(housing[attribs], figsize=(8, 6))
plt.suptitle("Matrice di scatterplot tra variabili selezionate", y=1.02)
plt.show()

# Scatter mirato: MedInc vs MedHouseVal
plt.figure(figsize=(8, 6))
plt.scatter(housing["Medinc"], housing["Medhouseval"], alpha=0.1)
plt.title("Relazione tra reddito mediano e valore medio delle case")
plt.xlabel("Reddito Mediano")
plt.ylabel("Valore Medio delle Case")
plt.grid(True)
plt.show()

# 3. Creazione di Attributi Combinati
print("\n"+"="*30)
print("Feature Engineering")
print("="*30)

housing["rooms_per_person"] = housing["Averooms"] / housing["Aveoccup"]
housing["bedrooms_per_room"] = housing["Avebedrms"] / housing["Averooms"]
housing["population_per_household"] = housing["Population"] / housing["Houseage"]

# Nuova matrice di correlazione
corr_matrix = housing.corr(numeric_only=True)
print("\nNuova correlazione con MedHouseVal (con attributi combinati):")
print(corr_matrix["Medhouseval"].sort_values(ascending=False))

# 4. Preparazione dei Dati per l’Addestramento
print("\n"+"="*30)
print("Preparazione dei Dati per l'Addestramento")
print("="*30)

# Divisione in training set e test set con campionamento stratificato
housing["IncomeCat"] = pd.cut(housing["Medinc"],
                                     bins=[0., 1.5, 3.0, 4.5, 6., np.inf],
                                     labels=[1, 2, 3, 4, 5])
train_set, test_set = train_test_split(
    housing, test_size=0.2, random_state=42,
    stratify=housing["IncomeCat"]
)
for dataset in (train_set, test_set):
    dataset.drop("IncomeCat", axis=1, inplace=True)

housing_labels = train_set["Medhouseval"].copy()
housing_features = train_set.drop("Medhouseval", axis=1)

# Pipeline di preprocessing per attributi numerici
num_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("std_scaler", StandardScaler()),
])
housing_prepared = num_pipeline.fit_transform(housing_features)

housing_prepared_df = pd.DataFrame(housing_prepared, columns=housing_features.columns, index=housing_features.index)
print("\nDataFrame preparato (dopo l'imputazione e la standardizzazione):")
print(housing_prepared_df.head())

# 5. Clustering Geografico (KMeans)
print("\n"+"="*30)
print("Clustering Geografico (KMeans)")
print("="*30)

geo_features_train = housing_features[["Latitude", "Longitude"]]
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10) # Ridotto il numero di cluster
housing_features["Cluster"] = kmeans.fit_predict(geo_features_train)

plt.figure(figsize=(8, 6))
plt.scatter(housing_features["Longitude"], housing_features["Latitude"], c=housing_features["Cluster"],
            cmap="tab10", s=10, alpha=0.4) # Ridotta l'alpha
plt.colorbar(label="Cluster")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Cluster Geografici dei Distretti (KMeans) sul Training Set")
plt.grid(True)
plt.show()

# 6. Addestramento e Valutazione dei Modelli
print("\n"+"="*30)
print("Addestramento e Valutazione dei Modelli")
print("="*30)

models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(random_state=42),
    "Random Forest": RandomForestRegressor(random_state=42)
}

print("\nRisultati modelli (cross-validated sul training set):")
for name, model in models.items():
    preds = cross_val_predict(model, housing_prepared, housing_labels, cv=5)
    rmse = root_mean_squared_error(housing_labels, preds)
    r2 = r2_score(housing_labels, preds)
    print(f"{name}: RMSE = {rmse:.2f}, R² = {r2:.4f}")