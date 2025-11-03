from turtle import *

showturtle()
shape("turtle")

def quadrat(länge, farbe):
    color(farbe)
    fillcolor(farbe)
    begin_fill()
    for _ in range(4):
        fd(länge)
        rt(90)
    end_fill()




while True:
    befehl = input("Befehl:").strip()

    try:
        eval(befehl)

    except:
        print("Unbekannter Befehl")    




done()