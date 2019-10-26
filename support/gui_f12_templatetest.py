import __init__
from gui_support import *

# ***********************************************************************
# ***********************************************************************
class Simple_Test_Form ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Simple GUI Demo', ini )

    GUI = """
      self.SplitV         ,SplitterVer
        self.Edit         ,Base_STC
        self.Edit2         ,Base_STC
    """
    #from Scintilla_support import Base_STC
    self.wxGUI = Create_wxGUI ( GUI, IniName = 'self.Ini_File' )
    # **********************************************************************
    #print self.wxGUI.code
    # some text
    self.wxGUI.Ready()

    self.Bind          ( wx.EVT_CLOSE,        self.On_Close    )

  # *****************************************************
  def On_Close ( self, event ) :
    if self.Ini_File :
      self.Ini_File.Section = self.Ini_Section
      self.wxGUI.Save_Settings ()
    event.Skip()

# ***********************************************************************
if __name__ == '__main__':
  My_Main_Application ( Simple_Test_Form )
