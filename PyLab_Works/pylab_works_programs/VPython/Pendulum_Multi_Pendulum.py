from visual import *

Forward_Up ( None, None, 15 )

# Constants and time step
N = 6       # number of bobs
R = 0.3     # Radius of bob (separation between bobs=1)
Ks = 50.    # K of springs(masses=1)
g = 9.8     # Relative strength of gravity
gamma= 0.03 # Some friction
Rgdt = 1.0  # Rigidity factor (Rgdt=0 is a regular spring)

#Dt = 0.002*sqrt(1/g)    # Full time step
Dt = 0.02*sqrt(1/g)    # Full time step
Dt2 = Dt/2.0            # Midpoint time step
DiaSq = (2*R)**2        # Diameter of bob squared 

RandomStart = False
if RandomStart:         # Get the random number generator
    from random import *
    seed()

Cbob0 = color.red
Cbob = color.yellow
Cstring = color.cyan

# Properties of the display window 
#window = display(title="Multiple Pendulum", width=800, height=600)
#window.fullscreen = 1      # Change to 0 to get a floating window
window = scene
#window.range = (2*N,2*N,2*N)
#window.cursor.visible = 0  # Hide the mouse
window.userspin = 0        # No rotation with mouse
#window.forward = (0,0,-1)  # +z-axis toward you       
window.lights = [vector(0,0,1)] # Vector pointing to the light source
window.ambient=0

# Create the initial positions and velocitites (0,0) of the bobs
bob_x=[0.]
bob_y=[0.85*N]
x_dot=[0.]*(N+1)
y_dot=[0.]*(N+1)

for k in range(1,N+1):
    if RandomStart:
        alpha = uniform(0,2*pi)  # 2*pi*random()
    else:
        alpha = pi/5 
    bob_x.append(bob_x[k-1]+cos(alpha))
    bob_y.append(bob_y[k-1]+sin(alpha))

# Create the bobs
bob=[sphere(pos=(bob_x[0],bob_y[0]),  radius=R*0.5, color=Cbob0)]

for k in range(1,N+1):
    bob.append(sphere(pos=(bob_x[k],bob_y[k]), radius=R, color=Cbob))

# Create the string out of N links

link = [0]*N
for k in range(N):
    link[k] = cylinder(pos=bob[k].pos,axis = bob[k+1].pos-bob[k].pos,
                         radius=R/3, color=Cstring)

# Create some auxiliary variables
x_dot_m = [0.]*(N+1)
y_dot_m = [0.]*(N+1)
dij = [0.]*(N+1)    # array with distances to previous bob
dij_m = [0.]*(N+1)

for k in range(1,N+1):
    dij[k] = sqrt((bob_x[k]-bob_x[k-1])**2+(bob_y[k]-bob_y[k-1])**2)

fctr = (lambda x: (x-1.+Rgdt*(x-1.)**3)/x)

# Click the mouse to start
#window.mouse.getclick()   # Empty the mouse queue
    
# The main loop
while True :
    #rate(1000)
    rate(50)

    # Compute the midpoint variables
    bob_x_m = map((lambda x,dx:x+Dt2*dx),bob_x,x_dot)
    bob_y_m = map((lambda y,dy:y+Dt2*dy),bob_y,y_dot)
    
    for k in range(1,N+1):
        dij_m[k] = sqrt((bob_x_m[k]-bob_x_m[k-1])**2 +
                        (bob_y_m[k]-bob_y_m[k-1])**2)
        
    for k in range(1,N+1):
        factor =  fctr(dij[k]) 
        x_dot_m[k] = x_dot[k] - Dt2*(Ks*(bob_x[k]-bob_x[k-1])*fctr(dij[k])
                     + gamma*x_dot[k])
        y_dot_m[k] = y_dot[k] - Dt2*(Ks*(bob_y[k]-bob_y[k-1])*factor + g
                     + gamma*y_dot[k])
                                   
    for k in range(1,N):
        factor =  fctr(dij[k+1]) 
        x_dot_m[k] -= Dt2*Ks*(bob_x[k]-bob_x[k+1])*factor
        y_dot_m[k] -= Dt2*Ks*(bob_y[k]-bob_y[k+1])*factor

    # Compute the full step variables
    bob_x = map((lambda x,dx:x+Dt*dx),bob_x,x_dot_m)
    bob_y = map((lambda y,dy:y+Dt*dy),bob_y,y_dot_m)

    for k in range(1,N+1):
        dij[k] = sqrt((bob_x[k]-bob_x[k-1])**2+(bob_y[k]-bob_y[k-1])**2)

    for k in range(1,N+1):
        factor = fctr(dij_m[k])
        x_dot[k] -=  Dt*(Ks*(bob_x_m[k]-bob_x_m[k-1])*factor
                         + gamma*x_dot_m[k])
        y_dot[k] -=  Dt*(Ks*(bob_y_m[k]-bob_y_m[k-1])*factor + g
                         + gamma*y_dot_m[k])

    for k in range(1,N):
        factor = fctr(dij_m[k+1])
        x_dot[k] -= Dt*Ks*(bob_x_m[k]-bob_x_m[k+1])*factor
        y_dot[k] -= Dt*Ks*(bob_y_m[k]-bob_y_m[k+1])*factor

    # Check to see if the spheres are colliding
    for i in range(1,N):
        for j in range(i+1,N+1):
            dist2 = (bob_x[i]-bob_x[j])**2+(bob_y[i]-bob_y[j])**2
            if dist2 < DiaSq:  # Spheres are colliding
                Ddist = sqrt(dist2)-2*R
                tau = norm(vector(bob_x[j]-bob_x[i],bob_y[j]-bob_y[i]))
                DR = Ddist/2*tau
                bob_x[i] += DR.x
                bob_y[i] += DR.y
                bob_x[j] -= DR.x
                bob_y[j] -= DR.y
                Vji = vector(x_dot[j]-x_dot[i],y_dot[j]-y_dot[i])
                DV = dot(Vji,tau)*tau
                x_dot[i] += DV.x
                y_dot[i] += DV.y
                x_dot[j] -= DV.x
                y_dot[j] -= DV.y
                
    # Update the loations of the bobs and the links in the string
    for k in range(1,N+1):
        bob[k].pos = (bob_x[k],bob_y[k])
        link[k-1].pos = bob[k-1].pos
        link[k-1].axis = bob[k].pos-bob[k-1].pos
    


