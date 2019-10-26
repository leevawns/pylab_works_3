# ***********************************************************************
# ***********************************************************************
from brick import *
from math import pi
from dialog_support import *
from PyLab_Works_Globals import *
#from base_control        import *
from import_controls import *
import wx
# ***********************************************************************

# If color is ignored, default BLACK is selected
Library_Color = wx.Colour ( 180, 180, 50 )

# Library_Icon,
#   - can be an index in the image-list (not recommended)
#   - or the filename of an image in this directory
Library_Icon = 'people-581.png'


# ***********************************************************************
# ***********************************************************************
class t_Switch_Single ( tLWB_Brick ):

  Description = """One Pole Switch"""

  def After_Init (self):
    self.Caption = 'Switch Single'
    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = \
      ['Output', TIO_NUMBER,
       'If the Switch is down, connection is made between Input and Output.']

    # Create the GUI controls
    CD = self.Create_Control ( t_C_Buttons, 'LED1', False )

  # **********************************************************************
  # this procedure is only called when inputs (or parameters) have changed
  # **********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    pass
    #if self.Params[1] != None :
    #  self.Output_Value[1] = self.Params [1]
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class t_LED ( tLWB_Brick ):

  Description = """Displays a LED"""

  def After_Init (self):
    self.Caption = 'LED'
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = \
      ['Current In', TIO_NUMBER, True,'']

    # Create the GUI controls
    CD = self.Create_Control ( t_C_LED )
    CD.Input_Channel = 1
# ***********************************************************************

