import pandas as pd

# Caricamento dei dati
data = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\22_04_CorsoPython\manipolazioneAggregazione\vendite.csv'
df = pd.read_csv(data)

# Anteprima dei dati
print("Prime 5 righe del DataFrame:")
print(df.head(5))

# Calcolo del totale vendite
df['TotaleVendite'] = df['Prezzo Unitario'] * df['Quantità']
print("\nDataFrame con totale vendite:")
print(df)

# Vendite totali per prodotto
print("\nVendite totali per ciascun prodotto:")
perProdotto = df.groupby('Prodotto')['TotaleVendite'].sum()
print(perProdotto)

# Prodotto più venduto (per quantità)
print("\nIl prodotto più venduto (per quantità) è:")
piuVenduto = df.loc[df['Quantità'].idxmax()]
print(piuVenduto[['Prodotto', 'Quantità']])

# Città con maggior volume di vendite
print("\nCittà con maggior volume di vendite:")
citta_max = df.groupby('Città')['TotaleVendite'].sum().idxmax()
print(f"{citta_max} (Totale: {df.groupby('Città')['TotaleVendite'].sum().max():.2f}€)")

# Vendite superiori a 1000 euro
print("\nLe vendite superiori a 1000 euro sono:")
vendite1000 = df[df['TotaleVendite'] > 1000]
print(vendite1000)

# Ordinamento per TotaleVendite (decrescente)
print("\nDataFrame ordinato per TotaleVendite (decrescente):")
df_ordinato = df.sort_values('TotaleVendite', ascending=False)
print(df_ordinato)

# Numero di vendite per città
print("\nNumero di vendite per ogni città:")
conteggio_citta = df['Città'].value_counts()
print(conteggio_citta)