from visual import *

dt = 4000
G = 6.67e-11
M = 5.98e24
m = 7.36e22    
R = 6.38e6  
r = 1.74e6   
d = 3.84e8  

earth = sphere(pos=(0,0,0),radius=10*R,color=color.blue)
satellite = sphere(pos=(0,d,0),radius=10*r,color=color.white)

a0 = (G * M * m / d**2) / m
v0 = (a0 * d)**.5
v = v0 * vector(1,0,0)  

def make_time_string(t): 
    "Accept a number of seconds, return a relative string."
    if t < 60: return "%02i seconds"%t
    mins,secs = divmod(t, 60)
    if mins < 60: return "%02i minutes %02i seconds"%(mins,secs)
    hours, mins = divmod(mins,60)
    if hours < 24: return "%02i hours %02i minutes"%(hours,mins)
    days,hours = divmod(hours,24)
    return "%02i days %02i hours"%(days,hours)

Forward_Up ( None, None, 1.6e9 )

mylabel = label ( yoffset = 80 , 
                  line = 1, opacity = 0 )
secs = 0

while True:
    rate(50)
    secs += dt
    D = mag(earth.pos - satellite.pos)
    Dir = norm(earth.pos - satellite.pos)    
    Mag = G * M * m / D**2
    F = Mag * Dir
    a = F / m
    v += a * dt
    satellite.pos += v* dt + .5 * a * dt**2

    # Display info to the user
    message = "Satellite's distance: %3.f kilometers" % ((d-R)/1000.0)
    message += "\nSatellite's speed: %.0f m/s" % mag(v)
    #message += "\nSatellite's acceleration magnitude: %.4f m/s**2" % mag(a)
    message += "\nTime: " + make_time_string(secs)
    mylabel.text = message


