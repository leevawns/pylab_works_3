import __init__

# ***********************************************************************
# control_scope.py : a fast plot library for real-time signals.
# This plot library is more like a oscilloscope than like MatPlot.
# This library should be faster than MatPlot, PyPlot and FloatCanvas.
# This library has some extra features:
#   - measurement cursor
#   - no scaling in X-axis, so you'll see all samples
#   - storage all settings in a ini-file
#   - scaling and offset is set for each individual signal
#   - Time history window for 1 signal with min/max display
#   - set attributes for all signals at once
#   - border values on top and bottom
#   -
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007 Stef Mientki
# mailto:S.Mientki@ru.nl
#
# Problems / Bugs / Limitations
#  - doubleclick on form caption, maximizes the form,
#    now closing the form will store these maxima and you never get back
#    maybe we should another window type instead of the miniframe
#
# <Version: 0.4       , 10-02-2008, Stef Mientki
#   - scaling and offset is set for each individual signal
#   - Time history window for 1 signal with min/max display
#   - set attributes for all signals at once
#   - border values on top and bottom
#   - second measurement cursor
#
# <Version: 0.3       , 29-01-2008, Stef Mientki
#   - settings made simpeler, table only
#   - better interface, independant of capabilities of parent / dock
#
# <Version: 0.2       , Stef Mientki
#   - bug in demo code:
#     def _Copy_Tree_2_Vars ( self ) :
#            ...
#     was:
#              'self.SD' + str(N) + '[ self.SD_p ] % self.SD_Max')
#     should be:
#              'self.SD' + str(N) + '[ self.SD_p % self.SD_Max ]')
#
#
# <Version: 0.1       ,04-11-2007, Stef Mientki
#    - orginal release
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
from   PyLab_Works_Globals import _
from   numpy import *
import wx
import wx.grid as gridlib
from   wx.lib.expando import ExpandoTextCtrl, EVT_ETC_LAYOUT_NEEDED
import time

# add some standard library paths
"""
import os
import sys
subdirs = [ '../support' ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
"""

from   picture_support import Get_Image_16
from   inifile_support import *
from   utility_support import *
from   dialog_support  import *
from   grid_support    import *

ct_none     = 0
ct_checkbox = 1
ct_radio    = 2

XDIV = YDIV = 10
MAX_SCREEN_WIDTH = 1680  # 19" widescreen TFT
# ***********************************************************************



from   control_scope_channel import _Channel
from   scope_plot         import _PlotCanvas
from   scope_plot_hist    import _PlotCanvas_History
from   control_scope_base import *
import copy


# ***********************************************************************
# important data flow
# ***********************************************************************
"""
                  Signal Display
                   |    /|\
     OnButtonClick |     | Scope_Add_New_SampleSet
                  \|/    |
                  Fast Display Parameters
                   |    /|\
 _Copy_Vars_2_Tree |     | _Copy_Tree_2_Vars
                  \|/    |
                  Tree Data  <-----  Prepare_Scope_Signals (also called by main ??)
                  Tree Data  ----->  Tree_2_IniFile
                   |    /|\
 _Copy_Tree_2_Grid |     | _Enum_Grid_2_Tree
                  \|/    |
                  Grid Data
"""
# ************************************************************
"""
                  Signal Display
                   |    /|\
     OnButtonClick |     | Scope_Add_New_SampleSet
                  \|/    |
                  Fast Display Parameters
                   |    /|\
 _Copy_Vars_2_Grid |     | _Copy_Grid_2_Vars
                  \|/    |
                  Grid Data
                   |    /|\
    Tree_2_IniFile |     | Prepare_Scope_Signals (also called by main ??)
                  \|/    |
                  Ini-File
"""
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
#class tScope_Display ( object ):

class t_C_ScopePlot ( My_Control_Class ) :
  # *************************************************************
  # Form creation
  # *************************************************************
  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )
    print ('piep1')
    
    # to prevent maximizing of the form, this doesn't work perfect !!
    # Maybe it's better to use another window instead of the miniframe.
    self.Dock.SetSizeHints ( 100, 100, maxH=1050, maxW = 1680 )

    # Be sure to make it large enough
    self.NB = wx.Notebook ( self.Dock, -1,
                       size = ( 2000, 1200 ),
                       style = wx.BK_LEFT )

    # *****************************************************************
    # make an image list (needed for notebook)
    # *****************************************************************
    Set_NoteBook_Images ( self.NB, ( 47, 76 ) )

    # *****************************************************************
    # create the notebook tabs and put images on the tabs
    # *****************************************************************
    p1 = wx.Panel ( self.NB )
    self.NB.AddPage ( p1, "Scope", imageId=il1)
    #self.panel_2 = wx.Panel ( NB )
    #NB.AddPage ( self.panel_2, "Setting", imageId=il2 )


    # *****************************************************************
    self.Splitter = wx.SplitterWindow ( p1, style = wx.SP_LIVE_UPDATE )

    self.Panel_Left = wx.Panel ( self.Splitter, style = wx.BORDER_SUNKEN )
    self.Panel_Left.SetBackgroundColour ( wx.BLACK )
    #self.Panel_Right = wx.Panel ( self.Splitter, style = wx.BORDER_SUNKEN )

    self.Splitter_Plots = wx.SplitterWindow (self.Splitter, style = wx.SP_LIVE_UPDATE )

    self.Splitter.SplitVertically ( self.Panel_Left, self.Splitter_Plots, 105 )

    self.Splitter.SetMinimumPaneSize(20)
    # *****************************************************************
    box = wx.BoxSizer ( wx.HORIZONTAL )
    box.Add ( self.Splitter, 1, wx.EXPAND )
    self.Dock.SetSizer ( box )
    # *****************************************************************


    # *****************************************************************
    self.Panel_Right = wx.Panel ( self.Splitter_Plots, style = wx.BORDER_SUNKEN )
    self.Scope_History = _PlotCanvas_History ( self.Splitter_Plots, self, True )
    self.Splitter_Plots.SplitHorizontally ( self.Panel_Right, self.Scope_History, 105 )
    self.Splitter_Plots.SetMinimumPaneSize(20)
    # *****************************************************************
    box = wx.BoxSizer ( wx.VERTICAL )
    box.Add ( self.Splitter_Plots, 1, wx.EXPAND )
    self.Splitter.SetSizer ( box )
    # *****************************************************************


    print ('piep1')

    self.Panel_Top = wx.Panel ( self.Panel_Right,
                                style = wx.NO_BORDER )
    self.Panel_Bottom = wx.Panel ( self.Panel_Right,
                                style = wx.NO_BORDER )
    self.Scope_Canvas = _PlotCanvas ( self.Panel_Right, self )
    Sizer = wx.BoxSizer ( wx.VERTICAL )
    self.Panel_Right.SetSizer ( Sizer )
    Sizer.Add ( self.Panel_Top, 0, wx.EXPAND )
    Sizer.Add ( self.Scope_Canvas, 1, wx.EXPAND )
    Sizer.Add ( self.Panel_Bottom, 0, wx.EXPAND )

    #self.Panel_Top.SetBackgroundColour ( self.Scope_Canvas.Brush.GetColour () )
    #self.Panel_Bottom.SetBackgroundColour ( self.Scope_Canvas.Brush.GetColour () )
    self.Top_Sizer = wx.BoxSizer ( wx.HORIZONTAL )
    self.Panel_Top.SetSizer ( self.Top_Sizer )
    self.Bottom_Sizer = wx.BoxSizer ( wx.HORIZONTAL )
    self.Panel_Bottom.SetSizer ( self.Bottom_Sizer )

    data_values = [
      [ 'Name', 'On', 'NumOn', 'Lower','Upper',
        'AC', 'AC[s]', 'Delay[s]',
        'LineColor', 'LineWidth',
        'World-1', 'Cal-1', 'World-2', 'Cal-2' ] ]
    data_values_default = [
      'Signal i', False, True, -10, 10,
      False, 1, 0,
      (200,0,0), 2, 0, 0, 1, 1 ]
    for i in range (16 ):
      default = copy.copy ( data_values_default )
      default[0] = ' Signal ' + str(i+1) + ' [Volt]'
      A, B = 100, 255

      if i < 3 :
        default [1] = True
        default [8] = ( (i*A)%B, ((i+1)*A)%B, ((i+2)*A)%B )
      data_values.append ( default ) #14*[''])
    #print data_values
    data_types = [
      gridlib.GRID_VALUE_STRING,
      gridlib.GRID_VALUE_BOOL,
      gridlib.GRID_VALUE_BOOL,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_BOOL,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER,
      MY_GRID_TYPE_COLOR,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER ]
    data_defs = ( MY_GRID_ROW_FIXED, MY_GRID_COL_TYPED )

    #                           Frame,         Device, Parent
    self.Grid = Base_Table_Grid ( self.NB, None,
                                data_values, data_types, data_defs,
                                None, #Program_Custom_Colors,
                                None, #self.Set_Modal_Open,
                                None  #self.Notify_Params_Changed
                                )

    # *****************************************************************
    # we don't use a boxer sizer here, it's done in pagechange
    # otherwise it won't work in an AUI pane !!
    self.NB.AddPage ( self.Grid, "Setting", imageId=il2 )
    #box = wx.BoxSizer ( wx.VERTICAL )
    #box.Add ( self.Grid, 1, wx.GROW | wx.ALL, 0 )
    #self.panel_2.SetSizer ( box )

    # *****************************************************************
    print ('piep3')


    """
    color_bg = wx.Color( 249, 249, 217 )
    gc = 200
    self.Scope_Canvas.Set_Canvas ( color_bg,
                                   wx.Color( gc, gc, gc ) )

    self.Scope_History.Set_Canvas ( color_bg )
    """
    
    # *****************************************************************
    # Create some fast control buttons
    # *****************************************************************
    x = 2
    w = 25
    bmp = Get_Image_16 ( 'control_pause_blue.png' )
    button = wx.BitmapButton ( self.Panel_Left, -1, bmp, pos = ( x, x) )
    button.SetToolTipString ( _(0, 'Pause Recording' ) )
    self.buttons_ID = button.GetId()
    bmp = Get_Image_16 ( 'control_play_blue.png')
    button = wx.BitmapButton ( self.Panel_Left, -1, bmp, pos = ( x, x+w ) )
    button.SetToolTipString ( _(0, 'Start Recording' ) )

    bmp = Get_Image_16 ( 'list-add.png' )
    button = wx.BitmapButton ( self.Panel_Left, -1, bmp, pos = ( x+w, x) )
    button.SetToolTipString ( _(0, 'Increase selected signal Amplitude' ) )
    bmp = Get_Image_16 ( 'list-remove.png')
    button = wx.BitmapButton ( self.Panel_Left, -1, bmp, pos = ( x+w, x+w ) )
    button.SetToolTipString ( _(0, 'Decrease selected signal Amplitude' ) )

    bmp = Get_Image_16 ( 'arrow_up.png')
    button = wx.BitmapButton ( self.Panel_Left, -1, bmp, pos = ( x+2*w, x ) )
    button.SetToolTipString ( _(0, 'Shift selected signal Up' ) )
    bmp = Get_Image_16 ( 'arrow_down.png')
    button = wx.BitmapButton ( self.Panel_Left, -1, bmp, pos = ( x+2*w, x+w ) )
    button.SetToolTipString ( _(0, 'Shift selected signal Down' ) )

    bmp = Get_Image_16 ( 'color_wheel.png')
    button = wx.BitmapButton ( self.Panel_Left, -1, bmp, pos = ( x+3*w, x ) )
    button.SetToolTipString ( _(0, 'Set Color of selected signal' ) )
    self.Selected_Signalname  =  wx.StaticText( self.Panel_Left, -1, '--',( x+3*w, x+w+5 ))
    self.Selected_Signalname.SetForegroundColour ( wx.WHITE )
    self.Selected_Signalname.SetToolTipString ( _( 0, 'Selected Signal') )

    self.New_Data = False
    self.Ny = 100 # 200
    self.Nx = 600  # gives 10 divisions

    self.Values          = []
    self.Values_Labels   = []
    self.Values_IDs      = []
    self.Top_Labels      = []
    self.Bottom_Labels   = []
    self.Labels_IDs      = []
    self.Selected_Signal = None

    self.Scope_Signal_Names  = []
    self.Scope_Signal_Gain   = []
    self.Scope_Signal_Offset = []
    self.Scope_Delay_Len     = []
    self.Scope_Top           = []
    self.Scope_Bottom        = []
    self.Scope_Signal_Color  = []
    self.My_Signals          = []

    self.timer = wx.Timer ( self.TopFrame )
    self.sub_timer = 0

    # reload previous settings
    #if self.Test :
    self.Ini.Section = self.IniSection
    self.Load_Settings ( self.Ini )

    #Frame.Bind ( wx.EVT_NOTEBOOK_PAGE_CHANGED,  self.OnPageChanged )
    #Frame.Bind ( wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging )
    #Frame.Bind ( wx.EVT_CLOSE,  self._OnCloseWindow )
    #Frame.Bind ( wx.EVT_TIMER,  self.OnTimer,  self.timer)
    #Frame.Bind ( wx.EVT_BUTTON, self.OnButtonClick )
    #Frame.Bind ( wx.EVT_SIZE, self._OnSize )

    self.Dock.Bind ( wx.EVT_NOTEBOOK_PAGE_CHANGED,  self.OnPageChanged )
    self.Dock.Bind ( wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging )
    self.Dock.Bind ( wx.EVT_CLOSE,  self._OnCloseWindow )
    self.Dock.Bind ( wx.EVT_TIMER,  self.OnTimer,  self.timer)
    self.Dock.Bind ( wx.EVT_BUTTON, self.OnButtonClick )
    self.Dock.Bind ( wx.EVT_SIZE, self._OnSize )

    self.Splitter_Plots.Bind ( wx.EVT_SPLITTER_SASH_POS_CHANGED, self._OnSize )

    # *****************************************************************
    # History Trace
    # *****************************************************************
    #timebase_bufmax = zeros ( MAX_SCREEN_WIDTH )
    #timebase_bufmin = zeros ( MAX_SCREEN_WIDTH )
    #timebase_p      = 0
    # *****************************************************************
    print ('piep4')

    #self.Dock.SendSizeEvent ()
    self.Prepare_Scope_Signals ()

    # Doking in AUI panel, doesn't generate an OnShowEvent
    if self.Test :
      self.Dock.Bind ( wx.EVT_SHOW,   self._OnShowWindow )
    else :
      self.timer.Start( 100 )

    print ('piep5')

  def _On_History_Signal_Selection ( self, signal ):
    print ('ppppppooooopppp')
  def _On_History_Cursor_Selection ( self, x0, x1 ) :
    print ('ppppppoooooppppsss')

  # *****************************************************************
  # *****************************************************************
  def Add_Data ( self, data ) :
    #print 'CALLLL1111'
    #a = array([56294, 56402, 57064, 59718, 66146])
    #b=a.reshape(5,1)
    #print 'Calc_Scope', data, self.Scope_Canvas.Get_NCurve(),type(data),data.shape
    self.Scope_Canvas.Add_Data ( data )

    #print data[0][0]
    #self.Scope_History.Add_Data ( [data [0][0]] )
    self.Scope_History.Add_Data ( data[0] )


  # *****************************************************************
  # Combine the signal calibration with screen calibration
  # *****************************************************************
  def _Update_Channel ( self, chan ) :
    gain1   = self.Scope_Signal_Gain   [chan]
    offset1 = self.Scope_Signal_Offset [chan]
    name    = self.Scope_Signal_Names  [chan]

    cal1 = self.Scope_Bottom [chan]
    cal2 = self.Scope_Top [chan]
    w1 = self.Scope_Canvas.GetClientSize ()[1] #- 12
    w2 = 0
    gain2 = 1.0 * ( w2 - w1 ) / ( cal2-cal1 )
    offset2 = 1.0 * ( cal2 * w1 - cal1 * w2  ) / ( cal2 - cal1 )

    """
    self.Scope_Canvas.Set_Channel ( chan, gain1, offset1, name,
                              cal1   = gain1 * gain2,
                              cal2   = gain2 * offset1 + offset2,
                              delay  = self.Scope_Delay_Len [chan],
                              color  = self.Scope_Signal_Color  [chan] )
    """
    self.Scope_Canvas.Set_Channel ( chan, gain1, offset1, name,
                              cal1   = self.Scope_Bottom [chan],
                              cal2   = self.Scope_Top [chan],
                              delay  = self.Scope_Delay_Len [chan],
                              color  = self.Scope_Signal_Color  [chan] )

  # *****************************************************************
  # called by the update display timer, to refresh the value labels
  # *****************************************************************
  def Refresh_Value_Labels ( self ) :
    data = self.Scope_Canvas.Get_DataSet (0)
    for chan in range ( len ( self.Scope_Signal_Names ) ):
      value = self.Scope_Signal_Gain [chan] * data [chan] + self.Scope_Signal_Offset[chan]
      self.Values[chan].SetLabel ( nice_number ( value ) )

  # *****************************************************************
  # *****************************************************************
  def _OnSize ( self, event ) :
    for chan in range ( len ( self.Scope_Signal_Names ) ) :
      self._Update_Channel ( chan )
    event.Skip ()

  # *****************************************************************
  # Starts the display update timer, when the form is made visible
  # *****************************************************************
  def _OnShowWindow ( self, event ):
    print ('Display SHOW')
    #if self.Frame.Shown:
    #  self.timer.Start( 100 )

  # *****************************************************************
  # Stops the display update timer, when the form is made invisible
  # *****************************************************************
  def _OnCloseWindow(self, event):
    if self.Dock.Shown:
      self.timer.Stop ()
      if self.Test and self.Ini :
        self.Save_Settings ( self.Ini)
      self.Dock.Show(False)
    event.Skip()

  # *****************************************************************
  # Display update timer, plots the signals and
  # once a while refreshes the value labels
  # *****************************************************************
  def OnTimer( self, event ):
    #print 'Display timer'
    if self.New_Data :
      #print 'Display timer', 'NEw DATA'
      self.New_Data = False
      self.Scope_Canvas.Draw ()

    # once a while also update the value labels
    self.sub_timer = ( self.sub_timer + 1 ) % 5
    if self.sub_timer == 0:
      self.Refresh_Value_Labels()

  # *****************************************************************
  # *****************************************************************
  def _Update_Border_Labels ( self, chan ):
    line = self.Scope_Signal_Names [chan].replace(']','').split('[')
    #if len(line) > 1 : line[1] = '[' + line[1]
    line.insert ( 1, str(self.Scope_Top [chan]))
    line = '  '.join ( line )
    self.Top_Labels[chan].SetLabel ( line )
    line = self.Scope_Signal_Names [chan].replace(']','').split('[')
    #if len(line) > 1 : line[1] = '[' + line[1]
    line.insert ( 1, str(self.Scope_Bottom [chan]))
    line = '  '.join ( line )
    self.Bottom_Labels[chan].SetLabel ( line )

  # *****************************************************************
  # Action upon the speed button clicks
  # *****************************************************************
  def OnButtonClick ( self, event ) :
    button = self.buttons_ID - event.GetId()
    if button > 1:
      chan = self.Selected_Signal
      if chan < 0 : return
      if   button == 2 :  # increase signal gain
        delta = ( self.Scope_Top [chan] - self.Scope_Bottom [chan] ) / 4
        self.Scope_Top [chan]    -= delta
        self.Scope_Bottom [chan] += delta
      elif button == 3 :  # decrease signal gain
        delta = ( self.Scope_Top [chan] - self.Scope_Bottom [chan] ) / 2
        self.Scope_Top [chan]    += delta
        self.Scope_Bottom [chan] -= delta
      elif button == 4 :  # shift signal up
        delta = ( self.Scope_Top [chan] - self.Scope_Bottom [chan] ) / 4
        self.Scope_Top [chan]    -= delta
        self.Scope_Bottom [chan] -= delta
      elif button == 5 :  # shift signal down
        delta = ( self.Scope_Top [chan] - self.Scope_Bottom [chan] ) / 4
        self.Scope_Top [chan]    += delta
        self.Scope_Bottom [chan] += delta
      elif button == 6 :  # change signal color
        # First block closing of the application
        if self.Set_Modal_Open : self.Set_Modal_Open ( True )
        try:
          from dialog_support import Color_Dialog
          color = Color_Dialog ( self.Dock, self.Scope_Signal_Color [chan] )
          self.Values[chan].SetForegroundColour ( color )
          self.Values_Labels[chan].SetForegroundColour ( color )
          self.Values_Labels[chan].SetLabel ( self.Scope_Signal_Names [chan] )

          self.Top_Labels[chan].SetForegroundColour ( color )
          self.Bottom_Labels[chan].SetForegroundColour ( color )

          self.Selected_Signalname.SetForegroundColour ( color )
          self.Selected_Signalname.SetLabel ( self.Scope_Signal_Names [chan] )

          if chan == 0 :
            self.Scope_History.Set_Channel ( self.Scope_Signal_Color  [chan] )

          """
          colordlg = wx.ColourDialog ( self.Dock )
          colordlg.GetColourData().SetChooseFull(True)

          if PG.Main_Form :
            cc = PG.Main_Form.Custom_Colors
            for i in range ( len ( cc ) ):
              colordlg.GetColourData().SetCustomColour ( i, cc[i] )

          colordlg.GetColourData().SetColour ( self.Scope_Signal_Color [chan])
          if colordlg.ShowModal() == wx.ID_OK:
            # get the new color and store it
            color = self.Scope_Signal_Color [chan] = colordlg.GetColourData().GetColour()
            self.Values[chan].SetForegroundColour ( color )
            self.Values_Labels[chan].SetForegroundColour ( color )
            self.Values_Labels[chan].SetLabel ( self.Scope_Signal_Names [chan] )

            self.Top_Labels[chan].SetForegroundColour ( color )
            self.Bottom_Labels[chan].SetForegroundColour ( color )

            self.Selected_Signalname.SetForegroundColour ( color )
            self.Selected_Signalname.SetLabel ( self.Scope_Signal_Names [chan] )

            if chan == 0 :
              self.Scope_History.Set_Channel ( self.Scope_Signal_Color  [chan] )

          if PG.Main_Form :
            cc = []
            for i in range ( 16 ):
              cc.append ( colordlg.GetColourData().GetCustomColour ( i ) )
            PG.Main_Form.Custom_Colors = cc
          colordlg.Destroy()
          """
        finally:
          # unlock possibility to close the application
          if self.Set_Modal_Open : self.Set_Modal_Open ( False )

      #print 'SSSSSS', delta, self.Scope_Top [chan], self.Scope_Bottom [chan]
      self._Update_Border_Labels ( chan )
      self._Update_Channel ( chan )

      self.Panel_Top.SendSizeEvent ()
      self.Panel_Bottom.SendSizeEvent ()
      #self.Frame.SendSizeEvent ()
      self.Dock.SendSizeEvent ()

    else:
      if self.Test :
        self.Dock.Set_Run_Simulation ( button != 0 )
      else :
        # PyLab_Works: toggle the start / stop output
        # which is a callcback function
        if self.Brick.Out [1] :
          self.Brick.Out [1] ( button != 0 )

  # *****************************************************************
  # If a signal label is clicked,
  # set the signal as active (available for changes by the speedbuttons)
  # *****************************************************************
  def OnLabelClick ( self, event ) :
    try :
      i = self.Values_IDs.index ( event.GetId() )
    except :
      return
    i = i // 2
    self.Selected_Signal = i
    s = self.Values_Labels[i].GetLabelText()
    self.Selected_Signalname.SetLabel (s)
    self.Selected_Signalname.SetForegroundColour ( self.Scope_Signal_Color [i] )


  # *****************************************************************
  # *****************************************************************
  def _OnLabel_Top_Click ( self, event ) :
    try :
      chan = self.Labels_IDs.index ( event.GetId() )
    except :
      return
    chan = chan // 2

    self.Selected_Signal = chan
    s = self.Values_Labels[chan].GetLabelText()
    self.Selected_Signalname.SetLabel (s)
    self.Selected_Signalname.SetForegroundColour ( self.Scope_Signal_Color [chan] )

    Names = [ 'For All Signals', 'AutoScale', 'Upper Value', 'Lower Value' ]
    Values = [ False, False, self.Scope_Top[chan], self.Scope_Bottom[chan] ]
    Types = [ bool, bool ]
    x,y = self.Top_Labels[chan].ScreenToClient ( (0, 0 ))
    x1,y = self.Scope_Canvas.ScreenToClient ( (0, 0 ))
    OK, Values = MultiLineDialog ( Names, Values, Types,
                                   'Set Borders Chan = ' +str(chan+1),
                                   width = 70,
                                   pos = ( abs(x), abs(y)+5 ) )
    if OK :
      #print Values
      channels = [chan]
      if Values[0] :
        channels = range ( len ( self.Scope_Signal_Names ) )
      for chan in channels:
        self.Scope_Top [chan]    = float ( Values [2] )
        self.Scope_Bottom [chan] = float ( Values [3] )
        self._Update_Border_Labels (chan)
        
      self.Panel_Top.SendSizeEvent ()
      self.Panel_Bottom.SendSizeEvent ()
      #self.Frame.SendSizeEvent ()
      self.Dock.SendSizeEvent ()

  # *****************************************************************
  # Occures just before another is selected
  # *****************************************************************
  def OnPageChanging ( self, event ) :
    old = event.GetOldSelection()
    if old == 1:
      self.Prepare_Scope_Signals ()
      self.timer.Start ( 100 )
    else :
      self.timer.Stop ()

    event.Skip()

  # *****************************************************************
  # Occures just after another is selected
  # *****************************************************************
  def OnPageChanged( self, event ):
    old = event.GetOldSelection()
    new = event.GetSelection()

    # In AUI-panes we've a problem, only the last sizer is used
    # therefore we always assign the actual sizer to the parent
    # and generate an size-event to ensure correct sizing of each page
    ##box = wx.BoxSizer ( wx.VERTICAL )
    if new == 1 :
      #box.Add ( self.panel_2, 1, wx.EXPAND)
      #box.Add ( self.NB, 1, wx.GROW | wx.ALL, 0 )
      #box.Add ( self.NB, 1, wx.EXPAND, 0 )
      ##box.Add ( self.NB, 1, wx.EXPAND )
      self._Copy_Vars_2_Grid ()
    else :
      #box.Add ( self.Splitter, 1, wx.EXPAND )
      ##box.Add ( self.NB, 1, wx.EXPAND )
      pass
    ##self.Dock.SetSizer ( box )
    self.Dock.SendSizeEvent ()
    event.Skip ()

  # *****************************************************************
  # *****************************************************************
  def Prepare_Scope_Signals ( self ) :
    self._Copy_Grid_2_Vars ()

    count = len ( self.Scope_Signal_Names )

    h = 16
    base = 60
    name = wx.StaticText( self.Panel_Left, -1, _(0, 'BackGround/Grid'),(5, base-8))
    name.SetForegroundColour ( wx.WHITE )
    name.Bind ( wx.EVT_LEFT_DOWN,  self.OnLabelClick )
    # be sure there are enough data storages and labels
    while self.Scope_Canvas.Get_NCurve() < count:
      i = len ( self.Values )
      self.Scope_Canvas.Add_Channel ( )

      name =  wx.StaticText( self.Panel_Left, -1, '',(5, i*(h+17) + 5 + base))
      name.SetToolTipString ( _(1, 'Click to Select' ) )
      self.Values_Labels.append ( name )
      self.Values_IDs.append ( name.GetId() )
      name.Bind ( wx.EVT_LEFT_DOWN,  self.OnLabelClick )

      value =  wx.StaticText( self.Panel_Left, -1, '',(5, i*(h+17) + 2+h + base))
      value.SetToolTipString ( _(1, 'Click to Select' ) )
      value.SetFont(wx.FFont( h, wx.ROMAN ) )
      self.Values.append ( value )
      self.Values_IDs.append ( value.GetId() )
      value.Bind ( wx.EVT_LEFT_DOWN,  self.OnLabelClick )

      # Create top and bottom labels
      label = wx.StaticText( self.Panel_Top, -1, 'S'+str(i) )
      label.SetToolTipString ( _(2, 'Click to Set Margins' ) )
      label.Bind ( wx.EVT_LEFT_DOWN,  self._OnLabel_Top_Click )
      self.Top_Labels.append ( label )
      self.Labels_IDs.append ( label.GetId() )
      self.Top_Sizer.Add ( label, 1, wx.EXPAND )

      label = wx.StaticText( self.Panel_Bottom, -1, 'S'+str(i) )
      label.SetToolTipString ( _(2, 'Click to Set Margins' ) )
      label.Bind ( wx.EVT_LEFT_DOWN,  self._OnLabel_Top_Click )
      self.Bottom_Labels.append ( label )
      self.Labels_IDs.append ( label.GetId() )
      self.Bottom_Sizer.Add ( label, 1, wx.EXPAND )

    # but not too many
    N = self.Scope_Canvas.Get_NCurve()
    if N > count:
      nd = count - N
      del self.Scope_Canvas.curves [ nd: ]
      for i in range ( -nd ) :
        self.Values [ -i-1 ].Destroy ()
        self.Values_Labels [ -i-1 ].Destroy ()

        self.Top_Sizer.Remove ( N - i -1 )
        self.Bottom_Sizer.Detach ( N - i -1 )
        self.Top_Labels [ -i-1 ].Destroy ()
        self.Bottom_Labels [ -i-1 ].Destroy ()

      del self.Values [ nd: ]
      del self.Values_Labels [ nd: ]
      del self.Top_Labels [ nd: ]
      del self.Bottom_Labels [ nd: ]
      del self.Values_IDs [ 2*nd: ]
      del self.Labels_IDs [ 2*nd: ]

    # Set and create (if necessary) the polylines
    #print 'TOP',self.Top_Labels
    #print 'NUM',self.Values
    for chan in range ( count ) :
      self.Values_Labels [chan].SetForegroundColour ( self.Scope_Signal_Color [chan] )
      self.Values_Labels [chan].SetLabel ( self.Scope_Signal_Names [chan] )

      self.Top_Labels [chan].SetForegroundColour ( self.Scope_Signal_Color [chan] )
      self.Top_Labels [chan].SetBackgroundColour ( self.Scope_Canvas.Brush.GetColour () )
      self.Bottom_Labels [chan].SetForegroundColour ( self.Scope_Signal_Color [chan] )
      self.Bottom_Labels [chan].SetBackgroundColour ( self.Scope_Canvas.Brush.GetColour () )
      self._Update_Border_Labels ( chan )

      self.Values [chan].SetForegroundColour ( self.Scope_Signal_Color [chan] )
      self._Update_Channel ( chan )

    #print 'HIST',self.Scope_History.Get_NCurve(),
    #print self.Scope_Signal_Gain   [0],
    #print self.Scope_Signal_Offset   [0]
    if count > 0 :
      self.Scope_History.Set_Channel ( self.Scope_Signal_Color  [0] )

    #self.signal_range = range ( self.Scope_Canvas.Get_NCurve() )
    self.Refresh_Value_Labels()
    self.Panel_Top.SendSizeEvent ()
    self.Panel_Bottom.SendSizeEvent ()

  # *****************************************************************
  # Copy all TREE datasets from checked items,
  # to the fast display parameters
  # *****************************************************************
  def _Copy_Grid_2_Vars ( self ) :
    self.Scope_Signal_Names = []
    self.Scope_Signal_Gain = []
    self.Scope_Signal_Offset = []
    self.Scope_Delay_Len = []
    self.Scope_Top = []
    self.Scope_Bottom = []
    self.Scope_Signal_Color = []
    for R in range ( self.Grid.table.GetNumberRows () ) :
      data = self.Grid.GetRowValue ( R )
      #print 'ROW',data
      if data[0] and data[1] :
        self.Scope_Signal_Names.append ( data[0] )

        # *****************************************************************
        # Calculates the fast display dataset,
        # for 1 item of the TREE dataset
        # *****************************************************************
        try :
          #print 'GRID-2-VAR', R, data(R,2), data(R,3), data(R,4)
          #gain = 1.0 * int(data[4]) / ( int(data[3]) - int(data[2]) )
          w1 = data[10]
          w2 = data[12]
          cal1 = data[11]
          cal2 = data[13]
          gain = 1.0 * ( w2 - w1 ) / ( cal2-cal1 )
          offset = 1.0 * ( cal1 * w2 - cal2 * w1 ) / ( cal2 - cal1 )
          self.Scope_Signal_Gain.append ( gain )
          self.Scope_Signal_Offset.append ( offset )
          self.Scope_Delay_Len.append ( data[7] )
          self.Scope_Bottom.append ( data[3] )
          self.Scope_Top.append ( data[4] )
        except :
          self.Scope_Signal_Gain.append ( 1.0 )
          self.Scope_Signal_Offset.append ( 50 )
          self.Scope_Delay_Len.append ( 0 )
          self.Scope_Bottom.append ( -100 )
          self.Scope_Top.append ( 100 )

        try :
          color = data[8]
          if not ( isinstance ( color, wx.Colour ) ) :
            color = wx.Color ( *color )
          self.Scope_Signal_Color.append ( color )
        except :
          self.Scope_Signal_Color.append ( wx.Color ( 255,0,255 ) )


  # *****************************************************************
  # Copy all fast display parameters
  # to the TREE datasets
  # *****************************************************************
  def _Copy_Vars_2_Grid ( self ) :
    N = 0
    for R in range ( self.Grid.table.GetNumberRows () ) :
      data = self.Grid.GetRowValue ( R )
      if data[0] and data[1] :
        #print 'VAR-2-GRID', R, data(R,2), data(R,3), data(R,4)
        #print 'VAR-2-GRID', type(data(R,2)), type(data(R,3)), type(data(R,4))
        try :
          self.Grid.table.SetValue ( R, 3, self.Scope_Bottom [N] )
          self.Grid.table.SetValue ( R, 4, self.Scope_Top [N] )
          self.Grid.table.SetValue ( R, 8, self.Scope_Signal_Color [N] )
        except :
          pass
        N += 1

  # *****************************************************************
  # Save all form settings and signal parameters
  # *****************************************************************
  def Save_Settings ( self, ini = None, key = None ):
    if not ( key ) :
      key = 'CS_'
    line = []
    line.append ( self.Splitter.GetSashPosition() )
    line.append ( self.Splitter_Plots.GetSashPosition() )
    line.append ( tuple ( self.Scope_Canvas.Color_Grid  ) )
    line.append ( tuple ( self.Scope_Canvas.Brush.GetColour ()  ) )

    for C in range ( self.Grid.table.GetNumberCols () ) :
      line.append ( self.Grid.GetColSize (C) )

    if ini :
      ini.Write ( key, line )
      if self.NB.GetSelection() == 0 :
        self._Copy_Vars_2_Grid ()

      #ini.Section = self.IniSection
      for R in range ( self.Grid.table.GetNumberRows () ) :
        line = []
        empty = True
        data = self.Grid.GetRowValue ( R )
        for D in data :
          if D != '' :
            empty = False
          if isinstance ( D, wx.Color ) :
            D = tuple ( D )
          line.append ( D )
        if not empty :
          ini.Write ( key + str(R), line )

    #return line

  # *****************************************************************
  # Loads all form settings
  # *****************************************************************
  def Load_Settings ( self, ini, key = None ) :
    if ini :
      if not ( key ) :
        key = 'CS_'
      ini.Section = self.IniSection

      line = ini.Read ( key, '' )
      if line :
        wx.CallLater ( wxGUI_Delay, self.Splitter.SetSashPosition, line [ 0 ] )
        wx.CallLater ( wxGUI_Delay, self.Splitter_Plots.SetSashPosition, line [ 1 ] )
        self.Scope_Canvas.Color_Grid = line [ 2 ]
        self.Scope_Canvas.Brush.SetColour ( line [ 3 ] )

        for C in range ( self.Grid.table.GetNumberCols () ) :
          self.Grid.SetColSize ( C, int ( line [C+4] ) )

      R = 0
      line = ini.Read ( key + str(R), '' )
      while line :
        #print 'CCSS',line,self.Grid.table.GetNumberCols ()
        if self.Grid.table.GetNumberRows () <= R :
          self.Grid.AppendRows ( R - self.Grid.table.GetNumberRows () + 1 )
          self.Grid.ForceRefresh()

        #print 'RRRRRR', R, self.Grid.table.GetNumberCols (),line
        for C in range ( self.Grid.table.GetNumberCols () ) :
          #print R,C,line[C]
          self.Grid.table.SetValue ( R, C, line [C] )

        R += 1
        line = ini.Read ( key + str(R) )


  # *****************************************************************
  # The following procedures should be implemented by the descendant
  # *****************************************************************
  #def Scope_Add_New_SampleSet ( self ) :
  # *****************************************************************

# ***********************************************************************



# ***********************************************************************
# This is the demo part, the part you will normally incorporate in your design.
# We have to perform the following tasks:
#   - indicate which signals should become available
#   - how the signals are organized (here a simple 1 level tree is shown,
#     in the animated demo a more complex organization is shown)
#   - how the signals are generated / calculated
# This code also contains some parts that will be normally placed in the
# applications main code, at least somewhere else.
# ***********************************************************************
class my_tScope_Form ( wx.MiniFrame ) :

  # *****************************************************************
  # *****************************************************************
  def __init__( self, main_form= None, ini = None, root_title = 'No Title' ) :

    self.main_form = main_form
    FormStyle = wx.DEFAULT_FRAME_STYLE | wx.TINY_CAPTION_HORIZ
    #if parent:
    #  FormStyle = FormStyle | wx.FRAME_FLOAT_ON_PARENT    # needs a parent

    Pos = ( 100, 100 )
    if ini :
      ini.Section = 'Device Scope'
      Pos  = ini.Read ( 'Pos',  ( 100, 100 ) )
      Size = ini.Read ( 'Size', ( 600, 400 ) )

    wx.MiniFrame.__init__(
        self, None, -1, 'JALsPy Scope',
        size  = Size,
        pos   = Pos,
        style = FormStyle)


    self.Scope = t_C_ScopePlot ( self, None, Ini=ini, Test=True )

    # Create the AD converter
    from control_adc import Simple_Test_Form
    frame2 = Simple_Test_Form (ini = ini)
    frame2.Show ( True )

    # Modal forms will toggle this,
    # so the main application knows if any modal form is open
    if self.main_form:
      self.main_form.Modal_Open = False

    # For this example we also need a timer to generate signals
    # YOU MUST BIND IN THIS WAY,
    # to allow the already present timer to work !!!
    self.Timer2 = wx.Timer ( self )
    self.Bind ( wx.EVT_TIMER, self.OnTimer2, self.Timer2)

    # we also create some data for this example
    self.SD_Max = 6684
    self.SD_p = 0
    SD0 = 50 + 100 * sin ( 0.1 * array ( range (self.SD_Max )))
    SD1 = 100 * ( SD0 > 100 )
    SD2 = array ( range (self.SD_Max )) % 30
    self.AR = []
    self.AR.append (SD0)
    self.AR.append (SD1)
    self.AR.append (SD2)

    # define the signals, first item is the parent node
    self.Scope.My_Signals = [ 'My Signals', 'Signal 1', 'Signal 2', 'Signal 3' ]

    self.Bind ( wx.EVT_CLOSE, self.OnClose )

    #self.SendSizeEvent()

  # *****************************************************************
  # *****************************************************************
  def OnClose ( self, event ) :
    if ini :
      ini.Section = 'Device Scope'
      ini.Write ( 'Pos',  self.GetPosition () )
      ini.Write ( 'Size', self.GetSize () )
    event.Skip ()

  # *****************************************************************
  # NORMALLY THIS ISN'T NECESSARY,
  # *****************************************************************
  def OnTimer2 (self, event):
    self.Scope_Add_New_SampleSet ()

  # *****************************************************************
  # NORMALLY THIS ISN'T NECESSARY,
  # This function is called by the scope form,
  # to give feedback of pressing step / run buttons
  # *****************************************************************
  def Set_Run_Simulation ( self, Run ) :
    if Run:
      # remove measurement cursors
      self.Scope.Scope_Canvas._Draw_Cursor ( 0, -1 )
      self.Scope.Scope_Canvas._Draw_Cursor ( 1, -1 )
      self.Timer2.Start ( 100 )
    else :
      self.Timer2.Stop ()

  # *****************************************************************
  # adds a new sample set to the rawdata buffer and plotlines
  # *****************************************************************
  def Scope_Add_New_SampleSet ( self ) :
    print (' add')
    if not ( self.Scope.Scope_Signal_Names ) :
      return
    else:
      print (' new data')
      data = []
      N2 = self.SD_p + 37
      for i,signal in enumerate ( self.Scope.Scope_Signal_Names ):
        x = self.AR[i][self.SD_p : N2]
        data.append (x)
      self.SD_p = N2 % self.SD_Max
      self.Scope.Scope_Canvas.Add_Data ( data )
# ***********************************************************************



# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':
  app = wx.PySimpleApp ()
  ini = inifile ( os.path.join (os.getcwd(), 'Scope_Form_Test.cfg' ))
  ini.Section = 'Device Scope'

  # Create the scope form and show it
  Main_Form = my_tScope_Form ( None, ini , 'Scope Test Application' )
  #def __init__( self, main_form= None, ini = None, root_title = 'No Title' ) :


  Main_Form.Show()

  app.MainLoop ()
  
  # The inifile can be used by more forms, so we close it here
  ini.Close ()
# ***********************************************************************
pd_Module ( __file__ )

"""
ROW ['sign 1', True, True, -200.0, 200.0, False, 1, wx.Colour(0, 128, 0, 255), 1, 0, 0, 100, 80000]
ROW ['s2', 1, True, -50.0, 150.0, False, 1, wx.Colour(255, 0, 255, 255), 2, 0, 0, 100, 80000]
ROW ['bp [mmHg]', 1, True, -200, 200, False, 1, wx.Colour(255, 255, 0, 255), 2, 0, 0, 100, 80000]
ROW ['bp [mmHg]', 1, True, -200, 200, False, 1, (128, 128, 255), 2, 0, 0, 100, 80000]
ROW ['', '', '', '', '', '', '', '', '', '', '', '', '']
"""
