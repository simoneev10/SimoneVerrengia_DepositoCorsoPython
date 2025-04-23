# Introduzione alla Visualizzazione dei Dati con Matplotlib e Seaborn

Questo repository contiene i materiali per un'introduzione sulle librerie di visualizzazione dati in Python: **Matplotlib** e **Seaborn**, parte del Corso Python.

## 🎯 Obiettivi della lezione

Questo modulo introduce i concetti fondamentali della visualizzazione dei dati in Python utilizzando due delle librerie più potenti e diffuse:

- **Matplotlib**: libreria di base per la creazione di grafici statici, animazioni e visualizzazioni interattive
- **Seaborn**: libreria di alto livello basata su Matplotlib che fornisce un'interfaccia semplificata per creare visualizzazioni statistiche esteticamente gradevoli

## 📋 Contenuti della lezione

### Matplotlib

- **Struttura di base**: Figure e Axes
- **Tipi di grafici principali**:
  - Line plots (plot)
  - Scatter plots (scatter)
  - Bar charts (bar, barh)
  - Histograms (hist)
  - Pie charts (pie)
  - Box plots (boxplot)
- **Personalizzazione dei grafici**:
  - Titoli, etichette e leggende
  - Colori e stili
  - Griglie e assi
  - Annotazioni
- **Layout e subplot**: creazione di visualizzazioni multiple

### Seaborn

- **Vantaggi di Seaborn rispetto a Matplotlib**
- **Stili e palette di colori predefiniti**
- **Principali funzioni di visualizzazione**:
  - `relplot()`, `scatterplot()`, `lineplot()` per relazioni
  - `displot()`, `histplot()`, `kdeplot()` per distribuzioni
  - `catplot()`, `boxplot()`, `violinplot()`, `stripplot()` per dati categorici
  - `heatmap()` per matrici di correlazione
- **Facet Grid e FacetGrid per visualizzazioni condizionali**

### Integrazione con Pandas

- Visualizzazione diretta da DataFrame
- Manipolazione dei dati per visualizzazioni efficaci

## 📁 Contenuto del repository

- `01_MatplotlibIntroduzione.ipynb`: Notebook con introduzione a Matplotlib
- `02_Seaborn.ipynb`: Notebook con introduzione a Seaborn
- Dataset di esempio

## 🛠️ Setup e prerequisiti

Per seguire questa dir è necessario avere installato:

```bash
pip install matplotlib seaborn pandas numpy
```
