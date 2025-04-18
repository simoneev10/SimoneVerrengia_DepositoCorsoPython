"""
7. Quali sono le tre regole fondamentali dell'OOP? Spiegale teoricamente e con esempi pratici, puoi includere codice

Le tre regole fondamentali dell'OOP sono:
-Incapsulamento
-Ereditarietà
-Polimorfismo

Incapsulamento:
consente al programmatore di nascondere i detteagli di un'implementazione,
esponendo solo le interazioni con essa. Esso serve per mantenere il codice pulito e sicuro.

Ereditarietà:
consente di creare nuove classi a partire da classi esistenti, quindi di "ereditare" 
caratteristriche e comportamenti (metodi ed attributi). Quindi riutilizzando o
specificando un comportamento definito in classi base

Polimorfismo:
consente di trattare oggetti di classi differenti attraverso un'interfaccia comune,
facilitando estensione e gestione del codice


9. Cos'è un DB relazionale?  Come posso collegare un DB a Python?

Un Database Relazionale è un tipo di database che organizza i dati in tabelle (dette relazioni) fatte di righe e colonne,
dove ogni tabella rappresenta un'entità (es. clienti, ordini, prodotti). Nelle tabelle ci sono righe,ossia un record (es. Simone, 27),
e colonne, ossia un attributo (es. nome, età - collegandoci alle righe).
Le relazioni tra tabelle sono definite da chiavi primarie e chiavi esterne.
- chiavi primarie = sono le attributi univoci per ogni record della tabella e vengono usate come collegamento ad altre tabelle
- chiavi esterne = sono i riferimenti alle chiavi primarie di tabelle collegate ad altre

Un db può essere collegato a Python tramite sqlite3, importandolo nel file creando tabelle e gestendo file direttamente da qui.
Durante il corso poi abbiamo anche visto come connettere un db tramite my-sql-connector collegandoci ad un db esterno creato con XAMP


11. Cos'è un JOIN? Di quali tipi ne esistono? Spiegali teoricamente, puoi aggiungere query esplicative

Un JOIN è un'operazione SQL che combina righe da due o più tabelle in base a una condizione di relazione tra di esse. 
Viene utilizzato per recuperare dati correlati da tabelle diverse in un unico risultato.
Esistono diversi tipi di JOIN ed essi sono:

- INNER JOIN
Restituisce solo le righe che hanno corrispondenza in entrambe le tabelle.
ES:

SELECT colonne
FROM Tabella1
INNER JOIN Tabella2 ON Tabella1.colonna = Tabella2.colonna;

- LEFT JOIN 
Restituisce tutte le righe della tabella a sinistra (prima menzionata) e le corrispondenze dalla tabella a destra. Se non c'è corrispondenza, i valori a destra sono NULL.

SELECT colonne
FROM Tabella1
LEFT JOIN Tabella2 ON Tabella1.colonna = Tabella2.colonna;

- RIGHT JOIN 
Restituisce tutte le righe della tabella a destra (seconda menzionata) e le corrispondenze da quella a sinistra. Se non c'è corrispondenza, i valori a sinistra sono NULL.

SELECT colonne
FROM Tabella1
RIGHT JOIN Tabella2 ON Tabella1.colonna = Tabella2.colonna;


- FULL JOIN 
Restituisce tutte le righe quando c'è una corrispondenza in una delle due tabelle. Se non c'è corrispondenza, NULL dove mancano corrispondenze.

SELECT colonne
FROM Tabella1
FULL JOIN Tabella2 ON Tabella1.colonna = Tabella2.colonna;


14. Cos'è l'astrazione? Spiegala teoricamente e con esempi pratici, puoi includere codice

L'astrazione è quel concetto per cui il programmatore può astrarre un concetto reale e portandolo nel codice simulandone
caratteristiche e comportamenti. Si può intendere come una creazione di un tipo presente nella realtà ma non nei linguaggi di programmazione.

class Veicolo: # Creazione classe veicolo con attributi protetti
    def __init__(self, marca, anno_immatricolazione, targa):
        self._marca = marca
        self._anno_immatricolazione = anno_immatricolazione
        self._targa = targa
        self._revisione = False # la imposto inizialmente a False

    # Getter e Setter
    def get_marca(self):
        return self._marca

    def set_marca(self, marca):
        self._marca = marca

    def get_anno_immatricolazione(self):
        return self._anno_immatricolazione

    def set_anno_immatricolazione(self, anno):
        self._anno_immatricolazione = anno

    def get_targa(self):
        return self._targa

    def set_targa(self, targa):
        self._targa = targa

    def is_revisionato(self):
        return self._revisione

    def set_revisione(self, stato):
        self._revisione = stato

    def descrivi(self):
        return f"Marca: {self._marca}\nAnno: {self._anno_immatricolazione}\nTarga: {self._targa}\nRevisione: {'Sì' if self._revisione else 'No'}"

class Auto(Veicolo):
    def __init__(self, marca, anno_immatricolazione, targa, modello):
        super().__init__(marca, anno_immatricolazione, targa)
        self.modello = modello
        
    def descrivi(self):
        return f"\nMarca: {self._marca}\nModello: {self.modello}\nAnno: {self._anno_immatricolazione}\nTarga: {self._targa}\nRevisione: {'Sì' if self._revisione else 'No'}"

Tramite questo esempio possiamo capire come abbiamo fatto in modo di creare un veicolo che è un tipo che non esiste in python e l'abbiamo concretizzato tramite la classe Auto

18. Cos'è NumPy? Spiega le sue funzioni e perché viene ancora utilizzato? Quali sono le sue principali funzioni?

NumPy è una libreria open-source per Python specializzata in calcolo numerico ad alte prestazioni, ottimizzato 
ed utilizzato principalmente per operazioni matematiche, scientifiche e di data analysis.
Fornisce un nuovo oggetto l'array multidimensionale (ndarray), più efficiente delle liste Python.
NumPy è ancora usato e rimane fondamentale perché:
- Gli array NumPy sono implementati in C, quindi molto più veloci delle liste Python.
- Modalità di memorizzazione dei dati, più efficiente
- Operazioni vettorizzate: Permette di evitare loop espliciti (es. array * 2 invece di [x*2 for x in lista]).
- Base per altre librerie molto importanti per il Machine Learning come Pandas, SciPy e Scikit-learn.
- Possibilità di utilizzare formule matematiche avanzate

20. Extra: Cos'è la coerenza funzionale e perchè è importante per l'OOP?

La coerenza funzionale è la capacità del codice di essere eseguito in maniera coerente inpendentemente dalla macchina (a parità di caratterestiche).
è importante perchè aiuta a scrivere codice chiaro e prevedibile, favorisce la manutenibilità e la leggibilità, riduce il rischio di bug legati a comportamenti "strani" o inaspettati



"""