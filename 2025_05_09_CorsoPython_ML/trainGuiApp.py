import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import joblib
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os
import threading # Useremo threading per non bloccare la GUI durante l'addestramento

# Aggiungi la directory corrente al PATH per trovare 'preprocessing.py'
# Assicurati che preprocessing.py sia nella stessa directory di train_gui_app.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from preprocessing import preprocess_train, elimina_variabili_vif_pvalue
except ImportError:
    messagebox.showerror("Errore di Importazione", "Impossibile importare le funzioni di preprocessing. Assicurati che 'preprocessing.py' sia nella stessa directory.")
    sys.exit() # Esci se preprocessing non può essere importato

# Importa le metriche necessarie (assicurati che siano installate: pip install scikit-learn imbalanced-learn xgboost)
try:
    from sklearn.model_selection import GridSearchCV, train_test_split
    from sklearn.linear_model import LogisticRegression
    from xgboost import XGBClassifier
    from imblearn.over_sampling import SMOTE
    from imblearn.pipeline import Pipeline as ImbPipeline
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
except ImportError:
    messagebox.showerror("Errore di Importazione", "Impossibile importare le librerie di Machine Learning (sklearn, imblearn, xgboost). Assicurati che siano installate (pip install scikit-learn imbalanced-learn xgboost).")
    sys.exit()


# --- Funzioni di Plottaggio (prese dal tuo codice originale) ---
def plot_combined_confusion_matrices(y_true, y_pred_list, model_names):
    plt.figure(figsize=(15, 4))

    for i, (y_pred, name) in enumerate(zip(y_pred_list, model_names)):
        plt.subplot(1, 3, i+1)
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
        plt.title(f"Confusion Matrix - {name}")
        plt.ylabel('Actual')
        plt.xlabel('Predicted')

    plt.tight_layout()
    # Non chiamiamo plt.show() qui, lo faremo alla fine della funzione di training per mostrarli tutti insieme.


def plot_metrics_comparison(y_true, y_pred_list, model_names):
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

    # Creiamo un DataFrame per facilitare la visualizzazione
    metrics_df = pd.DataFrame(metrics, index=model_names)

    # Plot
    metrics_df.plot(kind='bar', figsize=(12, 6))
    plt.title('Confronto delle metriche tra i modelli')
    plt.ylabel('Score')
    plt.ylim(0, 1.0)
    plt.xticks(rotation=0)
    plt.legend(loc='lower right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    # Non chiamiamo plt.show() qui

    return metrics_df

# --- Funzione principale di Addestramento (Adattata per la GUI) ---
def run_training_process(data_path, status_callback, root_window):
    """
    Esegue l'intero processo di training e valutazione.
    Inviando aggiornamenti di stato tramite status_callback.
    """
    status_callback("Avvio processo di addestramento...")

    try:
        # Caricamento dei dati
        status_callback("Caricamento dati...")
        train_df = pd.read_csv(data_path)
        status_callback(f"Dati caricati da {data_path}")

        # Preprocessing
        status_callback("Avvio preprocessing dati...")
        df_clean = preprocess_train(train_df)
        status_callback("Preprocessing completato.")

        # Selezione delle Feature e del Target
        X = df_clean.drop(columns=['Depression'])
        y = df_clean['Depression']
        status_callback(f"Features iniziali: {list(X.columns)}")

        # Eliminazione variabili con VIF/pValue
        status_callback("Avvio selezione variabili (VIF/p-value)...")
        X_selected = elimina_variabili_vif_pvalue(X, y)
        status_callback(f"Selezione variabili completata. Features finali: {list(X_selected.columns)}")

        # Distribuzione delle classi
        class_distribution = y.value_counts(normalize=True)
        status_callback(f"\nDistribuzione delle classi nel target:\n{class_distribution.to_string()}") # Usa to_string per formattazione migliore in label

        # Calcoliamo il rapporto per scale_pos_weight
        negative_count, positive_count = np.bincount(y)
        scale_pos_weight = negative_count / positive_count
        status_callback(f"Rapporto delle classi (negativo/positivo): {scale_pos_weight:.2f}")

        # Separazione train/test
        status_callback("Separazione dati in train/test (stratified)...")
        X_train, X_test, y_train, y_test = train_test_split(
            X_selected, y,
            test_size=0.2,
            random_state=73,
            stratify=y
        )
        status_callback("Separazione completata.")

        # Inizializzazione modelli
        status_callback("Inizializzazione modelli...")
        log_reg = LogisticRegression(
            random_state=73,
            max_iter=1000,
            class_weight='balanced'
        )
        xgb_clf = XGBClassifier(
            objective='binary:logistic',
            random_state=73,
            scale_pos_weight=scale_pos_weight
        )
        smote = SMOTE(random_state=73, sampling_strategy='auto')
        xgb_smote_pipeline = ImbPipeline([
            ('smote', smote),
            ('xgb', XGBClassifier(objective='binary:logistic', random_state=73))
        ])
        status_callback("Modelli inizializzati.")

        # Parametri per la GridSearch (usiamo un set ridotto per demo veloce, aumenta per risultati migliori)
        param_grid = {
            'xgb__n_estimators': [50, 100], # Ridotto per demo veloce
            'xgb__max_depth': [3, 5],      # Ridotto per demo veloce
            'xgb__learning_rate': [0.05, 0.1], # Ridotto per demo veloce
            'xgb__scale_pos_weight': [1, scale_pos_weight]
        }
        # Per un addestramento più approfondito, usa:
        # param_grid = {
        #     'xgb__n_estimators': [50, 100, 200, 300],
        #     'xgb__max_depth': [3, 5, 7, 9],
        #     'xgb__learning_rate': [0.01, 0.05, 0.1, 0.2],
        #     'xgb__scale_pos_weight': [1, scale_pos_weight, scale_pos_weight * 0.5, scale_pos_weight * 2]
        # }


        grid_clf = GridSearchCV(
            xgb_smote_pipeline, # Usa la pipeline
            param_grid,
            scoring='f1', # Utilizza una metrica appropriata per dataset sbilanciato
            cv=5,
            n_jobs=-1 # Usa tutti i core disponibili
        )

        # Addestramento modelli
        status_callback("Addestramento Logistic Regression...")
        log_reg.fit(X_train, y_train)
        status_callback("Addestramento XGBoost (default)...")
        xgb_clf.fit(X_train, y_train)
        status_callback("Avvio GridSearch per XGBoost (SMOTE)... (Questo potrebbe richiedere tempo)")
        grid_clf.fit(X_train, y_train)
        status_callback("Addestramento modelli completato.")

        # Miglior modello con SMOTE (dal GridSearch)
        best_xgb_clf = grid_clf.best_estimator_
        status_callback(f"\nMigliori parametri per XGBoost (SMOTE):\n{grid_clf.best_params_}")
        status_callback(f"Miglior score F1 (GridSearchCV): {grid_clf.best_score_:.4f}")


        # Predizioni sui dati di test
        status_callback("Esecuzione predizioni sul test set...")
        y_pred_log = log_reg.predict(X_test)
        y_pred_xgb = xgb_clf.predict(X_test)
        y_pred_xgb_best = best_xgb_clf.predict(X_test)
        status_callback("Predizioni completate.")

        # Salvataggio modelli
        status_callback("Salvataggio modelli addestrati...")
        joblib.dump(best_xgb_clf, 'best_xgb_clf_smote.pkl')
        joblib.dump(log_reg, 'logistic_regression_smote.pkl')
        joblib.dump(xgb_clf, 'xgb_clf_default_smote.pkl')
        status_callback("Modelli salvati: 'best_xgb_clf_smote.pkl', 'logistic_regression_smote.pkl', 'xgb_clf_default_smote.pkl'")

        # Visualizzazione e confronto (chiama le funzioni di plottaggio)
        status_callback("Generazione grafici...")
        plot_combined_confusion_matrices(
            y_test,
            [y_pred_log, y_pred_xgb, y_pred_xgb_best],
            ["Logistic Regression", "XGBoost (Default)", "XGBoost (Optimized SMOTE)"]
        )

        metrics_df = plot_metrics_comparison(
            y_test,
            [y_pred_log, y_pred_xgb, y_pred_xgb_best],
            ["Logistic Regression", "XGBoost (Default)", "XGBoost (Optimized SMOTE)"]
        )
        status_callback("Grafici generati. Verranno visualizzati in finestre separate.")
        status_callback("\nConfronti metriche in formato tabella:")
        status_callback(metrics_df.round(4).to_string()) # Converte il DataFrame in stringa

        # Mostra i grafici (chiamato dal thread principale tramite after)
        root_window.after(0, plt.show)

        status_callback("\nProcesso di addestramento completato con successo!")

    except FileNotFoundError:
        status_callback(f"Errore: File non trovato all'indirizzo specificato: {data_path}")
        # Mostra anche una message box
        root_window.after(0, lambda: messagebox.showerror("Errore File", f"File non trovato:\n{data_path}"))
    except pd.errors.EmptyDataError:
         status_callback(f"Errore: Il file CSV è vuoto o non ha colonne: {data_path}")
         root_window.after(0, lambda: messagebox.showerror("Errore Dati", f"Il file CSV è vuoto o non ha colonne:\n{data_path}"))
    except Exception as e:
        # In caso di altri errori non gestiti
        status_callback(f"Errore critico durante il processo: {type(e).__name__} - {e}")
        print(f"Errore critico: {type(e).__name__} - {e}") # Stampa anche nel terminale per debug
        root_window.after(0, lambda: messagebox.showerror("Errore Critico", f"Si è verificato un errore durante l'addestramento:\n{type(e).__name__} - {e}"))


# --- Funzione trigger per il pulsante ---
def start_training():
    data_path = file_path_entry.get()
    if not data_path:
         messagebox.showwarning("Input Mancante", "Per favore, seleziona il file CSV di training.")
         return
    if not os.path.exists(data_path):
        messagebox.showerror("Errore Percorso File", "Il file specificato non esiste.")
        return
    if not data_path.lower().endswith('.csv'):
         messagebox.showwarning("Formato File", "Per favore, seleziona un file con estensione .csv")
         return


    # Pulisce l'area di stato
    status_text.set("Avvio...")

    # Disabilita il pulsante per evitare click multipli
    train_button.config(state=tk.DISABLED)
    browse_button.config(state=tk.DISABLED)

    # Esegue l'addestramento in un thread separato
    # Passiamo la funzione per aggiornare lo stato e la finestra root per plt.show()
    training_thread = threading.Thread(target=run_training_process,
                                       args=(data_path, update_status, root))
    training_thread.start()

    # Abilita i pulsanti una volta che il thread finisce
    # Usiamo check_thread per monitorare il thread
    check_thread(training_thread)


# Funzione per controllare se il thread è finito e riabilitare i pulsanti
def check_thread(thread):
    if thread.is_alive():
        # Se il thread è ancora vivo, pianifica un altro controllo tra 100ms
        root.after(100, check_thread, thread)
    else:
        # Se il thread è finito, riabilita i pulsanti
        train_button.config(state=tk.NORMAL)
        browse_button.config(state=tk.NORMAL)


# Funzione callback per aggiornare la Label di stato (chiamata dal thread di training)
def update_status(message):
    """Aggiorna la label di stato nella GUI (thread-safe tramite root.after)."""
    # Aggiungi il nuovo messaggio e mantieni solo le ultime 20 righe (circa) per non riempire troppo
    current_text = status_text.get()
    lines = current_text.split('\n')
    # Evita di aggiungere messaggi vuoti se la callback viene chiamata senza testo
    if message.strip():
         lines.append(message)
    # Mantieni solo le ultime N righe (es. 25 righe)
    max_lines = 25
    if len(lines) > max_lines:
        lines = lines[-max_lines:]

    new_text = "\n".join(lines)

    # Pianifica l'aggiornamento sulla Label nel thread principale
    root.after(0, lambda: status_text.set(new_text))
    # Forzare l'aggiornamento della GUI immediatamente (opzionale, ma a volte utile)
    # root.after(0, root.update_idletasks)


# --- Gestione chiusura finestra e plot Matplotlib ---
def on_closing():
    """
    Gestisce la chiusura della finestra principale.
    Chiude esplicitamente i grafici matplotlib prima di distruggere la finestra Tkinter
    per evitare errori durante la pulizia.
    """
    print("Tentativo di chiusura...") # Per debug nel terminale
    try:
        # Chiudi tutte le figure matplotlib aperte
        # Questo è cruciale per evitare l'errore RuntimeError durante la pulizia
        plt.close('all') # 'all' chiude tutte le figure
        print("Grafici matplotlib chiusi.") # Per debug
    except Exception as e:
        print(f"Avviso: Errore durante la chiusura dei grafici matplotlib: {type(e).__name__} - {e}")
        # Non bloccare, procedi comunque alla distruzione della finestra principale

    # Distruggi la finestra principale di Tkinter
    root.destroy()
    print("Finestra Tkinter distrutta.") # Per debug


# --- Creazione dell'Interfaccia Grafica ---
root = tk.Tk()
root.title("Tool di Addestramento Modelli Depressione")

# Collega la funzione on_closing all'evento di chiusura della finestra
root.protocol("WM_DELETE_WINDOW", on_closing)

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

main_frame.columnconfigure(1, weight=1) # Rendi l'entry del path espandibile

# Widget per il percorso del file CSV
ttk.Label(main_frame, text="Percorso file CSV di training:").grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
file_path_entry = ttk.Entry(main_frame, width=50)
file_path_entry.grid(column=1, row=0, sticky=(tk.W, tk.E), padx=5, pady=5)

# Funzione per aprire il file dialog
def browse_file():
    filepath = filedialog.askopenfilename(
        initialdir=".", # Puoi impostare una directory iniziale
        title="Seleziona file CSV di training",
        filetypes=(("CSV files", "*.csv"), ("all files", "*.*"))
    )
    if filepath:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, filepath)

browse_button = ttk.Button(main_frame, text="Sfoglia...", command=browse_file)
browse_button.grid(column=2, row=0, sticky=tk.W, padx=5, pady=5)

# Pulsante per avviare l'addestramento
train_button = ttk.Button(main_frame, text="Avvia Addestramento", command=start_training)
train_button.grid(column=0, row=1, columnspan=3, pady=10)

# Label per lo stato (usiamo un Text widget o aumentare wraplength e righe per più output)
# Ho modificato update_status per gestire l'accumulo di testo nella StringVar per mostrare più righe
status_text = tk.StringVar()
status_text.set("Inserisci il percorso del file CSV e avvia l'addestramento.")
# Aumenta wraplength per permettere più testo sulla stessa riga prima di andare a capo
# Usa anchor=tk.NW per allineare il testo in alto a sinistra
status_label = ttk.Label(main_frame, textvariable=status_text, wraplength=600, justify=tk.LEFT, anchor=tk.NW)
# Aumenta l'altezza della riga per dare più spazio alla label di stato
main_frame.rowconfigure(2, weight=1) # Permette alla riga della label di espandersi
status_label.grid(column=0, row=2, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=10)


# --- Avvia il loop principale della GUI ---
# root.mainloop() deve essere l'ultima chiamata bloccante nel thread principale
root.mainloop()