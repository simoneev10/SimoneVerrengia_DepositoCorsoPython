# Esercizio cifrario di Cesare
# Dizionario di mappatura
alfabeto_chiave_id = {
    # Numeri -> Lettere maiuscole (1-26)
    1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I',
    10: 'J', 11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q',
    18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y',
    26: 'Z',
    
    # Numeri -> Lettere minuscole (101-126)
    101: 'a', 102: 'b', 103: 'c', 104: 'd', 105: 'e', 106: 'f', 107: 'g',
    108: 'h', 109: 'i', 110: 'j', 111: 'k', 112: 'l', 113: 'm', 114: 'n',
    115: 'o', 116: 'p', 117: 'q', 118: 'r', 119: 's', 120: 't', 121: 'u',
    122: 'v', 123: 'w', 124: 'x', 125: 'y', 126: 'z',
    
    # Caratteri speciali (201-...)
    201: '!', 202: '"', 203: '#', 204: '$', 205: '%', 206: '&', 207: "'",
    208: '(', 209: ')', 210: '*', 211: '+', 212: ',', 213: '-', 214: '.',
    215: '/', 216: ':', 217: ';', 218: '<', 219: '=', 220: '>', 221: '?',
    222: '@', 223: '[', 224: '\\', 225: ']', 226: '^', 227: '_', 228: '`',
    229: '{', 230: '|', 231: '}', 232: '~',
    
    # Caratteri speciali internazionali
    233: '£', 234: '€', 235: '¥', 236: '§', 237: '©', 238: '®', 239: '™',
    240: '°', 241: '±', 242: '¶', 243: '•', 244: '–', 245: '—', 246: '‘',
    247: '’', 248: '“', 249: '”', 250: '…', 251: '‰', 252: '‹', 253: '›',
    254: '⁄', 255: '₿'
}

def cifra(testo, chiave):
    # Crea un dizionario inverso, mappando le lettere ai numeri
    alfabeto_chiave_lettera = {v: k for k, v in alfabeto_chiave_id.items()}
    
    # Cifratura
    testo_cifrato = []
    
    for char in testo:
        if char in alfabeto_chiave_lettera:
            # Trova la posizione numerica del carattere nel dizionario
            posizione = alfabeto_chiave_lettera[char]
            
            # Applica la chiave con il modulo 256 (per includere anche caratteri speciali)
            nuova_posizione = (posizione + chiave) % 256
            
            # Trova il carattere corrispondente alla nuova posizione
            testo_cifrato.append(alfabeto_chiave_id[nuova_posizione])
        else:
             # Se non lo trova space lo appende
            testo_cifrato.append(char)

    
    return ''.join(testo_cifrato) #per restituire una stringa

def decifra(testo, chiave):
    return cifra(testo, -chiave)

while True:
    print("\nMENU CIFRATURA")
    print("1. Cifra un messaggio")
    print("2. Decifra un messaggio")
    print("3. Esci")
    scelta = input("Scegli un'opzione (1-3): ")    
    match scelta:
        case "1":
            frase = input("Inserisci la frase da cifrare: ")
            chiave = int(input("Inserisci la chiave numerica: "))
            print(f"\nRisultato cifrato: {cifra(frase, chiave)}")
        case "2":
            frase = input("Inserisci la frase da decifrare: ")
            chiave = int(input("Inserisci la chiave numerica: "))
            print(f"\nRisultato decifrato: {decifra(frase, chiave)}")
        case "3":
            print("Programma terminato.")
            break
        case _:
            print("Scelta non valida. Riprova.")