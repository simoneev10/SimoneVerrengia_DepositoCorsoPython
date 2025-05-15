

# Mentally Stability Of The Person-Predication

## Introduzione

Questo progetto affronta il tema critico della salute mentale attraverso l'analisi di un dataset, con l'obiettivo di sviluppare un modello di Machine Learning capace di predire la probabilità di uno stato depressivo. Implementa una pipeline completa che include fasi di preprocessing avanzato, addestramento di diversi modelli di classificazione, valutazione delle performance e una semplice interfaccia a menu per l'interazione.

## Funzionalità Principali

Il progetto offre le seguenti funzionalità:

* **Preprocessing Dati Avanzato:**
    * Gestione sofisticata dei valori mancanti tramite tecniche di imputazione (mediana, moda) con logiche differenziate per sottogruppi specifici (Studenti vs Working Professionals).
    * Normalizzazione e standardizzazione di dati testuali e categorici non uniformi (es. durate del sonno, titoli di studio).
    * Codifica di variabili categoriche (binarie, ordinali, nominali) utilizzando mappature personalizzate, OrdinalEncoder e LabelEncoder.
    * Raggruppamento intelligente di categorie con alta cardinalità (es. Professioni, Città) in gruppi più gestibili (Professional Group, Region, Degree Group).
    * Selezione automatica delle feature basata su test statistici (VIF e p-value) per ridurre la multicollinearità e migliorare la stabilità del modello (applicata sul training set prima dello split).
* **Pipeline di Addestramento Modelli:**
    * Addestramento di modelli di classificazione robusti come Logistic Regression e XGBoost.
    * Strategie mirate per gestire il potenziale sbilanciamento delle classi nel dataset (stato depressivo presente vs assente), inclusi `class_weight`, `scale_pos_weight` e l'applicazione di SMOTE tramite `imblearn.pipeline`.
    * Ottimizzazione degli iperparametri del modello XGBoost utilizzando GridSearchCV con cross-validation (5 fold) focalizzata sull'ottimizzazione del F1-Score.
* **Valutazione e Confronto Performance:**
    * Calcolo e visualizzazione delle metriche di valutazione standard: Accuracy, Precision, Recall, e F1-Score.
    * Generazione e visualizzazione comparativa delle Matrici di Confusione per una comprensione approfondita delle performance dei modelli.
* **Predizione su Nuovi Dati:**
    * Applicazione del preprocessing identico a quello del training set per garantire coerenza.
    * Caricamento del modello addestrato ottimizzato (`best_xgb_clf_smote.pkl`).
    * Generazione di previsioni sul dataset di test e creazione di un file `submission.csv` nel formato standard ID/Predizione.
    * Possibilità di ottenere una predizione per un singolo individuo inserendo i dati manualmente (richiede script dedicato).
* **Interfaccia Utente Interattiva:**
    * Menu testuale semplice per lanciare le varie fasi della pipeline (Addestramento, Test, Predizione Singola).
    * Integrazione con uno script esterno per visualizzazioni aggiuntive (richiede script dedicato).

## Struttura del Progetto

La struttura delle cartelle e dei file è organizzata come segue:

```
.
├── Mentally/
│   ├── train.csv                       # Dataset di training originale (input)
│   ├── test.csv                        # Dataset di test originale (input)
│   ├── submission.csv                  # Output: File CSV con le previsioni sul test set
│   ├── cleaned_train.csv               # Output: Training set dopo preprocessing
│   ├── cleaned_test.csv                # Output: Test set dopo preprocessing
│   ├── person_test.csv                 # Output: File CSV temporaneo per input manuale singolo
│   ├── best_xgb_clf_smote.pkl          # Output: Modello XGBoost ottimizzato addestrato
│   ├── logistic_regression_smote.pkl   # Output: Modello Logistic Regression addestrato
│   └── xgb_clf_default_smote.pkl       # Output: Modello XGBoost di base addestrato
├── main.py                             # Script principale con menu
├── mainTrain.py                        # Modulo: Addestramento, valutazione, salvataggio
├── mainTest.py                         # Modulo: Predizione su test set e submission
├── preprocessing.py                    # Modulo: Funzioni centralizzate di pulizia e trasformazione dati
├── insertUtente.py                     # Modulo: Gestione input manuale utente (CODICE NON FORNITO)
└── grafici.py                          # Modulo: Funzioni per visualizzazioni aggiuntive (CODICE NON FORNITO)
```

## Requisiti di Sistema e Installazione

### Requisiti

Assicurati di avere **Python 3.6+** installato. Le librerie Python necessarie sono:

* `pandas`
* `numpy`
* `scikit-learn`
* `imbalanced-learn`
* `xgboost`
* `statsmodels`
* `seaborn`
* `matplotlib`
* `joblib`

Puoi installarle tutte tramite pip:

```bash
pip install pandas numpy scikit-learn imbalanced-learn xgboost statsmodels seaborn matplotlib joblib
```

Il modulo `re` è una libreria standard di Python e non richiede installazione aggiuntiva.

### Installazione

1.  Clona il repository:
    ```bash
    git clone <URL_DEL_TUO_REPOSITORY>
    cd <nome_cartella_progetto>
    ```
2.  Crea la cartella necessaria per i dati e gli output:
    ```bash
    mkdir Mentally
    ```
3.  Posiziona i file `train.csv` e `test.csv` (ottenuti dal dataset) all'interno della cartella `Mentally/`.

## Utilizzo del Programma

Per avviare l'applicazione interattiva, esegui lo script principale dal terminale nella directory radice del progetto:

```bash
python main.py
```

Ti verrà presentato un menu:

```
Benvenuto nel menu principale!
1. Analisi, preprocessing, addestramento e previsione su file CSV di training
2. Analisi, preprocessing, previsione su test e generazione submission
3. Predizione dello stato depressivo di una persona (inserimento manuale)
4. Visualizza grafici
5. Esci
```

Seleziona l'opzione desiderata digitando il numero corrispondente.

* **Opzione 1 (Addestramento):** Questa è la fase iniziale. Carica `train.csv`, pulisce i dati (`preprocessing.py`), seleziona le feature, addestra e ottimizza i modelli, valuta i risultati (con output a console e grafici delle matrici/metriche) e salva i modelli addestrati (`.pkl`) e il dataset pulito in `Mentally/`. **È indispensabile eseguire questa opzione almeno una volta prima di procedere con le opzioni 2 e 3, poiché queste ultime dipendono dai modelli salvati.**
* **Opzione 2 (Test e Submission):** Carica `test.csv`, applica le stesse trasformazioni del training, carica il miglior modello addestrato (`best_xgb_clf_smote.pkl`) ed effettua le predizioni per generare il file `Mentally/submission.csv`.
* **Opzione 3 (Predizione Singola):** Permette di inserire manualmente i dati di un individuo per ottenere una predizione in tempo reale. Richiama le logiche di preprocessing per un singolo record (`preprocess_person_test` in `preprocessing.py`) e utilizza il modello salvato. **Nota: Richiede la presenza del file `insertUtente.py`.**
* **Opzione 4 (Visualizzazioni):** Accede a un sottomenu o a funzionalità grafiche definite nello script `grafici.py`. **Nota: Richiede la presenza del file `grafici.py`.**
* **Opzione 5 (Esci):** Termina l'esecuzione del programma.

## Descrizione Dettagliata dei Moduli

### `main.py`

Agisce da orchestratore. Contiene la funzione `menu()` che gestisce il loop principale, presenta le opzioni all'utente, cattura l'input e invoca le funzioni appropriate dagli altri moduli (`mainTrain.py`, `mainTest.py`, `insertUtente.py`, `grafici.py`) basandosi sulla scelta effettuata.

### `mainTrain.py`

È il cuore del processo di addestramento. La funzione `train()` al suo interno si occupa di:
1.  Caricare i dati di training.
2.  Invocare `preprocess_train` per pulire e trasformare il DataFrame.
3.  Separare feature (`X`) e target (`y`).
4.  Applicare la selezione feature (`elimina_variabili_vif_pvalue`).
5.  Suddividere il dataset (già con feature selezionate) in set di addestramento e test *interni* (`X_train`, `X_test`, `y_train`, `y_test`) in modo stratificato.
6.  Inizializzare i vari modelli (Logistic Regression con bilanciamento, XGBoost con pesi di posizione).
7.  Costruire una pipeline `imblearn` che combina SMOTE con XGBoost.
8.  Definire e eseguire una ricerca a griglia (`GridSearchCV`) sulla pipeline SMOTE+XGBoost per trovare i migliori iperparametri, ottimizzando l'F1-Score.
9.  Addestrare tutti i modelli definiti (LogReg, XGBoost base, XGBoost ottimizzato dalla Grid Search) sui dati di addestramento interni (`X_train`, `y_train`).
10. Salvare i modelli addestrati (in formato `.pkl`) nella cartella `Mentally/`.
11. Generare predizioni sui dati di test interni (`X_test`) per valutare i modelli.
12. Chiamare le funzioni di visualizzazione (`plot_combined_confusion_matrices`, `plot_metrics_comparison`) per mostrare graficamente le performance dei modelli a confronto.

Le funzioni `plot_combined_confusion_matrices` e `plot_metrics_comparison` sono definite in questo modulo per facilitare la visualizzazione dei risultati della valutazione.

### `mainTest.py`

Contiene la funzione `test()` responsabile della fase di predizione finale sul test set originale:
1.  Carica il dataset `Mentally/test.csv`.
2.  Applica le trasformazioni chiamando la funzione `preprocess_test` da `preprocessing.py`. Questa funzione restituisce il DataFrame pulito e gli ID originali, garantendo che le predizioni possano essere associate correttamente.
3.  Carica il modello ottimizzato salvato durante l'addestramento (`best_xgb_clf_smote.pkl`).
4.  Utilizza il modello caricato per generare le predizioni sullo stato depressivo (`y_pred_class`) per ogni riga del test set pulito.
5.  Crea un DataFrame `submission` combinando gli ID originali e le predizioni.
6.  Salva il DataFrame `submission` in formato CSV (`Mentally/submission.csv`) senza l'indice.

### `preprocessing.py`

Questo modulo è fondamentale e centralizza tutta la logica di pulizia e trasformazione dei dati per garantire coerenza tra training, test e input manuale. Contiene le seguenti funzioni:

* `map_sleep_duration(duration_str)`: Una funzione ausiliaria che utilizza espressioni regolari per interpretare e convertire stringhe eterogenee che descrivono la durata del sonno in valori numerici (ore).
* `elimina_variabili_vif_pvalue(X, y, vif_threshold, pvalue_threshold)`: Implementa un algoritmo di selezione delle feature backward-stepwise. Itera rimuovendo le feature che contemporaneamente superano una soglia di VIF (indicando alta multicollinearità) e una soglia di p-value (indicando bassa significatività statistica in un modello lineare semplice), finché non vengono soddisfatte le condizioni.
* `preprocess_train(df)`: Implementa l'intera pipeline di preprocessing per il dataset di training. Include la gestione dei NaN con logiche basate sul ruolo (Student/Professional), imputazione con mediana/moda, codifica binaria (Genere, Stato Lavorativo/Studentesco, Suicidal Thoughts, Family History), applicazione di `map_sleep_duration`, pulizia e codifica ordinale del Grado di Istruzione (`Degree_Group_Encoded`), pulizia, validazione e codifica ordinale delle Abitudini Alimentari (`Dietary Habits`), raggruppamento e codifica nominale della Professione (`Professional_Group_Encoded`) e della Città/Regione (`Region_Encoded`). Infine, rimuove le colonne originali e quelle intermedie non più necessarie e salva il DataFrame pulito in `cleaned_train.csv`. **Nota:** Il codice rimuove la colonna `Have you ever had suicidal thoughts ?` (rinominata in `SuicidalThoughts`) alla fine del preprocessing.
* `preprocess_test(df)`: Implementa una pipeline di preprocessing identica a `preprocess_train` ma specifica per il dataset di test. È cruciale che le trasformazioni (mappature, imputazioni) siano basate *solo* sui dati del training set originale per evitare data leakage. Questa funzione restituisce il DataFrame pulito e gli ID originali del test set. Salva il DataFrame pulito in `cleaned_test.csv`.
* `preprocess_person_test(df)`: Una versione della pipeline di preprocessing ottimizzata per gestire un singolo record di input (presumibilmente da `insertUtente.py`). Applica le stesse trasformazioni di imputazione e codifica per rendere il formato del singolo record compatibile con quello dei dati su cui è stato addestrato il modello. Salva il record processato in `person_test.csv` (probabilmente temporaneo).

### `insertUtente.py` 

Basato sull'importazione nel `main.py`, questo script è atteso per contenere la funzione `insert_data()`. Il suo scopo è di:
1.  Interagire con l'utente tramite input da console (o altra GUI) per raccogliere i dati di una singola persona (età, genere, professione, ecc.).
2.  Organizzare questi dati in un formato compatibile con le funzioni di preprocessing (tipicamente un DataFrame pandas con una singola riga).
3.  Chiamare la funzione `preprocess_person_test` da `preprocessing.py` per pulire e trasformare l'input dell'utente.
4.  Caricare il modello addestrato (es. `best_xgb_clf_smote.pkl`).
5.  Effettuare una predizione sullo stato depressivo per l'input pre-processato.
6.  Comunicare la predizione risultante all'utente.

### `grafici.py` 

Basato sull'importazione nel `main.py`, questo script è atteso per contenere la funzione `menu_visualizzazioni()` e potenzialmente altre funzioni di supporto per la generazione di grafici. Il suo scopo è di fornire visualizzazioni aggiuntive rispetto a quelle incluse in `mainTrain.py`, che potrebbero includere:
1.  Visualizzazioni esplorative del dataset originale (distribuzioni di feature, relazioni tra variabili).
2.  Visualizzazioni relative ai risultati o alle performance del modello (oltre matrici di confusione e metriche riassuntive).
Utilizzerebbe tipicamente le librerie `matplotlib` e `seaborn`.

*Autore: Giacomo Visciotti-Simone Verrengia-Giuseppe Pio del Vecchio-Liliana Gilca*

