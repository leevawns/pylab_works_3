from visual import *
from time import clock, sleep
from random import Random, random

# Stars interacting gravitationally
# Program uses Numeric Python arrays for high speed computations
# Adapted by Lensyl Urbano January 4th, 2006.

win=600

Nstars = 20  # change this to have more or fewer stars

G = 6.7e-11 # Universal gravitational constant

# Typical values
Msun = 2E30
Rsun = 2E9
Rtrail = 2e8
L = 0.5e11
vsun = 0.8*sqrt(G*Msun/Rsun)


print """
Right button drag to rotate view.
Left button drag up or down to move in or out.
R = toggle Run mode
T = toggle Trace on / off
C = Clear Trace
"""
origx = 0
origy = 0
w = 704 #+4+4
h = 576 #+24+4
#scene.width=w
#scene.height=h
#scene.x = origx
#scene.y = origy

#setting up camera moves lurbano
maxRange = 2*L
minRange = 0.75*L
lastRange = maxRange
startRange = vector(maxRange, maxRange, maxRange)
Rsteps = 200
start_steps = 400

#scene = display(title="Stars", width=w, height=h, x = 0, y=0,
#                range=startRange, forward=(-1,-1,-1))
#scene.range = startRange * (1.0-(0.5))
#scene.autocenter = 0
##Forward_Up ( None, None, 2e11 )
Forward_Up ( (-1,-1,-1), None, 4*L )

tekst = label ( yoffset = 3.8,
  text = 'R=Run toggle, T=Trace toggle,  C=Trace Clear', 
  font='serif', pos=(0,1.5*L,0))

Stars = []
colors = [color.red, color.green, color.blue,
          color.yellow, color.cyan, color.magenta]
poslist = []
plist = []
mlist = []
rlist = []

rv = Random(10)
print rv

for i in range(Nstars):
    x = -L+2*L*rv.random()
    y = -L+2*L*rv.random()
    z = -L+2*L*rv.random()
    r = Rsun/2+Rsun*rv.random()
    Stars = Stars+[sphere(pos=(x,y,z), radius=r, color=colors[i % 6])]
    #Stars[-1].trail = curve(pos=[Stars[-1].pos], color=colors[i % 6], radius=Rtrail)
    Stars[-1].trail = curve( color=colors[i % 6], radius=Rtrail)
    Stars[-1].alive = 1
    Stars[-1].showtrail = 0
    Stars[-1].vec = 0.0
    mass = Msun*r**3/Rsun**3
    px = mass*(-vsun+2*vsun*rv.random())
    py = mass*(-vsun+2*vsun*rv.random())
    pz = mass*(-vsun+2*vsun*rv.random())
    poslist.append((x,y,z))
    plist.append((px,py,pz))
    mlist.append(mass)
    rlist.append(r)

pos = array(poslist)
p = array(plist)
m = array(mlist)
m.shape = (Nstars,1) # Numeric Python: (1 by Nstars) vs. (Nstars by 1)
radius = array(rlist)

vcm = sum(p)/sum(m) # velocity of center of mass
p = p-m*vcm # make total initial momentum equal zero


#create control window - lurbano
#cwin = display(title="Controls", width=200, height=100,
#               x=0, y=h+24)
#trail_but = uSwitch(title="Trails")
#ride_but = uSwitch(title="Ride", pos=(2.5,0,0))
ride_star = -1

t = 0.0
dt = 1000.0
Nsteps = 0
pos = pos+(p/m)*(dt/2.) # initial half-step
time = clock()
Nhits = 0


###scene_rot_period = 5.0 #seconds for a full rotation of scene
##
###rotate scene
##for i in range(360):
##    scene.forward = rotate(scene.forward, angle=pi/180.0, axis=(0,1,0))
##    sleep(5.0/360.0)
##    
##sleep(5.0)
Trail_On = False
Running  = True

while 1:
  rate(50)
  if Running :
    # Compute all forces on all stars
    r = pos-pos[:,NewAxis] # all pairs of star-to-star vectors
    for n in range(Nstars):
        r[n,n] = 1e6  # otherwise the self-forces are infinite
    rmag = sqrt(add.reduce(r*r,-1)) # star-to-star scalar distances
    hit = less_equal(rmag,radius+radius[:,NewAxis])-identity(Nstars)
    
    try :
      # VPython-5 
      hitlist = sort(nonzero(hit.flat)[0]).tolist() # 1,2 encoded as 1*Nstars+2
    except :
      # VPython-3
      hitlist = sort(nonzero(hit.flat)) # 1,2 encoded as 1*Nstars+2

    F = G*m*m[:,NewAxis]*r/rmag[:,:,NewAxis]**3 # all force pairs
    for n in range(Nstars):
        F[n,n] = 0  # no self-forces
    p = p+sum(F,1)*dt

    # Having updated all momenta, now update all positions         
    pos = pos+(p/m)*dt

    # Update positions of display objects; add trail
    for i in range(Nstars):
        Stars[i].vec = Stars[i].pos - pos[i]
        Stars[i].pos = pos[i]
        #if (Nsteps % 5 == 0 and
        #    trail_but.value == 1 and Stars[i].alive == 1) or Stars[i].showtrail == 1:
        if (Nsteps % 5 == 0 and Trail_On and 
            Stars[i].alive == 1) or Stars[i].showtrail == 1:
            Stars[i].trail.append(pos=pos[i])
            Stars[i].trail.visible = 1

    # If any collisions took place, merge those stars
    for ij in hitlist:
        i, j = divmod(ij,Nstars) # decode star pair
        if not Stars[i].visible: continue
        if not Stars[j].visible: continue
        # m[i] is a one-element list, e.g. [6e30]
        # m[i,0] is an ordinary number, e.g. 6e30
        newpos = (pos[i]*m[i,0]+pos[j]*m[j,0])/(m[i,0]+m[j,0])
        newmass = m[i,0]+m[j,0]
        newp = p[i]+p[j]
        newradius = Rsun*((newmass/Msun)**(1./3.))
        iset, jset = i, j
        if radius[j] > radius[i]:
            iset, jset = j, i
        Stars[iset].radius = newradius
        m[iset,0] = newmass
        pos[iset] = newpos
        p[iset] = newp
        Stars[jset].trail.visible = 0
        Stars[jset].visible = 0
        p[jset] = vector(0,0,0)
        m[jset,0] = Msun*1E-30  # give it a tiny mass
        Nhits = Nhits+1
        pos[jset] = (10.*L*Nhits, 0, 0) # put it far away
        Stars[jset].alive = 0
        Stars[jset].showtrail = 0
        if jset == ride_star:
            ride_star = -1
        

    #if Nsteps == 100:
    #    print '%3.1f seconds for %d steps with %d stars' % (clock()-time, Nsteps, Nstars)
    Nsteps = Nsteps+1
    t = t+dt

  if scene.kb.keys: # is there an event waiting to be processed?
    print 'pipop'
    key = scene.kb.getkey() # obtain keyboard information
    if key in 'rR' :
      Running = not Running
    elif key in 'tT' :
      Trail_On = not Trail_On
    if key in 'cCtT' :
      for i in range ( Nstars ):
        Stars[i].trail.visible = 0
        Stars[i].trail.pos=[]
