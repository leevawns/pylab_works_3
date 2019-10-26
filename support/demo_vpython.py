import wx
import visual

# ***********************************************************************
# ***********************************************************************
def My_Main_Application ( My_Form ) :
  app = wx.PySimpleApp ()
  frame = My_Form ( )
  frame.Show ( True )
  app.MainLoop ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Simple_Test_Form ( wx.Frame ):
  def __init__ ( self, ini = None ) :
    wx.Frame.__init__ ( self, None )

    self.Splitter=wx.SplitterWindow( self)
    self.p1=wx.Panel( self.Splitter)
    self.p2=wx.Panel( self.Splitter)
    self.Splitter.SplitVertically ( self.p1, self.p2 )
    self.Splitter.SetMinimumPaneSize(20)
    Sizer = wx.BoxSizer ( )
    Sizer.Add ( self.Splitter, 1, wx.EXPAND )
    self.SetSizer ( Sizer )

    # create a VPython application, just an copy of the Ball-demo
    floor = visual.box (pos=(0,0,0), length=4, height=0.5, width=4, color=visual.color.blue)
    ball  = visual.sphere (pos=(0,4,0), radius=1, color=visual.color.red)
    ball.velocity = visual.vector(0,-1,0)
    dt = 0.01

    # initialize the State_Machine and start the timer
    self.VP_State = 0
    self.Old_Size = ( 0, 0 )
    self.Timer = wx.Timer ( self )
    # the third parameter is essential to allow other timers
    self.Bind ( wx.EVT_TIMER, self._On_Timer, self.Timer)
    self.Timer.Start ( 100 )

  # *****************************************************************
  # *****************************************************************
  def _On_Timer ( self, event ) :
    size = self.p1.GetSize ()

    # Rest, wait till a resize is detected
    if self.VP_State == 0 :
      if size != self.Old_Size :
        self.Old_Size = size
        self.VP_State = 1
        visual.scene.visible = False

    # wait in this state until size remains stable
    elif self.VP_State == 1 :
      if size != self.Old_Size :
        self.Old_Size = size
      else :
        self.VP_State = 2

    # do an extra test if size is still unchanged
    elif self.VP_State == 2 :
      if size != self.Old_Size :
        self.Old_Size = size
        self.VP_State = 1
      else :
        self.VP_State = 3

    # now the size is stable for at least 2 clock cycli
    # so it's time to recreate the VPython window
    elif self.VP_State == 3 :
      visual.scene.visible = True
      wx.CallLater ( 10, self.Fetch_VP )
      self.VP_State = 4

  # *****************************************************************
  # Recreate and Position the VPython window
  # *****************************************************************
  def Fetch_VP ( self ) :
    import win32gui, win32con

    # Try to find the newly created VPython window
    # which is now a main-application-window
    self.VP = win32gui.FindWindow ( None, 'VPython' )

    if self.VP:
      w = self.Old_Size[0]
      h = self.Old_Size[1]

      # get the handle of the dock container
      PP = self.p1.GetHandle ()

      # Set Position and Size of the VPython window,
      # Before Docking it !!
      #flags = win32con.SWP_ASYNCWINDOWPOS or \
      #        win32con.SWP_SHOWWINDOW     or \
      #        win32con.SWP_FRAMECHANGED
      flags = win32con.SWP_SHOWWINDOW or \
              win32con.SWP_FRAMECHANGED
      win32gui.SetWindowPos ( self.VP, win32con.HWND_TOPMOST,
                              -4, -22, w+8, h+26, flags )

      # Dock the VPython window
      win32gui.SetParent ( self.VP, PP )

      # reset the State Machine
      self.VP_State = 0
# ***********************************************************************


# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  My_Main_Application ( Simple_Test_Form )
# ***********************************************************************
