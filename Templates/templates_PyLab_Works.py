#icon = vippi_bricks_323.png

## Brick Template
# ***********************************************************************
# ***********************************************************************
class t_MYNAME ( tLWB_Brick ) :

  Description = """Extended Description of this Brick"""

  def After_Init (self):
    self.Caption = 'My Caption'

    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = [ 'SQL', TIO_STRING, False, 'SQL query' ]

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = [ 'Meta Data', TIO_TREE, 'Tables, etc' ]

    # Create the GUI controls
    C = self.Create_Control ( Default = 'TO_pat.db' )
    C.Type    = CT_FILEOPEN
    C.Range   = FT_DBASE_FILES
    C.Caption = 'dBase FileName'

    # Temporary use the Debug Output Generator
    self.Generate_Output_Signals = \
      self.Generate_Output_Signals_Debug

  # **********************************************************************
  # **********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    # The actions of this Brick
    pass  


## Scintilla Editor
    # *************************************************
    # Create the Scintilla editor
    # Parameters
    #   1 = output, ( <complete code>, <selected code> )
    #   2 = IO_Interaction
    #         FileName  = output, the loaded code file
    #         CMD Shell = input, the local Help Browser
    C = self.Create_Control ()
    C [ 'Type' ]          = CT_EDITOR
    C [ 'Extra_Pars' ]    = 1, 2
    # *************************************************

## File Open Select
    # *************************************************
    # Create File Select
    # Range = one of the constants definied in
    #         ../support/dialog_support.py
    #       or
    #         a general file dialog mask, e.g.
    #         'dBase Files(*.db)|*.db|All Files(*.*)|*.*'
    # Parameters
    #   1 = output, filename of the selected file
    C = self.Create_Control ( Default = '../pictures/vippi_bricks.png' )
    C [ 'Type'    ] = CT_FILEOPEN
    C [ 'Range'   ] = FT_IMAGE_FILES
    C [ 'Caption' ] = 'Read Image File'
    # *************************************************


## Slider
    # *************************************************
    # Create a Slider
    C = self.Create_Control ( t_C_Slider, 'Rotation [degrees]', 30 )
    C.Range         = [ 0, 360 ]
    C.Input_Channel = 2
    # *************************************************

## Radio Buttons 
    # *************************************************
    C = self.Create_Control ( Default = True )
    C [ 'Type'          ] = CT_RADIO_BUTTON
    C [ 'NCol'          ] = 1
    C [ 'Range'         ] = [ 'False', 'True' ]
    C [ 'Caption'       ] = 'Interpolation'
    C [ 'Input Channel' ] = 3                   # if needed
    # *************************************************

## Image Display
    # *************************************************
    C = self.Create_Control ( t_C_Image_Show )
    C.Input_Channel = 1    # Connect to an input channel
                           # so the signal goes directly
                           # to the control
    # *************************************************


## CMD_Shell_Doc
    # *************************************************
    C = self.Create_Control ( Default = '' )
    C [ 'Type'         ] = CT_CMD_SHELL_DOC
    C [ 'Input Channel'] = 1
    # *************************************************


## VPython
    # *************************************************
    # Create VPython
    C = self.Create_Control ()
    C [ 'Type'          ] = CT_VPYTHON
    C [ 'Input Channel' ] = 1
    # *************************************************

## VPython Control
    # *************************************************
    # Create VPython_Control
    # Because we need an IO_Interaction,
    # We must declare "Extra_Pars"
    C = self.Create_Control ( Default = 0 )
    C [ 'Type'       ] = CT_VPYTHON_CONTROL
    C [ 'Extra_Pars' ] = 1
    # *************************************************


##-

## Main Tests
# ***********************************************************************
"""
This is the prefered way to create tests in Main
Test_Defs + Test prints Test-header and does administration
First define which tests should be performed
Then define what should be tested for each number
"""
  Test_Defs ( 1,  3 )
  if Test ( 1 ) :


##-

## Version - header
# ***********************************************************************
"""
If the module has run standalone and
is located in a different path from language_support
be sure we can reach language_support
"""
import __init__

from language_support import  _
__doc__ = _(0,"""
Doc string
""")

_Version_Text = [
[ 1.0 , '32-10-2008', 'Stef Mientki',
'Test Conditions:', ( 2,3, ),
_(0, ' - original release')]
]

from General_Globals import *
# ***********************************************************************

## Main GUI
# ***********************************************************************
# ***********************************************************************
class Simple_Test_Form ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Simple GUI Demo', ini )

    GUI = """
    Splitter1       ,SplitterVer
      Panel_Top     ,wx.Panel
      Panel_Bottom  ,wx.Panel
        Button_1    ,wx.Button,  label = "Test"
        Button_2    ,wx.Button,  label = "Test2", pos = (100,0)
    """
    self.wxGUI = Create_wxGUI ( GUI )

# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  My_Main_Application ( Simple_Test_Form )
# ***********************************************************************
pd_Module ( __file__ )


## PyLab_Works GUI
# If the module has run standalone and
# is located in a different path from language_support
# be sure we can reach language_support
import __init__

from language_support import  _
__doc__ = _(0,"""
Doc string
""")

_Version_Text = [
[ 1.0 , '32-10-2008', 'Stef Mientki',
'Test Conditions:', ( 2,3, ),
_(0, ' - original release')]
]

from General_Globals import *
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class Simple_Test_Form ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Simple GUI Demo', ini )

    GUI = """
    Splitter1       ,SplitterVer
      Panel_Top     ,wx.Panel
      Panel_Bottom  ,wx.Panel
        Button_1    ,wx.Button,  label = "Test"
        Button_2    ,wx.Button,  label = "Test2", pos = (100,0)
    """
    self.wxGUI = Create_wxGUI ( GUI )

# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  My_Main_Application ( Simple_Test_Form )
# ***********************************************************************
pd_Module ( __file__ )


