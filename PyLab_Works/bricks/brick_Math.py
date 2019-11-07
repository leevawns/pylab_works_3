# ***********************************************************************
from PyLab_Works_Globals import *
from language_support import _
#from base_control        import *
from import_controls import *
from path_support import *
# ***********************************************************************


__doc__ = """
# ***********************************************************************
# control_scope.py : a fast plot library for real-time signals.
# This plot library is more like a oscilloscope than like MatPlot.
# This library should be faster than MatPlot, PyPlot and FloatCanvas.
# This library has some extra features:
#   - measurement cursor
#   - no scaling in X-axis, so you'll see all samples
#   - storage all settings in a ini-file
#   - scaling and offset is set for each individual signal
#   - Time history window for 1 signal with min/max display
#   - set attributes for all signals at once
#   - border values on top and bottom
#   -
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007 Stef Mientki
# mailto:S.Mientki@ru.nl
#
# Problems / Bugs / Limitations
#  - doubleclick on form caption, maximizes the form,
#    now closing the form will store these maxima and you never get back
#    maybe we should another window type instead of the miniframe
#
"""

_Version_Text = [
[ 0.4, '10-02-2008', 'Stef Mientki',
'Test Conditions:', (1,2),
_(12, """
   - scaling and offset is set for each individual signal
   - Time history window for 1 signal with min/max display
   - set attributes for all signals at once
   - border values on top and bottom
   - second measurement cursor
""") ],


[ 0.3, '29-01-2008', 'Stef Mientki',
'Test Conditions:', (1,),
_(0, """
   - some more changes
   - and even more changes
""" ) ],


[ 0.2, '20-01-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
   - some changes
""" ) ],


[ 0.1, '04-11-2007', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
    - orginal release
""" ) ]
]
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
from brick import *
# ***********************************************************************

 
# ***********************************************************************
# Library_Icon,
#   - can be an index in the image-list (not recommended)
#   - or the filename of an image in this directory
# ***********************************************************************
Library_Icon = 'brick_math_icon.PNG'
Library_Color = wx.Colour ( 200, 0, 200 )


Description = _(11, 'Library with basic math functions.' )
 
# ***********************************************************************
# ***********************************************************************
class t_addition ( tLWB_Brick ):
  Description = _(2, 'Add two numbers' )
 
  def After_Init (self):   
    self.Caption = '+'
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = [ _(3, 'First Number') , TIO_NUMBER, True ]
    self.Inputs [2] = [ _(4, 'Second number'), TIO_NUMBER, True ]
   
    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = [_(5, 'Sum'), TIO_NUMBER]
   
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    if In[1] and In[2] :
      Out[1] = In[1] +  In [2]
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************

class t_Numeric_Display( tLWB_Brick ):
  Description = _(6, 'Display a number' )


  def After_Init(self):
    self.Caption = _(8, 'DisplayNum' )
    # Define the input pins
    self.Inputs [1] = [ _(7, 'Number to display'), TIO_NUMBER ]

    # Create the GUI controls
    CD = self.Create_Control ( t_C_Static_Text )
    CD.Caption       = _(9, 'Displayed Number' )
    CD.FontSize      = 40
    CD.FontColor     = wx.BLUE
    CD.Input_Channel = 1
# ***********************************************************************
       

# ***********************************************************************
# ***********************************************************************
class t_Numeric_Control( tLWB_Brick ):
  Description = _(10, 'User can enter a number' )
 
  def After_Init(self):  
    self.Caption = _(1, 'Number' )
    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = [ _(1, 'Number'), TIO_NUMBER ]
 
    # Create the GUI controls, Creation order is Display order
    # <control type>, self, <input channel or None>
    #    <caption>, <hinttext>,
    #       <value>, <range>, <other control specific information>
    # Create the GUI controls
    CD = self.Create_Control ( t_C_Text_Control, _(1, 'Number') )
    CD.Value   = str(0) #self.Params[1] = str(0)
 
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    if(Par[1] == ""):
      Out[1] = 0.0
    else:
      Out[1] = float(Par[1])
# ***********************************************************************