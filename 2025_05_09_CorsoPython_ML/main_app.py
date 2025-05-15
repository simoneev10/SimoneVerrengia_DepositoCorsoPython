import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import joblib
import numpy as np
import sys
import os
import threading

# Importa Matplotlib per l'embedding nei frame
import matplotlib.pyplot as plt
# Importa il backend Tkinter per l'embedding
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importa i moduli locali
try:
    # Assicurati che preprocess_train e preprocess_person_test siano in preprocessing.py
    from preprocessing import preprocess_train, elimina_variabili_vif_pvalue, preprocess_person_test
except ImportError:
    messagebox.showerror("Errore di Importazione", "Impossibile importare 'preprocessing.py' o le sue funzioni. Assicurati che sia nella stessa directory e contenga preprocess_train, elimina_variabili_vif_pvalue, preprocess_person_test.")
    sys.exit()

try:
    # Importa il modulo grafici che hai creato/rinominato
    import grafici
except ImportError:
     messagebox.showerror("Errore di Importazione", "Impossibile importare 'grafici.py'. Assicurati che sia nella stessa directory e contenga le funzioni di plottaggio.")
     sys.exit()


# Importa le metriche necessarie
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


# --- Costanti ---
CLEANED_CSV = 'cleaned_data_for_graphs.csv'
PREDICTION_MODEL_FILE = 'best_xgb_clf_smote.pkl' # Nome del file del modello di predizione


# --- Classe Principale dell'Applicazione ---
class DepressionAnalysisApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Analisi e Predizione Depressione")
        self.geometry("800x600") # Dimensioni iniziali
        self.protocol("WM_DELETE_WINDOW", self._on_closing) # Gestisce la chiusura

        # Container dove i frame verranno impilati
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Definisci e crea le istanze dei Frame
        # Passa 'self' come controller a ogni frame
        for F in (MenuFrame, TrainFrame, GraphsFrame, PredictFrame): # Ora includiamo PredictFrame
            page_name = F.__name__
            frame = F(parent=container, controller=self) # Passa self come controller
            self.frames[page_name] = frame

            # Posiziona ogni frame nello stesso posto, saranno impilati
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuFrame") # Mostra la pagina iniziale

    def show_frame(self, page_name):
        """Mostra il frame specificato dal nome della pagina."""
        frame = self.frames[page_name]
        frame.tkraise() # Porta il frame desiderato in primo piano

    def _on_closing(self):
        """Gestisce la chiusura dell'applicazione."""
        try:
            # Chiudi tutte le figure matplotlib aperte prima di distruggere la finestra
            plt.close('all')
        except Exception as e:
            print(f"Avviso: Errore durante la chiusura dei grafici matplotlib: {e}")

        # Distruggi la finestra principale di Tkinter
        self.destroy()


# --- Definizione dei Frame (Pagine dell'applicazione) ---

# --- MenuFrame ---
class MenuFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller # Salva una referenza al controller

        ttk.Label(self, text="Menu Principale", font=("Segoe UI", 20)).pack(pady=20)

        ttk.Button(self, text="Addestra Modelli",
                   command=lambda: controller.show_frame("TrainFrame")).pack(pady=5)

        ttk.Button(self, text="Visualizza Grafici",
                   command=lambda: controller.show_frame("GraphsFrame")).pack(pady=5)

        ttk.Button(self, text="Predizione Singola",
                   command=lambda: controller.show_frame("PredictFrame")).pack(pady=5)


# --- TrainFrame ---
class TrainFrame(ttk.Frame):
    # ... (il codice di TrainFrame è lo stesso di prima) ...
    # Assicurati di aver copiato qui l'intera definizione della classe TrainFrame
    # dall'ultimo script di main_app.py che ti ho fornito.
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Addestramento Modelli", font=("Segoe UI", 20)).grid(row=0, column=0, columnspan=3, pady=10)

        ttk.Label(self, text="Percorso file CSV di training:").grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        self.file_path_entry = ttk.Entry(self, width=50)
        self.file_path_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.columnconfigure(1, weight=1)

        self.browse_button = ttk.Button(self, text="Sfoglia...", command=self._browse_file)
        self.browse_button.grid(column=2, row=1, sticky=tk.W, padx=5, pady=5)

        self.train_button = ttk.Button(self, text="Avvia Addestramento", command=self._start_training)
        self.train_button.grid(column=0, row=2, columnspan=3, pady=10)

        self.status_text = tk.StringVar()
        self.status_text.set("Inserisci il percorso del file CSV e avvia l'addestramento.")
        self.status_label = ttk.Label(self, textvariable=self.status_text, wraplength=600, justify=tk.LEFT, anchor=tk.NW)
        self.rowconfigure(3, weight=1)
        self.status_label.grid(column=0, row=3, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=10)

        ttk.Button(self, text="Indietro", command=lambda: controller.show_frame("MenuFrame")).grid(row=4, column=0, columnspan=3, pady=10)

    def _browse_file(self):
        filepath = filedialog.askopenfilename(
            initialdir=".",
            title="Seleziona file CSV di training",
            filetypes=(("CSV files", "*.csv"), ("all files", "*.*"))
        )
        if filepath:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, filepath)

    def _start_training(self):
        data_path = self.file_path_entry.get()
        if not data_path:
             messagebox.showwarning("Input Mancante", "Per favore, seleziona il file CSV di training.")
             return
        if not os.path.exists(data_path):
            messagebox.showerror("Erroso Percorso File", "Il file specificato non esiste.")
            return
        if not data_path.lower().endswith('.csv'):
             messagebox.showwarning("Formato File", "Per favore, seleziona un file con estensione .csv")
             return

        self.status_text.set("Avvio...")
        self.train_button.config(state=tk.DISABLED)
        self.browse_button.config(state=tk.DISABLED)

        training_thread = threading.Thread(target=self._run_training_process,
                                           args=(data_path, self._update_status))
        training_thread.start()
        self._check_thread(training_thread)

    def _check_thread(self, thread):
        if thread.is_alive():
            self.controller.after(100, self._check_thread, thread)
        else:
            self.train_button.config(state=tk.NORMAL)
            self.browse_button.config(state=tk.NORMAL)

    def _update_status(self, message):
        current_text = self.status_text.get()
        lines = current_text.split('\n')
        if message.strip():
             lines.append(message)
        max_lines = 25
        if len(lines) > max_lines:
            lines = lines[-max_lines:]
        new_text = "\n".join(lines)
        self.controller.after(0, lambda: self.status_text.set(new_text))

    def _run_training_process(self, data_path, status_callback):
        status_callback("Avvio processo di addestramento...")
        try:
            status_callback("Caricamento dati...")
            train_df = pd.read_csv(data_path)
            status_callback(f"Dati caricati da {data_path}")
            status_callback("Avvio preprocessing dati...")
            df_clean = preprocess_train(train_df)
            status_callback("Preprocessing completato.")

            try:
                df_clean.to_csv(CLEANED_CSV, index=False)
                status_callback(f"Dati puliti salvati in '{CLEANED_CSV}' per l'analisi grafica.")
            except Exception as e:
                 status_callback(f"Avviso: Impossibile salvare il file '{CLEANED_CSV}': {e}")

            X = df_clean.drop(columns=['Depression'])
            y = df_clean['Depression']
            status_callback(f"Features iniziali: {list(X.columns)}")
            status_callback("Avvio selezione variabili (VIF/p-value)...")
            X_selected = elimina_variabili_vif_pvalue(X, y)
            status_callback(f"Selezione variabili completata. Features finali: {list(X_selected.columns)}")
            class_distribution = y.value_counts(normalize=True)
            status_callback(f"\nDistribuzione delle classi nel target:\n{class_distribution.to_string()}")
            negative_count, positive_count = np.bincount(y)
            scale_pos_weight = negative_count / positive_count
            status_callback(f"Rapporto delle classi (negativo/positivo): {scale_pos_weight:.2f}")
            status_callback("Separazione dati in train/test (stratified)...")
            X_train, X_test, y_train, y_test = train_test_split(
                X_selected, y,
                test_size=0.2,
                random_state=73,
                stratify=y
            )
            status_callback("Separazione completata.")
            status_callback("Inizializzazione modelli...")
            log_reg = LogisticRegression(random_state=73, max_iter=1000, class_weight='balanced')
            xgb_clf = XGBClassifier(objective='binary:logistic', random_state=73, scale_pos_weight=scale_pos_weight)
            smote = SMOTE(random_state=73, sampling_strategy='auto')
            xgb_smote_pipeline = ImbPipeline([('smote', smote), ('xgb', XGBClassifier(objective='binary:logistic', random_state=73))])
            status_callback("Modelli inizializzati.")
            param_grid = {'xgb__n_estimators': [50, 100],'xgb__max_depth': [3, 5],'xgb__learning_rate': [0.05, 0.1],'xgb__scale_pos_weight': [1, scale_pos_weight]}
            grid_clf = GridSearchCV(xgb_smote_pipeline, param_grid, scoring='f1', cv=5, n_jobs=-1)
            status_callback("Addestramento Logistic Regression...")
            log_reg.fit(X_train, y_train)
            status_callback("Addestramento XGBoost (default)...")
            xgb_clf.fit(X_train, y_train)
            status_callback("Avvio GridSearch per XGBoost (SMOTE)... (Questo potrebbe richiedere tempo)")
            grid_clf.fit(X_train, y_train)
            status_callback("Addestramento modelli completato.")
            best_xgb_clf = grid_clf.best_estimator_
            status_callback(f"\nMigliori parametri per XGBoost (SMOTE):\n{grid_clf.best_params_}")
            status_callback(f"Miglior score F1 (GridSearchCV): {grid_clf.best_score_:.4f}")
            status_callback("Esecuzione predizioni sul test set...")
            y_pred_log = log_reg.predict(X_test)
            y_pred_xgb = xgb_clf.predict(X_test)
            y_pred_xgb_best = best_xgb_clf.predict(X_test)
            status_callback("Predizioni completate.")
            status_callback("Salvataggio modelli addestrati...")
            joblib.dump(best_xgb_clf, PREDICTION_MODEL_FILE) # Salva il modello con il nome della costante
            joblib.dump(log_reg, 'logistic_regression_smote.pkl')
            joblib.dump(xgb_clf, 'xgb_clf_default_smote.pkl')
            status_callback(f"Modelli salvati: '{PREDICTION_MODEL_FILE}', 'logistic_regression_smote.pkl', 'xgb_clf_default_smote.pkl'")
            status_callback("\nCalcolo metriche di valutazione...")
            model_names = ["Logistic Regression", "XGBoost (Default)", "XGBoost (Optimized SMOTE)"]
            y_preds = [y_pred_log, y_pred_xgb, y_pred_xgb_best]
            metrics = {'Accuracy': [], 'Precision': [], 'Recall': [], 'F1 Score': []}
            for y_pred in y_preds:
                metrics['Accuracy'].append(accuracy_score(y_test, y_pred))
                metrics['Precision'].append(precision_score(y_test, y_pred))
                metrics['Recall'].append(recall_score(y_test, y_pred))
                metrics['F1 Score'].append(f1_score(y_test, y_pred))
            metrics_df = pd.DataFrame(metrics, index=model_names)
            status_callback("Metriche calcolate.")
            status_callback("\nConfronti metriche in formato tabella:")
            status_callback(metrics_df.round(4).to_string())
            status_callback("\nProcesso di addestramento completato con successo!")

        except FileNotFoundError:
            status_callback(f"Errore: File non trovato all'indirizzo specificato: {data_path}")
            self.controller.after(0, lambda: messagebox.showerror("Errore File", f"File non trovato:\n{data_path}"))
        except pd.errors.EmptyDataError:
             status_callback(f"Errore: Il file CSV è vuoto o non ha colonne: {data_path}")
             self.controller.after(0, lambda: messagebox.showerror("Errore Dati", f"Il file CSV è vuoto o non ha colonne:\n{data_path}"))
        except Exception as e:
            status_callback(f"Errore critico durante il processo: {type(e).__name__} - {e}")
            print(f"Errore critico: {type(e).__name__} - {e}")
            self.controller.after(0, lambda: messagebox.showerror("Errore Critico", f"Si è verificato un errore durante l'addestramento:\n{type(e).__name__} - {e}"))


# --- GraphsFrame ---
class GraphsFrame(ttk.Frame):
    # ... (il codice di GraphsFrame è lo stesso di prima, include l'import di grafici) ...
    # Assicurati di aver copiato qui l'intera definizione della classe GraphsFrame
    # dall'ultimo script di main_app.py che ti ho fornito (quello con grafici importato).
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Visualizza Grafici", font=("Segoe UI", 20)).pack(pady=10)

        if not os.path.exists(CLEANED_CSV):
            ttk.Label(self, text=f"File '{os.path.basename(CLEANED_CSV)}' non trovato.\nEsegui prima l'addestramento per generarlo.", foreground="red").pack(pady=20)
            ttk.Button(self, text="Indietro", command=lambda: controller.show_frame("MenuFrame")).pack(pady=10)
            self.df = None
            return

        try:
             self.df = pd.read_csv(CLEANED_CSV)
             if self.df.empty:
                  ttk.Label(self, text=f"File '{os.path.basename(CLEANED_CSV)}' è vuoto.\nEsegui correttamente l'addestramento.", foreground="red").pack(pady=20)
                  ttk.Button(self, text="Indietro", command=lambda: controller.show_frame("MenuFrame")).pack(pady=10)
                  self.df = None
                  return
        except pd.errors.EmptyDataError:
             ttk.Label(self, text=f"File '{os.path.basename(CLEANED_CSV)}' è vuoto o danneggiato.\nEsegui correttamente l'addestramento.", foreground="red").pack(pady=20)
             ttk.Button(self, text="Indietro", command=lambda: controller.show_frame("MenuFrame")).pack(pady=10)
             self.df = None
             return
        except Exception as e:
             ttk.Label(self, text=f"Errore nel caricamento di '{os.path.basename(CLEANED_CSV)}':\n{e}", foreground="red").pack(pady=20)
             ttk.Button(self, text="Indietro", command=lambda: controller.show_frame("MenuFrame")).pack(pady=10)
             self.df = None
             return


        frm = ttk.Frame(self)
        frm.pack(fill='both', expand=True, padx=10, pady=10)
        frm.columnconfigure(1, weight=1)

        left = ttk.Frame(frm)
        left.grid(row=0, column=0, sticky='ns', padx=(0,10))

        self.canvas_holder = ttk.Frame(frm)
        self.canvas_holder.grid(row=0, column=1, sticky='nsew')


        self.graphs = {
            "1. Distribuzione Genere":           lambda: grafici.plot_gender_distribution(self.df),
            "2. Studente vs Professionista":     lambda: grafici.plot_status_distribution(self.df),
            "3. Pensieri Suicidi Precedenti":    lambda: grafici.plot_suicidal_thoughts_distribution(self.df['Have you ever had suicidal thoughts ?'].value_counts()),
            "4. Condizione di Depressione":      lambda: grafici.plot_depression_distribution(self.df),
            "5. Depressione per Genere":         lambda: grafici.plot_depression_by_gender(self.df),
            "6. Pensieri Suicidi vs Depressione":lambda: grafici.plot_suicidal_thoughts_by_depression(self.df),
            "7. Depressione per Regione":        lambda: grafici.plot_depression_by_region(self.df),
            "8. Stress Finanziario":             lambda: grafici.plot_financial_stress_by_depression(self.df),
            "9. Età vs Depressione":             lambda: grafici.plot_age_distribution_by_depression(self.df),
            "10. Correlazione Pearson":          lambda: grafici.plot_pearson_correlation(self.df),
            "11. Depressione per Gruppo Laurea": lambda: grafici.plot_depression_by_degree_group(self.df),
            "12. Soddisf. Studio":               lambda: grafici.plot_depression_by_study_satisfaction(self.df),
            "13. Depressione per Status":        lambda: grafici.plot_depression_by_status(self.df),
        }

        for name in self.graphs:
            ttk.Button(left, text=name, width=30,
                       command=lambda n=name: self._show_graph(n))\
                .pack(fill='x', pady=2)

        ttk.Button(self, text="Indietro", command=lambda: controller.show_frame("MenuFrame")).pack(side='bottom', pady=10)

    def _show_graph(self, name):
        for w in self.canvas_holder.winfo_children():
            w.destroy()
        try:
            fig = self.graphs[name]()
        except Exception as e:
             messagebox.showerror("Errore Generazione Grafico", f"Si è verificato un errore durante la creazione del grafico:\n{e}")
             print(f"Errore nella generazione del grafico '{name}': {e}")
             for w in self.canvas_holder.winfo_children():
                 w.destroy()
             return

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_holder)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)


# --- PredictFrame (Nuova Implementazione) ---
class PredictFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller # Salva una referenza al controller

        ttk.Label(self, text="Predizione Singola", font=("Segoe UI", 20)).grid(row=0, column=0, columnspan=4, pady=10)

        # Layout per il form
        form_frame = ttk.Frame(self)
        form_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        form_frame.columnconfigure(1, weight=1) # Colonna per gli input espandibile

        # --- Definizione delle colonne e delle loro proprietà (dal tuo codice originale) ---
        self.feature_definitions = {
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

        # Dizionario per memorizzare i widget di input
        self.input_widgets = {}
        row_counter = 0

        # Crea i widget di input dinamicamente basandosi su feature_definitions
        for col, definition in self.feature_definitions.items():
            ttk.Label(form_frame, text=f"{col}:").grid(column=0, row=row_counter, sticky=tk.W, pady=2, padx=5)

            if definition['type'] == 'numeric' or definition['type'] == 'text':
                entry = ttk.Entry(form_frame, width=40)
                entry.grid(column=1, row=row_counter, sticky=(tk.W, tk.E), pady=2, padx=5)
                self.input_widgets[col] = entry
                if definition['type'] == 'numeric':
                     # Aggiungi il range come suggerimento accanto all'entry
                     ttk.Label(form_frame, text=f"({definition['range'][0]}-{definition['range'][1]})").grid(column=2, row=row_counter, sticky=tk.W, pady=2, padx=5)


            elif definition['type'] == 'categorical':
                # Usa Combobox per le scelte categoriche
                combobox = ttk.Combobox(form_frame, values=definition['options'], state='readonly', width=38)
                combobox.grid(column=1, row=row_counter, sticky=(tk.W, tk.E), pady=2, padx=5)
                self.input_widgets[col] = combobox

            # Rendi la colonna 1 del form_frame espandibile
            form_frame.columnconfigure(1, weight=1)


            row_counter += 1

        # Pulsante Esegui Predizione
        predict_button = ttk.Button(self, text="Esegui Predizione", command=self._perform_prediction)
        predict_button.grid(row=2, column=0, columnspan=4, pady=10)

        # Label per il risultato della predizione
        self.result_text = tk.StringVar()
        self.result_text.set("Inserisci i dati e clicca 'Esegui Predizione'.")
        result_label = ttk.Label(self, textvariable=self.result_text, wraplength=600, justify=tk.CENTER, font=("Segoe UI", 12, "bold"))
        result_label.grid(row=3, column=0, columnspan=4, pady=10)

        # Pulsante Indietro
        ttk.Button(self, text="Indietro", command=lambda: controller.show_frame("MenuFrame")).grid(row=4, column=0, columnspan=4, pady=10)

        # Carica il modello una volta all'inizializzazione del frame
        self.model = None
        self.model_loaded = False
        try:
            self.model = joblib.load(PREDICTION_MODEL_FILE)
            self.model_loaded = True
        except FileNotFoundError:
            messagebox.showerror("Errore Modello", f"File del modello '{PREDICTION_MODEL_FILE}' non trovato.\nEsegui prima l'addestramento per generarlo.")
            self.result_text.set(f"Errore: Modello '{PREDICTION_MODEL_FILE}' non trovato.")
            predict_button.config(state=tk.DISABLED) # Disabilita il pulsante se il modello non c'è
        except Exception as e:
             messagebox.showerror("Errore Caricamento Modello", f"Errore durante il caricamento del modello '{PREDICTION_MODEL_FILE}':\n{e}")
             self.result_text.set(f"Errore caricamento modello: {e}")
             predict_button.config(state=tk.DISABLED) # Disabilita il pulsante in caso di altri errori


    def _perform_prediction(self):
        """Raccoglie i dati dalla GUI, li valida, esegue il preprocessing e la predizione."""
        if not self.model_loaded:
            messagebox.showerror("Errore", "Modello di predizione non caricato. Esegui prima l'addestramento.")
            return

        data = {'id': [0]} # Aggiungi l'id dummy come richiesto dal preprocessing (se necessario)
        errors = []

        # Raccogli e valida i dati dai widget
        for col, definition in self.feature_definitions.items():
            widget = self.input_widgets[col]
            value = widget.get().strip() # Usa strip() per rimuovere spazi bianchi

            if definition['type'] == 'numeric':
                lo, hi = definition['range']
                if not value: # Controlla se il campo è vuoto
                     errors.append(f"'{col}': campo richiesto")
                     continue
                try:
                    # Prova a convertire in float o int in base al range
                    if isinstance(lo, float) or isinstance(hi, float):
                         val = float(value)
                    else:
                         val = int(value)

                    if not (lo <= val <= hi):
                        errors.append(f"'{col}': valore fuori range ({lo}-{hi})")
                        continue
                    data[col] = [val] # Aggiungi il valore valido
                except ValueError:
                    errors.append(f"'{col}': non è un numero valido")
                    continue
            elif definition['type'] == 'categorical':
                 if not value: # Controlla se il campo è vuoto (Combobox vuota)
                     errors.append(f"'{col}': selezione richiesta")
                     continue
                 if value not in definition['options']:
                      # Questo non dovrebbe succedere con Combobox readonly, ma è una buona precauzione
                      errors.append(f"'{col}': opzione '{value}' non valida")
                      continue
                 data[col] = [value] # Aggiungi il valore valido
            else: # 'text' o altri tipi
                if not value and col != 'Name' and col != 'City' and col != 'Profession' and col != 'Degree' and col != 'Working Professional or Student':
                     # Controlla se campi di testo *non* opzionali sono vuoti (adatta i nomi opzionali)
                     errors.append(f"'{col}': campo richiesto")
                     continue
                data[col] = [value] # Aggiungi il valore così com'è

        if errors:
            # Mostra un messaggio di errore se ci sono problemi
            messagebox.showerror("Errore di input", "\n".join(errors))
            self.result_text.set("Errore di input. Controlla i dati inseriti.")
            return # Ferma l'esecuzione se la validazione fallisce

        # Creazione DataFrame dal singolo input validato
        user_df_raw = pd.DataFrame(data)

        # Applica il preprocessing
        try:
            # Assicurati che preprocess_person_test gestisca il DataFrame con 'id'
            # e che le feature siano nell'ordine atteso dal modello se il preprocessing riordina
            df_clean = preprocess_person_test(user_df_raw)
        except Exception as e:
            messagebox.showerror("Errore di Preprocessing", f"Si è verificato un errore durante il preprocessing:\n{e}")
            print(f"Errore durante il preprocessing: {e}")
            print(f"DataFrame raw prima del preprocessing:\n{user_df_raw}")
            self.result_text.set("Errore durante il preprocessing.")
            return

        # Esegui la predizione
        try:
            y_pred = self.model.predict(df_clean)
            # Assicurati che il modello abbia predict_proba
            if hasattr(self.model, 'predict_proba'):
                proba = self.model.predict_proba(df_clean)[:, 1] # Probabilità per la classe positiva (Depressione=1)
                proba_text = f" (probabilità: {proba[0]:.2%})"
            else:
                proba_text = ""


            # Mostra il risultato
            if y_pred[0] == 1:
                self.result_text.set(f"Risultato: La persona potrebbe essere depressa{proba_text}.")
            else:
                self.result_text.set(f"Risultato: La persona non sembra depressa{proba_text}.")

        except Exception as e:
            messagebox.showerror("Errore di Predizione", f"Si è verificato un errore durante la predizione:\n{e}")
            print(f"Errore durante la predizione: {e}")
            print(f"DataFrame pulito usato per la predizione:\n{df_clean}")
            self.result_text.set("Errore durante la predizione.")



# --- Esecuzione dell'applicazione ---
if __name__ == "__main__":
    app = DepressionAnalysisApp()
    app.mainloop()