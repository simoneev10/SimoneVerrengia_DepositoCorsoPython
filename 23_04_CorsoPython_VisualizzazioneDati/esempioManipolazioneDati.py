import pandas as pd

# Caricamento del file CSV
file_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\23_04_CorsoPython\personale_pulito_con_categorie.csv'
df = pd.read_csv(file_path)

# Metodo per ordinare tramite un valore
df_sorted = df.sort_values(by='Eta')

print(df_sorted)

# Unione di due dataFrame
#merged_df = pd.merge(df, df_csv, on='nome')

df['Eta_doppia'] = df['Eta'].apply(lambda x: x*2)
print(df)