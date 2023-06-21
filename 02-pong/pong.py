"""
da un'idea online anonima
riadattamento per il laboratorio python delle scuole superiori di Monfalcone e Staranzano
autore: Maurizio Colautti
ctrl.mau@gmail.com 

nota: la versione corrente e' volutamente semplificata per poter adattarsi
      ad una lezione di 3 ore per ragazzi con un certo tipo di competenze
"""

import turtle
import random

# impostazioni della finestra
finestra = turtle.getscreen()
finestra.setup(800, 600)
finestra.bgcolor("black")
finestra.title("python Pong")
finestra.tracer(0)
finestra.delay(10000)

# registro una nuova forma, con centro in 0,0 e altezza 100, larghezza 20
finestra.register_shape("blocco", ( (-50, -10),
                                    (-50,  10),
                                    ( 50,  10),
                                    ( 50, -10)
                                  )
                       )

blocco_A = turtle.Turtle()
blocco_A.shape("blocco")
blocco_A.color("white")
blocco_A.speed(0)  # sposta istantaneamente
blocco_A.penup()  # non lasciare traccia
blocco_A.setx(-350)  # tutto a sinitra
blocco_A.sety(0)  # centrato in altezza

blocco_B = turtle.Turtle()
blocco_B.shape("blocco")
blocco_B.color("white")
blocco_B.speed(0)
blocco_B.penup()
blocco_B.setx(350)
blocco_B.sety(0)

punteggio = turtle.Turtle()
punteggio.color("yellow")
punteggio.hideturtle()
punteggio.speed(0)
punteggio.penup()
punteggio.setx(0)
punteggio.sety(260)
punteggio.write("Punteggio A: 0 - Punteggio B: 0", align="center", font=("Courier", 24, "bold"))

palla = turtle.Turtle()
palla.shape("circle")
palla.color("red")
palla.speed(0)
palla.penup()
palla.dx = 2
palla.dy = 2

def blocco_A_su():
    y = blocco_A.ycor()
    if y < 220:
        y = y + 10
        blocco_A.sety(y)

def blocco_A_giu():
    y = blocco_A.ycor()
    if y > -235:
        y = y - 10
        blocco_A.sety(y)

def blocco_B_su():
    y = blocco_B.ycor()
    if y < 220:
        y = y + 10
        blocco_B.sety(y)

def blocco_B_giu():
    y = blocco_B.ycor()
    if y > -235:
        y = y - 10
        blocco_B.sety(y)

# fai si che la finestra "ascolti" queste specifiche azioni (pressione tasti)
finestra.listen()
finestra.onkeypress(blocco_A_su, "w")
finestra.onkeypress(blocco_A_giu, "s")
finestra.onkeypress(blocco_B_su, "Up")
finestra.onkeypress(blocco_B_giu, "Down")

punti_A = 0
punti_B = 0

def main():

    # definite globali per fare riferimento a quelle inizializzate al di fuori della funzione
    # e per poterle modificare a piacere
    global punti_A
    global punti_B

    finestra.update()

    if palla.ycor() > 250:
        palla.dy = palla.dy * -1  # rimbalzo sopra
        palla.sety(250)
    if palla.ycor() < -285:
        palla.dy = palla.dy * -1  # rimbalzo sotto
        palla.sety(-285)

    if palla.xcor() > 330 and \
       palla.ycor() < blocco_B.ycor() + 50 and \
       palla.ycor() > blocco_B.ycor() - 50:
        palla.setx(330)  # per non validare l'if sotto > 330
        palla.dx = palla.dx * -1  # rimbalzo
        palla.dx = palla.dx + random.uniform(-0.7, 0)  # palla accelera
        palla.dy = palla.dy + random.uniform(-0.7, 0.7)  # e varia angolazione

    if palla.xcor() < -330 and \
       palla.ycor() < blocco_A.ycor() + 50 and \
       palla.ycor() > blocco_A.ycor() - 50:
        palla.setx(-330)  # per non validare l'if sotto < -330
        palla.dx = palla.dx * -1
        palla.dx = palla.dx + random.uniform(0, 0.7)
        palla.dy = palla.dy + random.uniform(-0.7, 0.7)

    if palla.xcor() > 330:
        print("Punto per A")  # evento importante! lo scrivo sulla consolle
        punti_A = punti_A + 1
        messaggio = f"Punteggio A: {punti_A} - Punteggio B: {punti_B}"
        punteggio.clear()
        punteggio.write(messaggio, align="center", font=("Courier", 24, "bold"))
        palla.setx(0)
        palla.dx = palla.dx * -1
        if palla.dx > 1:  # rallento la palla
            palla.dx = palla.dx / 2


    if palla.xcor() < -330:
        print("Punto per B")
        punti_B = punti_B + 1
        messaggio = f"Punteggio A: {punti_A} - Punteggio B: {punti_B}"
        punteggio.clear()
        punteggio.write(messaggio, align="center", font=("Courier", 24, "bold"))
        palla.setx(0)
        palla.dx = palla.dx * -1
        if palla.dx > 1:
            palla.dx = palla.dx / 2

    palla.goto(palla.xcor() + palla.dx,
               palla.ycor() + palla.dy)
    finestra.ontimer(main, 10)


main()
finestra.mainloop()
