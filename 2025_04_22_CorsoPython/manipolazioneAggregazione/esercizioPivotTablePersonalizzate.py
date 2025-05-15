import pandas as pd

data_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\22_04_CorsoPython\manipolazioneAggregazione\vendite.csv'
df = pd.read_csv(data_path)
df['TotaleVendite'] = df['Prezzo Unitario'] * df['Quantità']

# Pivot 1: Vendite totali per prodotto e città
pivot1 = pd.pivot_table(df, 
                       values='TotaleVendite',
                       index='Prodotto',
                       columns='Città',
                       aggfunc='sum',
                       fill_value=0)

# Pivot 2: Quantità media venduta per prodotto
pivot2 = pd.pivot_table(df,
                       values='Quantità',
                       index='Prodotto',
                       aggfunc='mean')

# Menù interattivo per pivot personalizzate
def crea_pivot_personalizzato():
    print("\nCREA LA TUA PIVOT TABLE")
    print("Colonne disponibili:", list(df.columns))
    
    valori = input("Inserisci colonna valori (es: TotaleVendite): ")
    righe = input("Inserisci colonna righe (es: Prodotto): ")
    colonne = input("Inserisci colonna colonne (opzionale, premi Invio per saltare): ")
    operazione = input("Tipo di operazione (sum/mean/count): ")
    
    try:
        if colonne:
            pivot = pd.pivot_table(df,
                                 values=valori,
                                 index=righe,
                                 columns=colonne,
                                 aggfunc=operazione,
                                 fill_value=0)
        else:
            pivot = pd.pivot_table(df,
                                 values=valori,
                                 index=righe,
                                 aggfunc=operazione)
        
        print("\nRisultato:")
        print(pivot)
        
        # Salvataggio opzionale
        salva = input("\nVuoi salvare come CSV? (s/n): ")
        if salva.lower() == 's':
            nome_file = input("Nome file (senza estensione): ")
            pivot.to_csv(f"{nome_file}.csv")
            print(f"File salvato come {nome_file}.csv")
    
    except Exception as e:
        print(f"Errore: {e}")

# Analisi originali con migliorie
def analisi_base():
    print("\nANALISI BASE: ")
    print("\nVendite totali per prodotto:")
    print(df.groupby('Prodotto')['TotaleVendite'].sum())
    
    print("\nProdotto più venduto (quantità):")
    print(df.loc[df['Quantità'].idxmax()]['Prodotto'])
    
    print("\nCittà con maggior fatturato:")
    print(df.groupby('Città')['TotaleVendite'].sum().idxmax())

# Menù principale
while True:
    print("\nMENÙ PRINCIPALE")
    print("1. Visualizza pivot table predefinite")
    print("2. Crea pivot table personalizzata")
    print("3. Esegui analisi base")
    print("4. Esci")
    
    scelta = input("Seleziona un'opzione (1-4): ")
    
    if scelta == '1':
        print("\n1. Vendite per Prodotto/Città")
        print(pivot1)
        print("\n2. Quantità media per Prodotto")
        print(pivot2)
    elif scelta == '2':
        crea_pivot_personalizzato()
    elif scelta == '3':
        analisi_base()
    elif scelta == '4':
        break
    else:
        print("Scelta non valida. Riprova.")