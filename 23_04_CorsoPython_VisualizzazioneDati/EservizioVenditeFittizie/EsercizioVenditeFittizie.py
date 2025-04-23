import pandas as pd
# Leggo il file e lo trasformo in DataFrame
file_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\23_04_CorsoPython\EservizioVenditeFittizie\vendite_mensili.csv'
df = pd.read_csv(file_path)

# Tabella pivot per visualizzare le vendite medie di ciascun prodotto per città
tabellap = pd.pivot_table(df,
                          values='Vendite',
                          index='Città',
                          columns='Prodotto',
                          aggfunc='mean')
print("\nTabella pivot per visualizzare le vendite medie di ciascun prodotto per città")
print(tabellap.head(5),"\n")

# Utilizzo groupby per visualizzare le vendite totali per ogni prodotto
print("Vendite totali per ogni prodotto: ")
vendite_prodotto = df.groupby('Prodotto')['Vendite'].sum().reset_index().sort_values(by='Vendite', ascending=False)
print(vendite_prodotto)

# Esporto la tabella pivot in un csv
tabellap.to_csv(r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\23_04_CorsoPython\EservizioVenditeFittizie\tabellapivot.csv')