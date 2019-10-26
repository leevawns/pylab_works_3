from visual import *
#from Numeric import *

print """
Simple solar system model showing the orbits of the planets
Note: In this version the orbits are not tilted so
      the longitude of the ascending node is not correct.
created by Lensyl Urbano, Jan. 2006.
"""

class orbit:

    def __init__(self,e=0.0,rad=1.0, mu=10.0, planet_size=1.0, period=365,
                 inclination=0.0, lap=0.0, frate=10000000):
        self.orbit_path = curve(color=color.green,radius=0.075)
        self.planet = sphere(color=color.red,radius=planet_size)
        if e >= 1.0:
            e = 0.99
        if e < 0.0:
            e = 0.0
        fx = 2.0 - 2.0*min(abs((1-e*e)/(1-e)), abs(-(1-e*e)/(1+e)))
        self.fx = fx
        self.e = e
        self.rad = rad
        self.dangle = 360./period
        self.inclination = inclination
        self.lap = lap
        if False :
          for i in range(int(period)+1):
            #rate(frate)
            theta = radians(float(360.*i/period))
            #h_sq = a*(1-e*e)*mu
            r = (1-e*e)/(1-e*cos(theta))
            nx = rad*(r*cos(theta) - fx)
            ny = rad*r*sin(theta) 

            #print i, f, r, cos(theta), sin(theta), nx, ny
            #nz = rotate(vector(nx,ny,0.0), angle=inclination, 
            posi = rotate(vector(nx,ny,0.0), angle=radians(inclination), axis=(0,1,0))
            posi = rotate(posi, angle=radians(lap), axis=(0,0,1))
            
            self.orbit_path.append(pos=posi)
            self.planet.pos=posi
        self.angle = 0.0

    def re_draw2(self,e=0.0,rad=1.0,mu=10.0, frate=10000000):
        #redraw last path
        if e >= 1.0:
            e = 0.99
        if e < 0.0:
            e = 0.0
        fx = 2.0 - 2.0*min(abs((1-e*e)/(1-e)), abs(-(1-e*e)/(1+e)))
        self.fx = fx
        self.e = e
        self.rad = rad
        for i in range(361):
            #rate(frate)
            theta = radians(float(i))
            #h_sq = a*(1-e*e)*mu
            r = (1-e*e)/(1-e*cos(theta))
            nx = rad*(r*cos(theta) - fx)
            ny = rad*r*sin(theta) 
            self.orbit_path.pos[i]=vector(nx, ny, 0.0)

    def move_planet(self):
        self.angle = self.angle + self.dangle
        #to show the planet orbiting the Sun
        theta = radians(float(self.angle))
        r = (1-self.e*self.e)/(1-self.e*cos(theta))
        nx = self.rad*(r*cos(theta) - self.fx)
        ny = self.rad*r*sin(theta) 
        posi=rotate(vector(nx,ny,0.0), angle=radians(self.inclination), axis=(0,1,0))
        posi = rotate(posi, angle=radians(self.lap), axis=(0,0,1))
        self.planet.pos = posi

        
origx = 0
origy = 0
w = 704+4+4
h = 576+24+4

mu = 10.0 #gravitational acceleration
#e = 0.6 #eccentricity
#a = 10.0 #distance of sun from center of elipse

# to draw an elipse


sun = sphere(color=color.yellow)
#orbitor = sphere()

earth = orbit(e=0.0167, rad=15.0, mu=mu, 
              planet_size=1.0, period=365,
              lap=102.9)

mercury = orbit(e=0.2056, rad=5.8, mu=mu, 
                planet_size=0.38*earth.planet.radius, period=87,
                inclination=7., lap=77.46)
venus = orbit(e=0.0067, rad=10.8, mu=mu, 
              planet_size=0.95*earth.planet.radius, period=224,
              inclination=3.4, lap=131.5)
mars = orbit(e=0.093, rad=22.8, mu=mu, 
             planet_size=0.53*earth.planet.radius, period=687,
             inclination=1.8, lap=336.0)
print """
jupiter = orbit(e=0.05, rad=77.8, mu=mu, 
                planet_size=11.*earth.planet.radius, period=4330,
                inclination=1.3, lap=14.75)
saturn = orbit(e=0.06, rad=143.3, mu=mu, 
               planet_size=9.*earth.planet.radius, period=10750,
               inclination=2.5, lap = 92.4)
uranus = orbit(e=0.05, rad=287.2, mu=mu, 
               planet_size=4.*earth.planet.radius, period=30600,
               inclination=0.8, lap=171.0)
neptune = orbit(e=0.01, rad=449.5, mu=mu, 
                planet_size=3.85*earth.planet.radius, period=60000,
                inclination=1.8, lap=45.0)
pluto = orbit(e=0.2488, rad=590.6, mu=mu, 
                planet_size=0.187*earth.planet.radius, period=90500,
              inclination=17.16, lap=224)
"""

print 'piep-1'
scene.center = sun.pos
scene.autoscale = 0
print 'piep-2'

#Coordinate_Axis ( 10 )
#Forward_Up ( (0,-0.5,-1), None, 5e1 )
Forward_Up ( None, None, 50 )

runtime = 0.0
pick = None
planet_angle = 0
print 'piep-3'

while 1:
    rate ( 50 )

    earth.move_planet()
    mercury.move_planet()
    venus.move_planet()
    mars.move_planet()
    """
    jupiter.move_planet()
    saturn.move_planet()
    uranus.move_planet()
    neptune.move_planet()
    pluto.move_planet()
    """

    
