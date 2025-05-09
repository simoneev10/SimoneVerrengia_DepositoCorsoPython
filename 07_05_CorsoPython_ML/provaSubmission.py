import re
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt
from xgboost import XGBClassifier # Usiamo XGBClassifier per la classificazione
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score, mean_squared_error # Questi sono per regressione, potremmo rimuoverli per classificazione
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import GridSearchCV, train_test_split
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
# Rimuoviamo import non necessari per classificazione se non usati altrove
# from xgboost import XGBRegressor
# from sklearn.linear_model import LinearRegression


# Caricamento dei dati dal file CSV
# Assicurati che il percorso dei file sia corretto per il tuo ambiente
train_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\07_05_CorsoPython_ML\MentallyStabilityOfThePerson\train.csv'
test_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\07_05_CorsoPython_ML\MentallyStabilityOfThePerson\test.csv'

train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)

print("Dati caricati con successo!")

# --- Visualizzazione iniziale dei dati di training ---
print("\nAnteprima del DataFrame 'train_df':")
print(train_df.head())
print("\nInformazioni sul DataFrame 'train_df':")
print(train_df.info())
print("\Statistiche descrittive del DataFrame 'train_df':")
print(train_df.describe())

# Salva gli ID del test set originale per il file di submission
original_test_ids = test_df['id'].copy()

# Calcola la moda di 'Dietary Habits' dal set di training PRIMA di qualsiasi rimozione/imputazione
# Questo valorerà usato per imputare i valori non validi nel test set
train_dietary_mode = train_df['Dietary Habits'].mode()[0]
print(f"\nModa di 'Dietary Habits' dal set di training (originale): '{train_dietary_mode}'")


# Funzione per applicare le stesse trasformazioni a un DataFrame (train o test)
def preprocess_data(df, is_test_set=False, train_mode_dietary=None):
    df_processed = df.copy()

    # --- Imputazione della colonna 'Profession' ---
    df_processed.loc[
        (df_processed['Working Professional or Student'] == 'Student') & (df_processed['Profession'].isna()),
        'Profession'
    ] = 'Student'
    df_processed.loc[
        (df_processed['Working Professional or Student'] == 'Working Professional') & (df_processed['Profession'].isna()),
        'Profession'
    ] = 'Unemployed'

    # --- Imputazione condizionale con 0 per i valori non applicabili ---
    academic_cols = ['Academic Pressure', 'CGPA', 'Study Satisfaction']
    for col in academic_cols:
        df_processed.loc[
            (df_processed['Working Professional or Student'] == 'Working Professional') & (df_processed[col].isna()),
            col
        ] = 0

    work_cols = ['Work Pressure', 'Job Satisfaction']
    for col in work_cols:
        df_processed.loc[
            (df_processed['Working Professional or Student'] == 'Student') & (df_processed[col].isna()),
            col
        ] = 0

    # --- Gestione dei rimanenti mancanti con la mediana del sottogruppo ---
    for col in academic_cols:
        condition = (df_processed['Working Professional or Student'] == 'Student') & (df_processed[col].isna())
        if df_processed.loc[condition].shape[0] > 0: # Controlla se ci sono righe da imputare
             mediana_sottogruppo = df_processed[df_processed['Working Professional or Student'] == 'Student'][col].median()
             df_processed.loc[condition, col] = mediana_sottogruppo

    for col in work_cols:
        condition = (df_processed['Working Professional or Student'] == 'Working Professional') & (df_processed[col].isna())
        if df_processed.loc[condition].shape[0] > 0: # Controlla se ci sono righe da imputare
            mediana_sottogruppo = df_processed[df_processed['Working Professional or Student'] == 'Working Professional'][col].median()
            df_processed.loc[condition, col] = mediana_sottogruppo


    # --- Gestione dei mancanti nelle altre colonne con pochi valori assenti ---
    for col in ['Degree', 'Financial Stress']: # Rimosso 'Dietary Habits' da qui
        if col in df_processed.columns and not df_processed[col].empty and df_processed[col].notna().any():
             if df_processed[col].dtype == 'object': # Se categorica, usa la moda
                 moda_val = df_processed[col].mode()[0]
                 df_processed[col] = df_processed[col].fillna(moda_val)
             else: # Se numerica, usa la mediana
                 mediana_val = df_processed[col].median()
                 df_processed[col] = df_processed[col].fillna(mediana_val)


    # --- Pulizia e Imputazione/Rimozione di 'Dietary Habits' ---
    valid_dietary_habits = ['Unhealthy', 'Moderate', 'Healthy']
    condition_not_valid = (df_processed['Dietary Habits'] != 'Unhealthy') & \
                          (df_processed['Dietary Habits'] != 'Moderate') & \
                          (df_processed['Dietary Habits'] != 'Healthy') & \
                          df_processed['Dietary Habits'].notna()

    if is_test_set:
        # Nel set di test, imputa i valori non validi con la moda del training set
        if train_mode_dietary is not None:
            df_processed.loc[condition_not_valid, 'Dietary Habits'] = train_mode_dietary
            print(f"Imputati {condition_not_valid.sum()} valori non validi in 'Dietary Habits' (Test Set) con '{train_mode_dietary}'.")
        else:
             print("Attenzione: Moda del training set per 'Dietary Habits' non fornita per l'imputazione del test set.")
             # Potresti voler gestire questo caso diversamente, ad es. imputare con un placeholder
             df_processed.loc[condition_not_valid, 'Dietary Habits'] = 'Unknown' # Esempio: imputa con 'Unknown'
    else:
        # Nel set di training, rimuovi le righe con valori non validi
        rows_to_drop = df_processed[condition_not_valid].index
        print(f"\nNumero di righe da eliminare nella colonna 'Dietary Habits' (Train Set): {len(rows_to_drop)}")
        df_processed = df_processed.drop(rows_to_drop)
        print(f"Numero di righe rimanenti nel DataFrame (Train Set): {len(df_processed)}")


    # --- Resetta l'indice dopo aver rimosso le righe (solo se non è il test set) ---
    if not is_test_set:
         df_processed = df_processed.reset_index(drop=True)


    # === Codifica delle variabili categoriche ===

    # Codifica 'Gender': Male=1, Female=0
    df_processed['Gender'] = df_processed['Gender'].map({'Male': 1, 'Female': 0})

    # Codifica 'Working Professional or Student': Working Professional=1, Student=0
    df_processed['Working Professional or Student'] = df_processed['Working Professional or Student'].map({'Working Professional': 1, 'Student': 0})

    # --- Codifica 'Sleep Duration' ---
    def map_sleep_duration(duration_str):
        s = str(duration_str).strip()
        if re.search(r'less.*?\d+|under.*?\d+', s, re.IGNORECASE):
            num = re.search(r'\d+', s)
            return float(num.group()) - 1 if num else np.nan
        elif re.search(r'more.*?\d+|over.*?\d+', s, re.IGNORECASE):
            num = re.search(r'\d+', s)
            return float(num.group()) + 1 if num else np.nan
        range_match = re.search(r'(\d+)\s*[-–—]\s*(\d+)', s)
        if range_match:
            num1, num2 = map(float, range_match.groups())
            return (num1 + num2) / 2
        num_match = re.search(r'\d+\.?\d*', s)
        if num_match:
            return float(num_match.group())
        return np.nan

    df_processed['Sleep Duration'] = df_processed['Sleep Duration'].apply(map_sleep_duration)
    if df_processed['Sleep Duration'].isna().any():
         mediana_sleep = df_processed['Sleep Duration'].median()
         df_processed['Sleep Duration'] = df_processed['Sleep Duration'].fillna(mediana_sleep)


    # --- Pulizia e Codifica 'Degree' ---
    df_processed['Degree'] = (
        df_processed['Degree']
        .astype(str)
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
        .str.replace(r'[^\w\s.-]', '', regex=True)
        .str.title()
    )

    mapping_groups = {
        'Class 11': 'High School', 'Class 12': 'High School', 'Diploma': 'High School',
        'B.Tech': 'Bachelor', 'Btech': 'Bachelor', 'B.Sc': 'Bachelor', 'Bsc': 'Bachelor',
        'B.Com': 'Bachelor', 'Bcom': 'Bachelor', 'Bca': 'Bachelor', 'Ba': 'Bachelor',
        'Bba': 'Bachelor', 'Bed': 'Bachelor', 'B.Arch': 'Bachelor', 'Barch': 'Bachelor',
        'B.Pharm': 'Bachelor', 'Bpharm': 'Bachelor', 'Bdes': 'Bachelor', 'Bfa': 'Bachelor',
        'Bhm': 'Bachelor', 'Bpt': 'Bachelor', 'Bds': 'Bachelor', 'Bams': 'Bachelor',
        'Bhms': 'Bachelor', 'Bums': 'Bachelor', 'B.A.': 'Bachelor', 'B.Com.': 'Bachelor',
        'B.Sc.': 'Bachelor', 'B.B.A.': 'Bachelor', 'B.C.A.': 'Bachelor', 'B.Ed.': 'Bachelor',
        'M.Tech': 'Master', 'Mtech': 'Master', 'M.Sc': 'Master', 'Msc': 'Master',
        'M.Com': 'Master', 'Mcom': 'Master', 'Mca': 'Master', 'M.Ed': 'Master', 'Med': 'Master',
        'M.Pharm': 'Master', 'Mpharm': 'Master', 'Mba': 'Master', 'Mdes': 'Master',
        'Mfa': 'Master', 'Mhm': 'Master', 'Mpt': 'Master', 'Mds': 'Master', 'Mams': 'Master',
        'Mhms': 'Master', 'M.A.': 'Master', 'M.Com.': 'Master', 'M.Sc.': 'Master',
        'M.B.A.': 'Master', 'M.C.A.': 'Master', 'M.Ed.': 'Master',
        'Phd': 'Doctorate', 'Mbbs': 'Doctorate', 'Md': 'Doctorate', 'Llm': 'Doctorate',
        'Ll.B.Ed': 'Doctorate', 'Ll.Ba': 'Doctorate', 'D.Phil': 'Doctorate', 'Dr': 'Doctorate',
        'Ph.D.': 'Doctorate', 'M.D.': 'Doctorate', 'L.L.M.': 'Doctorate',
        'Academic': 'Education', 'City Manager': 'Management', 'Medical Doctor': 'Healthcare',
        'Analyst': 'Business/Consulting'
    }
    df_processed['Degree_Group'] = df_processed['Degree'].map(mapping_groups).fillna('Other')


    # --- Raggruppamento e Codifica 'Profession' ---
    professional_map = {
        'Chef': 'Culinary', 'Teacher': 'Education', 'Business Analyst': 'Business/Consulting',
        'Finanancial Analyst': 'Finance', 'Chemist': 'Science', 'Electrician': 'Trades',
        'Software Engineer': 'IT/Tech', 'Data Scientist': 'IT/Tech', 'Plumber': 'Trades',
        'Marketing Manager': 'Marketing/Sales', 'Accountant': 'Finance', 'Entrepreneur': 'Business/Consulting',
        'HR Manager': 'Human Resources', 'UX/UI Designer': 'Creative', 'Content Writer': 'Creative',
        'Educational Consultant': 'Education', 'Civil Engineer': 'Engineering', 'Manager': 'Management',
        'Pharmacist': 'Healthcare', 'Financial Analyst': 'Finance', 'Architect': 'Architecture',
        'Mechanical Engineer': 'Engineering', 'Customer Support': 'Customer Service', 'Consultant': 'Business/Consulting',
        'Judge': 'Legal', 'Researcher': 'Science', 'Pilot': 'Transportation', 'Graphic Designer': 'Creative',
        'Travel Consultant': 'Tourism', 'Digital Marketer': 'Marketing/Sales', 'Lawyer': 'Legal',
        'Research Analyst': 'Science', 'Sales Executive': 'Marketing/Sales', 'Doctor': 'Healthcare',
        'Investment Banker': 'Finance', 'Family Consultant': 'Social Services',
        'B.Com': 'Other', 'BE': 'Other', 'Yogesh': 'Other', 'Dev': 'Other', 'MBA': 'Other', 'LLM': 'Other',
        'BCA': 'Other', 'Profession': 'Other', 'FamilyVirar': 'Other', 'BBA': 'Other', 'MBBS': 'Other',
        'Patna': 'Other', 'Unveil': 'Other', 'B.Ed': 'Other', 'Nagpur': 'Other', 'Moderate': 'Other',
        'M.Ed': 'Other', 'Pranav': 'Other', 'Visakhapatnam': 'Other', 'PhD': 'Other', 'Yuvraj': 'Other'
    }
    df_processed['Professional_Group'] = df_processed['Profession'].map(professional_map).fillna('Other')


    # --- Definizione e Mappatura delle Regioni ---
    region_map = {
        'Patna': 'North-East India', 'Varanasi': 'North-East India',
        'Meerut': 'North-West India', 'Ludhiana': 'North-West India', 'Agra': 'North-West India',
        'Kanpur': 'North-West India', 'Jaipur': 'North-West India', 'Lucknow': 'North-West India',
        'Srinagar': 'North-West India', 'Delhi': 'North-West India', 'Ghaziabad': 'North-West India',
        'Faridabad': 'North-West India',
        'Surat': 'West-Gujarat', 'Vadodara': 'West-Gujarat', 'Rajkot': 'West-Gujarat', 'Ahmedabad': 'West-Gujarat',
        'Kalyan': 'West-Maharashtra', 'Vasai-Virar': 'West-Maharashtra', 'Mumbai': 'West-Maharashtra',
        'Pune': 'West-Maharashtra', 'Nashik': 'West-Maharashtra', 'Thane': 'West-Maharashtra',
        'Indore': 'Central India', 'Bhopal': 'Central India', 'Nagpur': 'Central India',
        'Kolkata': 'East India', 'Visakhapatnam': 'East India',
        'Bangalore': 'South India', 'Chennai': 'South India', 'Hyderabad': 'South India'
    }
    df_processed['Region'] = df_processed['City'].map(region_map).fillna('Other')

    # --- Aggiunto: Conversione esplicita a int per colonne binarie ---
    binary_cols = ['Gender', 'Working Professional or Student', 'Have you ever had suicidal thoughts ?', 'Family History of Mental Illness']
    for col in binary_cols:
        # Controlla se la colonna esiste prima di tentare la conversione
        if col in df_processed.columns:
            # Assicurati che non ci siano NaN prima della conversione a int
            if df_processed[col].isnull().any():
                print(f"Attenzione: Trovati NaN nella colonna '{col}' prima della conversione a int. Imputazione con 0.")
                df_processed[col] = df_processed[col].fillna(0) # Imputa NaN con 0 (o un altro valore appropriato)

            # Controlla se ci sono valori non numerici dopo la mappatura (dovrebbero essere solo 0 o 1 ora)
            # Questo è un controllo di debug aggiuntivo
            non_numeric_values = df_processed[col][~pd.to_numeric(df_processed[col], errors='coerce').notna()].unique()
            if len(non_numeric_values) > 0:
                 print(f"Attenzione: Trovati valori non numerici in '{col}' prima della conversione a int: {non_numeric_values}")
                 # Potrebbe essere necessario aggiungere qui una logica per gestire questi valori,
                 # ad esempio mappandoli a 0 o 1 o imputandoli.
                 # Per ora, procediamo con la conversione, che potrebbe fallire se i non numerici non sono NaN.


            # Converti a int. Usa errors='coerce' per trasformare valori non convertibili in NaN,
            # anche se l'imputazione precedente dovrebbe aver gestito i NaN.
            df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce').astype('int', errors='ignore')
            # Se errors='ignore', i non convertibili rimangono nel loro formato originale,
            # il che potrebbe causare problemi successivi. Preferiamo 'coerce' e gestire i NaN risultanti.
            df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
            # Dopo coerce, se ci sono ancora NaN (da valori non convertibili), imputali
            if df_processed[col].isnull().any():
                 print(f"Attenzione: Trovati NaN in '{col}' dopo la conversione numerica. Imputazione con 0.")
                 df_processed[col] = df_processed[col].fillna(0)

            # Ora converti in int (dovrebbe essere sicuro)
            df_processed[col] = df_processed[col].astype(int)

    # --- Fine Aggiunta ---


    return df_processed

# Applica il pre-processing ai dati di training e test
# Passiamo la moda di Dietary Habits del training set al pre-processing del test set
df_train_processed = preprocess_data(train_df, is_test_set=False)
df_test_processed = preprocess_data(test_df, is_test_set=True, train_mode_dietary=train_dietary_mode)

# --- Aggiunto: Imputazione dei NaN nelle colonne categoriche PRIMA di fittare gli encoder (solo training) ---
# Queste colonne saranno codificate e usate come feature
categorical_cols_to_encode = ['Degree_Group', 'Dietary Habits', 'Professional_Group', 'Region']
for col in categorical_cols_to_encode:
    if df_train_processed[col].isnull().any():
        print(f"\nAttenzione: Trovati valori NaN nella colonna '{col}' (Train Set) prima della codifica. Imputazione con la moda.")
        # Calcola la moda sul set di training processato (dopo le rimozioni/imputazioni iniziali)
        mode_val = df_train_processed[col].mode()[0]
        df_train_processed[col] = df_train_processed[col].fillna(mode_val)
        print(f"Imputata colonna '{col}' (Train Set) con moda: '{mode_val}'")

# --- Fine Aggiunta ---

# Inizializza e fitta gli encoder sulle colonne categoriche del TRAIN set (ORA SENZA NaN)
ordinal_encoder_degree = OrdinalEncoder(categories=[['Other', 'High School', 'Bachelor', 'Master', 'Doctorate']])
encoder_dietary = OrdinalEncoder(categories=[['Unhealthy', 'Moderate', 'Healthy']])
label_encoder_profession = LabelEncoder()
label_encoder_region = LabelEncoder()


# Fit gli encoder sul TRAIN set processato
df_train_processed['Degree_Group_Encoded'] = ordinal_encoder_degree.fit_transform(df_train_processed[['Degree_Group']])
df_train_processed['Dietary Habits_Encoded'] = encoder_dietary.fit_transform(df_train_processed[['Dietary Habits']]) # Rinomina per chiarezza
df_train_processed['Professional_Group_Encoded'] = label_encoder_profession.fit_transform(df_train_processed['Professional_Group'])
df_train_processed['Region_Encoded'] = label_encoder_region.fit_transform(df_train_processed['Region'])


# --- Aggiunto: Imputazione dei NaN nelle colonne categoriche del test set PRIMA della trasformazione ---
# Usa le mode calcolate dal training set processato per l'imputazione nel test set
train_degree_group_mode = df_train_processed['Degree_Group'].mode()[0]
train_dietary_mode_processed = df_train_processed['Dietary Habits'].mode()[0] # Moda dal TRAIN *processato*
train_profession_mode = df_train_processed['Professional_Group'].mode()[0]
train_region_mode = df_train_processed['Region'].mode()[0]


if df_test_processed['Degree_Group'].isnull().any():
    print(f"\nAttenzione: Trovati valori NaN nella colonna 'Degree_Group' (Test Set) prima della codifica. Imputazione con la moda del training set.")
    df_test_processed['Degree_Group'] = df_test_processed['Degree_Group'].fillna(train_degree_group_mode)

# Aggiunto: Controllo e imputazione specifica per 'Dietary Habits' nel test set
print(f"\nVerifica 'Dietary Habits' (Test Set) prima della codifica:")
print(df_test_processed['Dietary Habits'].dtype)
print(df_test_processed['Dietary Habits'].unique())
if df_test_processed['Dietary Habits'].isnull().any():
    print(f"\nAttenzione: Trovati valori NaN nella colonna 'Dietary Habits' (Test Set) prima della codifica. Imputazione con la moda del training set processato.")
    df_test_processed['Dietary Habits'] = df_test_processed['Dietary Habits'].fillna(train_dietary_mode_processed)
    print(f"Imputata colonna 'Dietary Habits' (Test Set) con moda del training set processato: '{train_dietary_mode_processed}'")


if df_test_processed['Professional_Group'].isnull().any():
    print(f"\nAttenzione: Trovati valori NaN nella colonna 'Professional_Group' (Test Set) prima della codifica. Imputazione con la moda del training set.")
    df_test_processed['Professional_Group'] = df_test_processed['Professional_Group'].fillna(train_profession_mode)


if df_test_processed['Region'].isnull().any():
    print(f"\nAttenzione: Trovati valori NaN nella colonna 'Region' (Test Set) prima della codifica. Imputazione con la moda del training set.")
    df_test_processed['Region'] = df_test_processed['Region'].fillna(train_region_mode)

# --- Fine Aggiunta ---


# Trasforma il TEST set usando gli encoder fittati sul TRAIN
df_test_processed['Degree_Group_Encoded'] = ordinal_encoder_degree.transform(df_test_processed[['Degree_Group']])
df_test_processed['Dietary Habits_Encoded'] = encoder_dietary.transform(df_test_processed[['Dietary Habits']]) # Rinomina per chiarezza
df_test_processed['Professional_Group_Encoded'] = label_encoder_profession.transform(df_test_processed['Professional_Group'])
df_test_processed['Region_Encoded'] = label_encoder_region.transform(df_test_processed[['Region']])


# Rinomina la colonna per coerenza prima di dropparla
df_train_processed = df_train_processed.rename(columns={'Have you ever had suicidal thoughts ?': 'SuicidalThoughts'})
df_test_processed = df_test_processed.rename(columns={'Have you ever had suicidal thoughts ?': 'SuicidalThoughts'})


# --- Salva gli ID dal DataFrame di test *dopo* il pre-processing ---
# Questi ID corrispondono alle righe rimanenti dopo la pulizia (che ora dovrebbero essere tutte 93800)
processed_test_ids = df_test_processed['id'].copy()


# Rimuovi le colonne non necessarie da entrambi i set
# Assicurati di rimuovere le colonne originali *non* codificate
cols_to_drop = ['City','Name','id','Profession', 'Degree', 'Degree_Group', 'Professional_Group', 'Region', 'Dietary Habits'] # Aggiunto 'Dietary Habits' originale
df_clean_train = df_train_processed.drop(columns=cols_to_drop)
df_clean_test = df_test_processed.drop(columns=cols_to_drop) # Rimuovi anche dal test set


# --- Aggiunto: Debug prints per controllare i tipi di dato e i valori unici prima della matrice di correlazione ---
print("\n--- Debug: Controllo tipi di dato e valori unici in df_clean_train prima della matrice di correlazione ---")
print(df_clean_train.info())
for col in ['Gender', 'Working Professional or Student', 'SuicidalThoughts', 'Family History of Mental Illness']:
     if col in df_clean_train.columns:
        print(f"\nColonna '{col}':")
        print(f"  Dtype: {df_clean_train[col].dtype}")
        print(f"  Valori unici: {df_clean_train[col].unique()}")
# --- Fine Aggiunta ---


# --- Visualizzazione della Matrice di Correlazione (sul training data pulito) ---
# Assicurati che tutte le colonne incluse qui siano numeriche
numeric_cols_clean = [col for col in df_clean_train.columns if df_clean_train[col].dtype != 'object']

# Aggiungi la colonna target se presente
if 'Depression' in df_clean_train.columns:
    if 'Depression' not in numeric_cols_clean: # Evita duplicati se già numerica
        numeric_cols_clean.append('Depression')


print(f"\nColonne numeriche utilizzate per la matrice di correlazione: {numeric_cols_clean}")


#calcolo la Pearson-corr
corr_matrix = df_clean_train[numeric_cols_clean].corr()

plt.figure(figsize=(8,6))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlation matrix (variabili continue)")
plt.show()


# Funzione per eliminare variabili in base a VIF e p-value (fittata solo sul TRAIN)
def elimina_variabili_vif_pvalue(X_train, y_train, vif_threshold=5.0, pvalue_threshold=0.05):
    X_current = X_train.copy()

    # --- Controllo e gestione di NaN/Inf prima di OLS ---
    X_current = X_current.replace([np.inf, -np.inf], np.nan)
    if X_current.isnull().any().any():
        print("\nAttenzione: Trovati valori NaN in X_train. Imputazione con la mediana.")
        for col in X_current.columns:
            if X_current[col].isnull().any():
                mediana = X_current[col].median()
                X_current[col] = X_current[col].fillna(mediana)
                print(f"Imputata colonna '{col}' (Train Set) con mediana: {mediana}")

    # --- Controllo e gestione di NaN/Inf nel target (y_train) ---
    # Se il target contiene NaN, potresti voler rimuovere le righe corrispondenti
    if y_train.isnull().any():
        print("\nAttenzione: Trovati valori NaN nel target (y_train). Rimozione delle righe corrispondenti.")
        nan_rows_index = y_train[y_train.isnull()].index
        X_current = X_current.drop(nan_rows_index)
        y_train = y_train.drop(nan_rows_index)
        print(f"Rimosse {len(nan_rows_index)} righe con NaN nel target.")


    initial_features = set(X_current.columns)
    removed_features = set()

    while True:
        X_const = sm.add_constant(X_current)
        # Assicurati che y_train non contenga NaN dopo la pulizia
        if y_train.isnull().any():
             print("Errore: y_train contiene ancora NaN dopo la pulizia.")
             break # Esci dal loop se y_train ha NaN

        try:
            model = sm.OLS(y_train, X_const).fit()
        except ValueError as e:
            print(f"Errore durante il fitting del modello OLS: {e}")
            print("Controlla i dati in X_current e y_train.")
            print("NaN in X_current:", X_current.isnull().sum().sum())
            print("Inf in X_current:", np.isinf(X_current).sum().sum())
            print("NaN in y_train:", y_train.isnull().sum())
            print("Inf in y_train:", np.isinf(y_train).sum())
            break # Esci in caso di errore

        pvals = model.pvalues.drop('const')

        # Assicurati che pvals e X_current.columns siano allineati
        if not pvals.index.equals(X_current.columns):
             print("Attenzione: Indici di p-value e colonne di X_current non allineati.")
             # Questo potrebbe indicare un problema serio, potresti voler interrompere o investigare
             break

        vif_data = pd.DataFrame({
            'Feature': X_current.columns,
            'VIF': [variance_inflation_factor(X_current.values, i)
                    for i in range(X_current.shape[1])],
            'p-value': pvals.values
        })

        # Seleziona le variabili che superano entrambe le soglie
        cond = (vif_data['VIF'] > vif_threshold) & (vif_data['p-value'] > pvalue_threshold)

        print("\nVIF e p-value correnti:")
        print(vif_data[['Feature', 'VIF', 'p-value']])

        if not cond.any():
            print("\nNessuna variabile soddisfa le condizioni di rimozione.")
            break

        # Rimuovi la variabile con VIF più alto tra quelle che superano le soglie
        to_remove_row = vif_data.loc[cond].iloc[vif_data.loc[cond,'VIF'].argmax()]
        to_remove = to_remove_row['Feature']

        print(f"\nRimuovo {to_remove} (VIF={to_remove_row['VIF']:.2f}, "
              f"p-val={to_remove_row['p-value']:.4f})")

        X_current.drop(columns=[to_remove], inplace=True)
        removed_features.add(to_remove)

    final_features = set(X_current.columns)
    print("\nFeature finali selezionate:", X_current.columns.tolist())
    print("Numero di feature finali:", len(X_current.columns))
    print("Feature rimosse:", list(removed_features))

    return X_current.columns.tolist() # Restituisce la lista dei nomi delle colonne selezionate


# Separazione X/y dal TRAIN set pulito
X_train_full = df_clean_train.drop(columns=['Depression'])
y_train_full = df_clean_train['Depression']

# Applica la selezione delle feature sul set di TRAIN completo
selected_features = elimina_variabili_vif_pvalue(X_train_full, y_train_full)

# Seleziona le feature identificate sia dal set di TRAIN che dal set di TEST
X_train_selected = X_train_full[selected_features]
X_test_final = df_clean_test[selected_features] # Questo è il vero set di test per la submission


# Analizziamo la distribuzione delle classi nel target del TRAIN set
print("\nDistribuzione delle classi nel target (Train Set):")
print(y_train_full.value_counts(normalize=True))

# Calcoliamo il rapporto per scale_pos_weight in XGBoost (sul TRAIN set)
negative_count, positive_count = np.bincount(y_train_full)
scale_pos_weight = negative_count / positive_count
print(f"\nRapporto delle classi (negativo/positivo) per XGBoost: {scale_pos_weight:.2f}")

# Separazione train/validation mantenendo la distribuzione delle classi (dal TRAIN set originale)
# Usiamo X_train_selected e y_train_full per creare il set di training e validation per i modelli
X_train, X_val, y_train, y_val = train_test_split(
    X_train_selected, y_train_full,
    test_size=0.2, # Puoi aggiustare questa dimensione
    random_state=73,
    stratify=y_train_full # Mantiene la distribuzione originale
)

print(f"\nDimensioni dei set dopo lo split (Train/Validation):")
print(f"X_train: {X_train.shape}, y_train: {y_train.shape}")
print(f"X_val: {X_val.shape}, y_val: {y_val.shape}")
print(f"X_test_final (per submission): {X_test_final.shape}")


# 1. Logistic Regression con class weights
log_reg = LogisticRegression(
    random_state=73,
    max_iter=1000,
    class_weight='balanced'  # Aggiunto bilanciamento classi
)

# 2. XGBoost con pesi per la classe positiva
xgb_clf = XGBClassifier(
    objective='binary:logistic',
    random_state=73,
    scale_pos_weight=scale_pos_weight  # Aggiunto bilanciamento
)

# 3. Pipeline con SMOTE e XGBoost
# Applichiamo SMOTE solo sul set di TRAIN (X_train, y_train)
smote = SMOTE(random_state=73, sampling_strategy='auto')
xgb_smote = ImbPipeline([
    ('smote', smote),
    ('xgb', XGBClassifier(objective='binary:logistic', random_state=73))
])

# Parametri per la GridSearch con SMOTE
param_grid = {
    'xgb__n_estimators': [50, 100, 150], # Aggiunti più valori
    'xgb__max_depth': [3, 5, 7],       # Aggiunti più valori
    'xgb__learning_rate': [0.01, 0.05, 0.1], # Aggiunti più valori
    'xgb__scale_pos_weight': [1, scale_pos_weight]  # Testa con e senza pesi
}

# Usiamo il set di VALIDATION (X_val, y_val) per valutare durante la GridSearch
grid_clf = GridSearchCV(
    xgb_smote,
    param_grid,
    scoring='f1', # Metrica F1 è buona per classi sbilanciate
    cv=5,
    n_jobs=-1,
    verbose=1 # Mostra l'avanzamento
)

# Addestramento modelli (sul set di TRAIN)
print("\nAddestramento modelli...")
log_reg.fit(X_train, y_train)
xgb_clf.fit(X_train, y_train)
grid_clf.fit(X_train, y_train)

# Miglior modello con SMOTE + XGBoost
best_xgb_clf = grid_clf.best_estimator_
print(f"\nMigliori parametri trovati dalla Grid Search: {grid_clf.best_params_}")
print(f"Miglior F1 score sulla validation set (Grid Search): {grid_clf.best_score_:.4f}")


# Valutazione dei modelli sul set di VALIDATION (X_val, y_val)
print("\nValutazione dei modelli sul set di Validation:")
y_pred_log_val = log_reg.predict(X_val)
y_pred_xgb_val = xgb_clf.predict(X_val)
y_pred_xgb_best_val = best_xgb_clf.predict(X_val)

print("\nReport di Classificazione - Logistic Regression (Validation):")
print(classification_report(y_val, y_pred_log_val))

print("\nReport di Classificazione - XGBoost (Validation):")
print(classification_report(y_val, y_pred_xgb_val))

print("\nReport di Classificazione - XGBoost (Optimized) (Validation):")
print(classification_report(y_val, y_pred_xgb_best_val))


# Funzione per visualizzare più matrici di confusione in un unico grafico
def plot_combined_confusion_matrices(y_true, y_pred_list, model_names, title_suffix="Validation"):
    plt.figure(figsize=(15, 4))

    for i, (y_pred, name) in enumerate(zip(y_pred_list, model_names)):
        plt.subplot(1, 3, i+1)
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
        plt.title(f"Confusion Matrix - {name} ({title_suffix})")
        plt.ylabel('Actual')
        plt.xlabel('Predicted')

    plt.tight_layout()
    plt.show()

# Visualizza le matrici di confusione per i set di Validation
plot_combined_confusion_matrices(
    y_val,
    [y_pred_log_val, y_pred_xgb_val, y_pred_xgb_best_val],
    ["Logistic Regression", "XGBoost", "XGBoost (Optimized)"],
    "Validation"
)

# Funzione per confrontare le metriche
def plot_metrics_comparison(y_true, y_pred_list, model_names, title_suffix="Validation"):
    metrics = {
        'Accuracy': [],
        'Precision': [],
        'Recall': [],
        'F1 Score': []
    }

    for y_pred in y_pred_list:
        metrics['Accuracy'].append(accuracy_score(y_true, y_pred))
        metrics['Precision'].append(precision_score(y_true, y_pred))
        metrics['Recall'].append(recall_score(y_true, y_pred))
        metrics['F1 Score'].append(f1_score(y_true, y_pred))

    metrics_df = pd.DataFrame(metrics, index=model_names)

    plt.figure(figsize=(12, 6))
    metrics_df.plot(kind='bar', figsize=(12, 6))
    plt.title(f'Confronto delle metriche tra i modelli ({title_suffix})')
    plt.ylabel('Score')
    plt.ylim(0, 1.0)
    plt.xticks(rotation=0)
    plt.legend(loc='lower right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    return metrics_df

# Confrontiamo le metriche sui set di Validation
metrics_df_val = plot_metrics_comparison(
    y_val,
    [y_pred_log_val, y_pred_xgb_val, y_pred_xgb_best_val],
    ["Logistic Regression", "XGBoost", "XGBoost (Optimized)"],
    "Validation"
)

print("\nConfronti metriche (Validation) in formato tabella:")
print(metrics_df_val.round(4))


# === Generazione del file di Submission ===

# Fai previsioni sul set di TEST (X_test_final) usando il modello migliore
print("\nGenerazione delle previsioni sul set di test per la submission...")
test_predictions = best_xgb_clf.predict(X_test_final)

# Crea il DataFrame di submission con gli ID *processati* e le previsioni
# Usa processed_test_ids che ora dovrebbe avere 93800 righe
submission_df = pd.DataFrame({'id': processed_test_ids, 'Depression': test_predictions})

# Esporta il DataFrame di submission nel formato richiesto
submission_file_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\07_05_CorsoPython_ML\MentallyStabilityOfThePerson\submission.csv'
try:
    submission_df.to_csv(submission_file_path, index=False)
    print(f"\nFile di submission creato con successo in '{submission_file_path}'")
    print("Anteprima del file di submission:")
    print(submission_df.head())
    print(f"Numero di righe nel file di submission: {len(submission_df)}") # Aggiunto per verifica
except Exception as e:
    print(f"\nErrore durante l'esportazione del file di submission: {e}")

