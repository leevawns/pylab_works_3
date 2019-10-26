import __init__
import wx

"""
import sys
subdirs = [ '../support' ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
"""

from gui_support import *
from system_support import run

# ***********************************************************************
# ***********************************************************************
class Simple_Test_Form ( wx.MiniFrame ):
  def __init__ ( self ):
    wx.MiniFrame.__init__( self, None, style = wx.DEFAULT_FRAME_STYLE  )

    GUI = """
    self.Splitter_Plots    ,SplitterVer
      Panel1        ,PanelVer, 01  ,name  = "Hello"
        Button_1    ,wx.Button     ,label = "Test"
        self.KeyB   ,wx.TextCtrl   ,style = wx.TE_MULTILINE | wx.TE_PROCESS_ENTER
      Panel2        ,PanelVer, 11  ,name  = "Page2"
        self.Log    ,wx.TextCtrl   ,style = wx.TE_MULTILINE | wx.TE_PROCESS_ENTER
    """
    exec ( Create_wxGUI ( GUI ) )

    self.KeyB.Bind ( wx.EVT_TEXT_ENTER, self.On_Enter_Key )
    self.Bind ( wx.EVT_BUTTON, self.B )
    self.process = None
    self.Bind(wx.EVT_IDLE, self.OnIdle)

  def On_Enter_Key ( self, event ) :
    print event.GetString()
    self.process.GetOutputStream().write(event.GetString() + '\n')

  def OnIdle(self, evt):
    if self.process is not None:
      stream = self.process.GetInputStream()
      if stream.CanRead():
        text = stream.read()
        print 'POP',text
        self.Log.AppendText(text)

  def B ( self, event ):
    cmd = 'python -u -m pdb test_IDE.py"'
    self.process = wx.Process(self)
    self.process.Redirect();
    pid = wx.Execute(cmd, wx.EXEC_ASYNC, self.process)
# ***********************************************************************


# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  app = wx.PySimpleApp ()
  frame = Simple_Test_Form ()
  frame.Show ( True )
  app.MainLoop ()
# ***********************************************************************

