# ***********************************************************************
# ***********************************************************************
from brick import *
from PyLab_Works_Globals import *
#from base_control        import *
from import_controls import *
# ***********************************************************************

Library_Color = wx.Colour(180,50,180)
Library_Icon = 'python.png'

# ***********************************************************************
# Can take over stdout and/or stderr
# following commands work:
#   select / select all / copy
# ***********************************************************************
class t_CMD_Shell_Doc ( tLWB_Brick ):

  Description = """Can catch stdout and/or stderr messages,
settings can be toggled"""

  def After_Init (self):
    self.Caption = 'CMD Shell Doc'
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = ['IN[1]', TIO_INTERACTION, False, 'Editor Interaction' ]

    # Create the GUI controls
    CD = self.Create_Control ( t_C_Cmd_Shell_Doc )
    CD.Input_Channel = 1

  # *********************************************************************
  # Procedure only called when inputs and/or parameters have changed
  # *********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    # Clicked on the tree, to select another py-file
    if XPar [1] :
      for key in Par [1] :
        In [1] [key] = Par [1] [key]
# ***********************************************************************

# ***********************************************************************
# Can take over stdout and/or stderr
# following commands work:
#   select / select all / copy
# ***********************************************************************
class t_CMD_Shell ( tLWB_Brick ):

  Description = """Can catch stdout and/or stderr messages,
settings can be toggled"""

  def After_Init (self):
    self.Caption = 'CMD Shell'
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = ['IN[1]', TIO_INTERACTION, False, 'Editor Interaction' ]

    # Create the GUI controls
    CD = self.Create_Control ( t_C_Cmd_Shell )

    ##self.Params[0] = 0

  # *********************************************************************
  # Procedure only called when inputs and/or parameters have changed
  # *********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    #print 'CMD SHELL IN',self.In
    IO = self.In [1]
    FileName = 'FileName'
    if FileName in IO :
      self.CMD_Shell = self.GUI_Controls [0]
      self.CMD_Shell.Set_FileName ( IO [ FileName ] )
    if not ( 'CMD_Shell' in IO ) :
      IO [ 'CMD_Shell' ] = self.CMD_Shell
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_Doc_Viewer ( tLWB_Brick ):

  Description = """Can catch stdout and/or stderr messages,
settings can be toggled"""

  def After_Init (self):
    self.Caption = 'Document Viewer'
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = ['IN[1]', TIO_INTERACTION, False, 'Editor Interaction' ]

    # Create the GUI controls
    CD = self.Create_Control ( t_C_Doc_Viewer )

  # *********************************************************************
  # Procedure only called when inputs and/or parameters have changed
  # *********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    #print 'CMD SHELL IN',self.In
    # ???? id it nodig ???
    IO = self.In [1]
    FileName = 'FileName'
    if FileName in IO :
      self.CMD_Shell = self.Control_Defs[0]['Control']
      self.CMD_Shell.Set_FileName ( IO [ FileName ] )
    if not ( 'CMD_Shell' in IO ) :
      IO [ 'CMD_Shell' ] = self.CMD_Shell
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_For_Loop ( tLWB_Brick ):
  Description = """Basic Python Syntax"""

  def After_Init (self):
    self.Caption = 'For Loop'
    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = ['Start Value', TIO_NUMBER, False, '']
    self.Inputs [2] = ['End Value',   TIO_NUMBER, False, '']
    self.Inputs [3] = ['Step Size',   TIO_NUMBER, False, '']

    # Define the output pins
    # <Pin-Name>, <Data_Type>, <Description>
    self.Outputs [1] = ['Current Value', TIO_NUMBER, '']

    #self.Params.append ( 0 )      # Actual Value
    #self.Params.append ( 0 )      # Start Value
    #self.Params.append ( 360 )    # End Value
    #self.Params.append ( 1 )      # Step Size

    # Create the GUI controls, Creation order is Display order
    # <control type>, self, <input channel or None>
    #    <caption>, <hinttext>,
    #       <value>, <range>, <other control specific information>
    # Create the GUI controls
    CD = self.Create_Control ( t_C_Static_Text )
    CD.Caption = 'Actual Value %2d' %33

    CD = self.Create_Control ( t_C_Spin_Button, 'Start Value', 0 )
    CD.Range         = [ -1000, 1000 ]
    CD.Input_Channel = 1

    CD = self.Create_Control ( t_C_Spin_Button, 'End Value', 360 )
    CD.Input_Channel = 2

    CD = self.Create_Control ( t_C_Spin_Button, 'Step Size', 1 )
    CD.Input_Channel = 3

  # **********************************************************************
  # this procedure is only called when inputs (or parameters) have changed
  # Because it has no input parameters it will be called every cycle, IS THIS NECESARY ??
  # **********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    pass
    """
    try :
      #print self.Output_Value[0]
      #print self.Params
      new = self.Out[0] + self.Params[3] - self.Params[2]
      delta = self.Params[3]
      #print new,delta,new/delta,abs(new/delta)
      # check if new value inside the given range
      if abs ( new / delta ) != new / delta :
        self.Out[0] = self.Out[0] + self.Params[3]

    except :
      print 'error in FOR LOOP'
    """
# ***********************************************************************


