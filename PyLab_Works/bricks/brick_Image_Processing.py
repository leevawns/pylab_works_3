# ***********************************************************************
# Standard libraries
# ***********************************************************************
from brick import *
from PyLab_Works_Globals import *
#from base_control        import *
from import_controls import *

# ***********************************************************************
# If color is ignored, default BLACK is selected
# ***********************************************************************
Library_Color = wx.Colour ( 50, 180, 180 )

# ***********************************************************************
# Library_Icon,
#   - can be an index in the image-list (not recommended)
#   - or the filename of an image in this directory
# ***********************************************************************
Library_Icon = 'camera_edit.png'


Description = """This is the description of the complete library.
Line 2 of ... """


# ***********************************************************************
# ***********************************************************************
class t_Read ( tLWB_Brick ):

  Description = """Reads an image from a file.
Images of the following types are accepted:
ANI, BMP, CUR, GIF, ICO, IFF, JPG, PCX, PNG, PNM, TIF, XPM """

  def After_Init (self):
    self.Caption = 'Load File'
    
    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = \
      ['Image', TIO_IMAGE,
       'Image read from the file.']

    # *************************************************
    # Create File Select
    # Range = one of the constants definied in
    #         ../support/dialog_support.py
    #       or
    #         a general file dialog mask, e.g.
    #         'dBase Files(*.db)|*.db|All Files(*.*)|*.*'
    # Parameters
    #   1 = output, filename of the selected file
    CD = self.Create_Control ( t_C_File_Open, 'Read Image File',
                               '../pictures/vippi_bricks.png' )
    CD.Range   = FT_IMAGE_FILES
    # *************************************************

  # **********************************************************************
  # this procedure is only called when inputs (or parameters) have changed
  # **********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    if Par[1] :
      Filename = os.path.join ( Application.Dir, Par[1] )
      if File_Exists ( Filename ) :
        Out[1] = wx.Image ( Filename, wx.BITMAP_TYPE_ANY )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_Rotate ( tLWB_Brick ):

  Description = """Rotates an Image counter clockwise.
The rotation angle (in degrees) and the interpolation are either taken from
the internal GUI controls, or from the external signals,
whichever has been changed last."""

  def After_Init (self):
    self.Caption = 'Rotate'
    
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = \
      ['Image', TIO_IMAGE, True,
       'Accepts images of the type wx.Image:\n']
    self.Inputs [2] = \
      ['Rotation [degrees]', TIO_NUMBER, False,
       'The rotation angle is taken modulo 360 degrees.\n'
       'If this input signal is not present,\n'
       'the rotation angle is taken from  the internal GUI.']
    self.Inputs [3] = \
      ['Interpolation', TIO_NUMBER, False,
       'If False, faster calculation,\n'
       'If True, better quality.']

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = \
      ['Image', TIO_IMAGE,
       'Rotated image in the same format as the input.']

    # Create the GUI controls
    CD = self.Create_Control ( t_C_Slider, 'Rotation [degrees]', 30 )
    CD.Range         = [ 0, 360 ]
    CD.Input_Channel = 2

    CD = self.Create_Control ( t_C_RadioBox, 'Interpolation', True )
    CD.NCol          = 1
    CD.Range         = [ 'False', 'True' ]
    CD.Input_Channel = 3

  # *********************************************************************
  # Procedure only called when inputs and/or parameters have changed
  # *********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    if In[1] != None:
      Out[1] = In[1].Rotate ( pi * Par[2] / 180, (0,0), Par[3] )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_Show( tLWB_Brick ):

  Description = """Shows the image at input[1]"""

  def After_Init (self):
    self.Caption = 'Show'
    # we want this image-window to be centered
    self.Center = True

    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = \
      [ 'Image In',  TIO_IMAGE, True, '' ]

    # Create the GUI controls
    CD = self.Create_Control ( t_C_Image_Show )
    CD.Input_Channel = 1
# ***********************************************************************
