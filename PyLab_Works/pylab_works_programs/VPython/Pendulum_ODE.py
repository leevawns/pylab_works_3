Forward_Up ( None, None, 5 )

# A simple example of the use of VPython
# and the Open Dynamics Engine (http://pyode.sourceforge.net).

# pyODE example: Connecting bodies with joints

# Miles Jacobs <milesjacobs@hotmail.com>
# Department of Electrical Engineering
# Cape Peninsula University of Technology
# Bellville, South Africa

from visual import *
import ode

# Create a world object
world = ode.World()
world.setGravity((0,-9.81,0))

# Create two bodies
body1 = ode.Body(world)
M = ode.Mass()
M.setSphere(2500, 0.05)
body1.setMass(M)
body1.setPosition((1,2,0))

body2 = ode.Body(world)
M = ode.Mass()
M.setSphere(2500, 0.05)
body2.setMass(M)
body2.setPosition((2,2,0))

# Connect body1 with the static environment
j1 = ode.HingeJoint(world)
j1.attach(body1, ode.environment)
j1.setAnchor( (0,2,0) )
j1.setAxis( (0,0,1) )
j1.setParam(ode.ParamVel, 3)
j1.setParam(ode.ParamFMax, 20)

# Connect body2 with body1
j2 = ode.BallJoint(world)
j2.attach(body1, body2)
j2.setAnchor( (1,2,0) )

# Display system using VPython
p1 = body1.getPosition()
p2 = body2.getPosition()

line1=curve(pos=[(0,2,0), p1], radius=0.1,color=color.white)
ball1=sphere(pos=p1, radius=0.2,color=color.red)
line2=curve(pos=[p1, p2], radius=0.1,color=color.green)
ball2=sphere(pos=p2, radius=0.2,color=color.blue)

scene.center=(0,2,0)
scene.autoscale=0

# Simulation loop...

fps = 50
dt = 1.0/fps

while True :
    # Try to keep the specified framerate
    rate ( fps )

    # Draw the two bodies
    p1 = body1.getPosition()
    p2 = body2.getPosition()

    line1.pos=[(0,2,0), p1]
    ball1.pos=p1
    line2.pos=pos=[p1, p2]
    ball2.pos=p2

    # Next simulation step
    world.step(dt)



