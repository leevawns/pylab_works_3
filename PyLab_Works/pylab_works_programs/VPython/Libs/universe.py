from visual import *
from random import random

a   = vector(0,-9.8,0) # acceleration due to gravity

def collide(object,plane):
    'determine if a collision has occured and send object off on new path'
    if object.visual.pos.y-object.visual.radius<plane.pos.y+plane.size.y/2:
        object.v.y = -object.v.y*object.bounciness
        object.visual.pos.y = object.visual.radius

class Ball:
    def __init__(self,pos=vector(0,0,0),v0=vector(0,0,0),
                 bounciness=1.0, radius=1.0,color=(1,1,1)):
        self.visual = sphere(pos=pos,radius=radius,color=color)
        self.v=v0
        self.visual.pos = pos
        self.bounciness = bounciness

    def update(self,dt):
        # Use Euler's method to update position
        self.visual.pos += self.v*dt
        self.v          += a*dt


class Universe:
    def __init__(self,extent=10,fps=10):
        self.extent=extent
         # Extent is how far from the origin the spherical universe extends
         # in the x and z directions.  It is infinitely tall and deep
         # (y direction).
        self.objects=[]
        self.stationary_objects=[]
        self.fps=fps
        self.dt=1.0/fps
        
    def add(self,object,animated=True):
        'Adds objects to this universe'
        # Objects can be either animated or stationary.
        # Only animated objects get their update methods called.
        if animated:
            self.objects.append(object)
        else:
            self.stationary_objects.append(object)

    def bigbang(self):
        'begins the simulation'
        while True:
            self.tick()
            
    def clip(self,object):
        "removes objects outside this universe's extent"
        if object.visual.pos.x > self.extent or \
           object.visual.pos.z > self.extent or \
           object.visual.pos.x < -self.extent or \
           object.visual.pos.z < -self.extent:
            object.visual.visible=0
            self.objects.remove(object)

    def tick(self):
        '''simulates one time step updating all objects,
           collisions, and clipping'''
        for object in self.objects:
            object.update(self.dt)
            self.clip(object)
            for thing in self.stationary_objects:
                collide(object,thing)
        rate(self.fps)
 
