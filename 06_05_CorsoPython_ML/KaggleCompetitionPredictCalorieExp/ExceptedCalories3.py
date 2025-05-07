import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler, PowerTransformer
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score, mean_squared_error

# 1. Caricamento dati
train = pd.read_csv(r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\06_05_CorsoPython_ML\KaggleCompetitionPredictCalorieExp\train.csv')
test = pd.read_csv(r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\06_05_CorsoPython_ML\KaggleCompetitionPredictCalorieExp\test.csv')

# Preserva id
train_ids = train['id']
test_ids = test['id']

# Rimuovi id per feature engineering
train = train.drop(columns=['id'])
test = test.drop(columns=['id'])

# 2. Feature engineering
for df in [train, test]:
    df['BMI'] = df['Weight'] / (df['Height'] ** 2)
    df['Age_Group'] = pd.cut(df['Age'], bins=[0, 18, 40, 65, 100], labels=[0,1,2,3]).astype(int)

# 3. Gestione outlier (train)
# usa z-score per le variabili numeriche
num_cols = ['Age', 'Height', 'Weight', 'BMI']
z_scores = np.abs(stats.zscore(train[num_cols]))
outlier_mask = (z_scores < 3).all(axis=1)
train = train[outlier_mask]
train_ids = train_ids[outlier_mask]

# 4. Encoding categorico
le = LabelEncoder()
train['Sex'] = le.fit_transform(train['Sex'])
test['Sex'] = le.transform(test['Sex'])

# 5. Separazione X/y e trasformazione logaritmica del target
X = train.drop(columns=['Calories'])
y = np.log1p(train['Calories'])  # log transform

# 6. Feature selection con p-value
# aggiungi costante
oX = sm.add_constant(X)
model_sm = sm.OLS(y, oX).fit()
# seleziona feature con p-value < 0.05
signif_features = model_sm.pvalues[model_sm.pvalues < 0.05].index.drop('const').tolist()
X = X[signif_features]

# 7. Split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# 8. Scaling + PowerTransformer
scaler = StandardScaler()
pt = PowerTransformer(method='yeo-johnson')

X_train_scaled = pt.fit_transform(scaler.fit_transform(X_train))
X_val_scaled = pt.transform(scaler.transform(X_val))

# 9. Modelli e grid search
models = {
    'xgb': XGBRegressor(objective='reg:squarederror', random_state=42),
    'rf': RandomForestRegressor(random_state=42)
}
params = {
    'xgb': {'n_estimators': [100, 200], 'max_depth': [3,5], 'learning_rate': [0.01, 0.1]},
    'rf': {'n_estimators': [100,200], 'max_depth': [None,10,20]}
}
best_models = {}
for name in models:
    grid = GridSearchCV(models[name], params[name], cv=5, scoring='r2', n_jobs=-1)
    grid.fit(X_train_scaled, y_train)
    best_models[name] = grid.best_estimator_
    print(f"Best {name}: {grid.best_params_}")

# 10. Valutazione locale
y_val_pred_xgb = best_models['xgb'].predict(X_val_scaled)
y_val_pred_rf = best_models['rf'].predict(X_val_scaled)

for name, y_pred in zip(['XGB', 'RF'], [y_val_pred_xgb, y_val_pred_rf]):
    r2 = r2_score(y_val, y_pred)
    rmse = np.sqrt(mean_squared_error(y_val, y_pred))
    print(f"{name} R2: {r2:.4f}, RMSE: {rmse:.4f}")

# Scegli il migliore
best_name = max(['XGB','RF'], key=lambda n: r2_score(y_val, best_models[n.lower()].predict(X_val_scaled)))
final_model = best_models[best_name.lower()]
print(f"Selected final model: {best_name}")

# 11. Retrain su tutto il train set
X_full = train[signif_features]
y_full = np.log1p(train['Calories'])
X_full_scaled = pt.fit_transform(scaler.fit_transform(X_full))
final_model.fit(X_full_scaled, y_full)

# 12. Prepare test set
X_test = test[signif_features]
X_test_scaled = pt.transform(scaler.transform(X_test))

test_preds_log = final_model.predict(X_test_scaled)
test_preds = np.expm1(test_preds_log)  # invert log

# 13. Submission
submission = pd.DataFrame({'id': test_ids, 'Calories': test_preds})
submission.to_csv('submission.csv', index=False)
print("Submission file saved.")