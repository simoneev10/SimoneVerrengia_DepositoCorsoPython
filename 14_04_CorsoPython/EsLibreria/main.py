from libreria import Libreria

def menu(libreria):
    print("\n1) Aggiungi libro\n2) Rimuovi libro\n3) Visualizza catalogo\n4) Ricerca libro per titolo\n5) Esci")
    scelta = input("Scegli un'opzione: ")

    match scelta:
        case "1":
            libreria.aggiungi_libro()
            menu(libreria)
        case "2":
            libreria.rimuovi_libro()
            menu(libreria)
        case "3":
            libreria.mostra_catalogo()
            menu(libreria)
        case "4":
            titolo = input("Inserisci il titolo da cercare: ")
            risultati = libreria.cerca_per_titolo(titolo)
            if risultati:
                print("\nRisultati trovati:")
                for libro in risultati:
                    print(f"Titolo: {libro.titolo} - Autore: {libro.autore}")
            else:
                print("Nessun libro trovato con quel titolo.")
            menu(libreria)
        case "5":
            print("Uscita...")
        case _:
            print("Scelta non valida.")
            menu(libreria)

def main():
    l = Libreria()
    menu(l)

if __name__ == "__main__":
    main()
