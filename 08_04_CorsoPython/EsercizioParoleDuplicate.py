# Restituire parole duplicate a partire dagli articoli (quindi >= 2)
def pulisciParola(ins):
    sostpromax = [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
    ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', 
    '{', '|', '}', '~', '£', '€', '¥', '§', '©', '®', '™', '°', '±', '¶', '•',
    '–', '—', '‘', '’', '“', '”', '„', '…', '‰', '‹', '›', '⁄', '⁎', '⁑', '⁓',
    '₤', '₧', '₨', '₩', '₪', '₫', '€', '₭', '₮', '₯', '₰', '₱', '₲', '₳', '₴',
    '₵', '₶', '₷', '₸', '₹', '₺', '₻', '₼', '₽', '₾', '₿']
    for c in sostpromax: # ciclo tutti i careatteri speciali e tramite replace sostituiamo con il nulla
        ins = ins.replace(c,"")
    return ins


def contaParole(inserimento): # Funzione che controlla i duplicati
    conteggio = {} # Dizionario dove successivamente inserire le parole
    parole = inserimento.split() 
    for parola in parole: # tramite il ciclo e l'if conto l'occorrenza delle parole
        if parola in conteggio:
            conteggio[parola] += 1
        else:
            conteggio[parola] = 1

    duplicato = {k : v for k,v in conteggio.items() if v > 1} # Controllo tutte le parole che appaiono più di una volta
    for key, value in duplicato.items():
        print(f"\nLa parola [{key}] appare [{value}] volte, ed è lunga [{len(key)}]!")
    
    if not duplicato:
        print("\nNon ci sono duplicati!")
    
    

inserimento = input("\nBenvenuto in Duplicas!\nInserisci la tua parola o frase: ").lower().strip()
ins = pulisciParola(inserimento)
contaParole(ins)