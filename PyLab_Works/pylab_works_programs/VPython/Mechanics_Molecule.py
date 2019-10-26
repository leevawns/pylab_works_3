from visual import *

Forward_Up ( None, None, 5 )

#=================================
# Function to update a spring
#=================================
def UpdateSpring( spring, point1, point2, \
                  OffPoint, L0, R0,  N0=10 ):
    """Function to update a spring
    Arguments:
    spring = a curve object
    point1 = start point in axis of spring
    point2 = end point in axis of spring
    OffPoint = a point not in the axis of spring
    L0 = unstrtched length of spring
    R0 = unstrtched radius of spring  
    N0 = number of turns in the spring (def 10)"""

    Segments = 20           # Segments per turn of spring
    L = mag(point2-point1)  # Lenght of stretched spring 
    e3 = (point2-point1)/L  # Unit vector along axis of spring
    v1 = cross(OffPoint, e3)
    e1 = v1/mag(v1)
    e2 = cross(e3,e1)

    tau_max = 6.283186*N0
    TSteps = Segments*N0
    Lrec = L0*sqrt(1+(R0*tau_max/L0)**2) # Rectified length
    R = sqrt(Lrec**2-L**2)/tau_max       # Radius of spring
    c = L/tau_max                        # Helix step
    Dtau = c*tau_max/TSteps

    cs = []
    sn = []
    for n in range(0,Segments):
        cs.append(R*cos(n*6.283186/Segments)*e1)
        sn.append(R*sin(n*6.283186/Segments)*e2)
   
    position = []
    tau = 0
    n=0
    for count in range(0, TSteps+1):
        n = n+1
        if n==Segments :
            n = n - Segments
        position.append(point1+cs[n]+sn[n]+tau*e3)
        tau += Dtau
        
    spring.pos = position
    
#=================================
Frames = 100             # Frames per cycle
ct=[]
for n in range(0,Frames):
    ct.append(1-0.5*cos(n*6.283186/Frames))

# First define the properties of the display window 
#window = display(title="Spring", width=800, height=600)
#window.fullscreen = 1         # Change to 0 to get a floating window
window = scene
#window.range = (2.3,2.3,2.3)
#window.cursor.visible=0       # Hide the mouse cursor
#window.select()

pt1 = vector(-ct[0],0,0)
pt2 = vector(ct[0],0,0)

MySpring = curve(color=color.red, radius=0.02)

Ball1 = sphere(radius=0.35,pos=pt1-vector(0.3,0,0), color=color.blue)
Ball2 = sphere(radius=0.35,pos=pt2+vector(0.3,0,0), color=color.orange)
    
n=0
while 1 :
    #rate(100)
    rate(50)
    pt1 = vector(-ct[n],0,0)
    pt2 = vector(ct[n],0,0) 
    UpdateSpring(MySpring, pt1, pt2, vector(0,0,1), 1.0, 0.25)
    Ball1.pos=pt1-vector(0.3,0,0)
    Ball2.pos=pt2+vector(0.3,0,0)
    n += 1
    if n==Frames :
        n=0
