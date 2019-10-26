#  Hit any key (except 'q') to pause/unpause, drag the slider to change the acceleration
#     voltage.  'q'fff will quit.
#
#  Aaron J. Miller, ajmiller@albion.edu
#  http://www.albion.edu/physics/ajmiller/VPython
# 
 
#from __future__ import division
from visual import *
from visual.controls import *
from random import random, uniform
from math import *
import time

# make a random vector of various scales in x, y, z
def randvec(x,y,z):
    return vector(x*(random()-0.5),y*(random()-0.5),z*(random()-0.5))

# Define a constant electric field between the electrodes and an opposing field
#   between the counter and the collector plate
def Efield(Egrid,Ecounter,xg,x):
    return vector((x<xg)*Egrid + (x>xg)*Ecounter,0,0)

# make a fancy grid electrode out of cylinders
def drawgrid(xg, nbars=10, width=1, barfill=0.25, color=color.white):
    minx = -width/2
    maxx = width/2
    dx = (maxx - minx)/(nbars-1)
    gridcol=color
    gridr = dx*barfill/2
    for x in arange(minx, maxx+dx, dx):
        cylinder(pos=(xg,x,minx), axis=(0,0,maxx-minx),radius = gridr, color=gridcol)
        cylinder(pos=(xg,minx,x), axis=(0,maxx-minx,0),radius = gridr, color=gridcol)
    # round the corners of the grid, just for fun    
    sphere(pos=(xg,minx,minx),color=gridcol, radius=gridr)
    sphere(pos=(xg,minx,maxx),color=gridcol, radius=gridr)
    sphere(pos=(xg,maxx,minx),color=gridcol, radius=gridr)
    sphere(pos=(xg,maxx,maxx),color=gridcol, radius=gridr)

# calling function for the slider control
def setbias(voltage):
  global Egrid
  Egrid = -voltage/grid_distance
  vlabel.text="V = %1.2f"%(voltage)
  #scene.width = 50

# this is called to "reset" an electron once it is absorbed or lost off screen
def reset(elec):
   elec.vel=initial_speed/sqrt(3)*randvec(1,1,1)
   elec.pos=vector(pos0)
   elec.y=uniform(-plate_radius,plate_radius)  # randomly spaced in y
   elec.z=uniform(-filament_radius,filament_radius) # randomly spaced in y
   elec.charge=0  # set a charge attribute to zero until the electron is "emitted"
   elec.color = elec_color
   elec.visible=False

# set up the geometry
cavity_length = 0.3  # m
plate_thick = cavity_length/80
plate_radius = cavity_length/5 
filament_radius = plate_radius/4

#set up the voltages and positions of the metal plates
grid_distance = cavity_length * 4/5
counter_distance = cavity_length - grid_distance

grid_V = 1.0  # initial grid voltage
Egrid = -grid_V/grid_distance
counter_V = -1.5  # relative to grid voltage
Ecounter = -counter_V/counter_distance
counter_flash_duration = 5  # visually highlight when an electron is "counted" by counter
counter_color_dark = (0.5,0,0)  # "natural" state of the counter electrode
counter_color_bright = (1,0.5,0.5) # highlight the electrode this color when an e is counted

xf=-cavity_length/2-counter_distance
x0=-cavity_length/2
xg=x0+grid_distance
xc=cavity_length/2
gridmin = xg-plate_thick/2
gridmax = xg+plate_thick/2

# electron properties
elec_color = color.green
elec_radius = plate_radius/15
N_elec = 150  # number of electrons to simulate

# atomic emission properties
emitcolor = color.yellow  # display a flash of light
emitradius = 3*elec_radius

# general constants
qe = -1.6e-19 # e
mass = 9.11e-31 # kg
E_gas = 2.5  # eV, delta E from n=1 to n=2 for the gas
K_max = E_gas*1.6e-19  # J,  kinetic energy threshold before ionization
v_max = sqrt(K_max/2/mass)  # max speed of electrons before exciting the atoms

# build the electron properties
pos0 = (xf+filament_radius,0,0) # initial (x,y,z) position
v0 = (0,0,0) # initial (vx,vy,vz)
elecs = []  # initialize an array to keep track of the electrons
p_capture = 0.4 # probability of being absorbed by the grid (per dt)
p_emit = 0.003 # probability of being emitted (per dt)
initial_speed = 2e5 # m/s, randomize the electron speed up to this value

# make the atom properties
atoms = []  # an array to keep track of excited atoms
life = 20  # number of loop iterations to show the atom as "lit up"

### Ok, everything is set up... let's start drawing things!

#Set up the display and control window
#scene = display(x=120, y=0, title='Franck Hertz Simulation',width=900, height=700,background=color.black)
#scene.center = (-0.015,0,0)


#************************************************************
#cw = controls(x=0, y=0, width=50, height=200, range=60)
#vslide = slider(pos=(0,-50), width=7, length=100, axis=(0,1,0),
#                min=1.0, max=12.0, action=lambda: setbias(vslide.value))
#
VPC.Define ( 0, 1 ) 
VPC.Set_Slider ( 0, 'Voltage', 1, 12, 2, 'lin', '%5.1f', setbias )
#************************************************************


vlabel=label(pos=(0,-1.5*plate_radius,1.5*plate_radius),text="V = %1.2f"%(grid_V), height = 30)



# make the cathode, counter, and counter electrode
counter = box(pos=(xc,0,0),length=plate_thick, width=plate_radius*2, height=plate_radius*2,
         color=counter_color_dark,opacity=0.5)
drawgrid(xg, nbars=10, width=2*plate_radius, barfill=0.25, color=color.yellow)
drawgrid(x0, nbars=10, width=2*plate_radius, barfill=0.25, color=(0,0.7,1))

# draw a coiled filament
helix(pos=(xf,-plate_radius,0), axis=(0,plate_radius*2,0),
      radius=filament_radius,thickness=plate_radius/10, color=color.yellow)

   
for elecnum in range(1,N_elec+1):
  newelec=sphere(pos=pos0, radius=elec_radius, color=elec_color)
  reset(newelec)
  newelec.m=mass
  elecs.append(newelec)

scene.autoscale=0
#scene.range=0.24
Forward_Up ( None, None, 0.4 )
fps=100 # maximum frames per second
dt=1.5e-9 # set this as our time step for the simulation
dt *= 2

counter_flash=counter_flash_duration

exitloop=False
while True :
  rate ( 50 )
  k=0
  for elec in elecs:
    if elec.charge == 0:
      val=random()<p_emit
      elec.charge = val*qe        
      elec.visible = val
    else:
      F=Efield(Egrid,Ecounter,xg,elec.x)*elec.charge
      elec.vel+=F/elec.m*dt
      elec.pos+=elec.vel*dt
      K = 0.5*elec.m*elec.vel.mag**2
      if K > K_max:
        elec.vel = vector(0,0,0)
        atom = sphere(pos=elec.pos,color=emitcolor,radius=emitradius)
        atom.life=life
        atoms.append(atom)

      if (elec.x>gridmin and elec.x<gridmax):
        if random()<p_capture: # capture the electron at grid
          reset(elec)
      elif elec.x>(xc-plate_thick): # count the electron
        counter.color=counter_color_bright
        counter_flash=counter_flash_duration
        reset(elec)
      elif  abs(elec.y)>plate_radius or abs(elec.z)>plate_radius:
        reset(elec)

  for atom in atoms:
    if atom.life<1:
      atom.visible=False
      atoms.remove(atom)
      del(atom)
    else:
      atom.life-=1
      atom.radius=emitradius*atom.life/life            

  if counter_flash<1:
    counter.color=counter_color_dark
  else:
    counter_flash-=1

  #********************************************************
  #cw.interact() # check for events, drive actions; must be executed repeatedly in a loop
  #if VPC.modified :
    
  #********************************************************


