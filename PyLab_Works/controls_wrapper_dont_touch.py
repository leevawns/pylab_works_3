#import visual
import __init__
from base_control        import *

# *******************************************************
# This file is called with the following statements
# *******************************************************
#   control_filename = ...
#   filename = 'controls_wrapper_dont_touch.py'
#   self.p_Globals = { 'control_filename' : control_filename }
#   execfile ( filename , self.p_Globals )
# *******************************************************

import wx
import wx.aui
import inspect

# ***********************************************************************
# ***********************************************************************
class Settings_Panel ( wx.Panel ):
  def __init__ ( self, Parent, Control ) :
    wx.Panel.__init__ ( self, Parent )
    self.Control = Control

    w = 85
    h = 24
    GUI = """
    p1                         ,PanelHor  ,01
      p2                       ,wx.Panel
        self.B_SetValue        ,wx.Button     ,label = 'SetValue'       ,pos = (0,0)    ,size = (w,h)
        self.B_Calculate       ,wx.Button     ,label = 'Calculate'      ,pos = (0,30)   ,size = (w,h)
        self.B_Save_Settings   ,wx.Button     ,label = 'Save_Settings'  ,pos = (0,60)   ,size = (w,h)
        self.B_Load_Settings   ,wx.Button     ,label = 'Load_Settings'  ,pos = (0,90)   ,size = (w,h)
        self.B_Kill            ,wx.Button     ,label = 'Kill'           ,pos = (0,120)  ,size = (w,h)

        self.B_Test1           ,wx.Button     ,label = 'Test-1'         ,pos = (0,180)  ,size = (w,h)
        self.B_Test2           ,wx.Button     ,label = 'Test-2'         ,pos = (0,210)  ,size = (w,h)
        self.B_Test3           ,wx.Button     ,label = 'Test-3'         ,pos = (0,240)  ,size = (w,h)

      self.Split_Memo          ,SplitterVer
        self.Memo              ,wx.TextCtrl   ,style = wx.TE_MULTILINE
        self.Memo2             ,wx.TextCtrl   ,style = wx.TE_MULTILINE
    """
    from gui_support import Create_wxGUI
    self.wxGUI = Create_wxGUI ( GUI )
    
    self.B_SetValue      .Bind ( wx.EVT_BUTTON,   self._On_B_SetValue       )
    self.B_Calculate     .Bind ( wx.EVT_BUTTON,   self._On_B_Calculate      )
    self.B_Save_Settings .Bind ( wx.EVT_BUTTON,   self._On_B_Save_Settings  )
    self.B_Load_Settings .Bind ( wx.EVT_BUTTON,   self._On_B_Load_Settings  )
    self.B_Kill          .Bind ( wx.EVT_BUTTON,   self._On_B_Kill           )
    self.B_Test1         .Bind ( wx.EVT_BUTTON,   self._On_B_Test1          )
    self.B_Test2         .Bind ( wx.EVT_BUTTON,   self._On_B_Test2          )
    self.B_Test3         .Bind ( wx.EVT_BUTTON,   self._On_B_Test3          )

    # let's call all buttons, to get the start properties
    self._Display_Value ()

    # Hook on to the change event
    self.Control._On_Extra_Event_Handler = self._On_Extra_Event_Handler

    self.Memo.AppendText ( 'Size = ' + str ( self.Control.GetSize () ) +'\n' )
    self.Memo.AppendText ( '\n' )

    # Print all methods / properties
    self.Memo.AppendText ( '***** Control_Defs *****\n' )
    Issue = self.Control.CD
    NameSpace = dir ( Issue )
    for item in NameSpace :
      if ( item[0] != '_' ) and \
         item[0].isupper() :
        value = getattr ( Issue, item )
        if not ( inspect.ismethod ( value ) ) and \
           not ( inspect.isclass  ( value ) ):
          value = str ( value )
          if value.lower().find ( 'object' ) < 0 :
            self.Memo.AppendText ( '    ' + item + ' = ' + value + '\n' )
    self.Memo.AppendText ( '\n' )

    self.Memo.AppendText ( '***** Control Attributes *****\n' )
    Issue = self.Control
    NameSpace = dir ( Issue )
    for item in NameSpace :
      if ( item[0] != '_' ) and \
         item[0].isupper()  and \
         not ( item in self.Control.Exclude_Dir ) and \
         item != 'Exclude_Dir' :
        value = getattr ( Issue, item )
        if not ( inspect.ismethod ( value ) ) and \
           not ( inspect.isclass  ( value ) ):
          value = str ( value )
          if value.lower().find ( 'object' ) < 0 :
            self.Memo.AppendText ( '    ' + item + ' = ' + value + '\n' )
    self.Memo.AppendText ( '\n' )

    self.Memo.AppendText ( '***** Control Methods *****\n' )
    Issue = self.Control
    NameSpace = dir ( Issue )
    Own_NameSpace = dir ( My_Control_Class )
    for item in NameSpace :
      if not ( item.startswith ( '__' )) and \
            ((  not ( item in self.Control.Exclude_Dir ) and \
               (item != 'Exclude_Dir')                        ) or  \
             ( item in Own_NameSpace )) :
        value = getattr ( Issue, item )
        if inspect.ismethod ( value ) :
          value = str ( value )
          self.Memo.AppendText ( '    ' + item + '\n' )
    self.Memo.AppendText ( '\n' )


  # ***************************************
  def _Display_Value ( self ) :
    #self.Memo2.AppendText ( 'Value = '+ str ( self.Control.GetValue () ) +'\n')
    self.Memo2.AppendText ( 'Par  = '+ str ( self.Control.Brick.Par )    +'\n')
    self.Memo2.AppendText ( 'XPar = '+ str ( self.Control.Brick.Par.Modified )    +'\n')
    self.Control.Brick.Par.Clear_Modified ()
    self.Memo2.AppendText ( 'XPar = '+ str ( self.Control.Brick.Par.Modified )    +'\n')
    #self.Memo2.AppendText ( 'In  = '+ str ( self.Control.Brick.In  )    +'\n')
    #self.Memo2.AppendText ( 'Out = '+ str ( self.Control.Brick.Out )    +'\n')
    self.Memo2.AppendText ( '\n' )

  # ***************************************
  def _On_Extra_Event_Handler ( self, event = None ) :
    #v3print ( '-------------NEW---------------' )
    self._Display_Value ()

  # ***************************************************
  def _On_B_SetValue ( self, event = None ):
    from dialog_support import MultiLineDialog
    Names  = [ 'Value' ]
    Values = [ self.Control.GetValue () ]
    Ok, Values = MultiLineDialog ( Names, Values, [],
                                  'SetValue')
    if Ok :
      # Convert the string value to the correct type
      Type = type ( self.Control.GetValue () )

      if Type == int :
        val = int ( Values [0] )
      elif Type == float :
        val = float ( Values [0] )
      else :
        val = Values [0]
      self.Control.SetValue ( val )

      self.Memo2.AppendText ( "Control Decided:\n" )
      self._Display_Value ()

  # ***************************************************
  def _On_B_Calculate ( self, event = None ):
    try :
      label = self.Control.Calculate ()
      self._Display_Value ()
    except :
      pass

  # ***************************************************
  def _On_B_Save_Settings ( self, event = None ):
    try :
      self.Control.Save_Settings ()
    except :
      pass

  # ***************************************************
  def _On_B_Load_Settings ( self, event = None ):
    try :
      self.Control.Load_Settings ()
    except :
      pass

  # ***************************************************
  def _On_B_Test1 ( self, event = None ):
    self.Control.Test1 ()

  # ***************************************************
  def _On_B_Test2 ( self, event = None ):
    self.Control.Test2 ()

  # ***************************************************
  def _On_B_Test3 ( self, event = None ):
    self.Control.Test3 ()

  # ***************************************************
  def _On_B_Kill ( self, event = None ):
    try :
      self.Control.Kill ()
    except :
      pass

# ***********************************************************************



# ***********************************************************************
# A simple form to test the control
# ***********************************************************************
class Simple_Test_Form ( wx.Frame ) :  #wx.MiniFrame ):
  def __init__ ( self, ini = None ):
    # restore position and size
    pos = ( 50, 50 )
    size = ( 500, 500 )
    if ini :
      ini.Section = 'Test'
      pos  = ini.Read ( 'Pos'  , pos )
      size = ini.Read ( 'Size' , size )

    #wx.MiniFrame.__init__(
    wx.Frame.__init__(
      self, None, -1, 'Test PyLab Works GUI Control',
      size  = size,
      pos   = pos,
      style = wx.DEFAULT_FRAME_STYLE )

    # *************************************************************
    self.StatusBar = self.CreateStatusBar()
    self.StatusBar.SetFieldsCount(3)
    self.StatusBar.SetStatusWidths([-2, -1, -2])
    self.StatusBar.SetStatusText(' Edit',0)
    self.StatusBar.SetStatusText(' aap',2)
    self.StatusBar_Controls = []
    # *************************************************************

    # tell FrameManager to manage this frame
    self._mgr = wx.aui.AuiManager ()
    self._mgr.SetManagedWindow ( self )

    # Set AUI manager flags
    self._mgr.SetFlags ( self._mgr.GetFlags () ^ wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE )
    self._mgr.GetArtProvider().SetMetric (
      wx.aui.AUI_DOCKART_GRADIENT_TYPE, wx.aui.AUI_GRADIENT_HORIZONTAL )
    self._mgr.GetArtProvider().SetMetric ( wx.aui.AUI_DOCKART_SASH_SIZE, 3 )
    self._mgr.GetArtProvider().SetMetric ( wx.aui.AUI_DOCKART_CAPTION_SIZE, 14 )

    #self.Controls = []

    # Create Dummy Brick
    import brick
    Name = 't_C_' + Control_Name
    Brick = brick.t_Dummy_Brick ( None, 'Test', Name, Control_Filename )

    # Create and Add Control Pane
    from PyLab_Works_appform import Control_Pane
    pane = Control_Pane ( self, Brick, ini )

    #self._mgr.SetDockSizeConstraint(0.5, 0.5)
    self._mgr.AddPane( pane,
                       wx.aui.AuiPaneInfo().
                       Name ( Brick.Name ).
                       Caption ( 'Control under Test :  ' + Name ).
                       CaptionVisible ( True ).
                       Left().
                       MinSize( ( 200, 40 ) ).
                       CloseButton ( False ).
                       MaximizeButton ( False ) )

    self.My_Control = Brick.GUI_Controls [0]
    self.My_Control.SetForegroundColour ( wx.BLUE )

    pane = Settings_Panel ( self, self.My_Control )
    self._mgr.AddPane ( pane,
                           wx.aui.AuiPaneInfo().
                           Name ( '_Tester' ).
                           #Caption ( 'Control Tester' ).
                           #CaptionVisible ( True ).
                           Right().
                           MinSize( ( 40, 40 ) ).
                           CloseButton ( False ).
                           MaximizeButton ( False ).
                           CenterPane() )

    # Attach test explanation to buttons
    line = pane.Control.Test1.__doc__
    if not ( line ) : line = 'No Docstring'
    pane.B_Test1.SetToolTipString ( line.strip() )

    line = pane.Control.Test2.__doc__
    if not ( line ) : line = 'No Docstring'
    pane.B_Test2.SetToolTipString ( line.strip() )

    line = pane.Control.Test3.__doc__
    if not ( line ) : line = 'No Docstring'
    pane.B_Test3.SetToolTipString ( line.strip() )


    #self._mgr.GetAllPanes()[0].SetSize(200,-1)
    #pane.SetSize ( ( 100, -1 ) )
    #pane.BestSize ( ( 100, -1 ) )
    self._mgr.Update()
    #self.Bind ( wx.EVT_CLOSE, self._On_Close )
    
  # ******************************************
  # ******************************************
  def _On_Close ( self, event ) :
    """ Some component need to be destroyed, so we send a Kill command """
    event.Skip()
    #v3print ('FOM')
    ##for Control in self.Controls :
    ##  Control.Kill ()
# ***********************************************************************


# ***********************************************************************
# THIS IS NOT THE MAIN PART !!
# ***********************************************************************
frame = Simple_Test_Form ()
frame.Show ( True )
# ***********************************************************************
## NOT ALLOWED IN HERE:  pd_Module ( __file__ )
