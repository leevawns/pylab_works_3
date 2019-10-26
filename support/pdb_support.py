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
class New_PDBx ( object ) :
  # *********************************************************
  # *********************************************************
  def __init__ ( self, Owner ) :
    self.Owner    = Owner
    self.filename = None
    self.Started  = False
    self.process  = None
    self.Owner.Bind ( wx.EVT_IDLE, self.OnIdle )

  # *********************************************************
  # *********************************************************
  def OnIdle(self, evt):
    if self.process and  self.process.IsInputOpened() :
      stream = self.process.GetInputStream()
      if stream.CanRead():
        print '==ONIDLE'
        text  = stream.read()
        lines = text.split ( '\n' )
        for line in lines :
          if line.find ( '<bp>' ) == 0 :
            i = line.find ( '\t' )
            filename = line [ 4 : i ]
            lineno   = int ( line [ i+1 : ].strip() )

            self.Owner.Leave_Editor_On_BP ()
            self.Owner.Callback_Load_Editor ( filename, lineno )

          # Step over Call and Return
          elif ( line.find ( '--Call--' )   == 0 ) or \
               ( line.find ( '--Return--' ) == 0 ) :
            self.process.GetOutputStream().write( 's\n' )

          elif line :
            self.Owner.Log_Cmd.AppendText ( line + '\n' )


  # *********************************************************
  # *********************************************************
  def Start_Debug_Application ( self, filename ) :
    if not ( self.filename ) and filename :
      ##filename = '../PyLab_Works/test_IDE.py'
      filename = '../PyLab_Works/test_IDE.py'
      self.filename = filename
      #print 'FF',filename

      debugger = 'pdb_my' #'../Lib_Extensions'
                       #'../Lib_Extensions/my_pdb.py'
      cmd = 'python -u -m ' + debugger + ' ' + filename
      self.process = wx.Process ( self.Owner )
      #self.process.OnTerminate = self.My_Terminate
      self.process.Redirect()
      pid = wx.Execute ( cmd, wx.EXEC_ASYNC, self.process )
      self.Started = True

  #def My_Terminate ( self, PID, Status ) :
  #  print 'Terminate', PID, Status

  # *********************************************************
  # *********************************************************
  def Stop_Debug_Application ( self ) :
    self.Started = False
    """
    while Kill_Process ( 'cmd' ) :
      time.sleep ( 0.1 )
    while Kill_Process ( 'python' ) :
      time.sleep ( 0.1 )
    """

  # *********************************************************
  # *********************************************************
  def Step ( self ) :
    self.process.GetOutputStream().write( 's\n' )

  # *********************************************************
  # *********************************************************
  def Go ( self ) :
    pass #self.process.GetOutputStream().write( 's\n' )

  # *********************************************************
  # *********************************************************
  def Put_Command ( self, line ) :
    print '==PUT',line
    if self.process :
      if line.find ( '>' ) == 0 :
        #wx.Process_Exists(pid)
        self.process.GetOutputStream().write( line [ 1: ] )
        if line[1]=='q' :
          self.process = None
      else :
        print 'OOOO',line
        self.process.GetOutputStream().write( line + '\n' )
        #self.process.GetOutputStream().write( 'eval ' + line + '\n' )
        #self.Eval_Error = 'exec ' + line + '\n'

# ***********************************************************************


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
    #exec ( Create_wxGUI ( GUI ) )
    self.wxGUI = Create_wxGUI ( GUI )

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
    cmd = 'python -u -m pdb D:/Data_Python_25/PyLab_Works/test_IDE.py"'
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
pd_Module ( __file__ )

