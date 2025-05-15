import pandas as pd

data = {
'Nome': ['Alice', 'Bob', 'Carla','Alessia'],
'Età': [25, 30, 22, 15],
'Città': ['Roma', 'Milano', 'Napoli', 'Verona']
}
# Tramite pandas trasformo il dizionario creato in un dataframe
df = pd.DataFrame(data)

print("\nDataFrame originale")
print(df)

df_older = df[df['Età']>23]

print("\nPersone con età maggiore di 23: ")
print(df_older)

df['Maggiorenne'] = df['Età'] >= 18

print("\nDataFrame con l'aggiunta della colonna 'Maggiorenne'")
print(df)
