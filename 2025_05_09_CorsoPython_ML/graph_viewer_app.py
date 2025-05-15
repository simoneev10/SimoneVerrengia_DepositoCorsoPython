import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Importa il modulo grafici che contiene le funzioni di plottaggio
# Assicurati che grafici.py sia nella stessa directory
try:
    import grafici
except ImportError:
     messagebox.showerror("Errore di Importazione", "Impossibile importare 'grafici.py'. Assicurati che sia nella stessa directory e contenga le funzioni di plottaggio.")
     sys.exit()

# --- Costante per il file CSV pulito ---
# Questo file deve essere generato da un processo di preprocessing separato
CLEANED_CSV = 'cleaned_train.csv'


# --- Gestione chiusura finestra e plot Matplotlib ---
def on_closing():
    """
    Gestisce la chiusura della finestra principale.
    Chiude esplicitamente i grafici matplotlib prima di distruggere la finestra Tkinter
    per evitare errori durante la pulizia.
    """
    print("Tentativo di chiusura...") # Per debug nel terminale
    try:
        # Chiudi tutte le figure matplotlib aperte
        plt.close('all')
        print("Grafici matplotlib chiusi.") # Per debug
    except Exception as e:
        print(f"Avviso: Errore durante la chiusura dei grafici matplotlib: {type(e).__name__} - {e}")

    # Distruggi la finestra principale di Tkinter
    root.destroy()
    print("Finestra Tkinter distrutta.") # Per debug


# --- Classe per il Frame dei Grafici (Adattata per standalone) ---
class GraphsFrame(ttk.Frame):
    # Rimosso il parametro 'controller' perché non c'è un controller di frame in un'app standalone
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent # Salva una referenza al parent (la finestra root)

        ttk.Label(self, text="Visualizza Grafici di Analisi", font=("Segoe UI", 20)).pack(pady=10)

        # Controlla subito se il file pulito esiste
        if not os.path.exists(CLEANED_CSV):
            ttk.Label(self, text=f"File '{os.path.basename(CLEANED_CSV)}' non trovato.\nAssicurati che il file esista e sia nella stessa directory.", foreground="red").pack(pady=20)
            # Rimosso il bottone "Indietro" perché non c'è dove tornare
            #ttk.Button(self, text="Chiudi", command=self.parent.destroy).pack(pady=10) # Opzionale: bottone per chiudere l'app
            self.df = None # Assicura che df non esista se il file manca
            return # Esce dalla __init__ se il file non c'è

        try:
             self.df = pd.read_csv(CLEANED_CSV)
             if self.df.empty:
                  ttk.Label(self, text=f"File '{os.path.basename(CLEANED_CSV)}' è vuoto.\nAssicurati che contenga dati validi.", foreground="red").pack(pady=20)
                  self.df = None
                  #ttk.Button(self, text="Chiudi", command=self.parent.destroy).pack(pady=10) # Opzionale
                  return
        except pd.errors.EmptyDataError:
             ttk.Label(self, text=f"File '{os.path.basename(CLEANED_CSV)}' è vuoto o danneggiato.\nAssicurati che sia un file CSV valido.", foreground="red").pack(pady=20)
             self.df = None
             #ttk.Button(self, text="Chiudi", command=self.parent.destroy).pack(pady=10) # Opzionale
             return
        except Exception as e:
             ttk.Label(self, text=f"Errore nel caricamento di '{os.path.basename(CLEANED_CSV)}':\n{e}", foreground="red").pack(pady=20)
             self.df = None
             #ttk.Button(self, text="Chiudi", command=self.parent.destroy).pack(pady=10) # Opzionale
             return

        # Se il file è stato caricato con successo, crea la UI per i grafici
        frm = ttk.Frame(self)
        frm.pack(fill='both', expand=True, padx=10, pady=10)
        frm.columnconfigure(1, weight=1) # Rende il contenitore del canvas espandibile

        left = ttk.Frame(frm)
        left.grid(row=0, column=0, sticky='ns', padx=(0,10))

        self.canvas_holder = ttk.Frame(frm)
        self.canvas_holder.grid(row=0, column=1, sticky='nsew')

        # Assicurati che i nomi delle funzioni in grafici.py corrispondano a questi
        # Usa il prefisso grafici. per chiamare le funzioni dal modulo importato
        self.graphs = {
            "1. Distribuzione Genere":           lambda: grafici.plot_gender_distribution(self.df),
            "2. Studente vs Professionista":     lambda: grafici.plot_status_distribution(self.df),
            "3. Pensieri Suicidi Precedenti":    lambda: grafici.plot_suicidal_thoughts_distribution(self.df['Have you ever had suicidal thoughts ?'].value_counts()),
            "4. Condizione di Depressione":      lambda: grafici.plot_depression_distribution(self.df),
            "5. Depressione per Genere":         lambda: grafici.plot_depression_by_gender(self.df),
            "6. Pensieri Suicidi vs Depressione":lambda: grafici.plot_suicidal_thoughts_by_depression(self.df),
            "7. Depressione per Regione":        lambda: grafici.plot_depression_by_region(self.df),
            "8. Stress Finanziario":             lambda: grafici.plot_financial_stress_by_depression(self.df),
            "9. Età vs Depressione":             lambda: grafici.plot_age_distribution_by_depression(self.df),
            "10. Correlazione Pearson":          lambda: grafici.plot_pearson_correlation(self.df),
            "11. Depressione per Gruppo Laurea": lambda: grafici.plot_depression_by_degree_group(self.df),
            "12. Soddisf. Studio":               lambda: grafici.plot_depression_by_study_satisfaction(self.df),
            "13. Depressione per Status":        lambda: grafici.plot_depression_by_status(self.df),
            # Aggiungi qui altre associazioni nome -> lambda per gli altri grafici
        }

        # Crea i bottoni per i grafici
        for name in self.graphs:
            ttk.Button(left, text=name, width=30,
                       command=lambda n=name: self._show_graph(n))\
                .pack(fill='x', pady=2)

        # Rimosso il pulsante "Indietro" nel frame standalone


    def _show_graph(self, name):
        """Mostra il grafico selezionato nel canvas_holder."""
        # Pulisce il contenitore del canvas da widget precedenti
        for w in self.canvas_holder.winfo_children():
            w.destroy()

        # Genera la figura Matplotlib chiamando la funzione corrispondente in grafici.py
        try:
            fig = self.graphs[name]()
        except Exception as e:
             messagebox.showerror("Errore Generazione Grafico", f"Si è verificato un errore durante la creazione del grafico:\n{e}")
             print(f"Errore nella generazione del grafico '{name}': {e}")
             # Pulisci l'area del canvas in caso di errore di generazione
             for w in self.canvas_holder.winfo_children():
                 w.destroy()
             return


        # Embedda la figura nel canvas di Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_holder)
        canvas.draw() # Disegna la figura sul canvas

        # Posiziona il widget Tkinter del canvas nel canvas_holder e fallo espandere
        canvas.get_tk_widget().pack(fill='both', expand=True)

        # Opzionale: Aggiungi la toolbar per zoom/pan (richiede importare NavigationToolbar2Tk)
        # from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        # toolbar = NavigationToolbar2Tk(canvas, self.canvas_holder)
        # toolbar.update()
        # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


# --- Esecuzione dell'applicazione standalone ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Visualizzatore Grafici Analisi Depressione")
    root.geometry("800x600") # Dimensioni iniziali

    # Collega la funzione on_closing all'evento di chiusura della finestra
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Crea un'istanza del GraphsFrame, passandogli la finestra root come parent
    graphs_frame = GraphsFrame(root)
    # Posiziona il frame principale in modo che riempia l'intera finestra
    graphs_frame.pack(fill="both", expand=True)

    # Avvia il loop principale della GUI
    root.mainloop()