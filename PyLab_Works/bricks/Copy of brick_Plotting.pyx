# ***********************************************************************
# Standard libraries
# ***********************************************************************
from brick import *
from PyLab_Works_Globals import _
from PyLab_Works_Globals import *
#print 'PG2',dir (PyLab_Works_Globals)
#print 'brick1',dir()
#from language_support import  * #_, Set_Language
#print 'brick2',dir()
# ***********************************************************************
# Application specific libraries
# ***********************************************************************
from math           import pi
from dialog_support import *
from file_support   import *
from numpy          import *
from copy           import copy
# ***********************************************************************
# If color is ignored, default BLACK is selected
# ***********************************************************************
Library_Color = wx.Color ( 250, 150, 90 )

# ***********************************************************************
# Library_Icon,

#   - can be an index in the image-list (not recommended)
#   - or the filename of an image in this directory
# ***********************************************************************
Library_Icon = 'camera_edit.png'


Description = """This is the description of the complete library.
Line 2 of ... """

# ***********************************************************************
# ***********************************************************************
class t_HTML ( tLWB_Brick ):

  Description = """Shows an html page, that can be used for
- course material
- instructions
- to store answers of students"""

  def After_Init (self):
    # we want this image-window to be centered
    self.Center = False

    # we want to let this window float,
    # so it can be extracted from the application
    self.Float = True
    
    # Create the shape and set the caption
    self.After_Init_Default ( 'HTML' )

    # Create the GUI controls
    C = self.Create_New_Control ()
    C [ 'Type' ]          = CT_HTML

# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class t_MatPlot_2D( tLWB_Brick ):

  #Description = """Shows the image at input[1]"""
  I = 5

  def After_Init (self):
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    for i in range ( 1, self.I + 1 ) :
      self.Inputs [i] = ['Signal ' +  str(i), TIO_ARRAY, (i==1) ]

    # we want this image-window to be centered
    self.Center = True
    # Create the shape and set the caption
    self.After_Init_Default ( 'MatPlot-2D' )

    # Create the GUI controls
    C = self.Create_New_Control ()
    C [ 'Type' ]          = CT_MATPLOT

  def Generate_Output_Signals ( self ) :
    C = self.Control_Pane.GUI_Controls [0]
    C[ 'Control' ].Calculate ()
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class t_PyPlot_XT( tLWB_Brick ):

  #Description = """Shows the image at input[1]"""
  I = 5

  def After_Init (self):
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    for i in range ( 1, self.I + 1 ) :
      self.Inputs [i] = ['Signal ' +  str(i), TIO_ARRAY, (i==1) ]

    # we want this image-window to be centered
    self.Center = True
    # Create the shape and set the caption
    self.After_Init_Default ( 'XT-PyPlot' )

    # Create the GUI controls
    C = self.Create_New_Control ()
    C [ 'Type' ]          = CT_PYPLOT
    C [ 'Input Channel' ] = 1
    C [ 'Range' ]         = self.N_Inputs - 1

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_PyPlot_Signal ( tLWB_Brick ):

  #Description = """Shows the image at input[1]"""

  def After_Init (self):
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = \
      ['Signal',  TIO_ARRAY, True,'']

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = \
      ['Signal + Parameters', TIO_ARRAY ]

    # Create the shape and set the caption
    self.After_Init_Default ( 'PyPlot Signal' )

    # Create the GUI controls
    C = self.Create_New_Control ()
    C [ 'Type' ]    = CT_EDIT
    C [ 'Caption' ] = 'Name'
    C [ 'Value' ]   = self.Params[1] = ''

    C = self.Create_New_Control ()
    C [ 'Type' ]    = CT_COLOR_PICKER
    C [ 'Caption' ] = 'Line Color'
    C [ 'Value' ]   = self.Params[2] = wx.Color ( 100, 200, 100 )

    C = self.Create_New_Control ()
    C [ 'Type' ]    = CT_SPIN_BUTTON
    C [ 'Caption' ] = 'Line Width'
    C [ 'Value' ]   = self.Params[3] = 1
    C [ 'Range' ]   = [1,5]

  def Generate_Output_Signals ( self ) :
    self.Output_Value [1] = [ self.Input_Value [1], self.Params ]
    self.Output_Changed [1] = True
    pass
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class t_Generator ( tLWB_Brick ):

  Description = """Generator as used in electronics workplaces.
Generates a signal 100 samples ???
All basic signals have a separate output.
The frequency, duty-cycle, amplitude and offset can be either
be set by a control or by an input signal (for modulation),
and apply to all output signals."""

  def After_Init (self):
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = \
      ['Frequency [Hz]', TIO_NUMBER, False,
       'Can be used for frequency modulation (FM)']
    self.Inputs [2] = \
      ['Amplitude [V]', TIO_NUMBER, False,
       'Can be used for amplitude modulation (AM)']
    self.Inputs [3] = \
      ['Offset [V]', TIO_NUMBER, False ]

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = \
      ['Sine Wave', TIO_ARRAY ]
    self.Outputs [2] = \
      ['Square Wave', TIO_ARRAY ]

    # Create the shape and set the caption
    self.After_Init_Default ( 'Generator' )

    # Create the GUI controls
    C = self.Create_New_Control ( 20 )
    C [ 'Type' ]          = CT_SLIDER
    C [ 'Range' ]         = [10,100]
    C [ 'Caption' ]       = self.Inputs [1][0]
    C [ 'Input Channel' ] = 1

    C = self.Create_New_Control ( 1 )
    C [ 'Type' ]          = CT_RADIO_BUTTON
    C [ 'NCol']           = 1
    C [ 'Range' ]         = [ '*0.1 : 1..10', '*1 : 10..100', '*10 : 100..1000' ]
    C [ 'Caption' ]       = 'Frequency Factor'

    C = self.Create_New_Control ( 30 )
    C [ 'Type' ]          = CT_SLIDER
    C [ 'Range' ]         = [0,100]
    C [ 'Caption' ]       = self.Inputs [2][0]
    C [ 'Input Channel' ] = 2

    C = self.Create_New_Control ( 0 )
    C [ 'Type' ]          = CT_SLIDER
    C [ 'Range' ]         = [-10,10]
    C [ 'Caption' ]       = self.Inputs [3][0]
    C [ 'Input Channel' ] = 3

    # initial values
    self.start = 0
    self.Frequency_Factor = [ 0.1, 1.0, 10.0 ]

    self.Timer = wx.Timer ( self.my_Container )
    # YOU MUST BIND IN THIS WAY,
    # to allow the already present timer to work !!!
    self.my_Container.Bind ( wx.EVT_TIMER, self.OnTimer, self.Timer )
    self.Timer.Start ( 200 )
    self.Triggered = False
    # By making a change to PARAMS[0],
    # a change in parameter settings is detected,
    # so Generate_Output_Signals will be called !!
    self.Params [0] = 0
    
  # *********************************************************************
  # *********************************************************************
  def OnTimer ( self, event ) :
    if ( PG.State == PG.SS_Run ) and not ( self.Triggered ) :
      self.Create_New_Output_Signals()
      self.Triggered = True
      
      self.Params [0] += 1

  # *********************************************************************
  # *********************************************************************
  def Create_New_Output_Signals ( self ) :
      N = 100
      if self.Output_Value[1] == None :
        self.Output_Value[1] = zeros ( N )
        self.Output_Value[2] = zeros ( N )
      fSamp = 1000
      A = 0.1 * self.Params [3]
      FF = self.Frequency_Factor [ self.Params [2] ]
      F = 2 * pi * FF * self.Params [1] / fSamp
      O = self.Params [4]

      for i in arange ( N ) :
        sinus = A * sin ( ( self.start + i ) * F )
        self.Output_Value[1][i] = O + sinus
        if sinus >= 0 :
          self.Output_Value [2][i] = O + A
        else :
          self.Output_Value [2][i] = O - A
      self.start = self.start + N

  # *********************************************************************
  # Procedure only called when inputs and/or parameters have changed
  # *********************************************************************
  def Generate_Output_Signals ( self ) :
    if self.Triggered :
      for i in range(1,3):
        self.Output_Changed [i] = True
      self.Triggered = False

# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class t_ADC ( tLWB_Brick ):

  Description = """AD converter,
supports several AD converters (works only under Windows)."""

  def After_Init (self):
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = \
      ['Start/Stop', TIO_CALLBACK, False,
       'Can be used to start/stop the ADC immediately']

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = \
      ['Signals', TIO_ARRAY ]
    self.Outputs [2] = \
      ['Signal Names', TIO_ARRAY ]

    # Create the shape and set the caption
    self.After_Init_Default ( 'AD Converter' )

    # Create the GUI controls
    C = self.Create_New_Control ( )
    C [ 'Type' ]    = CT_ADC
    C [ 'Value' ]   = self.Params[1] = 0
    

  # *********************************************************************
  # Procedure only called when inputs and/or parameters have changed
  # *********************************************************************
  def Generate_Output_Signals ( self ) :
    ##from time import time
    ##try :
    ##  print 'Generate ADC', 1000* (time() - self.aap)
    ##except : pass
    ##self.aap = time()

    C = self.Control_Pane.GUI_Controls [0]
    N = C ['Control'].Get_New_Samples ()
    if N > 0 :
      self.Output_Value [1] = C[ 'Control' ].data
      self.Output_Changed [1] = True
      #print 'ADC data', N

    # we need to ensure that this procedure is called every time
    self.Params [1] += 1
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_BP_Analysis ( tLWB_Brick ):

  Description = """Rotates an Image counter clockwise.
The rotation angle (in degrees) and the interpolation are either taken from
the internal GUI controls, or from the external signals,
whichever has been changed last."""

  def After_Init (self):
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = \
      ['Raw Bloodpressure', TIO_ARRAY, True,
       'Accepts a single bloodpressure signal\n'+
       'or a multi channel Signal.']

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = \
      ['Analyzed Signals', TIO_ARRAY,
       'PDias, MAP, PSys, HR, RR-interval, Onset_Dias']

    # Create the shape and set the caption
    self.After_Init_Default ( 'BP Analysis' )

    # Create the GUI controls
    C = self.Create_New_Control ()
    C [ 'Type' ]    = CT_SPIN_BUTTON
    C [ 'Caption' ] = 'Input Selector'
    C [ 'Value' ]   = self.Params[1] = 1
    C [ 'Range' ]   = [1,5]

    C = self.Create_New_Control ( 30 )
    C [ 'Type' ]          = CT_SLIDER
    C [ 'Range' ]         = [0,360]
    C [ 'Caption' ]       = 'Rotation [degrees]'

    self.buffer = zeros (100)
    self.p = 0

    # initialize the BP analysis function
    from medilab_pw import BP_analysis
    fsamp = 100
    self.BP = BP_analysis ( fsamp )

  # *********************************************************************
  # Procedure only called when inputs and/or parameters have changed
  # *********************************************************************
  def Generate_Output_Signals ( self ) :
    # get index of the selected signal
    S = self.Params [1] - 1
    
    # get the length of one of the signals
    N = self.Input_Value[1].shape[1]

    # do the analysis
    self.Output_Value[1] = \
      self.BP.execute ( self.Input_Value [1][S] )

    # set we've new outputs
    self.Output_Changed[1] = True
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_Scope_Display( tLWB_Brick ):

  I = 6

  def After_Init (self):
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    for i in range ( 1, self.I + 1 ) :
      self.Inputs [i] = ['Signals ' +  str(i), TIO_ARRAY, (i==1),
        _(0, 'Signals to be displayed on the Scope Display' )]

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = [ _(0,'Start / Stop'), TIO_CALLBACK,
                         _(0,'Can be used to control an AD-Converter.') ]

    # we want this image-window to be centered
    self.Center = True
    # Create the shape and set the caption
    self.After_Init_Default ( _(0,'Oscilloscope') )

    # Create the GUI controls
    C = self.Create_New_Control ()
    C [ 'Type' ]          = CT_SCOPEPLOT

  def Generate_Output_Signals ( self ) :
    #print 'Generate Scope', self.Input_Changed [1]
    if self.Input_Changed [1] or \
       self.Input_Changed [2] or \
       self.Input_Changed [3] or \
       self.Input_Changed [4] or \
       self.Input_Changed [5] :

      # we need to concatenate the indivual arrays, to one array
      Signals = self.Input_Value [1]
      if self.Input_Value [2] != None :
        Signals = r_ [ Signals, self.Input_Value [2] ]
      if self.Input_Value [3] != None:
        Signals = r_ [ Signals, self.Input_Value [3] ]
      if self.Input_Value [4] != None:
        Signals = r_ [ Signals, self.Input_Value [4] ]
      if self.Input_Value [5] != None:
        Signals = r_ [ Signals, self.Input_Value [5] ]
        
      # now send the array to the control
      C = self.Control_Pane.GUI_Controls [0]
      C[ 'Control' ].Calculate ( Signals )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_Scope_Hist_Display( tLWB_Brick ):

  I = 5
  
  def After_Init (self):
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    for i in range ( 1, self.I + 1 ) :
      self.Inputs [i] = [ _(0,'Signals ') +  str(i), TIO_ARRAY, (i==1),
        _(0, 'Signals to be displayed on the Scope Display' )]

    # we want this image-window to be centered
    self.Center = True
    # Create the shape and set the caption
    self.After_Init_Default ( _(0,'Oscilloscope\nHistory') )

    # Create the GUI controls
    C = self.Create_New_Control ()
    C [ 'Type' ]          = CT_SCOPE_HIST

  def Generate_Output_Signals ( self ) :
    for i in range ( 1, self.I + 1 ) :
      if self.Input_Changed [i] :
        break;

      C = self.Control_Pane.GUI_Controls [0]
      calc = []
      for signal in self.Input_Value [1:] :
        if signal != None :
          calc.append ( signal )

      #Type_Enumerate ( calc  )
      C[ 'Control' ].Calculate ( calc )

    else :
      pass
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_Code_Editor ( tLWB_Brick ):

  Description = _(0, """Scintilla Code Editor.
Can be used to test small pieces of Python code,
or to make something like a graphical calculator.
This Brick contains a number of input and output nodes,
so it can communicate with other Bricks,
through the variables IN[] and OUT[]""" )
  I = 3
  O = 5
  
  def After_Init (self):
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    for i in range ( 1, self.I+1 ) :
      self.Inputs [i] = ['IN['+ str(i)+']', TIO_NUMBER ]
    self.Inputs [ self.I + 1] = ['All IN', TIO_LIST ]

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    for i in range ( 1, self.O+1 ) :
      self.Outputs [i] = ['OUT['+str(i)+']', TIO_ARRAY ]

    # Create the shape and set the caption
    self.After_Init_Default ( 'Code Editor' )

    # Create the GUI controls
    C = self.Create_New_Control ( '' )
    C [ 'Type' ]          = CT_EDITOR

    self.start = 0

  # *********************************************************************
  # Procedure only called when inputs and/or parameters have changed
  # *********************************************************************
  def Generate_Output_Signals ( self ) :
    #print 'Generate Code Editor'
    Code = self.Params[1]
    # only \n is allowed !!  (see "compile")
    Code = Code.replace('\r\n','\n')
    # remove line continuation, not accepted by exec-statement
    Code = Code.replace('\\\n','')
    # and last line must end with \n   (see "compile")
    Code = Code + '\n'

    for i in range ( 1, self.I+1 ) :
      Code = Code.replace('IN'+str(i),'self.Input_Value['+str(i)+']')

    for i in range ( 1, self.O+1 ) :
      Code = Code.replace('OUT'+str(i),'self.Output_Value['+str(i)+']')

    # if list-pin is connected, use that to control all inputs
    if self.Input_Value [ self.I + 1 ] != None :
      temp = copy ( self.Input_Value [ self.I + 1 ] )
      self.Input_Value = copy ( temp )
      self.Input_Value.insert( 0, None )
      self.Input_Value.append ( temp )

    try :
      exec ( Code )
      self.Output_Changed[1] = True
    except :
      print '******** Code Editor, ERROR: *********'
      print Code
    self.Output_Changed [1] = True

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_Signal_Workbench ( tLWB_Brick ):

  Description = _(0, """Signal WorkBench.
bla bla ... """ )
  I = 3
  O = 5

  def After_Init (self):
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    for i in range ( 1, self.I+1 ) :
      self.Inputs [i] = ['IN['+ str(i)+']', TIO_NUMBER ]
    self.Inputs [ self.I + 1] = ['All IN', TIO_LIST ]

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    for i in range ( 1, self.O+1 ) :
      self.Outputs [i] = ['OUT['+str(i)+']', TIO_ARRAY ]

    # we want this image-window to be centered
    self.Center = True
    # Create the shape and set the caption
    self.After_Init_Default ( 'Signal WorkBench' )

    # Create the GUI controls
    C = self.Create_New_Control ( '' )
    C [ 'Type' ]          = CT_SIGNAL_WORKBENCH

    self.start = 0

  # *********************************************************************
  # Procedure only called when inputs and/or parameters have changed
  # *********************************************************************
  def Generate_Output_Signals ( self ) :
    #print 'Generate Code Editor'
    Code = self.Params[1]
    # only \n is allowed !!  (see "compile")
    Code = Code.replace('\r\n','\n')
    # remove line continuation, not accepted by exec-statement
    Code = Code.replace('\\\n','')
    # and last line must end with \n   (see "compile")
    Code = Code + '\n'

    for i in range ( 1, self.I+1 ) :
      Code = Code.replace('IN'+str(i),'self.Input_Value['+str(i)+']')

    for i in range ( 1, self.O+1 ) :
      Code = Code.replace('OUT'+str(i),'self.Output_Value['+str(i)+']')

    # if list-pin is connected, use that to control all inputs
    if self.Input_Value [ self.I + 1 ] != None :
      temp = copy ( self.Input_Value [ self.I + 1 ] )
      self.Input_Value = copy ( temp )
      self.Input_Value.insert( 0, None )
      self.Input_Value.append ( temp )

    try :
      exec ( Code )
      self.Output_Changed[1] = True
    except :
      print '******** Code Editor, ERROR: *********'
      print Code
    self.Output_Changed [1] = True

# ***********************************************************************




# ***********************************************************************
# Can take over stdout and/or stderr
# following commands work:
#   select / select all / copy
# ***********************************************************************
class t_STD_Viewer ( tLWB_Brick ):

  Description = """Can catch stdout and/or stderr messages,
settings can be toggled"""

  def After_Init (self):
    # Create the shape and set the caption
    self.After_Init_Default ( 'STD Viewer' )

    # Create the GUI controls
    C = self.Create_New_Control ( '' )
    C [ 'Type' ]          = CT_STD_VIEWER
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_Code_Slider ( tLWB_Brick ):

  Description = """Sliders for Code Generator."""
  N = 3
  
  def After_Init (self):
    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    for i in range ( 1, self.N+1 ) :
      self.Outputs [i] = ['Slider Value '+ str(i), TIO_NUMBER ]
    self.Outputs [ self.N + 1] = ['All Sliders', TIO_LIST]

    # Create the shape and set the caption
    self.After_Init_Default ( 'Code Sliders' )

    # Create the GUI controls
    for i in range ( 1, self.N+1 ) :
      C = self.Create_New_Control ( 0 )
      C [ 'Type' ]          = CT_SLIDER
      C [ 'Range' ]         = [0,100]
      C [ 'Caption' ]       = 'Value ' + str ( i )

  # *********************************************************************
  # Procedure only called when inputs and/or parameters have changed
  # *********************************************************************
  def Generate_Output_Signals ( self ) :
    self.Output_Value [ self.N+1] = []
    for i in range ( 1, self.N+1 ) :
      self.Output_Value [i] = self.Params [i]
      self.Output_Value [ self.N+1].append ( self.Params [i] )
      self.Output_Changed [i] = True
    self.Output_Changed [ self.N+1 ] = True

# ***********************************************************************

#CS_SN0 = "x = arange ( 0.0, 3.0, 0.01 )\ny = 15*cos  ( IN1 * pi * x )\ny2 = 10*sin ( IN2 * pi * x )\nOUT1 = x,y,y2,\\\n('cosine', 'sine')\n"
#CS_SN1 = [(192, 192, 192), (0, 0, 0), True, True, True, False, False]


# ***********************************************************************
# ***********************************************************************
class t_Read_Sound ( tLWB_Brick ):

  Description = """Reads an image from a file.
Images of the following types are accepted:
ANI, BMP, CUR, GIF, ICO, IFF, JPG, PCX, PNG, PNM, TIF, XPM """

  def After_Init (self):
    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = \
      [ _(0, 'FileName'), TIO_ARRAY,
        _(0, 'Image read from the file.' ) ]
    self.Outputs [2] = \
      [ _(0, 'Sound'), TIO_ARRAY,
        _(0, 'Image read from the file.' ) ]

    # Create the shape and set the caption
    self.After_Init_Default ( _(0, 'Load SoundFile') )

    # Create the GUI controls
    C = self.Create_New_Control ('')
    C [ 'Type' ]    = CT_FILEOPEN
    C [ 'Range' ]   = '*.wav'
    C [ 'Caption' ] = 'Read Sound File'

  # **********************************************************************
  # this procedure is only called when inputs (or parameters) have changed
  # **********************************************************************
  def Generate_Output_Signals ( self ) :

    if not ( File_Exists ( self.Params [1] ) ) :
      return

    self.Output_Value[1]    = self.Params[1]

    # read the sound data into a stream
    import wave
    wav  = wave.open ( self.Params[1], 'r' )
    amount = 14*256*35
    data = []
    for frame in wav.readframes ( amount ) :
      data.append ( ord ( frame ) * 5.0 / 256.0 )
    wav.close ()
    self.Output_Value [2] = array ( data )

    self.Output_Changed [1] = True
    self.Output_Changed [2] = True
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_Input_Selector ( tLWB_Brick ):

  Description = _(0, """Signal WorkBench.
bla bla ... """ )
  I = 5

  def After_Init (self):
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    for i in range ( 1, self.I+1 ) :
      self.Inputs [i] = ['IN['+ str(i)+']', TIO_ARRAY, i==1 ]

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = \
      [ _(0, 'FileName'), TIO_ARRAY,
        _(0, 'Image read from the file.' ) ]

    # Create the shape and set the caption
    self.After_Init_Default ( _(0, 'Input Selector') )

    # Create the GUI controls
    C = self.Create_New_Control ()
    C [ 'Type' ]    = CT_SPIN_BUTTON
    C [ 'Caption' ] = 'Input'
    C [ 'Value' ]   = self.Params[1] = 1
    C [ 'Range' ]   = [1,self.I]

  # **********************************************************************
  # this procedure is only called when inputs (or parameters) have changed
  # **********************************************************************
  def Generate_Output_Signals ( self ) :
    self.Output_Value   [1] = self.Input_Value [ self.Params [1] ]
    self.Output_Changed [1] = True
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
from brick_Media import t_Play_Sound
class t__Play_Sound ( t_Play_Sound ) :
  pass
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_BTC ( tLWB_Brick ):

  Description = _(0, """Scintilla Code Editor.
Can be used to test small pieces of Python code,
or to make something like a graphical calculator.
This Brick contains a number of input and output nodes,
so it can communicate with other Bricks,
through the variables IN[] and OUT[]""" )

  def After_Init (self):
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = ['Input Stream', TIO_ARRAY, True ]

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = ['Output_Stream', TIO_ARRAY ]

    # Create the shape and set the caption
    self.After_Init_Default ( 'BTC Sound' )

    # Create the GUI controls
    C = self.Create_New_Control ()
    C [ 'Type' ]    = CT_EDIT
    C [ 'Caption' ] = 'Btc         '
    C [ 'Value' ]   = self.Params[1] = '16'

    C = self.Create_New_Control ()
    C [ 'Type' ]    = CT_EDIT
    C [ 'Caption' ] = 'R [kOhm]'
    C [ 'Value' ]   = self.Params[2] = '10'

    C = self.Create_New_Control ()
    C [ 'Type' ]    = CT_EDIT
    C [ 'Caption' ] = 'C [nF]      '
    C [ 'Value' ]   = self.Params[3] = '330'

    C = self.Create_New_Control ()
    C [ 'Type' ]    = CT_EDIT
    C [ 'Caption' ] = 'Freq. [Hz]'
    C [ 'Value' ]   = self.Params[4] = '11050'

    C = self.Create_New_Control ()
    C [ 'Type' ]          = CT_BUTTONS
    C [ 'Caption' ]       = [ 'Knopje' ]

  # *********************************************************************
  # Procedure only called when inputs and/or parameters have changed
  # *********************************************************************
  def Generate_Output_Signals ( self ) :

    data = self.Input_Value [1]
    Vmax = 5
    Vmin = 0
    Vold = 2.5
    Btc = 36 #0.1393 * 0.632

    bert_bitlist = []
    bert_list = s_list ()
    for frame in data:
      #  frame = frame / 256.0 * 5.0
      hi = Vold + (Vmax - Vold) / Btc
      lo = Vold + (Vmin - Vold) / Btc
      if abs(frame - hi) < abs(frame - lo):
        # Hi bit
        bert_bitlist.append(1)
        Vold = hi
      else:
        bert_bitlist.append(0)
        Vold = lo
      bert_list.append(Vold)

    bert_list.Frequency = 11050
    self.Output_Value [1]   = bert_list


    self.Output_Changed [1] = True

# ***********************************************************************




# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':
  pass