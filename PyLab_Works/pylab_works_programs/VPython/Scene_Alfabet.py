from __future__ import division
from visual.text import *

Forward_Up ( None, None, 15 )
#Forward_Up ( scene.center-camera, None, 15 )


# Bruce Sherwood, December 2007
print """
With left mouse button down,
move left or right to look around.
"""
s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
c = len(s)
R = 5
for n in range(c):
    theta = n*2*pi/c-pi/2
    text(pos=(R*cos(theta), 0, R*sin(theta)),
         axis=(-sin(theta), 0, cos(theta)),
         string=s[n], height = 1, depth=0.5,
         color=color.yellow)
camera = vector(0,0,0) # for generality; need not be at origin
# Place center of scene at a distance R from the camera:
scene.center = camera+vector(0,0,-R)
# Point the camera:
#scene.userspin = False
down = False
lastpos = None

#scene.forward = scene.center-camera
# scene.fov is "field of view" in radians. R times the tangent
#  of half the field of view is half of the width of the scene:
#scene.range = R*tan(scene.fov/2)

Forward_Up ( scene.center-camera, None, 15 )
#Forward_Up ( None, None, 1 )

if scene.mouse.events:
  while scene.mouse.events:
    scene.mouse.getevent()

while 1:
    rate(50)
    if scene.mouse.events:
        m = scene.mouse.getevent()
        if m.press == 'left':
            down = True
        elif m.release == 'left':
            down = False
    if down: # and scene.mouse.pos != lastpos:
        lastpos = scene.mouse.pos
        lastpos.y = 0 # force mouse position to have y=0
        # (lastpos-camera) is a vector parallel to screen.
        # (lastpos-camera) cross norm(forward) is a vector in the +y direction,
        #   and this y component of the cross product is proportional to
        #   how far to the right the mouse is (if mouse is to left, this y
        #   component is negative)
        rotation = cross((lastpos-camera),norm(scene.forward))
        # If the mouse is to the right, y component is positive, and we need to
        #   turn the view toward the right, which means rotating the forward
        #   vector toward the right, about the +y axis, which requires a
        #   negative angle (vice versa if mouse is to the left, in which case
        #   the cross product is in the -y direction. The factor of 1/100 was
        #   chosen experimentally as giving an appropriate sensitivity to how
        #   far to the right (or left) the mouse is. Bigger mouse displacement
        #   makes the rotation faster.
        scene.forward = scene.forward.rotate(angle=-rotation.y/100, axis=(0,1,0))
        # Move the center of the scene to be a distance R from the camera,
        #   in the direction of forward.
        scene.center = camera+R*norm(scene.forward)

