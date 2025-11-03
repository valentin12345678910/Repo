from turtle import *

def kreis(radius, farbe):
    fillcolor(farbe)
    begin_fill()
    circle(radius)
    end_fill()

    farben = [ "purple", "orange", "pink", "cyan", "magenta", "lime", "navy", "teal" ]

    goto(0, -300)

    for i in range(12):
        kreis(50, farben[i % len(farben)])
        left(30)
        forward(50)
        right(30)
        forward(50)
        right(150)
        forward(50)
        left(30)
        backward(50)