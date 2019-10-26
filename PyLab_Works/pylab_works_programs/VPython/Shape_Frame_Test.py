Forward_Up ( (-1,-1,-1), None, 30 )
Coordinate_Axis ( 12 )

# for reference, display origin and floor
org = visual.sphere ( 
  pos=(0,0,0), radius = 0.4 )
l = 10.
floor = visual.box (
  pos=(l/2,-1,l/2), axis=(1,0,0), 
  color=(1,0,0), 
  length=l, width=l, height=2 )

# create a normal box
box_free = visual.box ( color=(0,0,1),
  pos=(2,3,3), 
  length = 4,
  width  = 2,
  height = 1 )

# create the same box in a frame
test_frame = frame ()
box_frame = visual.box ( frame=test_frame, color=(0,1,0),
  pos=(2,1,3), 
  length = 4,
  width  = 2,
  height = 1 )

# rotate free_box and test_frame, works as expected
Y_AXIS = ( 0, 1, 0 )
box_free  .rotate ( angle = pi/2, axis = Y_AXIS )
test_frame.rotate ( angle = pi/2, axis = Y_AXIS,
  origin = test_frame.pos + box_frame.pos )

# now move the box and the frame in the z-direction
box_free.z   += 2
test_frame.z += 2

# rotate box and frame back
box_free  .rotate ( angle = -pi/2, axis = Y_AXIS )

def world_space_pos(frame, local):
  """Returns the position of local in world space."""
  x_axis = norm(frame.axis)
  z_axis = norm(cross(frame.axis, frame.up))
  y_axis = norm(cross(z_axis, x_axis))
  return frame.pos+local.x*x_axis+local.y*y_axis+local.z*z_axis

origin = world_space_pos(test_frame,box_frame.pos)
test_frame.rotate ( angle = -pi/2, axis = Y_AXIS, 
  origin = origin )
#  origin = test_frame.pos + box_frame.pos ) 

