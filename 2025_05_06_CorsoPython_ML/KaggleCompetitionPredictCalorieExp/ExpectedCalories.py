import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.linear_model import LinearRegression

# === Caricamento dati ===
train = pd.read_csv(r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\06_05_CorsoPython_ML\KaggleCompetitionPredictCalorieExp\train.csv')
test = pd.read_csv(r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\06_05_CorsoPython_ML\KaggleCompetitionPredictCalorieExp\test.csv')

train.drop(columns=['id'], inplace=True)
test_id = test['id']
test.drop(columns=['id'], inplace=True)

# === Feature engineering ===
train['BMI'] = train['Weight'] / (train['Height'] ** 2)
test['BMI'] = test['Weight'] / (test['Height'] ** 2)

train['HRxDur'] = train['Heart_Rate'] * train['Duration']
test['HRxDur'] = test['Heart_Rate'] * test['Duration']

train['Temp_Dev'] = train['Body_Temp'] - 36.5
test['Temp_Dev'] = test['Body_Temp'] - 36.5

train['Age_Group'] = pd.cut(train['Age'], bins=[0, 18, 40, 65, 100], labels=[0, 1, 2, 3]).astype(int)
test['Age_Group'] = pd.cut(test['Age'], bins=[0, 18, 40, 65, 100], labels=[0, 1, 2, 3]).astype(int)

# === Encoding ===
le = LabelEncoder()
train['Sex'] = le.fit_transform(train['Sex'])
test['Sex'] = le.transform(test['Sex'])

# === Outlier visualization ===
numeric_features = train.drop(columns='Calories').select_dtypes(include=np.number).columns

plt.figure(figsize=(15, 10))
for i, feature in enumerate(numeric_features, 1):
    plt.subplot(3, 4, i)
    sns.boxplot(y=train[feature])
    plt.title(f'Outlier: {feature}')
plt.tight_layout()
plt.show()

# === Rimozione outlier via residui modello lineare ===
X = train.drop(columns='Calories')
y = train['Calories']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model_lr = LinearRegression()
model_lr.fit(X_scaled, y)

res_lr = y - model_lr.predict(X_scaled)
df_res = pd.DataFrame({'residui': res_lr})

Q1, Q3 = df_res['residui'].quantile([0.25, 0.75])
IQR = Q3 - Q1
lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
filtro = df_res['residui'].between(lower, upper)

# === Filtro dati ===
X_filtered = X[filtro]
y_filtered = y[filtro]

# === Split ===
X_train, X_test, y_train, y_test = train_test_split(X_filtered, y_filtered, test_size=0.2, random_state=73)

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# === XGBoost base ===
xgb = XGBRegressor(objective='reg:squarederror', random_state=73)
xgb.fit(X_train_scaled, y_train)
y_pred_xgb = xgb.predict(X_test_scaled)

# === GridSearch con regolarizzazione
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5],
    'learning_rate': [0.01, 0.1],
    'reg_alpha': [0.1],
    'reg_lambda': [10],
}

grid = GridSearchCV(
    estimator=XGBRegressor(objective='reg:squarederror', random_state=73),
    param_grid=param_grid,
    scoring='r2',
    cv=5,
    n_jobs=-1
)

grid.fit(X_train_scaled, y_train, 
         eval_set=[(X_test_scaled, y_test)],
         verbose=False)

best_xgb = grid.best_estimator_
y_pred_xgb_best = best_xgb.predict(X_test_scaled)

# === Valutazione ===
metrics = pd.DataFrame({
    'Model': ['XGBoost_Base', 'XGBoost_CV'],
    'R2': [r2_score(y_test, y_pred_xgb), r2_score(y_test, y_pred_xgb_best)],
    'RMSE': [
        np.sqrt(mean_squared_error(y_test, y_pred_xgb)),
        np.sqrt(mean_squared_error(y_test, y_pred_xgb_best))
    ]
})

print(metrics)
print("\nTrain R2 (best model):", r2_score(y_train, best_xgb.predict(X_train_scaled)))
print("Test R2 (best model):", r2_score(y_test, y_pred_xgb_best))

# === Preprocessing del test di Kaggle ===
test_scaled = scaler.transform(test)

# === Predizioni finali, forzando valori negativi a 0 (per MSLE) ===
final_predictions = best_xgb.predict(test_scaled)
final_predictions = np.maximum(final_predictions, 0)

# === Creazione file di submission ===
submission_df = pd.DataFrame({'id': test_id, 'Calories': final_predictions})
submission_df.to_csv('submission.csv', index=False)

print("\nFile di submission 'submission.csv' creato con le predizioni finali.")

