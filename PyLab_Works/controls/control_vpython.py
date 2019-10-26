import __init__
from vpython import *
#from visual import *

import __init__
from base_control import *
#from base_control import _tScenery_Base

import os, sys
from language_support import  _
# ***********************************************************************
__doc__ = _(0, """
doc_string translated ?
""" )

# ***********************************************************************
_Version_Text = [

[ 0.1 , '24-10-2008', 'Stef Mientki',
'Test Conditions:', ( 2, ),
_(0, ' - orginal release')]
]


import sys
import os

import PyLab_Works_Globals as PG
from   PyLab_Works_Globals import *

# ***********************************************************************
# This code must be here, otherwise we don't have the global "visual"
# when we run through PG.P_Globals this could be placed anywhere
# ***********************************************************************
class _tScenery_Base_weg ( My_Control_Class ):
  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    GUI = """
      self.p1  ,wx.Panel
    """
    self.wxGUI = Create_wxGUI ( GUI, my_parent = 'self.Dock' )
    self.Script_Error = False

    self.Init_Code_Before_weg = """
#from __future__ import division  doesn't seem to work here
import visual
from visual import *
import __init__
from visual_support import *

#print Active_Project_Filename
import sys, os
#path = os.path.join ( Application.Dir, PG.Active_Project_Filename, 'Libs')
#, path


# remove all previous objects
for object in visual.scene.objects:
  object.visible = False
  #del object #NOT ALLOWED !!

#scene.fov = pi / 3

# DEFAULTS VALUES FROM THE MANUAL:
scene.center = ( 0, 0, 0 )

#scene.forward = ( 0, 0, -1 )
#scene.up      = ( 0, 1,  0 )
Forward_Up ( (0,0,-1), ( 0,1,0) )


# To distingish between VP3 and VP5
from General_Globals import Application
if Application._VPython_Version == 5 :
  NewAxis = newaxis

scene.userzoom = True
scene.userspin = True
scene.background = ( 0, 0, 0 )
scene.range = ( 10, 10, 10 )
scene.ambient = 0.2
scene.lights = [ (0.17, 0.35, 0.7), (-0.26, -0.07, -0.13 ) ]

PW_Embed = True
if not ( My_Path in sys.path ) :
  sys.path.append ( My_Path )
"""

    self.Code_Globals = {}
    self.Init_Code_Before = None
    self.Init_Code_After  = None
    self.Loop_Code_Before = None
    self.Loop_Code_After  = None


  # *********************************************************
  # *********************************************************
  def Start_Script ( self, Code ) :
    #PG.P_Globals = {}
    
    Init_Code, self.VPC_Code, self.Loop_Code = \
      Split_Init_Code ( Code, self, self.Code_Globals ) #PG.P_Globals )

    """
    v3print ( '======= INIT ======' )
    v3print ( Init_Code )
    v3print ( '======= VPython Control Code ======' )
    v3print ( self.VPC_Code )
    v3print ( '======= Loop ======' )
    v3print ( self.Loop_Code )
    v3print ( '======= END Loop ======' )
    """

    # Add own Library directory to the namespace
    path = os.path.join ( Application.Dir, PG.Active_Project_Filename, 'Libs' )
    #PG.P_Globals [ 'My_Path' ] = path + '/'
    self.Code_Globals [ 'My_Path' ] = path + '/'

    # The init code is executed separately
    # to get the correct line number for error messages
    if self.Init_Code_Before :
      try :
        exec ( self.Init_Code_Before, self.Code_Globals ) #PG.P_Globals )
      except :
        pass
      
    try :
      exec ( Init_Code, self.Code_Globals ) #PG.P_Globals )
      self.Script_Error = False
    except :
      import traceback
      traceback.print_exc ( 5 )
      print ('******** SCENE Code Editor, ERROR: *********')

  # *********************************************************
  # *********************************************************
  def Execute_Script ( self ) :
    # The Pre-Loop code is executed separately
    # to get the correct line number for error messages
    if self.Loop_Code_Before :
      try :
        exec ( self.Loop_Code_Before, self.Code_Globals )
      except :
        pass

    if self.Loop_Code :
      try :
        exec ( self.Loop_Code, self.Code_Globals ) # PG.P_Globals )
        self.Script_Error = False
      except :
        if not  ( self.Script_Error ) :
          self.Script_Error = True
          import traceback
          traceback.print_exc ( 5 )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_C_VPython_Control ( My_Control_Class ):
  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    # Set Par to a Dictionairy
    self.EP_IsDict = [ True ]

    GUI = """
      self.Panel  ,wx.ScrolledWindow
    """
    self.wxGUI = Create_wxGUI ( GUI, my_parent = 'self.Dock' )
    self.Buttons = []
    self.Texts   = []
    self.Sliders = []

    self.Panel.Bind ( wx.EVT_SIZE, self._On_Size )
    #self.Define ( 1, 0 )

  #*************************************************
  #*************************************************
  def Set_Button ( self, N, Caption, Completion ) :
    #print 'SETBUTTON'
    self.Buttons[N].SetLabel ( Caption )
    self.Buttons[N].Bind ( wx.EVT_BUTTON, Completion )

  #*************************************************
  #*************************************************
  def Set_Text ( self, N, Caption, Completion = None ) :
    self.Texts[N].SetValue ( Caption )
    # NOT SURE WHICH EVENT TO SUPPORT HERE
    if Completion :
      self.Texts[N].Bind ( wx.EVT_TEXT, Completion )
      self.Texts[N].Bind ( wx.EVT_LEFT_DOWN, Completion )

  #*************************************************
  #*************************************************
  def Set_Slider ( self, N, Caption,
                   Min, Max, Value,
                   LinLog, Format, Completion ):
    self.Sliders[N].Set_Params (
      Caption, Min, Max, Value, LinLog, Format, Completion )

  #*************************************************
  #*************************************************
  def _On_Size ( self, event = None ) :
    if event :
      event.Skip ()
    x = 0
    w = event.GetSize () [0] - 15
    if len ( self.Buttons ) > 0 :
      x += 75
    w -= x
    for Text in self.Texts :
      Text.SetPosition ( ( x, -1 ) )
      Text.SetSize     ( ( w, -1 ) )
    for Slider in self.Sliders :
      Slider.SetPosition ( ( x, -1 ) )
      Slider.SetSize     ( ( w, -1 ) )

  #*************************************************
  #*************************************************
  def Define ( self, N_Button = 0, N_Slider = 0, N_Text = 0 ) :
    # Correct the number of buttons
    N = len ( self.Buttons )
    BH = 25
    BW = 75
    if N_Button < N :
      for i in range ( N - N_Button ) :
        Button = self.Buttons.pop ()
        Button.Hide ()
        del Button
    elif N_Button > N :
      for i in range ( N_Button - N ) :
        N += 1
        Button = wx.Button ( self.Panel, label = 'Button ' + str ( N ),
                             pos= ( 0, (N-1)*BH ) )
        self.Buttons.append ( Button )

    # Calculate X-pos of texts and sliders
    x = 0
    if N_Button > 0 :
      x = 75

    # Correct the number of Text labels
    T = len ( self.Texts )
    TH = 20
    TW = 75
    if N_Text < T :
      for i in range ( T - N_Text ) :
        Text = self.Texts.pop ()
        Text.Hide ()
        del Text
    elif N_Text > T :
      for i in range ( N_Text - T ) :
        T += 1
        Text = wx.TextCtrl ( self.Panel, -1, 'Text ' + str ( T ),
          pos  = ( x, (T-1)*TH ),
          size = ( self.Panel.GetSize () [0] - x, TH ) )
        self.Texts.append ( Text )

    from float_slider import Float_Slider
    N = len ( self.Sliders )
    SH = 55
    Y_Off = T * TH
    if N_Slider < N :
      for i in range ( N - N_Slider ) :
        Slider = self.Sliders.pop ()
        Slider.Hide ()
        del Slider
    elif N_Slider > N :
      for i in range ( N_Slider - N ) :
        N += 1
        Slider = Float_Slider ( self.Panel,
           caption  = 'Slider' + str (N),
           pos = ( x, Y_Off + (N-1) * SH ),
           size = ( self.Panel.GetSize () [0] - x, SH ) )
        if ( T + N ) % 2 == 0 :
          Slider.SetForegroundColour ( wx.BLUE )
        self.Sliders.append ( Slider )

    maxH = max ( N_Button * BH, N_Text * TH + N_Slider * SH )
    self.Panel.SetScrollbars ( 1, 1, 10, maxH )

    # Repositioning and resizing doesn't happen automatically
    # SendSizeEvent doesn't work either
    if maxH > self.Panel.GetSize () [1] :
      Scroll = 15
    else :
      Scroll = 0
    for Slider in self.Sliders :
      Slider.SetSize ( ( self.Panel.GetSize () [0] - x - Scroll, -1 ) )
      Slider.SetPosition ( ( x, -1 ) )

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_C_VPython ( tScenery_Base ):
  def __init__ ( self, *args, **kwargs ):
    #print 'VPVP', self, args, kwargs
    #import visual
    tScenery_Base.__init__ ( self, *args, **kwargs )

    self.Init_Code_Before= """
#from __future__ import division  doesn't seem to work here
import visual
from visual import *
import __init__
from visual_support import *

#print Active_Project_Filename
import sys, os
#path = os.path.join ( Application.Dir, PG.Active_Project_Filename, 'Libs')
#, path


# remove all previous objects
for object in visual.scene.objects:
  object.visible = False
  #del object #NOT ALLOWED !!

#scene.fov = pi / 3

# DEFAULTS VALUES FROM THE MANUAL:
scene.center = ( 0, 0, 0 )

#scene.forward = ( 0, 0, -1 )
#scene.up      = ( 0, 1,  0 )
Forward_Up ( (0,0,-1), ( 0,1,0) )


# To distingish between VP3 and VP5
from General_Globals import Application
if Application._VPython_Version == 5 :
  NewAxis = newaxis

scene.userzoom = True
scene.userspin = True
scene.background = ( 0, 0, 0 )
scene.range = ( 10, 10, 10 )
scene.ambient = 0.2
scene.lights = [ (0.17, 0.35, 0.7), (-0.26, -0.07, -0.13 ) ]

PW_Embed = True
if not ( My_Path in sys.path ) :
  sys.path.append ( My_Path )
"""


    self.Linux_Message = False

    # create a VPython application, just an copy of the Ball-demo
    visual.scene.title = 'PyLab Works VPython'
    #floor = visual.box (pos=(0,0,0), length=4, height=0.5, width=4, color=visual.color.blue)
    #ball = visual.sphere()
    #visual.scene.show()
    visual.scene.exit = False
    #ball  = visual.sphere (pos=(0,4,0), radius=1, color=visual.color.red)
    #ball.velocity = visual.vector(0,-1,0)
    #dt = 0.01

    # initialize the State_Machine and start the timer
    self.VP_State = 0
    self.Old_Size = ( 0, 0 )
    self.Timer = wx.Timer ( self.Dock )
    # the third parameter is essential to allow other timers
    self.Dock.Bind ( wx.EVT_TIMER, self._On_Timer, self.Timer)
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

    # if we didn't find the VPython window previous time
    elif self.VP_State == 4 :
      wx.CallLater ( 10, self.Fetch_VP )

  # *****************************************************************
  # Recreate and Position the VPython window
  # *****************************************************************
  def Fetch_VP ( self ) :
    w = self.Old_Size[0]
    h = self.Old_Size[1]

    if Platform_Windows :
      import win32gui, win32con
      # Try to find the newly created VPython window
      # which is now a main-application-window
      self.VP = win32gui.FindWindow ( None, visual.scene.title ) #'VPython' )

      if self.VP:
        # reset the State Machine
        self.VP_State = 0

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
        #win32gui.MoveWindow ( self.VP, -4, -22, w+8, h+26, True )
        
        # Dock the VPython window
        win32gui.SetParent ( self.VP, PP )

    else :  # not Windows
      self.VP_State = 0
      if not ( self.Linux_Message ) :
        self.Linux_Message = True
        line = """
In this panel the Vpython window
should be captured.
Unfortunately I don't know
how to accomplsh this
under Linux / Mac
"""
        self.Message = wx.StaticText ( self.p1 )
        self.Message.SetLabel ( line )
        #self.Message = wx.TextCtrl ( self.p1, style = wx.TE_MULTILINE | wx.TE_READONLY )
        #self.Message.AppendText ( line )

  def Kill ( self ) :
    self.Timer.Stop ()
    visual.scene.visible = False

# ***********************************************************************

