

from visual import *
import visual
import time


# ***********************************************************************
# Some default vectors defined as constants
# ***********************************************************************
X_AXIS    = vector ( 1., 0., 0. )
Y_AXIS    = vector ( 0., 1., 0. )
Z_AXIS    = vector ( 0., 0., 1. )
NULL_AXIS = vector ( 0., 0., 0. )

# for projections on the floor, xz-plane
# we operate in the region x>0 and z>0
# because diff_angle only generates the absolute angle
# i.e. 0 .. pi we want the x_axis to be at pi/4,
# so the z_axis will be at 3*pi/4
REF_AXIS = vector ( 1, 0, -1 )


_VArrow_Color = ( 0, 1, 1 )

# ***********************************************************************
# ***********************************************************************
def Forward_Up ( Forward = None, Up = None, Scale = None ) :
  """
  Sets both FORWARD and UP,
  preventing temporary parallelism of FORWARD and UP
  Defaults :
    Forward_Up ( 0, 0, -1 ), ( 0, 1, 0 ) )
  """
  if not ( Forward ) :
    if Up :
      scene.up = Up
  elif Forward and not ( Up ) :
    scene.forward = Forward
    
  else :
    # Be sure we've vectors
    #time.sleep ( 0.5 )
    Forward = vector ( Forward )
    Up      = vector ( Up      )

    # Temp_Forward should not allign with
    #   1. scene.up
    #   2. Up
    #   3. Forward
    # And we may assume that Up and Forward don't allign
    # The sum of Forward and Up, will fullfill conditions 2,3
    Temp_Forward = Up + Forward

    # calculate alfa, critical a=0  and alfa=pi
    alfa = Temp_Forward.diff_angle ( scene.up )
    # make alfa in range 0 .. pi/2, critical alfa = pi/2
    alfa = abs ( alfa - pi/2 )
    # make alfa in range pi/2 .. 0, critical alfa = 0
    alfa = pi/2 - alfa
    # if Temp_Forward alligned with current scene.up
    if alfa < 0.1 :
      # Create the product vector,
      # which is perpendicular to Up and Forward (conditions 2,3)
      # and will not allign with scene.up
      Temp_Forward = cross ( Up, Forward )

    scene.forward = Temp_Forward
    scene.up = Up
    scene.forward = Forward

  time.sleep ( 0.1 )
  if Scale and not ( scene.autoscale ) :
    #a = scene.mouse.camera [1] / Scale
    a = mag ( scene.mouse.camera ) / abs(Scale)
    if a > 0 :
      scene.scale = a * scene.scale
# ***********************************************************************


# ***********************************************************************
def Set_Scale ( Scale ) :
  time.sleep ( 0.1 )

  a = scene.mouse.camera [1] / Scale
  a = mag ( scene.mouse.camera ) / abs(Scale)
  scene.scale = a * scene.scale
# ***********************************************************************


# ***********************************************************************
def degrees ( radians ) :
  """translates radians to degrees (float)."""
  return 180 * radians / pi

# ***********************************************************************
def degree ( radians ) :
  """translates radians to degrees (int)."""
  return int ( 180 * radians / pi )

# ***********************************************************************
def proj_XZ ( axis, d = 0 ) :
  return vector ( axis.x, d, axis.z )
# ***********************************************************************
def proj_XY ( axis, d = 0 ) :
  return vector ( axis.x, axis.y, d )
# ***********************************************************************
def proj_YZ ( axis, d = 0 ) :
  return vector ( d, axis.y, axis.z )

# ***********************************************************************
def XZ_proj_Object ( Object, d = 0 ) :
  """ projects an object = ( pos, axis )
  on the XZ-plane, at a height y = d """
  Object.pos.y  = d
  Object.axis.y = 0

# ***********************************************************************
def XZ_Angle ( axis ) :
  """projects the vector on the XZ-plane and
  calculates the angle with the X-axis [ 0 .. 2*pi ]"""
  axis = vector ( axis.x, 0, axis.z )
  a1 = axis.diff_angle ( X_AXIS )
  a2 = axis.diff_angle ( Z_AXIS )
  if a2 < pi/2 :
    a1 = 2*pi - a1
  return a1

# ***********************************************************************
def f2w ( frame, local ) :
  """Translates local coordinate within a frame
  to world coordinate"""
  x_axis = norm ( frame.axis)
  z_axis = norm ( cross ( frame.axis, frame.up ))
  y_axis = norm ( cross ( z_axis, x_axis       ))
  return frame.pos + local.x * x_axis + \
                     local.y * y_axis + \
                     local.z * z_axis



# ***********************************************************************
# This event extension translates from PPyGui to wxPython
#   bind         ==> Bind
#   PPyGui event ==> wxPython event
#   event += event.window
# in the control's __init__,
# the binding to the correct wxPython should be done,
# e.g. for a Label :
#    self.Bind ( wx.EVT_LEFT_DOWN, self._OnChange )
# ***********************************************************************
class _visual_extension ( object ) :
  def __init__ ( self ) :
    self.extra_setters = {}
    self.extra_getters = {}

  # *********************************************************
  # *********************************************************
  def _add_attrib ( self, text, setter = None, getter = None ) :
    if setter :
      self.extra_setters [ text ] = setter
    if getter :
      self.extra_getters [ text ] = getter

  # *********************************************************
  # always called instead of the normal mechanism
  # *********************************************************
  def __setattr__ ( self, attr, value ) :
    if attr in self.extra_setters :
      self.extra_setters [ attr ] ( value )
    else :
      self.__dict__[attr] = value

  # *********************************************************
  # only called when not found with the normal mechanism
  # *********************************************************
  def __getattr__ ( self, attr ) :
    try :
      if attr in self.__dict__['extra_getters'] :
        return self.extra_getters [ attr ] ( )
    except :
      return []
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Coordinate_Axis ( object ) :
  """
  Draws a coordinate system of size = Size.
  """
  def __init__ ( self, Size = 1 ) :
    XC = ( 1, 0, 0 )
    YC = ( 0, 1, 0 )
    ZC = ( 0, 0, 1 )
    L = Size
    SW = 0.01 * L
    X = visual.arrow ( axis = ( L, 0, 0 ), color = XC, shaftwidth = SW, fixedwidth = True )
    Y = visual.arrow ( axis = ( 0, L, 0 ), color = YC, shaftwidth = SW, fixedwidth = True )
    Z = visual.arrow ( axis = ( 0, 0, L ), color = ZC, shaftwidth = SW, fixedwidth = True )
    label ( pos = ( L, 0, 0 ), text = 'X', color = XC )
    label ( pos = ( 0, L, 0 ), text = 'Y', color = YC )
    label ( pos = ( 0, 0, L ), text = 'Z', color = ZC )
# ***********************************************************************


# ***********************************************************************
class varrow ( visual.arrow ) : #, _visual_extension ) :
  """ draws a vertical arrow perpendicular to the XZ-plane"""
  def __init__ ( self, axis = None, pos = None ) :
    visual.arrow.__init__ ( self, shaftwidth=3, fixedwidth=1 )
    if axis :
      self.axis = axis
    if pos :
      self.pos = pos
      #print isinstance(self.pos,visual.cvisual.Vector)

    #self.color = _VArrow_Color
    #_visual_extension.__init__ ( self )
    #self._add_attrib ( 'color', self.Set_Color )

    self.children = []

  def Set_Color ( self, color ) :
    #global _VArrow_Color
    #varrow.color = _Varrow_Color = color
    varrow.color = color

  def append_new ( self, new_varrow = None ) :
    """
    Appends a new_varrow to the tip of myself,
    by correcting it's position and returns the varrow.
    New_varrow may either be a varrow or just a vector.
    If the input is a vector, a new varrow is created.
    """
    # Return on no input
    if not ( new_varrow ) :
      return

    # If not a varrow, we assume a vector
    # and thus create a varrow with properties of the vector
    if not ( isinstance ( new_varrow, varrow ) ) :
      new_varrow = varrow ( axis = new_varrow )

    # now finally position the varrow
    new_varrow.pos = self.axis + self.pos
    
    # append to children list ( used for tracking )
    self.children.append ( new_varrow )
    return new_varrow
    

# ***********************************************************************
class grid____2 ( object ) :
  def __init__ ( self, N, M, maze, normal, d, color = (1,0,1) ) :
    w = N * maze
    h = M * maze
    A = ( w, 0, 0 )
    for i in range ( M+1 ) :
      print 'grid',i
      visual.cylinder ( pos = ( 0, i*maze, d ), axis = A,
                        radius = 3, color = color )

    A = ( 0, h, 0 )
    for i in range ( N+1 ) :
      print 'grid',i
      visual.cylinder ( pos = ( i*maze, 0, d ), axis = A,
                        radius = 3, color = color )

# ***********************************************************************
class grid_Object ( object ) :
  """
  Create a grid perpendicular to the given object,
  at the position object.pos + object.axis.
  For now only planes parallel to the Y-axis works.
  If the Object in not parallel to the XZ-plane,
  the Y-components of the object are not used.
  """
  def __init__ ( self, Object, h, maze = 20, color = (1,0,1) ) :
    R = 1
    
    alfa = XZ_Angle ( Object.axis ) + pi/2
    Vtot = Object.pos + Object.axis
    Vhaaks = rotate ( Object.axis, angle = pi/2, axis= Y_AXIS )
    print 'Grid pars', alfa, Vtot, Vhaaks

    # Z-axis crossing
    Zxx = Vtot.z + Vtot.x * sin( alfa ) / cos ( alfa )
    # X-axis crossing = PP.pos.z + PP.pos.x * cos( alfa ) / sin ( alfa )
    ##Xxx = PP.pos.x + PP.pos.z * cos( alfa ) / sin( alfa )

    # Calculate total length
    L = Zxx / sin ( alfa )

    # Lines parallel to the XZ-plane
    M = int ( h / maze )
    PA = L * norm ( Vhaaks )
    Px = 0
    Pz = Zxx
    for i in range ( M+1 ) :
      visual.cylinder ( pos = ( Px, i*maze, Pz ), axis = PA,
                        radius = R, color = color )

    # Lines perpendicular to the XZ-plane
    N = int ( L / maze )
    dPz = - L * sin ( alfa ) / N
    dPx = L * cos ( alfa )/ N
    for i in range ( N+1 ) :
      visual.cylinder ( pos = ( Px + i*dPx, 0, Pz + i*dPz ), axis = h*Y_AXIS,
                        radius = R, color = color )

# ***********************************************************************
if __name__ == '__main__' :
  import visual
  from visual import *
  visual.scene.title = 'PyLab Works VPython'
  visual.scene.exit = False
  visual.scene.center = ( 200, 0, 200 )
  visual.scene.forward = ( -0.1, -1000, -0.1 )

  # create a coordinate system
  Color = ( 0.5, 1, 0.5 )
  visual.sphere ( radius = 8 )
  visual.cylinder ( axis = 400 * X_AXIS, radius = 3, color = Color )
  visual.cylinder ( axis = 500 * Z_AXIS, radius = 3, color = Color )
  visual.cylinder ( axis = 200 * Y_AXIS, radius = 3, color = Color )

  # create an object = ( pos, axis )
  Pos  = varrow ( 50 * vector ( 1, 0, 3 ) )
  Pos.color = ( 1, 0, 0 )

  Axis = Pos.append_new ( 30 * vector ( 2, 0, 1 ) )

  #Axis = varrow ( axis = 30 * vector ( 2, 0, 1 ), pos = Pos.axis )
  Axis.color = Pos.color

  grid_Object ( Axis, 240 )



  while True :
    visual.rate ( 50 )

    if scene.mouse.events :
      m = scene.mouse.getevent()
      #print m.ctrl,m.shift
      if m.press and ( m.button == 'left' ) :
        EP = scene.mouse.project ( normal = (1,0,0), d = 50 )
        print EP
    """
    # method 2: explicit projection on the front of the object
    A = proj_XZ ( self.Console.pos )
    B = proj_XZ ( self.Kast.axis )
    Vtot = A + B
    alfa = Vtot.diff_angle ( B )
    D = mag ( Vtot ) * cos ( alfa )
    #print D
    EP = scene.mouse.project ( normal = self.Kast.axis, d = D )
    EP.y = 0
    self.v_white.axis = EP
    print D,self.Kast.axis, self.v_white.axis
    """
