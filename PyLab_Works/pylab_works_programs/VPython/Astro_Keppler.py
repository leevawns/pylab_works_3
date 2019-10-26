#Kepler's Laws.py
# plots the orbit of a planet in an eccentric orbit to illustrate
# the sweeping out of equal areas in equal times, with sun at focus
# The eccentricity of the orbit is random and determined by the initial velocity
# program uses normalised units (G =1)
# program by Peter Borcherds, University of Birmingham, England
   
from visual import *             
from random import random    
 
steps = 10
dt = 0.5 / float(steps)
step = 0
ccolor = color.white
time = 0

def MonthStep(time, offset = 20, whole = 1): # mark the end of each "month"
  global ccolor   # have to make it global, since label uses it before it is updated
  if whole :
    Ltext = str(int(time *2 + dt))  #end of 'month', printing twice time gives about 12 'months' in 'year'
  else:
    Ltext =  duration + str ( time * 2 ) + \
      ' "months"\n Initial speed: ' + str(round(speed, 3))
    ccolor = color.white
  #print 'LT',Ltext
  label ( pos = planet.pos, text = Ltext, color= ccolor,
    xoffset = offset * planet.pos.x, yoffset = offset * planet.pos.y)
  ccolor = (0.5*(1+random()),random(),random())   #randomise colour of radial vector
  return ccolor

#scene = display(title = "Kepler's law of equal areas", width=1000, height=1000, range=3.2)
#scene = display(width=1000, height=1000, range=3.2)
scene.range = 3.2
scene.userspin = False 
duration = 'Period: '
sun = sphere(color = color.yellow, radius = 0.1)    # motion of sun is ignored (or centre of mass coordinates)
scale = 1.0
poss = vector(0,scale,0)
planet = sphere(pos = poss, color = color.cyan, radius = 0.02)

Finished = True
#**************************************************
def Init ( Vx = None ):
  global Finished, oldpos, speed, time, velocity

  if not ( Finished ) :
    return
  if not ( Vx ) :
    Vx = 0.7 + 0.5 *random()
  velocity = -vector ( Vx, 0, 0 )
  speed    = mag ( velocity )
  oldpos   = vector ( planet.pos )
  ccolor   = MonthStep ( time )
  curve ( pos = [ sun.pos, planet.pos ], color = ccolor )
  time = 0
  step = 0

  MonthStep ( time, 50, 0 )
  for obj in scene.objects:
    if obj is sun or obj is planet:
      continue
    obj.visible = 0
  label ( yoffset = 100 ,
          text = 'Intial Velocity = ' + str ( round ( Vx, 3 ) ) )

  time = 0
  step = 0
  Finished = False

#**************************************************
def _On_Draw ( Value ) :
  global Slider_Value
  Init ( Slider_Value )

#**************************************************
def _On_Random ( Value ) :
  Init ()

#**************************************************
Slider_Value = 0.984
def _On_Set_Slider ( Value ) :
  global Slider_Value
  Slider_Value = Value

#**************************************************
VPC.Define ( 2, 1, 1 )
VPC.Set_Button ( 0, 'Random', _On_Random )
VPC.Set_Button ( 1, 'Draw', _On_Draw )
VPC.Set_Text   ( 0, 'Click for a random orbit.', _On_Random )
VPC.Set_Slider ( 0, 'Start Velocity', 0.7, 1.2, 0.984, 'Lin', '%5.2f', _On_Set_Slider )

Init()
Forward_Up ( None, None, 5 )

while True :
  rate ( 50 )
  if not (Finished) and not( ( oldpos.x > 0 ) and ( planet.pos.x < 0 ) ) :
    time += dt
    oldpos = vector ( planet.pos )  # construction vector(planet.pos) makes oldpos a varible in its own right
                                    # oldpos = planet.pos makes "oldposs" point to "planet.pos"
                                    # oldposs = planet.pos[:] does not work, because vector does not permit slicing
    denom = mag(planet.pos) ** 3
    velocity -= planet.pos * dt /denom  #inverse square law; force points toward sun
    planet.pos += velocity * dt

    # plot orbit
    curve(pos =[oldpos, planet.pos], color = color.red)

    step += 1
    if step == steps:
      step = 0
      ccolor = MonthStep(time)
      curve(pos=[sun.pos, planet.pos], color = color.white)
    else:
      #plot radius vector
      curve(pos=[sun.pos, planet.pos], color = ccolor)

  else :
    # remove all clicks received during drawing
    if not ( Finished ) :
      if scene.mouse.clicked > 0 :
        while scene.mouse.clicked > 0 :
          scene.mouse.getclick()
      Finished = True
      #label ( pos = ( 0, 2.5, 0 ), text = 'Click for another orbit' )

    # wait for click to start next one
    else :
      if scene.mouse.clicked > 0 :
        while scene.mouse.clicked > 0 :
          scene.mouse.getclick()
        Init ()
        """
        MonthStep(time, 50, 0)
        for obj in scene.objects:
          if obj is sun or obj is planet: continue
          obj.visible = 0  # clear the screen to do it again
        """