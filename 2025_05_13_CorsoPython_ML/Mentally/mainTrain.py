# Importiamo le librerie necessarie
import joblib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.model_selection import GridSearchCV, train_test_split
from preprocessing import preprocess_train, elimina_variabili_vif_pvalue
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Funzione per visualizzare più matrici di confusione in un unico grafico
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
    plt.show()
    
# Per un confronto ancora più approfondito, possiamo anche aggiungere una visualizzazione 
# delle metriche principali in un unico grafico a barre
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
    plt.show()
    
    return metrics_df
def train():
    # Caricamento dei dati nella variabile train
    train = pd.read_csv('Mentally/train.csv')
    df_clean = preprocess_train(train)

    # Selezione delle Feature e del Target
    X = df_clean.drop(columns=['Depression'])
    y = df_clean['Depression']
    X_selected = elimina_variabili_vif_pvalue(X, y)
    # Analizziamo la distribuzione delle classi
    print("\nDistribuzione delle classi nel target:")
    print(y.value_counts(normalize=True))

    # Calcoliamo il rapporto per scale_pos_weight in XGBoost
    negative_count, positive_count = np.bincount(y)
    scale_pos_weight = negative_count / positive_count
    print(f"\nRapporto delle classi (negativo/positivo): {scale_pos_weight:.2f}")

    # Separazione train/test mantenendo la distribuzione delle classi
    X_train, X_test, y_train, y_test = train_test_split(
        X_selected, y, 
        test_size=0.2, 
        random_state=73,
        stratify=y  # Mantiene la distribuzione originale
    )

    # 1. Logistic Regression con class weights
    log_reg = LogisticRegression(
        random_state=73, 
        max_iter=1000,
        class_weight='balanced'  # Bilanciamento classi
    )

    # 2. XGBoost con pesi per la classe positiva
    xgb_clf = XGBClassifier(
        objective='binary:logistic', 
        random_state=73,
        scale_pos_weight=scale_pos_weight  # Bilanciamento classi
    )

    # 3. Pipeline con SMOTE e XGBoost
    smote = SMOTE(random_state=73, sampling_strategy='auto')
    xgb_smote = ImbPipeline([
        ('smote', smote),
        ('xgb', XGBClassifier(objective='binary:logistic', random_state=73))
    ])

    # Parametri per la GridSearch con SMOTE
    param_grid = {
        'xgb__n_estimators': [50, 100],
        'xgb__max_depth': [3, 5],
        'xgb__learning_rate': [0.01, 0.1],
        'xgb__scale_pos_weight': [1, scale_pos_weight]  # Testa con e senza pesi
    }

    grid_clf = GridSearchCV(
        xgb_smote,
        param_grid, 
        scoring='f1', 
        cv=5, 
        n_jobs=-1
    )

    # Addestramento modelli
    print("\nAddestramento modelli...")
    log_reg.fit(X_train, y_train)
    xgb_clf.fit(X_train, y_train)
    grid_clf.fit(X_train, y_train)

    # Miglior modello con SMOTE
    best_xgb_clf = grid_clf.best_estimator_

    # Predizioni
    y_pred_log = log_reg.predict(X_test)
    y_pred_xgb = xgb_clf.predict(X_test)
    y_pred_xgb_best = best_xgb_clf.predict(X_test)

    # Salvataggio modelli
    joblib.dump(best_xgb_clf, 'best_xgb_clf_smote.pkl')
    print("Modello XGB ottimizzato (SMOTE) salvato in 'best_xgb_clf_smote.pkl'")

    joblib.dump(log_reg, 'logistic_regression_smote.pkl')
    joblib.dump(xgb_clf, 'xgb_clf_default_smote.pkl')
    print("Modelli log_reg e xgb_clf default salvati in 'logistic_regression_smote.pkl' e 'xgb_clf_default_smote.pkl'")

    # Visualizzazione e confronto
    plot_combined_confusion_matrices(
        y_test, 
        [y_pred_log, y_pred_xgb, y_pred_xgb_best], 
        ["Logistic Regression", "XGBoost", "XGBoost (Optimized)"]
    )

    metrics_df = plot_metrics_comparison(
        y_test, 
        [y_pred_log, y_pred_xgb, y_pred_xgb_best], 
        ["Logistic Regression", "XGBoost", "XGBoost (Optimized)"]
    )

    # Distribuzione delle classi
    print("\nDistribuzione delle classi nel target dopo lo SMOTE:")
    print(y.value_counts(normalize=True))

    print("\nConfronti metriche in formato tabella:")
    print(metrics_df.round(4))
