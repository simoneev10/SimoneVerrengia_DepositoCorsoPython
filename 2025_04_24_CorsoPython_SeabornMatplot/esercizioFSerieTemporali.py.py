import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Generazione dei dati giornalieri con tendenza crescente
def generazione_dati():
    np.random.seed(69)  # Per rendere i risultati riproducibili

    num_giorni = 365
    date = pd.date_range(start='2024-01-01', periods=num_giorni)
    
    trend = np.linspace(0, 500, num_giorni)  # Simula crescita di popolarità
    visitatori_casuali = np.random.normal(loc=2000, scale=500, size=num_giorni)
    visitatori = visitatori_casuali + trend

    # Crea DataFrame con indice temporale
    df = pd.DataFrame({'visitatori': visitatori}, index=date)
    return df

# Calcolo della media e deviazione standard per ciascun mese
def statistiche_mensili(df):
    media_mensile = df.resample('M').mean()
    dev_std_mensile = df.resample('M').std()

    # Rinomina le colonne per chiarezza
    media_mensile.columns = ['Media_mensile_visitatori']
    dev_std_mensile.columns = ['Deviazione_mensile_visitatori']

    print(media_mensile)
    print(dev_std_mensile)

# Grafico giornaliero dei visitatori
def grafico_a_linee(df):
    sns.set_theme(context='talk', style='whitegrid', palette='coolwarm', font='serif')
    plt.figure(figsize=(16,8))
    sns.lineplot(x=df.index, y=df['visitatori'], marker='D')
    plt.title('Numero di visitatori giornalieri (2024)')
    plt.xlabel('Data')
    plt.ylabel('Numero visitatori')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Grafico della media mensile dei visitatori
def grafico_media_mensile(df):
    media_mensile = df.resample('M').mean()
    media_mensile.index = media_mensile.index.strftime('%Y-%m')  # Formatta l'indice per leggibilità

    plt.figure(figsize=(12,6))
    plt.plot(media_mensile.index, media_mensile['visitatori'], color='red', marker='o')
    plt.title('Media Mensile dei visitatori')
    plt.xlabel('Mese')
    plt.ylabel('Media visitatori')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Visualizza la media mobile a 7 giorni per un mese selezionato
def media_mobile_mensile(df):
    mese_input = input("Inserisci il mese nel formato YYYY-MM (es: 2024-03): ")
    try:
        mese = df.index.to_period('M') == mese_input
        df_mese = df.loc[mese]

        if df_mese.empty:
            print("Mese non trovato. Riprova.")
            return

        df_mese['media_mobile_7'] = df_mese['visitatori'].rolling(window=7).mean()

        plt.figure(figsize=(12, 6))
        plt.plot(df_mese.index, df_mese['media_mobile_7'], label='Media mobile (7 giorni)', color='blue', marker='o')
        plt.title(f'Andamento nel mese {mese_input}')
        plt.xlabel('Data')
        plt.ylabel('Visitatori')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print("Errore:", e)

# Grafico combinato con Seaborn: visitatori + media mobile
def grafico_combinato(df):
    df['media_mobile_7'] = df['visitatori'].rolling(window=7).mean()
    
    # Trasformazione per usare seaborn con più serie
    df_plot = df[['visitatori', 'media_mobile_7']].reset_index().melt(
        id_vars='index', 
        value_vars=['visitatori', 'media_mobile_7'],
        var_name='Tipo', 
        value_name='Valore'
    )
    
    plt.figure(figsize=(14, 6))
    sns.lineplot(data=df_plot, x='index', y='Valore', hue='Tipo', palette=['green', 'blue'])
    plt.title('Visitatori e Media Mobile a 7 Giorni (Seaborn)')
    plt.xlabel('Data')
    plt.ylabel('Numero di Visitatori')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Menù di selezione per accedere alle funzionalità
def menu():
    df = generazione_dati()
    while True:
        print("\n--- Menu ---")
        print("1. Mostra statistiche mensili")
        print("2. Mostra grafico giornaliero")
        print("3. Mostra media mobile a 7 giorni per un mese")
        print("4. Mostra media mensile")
        print("5. Grafico combinato (Seaborn)")
        print("6. Esci")
        
        scelta = input("Scegli un'opzione (1-6): ")

        if scelta == '1':
            statistiche_mensili(df)
        elif scelta == '2':
            grafico_a_linee(df)
        elif scelta == '3':
            media_mobile_mensile(df)
        elif scelta == '4':
            grafico_media_mensile(df)
        elif scelta == '5':
            grafico_combinato(df)
        elif scelta == '6':
            print("Uscita dal programma.")
            break
        else:
            print("Scelta non valida. Riprova.")

menu()
