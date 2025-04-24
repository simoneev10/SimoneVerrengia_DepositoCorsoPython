# Normalizzazione Min-Max in Pandas

Questo progetto dimostra come applicare la normalizzazione min-max a un dataset di caratteristiche fisiche utilizzando la libreria pandas in Python.

## Panoramica

La normalizzazione è un passaggio fondamentale nel preprocessing dei dati, specialmente quando si lavora con algoritmi di machine learning sensibili alla scala. Questo esempio illustra come normalizzare selettivamente alcune colonne di un DataFrame, mantenendo altre nel loro formato originale.

## Funzionalità

- Creazione di un DataFrame pandas con dati demografici simulati (altezza, peso, età)
- Applicazione della normalizzazione min-max a colonne specifiche
- Visualizzazione comparativa tra dati originali e normalizzati

## Normalizzazione Min-Max

La normalizzazione min-max ridimensiona i valori di una variabile nell'intervallo [0,1] utilizzando la formula:

```
x_norm = (x - x.min()) / (x.max() - x.min())
```

dove:
- `x` è il valore originale
- `x.min()` è il valore minimo della variabile
- `x.max()` è il valore massimo della variabile

Dopo questa trasformazione:
- Il valore minimo nella serie originale diventa 0
- Il valore massimo nella serie originale diventa 1
- Tutti gli altri valori vengono ridimensionati proporzionalmente tra 0 e 1

## Vantaggi della Normalizzazione Min-Max

- **Scala uniforme**: Porta tutte le variabili nella stessa scala
- **Preserva le relazioni**: Mantiene le relazioni tra i valori originali
- **Migliora le performance**: Molti algoritmi di machine learning funzionano meglio con dati normalizzati
- **Riduce il bias di scala**: Impedisce che variabili con valori maggiori dominino nell'analisi

## Limitazioni

- È sensibile agli outlier
- Non rende la distribuzione dei dati più gaussiana (a differenza della standardizzazione Z-score)

## Applicazioni

La normalizzazione min-max è particolarmente utile per:

- Reti neurali con funzioni di attivazione sigmoidali
- Algoritmi basati sulla distanza (come k-nearest neighbors)
- Visualizzazione di dati con scale diverse
- Sistemi di raccomandazione e algoritmi di clustering

## Estensioni Possibili

- Implementare altri metodi di normalizzazione (Z-score, Robust Scaling)
- Aggiungere gestione automatica degli outlier
- Creare una funzione generica per normalizzare selettivamente le colonne
