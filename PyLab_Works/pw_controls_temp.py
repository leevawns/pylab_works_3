import __init__

"""
print 'peip'
print 'piep'
import os
import sys
subdirs = [ '../support' ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
"""

import subprocess
import time
from   stat import *

# !!! import wx before any support library !!!
# otherwise the IDE won't do auto-suggest
import wx

from dialog_support import *
from inifile_support import *
from file_support import *
from numpy import fromfile, size, transpose


ADC_Killed   = 0
ADC_Stopped  = 1
ADC_Started  = 2
ADC_Buffer_Switching = 3

# ***********************************************************************
# ***********************************************************************
class AD_Converter ( object ) :


  def __init__ ( self,  Dock,     # the frame/panel/... where we can put
                                  # the GUI controls that will catch events
                 Brick,           # the Brick, with its inputs and outputs
                 ini  = None,     # inifile to store and reload settings
                 Test = False ):  # if True, testmode with buildin examples

    self.Dock  = Dock
    self.Brick = Brick
    self.Test  = Test
    self.Ini   = ini

    # *************************************************************
    # if the ADC is used a s Brick in PyLab_Works,
    # something special needs to be done,
    # we connect the input value to a callback function
    # *************************************************************
    if self.Brick :
      self.Brick.In [1] = self.Start_Stop

    # *************************************************************
    # *************************************************************
    self.Path = os.getcwd ()
    self.Filename_Start  = os.path.join (self.Path, 'midadc_start.txt')
    self.Filename_Answer = os.path.join (self.Path, 'midadc_answer.txt')
    self.Filename_Kill   = os.path.join (self.Path, 'midadc_kill.txt')
    self.Filename_Buf1   = os.path.join (self.Path, 'midadc1.dat')
    self.Filename_Buf2   = os.path.join (self.Path, 'midadc2.dat')
    self.Data_FileName   = [ self.Filename_Buf1, self.Filename_Buf2 ]
    self.BufNr = False
    self.BufP = 0
    self.Buf_Max = 10000
    self.Navailable = 0

    # create the wx-components here and
    # set as parent : "self.Dock" !!
    # ....

    self.Graph = wx.TextCtrl ( self.Dock, -1,  style = wx.TE_MULTILINE|wx.TE_PROCESS_ENTER )

    self.Panel = wx.Panel ( self.Dock, -1 )
    self.Button_Start = wx.Button ( self.Panel, -1, "Start",
                                    pos = ( 0, 0 ), size = ( 40, -1 ) )
    self.Button_Start.Bind ( wx.EVT_BUTTON, self.OnStart, self.Button_Start )

    self.T1 = wx.StaticText ( self.Panel, -1, 'ADC type', pos = ( 50, 3 ))
    ADC_Types = [ 'Timer', 'Recorded File', 'Delphi Debug', 'FysioFlex', 'NI-DAQmx',
                  'SoundCard' ]
    self.Combo_ADC = wx.ComboBox ( self.Panel, -1,
                                   pos = ( 98, 0 ), size = ( 100, -1 ),
                                   choices = ADC_Types,
                                   style = wx.CB_DROPDOWN )
    self.Combo_ADC.SetSelection ( 1 )
    
    self.T2 = wx.StaticText ( self.Panel, -1, 'N chan', pos = ( 210, 3 ))
    self.Spin_NChan = wx.SpinCtrl ( self.Panel, initial = 2,
                                    pos = ( 245, 0 ), size = ( 50, -1 ),
                                    min = 1, max = 16 )

    self.T3 = wx.StaticText ( self.Panel, -1, 'Fsamp', pos = ( 310, 3 ))
    self.Fsamp = wx.TextCtrl ( self.Panel, value = '100',
                               pos = ( 342, 0 ), size = ( 50, -1 ))

    bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_BUTTON, (16,16))
    self.ADC_FileB = wx.BitmapButton ( self.Panel, -1 , bmp,
                                  pos = ( 0, 25 ) )
    self.ADC_FileB.Bind ( wx.EVT_BUTTON, self.OnFileB, self.ADC_FileB )
    self.ADC_File = wx.TextCtrl ( self.Panel, -1, "D:\d_midorg\mid-data\polygraf\crcn1\ipc_4.d1",
                                  pos = ( 25, 25 ), size = ( 370, 24 ) )

    self.State = ADC_Killed
    # Be sure there is no answer file yet
    if File_Exists ( self.Filename_Answer ) :
      File_Delete ( self.Filename_Answer )
    
    # *************************************************************
    # Create Sizers,
    # BUT let the parent do the resizing !!
    # *************************************************************
    Sizer = wx.BoxSizer ( wx.VERTICAL )
    Sizer.Add ( self.Graph, 1, wx.EXPAND )
    Sizer.Add ( self.Panel, 0 )
    Dock.SetSizer ( Sizer )
    # *************************************************************

    Dock.Bind ( wx.EVT_CLOSE, self.OnClose )

    # the Timer must be bound to Dock
    self.Timer = wx.Timer ( Dock )
    # the third parameter is essential to allow other timers
    Dock.Bind ( wx.EVT_TIMER, self.OnTimer, self.Timer)

  def OnFileB ( self, event ) :
    try :
      filepath, filename = path_split ( self.ADC_File )
    except:
      filename = ''
      filepath = os.getcwd()
    filename= AskFileForOpen ( filepath, filename )
    if filename: self.ADC_File.SetValue ( filename )

  def Read_Data ( self ) :
    #self.datafile = open ( self.Filename_Buf1,'rb')       # Readonly Binary
    pass

  def OnTimer ( self, event ) :
    self.Fetch_Samples ()
    
  def Fetch_Samples ( self ):
    #print 'FETCH',self.State
    if   self.State == ADC_Killed :
      # test if there's an answer file from the sample program
      try :
        fh = open ( self.Filename_Answer, 'r' )
        self.State = ADC_Started
      except :
        pass

    elif self.State == ADC_Buffer_Switching :
      # wait till other file is reduced in length
      file_mode = os.stat ( self.Data_FileName [ self.BufNr ] )
      file_size = file_mode [ ST_SIZE ]
      #file_size = os.path.getsize ( self.Data_FileName [ self.BufNr ] )
      if file_size < self.Buf_Max :
        self.State = ADC_Started

    elif self.State == ADC_Started :
      file_mode = os.stat ( self.Data_FileName [ self.BufNr ] )
      file_size = file_mode [ ST_SIZE ]
      #file_size = os.path.getsize ( self.Data_FileName [ self.BufNr ] )
      new_bytes = file_size - self.BufP
      if new_bytes > 4 * self.ADC_Nchan :
        new_bytes = 4 * ( new_bytes / 4 )
        self.data = fromfile ( self.Data_File, dtype=int ,count=new_bytes )
        self.BufP = self.BufP + new_bytes
        self.data = self.data.reshape (
          size(self.data) / self.ADC_Nchan ,self.ADC_Nchan)
        #print 'SHAPE1',self.data.shape,self.ADC_Nchan
        self.data = transpose ( self.data )
        #print 'SHAPE2',self.data.shape

        new_bytes /= (4*self.ADC_Nchan)
        self.Navailable += new_bytes

        #self.Graph.AppendText ( str ( self.BufNr ) + ' ' +
        #                        str ( new_bytes ) +'\n')

        #print new_bytes, self.BufP, self.data.shape

      else :
        if self.BufP >= self.Buf_Max :
          self.Data_File.close ()
          self.BufNr = not ( self.BufNr )
          self.BufP = 0
          self.Data_File = open ( self.Data_FileName [ self.BufNr ], 'rb' )
          self.State = ADC_Buffer_Switching

  # ************************************************
  # CallBack function, used by PyLab_Works
  # ************************************************
  def Start_Stop ( self, Start = True ) :
    if Start == ( self.State == ADC_Started ) :
      return
    self.OnStart ( None )
    
  def OnStart ( self, event ) :
    if   self.State == ADC_Killed :
      self.Init_ADC ()
    elif self.State == ADC_Stopped :
      self.Start_ADC ()
    else :
      self.Stop_ADC ()

  def Init_ADC ( self ):
    # disable all controls
    self.Combo_ADC.Enable (False )
    self.T1.Enable ( False )
    self.T2.Enable ( False )
    self.Spin_NChan.Enable ( False )
    self.T3.Enable ( False )
    self.Fsamp.Enable ( False )
    self.ADC_FileB.Enable ( False )
    self.ADC_File.Enable ( False )

    # remove the communication files
    File_Delete ( self.Data_FileName [0] )
    File_Delete ( self.Data_FileName [1] )
    File_Delete ( self.Filename_Kill )

    # start the hardware
    result = subprocess.Popen ( os.path.join ( self.Path, 'midacadc.exe' ) )

    # initialize pointers
    self.BufNr = False
    self.Bufp = 0

    # start the ADC
    self.Start_ADC ()

  def Start_ADC ( self ):
    # get all settings
    #self.ADC_Nchan = 2
    self.ADC_Nchan = self.Spin_NChan.GetValue()

    #         ADC / NChan / sample-frequency / bufsize / file
    line  = str ( self.Combo_ADC.GetSelection () ) + '/'
    line += str ( self.ADC_Nchan ) + '/'
    line += self.Fsamp.GetValue() + '/'
    # BUF_max zou moeten zijn 0.5 seconden of zo: Nchan*4*fSamp
    line += str ( self.Buf_Max ) + '/'
    line += self.ADC_File.GetValue ()
    #print line
    fh = open ( self.Filename_Start, 'w' )
    fh.write ( line )
    fh.close ()


    # wait till datafile available
    filnam = self.Data_FileName [ self.BufNr ]
    while not ( File_Exists ( filnam ) ) :
      time.sleep(0.02)
    self.Data_File = open ( filnam, 'rb' )


    self.State = ADC_Started
    self.Button_Start.SetLabel ( 'Stop' )
    if self.Test :
      self.Timer.Start ( 50 )

  def Stop_ADC ( self ) :
    os.remove ( self.Filename_Start )
    self.State = ADC_Stopped
    self.Button_Start.SetLabel ( 'Start' )
    self.Timer.Stop ()

  def Get_New_Samples ( self ) :
    self.Fetch_Samples ()
    N = self.Navailable
    self.Navailable = 0
    return N
    
  def Kill ( self ) :
    if self.State != ADC_Killed :
      self.Timer.Stop ()
      if self.State != ADC_Stopped :
        self.Stop_ADC ()
      fh = open ( self.Filename_Kill, 'w' )
      fh.write ( 'kill')
      fh.close ()

  def OnClose ( self, event ) :
    self.Kill ()
    event.Skip()

  """
  # ********************************************************
  # Close isn't always called, so we use __del__
  # to kill the external processes
  # ********************************************************
  def __del__ ( self ) :
    print 'kill ADC'
    if self.State != ADC_Killed :
      self.Timer.Stop ()
      if self.State != ADC_Stopped :
        self.Stop_ADC ()
      fh = open ( self.Filename_Kill, 'w' )
      fh.write ( 'kill')
      fh.close ()
    # always necessary to propagate the destroy function
    #object.__del__ ()
  """
# ***********************************************************************

# ***********************************************************************
# A simple form to test the control
# ***********************************************************************
class Simple_Test_Form ( wx.MiniFrame ):
  def __init__ ( self, ini = None ):
    # restore position and size
    if ini :
      ini.Section = 'Test'
      pos  = ini.Read ( 'Pos'  , ( 50, 50 ) )
      size = ini.Read ( 'Size' , ( 500, 300 ) )

    wx.MiniFrame.__init__(
      self, None, -1, 'Test PyLab Works GUI Control',
      size  = size,
      pos   = pos,
      style = wx.DEFAULT_FRAME_STYLE )

    # Create the control to be tested
    AD_Converter ( self, None, ini = ini, Test = True )
# ***********************************************************************



# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  app = wx.PySimpleApp ()
  ini = inifile ( 'test_My_ADC_Control.cfg' )
  frame = Simple_Test_Form (ini = ini)
  frame.Show ( True )
  app.MainLoop ()
  ini.Close ()
# ***********************************************************************

#pd_Module ( __file__ )

Control = AD_Converter
import wx
import wx.aui


# ***********************************************************************
# ***********************************************************************
class Control_Panel ( wx.Panel ):
  def __init__ ( self, parent, Control ) :
    wx.Panel.__init__ ( self, parent )
    #Control = wx.TextCtrl ( self,-1,
    #                    'swat text\n meer regels', #wx.Point(0, 0), #wx.Size(150, 90),
    #                       style = wx.NO_BORDER | wx.TE_MULTILINE)

    # Create the control to be tested
    My_Control = Control ( self , None ) #, ini = ini, Test = True )

    #sizer = wx.BoxSizer ()
    #sizer.Add ( My_Control, 1, wx.EXPAND )
    #self.SetSizer ( sizer )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Settings_Panel ( wx.Panel ):
  def __init__ ( self, parent, Control ) :
    self.Control = Control
    wx.Panel.__init__ ( self, parent )
    w = 85
    h = 24
    GUI = """
    p1                         ,PanelHor  ,01
      p2                       ,wx.Panel
        self.B_Calculate       ,wx.Button     ,label = 'Calculate'      ,pos = (0,0)   ,size = (w,h)
        self.B_Save_Settings   ,wx.Button     ,label = 'Save_Settings'  ,pos = (0,30)  ,size = (w,h)
        self.B_Load_Settings   ,wx.Button     ,label = 'Load_Settings'  ,pos = (0,60)  ,size = (w,h)
        self.B_Kill            ,wx.Button     ,label = 'Kill'           ,pos = (0,90)  ,size = (w,h)
        self.B_ForGroundColor  ,wx.Button     ,label = 'ForGroundColor' ,pos = (0,120) ,size = (w,h)
      p3                       ,PanelVer  ,010
        p5                     ,PanelHor  ,010
          self.B_GetValue      ,wx.Button     ,label = 'Get'                           ,size=(40,h)
          Label_Top            ,wx.StaticText ,label = 'Value'          ,style=wx.ALIGN_CENTER
          self.B_SetValue      ,wx.Button     ,label = 'Set'                           ,size=(40,h)
        self.Value             ,wx.TextCtrl   ,style = wx.TE_MULTILINE
        p4                     ,wx.Panel
          self.B_GetSize       ,wx.Button     ,label = 'GetSize'        ,pos = (0,0)   ,size =(50,h)
          self.L_GetSize       ,wx.StaticText ,label = 'GetSize'        ,pos = (55,5)
          self.B_GetID         ,wx.Button     ,label = 'GetID'          ,pos = (0,25)  ,size =(50,h)
          self.L_GetID         ,wx.StaticText ,label = 'GetID'          ,pos = (55,30)
    """
    from gui_support import Create_wxGUI
    self.wxGUI = Create_wxGUI ( GUI )
    
    self.B_GetValue      .Bind ( wx.EVT_BUTTON, self._On_B_GetValue       )
    self.B_SetValue      .Bind ( wx.EVT_BUTTON, self._On_B_SetValue       )
    self.B_Calculate     .Bind ( wx.EVT_BUTTON, self._On_B_Calculate      )
    self.B_GetSize       .Bind ( wx.EVT_BUTTON, self._On_B_GetSize        )
    self.B_GetID         .Bind ( wx.EVT_BUTTON, self._On_B_GetId          )
    self.B_ForGroundColor.Bind ( wx.EVT_BUTTON, self._On_B_ForGroundColor )
    self.B_Save_Settings .Bind ( wx.EVT_BUTTON, self._On_B_Save_Settings  )
    self.B_Load_Settings .Bind ( wx.EVT_BUTTON, self._On_B_Load_Settings  )
    self.B_Kill          .Bind ( wx.EVT_BUTTON, self._On_B_Kill           )

  # ***************************************************
  def _On_B_GetValue ( self, event ):
    try :
      label = self.Control.GetValue ()
    except :
      label = 'No GetValue Available'
    self.Value.SetValue ( label )

  # ***************************************************
  def _On_B_SetValue ( self, event ):
    try :
      self.Control.SetValue ( self.Value.GetValue () )
    except :
      pass
    
  # ***************************************************
  def _On_B_Calculate ( self, event ):
    try :
      label = self.Control.Calculate ()
    except :
      pass

  # ***************************************************
  def _On_B_GetSize ( self, event ):
    try :
      label = self.Control.GetSize ()
    except :
      label = '-'
    self.L_GetSize.SetLabel ( label )

  # ***************************************************
  def _On_B_GetId ( self, event ):
    try :
      label = self.Control.GetId ()
    except :
      label = '-'
    self.L_GetID.SetLabel ( label )

  # ***************************************************
  def _On_B_ForGroundColor ( self, event ):
    from dialog_support import Color_Dialog
    color = Color_Dialog ( self, None )
    try :
      self.Control.SetForegroundColour ( color )
    except :
      pass

  # ***************************************************
  def _On_B_Save_Settings ( self, event ):
    try :
      self.Control.Save_Settings ()
    except :
      pass

  # ***************************************************
  def _On_B_Load_Settings ( self, event ):
    try :
      self.Control.Load_Settings ()
    except :
      pass

  # ***************************************************
  def _On_B_Kill ( self, event ):
    try :
      self.Control.Kill ()
    except :
      pass

# ***********************************************************************



# ***********************************************************************
# A simple form to test the control
# ***********************************************************************
class Simple_Test_Form ( wx.MiniFrame ):
  def __init__ ( self, ini = None ):
    # restore position and size
    pos = ( 50, 50 )
    size = ( 500, 500 )
    if ini :
      ini.Section = 'Test'
      pos  = ini.Read ( 'Pos'  , pos )
      size = ini.Read ( 'Size' , size )

    #import wx
    wx.MiniFrame.__init__(
      self, None, -1, 'Test PyLab Works GUI Control',
      size  = size,
      pos   = pos,
      style = wx.DEFAULT_FRAME_STYLE )

    # tell FrameManager to manage this frame
    self._mgr = wx.aui.AuiManager ()
    self._mgr.SetManagedWindow ( self )

    # Set AUI manager flags
    self._mgr.SetFlags ( self._mgr.GetFlags () ^ wx.aui.AUI_MGR_ALLOW_ACTIVE_PANE )
    self._mgr.GetArtProvider().SetMetric (
      wx.aui.AUI_DOCKART_GRADIENT_TYPE, wx.aui.AUI_GRADIENT_HORIZONTAL )
    self._mgr.GetArtProvider().SetMetric ( wx.aui.AUI_DOCKART_SASH_SIZE, 3 )
    self._mgr.GetArtProvider().SetMetric ( wx.aui.AUI_DOCKART_CAPTION_SIZE, 10 )

    # Update the complete frame
    #self._mgr.Update ()



    #Control = 1
    pane = Control_Panel ( self, Control )
    self._mgr.AddPane(pane,
                           wx.aui.AuiPaneInfo().
                           Name ( '_Control' ).
                           Caption ( 'Control' ).
                           CaptionVisible ( True ).
                           Left().
                           MinSize( ( 200, 40 ) ).
                           CloseButton ( False ).
                           MaximizeButton ( False ) )

    pane = Settings_Panel ( self, Control )
    self._mgr.AddPane(pane,
                           wx.aui.AuiPaneInfo().
                           Name ( '_Tester' ).
                           Caption ( 'Control Tester' ).
                           CaptionVisible ( True ).
                           Right().
                           MinSize( ( 200, 40 ) ).
                           CloseButton ( False ).
                           MaximizeButton ( False ) )

    self._mgr.Update()

    """
    # Create the control to be tested
    ADC = AD_Converter ( self, None, ini = ini, Test = True )
    """
# ***********************************************************************

frame = Simple_Test_Form ()
frame.Show ( True )

