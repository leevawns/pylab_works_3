from visual import *
from random import random, randrange

## this is mostly for experimenting with zooming and rotating

Forward_Up ( None, None, 180 )

print """
Right button drag to rotate "camera" to view scene.
Middle button to drag up or down to zoom in or out.
  On a two-button mouse, middle is left + right.
  On a one-button mouse, middle is CTRL + mouse.
"""

def random_box ():
    xx = randrange (-55,54)
    yy = randrange (-55,54)
    zz = randrange (-55,54)
    x = randrange (-10,11)
    y = randrange (-10,11)
    z = randrange (-10,11)
    red = random()
    green = random()
    blue = random()
    #print xx,yy,zz,x,y,z
    box (pos = vector(xx,yy,zz), length=abs(x), height=abs(y), width=abs(z),
         color=(red,green,blue))
    
def wirecube (s):
    c=curve (color=color.white, radius=1)
    pts = [(-s, -s, -s),(-s, -s, s), (-s, s, s),
           (-s, s, -s), (-s, -s, -s), (s, -s, -s),
           (s, s, -s), (-s, s, -s), (s, s, -s),
           (s, s, s), (-s, s, s), (s, s, s),
           (s, -s, s), (-s, -s, s), (s, -s, s),(s, -s, -s)]
    for pt in pts:
        c.append(pos=pt)

#scene.title = "Random Boxes"
side=60.
wirecube (side)
for i in range ( 100 ) :
    random_box()

arrow(axis = (0,12,0), shaftwidth = 3.5, color=color.red )

ball=sphere(pos=(-side/2.,-side/2.,-side/2.), color=(1,1,0), radius=3)
disk=cylinder(pos=(side/2., side/2., -side/2.), color=(.3,.3,1), axis=(1,1,0),
              radius=5)
xx=arange(0,4*pi,pi/10.)
spring=curve(color=(1,.7,.1), radius=0.4)
for y in xx:
    spring.append(pos=(20+cos(2*y), y/2.-30, -20+sin(2*y)+30))

while True :
  pass