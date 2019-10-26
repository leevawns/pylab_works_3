import __init__
from base_control import *
#from base_control import _tScenery_Base

# ***********************************************************************
# <Description>
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007 <author>
# mailto: ...
# Please let me know if it works or not under different conditions
#
# <Version: x.y    ,dd-mm-yyyy, <author>
# Test Conditions: 1
#    - orginal release
#
# Test Conditions
# 1. WinXP-SP2, Python 2.4.3, wxPython wx-2.8-msw-ansi
# ***********************************************************************


"""
import os
import sys
subdirs = [ '../support' ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
"""

# !!! import wx before any support library !!!
# otherwise the IDE won't do auto-suggest
import wx

print ('*************AL1')
import PyLab_Works_Globals as PG
print ('*************AL1')

from   dialog_support  import *
from   inifile_support import *
from   gui_support     import *
import OGLlike as ogl
import ogl_2D

from numpy import arange, pi, sin, arctan, sqrt

# ***********************************************************************
# This code must be here, otherwise we don't have the global "visual"
# when we run through PG.P_Globals this could be placed anywhere
# ***********************************************************************
class _tScenery_Base2_weg ( My_Control_Class ):
  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    GUI = """
      self.p1  ,wx.Panel
    """
    self.wxGUI = Create_wxGUI ( GUI, my_parent = 'self.Dock' )

    self.Script_Error     = False
    self.Init_Code_Before = None
    self.Init_Code_After  = None
    self.Loop_Code_Before = None
    self.Loop_Code_After  = None


  # *********************************************************
  # *********************************************************
  def Start_Script ( self, Code ) :
    Init_Code, self.VPC_Code, self.Loop_Code = \
      Split_Init_Code ( Code, self, self.Code_Globals )

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
    self.Code_Globals [ 'My_Path' ] = path + '/'

    # The Pre-Init code is executed separately
    # to get the correct line number for error messages
    if self.Init_Code_Before :
      try :
        exec ( self.Init_Code_Before, self.Code_Globals )
      except :
        pass

    try :
      exec ( Init_Code, self.Code_Globals )
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
        exec ( self.Loop_Code, self.Code_Globals )
        self.Script_Error = False
      except :
        if not  ( self.Script_Error ) :
          self.Script_Error = True
          import traceback
          traceback.print_exc ( 5 )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_C_2D_Scene ( tScenery_Base ):
  def __init__ ( self, *args, **kwargs ):
    tScenery_Base.__init__ ( self, *args, **kwargs )

    #self.Code_Globals = {}
    self.Code_Globals [ 'self'              ] = self
    self.Code_Globals [ 'Set_Coordinates'   ] = self.Set_Coordinates
    self.Code_Globals [ 'Create_Axis'       ] = self.Create_Axis
    self.Code_Globals [ 'Create_Grid'       ] = self.Create_Grid
    self.Code_Globals [ 'Create_Text'       ] = self.Create_Text
    self.Code_Globals [ 'Create_Points'     ] = self.Create_Points
    self.Code_Globals [ 'Create_Function'   ] = self.Create_Function
    self.Code_Globals [ 'Create_Line'       ] = self.Create_Line
    self.Code_Globals [ 'Create_Arrow'      ] = self.Create_Arrow
    self.Code_Globals [ 'Create_Circle'     ] = self.Create_Circle
    self.Code_Globals [ 'Create_Button'     ] = self.Create_Button
    self.Code_Globals [ 'Create_Rectangle'  ] = self.Create_Rectangle
    self.Code_Globals [ 'Create_Free_Shape' ] = self.Create_Free_Shape

    self.Init_Code_Before  = 'self._Trail_Count = -1 \n'
    self.Init_Code_Before += 'self.Trail_Count = 5\n'

    self.Loop_Code_Before  = 'self._Trail_Count += 1 \n'
    self.Loop_Code_Before += 'if (self._Trail_Count % self.Trail_Count) == 0 :\n'
    self.Loop_Code_Before += '  self.Canvas.Add_Trail ()\n'

    self.Loop_Code_After   = 'self.Canvas.Refresh()\n'

    #print Dock,Brick,Test,ini
    
    # create the wx-components here and
    self.Canvas = ogl.ShapeCanvas ( self.Dock, pos=(0,0), size=(500,500) )
    #self.Canvas.SetBackgroundColour ( wx.RED )
    Sizer = wx.BoxSizer ( wx.VERTICAL )
    self.Dock.SetSizer ( Sizer )
    Sizer.Add ( self.Canvas, 1, wx.EXPAND )
    #self.Dock.SendSizeEvent ()

    # Create a diagram and assign it to the Canvas
    self.diagram = ogl.Diagram ()
    self.Canvas.SetDiagram ( self.diagram )

    """
    # uniform coordinate system with WH
    self.Set_Coordinates (
        ( -100, -100 ), ( 200, None ) )

    # uniform coordinate system with RT
    self.Set_Coordinates (
        ( -100, -100 ), RT = ( 100, None ) )

    # non-uniform coordinate system with WH
    self.Set_Coordinates (
        ( -100, -100 ), ( 200, 200 ) )
    shape = self.Create_Axis ( 0,  0 )

    shape = self.Create_Rectangle ( (20,30) , RT = (60,70) )
    shape.Color = wx.BLUE
    """

    """
    self.Set_Coordinates (
        ( -10, -10 ), RT = ( 100, None ) )
    shape = self.Create_Axis ( 0,  0 )
    shape.Line_Width = 2
    shape = self.Create_Grid ( 20 )


    shape = self.Create_Text ( 'test1', (30,20))
    shape.Line_Width = 1
    shape = self.Create_Text ( 'test2', (30,40))
    shape.Line_Width = 3
    shape.Color = wx.BLUE
    shape = self.Create_Text ( 'test2', (30,60))
    shape.Line_Width = 5
    shape.rot = pi / 4
    """


    """
    self.Set_Coordinates (
        ( -10, -10 ), RT = ( 100, None ) )
    shape = self.Create_Axis ( 0,  0 )
    shape.Color = wx.GREY_PEN.GetColour()
    shape.Line_Width = 3

    shape = self.Create_Grid ( 10 )
    shape = self.Create_Grid ( 10, arctan (0.2) )
    shape.Color = wx.RED
    shape.Line_Width = 2
    shape = self.Create_Arrow ( ( 0,  0), ( 70, 70 ) )
    shape.Color = wx.BLUE
    """

    """
    self.Set_Coordinates (
        ( -10, -10 ), RT = ( 100, None ) )
    shape = self.Create_Grid ()
    shape = self.Create_Axis ()


    shape = self.Create_Free_Shape (
        ( (0,0) , (30,0), (15, 30*sin(pi/6) ) ) )
    shape.Color = wx.RED

    shape = self.Create_Free_Shape (
        ( (0,0) , (30,0), (15, 30*sin(pi/6) ) ) )
    shape.x   = 30
    shape.y   = 40
    shape.rot = pi
    """

    """
    self.Set_Coordinates (
        ( -10, -10 ), RT = ( 100, None ) )
    #shape = self.Create_Grid ()
    #shape = self.Create_Axis ()
    shape = self.Create_Text ( 'test2', (30,60))
    shape.Line_Width = 5
    shape.rot = pi / 4
    """

    """
    #shape = self.Create_Function (
    #  '30 + 20 * sin ( pi * x / 10 )',
    #  ( 10,50,1 ) )
      
      
    x = arange ( 10, 50, 1 )
    y = 30 + 20 * sin ( pi * x / 10 )
    Points = []
    for i, xi in enumerate ( x ) :
      Points.append ( (xi, y[i] ) )
    shape = self.Create_Points (Points)
    shape.Line_Width = 4
    """

    #shape = self.Create_Button ( 5, (50,70))
    #shape = self.Create_Button ( 5, (30,70))

    #self.shape = ogl_2D.Circle_Shape ( (50,50), 10 )

    #shape = self.Create_Function ( '20 * sin ( x )', range ( 10,50 ) )


    """
    self.Set_Coordinates (
        ( -10, -10 ), RT = ( 100, None ) )

    shape = self.Create_Rectangle ( (0,0) , (40,40) )
    shape.Color = wx.RED

    shape = self.Create_Rectangle ( (20,30) , RT = (60,70) )
    shape.Color = wx.BLUE

    shape = self.Create_Rectangle ( (50,10) ,
       RPhi = ( sqrt(3200), pi/4 )  )
    shape.Color = wx.Color ( 255, 255, 50 )
    """


    """
    self.Set_Coordinates (
        ( -100, -100 ), ( 200, 200 ) )
    #self.Set_Coordinates (
    #    ( -100, -100 ), ( 200, None ) )
    shape = self.Create_Axis ( 0,  0 )
    shape = self.Create_Grid ( 10 )
    shape = self.Create_Arrow ( ( 0,  0),      ( 50, 50 ) )
    shape.Line_Width = 8
    shape = self.Create_Arrow ( ( 20, 0), RT = ( 70, 50 ) )
    shape.Color = wx.BLUE
    shape = self.Create_Arrow ( ( 40, 0),
                               RPhi = ( sqrt(5000), pi/4 ) )
    shape.Color = wx.BLACK
    shape.Line_Width = 1
    """


    """
    shape = self.Create_Line ( ( 0,  0),      ( 50, 50 ) )
    shape.Line_Width = 8
    shape = self.Create_Line ( ( 20, 0), RT = ( 70, 50 ) )
    shape.Color = wx.BLUE
    shape = self.Create_Line ( ( 40, 0),
                               RPhi = ( sqrt(5000), pi/4 ) )
    shape.Color = wx.BLACK
    shape.Line_Width = 1
    """
    


    self.Canvas.Refresh ()
    
  # *********************************************************
  # *********************************************************
  def Set_Coordinates ( self,  *args, **kwargs ) :
    self.Canvas.Set_Coordinates ( *args, **kwargs )

  # *********************************************************
  # *********************************************************
  def Create_Axis ( self, *args, **kwargs  ) :
    item = ogl_2D.Axis_Shape ( self.Canvas, *args, **kwargs  )
    self.diagram.AddShape ( item )
    return item

  # *********************************************************
  # *********************************************************
  def Create_Grid ( self, *args, **kwargs  ) :
    item = ogl_2D.Grid_Shape ( self.Canvas, *args, **kwargs  )
    self.diagram.AddShape ( item )
    return item

  # *********************************************************
  # *********************************************************
  def Create_Text ( self, *args, **kwargs ) :
    item = ogl_2D.Text_Shape ( self.Canvas, *args, **kwargs  )
    self.diagram.AddShape ( item )
    return item

  # *********************************************************
  # *********************************************************
  def Create_Points ( self, *args, **kwargs ) :
    item = ogl_2D.Points_Shape ( self.Canvas, *args, **kwargs  )
    self.diagram.AddShape ( item )
    return item

  # *********************************************************
  # *********************************************************
  def Create_Function ( self, *args, **kwargs ) :
    item = ogl_2D.Function_Shape ( self.Canvas, *args, **kwargs  )
    self.diagram.AddShape ( item )
    return item


  # *********************************************************
  # *********************************************************
  def Create_Line ( self, *args, **kwargs ) :
    item = ogl_2D.Line_Shape ( self.Canvas, *args, **kwargs ) #LB, WH )
    self.diagram.AddShape ( item )
    return item

  # *********************************************************
  # *********************************************************
  def Create_Arrow ( self, *args, **kwargs ) :
    item = ogl_2D.Arrow_Shape ( self.Canvas, *args, **kwargs ) #LB, WH )
    self.diagram.AddShape ( item )
    return item

  # *********************************************************
  # *********************************************************
  def Create_Circle ( self, *args, **kwargs  ) :
    item = ogl_2D.Circle_Shape ( self.Canvas, *args, **kwargs )
    self.diagram.AddShape ( item )
    return item

  # *********************************************************
  # *********************************************************
  def Create_Button ( self, *args, **kwargs  ) :
    item = ogl_2D.Button_Shape ( self.Canvas, *args, **kwargs )
    self.diagram.AddShape ( item )
    return item

  # *********************************************************
  # *********************************************************
  def Create_Rectangle ( self, *args, **kwargs  ) :
    item = ogl_2D.Rectangle_Shape ( self.Canvas, *args, **kwargs  )
    self.diagram.AddShape ( item )
    return item

  # *********************************************************
  # *********************************************************
  def Create_Free_Shape ( self, *args, **kwargs  ) :
    item = ogl_2D.Free_Shape ( self.Canvas, *args, **kwargs  )
    self.diagram.AddShape ( item )
    return item
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class t_C_Visual_SQL ( t_C_2D_Scene ) :

  def __init__ ( self,  Dock,     # the frame/panel/... where we can put
                                  # the GUI controls that will catch events
                 Brick,           # the Brick, with its inputs and outputs
                 ini  = None,     # inifile to store and reload settings
                 Test = False ):  # if True, testmode with buildin examples
    t_C_2D_Scene.__init__ ( self, Dock, Brick, ini, Test )

    #PG.OGL_Orientation_Hor = True
    self.Canvas.Orientation_Hor = True

    #self.shape = self.Scene.Create_Rectangle ( (0,0), (10,40) )
    self.shape = self.Create_Circle ( 5 )


    #def Create_Circle ( self, *args, **kwargs  ) :
    #item = ogl_2D.Circle_Shape ( self.Scene.Canvas, *args, **kwargs )

    List = [ 'Table 2', 'veld 1', 'veld 2', 'veld 3']
    item = ogl.DB_Table_Shape ( self.Canvas, List )
    self.diagram.AddShape ( item )

    List = [ 'Table 2', 'veld 5', 'veld 2', 'veld 3']
    item = ogl.DB_Table_Shape ( self.Canvas, List )
    self.diagram.AddShape ( item )

  def SetValue ( self, value ):
    print (' NEWWWWW') #,value)

# ***********************************************************************


# ***********************************************************************
# A simple form to test the control
# ***********************************************************************
class Simple_Test_Form ( wx.MiniFrame ):
  def __init__ ( self, ini = None ):
    # restore position and size
    pos = ( 50, 50 )
    size = ( 500, 300 )
    if ini :
      ini.Section = 'Test'
      pos  = ini.Read ( 'Pos'  , pos )
      size = ini.Read ( 'Size' , size )

    wx.MiniFrame.__init__(
      self, None, -1, 'Test PyLab Works GUI Control',
      size  = size,
      pos   = pos,
      style = wx.DEFAULT_FRAME_STYLE )

    # Create the control to be tested
    from brick_Plotting import t_Scene_2D
    self.Scene = t_Scene_2D ( self, None ) #, Ini = ini )
    #PG.OGL_Orientation_Hor = True
    #self.Scene.Canvas.Orientation_Hor = True

    #self.shape = self.Scene.Create_Rectangle ( (0,0), (10,40) )
    self.shape = self.Scene.Create_Circle ( 5 )


    #def Create_Circle ( self, *args, **kwargs  ) :
    #item = ogl_2D.Circle_Shape ( self.Scene.Canvas, *args, **kwargs )

    List = [ 'Table 2', 'veld 1', 'veld 2', 'veld3']
    item = ogl.DB_Table_Shape ( self.Scene.Canvas, List )
    self.Scene.diagram.AddShape ( item )

    List = [ 'TableName', 'field 1', 'field 2', 'field 3', 'field 4', 'field 5']
    item = ogl.DB_Table_Shape ( self.Scene.Canvas, List )
    self.Scene.diagram.AddShape ( item )

    # the Timer must be bound to Dock
    self.Timer = wx.Timer ( self )
    # the third parameter is essential to allow other timers
    self.Bind ( wx.EVT_TIMER, self.On_Timer, self.Timer)
    self.Timer.Start ( 10 )

  def On_Timer ( self, event ) :
    ball = self.shape
    dt   = 0.1
    ball.x   = ball.x + ball.vx * dt
    ball.vx *= 0.997

    ball.y   = ball.y - ball.vy * dt
    if ( ball.y <= 0 ) and ( ball.vy > 0 ) :
      ball.vy = -0.8 * ball.vy
      ball.y  = 0
    else :
      ball.vy = ball.vy + 9.8 * dt

    self.Scene.Canvas.Refresh()
    #print ball.GetX(),ball.GetY(),self.velocity,ball.GetY () + self.velocity*self.dt
# ***********************************************************************


# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  import PyLab_Works_Globals as PG
  app = wx.PySimpleApp ()
  ini = inifile ( 'test_My_New_GUI_Control.cfg' )
  frame = Simple_Test_Form (ini = ini)
  frame.Show ( True )
  app.MainLoop ()
  ini.Close ()
# ***********************************************************************
pd_Module ( __file__ )

