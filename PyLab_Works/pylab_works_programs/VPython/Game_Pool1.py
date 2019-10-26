from copy import copy
from visual import vector,sphere,box,rate,scene,color,mag,norm,dot
from time import time
from random import random,uniform

restitution = 0.5 
friction    = 0.5

# *************************************************
# *************************************************
class Ball:
  def __init__(self,p=vector(0,0,0), v=vector(0,0,0),radius=1.0, mass=1.0,color=color.red):
    self.p = p
    self.v = v
    self.mass=mass
    self.radius=radius
    self.graphic = sphere(pos=self.p,radius=self.radius,color=color)

  def Reset ( self, x, y ) :
    self.p = vector ( x, y, 0 )
    self.v = vector ( 0, 0, 0 )
    self.updategraphic ()
    
  def step(self,dt):
    force = -(friction)*self.v
    a = force/self.mass
    self.v = self.v + a*dt
    self.p = self.p + self.v*dt+1/2*a*dt**2
    if self.p.x > wallR.x-self.radius:
      self.v.x = -self.v.x
    if self.p.x < wallL.x+self.radius:
      self.v.x = -self.v.x
    if self.p.y > wallb.y:
      self.v.y = -self.v.y
    if self.p.y < wallf.y:
      self.v.y = -self.v.y

  def updategraphic(self):
    self.graphic.pos = self.p

  def handleCollision(self,other):
    difference = other.p - self.p
    if mag(difference) < self.radius+other.radius:
      vrelative=other.v - self.v
      normal=norm(difference)
      vrn = dot(vrelative,normal)
      if vrn<0:
        #Collision Detected!
        difference = norm(difference)

        #Compute magnitude of Impulse
        Imag = -(1+restitution) * vrn / (1.0/self.mass + 1.0/other.mass)

        I = Imag*normal # convert to a vector
        
        #Apply impulse to both affected balls
        self.v  -= I / self.mass   
        other.v += I / other.mass


balls=[]  #this list will hold all Ball objects

# Rack `em - make an inverted triangle of balls with random colors
for y in range(6):
  py = 25 + 1.7 * y
  for x in range(y):
    color=(random(),random(),random())
    px = 2 * ( x - ( y - 1 ) / 2.0 )
    balls.append( Ball(p=vector(px,py,0), color=color) )

# *************************************************
# *************************************************
def Restart ( Value = None ) :
  global balls
  i = 0
  for y in range ( 6 ) :
    py = 25 + 1.7 * y
    for x in range ( y ) :
      px = 2 * ( x - ( y - 1 ) / 2.0 )
      balls [i].Reset ( px, py )
      i += 1
  # and the cue ball
  balls[-1].Reset ( uniform(-1,1), 0 )
  balls[-1].v = vector ( 0, 226, 0 )

# *************************************************
# *************************************************
def _On_Set_Friction ( Value = 0.5 ) :
  global friction
  friction = Value

# *************************************************
# *************************************************
def _On_Set_Collision ( Value = 0.5 ) :
  global restitution
  restitution = Value

#add a cueball to the end of the list with slightly random position
balls.append(Ball(p=vector(uniform(-1,1),0,0),v=vector(0,226,0),color=(1,1,.7)))

Forward_Up ( (0,1,-1), None, 40 ) 

table = box(pos=(0,0,-1.1),size=(50,100,.2),color=(.1,.7,0))
wallb = box(pos=(0,-50,0),size=(50,.2,4))
wallf = box(pos=(0,50,0),size=(50,.2,4))
wallL = box(pos=(-25,0,0),size=(.2,100,4))
wallR = box(pos=(25,0,0),size=(.2,100,4))

dt = 1.0/256

# *************************************************
# Define Control Buttons
# *************************************************
VPC.Define ( 1, 2 )
VPC.Set_Button ( 0, 'Restart', Restart  )
VPC.Set_Slider ( 0, 'Friction',  0.0, 1.0, 0.5, 'Lin', '%5.2f', _On_Set_Friction  )
VPC.Set_Slider ( 1, 'Collision', 0.0, 1.0, 0.5, 'Lin', '%5.2f', _On_Set_Collision )

# *************************************************
# Main Loop
# *************************************************
while True:
  rate(50)

  for ball in balls:
    ball.step(dt)

  for i in range(len(balls)):
    for j in range(i+1,len(balls)):
      balls[i].handleCollision ( balls[j] )

  for ball in balls:
    ball.updategraphic()


    
