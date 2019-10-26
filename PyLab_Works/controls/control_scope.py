import __init__

from   PyLab_Works_Globals import _
import wx
import wx.grid as gridlib
from   wx.lib.expando import ExpandoTextCtrl, EVT_ETC_LAYOUT_NEEDED

from   picture_support import Get_Image_16
from   inifile_support import *
from   utility_support import *
from   dialog_support  import *
from   grid_support    import *

from   control_scope_base import *
import copy


# ***********************************************************************
# ***********************************************************************
class t_C_Scope_Display ( My_Control_Class ) :
  # *************************************************************
  # Form creation
  # *************************************************************
  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )
    '''
    import copy
    import wx
    import wx.grid as gridlib
    from   grid_support    import *
    '''
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

    Image_List = Get_Image_List ()
    bmp_Pause = Image_List.GetBitmap ( 49 )
    bmp_Run   = Image_List.GetBitmap ( 50 )
    bmp_Plus  = Image_List.GetBitmap ( 56 )
    bmp_Minus = Image_List.GetBitmap ( 57 )
    bmp_Up    = Image_List.GetBitmap ( 45 )
    bmp_Down  = Image_List.GetBitmap ( 44 )
    bmp_Color = Image_List.GetBitmap ( 48 )

    b_size = ( 22, 22 )
    GUI = """
    self.NB            ,wx.Notebook  ,style = wx.BK_LEFT
      self.Splitter      ,SplitterHor  ,name = 'Scope'  ,style = wx.NO_BORDER
        self.Panel_Left    ,wx.Panel
          B_Pause     ,BmpBut  ,bitmap = bmp_Pause  ,pos = (2,2)   ,size = b_size
          B_Run       ,BmpBut  ,bitmap = bmp_Run    ,pos = (2,27)  ,size = b_size
          B_Plus      ,BmpBut  ,bitmap = bmp_Plus   ,pos = (27,2)  ,size = b_size
          B_Minus     ,BmpBut  ,bitmap = bmp_Minus  ,pos = (27,27) ,size = b_size
          B_Up        ,BmpBut  ,bitmap = bmp_Up     ,pos = (52,2)  ,size = b_size
          B_Down      ,BmpBut  ,bitmap = bmp_Down   ,pos = (52,27) ,size = b_size
          B_Color     ,BmpBut  ,bitmap = bmp_Color  ,pos = (77,2)  ,size = b_size
          self.Sel_Signal  ,wx.StaticText, label = '--', pos = ( 77, 27 )
          self.BG     ,wx.StaticText  ,label = _(0, 'BackGround')  ,pos = (2, 52)
          self.GR     ,wx.StaticText  ,label = _(0, 'Grid')        ,pos = (70, 52)
        self.Panel_Right   ,wx.Panel
          self.Scope       ,tBase_Scope_with_History  ,Real_Time = True
      self.grid          ,Base_Table_Grid  ,data_values, data_types, data_defs, name='Settings'
    """
    self.wxGUI = Create_wxGUI ( GUI, my_parent = 'self.Dock' )

    self.Panel_Left.SetBackgroundColour ( wx.BLACK )

    B_Pause.SetToolTip ( _(0, 'Pause Recording'                    ) )
    B_Run  .SetToolTip ( _(0, 'Start Recording'                    ) )
    B_Plus .SetToolTip ( _(0, 'Increase selected signal Amplitude' ) )
    B_Minus.SetToolTip ( _(0, 'Decrease selected signal Amplitude' ) )
    B_Up   .SetToolTip( _(0, 'Shift selected signal Up'           ) )
    B_Down .SetToolTip ( _(0, 'Shift selected signal Down'         ) )
    B_Color.SetToolTip ( _(0, 'Set Color of selected signal'       ) )

    self.Button_IDs = []
    self.Button_IDs.append ( B_Pause.GetId () )
    self.Button_IDs.append ( B_Run  .GetId () )
    self.Button_IDs.append ( B_Plus .GetId () )
    self.Button_IDs.append ( B_Minus.GetId () )
    self.Button_IDs.append ( B_Up   .GetId () )
    self.Button_IDs.append ( B_Down .GetId () )
    self.Button_IDs.append ( B_Color.GetId () )

    self.Sel_Signal.SetForegroundColour ( wx.WHITE )
    self.Sel_Signal.SetToolTip ( _( 0, 'Selected Signal') )

    self.BG.SetForegroundColour ( wx.WHITE )
    self.BG.Bind ( wx.EVT_LEFT_DOWN,  self._OnLabelClick )
    self.GR.SetForegroundColour ( wx.RED )
    self.GR.Bind ( wx.EVT_LEFT_DOWN,  self._OnLabelClick )

    Set_NoteBook_Images ( self.NB, ( 47, 76 ) )

    wx.CallLater ( wxGUI_Delay, self.Splitter.SetSashPosition, 102 )

    self.New_Data = False
    self.Ny = 100 # 200
    self.Nx = 600  # gives 10 divisions

    self.Display_NChan   = 0
    
    self.Values_Value    = [ 0               , 0                ]
    self.Values_Label    = [ self.BG         , self.GR          ]
    self.Values_ID       = [ self.BG.GetId (), self.GR.GetId () ]
    self.Selected_Signal = None

    self.Num_Value_Timer = wx.Timer ( self.Dock )

    # reload previous settings
    #if self.Test :
    if self.Ini :
      self.Ini.Section = self.IniSection
      self.Load_Settings ( self.Ini )

    #self.Dock.Bind ( wx.EVT_NOTEBOOK_PAGE_CHANGED,  self.OnPageChanged )
    self.Dock.Bind ( wx.EVT_NOTEBOOK_PAGE_CHANGING, self._OnPageChanging )
    self.Dock.Bind ( wx.EVT_CLOSE,  self._OnCloseWindow )
    self.Dock.Bind ( wx.EVT_TIMER,  self._OnTimer,  self.Num_Value_Timer)
    self.Dock.Bind ( wx.EVT_BUTTON, self._OnButtonClick )

    self.Scope.Parent_Notify_Chan_Params = self.Notify_Chan_Params

    self.Prepare_Scope_Signals ()
    self.Num_Value_Timer.Start ( 500 )

    # for testpurposes
    self.Timer_Test  = None

    # NOTEBOOK resizes wrong,
    # too much space for tabs,
    # this will correct it
    wx.CallAfter ( self.NB.SendSizeEvent )

  # *****************************************************************
  # *****************************************************************
  def Kill ( self ) :
    self.Num_Value_Timer.Stop ()
    if self.Timer_Test :
      self.Timer_Test.Stop ()

  # *****************************************************************
  # *****************************************************************
  def Add_Data ( self, *args ) :
    data, params = Analyze_TIO_Array ( *args )

    # pass the data to the scope
    self.Scope.Add_Data ( *args )

    # Use the params to update names
    if params :
      print ( 't_C_Scope_Display: Set Params through Add_Data')
      for chan, param in enumerate ( params ) :

        value = param.Get ( 'SignalName', None )
        Units = param.Get ( 'Units', None )
        print ( chan, value )
        if value :
          if Units :
            value = value.replace (']','').strip().split('[') [0]
            value += ' [' + Units + ']'
          self.Values_Label[chan+2].SetLabel ( value )
          self.grid.table.SetValue ( chan, 0, value )

        value = param.Get ( 'Calibrate', None )
        #v3print ( 'Calibrate', chan, value )
        if value :
          # in case of ( gain, offset )
          if len ( value ) == 2 :
            self.Scope.Signal_Gain   [ chan ] = value [0]
            self.Scope.Signal_Offset [ chan ] = value [1]
          else :
            print ( 'TODO: 2-points calibration')
        self

  # *****************************************************************
  # called by the update display timer, to refresh the value labels
  # *****************************************************************
  def Refresh_Value_Labels ( self ) :
    data = self.Scope.Scope_Normal.Get_DataSet (0)
    for chan in range ( self.Display_NChan ):
      self.Values_Value [chan+2].SetLabel ( nice_number ( data [ chan ] ) )

  # *****************************************************************
  # Starts the display update timer, when the form is made visible
  # *****************************************************************
  def _OnShowWindow ( self, event ):
    pass #print 'Display SHOW'
    #if self.Frame.Shown:
    #  self.Num_Value_Timer.Start( 100 )

  # *****************************************************************
  # Stops the display update timer, when the form is made invisible
  # *****************************************************************
  def _OnCloseWindow(self, event):
    if self.Dock.Shown:
      self.Num_Value_Timer.Stop ()
      if self.Test and self.Ini :
        self.Save_Settings ( self.Ini)
      self.Dock.Show(False)
    event.Skip()

  # *****************************************************************
  # *****************************************************************
  def _OnTimer( self, event = None ):
    #v3print ( 'Num Timer' )
    self.Refresh_Value_Labels()

  # *****************************************************************
  # Action upon the speed button clicks
  # *****************************************************************
  def _OnButtonClick ( self, event ) :
    button = self.Button_IDs.index ( event.GetId () )
    chan = self.Selected_Signal
    
    if 1 < button < 6 :
      if chan == None :
        return

      chan -= 2

      if   button == 2 :
        self.Scope.Channel_Increase_Gain ( chan )

      elif button == 3 :
        self.Scope.Channel_Decrease_Gain ( chan )

      elif button == 4 :
        self.Scope.Channel_Shift_Up ( chan )

      elif button == 5 :
        self.Scope.Channel_Shift_Down ( chan )

    elif button == 6 :  # change signal color
      if chan == None :
        return

      Color = self.Values_Label [ chan ].GetForegroundColour ()
  
      from dialog_support import Color_Dialog
      Color = Color_Dialog ( self.Dock, Color )
        #self.Scope.Signal_Color [ chan ] )

      if Color :
        self.Values_Label [ chan ].SetForegroundColour ( Color )
        self.Sel_Signal.SetForegroundColour ( Color )

        if chan == 0 :
          #v3print ( 'MMKLOP', type(Color), Color )
          R, G, B = Color.asTuple ()
          R = 255 - R
          G = 255 - G
          B = 255 - B
          Invers_Color = wx.Colour ( R, G, B )

          self.Sel_Signal.SetForegroundColour ( Invers_Color )
          self.Values_Label [ chan ].SetForegroundColour ( Invers_Color )

          self.Panel_Left.SetBackgroundColour ( Color )
          self.Scope.Set_Background_Params ( Color )
        elif chan == 1 :
          self.Scope.Set_Background_Params ( None, Color )
        else :
          self.Values_Value [ chan ].SetForegroundColour ( Color )
          self.Scope.Set_Channel_Params ( chan-2, color = Color )

        ##self.Values_Label[chan].SetLabel ( self.Scope.Signal_Name [ chan ] )
        ##self.Sel_Signal.SetLabel ( self.Scope_Signal_Names [ chan ] )
        self.Panel_Left.Refresh ()

    else:
      if self.Test :
        self.Dock.Set_Run_Simulation ( button != 0 )
      else :
        # PyLab_Works: toggle the start / stop output
        # which is a callback function
        #if self.Brick.Out [1] :
        #  self.Brick.Out [1] ( button != 0 )
        self.P[0] = button != 0

  # *****************************************************************
  # If a signal label is clicked,
  # set the signal as active (available for changes by the speedbuttons)
  # *****************************************************************
  def _OnLabelClick ( self, event ) :
    try :
      i = self.Values_ID.index ( event.GetId() )
    except :
      return
    if i > 1 :
      i = 1 + i // 2
      
    self.Selected_Signal = i
    S = self.Values_Label [i]
    self.Sel_Signal.SetLabel            ( S.GetLabelText() )
    self.Sel_Signal.SetForegroundColour ( S.GetForegroundColour () )
      ##self.Scope.Signal_Color [i] )

  # *****************************************************************
  # Occures just before another is selected
  # *****************************************************************
  def _OnPageChanging ( self, event ) :
    old = event.GetOldSelection()
    if old == 1:
      self.Prepare_Scope_Signals ()
      self.Num_Value_Timer.Start ( 100 )
    else :
      self.Num_Value_Timer.Stop ()

    event.Skip()

  # *****************************************************************
  # *****************************************************************
  def Prepare_Scope_Signals ( self ) :
    self._Copy_Grid_2_Vars ()

    count = self.Display_NChan
    #print 'PrepSS 1',self.Scope.Scope_Normal.Get_NCurve(),count

    h = 16
    base = 60
    # be sure there are enough data storages and labels
    while self.Scope.Scope_Normal.Get_NCurve() < count:
      self.Scope.Scope_Normal.Add_Channel ( )

    while len ( self.Values_Value ) < count + 2 :
      i = len ( self.Values_Value ) - 2
      name =  wx.StaticText( self.Panel_Left, -1, '',(5, i*(h+17) + 5 + base))
      name.SetToolTip ( _(1, 'Click to Select' ) )
      self.Values_Label.append ( name )
      self.Values_ID.append ( name.GetId() )
      name.Bind ( wx.EVT_LEFT_DOWN,  self._OnLabelClick )

      value =  wx.StaticText( self.Panel_Left, -1, '',(5, i*(h+17) + 2+h + base))
      value.SetToolTip ( _(1, 'Click to Select' ) )
      value.SetFont(wx.FFont( h, wx.ROMAN ) )
      self.Values_Value.append ( value )
      self.Values_ID.append ( value.GetId() )
      value.Bind ( wx.EVT_LEFT_DOWN,  self._OnLabelClick )

    # but not too many
    N = self.Scope.Scope_Normal.Get_NCurve()
    #print 'PrepSS 2',N,count
    if N > count+1:
      nd = count+1 - N
      del self.Scope.Scope_Normal.curves [ nd: ]
      for i in range ( -nd ) :
        self.Values_Value [ -i-1 ].Destroy ()
        self.Values_Label [ -i-1 ].Destroy ()

        self.Top_Sizer.Remove ( N - i -1 )
        self.Bottom_Sizer.Detach ( N - i -1 )
        self.Top_Labels [ -i-1 ].Destroy ()
        self.Bottom_Labels [ -i-1 ].Destroy ()

      del self.Values_Value [ nd: ]
      del self.Values_Label [ nd: ]
      del self.Values_ID    [ 2*nd: ]

    # Set and create (if necessary) the polylines
    for chan in range ( count ) :
      self.Values_Label [chan+2].SetForegroundColour ( self.Scope.Signal_Color [chan] )
      self.Values_Label [chan+2].SetLabel            ( self.Scope.Signal_Name  [chan] )
      self.Values_Value [chan+2].SetForegroundColour ( self.Scope.Signal_Color [chan] )
      #self.Values_Value [chan].SetLabel ( '6.84')

    #self.signal_range = range ( self.Scope.Scope_Normal.Get_NCurve() )
    ## ??self.Refresh_Value_Labels ()

    self.Refresh_Value_Labels()


  # *****************************************************************
  # Copy all TREE datasets from checked items,
  # to the fast display parameters
  # *****************************************************************
  def _Copy_Grid_2_Vars ( self ) :

    indx = 0
    for R in range ( self.grid.table.GetNumberRows () ) :
      data = self.grid.GetRowValue ( R )
      #print 'ROW',data
      if data[0] and data[1] :
        # *****************************************************************
        # Calculates the fast display dataset,
        # for 1 item of the TREE dataset
        # *****************************************************************
        w1 = data[10]
        w2 = data[12]
        cal1 = data[11]
        cal2 = data[13]
        ## self.Scope_Delay_Len.append ( data[7] )

        color = data[8]
        if not ( isinstance ( color, wx.Colour ) ) :
          color = wx.Colour ( *color )

        self.Scope.Set_Channel_Params ( indx, data[0], color, data[3], data[4])
        indx += 1

    self.Display_NChan = indx
    
  # *****************************************************************
  # *****************************************************************
  def Notify_Chan_Params ( self, chan, name, color, bottom, top ) :
    R = chan
    #self.grid.Grid.table.SetValue ( R, 0, name )
    self.grid.table.SetValue ( R, 3, bottom )
    self.grid.table.SetValue ( R, 4, top    )
    self.grid.table.SetValue ( R, 8, color  )

  # *****************************************************************
  # Save all form settings and signal parameters
  # *****************************************************************
  def Save_Settings ( self, ini = None, key = None ):
    if ini :
      if not ( key ) :
        key = 'CS_'

      ini.Section = self.IniSection
      line = []
      line.append ( self.Splitter.GetSashPosition() )
      for C in range ( self.grid.table.GetNumberCols () ) :
        line.append ( self.grid.GetColSize (C) )
      ini.Write ( key + 'Scope_', line )

      for R in range ( self.grid.table.GetNumberRows () ) :
        line = []
        empty = True
        data = self.grid.GetRowValue ( R )
        for D in data :
          if D != '' :
            empty = False
          if isinstance ( D, wx.Colour ) :
            D = tuple ( D )
          line.append ( D )
        if not empty :
          ini.Write ( key + 'Scope_' + str(R), line )

      self.Scope.Save_Settings ( ini, key )

  # *****************************************************************
  # Loads all form settings
  # *****************************************************************
  def Load_Settings ( self, ini, key = None ) :
    if ini :
      ini.Section = self.IniSection

      default = [ 139, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80 ]

      if not ( key ) :
        key = 'CS_'
        
      line = ini.Read ( key + 'Scope_', default )
      print ('    Scope,Line', key, line)
      wx.CallLater ( wxGUI_Delay, self.Splitter.SetSashPosition, line [ 0 ] )
      for C in range ( self.grid.table.GetNumberCols () ) :
        self.grid.SetColSize ( C, line [C+1] )

      for R in range ( self.grid.table.GetNumberRows () ) :
        line = ini.Read ( key + 'Scope_' + str(R), '' )
        if line :
          if self.grid.table.GetNumberRows () <= R :
            self.grid.AppendRows ( R - self.grid.table.GetNumberRows () + 1 )
            self.grid.ForceRefresh()

          for C in range ( self.grid.table.GetNumberCols () ) :
            self.grid.table.SetValue ( R, C, line [C] )

      self.Scope.Load_Settings ( ini, key )

      # transport color also to the own background
      self.Panel_Left.SetBackgroundColour ( self.Scope.Scope_Normal.BG_Color )





  # ******************************************************
  def _Create_Test_Signals ( self, NPoints = 4 ) :
    """
    Generates signals for testing this control.
    """
    rang = array ( range ( NPoints ) ) + self.TestPointer
    self.TestPointer = rang [ -1 ] + 1
    SD0 = 5 + 5 * sin ( 0.1 * rang )
    SD1 = 10 * ( SD0 > 5 )
    SD2 = rang % 20
    return SD0, SD1, SD2

  # ******************************************************
  def _OnTimer_Test ( self, event ) :
    """
    Only create new samples if the scope is running
    """
    print ( 'TEST Timer' )
    if self.P[0] :
      SD0, SD1, SD2 = self._Create_Test_Signals ()
      self.Scope.Add_Data ( SD0, SD1, SD2 )

  # ******************************************************
  def Test1 ( self ) :
    """
Generates 3 dynamic signals: sine, square, sawtooth.
This button should only be pressed once to start the Test-Timer,
after that, you can control the dataflow with the scope controls.
    """
    if not ( self.Timer_Test ) :
      self.TestPointer = 0
      self.TestMode    = 0
      self.Timer_Test  = wx.Timer ( self.TopFrame )
      self.TopFrame.Bind ( wx.EVT_TIMER, self._OnTimer_Test, self.Timer_Test )

    if self.Timer_Test.IsRunning () :
      self.Timer_Test.Stop ()
    else :
      # remove measurement cursors
      self.Scope.Scope_Normal._Draw_Cursor ( 0, -1 )
      self.Scope.Scope_Normal._Draw_Cursor ( 1, -1 )
      self.Timer_Test.Start ( 100 )
      self.P[0] = True
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
class Test_Control_Scope ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Test of Control_Scope', ini )

    self.Scope = t_C_Scope_Display ( self, None, Ini=ini, Test=True )

    # Create the AD converter
    #from control_adc import Simple_Test_Form
    #frame2 = Simple_Test_Form (ini = ini)
    #frame2.Show ( True )

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
      self.Scope.Scope.Scope_Normal._Draw_Cursor ( 0, -1 )
      self.Scope.Scope.Scope_Normal._Draw_Cursor ( 1, -1 )
      self.Timer2.Start ( 100 )
    else :
      self.Timer2.Stop ()

  # *****************************************************************
  # adds a new sample set to the rawdata buffer and plotlines
  # *****************************************************************
  def Scope_Add_New_SampleSet ( self ) :
    data = []
    N2 = self.SD_p + 3
    if N2 > self.SD_Max :
      N2 = self.SD_Max
    for i in range ( self.Scope.Display_NChan ):
      x = self.AR[i][self.SD_p : N2]
      data.append (x)
      
    self.SD_p = N2 % self.SD_Max
    self.Scope.Add_Data ( data )
# ***********************************************************************



# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':

  Test_Defs ( 1 )

  if Test ( 1 ) :
    My_Main_Application ( Test_Control_Scope )

# ***********************************************************************
pd_Module ( __file__ )


"""
ROW ['sign 1', True, True, -200.0, 200.0, False, 1, wx.Colour(0, 128, 0, 255), 1, 0, 0, 100, 80000]
ROW ['s2', 1, True, -50.0, 150.0, False, 1, wx.Colour(255, 0, 255, 255), 2, 0, 0, 100, 80000]
ROW ['bp [mmHg]', 1, True, -200, 200, False, 1, wx.Colour(255, 255, 0, 255), 2, 0, 0, 100, 80000]
ROW ['bp [mmHg]', 1, True, -200, 200, False, 1, (128, 128, 255), 2, 0, 0, 100, 80000]
ROW ['', '', '', '', '', '', '', '', '', '', '', '', '']
"""
