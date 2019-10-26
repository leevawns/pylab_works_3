#=======================================================
# Simple demo to illustrate the motion of a Big brownian
# particle in a swarm of small particles in 2D motion.
# The spheres collide elastically with themselves and
# with the walls of the box. The masses of the spheres
# are proportional to their radius**3 (as in 3D).
#
# Clicking the left mouse button toggles the display of the
# orbit of the Big brownian sphere. Numerical arrays are
# used to improve the efficiency of the program.
#
# This version uses a multisegmented orbit to improve the
# display of the curve in VPython 2.4
#
# ** To exit the program press ESC **
#
# by E. Velasco. July 2006 version
#=======================================================
from visual import *
from random import *

# Constants and time step
Nsp = 71                # Number of small spheres
Rb = 1.0                # Radius of the big sphere
Rs = 0.43               # Radius of small spheres
Ms=(Rs/Rb)**3           # Mass of the small spheres (Mbig=1)

ShowOrbit = 1           # Do not show the big sphere trajectory
LBox=(16*Rb,12*Rb)      # Size of the box = 2LBox[0].2LBox[1]

#Dt = 0.017              # Time step
Dt = 0.17              # Time step
PSteps = 10             # Plot orbit every PSteps
Nt = 1                  # Number of steps counter

# Color definitions
CSpheres  = (0,0.5,0.9)      # Color of small spheres
CBigSphere  =  (0.9,0.2,0.1) # Color of big sphere
COrbit = color.yellow        # Color of orbit

# Properties of the display window 
#window = display(title="Brownian Motion", width=800, height=600)
#window.fullscreen = 1      # Change to 0 to get a floating window
window = scene
#window.range = (LBox[0],LBox[0],LBox[0])
#window.cursor.visible = 0  # Hide the mouse
window.userspin = 0        # No rotation with mouse
window.userzoom = 0        # No zoom with mouse
#window.forward = (0,0,1)       
Forward_Up ( (0,0,1), None, 40 )
window.lights = [vector(0,0,-1)]
window.ambient=0

label ( pos = ( 0, 13, 0 ), text = 'Click: Clear the track' )

class SegmentedCurve:

    def __init__(self, color=color.white, radius=0):
        self.color = color
        self.radius = radius   
        self.orbit = [curve(pos=[], color=self.color, radius=self.radius)]
        
    def append(self, vector):
        if len(self.orbit[-1].pos)>=1024: # Hardwired in VPython
            self.orbit.append(curve(color=self.color, radius=self.radius))
            self.orbit[-1].pos=[self.orbit[-2].pos[-1]]
        self.orbit[-1].append(pos=vector)
    
    def clear(self):
        for n in xrange(len(self.orbit)):
                self.orbit[n].pos=[]
        del self.orbit[1:]

seed()      # Randomize the random number generator

# Create the arrays with the initial positions of the spheres.
# Start with the big sphere at the center, then put the small
# spheres at random selected from a grid of possible positions.
ListPos=[(0,0)]

PossiblePos=[(x,y) for x in arange(-LBox[0]+2*Rs,LBox[0]-2*Rs,2.2*Rs)
             for y in arange(-LBox[1]+2*Rs,LBox[1]-2*Rs,2.2*Rs)
             if x*x+y*y > Rb+Rs]
             
if Nsp > len(PossiblePos)+1: Nsp = len(PossiblePos)+1

for s in xrange(Nsp-1):
    n = randint(0,len(PossiblePos)-1)
    ListPos.append(PossiblePos[n])
    del PossiblePos[n] 
del PossiblePos
             
Pos = array(ListPos)
del ListPos

# Create an array with all the radius and a list with all the masses
Radius = concatenate( (array([Rb]),array([Rs]*(Nsp-1))) )
Mass=[1.0]+[Ms]*(Nsp-1)

# Create the initial array of velocities at random with big sphere at rest
ListVel=[(0.,0.)]
for s in xrange(1,Nsp):
    ListVel.append( (uniform(-1,1),uniform(-1,1)) )
Vel = array(ListVel)
del ListVel

# Create the spheres (really cylinders in 2D)
Spheres = [cylinder(pos=Pos[0], radius=Radius[0], axis=(0,0,0.2), 
                    color=CBigSphere)]

for s in xrange(1,Nsp):
    Spheres.append( cylinder(pos=Pos[s],axis=(0,0,0.2),
                             radius=Radius[s], color=CSpheres) )

# Create the segmented curve = orbit and put initial point
orbit = SegmentedCurve(color=COrbit)
orbit.append(vector(Pos[0])+vector(0,0,-0.1))

# Auxiliary variables
ID = identity(Nsp)
Q = (Radius+Radius[:,NewAxis])**2

Rij= Pos-Pos[:,NewAxis]
RijMag2 = add.reduce(Rij*Rij,-1)  # Pairs of distances**2
hit = less_equal(RijMag2,Q)-ID

# The main loop
while True :
    #rate(500)   # Slow things down
    rate (50)

    # Update all positions
    add(Pos,Vel*Dt,Pos)      # Fast version of Pos = Pos + Vel*Dt

    # Impose the bouncing at the walls
    for s in xrange(Nsp):
        for n in xrange(2):
            if Pos[s,n] <= -LBox[n]+Radius[s]:
                Pos[s,n] = -LBox[n]+Radius[s]
                Vel[s,n] = -Vel[s,n]
            if Pos[s,n] >= LBox[n]-Radius[s]:
                Pos[s,n] = LBox[n]-Radius[s]
                Vel[s,n] = -Vel[s,n]

    # Create the set of all pairs and the list the colliding spheres
    subtract(Pos,Pos[:,NewAxis],Rij)
    RijMag2 = add.reduce(Rij*Rij,-1)       # Pairs of distances**2
    subtract(less_equal(RijMag2,Q),ID,hit)
    #if VPython_Version == 3 :
    #  hitlist = sort(nonzero(hit.flat)).tolist() # i,j encoded as i*Nsp+j
    #else :
    hitlist = sort(nonzero(hit.flat)[0]).tolist() # i,j encoded as i*Natoms+j
    
    # Check to see if the spheres are colliding
    for ij in hitlist:
        s1,s2 = divmod(ij,Nsp)    # decode the spheres pair (s1,s2) colliding
        hitlist.remove(s2*Nsp+s1) # remove symmetric (s2,s1) pair from list
        R12 = Pos[s2]-Pos[s1]
        d12 = Radius[s1]+Radius[s2] - mag(R12)
        tau = norm(R12)
        DR0 = d12*tau
        x1 = Mass[s1]/(Mass[s1]+Mass[s2])
        x2 = 1-x1                 # x2 = Mass[s2]/(Mass[s1]+Mass[s2])
        DR = array(DR0)[:-1]      # 2D vector DR
        Pos[s1] -= x2*DR
        Pos[s2] += x1*DR
        DV0 = 2*dot(vector(Vel[s2]-Vel[s1]),tau)*tau
        DV =array(DV0)[:-1]       # 2D vector DV0
        Vel[s1] +=  x2*DV
        Vel[s2] -=  x1*DV

    # Toggle the orbit
    if window.mouse.clicked:
        """
        window.mouse.getclick()   # Empty the mouse queue
        ShowOrbit = 1 - ShowOrbit
        Nt = 0
        if ShowOrbit == 0: orbit.clear()
        """
        window.mouse.getclick()   # Empty the mouse queue
        Nt = 0
        orbit.clear()

    # Update the location of the spheres
    for s in xrange(Nsp):
        Spheres[s].pos = Pos[s]
    if ShowOrbit == 1:
        if Nt%PSteps == 0:
           orbit.append(vector(Pos[0])+vector(0,0,-0.1))
        Nt = Nt+1
