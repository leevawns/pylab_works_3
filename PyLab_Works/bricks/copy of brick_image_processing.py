# ***********************************************************************
# ***********************************************************************
from brick import *
# ***********************************************************************



# ***********************************************************************
# Base Class for the Image Library
# ***********************************************************************
class t_Brick_ImageLib ( tLWB_Brick ):

  default_Color_On  = wx.BLUE
  default_Color_Off = wx.GREEN

  # ************************************
  # __init__ of ancestor, will call after_init
  # ************************************
  def after_init ( self ):
    self.Caption = 'Image'

    # set the colors of this library
    self.Color_On  = self.default_Color_On
    #self.Color_Off = self.default_Color_Off
    
    # shape is always a block so we can define it here
    self.shape = ogl.OGL_Rectangle ( self, self.Pos )

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class tRotate ( t_Brick_ImageLib ):
  Description = """Rotates an Image,
either by the internal GUI control, or from the external signal.
Images of the following types are accepted: BMP, PNG, GIF, ..
The output format of the rotated image is the same as the input format."""

  def after_init (self):
    # Define the input pins
    # Pin-Name, Data_Type, Necessary, Description
    self.Inputs [1] = \
      ['Image In',  TIO_ARRAY, True,
       'Accepts images of the following types:\n'
       '   BMP, PNG, GIF, ...']
    self.Inputs [2] = \
      ['Rotation',  TIO_NUMBER, False,
       'The rotation ineeds not to be present (may come from internal GUI)\n'
       'Rotation is normally in the range of 0 .. 360 degrees\n'
       'Values outside this range will be taken module (360)']
    self.N_Inputs = len ( self.Inputs )

    # Define the output pins
    self.Outputs [1] = \
      ['Image Out',  TIO_ARRAY, 'Generates a rotated image in the same format as the input']
    self.N_Outputs = len ( self.Outputs )

    # Create the shape
    t_Brick_ImageLib.after_init (self)
    self.Caption = 'Rotate'
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class tShow( t_Brick_ImageLib ):
  def after_init (self):
    # Define the input pins
    # Pin-Name, Data_Type, Necessary, Description
    self.Inputs [1] = \
      ['Image In',  TIO_ARRAY, True,
       'Accepts images of the following types:\n'
       '   BMP, PNG, GIF, ...']
    self.N_Inputs = len ( self.Inputs )

    # Create the shape
    t_Brick_ImageLib.after_init (self)
    self.Caption = 'Show'
# ***********************************************************************



