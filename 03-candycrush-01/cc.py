"""
candy crush, prima parte. concetti e funzionamento su una singola linea.
realizzato per il laboratorio python delle scuole superiori di Monfalcone e Staranzano
autore: Maurizio Colautti
ctrl.mau@gmail.com 

nota: la versione corrente e' volutamente semplificata per poter adattarsi
      ad una lezione di 3 ore per ragazzi con un certo tipo di competenze
alcuni comandi print sono commentati; venivano usati per verificare
da parte degli studenti che tutto funzionasse correttamente

semplificazioni di gioco:
- in candy crush originale si possono invertire due elementi solo la loro inversione
  produce una sequenza di elementi che poi vengono eliminati. La nostra versione no.
- in candy crush originale gli elementi vengono eliminati prima di poter effettuare mosse
  se i nuovi elementi formano gia' una combinazione eliminabile. La nostra versione no.
"""

import random
import pygame
import datetime

lato = 58
numero_colonne = 7
colore_colonne = []
vicino_uguale = []

# scelgo un colore a caso, lo ritorno
def colore_a_caso():
    colore = random.choice(["blu", "rosso", "verde"])
    return colore

for indice in range(numero_colonne):     # faccio un po' (=numero_colonne) di "giri"
    # e a ogni giro chiedo un colore a caso, e lo aggiungo (append) alla lista
    colore_colonne.append(colore_a_caso())

# print(colore_colonne)  # decommentare per effettuare eventuali "controlli"

# inizializzazioni di pygame...
pygame.init()
finestra = pygame.display.set_mode((lato*numero_colonne, lato))
colore_neutro = (175, 175, 180)
finestra.fill(colore_neutro)
pygame.display.update()


def carica_immagine(nome_file):
    immagine = pygame.image.load(nome_file)
    immagine_scalata = pygame.transform.scale(immagine, (lato, lato))
    return immagine_scalata

blu_img = carica_immagine("blu.png")
blu_giu_img = carica_immagine("blu_giu.png")

rosso_img = carica_immagine("rosso.png")
rosso_giu_img = carica_immagine("rosso_giu.png")

verde_img = carica_immagine("verde.png")
verde_giu_img = carica_immagine("verde_giu.png")

giallo_img = carica_immagine("giallo.png")
giallo_giu_img = carica_immagine("giallo_giu.png")

viola_img = carica_immagine("viola.png")
viola_giu_img = carica_immagine("viola_giu.png")

vuoto_img = carica_immagine("vuoto.png")


def disegna_quadrati(colore_colonne, evidenziato=-1):
    for posizione, colore in enumerate(colore_colonne):
        if colore == "blu":
            if evidenziato == posizione:
                immagine = blu_giu_img
            else:
                immagine = blu_img
        elif colore == "rosso":
            if evidenziato == posizione:
                immagine = rosso_giu_img
            else:
                immagine = rosso_img
        elif colore == "verde":
            if evidenziato == posizione:
                immagine = verde_giu_img
            else:
                immagine = verde_img
        elif colore == "viola":
            if evidenziato == posizione:
                immagine = viola_giu_img
            else:
                immagine = viola_img
        elif colore == "giallo":
            if evidenziato == posizione:
                immagine = giallo_giu_img
            else:
                immagine = giallo_img
        elif colore == "vuoto":
            immagine = vuoto_img
        # disegna: l'immagine, a pos x, y, di larghezza e altezza = lato
        finestra.blit(immagine, (posizione * lato, 0, lato, lato))

    pygame.display.update()


# da coordinata di pixel, a indice di colonna
def trasforma_x_in_numero(coordinata_x):
    colonna = coordinata_x // lato
    return colonna

# uno scambio e' valido solo fra elementi adiacenti
# in candy crush uno scambio inoltre deve produrre elementi contigui uguali...
# ma questa seconda condizione e' stata ignorata in questa versione semplificata
def scambio_valido(pos1, pos2):
    if pos1 == pos2 + 1:
        return True
    if pos2 == pos1 + 1:
        return True

    return False

# scambio le posizioni... solo se lo scambio e' valido!
def scambia_posizioni(pos1, pos2):
    if scambio_valido(pos1, pos2):
        originale_pos1 = colore_colonne[pos1]
        originale_pos2 = colore_colonne[pos2]
        colore_colonne[pos1] = originale_pos2
        colore_colonne[pos2] = originale_pos1

# tengo traccia per ogni elemento con una lista parallela
# se, elemento per elemento, fa parte di una sequenza di DUE elementi uguali
def calcola_vicini_uguali(colore_colonne):
    vicino_uguale.clear()
    for index in range(numero_colonne):
        vicino_uguale.append(False)

    for index in range(numero_colonne - 1):
        if colore_colonne[index] == colore_colonne[index + 1]:
            vicino_uguale[index] = True
            vicino_uguale[index + 1] = True

# verifico se devo eliminare
def devo_eliminare(vicino_uguale):
    for vero_o_falso in vicino_uguale:
        if vero_o_falso == True:
            return True
    return False

# eliminare significa impostare al "colore vuoto"
def elimina_quadrato(colore_colonne, vicino_uguale):
    for indice, vero_o_falso in enumerate(vicino_uguale):
        if vero_o_falso == True:
            colore_colonne[indice] = "vuoto"

# un algoritmo semplice semplice per attribuire un punteggio ad una mossa
def calcola_punteggio(vicino_uguale):
    numero_eliminati = 0
    for vero_o_falso in vicino_uguale:
        if vero_o_falso == True:
            numero_eliminati = numero_eliminati + 1

    if numero_eliminati == 2:
        return 1
    if numero_eliminati == 3:
        return 3
    if numero_eliminati == 4:
        return 7
    if numero_eliminati == 5:
        return 15
    if numero_eliminati == 6:
        return 31
    if numero_eliminati == 7:
        return 63
    if numero_eliminati > 7:
        return 127

# se ho eliminato elementi, ho bisogno di nuovi colori casuali
def nuovi_quadrati(colore_colonne):
    for index, colore in enumerate(colore_colonne):
        if colore == "vuoto":
            colore_colonne[index] = colore_a_caso()

selezione_1 = -1  # uso -1 per indicare che il primo elemento NON e' stato ancora selezionato
disegna_quadrati(colore_colonne)
game_over = False           # tengo traccia se sto giocando o se è game over
elimina = False
punteggio = 0

inizio_gioco = datetime.datetime.now()
durata_gioco = datetime.timedelta(seconds=120)

while not game_over:        # fintanto che non è game over...
    pygame.time.delay(100)         # aspetto un po'

    for event in pygame.event.get():        # e controllo tutto quello che succede

        if event.type == pygame.QUIT:       # se si e' premuto sul bottone di chiusura
            game_over = True                # allora game over

        elif event.type == pygame.MOUSEBUTTONDOWN:  # se si e' premuto il mouse...
            coordinata_x = event.pos[0]
            # print("Hai cliccato a x = ", coordinata_x)
            colonna = trasforma_x_in_numero(coordinata_x)
            # print("Che equivale alla colonna: ", colonna)

            if selezione_1 == -1:
                selezione_1 = colonna
            else:
                if selezione_1 == colonna:
                    selezione_1 = -1
                else:
                    selezione_2 = colonna
                    scambia_posizioni(selezione_1, selezione_2)
                    calcola_vicini_uguali(colore_colonne)
                    # print(vicino_uguale)
                    elimina = devo_eliminare(vicino_uguale)
                    selezione_1 = -1
                    selezione_2 = -1

            disegna_quadrati(colore_colonne, selezione_1)
            if elimina:
                elimina_quadrato(colore_colonne, vicino_uguale)
                pygame.time.delay(250)
                disegna_quadrati(colore_colonne)
                # print(colore_colonne)
                punti_mossa = calcola_punteggio(vicino_uguale)
                punteggio = punteggio + punti_mossa
                print("Punti mossa: ", punti_mossa)
                nuovi_quadrati(colore_colonne)
                pygame.time.delay(300)
                disegna_quadrati(colore_colonne)
                elimina = False

    # adesso sono passati piu di 30 secondi?
    adesso = datetime.datetime.now()
    if adesso - inizio_gioco > durata_gioco:
        game_over = True

print("------------------")
print("   GAME OVER      ")
print("  tempo scaduto!  ")
print("punteggio: ", punteggio)


pygame.display.quit()
pygame.quit()
