#------------------------------------------------------------
# Demo of the free motion of a symmetric top in the reference
# frame of the center of mass (fixed at the origin).
#
# Left-click the mouse to toggle the curve of the tip of the
#    x1 moving axis.
#
# Right-click to toggle display of the angular momentum and
#    angular velocity.
#
# Center click (=left+right click) to zoom.
# 
# Press ESC to end the program.
#
# By E. Velasco, December 2004
#-------------------------------------------------------------
from visual import *

# Define the global constants
I1 = 1.0              # I1=I2 symmetric princ. moments of inertia
I3 = 2.0              # The tird principal moment of inertia
omega0 = 1.0          # positive by definition
omega3 = 1.0



Omega_p = sqrt((I1*omega0)**2+(I3*omega3)**2)/I1  # precession omega
Omega_e  = omega3*(I3-I1)/I1     # extra rotation around 3 

CosTheta = I3*omega3/sqrt((I1*omega0)**2+(I3*omega3)**2)
SinTheta = sqrt(1-CosTheta**2)

def MovingFrame(t):
    phi = Omega_p*t
    psi = pi/2-Omega_e*t
    CosPhi = cos(phi); SinPhi = sin(phi)
    CosPsi = cos(psi); SinPsi = sin(psi)
    V1 = vector(CosPhi*CosPsi-CosTheta*SinPhi*SinPsi,
                SinPhi*CosPsi+CosTheta*CosPhi*SinPsi,
                SinTheta*SinPsi)
    V3 = vector(SinTheta*SinPhi,-SinTheta*CosPhi, CosTheta)
    V2 = cross(V3,V1)
    return (V1,V2,V3)

# A function that returns a "L" in the y-z plane displaced by V
def Char_L(V):
    sz = 0.04 # size of letter
    return [V+vector(0,-sz,3*sz),V+vector(0,-sz,0), V+vector(0,sz,0)]

# Build a leter omega in the y-z plane
sz_omega  = 0.04   # size of letter
Npts = 10
alpha0=2*pi/3
Dalpha = (2*pi-alpha0)/(Npts-1)
l_omega = []
for k in range(Npts):
    alpha = alpha0+k*Dalpha
    l_omega.append(sz_omega*vector(0,cos(alpha)-1,1+sin(alpha)))
for k in range(Npts):
    alpha = pi+k*Dalpha
    l_omega.append(sz_omega*vector(0,1+cos(alpha),1+sin(alpha)))
letter_omega = array(l_omega) # Use a numeric array for efficiency

# A function that returns a omega in the y-z plane displaced by V
def Char_omega(V):
    char=array([V])+letter_omega  # Fast numeric array addition 
    return char

# Define some variables such as lenghts and time parametes
L1 = 1.0
L3 = 3.0

LF = 0.7*L3   # lenght of the moving frame axis

#Dt = 0.02/Omega_p
Dt = 0.05/Omega_p
PaintOrbit = False

# Define the colors of all the objects
CL = (1,0.4,1)          # Angular momentum
COmega = color.green    # Angular velocity
CMvFrm = color.yellow   # Moving coordinate system
CObject = (0,0.6,0.9)   # Rotating top
COrbit = (1,0.5,0.2)    # Orbit of the x1 axis

# Properties of the display window 
#window = display(title="Free Symmetric Top", width=700, height=600)
#window.fullscreen = 1      # Change to 0 to get a floating window
window = scene
window.userspin = 0        # No rotation with mouse
#window.range = (4,4,4)
#window.forward =  (-1,0,0)
#window.up = (0,0,1)        # psoitive z axis vertically up!  
window.ambient=ambient=0.3
window.lights = [0.2*norm((1,-0.5,-0.2)),0.6*norm((1,0.5,0.2))]
#window.select()
Forward_Up ( (-1,0,0), (0,0,1), 7 )

label ( yoffset = 140, line = 0, text = 'Left-Click: Toggle orbit of tip' )
label ( yoffset = 110, line = 0, text = 'Right-Click: Toggle L and w' )

Info = (I3/I1, omega3/omega0)
label(text = "I3/I1 = %.2f    w3/w0 = %.2f" % Info, pos=(0,0,-2.5),
      height=20, color=color.red, box=0)

# Define the unit vectors of the moving frame and the object at t=0
t=0
(V1,V2,V3) = MovingFrame(t)

cm = vector(0,0,0)
MvFrm1 = curve(pos=[cm,LF*V1], color=CMvFrm, radius=0.02)
MvTip1 = cone(pos=LF*V1, axis=0.1*LF*V1, radius=0.05, color=CMvFrm) 
MvFrm2 = curve(pos=[cm,LF*V2], color=CMvFrm, radius=0.02)
MvTip2 = cone(pos=LF*V2, axis=0.1*LF*V2, radius=0.05, color=CMvFrm) 
MvFrm3 = curve(pos=[cm,LF*V3], color=CMvFrm, radius=0.02)
MvTip3 = cone(pos=LF*V3, axis=0.1*LF*V3, radius=0.05, color=CMvFrm)

tip = curve(color=COrbit)
if PaintOrbit == True: tip.append(pos=MvTip1.pos+MvTip1.axis)

# Define the object: a body (ellipsoid) +2 arms (cylinders)
Body = ellipsoid(pos=cm, axis=L3*V3,
                 height=L1, width=L1, color=CObject)
Arm1 = cylinder(pos=-1.2*L1*V1, axis=2.4*L1*V1, radius=0.15*L1, color=CObject)
Arm2 = cylinder(pos=-1.2*L1*V2, axis=2.4*L1*V2, radius=0.15*L1, color=CObject)

# Create the angular momentum (L) and angular velocity (w) vectors
ShowVectors = 0  # Show L and w. 0=hide, 1=show

L_body = curve(pos=[cm,(0,0,LF)], color=CL, radius=0.02,
             visible=ShowVectors)
L_tip = cone(pos=(0,0,LF), axis=(0,0,0.1*LF), radius=0.05, color=CL,
             visible=ShowVectors)
L_label = curve(pos=Char_L(L_tip.pos+1.2*L_tip.axis), radius= 0.015,
                color=CL, visible=ShowVectors)

w = omega0*(cos(Omega_e*t)*V1+sin(Omega_e*t)*V2)+omega3*V3
w = w/mag(w)*LF
w_body = curve(pos=[cm,w], radius=0.02, color=COmega,
             visible=ShowVectors)
w_tip = cone(pos=w, axis=0.1*w, radius=0.05, color=COmega,
             visible=ShowVectors)
w_label = curve(pos=Char_omega(w_tip.pos+1.2*w_tip.axis), radius= 0.015,
                color=COmega, visible=ShowVectors) 

#main loop
                         
while True:
    #rate(125)
    rate (50)
    
    t += Dt
    (V1,V2,V3) = MovingFrame(t) # The new unit vectors

    # Update the body and the moving frame
    Body.axis=L3*V3
    Arm1.pos=-1.2*L1*V1; Arm1.axis=2.4*L1*V1
    Arm2.pos=-1.2*L1*V2; Arm2.axis=2.4*L1*V2

    MvFrm1.pos=[cm,LF*V1]
    MvTip1.pos=LF*V1; MvTip1.axis=0.1*LF*V1
    MvFrm2.pos=[cm,LF*V2]
    MvTip2.pos=LF*V2; MvTip2.axis=0.1*LF*V2
    MvFrm3.pos=[cm,LF*V3]
    MvTip3.pos=LF*V3; MvTip3.axis=0.1*LF*V3

    # Toggle Painting of orbit and the L w vectors
    if window.mouse.events:
        mouseObj = window.mouse.getevent()
        window.mouse.events = 0
        if mouseObj.click == "left":   # Toggle orbit of x1
            if PaintOrbit == True:
                PaintOrbit = False
                tip.pos=[]
            else: PaintOrbit = True
        if mouseObj.click == "right":  # Togle display of L and w
            ShowVectors = 1 - ShowVectors
            L_body.visible = ShowVectors
            L_tip.visible = ShowVectors
            L_label.visible = ShowVectors
            w_body.visible = ShowVectors
            w_tip.visible = ShowVectors
            w_label.visible = ShowVectors 

    # Paint orbit of x1 tip and the angular velocity w        
    if PaintOrbit == True:
        tip.append(pos=MvTip1.pos+MvTip1.axis)

    w = omega0*(cos(Omega_e*t)*V1+sin(Omega_e*t)*V2)+omega3*V3
    w = w/mag(w)*LF
    w_body.pos = [cm,w]
    w_tip.pos=w; w_tip.axis=0.1*w
    w_label.pos= Char_omega(w_tip.pos+1.2*w_tip.axis)
        
    
                         

    

    

    

