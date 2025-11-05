from turtle import *
import random

def zufalls_farbe():
    r, g, b = (random.random() for _ in range(3))
    color(r, g, b)

speed(3000000)
for i in range(10000000000000000000):
    zufalls_farbe()
    circle(100*(1+i*0.001))
    left(10)
    left(10)
done()