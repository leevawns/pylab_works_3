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
    self.Scene = self.GUI_Controls [0]
    #self.Scene.Start_Script ( self.Input_Value [1] )
    self.Scene.Start_Script ( self.In [1] )
    if self.Scene.VPC_Code :
      self.In [2] [ 'VPC_Code ' ] = self.Scene.VPC_Code

  def Run_Loop ( self ) :
    self.Scene.Execute_Script ( )
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
                               wx.Color ( 100, 200, 100 ) )

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
      v3print ( '++++++++++ PyPlot Signal', XPar )

    # else send only the signal
    else :
      #v3print ( '++++++++++ PyPlot Signal nooooo PARRRR')
      Out[1] = In[1]
    """

    if XPar[0] or XIn[0] :
      self.Signal_Attr.Name      = Par [2]
      self.Signal_Attr.Color     = Par [3]
      self.Signal_Attr.LineWidth = Par [4]
      Out[1] = In[1], self.Signal_Attr
      v3print ( '++++++++++ PyPlot Signal', XPar )
    """

# ***********************************************************************



