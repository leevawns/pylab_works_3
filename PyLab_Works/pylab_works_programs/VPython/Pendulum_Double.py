#--------------------------------------------------------
# Demo of the motion of a double pendulum.
# It uses a crude mid point numerical integration of
# the equations of motion, but good enough for this demo.
#
# Left mouse toggles the display of the trail of the
# orbit of the second mass.
#
# Right mouse toggles the fast/slow motion display.
#
# Center mouse button (or left+right) zooms the view.
#
# ** To exit press ESC **
#
# by E. Velasco. September 2005
#---------------------------------------------------------
from visual import *

# Initial conditions
theta = 90.0*(pi/180.0)
phi = -90.0*(pi/180.0)
theta_dot = 0.0
phi_dot = 0.0

# Constants and time step
L1 = 1.0
L2 = 1.0
M1 = 1.0
M2 = 1.0
g = 9.8

#Dt = 0.002*sqrt(L1/g)   # Full time step
Dt = 0.02*sqrt(L1/g)   # Full time step
Dt2 = Dt/2.0            # Midpoint time step
 
Q = vector(0,(L1+L2)/2.0)  # Position of fixed point
R=(L1+L2)/16.0          # Radius of bobs
Rs = R/4.5              # Radius of strings
RQ = R/2.0              # Radius of fixed point
CFixed = color.red      # Color of fixed point
Cbob   = color.yellow
Cstring = color.cyan
Corbit = color.green
ShowOrbit = False

m = M2/M1
L = L2/L1
g = g/L1

def GetPosition(theta,phi):
    x1=L1*sin(theta)+Q[0]
    y1=L1*cos(theta)-Q[1]
    x2=x1-L2*sin(phi)
    y2=y1+L2*cos(phi)
    return (x1,-y1, x2,-y2)

def F(theta, phi, theta_dot, phi_dot):
    sn=sin(theta+phi)
    cn=cos(theta+phi)
    A = m*L*sn*phi_dot**2+(1+m)*g*sin(theta)
    B = sn*theta_dot**2+g*sin(phi)
    C = 1+m*sn*sn
    F1 = (-A-m*cn*B)/C
    F2 = (-cn*A-(1+m)*B)/(L*C)
    return (F1,F2)
    
def E(theta, phi, theta_dot, phi_dot):
    En = 0.5*(M1+M2)*(L1*theta_dot)**2+0.5*M2*((L2*phi_dot)**2-
         2*L1*L2*phi_dot*theta_dot*cos(phi+theta))-(M1+M2)*L1**2*g*cos(theta)-\
         M2*L1*L2*g*cos(phi)
    return En

# Properties of the display window 
#window = display(title="Double Pendulum", width=800, height=600)
window = scene
#window.fullscreen = 1      # Change to 0 to get a floating window
window.center = ( 0, 0, 0 )
#window.forward = ( 0, 0, -1 )
label ( pos = ( 0, 1.5, 0 ), text= 'Click to toggle trace' )
#window.cursor.visible = 0  # Hide the mouse

window.userspin = 0        # No rotation with mouse
window.autoscale = False
window.autocenter = False
#window.range = 1.3*(L1+L2)*vector(1,1,1)
#window.forward = (0,0,-1)  # +z-axis toward you       
 
Forward_Up ( (0,0,-1), None, 4 )

# Create the double pendulum
(x1,y1, x2,y2) = GetPosition(theta,phi)

bob1 = sphere(pos=(x1,y1), radius=R, color=Cbob)
bob2 = sphere(pos=(x2,y2), radius=R, color=Cbob)
FixedP = sphere(pos=Q, radius=RQ, color= CFixed)
#print bob1

string1 = cylinder(pos=Q,axis = bob1.pos-Q, radius=Rs, color=Cstring)
string2 = cylinder(pos=bob1.pos,axis = bob2.pos-bob1.pos, radius=Rs,
                   color=Cstring)

orbit = curve(pos=[], color=Corbit)

# empty mouse queue
if scene.mouse.clicked :
  while scene.mouse.clicked  > 0 :
    scene.mouse.getclick()
    

count=5000
ShowRate=1000
# The main loop
while True :
    #rate(ShowRate)
    rate(50)
    
    ##    if count >= 5000:        # Check the value of the energy
    ##         print E(theta, phi, theta_dot, phi_dot)
    ##         count=0
    ##    else: count += 1
    
    # Compute the midpoint variables
    (F1,F2) = F(theta, phi, theta_dot, phi_dot)
    theta_m = theta+theta_dot*Dt2
    phi_m = phi+phi_dot*Dt2
    theta_dot_m = theta_dot + F1*Dt2
    phi_dot_m = phi_dot + F2*Dt2
    
    # Compute the full step variables
    (F1,F2) = F(theta_m, phi_m, theta_dot_m, phi_dot_m)
    theta += theta_dot_m*Dt
    phi += phi_dot_m*Dt
    theta_dot += F1*Dt
    phi_dot += F2*Dt
               
    # Update the loations of the bobs and the links in the string
    (x1,y1, x2,y2) = GetPosition(theta,phi)
    bob1.pos = (x1,y1)
    bob2.pos = (x2,y2)
    string1.axis = bob1.pos-Q
    string2.pos = bob1.pos
    string2.axis = bob2.pos-bob1.pos

    # Toggle painting the orbit of M2
    if window.mouse.events:
        mouseObj = window.mouse.getevent()
        window.mouse.events = 0
        if mouseObj.click == "left":   # Toggle orbit of M2
            if ShowOrbit == True:
                ShowOrbit = False
                orbit.pos=[]
            else: ShowOrbit = True
        if mouseObj.click == "right":  # Togle slow/fast display
            if ShowRate > 500: ShowRate = 300
            else:              ShowRate = 1000
            
    if ShowOrbit:
        orbit.append(pos=(x2,y2,0))
