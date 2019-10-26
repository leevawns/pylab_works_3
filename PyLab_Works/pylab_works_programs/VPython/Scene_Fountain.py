
from universe import *
from random import random,uniform

#The purpose of the universe object is to update all of the animated
#objects within it and check for collisions between the animated
#objects and stationary objects (like the ground)
universe = Universe(extent=50.0,fps=24) 

# The extent of the universe is how far it extends in the x and z
# directions (horizontal directions) out from the
# origin. The universe in infinite in the vertical direction. Objects
# which travel outside the universe get clipped out of 
# existence.  

# the fps parameter is "frames per second", the maximum frame rate for
# the animation. If the computer is too slow it may run at a slower
# frame rate. 

# add a box to be the ground plane which balls will bounce off of

universe.add(box(size=(2*universe.extent,.1,2*universe.extent),color=(.1,.6,.1)),animated=False)

# add a cylinder which will appear to launch balls out of itself.
# The cylider is not added to the universe because there is no need
# to check for collisions between the balls and the cylinder.

launcher = cylinder(pos=(0,0,0),axis=(0,10,0))

#Need to know the tip position to fire balls from
launchertip = launcher.pos+launcher.axis

targetballnum = 1000 # the number of balls we want to have in the universe

#set the viewing angle and "zoom" to something reasonable
#scene.range=universe.extent
#scene.forward=(0,0,-1)
Forward_Up ( (0,0,-1), None, 100 ) 

# loop forever updating the universe
while True:
    rate ( 50 )
    universe.tick() # the universe updates all of the objects
                    # within it on each time "tick"


    for i in xrange(5):
        # if some balls have been destroyed because they went outside the
        # extent of the universe then add new ones. The for loop
        # allows up to 5 to be added in one frame of animation which
        # corresponds to one "tick" of the universes clock
        if len(universe.objects) < targetballnum:

            #compute randomized starting velocity
            angle = uniform(0,2*pi)
            vx=cos(angle)
            vy=5
            vz=sin(angle)
            initial_velocity =  4*vector(vx,vy,vz)

            #compute a random color
            ballcolor  = (random(),random(),random())

            # contruct a new ball and add it to the universe
            universe.add(Ball(pos=launchertip,
                              v0=initial_velocity,
                              color=ballcolor,
                              radius=0.5,
                              bounciness=0.7))
