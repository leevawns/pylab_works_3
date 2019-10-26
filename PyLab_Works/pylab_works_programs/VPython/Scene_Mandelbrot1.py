#from __future__ import division
from visual import *

# Pixel plotting, Bruce Sherwood, Jan. 1, 2008

# Lay out a vertical stack of horizontal lines (curve objects).
# Each line has two points per pixel, with the same color
# applied to the two points, so that there is no color
# interpolation between pixels (see curve in reference manual).

XMAX = 400 # x and y range over 0 to XMAX
#scene.width = XMAX
#scene.fov = 0.01 # make effectively 2D
#scene.range = XMAX/2
scene.center = (XMAX/2,XMAX/2)
haspoints = False # assume no "points" object (Visual 4)

Coordinate_Axis (100)
scene.range = 300



try: 
    #scene.height = XMAX+60 # titlebar plus toolbar 60 pixels high
    pixels = points() 
    haspoints = True
except:
    #scene.height = XMAX+23 # the title bar is 23 pixels high
    # Set up a vertical stack of horizontal lines
    #scene.visible = False # while laying out the curves
    t = arange(2*XMAX) # a numeric/numpy array
    lines = []
    for y in range(XMAX):
        lines.append(curve())
        last = lines[-1]
        last.x = (t+1)//2 # integer division gives 0,1,1,2,2,3,3,....
        last.y = y
        last.color = array(zeros((2*XMAX,3)))
    #scene.visible = True

# This sets the color c of a point at pixel location (nx,ny).
# nx and ny must be integers.
# (nx,ny) measured from lower left corner of window.
# c is a triple (red,green,blue).
def plot(nx,ny,c):
    if haspoints:
        pixels.append(pos=(nx,ny,0), color=c)
    else:
        lines[ny].color[2*nx] = c
        lines[ny].color[2*nx+1] = c

#---------------------------------------

### Simple example: Give every pixel a random color:
##from random import random
##for y in range(XMAX):
##    for x in range(XMAX):
##        randomcolor = (random(),random(),random())
##        plot(x,y,randomcolor)

Forward_Up ( None, None, 500 )

# Mandelbrot set (see Wikipedia, for example):
max_iteration = 100.
ny = 0
while True :
  #rate ( 10 )
  if ny < XMAX :
    for nx in range(XMAX):
        x = x0 = -2+nx*3./XMAX # from -2 to 1
        y = y0 = -1.5+ny*3./XMAX
        ##print ny,nx,x,x0,y,y0,
        iteration = 0
        while ( ((x*x+y*y) < 4) and (iteration < max_iteration)):
            xtemp = x*x - y*y + x0
            ytemp = 2*x*y + y0
            x = xtemp
            y = ytemp
            iteration += 1
        # Leave points black if the iteration quickly escapes:
        ##print iteration, max_iteration
        if (.1 < iteration/max_iteration < 1):
            c = color.hsv_to_rgb((iteration/max_iteration-.1,1,1))
            plot(nx,ny,c)

    ny += 1