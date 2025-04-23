import pandas as pd

# Generazione di una serie di date
date_range = pd.date_range(start='2021-01-01', periods=10, freq='M')

# Resampling dei dati di una serie temporale
df_resampled = df.resample('M').mean()

# esempio: colonna "date" in stringhe -> datetime
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# oppure creare un indice
df.index = pd.to_datetime(df['date'])

Series.shift()
# "Sposta" i valori lungo l'asse temporale di un numero di periodi, utile per calcolare le differenze
# ritardate, tassi di crescita ecc...

# aggiunge una colonna con il valore del giorno precedente
df['prev_day'] = df['value'].shift(1)
# tasso di variazione giornaliero
df['daily_return'] = df['value'].pct_change() # equivalente a shift + calcolo %

Series.rolling()
# calcola statistiche mobili su una finestra temporale scorrevole.
df['rolling_mean7'] = df['value'].rolling(window=7).mean()
