#icon = vippi_bricks_323.png
## Version - header
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
# ***********************************************************************
_ToDo = """
"""
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

# ***********************************************************************
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


