import pandas as pd
from preprocessing import preprocess_test
import joblib

def test():
    test = pd.read_csv(r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\09_05_CorsoPython_ML\test.csv')


    print("Dati caricati con successo!")
    df_clean, test_ids = preprocess_test(test)
    # --- Preparazione X_test e predizione ---
    X_test = df_clean  # già senza 'Depression'

    model = joblib.load('best_xgb_clf_smote.pkl')
    y_pred_class = model.predict(X_test)

    # --- Creazione della submission ---
    submission = pd.DataFrame({
        'id': test_ids,
        'Depression': y_pred_class
    })

    # --- Salvataggio su file ---
    submission.to_csv(r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\09_05_CorsoPython_ML\submission.csv')
    print("Submission salvata su 'Mentally/submission.csv'")

