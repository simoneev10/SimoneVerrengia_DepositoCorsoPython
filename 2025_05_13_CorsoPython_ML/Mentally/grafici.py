import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Distribuzione della Frequenza del Genere
def plot_gender_distribution(train):
    gender_labels = {0: 'Femmina', 1: 'Maschio'}
    gender_counts = train['Gender'].value_counts()
    gender_counts_labeled = gender_counts.rename(index=gender_labels)

    plt.figure(figsize=(8, 6))
    ax = sns.barplot(x=gender_counts_labeled.index, y=gender_counts_labeled.values, palette='viridis')
    plt.title('Distribuzione della Frequenza del Genere', fontsize=16)
    plt.xlabel('Genere', fontsize=12)
    plt.ylabel('Frequenza (Numero di Individui)', fontsize=12)

    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f')

    plt.tight_layout()
    plt.show()

# Distribuzione della Frequenza: Studente vs Professionista
def plot_status_distribution(train):
    status_counts = train['Working Professional or Student'].value_counts()
    status_labels = {0: 'Studente', 1: 'Professionista'}
    status_counts_labeled = status_counts.rename(index=status_labels)

    plt.figure(figsize=(8, 6))
    ax = sns.barplot(x=status_counts_labeled.index, y=status_counts_labeled.values, palette='viridis')
    plt.title('Distribuzione della Frequenza: Studente vs Professionista', fontsize=16)
    plt.xlabel('Status', fontsize=12)
    plt.ylabel('Frequenza (Numero di Individui)', fontsize=12)

    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f')

    plt.tight_layout()
    plt.show()

# Frequenza della Depressione per Status 
def plot_depression_by_status(train):
    # Mappiamo le etichette per chiarezza
    status_labels = {0: 'Studente', 1: 'Professionista'}
    depression_labels = {0: 'No Depressione', 1: 'Sì Depressione'}

    # Creiamo una tabella di contingenza
    grouped = train.groupby(['Working Professional or Student', 'Depression']).size().unstack()

    # Rinominiamo righe e colonne
    grouped.index = grouped.index.map(status_labels)
    grouped.columns = [depression_labels[col] for col in grouped.columns]

    # Plot a barre
    ax = grouped.plot(kind='bar', figsize=(8, 6), color=['#1f77b4', '#2ca02c'])
    plt.title('Frequenza della Depressione per Status (Studente vs Professionista)', fontsize=16)
    plt.xlabel('Status', fontsize=12)
    plt.ylabel('Numero di Individui', fontsize=12)
    plt.xticks(rotation=0)

    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f')

    plt.legend(title='Condizione di Depressione')
    plt.tight_layout()
    plt.show()

# Frequenza di Risposte su Pensieri Suicidi Precedenti
def plot_suicidal_thoughts_distribution(suicidal_thoughts_counts):
    suicidal_thoughts_labels = {0: 'No', 1: 'Sì'}
    suicidal_thoughts_counts_labeled = suicidal_thoughts_counts.rename(index=suicidal_thoughts_labels)

    plt.figure(figsize=(8, 6))
    ax = sns.barplot(x=suicidal_thoughts_counts_labeled.index, y=suicidal_thoughts_counts_labeled.values, palette='viridis')
    plt.title('Frequenza di Risposte su Pensieri Suicidi Precedenti', fontsize=16)
    plt.xlabel('Risposta', fontsize=12)
    plt.ylabel('Frequenza (Numero di Individui)', fontsize=12)

    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f')

    plt.tight_layout()
    plt.show()

# Frequenza della Condizione di Depressione 
def plot_depression_distribution(train):
    depression_counts = train['Depression'].value_counts()
    depression_labels = {0: 'No', 1: 'Sì'}
    depression_counts_labeled = depression_counts.rename(index=depression_labels)

    plt.figure(figsize=(7, 5))
    ax = sns.barplot(x=depression_counts_labeled.index, y=depression_counts_labeled.values, palette='viridis')
    plt.title('Frequenza della Condizione di Depressione', fontsize=16)
    plt.xlabel('Presenza di Depressione', fontsize=12)
    plt.ylabel('Frequenza (Numero di Individui)', fontsize=12)

    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f')

    plt.tight_layout()
    plt.show()

# Frequenza della Depressione per Genere
def plot_depression_by_gender(train):
    gender_labels = {0: 'Femmina', 1: 'Maschio'}
    depression_labels = {0: 'No Depressione', 1: 'Sì Depressione'}

    plt.figure(figsize=(10, 6))
    ax = sns.countplot(data=train, x='Gender', hue='Depression', palette='viridis')
    plt.title('Frequenza della Depressione per Genere', fontsize=16)
    plt.xlabel('Genere', fontsize=12)
    plt.ylabel('Frequenza (Numero di Individui)', fontsize=12)
    plt.xticks(ticks=[0, 1], labels=[gender_labels[0], gender_labels[1]], rotation=0)

    handles, labels = ax.get_legend_handles_labels()
    new_labels = [depression_labels[int(lbl)] for lbl in labels]
    ax.legend(handles, new_labels, title='Condizione Depressione')

    for container in ax.containers:
        for p in container.patches:
            height = p.get_height()
            if height > 0:
                ax.text(p.get_x() + p.get_width() / 2., height + 50,
                        f'{int(height)}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

# Frequenza dei Pensieri Suicidi Precedenti in base alla Depressione
def plot_suicidal_thoughts_by_depression(train):
    depression_labels = {0: 'No Depressione', 1: 'Sì Depressione'}
    suicidal_thoughts_labels = {'0': 'No (Pensieri)', '1': 'Sì (Pensieri)', 0: 'No (Pensieri)', 1: 'Sì (Pensieri)'}

    plt.figure(figsize=(9, 6))
    ax = sns.countplot(data=train, x='Depression', hue='Have you ever had suicidal thoughts ?', palette='pastel')
    plt.title('Frequenza dei Pensieri Suicidi Precedenti in base alla Depressione', fontsize=16)
    plt.xlabel('Condizione di Depressione', fontsize=12)
    plt.ylabel('Frequenza (Numero di Individui)', fontsize=12)
    plt.xticks(ticks=[0, 1], labels=[depression_labels[0], depression_labels[1]], rotation=0)

    handles, labels = ax.get_legend_handles_labels()
    new_legend_labels = [suicidal_thoughts_labels.get(lbl, lbl) for lbl in labels]
    ax.legend(handles, new_legend_labels, title='Pensieri Suicidi Precedenti')

    for container in ax.containers:
        for p in container.patches:
            height = p.get_height()
            if height > 0:
                ax.text(p.get_x() + p.get_width() / 2., height + 50, f'{int(height)}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

# --- Frequenza della Depressione per Regione ---

# 0     Central India              0
# 1        East India              1
# 2  North-East India              2
# 3  North-West India              3
# 4             Other              4
# 5       South India              5
# 6      West-Gujarat              6
# 7  West-Maharashtra              7
def plot_depression_by_region(train):
    depression_labels = {0: 'No Depressione', 1: 'Sì Depressione'}
    region_codes_order_sorted = sorted(train['Region_Encoded'].unique())
    region_labels = {
        0: 'Central India',
        1: 'East India',
        2: 'North-East India',
        3: 'North-West India',
        4: 'Other',
        5: 'South India',
        6: 'West-Gujarat',
        7: 'West-Maharashtra'
    }

    # Create the countplot
    plt.figure(figsize=(14, 7))
    ax = sns.countplot(
        data=train,
        x='Region_Encoded',
        hue='Depression',
        palette='viridis',
        order=region_codes_order_sorted
    )

    # Replace numeric x-tick labels with region names
    xtick_names = [region_labels[code] for code in region_codes_order_sorted]
    ax.set_xticklabels(xtick_names, rotation=45, ha='right')

    # Titles and labels
    plt.title('Frequenza della Depressione per Regione', fontsize=16)
    plt.xlabel('Regione', fontsize=12)
    plt.ylabel('Frequenza (Numero di Individui)', fontsize=12)

    # Update legend labels
    handles, labels = ax.get_legend_handles_labels()
    new_legend_labels = [depression_labels[int(lbl)] for lbl in labels]
    ax.legend(handles, new_legend_labels, title='Condizione Depressione')

    plt.tight_layout()
    plt.show()

# Distribuzione dello Stress Finanziario per Stato di Depressione
def plot_financial_stress_by_depression(train):
    depression_labels_plot = {0: 'No Depressione', 1: 'Sì Depressione'}

    plt.figure(figsize=(8, 6))
    ax = sns.boxplot(data=train, x='Depression', y='Financial Stress', palette='viridis')
    plt.title('Distribuzione dello Stress Finanziario per Stato di Depressione', fontsize=16)
    plt.xlabel('Condizione di Depressione', fontsize=12)
    plt.ylabel('Stress Finanziario', fontsize=12)
    plt.xticks(ticks=[0, 1], labels=[depression_labels_plot[0], depression_labels_plot[1]], rotation=0)
    plt.tight_layout()
    plt.show()

# Distribuzione dell'Età per Stato di Depressione 
def plot_age_distribution_by_depression(train):
    depression_labels_plot = {0: 'No Depressione', 1: 'Sì Depressione'}

    plt.figure(figsize=(8, 6))
    ax = sns.boxplot(data=train, x='Depression', y='Age', palette='viridis')
    plt.title("Distribuzione dell'Età per Stato di Depressione", fontsize=16)
    plt.xlabel('Condizione di Depressione', fontsize=12)
    plt.ylabel('Età', fontsize=12)
    plt.xticks(ticks=[0, 1], labels=[depression_labels_plot[0], depression_labels_plot[1]], rotation=0)

    plt.tight_layout()
    plt.show()
   
# Frequenza della Depressione per Gruppo di Laurea
def plot_depression_by_degree_group(train):
    """
    Plotta la frequenza della depressione suddivisa per gruppo di laurea utilizzando le etichette testuali.
    """
    depression_labels = {0: 'No Depressione', 1: 'Sì Depressione'}
    degree_order = sorted(train['Degree_Group_Encoded'].unique())
    degree_labels = {
        0: 'Other',
        1: 'High School',
        2: 'Bachelor',
        3: 'Master',
        4: 'Doctorate'
    }

    plt.figure(figsize=(10, 6))
    ax = sns.countplot(
        data=train,
        x='Degree_Group_Encoded',
        hue='Depression',
        palette='viridis',
        order=degree_order
    )

    # Sostituisci i codici dei gruppi di laurea con le etichette testuali
    xtick_names = [degree_labels[code] for code in degree_order]
    ax.set_xticklabels(xtick_names, rotation=0, ha='center')

    # Titolo e assi
    plt.title('Frequenza della Depressione per Gruppo di Laurea', fontsize=16)
    plt.xlabel('Gruppo di Laurea', fontsize=12)
    plt.ylabel('Frequenza (Numero di Individui)', fontsize=12)

    # Legenda con etichette di depressione testuali
    handles, labels = ax.get_legend_handles_labels()
    new_legend_labels = [depression_labels[int(lbl)] for lbl in labels]
    ax.legend(handles, new_legend_labels, title='Condizione Depressione')

    # Aggiungi etichette sui bar
    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f', label_type='edge', padding=3)

    plt.tight_layout()
    plt.show()

# Frequenza della Depressione per Livello di Soddisfazione nello Studio
def plot_depression_by_study_satisfaction(train):
    depression_labels = {0: 'No Depressione', 1: 'Sì Depressione'}
    satisfaction_order = sorted(train['Study Satisfaction'].unique())

    plt.figure(figsize=(10, 6))
    ax = sns.countplot(data=train, x='Study Satisfaction', hue='Depression',
                       palette='viridis', order=satisfaction_order)

    plt.title('Frequenza della Depressione per Livello di Soddisfazione nello Studio', fontsize=16)
    plt.xlabel('Soddisfazione nello Studio (Scala)', fontsize=12)
    plt.ylabel('Frequenza (Numero di Individui)', fontsize=12)
    plt.xticks(rotation=0)

    handles, labels = ax.get_legend_handles_labels()
    new_legend_labels = [depression_labels[int(lbl)] for lbl in labels]
    ax.legend(handles, new_legend_labels, title='Condizione Depressione')

    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f', label_type='edge', padding=3)

    plt.tight_layout()
    plt.show()

# Matrice di correlazione
def plot_pearson_correlation(train):
    cols = ['Age', 'CGPA', 'Sleep Duration', 'Work/Study Hours']
    corr_matrix = train[cols].corr(method='pearson')

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='viridis', fmt='.2f', square=True,
                linewidths=0.5, linecolor='white', cbar_kws={'shrink': .75})
    plt.title('Matrice di Correlazione di Pearson', fontsize=16)
    plt.tight_layout()
    plt.show()

def menu_visualizzazioni():
    train = pd.read_csv('Mentally/cleaned_train.csv')

    print(train[['Gender', 'Depression']].head())

    # Calcolo della distribuzione proporzionale
    proportions = train.groupby('Gender')['Depression'].value_counts(normalize=True).unstack()

    # Moltiplica per 100 per ottenere percentuali
    proportions_percentuali = proportions * 100

    # Visualizza il risultato
    print(proportions_percentuali)
    while True:
        print("\n MENU VISUALIZZAZIONI")
        print("1. Distribuzione del Genere")
        print("2. Distribuzione Studente vs Professionista")
        print("3. Frequenza Pensieri Suicidi Precedenti")
        print("4. Frequenza della Condizione di Depressione")
        print("5. Depressione per Genere")
        print("6. Pensieri Suicidi in base alla Depressione")
        print("7. Depressione per Regione")
        print("8. Stress Finanziario per Stato di Depressione")
        print("9. Età per Stato di Depressione")
        print("10. Correlazione Pearson (Age, CGPA, Sleep, Work Hours)")
        print("11. Depressione per Gruppo di Laurea")
        print("12. Depressione per Soddisfazione nello Studio")
        print("13. Depressione per Status (Studente vs Professionista)")
        print("0. Esci")

        scelta = input("\nSeleziona un'opzione (0-13): ")

        if scelta == '1':
            plot_gender_distribution(train)
        elif scelta == '2':
            plot_status_distribution(train)
        elif scelta == '3':
            suicidal_thoughts_counts = train['Have you ever had suicidal thoughts ?'].value_counts()
            plot_suicidal_thoughts_distribution(suicidal_thoughts_counts)
        elif scelta == '4':
            plot_depression_distribution(train)
        elif scelta == '5':
            plot_depression_by_gender(train)
        elif scelta == '6':
            plot_suicidal_thoughts_by_depression(train)
        elif scelta == '7':
            plot_depression_by_region(train)
        elif scelta == '8':
            plot_financial_stress_by_depression(train)
        elif scelta == '9':
            plot_age_distribution_by_depression(train)
        elif scelta == '10':
            plot_pearson_correlation(train)
        elif scelta == '11':
            plot_depression_by_degree_group(train)
        elif scelta == '12':
            plot_depression_by_study_satisfaction(train)
        elif scelta == '13':
            plot_depression_by_status(train)
        elif scelta == '0':
            print("Uscita dal menù.")
            break
        else:
            print("Scelta non valida. Riprova.")
