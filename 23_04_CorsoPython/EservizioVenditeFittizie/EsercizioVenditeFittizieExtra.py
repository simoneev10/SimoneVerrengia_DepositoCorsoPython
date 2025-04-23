import pandas as pd

class AnalisiVendite:
    def __init__(self, percorso_file):
        self.df = pd.read_csv(percorso_file)
        self.tabella_pivot = None
    
    def genera_pivot(self):
        #Crea la tabella pivot delle vendite medie
        self.tabella_pivot = pd.pivot_table(
            self.df,
            values='Vendite',
            index='Città',
            columns='Prodotto',
            aggfunc='mean'
        )
        return self.tabella_pivot
    
    def vendite_per_prodotto(self):
        # Calcola le vendite totali per prodotto
        return self.df.groupby('Prodotto')['Vendite'].sum().reset_index()\
                     .sort_values(by='Vendite', ascending=False)
    
    def esporta_pivot(self, percorso):
        # Esporta la tabella pivot in CSV
        if self.tabella_pivot is not None:
            self.tabella_pivot.to_csv(percorso)
            return f"File salvato in: {percorso}"
        return "Generare prima la tabella pivot!"

# Creazione oggetto
percorso_file = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\23_04_CorsoPython\EservizioVenditeFittizie\vendite_mensili.csv'
analisi = AnalisiVendite(percorso_file)

# Menù interattivo
def mostra_menu():
    print("\n=== MENU ANALISI VENDITE ===")
    print("1. Genera tabella pivot vendite medie")
    print("2. Mostra vendite totali per prodotto")
    print("3. Esporta tabella pivot in CSV")
    print("4. Esci")

while True:
    mostra_menu()
    scelta = input("Seleziona un'opzione (1-4): ")
    
    if scelta == '1':
        pivot = analisi.genera_pivot()
        print("\nTabella pivot vendite medie:")
        print(pivot.head())
    
    elif scelta == '2':
        vendite = analisi.vendite_per_prodotto()
        print("\nVendite totali per prodotto:")
        print(vendite)
    
    elif scelta == '3':
        percorso_export = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\23_04_CorsoPython\EservizioVenditeFittizie\tabellapivot.csv'
        risultato = analisi.esporta_pivot(percorso_export)
        print(f"\n{risultato}")
    
    elif scelta == '4':
        print("Arrivederci!")
        break
    
    else:
        print("Scelta non valida. Riprova.")