import pandas as pd

file_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\22_04_CorsoPython\vendite.csv'
fp = r'vendite.csv'
df = pd.read_csv(file_path)

print(df.head(5))