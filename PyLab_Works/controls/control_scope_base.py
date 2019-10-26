import __init__
from base_control import *

# ***********************************************************************
# ***********************************************************************
from   PyLab_Works_Globals import _
from   numpy import *
import wx
import wx.grid as gridlib
from   wx.lib.expando import ExpandoTextCtrl, EVT_ETC_LAYOUT_NEEDED
import time

from   inifile_support import *
from   utility_support import *
from   dialog_support  import *
from   grid_support    import *
from   gui_support     import Create_wxGUI
from   array_support   import *

ct_none     = 0
ct_checkbox = 1
ct_radio    = 2

XDIV = YDIV = 10
MAX_SCREEN_WIDTH = 1680  # 19" widescreen TFT
# ***********************************************************************


from control_scope_channel import _Channel
from scope_plot            import _PlotCanvas
from scope_plot_hist       import _PlotCanvas_History


# ***********************************************************************
# ***********************************************************************
class tBase_Scope_with_History ( object ) :
  def __init__ ( self, Plots_Dock, Real_Time = False  ) :

    self.Frame          = Plots_Dock
    self.Real_Time      = Real_Time
    self.No_Data        = True
    self.Hist_Selection = 0
    self.x0             = -1
    self.x1             = -1

    # *****************************************************************
    # *****************************************************************
    self.Signal_Name   = []
    self.Signal_Color  = []
    self.Signal_Top    = []
    self.Signal_Bottom = []
    self.Signal_Gain   = []
    self.Signal_Offset = []

    #self.Values          = []
    #self.Values_IDs      = []
    self.Top_Labels      = []
    self.Bottom_Labels   = []
    self.Labels_IDs      = []
    #self.Selected_Signal = None

    self.Colors =[]
    self.Colors.append ( wx.RED   )
    self.Colors.append ( wx.BLUE  )
    self.Colors.append ( wx.BLACK )
    self.Colors.append ( wx.Colour ( 0,200,0 ) )
    self.Colors.append ( wx.Colour ( 0,  128,128 ) )
    self.Colors.append ( wx.Colour ( 128,0,128 ) )
    self.Colors.append ( wx.Colour ( 128,128,0 ) )
    self.Colors.append ( wx.Colour ( 128,128,0 ) )
    # *****************************************************************


    # *****************************************************************
    # Create at least one top and bottom label
    # *****************************************************************
    self.Initialized = False
    self._Create_Channel ( 0 )
    # *****************************************************************


    # *****************************************************************
    # Create the GUI
    # *****************************************************************
    GUI = """
    self.Splitter_Plots    ,SplitterVer
      self.Panel           ,PanelVer, 010
        self.Panel_Top     ,PanelHor, 11
          Label_Top        ,wx.StaticText
        self.Scope_Normal  ,_PlotCanvas         ,self  ,self.Real_Time
        self.Panel_Bottom  ,PanelHor
          Label_Bottom     ,wx.StaticText
      self.Scope_History   ,_PlotCanvas_History ,self  ,self.Real_Time
    """
    self.wxGUI = Create_wxGUI ( GUI, my_parent = 'Plots_Dock' ) #, IniName = 'self.Ini_File' )
    # *****************************************************************

    # Set the history window to 20%
    wx.CallLater ( wxGUI_Delay, self.Splitter_Plots.SetSashPosition, -70 )

    ##self.Scope_Normal.Real_Time = True
    ##self.Scope_History.Real_Time = True
    ##self.Scope_History.Set_Channel ( self.Colors [0] )
    self._Create_Channel_Labels ( 0, Label_Top, Label_Bottom )
    self.Initialized = True

    self.Parent_Notify_Chan_Params = None

  #def GetSize ( self ):
  #  return 50,50
  
  # *****************************************************************
  # *****************************************************************
  def _Create_Channel ( self, chan ) :
    self.Signal_Name  .append ( _(0,'Signal-' + str ( chan + 1 ) ) )
    self.Signal_Gain.  append ( None )
    self.Signal_Offset.append ( None )
    self.Signal_Color. append  ( self.Colors [chan] )
    self.Signal_Top.append    (  100 )
    self.Signal_Bottom.append ( -100 )

  # *****************************************************************
  # *****************************************************************
  def _Create_Channel_Labels ( self, chan, Label_Top, Label_Bottom ) :
    Label_Top.SetBackgroundColour ( self.Scope_Normal.BG_Color )
    Label_Top.SetForegroundColour ( self.Signal_Color [chan] )
    Label_Top.SetToolTip( _(2, 'Click to Set Margins' ) )
    Label_Top.Bind ( wx.EVT_LEFT_DOWN,  self._OnLabel_Top_Click )
    self.Top_Labels.append ( Label_Top )
    self.Labels_IDs.append ( Label_Top.GetId() )

    Label_Bottom.SetBackgroundColour ( self.Scope_Normal.BG_Color )
    Label_Bottom.SetForegroundColour ( self.Signal_Color [chan] )
    Label_Bottom.SetToolTip ( _(2, 'Click to Set Margins' ) )
    Label_Bottom.Bind ( wx.EVT_LEFT_DOWN,  self._OnLabel_Top_Click )
    self.Bottom_Labels.append ( Label_Bottom )
    self.Labels_IDs.append ( Label_Bottom.GetId() )

    self._Update_Channel (chan)

    # After changing a label, it's resized,
    # So we need to call the containers resizer
    self.Panel_Top.SendSizeEvent ()
    self.Panel_Bottom.SendSizeEvent ()

  # *****************************************************************
  # *****************************************************************
  def Channel_Increase_Gain ( self, chan ) :
    delta = ( self.Signal_Top [ chan ] - self.Signal_Bottom [ chan ] ) / 4
    self.Signal_Top    [ chan ] -= delta
    self.Signal_Bottom [ chan ] += delta
    self._Update_Channel ( chan )

  # *****************************************************************
  # *****************************************************************
  def Channel_Decrease_Gain ( self, chan ) :
    delta = ( self.Signal_Top [ chan ] - self.Signal_Bottom [ chan ] ) / 2
    self.Signal_Top    [ chan ] += delta
    self.Signal_Bottom [ chan ] -= delta
    self._Update_Channel ( chan )

  # *****************************************************************
  # *****************************************************************
  def Channel_Shift_Up ( self, chan ) :
    delta = ( self.Signal_Top [ chan ] - self.Signal_Bottom [ chan ] ) / 4
    self.Signal_Top    [ chan ] -= delta
    self.Signal_Bottom [ chan ] -= delta
    self._Update_Channel ( chan )

  # *****************************************************************
  # *****************************************************************
  def Channel_Shift_Down ( self, chan ) :
    delta = ( self.Signal_Top [ chan ] - self.Signal_Bottom [ chan ] ) / 4
    self.Signal_Top    [ chan ] += delta
    self.Signal_Bottom [ chan ] += delta
    self._Update_Channel ( chan )

  # *****************************************************************
  # *****************************************************************
  def Set_Background_Params ( self, BackGround, Grid = None ) :
    self.Scope_Normal.Set_Canvas ( BackGround, Grid )
    for label in self.Panel_Top.GetChildren () :
      label.SetBackgroundColour ( BackGround )
      label.Refresh ()
    for label in self.Panel_Bottom.GetChildren () :
      label.SetBackgroundColour ( BackGround )
      label.Refresh ()
    self.Scope_History.Set_Canvas ( BackGround )

  # *****************************************************************
  # *****************************************************************
  def Set_Channel_Params ( self, chan,
                           name   = None, color = None,
                           bottom = None, top   = None ) :
    """
    Change one or more parameters of the selected signal.
    This function will assure there are enough channels.
    """
    # be sure we have enough channels
    while len ( self.Signal_Name ) <= chan :
      self.Add_Channel ()

    # set the specified parameters
    if name :
      self.Signal_Name [ chan ] = name
    if color :
      self.Signal_Color [ chan ] = color
    if bottom :
      self.Signal_Bottom [ chan ] = bottom
    if top :
      self.Signal_Top [ chan ] = top

    self._Update_Channel ( chan )
    
  # *****************************************************************
  # *****************************************************************
  def Add_Channel ( self ) :
    chan = len ( self.Signal_Name )

    self._Create_Channel ( chan )

    Label_Top = wx.StaticText    ( self.Panel_Top             )
    self.Panel_Top_box.Add       ( Label_Top,    1, wx.EXPAND )
    Label_Bottom = wx.StaticText ( self.Panel_Bottom          )
    self.Panel_Bottom_box.Add    ( Label_Bottom, 1, wx.EXPAND )

    self._Create_Channel_Labels ( chan, Label_Top, Label_Bottom )

  # *****************************************************************
  # *****************************************************************
  def _OnLabel_Top_Click ( self, event ) :
    try :
      chan = self.Labels_IDs.index ( event.GetId() )
    except :
      return
    chan = chan // 2
    self.Selected_Signal = chan

    Names = [ 'For All Signals', 'AutoScale', 'Upper Value', 'Lower Value' ]
    Values = [ False, False, self.Signal_Top[chan], self.Signal_Bottom[chan] ]
    Types = [ bool, bool ]
    x,y  = self.Top_Labels[chan].ScreenToClient ( (0, 0 ) )
    x1,y = self.Scope_Normal.ScreenToClient     ( (0, 0 ) )
    OK, Values = MultiLineDialog ( Names, Values, Types,
                                   'Set Borders Chan = ' +str(chan+1),
                                   width = 70,
                                   pos = ( abs(x), abs(y)+5 ) )
    if OK :
      channels = [chan]
      if Values [0] :
        channels = range ( len ( self.Signal_Name ) )
      for chan in channels:
        if Values [1] :
          self._Set_Scale ( chan, True )
        else :
          self._Set_Scale ( chan, float ( Values [3] ), float ( Values [2] ) )

  # *************************************************************
  # *************************************************************
  def _Set_Scale ( self, chan, bottom, top = None ) :
    if bottom == True :
      #mins, maxs = self.Frame._Get_MinMax ( chan )
      mins, maxs = self._Get_MinMax ( chan )
      self.Signal_Top    [chan] = maxs
      self.Signal_Bottom [chan] = mins
    else :
      self.Signal_Top    [chan] = top
      self.Signal_Bottom [chan] = bottom

    self._Update_Channel (chan)
    if self.Parent_Notify_Chan_Params :
      self.Parent_Notify_Chan_Params ( chan,
         self.Signal_Name   [ chan ],
         self.Signal_Color  [ chan ],
         self.Signal_Bottom [ chan ],
         self.Signal_Top    [ chan ] )


  # *************************************************************
  # CALLBACK, to get autoscale parameters
  # *************************************************************
  def _Get_MinMax ( self, chan ) :
    if not ( self.Initialized ) : return

    x0 = self.x0
    x1 = self.x1
    if x0 ==  -1 :
      mins = min ( self.data [ chan, : ] )
      maxs = max ( self.data [ chan, : ] )
    else :
      mins = min ( self.data [ chan, self.x0 : self.x1 ] )
      maxs = max ( self.data [ chan, self.x0 : self.x1 ] )
      
    if self.Signal_Gain [ chan ] :
      print ( ' AutoScale', x0,mins,maxs,self.Signal_Gain   [ chan ],self.Signal_Offset   [ chan ])
      mins *= self.Signal_Gain   [ chan ]
      mins += self.Signal_Offset [ chan ]
      maxs *= self.Signal_Gain   [ chan ]
      maxs += self.Signal_Offset [ chan ]
    return mins, maxs


  # *****************************************************************
  # CALLBACK
  # The two cursors in the history array,
  # determine the visual part in the normal display
  # *****************************************************************
  def _On_History_Cursor_Selection ( self, x0, x1 ) :
    #v3print ( 'On_History_Cursor', x0, x1 )
    if not ( self.Initialized ) or self.No_Data :
      return

    # save values for autoscaling
    self.x0 = x0
    self.x1 = x0 + x1

    # if cursors are removed ReDraw the whole curve
    #v3print  ( 'SC On HIstory Cursor_Selextion', self.data.shape, x0 )
    if x0 < 0 :
      #self.Scope_Normal.Set_Data ()
      self.Scope_Normal.Set_Data ( self.data )
    else :
      # otherwise draw a part of the curve
      data = self.data [:, self.x0 : self.x1 ]
      self.Scope_Normal.Set_Data ( data )

  # *****************************************************************
  # The signal that's displayed in the history display
  # *****************************************************************
  def _On_History_Signal_Selection ( self, Signal ) :
    if not ( self.Initialized ) or self.No_Data :
      return

    self.Hist_Selection = Signal
    # Use the colors from the normal Scope
    self.Scope_History.Set_Channel_Color ( self.Colors [Signal] )
    #self.Scope_History.Append_Data ( self.data [ Signal ] )
    self.Scope_History.Set_Data ( self.data [ Signal ] )

  # *****************************************************************
  # Combine the signal calibration with screen calibration
  # *****************************************************************
  def _Update_Channel ( self, chan ) :
    gain1   = 1 #self.Scope_Signal_Gain   [chan]
    offset1 = 0 #self.Scope_Signal_Offset [chan]
    name    = self.Signal_Name  [chan]

    if self.Signal_Gain [ chan ] :
      g = 1.0 / self.Signal_Gain [ chan ]
      o = -self.Signal_Offset  [ chan ]* g
    else :
      g = 1
      o = 0

    #cal1 = self.Signal_Bottom [chan]
    #cal2 = self.Signal_Top    [chan]
    cal1 = g * self.Signal_Bottom [chan] + o
    cal2 = g * self.Signal_Top    [chan] + o

    #v3print ( 'Scope : _Update_Channel', chan, cal1, cal2 )
    self.Scope_Normal.Set_Channel ( chan, gain1, offset1, name,
                              cal1 = cal1,
                              cal2 = cal2,
                              delay  = 0, #self.Scope_Delay_Len [chan],
                              color  = self.Signal_Color  [chan] )

    line = self.Signal_Name [chan].replace(']','').split('[')

    # add the signal name to the history scope for selection
    self.Scope_History.Add_SignalName ( chan, line[0] )

    line.insert ( 1, nice_number ( self.Signal_Top [ chan ] ) )
    line = ' '  + '  '.join ( line )
    self.Top_Labels [ chan ].SetLabel ( line )
    self.Top_Labels [ chan ].SetForegroundColour ( self.Signal_Color [ chan ] )

    line = self.Signal_Name [chan].replace(']','').split('[')
    line.insert ( 1, nice_number ( self.Signal_Bottom [ chan ] ) )
    line = ' '  + '  '.join ( line )
    self.Bottom_Labels [ chan ].SetLabel ( line )
    self.Bottom_Labels [ chan ].SetForegroundColour ( self.Signal_Color [ chan ] )

    self.Panel_Top.SendSizeEvent ()
    self.Panel_Bottom.SendSizeEvent ()

  # *****************************************************************
  # Used by the main program to transport data (and parameters)
  #    .Calculate ( Display_Data, Display_Params )
  # *****************************************************************
  def Add_Data ( self, *args ) :
    if not ( self.Initialized ) :
      return

    #data, data_dim, params, Title = Analyze_TIO_Array ( *args )
    data, params = Analyze_TIO_Array ( *args )
    #print len(data), len(params),len(args)
    #params   = None
    data_dim = 1
    #Title    = 'aap' #None

    #if Title :
    #  self.Frame.SetTitle ( Title )

    # clear initialize flag
    self.No_Data = False

    # make a nice 2-dim array of all signals
    self.data = Make_2dim_Array ( data )

    #v3print  ( 'tBase_Scope_with_History.Add_Data,Title', Title )
    #v3print  ( 'tBase_Scope_with_History.Add_Data,data_dim', data_dim )
    #v3print  ( 'tBase_Scope_with_History.Add_Data,data', self.data.shape )
    #v3print  ( 'tBase_Scope_with_History.Add_Data,params', params )

    # be sure there are enough scope channels
    while self.data.shape[0] > self.Scope_Normal.Get_NCurve():
      self.Add_Channel ()

    # add channel information to the scope ( if any )
    if params :
      print ( 'Param', params, self.data.shape,self.Scope_Normal.Get_NCurve() )
      for chan, param in enumerate ( params ) :

        value = param.Get ( 'SignalName', None )
        Units = param.Get ( 'Units', None )
        print ( chan, value )
        if value :
          if Units :
            value = value.replace (']','').strip().split('[') [0]
            value += ' [' + Units + ']'
          self.Signal_Name [chan] = value
          #self._Update_Channel ( chan )
          self.Scope_History.Add_SignalName ( chan, self.Signal_Name [chan] )

        value = param.Get ( 'Calibrate', None )
        #v3print ( 'Calibrate', chan, value )
        if value :
          # in case of ( gain, offset )
          if len ( value ) == 2 :
            self.Signal_Gain   [ chan ] = value [0]
            self.Signal_Offset [ chan ] = value [1]
          else :
            print ( 'TODO: 2-points calibration')
          #self

        value = param.Get ( 'DisplayRange', None )
        if value :
          if value == True :
            self._Set_Scale ( chan, value )
          else :
            self._Set_Scale ( chan, float ( value[0] ), float ( value[1] ) )

        self._Update_Channel (chan)
          
        """
        try :

          param = paramx.Get ( 'Signal_Params', [] )
          #param = list ( paramx )
          self.Signal_Name [chan] = param.pop(0)
          value = param.pop(0)
          if value == True :
            self._Set_Scale ( chan, value )
          else :
            self._Set_Scale ( chan, float ( value ), float ( param.pop(0) ) )

          # signal color / linewidth
          value = param.pop(0)
          if value :
            self.Set_Channel_Params ( chan, color = wx.Color ( *value ) )

          value = param.pop(0)
          if value :
            v3print ( 'Linewidth (not implemented yet ) =', value )
        except :
          pass

        v3print ( 'Updateee',chan )
        self._Update_Channel (chan)
        self.Scope_History.Add_SignalName ( chan, self.Signal_Name [chan] )
        """


    # Add data to the normal display
    #v3print ( '_______SCOPEBASE ',self.Real_Time )
    #self.Scope_History.Append_Data ( self.data [ self.Hist_Selection] )

    # make history cursors invisible and and add data to history display
    #self.x0 = -1
    #self.x1 = -1
    #self.Scope_Normal.Add_Data_Static ( self.data )

    # if cursors are removed ReDraw the whole curve
    if self.Real_Time :
      self.Scope_Normal.Append_Data ( self.data )
      self.Scope_History.Append_Data ( self.data [ self.Hist_Selection] )
    else :
      #v3print ( self.x0,self.data.shape )
      if  self.x0 >= 0 :
        data = self.data [:, self.x0 : self.x1 ]
        self.Scope_Normal.Set_Data ( data )
      else :
        self.Scope_Normal.Set_Data ( self.data )
      self._On_History_Signal_Selection ( self.Hist_Selection )
  """
  def Add_Data ( self, data, params = None, Title = None ) :
    #print 'SI',self.Initialized
    if not ( self.Initialized ) :
      return

    if Title :
      self.Frame.SetTitle ( Title )

    # clear initialize flag
    self.No_Data = False

    # make a nice 2-dim array of all signals
    self.data = Make_2dim_Array ( data )

    # be sure there are enough scope channels
    while self.data.shape[0] > self.Scope_Normal.Get_NCurve():
      self.Add_Channel ()

    # add channel information to the scope ( if any )
    if params :
      for chan, param in enumerate ( params ) :
        self.Signal_Name [chan] = param[0]
        if param[1] == True :
          print 'autoscale'
        else :
          self.Signal_Top    [chan] = float ( param [2] )
          self.Signal_Bottom [chan] = float ( param [1] )

        self._Update_Channel (chan)
      self.Scope_History.Add_SignalName ( chan, param[0] )

    # Add data to the normal display
    #v3print ( '_______SCOPEBASE ',self.Real_Time )
    #self.Scope_History.Append_Data ( self.data [ self.Hist_Selection] )

    # make history cursors invisible and and add data to history display
    #self.x0 = -1
    #self.x1 = -1
    #self.Scope_Normal.Add_Data_Static ( self.data )
    
    # if cursors are removed ReDraw the whole curve
    if self.Real_Time :
      self.Scope_Normal.Append_Data ( self.data )
      self.Scope_History.Append_Data ( self.data [ self.Hist_Selection] )
    else :
      #v3print ( self.x0,self.data.shape )
      if  self.x0 >= 0 :
        data = self.data [:, self.x0 : self.x1 ]
        self.Scope_Normal.Set_Data ( data )
      else :
        self.Scope_Normal.Set_Data ( self.data )
      self._On_History_Signal_Selection ( self.Hist_Selection )
  """

  def Save_Settings ( self, ini, key = None ) :
    if ini :
      if not ( key ) :
        key = 'CS_'

      line =[]
      chan = 0
      for chan in range ( self.Scope_Normal.Get_NCurve() ) :
        line.append ( self.Signal_Top    [chan] )
        line.append ( self.Signal_Bottom [chan] )
      line = ini.Write ( key, line )

      line =[]
      line.append ( self.Splitter_Plots.GetSashPosition () )
      line.append ( self.Scope_Normal.Linear_Interpolation )

      line.append ( self.Scope_History.CursorType          )
      line.append ( self.Scope_History.Selected_Signal     )

      line.append ( tuple ( self.Scope_Normal.BG_Color   ) )
      line.append ( tuple ( self.Scope_Normal.Grid_Color ) )

      line.append ( self.x0 )
      line.append ( self.x1 )

      line = ini.Write ( key + 'Scope_Display', line )

  def Load_Settings ( self, ini, key = None ) :
    if not ( key ) :
      key = 'CS_'
    line = ini.Read ( key, '' )
    print ( '          LOAD', key, line )
    chan = 0
    while len(line) > 0:
      if chan >= self.Scope_Normal.Get_NCurve() :
        self.Add_Channel ()
      self.Signal_Top    [chan] = line [0]
      line.pop(0)
      if len(line) > 0 :
        self.Signal_Bottom [chan] = line [0]
        line.pop(0)
      self._Update_Channel (chan)
      chan += 1

    line = ini.Read ( key + 'Scope_Display', [] )
    print ( '          PPPP', line )
    if line :
      try :
        wx.CallLater ( wxGUI_Delay, self.Splitter_Plots.SetSashPosition, line.pop(0) )
        self.Scope_Normal.Linear_Interpolation  = line.pop(0)

        self.Scope_History.CursorType           = line.pop(0)
        self.Hist_Selection = \
          self.Scope_History.Selected_Signal    = line.pop(0)
        self.Scope_History.Set_Channel_Color ( self.Colors [self.Hist_Selection] )

        BG_Color   = wx.Colour ( *line.pop(0) )
        Grid_Color = wx.Colour ( *line.pop(0) )
        self.Set_Background_Params ( BG_Color, Grid_Color )

        # no data yet, so the following settings can't be restored (yet):
        #self._On_History_Signal_Selection ( self.Hist_Selection )
        x0 = line.pop (0)
        x1 = line.pop (0)
        self._On_History_Cursor_Selection ( self.x0, self.x1 )

      except :
        import traceback
        traceback.print_exc ( 5 )
# ***********************************************************************



# ***********************************************************************
# normal control for Pylab_Works
# ***********************************************************************
#class t_C_Scope_Plot ( My_Control_Class, tBase_Scope_with_History ):
class t_C_Scope_Plot ( tBase_Scope_with_History, My_Control_Class ):
  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )
    tBase_Scope_with_History.__init__ ( self, self.Dock )
    
    # for testpurposes
    self.TestPointer = 0
    self.TestMode = 0
    
  # ******************************************************
  def _Create_Test_Signals ( self, NPoints = 40 ) :
    rang = array ( range ( NPoints ) ) + self.TestPointer
    self.TestPointer = rang [ -1 ] + 1
    SD0 = 5 + 5 * sin ( 0.1 * rang )
    SD1 = 10 * ( SD0 > 5 )
    SD2 = rang % 20
    return SD0, SD1, SD2


  # ******************************************************
  def Test1 ( self ) :
    """
Generates 3 static signals: sine, square, sawtooth.
Subsequent calls, will toggle through different calling methods:
1: [ all data, all metadata ], metadata only name of signal 1
2: [ data / metadata mixed ], autoscale of square
3: [ even more mixing / nesting ], color change of sawtooth
    """
    # we also create some data for this example
    self.Real_Time               = False
    self.Scope_Normal.Real_Time  = self.Real_Time
    self.Scope_History.Real_Time = self.Real_Time

    SD0, SD1, SD2 = self._Create_Test_Signals ( 300 )
    S1 = 'Sine', -20, 20
    S2 = 'Square', -20, 20
    S3 = 'Sawtooth', -20, 20, (100,240,100), 5

    if self.TestMode == 0 :
      self.Add_Data ( SD0, SD1, SD2, S1 )

    elif self.TestMode == 1 :
      S2 = 'Square', True
      self.Add_Data ( SD0, S1, SD1, S2, SD2 )

    else :
      self.Add_Data ( S1, S2, SD0, S3, (SD1, SD2) )

    self.TestMode += 1
    self.TestMode %= 3

  # ******************************************************
  def Test2 ( self ) :
    """
Generates 3 dynamic signals: sine, square, sawtooth,
which will be shown in Real-Time mode.
    """
    self.Real_Time = True
    self.Scope_Normal.Real_Time  = self.Real_Time
    self.Scope_History.Real_Time = self.Real_Time

    SD0, SD1, SD2 = self._Create_Test_Signals ()
    self.Add_Data ( SD0, SD1, SD2 )
# ***********************************************************************


# ***********************************************************************
# Specially made for Signal WorkBench
# ***********************************************************************
class tScope_Display_Light ( wx.MiniFrame ):
  def __init__ ( self, owner, parentnode ) :
    self.owner = owner
    self.parentnode = parentnode

    ini = False
    Pos = ( 100, 100 )
    Size = ( 400, 300 )
    if ini :
      ini.Section = 'Device Scope'
      Pos  = ini.Read ( 'Pos',  Pos )
      Size = ini.Read ( 'Size', Size )

    FormStyle = wx.DEFAULT_FRAME_STYLE | wx.TINY_CAPTION_HORIZ
    wx.MiniFrame.__init__(
        self, None, -1, 'SWB: ' + owner.Tree.GetItemText ( parentnode ),
        size  = Size,
        pos   = Pos,
        style = FormStyle)

    self.Scope = tBase_Scope_with_History ( self )

    #self.Bind ( wx.EVT_KEY_DOWN, self._OnKeyDown )
    self.Bind ( wx.EVT_CLOSE,  self._OnClose )
    self.Show ()

  # *************************************************************
  # *************************************************************
  def _OnKeyDown ( self, event ) :
    print ( 'TTTT',event.GetKeyCode() ) # == wx.WXK_F7 :
    event.Skip()

  # *************************************************************
  # Notify the parent this Display is closed
  # *************************************************************
  def _OnClose ( self, event ) :
    self.owner.Notify_Closed ( self.parentnode )
    self.Destroy ()

# ***********************************************************************
pd_Module ( __file__ )
