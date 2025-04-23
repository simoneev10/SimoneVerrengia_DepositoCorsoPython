import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score

# Caricamento del file 
file_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\23_04_CorsoPython\EsercizioCompagniaTelecomunicazioni\clienti_telecomunicazioni.csv'
df = pd.read_csv(file_path)

# Copia del DataFrame originale per la pulizia 
df_cleaned = df.copy()

# Pulizia della colonna 'Dati_Consumati' 
df_cleaned['Dati_Consumati'].fillna(df_cleaned['Dati_Consumati'].mean(), inplace=True)

# Pulizia della colonna 'Servizio_Clienti_Contatti' 
df_cleaned['Servizio_Clienti_Contatti'] = pd.to_numeric(df_cleaned['Servizio_Clienti_Contatti'], errors='coerce')
df_cleaned['Servizio_Clienti_Contatti'].fillna(0, inplace=True)

# Pulizia della colonna 'Età' 
df_cleaned['Età'] = pd.to_numeric(df_cleaned['Età'], errors='coerce')

# Rimozione delle righe con età non valide o mancanti
eta_invalid = df_cleaned[(df_cleaned['Età'] > 99) | (df_cleaned['Età'] < 0)].index
eta_nan = df_cleaned[df_cleaned['Età'].isna()].index
df_cleaned.drop(index=eta_invalid.union(eta_nan), inplace=True)

# Pulizia della colonna 'Churn' 
df_cleaned['Churn'] = df_cleaned['Churn'].astype(str).str.lower().str.strip()
df_cleaned['Churn'] = df_cleaned['Churn'].replace({
    'sì': '1',
    'si': '1',
    'no': '0',
    'nan': '0'  # Gestione di valori mancanti convertiti in stringa
}).astype(int)

# Visualizzazione dei valori puliti di Churn
print("Distribuzione valori 'Churn' dopo la pulizia:")
print(df_cleaned['Churn'].value_counts())

#  Pulizia della colonna 'Durata_Abbonamento' 

# Stima dei valori mancanti usando altri campi
df_cleaned['Durata_Abbonamento'] = df_cleaned['Durata_Abbonamento'].fillna(
    df_cleaned['Dati_Consumati'] / df_cleaned['Tariffa_Mensile'] / 10
)

# Conversione a numerico e rimozione valori negativi
df_cleaned['Durata_Abbonamento'] = pd.to_numeric(df_cleaned['Durata_Abbonamento'], errors='coerce')
durata_invalid = df_cleaned[df_cleaned['Durata_Abbonamento'] < 0].index
df_cleaned.drop(index=durata_invalid, inplace=True)

df_cleaned['Costo_per_GB'] = df_cleaned['Dati_Consumati'] / df_cleaned['Tariffa_Mensile']

# Visualizzazione finale 
print("\nDataFrame finale pulito:")
print(df_cleaned.reset_index()) # Aggiusto gli indici

# Calcolo della matrice di correlazione
correlation_matrix = df_cleaned.corr(numeric_only=True)

print(correlation_matrix)

# Selezione di Feature e target
features = ['Età', 'Durata_Abbonamento', 'Tariffa_Mensile', 'Dati_Consumati', 'Servizio_Clienti_Contatti']
X = df_cleaned[features]
y = df_cleaned['Churn']

X = X.fillna(X.mean())

# Divisione in train/test set 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Addestramento del modello 
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Predizioni
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuratezza del modello: {accuracy:.2f}")

# AUC (Area Under Curve)
auc = roc_auc_score(y_test, y_proba)
print(f"AUC: {auc:.2f}")

