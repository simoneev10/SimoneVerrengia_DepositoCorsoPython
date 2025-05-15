from mainTest import test
from mainTrain import train
from insertUtente import insert_data
from grafici import menu_visualizzazioni

def menu():
    while True:
        print("Benvenuto nel menu principale!")
        print("1. Analisi, preprocessing, addestramento e previsione su file CSV di training")
        print("2. Analisi, preprocessing, previsione su test e generazione submission" )
        print("3. Predizione dello stato depressivo di una persona (inserimento manuale)")
        print("4. Visualizza grafici")
        print("5. Esci")

    
        choice = input("Scegli un'opzione (1-4): ").strip()
        if choice == '1':
            train()
        elif choice == '2':
            test()
        elif choice == '3':
            insert_data()
        elif choice == '4':
            menu_visualizzazioni()
        elif choice == '5':
            print("Uscita dal programma.")
            break
        else:
            print("Opzione non valida. Riprova.")

if __name__ == "__main__":   
    menu()
