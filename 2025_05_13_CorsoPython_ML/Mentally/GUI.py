import os
import sys
import warnings
import threading
import pandas as pd
import joblib
import numpy as np
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QPushButton, QFileDialog, QMessageBox,
    QLineEdit, QTextEdit, QComboBox
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from preprocessing import preprocess_train, elimina_variabili_vif_pvalue, preprocess_person_test
import graphicGui

warnings.filterwarnings("ignore", message=".*use_label_encoder.*")

# Costanti
CLEANED_CSV = 'data/cleaned_data_for_graphs.csv'
DEFAULT_MODEL_FILE = 'modelli/best_xgb_clf_smote.pkl'


class Worker(QObject):
    status = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, data_path):
        super().__init__()
        self.data_path = data_path

    def run(self):
        try:
            self.status.emit("Caricamento dati...")
            df = pd.read_csv(self.data_path)
            
            os.makedirs('data', exist_ok=True)
            
            self.status.emit("Preprocessing...")
            df_clean = preprocess_train(df)
            df_clean.to_csv(CLEANED_CSV, index=False)

            X = df_clean.drop(columns=['Depression'])
            y = df_clean['Depression']
            self.status.emit("Selezione variabili...")
            X_sel = elimina_variabili_vif_pvalue(X.copy(), y.copy()) 

            self.status.emit("Preparazione modelli...")
            counts = np.bincount(y)
            if len(counts) < 2:
                 self.status.emit("Errore: La colonna target 'Depression' contiene solo una classe dopo il preprocessing.")
                 self.finished.emit()
                 return
            neg, pos = counts
            scale = neg / pos if pos > 0 else 1.0 # scale_pos_weight

            X_train, X_test, y_train, y_test = train_test_split(
                X_sel, y, test_size=0.2, random_state=73, stratify=y
            )

            log_reg = LogisticRegression(random_state=73, max_iter=1000, class_weight='balanced')
            xgb_model_default = XGBClassifier(objective='binary:logistic', random_state=73, scale_pos_weight=scale, eval_metric='logloss')
            
            smote = SMOTE(random_state=73)
            pipeline_xgb_smote = ImbPipeline([
                ('smote', smote),
                ('xgb', XGBClassifier(objective='binary:logistic', random_state=73, eval_metric='logloss'))
            ])
            
            param_grid_xgb_smote = {
                'xgb__n_estimators': [50, 100], # Valori ridotti per test più rapidi, espandere se necessario
                'xgb__max_depth': [3, 5],
                'xgb__learning_rate': [0.05, 0.1],
                'xgb__scale_pos_weight': [1, scale] 
            }
            grid_search_cv = GridSearchCV(pipeline_xgb_smote, param_grid_xgb_smote, scoring='f1', cv=3, n_jobs=-1) # cv ridotto per test più rapidi

            self.status.emit("Addestramento modelli...")
            log_reg.fit(X_train, y_train)
            self.status.emit("Logistic Regression addestrato.")
            xgb_model_default.fit(X_train, y_train)
            self.status.emit("XGBoost di default addestrato.")
            grid_search_cv.fit(X_train, y_train)
            self.status.emit("GridSearchCV per XGBoost con SMOTE completato.")

            best_xgb_smote_model = grid_search_cv.best_estimator_
            
            os.makedirs('modelli', exist_ok=True)
            joblib.dump(best_xgb_smote_model, DEFAULT_MODEL_FILE)
            joblib.dump(log_reg, 'modelli/logistic_regression_balanced.pkl')
            joblib.dump(xgb_model_default, 'modelli/xgb_clf_default_scaled.pkl')

            self.status.emit("Addestramento completato.")
            self.status.emit("Salvataggio modelli completato.")
            
            self.status.emit("\n--- Valutazione Modelli su Test Set ---")

            models_to_evaluate = {
                "Logistic Regression (balanced)": log_reg,
                "XGBoost (default with scale_pos_weight)": xgb_model_default,
                "Best XGBoost (GridSearchCV with SMOTE)": best_xgb_smote_model
            }

            y_true = y_test

            for model_name, model_instance in models_to_evaluate.items():
                y_pred = model_instance.predict(X_test)

                accuracy = accuracy_score(y_true, y_pred)
                precision = precision_score(y_true, y_pred, zero_division=0)
                recall = recall_score(y_true, y_pred, zero_division=0)
                f1 = f1_score(y_true, y_pred, zero_division=0)

                self.status.emit(f"\nMetriche per il modello: {model_name}")

                # elenco delle metriche
                for label, val in [
                    ("Accuracy",  accuracy),
                    ("Precision", precision),
                    ("Recall",    recall),
                    ("F1 Score",  f1)
                ]:
                    self.status.emit(f"{label}:\t{val:.4f}")


            self.status.emit("\nValutazione metriche completata.")

        except Exception as e:
            self.status.emit(f"Errore: {e}")
            import traceback
            self.status.emit(traceback.format_exc())
        finally:
            self.finished.emit()


class TrainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        form = QHBoxLayout()
        self.path_edit = QLineEdit()
        btn_browse = QPushButton("Sfoglia...")
        form.addWidget(QLabel("Percorso CSV:"))
        form.addWidget(self.path_edit)
        form.addWidget(btn_browse)
        layout.addLayout(form)

        self.start_btn = QPushButton("Avvia Addestramento")
        layout.addWidget(self.start_btn)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        btn_browse.clicked.connect(self.browse)
        self.start_btn.clicked.connect(self.start)

    def browse(self):
        fp, _ = QFileDialog.getOpenFileName(self, "Seleziona CSV", ".", "CSV files (*.csv)")
        if fp:
            self.path_edit.setText(fp)

    def start(self):
        path = self.path_edit.text().strip()
        if not os.path.exists(path):
            QMessageBox.warning(self, "Errore", "File non esistente")
            return

        self.log.clear()
        self.start_btn.setEnabled(False)

        self.worker = Worker(path)
        self.thread = threading.Thread(target=self.worker.run) # Salva riferimento al thread
        self.worker.status.connect(self.log.append)
        self.worker.finished.connect(lambda: self.start_btn.setEnabled(True))
        self.worker.finished.connect(self.training_done_message) # Messaggio opzionale
        self.thread.start()

    def training_done_message(self):
        # Controlla se l'ultimo messaggio nel log indica un errore grave
        log_content = self.log.toPlainText()
        if "Errore:" not in log_content.splitlines()[-5:]: # Controlla le ultime righe per errori
             QMessageBox.information(self, "Completato", "Addestramento e valutazione modelli terminati.")


class GraphsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        top = QHBoxLayout()
        self.lbl_datafile = QLabel(f"Dati: {os.path.basename(CLEANED_CSV) if os.path.exists(CLEANED_CSV) else 'N/A'}")
        btn_load_csv = QPushButton("Carica Dati…")
        top.addWidget(self.lbl_datafile)
        top.addStretch()
        top.addWidget(btn_load_csv)
        layout.addLayout(top)

        body = QHBoxLayout()
        self.btn_layout = QVBoxLayout()
        self.canvas_holder = QVBoxLayout()
        body.addLayout(self.btn_layout)
        body.addLayout(self.canvas_holder, 1) # Canvas holder prende più spazio
        layout.addLayout(body)

        self.data_file = CLEANED_CSV
        btn_load_csv.clicked.connect(self.browse_csv)

        self.graph_funcs = {
            "Distribuzione Genere": graphicGui.plot_gender_distribution,
            "Studente vs Professionista": graphicGui.plot_status_distribution,
            "Condizione di Depressione": graphicGui.plot_depression_distribution,
            "Depressione per Genere": graphicGui.plot_depression_by_gender,
            "Stress Finanziario": graphicGui.plot_financial_stress_by_depression,
            "Età vs Depress.": graphicGui.plot_age_distribution_by_depression,
            "Correlaz. Pearson": graphicGui.plot_pearson_correlation,
            "Depress. per Laurea": graphicGui.plot_depression_by_Degree_Group_Encoded_group,
            "Soddisf. Studio": graphicGui.plot_depression_by_study_satisfaction,
            "Depress. per Status": graphicGui.plot_depression_by_status
        }

        for name in self.graph_funcs:
            btn = QPushButton(name)
            self.btn_layout.addWidget(btn)
            btn.clicked.connect(lambda _, n=name: self.show_graph(n)) # Corretto per usare n

    def browse_csv(self):
        fp, _ = QFileDialog.getOpenFileName(self, "Seleziona CSV pulito", ".", "CSV files (*.csv)")
        if fp:
            self.data_file = fp
            self.lbl_datafile.setText(f"Dati: {os.path.basename(fp)}")
            # Pulisci il grafico precedente quando si caricano nuovi dati
            self.clear_canvas()

    def clear_canvas(self):
        for i in reversed(range(self.canvas_holder.count())):
            w = self.canvas_holder.itemAt(i).widget()
            if w:
                w.setParent(None)
                w.deleteLater()


    def load_data(self):
        if not self.data_file or not os.path.exists(self.data_file):
            QMessageBox.warning(self, "Dati non trovati", f"Il file {self.data_file} non è stato trovato o non è specificato.")
            return None
        try:
            return pd.read_csv(self.data_file)
        except Exception as e:
            QMessageBox.critical(self, "Errore Lettura CSV", f"Impossibile leggere il file CSV: {e}")
            return None

    def show_graph(self, name):
        df = self.load_data()
        if df is None:
            return 

        if name not in self.graph_funcs:
            QMessageBox.warning(self, "Errore", f"Funzione Grafico '{name}' non trovata.")
            return

        try:
            fig = self.graph_funcs[name](df) 
            if fig is None: 
                QMessageBox.information(self, "Info Grafico", f"Impossibile generare il grafico '{name}'. Dati insufficienti o formato non corretto?")
                return

            self.clear_canvas() 

            canvas = FigureCanvas(fig)
            self.canvas_holder.addWidget(canvas)
        except Exception as e:
            QMessageBox.critical(self, "Errore Generazione Grafico", f"Errore nel generare '{name}': {e}")
            import traceback
            print(traceback.format_exc()) # Per debug in console


class PredictPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        hmod = QHBoxLayout()
        self.lbl_model = QLabel(f"Modello: {os.path.basename(DEFAULT_MODEL_FILE) if os.path.exists(DEFAULT_MODEL_FILE) else 'N/A'}")
        btn_load = QPushButton("Carica Modello…")
        hmod.addWidget(self.lbl_model)
        hmod.addStretch()
        hmod.addWidget(btn_load)
        layout.addLayout(hmod)

        self.model = None
        if os.path.exists(DEFAULT_MODEL_FILE):
            self.load_model(DEFAULT_MODEL_FILE)
        else:
             QMessageBox.warning(self, "Modello Default Mancante", f"Il file modello di default {DEFAULT_MODEL_FILE} non è stato trovato. Caricane uno manualmente.")

        btn_load.clicked.connect(self.browse_model)

        self.features = {
            'Name': {'type':'text'},
            'Gender': {'type':'categorical','options':['Male','Female']},
            'Age': {'type':'numeric','range':(18,60)},
            'City': {'type':'text'}, 
            'Working Professional or Student':{'type':'categorical', 'options': ['Student', 'Working Professional']},
            'Profession':{'type':'text'}, 
            'Academic Pressure':{'type':'numeric','range':(0,5)},
            'Work Pressure':{'type':'numeric','range':(0,5)},
            'CGPA':{'type':'numeric','range':(0.0,10.0)}, 
            'Study Satisfaction':{'type':'numeric','range':(0,5)},
            'Job Satisfaction':{'type':'numeric','range':(0,5)},
            'Sleep Duration':{'type':'numeric','range':(0.0,12.0)},
            'Dietary Habits':{'type':'categorical','options':['Unhealthy','Moderate','Healthy']},
            'Degree':{'type':'text'}, 
            'Have you ever had suicidal thoughts ?':{'type':'categorical','options':['No','Yes']}, 
            'Work/Study Hours':{'type':'numeric','range':(0.0,12.0)},
            'Financial Stress':{'type':'numeric','range':(0,5)},
            'Family History of Mental Illness':{'type':'categorical','options':['No','Yes']} 
        }
        form = QFormLayout()
        self.inputs = {}
        for col, defn in self.features.items():
            if defn['type']=='categorical':
                cb = QComboBox()
                cb.addItems(defn['options'])
                form.addRow(col, cb)
                self.inputs[col] = cb
            else:
                le = QLineEdit()
                label_text = f"{col}"
                if defn['type']=='numeric':
                    label_text += f" ({defn['range'][0]}-{defn['range'][1]})"
                form.addRow(label_text, le)
                self.inputs[col] = le
        layout.addLayout(form)

        self.btn_pred = QPushButton("Esegui Predizione")
        self.lbl_res  = QLabel("Inserisci i dati e premi Predizione")
        layout.addWidget(self.btn_pred)
        layout.addWidget(self.lbl_res)

        self.btn_pred.clicked.connect(self.perform_prediction)

    def browse_model(self):
        fp, _ = QFileDialog.getOpenFileName(self, "Seleziona modello .pkl", "modelli/", "Pickle files (*.pkl)")
        if fp:
            self.load_model(fp)


    def load_model(self, path):
        try:
            self.model = joblib.load(path)
            self.lbl_model.setText(f"Modello: {os.path.basename(path)}")
            QMessageBox.information(self, "Modello Caricato", f"Caricato: {os.path.basename(path)}")
        except Exception as e:
            QMessageBox.critical(self, "Errore Caricamento Modello", f"Impossibile caricare il modello: {e}")
            self.model = None # Assicura che il modello sia None in caso di errore
            self.lbl_model.setText("Modello: N/A")


    def perform_prediction(self):
        if self.model is None:
            QMessageBox.warning(self, "Nessun Modello", "Nessun modello caricato. Carica un modello prima di eseguire una predizione.")
            return

        data = {'id':[0]} 
        errors = []
        for col, defn in self.features.items():
            widget = self.inputs[col]
            raw_value = widget.currentText() if defn['type']=='categorical' else widget.text().strip()
            
            if defn['type']=='numeric':
                if not raw_value: 
                    data[col] = [np.nan] # Invia NaN se vuoto, preprocess_person_test dovrebbe gestirlo
                    continue
                try:
                    val = float(raw_value) if isinstance(defn['range'][0], float) else int(raw_value)
                    min_val, max_val = defn['range']
                    if not (min_val <= val <= max_val):
                        errors.append(f"'{col}' fuori range ({min_val}-{max_val}). Valore: {val}")
                    data[col] = [val]
                except ValueError:
                    errors.append(f"'{col}' non valido (valore numerico atteso). Ricevuto: '{raw_value}'")
                    data[col] = [np.nan] # Invia NaN se non valido
            else: # text o categorical
                if not raw_value and col in ['Gender', 'Working Professional or Student', 'Dietary Habits', 'Have you ever had suicidal thoughts ?', 'Family History of Mental Illness']: # Campi categorici obbligatori
                     data[col] = [None] # Invia None se vuoto, preprocess_person_test dovrebbe gestirlo
                else:
                    data[col] = [raw_value]
        
        if errors:
            QMessageBox.warning(self, "Errori di input", "\n".join(errors))
            return

        df_input = pd.DataFrame(data)
        
        try:
            # preprocess_person_test dovrebbe restituire un DataFrame con le feature pronte per il modello
            df_clean = preprocess_person_test(df_input.copy()) 
            
            y_pred_proba = self.model.predict_proba(df_clean)
            prediction = y_pred_proba[:, 1][0] # Probabilità della classe positiva (Depressione = SI)
            
            threshold = 0.5 # Soglia standard
            depressione_status = "SI" if prediction >= threshold else "NO"
            
            text = f"Predizione Depressione: {depressione_status} (Probabilità: {prediction:.2%})"
            self.lbl_res.setText(text)

        except Exception as e:
            QMessageBox.critical(self, "Errore Predizione", f"Si è verificato un errore: {str(e)}")
            import traceback
            self.lbl_res.setText(f"Errore Predizione: {str(e)}")
            print(traceback.format_exc())


class DepressionAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analisi e Predizione Depressione")
        self.resize(900, 700)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        nav_bar = QWidget()
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(5, 5, 5, 5)
        self.btn_train  = QPushButton("Addestra Modelli")
        self.btn_graphs = QPushButton("Visualizza Grafici")
        self.btn_predict= QPushButton("Predizione Singola")
        nav_layout.addWidget(self.btn_train)
        nav_layout.addWidget(self.btn_graphs)
        nav_layout.addWidget(self.btn_predict)
        nav_layout.addStretch()
        main_layout.addWidget(nav_bar)

        self.stack = QStackedWidget()
        self.train_page   = TrainPage(self)
        self.graphs_page  = GraphsPage(self)
        self.predict_page = PredictPage(self)
        self.stack.addWidget(self.train_page)
        self.stack.addWidget(self.graphs_page)
        self.stack.addWidget(self.predict_page)
        main_layout.addWidget(self.stack)

        self.btn_train.clicked.connect(lambda: self.stack.setCurrentWidget(self.train_page))
        self.btn_graphs.clicked.connect(lambda: self.stack.setCurrentWidget(self.graphs_page))
        self.btn_predict.clicked.connect(lambda: self.stack.setCurrentWidget(self.predict_page))

        # Inizializza le directory se non esistono
        os.makedirs('data', exist_ok=True)
        os.makedirs('modelli', exist_ok=True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DepressionAnalysisApp()
    window.show()
    sys.exit(app.exec_())