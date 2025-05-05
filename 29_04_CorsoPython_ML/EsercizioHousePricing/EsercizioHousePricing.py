import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Caricamento dati
file_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\29_04_CorsoPython_ML\EsercizioHousePricing\kc_house_data.csv'
df = pd.read_csv(file_path)

print(df.head())
print(df.info())
print(df.describe())

# Rimozione duplicati
df_cleaned = df.drop_duplicates()

# Feature e target
X = df_cleaned.drop(['price', 'id', 'zipcode', 'date'], axis=1)
y = df_cleaned['price']

# Matrice di correlazione iniziale
plt.figure(figsize=(8, 6))
correlation_matrix = df_cleaned.corr(numeric_only=True)
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Matrice di correlazione delle colonne numeriche')
plt.show()

# Calcolo VIF con standardizzazione per stabilità
def calculate_vif(df):
    numeric_df = df.select_dtypes(include=np.number)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(numeric_df)
    vif_data = pd.DataFrame()
    vif_data["Feature"] = numeric_df.columns
    vif_data["VIF"] = [variance_inflation_factor(X_scaled, i) for i in range(X_scaled.shape[1])]
    return vif_data.sort_values(by='VIF', ascending=False)

def elimina_variabili_vif_pvalue(X_train, y_train, vif_threshold=10.0, pvalue_threshold=0.05):
    """
    Rimuove variabili da X_train basandosi su VIF e p-value.
    
    - Elimina solo variabili con VIF > soglia e p-value > soglia.
    - Ricalcola VIF e p-value dopo ogni eliminazione.
    """
    
    # Copia dei dati per lavorare in sicurezza
    X_current = X_train.copy()
    
    # Aggiungi costante per statsmodels
    X_const = sm.add_constant(X_current)
    
    while True:
        # Modello OLS per calcolare p-value
        model = sm.OLS(y_train, X_const).fit()
        pvalues = model.pvalues.drop('const')  # escludi l'intercetta
        
        # Calcolo VIF
        vif = pd.DataFrame()
        vif["Feature"] = X_current.columns
        vif["VIF"] = [variance_inflation_factor(X_current.values, i) for i in range(X_current.shape[1])]
        
        # Unisco p-value e VIF
        stats = vif.copy()
        stats["p-value"] = pvalues.values
        
        # Trova candidati da eliminare: VIF alto + p-value alto
        candidates = stats[(stats["VIF"] > vif_threshold) & (stats["p-value"] > pvalue_threshold)]
        
        if candidates.empty:
            print("\nNessuna variabile da eliminare. Selezione completata.")
            break
        
        # Elimina la variabile con il VIF più alto tra i candidati
        worst_feature = candidates.sort_values(by="VIF", ascending=False)["Feature"].iloc[0]
        print(f"Rimuovo '{worst_feature}' con VIF = {candidates.loc[candidates['Feature'] == worst_feature, 'VIF'].values[0]:.2f} "
              f"e p-value = {candidates.loc[candidates['Feature'] == worst_feature, 'p-value'].values[0]:.4f}")
        
        # Aggiorna i dati
        X_current = X_current.drop(columns=[worst_feature])
        X_const = sm.add_constant(X_current)
    
    print("\nFeature finali selezionate:")
    print(X_current.columns.tolist())
    
    return X_current

# Rimozione multicollinearità
columns_to_drop = ['price', 'id', 'zipcode', 'date']
df_vif = df_cleaned.drop(columns=columns_to_drop)

# Rimozione manuale iniziale (basata su VIF noti alti)
columns_to_remove = ['sqft_above', 'grade', 'bathrooms']
for col_to_remove in columns_to_remove:
    if col_to_remove in df_vif.columns:
        print(f"\nEliminando la colonna: {col_to_remove}")
        df_vif_temp = df_vif.drop(columns=[col_to_remove])
        vif_result = calculate_vif(df_vif_temp)
        print("VIF dopo la rimozione:")
        print(vif_result.head())
        df_vif = df_vif_temp

# Rimozione iterativa di VIF > 10
while True:
    vif_result = calculate_vif(df_vif)
    highest_vif_feature = vif_result.iloc[0]
    if highest_vif_feature['VIF'] < 10:
        break
    column_to_remove = highest_vif_feature['Feature']
    print(f"\nEliminando la colonna con VIF più alto: {column_to_remove} (VIF = {highest_vif_feature['VIF']:.2f})")
    df_vif = df_vif.drop(columns=[column_to_remove])
    print("VIF dopo la rimozione:")
    print(calculate_vif(df_vif).head())

# Reintegro sicuro della variabile target
df_vif['price'] = y.values

# Creazione della nuova feature n_stanze
df_vif['n_stanze'] = df_cleaned.loc[df_vif.index, 'bedrooms'].values + df_cleaned.loc[df_vif.index, 'bathrooms'].values

# Rimozione delle feature originali (se ancora presenti)
df_vif = df_vif.drop(columns=['bedrooms', 'bathrooms'], errors='ignore')

# Visualizzazione finale della correlazione
print("\nDataFrame finale (df_vif) dopo la gestione della multicollinearità:")
print(df_vif.head())

plt.figure(figsize=(8, 6))
sns.heatmap(df_vif.corr(numeric_only=True), annot=True, cmap='coolwarm')
plt.title("Matrice di correlazione dopo l'utilizzo di VIF")
plt.show()

# Split train/test
X = df_vif.drop('price', axis=1)
y = df_vif['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=69)

# Standardizzazione
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Regressione Lineare
linear_regression = LinearRegression()
linear_regression.fit(X_train_scaled, y_train)
y_pred_linear = linear_regression.predict(X_test_scaled)
r2_linear = r2_score(y_test, y_pred_linear)

# Ridge
ridge = Ridge(alpha=1.0)
ridge.fit(X_train_scaled, y_train)
y_pred_ridge = ridge.predict(X_test_scaled)
r2_ridge = r2_score(y_test, y_pred_ridge)

# Lasso
lasso = Lasso(alpha=0.1)
lasso.fit(X_train_scaled, y_train)
y_pred_lasso = lasso.predict(X_test_scaled)
r2_lasso = r2_score(y_test, y_pred_lasso)

# Risultati
results = {
    "R^2 Regressione Lineare": r2_linear,
    "R^2 Ridge": r2_ridge,
    "R^2 Lasso": r2_lasso,
}
print("\nRisultati dei modelli:")
print(results)

# ================================
# Grafico finale dei risultati
# ================================
plt.figure(figsize=(8, 5))
model_names = list(results.keys())
r2_scores = list(results.values())

df_results = pd.DataFrame({
    'Model': model_names,
    'R2': r2_scores
})

sns.barplot(data=df_results, x='Model', y='R2', hue='Model', palette='viridis', legend=False)

plt.ylabel('R² Score')
plt.title('Confronto delle performance dei modelli')
plt.ylim(0, 1)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()