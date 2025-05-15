import re
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import matplotlib.pyplot as plt

from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from statsmodels.stats.outliers_influence import variance_inflation_factor

# --- Codifica 'Sleep Duration' ---
# Funzione per mappare le stringhe di durata del sonno a valori numerici
def map_sleep_duration(duration_str):
    s = str(duration_str).strip()  # Converti in stringa e rimuovi spazi

    # Casi speciali (es. "Less than 5", "Under 4")
    if re.search(r'less.*?\d+|under.*?\d+', s, re.IGNORECASE):
        num = re.search(r'\d+', s)
        return float(num.group()) - 1 if num else np.nan

    # Casi speciali (es. "More than 8", "Over 9")
    elif re.search(r'more.*?\d+|over.*?\d+', s, re.IGNORECASE):
        num = re.search(r'\d+', s)
        return float(num.group()) + 1 if num else np.nan

    # Intervallo (es. "6-7", "4–5 hours")
    range_match = re.search(r'(\d+)\s*[-–—]\s*(\d+)', s)
    if range_match:
        num1, num2 = map(float, range_match.groups())
        avg = (num1 + num2) / 2
        return avg if avg <= 24 else float(str(int(avg))[0])  # correzione se media troppo alta

    # Singolo numero (es. "7", "about 6.5")
    num_match = re.search(r'\d+\.?\d*', s)
    if num_match:
        val = float(num_match.group())
        # Corregge se il valore è palesemente errato (>24 ore)
        if val > 24:
            return float(str(int(val))[0])  # Es. "49" -> "4"
        return val

    return np.nan

# Utilizziamo la funzione per calcolare il VIF ed il Pvalue sulle Feature per verificare eventuali rimozioni
def elimina_variabili_vif_pvalue(X, y, vif_threshold=5.0, pvalue_threshold=0.05):
    
    X_current = X.copy()
    
    while True:
        X_const = sm.add_constant(X_current)
        model = sm.OLS(y, X_const).fit()
        pvals = model.pvalues.drop('const')
        vif_data = pd.DataFrame({
            'Feature': X_current.columns,
            'VIF': [variance_inflation_factor(X_current.values, i) 
                    for i in range(X_current.shape[1])],
            'p-value': pvals.values
        })
        cond = (vif_data['VIF'] > vif_threshold) & (vif_data['p-value'] > pvalue_threshold)
        print(vif_data[['VIF','p-value']])
        if not cond.any():
            break
        # Rimuovo la variabile con VIF più alto
        to_remove = vif_data.loc[cond, 'Feature'].iloc[vif_data.loc[cond,'VIF'].argmax()]
        print(f"Rimuovo {to_remove} (VIF={vif_data.loc[vif_data.Feature==to_remove,'VIF'].values[0]:.2f}, "
            f"p-val={vif_data.loc[vif_data.Feature==to_remove,'p-value'].values[0]:.4f})")
        X_current.drop(columns=[to_remove], inplace=True)
    print("Feature finali:", X_current.columns.tolist())
    print("Numero di feature:", len(X_current.columns))
    
    return X_current

def preprocess_train(df):
    # Preparazione del DataFrame per l'imputazione
    # --- Imputazione della colonna 'Profession' ---
    # Applichiamo la seguente logica:
    # - Se 'Working Professional or Student' è valorizzato 'Student' E 'Profession' è NaN, imputiamo con 'Student'.
    # - Se 'Working Professional or Student' è valorizzato 'Working Professional' E 'Profession' è NaN, imputa con 'Unknown'.

    df.loc[
        (df['Working Professional or Student'] == 'Student') & (df['Profession'].isna()),
        'Profession'
    ] = 'Student'

    df.loc[
        (df['Working Professional or Student'] == 'Working Professional') & (df['Profession'].isna()),
        'Profession'
    ] = 'Unknown'

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
    # Imputiamo i rimanenti mancanti nelle colonne accademiche per gli 'Studenti' con la mediana del sottogruppo 'Student'.
    for col in academic_cols:
        # Seleziona le righe dove lo stato è 'Student' e la colonna corrente è NaN
        condition = (df['Working Professional or Student'] == 'Student') & (df[col].isna())
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
    # Imputazione con la moda per 'Dietary Habits' e 'Degree' (categoriche)
    for col in ['Dietary Habits', 'Degree']:
        if col in df.columns and not df[col].empty:
            # Calcola la moda solo se ci sono valori non-null
            if df[col].notna().any():
                moda_val = df[col].mode()[0]
                df[col] = df[col].fillna(moda_val)
            else:
                print(f"Attenzione: La colonna '{col}' contiene solo valori NaN. Imputazione con moda non possibile.")

    # Imputazione con la mediana per 'Financial Stress' (numerica)
    if 'Financial Stress' in df.columns and not df['Financial Stress'].empty:
        # Calcola la mediana solo se ci sono valori non-null
        if df['Financial Stress'].notna().any():
            mediana_val = df['Financial Stress'].median()
            df['Financial Stress'] = df['Financial Stress'].fillna(mediana_val)
        else:
            print("Attenzione: La colonna 'Financial Stress' contiene solo valori NaN. Imputazione con mediana non possibile.")

    # --- Codifica delle variabili categoriche ---
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

    df['Sleep Duration'] = df['Sleep Duration'].apply(map_sleep_duration)

    # Controlla se ci sono valori non mappati (dovrebbero essere NaN se la funzione non li ha riconosciuti)
    if df['Sleep Duration'].isna().any():
        print("Attenzione: Valori non previsti nella colonna 'Sleep Duration' dopo la mappatura. Potrebbero essere NaN.")
        mediana_sleep = df['Sleep Duration'].median()
        df['Sleep Duration'] = df['Sleep Duration'].fillna(mediana_sleep)

    # --- Pulizia e Codifica 'Degree' ---
    # Standardizziamo spazi e rimuoviamo punteggiatura non necessaria
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

    # --- Codifica 'Dietary Habits' con OrdinalEncoder ---
    print("\nValori unici nella colonna 'Dietary Habits' prima della codifica:")
    print(df['Dietary Habits'].unique())

    # Definisci i valori validi per 'Dietary Habits'
    valid_dietary_habits = ['Unhealthy', 'Moderate', 'Healthy']

    # Elimina le righe dove 'Dietary Habits' non è uno dei valori validi E non è NaN
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

    # Ordine: Unhealthy < Moderate < Healthy
    encoder = OrdinalEncoder(categories=[valid_dietary_habits])

    try:
        # Modifica per usare solo i valori validi definiti
        encoder = OrdinalEncoder(categories=[valid_dietary_habits])
        df['Dietary Habits'] = encoder.fit_transform(df[['Dietary Habits']])
        print("\nCodifica 'Dietary Habits' completata con successo.")
    except ValueError as e:
        print(f"\nErrore durante la codifica di 'Dietary Habits': {e}")
        print("Controlla i valori unici stampati sopra. La colonna 'Dietary Habits' contiene valori non previsti.")

    # Codifichiamo 'Have you ever had suicidal thoughts ?': Yes=1, No=0
    df['Have you ever had suicidal thoughts ?'] = df['Have you ever had suicidal thoughts ?'].map({'Yes': 1, 'No': 0})
    # Controlla se ci sono valori non mappati
    if df['Have you ever had suicidal thoughts ?'].isna().any():
        print("Attenzione: Valori non previsti nella colonna 'Have you ever had suicidal thoughts ?' dopo la mappatura.")

    # Codifichiamo 'Family History of Mental Illness': Yes=1, No=0
    df['Family History of Mental Illness'] = df['Family History of Mental Illness'].map({'Yes': 1, 'No': 0})
    # Controlla se ci sono valori non mappati
    if df['Family History of Mental Illness'].isna().any():
        print("Attenzione: Valori non previsti nella colonna 'Family History of Mental Illness' dopo la mappatura.")

    # --- Verifica dei risultati finali ---
    print("\nDataFrame dopo TUTTE le trasformazioni (imputazione, eliminazione righe e codifica):")
    print(df.head())
    print("\nInformazioni sul DataFrame dopo TUTTE le trasformazioni:")
    print(df.info()) 
    print("\nValori unici nella colonna 'Profession':")
    print(df['Profession'].unique())
    print("Numero di valori unici:", len(df['Profession'].unique()))

    # --- Raggruppamento e Codifica 'Profession' ---
    print("\nRaggruppamento e Codifica della colonna 'Profession'...")

    # Definisci la mappatura per Profession -> Professional_Group
    professional_map = {
        'Chef': 'Culinary',
        'Teacher': 'Education',
        'Business Analyst': 'Business/Consulting',
        'Finanancial Analyst': 'Finance',
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
        'B.Com': 'Other',  # Titolo di studio, non professione
        'BE': 'Other',     # Titolo di studio, non professione
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

    # Utilizziamo l'encoder per 'Professional_Group'
    df['Professional_Group_Encoded'] = label_encoder_profession.fit_transform(df['Professional_Group'])
    print("\nMappatura Label Encoding per 'Professional_Group':")
    # Crea una Series per mostrare la mappatura
    label_mapping_profession = pd.Series(label_encoder_profession.classes_, name='Professional_Group').to_frame()
    label_mapping_profession['Encoded_Value'] = label_encoder_profession.transform(label_encoder_profession.classes_)
    print(label_mapping_profession)

    # KNN per raggruppare in base alla città (miglioria del metodo manuale)

    # --- Definizione e Mappatura delle Regioni ---
    # Definisci la mappatura 'region_map' per gestire tramite regione e non per City
    region_map = {
        # North-East India
        'Patna': 'North-East India',
        'Varanasi': 'North-East India',
        # North-West India
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
        # Central India
        'Indore': 'Central India', 'Bhopal': 'Central India', 'Nagpur': 'Central India',
        # East India
        'Kolkata': 'East India', 'Visakhapatnam': 'East India',
        # South India
        'Bangalore': 'South India', 'Chennai': 'South India', 'Hyderabad': 'South India'
    }

    # Applica la mappatura e gestisci i casi non riconosciuti
    df['Region'] = df['City'].map(region_map).fillna('Other')

    # Raggruppa e conta per regione
    print("\nConteggio delle città per Regione:")
    region_counts = df['Region'].value_counts()
    print(region_counts)

    # --- Codifica 'Region' con LabelEncoder ---
    print("\nEseguendo Label Encoding per la colonna 'Region'...")

    # Inizializza LabelEncoder
    label_encoder = LabelEncoder()

    # Fit e trasforma la colonna 'Region'
    df['Region_Encoded'] = label_encoder.fit_transform(df['Region'])

    # Puoi vedere la mappatura creata dal LabelEncoder
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

    df_clean = df.copy()
    df_clean = df_clean.drop(columns=['City','Name','id','Profession', 'Degree', 'Degree_Group', 'Professional_Group', 'Region'])

    try:
        file_path = r'Mentally\cleaned_train.csv'
        df_clean.to_csv(file_path, index=False)
        print("\nDataFrame esportato con successo in 'cleaned_train.csv'")
    except Exception as e:
        print(f"\nErrore durante l'esportazione del DataFrame: {e}")
        
    # # --- Visualizzazione della Matrice di Correlazione ---
    # numeric_cols = [
    #     'Age', 'Academic Pressure', 'Work Pressure', 'CGPA', 'Study Satisfaction',
    #     'Job Satisfaction', 'Sleep Duration', 'Work/Study Hours', 'Financial Stress',
    #     'Depression', 'Gender', 'Working Professional or Student', 'Dietary Habits',
    #     'Have you ever had suicidal thoughts ?', 'Family History of Mental Illness',
    #     'Region_Encoded', 'Degree_Group_Encoded', 'Professional_Group_Encoded'
    # ]

    # # Visualizziamo la matrice di correlazione
    # corr_matrix = df_clean[numeric_cols].corr()

    # plt.figure(figsize=(8,6))
    # sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm")
    # plt.title("Correlation matrix (variabili continue)")
    # plt.show()

    # Modifichiamo il nome della colonna 'Have you ever had suicidal thoughts ?' in 'SuicidalThoughts' 
    df_clean = df_clean.rename(columns={'Have you ever had suicidal thoughts ?': 'SuicidalThoughts'}) 
    df_clean = df_clean.drop(columns=['SuicidalThoughts'])
    
    return df_clean

def preprocess_test(df):
    # --- Preparazione del DataFrame per l'imputazione ---

    # --- Imputazione della colonna 'Profession' ---
    # Applichiamo la logica:
    # - Se 'Working Professional or Student' è 'Student' E 'Profession' è NaN, imputa con 'Student'.
    # - Se 'Working Professional or Student' è 'Working Professional' E 'Profession' è NaN, imputa con 'Unknown'.

    # Imputa 'Profession' con 'Student' dove lo stato è 'Student' e 'Profession' è mancante
    df.loc[
        (df['Working Professional or Student'] == 'Student') & (df['Profession'].isna()),
        'Profession'
    ] = 'Student'

    # Imputa 'Profession' con 'Unemployed' dove lo stato è 'Working Professional' e 'Profession' è mancante
    df.loc[
        (df['Working Professional or Student'] == 'Working Professional') & (df['Profession'].isna()),
        'Profession'
    ] = 'Unknown'

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
    # Questi sono i mancanti nelle colonne accademiche per gli studenti e nelle colonne lavorative per i professionisti.
    # Li imputiamo con la mediana del rispettivo sottogruppo.
    # Imputa i rimanenti mancanti nelle colonne accademiche per gli 'Studenti' con la mediana del sottogruppo 'Student'.
    for col in academic_cols:
        # Seleziona le righe dove lo stato è 'Student' e la colonna corrente è NaN
        condition = (df['Working Professional or Student'] == 'Student') & (df[col].isna())
        mediana_sottogruppo = df[df['Working Professional or Student'] == 'Student'][col].median()
        df.loc[condition, col] = mediana_sottogruppo

    # Imputa i rimanenti mancanti nelle colonne lavorative per i 'Working Professional' con la mediana del sottogruppo 'Working Professional'.
    for col in work_cols:
        # Seleziona le righe dove lo stato è 'Working Professional' e la colonna corrente è NaN
        condition = (df['Working Professional or Student'] == 'Working Professional') & (df[col].isna())
        mediana_sottogruppo = df[df['Working Professional or Student'] == 'Working Professional'][col].median()
        df.loc[condition, col] = mediana_sottogruppo

    # --- Gestione dei mancanti nelle altre colonne con pochi valori assenti ---
    
    # Imputazione con la moda per 'Dietary Habits' e 'Degree' (categoriche)
    for col in ['Dietary Habits', 'Degree']:
        # Controlla se la colonna esiste e non è vuota prima di calcolare la moda
        if col in df.columns and not df[col].empty:
            # Calcola la moda solo se ci sono valori non-null
            if df[col].notna().any():
                moda_val = df[col].mode()[0]
                df[col] = df[col].fillna(moda_val)
            else:
                print(f"Attenzione: La colonna '{col}' contiene solo valori NaN. Imputazione con moda non possibile.")

    # Imputazione con la mediana per 'Financial Stress' (numerica)
    if 'Financial Stress' in df.columns and not df['Financial Stress'].empty:
        # Calcola la mediana solo se ci sono valori non-null
        if df['Financial Stress'].notna().any():
            mediana_val = df['Financial Stress'].median()
            df['Financial Stress'] = df['Financial Stress'].fillna(mediana_val)
        else:
            print("Attenzione: La colonna 'Financial Stress' contiene solo valori NaN. Imputazione con mediana non possibile.")

    # --- Codifica delle variabili categoriche ---

    # Codifica per 'Gender': Male=1, Female=0
    df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})
    # Controlla se ci sono valori non mappati dopo la trasformazione (potrebbero diventare NaN)
    if df['Gender'].isna().any():
        print("Attenzione: Valori non previsti nella colonna 'Gender' dopo la mappatura.")

    # Codifica 'Working Professional or Student': Working Professional=1, Student=0
    df['Working Professional or Student'] = df['Working Professional or Student'].map({'Working Professional': 1, 'Student': 0})
    # Controlla se ci sono valori non mappati
    if df['Working Professional or Student'].isna().any():
        print("Attenzione: Valori non previsti nella colonna 'Working Professional or Student' dopo la mappatura.")

    # Applichiamo la 'map_sleep_duration' nella colonna 'Sleep Duration'
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

    # Mappiamo in gruppi la sezione 'Degree'
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

    # --- Codifica 'Dietary Habits' con OrdinalEncoder ---
    print("\nValori unici nella colonna 'Dietary Habits' prima della codifica:")
    print(df['Dietary Habits'].unique())

    # Definisci i valori validi per 'Dietary Habits'
    valid_dietary_habits = ['Unhealthy', 'Moderate', 'Healthy']

    # Elimina le righe dove 'Dietary Habits' non è uno dei valori validi E non è NaN
    # Vogliamo le righe dove il valore NON è 'Unhealthy' AND NON è 'Moderate' AND NON è 'Healthy'
    # E il valore NON è NaN (per evitare di eliminare i NaN originali se non imputati)
    condition_not_valid = (df['Dietary Habits'] != 'Unhealthy') & \
                        (df['Dietary Habits'] != 'Moderate') & \
                        (df['Dietary Habits'] != 'Healthy') & \
                        df['Dietary Habits'].notna()

    # Sostituisci i valori non validi con la moda (o con 'Moderate', per esempio)
    df.loc[condition_not_valid, 'Dietary Habits'] = df['Dietary Habits'].mode()[0]

    # Ora selzioniamo gli id allineati:
    test_ids = df['id'].values

    print(f"Numero di righe rimanenti nel DataFrame: {len(df)}")

    # Ristampa i valori unici dopo l'eliminazione per verifica
    print("\nValori unici nella colonna 'Dietary Habits' dopo l'eliminazione delle righe non valide:")
    print(df['Dietary Habits'].unique())

    # Ordine: Unhealthy < Moderate < Healthy
    encoder = OrdinalEncoder(categories=[valid_dietary_habits])
    # Reshape necessario perché fit_transform si aspetta un input 2D

    try:
        # Modifica per usare solo i valori validi definiti
        encoder = OrdinalEncoder(categories=[valid_dietary_habits])
        df['Dietary Habits'] = encoder.fit_transform(df[['Dietary Habits']])
        print("\nCodifica 'Dietary Habits' completata con successo.")
        
    except ValueError as e:
        print(f"\nErrore durante la codifica di 'Dietary Habits': {e}")
        print("Controlla i valori unici stampati sopra. La colonna 'Dietary Habits' contiene valori non previsti.")

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
    print(df.info())
    print("\nValori unici nella colonna 'Profession':")
    print(df['Profession'].unique())
    print("Numero di valori unici:", len(df['Profession'].unique()))

    # --- Raggruppamento e Codifica 'Profession' ---
    print("\nRaggruppamento e Codifica della colonna 'Profession'...")

    # Definisco la mappatura per Professional_Group in base a Profession
    professional_map = {
        'Chef': 'Culinary',
        'Teacher': 'Education',
        'Business Analyst': 'Business/Consulting',
        'Finanancial Analyst': 'Finance',
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

    # Applichiamo la mappatura e gestisci i casi non riconosciuti
    df['Professional_Group'] = df['Profession'].map(professional_map).fillna('Other')

    # --- Codifica 'Professional_Group' con LabelEncoder ---
    print("\nEseguendo Label Encoding per la colonna 'Professional_Group'...")

    # Inizializziamo LabelEncoder
    label_encoder_profession = LabelEncoder()

    # Fit e trasforma la colonna 'Professional_Group'
    df['Professional_Group_Encoded'] = label_encoder_profession.fit_transform(df['Professional_Group'])

    # Puoi vedere la mappatura creata dal LabelEncoder
    print("\nMappatura Label Encoding per 'Professional_Group':")
    # Crea una Series per mostrare la mappatura
    label_mapping_profession = pd.Series(label_encoder_profession.classes_, name='Professional_Group').to_frame()
    label_mapping_profession['Encoded_Value'] = label_encoder_profession.transform(label_encoder_profession.classes_)
    print(label_mapping_profession)
    
    # KNN per raggruppare in base alla città (miglioria del metodo manuale)

    # --- Definizione e Mappatura delle Regioni ---
    # Definiamo la mappatura Region per City
    region_map = {
        # North-East India
        'Patna': 'North-East India',
        'Varanasi': 'North-East India',
        # North-West India
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
    }

    # Applica la mappatura e gestisci i casi non riconosciuti
    df['Region'] = df['City'].map(region_map).fillna('Other')

    # Raggruppa e conta per regione
    print("\nConteggio delle città per Regione:")
    region_counts = df['Region'].value_counts()
    print(region_counts)

    # --- Codifica 'Region' con LabelEncoder ---
    print("\nEseguendo Label Encoding per la colonna 'Region'...")

    # Inizializziamo LabelEncoder
    label_encoder = LabelEncoder()

    # Fit e trasforma la colonna 'Region'
    df['Region_Encoded'] = label_encoder.fit_transform(df['Region'])
    print("\nMappatura Label Encoding per 'Region':")
    # Crea una Series per mostrare la mappatura
    label_mapping = pd.Series(label_encoder.classes_, name='Region').to_frame()
    label_mapping['Encoded_Value'] = label_encoder.transform(label_encoder.classes_)
    print(label_mapping)

    # --- Verifica dei risultati finali ---
    print("\nDataFrame dopo TUTTE le trasformazioni (imputazione, eliminazione righe, codifica):")
    print(df.head())
    print("\nInformazioni sul DataFrame dopo TUTTE le trasformazioni:")
    print(df.info())
   
    df_clean = df.copy()
    df_clean = df_clean.drop(columns=['City','Name','id','Profession', 'Degree', 'Degree_Group', 'Professional_Group', 'Region'])

    try:
        file_path = r'Mentally\cleaned_test.csv'
        df_clean.to_csv(file_path, index=False)
        print("\nDataFrame esportato con successo in 'cleaned_test.csv'")
    except Exception as e:
        print(f"\nErrore durante l'esportazione del DataFrame: {e}")

    # # --- Visualizzazione della Matrice di Correlazione ---
    # numeric_cols = [
    #     'Age', 'Academic Pressure', 'Work Pressure', 'CGPA', 'Study Satisfaction',
    #     'Job Satisfaction', 'Sleep Duration', 'Work/Study Hours', 'Financial Stress',
    #     'Gender', 'Working Professional or Student', 'Dietary Habits',
    #     'Have you ever had suicidal thoughts ?', 'Family History of Mental Illness',
    #     'Region_Encoded', 'Degree_Group_Encoded', 'Professional_Group_Encoded'
    # ]

    # # Calcolo la Pearson-corr
    # corr_matrix = df_clean[numeric_cols].corr()

    # plt.figure(figsize=(8,6))
    # sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm")
    # plt.title("Correlation matrix (variabili continue)")
    # plt.show()

    df_clean = df_clean.rename(columns={'Have you ever had suicidal thoughts ?': 'SuicidalThoughts'}) 
    df_clean = df_clean.drop(columns=['SuicidalThoughts'])
    
    return df_clean, test_ids

def preprocess_person_test(df):
    # --- Preparazione del DataFrame per l'imputazione ---

    # --- Imputazione della colonna 'Profession' ---
    # Applichiamo la logica:
    # - Se 'Working Professional or Student' è 'Student' E 'Profession' è NaN, imputa con 'Student'.
    # - Se 'Working Professional or Student' è 'Working Professional' E 'Profession' è NaN, imputa con 'Unknown'.

    # Imputa 'Profession' con 'Student' dove lo stato è 'Student' e 'Profession' è mancante
    df.loc[
        (df['Working Professional or Student'] == 'Student') & (df['Profession'].isna()),
        'Profession'
    ] = 'Student'

    # Imputa 'Profession' con 'Unemployed' dove lo stato è 'Working Professional' e 'Profession' è mancante
    df.loc[
        (df['Working Professional or Student'] == 'Working Professional') & (df['Profession'].isna()),
        'Profession'
    ] = 'Unknown'

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
    # Questi sono i mancanti nelle colonne accademiche per gli studenti e nelle colonne lavorative per i professionisti.
    # Li imputiamo con la mediana del rispettivo sottogruppo.
    # Imputa i rimanenti mancanti nelle colonne accademiche per gli 'Studenti' con la mediana del sottogruppo 'Student'.
    for col in academic_cols:
        # Seleziona le righe dove lo stato è 'Student' e la colonna corrente è NaN
        condition = (df['Working Professional or Student'] == 'Student') & (df[col].isna())
        mediana_sottogruppo = df[df['Working Professional or Student'] == 'Student'][col].median()
        df.loc[condition, col] = mediana_sottogruppo

    # Imputa i rimanenti mancanti nelle colonne lavorative per i 'Working Professional' con la mediana del sottogruppo 'Working Professional'.
    for col in work_cols:
        # Seleziona le righe dove lo stato è 'Working Professional' e la colonna corrente è NaN
        condition = (df['Working Professional or Student'] == 'Working Professional') & (df[col].isna())
        mediana_sottogruppo = df[df['Working Professional or Student'] == 'Working Professional'][col].median()
        df.loc[condition, col] = mediana_sottogruppo

    # --- Gestione dei mancanti nelle altre colonne con pochi valori assenti ---
    
    # Imputazione con la moda per 'Dietary Habits' e 'Degree' (categoriche)
    for col in ['Dietary Habits', 'Degree']:
        # Controlla se la colonna esiste e non è vuota prima di calcolare la moda
        if col in df.columns and not df[col].empty:
            # Calcola la moda solo se ci sono valori non-null
            if df[col].notna().any():
                moda_val = df[col].mode()[0]
                df[col] = df[col].fillna(moda_val)
            else:
                print(f"Attenzione: La colonna '{col}' contiene solo valori NaN. Imputazione con moda non possibile.")

    # Imputazione con la mediana per 'Financial Stress' (numerica)
    if 'Financial Stress' in df.columns and not df['Financial Stress'].empty:
        # Calcola la mediana solo se ci sono valori non-null
        if df['Financial Stress'].notna().any():
            mediana_val = df['Financial Stress'].median()
            df['Financial Stress'] = df['Financial Stress'].fillna(mediana_val)
        else:
            print("Attenzione: La colonna 'Financial Stress' contiene solo valori NaN. Imputazione con mediana non possibile.")

    # --- Codifica delle variabili categoriche ---

    # Codifica per 'Gender': Male=1, Female=0
    df['Gender'] = df['Gender'].map({'Male': 1, 'Female': 0})
    # Controlla se ci sono valori non mappati dopo la trasformazione (potrebbero diventare NaN)
    if df['Gender'].isna().any():
        print("Attenzione: Valori non previsti nella colonna 'Gender' dopo la mappatura.")

    # Codifica 'Working Professional or Student': Working Professional=1, Student=0
    df['Working Professional or Student'] = df['Working Professional or Student'].map({'Working Professional': 1, 'Student': 0})
    # Controlla se ci sono valori non mappati
    if df['Working Professional or Student'].isna().any():
        print("Attenzione: Valori non previsti nella colonna 'Working Professional or Student' dopo la mappatura.")

    # Applichiamo la 'map_sleep_duration' nella colonna 'Sleep Duration'
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

    # Mappiamo in gruppi la sezione 'Degree'
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

    # --- Codifica 'Dietary Habits' con OrdinalEncoder ---
    print("\nValori unici nella colonna 'Dietary Habits' prima della codifica:")
    print(df['Dietary Habits'].unique())

    # Definisci i valori validi per 'Dietary Habits'
    valid_dietary_habits = ['Unhealthy', 'Moderate', 'Healthy']

    # Elimina le righe dove 'Dietary Habits' non è uno dei valori validi E non è NaN
    # Vogliamo le righe dove il valore NON è 'Unhealthy' AND NON è 'Moderate' AND NON è 'Healthy'
    # E il valore NON è NaN (per evitare di eliminare i NaN originali se non imputati)
    condition_not_valid = (df['Dietary Habits'] != 'Unhealthy') & \
                        (df['Dietary Habits'] != 'Moderate') & \
                        (df['Dietary Habits'] != 'Healthy') & \
                        df['Dietary Habits'].notna()

    # Sostituisci i valori non validi con la moda (o con 'Moderate', per esempio)
    df.loc[condition_not_valid, 'Dietary Habits'] = df['Dietary Habits'].mode()[0]

    # Ora selzioniamo gli id allineati:
    test_ids = df['id'].values

    print(f"Numero di righe rimanenti nel DataFrame: {len(df)}")

    # Ristampa i valori unici dopo l'eliminazione per verifica
    print("\nValori unici nella colonna 'Dietary Habits' dopo l'eliminazione delle righe non valide:")
    print(df['Dietary Habits'].unique())

    # Ordine: Unhealthy < Moderate < Healthy
    encoder = OrdinalEncoder(categories=[valid_dietary_habits])
    # Reshape necessario perché fit_transform si aspetta un input 2D

    try:
        # Modifica per usare solo i valori validi definiti
        encoder = OrdinalEncoder(categories=[valid_dietary_habits])
        df['Dietary Habits'] = encoder.fit_transform(df[['Dietary Habits']])
        print("\nCodifica 'Dietary Habits' completata con successo.")
        
    except ValueError as e:
        print(f"\nErrore durante la codifica di 'Dietary Habits': {e}")
        print("Controlla i valori unici stampati sopra. La colonna 'Dietary Habits' contiene valori non previsti.")

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
    print(df.info())
    print("\nValori unici nella colonna 'Profession':")
    print(df['Profession'].unique())
    print("Numero di valori unici:", len(df['Profession'].unique()))

    # --- Raggruppamento e Codifica 'Profession' ---
    print("\nRaggruppamento e Codifica della colonna 'Profession'...")

    # Definisco la mappatura per Professional_Group in base a Profession
    professional_map = {
        'Chef': 'Culinary',
        'Teacher': 'Education',
        'Business Analyst': 'Business/Consulting',
        'Finanancial Analyst': 'Finance',
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

    # Applichiamo la mappatura e gestisci i casi non riconosciuti
    df['Professional_Group'] = df['Profession'].map(professional_map).fillna('Other')

    # --- Codifica 'Professional_Group' con LabelEncoder ---
    print("\nEseguendo Label Encoding per la colonna 'Professional_Group'...")

    # Inizializziamo LabelEncoder
    label_encoder_profession = LabelEncoder()

    # Fit e trasforma la colonna 'Professional_Group'
    df['Professional_Group_Encoded'] = label_encoder_profession.fit_transform(df['Professional_Group'])

    # Puoi vedere la mappatura creata dal LabelEncoder
    print("\nMappatura Label Encoding per 'Professional_Group':")
    # Crea una Series per mostrare la mappatura
    label_mapping_profession = pd.Series(label_encoder_profession.classes_, name='Professional_Group').to_frame()
    label_mapping_profession['Encoded_Value'] = label_encoder_profession.transform(label_encoder_profession.classes_)
    print(label_mapping_profession)
    
    # KNN per raggruppare in base alla città (miglioria del metodo manuale)

    # --- Definizione e Mappatura delle Regioni ---
    # Definiamo la mappatura Region per City
    region_map = {
        # North-East India
        'Patna': 'North-East India',
        'Varanasi': 'North-East India',
        # North-West India
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
    }

    # Applica la mappatura e gestisci i casi non riconosciuti
    df['Region'] = df['City'].map(region_map).fillna('Other')

    # Raggruppa e conta per regione
    print("\nConteggio delle città per Regione:")
    region_counts = df['Region'].value_counts()
    print(region_counts)

    # --- Codifica 'Region' con LabelEncoder ---
    print("\nEseguendo Label Encoding per la colonna 'Region'...")

    # Inizializziamo LabelEncoder
    label_encoder = LabelEncoder()

    # Fit e trasforma la colonna 'Region'
    df['Region_Encoded'] = label_encoder.fit_transform(df['Region'])
    print("\nMappatura Label Encoding per 'Region':")
    # Crea una Series per mostrare la mappatura
    label_mapping = pd.Series(label_encoder.classes_, name='Region').to_frame()
    label_mapping['Encoded_Value'] = label_encoder.transform(label_encoder.classes_)
    print(label_mapping)

    # --- Verifica dei risultati finali ---
    print("\nDataFrame dopo TUTTE le trasformazioni (imputazione, eliminazione righe, codifica):")
    print(df.head())
    print("\nInformazioni sul DataFrame dopo TUTTE le trasformazioni:")
    print(df.info())
   
    df_clean = df.copy()
    df_clean = df_clean.drop(columns=['City','Name','id','Profession', 'Degree', 'Degree_Group', 'Professional_Group', 'Region'])

    try:
        file_path = r'Mentally\person_test.csv'
        df_clean.to_csv(file_path, index=False)
        print("\nDataFrame esportato con successo in 'person_test.csv'")
    except Exception as e:
        print(f"\nErrore durante l'esportazione del DataFrame: {e}")

    df_clean = df_clean.rename(columns={'Have you ever had suicidal thoughts ?': 'SuicidalThoughts'}) 
    df_clean = df_clean.drop(columns=['SuicidalThoughts'])
    
    return df_clean