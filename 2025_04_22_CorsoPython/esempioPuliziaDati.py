import pandas as pd
import numpy as np


# DataFrame esempio, inclusi valori mancanti e duplicati 4.
data = {
'Nome': ['Alice', 'Bob', 'Carla', 'Bob', 'Carla', 'Alice', None],
'Età': [25, 30, 22, 30, np.nan, 25, 29],
'Città': ['Roma', 'Milano', 'Napoli', 'Milano', 'Napoli', 'Roma', 'Roma']
}
# Tramite pandas trasformo il dizionario creato in un dataframe
df = pd.DataFrame(data)

print("\nDataFrame originale")
print(df)

# Rimozione dei duplicati
df = df.drop_duplicates()

# Gestione dati mancanti, rimozione delle righe con elemento mancante
df_cleaned = df.dropna()

# Possiamo sostituire dati mancanti con valori di default
df['Età'].fillna(df['Età'].mean(), inplace=True)

# Stampa del DataFrame pulito
print("Stampa del DataFrame pulito dai dati mancanti")
print(df_cleaned)

print("Stampa del DataFrame con dati mancanti sostituiti")
print(df)