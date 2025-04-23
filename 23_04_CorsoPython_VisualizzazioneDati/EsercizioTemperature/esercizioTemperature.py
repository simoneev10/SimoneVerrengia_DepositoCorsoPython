import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Generazione dati
temperature = np.random.randint(0, 40, 31)
giorni = [f"Giorno {i+1}" for i in range(31)]
df = pd.DataFrame({'Giorno': giorni, 'Temperature': temperature})

# Calcolo statistiche
tempMax = df['Temperature'].max()
tempMin = df['Temperature'].min()
tempMedia = df['Temperature'].mean()
tempMediana = df['Temperature'].median()

def mostra_menu():
    print("\nMenu visualizzazione Temperature:")
    print("1. Istogramma temperature")
    print("2. Grafico a linee")
    print("3. Grafico a barre")
    print("4. Scatter plot")
    print("0. Esci")

# Per ogni tipologia di grafico creo una funzione

def istogramma():
    plt.figure(figsize=(10, 6))
    plt.hist(df['Temperature'], bins=30)
    plt.title('Distribuzione delle Temperature')
    plt.xlabel('Temperatura (°C)')
    plt.ylabel('Frequenza')
    plt.grid(True)
    plt.show()

def grafico_linee():
    plt.figure(figsize=(10, 6))
    plt.plot(df['Giorno'], df['Temperature'], color='green', marker='o')
    plt.title('Andamento Temperature Giornaliere')
    plt.xlabel('Giorno')
    plt.ylabel('Temperatura (°C)')
    plt.grid(True)
    plt.xticks(rotation=90)
    plt.show()

def grafico_barre():
    plt.figure(figsize=(10, 6))
    plt.bar(df['Giorno'], df['Temperature'], color='orange', edgecolor='black')
    plt.title('Temperature Giornaliere')
    plt.xlabel('Giorno')
    plt.ylabel('Temperatura (°C)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()

def scatter_plot():
    plt.figure(figsize=(10, 5))
    plt.scatter(df['Giorno'], df['Temperature'], color='red') #, s=50
    plt.title('Distribuzione Temperature')
    plt.xlabel('Giorno')
    plt.ylabel('Temperatura (°C)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()

# Menu principale
while True:
    mostra_menu()
    scelta = input("\nScegli un'opzione (0-4): ")
    
    if scelta == '1':
        istogramma()
    elif scelta == '2':
        grafico_linee()
    elif scelta == '3':
        grafico_barre()
    elif scelta == '4':
        scatter_plot()
    elif scelta == '0':
        print("\nProgramma terminato.")
        break
    else:
        print("\nScelta non valida. Riprova.")
    