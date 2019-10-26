# ***********************************************************************
# ***********************************************************************
from brick import *
# ***********************************************************************



# ***********************************************************************
# Base Class for the Image Library
# ***********************************************************************
class tBrick_ShapesLib ( tLWB_Brick ):

  default_Color_On = wx.RED
  default_Color_Off = wx.GREEN

  # ************************************
  # ************************************
  def After_Init ( self ):
    self.Caption = 'Shapes'

    # create the visual shape
    self.Color_On  = self.default_Color_On
    #self.Color_Off = self.default_Color_Off

# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class t_Simplest ( tBrick_ShapesLib ):
  pass
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_Rectangle ( tBrick_ShapesLib ):

  # ************************************
  # __init__ of ancestor, will call After_Init
  # ************************************
  def After_Init (self):
    tBrick_ShapesLib.After_Init (self)

    # create the visual shape
    #self.shape = ogl.Rectangle ( self, self.Pos )
# ***********************************************************************


