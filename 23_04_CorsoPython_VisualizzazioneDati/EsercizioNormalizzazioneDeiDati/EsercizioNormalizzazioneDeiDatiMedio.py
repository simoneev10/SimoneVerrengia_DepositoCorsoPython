import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(42)
num_persone = 8

altezze = np.random.randint(155,205, num_persone)
pesi = np.random.randint(50,100, num_persone)
eta = np.random.randint(18,75, num_persone)

df = pd.DataFrame({
    'altezza': altezze,
    'peso' : pesi,
    'eta' : eta
    })

print(f"\nDataFrame originale:\n{df}")

# Funzione di normalizzazione
def min_max_norm(x):
    return (x - x.min()) / (x.max() - x.min())

df_normalizzato = df.copy()
df_normalizzato['altezza'] = min_max_norm(df['altezza'])
df_normalizzato['peso'] = min_max_norm(df['peso'])

print(f"\nDataFrame normalizzato:\n{df_normalizzato}")

# Creazione del grafico di confronto
plt.figure(figsize=(12, 8))

# Aggiunge identificatore numerico per ogni persona
df['id'] = range(1, num_persone + 1)
df_normalizzato['id'] = range(1, num_persone + 1)

# Subplot 1: Dati originali
plt.subplot(2, 1, 1)
plt.title('Dati Originali', fontsize=14)
plt.plot(df['id'], df['altezza'], 'o-', label='Altezza (cm)')
plt.plot(df['id'], df['peso'], 's-', label='Peso (kg)')
plt.plot(df['id'], df['eta'], '^-', label='eta (anni)')
plt.xlabel('Persona ID')
plt.ylabel('Valore')
plt.grid(True)
plt.legend()

# Subplot 2: Dati normalizzati
plt.subplot(2, 1, 2)
plt.title('Dati Normalizzati (min-max)', fontsize=14)
plt.plot(df_normalizzato['id'], df_normalizzato['altezza'], 'o-', label='Altezza (normalizzata)')
plt.plot(df_normalizzato['id'], df_normalizzato['peso'], 's-', label='Peso (normalizzato)')
plt.plot(df_normalizzato['id'], df_normalizzato['eta'], '^-', label='eta (non normalizzata)')
plt.xlabel('Persona ID')
plt.ylabel('Valore')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# Creiamo anche un grafico a barre per mostrare il confronto tra i valori originali e normalizzati
plt.figure(figsize=(12, 10))

# Per ogni variabile, mostriamo originale vs normalizzato
cols = ['altezza', 'peso', 'eta']
for i, col in enumerate(cols):
    plt.subplot(3, 1, i+1)
    
    # Crea un dataframe per il confronto
    df_temp = pd.DataFrame({
        'Originale': df[col],
        'Normalizzato': df_normalizzato[col]
    })
    
    # Plot
    df_temp.plot(kind='bar', ax=plt.gca())
    plt.title(f'Confronto {col} - Originale vs Normalizzato', fontsize=14)
    plt.xlabel('Persona ID')
    plt.ylabel('Valore')
    plt.grid(True, alpha=0.3)
    
plt.tight_layout()
plt.show()