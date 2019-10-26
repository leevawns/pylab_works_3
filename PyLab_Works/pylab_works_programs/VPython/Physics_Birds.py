#boids.py
#Explores flocking behavior of flying "boids" aka "bird android".
#Requires Python (www.python.org), my favorite programming language, and
#and VPython (www.vpython.org), a fine Python graphics simulation extension for beginners.
#Thanks to Conrad Parker conrad@vergenet.net for the boids pseudocode.
#http://www.vergenet.net/~conrad/boids/pseudocode.html
#Eric Nilsen 
#September 2003
#ericjnilsen@earthlink.net
#Ideas for version 2.0:
#    predators
#    obstructions
#    perching on the ground for a bit
#    prevailing wind
#    random flock scattering
#    cone boid shape --> change boid axis to indicate direction

from visual import *
from random import randrange

class Boids:
    def __init__(self, numboids = 10, sidesize = 100.0):     #class constructor with default parameters filled
        #class constants
        #display(title = "Boids v1.0")   #put a title in the display window

        self.SIDE = sidesize            #unit for a side of the flight space

        #the next six lines define the boundaries of the torus
        """
        torus:  donut shaped space, i.e. infinite
        effect: boids flying out of bounds appear at the opposite side
        note:   cartesian matrices don't handle toruses very well, but I couldn't
                figure out a better way to keep the flock in view.
        """
        self.MINX = self.SIDE * -1.0    #left
        self.MINY = self.SIDE * -1.0    #bottom
        self.MINZ = self.SIDE * -1.0    #back
        self.MAXX = self.SIDE           #right
        self.MAXY = self.SIDE           #top
        self.MAXZ = self.SIDE           #front

        self.RADIUS = 2                 #radius of a boid.  I wimped and used spheres.
        self.NEARBY = self.RADIUS * 5   #the 'halo' of space around each boid
        self.FACTOR = .95               #the amount of movement to the perceived flock center
        self.NEGFACTOR = self.FACTOR * -1.0 #same thing, only negative

        self.NUMBOIDS = numboids        #the number of boids in the flock

        self.boidflock = []             #empty list of boids
        self.DT = 0.02                  #delay time between snapshots

        #self.boids()                    #okay, now that all the constants have initialized, let's fly!

        #def boids(self):
        #self.initializePositions()      #create a space with boids
        #while (1==1):                   #loop forever
        #    rate(100)                   #controls the animation speed, bigger = faster
        #    self.moveAllBoidsToNewPositions()   #um ... what it says

    def initializePositions(self):
        #wire frame of space
        backBottom = curve(pos=[(self.MINX, self.MINY, self.MINZ), (self.MAXX, self.MINY, self.MINZ)], color=color.white)
        backTop = curve(pos=[(self.MINX, self.MAXY, self.MINZ), (self.MAXX, self.MAXY, self.MINZ)], color=color.white)
        frontBottom = curve(pos=[(self.MINX, self.MINY, self.MAXZ), (self.MAXX, self.MINY, self.MAXZ)], color=color.white)
        frontTop = curve(pos=[(self.MINX, self.MAXY, self.MAXZ), (self.MAXX, self.MAXY, self.MAXZ)], color=color.white)
        leftBottom = curve(pos=[(self.MINX, self.MINY, self.MINZ), (self.MINX, self.MINY, self.MAXZ)], color=color.white)
        leftTop = curve(pos=[(self.MINX, self.MAXY, self.MINZ), (self.MINX, self.MAXY, self.MAXZ)], color=color.white)
        rightBottom = curve(pos=[(self.MAXX, self.MINY, self.MINZ), (self.MAXX, self.MINY, self.MAXZ)], color=color.white)
        rightTop = curve(pos=[(self.MAXX, self.MAXY, self.MINZ), (self.MAXX, self.MAXY, self.MAXZ)], color=color.white)
        backLeft = curve(pos=[(self.MINX, self.MINY, self.MINZ), (self.MINX, self.MAXY, self.MINZ)], color=color.white)
        backRight = curve(pos=[(self.MAXX, self.MINY, self.MINZ), (self.MAXX, self.MAXY, self.MINZ)], color=color.white)
        frontLeft = curve(pos=[(self.MINX, self.MINY, self.MAXZ), (self.MINX, self.MAXY, self.MAXZ)], color=color.white)
        frontRight = curve(pos=[(self.MAXX, self.MINY, self.MAXZ), (self.MAXX, self.MAXY, self.MAXZ)], color=color.white)

        #splatter a flock in the space randomly
        c = 0                                   #initialize the color switch
        for b in range(self.NUMBOIDS):          #for each boid, ...
            x = randrange(self.MINX, self.MAXX) #random left-right
            y = randrange(self.MINY, self.MAXY) #random up-down
            z = randrange(self.MINZ, self.MAXZ) #random front-back

            if c > 2:                           #reset the color switch when it grows too big
                c = 0
            if c == 0:
                COLOR = color.yellow            #a third of the boids shall have yellow
            if c == 1:
                COLOR = color.red               #and yea a third of the boids shall have red
            if c == 2:
                COLOR = color.blue              #and verily a third of the boids shall have blue

            #splat a boid, add to flock list
            self.boidflock.append(sphere(pos=(x,y,z), radius=self.RADIUS, color=COLOR))

            c = c + 1                           #increment the color switch

##        self.greenie = sphere(radius=self.RADIUS, color=color.green)    #pseudo-boid for testing

    def moveAllBoidsToNewPositions(self):
        for b in range(self.NUMBOIDS):
            #manage boids hitting the torus 'boundaries'
            if self.boidflock[b].x < self.MINX:
                self.boidflock[b].x = self.MAXX

            if self.boidflock[b].x > self.MAXX:
                self.boidflock[b].x = self.MINX

            if self.boidflock[b].y < self.MINY:
                self.boidflock[b].y = self.MAXY

            if self.boidflock[b].y > self.MAXY:
                self.boidflock[b].y = self.MINY

            if self.boidflock[b].z < self.MINZ:
                self.boidflock[b].z = self.MAXZ

            if self.boidflock[b].z > self.MAXZ:
                self.boidflock[b].z = self.MINZ


            v1 = vector(0.0,0.0,0.0)        #initialize vector for rule 1
            v2 = vector(0.0,0.0,0.0)        #initialize vector for rule 2
            v3 = vector(0.0,0.0,0.0)        #initialize vector for rule 3


            v1 = self.rule1(b)              #get the vector for rule 1
            v2 = self.rule2(b)              #get the vector for rule 2
            v3 = self.rule3(b)              #get the vector for rule 3

            boidvelocity = vector(0.0,0.0,0.0)          #initialize the boid velocity
            boidvelocity = boidvelocity + v1 + v2 + v3  #accumulate the rules vector results
            self.boidflock[b].pos = self.boidflock[b].pos + (boidvelocity*self.DT) #move the boid



    def rule1(self, aboid):    #Rule 1:  boids fly to perceived flock center
        pfc = vector(0.0,0.0,0.0)                   #pfc: perceived flock center
        for b in range(self.NUMBOIDS):              #for all the boids
            if b != aboid:                          #except the boid at hand
                 pfc = pfc + self.boidflock[b].pos  #calculate the total pfc

        pfc = pfc/(self.NUMBOIDS - 1.0)             #average the pfc
##        self.greenie.pos = pfc                      #put greenie at the pfc, see what's going on

        #nudge the boid in the correct direction toward the pfc
        if pfc.x > self.boidflock[aboid].x:
            pfc.x = (pfc.x - self.boidflock[aboid].x)*self.FACTOR
        if pfc.x < self.boidflock[aboid].x:
            pfc.x = (self.boidflock[aboid].x - pfc.x)*self.NEGFACTOR
        if pfc.y > self.boidflock[aboid].y:
            pfc.y = (pfc.y - self.boidflock[aboid].y)*self.FACTOR
        if pfc.y < self.boidflock[aboid].y:
            pfc.y = (self.boidflock[aboid].y - pfc.y)*self.NEGFACTOR
        if pfc.z > self.boidflock[aboid].z:
            pfc.z = (pfc.z - self.boidflock[aboid].z)*self.FACTOR
        if pfc.z < self.boidflock[aboid].z:
            pfc.z = (self.boidflock[aboid].z - pfc.z)*self.NEGFACTOR

        return pfc

    def rule2(self, aboid):    #Rule 2: boids avoid other boids
        v = vector(0.0,0.0,0.0) #initialize the avoidance vector

        for b in range(self.NUMBOIDS):
            if b != aboid:
                if abs(self.boidflock[b].x - self.boidflock[aboid].x) < self.NEARBY:
                    if self.boidflock[b].x > self.boidflock[aboid].x:
                        v.x = self.NEARBY * 12.0    #works better when I multiply by 12, don't know why
                    if self.boidflock[b].x < self.boidflock[aboid].x:
                        v.x = -self.NEARBY * 12.0
                if abs(self.boidflock[b].y - self.boidflock[aboid].y) < self.NEARBY:
                    if self.boidflock[b].y > self.boidflock[aboid].y:
                        v.y = self.NEARBY * 12.0
                    if self.boidflock[b].y < self.boidflock[aboid].y:
                        v.y = -self.NEARBY * 12.0
                if abs(self.boidflock[b].z - self.boidflock[aboid].z) < self.NEARBY:
                    if self.boidflock[b].z > self.boidflock[aboid].z:
                        v.z = self.NEARBY * 12.0
                    if self.boidflock[b].z < self.boidflock[aboid].z:
                        v.z = -self.NEARBY * 12.0

        return v

    def rule3(self, aboid):    #Rule 3: boids try to match speed of flock
        pfv = vector(0.0,0.0,0.0)   #pfv: perceived flock velocity

        for b in range(self.NUMBOIDS):
            if b != aboid:
                 pfv = pfv + self.boidflock[b].pos

        pfv = pfv/(self.NUMBOIDS - 1.0)
        pfv = pfv/(aboid + 1)    #some of the boids are more sluggish than others

        return pfv


#if __name__ == "__main__":
#    #if you run this from Idle via the F5 key, the following occurs:
#    b = Boids()     #instantiate the Boids class, the class constructor takes care of the rest.
##    b = Boids(20, 60.0)   #here's a way to change the flock amount, and space size
b = Boids ()
b.initializePositions()      #create a space with boids

scene.autoscale = False 
scene.autocenter = False 
Forward_Up ( None, None, 300 )

while True :                   #loop forever
  rate(50)                   #controls the animation speed, bigger = faster
  b.moveAllBoidsToNewPositions()   #um ... what it says
