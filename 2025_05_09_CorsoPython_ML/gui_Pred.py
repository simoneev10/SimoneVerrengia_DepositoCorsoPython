import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import joblib
import sys
import os

# Aggiungi la directory corrente al PATH per trovare 'preprocessing.py'
# Assicurati che preprocessing.py sia nella stessa directory di gui_app.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from preprocessing import preprocess_person_test # Importa la funzione di preprocessing

# --- Caricamento del modello (Caricalo una volta all'avvio dell'app) ---
try:
    model = joblib.load('best_xgb_clf_smote.pkl')
    model_loaded = True
except FileNotFoundError:
    model = None
    model_loaded = False
    print("Errore: File del modello 'best_xgb_clf_smote.pkl' non trovato.")
    print("Assicurati che il file del modello si trovi nella stessa directory di gui_app.py.")
except Exception as e:
    model = None
    model_loaded = False
    print(f"Errore durante il caricamento del modello: {e}")

# --- Definizione delle colonne e delle loro proprietà ---
# Questi dati erano nella funzione gather_input e insert_data
feature_definitions = {
    'Name': {'type': 'text'},
    'Gender': {'type': 'categorical', 'options': ['Male', 'Female']},
    'Age': {'type': 'numeric', 'range': (18, 60)},
    'City': {'type': 'text'},
    'Working Professional or Student': {'type': 'text'}, # Potrebbe diventare categorico?
    'Profession': {'type': 'text'},
    'Academic Pressure': {'type': 'numeric', 'range': (0, 5)},
    'Work Pressure': {'type': 'numeric', 'range': (0, 5)},
    'CGPA': {'type': 'numeric', 'range': (0.0, 10.0)},
    'Study Satisfaction': {'type': 'numeric', 'range': (0, 5)},
    'Job Satisfaction': {'type': 'numeric', 'range': (0, 5)},
    'Sleep Duration': {'type': 'numeric', 'range': (0.0, 12.0)},
    'Dietary Habits': {'type': 'categorical', 'options': ['Unhealthy', 'Moderate', 'Healthy']},
    'Degree': {'type': 'text'},
    'Have you ever had suicidal thoughts ?': {'type': 'categorical', 'options': ['Yes', 'No']},
    'Work/Study Hours': {'type': 'numeric', 'range': (0.0, 12.0)},
    'Financial Stress': {'type': 'numeric', 'range': (0, 5)},
    'Family History of Mental Illness': {'type': 'categorical', 'options': ['Yes', 'No']}
}

# Dizionario per memorizzare i widget di input (Entry o Combobox)
input_widgets = {}

# --- Funzione per raccogliere e validare i dati dalla GUI ---
def collect_and_validate_data():
    data = {'id': [0]} # Aggiungi l'id dummy come nell'originale
    errors = []

    for col, definition in feature_definitions.items():
        widget = input_widgets[col]
        value = widget.get()

        # Validazione
        if definition['type'] == 'numeric':
            lo, hi = definition['range']
            try:
                # Prova a convertire in float o int in base al range
                if isinstance(lo, float) or isinstance(hi, float):
                     val = float(value)
                else:
                     val = int(value)

                if not (lo <= val <= hi):
                    errors.append(f"'{col}': valore fuori range ({lo}-{hi})")
                    continue # Passa alla prossima colonna in caso di errore
                data[col] = [val] # Aggiungi il valore valido
            except ValueError:
                errors.append(f"'{col}': non è un numero valido")
                continue # Passa alla prossima colonna in caso di errore
        elif definition['type'] == 'categorical':
            if value not in definition['options']:
                 # Questo non dovrebbe succedere con Combobox readonly, ma è una buona precauzione
                 errors.append(f"'{col}': opzione non valida scelta")
                 continue # Passa alla prossima colonna in caso di errore
            data[col] = [value] # Aggiungi il valore valido
        else: # 'text' o altri tipi non validati specificamente
            data[col] = [value] # Aggiungi il valore così com'è

    if errors:
        # Mostra un messaggio di errore se ci sono problemi
        messagebox.showerror("Errore di input", "\n".join(errors))
        return None # Indica che la validazione è fallita
    else:
        # Restituisce il DataFrame se la validazione è passata
        return pd.DataFrame(data)

# --- Funzione che esegue la predizione (triggered by button) ---
def perform_prediction():
    if not model_loaded:
        messagebox.showerror("Errore", "Modello non caricato. Controlla i messaggi nel terminale per i dettagli.")
        return

    # 1. Raccogli e valida i dati dalla GUI
    user_df_raw = collect_and_validate_data()

    if user_df_raw is None:
        return # Ferma l'esecuzione se la validazione fallisce

    # 2. Applica il preprocessing
    try:
        # Assicurati che preprocess_person_test gestisca il DataFrame con 'id'
        df_clean = preprocess_person_test(user_df_raw)
    except Exception as e:
        messagebox.showerror("Errore di Preprocessing", f"Si è verificato un errore durante il preprocessing: {e}")
        print(f"Errore durante il preprocessing: {e}")
        print(f"DataFrame raw prima del preprocessing:\n{user_df_raw}")
        return

    # 3. Esegui la predizione
    try:
        y_pred = model.predict(df_clean)
        proba = model.predict_proba(df_clean)[:, 1] # Probabilità per la classe positiva
    except Exception as e:
        messagebox.showerror("Errore di Predizione", f"Si è verificato un errore durante la predizione: {e}")
        print(f"Errore durante la predizione: {e}")
        print(f"DataFrame pulito usato per la predizione:\n{df_clean}")
        return


    # 4. Mostra il risultato nella GUI
    result_text = ""
    if y_pred[0] == 1:
        result_text = f"Risultato: La persona potrebbe essere depressa (probabilità: {proba[0]:.2%})."
    else:
        result_text = f"Risultato: La persona non sembra depressa (probabilità: {proba[0]:.2%})."

    result_label.config(text=result_text) # Aggiorna il testo della label di risultato

# --- Creazione dell'Interfaccia Grafica ---
root = tk.Tk()
root.title("Applicazione di Predizione Depressione")

# Usa un frame principale per padding
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Configura le colonne per espandersi
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=2) # Colonna per i campi di input più larga

row_counter = 0

# Crea i widget di input dinamicamente
for col, definition in feature_definitions.items():
    ttk.Label(main_frame, text=f"{col}:").grid(column=0, row=row_counter, sticky=tk.W, pady=2, padx=5)

    if definition['type'] == 'numeric' or definition['type'] == 'text':
        entry = ttk.Entry(main_frame, width=40)
        entry.grid(column=1, row=row_counter, sticky=(tk.W, tk.E), pady=2, padx=5)
        input_widgets[col] = entry
        if definition['type'] == 'numeric':
             ttk.Label(main_frame, text=f"({definition['range'][0]}-{definition['range'][1]})").grid(column=2, row=row_counter, sticky=tk.W, pady=2, padx=5)

    elif definition['type'] == 'categorical':
        combobox = ttk.Combobox(main_frame, values=definition['options'], state='readonly', width=38) # state='readonly' impedisce input manuale
        combobox.grid(column=1, row=row_counter, sticky=(tk.W, tk.E), pady=2, padx=5)
        # Imposta un valore di default se ce n'è uno preferito, altrimenti lascialo vuoto
        # if definition['options']:
        #     combobox.current(0) # Seleziona il primo elemento come default
        input_widgets[col] = combobox

    row_counter += 1

# Aggiungi un pulsante per la predizione
predict_button = ttk.Button(main_frame, text="Esegui Predizione", command=perform_prediction)
predict_button.grid(column=0, row=row_counter, columnspan=3, pady=15)

row_counter += 1

# Aggiungi una Label per mostrare il risultato
result_label = ttk.Label(main_frame, text="Attendi input...", wraplength=400) # wraplength per andare a capo
result_label.grid(column=0, row=row_counter, columnspan=3, pady=10)


# --- Avvia il loop principale della GUI ---
# Disabilita il pulsante se il modello non è stato caricato correttamente
if not model_loaded:
    predict_button.config(state=tk.DISABLED)
    result_label.config(text="Errore: Impossibile caricare il modello. Controlla il terminale.")


root.mainloop()