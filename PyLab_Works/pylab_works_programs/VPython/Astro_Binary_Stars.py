from visual import *

#import __init__
#from visual_support import *
Coordinate_Axis ( 2 ) 

#=============================================================
# This program visualizes the orbits of two stars (Binary stars).
# We use scaled variables. If alpha = G*m1*m2, a = major semiaxis
# of the ellipse of m2 around m1, and e = excentricity of that
# ellipse, we rescale the distance r between the stars and
# the time by: r->r/a, t->t*sqrt(alpha/mu*a^3), where mu is the
# reduced mass. The equations of motion for the relative position
# of m2 with respect to m1 are, in the rescaled variables are:
# 
#  r_dot_dot = -1/r^2+(1-e^2)/r^3  and phi_dot = sqrt(1-e^2)/r^2
#
# with initial conditions: r = 1-e, r_dot = 0, phi = 0.
# With the rescaled variables the period of the orbit is 2*pi.
# The program uses a very rudimentary midpoint solver for the
# equations of motion, but good enough for this demo.
# It only computes one cycle and then repeats it, to avoid drift.
#
# Change the value of e and the masses to get different orbits,
# with e = 0 to get the circle.
#
# ** Right and mid click the mouse to rotate and zoom **
# ** Left click to toggle a line joining the two stars **
# ** To exit the program press ESC **
#
# by E. Velasco. November 2004
#=============================================================

# Constants and initial data
e = 0.75       # Excentricity, 0 for circular orbit
m1 = 1.0       # Use this as the reference mass
m2 = 0.5

r = 1-e              # Start with m2 in its perihelion
r_dot = 0.0
phi = 0

R  = vector(r,0,0)   # Relative position vector
R1 = -m2/(m1+m2)*R   # Position vector of m1 from CM
R2 = m1/(m1+m2)*R    # Position vector of m2 from CM

fr = 1-e**2
fphi = sqrt(fr) 

if m2/(m1+m2)>= m1/(m1+m2):
    span = 1.2*(1+e)*m2/(m1+m2)
else:
    span= 1.2*(1+e)*m1/(m1+m2)
 
Info = (e,m1/m2)
     
# Time variable and increments
Npoints = 800         # Points in a period
Npoints = 300
dt = 2*pi/Npoints     # Full time step
dt2 =  pi/Npoints     # Half time step           

# Color definitions
CStar1  = color.yellow
CStar2  = color.cyan

CLz = color.red
CLine = color.red

# First define the properties of the display window 
#window = display(title="Binary Stars", width=800, height=600)
#window.fullscreen = 1          # Change to 0 to get a floating window
window = scene

Forward_Up ( ( 0, 3, -1 ), ( 0, 0, 1 ), -4 )
print 'Cam / For2 = ', scene.mouse.camera, scene.forward 
#import time
#time.sleep ( 0.1 )
#a = scene.mouse.camera [1] / -4.0
#s = scene.scale [0]
#a = a * s
#scene.scale = vector ( a, a, a )


#window.range = (span*1.65,span*1.65,span*1.65)
window.lights = [ vector ( 0, 0, 0.5 ) ]
window.ambient = 0.6                    
#window.select()  

 
label(text = "e = %.2f    m1/m2 = %.2f" % Info, 
  pos=(0,-span*0.9,0),
  color = ( 1,0,0 ),
  opacity = 0 )

# The Stars and their orbits
Star1 = sphere(pos=R1, radius=0.03*span, color=CStar1)
Star1.orbit = curve(color=CStar1, radius=0, pos=[Star1.pos])

Star2 = sphere(pos=R2, radius=0.03*span*(m2/m1)**(1/3), color=CStar2)
Star2.orbit = curve(color=CStar2, radius=0, pos=[Star2.pos])

# Draw horizontal plane z=0 
plane = curve( pos=[(-span,-span),(-span,span),(span,span),
              (span,-span),(-span,-span)], color=CLz)

# Create the Angular Momentum (Lz) vector and line joining the two stars
Lz = arrow( pos=(0,0,0), axis=(0,0,0.6*span), shaftwidth=0.02, color=CLz )
Line = curve(color=CLine, radius=0, pos=[])
ShowLine=0

# The main loop
step = 0
DrawOrbit = True

while 1:
    rate(150)

    if scene.kb.keys: # is there an event waiting to be processed?
      s = scene.kb.getkey() # obtain keyboard information
      print 'Cam / For = ', scene.mouse.camera, scene.forward,scene.scale
      if s == 'a' :
        a = scene.mouse.camera [1] / -4.0
        S = scene.scale[0]
        a = a * S
        scene.scale = vector( a,a,a)
        print 'Cam / For = ', a, scene.mouse.camera, scene.forward,scene.scale

    # mid point variables
    r_mid = r+ r_dot*dt2
    r_dot_mid = r_dot+(-1/r**2+fr/r**3)*dt2
  
    # full step varibles
    r = r + r_dot_mid*dt
    r_dot = r_dot+(-1/r_mid**2+fr/r_mid**3)*dt
    phi = phi + (fphi/r_mid**2)*dt  
    
    # Update position of object
    if step == Npoints:     # Completed period. Start again at initial point
        DrawOrbit = False   # Do not draw the orbit again!
        step=0
        r = 1-e
        r_dot = 0
        phi = 0
        
    R=vector(r*cos(phi),r*sin(phi),0)
    Star1.pos = -m2/(m1+m2)*R
    Star2.pos = m1/(m1+m2)*R
    if DrawOrbit == True:
        Star1.orbit.append(pos=Star1.pos)
        Star2.orbit.append(pos=Star2.pos)

    # Toggle line joining the two stars with left mouse
    if window.mouse.clicked:
        ShowLine = 1-ShowLine
        window.mouse.getclick()  # Empty the mouse queue

    if ShowLine == 1:
        Line.pos=[Star1.pos,Star2.pos]
    else:
        Line.pos=[]
               
    step=step+1
    
