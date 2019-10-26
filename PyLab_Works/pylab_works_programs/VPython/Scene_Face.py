
# Joel Kahn, 2004

# Treat this as if it were under the GNU General Public License,
# although I'm not actually doing the GPL procedures for a program this small.

from visual import *
from time import *

#scene = display()
#scene.width = 1024
#scene.height = 738
#scene.x = 0
#scene.y = 0
#scene.center = (0.0, -0.3, 0.0)

left_brow = frame ()
right_brow = frame ()
mouth_frame = frame ()

eye_length = 0.8
eye_width = 0.4
eye_height = 0.5

left_eye = ellipsoid (pos = (-1.0, 0.9, 0.0), length = eye_length, width = eye_width, height = eye_height, color = color.blue)
right_eye = ellipsoid (pos = (1.0, 0.9, 0.0), length = eye_length, width = eye_width, height = eye_height, color = color.blue)

left_eyebrow = curve (frame = left_brow, radius = 0.09, color = (0.91, 0.7, 0.15))
right_eyebrow = curve (frame = right_brow, radius = 0.09, color = (0.91, 0.7, 0.15))

nose = pyramid (pos = (0.0, 0.0, 0.0), axis = (0.0, 0.0, 1.0), width = 0.8, height = 0.8, length = 1.7)

mouth = curve (frame = mouth_frame, radius = 0.2, color = color.red)

eyebrow_x1 = 1.4
eyebrow_x2 = 1.1
eyebrow_x3 = 1.0
eyebrow_x4 = 0.9
eyebrow_x5 = 0.6

eyebrow_y1 = 1.25
eyebrow_y2 = 1.39
eyebrow_y3 = 1.41
eyebrow_y4 = 1.39
eyebrow_y5 = 1.25

left_eyebrow.append (pos = (-eyebrow_x1, eyebrow_y1, 0.0))
left_eyebrow.append (pos = (-eyebrow_x2, eyebrow_y2, 0.0))
left_eyebrow.append (pos = (-eyebrow_x3, eyebrow_y3, 0.0))
left_eyebrow.append (pos = (-eyebrow_x4, eyebrow_y4, 0.0))
left_eyebrow.append (pos = (-eyebrow_x5, eyebrow_y5, 0.0))

right_eyebrow.append (pos = (eyebrow_x1, eyebrow_y1, 0.0))
right_eyebrow.append (pos = (eyebrow_x2, eyebrow_y2, 0.0))
right_eyebrow.append (pos = (eyebrow_x3, eyebrow_y3, 0.0))
right_eyebrow.append (pos = (eyebrow_x4, eyebrow_y4, 0.0))
right_eyebrow.append (pos = (eyebrow_x5, eyebrow_y5, 0.0))

mouth.append (pos = (-1.5, -0.5, 0.0))
mouth.append (pos = (-0.5, -1.3, 0.0))
mouth.append (pos = (0.0, -1.4, 0.0))
mouth.append (pos = (0.5, -1.3, 0.0))
mouth.append (pos = (1.5, -0.5, 0.0))

ang = 0.00005
ang = 0.05
red_component = 0.001
green_component = 0.0

switcher = 1.0

Forward_Up ( None, None, 4 )

while True :
    rate ( 50 )
    mouth_frame.rotate (angle = ang, axis = (-1.0, 0.0, 0.0), origin = (0.0, -1.19, 0.0))
    left_brow.rotate (angle = ang, axis = (-1.0, 0.0, 0.0), origin = (0.0, 1.36, 0.0))
    right_brow.rotate (angle = ang, axis = (-1.0, 0.0, 0.0), origin = (0.0, 1.36, 0.0))
    nose.rotate (angle = ang, axis = (ang, ang, 1.0))

    if red_component > 0.999: switcher = -1.0
    if red_component < 0.001: switcher = 1.0
    red_component = red_component + switcher * ang
    green_component = green_component + 1.0 / time()
    if green_component > red_component: green_component = 0.0
    blue_component = 1.0 - red_component
    nose.color = (red_component, green_component, blue_component)
