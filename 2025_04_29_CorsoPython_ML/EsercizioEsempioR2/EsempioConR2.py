from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, r2_score, mean_squared_error, mean_absolute_error
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

file_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\29_04_CorsoPython_ML\train.csv'
data = pd.read_csv(file_path)

print("Dati Originali:")
print(data.head())
print(data.describe())
print(data.info())

df = data.copy()
df_cleaned = df.drop('Cabin', axis=1)
df_cleaned.drop_duplicates(inplace=True)

print("\nDataFrame dopo rimozione di 'Cabin' e duplicati:")
print(df_cleaned.head())
print(df_cleaned.describe())
print(df_cleaned.info())

media_eta = df_cleaned['Age'].mean()
df_cleaned['Age'] = df_cleaned['Age'].fillna(media_eta)
moda_embarked = df_cleaned['Embarked'].mode()[0]
df_cleaned['Embarked'] = df_cleaned['Embarked'].fillna(moda_embarked)

print("\nPulizia (gestione valori mancanti):")
print(df_cleaned.head())
print(df_cleaned.describe())
print(df_cleaned.info())

correlation_matrix = df_cleaned.corr(numeric_only=True)

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Matrice di correlazione delle colonne numeriche')
plt.show()

# Creazione della nuova feature 'FamilySize'
df_cleaned['FamilySize'] = df_cleaned['SibSp'] + df_cleaned['Parch'] + 1

# Visualizzazione dei boxplot per tutte le feature
df_cleaned.plot(kind='box', subplots=True, layout=(3, 3), figsize=(15, 15))
plt.suptitle('Boxplot di tutte le feature', y=1.02)
plt.tight_layout()
plt.show()

# Identificazione e rimozione degli outlier tramite IQR per la colonna 'Fare'
Q1_fare = df_cleaned['Fare'].quantile(0.25)
Q3_fare = df_cleaned['Fare'].quantile(0.75)
IQR_fare = Q3_fare - Q1_fare
threshold_lower_fare = Q1_fare - 1.5 * IQR_fare
threshold_upper_fare = Q3_fare + 1.5 * IQR_fare

df_no_outliers = df_cleaned[(df_cleaned['Fare'] >= threshold_lower_fare) & (df_cleaned['Fare'] <= threshold_upper_fare)].copy()

print(f"\nDataFrame dopo la rimozione degli outlier (IQR per 'Fare'): Dimensione originale: {len(df_cleaned)}, Dimensione dopo rimozione: {len(df_no_outliers)}")

# Creazione della nuova feature 'FamilySize'
df_no_outliers['FamilySize'] = df_no_outliers['SibSp'] + df_no_outliers['Parch'] + 1

# Codifica One-Hot delle variabili categoriche
df_encoded = pd.get_dummies(df_no_outliers, columns=['Sex', 'Embarked', 'Pclass'], drop_first=True)

# Definisci le feature (X) e la variabile target (y) utilizzando il DataFrame senza outlier e codificato
X = df_encoded.drop(['Survived', 'Name', 'Ticket'], axis=1)
y = df_encoded['Survived']

# Divisione dei dati in training e test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=73)

# Scalatura delle feature numeriche
scaler = StandardScaler()
numerical_features = ['Age', 'Fare', 'FamilySize', 'SibSp', 'Parch']
X_train[numerical_features] = scaler.fit_transform(X_train[numerical_features])
X_test[numerical_features] = scaler.transform(X_test[numerical_features])

# Addestramento del modello di Regressione Logistica
logistic_regression_model = LogisticRegression(random_state=73, max_iter=1000)
logistic_regression_model.fit(X_train, y_train)

# Predizioni sul set di test
y_pred_lr = logistic_regression_model.predict(X_test)

# Valutazione del modello di Regressione Logistica
accuracy_lr = accuracy_score(y_test, y_pred_lr)
report_lr = classification_report(y_test, y_pred_lr)
cm_lr = confusion_matrix(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr) # Calcolo dell'R-squared

print("\nRisultati della Regressione Logistica:")
print(f"Accuratezza: {accuracy_lr:.2f}")
print(f"R-squared: {r2_lr:.2f}") # Stampa dell'R-squared
print("\nClassification Report:")
print(report_lr)
plt.figure(figsize=(8, 6))
sns.heatmap(cm_lr, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Non Sopravvissuto', 'Sopravvissuto'],
            yticklabels=['Non Sopravvissuto', 'Sopravvissuto'])
plt.xlabel('Previsione')
plt.ylabel('Valore Reale')
plt.title('Confusion Matrix - Regressione Logistica')
plt.show()


