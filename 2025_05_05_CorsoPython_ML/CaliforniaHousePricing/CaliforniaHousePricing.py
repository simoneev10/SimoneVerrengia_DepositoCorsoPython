import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error, r2_score
from pandas.plotting import scatter_matrix
from sklearn.metrics.pairwise import rbf_kernel


# 1. Caricamento del Dataset
california = fetch_california_housing(as_frame=True)
housing = california.frame.copy()
housing.columns = [col.capitalize() for col in housing.columns]  # Capitalizza i nomi delle colonne

# 2. Esplorazione Iniziale dei Dati
print("="*30)
print("Esplorazione Iniziale dei Dati")
print("="*30)

print("\nPrime 5 righe del dataset:")
print(housing.head())

print("\nInformazioni sul dataset:")
housing.info()

print("\nStatistiche descrittive del dataset:")
print(housing.describe())

# Visualizzazione della distribuzione del reddito mediano
plt.figure(figsize=(10, 4))
housing["Medinc"].hist(bins=50)
plt.title("Distribuzione del Reddito Mediano")
plt.xlabel("Reddito Mediano")
plt.ylabel("Frequenza")
plt.show()

# Visualizzazione degli istogrammi di tutte le variabili numeriche
housing.hist(bins=50, figsize=(12, 8))
plt.tight_layout()
plt.show()

# Visualizzazione geografica dei distretti
plt.figure(figsize=(8, 6))
plt.scatter(housing["Longitude"], housing["Latitude"])
plt.title("Distribuzione geografica dei distretti")
plt.xlabel("Longitudine")
plt.ylabel("Latitudine")
plt.grid(True)
plt.show()

# Visualizzazione geografica con densità evidenziata
plt.figure(figsize=(8, 6))
plt.scatter(housing["Longitude"], housing["Latitude"], alpha=0.2)
plt.title("Distribuzione geografica con densità evidenziata")
plt.xlabel("Longitudine")
plt.ylabel("Latitudine")
plt.grid(True)
plt.show()

# Visualizzazione con prezzo e popolazione
plt.figure(figsize=(10, 7))
scatter = plt.scatter(housing["Longitude"], housing["Latitude"],
                    s=housing["Population"] / 100,  # dimensione
                    c=housing["Medhouseval"], cmap="jet",  # colore
                    alpha=0.4)
plt.colorbar(scatter, label="Prezzo medio")
plt.xlabel("Longitudine")
plt.ylabel("Latitudine")
plt.title("Prezzi delle case in funzione della posizione e densità")
plt.legend(*scatter.legend_elements(prop="sizes", num=6, fmt="{x:.2f}"), title="Popolazione (scala)")
plt.grid(True)
plt.show()

# Calcolo della matrice di correlazione
corr_matrix = housing.corr(numeric_only=True)
print("\nCorrelazione con MedHouseVal (ordinata):")
print(corr_matrix["Medhouseval"].sort_values(ascending=False))

# Scatter matrix tra variabili selezionate
attribs = ["Medhouseval", "Medinc", "Averooms", "Houseage"]
scatter_matrix(housing[attribs], figsize=(12, 8))
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

# Identificazione delle colonne numeriche
housing_num = housing_features.select_dtypes(include=np.number)
num_cols = housing_num.columns

# Imputazione dei valori mancanti (anche se non presenti)
imputer = SimpleImputer(strategy="median")
housing_imputed = imputer.fit_transform(housing_num)
housing_imputed_df = pd.DataFrame(housing_imputed, columns=num_cols, index=housing_num.index)

# Standardizzazione delle features numeriche
scaler = StandardScaler()
housing_scaled = scaler.fit_transform(housing_imputed_df)
housing_prepared = pd.DataFrame(housing_scaled, columns=num_cols, index=housing_imputed_df.index)

print("\nDataFrame preparato (dopo imputazione e standardizzazione):")
print(housing_prepared.head())

# 5. Trasformazioni Aggiuntive (esempio RBF su ‘Houseage’)
print("\n"+"="*30)
print("Trasformazioni Aggiuntive")
print("="*30)

rbf_transformer = FunctionTransformer(
    rbf_kernel, kw_args=dict(Y=[[35.]], gamma=0.1))
houseage_rbf = rbf_transformer.transform(housing_prepared[["Houseage"]])
print("\nFeature 'Houseage' trasformata con RBF:")
print(pd.DataFrame(houseage_rbf, index=housing_prepared.index).head())

# 6. Clustering Geografico (KMeans)
print("\n"+"="*30)
print("Clustering Geografico (KMeans)")
print("="*30)

geo_features_train = housing_features[["Latitude", "Longitude"]]
kmeans = KMeans(n_clusters=10, random_state=42, n_init=10) # Aggiunto n_init per evitare FutureWarning
housing_features["Cluster"] = kmeans.fit_predict(geo_features_train)

plt.figure(figsize=(10, 7))
plt.scatter(housing_features["Longitude"], housing_features["Latitude"], c=housing_features["Cluster"],
            cmap="tab10", s=10, alpha=0.6)
plt.colorbar(label="Cluster")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Cluster Geografici dei Distretti (KMeans) sul Training Set")
plt.grid(True)
plt.show()

# 7. Addestramento e Valutazione dei Modelli
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
    preds = cross_val_predict(model, housing_prepared, housing_labels, cv=3)
    rmse = root_mean_squared_error(housing_labels, preds)
    r2 = r2_score(housing_labels, preds)
    print(f"{name}: RMSE = {rmse:.2f}, R² = {r2:.4f}")