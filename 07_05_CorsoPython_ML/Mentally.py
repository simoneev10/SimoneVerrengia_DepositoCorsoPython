import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
import re # Importa il modulo re per le espressioni regolari

# Assicurati di avere installato le librerie necessarie:
# pip install pandas numpy seaborn matplotlib scikit-learn xgboost scikit-learn

# === Caricamento dati ===
# ATTENZIONE: Assicurati che i percorsi dei file siano corretti sul tuo sistema.
# Rimossi try-except e controlli if not empty come richiesto.
train = pd.read_csv(r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\07_05_CorsoPython_ML\MentallyStabilityOfThePerson\train.csv')
test = pd.read_csv(r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\07_05_CorsoPython_ML\MentallyStabilityOfThePerson\test.csv')

print("Dati caricati con successo!")

# --- Visualizzazione iniziale dei dati (opzionale ma utile) ---
print("\nAnteprima del DataFrame 'train':")
print(train.head())
print("\nInformazioni sul DataFrame 'train':")
print(train.info())
print("\Statistiche descrittive del DataFrame 'train':")
print(train.describe())

# === Preparazione del DataFrame per l'imputazione ===
# Creiamo una copia del DataFrame originale per lavorare.
df = train.copy()

# --- Correzione delle righe di drop ---
# Le righe seguenti nel tuo codice originale causerebbero un errore
# perché df['NomeColonna'] restituisce una Series, non il nome della colonna.
# Inoltre, stavi cercando di imputare queste colonne, quindi non dovrebbero essere droppate qui.
# Le commentiamo per ora. Se vuoi droppare colonne, usa df.drop(['NomeColonna1', 'NomeColonna2'], axis=1)

# --- Imputazione della colonna 'Profession' ---
# Applichiamo la logica:
# - Se 'Working Professional or Student' è 'Student' E 'Profession' è NaN, imputa con 'Student'.
# - Se 'Working Professional or Student' è 'Working Professional' E 'Profession' è NaN, imputa con 'Unemployed'.

# Imputa 'Profession' con 'Student' dove lo stato è 'Student' e 'Profession' è mancante
df.loc[
    (df['Working Professional or Student'] == 'Student') & (df['Profession'].isna()),
    'Profession'
] = 'Student'

# Imputa 'Profession' con 'Unemployed' dove lo stato è 'Working Professional' e 'Profession' è mancante
df.loc[
    (df['Working Professional or Student'] == 'Working Professional') & (df['Profession'].isna()),
    'Profession'
] = 'Unemployed'

# --- Imputazione condizionale con 0 per i valori non applicabili ---
# Imputiamo con 0 i mancanti nelle colonne accademiche SOLO per i 'Working Professional'.
academic_cols = ['Academic Pressure', 'CGPA', 'Study Satisfaction']
for col in academic_cols:
    # Seleziona le righe dove lo stato è 'Working Professional' e la colonna corrente è NaN
    df.loc[
        (df['Working Professional or Student'] == 'Working Professional') & (df[col].isna()),
        col
    ] = 0

# Imputiamo con 0 i mancanti nelle colonne lavorative SOLO per gli 'Student'.
work_cols = ['Work Pressure', 'Job Satisfaction']
for col in work_cols:
    # Seleziona le righe dove lo stato è 'Student' e la colonna corrente è NaN
    df.loc[
        (df['Working Professional or Student'] == 'Student') & (df[col].isna()),
        col
    ] = 0

# --- Gestione dei rimanenti mancanti nelle colonne applicabili ---
# Questi sono i mancanti nelle colonne accademiche per gli studenti
# e nelle colonne lavorative per i professionisti.
# Li imputiamo con la mediana del rispettivo sottogruppo.

# Imputa i rimanenti mancanti nelle colonne accademiche per gli 'Studenti' con la mediana del sottogruppo 'Student'.
for col in academic_cols:
    # Seleziona le righe dove lo stato è 'Student' e la colonna corrente è NaN
    condition = (df['Working Professional or Student'] == 'Student') & (df[col].isna())
    # Rimossa la condizione if df.loc[condition].shape[0] > 0:
    mediana_sottogruppo = df[df['Working Professional or Student'] == 'Student'][col].median()
    df.loc[condition, col] = mediana_sottogruppo

# Imputa i rimanenti mancanti nelle colonne lavorative per i 'Working Professional' con la mediana del sottogruppo 'Working Professional'.
for col in work_cols:
    # Seleziona le righe dove lo stato è 'Working Professional' e la colonna corrente è NaN
    condition = (df['Working Professional or Student'] == 'Working Professional') & (df[col].isna())
    # Rimossa la condizione if df.loc[condition].shape[0] > 0:
    mediana_sottogruppo = df[df['Working Professional or Student'] == 'Working Professional'][col].median()
    df.loc[condition, col] = mediana_sottogruppo

# --- Gestione dei mancanti nelle altre colonne con pochi valori assenti ---
# 'Dietary Habits' (4 mancanti)
# 'Degree' (2 mancanti)
# 'Financial Stress' (4 mancanti)

# Imputazione con la moda per 'Dietary Habits' e 'Degree' (categoriche)
# Nota: L'imputazione della moda per 'Dietary Habits' avviene prima dell'eliminazione delle righe non valide.
# Questo potrebbe imputare i 4 mancanti con 'Healthy', 'Moderate' o 'Unhealthy'.
# Se ci fossero stati valori non validi originariamente e non mancanti,
# l'imputazione con la moda non li avrebbe modificati.
for col in ['Dietary Habits', 'Degree']:
    # Rimossa la condizione if df[col].isna().any():
    # Controlla se la colonna esiste e non è vuota prima di calcolare la moda
    if col in df.columns and not df[col].empty:
        # Calcola la moda solo se ci sono valori non-null
        if df[col].notna().any():
            moda_val = df[col].mode()[0] # mode() restituisce una Series, prendiamo il primo elemento
            df[col] = df[col].fillna(moda_val)
        else:
            # Se tutti i valori sono NaN, potresti voler imputare con un valore predefinito o lasciare NaN
            print(f"Attenzione: La colonna '{col}' contiene solo valori NaN. Imputazione con moda non possibile.")
            # Ad esempio, potresti imputare con una stringa vuota o un valore specifico:
            # df[col] = df[col].fillna('Sconosciuto')

# Imputazione con la mediana per 'Financial Stress' (numerica)
# Rimossa la condizione if df['Financial Stress'].isna().any():
# Controlla se la colonna esiste e non è vuota prima di calcolare la mediana
if 'Financial Stress' in df.columns and not df['Financial Stress'].empty:
    # Calcola la mediana solo se ci sono valori non-null
    if df['Financial Stress'].notna().any():
        mediana_val = df['Financial Stress'].median()
        df['Financial Stress'] = df['Financial Stress'].fillna(mediana_val)
    else:
        print("Attenzione: La colonna 'Financial Stress' contiene solo valori NaN. Imputazione con mediana non possibile.")
        # Ad esempio, potresti imputare con 0 o un valore specifico:
        # df['Financial Stress'] = df['Financial Stress'].fillna(0)

# === Codifica delle variabili categoriche ===

# Codifica 'Gender': Male=1, Female=0
df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})
# Controlla se ci sono valori non mappati dopo la trasformazione (potrebbero diventare NaN)
if df['Gender'].isna().any():
    print("Attenzione: Valori non previsti nella colonna 'Gender' dopo la mappatura.")

# Codifica 'Working Professional or Student': Working Professional=1, Student=0
df['Working Professional or Student'] = df['Working Professional or Student'].map({'Working Professional': 1, 'Student': 0})
# Controlla se ci sono valori non mappati
if df['Working Professional or Student'].isna().any():
     print("Attenzione: Valori non previsti nella colonna 'Working Professional or Student' dopo la mappatura.")

# --- Codifica 'Sleep Duration' ---
# Funzione per mappare le stringhe di durata del sonno a valori numerici
def map_sleep_duration(duration_str):
    s = str(duration_str).strip()  # Converti in stringa e rimuovi spazi

    # Casi speciali (es. "Less than 5", "More than 8")
    if re.search(r'less.*?\d+|under.*?\d+', s, re.IGNORECASE):
        num = re.search(r'\d+', s)
        return float(num.group()) - 1 if num else np.nan  # Es. "Less than 5" → 4.0
    elif re.search(r'more.*?\d+|over.*?\d+', s, re.IGNORECASE):
        num = re.search(r'\d+', s)
        # Nota: qui restituisce num + 1 (es. More than 8 -> 9), diverso dal mapping precedente (8)
        return float(num.group()) + 1 if num else np.nan

    # Cerca intervalli (es. "5-6", "4-3", "6-7 hours")
    # Gestisce diversi tipi di trattini
    range_match = re.search(r'(\d+)\s*[-–—]\s*(\d+)', s)
    if range_match:
        num1, num2 = map(float, range_match.groups())
        return (num1 + num2) / 2  # Calcola la media (es. "5-6" → 5.5)

    # Cerca un singolo numero (es. "7 hours", "about 6.5")
    # Corretto per gestire numeri con punto decimale
    num_match = re.search(r'\d+\.?\d*', s)
    if num_match:
        return float(num_match.group())

    return np.nan  # Se non trova nulla

df['Sleep Duration'] = df['Sleep Duration'].apply(map_sleep_duration)

# Controlla se ci sono valori non mappati (dovrebbero essere NaN se la funzione non li ha riconosciuti)
if df['Sleep Duration'].isna().any():
     print("Attenzione: Valori non previsti nella colonna 'Sleep Duration' dopo la mappatura. Potrebbero essere NaN.")
     mediana_sleep = df['Sleep Duration'].median()
     df['Sleep Duration'] = df['Sleep Duration'].fillna(mediana_sleep)


# --- Pulizia e Codifica 'Degree' ---
# Pulizia: standardizza spazi e rimuove punteggiatura non necessaria
df['Degree'] = (
    df['Degree']
    .astype(str)
    .str.strip()
    .str.replace(r'\s+', ' ', regex=True) # Standardizza spazi multipli in singolo spazio
    .str.replace(r'[^\w\s.-]', '', regex=True) # Rimuove caratteri che non sono parola, spazio, punto o trattino
    .str.title() # Mette in maiuscolo la prima lettera di ogni parola
)

# Mappa in gruppi (aggiornato per gestire i valori puliti)
mapping_groups = {
    # High School / Diploma
    'Class 11': 'High School',
    'Class 12': 'High School',
    'Diploma': 'High School',
    # Bachelor
    'B.Tech': 'Bachelor', 'Btech': 'Bachelor',
    'B.Sc': 'Bachelor', 'Bsc': 'Bachelor',
    'B.Com': 'Bachelor', 'Bcom': 'Bachelor',
    'Bca': 'Bachelor', 'Ba': 'Bachelor', 'Bba': 'Bachelor', 'Bed': 'Bachelor',
    'B.Arch': 'Bachelor', 'Barch': 'Bachelor',
    'B.Pharm': 'Bachelor', 'Bpharm': 'Bachelor',
    'Bdes': 'Bachelor', 'Bfa': 'Bachelor', 'Bhm': 'Bachelor', 'Bpt': 'Bachelor',
    'Bds': 'Bachelor', 'Bams': 'Bachelor', 'Bhms': 'Bachelor', 'Bums': 'Bachelor',
    'B.A.': 'Bachelor', 'B.Com.': 'Bachelor', 'B.Sc.': 'Bachelor', # Aggiunti con punti
    'B.B.A.': 'Bachelor', 'B.C.A.': 'Bachelor', 'B.Ed.': 'Bachelor',
    # Master
    'M.Tech': 'Master', 'Mtech': 'Master',
    'M.Sc': 'Master', 'Msc': 'Master',
    'M.Com': 'Master', 'Mcom': 'Master',
    'Mca': 'Master', 'M.Ed': 'Master', 'Med': 'Master',
    'M.Pharm': 'Master', 'Mpharm': 'Master',
    'Mba': 'Master', 'Mdes': 'Master', 'Mfa': 'Master', 'Mhm': 'Master',
    'Mpt': 'Master', 'Mds': 'Master', 'Mams': 'Master', 'Mhms': 'Master',
    'M.A.': 'Master', 'M.Com.': 'Master', 'M.Sc.': 'Master', # Aggiunti con punti
    'M.B.A.': 'Master', 'M.C.A.': 'Master', 'M.Ed.': 'Master',
    # Doctorate / Professional
    'Phd': 'Doctorate', 'Mbbs': 'Doctorate', 'Md': 'Doctorate', 'Llm': 'Doctorate',
    'Ll.B.Ed': 'Doctorate', 'Ll.Ba': 'Doctorate',
    'D.Phil': 'Doctorate', 'Dr': 'Doctorate', 'Ph.D.': 'Doctorate', # Aggiunti
    'M.D.': 'Doctorate', 'L.L.M.': 'Doctorate',
    # Aggiungi altri se necessario in base all'esplorazione dei dati
}

# Applica il mapping; i non mappati diventano 'Other'
df['Degree_Group'] = df['Degree'].map(mapping_groups).fillna('Other')

# --- Codifica 'Degree_Group' con OrdinalEncoder ---
print("\nEseguendo Ordinal Encoding per la colonna 'Degree_Group'...")

# Definisci l'ordine delle categorie per il livello di istruzione
# Includiamo 'Other' come livello più basso per l'ordinamento.
degree_order = ['Other', 'High School', 'Bachelor', 'Master', 'Doctorate']

# Inizializza OrdinalEncoder con l'ordine specificato
ordinal_encoder_degree = OrdinalEncoder(categories=[degree_order])

# Fit e trasforma la colonna 'Degree_Group'
# Reshape necessario perché fit_transform si aspetta un input 2D
df['Degree_Group_Encoded'] = ordinal_encoder_degree.fit_transform(df[['Degree_Group']])

# Ora puoi, se vuoi, eliminare la colonna 'Degree' originale
# df = df.drop('Degree', axis=1)

# --- Codifica 'Dietary Habits' con OrdinalEncoder ---
print("\nValori unici nella colonna 'Dietary Habits' prima della codifica:")
print(df['Dietary Habits'].unique())

# Definisci i valori validi per 'Dietary Habits'
valid_dietary_habits = ['Unhealthy', 'Moderate', 'Healthy']

# Elimina le righe dove 'Dietary Habits' non è uno dei valori validi E non è NaN
# Ricostruiamo la condizione senza usare '~'
# Vogliamo le righe dove il valore NON è 'Unhealthy' AND NON è 'Moderate' AND NON è 'Healthy'
# E il valore NON è NaN (per evitare di eliminare i NaN originali se non imputati)
condition_not_valid = (df['Dietary Habits'] != 'Unhealthy') & \
                      (df['Dietary Habits'] != 'Moderate') & \
                      (df['Dietary Habits'] != 'Healthy') & \
                      df['Dietary Habits'].notna()

rows_to_drop = df[condition_not_valid].index


print(f"\nNumero di righe da eliminare nella colonna 'Dietary Habits': {len(rows_to_drop)}")

# Elimina le righe identificate
df = df.drop(rows_to_drop)

print(f"Numero di righe rimanenti nel DataFrame: {len(df)}")

# Ristampa i valori unici dopo l'eliminazione per verifica
print("\nValori unici nella colonna 'Dietary Habits' dopo l'eliminazione delle righe non valide:")
print(df['Dietary Habits'].unique())


# Ordine: Unhealthy < Moderate < Healthy
encoder = OrdinalEncoder(categories=[valid_dietary_habits])
# Reshape necessario perché fit_transform si aspetta un input 2D
# Assicurati che la colonna 'Dietary Habits' contenga solo i valori attesi o NaN prima di questo passaggio.
try:
    # fit_transform si aspetta un array 2D, quindi usiamo df[['Dietary Habits']]
    # Aggiungiamo handle_unknown='use_encoded_value' e unknown_value=-1 per gestire eventuali NaN
    # anche se con l'eliminazione delle righe non dovrebbero esserci valori inattesi.
    # Se ci fossero ancora NaN dopo l'imputazione e non fossero stati eliminati,
    # unknown_value=-1 li codificherebbe come -1.
    # Tuttavia, dato che l'imputazione con la moda è avvenuta prima, i NaN dovrebbero essere stati riempiti.
    # Quindi, con l'eliminazione delle righe non valide, questa colonna dovrebbe contenere SOLO i 3 valori validi.
    # Pertanto, handle_unknown non è strettamente necessario se l'eliminazione funziona come previsto.
    # Lo lasciamo per robustezza, ma unknown_value=-1 potrebbe non essere il comportamento desiderato per i NaN.
    # Data la tua richiesta di eliminare le righe *non* nella casistica, anche i NaN non nella casistica
    # (se ce ne fossero ancora) verrebbero eliminati.

    # Modifica per usare solo i valori validi definiti
    encoder = OrdinalEncoder(categories=[valid_dietary_habits])
    df['Dietary Habits'] = encoder.fit_transform(df[['Dietary Habits']])

    print("\nCodifica 'Dietary Habits' completata con successo.")
except ValueError as e:
    print(f"\nErrore durante la codifica di 'Dietary Habits': {e}")
    print("Controlla i valori unici stampati sopra. La colonna 'Dietary Habits' contiene valori non previsti.")
    # Potresti voler ispezionare il DataFrame in questo punto per capire da dove provengono i valori errati.

# Codifica 'Have you ever had suicidal thoughts ?': Yes=1, No=0
df['Have you ever had suicidal thoughts ?'] = df['Have you ever had suicidal thoughts ?'].map({'Yes': 1, 'No': 0})
# Controlla se ci sono valori non mappati
if df['Have you ever had suicidal thoughts ?'].isna().any():
     print("Attenzione: Valori non previsti nella colonna 'Have you ever had suicidal thoughts ?' dopo la mappatura.")


# Codifica 'Family History of Mental Illness': Yes=1, No=0
df['Family History of Mental Illness'] = df['Family History of Mental Illness'].map({'Yes': 1, 'No': 0})
# Controlla se ci sono valori non mappati
if df['Family History of Mental Illness'].isna().any():
     print("Attenzione: Valori non previsti nella colonna 'Family History of Mental Illness' dopo la mappatura.")


# --- Verifica dei risultati finali ---
print("\nDataFrame dopo TUTTE le trasformazioni (imputazione, eliminazione righe e codifica):")
print(df.head())
print("\nInformazioni sul DataFrame dopo TUTTE le trasformazioni:")
print(df.info()) # Controlla i tipi di dato e i conteggi non-null

# # Ristampa i valori unici dopo l'eliminazione per verifica
# print("\nValori unici nella colonna 'City':")
# print(df['City'].unique())
# print("Numero di valori unici:", len(df['City'].unique()))

print("\nValori unici nella colonna 'Profession':")
print(df['Profession'].unique())
print("Numero di valori unici:", len(df['Profession'].unique()))

# --- Raggruppamento e Codifica 'Profession' ---
print("\nRaggruppamento e Codifica della colonna 'Profession'...")

# Definisci la mappatura Profession -> Professional_Group
professional_map = {
    'Chef': 'Culinary',
    'Teacher': 'Education',
    'Business Analyst': 'Business/Consulting',
    'Finanancial Analyst': 'Finance', # Corretto typo
    'Chemist': 'Science',
    'Electrician': 'Trades',
    'Software Engineer': 'IT/Tech',
    'Data Scientist': 'IT/Tech',
    'Plumber': 'Trades',
    'Marketing Manager': 'Marketing/Sales',
    'Accountant': 'Finance',
    'Entrepreneur': 'Business/Consulting',
    'HR Manager': 'Human Resources',
    'UX/UI Designer': 'Creative',
    'Content Writer': 'Creative',
    'Educational Consultant': 'Education',
    'Civil Engineer': 'Engineering',
    'Manager': 'Management',
    'Pharmacist': 'Healthcare',
    'Financial Analyst': 'Finance',
    'Architect': 'Architecture',
    'Mechanical Engineer': 'Engineering',
    'Customer Support': 'Customer Service',
    'Consultant': 'Business/Consulting',
    'Judge': 'Legal',
    'Researcher': 'Science',
    'Pilot': 'Transportation',
    'Graphic Designer': 'Creative',
    'Travel Consultant': 'Tourism',
    'Digital Marketer': 'Marketing/Sales',
    'Lawyer': 'Legal',
    'Research Analyst': 'Science',
    'Sales Executive': 'Marketing/Sales',
    'Doctor': 'Healthcare',
    'Investment Banker': 'Finance',
    'Family Consultant': 'Social Services',
    # Le seguenti sembrano essere titoli di studio, nomi o categorie generiche.
    # Le mappiamo a 'Other' o a gruppi più specifici se appropriato.
    'B.Com': 'Other', # Titolo di studio, non professione
    'BE': 'Other',    # Titolo di studio, non professione
    'Yogesh': 'Other', # Nome
    'Dev': 'Other',    # Nome/Categoria generica
    'MBA': 'Other',    # Titolo di studio, non professione
    'LLM': 'Other',    # Titolo di studio, non professione
    'BCA': 'Other',    # Titolo di studio, non professione
    'Academic': 'Education', # Categoria generica -> Education
    'Profession': 'Other', # Categoria generica -> Other
    'FamilyVirar': 'Other', # Sembra una combinazione di nome e città
    'City Manager': 'Management', # Categoria specifica -> Management
    'BBA': 'Other',    # Titolo di studio, non professione
    'Medical Doctor': 'Healthcare', # Sinonimo di Doctor -> Healthcare
    'MBBS': 'Other',    # Titolo di studio, non professione
    'Patna': 'Other',  # Città
    'Unveil': 'Other', # Sembra un nome/parola generica
    'B.Ed': 'Other',    # Titolo di studio, non professione
    'Nagpur': 'Other', # Città
    'Moderate': 'Other', # Valore da Dietary Habits
    'M.Ed': 'Other',    # Titolo di studio, non professione
    'Analyst': 'Business/Consulting', # Categoria generica -> Business/Consulting
    'Pranav': 'Other', # Nome
    'Visakhapatnam': 'Other', # Città
    'PhD': 'Other',    # Titolo di studio, non professione
    'Yuvraj': 'Other'  # Nome
}

# Applica la mappatura e gestisci i casi non riconosciuti
df['Professional_Group'] = df['Profession'].map(professional_map).fillna('Other')

# --- Codifica 'Professional_Group' con LabelEncoder ---
print("\nEseguendo Label Encoding per la colonna 'Professional_Group'...")

# Inizializza LabelEncoder
label_encoder_profession = LabelEncoder()

# Fit e trasforma la colonna 'Professional_Group'
df['Professional_Group_Encoded'] = label_encoder_profession.fit_transform(df['Professional_Group'])

# Puoi vedere la mappatura creata dal LabelEncoder (utile per interpretare i risultati)
print("\nMappatura Label Encoding per 'Professional_Group':")
# Crea una Series per mostrare la mappatura
label_mapping_profession = pd.Series(label_encoder_profession.classes_, name='Professional_Group').to_frame()
label_mapping_profession['Encoded_Value'] = label_encoder_profession.transform(label_encoder_profession.classes_)
print(label_mapping_profession)

# Opzionale: Rimuovi la colonna originale 'Profession' e 'Professional_Group' se non più necessarie
# df = df.drop(['Profession', 'Professional_Group'], axis=1)

# KNN per raggruppare in base alla città (miglioria del metodo manuale)

# --- Definizione e Mappatura delle Regioni ---
# Definisci la mappatura City → Region
region_map = {
    # North-East India
    'Patna': 'North-East India',
    'Varanasi': 'North-East India',
    # North-West India (resto del vecchio 'North')
    'Meerut': 'North-West India', 'Ludhiana': 'North-West India',
    'Agra': 'North-West India', 'Kanpur': 'North-West India',
    'Jaipur': 'North-West India', 'Lucknow': 'North-West India',
    'Srinagar': 'North-West India', 'Delhi': 'North-West India',
    'Ghaziabad': 'North-West India', 'Faridabad': 'North-West India',
    # West-Gujarat
    'Surat': 'West-Gujarat', 'Vadodara': 'West-Gujarat',
    'Rajkot': 'West-Gujarat', 'Ahmedabad': 'West-Gujarat',
    # West-Maharashtra
    'Kalyan': 'West-Maharashtra', 'Vasai-Virar': 'West-Maharashtra',
    'Mumbai': 'West-Maharashtra', 'Pune': 'West-Maharashtra',
    'Nashik': 'West-Maharashtra', 'Thane': 'West-Maharashtra',
    # Central India (unchanged)
    'Indore': 'Central India', 'Bhopal': 'Central India', 'Nagpur': 'Central India',
    # East India (unchanged)
    'Kolkata': 'East India', 'Visakhapatnam': 'East India',
    # South India (unchanged)
    'Bangalore': 'South India', 'Chennai': 'South India', 'Hyderabad': 'South India'
    # Nota: Ho rimosso le città aggiunte precedentemente nel Sud per usare solo quelle fornite nella nuova mappa.
}

# Applica la mappatura e gestisci i casi non riconosciuti
df['Region'] = df['City'].map(region_map).fillna('Other')

# Raggruppa e conta per regione (opzionale)
print("\nConteggio delle città per Regione:")
region_counts = df['Region'].value_counts()
print(region_counts)

# (Opzionale) Se vuoi vedere il dettaglio per regione
# print("\nDettaglio delle città per Regione:")
# for region, group in df.groupby('Region'):
#     print(f"\n=== {region} ({len(group)} records) ===")
#     print(group['City'].value_counts().head()) # Stampa solo le prime 5 città per regione per brevità


# --- Codifica 'Region' con LabelEncoder ---
print("\nEseguendo Label Encoding per la colonna 'Region'...")

# Inizializza LabelEncoder
label_encoder = LabelEncoder()

# Fit e trasforma la colonna 'Region'
df['Region_Encoded'] = label_encoder.fit_transform(df['Region'])

# Opzionale: Rimuovi la colonna originale 'Region' e 'City' se non più necessarie
# df = df.drop(['Region', 'City'], axis=1)

# Puoi vedere la mappatura creata dal LabelEncoder (utile per interpretare i risultati)
print("\nMappatura Label Encoding per 'Region':")
# Crea una Series per mostrare la mappatura
label_mapping = pd.Series(label_encoder.classes_, name='Region').to_frame()
label_mapping['Encoded_Value'] = label_encoder.transform(label_encoder.classes_)
print(label_mapping)


# --- Verifica dei risultati finali ---
print("\nDataFrame dopo TUTTE le trasformazioni (imputazione, eliminazione righe, codifica):")
print(df.head())
print("\nInformazioni sul DataFrame dopo TUTTE le trasformazioni:")
print(df.info()) # Controlla i tipi di dato e i conteggi non-null

# === Esportazione del DataFrame in CSV ===
# Esporta il DataFrame risultante in un file CSV chiamato 'prova.csv'
try:
    file_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\07_05_CorsoPython_ML\MentallyStabilityOfThePerson\prova.csv'
    df.to_csv(file_path, index=False) # index=False per non scrivere l'indice del DataFrame come colonna
    print("\nDataFrame esportato con successo in 'prova.csv'")
except Exception as e:
    print(f"\nErrore durante l'esportazione del DataFrame: {e}")

df_clean = df.copy()

df_clean = df_clean.drop(columns=['City','Name','id','Profession', 'Degree', 'Degree_Group', 'Professional_Group', 'Region'])

try:
    file_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\07_05_CorsoPython_ML\MentallyStabilityOfThePerson\filepulito.csv'
    df_clean.to_csv(file_path, index=False) # index=False per non scrivere l'indice del DataFrame come colonna
    print("\nDataFrame esportato con successo in 'filepulito.csv'")
except Exception as e:
    print(f"\nErrore durante l'esportazione del DataFrame: {e}")
