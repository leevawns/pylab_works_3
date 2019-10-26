# ***********************************************************************
# Standard libraries
# ***********************************************************************
from brick import *
from PyLab_Works_Globals import _
from PyLab_Works_Globals import *
#from base_control        import *
from import_controls import *
#print 'PLOTDIR',dir()
from array_support   import Analyze_TIO_Array, class_MetaData

# ***********************************************************************
# If color is ignored, default BLACK is selected
# ***********************************************************************
Library_Color = wx.Colour ( 250, 150, 90 )

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

  Description = _(7,"""Shows an html page, that can be used for
- course material
- instructions
- to store answers of students""")

  def After_Init (self):
    self.Caption = 'HTML'
    # we want this image-window to be centered
    self.Center = False

    # we want to let this window float,
    # so it can be extracted from the application
    self.Float = True
    
    # Create the GUI controls
    CD = self.Create_Control ( t_C_Html )

# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class t_MatPlot_2D( tLWB_Brick ):

  Description = _(0, """Shows the image at input[1]""")
  I = 5

  def After_Init (self):
    self.Caption = 'MatPlot-2D'
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    for i in range ( 1, self.I + 1 ) :
      self.Inputs [i] = ['Signal ' +  str(i), TIO_ARRAY, (i==1) ]

    # we want this image-window to be centered
    self.Center = True

    # Create the GUI controls
    CD = self.Create_Control ( t_C_MatPlot )

  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    C = self.GUI_Controls [0]
    C.Calculate ()
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class t_PyPlot_XT( tLWB_Brick ):

  #Description = """Shows the image at input[1]"""
  I = 5

  def After_Init (self):
    self.Caption = 'XT-PyPlot'

    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    for i in range ( 1, self.I + 1 ) :
      self.Inputs [i] = ['Signal ' +  str(i), TIO_ARRAY, (i==1) ]

    # we want this image-window to be centered
    self.Center = True

    # Create the GUI controls
    CD = self.Create_Control ( t_C_PyPlot )
    CD.Range         = self.I
    CD.Input_Channel = 1

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_Scene_2D( tLWB_Brick ):

  #Description = """Shows the image at input[1]"""

  def After_Init (self):
    self.Caption = '2D Scene'
    #self.Diagnostic_Mode = True

    # This device wants to be executed every loop
    self.Continuous = True

    # Define the input pins
    self.Inputs [1] = [ _(4, 'Signal 1') , TIO_STRING, REQUIRED ]

    # we want this image-window to be centered
    self.Center = True

    # Create the GUI controls
    CD = self.Create_Control ( t_C_2D_Scene )
    CD.Input_Channel = 1

  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    #"""
    self.Scene = self.GUI_Controls [0]
    #self.Scene.Start_Script ( self.Input_Value [1] )
    self.Scene.Start_Script ( self.In [1] )
    if self.Scene.VPC_Code :
      self.In [2] [ 'VPC_Code ' ] = self.Scene.VPC_Code
    """
    #XXX684XXX
    print ( 'XXX684XXX', dir ( self.In[2] ) )
    self.Scene = self.GUI_Controls [0]
    #self.Scene.Start_Script ( self.Input_Value [1] )
    self.Scene.Start_Script ( self.In [2] [ 'CodeText' ])
    if self.Scene.VPC_Code :
      self.In [2] [ 'VPC_Code ' ] = self.Scene.VPC_Code
    """
    
  def Run_Loop ( self ) :
    self.Scene.Execute_Script ( )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_VPython_Controls ( tLWB_Brick ):

  Description = """
Dynamic Controls for VPython.
These Controls can be created from the VPython script code
"""

  def After_Init (self):
    self.Caption = 'VP Controls'

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = [ 'VPython ', TIO_INTERACTION ]

    # Create VPython_Control
    CD = self.Create_Control ( t_C_VPython_Control )

  # *********************************************************************
  # *********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    if XOut[1] :
      VPC = 'VP_Controls'
      if VPC in self.Out[1] :
        self.VP_Controls = self.GUI_Controls [0]
        VPC_Code = self.Out [1] [VPC].split ( '\n' )

        # If no controls wanted, remove them
        if VPC_Code == [''] :
          try:
            exec ( 'self.VP_Controls.Define ( 0, 0 )' )
          except :
            pass
          return

        for lin in VPC_Code :
          line = lin.rstrip ()

          if line :
            line = line.replace ( 'VPC.', 'self.VP_Controls.' )
            
            # all methods, except the Define
            # have a completion method as the last parameter
            # And that completion is not in our NameSpace
            # but in the PG.P_Globals NameSpace
            # Because there the VPython script is executed
            if line.find ( '.Define' ) < 0 :
              parts = line.split( ',' )
              last = parts [ -1 ].replace ( ')', '' ).strip()
              My_Globals = PG.P_Globals [ last ]
              #My_Globals = self.GUI_Controls [0].Code_Globals [ last ]
              line = ','.join ( parts [ : -1 ] ) + ',My_Globals )'
              print ( 'VPC-code', line )
              
            try :
              exec ( line )
            except :
              print ('==== ERR in VPCP parsing')

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_VPython( tLWB_Brick ):

  Description = """
A 3D animation scenery, by embedded VPython"""

  def After_Init (self):
    self.Caption = 'VPython'
    #self.Diagnostic_Mode = True

    # This device wants to be executed every loop
    self.Continuous = True

    # Define the input pins
    self.Inputs [1] = [ _(0, 'Python Code') , TIO_STRING, REQUIRED ]
    #self.Inputs [1] = [ _(0, 'Python Code') , TIO_INTERACTION, REQUIRED ]
    self.Inputs [2] = [ _(0, 'Python Controls') , TIO_INTERACTION ]

    # we want this image-window to be centered
    self.Center = True

    # Create VPython
    CD = self.Create_Control ( t_C_VPython )
    CD.Input_Channel = 1

    self.Scene = None

  # *********************************************************************
  # *********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    if XIn[1] :
      self.Scene = self.GUI_Controls [0]
      self.Scene.Start_Script ( In [1] )
      In [2] [ 'VP_Controls'] = self.Scene.VPC_Code

  # *********************************************************************
  # *********************************************************************
  def Run_Loop ( self ) :
    if self.Scene :
      self.Scene.Execute_Script ( )
# ***********************************************************************




# ***********************************************************************
# ***********************************************************************
class t_PyPlot_Signal ( tLWB_Brick ):

  Description = """Adds Name, Color, LineWidth to signals"""

  def After_Init (self):
    self.Caption = 'PyPlot Signal'

    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = ['Signal',  TIO_ARRAY, True,'']

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = ['Signal + Parameters', TIO_ARRAY ]

    # Create the GUI controls
    CD = self.Create_Control ( t_C_Text_Control, 'Name' )

    CD = self.Create_Control ( t_C_Color_Picker, 'Line Color',
                               wx.Colour ( 100, 200, 100 ) )

    CD = self.Create_Control ( t_C_Spin_Button, 'Line Width', 1 )
    CD.Range   = [ 1, 5 ]

    ##self.Signal_Attr = t_signal_attr ()
    
  # *************************************************
  # *************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :

    # If parameter changed, send all
    if XPar[0] :
      """
      self.Signal_Attr.Name      = Par [2]
      self.Signal_Attr.Color     = Par [3]
      self.Signal_Attr.LineWidth = Par [4]
      Out[1] = In[1], self.Signal_Attr
      """
      Signal_Attr = class_MetaData ()
      Signal_Attr.Name      = Par [2]
      Signal_Attr.Color     = Par [3]
      Signal_Attr.LineWidth = Par [4]
      Out[1] = In[1], Signal_Attr
      print ( '++++++++++ PyPlot Signal', XPar )

    # else send only the signal
    else :
      #print ( '++++++++++ PyPlot Signal nooooo PARRRR')
      Out[1] = In[1]
    """
    
    if XPar[0] or XIn[0] :
      self.Signal_Attr.Name      = Par [2]
      self.Signal_Attr.Color     = Par [3]
      self.Signal_Attr.LineWidth = Par [4]
      Out[1] = In[1], self.Signal_Attr
      print ( '++++++++++ PyPlot Signal', XPar )
    """

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
    self.Caption = 'Generator'

    # This device wants to be executed every loop
    self.Continuous = True

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
    self.Outputs [1] = ['Sine Wave', TIO_ARRAY ]
    self.Outputs [2] = ['Square Wave', TIO_ARRAY ]

    # Create the GUI controls
    CD = self.Create_Control ( t_C_Slider, self.Inputs [1][0], 20 )
    CD.Range         = [10,100]
    CD.Input_Channel = 1

    CD = self.Create_Control ( t_C_RadioBox, 'Frequency Factor', 1 )
    CD.NCol    = 1
    CD.Range   = [ '*0.1 : 1..10', '*1 : 10..100', '*10 : 100..1000' ]

    CD = self.Create_Control ( t_C_Slider, self.Inputs [2][0], 30 )
    CD.Range         = [0,100]
    CD.Input_Channel = 2

    CD = self.Create_Control ( t_C_Slider, self.Inputs [3][0], 0 )
    CD.Range         = [-10,10]
    CD.Input_Channel = 3

    # initial values
    self.start = 0
    self.Frequency_Factor = [ 0.1, 1.0, 10.0 ]

    self.Loop_Count = 4

  # *********************************************************************
  # *********************************************************************
  def Run_Loop ( self ) :
    self.Loop_Count -= 1
    if self.Loop_Count <= 0 :
      self.Loop_Count = 4
      self.Create_More_Samples ()

  # *********************************************************************
  # *********************************************************************
  def Create_More_Samples ( self ) :
    N = 10
    #if self.Out[1] == Null : #None :
    if self.Out[0] == None:
      self.Out[1] = zeros ( N )
      self.Out[2] = zeros ( N )
    fSamp = 1000
    A = 0.1 * self.Par [2]

    if self.Par[4] == None :
      self.Par[4] = 1
    FF = self.Frequency_Factor [ self.Par [4] ]
    F = 2 * pi * FF * self.Par [1] / fSamp
    O = self.Par [3]

    for i in arange ( N ) :
      sinus = A * sin ( ( self.start + i ) * F )
      self.Out [1][i] = O + sinus
      if sinus >= 0 :
        self.Out [2][i] = O + A
      else :
        self.Out [2][i] = O - A
    self.start = self.start + N

    # Because of complex arrays, we need to notify manual
    self.Out.Set_Modified ( 1 )
    self.Out.Set_Modified ( 2 )
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class t_ADC ( tLWB_Brick ):

  Description = """AD converter,
supports several AD converters (works only under Windows)."""

  def After_Init (self):
    self.Caption = 'AD Converter'

    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = \
      ['Start/Stop', TIO_NUMBER, False,
       'Can be used to start/stop the ADC immediately']

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = \
      ['Signals', TIO_ARRAY ]
    self.Outputs [2] = \
      ['Signal Names', TIO_ARRAY ]

    # This device wants to be executed every loop
    self.Continuous = True

    # Create the GUI controls
    CD = self.Create_Control ( t_C_AD_Converter, '', 0 )

  # *********************************************************************
  # Procedure only called when inputs and/or parameters have changed
  # *********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    print ( '***************',XIn,In,XPar,Par)
    if XIn[1] :
      C = self.GUI_Controls [0]
      C.Start_Stop ( Start = In[1] )

  
  def Run_Loop ( self ) :
    C = self.GUI_Controls [0]
    N = C.Get_New_Sample_Sets ()
    if N > 0 :
      #print ( 'ADC data', N, type (C.data[0]) )
      #print ( type(C.data ), C.data,C.data[0] )
      if C.MetaData_Changed :
        print ( 'ADC_MetaData_Changed' )
        self.Out [1]   = C.data[0], C.data[1], C.MetaData[0], C.MetaData[1]
        C.MetaData_Changed = False
      else :
        self.Out [1]   = C.data[0], C.data[1]


    B = C.Brick
    #print ( '********************        ***************',
    #           B.In,B.Par)
    # we need to ensure that this procedure is called every time
    #self.Params [1] += 1
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_BP_Analysis ( tLWB_Brick ):

  Description = """Rotates an Image counter clockwise.
The rotation angle (in degrees) and the interpolation are either taken from
the internal GUI controls, or from the external signals,
whichever has been changed last."""

  def After_Init (self):
    self.Caption = 'BP Analysis'

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

    # Create the GUI controls
    CD = self.Create_Control ( t_C_Spin_Button, 'Input Selector', 1 )
    CD.Range   = [ 1, 5 ]

    CD = self.Create_Control ( t_C_Slider, 'Rotation [degrees]', 30 )
    CD.Range   = [ 0, 360 ]

    self.buffer = zeros (100)
    self.p = 0

    # initialize the BP analysis function
    from medilab_pw import BP_analysis
    fsamp = 100
    self.BP = BP_analysis ( fsamp )

    self.Initialized = False

  # *********************************************************************
  # Procedure only called when inputs and/or parameters have changed
  # *********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    if not ( In [1] ) :
      return

    if XIn [1] :
      #print ( '******************** BP1', Par )
      # get index of the selected signal
      S = Par [2] - 1

      #print ( 'BP1', S )

      data, params = Analyze_TIO_Array ( In [1] )
      #print ( 'BP2', type(data),len(data))
      #print ( 'BP3', type(data[S]),len(data[S]),data[S].shape)
      #Analyze_TIO_Array

      # limit the selector switch
      #print ( 'Selected Signal', S, len (data), data.shape )
      if S > len ( data ) :
        S = len ( data )
        self.GUI_Controls [0] = SetValue ( S )

      #
      MetaData = []
      if not ( self.Initialized ) :
        self.Initialized = True
        
        
        Names = self.BP.Get_Signal_Names ()
        for chan, Name in enumerate ( Names ) :
          Signal_Attr = class_MetaData ()
          MetaData.append ( Signal_Attr )
          Signal_Attr.SignalName = Name
          if chan in ( 3, 4 ) :
            Signal_Attr.Calibrate = 1, 0
          else :
            Signal_Attr.Calibrate = params[0].Get ( 'Calibrate', (1,0) )
            Signal_Attr.Units     = params[0].Get ( 'Units', 'mmHg' )
           
          """
return [ 'Psys', 'Pdias', 'MAP', 'BPM', 'RR [msec]', 'BP-filt' ]

          """

      #Out[1] = \
      #  self.BP.execute ( data [S] )[0], MetaData
      if MetaData :
        MetaData = MetaData[0]
        print ( 'METEATAT', MetaData.SignalName)

      Out[1] = \
        self.BP.execute ( data [S] )[0], MetaData

      # NO!!! self.Out.Set_Modified ( 1 )

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_Scope_Display( tLWB_Brick ):

  I = 6

  def After_Init (self):
    self.Caption =  _(2,'Oscilloscope')
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    for i in range ( 1, self.I + 1 ) :
      self.Inputs [i] = ['Signals ' +  str(i), TIO_ARRAY, (i==1),
        _(5, 'Signals to be displayed on the Scope Display' )]

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = [ _(6,'Start / Stop'), TIO_NUMBER,
                         _(1,'Can be used to control an AD-Converter.') ]

    # we want this image-window to be centered
    self.Center = True

    # Create the GUI controls
    CD = self.Create_Control ( t_C_Scope_Display )

  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    #print 'Generate Scope', self.Input_Changed [1]
    if XIn [0] :
      Signals = []
      Signals.append ( self.In [1] )
      if self.In [2].any() :
        Signals.append ( self.In [2] )
      if self.In [3] != None :
        Signals.append ( self.In [3] )
      if self.In [4] != None :
        Signals.append ( self.In [4] )
      if self.In [5] != None :
        Signals.append ( self.In [5] )

      # now send the array to the control
      C = self.GUI_Controls [0]
      C.Add_Data ( Signals )

    # Start / Stop signal
    if XPar [7] :
      Out [1] = Par [7]
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_Scope_Plot( tLWB_Brick ):

  I = 5
  
  def After_Init (self):
    self.Caption = _(8,'Oscilloscope\nHistory')

    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    for i in range ( 1, self.I + 1 ) :
      self.Inputs [i] = [ _(3,'Signals ') +  str(i), TIO_ARRAY, (i==1),
        _(5, 'Signals to be displayed on the Scope Display' )]

    # we want this image-window to be centered
    self.Center = True

    # Create the GUI controls
    CD = self.Create_Control ( t_C_Scope_Plot )

  # *********************************************************************
  # *********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    if XIn [0] :
      C = self.GUI_Controls [0]
      data = []
      for signal in In [1:] :
        #if not ( signal in ( None, Null ) )  :
        if signal != None :
          print ( 'Scope_Plot add', len(signal), type(signal) )
          data.append ( signal )

      C.Add_Data ( data )

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_Code_Editor ( tLWB_Brick ):

  Description = _(9, """Scintilla Code Editor.
Can be used to test small pieces of Python code,
or to make something like a graphical calculator.
This Brick contains a number of input and output nodes,
so it can communicate with other Bricks,
through the variables IN[] and OUT[].
The last output just outputs the whole code as a string.""" )

  def After_Init (self):
    self.Caption = 'Code Editor'
    
    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = [
      'Code', TIO_STRING,
      'Contains Selected Code, All Code' ]
    self.Outputs [2] = [
      'CMD Shell', TIO_INTERACTION,
      'Communication with CMD-Shell' ]
    self.Outputs [3] = [
      'Data Array', TIO_ARRAY,
      """
When Input[1] is not connected,
code will be executed and
Array Data will be connected this Output[3].""" ]

    # Create the GUI controls
    # *************************************************
    # Create the Scintilla editor
    # Parameters
    #   1 = output, ( <complete code>, <selected code> )
    #   2 = IO_Interaction
    #         FileName  = output, the loaded code file
    #         CMD Shell = input, the local Help Browser
    CD = self.Create_Control ( t_C_Code_Editor )
    # *************************************************

    # Create a separate Namespace for the code in the editor
    self.Code_Globals = {'aap':33}
    self.Code_Locals  = {}

    # For TIO_INTERACTION create an empty dictionary
    #self.Params [0] = TIO_Dict ()  #{}
    print ('*********************&&&&&&&&&&&&')


  # *********************************************************************
  # Procedure only called when inputs and/or parameters have changed
  # *********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :

    #print 'CodeEditor-EXEC', Par,XIn,XOut,XPar
    # *******************************************
    # Test Loading of new code file
    # *******************************************
    if XOut [2] :
      if 'CodeFile_To_Open' in XOut[2] :
        FileName = Out [2] ['CodeFile_To_Open']
        self.GUI_Controls [0].STC.Change_File ( FileName )

    # *******************************************
    # Test Loading of new code file
    # *******************************************
    if XPar [1] :
      Out [1] = Par [1]

    # *******************************************
    # If Output[1] is connected,
    # we don't execute the code,
    # but leave that task to the receiver
    # *******************************************
    Code = self.Par[1]
    if Out.Receivers[1] or not ( Code ):
      return
    
    if not ( isinstance ( Code, str ) ) :
      Code = Code [0]

    """
    Error in Simulation File
    YYYY <type 'unicode'> x = arange ( 0.0, 3.0, 0.01 )
    y = 15*cos  ( IN1 * pi * x )
    y2 = 10*sin ( IN2 * pi * x )
    OUT1 = x,y,y2,\
      ('cosine', 'sine')
    """
    # only \n is allowed !!  (see "compile")
    Code = Code.replace('\r\n','\n')
    # remove line continuation, not accepted by exec-statement
    Code = Code.replace('\\\n','')
    # and last line must end with \n   (see "compile")
    Code = Code + '\n'

    #for i in range ( 1, 3 ) :
    #  Code = Code.replace('OUT'+str(i),'self.Output_Value['+str(i)+']')
    Code = Code.replace ( 'OUT1', 'self.Out[3]' )

    try :
      exec ( Code ) #, self.Code_Globals, self.Code_Locals )
      #self.Output_Changed[1] = True
    except :
      import traceback
      traceback.print_exc ()
      print ('******** Code Editor, ERROR: *********')
      print (Code)
    #self.Output_Changed [1] = True
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class t_Signal_Workbench ( tLWB_Brick ):

  Description = _(10, """Signal WorkBench.
bla bla ... """ )

  def After_Init (self):
    self.Caption = 'Signal WorkBench'

    # we want this image-window to be centered
    self.Center = True

    # Create the GUI controls
    CD = self.Create_Control ( t_C_Signal_WorkBench )

  # *********************************************************************
  # Procedure only called when inputs and/or parameters have changed
  # *********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    pass
    """
    print 'Generate SIGNAL WOB',self.Par,self.Params
    Code = self.Params[1]
    # only \n is allowed !!  (see "compile")
    Code = Code.replace('\r\n','\n')
    # remove line continuation, not accepted by exec-statement
    Code = Code.replace('\\\n','')
    # and last line must end with \n   (see "compile")
    Code = Code + '\n'

    for i in range ( 1, self.I+1 ) :
      Code = Code.replace('IN'+str(i),'self.In ['+str(i)+']')

    for i in range ( 1, self.O+1 ) :
      Code = Code.replace('OUT'+str(i),'self.Out['+str(i)+']')

    # if list-pin is connected, use that to control all inputs
    if self.In [ self.I + 1 ] != None :
      temp = copy ( self.In [ self.I + 1 ] )
      self.In = copy ( temp )
      self.In.insert( 0, None )
      self.In.append ( temp )

    try :
      exec ( Code )
    except :
      print '******** Code Editor, ERROR: *********'
      print Code
    """
# ***********************************************************************






# ***********************************************************************
# ***********************************************************************
class t_Code_Slider ( tLWB_Brick ):

  Description = """Sliders for Code Generator."""
  N = 3
  
  def After_Init (self):
    self.Caption = 'Code Sliders'
    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    for i in range ( 1, self.N+1 ) :
      self.Outputs [i] = ['Slider Value '+ str(i), TIO_NUMBER ]
    self.Outputs [ self.N + 1] = ['All Sliders', TIO_LIST]

    # Create the GUI controls
    for i in range ( 1, self.N+1 ) :
      CD = self.Create_Control ( t_C_Slider, 'Value '+str(i), 0 )
      CD.Range   = [0,100]

      #CD = self.Create_Control ( t_C_Slider, 'Frequency', 100 )
      #CD.Range = [1,10000]
      #CD.Log   = True


  # *********************************************************************
  # Procedure only called when inputs and/or parameters have changed
  # *********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    pass
    """
    self.Out [ self.N+1] = []
    for i in range ( 1, self.N+1 ) :
      self.Out [i] = self.Params [i]
      self.Out [ self.N+1].append ( self.Params [i] )
    """

    if XPar [0] :      # check if any Par changed
      if XPar [1] :    # check if Par [1] changed
        A = Par [1]    # use Par [1]
      if XPar [2] :
        B = Par [2]

    
# ***********************************************************************

#CS_SN0 = "x = arange ( 0.0, 3.0, 0.01 )\ny = 15*cos  ( IN1 * pi * x )\ny2 = 10*sin ( IN2 * pi * x )\nOUT1 = x,y,y2,\\\n('cosine', 'sine')\n"
#CS_SN1 = [(192, 192, 192), (0, 0, 0), True, True, True, False, False]


# ***********************************************************************
# ***********************************************************************
class t_Read_Sound ( tLWB_Brick ):

  Description = """
Reads a Sound File.
  Out[1] = Sound Filename
  Out[2] = Sound File Data (only if connected)
"""

  def After_Init (self):
    self.Caption = _(15, 'Load SoundFile')

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = \
      [ _(11, 'FileName'), TIO_STRING,
        _(12, 'Filename of the Sound File.' ) ]
    self.Outputs [2] = \
      [ _(13, 'Sound'), TIO_ARRAY,
        _(14, 'Data from the Sound File' ) ]

    # *************************************************
    # Create File Select
    # Range = one of the constants definied in
    #         ../support/dialog_support.py
    #       or
    #         a general file dialog mask, e.g.
    #         'dBase Files(*.db)|*.db|All Files(*.*)|*.*'
    CD = self.Create_Control ( t_C_File_Open, 'Read Sound File', Default = '' )
    CD.Range   = '*.wav'



  # **********************************************************************
  # this procedure is only called when inputs (or parameters) have changed
  # **********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    if XPar [1] :
      if not ( File_Exists ( Par [1] ) ) :
        return
      Out [1] = Par [1]

      if self.Output_Connected [2] :

        import wave
        wav  = wave.open ( Par[1], 'r' )
        amount = 14 * 256 * 35 #Max Amount

        MetaData = class_MetaData()
        MetaData.Frequency = wav.getframerate ()
        MetaData.ByteWidth  = wav.getsampwidth ()

        if MetaData.ByteWidth == 1:
          data = fromstring(wav.readframes(amount),uint8)
        else:
          data = fromstring(wav.readframes(amount),'>i'+str(MetaData.ByteWidth))

        Out [2] = data,MetaData

        print ( 'BTC', type ( Out[2]), type (data) )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_Input_Selector ( tLWB_Brick ):

  Description = _(16, """Select an input signal.""")
  I = 5

  def After_Init (self):
    self.Caption = _(19, 'Input Selector')
    
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    for i in range ( 1, self.I+1 ) :
      self.Inputs [i] = ['IN['+ str(i)+']', TIO_ARRAY, i==1 ]

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = \
      [ _(17, 'Output'), TIO_ARRAY,
        _(18, 'Data from selected Input' ) ]

    # Create the GUI controls
    CD = self.Create_Control ( t_C_Spin_Button, 'Input' )
    CD.Range   = [ 1, self.I ]

  # **********************************************************************
  # this procedure is only called when inputs (or parameters) have changed
  # **********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    if XIn [0] or XPar [0] :
      Out [1] = In [ Par [ self.I + 1 ] ]
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

  Description = _(20, """Scintilla Code Editor.
Can be used to test small pieces of Python code,
or to make something like a graphical calculator.
This Brick contains a number of input and output nodes,
so it can communicate with other Bricks,
through the variables IN[] and OUT[]""" )

  def After_Init (self):
    self.Caption =_(0, 'BTC Sound' )
    
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = ['Input Stream', TIO_ARRAY, True ]

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = ['Output_Stream', TIO_ARRAY ]

    # Create the GUI controls
    CD = self.Create_Control ( t_C_Text_Control, 'Btc'        )
    CD = self.Create_Control ( t_C_Text_Control, 'R [kOhm]'   )
    CD = self.Create_Control ( t_C_Text_Control, 'C [nF]'     )
    CD = self.Create_Control ( t_C_Text_Control, 'Freq. [Hz]' )

    CD = self.Create_Control ( t_C_Buttons, 'Knopje' )

  # **********************************************************************
  # this procedure is only called when inputs (or parameters) have changed
  # **********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    if In[1]==None:
      return

    C = self.GUI_Controls #???
    from numpy import array     #Moet niet nodig zijn, PyLab_Works moet hier voor zorgen

    data, MetaData = Analyze_TIO_Array(In[1])
    data = data[0]
    MetaData = MetaData[0]

    # Maybe scaling needs to be done only once... Just change Vmax & Vmin (Danger Vmin assumed 0)

    # Scale to 0..5 V range
    Bits = MetaData.Get('ByteWidth',1)*8
    if Bits == 8:
      data = data.astype(float64) * 5.0  / 2.0**8
    else:
      data = data.astype(float64)
      data = (data + 2.0**(Bits-1))/ 2.0**Bits * 5.0

    Vmax = 5.0 # Maximum voltage
    Vmin = 0.0 # Minimum voltage
    Vold = 0.0 # Start voltage
    Btc = 36 # The Btc (Binair time constant)

    # Bert's method
    bert_bitlist = [] # List of bits
    bert_list    = [] # List of voltages
    for frame in data:
      hi = Vold + (Vmax - Vold) / Btc
      lo = Vold + (Vmin - Vold) / Btc
      if abs(frame - hi) < abs(frame - lo):
        bert_bitlist.append(1) # High bit
        Vold = hi
      else:
        bert_bitlist.append(0) # Low bit
        Vold = lo
      bert_list.append(Vold)

    # Transform back to original range, for easy comparison
    if Bits == 8:
      data = array(bert_list) * 256.0 / 5.0
    else:
      data = array(bert_list) * 2.0**Bits / 5.0 - 2.0**(Bits-1)

    Out [1] = data, MetaData

# ***********************************************************************
pd_Module ( __file__ )
