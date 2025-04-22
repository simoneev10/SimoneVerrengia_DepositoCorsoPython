import pandas as pd

# Caricamento del file CSV
file_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\22_04_CorsoPython\EsercizioEsplorazioneDati\personale.csv'
df = pd.read_csv(file_path)

# Stampa del DataFrame originale e anteprime
print("\nDataFrame originale: ")
print(df)  # Mostra tutto il DataFrame

print("\nPrime 5 righe: ")
print(df.head(5))  # Prime 5 righe

print("\nUltime 5 righe: ")
print(df.tail(5))  # Ultime 5 righe

# Pulizia dei dati
cleaned_data = df.drop_duplicates().dropna()  # Rimuove duplicati e righe con valori mancanti

print("\nDataFrame pulito: ")
print(cleaned_data.head())  # Anteprima dati puliti

# Calcolo età media
etamedia = cleaned_data['Eta'].mean()
print("\nL'età media del personale è di: ", etamedia)

# Conversione e pulizia del salario
cleaned_data['Salario'] = pd.to_numeric(cleaned_data['Salario'], errors='coerce')  # Converti a numerico, (errori -> NaN)
salariomedio = cleaned_data['Salario'].mean()
print("\nIl salario medio è di: ", salariomedio)
print(cleaned_data)  # Mostra DataFrame con salari convertiti

# Sostituzione NaN con la mediana
print("Sostituisco i valori Nan dei salari con la mediana: ")
cleaned_data['Salario'].fillna(cleaned_data['Salario'].median(), inplace=True)
print(cleaned_data)

# Aggiunta colonna "Categoria Età"
cleaned_data["Categoria Età"] = ""  # Inizializza colonna vuota
cleaned_data.loc[cleaned_data['Eta'] < 19, "Categoria Età"] = "Giovane"
cleaned_data.loc[(cleaned_data['Eta'] >= 19) & (cleaned_data['Eta'] <= 65), "Categoria Età"] = "Adulto"
cleaned_data.loc[cleaned_data['Eta'] > 65, "Categoria Età"] = "Senior"
print(cleaned_data)  # Mostra DataFrame con categorie

print(cleaned_data.describe())

# Salvataggio del risultato in un nuovo CSV
percorso = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\22_04_CorsoPython\personale_pulito_con_categorie.csv'
cleaned_data.to_csv(percorso, index=False)  # Salva senza colonna indice
