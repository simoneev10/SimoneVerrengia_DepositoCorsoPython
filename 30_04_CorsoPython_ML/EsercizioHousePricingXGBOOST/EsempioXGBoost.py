import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

# Caricamento e Preprocessing Dati
file_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\29_04_CorsoPython_ML\EsercizioHousePricing\kc_house_data.csv'
df = pd.read_csv(file_path)

# Pulizia
df = df.drop_duplicates()
df['n_stanze'] = df['bedrooms'] + df['bathrooms']
df = df.drop(columns=['id', 'date', 'zipcode', 'bedrooms', 'bathrooms'])

# Separazione variabili indipendenti e target
X = df.drop('price', axis=1)
y = df['price']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modello XGBoost base
xgb_regressor = xgb.XGBRegressor(objective="reg:squarederror", random_state=42)
xgb_regressor.fit(X_train, y_train)
y_pred = xgb_regressor.predict(X_test)

# Valutazione iniziale
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

# Ottimizzazione con GridSearchCV
param_grid = {
    'n_estimators': [100, 200],
    'learning_rate': [0.05, 0.1],
    'max_depth': [3, 5],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

grid_search = GridSearchCV(
    estimator=xgb.XGBRegressor(objective="reg:squarederror", random_state=42),
    param_grid=param_grid,
    cv=3,
    scoring='r2',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_

# Modello XGBoost ottimizzato
best_xgb = xgb.XGBRegressor(**best_params, objective="reg:squarederror", random_state=42)
best_xgb.fit(X_train, y_train)
y_pred_best = best_xgb.predict(X_test)

# Valutazione finale
mse_best = mean_squared_error(y_test, y_pred_best)
rmse_best = np.sqrt(mse_best)
r2_best = r2_score(y_test, y_pred_best)

# Grafico Previsioni vs Valori Reali
plt.figure(figsize=(8,6))
plt.scatter(y_test, y_pred_best, color="blue", alpha=0.5, label="Previsioni")
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], linestyle="--", color="red", label="Perfetta corrispondenza")
plt.xlabel("Valori Reali")
plt.ylabel("Valori Predetti")
plt.title("XGBoost - Previsioni vs. Valori Reali")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

print(f"R² Iniziale: {r2:.4f}")
print(f"MSE Iniziale: {mse:.2f}")
print(f"RMSE Iniziale: {rmse:.2f}")

print(f"\nMigliori Parametri: {best_params}")

print(f"R² Ottimizzato: {r2_best:.4f}")
print(f"MSE Ottimizzato: {mse_best:.2f}")
print(f"RMSE Ottimizzato: {rmse_best:.2f}")


print(df.describe())
