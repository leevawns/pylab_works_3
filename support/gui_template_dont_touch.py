from gui_support import *

# ***********************************************************************
# ***********************************************************************
class Simple_Test_Form ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Simple GUI Demo', ini )

    GUI = """
%%%"""
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
