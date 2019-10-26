"""
import visuals
import sys
sys.path.append ( 'D:/Data_Python_25/support')
from visual_support import *
"""
Forward_Up ( ( -1, -2, -1 ), None, 900 )


# ************************************************************************
# Alle maten zijn in centimeters (floating point mag).
# Kleuren zijn in RGB-notatie, waarbij elke kleur loopt van 0.0 .. 1.0
# De pendels zijn gepositioneerd t.o.v. rechter-achter-hoek.
# Ten slotte: raak het hoofd van de patient niet aan.
# ************************************************************************
Kamer_Hoogte       = 240
Kamer_Breedte      = 450
Kamer_Diepte       = 400

Stoel_1_Achterwand = 80
Stoel_2_Achterwand = 110
Stoel_Zijwand      = 120

Arm_1_Lengten      = ( 110, 85 )
Console_1_Hoogte   = 150          # afstand onderkant arm tot onderkant kast
Kast_1_Diepte      = 50
Kast_1_Breedte     = 80
Kast_1_Hoogte      = 100

Arm_2_Lengten      = ( 85, 85 )
Console_2_Hoogte   = 180          # afstand onderkant arm tot onderkant kast
Kast_2_Diepte      = 50
Kast_2_Breedte     = 70
Kast_2_Hoogte      = 140

Bed_Lengte         = 200
Bed_Breedte        = 110 
Bed_Hoogte         = 60

Kast_1_Kleur       = ( 0.8, 0.8, 1.0 )
Kast_2_Kleur       = ( 0.8, 0.8, 1.0 )
Wand_Kleur         = ( 0, 0, 1 )
Vloer_Kleur        = ( 1, 0, 0 )
# ************************************************************************


# ************************************************************************
# onbelangrijke parameters
# ************************************************************************
Stoel_Kleur  = ( 0, 1, 0 )
Stoel_Radius = 10.0
arm_w		     = 20
arm_h        = 10
Arm_Kleur    = (1,0,1)
# ************************************************************************



# ************************************************************************
# some convenience constants
# ************************************************************************
kh2 = Kamer_Hoogte  / 2.0
kb2 = Kamer_Breedte / 2.0
kd2 = Kamer_Diepte  / 2.0
h   = Kamer_Hoogte


# ************************************************************************
# The room
# ************************************************************************
org = visual.sphere ( pos = NULL_AXIS, radius = 4 )
Floor = visual.box (  pos = ( kd2, 0, kb2 ), axis = X_AXIS, color = Vloer_Kleur, 
  length = Kamer_Diepte, width = Kamer_Breedte, height = 2 )
wall_1 = visual.box ( pos = ( kd2, kh2, 0 ), axis = X_AXIS, color = Wand_Kleur, 
  length = Kamer_Diepte, width = 2, height = Kamer_Hoogte )
wall_2 = visual.box ( pos=( 0, kh2 , kb2), axis = X_AXIS, color = Wand_Kleur, 
  length = 2, width = Kamer_Breedte, height = Kamer_Hoogte )
window = visual.box ( pos=( 5, kh2 , kb2), axis = X_AXIS, color = (1,1,0), 
  length = 2, width = Kamer_Breedte-50, height = Kamer_Hoogte-50 )




# *******************************************************
class pendel_arm ( visual.box ) :
  def __init__ ( self, x0, y0, z0, L, color ) :
    visual.box.__init__ ( self, color = color,
      width = arm_w, height = arm_h )
    self.y = h - y0 - arm_h / 2.0
    self.End_Objects = []
    
    self.L =  L / 2.0
    self.LL = L + arm_w 
    self.x0 = x0
    self.z0 = z0
    ##self.v  = varrow ( ( 0, -self.L, 0 ) ) 
    self.Old_Phi = XZ_Angle ( X_AXIS )
    self.Set_Dir ( X_AXIS )
    
  def ReSize ( self, L ) :
    self.L = L / 2 
    self.LL = L + arm_w 
    self.Set_Dir ( self.Dir )
      
  def Add_End_Object ( self, Object ) :
    self.End_Objects.append ( Object )
    
  def Set_Dir ( self, Dir ) :
    self.Dir = norm ( Dir )
    self.Extra_Angle = 0
    self.Update ()

  def Init_Mouse ( self ) :
    pass 
            
  def Follow_Mouse ( self ) :
    # determine mouse position in plane of the object
    # because probably we're not on the object anymore
    # projection on the object doesn't work
    MV = scene.mouse.project ( normal = (0,1,0), d =self.y )
        
    # now the direction is the difference vector from 
    # rotation point to mouse projection
    B = vector ( self.Org.x, self.y, self.Org.z )
    A = MV - B
    # but with the y-axis = 0
    A.y = 0
    self.Set_Dir ( A )
    
  def Update ( self ) :
    # Implement the extra rotation from a previous joint
    self.axis = rotate ( self.LL * self.Dir , angle=self.Extra_Angle, axis=Y_AXIS ) 

    # Determine normalized direction and absolute angle
    Dir = norm ( self.axis )
    Phi = XZ_Angle ( Dir )

    # Calculate the position ( centre of the block )
    self.x = self.x0  + self.L * cos (Phi) 
    self.z = self.z0  - self.L * sin (Phi) 

    # Determine the rotation points at both ends
    self.Org = vector ( self.x0 , 0, self.z0 ) 
    self.End = self.Org + 2.0 * self.L * Dir
  
    # Test vector at the end point
    ##self.v.pos = self.End + vector (0, self.y+10, 0 ) 

    # Correct all child joints by sending
    # New start point and the change in rotation
    Delta_Phi = Phi - self.Old_Phi
    self.Old_Phi = Phi
    for Object in self.End_Objects :
      Object.Follow_Parent ( self.End, Delta_Phi )
      
  def Follow_Parent ( self, End, Phi ) :
    self.Extra_Angle += Phi
    self.x0 = End.x
    self.z0 = End.z
    self.Update ()
# ************************************************************************


# *******************************************************
class pendel_console ( frame ) :
  def __init__ ( self, Arm, Console_Hoogte,
      Kast_Hoogte, Kast_Breedte, Kast_Diepte, Kast_Kleur ) :
    self.Arm = Arm

    frame.__init__ ( self )
  
    self.Console = visual.cylinder ( frame= self, axis = ( 0, -Console_Hoogte, 0 ), 
      color = Stoel_Kleur, radius = Stoel_Radius )
    CP = vector ( Arm.End ) 
    CP.y = Arm.y 
    self.Console.pos = CP
    
    self.Org = vector ( self.Console.pos )

    self.Kast = visual.box ( frame = self, color = Kast_Kleur )
    self.Kast.length = Kast_Diepte
    self.Kast.width  = Kast_Breedte
    self.Kast.height = Kast_Hoogte
    self.Kast.x = self.Console.x + Kast_Diepte / 2.0 - Stoel_Radius
    self.Kast.z = self.Console.z
    self.Kast.y = self.Console.y - self.Console.length + self.Kast.height / 2
    self.Kast_Top = self.Kast.y + self.Kast.height / 2.0
    self.Prev_Phi = 0

    #self.Grid = grid_Object ( self.Kast, Kamer_Hoogte , maze = 20, color = (1,0,1) )

    self.D = 3 + self.Kast.y + self.Kast.height / 2
    """
    self.v_red = varrow ()
    self.v_red.color = ( 1,0,0 )

    self.v_green = varrow ()
    self.v_green.frame = self
    self.v_green.color = ( 0,1,0 )
    self.v_green.pos = self.Console.pos
    self.v_green.pos.y = self.D
    
    #self.v_white = varrow ()
    self.v_blue = varrow ()
    self.v_blue.frame = self
    self.v_blue.color = (0,0,1)
    self.v_blue.pos = self.Console.pos
    self.v_blue.pos.y = self.D
    """
    
    self.Kast.Init_Mouse   = self.Init_Mouse
    self.Kast.Follow_Mouse = self.Follow_Mouse
 
  def Set_Dir ( self, Old_Pos, New_Pos ) :
    alfa1 = Old_Pos - proj_XZ ( self.Arm.End )
    alfa2 = New_Pos - proj_XZ ( self.Arm.End )
    Phi = XZ_Angle ( alfa2 ) - XZ_Angle ( alfa1 )
    self.Kast.rotate ( angle = Phi, axis = Y_AXIS, 
      origin = self.Console.pos )

  def Init_Mouse ( self ) : 
    MV = proj_XZ ( scene.mouse.pickpos )
    touch = MV - proj_XZ ( self.Console.pos )
    self.Prev_Phi = XZ_Angle ( touch ) - XZ_Angle ( self.Kast.axis )
    #print 'xx',scene.mouse.pickpos, scene.mouse.pos

  def Follow_Mouse ( self ) :
    """
    Although not perfect, a good way to detect the mouse position
    for rotation, seems to be projection on the top of the box
    """
    EP = scene.mouse.project ( normal = Y_AXIS, d = self.D )
    #self.v_red.axis = EP
    #self.v_green.axis = self.Kast.axis
    EP = EP - ( self.Console.pos + self.pos )
    EP.y = 0
    #self.v_blue.axis = 50 * norm ( EP )

    New_Phi = XZ_Angle ( EP ) - XZ_Angle ( self.Kast.axis )
    #if self.Prev_Phi != 0 :
    #  print '--',degree(New_Phi), degree(self.Prev_Phi)
    self.Kast.rotate ( angle = New_Phi-self.Prev_Phi, axis = Y_AXIS,
      origin = self.Console.pos )

  def Follow_Parent ( self, End, Phi ) :
    self.pos =  ( End - self.Org )  
    self.y = 0
    self.Kast.rotate ( angle=Phi, axis=Y_AXIS,
      origin = self.Console.pos )
    #self.v_blue.rotate ( angle=Phi, axis=Y_AXIS,
    #  origin = self.Console.pos )

  def ReSize ( self, w = 0, d = 0, h = 0, A = 0 ) :
    if d :
      self.Kast.length = d
    if w : 
      self.Kast.width  = w
    if h :
      self.Kast.height = h
    if A :
      self.Console.axis = ( 0, -A, 0 )
# ************************************************************************



# ************************************************************************
# Pendels
# ************************************************************************
Stoel_1 = visual.cylinder ( axis = ( 0, -50, 0 ), 
  pos = ( Stoel_1_Achterwand, Kamer_Hoogte, Stoel_Zijwand ),
  color = Stoel_Kleur, radius = Stoel_Radius )
Stoel_2 = visual.cylinder ( axis = ( 0, -15, 0 ), 
  pos = ( Stoel_2_Achterwand , Kamer_Hoogte, Stoel_Zijwand ),
  color = Stoel_Kleur, radius = Stoel_Radius )

arm1_1L = Arm_1_Lengten [0]
arm1_2L = Arm_1_Lengten [1]
Arm1_1 = pendel_arm ( Stoel_1.x, Stoel_1.length, Stoel_1.z, arm1_1L, Arm_Kleur )
Arm1_2 = pendel_arm ( Arm1_1.End.x, Stoel_1.length+arm_h+2, Arm1_1.End.z, arm1_2L, Arm_Kleur )
Arm1_1.Add_End_Object ( Arm1_2 )
Arm1_1.Set_Dir ( (1,0,1) )
Arm1_2.Set_Dir ( (0,0,1) )

Arm2_1L = Arm_2_Lengten [0]
Arm2_2L = Arm_2_Lengten [1]
Arm2_1 = pendel_arm ( Stoel_2.x, Stoel_2.length, Stoel_2.z, Arm2_1L, Arm_Kleur )
Arm2_2 = pendel_arm ( Arm2_1.End.x, Stoel_2.length+arm_h+2, Arm2_1.End.z, Arm2_2L, Arm_Kleur )
Arm2_1.Add_End_Object ( Arm2_2 )
Arm2_1.Set_Dir ( (1,0,-1) )
Arm2_2.Set_Dir ( (1,0,0) )

Console_1 = pendel_console ( Arm1_2, Console_1_Hoogte,
  Kast_1_Hoogte, Kast_1_Breedte, Kast_1_Diepte, Kast_1_Kleur )
Console_2 = pendel_console ( Arm2_2, Console_2_Hoogte,
  Kast_2_Hoogte, Kast_2_Breedte, Kast_2_Diepte, Kast_2_Kleur )
Arm1_2.Add_End_Object ( Console_1 )
Arm2_2.Add_End_Object ( Console_2 )
# ************************************************************************


# ************************************************************************
# Bed + patient
# ************************************************************************
Bed_Patient = frame ( )
Bed = visual.box ( frame = Bed_Patient )
Bed.length = Bed_Lengte
Bed.width  = Bed_Breedte
Bed.height = Bed_Hoogte
Bed.x = Bed.length / 2 
Bed.y = Bed.height / 2
Bed.z = Bed.width  / 2 

PH = visual.sphere ( frame = Bed_Patient, radius = 20, color = ( 1, 1, 0.5 ))
PH.y = Bed.height
PH.x = Bed.x - 60
PH.z = Bed.z
# patient body
PB = visual.ellipsoid ( frame = Bed_Patient, color = PH.color, 
  axis = ( 100, 0, 0 ), width = 50, height = 30 )
PB.y = PH.y  
PB.x = PH.x + PB.length / 2 + PH.radius  
PB.z = PH.z 

Bed_Patient.x = 120
Bed_Patient.z = 130
origin = f2w ( Bed_Patient, Bed.pos ) 
Bed_Patient.rotate ( angle = -pi / 4,
            origin = origin, axis = Y_AXIS )
# ************************************************************************
 

# ************************************************************************
# Convenience shortcuts
# ************************************************************************
KA = Console_1.ReSize
KB = Console_2.ReSize
def AA ( arm1 = 0, arm2 = 0 ) :
  if arm1 :
    Arm1_1.ReSize ( arm1 )
  if arm2 :
    Arm1_2.ReSize ( arm2 )
def AB ( arm1 = 0, arm2 = 0 ) :
  if arm1 :
    Arm2_1.ReSize ( arm1 )
  if arm2 :
    Arm2_2.ReSize ( arm2 )
     
def BP ( x = 0, y = 0, alfa = -1 ) :
  if x :
    Bed_Patient.z = x
  if y :
    Bed_Patient.x = y
  if alfa >= 0 :
    alfa = -alfa * pi / 180
    current = XZ_Angle ( Bed_Patient.axis ) 
    origin = f2w ( Bed_Patient, Bed.pos )  
    Bed_Patient.rotate ( angle = alfa - current,
                origin = origin, axis = Y_AXIS )
    
# ************************************************************************

#scene.autoscale = True
scene.center = ( 200, 0, 200 )
Forward_Up ( ( -1, -2, -1 ), None, 900 )

# some test vectors
#v1 = varrow () 
#v2 = varrow ()
#v3 = varrow ()
#v1.pos = v3.pos = vector ( 800,0,800)

#Test = varrow () 
#Test.color = ( 1, 0, 0.5 )
#Test.pos = Console_1.vaxis.pos
#Test.axis = Console_1.vaxis.axis
#Test.axis = rotate ( Console_1.vaxis.axis, angle = pi/4, axis = Y_AXIS )

Out_Of_The_Body = False
Drag_Controls = ( Bed, Arm1_1, Arm1_2, Arm2_1, Arm2_2, Console_1.Kast, Console_2.Kast ) 

Drag   = False
Rotate = False
Move   = False 
while True :

  if scene.mouse.clicked :
    click = scene.mouse.getclick ()
    if click.pick == PH :
      Out_Of_The_Body = True 
      pbn = PB.__copy__ ()
      phn = PH.__copy__ ()
      
  if Out_Of_The_Body :
    PB.y += .6
    PH.y = PB.y
    if PB.y > 1.5 * h:
      Out_Of_The_Body = False 
  
  # It's not possible to detect Ctrl-Alt-Shift changes
  if scene.mouse.events :
    m = scene.mouse.getevent() 
    #print m.ctrl,m.shift
    if m.press and ( m.button == 'left' ) :
      #print scene.mouse.pos, scene.mouse.ray, scene.mouse.camera, '$$'
      if m.pick in Drag_Controls :
        #if m.pick == Floor :
        Ctrl  			 = m.ctrl  == 1
        Alt          = m.alt   == 1
        Shift 	     = m.shift == 1
        Drag_Object  = m.pick
        Drag         = True
        Drag_Pos     = scene.mouse.project ( normal = (0,1,0) )

        # Some objects needs to be initialized before dragging
        if Drag_Object != Bed :
          Drag_Object.Init_Mouse ()
      
    elif m.drag and Drag :
      #scene.cursor.visible = 0
      pass 

    elif m.drop :
      Drag   = False
      #scene.cursor.visible = 1

  if Drag : 
    # During drag we stil want to switch breaks
    # we can't detect Shift / Ctrl / Alt
    # therefore we replace them by z / x / c
    if scene.kb.keys > 0 :
      key = scene.kb.getkey()
      if key in 'zxc ' :
        Shift = key == 'z'
        Ctrl  = key == 'x'
        Alt   = key == 'c'
    #m = scene.mouse
    #Alt   = m.alt
    #Ctrl  = m.ctrl
    #Shift = m.shift

    New_Pos = scene.mouse.project ( normal = (0,1,0) )
    if New_Pos != Drag_Pos : 

      if Drag_Object != Bed :
        Drag_Object.Follow_Mouse ()
        
      elif Drag_Object == Bed :
        displace = New_Pos - Drag_Pos
        if Ctrl :
          Bed_Patient.pos += displace
        else :
          a1 = Drag_Pos.diff_angle ( ( 1, 0, 0) ) 
          a2 =  New_Pos.diff_angle ( ( 1, 0, 0) )
          a = 0.01
          if a1 < a2 :
            a *= -1
          angle = a * displace.mag
          origin = f2w ( Bed_Patient, Bed.pos )  
          Bed_Patient.rotate ( angle = angle,
            origin = origin, axis = Y_AXIS )
        
      Drag_Pos = New_Pos
  
