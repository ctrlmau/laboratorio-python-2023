"""
da un'idea di @lemastertech
riadattamento per il laboratorio python delle scuole superiori di Monfalcone e Staranzano
autore: Maurizio Colautti
ctrl.mau@gmail.com

nota: la versione corrente e' volutamente semplificata per poter adattarsi
      ad una lezione di 3 ore per ragazzi con un certo tipo di competenze
"""

import pygame
from pygame import mixer
import json

pygame.init()
# avremo bisogno di un timer
timer = pygame.time.Clock()

# frame al secondo; per spostare la colonna a ritmo
fps = 60

# definizione colori
nero = (0, 0, 0)
grigio = (128, 128, 128)
verde = (0, 255, 0)
azzurro = (0, 255, 255)

# dimensioni personalizzabili! tutto si adatta da solo
finestra_larghezza = 1400
finestra_altezza = 800

# carico i suoni tramite il mixer
crash = mixer.Sound('crash.wav')
hi_hat = mixer.Sound('hihat.wav')
snare = mixer.Sound('snare.wav')
kick = mixer.Sound('kick.wav')
tom = mixer.Sound('tom.wav')
clap = mixer.Sound('clap.wav')

strumenti = [crash, hi_hat, snare, kick, tom, clap]
numero_strumenti = len(strumenti)
strumento_altezza = finestra_altezza // numero_strumenti

# ulteriori settaggi iniziali
numero_beats = 8
beat_attivo = 0
bpm = 240    # battiti al minuto
secondi_in_un_minuto = 60
frame_di_un_beat = fps * secondi_in_un_minuto // bpm  # 60 * 60 // 240


finestra = pygame.display.set_mode((finestra_larghezza, finestra_altezza))
pygame.display.set_caption("my Beat Maker")

# riproduciamo tutti gli strumenti "cliccati" del beat attuale
def riproduci_suono(beat_attivo):
    for indice_strumento in range(numero_strumenti):
        if cliccati[indice_strumento][beat_attivo]:
            strumenti[indice_strumento].play()

# disegniamo la griglia dei beat e degli strumenti
def disegna_griglia(cliccati, beat_attivo=0):
    # nella lista griglia tengo conto di tutti i rettangoli dello schema
    griglia = []
    un_beat_pixel = finestra_larghezza // numero_beats

    for indice_beat in range(numero_beats):
        for indice_strumento in range(numero_strumenti):

            # strumento cliccato sul beat attuale => colore verde
            if cliccati[indice_strumento][indice_beat]:
                colore = verde
            else:
                colore = grigio

            rettangolo = pygame.draw.rect(finestra,
                             colore,
                             [
                              indice_beat * un_beat_pixel + 5,
                              indice_strumento * strumento_altezza + 5,
                              un_beat_pixel - 10,
                              strumento_altezza - 10
                             ],
                             0,
                             10)
            # aggiungo       l'oggetto pygame rettangolo 
            #                             e le informazioni su beat e strumento ("x" e "y")
            griglia.append( [ rettangolo, [indice_beat, indice_strumento] ] )  # <1>

    # disegno un rettangolo attorno al beat attivo
    pygame.draw.rect(finestra,
                azzurro,
                [
                 beat_attivo * un_beat_pixel,
                 0,
                 un_beat_pixel,
                 finestra_altezza
                ],
                5,
                3)

    return griglia

# disegniamo la finestra, delegando quasi tutto a disegna_griglia
def disegna_finestra(cliccati, beat_attivo=0):
    finestra.fill(nero)
    griglia = disegna_griglia(cliccati, beat_attivo)
    pygame.display.update()
    return griglia


# inizializzo la lista degli elementi cliccati
# con n. righe = numero_strumenti
# con n. colorne = numero_beats
# a False (non cliccato)
cliccati = []
for _ in range(numero_strumenti):
    griglia_strumento = []
    for _ in range(numero_beats):
        griglia_strumento.append(False)
    cliccati.append(griglia_strumento)

# tengo traccia in beat_durata da quanto tempo il "beat" è in riproduzione
# per sapere se è ora di passare al prossimo beat 
beat_durata = 0
beat_maker = True
riproduci = True

while beat_maker:

    # qui le operazioni per riprodurre i suoni
    if riproduci:
        if beat_durata < frame_di_un_beat:  # beat ancora in riproduzione
            beat_durata = beat_durata + 1
        else:  # ora di passare al prossimo beat
            beat_attivo = beat_attivo + 1
            if beat_attivo >= numero_beats:
                beat_attivo = 0
            beat_durata = 0
            riproduci_suono(beat_attivo)


    timer.tick(fps)
    griglia = disegna_finestra(cliccati, beat_attivo)

    # qui gestiamo gli eventi
    for evento in pygame.event.get():

        # se vogliamo terminare
        if evento.type == pygame.QUIT:
            beat_maker = False

        # con il mouse gestiamo solo l'attivazione/disattivazione di uno strumento in un beat
        elif evento.type == pygame.MOUSEBUTTONDOWN:

            for elemento in range(len(griglia)):
                # griglia[elemento] torna la lista definita al passo <1>
                # all'indice 0 c'e' il rettangolo pygame che implementa il metodo "collidepoint"
                # per sapere se una coordinata e' interna al rettangolo
                if griglia[elemento][0].collidepoint(evento.pos):
                    coordinate = griglia[elemento][1]  # all'indice 1 ci sono le "coordinate" x e y
                    # con 'not' inverto il valore; True? not True => False; False? not False => True 
                    cliccati[coordinate[1]][coordinate[0]] = not cliccati[coordinate[1]][coordinate[0]]

        # gestione degli eventi da tastiera
        elif evento.type == pygame.KEYDOWN:

            # barra spaziatrice = metti in pausa / riavvia
            if evento.key == pygame.K_SPACE:
                riproduci = not riproduci

            # freccia su => aumenta il numero di beats
            elif evento.key == pygame.K_UP:
                numero_beats = numero_beats + 1
                # il nuovo beat va impostato a False per ogni strumento
                for indice_strumento in range(numero_strumenti):
                    cliccati[indice_strumento].append(False)

            # freccia giu' => diminuisci di uno il numero dei beat
            elif evento.key == pygame.K_DOWN:
                if numero_beats > 8:
                    numero_beats = numero_beats - 1
                    # e rimuovi il beat rimosso da ogni strumento
                    for indice_strumento in range(numero_strumenti):
                        cliccati[indice_strumento].pop()

            # f => faaaaaaaster!
            elif evento.key == pygame.K_f:
                bpm = bpm + 5
                frame_di_un_beat = fps * secondi_in_un_minuto // bpm

            # s => slower...
            elif evento.key == pygame.K_s:
                if bpm > 10:
                    bpm = bpm - 5
                    frame_di_un_beat = fps * secondi_in_un_minuto // bpm

            # ESC => riazzera lo schema
            elif evento.key == pygame.K_ESCAPE:
                for indice_strumento in range(numero_strumenti):
                    for indice_beat in range(numero_beats):
                        cliccati[indice_strumento][indice_beat] = False

            # tasto MENO => scarico giu' nel file salvataggio.json
            elif evento.key == pygame.K_MINUS:
                # un dizionario e' SIMILE ad una lista... con indici personalizzabili 
                dizionario = {}
                dizionario['frame_di_un_beat'] = frame_di_un_beat
                dizionario['bpm'] = bpm
                dizionario['numero_beats'] = numero_beats
                dizionario['cliccati'] = cliccati
                # e la libreria json gestisce i dizionari in modo semplice
                with open("salvataggio.json", "w") as file_salvataggio:
                    # indent = 4... per poter aprire il file e leggerlo ad occhio piu' agevolmente
                    json.dump(dizionario, file_salvataggio, indent=4)

            # tasto PIU' => carico su cio che avevo salvato in salvataggio.json
            elif evento.key == pygame.K_PLUS:
                # mancano dei controlli in questa versione semplificata... 
                with open("salvataggio.json", "r") as file_salvataggio:
                    dizionario = json.load(file_salvataggio)
                # sperando tutto sia andato nel modo giusto, carico le impostazioni
                # per ripartire dove avevamo lasciato!
                frame_di_un_beat = dizionario['frame_di_un_beat']
                bpm = dizionario['bpm']
                numero_beats = dizionario['numero_beats']
                cliccati = dizionario['cliccati']


pygame.display.quit()
pygame.quit()