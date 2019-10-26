from visual import *
from time import clock
import random

win=600

print """
Right button drag to rotate view.
Left button drag up or down to move in or out.

Galaxy orientations are random, and the sizes are scaled up by 10
"""

#scene = display(title="2367 Local Galaxies", width=win, height=win,
#                range=30, forward=(-1,-1,-1))

A=3.0
xaxis = curve(pos=[(0,0,0), (A,0,0)], color=(0.5,0.5,0.5))
yaxis = curve(pos=[(0,0,0), (0,A,0)], color=(0.5,0.5,0.5))
zaxis = curve(pos=[(0,0,0), (0,0,A)], color=(0.5,0.5,0.5))

Stars=[cylinder(pos=(0,0,0), radius=30/100.0, color=(1.0,0.0,0.0),
                              length=30/1000.0,
                              axis=(0.0,1.0,0.0) )]
Stars[0].name="Milky Way"

import os

for l in open(My_Path+'/Scene_Random.csv','r').readlines():
    #name,type,radvel,MB,diam,x,y,z,lum=tuple(string.split(l,','))
    name,type,radvel,MB,diam,x,y,z,lum=tuple(l.split(','))
    if name=='Name':
        continue
    type,radvel,MB,diam=int(type),int(radvel),float(MB),float(diam)
    x,y,z=float(x),float(y),float(z)
    if x==0 and y==0 and z==0:    #Discard LMC and SMC, too close to MW
        continue
    if diam<2.0:
        diam=2.0
    if type<-2 or type>9:
        Stars = Stars+[sphere(pos=(x,y,z), radius=diam/100.0, color=(1.0,1.0,1.0))]
    else:
        Stars=Stars+[cylinder(pos=(x,y,z), radius=diam/100.0, color=(1.0,1.0,1.0),
                              length=diam/1000.0,
                              axis=(-1+2*random.random(),
                                    -1+2*random.random(),
                                    -1+2*random.random()) )]
    Stars[-1].name=name  #Specify the name of the last galaxy added


autoscale=0
autocenter=0

Forward_Up ( None, None, 50 ) 

lab=None

while True:
    rate(50)
    if scene.mouse.clicked:
        m=scene.mouse.getclick()
        if m.pick:
            if lab:
                lab.visible=0
            lab=label(pos=m.pick.pos, xoffset=20, yoffset=20, text=m.pick.name)
        else:
            if lab:
                lab.visible=0
