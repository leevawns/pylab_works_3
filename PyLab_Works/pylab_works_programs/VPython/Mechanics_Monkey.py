# The classic Shoot-the-Monkey Demo
# John W. Keck, February 2003
# American University
# Modified by Stef Mientki

from visual import *

sys.path.append ( '../../../support')
from visual_support import *


# ****************************************************************************
# ****************************************************************************
mkcolor = ( 0.46, 0.28, 0.10)

g   = 9.84
dim = 40
v0  = dim / 2
dt  = 0.01
ball_pos0 = vector ( -dim / 2, 5, 0 ) # start ball position


# ****************************************************************************
# ****************************************************************************
def Build_Scene ():
  global aim, ball, bal_pos0, branch, cx, cy
  global mkcolor, mkpos, monkey, monkey1, monkey2
  global power1, pwr, tree, vel, vel2

  #set up the environment
  floor  = box (pos=(0,0,0), size=(300,0.5,6), color=color.green, opacity=0.5)  #length=110, height=0.5, width=6, color=color.green)
  tree   = cylinder(pos=(0.9*dim,0,0), axis=(0,dim,0), radius=3, color=(0.7,0.7,0.3))
  branch = cylinder(pos=(0.9*dim,dim-17,0), axis=(-12,30,0), radius=2, color=(0.7,0.7,0.3))

  #the monkey
  monkey = frame()
  monkey1 = sphere(frame=monkey, pos=(1,0,0),radius=2,color=mkcolor) #head
  sphere(frame=monkey, pos=(0.6,0,-1.9),radius=1.2,color=(1,0.8,0.5))
  #snout
  sphere(frame=monkey, pos=(1.5,0.12,-2.3),radius=0.2,color=color.black)
  #nostrils
  sphere(frame=monkey, pos=(1.5,-0.12,-2.3),radius=0.2,color=color.black)
  ring(frame=monkey, pos=(0.7,0,-2.2),axis=(2,0,-1),radius=0.9,thickness=0.2,color=color.black) # mouth
  eang0 = 65*pi/180
  eang1 = 20*pi/180
  sphere(frame=monkey, pos=(1+1.5*cos(eang0),1.5*sin(eang0)*sin(eang1),-1.5*sin(eang0)*cos(eang1)),radius=0.6,color=(0.9,0.9,0.9))
  #eyes
  sphere(frame=monkey, pos=(1+1.5*cos(eang0),-1.5*sin(eang0)*sin(eang1),-1.5*sin(eang0)*cos(eang1)),radius=0.6,color=(0.9,0.9,0.9))
  #eyes
  eang0 = 67*pi/180
  eang1 = 19*pi/180
  sphere(frame=monkey, pos=(1+2.02*cos(eang0),2.02*sin(eang0)*sin(eang1),-2.02*sin(eang0)*cos(eang1)),radius=0.2,color=color.black)
  #eyes
  sphere(frame=monkey, pos=(1+2.02*cos(eang0),-2.02*sin(eang0)*sin(eang1),-2.02*sin(eang0)*cos(eang1)),radius=0.2,color=color.black)
  monkey2 = cylinder(frame=monkey, pos=(-6,0,0), axis=(5,0,0), radius=2, color=mkcolor) #body

  monkey.axis  = (0,1,0)
  monkey.mass  = 5

  #the ball
  ball = sphere ( pos=ball_pos0, radius=5, color=(0.4,0.9,1))
  ball.mass = 1

  # take aim
  aim = curve(pos=[ball.pos,monkey.pos+monkey.axis], color=(0.9,0.7,0.7))
  vel2 = cylinder(pos=ball.pos, radius=1, color=color.yellow, opacity=0.9)
  vel  = arrow   (pos=ball.pos, shaftwidth=2, fixedwidth=1, color=color.yellow)


# ****************************************************************************
# ****************************************************************************
def Rebuild () :
  """
  The following parameters determine the whole scene
    - tree.pos.x
    - tree.axis.y
    - ball.pos.x
    - v0
  """
  global aim, ball, ball_pos0, branch, monkey, v0, vel

  ball.radius    = 3
  vel.visible    = True
  vel2.visible   = True

  ball.pos      = ball_pos0
  ball.velocity = vector(0,0,0)
  ball.trail    = curve ( color = ball.color )

  branch.pos = ( tree.x,      tree.axis.y - 17, 0 )
  monkey.pos = ( tree.x - 13, tree.axis.y,      0 )
  monkey.velocity = vector(0,0,0)

  aim.pos  = [ ball.pos, monkey.pos + monkey.axis ]

  vel.pos  = ball.pos
  vel.axis = v0 * norm ( monkey.pos - ball.pos)
  
  vel2.pos  = vel.pos
  vel2.axis = ( v0 - 4 ) * norm ( monkey.pos - ball.pos)

  #print tree.axis.y

# ****************************************************************************

a = 50
scene.background = (0.6,0.6,0.6)
scene.center = ( 0, a-10, 0 )
scene.range  = ( a, a, a )
scene.userspin = False
scene.userzoom = False
scene.autoscale = False
#Coordinate_Axis ( 100 )
#Forward_Up ( None, None , 300 )

Build_Scene ()


Rebuild ()
State = 0

Drag = False
Drag_Controls = [ ball, branch, monkey1, monkey2, tree, vel2 ]

while True :
  rate ( 50 )

  # ****************************************************
  # ****************************************************
  if State == 0 :

    # ****************************************************
    # ****************************************************
    if scene.mouse.clicked:
      while scene.mouse.clicked:
        scene.mouse.getclick()
      if scene.mouse.events :
        scene.mouse.getevent()
      State = 1

    # ****************************************************
    # It's not possible to detect Ctrl-Alt-Shift changes
    # ****************************************************
    if scene.mouse.events :
      m = scene.mouse.getevent()
      if m.press and ( m.button == 'left' ) :
        if m.pick in Drag_Controls :
          Drag_Object  = m.pick
          Drag         = True
          Drag_Pos     = scene.mouse.project ( normal = (0,0,1) )

      elif m.drop :
        Drag   = False

    # ****************************************************
    if Drag :
      New_Pos = scene.mouse.project ( normal = (0,0,1) )
      if New_Pos != Drag_Pos :
        if Drag_Object == ball :
          ball_pos0.x  += ( New_Pos - Drag_Pos ).x

        elif Drag_Object == vel2 :
          v0 = mag ( vel.axis + New_Pos - Drag_Pos )

        elif Drag_Object in  ( branch, tree, monkey1, monkey2 ) :
          tree.x  += (New_Pos - Drag_Pos).x
          tree.axis.y += (New_Pos - Drag_Pos).y

        Drag_Pos = New_Pos
      Rebuild ()

  # ****************************************************
  # ****************************************************
  elif State == 1 :
    ball.radius  = 1
    vel.visible  = False
    vel2.visible = False
    
    State = 2
    hit = False
    dist = mag ( ball.pos - monkey.pos )
    cx = ( monkey.x - ball.x ) / dist
    cy = ( monkey.y - ball.y ) / dist
    ball.velocity = 4 * v0 * vector ( cx, cy, 0 )

  # ****************************************************
  # ****************************************************
  elif State == 3 :
    if scene.mouse.clicked:
      while scene.mouse.clicked:
        scene.mouse.getclick ()
      Rebuild ()
      State = 0

  # ****************************************************
  # ****************************************************
  elif State == 2 :
    ball.velocity.y -= g * dt
    ball.pos        += ball.velocity * dt
    if ball.y < 0 :
      ball.y = 0
      ball.velocity = vector ( 0, 0, 0 )
    monkey.velocity.y -= g * dt
    monkey.pos        += monkey.velocity * dt

    if monkey.x > tree.x - tree.radius - 1 :
      ball.velocity.x = -0.8 * ball.velocity.x
      
    if ( monkey.y <= 6 ) and \
       ( ball.y   <= 2 ) :
      if scene.mouse.clicked:
        while scene.mouse.clicked:
          scene.mouse.getclick ()
      State = 3

    # leave trails and show ball's velocity vector
    ball.trail.append ( pos = ball.pos )

    # monkey-ball collision
    if not ( hit ) and \
       (ball.x > monkey.x-2 and ball.x < monkey.x+2) and \
       (ball.y > monkey.y-5 and ball.y < monkey.y+2):
      relvel = mag ( monkey.velocity - ball.velocity )

      # perfectly inelastic collision
      masstot = ball.mass + monkey.mass
      ball.velocity.x = (ball.mass*ball.velocity.x + monkey.mass*monkey.velocity.x)/masstot
      ball.velocity.y = (ball.mass*ball.velocity.y + monkey.mass*monkey.velocity.y)/masstot
      monkey.velocity = ball.velocity
      hit = True

