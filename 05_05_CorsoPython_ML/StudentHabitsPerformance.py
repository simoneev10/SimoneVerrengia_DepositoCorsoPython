import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
from xgboost import XGBRegressor, plot_importance
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from statsmodels.stats.outliers_influence import variance_inflation_factor

# 1. Caricamento e pulizia dati
file_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\05_05_CorsoPython_ML\student_habits_performance.csv'
df = pd.read_csv(file_path)

# Rimuovo ID e imputazione modalità per education
df.drop(columns=['student_id'], inplace=True)
df['parental_education_level'].fillna(df['parental_education_level'].mode()[0], inplace=True)

# Encoding categoriche ordinarie
diet_order = ['Poor', 'Fair', 'Good']
internet_order = ['Poor', 'Average', 'Good']
education_order = ['High School', 'Bachelor', 'Master', 'PhD']
ord_enc = OrdinalEncoder(categories=[diet_order, internet_order, education_order])
df[['diet_quality','internet_quality','parental_education_level']] = \
    ord_enc.fit_transform(df[['diet_quality','internet_quality','parental_education_level']])

# Label encoding per binary
le = LabelEncoder()
for col in ['gender','part_time_job','extracurricular_participation']:
    df[col] = le.fit_transform(df[col])

# Feature aggiuntiva: tempo di intrattenimento
if 'netflix_hours' in df.columns and 'social_media_hours' in df.columns:
    df['entertainment_time'] = df['netflix_hours'] + df['social_media_hours']

# 2. Visualizzazione iniziale
sns.set(style='whitegrid')
plt.figure(figsize=(10,4))
sns.histplot(df['exam_score'], bins=50, kde=True)
plt.title('Distribuzione dei punteggi d\'esame')
plt.xlabel('Exam Score')
plt.show()

# Matrice di correlazione
plt.figure(figsize=(8,6))
corr = df.corr(numeric_only=True)
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', square=True)
plt.title('Matrice di correlazione')
plt.xticks(rotation=45)
plt.show()

# 3. Rimozione multicollinearità (VIF + p-value)

def elimina_variabili_vif_pvalue(X, y, vif_threshold=5.0, pvalue_threshold=0.05):
    X_current = X.copy()
    while True:
        X_const = sm.add_constant(X_current)
        model = sm.OLS(y, X_const).fit()
        pvals = model.pvalues.drop('const')
        vif_data = pd.DataFrame({
            'Feature': X_current.columns,
            'VIF': [variance_inflation_factor(X_current.values, i) 
                    for i in range(X_current.shape[1])],
            'p-value': pvals.values
        })
        # Se nessuna variabile da rimuovere, esco
        cond = (vif_data['VIF'] > vif_threshold) & (vif_data['p-value'] > pvalue_threshold)
        if not cond.any():
            break
        # Rimuovo la variabile con VIF più alto
        to_remove = vif_data.loc[cond, 'Feature'].iloc[vif_data.loc[cond,'VIF'].argmax()]
        print(f"Rimuovo {to_remove} (VIF={vif_data.loc[vif_data.Feature==to_remove,'VIF'].values[0]:.2f}, "
              f"p-val={vif_data.loc[vif_data.Feature==to_remove,'p-value'].values[0]:.4f})")
        X_current.drop(columns=[to_remove], inplace=True)
    print("Feature finali:", X_current.columns.tolist())
    return X_current

# Separazione X/y e selezione
X = df.drop(columns=['exam_score'])
y = df['exam_score']
X_selected = elimina_variabili_vif_pvalue(X, y)

# Split e scaling
X_train, X_test, y_train, y_test = train_test_split(
    X_selected, y, test_size=0.2, random_state=73)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. Training e valutazione modelli
# Linear Regression
lr = LinearRegression().fit(X_train_scaled, y_train)
y_pred_lr = lr.predict(X_test_scaled)
# XGBoost base
xgb = XGBRegressor(objective='reg:squarederror', random_state=73).fit(X_train_scaled, y_train)
y_pred_xgb = xgb.predict(X_test_scaled)
# XGBoost ottimizzato (CV)
param_grid = { 'n_estimators': [50,100], 'max_depth': [3,5], 'learning_rate':[0.01,0.1] }
grid = GridSearchCV(XGBRegressor(objective='reg:squarederror', random_state=73),
                    param_grid, scoring='r2', cv=5, n_jobs=-1)
grid.fit(X_train_scaled, y_train)
best_xgb = grid.best_estimator_
y_pred_xgb_best = best_xgb.predict(X_test_scaled)

# R² e RMSE per tutti
metrics = pd.DataFrame({
    'Model': ['LinearReg','XGBoost_base','XGBoost_CV'],
    'R2': [r2_score(y_test,y_pred_lr), r2_score(y_test,y_pred_xgb), r2_score(y_test,y_pred_xgb_best)],
    'RMSE': [np.sqrt(mean_squared_error(y_test,y_pred_lr)),
             np.sqrt(mean_squared_error(y_test,y_pred_xgb)),
             np.sqrt(mean_squared_error(y_test,y_pred_xgb_best))]
})
print(metrics)

# 5. Grafico comparativo Predetti vs Reali

sns.set(style='ticks')
plt.figure(figsize=(12,12))
for i,(pred, name) in enumerate(zip(
        [y_pred_lr, y_pred_xgb, y_pred_xgb_best],
        ['LinearReg','XGBoost_base','XGBoost_CV']), 1):
    ax = plt.subplot(3,1,i)
    sns.scatterplot(x=y_test, y=pred, alpha=0.6)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    ax.set_xlabel('Valori Reali')
    ax.set_ylabel('Predetti')
    ax.set_title(f'{name}: Reali vs Predetti')
plt.tight_layout()
plt.show()

# 4. EXPLANATION: RESIDUI E BOXPLOT
# Definizione residuo: residuo = valore reale - valore predetto
# Un boxplot dei residui aiuta a visualizzare:
#   - la mediana (bias centrale)
#   - la dispersione (IQR)
#   - eventuali outlier (punti al di fuori di 1.5 * IQR)
# I residui dovrebbero essere simmetrici intorno a zero e senza outlier estremi.

# Calcolo residui per LinearReg
res_lr = y_test - y_pred_lr

plt.figure(figsize=(6,6))
sns.boxplot(y=res_lr)
plt.title('Boxplot dei Residui - Linear Regression')
plt.ylabel('Residui (Real - Predetto)')
plt.show()

# 5. RIMOZIONE OUTLIER BASATA SULL'IQR DEI RESIDUI

df_res = pd.DataFrame({'residui':res_lr})
Q1, Q3 = df_res['residui'].quantile([0.25,0.75])
IQR = Q3 - Q1
lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR
filtro = df_res['residui'].between(lower, upper)
print(f"Outlier rimossi: {len(df_res)-filtro.sum()}")
# Crea dati "puliti"
X_clean = X_test_scaled[filtro.values]
y_clean = y_test[filtro.values]
# Ricalcolo predizioni e metriche per Linear
y_pred_clean = lr.predict(X_clean)
r2_clean = r2_score(y_clean, y_pred_clean)
print(f"R2 before: {metrics.loc[0,'R2']:.3f} | R2 after: {r2_clean:.3f}")

# 6. GRAFICO COMPARATIVO LINEAR PRIMA/DOPO OUTLIER

plt.figure(figsize=(12,5))
# Prima rimozione
ax1 = plt.subplot(1,2,1)
sns.scatterplot(x=y_test, y=y_pred_lr, alpha=0.6)
ax1.plot([y_test.min(),y_test.max()],[y_test.min(),y_test.max()],'r--')
ax1.set_title('Linear: Reali vs Predetti (Originale)')
ax1.set_xlabel('Reali')
ax1.set_ylabel('Predetti')

# Dopo rimozione
ax2 = plt.subplot(1,2,2)
sns.scatterplot(x=y_clean, y=y_pred_clean, alpha=0.6)
ax2.plot([y_clean.min(),y_clean.max()],[y_clean.min(),y_clean.max()],'r--')
ax2.set_title('Linear: Reali vs Predetti (Pulito)')
ax2.set_xlabel('Reali')
ax2.set_ylabel('Predetti')
plt.tight_layout()
plt.show()
