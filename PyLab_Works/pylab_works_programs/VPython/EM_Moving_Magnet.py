from __future__ import division
from visual import *

# Faraday's Law: bar magnet moves at constant velocity, then briefly comes to rest and reverses

# Ruth Chabay 2007-08-07
# Revised Bruce Sherwood 2007-11-10

# Choose whether to show a ring or a disk through which passes magnetic flux
# Choose whether to show B at many places, not just in flux region
# Magenta arrow represents the vector dB_vec/dt

showring  = True # show ring if True, disk if False
showallB  = True # if True, show B at many places, not just within circle
showE     = True  # show E along ring if True
show_dBdt = True  # show magenta arrow for dB/dt

scene.background = color.white
scene.lights = [0.7*norm(vector(1,0,.5)), 0.7*norm(vector(-1,0.5,0.5))]
Bcolor = (0,.5,.5)
Bcolorother = (.8,1,1)
sw = 0.01
swother = 0.005

def Bfield(source,obsloc):
    r = source-obsloc
    return kmag*(3*dot(mu,norm(r))*norm(r) - mu)/mag(r)**3

def showB():
  for arr in Bother:
    arr.axis=Bscale*Bfield(magnet.pos, arr.pos)
    arr.visible = True

xhat = vector(1,0,0)

Rdisk = 0.3
f = cos(pi/4.)
rmagnet = 0.03
Lmagnet = 0.12
dpole = 0.03
magnet = frame(pos=(0,0,0))
south = cylinder(frame=magnet, pos=(-Lmagnet/2,0,0), radius=rmagnet, color = (0,0,1),
              axis=(dpole,0,0))
north = cylinder(frame=magnet, pos=(Lmagnet/2,0,0), radius=rmagnet, color = (1,0,0),
              axis=(-dpole,0,0))
bar = cylinder(frame=magnet, pos=south.pos+vector(dpole,0,0), radius=south.radius,
                  axis = north.pos-vector(dpole,0,0)-south.pos-vector(dpole,0,0), color=(0.7,0.7,0.7))

surface1 = ring(pos=vector(0.4,0,0), radius=Rdisk, thickness=0.001)
surface1.center = surface1.pos
surface2 = cylinder(pos=vector(0.4,0,0), radius=Rdisk, axis=(0.002,0,0), color=(0.8,0.8,0.8))
surface2.center = surface2.pos+surface2.axis/2
surface = surface1
surface2.visible = False

deltax = Lmagnet/5
kmag = 1e-7
mu = vector(1.0,0,0) # magnetic dipole moment of bar magnet

#B = Bfield(magnet.pos, surface.pos) # typical 2e-6 tesla

Bscale = 0.13*Rdisk/2e-6
Escale = 0.7*Rdisk/2e-7
xmax = 0.4*Rdisk

#E on perimeter of surface
Earr=[]
for theta in arange(0,2*pi,pi/6):
    a=arrow(pos=(surface.center.x, surface.radius*cos(theta),surface.radius*sin(theta)),
                           axis=(0,0,0), color=color.orange, shaftwidth=.01)
    a.vv = norm(a.pos - surface.pos)
    a.visible = showE
    Earr.append(a)

Bsurface = []  ## arrows on surface at which to calculate field, flux
dR = 0.2*Rdisk
for y in arange(-0.8*Rdisk,0.9*Rdisk,dR):
    a = arrow(pos=(surface.center.x, y, 0),axis=(0,0,0),
              color=Bcolor, fixedwidth=1, shaftwidth=sw)
    Bsurface.append(a)

## locations at which to display magnetic field around magnet
Bother = []
dtheta = pi/6
phi = pi/4
for theta in arange(dtheta, pi-dtheta/2, dtheta):
    x = Rdisk*cos(theta)
    y = Rdisk*sin(theta)
    z = 0
    Bother.append( arrow(pos=(x,y,z), axis=(0,0,0)) )
    Bother.append( arrow(pos=(x,-y,z), axis=(0,0,0)) )
    Bother.append( arrow(pos=(x,z,y), axis=(0,0,0)) )
    Bother.append( arrow(pos=(x,z-y), axis=(0,0,0)) )
    Bother.append( arrow(pos=(x,y,z), axis=(0,0,0)) )
    Bother.append( arrow(pos=(x,y,z), axis=(0,0,0)) )
    Bother.append( arrow(pos=(x,y,z), axis=(0,0,0)) )
    Bother.append( arrow(pos=(x,y,z), axis=(0,0,0)) )
    Bother.append( arrow(pos=(x,y,z), axis=(0,0,0)) )

    a = vector(x,y,z)
    b = rotate(a,angle=phi, axis=(1,0,0))
    Bother.append( arrow(pos=(b.x,b.y,b.z), axis=(0,0,0)) )
    Bother.append( arrow(pos=(b.x,-b.y,b.z), axis=(0,0,0)) )
    b = rotate(a, angle=3*phi, axis=(1,0,0))
    Bother.append( arrow(pos=(b.x,b.y,b.z), axis=(0,0,0)) )
    Bother.append( arrow(pos=(b.x,-b.y,b.z), axis=(0,0,0)) )

for arr in Bother:
    arr.color = Bcolorother
    arr.shaftwidth = swother
    arr.fixedwidth = 1

scene.center = surface.pos/2
scene.autoscale = 0
Forward_Up ( -vector(1,0,2.5), None, 1 )

flux = 0
dt = 0.01
dt = 0.02
t = 0
vx = v0 = 0.1
dBdtarr = arrow(pos=surface.pos+vector(0,-0.1*Rdisk,0.2*Rdisk), axis=(0,0,0), color=color.magenta,
                fixedwidth=1, shaftwidth=sw)

# *************************************************
# *************************************************
def Toggle_Surface ( Value = None ):
  global surface, showring
  surface.visible = False
  showring = not ( showring )
  if showring:
    surface = surface1
  else:
    surface = surface2
  surface.visible = True

# *************************************************
# *************************************************
def Toggle_All_B ( Value = None ) :
  global Bother, showallB
  showallB = not ( showallB )
  if not ( showallB ) :
    for arr in Bother:
      arr.visible = False

# *************************************************
# *************************************************
def Toggle_Show_E ( Value = None ) :
  global showE, Earr
  showE = not ( showE )
  for E in Earr :
    E.visible = showE

# *************************************************
# *************************************************
def Toggle_dBdt ( Value = None ) :
  global dBdtarr, show_dBdt
  show_dBdt = not ( show_dBdt )
  dBdtarr.visible = show_dBdt


# *************************************************
# Define Control Buttons
# *************************************************
VPC.Define ( 4 )
VPC.Set_Button ( 0, 'All B',      Toggle_All_B   )
VPC.Set_Button ( 1, 'Show dB/dt', Toggle_dBdt    )
VPC.Set_Button ( 2, 'Surface',    Toggle_Surface )
VPC.Set_Button ( 3, 'Show E',     Toggle_Show_E  )


# *************************************************
# Main Loop
# *************************************************
while 1:
    #rate(1/dt)
    rate ( 50 )
    t = t + dt
    if abs(magnet.pos.x+vx*dt) > 0.7*xmax:
        if magnet.pos.x > 0:
            ax = -0.2
        else:
            ax = 0.2
    else:
        ax = 0
        if vx > 0:
            vx = v0
        else:
            vx = -v0
    vx += ax*dt
    magnet.pos.x += vx*dt
    if showallB:
      showB()
    oldflux = flux
    flux = 0
    for arr in Bsurface:
        B = Bfield(magnet.pos, arr.pos)
        arr.axis = B*Bscale
        flux += dot(B,xhat)*pi*abs(arr.y)*dR # 2 B's per y
    dflux = flux - oldflux
    dBdtarr.axis = (0.15*dflux/1e-8,0,0)
    E = (dflux/dt)/(2*pi*surface.radius)
    for a in Earr:
        a.axis = -E*Escale*cross(xhat,a.vv)
    

