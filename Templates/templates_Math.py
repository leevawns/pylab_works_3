#icon = chart_curve.png
## Graph Sine
"""
Shows a sine wave
"""
x = arange ( 0.0, 3.0, 0.01 )
y = 10*sin ( 2.7 * pi * x )
OUT1 = y


## Graph multi signals
"""
Shows plotting of many signals,
and how to name the signals.
"""
x = arange ( 0.0, 3.0, 0.01 )
y = 5*cos  ( 1.3 * pi * x )
y2 = 10*sin ( 2.7 * pi * x )
OUT1 = x,y,y2,x ,2*x ,\
('cosine', 'sine', 'line y=x', 'line y=2x')  


## Graph Spiral
"""
Shows a spiral plot
"""
t = arange ( 0, 10 * pi, 0.1 )
x = t * sin ( t )
y = t * cos ( t )
OUT1 = x, y

## Graph Cardiod
"""
Shows a Cardiod
"""
t = arange ( 0, 2 * pi, 0.1 )
x = (1 + cos(t) ) * cos (t)
y = (1 + cos(t) ) * sin (t)
OUT1 = x, y

## My New Graph
"""
Some explaining text
"""
t = linspace ( 0, 4, 200 )
y = 3* sin ( 2 * pi * t )
OUT1 = y

## Graph Spiral
"""
Shows a Spiral
"""
phi = linspace ( 0, 4, 100 )
#r=sin(phi*pi) #
r = sin ( cos ( tan ( phi ) ) )
x = phi
y = 20 * r
OUT1 = x, y


## Graph 3D-pseudo
"""
Shows 3D pseudo color graph.
"""
def _func (x,y): return (1- x/2 + x**5 + y**3)*exp(-x**2-y**2)
dx, dy = 0.05, 0.05
x = arange(-3.0, 3.0, dx)
y = arange(-3.0, 3.0, dy)
X,Y = meshgrid(x, y)
OUT1 = _func ( X, Y ) 

##-

##2new program
"""
extended hintt description
and more lines of explaining text
"""
# -----------------------------------------------------------------------------
# New Program
# based on RPD
# -----------------------------------------------------------------------------
# include hardware definitions
for i in range (1, 5) :
  print i

##-

##test2
for i in range (1, 15) :
  print i

##|

## aap2
for i in range (1, 50) :
  print i

## aap33
for i in range (1, 50) :
  print i


