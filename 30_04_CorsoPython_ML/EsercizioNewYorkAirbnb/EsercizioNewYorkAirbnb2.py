import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.model_selection import ParameterGrid
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.stats.outliers_influence import variance_inflation_factor
import xgboost as xgb
import warnings
from sklearn.metrics import mean_squared_error
import numpy as np

# --- 1. Caricamento ed Esplorazione Iniziale del Dataset ---
file_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\30_04_CorsoPython_ML\EsercizioNewYorkAirbnb\AB_NYC_2019.csv'
df = pd.read_csv(file_path)

print("--- Esplorazione Iniziale ---")
print("Dimensioni del dataset:", df.shape)
print("\nInformazioni sul dataset:")
print(df.info())
print("\nPrime 5 righe del dataset:")
print(df.head())
print("\nStatistiche descrittive:")
print(df.describe())

# --- 2. Pulizia dei Dati ---
print("\n--- Pulizia dei Dati ---")

# Controllo valori mancanti
print("\nValori mancanti per colonna:")
missing_values = df.isnull().sum()
print(missing_values[missing_values > 0])

# Rimozione duplicati
df_cleaned = df.drop_duplicates()
print(f"\nDimensioni dopo la rimozione dei duplicati: {df_cleaned.shape}")

# --- 3. Analisi della Variabile Target ---
print("\n--- Analisi della Variabile Target (Prezzo) ---")
plt.figure(figsize=(10, 6))
sns.histplot(df_cleaned['price'], kde=True)
plt.title('Distribuzione del prezzo')
plt.xlabel('Prezzo per notte')
plt.ylabel('Frequenza')
plt.show()

# --- 4. Funzione per il Calcolo del VIF e Selezione delle Feature ---
def calcolo_vif_e_selezione(df):
    """
    Calcola il Variance Inflation Factor (VIF) per le feature numeriche
    e seleziona le feature con p-value significativo in una regressione OLS.

    Args:
        df (pd.DataFrame): Il DataFrame contenente i dati.

    Returns:
        pd.DataFrame: Il DataFrame con le feature numeriche selezionate
                      e le feature categoriche codificate tramite one-hot encoding.
    """
    print("\n--- Calcolo VIF e Selezione Feature ---")

    # 1. Definisci la variabile target e le feature numeriche iniziali
    target = 'price'
    numerical_features = [
        'minimum_nights', 'number_of_reviews', 'reviews_per_month',
        'calculated_host_listings_count', 'availability_365'
    ]

    # 2. Crea un DataFrame temporaneo con le feature numeriche e la target, rimuovendo i NaN
    df_model = df[numerical_features + [target]].dropna().copy()
    X_numerical = df_model[numerical_features]
    y = df_model[target]

    # 3. Calcola i p-value tramite regressione OLS
    X_with_const = sm.add_constant(X_numerical)
    ols_model = sm.OLS(y, X_with_const).fit()
    pvalues = ols_model.pvalues
    print("P-values:\n", pvalues)

    # 4. Calcola il VIF
    vif_data = pd.DataFrame()
    vif_data['feature'] = X_numerical.columns
    vif_data['VIF'] = [variance_inflation_factor(X_numerical.values, i) for i in range(X_numerical.shape[1])]
    print("\nVIF:\n", vif_data)

    # 5. Seleziona le feature numeriche con p-value < 0.05 (escludendo la costante)
    significant_numerical_features = pvalues[pvalues < 0.05].index.tolist()
    if 'const' in significant_numerical_features:
        significant_numerical_features.remove('const')
    print("\nFeature numeriche selezionate:\n", significant_numerical_features)

    # 6. Definisci le feature categoriche
    categorical_features = ['neighbourhood_group', 'neighbourhood', 'room_type']

    # 7. Crea un DataFrame contenente le feature selezionate (numeriche e categoriche) e la target, rimuovendo i NaN
    selected_features = significant_numerical_features + categorical_features
    df_selected = df[selected_features + [target]].dropna().copy()

    # 8. Codifica le feature categoriche utilizzando one-hot encoding
    df_encoded = pd.get_dummies(df_selected, columns=categorical_features, drop_first=True)
    print("\nDataFrame dopo l'encoding delle feature categoriche:\n", df_encoded.head())

    return df_encoded

# Esegui la funzione per ottenere il DataFrame processato
df_processed = calcolo_vif_e_selezione(df_cleaned)

# --- 5. Preparazione dei Dati per il Modello XGBoost ---
print("\n--- Preparazione Dati per XGBoost ---")

# Definisci la variabile target e le feature
X = df_processed.drop('price', axis=1)
y = df_processed['price']

# Divisione dei dati in training e test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardizzazione delle feature numeriche (opzionale ma spesso utile per XGBoost)
numerical_cols = X_train.select_dtypes(include=np.number).columns
scaler = StandardScaler()
X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
X_test[numerical_cols] = scaler.transform(X_test[numerical_cols])

print("\nDimensioni Training Set:", X_train.shape, y_train.shape)
print("Dimensioni Test Set:", X_test.shape, y_test.shape)

# --- 6. Inizializzazione e Training del Modello XGBoost (Base) ---
print("\n--- Training del Modello XGBoost (Base) ---")

# Inizializza il modello XGBoost Regressor con parametri di base
xgb_model_base = xgb.XGBRegressor(objective='reg:squarederror',
                                     n_estimators=100,
                                     learning_rate=0.1,
                                     max_depth=5,
                                     random_state=42)

# Allena il modello sul training set
xgb_model_base.fit(X_train, y_train)

# Fai previsioni con il modello base
y_pred_base = xgb_model_base.predict(X_test)

# Calcola le metriche del modello base
mse_base = mean_squared_error(y_test, y_pred_base)
rmse_base = np.sqrt(mse_base)
r2_base = r2_score(y_test, y_pred_base)

print(f'\nModello Base - Mean Squared Error (MSE): {mse_base:.2f}')
print(f'Modello Base - Root Mean Squared Error (RMSE): {rmse_base:.2f}')
print(f'Modello Base - R-squared (R²): {r2_base:.2f}')

# --- 7. Ottimizzazione degli Iperparametri con GridSearchCV ---
print("\n--- Ottimizzazione degli Iperparametri con GridSearchCV ---")

# Definisci la griglia di iperparametri da esplorare
param_grid = {
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

# Inizializza il modello XGBoost Regressor per GridSearchCV
xgb_regressor_grid = xgb.XGBRegressor(objective='reg:squarederror', random_state=42)

# Eseguiamo GridSearchCV per trovare la combinazione migliore
grid_search = GridSearchCV(xgb_regressor_grid, param_grid, cv=3, scoring="r2", n_jobs=-1)
grid_search.fit(X_train, y_train)

# Miglior set di parametri trovato
best_params = grid_search.best_params_
print("\nMigliori iperparametri trovati:", best_params)

# --- 8. Addestramento di XGBoost con i Migliori Parametri ---
print("\n--- Addestramento XGBoost con i Migliori Parametri ---")
best_xgb = xgb.XGBRegressor(**best_params, objective="reg:squarederror", random_state=42)
best_xgb.fit(X_train, y_train)

# Facciamo previsioni con il modello ottimizzato
y_pred_best = best_xgb.predict(X_test)

# Calcoliamo le metriche aggiornate
mse_best = mean_squared_error(y_test, y_pred_best)
rmse_best = np.sqrt(mse_best)
r2_best = r2_score(y_test, y_pred_best)

print(f'Modello Ottimizzato - Mean Squared Error (MSE): {mse_best:.2f}')
print(f'Modello Ottimizzato - Root Mean Squared Error (RMSE): {rmse_best:.2f}')
print(f'Modello Ottimizzato - R-squared (R²): {r2_best:.2f}')

# --- 6. Inizializzazione e Training del Modello XGBoost (con xgb.train) ---
print("\n--- Training del Modello XGBoost (con xgb.train) ---")

# Converti i dataset di training e test in formato DMatrix
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# Definisci i parametri del modello (puoi iniziare con i parametri base o quelli ottimizzati)
params_base_native = {
    'objective': 'reg:squarederror',
    'learning_rate': 0.1,
    'max_depth': 5,
    'seed': 42,
    'tree_method': 'hist'  # Specifichiamo l'algoritmo 'hist'
}

# Definisci il numero di round di boosting (equivalente a n_estimators)
num_round = 100

# Addestra il modello utilizzando xgb.train()
xgb_model_base_native = xgb.train(params_base_native, dtrain, num_round)

# Fai previsioni sul set di test
y_pred_base_native = xgb_model_base_native.predict(dtest)

# Calcola le metriche del modello base (nativo)
mse_base_native = mean_squared_error(y_test, y_pred_base_native)
rmse_base_native = np.sqrt(mse_base_native)
r2_base_native = r2_score(y_test, y_pred_base_native)

print(f'\nModello Base (Native) - Mean Squared Error (MSE): {mse_base_native:.2f}')
print(f'Modello Base (Native) - Root Mean Squared Error (RMSE): {rmse_base_native:.2f}')
print(f'Modello Base (Native) - R-squared (R²): {r2_base_native:.2f}')

# --- 7. Ottimizzazione degli Iperparametri con GridSearchCV (Adattato per xgb.train) ---
print("\n--- Ottimizzazione degli Iperparametri con GridSearchCV (Adattato per xgb.train) ---")

def train_evaluate_xgb(params, dtrain, dtest, y_test, num_round=100):
    """Funzione per addestrare e valutare il modello XGBoost con dati DMatrix."""
    model = xgb.train(params, dtrain, num_round)
    y_pred = model.predict(dtest)
    r2 = r2_score(y_test, y_pred)
    return r2

# Definisci la griglia di iperparametri da esplorare (adatta per xgb.train)
param_grid_native = {
    'learning_rate': [0.01, 0.05, 0.1],
    'max_depth': [3, 5, 7],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0],
    'tree_method': ['hist']  # Forza l'uso di 'hist'
}

best_r2_native = -1.0
best_params_native = None

# Itera sulla griglia di iperparametri
for params in ParameterGrid(param_grid_native):
    print(f"\nTesting parameters: {params}")
    current_r2 = train_evaluate_xgb(params, dtrain, dtest, y_test)
    if current_r2 > best_r2_native:
        best_r2_native = current_r2
        best_params_native = params

print("\nMigliori iperparametri trovati (xgb.train):", best_params_native)
print("Miglior R-squared (xgb.train):", best_r2_native)

# --- 8. Addestramento di XGBoost con i Migliori Parametri (xgb.train) ---
print("\n--- Addestramento XGBoost con i Migliori Parametri (xgb.train) ---")

best_xgb_native_params = {**best_params_native, 'objective': 'reg:squarederror', 'seed': 42}
best_xgb_native_model = xgb.train(best_xgb_native_params, dtrain, num_round)

# Facciamo previsioni con il modello ottimizzato (nativo)
y_pred_best_native = best_xgb_native_model.predict(dtest)

# Calcoliamo le metriche aggiornate (nativo)
mse_best_native = mean_squared_error(y_test, y_pred_best_native)
rmse_best_native = np.sqrt(mse_best_native)
r2_best_native = r2_score(y_test, y_pred_best_native)

print(f'Modello Ottimizzato (Native) - Mean Squared Error (MSE): {mse_best_native:.2f}')
print(f'Modello Ottimizzato (Native) - Root Mean Squared Error (RMSE): {rmse_best_native:.2f}')
print(f'Modello Ottimizzato (Native) - R-squared (R²): {r2_best_native:.2f}')

# --- 9. Grafico delle Previsioni vs. Valori Reali (Modello Ottimizzato Nativo) ---
print("\n--- Grafico Previsioni vs. Valori Reali (Modello Ottimizzato Nativo) ---")
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred_best_native, color="green", alpha=0.5, label="Previsioni (Native)")
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], linestyle="--", color="red", label="Perfetta corrispondenza")
plt.xlabel("Valori Reali")
plt.ylabel("Valori Predetti")
plt.title("XGBoost (Ottimizzato Native) - Previsioni vs. Valori Reali")
plt.legend()
plt.grid(True)
plt.show()

# --- 10. Risultati Finali Aggiornati ---
print("\n--- Risultati Finali Aggiornati ---")
print(f"Modello Base - MSE: {mse_base:.2f}, RMSE: {rmse_base:.2f}, R²: {r2_base:.2f}")
print(f"Modello Base (Native) - MSE: {mse_base_native:.2f}, RMSE: {rmse_base_native:.2f}, R²: {r2_base_native:.2f}")
print(f"Migliori Iperparametri (GridSearchCV): {best_params}")
print(f"Modello Ottimizzato - MSE: {mse_best}, RMSE: {rmse_best:.2f}, R²: {r2_best:.2f}")

# Calcola la media dei prezzi dal DataFrame pulito
average_price = df_cleaned['price'].mean()
print(f"\nLa media del prezzo per notte nel dataset pulito è: ${average_price:.2f}")