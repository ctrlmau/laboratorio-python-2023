"""
da un'idea online anonima
riadattamento per il laboratorio python delle scuole superiori di Monfalcone e Staranzano
autore: Maurizio Colautti
ctrl.mau@gmail.com 

nota: la versione corrente e' volutamente semplificata per poter adattarsi
      ad una lezione di 3 ore per ragazzi con un certo tipo di competenze
"""

import time
import random

print("\nBenvenuto al gioco dell'impiccato\n")
nome = input("Come ti chiami? ") # comando per interagire con l'utente
print("Ciao " + nome + "! Buona fortuna")
time.sleep(3)

# "terza versione" => complichiamo molto il gioco con una lunga lista di parole da cui pescare
# lettura file -> ogni riga un elemento di una lista
with open("parole.txt") as file_parole:
    parole = file_parole.readlines()

# la "seconda versione" usava questa lista di parole...
# parole = ["studente", "lezione", "sport", "computer", "daino", "baseball"]
# la "prima versione" usava una parola fissa
# parola = "studente"
# scelta di una parola a caso
parola = random.choice(parole)
# alla quale va rimosso il carattere di "newline"
parola = parola.replace("\n", "")
parola_originale = parola
lunghezza = len(parola)
gia_provato = []
mostra = "-" * lunghezza


tentativi = 5
indovinato = False

while tentativi > 0 and not indovinato:

    # introduzione testuale ad ogni tentativo
    print("Tentativi rimasti:", tentativi)
    time.sleep(2)
    print("La parola da indovinare è:", mostra)

    # chiedo una lettera
    while True:
        prova = input("Prova con una nuova lettera: \n")
        time.sleep(1)

        if prova not in gia_provato:
            gia_provato.append(prova)
            break
        else: # questo "else" poteva essere evitato ;)
            print("La lettera", prova, "è già stata tentata")
            time.sleep(1)

    # lettera buona!
    if prova in parola:
        print("lettera azzeccata")
        while parola.find(prova) != -1:
            indice = parola.find(prova)
            parola = parola[:indice] + "#" + parola[indice+1:]
            mostra = mostra[:indice] + prova + mostra[indice+1:]
        time.sleep(1)

        if "-" not in mostra:
            print("")
            print("Woooah! Sei riuscito ad indovinare la parola!")
            print("la parola era:", mostra)
            indovinato = True

    # lettera errata!
    else:
        print("La lettera", prova, "non è parte della parola misteriosa")
        tentativi = tentativi - 1

        if tentativi == 4:
            print("   _____ \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "__|__\n")

        if tentativi == 3:
            print("   _____ \n"
                  "  |     |\n"
                  "  |     |\n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "  |      \n"
                  "__|__\n")

        if tentativi == 2:
            print("   _____  \n"
                  "  |     | \n"
                  "  |     | \n"
                  "  |     | \n"
                  "  |       \n"
                  "  |       \n"
                  "  |       \n"
                  "__|__\n")

        if tentativi == 1:
            print("   _____  \n"
                  "  |     | \n"
                  "  |     | \n"
                  "  |     | \n"
                  "  |     O \n"
                  "  |       \n"
                  "  |       \n"
                  "__|__\n")

        if tentativi == 0:
            print("   _____  \n"
                  "  |     | \n"
                  "  |     | \n"
                  "  |     | \n"
                  "  |     O \n"
                  "  |    /|\ \n"
                  "  |    / \ \n"
                  "__|__\n")
            print("La parola da indovinare era:", parola_originale)


print("")
print("Gioco finito")
if indovinato:
    print("Sei stato bravo, ma vincerai la prossima volta?")
else:
    print("Peccato non sei riuscito ad indovinare la parola")
