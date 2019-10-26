import os
import PyLab_Works_Globals as PG
#from   PyLab_Works_Globals import *
from   PyLab_Works_Globals import _
from   base_control        import *
from   import_controls     import *

import wx
import wx.aui
import wx.html

from   menu_support import *
from   file_support import *
from   brick import *
from   dialog_support import *


# Alternate Color
AC = 'blue'


# ***********************************************************************
# Normally this class should be derived from wx.Window,
# but wx.Window prevents corrects sizing,
# therefor we use wx.Panel instead,
# which doesn't seems to interfere with AUI
# ***********************************************************************
class Control_Pane ( wx.Panel ):


  # ***********************************************************************
  # ***********************************************************************
  def __init__ ( self, parent, Brick, Ini, Title = 'Edit Values Below', Help = '' ) :
    #import _images
    wx.Panel.__init__ ( self, parent )
    self.parent = parent
    # watch out: section not set, therfor don't make it a self-var
    if Ini :
      Ini.Section ='Device ' + Brick.Name
    
    # counter for none value. to force a parameter change
    self.None_Counter = 0

    #self.panel = wx.Panel ( self , -1)
    #self.panel.SetBackgroundColour = 'RED'

    #panel = self
    self.y = 5
    #w, h = self.GetClientSize() #GetSize()
    w = self.GetClientSize()[0]
    w = w - 10


    ##self.GUI_Controls_Weg = []
    self.GUI_Controls = []
    self.Brick = Brick


    #for self.i, self.C  in enumerate ( Brick.Control_Defs ) :
    self.x = 0
    for self.i, Brick_CD  in enumerate ( self.Brick.Control_Defs ) :
      #self.x = 0  #10
      self.CD = Brick_CD

      # ********************************************************
      # Create the control
      # ********************************************************
      #print '*********** AAAA', Brick.Name, Brick.Caption, Brick_CD.Type
      #print Control_Classes
      #if Brick_CD.Type in Control_Classes and \
      #if not (isinstance ( Brick_CD.Type, int ) )  and \
      #  issubclass ( Brick_CD.Type, My_Control_Class ) :
      #print 'UIOYPKL',self.Brick.Name, self.Brick.Control_Defs,Brick_CD
      Control = Brick_CD.Type  ( self, self.Brick, Brick_CD, Ini )

      #self.y += Control.GetSize()[1]
      #self.y += Control.Y
      w = Control.GetSize()[0]
      if Brick_CD.NewLine or ( w <= 0 ) :
        self.x = 0
        self.y += Control.GetSize()[1] + 3
      else :
        self.x += w + 3

      Brick_CD.GUI_Control = Control
      self.GUI_Controls.append ( Control )

      if 'Hint' in dir ( Brick_CD ) :
        Control.SetToolTipString ( Brick_CD.Hint )
      odd = self.i % 2
      if odd : ## and ( 'SetForegroundColour' in dir ( Control ) ) :
        Control.SetForegroundColour ( AC )

      """ Maybe these have to be added
      Control_Pars [ 'X-Pos' ]        = self.x
      Control_Pars [ 'Y-Pos' ]        = self.y
      Control_Pars [ 'Height' ]       = -1
      """

      # ********************************************************
      # Call Bricks completions
      # ********************************************************
      self.Brick.After_Control_Create ()



      # ********************************************************
      # Diagnostic Information
      # ********************************************************
      if self.Brick.Diagnostic_Mode :

        line = '-- Set_Control_Params --' + '\n'
        ##line += '  Input_Index      = ' + str ( self.C.Input_Channel ) + '\n'
        line += '  Input_Index      = ' + str ( Brick_CD.Input_Channel ) + '\n'
        #Control_Pars [ 'Control_Index'] = self.i + '\n'
        line += '  X / Y            = ' + str ( Control.X_Pos ) + ' / ' + \
                                          str ( Control.Y_Pos ) + '\n'
        line += '  Scalable         = ' + str ( Control.Scalable ) + '\n'
        line += '  Save_Settings    = ' + str ( Control.Save_Settings ) + '\n'
        line += '  Load_Settings    = ' + str ( Control.Load_Settings ) + '\n'
        line += '  GetValue         = ' + str ( Control.GetValue ) + '\n'
        line += '  SetValue         = ' + str ( Control.SetValue ) + '\n'
        if 'Calculate' in dir ( Control ):
          line += '  Calculate        = ' + str ( Control.Calculate ) + '\n'
        if 'Add_Data' in dir ( Control ):
          line += '  Add_Data         = ' + str ( Control.Add_Data ) + '\n'
        if 'Kill' in dir ( Control ):
          line += '  Kill             = ' + str ( Control.Kill ) + '\n'
        if 'Hint' in dir ( Control ):
          line += '  Hint             = ' + str ( Brick_CD.Hint ) + '\n'
        line       += '\n'
        #PG.wbd ( self.Brick, line )

        #line  = ''
        line += _(0, 'Creating Control\n')
        for item in Control_Pars :
          s = str ( Control_Pars [ item ] )
          if len(s) > 60 :
            s = s [:60]
          line += '  ' + item + ' = ' + s
          line += '\n'

        # Here test some function call evaluations
        line += '\n'
        line += _(0, 'Function Evaluation: \n' )
        item = 'Control_GetValue'
        if Control_Pars.has_key ( item ) and \
           Control_Pars [ item ] != None :
          line += '  ' + item + ' = ' + str ( Control_Pars [ item ] () )
          line += '\n'

        PG.wbd ( self.Brick, line )

    if Brick.Main_Description :
      self.SetToolTip( Brick.Description )

    # For an easy access of the Controls from within the Brick
    Brick.GUI_Controls = self.GUI_Controls
    


    """
    # WHAT HAS WHAT
    print '************'
    print
    print '--------- Pane --------'
    for item in dir ( self ) :
      print '  ', item
    print '--------- Brick --------'
    for item in dir ( self.Brick ) :
      print '  ', item
    print '--------- Brick.CD[0] --------'
    for C in self.Brick.Control_Defs :
      print '  ', C.Caption
      for item in dir ( C  ) :
        print '    ', item
    print
    print '************'
    """
  # ********************************************************
  # LED temporary
  # ********************************************************
  def TC (self, par):
    #print 'TTTTTTTTTTTTTT',par,type(par)
    if par :
      self.StaticText.SetBackgroundColour ("green")
    else :
      self.StaticText.SetBackgroundColour ("red")
    self.StaticText.SetLabel (str(par))
    self.StaticText.SetSize ( (120,-1))




  # ********************************************************
  # If the parameters of a Brick have changed due to input signals,
  # this procedure must be called to correct the visual settings
  # of the control
  # ********************************************************
  def Brick_2_Control ( self, inputs ) :
    for Control in self.GUI_Controls :
      CD = Control.CD
      try :
        if Control.Brick.Diagnostic_Mode :
          line='Brick_2_Control: ' + str(inputs[CD.Input_Channel])
          PG.wbd ( Control.Brick, line )

        if  CD.Input_Channel and \
           ( inputs [ CD.Input_Channel ] != None ):
          #( inputs [ CD.Input_Channel ] != Null ):
          Control.SetValue ( inputs [ CD.Input_Channel ] )

      except :
        pass

  # ********************************************************
  # all event controls that will always need
  # to notify a brick of it's changes
  # ********************************************************
  """ Never OCCURRES
  def OnEvent ( self, event ) :
    print 'EVENT GUI_Controls'
    ID = event.GetId()
    #print '*******ONEVENT',ID
    for C in self.GUI_Controls :
      #print '*******ON',type(C)
      if C['ID'] == ID :
        break
    #print '*******ONEVENT',ID ,C.GetValue']()
    #print '*******ONECEEVT',type(C)
    #if PG.NEWW :
    C['Brick'].Par [ C['Control_Index'] + 1 ] = C['Control_GetValue']()
    #else :
    #  C['Brick'].Params [ C['Control_Index'] + 1 ] = C['Control_GetValue']()


    event.Skip()
  """

  # ********************************************************
  # Function that returns a Changing Value for controls
  # that don't have a GetValue.
  # By incrementing a counter, we'll be sure that params
  # of the brick will change, so i.e. a button press is detected
  # ********************************************************
  def Return_None_Value ( self ) :
    self.None_Counter += 1
    return self.None_Counter
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class my_App_Form ( wx.Frame, Menu_Event_Handler):

  def __init__(self, parent, id=-1, title="", pos=wx.DefaultPosition,
               size=wx.DefaultSize,
               style = None ):

    default_style = wx.DEFAULT_FRAME_STYLE | \
                    wx.SUNKEN_BORDER | \
                    wx.CLIP_CHILDREN

    ##if not ( PG.Standalone  ) :
    #if Application.Design_Mode :
    #  default_style |= wx.STAY_ON_TOP
    
    if style == None:
      style = default_style
    self.Titles = [ 'PyLab Works Application:    ', title + ':    ', '' ]
    Title = ''.join ( self.Titles )
    #self.Base_Title = len ( Title )
    wx.Frame.__init__(self, parent, id, Title, pos, size, style)

    Path = sys._getframe().f_code.co_filename
    Path = os.path.split ( Path ) [0]
    self.SetIcon ( wx.Icon (
      Joined_Paths ( Path,
      '../pictures/vippi_bricks_323.ico'), wx.BITMAP_TYPE_ICO ) )

    # *************************************************************
    self.MenuBar = Class_Menus ( self )
    # *************************************************************

    self.StatusBar = self.CreateStatusBar()
    self.StatusBar.SetFieldsCount(5)
    self.StatusBar_Controls = []
    # *************************************************************

    # tell FrameManager to manage this frame
    self._mgr = wx.aui.AuiManager()
    self._mgr.SetManagedWindow(self)

    # Set AUI manager flags
    self._mgr.SetFlags(self._mgr.GetFlags() ^ wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE)
    self._mgr.GetArtProvider().SetMetric (
      wx.aui.AUI_DOCKART_GRADIENT_TYPE, wx.aui.AUI_GRADIENT_HORIZONTAL)
    self._mgr.GetArtProvider().SetMetric ( wx.aui.AUI_DOCKART_SASH_SIZE, 3 )
    self._mgr.GetArtProvider().SetMetric ( wx.aui.AUI_DOCKART_CAPTION_SIZE, 10 )


    # Update the complete frame
    self._mgr.Update ()
    
    self.Bind ( wx.EVT_SIZE,     self.OnSize      )
    self.Bind ( wx.EVT_CLOSE,    self.OnClose     )
    self.Bind ( wx.EVT_MOTION,   self.Test        )
    self.Bind ( wx.EVT_KEY_DOWN, self.On_KeyPress )

    ##werkt niet self.Bind ( wx.EVT_SPLITTER_DCLICK, self.Test_RM )

    # *************************************************************
    # Menu completions
    # *************************************************************
    MB = self.MenuBar.Bind_MenuItem
    MB ( 'View', 'Fixed'    ,self._On_Menu_View_Fixed    )
    MB ( 'View', 'Flexible' ,self._On_Menu_View_Flexible )
    MB ( 'View', 'Moveable' ,self._On_Menu_View_Moveable )
    # *************************************************************

    self.Show ()

  # **************************************************
  def On_KeyPress ( self, event ):
    print ('MAIN', event.GetKeyCode())
    
  # **************************************************
  def Set_Caption ( self, line, level = 2 ) :
    #print 'JJJ',self.GetTitle(),'$$',self.Base_Title,'$$',line
    #self.SetTitle ( self.GetTitle () [ : self.Base_Title ] + line )
    if level == 1 :
      self.Titles [1] = line + ':    '
    else :
      self.Titles [2] = line
    Title = ''.join ( self.Titles )
    self.SetTitle ( Title )

  # **************************************************
  def OnMenu_Open ( self, event ) :
    # stop the simulation engine
    print ('mainnnopen')
    Old_State = PG.State
    if PG.State in ( PG.SS_Run, PG.SS_HighLight ) :
      PG.State = PG.SS_Stop

    # pass the Open File to the focussed widget
    FW = self.FindFocus ()
    if hasattr ( FW, 'Filename' ) and \
       ( os.path.splitext ( FW.Filename ) [1] == '.py' ) and \
       hasattr ( FW, 'OnMenu_Open' ) :
      FW.OnMenu_Open ()
      self.Set_Caption ( path_split ( FW.Filename ) [1], 1 )
      if hasattr ( FW,'My_Control' ) :
        FW.My_Control.Execute_Code ()

    # Restore the State of the simulation engine
    PG.State = Old_State

  # **************************************************
  def _On_Menu_View_Fixed ( self, event ):
    self._Set_Panes ( 0 )

  # ***************************************************
  def _On_Menu_View_Flexible ( self, event ):
    self._Set_Panes ( 1 )

  # ***************************************************
  def _On_Menu_View_Moveable ( self, event ):
    self._Set_Panes ( 2 )

  # ***************************************************
  def _Set_Panes ( self, style = 0 ) :
    Resizable = style > 0
    Moveable  = style > 1
    for pane in self._mgr.GetAllPanes() :
      name = pane.name
      # do nothing with implicit floating bricks
      for Brick in  PG.Main_Form.Shape_Container.Devices :
        if Brick.Name == name :
          if not ( Brick.Float ) :
            # some clumsy way to get rid of floating windows
            if pane.IsFloating ():
              if Moveable :
                pane.Show ()
              else :
                pane.Hide()
            else :
              pane.CaptionVisible ( Moveable and not ( Brick.Center ) )
              pane.PaneBorder     ( False ) #Resizable )
              pane.Resizable      ( Resizable )
            rect = pane.rect
            #pane.MinSize ( (40,40))
            #pane.MaxSize ( (500,500))
            pane.BestSize ( (rect[2],rect[3]))
    #self._mgr.GetArtProvider().SetMetric ( wx.aui.AUI_DOCKART_SASH_SIZE, 0 )
    self._mgr.Update()



  def OnMenu_View_weg ( self, event ):
    aap = 0
    for pane in self._mgr.GetAllPanes() :
      name = pane.name
      # do nothing with implicit floating bricks
      for Brick in  PG.Main_Form.Shape_Container.Devices :
        if Brick.Name == name :
          #print dir (pane)  #.CaptionVisible ( False )
          print ('FFGGHH',pane.HasCaption(),pane.IsMovable())
          """
['BestSize', 'Bottom', 'BottomDockable', 'Caption', 'CaptionVisible',
'Center', 'CenterPane', 'Centre', 'CentrePane', 'CloseButton', 'DefaultPane',
'DestroyOnClose', 'Direction', 'Dock', 'DockFixed', 'Dockable', 'Fixed',
'Float', 'Floatable', 'FloatingPosition', 'FloatingSize', 'Gripper',
'GripperTop', 'HasBorder', 'HasCaption', 'HasCloseButton', 'HasFlag',
'HasGripper', 'HasGripperTop', 'HasMaximizeButton', 'HasMinimizeButton',
'HasPinButton', 'Hide', 'IsBottomDockable', 'IsDestroyOnClose', 'IsDocked',
'IsFixed', 'IsFloatable', 'IsFloating', 'IsLeftDockable', 'IsMaximized',
'IsMovable', 'IsOk', 'IsResizable', 'IsRightDockable', 'IsShown', 'IsToolbar',
'IsTopDockable', 'Layer', 'Left', 'LeftDockable', 'MaxSize', 'Maximize',
'MaximizeButton', 'MinSize', 'MinimizeButton', 'Movable', 'Name',
'PaneBorder', 'PinButton', 'Position', 'Resizable', 'Restore', 'Right',
'RightDockable', 'Row', 'SafeSet', 'SetFlag', 'Show', 'ToolbarPane', 'Top',
'TopDockable', 'Window', '__class__', '__del__', '__delattr__', '__dict__',
'__doc__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__',
'__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__str__',
'__swig_destroy__', '__weakref__', 'actionPane', 'best_size', 'buttonClose',
'buttonCustom1', 'buttonCustom2', 'buttonCustom3', 'buttonMaximize',
'buttonMinimize', 'buttonPin', 'buttons', 'caption', 'dock_direction',
'dock_layer', 'dock_pos', 'dock_proportion', 'dock_row', 'floating_pos',
'floating_size', 'frame', 'max_size', 'min_size', 'name', 'optionActive',
'optionBottomDockable', 'optionCaption', 'optionDestroyOnClose',
'optionDockFixed', 'optionFloatable', 'optionFloating', 'optionGripper',
'optionGripperTop', 'optionHidden', 'optionLeftDockable', 'optionMaximized',
'optionMovable', 'optionPaneBorder', 'optionResizable', 'optionRightDockable',
'optionToolbar', 'optionTopDockable', 'rect', 'savedHiddenState', 'state',
 'this', 'thisown', 'window']"""
          if not ( Brick.Float ) :
            # some clumsy way to get rid of floating windows
            if pane.IsFloating ():
              pane.Hide()
            else :
              ##pane.CaptionVisible ( False )
              ##pane.PaneBorder ( False )
              ##pane.Resizable ( False )

              pane.CaptionVisible ( True )
              pane.PaneBorder ( True )
              pane.Resizable ( True )

              if aap == 0:
                pass
          ##pane.Fixed ()
          #pane.Resizable ( False )
          rect = pane.rect
          ##pane.MinSize ( (rect[2],rect[3]))
          ##pane.MaxSize ( (rect[2],rect[3]))
          ##pane.BestSize ( (rect[2],rect[3]))
          pane.MinSize ( (40,40))
          pane.MaxSize ( (500,500))
          pane.BestSize ( (rect[2],rect[3]))
          line = self._mgr.SavePaneInfo ( pane )
          print (line)
        print ('PANE',pane.IsFixed(),pane.rect)
        aap += 1
    self._mgr.GetArtProvider().SetMetric ( wx.aui.AUI_DOCKART_SASH_SIZE, 0 )
    self._mgr.Update()
    #print 'AAAAA',self._mgr.SavePerspective ()


  def Menu_FileOpen ( self, Completion ) :
    pass

  #def Test_RM ( self, event ) :
  #  print 'SASH RM down'
    
  def Test ( self, event ) :
    if event.ButtonDown(wx.MOUSE_BTN_LEFT) :
      pass
      #print 'move'
      #print event.Dragging
      """print dir(event)
      ['AltDown', 'Button', 'ButtonDClick', 'ButtonDown', 'ButtonIsDown', 'ButtonUp',
      'ClassName', 'Clone', 'CmdDown', 'ControlDown', 'Destroy', 'Dragging', 'Entering',
      'EventObject', 'EventType', 'GetButton', 'GetClassName', 'GetEventObject',
      'GetEventType', 'GetId', 'GetLinesPerAction', 'GetLogicalPosition', 'GetPosition',
      'GetPositionTuple', 'GetSkipped', 'GetTimestamp', 'GetWheelDelta', 'GetWheelRotation',
      'GetX', 'GetY', 'Id', 'IsButton', 'IsCommandEvent', 'IsPageScroll', 'IsSameAs',
      'Leaving', 'LeftDClick', 'LeftDown', 'LeftIsDown', 'LeftUp', 'LinesPerAction',
      'LogicalPosition', 'MetaDown', 'MiddleDClick', 'MiddleDown', 'MiddleIsDown',
      'MiddleUp', 'Moving', 'Position', 'ResumePropagation', 'RightDClick', 'RightDown',
      'RightIsDown', 'RightUp', 'SetEventObject', 'SetEventType', 'SetId', 'SetTimestamp',
      'ShiftDown', 'ShouldPropagate', 'Skip', 'Skipped', 'StopPropagation', 'Timestamp',
      'WheelDelta', 'WheelRotation', 'X', 'Y', '__class__', '__del__', '__delattr__',
      '__dict__', '__doc__', '__getattribute__', '__hash__', '__init__', '__module__',
       '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__str__',
       '__swig_destroy__', '__weakref__', 'm_altDown', 'm_controlDown', 'm_leftDown',
       'm_linesPerAction', 'm_metaDown', 'm_middleDown', 'm_rightDown', 'm_shiftDown',
       'm_wheelDelta', 'm_wheelRotation', 'm_x', 'm_y', 'this', 'thisown']
       """
    
    
  def Add_Pane ( self, Brick, Caption, Ini ) :
    if len ( Brick.Control_Defs ) == 0 :
      return
    pane = Control_Pane ( self, Brick, Ini )
    if Brick.Center:
      # first make all other center panes left sided
      self._mgr.AddPane( pane,
                         wx.aui.AuiPaneInfo().
                         Name ( Brick.Name ).
                         Caption ( Caption ).
                         PaneBorder ( False ).
                         #CaptionVisible ( False ).
                         Left().
                         MinSize( ( 40, 40 ) ).
                         CloseButton ( False ).
                         MaximizeButton ( False ).
                         CenterPane() )

      
    else:
      self._mgr.AddPane( pane,
                           wx.aui.AuiPaneInfo().
                           Name ( Brick.Name ).
                           Caption ( Caption ).
                           PaneBorder ( False ).
                           #CaptionVisible ( False ).
                           Left().
                           MinSize( ( 40, 40 ) ).
                           CloseButton ( False ).
                           MaximizeButton ( False ) )
    #if center:
    #  pane.CenterPane()
    #wx.aui.AuiPaneInfo.CenterPane()
    self._mgr.Update()

    return pane

  def Delete_Pane ( self, name ) :
    pane = self._mgr.GetPane ( name )
    if pane.IsOk () :
      self._mgr.ClosePane  ( pane )
      self._mgr.DetachPane ( pane.window )
      self._mgr.Update ()
      pane.window.Destroy ()

  # *************************************************************
  # *************************************************************
  def OnClose(self, event):

    # Stop the program in case of a standalone application
    ##if PG.Standalone :
    if not ( Application.Design_Mode ) :
      self.Save_Settings ( self.Ini )
      PG.App_Running = False
      ##PG.Standalone = False  #??
      Application.Design_Mode = True ##?? Yes otherwsie the appliaction won't close
      PG.Main_Form.OnCloseWindow ( None )
      
    else :
      # Look for special controls, that needs a finalize function
      if PG._Old_Std_Viewer :
        PG._Old_Std_Viewer.Release()
      for pane in self._mgr.GetAllPanes() :
        for Control in pane.window.GUI_Controls :
          Control.Kill ()
      self._mgr.UnInit()
      del self._mgr

      self.Destroy()

  def OnSize(self, event):
    event.Skip()
    
  def Save_Settings ( self, ini ) :
    ini.Section = 'Application Window'
    ini.Write ( 'Visible', True )
    ini.Write ( 'Pos', self.GetPosition() )
    ini.Write ( 'Size', self.GetSize() )

    #try :  # in StandAlone, _mgr doesn't exists
    #  a = self._mgr
    #print 'BBBBB',type(self._mgr.SavePerspective ())
    ini.Write ( 'Panes', self._mgr.SavePerspective () )
    #except :
    #  pass

    # save the settings of the GUI-Controls, not covered by Params
    for pane in self._mgr.GetAllPanes() :
      ini.Section = 'Device ' + pane.window.Brick.Name
      for i, Control in enumerate ( pane.window.GUI_Controls ) :
        key = 'CSS_' + str(i) + '_'
        #v3print ( 'Let Control Save Settings', ini.Section, key )
        #v3print ( '  ', Control.Save_Settings )
        #What_DO_I_Call ( Control.Save_Settings, 4 )
        Control.Save_Settings ( ini, key )

        #if PG.Debug_Table._On :
        #  PG.Debug_Table.Write ( pane.window.Brick.Nr,
        #    '*-*Save General = ' + str ( General_Settings ) )

      """
      General_Settings = []
      General_Settings_New = []

      for Control in pane.window.GUI_Controls :
        if Control.Save_Settings :
          ini.Section = 'Device ' + pane.window.Brick.Name
          v3print ( 'Let Control Save Settings', ini.Section )
          Control.Save_Settings ( ini )

          if PG.Debug_Table._On :
            PG.Debug_Table.Write ( pane.window.Brick.Nr,
              '*-*Save = ????' )

        # If the control has no Save Settings,
        # gather the values of the individual controls
        else :
          for Indx in Control.EP :
            Value = Control.Brick.Par [ Indx ]
            if isinstance ( Value, wx.Colour ) :
              temp = tuple ( Value) +  ( Value.Alpha(), )
              Value = temp

            ####  ????  ####
            #if Value == Null :
            #  Value = None

            General_Settings.append ( Value )
      #print 'FFFTTTRRR',General_Settings,General_Settings_New

      # if there were general settings (controls that don't have 'Save_Settings"
      # store them here in the ini-file
      if len ( General_Settings ) > 0 :
        ini.Section = 'Device ' + pane.window.Brick.Name
        ini.Write ( 'CS_gen', General_Settings )
        v3print ('GENREAL',Control [ 'Brick' ].Name,General_Settings)

        if PG.Debug_Table._On :
          PG.Debug_Table.Write ( pane.window.Brick.Nr,
            '*-*Save General = ' + str ( General_Settings ) )
      """
      
  def Load_Settings ( self, ini ) :
    self.Ini = ini
    ini.Section = 'Application Window'

    # Position the application window,
    # and assure it's on the visible part of the screen
    Pos = list ( ini.Read ( 'Pos' , (0,0) ) )
    ScreenSize = wx.DisplaySize ()
    if Pos[0] < 0 :
      Pos[0] = 0
    elif Pos[0] > ScreenSize[0] - 20  :
      Pos[0] = ScreenSize[0] - 20
    if Pos[1] < 0 :
      Pos[1] = 0
    elif Pos[1] > ScreenSize[1] - 40  :
      Pos[1] = ScreenSize[1] - 40
    self.SetPosition( Pos )
    #v3print ( 'ScreenSize = ', ScreenSize )


    self.SetSize( ini.Read ( 'Size' , (800,600) ) )
    #print 'AIUPANE',ini.Read ('Panes')
    line = ini.Read ( 'Panes' )
    if line :
      try :
        self._mgr.LoadPerspective ( line )
      except :
        pass

    """
    AIUPANE
layout2|name=SN10;caption=VPython (Plotting);
state=770;dir=5;layer=0;row=0;pos=0;prop=100000;
bestw=100;besth=40;minw=100;minh=40;maxw=-1;maxh=-1;
floatx=-1;floaty=-1;floatw=-1;floath=-1|
name=SN11;caption=Code Editor (Plotting);
state=2046;dir=4;layer=0;row=0;pos=0;prop=100000;
bestw=100;besth=40;minw=100;minh=40;maxw=-1;maxh=-1;
floatx=-1;floaty=-1;floatw=-1;floath=-1|

Panes = u'layout2|
name=SN10;caption=VPython (Plotting);
state=768;dir=5;layer=0;row=0;pos=0;prop=100000;
bestw=100;besth=40;minw=100;minh=40;maxw=-1;maxh=-1;
floatx=-1;floaty=-1;floatw=-1;floath=-1|
name=SN11;caption=Code Editor (Plotting);
state=2044;dir=4;layer=0;row=0;pos=0;prop=100000;
bestw=100;besth=40;minw=100;minh=40;maxw=-1;maxh=-1;
floatx=-1;floaty=-1;floatw=-1;floath=-1|
dock_size(5,0,0)=102|dock_size(4,0,0)=247|'

    """
    
    for pane in self._mgr.GetAllPanes() :
      """
      # Get the general settings string, if available
      if len ( pane.window.GUI_Controls ) > 0 :
        ini.Section = 'Device ' + pane.window.Brick.Name
        General_Settings = ini.Read ( 'CS_gen', [] )
        if PG.Debug_Table._On :
          PG.Debug_Table.Write ( pane.window.Brick.Nr,
            '*-*Load General = ' + str ( General_Settings ) )
      else :
        General_Settings = []
      """
      
      ini.Section = 'Device ' + pane.window.Brick.Name

      #for Control in pane.window.GUI_Controls :
      for i, Control in enumerate ( pane.window.GUI_Controls ) :
        key = 'CSS_' + str(i) + '_'
        #What_DO_I_Call ( Control.Load_Settings, 4 )
        
        line = ini.Read ( key, '' )
        print ( '*** LOAD SETTINGS', pane.window.Brick.Name, key, '=', line )

        if PG.Debug_Table._On :
          PG.Debug_Table.Write ( pane.window.Brick.Nr,
            '*-*Load = ' + str ( line ) )

        Control.Load_Settings ( ini, key )


        """
        if Control.Load_Settings :
          Control.Load_Settings ( ini )
          if PG.Debug_Table._On :
            PG.Debug_Table.Write ( pane.window.Brick.Nr,
              '*-*Load = ????' )

        elif len ( General_Settings ) > 0  :
          # Because changing the value not always (maybe even never ?)
          # triggers the event handler, we copy it manual to the parameter
          Initial_Value = General_Settings.pop(0)
          for i, Indx in enumerate ( Control.EP ) :
            if not ( Control.EP_IsDict [i] ) :
              Control.Brick.Par [ Indx ] = Initial_Value

          # prevent crashing from a wrong ini-file
          try :
            Control.SetValue ( Initial_Value )
          except :
            pass
        """
# ***********************************************************************







