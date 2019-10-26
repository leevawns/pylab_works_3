# by Eduardo Saraiva
# faubost@gmail.com

from visual import *
from visual.text import *
import time
import random

Forward_Up ( None, None, 30 )

#Terreno que vai aparecer por baixo
def terreno():

    coordenadas=list()
    for x in range(15):
        coordenadas.append(list())
        for y in range(10):
            coordenadas[x].append(list())
            coordenadas[x][y]=-8+cos(x)*sin(y)
    for x in range(14):
        for y in range(9):
            p1=(x,coordenadas[x][y],y)
            p2=(x+1,coordenadas[x+1][y],y)
            p3=(x,coordenadas[x][y+1],y+1)
            p4=(x+1,coordenadas[x+1][y+1],y+1)
            faces(frame=plano,pos=[p1,p3,p2],color=(random.random(),random.random(),random.random()))
            faces(frame=plano,pos=[p4,p2,p3],color=(random.random(),random.random(),random.random()))




#scene.fullscreen=1
plano=frame()
scene.center = (7,-1,0)
scene.background = (0.1,0.1,0.1)
nome=text(pos =(0.5,0,0), string ="EDUARDO SARAIVA", height=1, depth=0.2,
     color = (1,0.5,0))
empresa=text(pos =(3,-1.5,0), string ="96 672 16 48", height=1, depth=0.2,
     color = (0.5,0.5,1))

# A volta do nome
caixa = frame()
box(frame=caixa,pos=(7,-2,0), height=0.1, length=14, width=1)
box(frame=caixa,pos=(7,1.5,0), height=0.1, length=14, width=1)
box(frame=caixa,pos=(0,0,0), height=4.1, length=0.1, width=1)
box(frame=caixa,pos=(14,0,0), height=4.1, length=0.1, width=1)

# relogio e ponteiros
cylinder(pos=(7,-5,0), axis=(0,0,-0.2), radius=2.5, color=(0.9,0.9,0.9))
cylinder(pos=(7,-5,0.01), axis=(0,0,-0.2), radius=2.3, color=(0.7,0.7,0.7))
text(pos =(6.7,-3.2,.1), string ="12", height=0.4, depth=0.2, color =(0,0,0))
text(pos =(8.9,-5.2,.1), string ="3", height=0.4, depth=0.2, color =(0,0,0))
text(pos =(6.9,-7.2,.1), string ="6", height=0.4, depth=0.2, color =(0,0,0))
text(pos =(4.9,-5.2,.1), string ="9", height=0.4, depth=0.2, color =(0,0,0))
sphere(pos=(7,-5,0),radius=0.3,color=(1,0.7,0.1))
horas = arrow(pos=(7,-5,0), axis=(0,1.5,0), shaftwidth=0.2, color = (0.4,0.4,0.4))
minutos = arrow(pos=(7,-5,0), axis=(0,1.9,0), shaftwidth=0.18, color = (0,0.4,0.4))


# bola, sombra e anel e anel
bola=sphere(pos=(2,2,0), radius=0.5)
sombra = cylinder(pos=(2,1.5401,0), axis=(0,0.011,0), radius=0.5, color = (0,0,0))
anel = ring(pos=(7,3,0), radius=0.8, color = (1,0,0), thickness = 0.1)
bola_vel = 0.2
bola_vel = 0.1


scene.center = (7,-1,0)
tempo_str = time.strftime("%H:%M")
tempo_label = label(pos=(scene.center), text=tempo_str, xoffset=-400, yoffset=-320, line = 0)
tempo = text(pos =(0,4,0), string=tempo_str.upper(), height=0.5, depth=0.2, color = (1,0.5,1))

tempo_horas = int(time.strftime("%H"))
tempo_minutos = int(time.strftime("%M"))

horas.rotate(angle=((-(2.*pi)/60)/12)*((tempo_horas*60)+tempo_minutos), axis =(0,0,1))
minutos.rotate(angle=(-(2.*pi)/60)*tempo_minutos, axis=(0,0,1))

x=0
#faz o terreno
terreno()
while 1:
    rate(50)

    x = x + 0.001
    scene.forward=(sin(x*2),-0.4,-1)
    for obj in caixa.objects:
        obj.color = (abs(cos(-pi*x*10)),abs(cos(pi*x*7)),abs(sin(pi*x*15)))

    if (bola.pos.x>13.0)or(bola.pos.x<1):
        bola_vel = -bola_vel

    if bola.pos.x>4 and bola.pos.x<6:
        bola.pos.y = 2 + abs(cos((bola.pos.x-6) * pi/4))
    if bola.pos.x>8 and bola.pos.x<10:
        bola.pos.y = 2 + abs(cos((bola.pos.x-8) * pi/4))

    bola.pos.x = bola.pos.x + bola_vel
    sombra.pos.x = bola.pos.x

    bola.color = (1,3-bola.pos.y,3-bola.pos.y)
    anel.color = (1,-2+bola.pos.y,-2+bola.pos.y)

    if tempo.string <> time.strftime("%H:%M"):
        for obj in tempo.objects:
            obj.visible = 0
        tempo_str = time.strftime("%H:%M")
        tempo = text(pos =(0,4,0), text = tempo_str.upper(), height=0.5, depth=0.2, color = (1,0.5,1))
        horas.rotate(angle=((-(2.*pi)/60)/12), axis =(0,0,1))
        minutos.rotate(angle=(-(2.*pi)/60), axis=(0,0,1))

    tempo_label.text=time.strftime("%H:%M:%S")
    scene.background = (abs(cos(-pi*x*1))/3,abs(cos(pi*x*0.7))/3,abs(sin(pi*x*1.5))/3)












