import pandas as pd
from preprocessing import preprocess_person_test
import joblib

def gather_input(feature_columns):
    
    # Chiede all'utente di inserire i valori per ciascuna colonna non preprocessata.
    # Validazione per colonne numeriche e visualizzazione opzioni per colonne categoriche.
    # Restituisce un DataFrame con una singola riga comprensivo di 'id' dummy.
    print("Inserisci i seguenti dati:")
    data = {'id': [0]}

    # Range per colonne numeriche
    numeric_ranges = {
        'Age': (18, 60),
        'Academic Pressure': (1, 5),
        'Work Pressure': (0, 5),
        'Study Satisfaction': (0, 5),
        'Job Satisfaction': (0, 5),
        'Financial Stress': (1, 5),
        'CGPA': (0.0, 10.0),
        'Sleep Duration': (0.0, 12.0),
        'Work/Study Hours': (0.0, 12.0)
    }

    # Opzioni per colonne categoriche
    categorical_options = {
        'Gender': ['Male', 'Female'],
        'Dietary Habits': ['Unhealthy', 'Moderate', 'Healthy'],
        'Have you ever had suicidal thoughts ?': ['Yes', 'No'],
        'Family History of Mental Illness': ['Yes', 'No']
    }

    for col in feature_columns:
        # Costruisci prompt
        if col in numeric_ranges:
            lo, hi = numeric_ranges[col]
            prompt = f"- {col} (valore numerico tra {lo} e {hi}): "
        elif col in categorical_options:
            opts = categorical_options[col]
            prompt = f"- {col} (scegli tra {opts}): "
        else:
            prompt = f"- {col}: "

        # Loop di validazione
        while True:
            raw = input(prompt).strip()
            # Se colonna numerica
            if col in numeric_ranges:
                lo, hi = numeric_ranges[col]
                try:
                    val = float(raw) if isinstance(lo, float) else int(raw)
                    if not (lo <= val <= hi):
                        raise ValueError
                except ValueError:
                    print(f"Input non valido. Inserisci un numero tra {lo} e {hi}.")
                    continue
            # Se colonna categorica
            elif col in categorical_options:
                if raw not in categorical_options[col]:
                    print(f"Input non valido. Scegli una delle opzioni: {categorical_options[col]}")
                    continue
                val = raw
            # Altri tipi (es. stringhe libere)
            else:
                val = raw
            break

        data[col] = [val]

    return pd.DataFrame(data)

def insert_data():
    # Definisci qui le colonne raw (escludendo 'id')
    feature_columns = [
        'Name',
        'Gender',
        'Age',
        'City',
        'Working Professional or Student',
        'Profession',
        'Academic Pressure',
        'Work Pressure',
        'CGPA',
        'Study Satisfaction',
        'Job Satisfaction',
        'Sleep Duration',
        'Dietary Habits',
        'Degree',
        'Have you ever had suicidal thoughts ?',
        'Work/Study Hours',
        'Financial Stress',
        'Family History of Mental Illness'
    ]

    # Raccogli i dati dell'utente
    user_df = gather_input(feature_columns)

    # Applica il preprocessing (ora user_df contiene 'id')
    df_clean = preprocess_person_test(user_df)

    # Carica il modello
    model = joblib.load('best_xgb_clf_smote.pkl')

# Predizione
    y_pred = model.predict(df_clean)
    proba = model.predict_proba(df_clean)[:, 1]  # Probabilità per la classe positiva

    # Stampa il risultato per l'utente
    if y_pred[0] == 1:
        print(f"Risultato: La persona potrebbe essere depressa (probabilità: {proba[0]:.2%}).")
    else:
        print(f"Risultato: La persona non sembra depressa (probabilità: {proba[0]:.2%}).")
