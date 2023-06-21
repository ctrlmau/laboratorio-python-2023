"""
candy crush, seconda parte. concetti e funzionamento su una griglia.
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
numero_righe = 5
griglia_colori = []
vicino_uguale = []

# qui salveremo PuntoGriglia
class PuntoGriglia:

    def __init__(self, lato, x=None, y=None, riga=None, colonna=None):
        self.coordinata_x = x
        self.coordinata_y = y
        self.lato = lato

        self.riga = riga
        self.colonna = colonna

        # se sono impostate x e y, trasformo in riga e colonna
        if self.coordinata_x is not None and self.coordinata_y is not None:
            self.calcola_riga_colonna()

    def calcola_riga_colonna(self):
        self.riga = self.coordinata_y // self.lato
        self.colonna = self.coordinata_x // self.lato

    def __eq__(self, other):
        # due PuntoGriglia sono lo stesso, se riga e colonna combaciano
        if self.riga == other.riga and self.colonna == other.colonna:
            return True
        return False

    def __str__(self):
        return f"Sono un punto di riga {self.riga} e colonna {self.colonna}"



def colore_a_caso():
    colore = random.choice(["blu", "rosso", "verde", "giallo", "viola"])
    return colore

# ... qui caricheremo i colori
for indice_riga in range(numero_righe):
    riga = []
    for indice_colonna in range(numero_colonne):
        riga.append(colore_a_caso())
    griglia_colori.append(riga)

# print(griglia_colori)


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
vuoto_img = carica_immagine("vuoto2.png")

pygame.init()
finestra = pygame.display.set_mode((lato * numero_colonne, lato * numero_righe)) # tengo ora conto anche delle righe
pygame.display.update()

def disegna_candy(griglia_colori, quadrato_selezionato=None):
    for riga_indice, riga in enumerate(griglia_colori):
        for colonna_indice, colore in enumerate(riga):
            if colore == "blu":
                if quadrato_selezionato is not None and quadrato_selezionato.colonna == colonna_indice and quadrato_selezionato.riga == riga_indice:
                    immagine = blu_giu_img
                else:
                    immagine = blu_img
            elif colore == "rosso":
                if quadrato_selezionato is not None and quadrato_selezionato.colonna == colonna_indice and quadrato_selezionato.riga == riga_indice:
                    immagine = rosso_giu_img
                else:
                    immagine = rosso_img
            elif colore == "verde":
                if quadrato_selezionato is not None and quadrato_selezionato.colonna == colonna_indice and quadrato_selezionato.riga == riga_indice:
                    immagine = verde_giu_img
                else:
                    immagine = verde_img
            elif colore == "viola":
                if quadrato_selezionato is not None and quadrato_selezionato.colonna == colonna_indice and quadrato_selezionato.riga == riga_indice:
                    immagine = viola_giu_img
                else:
                    immagine = viola_img
            elif colore == "giallo":
                if quadrato_selezionato is not None and quadrato_selezionato.colonna == colonna_indice and quadrato_selezionato.riga == riga_indice:
                    immagine = giallo_giu_img
                else:
                    immagine = giallo_img
            elif colore == "vuoto":
                immagine = vuoto_img
            finestra.blit(immagine, (colonna_indice * lato, riga_indice * lato, lato, lato))

    pygame.display.update()



def scambio_valido(quadrato_origine, quadrato_destinazione):
    # lo scambio valido in candy crush controlla anche che si formino almeno 3 elementi in fila con la mossa...
    # la nostra e' una versione un po' semplificata
    if quadrato_origine.riga == quadrato_destinazione.riga:
        if quadrato_origine.colonna == quadrato_destinazione.colonna + 1:
            return True

        if quadrato_origine.colonna == quadrato_destinazione.colonna - 1:
            return True

    if quadrato_origine.colonna == quadrato_destinazione.colonna:
        if quadrato_origine.riga == quadrato_destinazione.riga + 1:
            return True

        if quadrato_origine.riga == quadrato_destinazione.riga - 1:
            return True

    print("Scambio non valido!")
    return False

def scambia_quadrati(quadrato_origine, quadrato_destinazione):
    if not scambio_valido(quadrato_origine, quadrato_destinazione):
        return False
    pos1_x = quadrato_origine.colonna
    pos1_y = quadrato_origine.riga
    pos2_x = quadrato_destinazione.colonna
    pos2_y = quadrato_destinazione.riga
    originale_pos1 = griglia_colori[pos1_y][pos1_x]
    originale_pos2 = griglia_colori[pos2_y][pos2_x]

    # questo controllo e' necessario per non scambiare un "vuoto" con quello sopra "vuoto"
    # quando i "vuoti" stanno cadendo dall'alto... al posto di un altro vuoto...
    if originale_pos1 == "vuoto" and originale_pos2 == "vuoto":
        return False
    
    griglia_colori[pos1_y][pos1_x] = originale_pos2
    griglia_colori[pos2_y][pos2_x] = originale_pos1
    return True


def calcola_vicini_uguali(griglia_colori):
    # versione che guarda a 3 elementi uguali in fila
    # simile a quella della versione precedente, che pero' si fermava a 2
    vicino_uguale.clear()
    # prima inizializzo tutto a False...
    for contatore_riga in range(numero_righe):
        riga = []
        for index in range(numero_colonne):
            riga.append(False)
        vicino_uguale.append(riga)

    # verifico per le righe, gli elementi vicini da mettere True:
    for pos_y in range(numero_righe):
        for pos_x in range(numero_colonne - 2):
            if griglia_colori[pos_y][pos_x] == griglia_colori[pos_y][pos_x + 1] and \
               griglia_colori[pos_y][pos_x] == griglia_colori[pos_y][pos_x + 2]:
                vicino_uguale[pos_y][pos_x] = True
                vicino_uguale[pos_y][pos_x + 1] = True
                vicino_uguale[pos_y][pos_x + 2] = True

    # verifico per le colonne, gli elementi vicini da mettere True:
    for pos_y in range(numero_righe - 2):
        for pos_x in range(numero_colonne):
            if griglia_colori[pos_y][pos_x] == griglia_colori[pos_y+1][pos_x] and \
               griglia_colori[pos_y][pos_x] == griglia_colori[pos_y+2][pos_x]:
                vicino_uguale[pos_y][pos_x] = True
                vicino_uguale[pos_y + 1][pos_x] = True
                vicino_uguale[pos_y + 2][pos_x] = True

    # print(vicino_uguale)


# verifica se devo eliminare elementi
def devo_eliminare(vicino_uguale):
    for riga in vicino_uguale:
        for vero_o_falso in riga:
            # essendo un valore booleano e' gia' di per se True/False
            # non serve verificare l'uguaglianza con == True
            if vero_o_falso:
                return True
    return False

# elimino tutti gli elementi con un "vicino uguale"
def elimina_candy(griglia_colori, vicino_uguale):
    for pos_y in range(numero_righe):
        for pos_x in range(numero_colonne):
            # essendo un valore booleano e' gia' di per se True/False
            # non serve verificare l'uguaglianza con == True
            if vicino_uguale[pos_y][pos_x]:
                griglia_colori[pos_y][pos_x] = "vuoto"


# se elimino candy devo gestire la caduta di quelli sopra
def cadono_candy(griglia_colori):
    cadono = True
    while cadono:
        cadono = False
        # le righe dal basso verso l'alto fino alla penultima (seconda), in ordine inverso
        for pos_y in range(numero_righe - 1, 0, -1):
            for pos_x in range(numero_colonne):
                if griglia_colori[pos_y][pos_x] == "vuoto":
                    origine = PuntoGriglia(lato, riga=pos_y, colonna=pos_x)
                    destinazione = PuntoGriglia(lato, riga=(pos_y-1), colonna=pos_x)
                    scambiato = scambia_quadrati(origine, destinazione)
                    if scambiato:
                        cadono = True

# gli elementi vuoti, vengono riempiti con un nuovo simbolo a caso
def nuovi_candy(griglia_colori):
    for pos_y in range(numero_righe):
        for pos_x in range(numero_colonne):
            if griglia_colori[pos_y][pos_x] == "vuoto":
                griglia_colori[pos_y][pos_x] = colore_a_caso()

# un semplice algoritmo per determinare i punti di una mossa
def calcola_punteggio(vicino_uguale):
    quanti_elimino = 0
    for pos_y in range(numero_righe):
        for pos_x in range(numero_colonne):
            if vicino_uguale[pos_y][pos_x]:
                quanti_elimino = quanti_elimino + 1

    if quanti_elimino == 3:
        return 3
    if quanti_elimino == 4:
        return 7
    if quanti_elimino == 5:
        return 15
    if quanti_elimino == 6:
        return 31
    if quanti_elimino == 7:
        return 63
    if quanti_elimino > 7:
        return 127



disegna_candy(griglia_colori)

game_over = False
eliminare = False
quadrato_origine = None
quadrato_destinazione = None
punteggio = 0

inizio_gioco = datetime.datetime.now()
durata_gioco = datetime.timedelta(seconds=120)

while not game_over:
    pygame.time.delay(100)

    # gestione degli eventi
    for event in pygame.event.get():

        # usciamo dal programma?
        if event.type == pygame.QUIT:
            game_over = True

        # se invece interagiamo col mouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            coordinata_x = event.pos[0]
            coordinata_y = event.pos[1]

            # punto cliccato come oggetto PuntoGriglia
            punto_cliccato = PuntoGriglia(lato, x=coordinata_x, y=coordinata_y)
            # print("Punto cliccato, riga", punto_cliccato.riga)
            # print("Punto cliccato, colonna", punto_cliccato.colonna)
            if quadrato_origine is None:  # non posso piu usare = None per come ho definito __eq__ sopra
                quadrato_origine = punto_cliccato
            else:
                if quadrato_origine == punto_cliccato:
                    quadrato_origine = None
                else:
                    quadrato_destinazione = punto_cliccato
                    scambia_quadrati(quadrato_origine, quadrato_destinazione)
                    quadrato_origine = None
                    quadrato_destinazione = None
                    calcola_vicini_uguali(griglia_colori)
                    eliminare = devo_eliminare(vicino_uguale)
                    # print("Elementi da elminare:", eliminare)

            disegna_candy(griglia_colori, quadrato_origine)

            if eliminare:
                elimina_candy(griglia_colori, vicino_uguale)
                disegna_candy(griglia_colori)
                eliminare = False
                pygame.time.delay(300)
                cadono_candy(griglia_colori)
                disegna_candy(griglia_colori)
                pygame.time.delay(500)
                nuovi_candy(griglia_colori)
                disegna_candy(griglia_colori)
                punti_mossa = calcola_punteggio(vicino_uguale)
                punteggio = punteggio + punti_mossa
                print("Punti per questa mossa:", punti_mossa)

    adesso = datetime.datetime.now()
    if adesso - inizio_gioco > durata_gioco:
        game_over = True


print("------------------")
print("   GAME OVER      ")
print("  tempo scaduto!  ")
print("punteggio: ", punteggio)

pygame.display.quit()
pygame.quit()