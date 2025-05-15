from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import numpy as np


# === Caricamento dati ===
# NOTE: Ensure these file paths are correct for your system.
# I cannot correct the paths themselves as they are specific to your local machine.
data = pd.read_csv(r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\06_05_CorsoPython_ML\KaggleCompetitionPredictCalorieExp\train.csv')
test = pd.read_csv(r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\06_05_CorsoPython_ML\KaggleCompetitionPredictCalorieExp\test.csv')

# Drop id columns
data.drop(columns=['id'], inplace=True)
test_id = test['id']
test.drop(columns=['id'], inplace=True)


# === Feature engineering (Applicare sia a train che test) ===
data['BMI'] = data['Weight'] / (data['Height'] ** 2)
data['Age_Group'] = pd.cut(data['Age'], bins=[0, 18, 40, 65, 100], labels=[0, 1, 2, 3], right=True, include_lowest=True).astype(int) # Added include_lowest and right for clarity on bin edges

test['BMI'] = test['Weight'] / (test['Height'] ** 2)
# Apply the same bins and labels to test data
test['Age_Group'] = pd.cut(test['Age'], bins=[0, 18, 40, 65, 100], labels=[0, 1, 2, 3], right=True, include_lowest=True).astype(int)


# === Encoding (Applicare sia a train che test usando lo stesso encoder) ===
le = LabelEncoder()
data['Sex'] = le.fit_transform(data['Sex'])
# Use the *same* fitted encoder to transform the test data
test['Sex'] = le.transform(test['Sex'])


# === Split train data ===
X = data.drop(columns='Calories')
y = data['Calories']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=73)

# === Scaling (Fit only on train, transform train, test, and Kaggle test) ===
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# === XGBoost con fortissima regolarizzazione (underfitting) ===
xgb = XGBRegressor(
    objective='reg:squarederror',
    n_estimators=50,
    max_depth=2,
    learning_rate=0.01,
    reg_alpha=10,
    reg_lambda=100,
    random_state=73
)

xgb.fit(X_train_scaled, y_train)

# Evaluate on the held-out test set from the training data
y_pred = xgb.predict(X_test_scaled)

print("Evaluation on internal test set:")
print("R2 Score:", r2_score(y_test, y_pred))
print("RMSE:", np.sqrt(mean_squared_error(y_test, y_pred)))


# === Preprocessing del test di Kaggle (Dopo aver applicato feature engineering ed encoding) ===
# Ensure columns in test match the order of columns in X_train before scaling
test_processed = test[X_train.columns] # Select columns in the same order as X_train
test_scaled = scaler.transform(test_processed) # Now scale the correctly preprocessed test data

# === Predizioni finali, forzando valori negativi a 0 (per MSLE) ===
final_predictions = xgb.predict(test_scaled)
final_predictions = np.maximum(final_predictions, 0) # Ensure predictions are non-negative


# === Creazione file di submission ===
submission_df = pd.DataFrame({'id': test_id, 'Calories': final_predictions})
submission_df.to_csv('submission.csv', index=False)

print("\nFile di submission 'submission.csv' creato con le predizioni finali.")