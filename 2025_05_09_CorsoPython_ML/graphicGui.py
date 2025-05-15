import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Esempio di alcune funzioni (devi implementare le altre)
# Assicurati che ogni funzione restituisca un oggetto Figure

def plot_gender_distribution(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=df, x='Gender', ax=ax, palette='viridis')
    ax.set_title('Distribuzione Genere')
    ax.set_xlabel('Genere')
    ax.set_ylabel('Conteggio')
    plt.close(fig) # Chiudi la figura subito dopo averla creata per non mostrarla qui
    return fig

def plot_status_distribution(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df, x='Working Professional or Student', ax=ax, palette='viridis')
    ax.set_title('Distribuzione Studente vs Professionista')
    ax.set_xlabel('Status')
    ax.set_ylabel('Conteggio')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.close(fig)
    return fig

def plot_suicidal_thoughts_distribution(counts):
     # Questa funzione prende già un Series di value_counts
    fig, ax = plt.subplots(figsize=(6, 4))
    counts.plot(kind='bar', ax=ax, color=['skyblue', 'salmon'])
    ax.set_title('Distribuzione Pensieri Suicidi Precedenti')
    ax.set_xlabel('Ha avuto pensieri suicidi?')
    ax.set_ylabel('Conteggio')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.close(fig)
    return fig

def plot_depression_distribution(df):
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=df, x='Depression', ax=ax, palette='coolwarm')
    ax.set_title('Distribuzione Condizione di Depressione')
    ax.set_xlabel('Depressione (0=No, 1=Sì)')
    ax.set_ylabel('Conteggio')
    plt.xticks([0, 1], ['No', 'Sì'])
    plt.close(fig)
    return fig

# Aggiungi qui tutte le altre funzioni di plottaggio richieste da GraphsFrame
# Esempio:
def plot_depression_by_gender(df):
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.countplot(data=df, x='Gender', hue='Depression', ax=ax, palette='coolwarm')
    ax.set_title('Depressione per Genere')
    ax.set_xlabel('Genere')
    ax.set_ylabel('Conteggio')
    plt.legend(title='Depressione', labels=['No', 'Sì'])
    plt.close(fig)
    return fig

# ... implementa le altre funzioni (plot_suicidal_thoughts_by_depression, etc.)

def plot_suicidal_thoughts_by_depression(df):
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.countplot(data=df, x='Have you ever had suicidal thoughts ?', hue='Depression', ax=ax, palette='coolwarm')
    ax.set_title('Pensieri Suicidi vs Depressione')
    ax.set_xlabel('Pensieri Suicidi Precedenti')
    ax.set_ylabel('Conteggio')
    plt.legend(title='Depressione', labels=['No', 'Sì'])
    plt.close(fig)
    return fig

def plot_depression_by_region(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    # Potrebbe esserci molte città, potresti voler raggruppare o mostrare solo le top N
    city_counts = df.groupby('City')['Depression'].value_counts(normalize=True).unstack().fillna(0)
    # Ordina per incidenza di depressione nel 1 (True)
    city_counts = city_counts.sort_values(by=1, ascending=False)
    # Mostra solo le prime 10 o 15 città per non affollare il grafico
    top_cities = city_counts.head(15)

    top_cities.plot(kind='bar', stacked=True, ax=ax, colormap='coolwarm')
    ax.set_title('Incidenza di Depressione per Città (Top 15)')
    ax.set_xlabel('Città')
    ax.set_ylabel('Proporzione')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Depressione', labels=['No', 'Sì'])
    plt.tight_layout()
    plt.close(fig)
    return fig

def plot_financial_stress_by_depression(df):
     fig, ax = plt.subplots(figsize=(8, 5))
     sns.boxplot(data=df, x='Depression', y='Financial Stress', ax=ax, palette='viridis')
     ax.set_title('Stress Finanziario vs Depressione')
     ax.set_xlabel('Depressione (0=No, 1=Sì)')
     ax.set_ylabel('Stress Finanziario')
     plt.xticks([0, 1], ['No', 'Sì'])
     plt.close(fig)
     return fig

def plot_age_distribution_by_depression(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data=df, x='Age', hue='Depression', kde=True, ax=ax, palette='coolwarm')
    ax.set_title('Distribuzione Età per Condizione di Depressione')
    ax.set_xlabel('Età')
    ax.set_ylabel('Frequenza')
    plt.legend(title='Depressione', labels=['No', 'Sì'])
    plt.close(fig)
    return fig


def plot_pearson_correlation(df):
    fig, ax = plt.subplots(figsize=(10, 8))
    # Seleziona solo le colonne numeriche per la correlazione
    numeric_df = df.select_dtypes(include=np.number)
    # Rimuovi l'ID se presente e target per la matrice completa se vuoi
    # Oppure calcola la correlazione con il target separatamente
    # Per la matrice completa:
    corr_matrix = numeric_df.corr()
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
    ax.set_title('Matrice di Correlazione Pearson (Variabili Numeriche)')
    plt.tight_layout()
    plt.close(fig)
    return fig

def plot_depression_by_degree_group(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    # Questa funzione potrebbe richiedere una categorizzazione o pulizia della colonna 'Degree'
    # Esempio semplificato: mostra per i valori più comuni o dopo raggruppamento
    degree_counts = df['Degree'].value_counts()
    top_degrees = degree_counts[degree_counts > 10].index # Mostra solo degree con più di 10 occorrenze
    df_filtered = df[df['Degree'].isin(top_degrees)]

    sns.countplot(data=df_filtered, x='Degree', hue='Depression', ax=ax, palette='coolwarm')
    ax.set_title('Depressione per Gruppo Laurea (più comuni)')
    ax.set_xlabel('Laurea')
    ax.set_ylabel('Conteggio')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Depressione', labels=['No', 'Sì'])
    plt.tight_layout()
    plt.close(fig)
    return fig

def plot_depression_by_study_satisfaction(df):
     fig, ax = plt.subplots(figsize=(7, 5))
     sns.boxplot(data=df, x='Depression', y='Study Satisfaction', ax=ax, palette='viridis')
     ax.set_title('Soddisfazione Studio vs Depressione')
     ax.set_xlabel('Depressione (0=No, 1=Sì)')
     ax.set_ylabel('Soddisfazione Studio')
     plt.xticks([0, 1], ['No', 'Sì'])
     plt.close(fig)
     return fig

def plot_depression_by_status(df):
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.countplot(data=df, x='Working Professional or Student', hue='Depression', ax=ax, palette='coolwarm')
    ax.set_title('Depressione per Status (Studente/Professionista)')
    ax.set_xlabel('Status')
    ax.set_ylabel('Conteggio')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Depressione', labels=['No', 'Sì'])
    plt.tight_layout()
    plt.close(fig)
    return fig