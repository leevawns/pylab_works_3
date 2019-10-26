# ***********************************************************************
# device.py will take care of all imports
# ***********************************************************************
from brick import *
# ***********************************************************************


# ***********************************************************************
# simulates a LED
# in a digital manner, i.e. Anode and Cathode are booleans
# ***********************************************************************
class t_unknown ( tLWB_Brick ):

  # ************************************
  # __init__ of ancestor, will call init
  # ************************************
  def init (self):
    i = 220
    self.Color_On = (i,i,i) 
    #i = 140
    #self.Color_Off = (i,i,i)
    self.On = False

    # create the visual shape
    if self.Size[0]<100: self.Size[0] = 100
    if self.Size[1]<30: self.Size[1] = 30
    self.shape = ogl.RectangleShape(self.Size[0],self.Size[1])
# ***********************************************************************


# ***********************************************************************
# When this file is ran as the "mainfile"
# The device can simply be tested,
# by just creating one or more instances of the device,
# without affecting the main JALsPy settings
# ***********************************************************************
if __name__ == "__main__":
  from JALsPy import Run_JALsPy_Application
  # specify a filename, so we don't interrupt with normal JALsPy settings
  Run_JALsPy_Application ( 'testapp_unknown.ini' )
# ***********************************************************************

