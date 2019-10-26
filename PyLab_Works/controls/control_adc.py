import __init__
from base_control        import *

import subprocess
import time
from   stat import *

# !!! import wx before any support library !!!
# otherwise the IDE won't do auto-suggest
import wx

from dialog_support import *
from inifile_support import *
from win_inifile_support import *
from file_support import *
from numpy import fromfile, int32, size, transpose
from array_support   import Analyze_TIO_Array, class_MetaData


ADC_Killed   = 0
ADC_Stopped  = 1
ADC_Started  = 2
ADC_Buffer_Switching = 3

# ***********************************************************************
# ***********************************************************************
class t_C_AD_Converter ( My_Control_Class ) :

  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    # *************************************************************
    # if the ADC is used a s Brick in PyLab_Works,
    # something special needs to be done,
    # we connect the input value to a callback function
    # *************************************************************
    #if self.Brick :
    #  self.Brick.In [1] = self.Start_Stop

    # *************************************************************
    # *************************************************************
    #self.Path = path_split ( __file__ ) [0]
    self.Path = sys._getframe().f_code.co_filename
    self.Path = os.path.split ( self.Path ) [0]
    
    self.Filename_Start  = os.path.join ( self.Path, 'midadc_start.txt'  )
    self.Filename_Answer = os.path.join ( self.Path, 'midadc_answer.txt' )
    self.Filename_Kill   = os.path.join ( self.Path, 'midadc_kill.txt'   )
    self.Filename_Buf1   = os.path.join ( self.Path, 'midadc1.dat'       )
    self.Filename_Buf2   = os.path.join ( self.Path, 'midadc2.dat'       )
    self.Data_FileName   = [ self.Filename_Buf1, self.Filename_Buf2 ]
    self.FileNr = False
    self.FileP = 0
    self.Buf_Max = 10000
    self.Navailable = 0

    self.Memo = wx.TextCtrl ( self.Dock, -1,  style = wx.TE_MULTILINE|wx.TE_PROCESS_ENTER )

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

    filename = os.path.normpath ( Application.Dir + "../data/ipc_4.d1" )
    filename = os.path.join ( Application.Dir, '..', 'data', 'p50sz3.d1' )
    filename = os.path.join ( Application.Dir, '..', 'data', 'ipc_4.d1' )
    filename = os.path.normpath ( filename )
    self.ADC_File = wx.TextCtrl ( self.Panel, -1, filename,
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
    Sizer.Add ( self.Memo, 1, wx.EXPAND )
    Sizer.Add ( self.Panel, 0 )
    self.Dock.SetSizer ( Sizer )
    # *************************************************************

    self.Dock.Bind ( wx.EVT_CLOSE, self.OnClose )

    # the Timer must be bound to Dock
    self.Timer = wx.Timer ( self.Dock )
    # the third parameter is essential to allow other timers
    self.Dock.Bind ( wx.EVT_TIMER, self.OnTimer, self.Timer)



  def OnFileB ( self, event ) :
    try :
      filepath, filename = path_split ( self.ADC_File.GetValue() )
    except:
      filename = ''
      filepath = self.Path

    FileTypes = 'Midac format (*.d1)|*.d1'   +\
                '|All Files (*.*)|*.*'

    filename = AskFileForOpen ( filepath, filename, FileTypes )
    if filename:
      self.ADC_File.SetValue ( filename )

  def Read_Data ( self ) :
    #self.datafile = open ( self.Filename_Buf1,'rb')       # Readonly Binary
    pass

  def OnTimer ( self, event ) :
    event.Skip()
    v3print ( ' timer')
    self.Fetch_Samples ()
    
  def Fetch_Samples ( self ):
    #print 'FETCH',self.State,self.Filename_Answer
    if   self.State == ADC_Killed :
      # test if there's an answer file from the sample program
      try :
        fh = open ( self.Filename_Answer, 'r' )
        self.State = ADC_Started
      except :
        pass

    elif self.State == ADC_Buffer_Switching :
      # wait till other file is reduced in length
      file_mode = os.stat ( self.Data_FileName [ self.FileNr ] )
      file_size = file_mode [ ST_SIZE ]
      #file_size = os.path.getsize ( self.Data_FileName [ self.FileNr ] )
      if file_size < self.Buf_Max :
        self.State = ADC_Started

    elif self.State == ADC_Started :
      file_mode = os.stat ( self.Data_FileName [ self.FileNr ] )
      file_size = file_mode [ ST_SIZE ]
      #file_size = os.path.getsize ( self.Data_FileName [ self.FileNr ] )
      #new_bytes = file_size - self.FileP
      NBytes   = file_size - self.FileP
      NSamples = NBytes // 4
      ##NSamples = file_size // 4 - self.FileP
      #N = 4 * self.ADC_NChan
      #if new_bytes >= N :
      if NSamples > self.ADC_NChan :
        NSamples = self.ADC_NChan * ( NSamples // self.ADC_NChan )
        self.data = fromfile ( self.Data_File, dtype=int32, count = NSamples )

        # Update file pointer, on the base of really fetched samples
        self.FileP += 4 * self.data.size
        self.Navailable += ( self.data.size // self.ADC_NChan )

        self.data = self.data.reshape (
          size(self.data) / self.ADC_NChan ,self.ADC_NChan)
        #v3print ( 'SHAPE1', self.data.shape, self.ADC_NChan )
        self.data = transpose ( self.data )

        if self.Test :
          self.Memo.AppendText (
            ' FileNr = ' + str ( self.FileNr ) + '   ' +
            ' Sample = ' + str ( NSamples ) + '   ' +
            ' FilePoint = ' + str ( self.FileP ) + '\n')


      else :
        if self.FileP >= self.Buf_Max :
          self.Data_File.close ()
          self.FileNr = not ( self.FileNr )
          self.FileP = 0
          self.Data_File = open ( self.Data_FileName [ self.FileNr ], 'rb' )
          #self.Data_File = open ( self.Data_FileName [ self.FileNr ], 'r' )
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
    self.FileNr = False
    self.FileP  = 0

    # start the ADC
    self.Start_ADC_FirstTime ()
    self.Start_ADC ()

  def Start_ADC_FirstTime ( self ):
    self.ADC_NChan = self.Spin_NChan.GetValue()

    #         ADC / NChan / sample-frequency / bufsize / file
    line  = str ( self.Combo_ADC.GetSelection () ) + '/'
    line += str ( self.ADC_NChan ) + '/'
    line += self.Fsamp.GetValue() + '/'

    # BUF_max zou moeten zijn 0.5 seconden of zo: Nchan*4*fSamp
    line += str ( self.Buf_Max ) + '/'
    line += self.ADC_File.GetValue ()
    self.Start_Code = line
    
    #if self.Test :
    self.Memo.AppendText ( 'OPEN: ' + line )

    # Get MetaData
    filename ,ext = os.path.splitext ( self.ADC_File.GetValue () )
    self.ADC_MetaFile = filename + '.c' + ext [2:]
    self.Memo.AppendText  ( '\nMetaDataFile = ' + self.ADC_MetaFile )
    
    self.MetaData = []
    meta_ini = win_inifile ( self.ADC_MetaFile, Force_Identifiers = True )
    meta_ini.Section = 'ad-converter'
    First_Channel = meta_ini.Read_Integer ( 'AD-channel_first', 1 )
    Last_Channel  = meta_ini.Read_Integer ( 'AD-channel_last' , 4 )
    self.Memo.AppendText ( '\nChannels = ' + str (First_Channel) + '/' + str(Last_Channel) )

    #ADC1 = meta_ini.Read_Integer ( 'AD_ondergrens_(ADC)' , -10 )
    #ADC2 = meta_ini.Read_Integer ( 'AD_bovengrens_(ADC)' , +10 )
    #V1   = meta_ini.Read_Integer ( 'AD_ondergrens_(V)'   , -110 )
    #V2   = meta_ini.Read_Integer ( 'AD_bovengrens_(V)'   , +110 )
    #print 'PPPPPPPPPTTTT', ADC1,ADC2, V1,V2
    
    self.gain   = []
    self.offset = []
    ##self.ADC_NChan = Last_Channel + 1 - First_Channel
    for chan in range ( First_Channel, Last_Channel+1 ) :
      Signal_Attr = class_MetaData ()
      self.MetaData.append ( Signal_Attr )

      meta_ini.Section = 'Signal-' + str ( chan )
      Chan_Name  = meta_ini.Read ( 'name' , '???' )
      Chan_Units = meta_ini.Read ( 'measurement_units' , '' )
      line = Chan_Name + ' [' + Chan_Units + ']'
      self.Memo.AppendText ( '\n  chan-' + str ( chan )  + ' = ' + line )
      Signal_Attr.SignalName = line

      x1 = ADV1 = meta_ini.Read_Integer ( 'lower_ADV-value' , -10 )
      x2 = ADV2 = meta_ini.Read_Integer ( 'upper_ADV-value' , 10 )
      y1 = Cal1 = meta_ini.Read_Integer ( 'lower_cal-value' , -110 )
      y2 = Cal2 = meta_ini.Read_Integer ( 'upper_cal-value' , 110 )
      #print 'PPPPPPPPPTTTT', chan, ADV1,ADV2, Cal1,Cal2

      y2y1 = 1.0 * ( y2 - y1 ) / ( x2 - x1 )
      self.gain.append  ( 5 * y2y1 / 2048 )
      self.offset.append ( y1 - y2y1 * ( 5 + x1 ) )

      Signal_Attr.Calibrate =  self.gain [-1], self.offset [-1]

      #Signal_Attr.DisplayRange = ( 0, 200 )

    #v3print ( 'GAIN', self.gain )
    #v3print ( 'OFFS', self.offset )
    # Set Change flag, should be cleared by the ADC-Brick
    self.MetaData_Changed = True
    self.Memo.AppendText ( '\n' )
    """
x1 = -10   # AD
x2 = 212   # AD
y1 = 20    # mmHg
y2 = 120   # mmHg
for ADC in 50000, 90000 :
  Volt = ( ADC - 2048 ) * 5.0 / 2048
  World = y1 + 1.0 * ( y2 - y1 ) * ( Volt - x1 ) / ( x2 - x1 )
  print 'A2V', Volt, World


[AD-converter]
AD-channel first=1
AD-channel last=13
Sample Frequency (Hz)=100.00
Prefered Sample Frequency (Hz)=100.00
AD ondergrens (ADC)=0
AD bovengrens (ADC)=4095
AD ondergrens (V)=-5000000
AD bovengrens (V)=5000000

[Signal-1]
techname=AD1
name=Druk
measurement units=mmHg
lower ADV-value=63.7
upper ADV-value=212
lower cal-value=20
upper cal-value=120
AC=0
    """
    
  def Start_ADC ( self ):
    fh = open ( self.Filename_Start, 'w' )
    fh.write ( self.Start_Code )
    fh.close ()

    # wait till datafile available
    filnam = self.Data_FileName [ self.FileNr ]
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

  def Get_New_Sample_Sets ( self ) :
    self.Fetch_Samples ()
    N = self.Navailable
    #v3print ( 'New Samples Sets', N )
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
    event.Skip()
    self.Kill ()

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
    t_C_AD_Converter ( self, None, Ini = ini, Test = True )
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
pd_Module ( __file__ )

