#-----------------------------------------------------
# Demo of a symmetric (I1=I2) gyroscope. It uses
# numerical integration with a primitive mid point
# solver of Euler's equations using the Euler angles
# [phi,theta,psi] as variables.
#
# Left mouse toggles the display of the trail of the
# orbit of the tip of the gyroscope.
#
# Right mouse toggles the display of the vectors L and
# omega (angular momentum and velocity).
#
# Center mouse button (or left+right) zooms the view.
#
# ** To exit press ESC **
#
# by E. Velasco. December 2004
#-----------------------------------------------------
from visual import *

# Initial conditions for the Euler angles
phi = 0.  
phidot = -2.6
theta = pi/4             # Must satisfy 0<theta<pi 
thetadot = 1.  
psi = 0.     
psidot = 50.             # Fast for the gyro to work 

# Constant definitions
Ulenght = 1.0        # Unit of lenght in m
Lshaft = 0.8         # length of gyroscope shaft
Rshaft = 0.03        # radius of gyroscope shaft
Hshaft = Lshaft/15.  # height of cone tip of shaft
Cshaft = (0,0.6,0.9) # Color of shaft


Rrotor = 0.38        # radius of gyroscope rotor
Drotor = 0.12        # thickness of gyroscope rotor
Lcm    = Lshaft/1.8+Hshaft  # Distance of cm to fixed point
Crotor =  (0,0.5,0.8)       # Color of rotor
Cbraces = (1,0.1,0)         # Color of braces of rotor
 
hpedestal = Lshaft   # height of pedestal
wpedestal = 0.17     # Width of pedestal
Cpedestal = (0.4,0.4,0.5)   # Color of pedestal and base
tbase = 0.05         # thickness of base
wbase = 4.*wpedestal        # width of base

Lvector = 1.05*Lshaft +2*Hshaft
CL = (1,0.4,1)         # Color of angular momentum
COmega = color.green   # Color of angular velocity
Ctrail = color.yellow  # Color of the trail of the tip of gyro
ShowVectors = 0
ShowTrail = False

# Moments of inertia divided by mass (only from rotor)
I1 = 0.25*(Rrotor**2+Drotor**2) + Lcm**2
I3 = 0.5*Rrotor**2

# Components of the angular velocity in the MOVING frame
omega1 = phidot*sin(theta)*sin(psi)+thetadot*cos(psi)
omega2 = phidot*sin(theta)*cos(psi)-thetadot*sin(psi)
omega3 = phidot*cos(theta)+psidot  # A constant of motion

gL_I = 9.8*Lcm/(I1*Ulenght)
Delta = (I3-I1)/I1*omega3

scene.userspin = 0       # No rotation with mouse
scene.ambient=0.3
scene.lights = [0.3*norm((1,-0.5,-0.2)),0.5*norm((1,0.5,0.2))]
Forward_Up ( (-1,0,0), (0,0,1), 3 ) 

label ( yoffset = 100, line = 0,
  text = 'Left-Click: Toggle orbit of tip\nRight-Click: Toggle L and w' )

# A function that returns the three moving unit vectors
def MovingFrame(phi,theta,psi):
    CosPhi = cos(phi); SinPhi = sin(phi)
    CosTheta = cos(theta); SinTheta = sin(theta)
    CosPsi = cos(psi); SinPsi = sin(psi)
    V1 = vector(CosPhi*CosPsi-CosTheta*SinPhi*SinPsi,
                SinPhi*CosPsi+CosTheta*CosPhi*SinPsi,
                SinTheta*SinPsi)
    V3 = vector(SinTheta*SinPhi,-SinTheta*CosPhi, CosTheta)
    V2 = cross(V3,V1)
    return (V1,V2,V3)

# A function that returns an L in the y-z plane displaced by V
def Char_L(V):
    sz = 0.017 # size of letter
    return [V+vector(0,-sz,3*sz),V+vector(0,-sz,0), V+vector(0,sz,0)]

# Build a leter omega in the y-z plane
sz_omega  = 0.015   # size of letter
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
 
# Get the vectors angular velocity and angular momentum in fixed frame
(V1,V2,V3) = MovingFrame(phi,theta,psi)
Omega = omega1*V1+omega2*V2+omega3*V3
L = I1*omega1*V1+I1*omega2*V2+I3*omega3*V3
OmegaScale = Lvector/mag(Omega)
LScale = Lvector/mag(L)

Omega_body = curve(pos=[(0,0,0),0.95*OmegaScale*Omega], color=COmega,
                   radius=0.01, visible=ShowVectors)
Omega_tip = cone(pos=0.95*OmegaScale*Omega, axis=0.05*OmegaScale*Omega,
                 radius=0.02, color=COmega, visible=ShowVectors)
Omega_label = curve(pos=Char_omega(1.05*OmegaScale*Omega), color=COmega,
                    radius=0.005, visible=ShowVectors)

L_body = curve(pos=[(0,0,0),0.95*LScale*L], color=CL, radius=0.01,
             visible=ShowVectors)
L_tip = cone(pos=0.95*LScale*L, axis=0.05*LScale*L, radius=0.02,
             color=CL, visible=ShowVectors)
L_label = curve(pos=Char_L(1.05*LScale*L), color=CL,
                radius=0.006, visible=ShowVectors)

# Define the fixed support of the gyro
support=frame()
pedestal = pyramid(pos=(0,0,-hpedestal), axis = (0,0,hpedestal),
                   size=(hpedestal,wpedestal,wpedestal),
                   color=Cpedestal, frame=support)
base = box(pos=(0,0,-hpedestal-tbase/2.), 
                 height=wbase, length=tbase, width=wbase,
                 axis=(0,0,1), color=Cpedestal,frame=support)
sphere(pos=(0,0,0), radius=0.01, color=Cshaft) # Articulation at the pivot

# Bolts
B1 = sphere(pos=(wbase/2.3,wbase/2.3,-hpedestal),radius=wbase*0.04,
            color=Cpedestal, frame=support)
B2 = sphere(pos=(wbase/2.3,-wbase/2.3,-hpedestal),radius=wbase*0.04,
            color=Cpedestal, frame=support)
B3 = sphere(pos=(-wbase/2.3,wbase/2.3,-hpedestal),radius=wbase*0.04,
            color=Cpedestal, frame=support)
B4 = sphere(pos=(-wbase/2.3,-wbase/2.3,-hpedestal),radius=wbase*0.04,
            color=Cpedestal, frame=support)

support.rotate(angle=pi/7, axis=(0,0,1))

# Define the gyro
gyro=frame(visible=0)
pivot = cone(pos=(0,0,Hshaft), axis=(0,0,-Hshaft), color=Cshaft,
             frame=gyro, radius=Rshaft)
shaft = cylinder(axis=(0,0,Lshaft), pos=pivot.pos,
                 radius=Rshaft, color=Cshaft, frame=gyro)
tip = cone(pos= pivot.pos+shaft.axis, axis=(0,0,Hshaft),
           color=Cshaft, radius=Rshaft, frame=gyro) 
rotor = cylinder(pos=(0,0,Lcm - Drotor/2), radius=Rrotor,
                 axis=(0,0,Drotor), color=Crotor, frame=gyro)
# Braces of rotor
cylinder(pos =(-Rrotor,0,Lcm - Drotor/3.), radius=Drotor/2,
               axis=(2*Rrotor,0,0), color=Cbraces, frame=gyro)
cylinder(pos =(0,-Rrotor,Lcm - Drotor/3.), radius=Drotor/2,
               axis=(0,2*Rrotor,0), color=Cbraces, frame=gyro)
cylinder(pos =(-Rrotor,0,Lcm + Drotor/3.), radius=Drotor/2,
               axis=(2*Rrotor,0,0), color=Cbraces, frame=gyro)
cylinder(pos =(0,-Rrotor,Lcm + Drotor/3.), radius=Drotor/2,
               axis=(0,2*Rrotor,0), color=Cbraces, frame=gyro)
ring(pos=(0,0,Lcm), radius=Rrotor, thickness=Drotor/2, axis=(0,0,1),
     color=Cbraces, frame=gyro)

# Rotate gyro to its starting position

    # First rotate by phi around the z axis
gyro.rotate(angle=phi, axis=(0,0,1))

    # Use the new x axis (Vx) and rotate by theta
Vx=(cos(phi),sin(phi),0)
gyro.rotate(angle=theta, axis=Vx)

    # Use the final z axis (V3) and rotate by psi
gyro.rotate(angle=psi, axis=V3)

gyro.visible=1  # Make the gyro visible


# Curve described by tip of gyro
trail = curve(radius=0, color=Ctrail)

dt = 0.0002     # Time step
dt = 0.004
dt2 = dt/2      # Half time step

# First rotate the gyro around current Omega by mag(Omega)*dt2
gyro.rotate(angle=mag(Omega)*dt2, axis=Omega)

while 1:
    #rate(800)
    rate (50)

    # Find midtime variables
    CosPsi = cos(psi); SinPsi=sin(psi); SinTheta=sin(theta)
    phidot = (SinPsi*omega1+CosPsi*omega2)/SinTheta
    
    phi_m = phi + phidot*dt2
    theta_m = theta + (CosPsi*omega1 - SinPsi*omega2)*dt2
    psi_m = psi + (omega3-phidot*cos(theta))*dt2
    omega1_m = omega1 +(gL_I*SinTheta*CosPsi-Delta*omega2)*dt2
    omega2_m = omega2 -(gL_I*SinTheta*SinPsi-Delta*omega1)*dt2

    # Get the full step variables
    CosPsi_m = cos(psi_m); SinPsi_m=sin(psi_m); SinTheta_m=sin(theta_m)
    phidot_m = (SinPsi_m*omega1_m+CosPsi_m*omega2_m)/SinTheta_m
    
    phi +=  phidot_m*dt
    theta +=  (CosPsi_m*omega1_m - SinPsi_m*omega2_m)*dt
    psi += (omega3 - phidot_m*cos(theta_m))*dt
    omega1 += (gL_I*SinTheta_m*CosPsi_m - Delta*omega2_m)*dt
    omega2 -= (gL_I*SinTheta_m*SinPsi_m - Delta*omega1_m)*dt

    # Get the vectors angular velocity and momentum in the fixed frame
    (V1,V2,V3) = MovingFrame(phi,theta,psi)
    Omega = omega1*V1+omega2*V2+omega3*V3
    L = I1*omega1*V1+I1*omega2*V2+I3*omega3*V3
    
    # Toggle Painting the trail and the L w vectors
    if scene.mouse.events:
        mouseObj = scene.mouse.getevent()
        scene.mouse.events = 0
        if mouseObj.click == "left":   # Toggle orbit of tip
            if ShowTrail == True:
                ShowTrail = False
                trail.pos=[]
            else: ShowTrail = True
        if mouseObj.click == "right":  # Togle display of L and w
            ShowVectors = 1 - ShowVectors
            L_body.visible = L_tip.visible = ShowVectors
            L_label.visible = ShowVectors
            Omega_body.visible = Omega_tip.visible = ShowVectors
            Omega_label.visible = ShowVectors

    # Update the trail and the L w vectors
    L_body.pos = [(0,0,0),0.95*LScale*L]
    L_tip.pos=0.95*LScale*L;
    L_tip.axis=0.05*LScale*L
    L_label.pos=Char_L(1.05*LScale*L)
    Omega_body.pos = [(0,0,0),0.95*OmegaScale*Omega]
    Omega_tip.pos=0.95*OmegaScale*Omega;
    Omega_tip.axis=0.05*OmegaScale*Omega
    Omega_label.pos=Char_omega(1.05*OmegaScale*Omega)

    if ShowTrail == True:
        trail.append(pos=V3*(Lshaft+2*Hshaft))
            
    # Rotate the gyro around new Omega by mag(Omega)*dt
    gyro.rotate(angle=mag(Omega)*dt, axis=Omega)
