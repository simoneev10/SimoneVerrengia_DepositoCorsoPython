import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Caricamento dati
file_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\29_04_CorsoPython_ML\EsercizioHousePricing\kc_house_data.csv'
df = pd.read_csv(file_path)

# Rimozione duplicati
df_cleaned = df.drop_duplicates()

# Matrice di correlazione iniziale
plt.figure(figsize=(8, 6))
correlation_matrix = df_cleaned.corr(numeric_only=True)
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Matrice di correlazione delle colonne numeriche')
plt.show()

# Funzione per calcolare il VIF
def calculate_vif(df):
    numeric_df = df.select_dtypes(include=np.number)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(numeric_df)
    vif_data = pd.DataFrame()
    vif_data["Feature"] = numeric_df.columns
    vif_data["VIF"] = [variance_inflation_factor(X_scaled, i) for i in range(X_scaled.shape[1])]
    return vif_data.sort_values(by='VIF', ascending=False)

# Preparazione per VIF
df_vif = df_cleaned.drop(columns=['price', 'id', 'zipcode', 'date'])

# Rimozione manuale iniziale
initial_drops = ['sqft_above', 'grade', 'bathrooms']
for col in initial_drops:
    if col in df_vif.columns:
        print(f"\nEliminando la colonna: {col}")
        df_vif = df_vif.drop(columns=col)

# Rimozione iterativa delle colonne con VIF > 10
while True:
    vif_result = calculate_vif(df_vif)
    max_vif = vif_result.iloc[0]
    if max_vif['VIF'] < 10:
        break
    print(f"\nRimuovo {max_vif['Feature']} con VIF={max_vif['VIF']:.2f}")
    df_vif = df_vif.drop(columns=max_vif['Feature'])

# Reintegro della variabile target
df_vif['price'] = df_cleaned['price'].values

# Creazione della nuova feature "n_stanze"
df_vif['n_stanze'] = df_cleaned['bedrooms'].values + df_cleaned['bathrooms'].values

# Rimozione delle feature originali (se ancora presenti)
df_vif = df_vif.drop(columns=['bedrooms', 'bathrooms'], errors='ignore')

# Visualizzazione finale
print("\nDataFrame finale dopo VIF e feature engineering:")
print(df_vif.head())

# Heatmap finale
plt.figure(figsize=(8, 6))
sns.heatmap(df_vif.corr(numeric_only=True), annot=True, cmap='coolwarm')
plt.title("Matrice di correlazione finale")
plt.show()

# Preparazione dati per il modello
X = df_vif.drop('price', axis=1)
y = df_vif['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=69)

# Standardizzazione
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Modelli
models = {
    "Regressione Lineare": LinearRegression(),
    "Ridge": Ridge(alpha=1.0),
    "Lasso": Lasso(alpha=0.1)
}

results = {}
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    r2 = r2_score(y_test, y_pred)
    results[f"R^2 {name}"] = r2

# Output
print("\nRisultati dei modelli:")
for k, v in results.items():
    print(f"{k}: {v:.4f}")

# Grafico finale
plt.figure(figsize=(8, 5))
sns.barplot(x=list(results.keys()), y=list(results.values()), palette='viridis')
plt.ylabel('R² Score')
plt.title('Confronto delle performance dei modelli')
plt.ylim(0, 1)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()
