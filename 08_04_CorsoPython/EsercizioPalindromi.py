# Scrivere una funzione che accetta una parola o una frase e verificare se palindroma

def palindroma(inserimento, ins):
    # sost = [" ",",",".","!","?","-"]
    sostpromax = [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
    ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', 
    '{', '|', '}', '~', '£', '€', '¥', '§', '©', '®', '™', '°', '±', '¶', '•',
    '–', '—', '‘', '’', '“', '”', '„', '…', '‰', '‹', '›', '⁄', '⁎', '⁑', '⁓',
    '₤', '₧', '₨', '₩', '₪', '₫', '€', '₭', '₮', '₯', '₰', '₱', '₲', '₳', '₴',
    '₵', '₶', '₷', '₸', '₹', '₺', '₻', '₼', '₽', '₾', '₿']
    for c in sostpromax: # ciclo tutti i careatteri speciali e tramite replace sostituiamo con il nulla
        ins = ins.replace(c,"")
    
    appo = ins[::-1] # metto la parola 'reverse' in appo
    if ins == appo:
        print(f"\nLa parola o la frase [{inserimento}] è palindorma")
    else:
        print(f"\nLa parola o la frase [{inserimento}] non è palindorma")


inserimento = input("\nBenvenuto in Palimbros!\nInserisci la tua parola o frase: ")       
ins = inserimento.lower()
palindroma(inserimento, ins)