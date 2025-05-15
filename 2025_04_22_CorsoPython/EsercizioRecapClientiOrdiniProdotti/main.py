from ConnessioneDB import (
    crea_database, crea_tabelle,
    inserisci_cliente, inserisci_ordine, inserisci_prodotto,
    inserisci_prodotto_in_ordine,
    leggi_clienti, leggi_prodotti, leggi_ordini, prezzi_prodotti_ordinati, crea_ordine_e_restituisci_id
)

import numpy as np

def menu():
    while True:
        print("\nBenvenuti nel negozio recappone")
        print("1. Aggiungi cliente")
        print("2. Aggiungi ordine")
        print("3. Aggiungi prodotto")
        print("4. Mostra clienti")
        print("5. Mostra prodotti")
        print("6. Mostra ordini")
        print("7. Associa prodotto a ordine")
        print("8. Statistiche prezzi dei prodotti ordinati")
        print("0. Esci")

        scelta = input("Scegli un'opzione: ")

        if scelta == "1":
            cliente_id = int(input("ID cliente: "))
            nome = input("Nome cliente: ")
            
            risposta = input("Vuoi acquistare un prodotto ora? (s/n): ").lower()
            if risposta == "s":
                prodotti = leggi_prodotti()
                if not prodotti:
                    print("Nessun prodotto disponibile.")
                    continue
                print("Prodotti disponibili:")
                for p in prodotti:
                    print(f"ID: {p[0]}, Nome: {p[1]}, Prezzo: €{p[3]:.2f}")
                prodotto_id = int(input("Inserisci l'ID del prodotto che vuoi acquistare: "))
                
                ordini_id = crea_ordine_e_restituisci_id()
                if ordini_id:
                    inserisci_cliente(cliente_id, ordini_id, nome)
                    inserisci_prodotto_in_ordine(ordini_id, prodotto_id)
                    print("Cliente e ordine registrati correttamente.")
            else:
                inserisci_cliente(cliente_id, None, nome)
                
        elif scelta == "2":
            ordini_id = int(input("ID ordine: "))
            inserisci_ordine(ordini_id)

        elif scelta == "3":
            nome_prodotto = input("Nome prodotto: ")
            prezzo = float(input("Prezzo prodotto: "))
            inserisci_prodotto(nome_prodotto, prezzo)

        elif scelta == "4":
            clienti = leggi_clienti()
            for c in clienti:
                print(f"ID: {c[0]}, Ordine: {c[1]}, Nome: {c[2]}, CF: {c[3]}")

        elif scelta == "5":
            prodotti = leggi_prodotti()
            for p in prodotti:
                print(f"ID: {p[0]}, Nome: {p[1]}, Barcode: {p[2]}, Prezzo: €{p[3]:.2f}")

        elif scelta == "6":
            ordini = leggi_ordini()
            if ordini.size > 0:
                print("Ordini:", ordini)
                print("Totale ordini:", np.sum(ordini))
                print("Media ordini:", np.mean(ordini))
                print("Massimo:", np.max(ordini), "Minimo:", np.min(ordini))
            else:
                print("Nessun ordine presente.")

        elif scelta == "7":
            ordini_id = int(input("ID ordine: "))
            prodotto_id = int(input("ID prodotto: "))
            inserisci_prodotto_in_ordine(ordini_id, prodotto_id)

        elif scelta == "8":
            prezzi = prezzi_prodotti_ordinati()
            totale_ordini = len(prezzi)
            if totale_ordini > 0:
                print(f"\n--- Statistiche ordini ---")
                print(f"Numero ordini con prodotti: {totale_ordini}")
                print(f"Totale valore ordini: €{np.sum(prezzi):.2f}")
                print(f"Prezzo medio per prodotto: €{np.mean(prezzi):.2f}")
                print(f"Prezzo massimo: €{np.max(prezzi):.2f}")
                print(f"Prezzo minimo: €{np.min(prezzi):.2f}")
            else:
                print("Nessun prodotto ordinato.")

        elif scelta == "0":
            print("Uscita dal programma.")
            break

        else:
            print("Opzione non valida.")

if __name__ == "__main__":
    crea_database("negozio")
    crea_tabelle()
    menu()
