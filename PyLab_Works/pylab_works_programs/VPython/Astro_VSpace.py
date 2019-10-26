#    vspace.py
#
#    Visual Python Space Demo
#    by Ronald Adam 3/20/2005
#
#    A fun little Visual Python Demo
#    Free to use anyway you want, but please send
#    me any changes if you make any improvements.
#
#    Email: ron@ronadam.com

from __future__ import division
from visual import *
import random

def randpoint_onsphere(radius):
    """ Generate a random point on the outside of a sphere.
    """
    theta = random.random() * ( 2 * pi )
    u = random.random() * 2 - 1
    x = radius * sqrt(  1 - u**2) * cos(theta)
    y = radius * sqrt(  1 - u**2) * sin(theta)
    z = radius * u
    return [x,y,z]

def randpoint_incube(side):
    """ Generate a random point inside a cube.
    """
    r = side/2
    x = random.random()*radius*2-radius
    y = random.random()*radius*2-radius
    z = random.random()*radius*2-radius
    return [x,y,z]

def randpoint_insphere(radius):
    """ Generate a random point inside a sphere.
    """
    outside = True
    while outside:
        x = random.random()*radius*2-radius
        y = random.random()*radius*2-radius
        z = random.random()*radius*2-radius
        if (x**2+y**2+z**2)**.5 < radius:
            outside = False
    return [x,y,z]

def rand_3tuple(min=0, max=1):
    """ Generate a random 3 item tuple between a
        minimum and maximum level.
        Good for randome colors values.
    """
    r = (max-min) * random.random() + min
    b = (max-min) * random.random() + min
    g = (max-min) * random.random() + min
    return [r,g,b]


def showhelp():
    text = """
    A Visual Python Space Demo
    By Ronald Adam, 2005

    Point mouse in direct you want to turn.
    Hold left mouse button down to spin.
    """
    print text

showhelp()

# Set up window and sceen.
#scene = display()
#scene.fullscreen = 0
scene.autocenter = 0
scene.autoscale = 0
scene.userzoom = 0
scene.userspin = 0
scene.ambient = 0
scene.range = (10,10,10)
scene.scale = (.1,.1,.1)
lt1 = vector(0,0,1)
lt1.mag = .7

# Size of the visible universe.
spacesize = 500

# Fill outerspace with stars.
nstars = 500
radius = 1+random.random()
outerspace = frame()
for n in xrange(nstars):
    pos = randpoint_onsphere(spacesize*1.5)
    color = rand_3tuple(.3, .7)
    sphere( frame=outerspace, pos=pos, radius=radius, color=color)

# Fill innerspace with space junk.
njunk = 200
radius = 20
innerspace = frame()
adata = {}
for n in xrange(njunk):
    # Get position and size
    pos = randpoint_insphere(spacesize)
    r = random.random()*radius
    # Remember color and motion in dictionary
    rgb = rand_3tuple(.3, .7)
    rotangle = random.random()*.2-.1
    rotaxis = rand_3tuple(.5,1)
    motion = rand_3tuple(.5,1)
    adata[n]= rgb,rotangle,rotaxis,motion
    # Pick a shape
    choice = random.choice([0,1,2,3,4,5])
    if choice == 0:
        sphere(frame=innerspace, pos=pos, radius=r, color=rgb)
    if choice == 1:
        ring(frame=innerspace, pos=pos, radius=r, color=rgb)
    if choice == 2:
        box(frame=innerspace, pos=pos, length=r, height=r*.8, width=r*.6, color=rgb)
    if choice == 3:
        ellipsoid(frame=innerspace, pos=pos, length=r*.8, height=r, width=r*.6, color=rgb)
    if choice == 4:
        pyramid(frame=innerspace, pos=pos, size=[r,r,r], color=rgb)
    if choice == 5:
        cylinder(frame=innerspace, pos=pos, axis=(5,0,0), radius=1, color=rgb)

# sun
sunpos = [0,0,spacesize*1.25]
color = [ 3, 1.5, .75]
sun = sphere( pos=sunpos, radius=50, color=color)

# Spaceship view would go here if we had one.
speed = vector(0,0,3)
xr = yr = zr = yv = xv = zv = 0

# Main loop
while True:
        #rate(100)
        rate(50)
        # Adjust mouse response in case of zoom.
        rotspeed = 200 #+mag(scene.mouse.camera-scene.center)

        # The control stick.
        rx, ry, rz = scene.mouse.pos
        yv += (ry-yv)/10
        try:
            if scene.mouse.button == 'left':
                zv += (rx-zv)/5
        except:
            xv += (rx-xv)/10

        # Our gyro stabalizer... ;)
        xv *= .9
        zv *= .9

        # rotate star frame
        outerspace.rotate( angle=xv/rotspeed, axis=[0,6,0], origin=scene.center)
        outerspace.rotate( angle=yv/rotspeed, axis=[-6,0,0], origin=scene.center)
        outerspace.rotate( angle=zv/rotspeed, axis=[0,0,8], origin=scene.center)

        # rotate sun
        sun.rotate( angle=xv/rotspeed, axis=[0,6,0], origin=scene.center)
        sun.rotate( angle=yv/rotspeed, axis=[-6,0,0], origin=scene.center)
        sun.rotate( angle=zv/rotspeed, axis=[0,0,8], origin=scene.center)
        lt2 = vector(sun.pos)
        lt2.mag = 1.5
        scene.lights = [lt1,lt2]

        # move asteroids
        n = 0
        for obj in innerspace.objects:
            obj.rotate( angle=xv/rotspeed, axis=[0,6,0], origin=scene.center)
            obj.rotate( angle=yv/rotspeed, axis=[-6,0,0], origin=scene.center)
            obj.rotate( angle=zv/rotspeed, axis=[0,0,8], origin=scene.center)
            pos = obj.pos + speed
            if mag(pos) > spacesize:
                pos = randpoint_onsphere(spacesize) # get new position
            obj.pos = vector(pos)
            [r,g,b], rotangle, rotaxis, motion = adata[n]
            # fade to black
            ad = 1-mag(pos)/spacesize
            obj.color = [r*ad,g*ad,b*ad]
            obj.rotate( angle=rotangle/2, axis=rotaxis)
            obj.pos += vector(motion)
            n += 1


