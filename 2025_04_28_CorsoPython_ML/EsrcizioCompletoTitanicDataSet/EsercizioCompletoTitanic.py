import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler

# Caricamento e pulizia dei dati
file_path = r'C:\Users\Simxyz\Desktop\DataScienceCarreer\4.ItConsultingGiGroup\CorsoPythonwGithub\SimoneVerrengia_DepositoCorsoPython\28_04_CorsoPython_ML\EsrcizioCompletoTitanicDataSet\train.csv'
data = pd.read_csv(file_path)

df_cleaned = data.drop('Cabin', axis=1).drop_duplicates()
df_cleaned['Age'] = df_cleaned['Age'].fillna(df_cleaned['Age'].mean())

# Matrice di correlazione
correlation_matrix = df_cleaned.corr(numeric_only=True)
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Matrice di correlazione delle colonne numeriche')
plt.show()

# Feature engineering
df_cleaned['FamilySize'] = df_cleaned['SibSp'] + df_cleaned['Parch'] + 1

# Tasso di sopravvivenza per dimensione della famiglia
survival_rate_family = df_cleaned.groupby('FamilySize')['Survived'].mean()
plt.figure(figsize=(10, 8))
survival_rate_family.plot(kind='bar', color='skyblue')
plt.title("Media del tasso di sopravvivenza per 'FamilySize'")
plt.xlabel("Dimensione della famiglia")
plt.ylabel("Tasso di sopravvivenza media")
plt.grid(axis='y', linestyle='--')
plt.tight_layout()
plt.show()

# Codifica One-Hot
df_cleaned = pd.get_dummies(df_cleaned, columns=['Sex'], drop_first=True)
df_cleaned = pd.get_dummies(df_cleaned, columns=['Embarked'])

# Definizione feature e target
X = df_cleaned.drop(['Survived', 'Name', 'Ticket'], axis=1)
y = df_cleaned['Survived']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=73)

# Scaling
numerical_cols = ['Age', 'Fare', 'FamilySize', 'SibSp', 'Parch']
scaler = StandardScaler()
X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
X_test[numerical_cols] = scaler.transform(X_test[numerical_cols])

# Addestramento modello
param_grid = {
    'criterion': ['gini', 'entropy'],
    'max_depth': [None, 5, 10, 15]
}
grid_search = GridSearchCV(DecisionTreeClassifier(random_state=73),
                           param_grid=param_grid,
                           cv=5,
                           scoring='accuracy',
                           n_jobs=-1)
grid_search.fit(X_train, y_train)
best_decision_tree = grid_search.best_estimator_

# Valutazione
y_pred = best_decision_tree.predict(X_test)
print(f"\nAccuratezza: {accuracy_score(y_test, y_pred):.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues',
            xticklabels=['Non Sopravvissuto', 'Sopravvissuto'],
            yticklabels=['Non Sopravvissuto', 'Sopravvissuto'])
plt.xlabel('Previsione')
plt.ylabel('Valore Reale')
plt.title('Confusion Matrix')
plt.show()

# Predizione da input utente
def predict_survival(model, scaler, feature_columns):
    inputs = ['Pclass', 'Age', 'SibSp', 'Parch', 'Fare', 'Sex', 'Embarked']
    user_input = {}
    for col in inputs:
        while True:
            val = input(f"Inserisci il valore per '{col}': ")
            try:
                if col in ['Pclass', 'SibSp', 'Parch']:
                    user_input[col] = int(val)
                elif col in ['Age', 'Fare']:
                    user_input[col] = float(val)
                elif col == 'Sex':
                    if val.lower() in ['male', 'female']:
                        user_input[col] = val.lower()
                        break
                elif col == 'Embarked':
                    if val.upper() in ['C', 'Q', 'S', '']:
                        user_input[col] = val.upper() if val else None
                        break
                break
            except ValueError:
                print("Valore non valido.")

    user_df = pd.DataFrame([user_input])
    user_df['FamilySize'] = user_df['SibSp'] + user_df['Parch'] + 1
    user_df = pd.get_dummies(user_df, columns=['Sex'], drop_first=True)
    user_df = pd.get_dummies(user_df, columns=['Embarked'])

    for col in feature_columns:
        if col not in user_df.columns:
            user_df[col] = 0
    user_df = user_df[feature_columns]
    user_df[numerical_cols] = scaler.transform(user_df[numerical_cols])

    prediction = model.predict(user_df)
    print("\nRisultato: SOPRAVVISSUTO" if prediction[0] else "\nRisultato: NON SOPRAVVISSUTO")

if __name__ == "__main__":
    predict_survival(best_decision_tree, scaler, X_train.columns)
