import __init__

#import PyLab_Works_Globals as PG
import os
import PyLab_Works_Globals as PG
from file_support    import File_Exists, Find_Files
from gui_support import Create_wxGUI
from General_Globals import *
import wx

My_Control_dX2 = 70

# ***********************************************************************
# ***********************************************************************
class _Simple_Par ( object ) :
  """
  Class to make it more easy to set a Bricks.Par
  from a control.
  So instead of :
    self.Brick.Par [ self.EP[0] ] = self.GetValue ()
  you can write
    self.P [0] = self.GetValue ()
  """
  def __init__ ( self, control ) :
    self.Control = control

  def __setitem__ ( self, index, value ) :
    #v3print ( '_Simple_Par', index, value, self.Control.Brick.Caption,
    #          self.Control.EP, self.Control.Brick.Par)
    i = self.Control.EP [ index ]
    if i :
      self.Control.Brick.Par [ i ] = value

  def __getitem__ ( self, index ) :
    i = self.Control.EP [ index ]
    if i :
      return self.Control.Brick.Par [ i ]
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class My_Control_Class ( object ) :
  # *************************************************************
  # Form creation
  # *************************************************************
  def __init__ ( self,  Dock,         # the frame/panel/... where we can put
                                      # the GUI controls that will catch events
                 Brick = None,        # the Brick, with its inputs and outputs
                 Control_Defs = None, #
                 Ini   = None,        # inifile to store and reload settings
                 Test  = False ):     # if True, testmode with buildin examples

    self._Control_Dir = dir ( self )

    # Collect all methods and attributes of other classes
    self.Exclude_Dir  = []
    Base_Classes = self.__class__.__bases__
    for BC in Base_Classes :
      if BC != My_Control_Class :
        self.Exclude_Dir += dir ( BC )

    #Frame = Dock
    #while not ( isinstance ( Frame, wx.Frame )) and \
    #      not ( isinstance ( Frame, wx.Window )) :
    #  Frame = Frame.parent
    self.TopFrame = wx.GetTopLevelParent ( Dock )
    #top = child.GetTopLevelParent()

    self.Dock  = Dock
    self.Brick = Brick
    self.CD    = Control_Defs
    #self.Display_Label =  self.Dock.Display_Label
    #self.Caption = self.CD.Caption
    self.Caption = None

    self.Type = None

    self.Test  = Test
    self.Ini   = Ini

    # sometimes the parent doesn't has x,y
    try :
      self.X    = self.Dock.x + 5
      self.Y    = self.Dock.y
    except :
      pass
    self.dX = 0
    self.dY = 0

    self.Icon  = None
    if Brick :
      self.IniSection = 'Device ' + Brick.Name
    else :
      self.IniSection = 'Device ...'

    self.EP        = [ None  ]
    self.EP_IsDict = [ False ]

    self.P = _Simple_Par ( self )

    # weet niet of dit goed gaat
    if not ( 'Load_Settings' in dir ( self ) ) :
      self.Load_Settings = None
    #if not ( 'Save_Settings' in dir ( self ) ) :
    #  self.Save_Settings = None

    self.Dock.Bind ( wx.EVT_SIZE                , self._On_Size  )

    # Bind all simple control events
    self.Dock.Bind ( wx.EVT_BUTTON              , self._On_Event )
    self.Dock.Bind ( wx.EVT_SLIDER              , self._On_Event )
    self.Dock.Bind ( wx.EVT_RADIOBOX            , self._On_Event )
    self.Dock.Bind ( wx.EVT_SPINCTRL            , self._On_Event )
    self.Dock.Bind ( wx.EVT_TEXT_ENTER          , self._On_Event )
    self.Dock.Bind ( wx.EVT_COLOURPICKER_CHANGED, self._On_Event )

  # ***********************************************************************
  # ***********************************************************************
  def Save_Settings ( self, ini, key ) :
    Value = self.GetValue ()
    if isinstance ( Value, wx.Colour ) :
      temp = tuple ( Value) +  ( Value.Alpha(), )
      Value = temp
    ini.Write ( key, Value )
    #v3print ( '**** GENERAL SAVING', key )

  # ***********************************************************************
  # ***********************************************************************
  def Load_Settings ( self, ini, key ) :
    Value = ini.Read ( key, None )
    if Value :
      #v3print ( '**** GENERAL LOADING', key, Value )
      if self.Type :
        Value = self.Type ( Value )
      self.SetValue ( Value )
      
      # AND simply pass this value also to the Par-array
      self.P[0] = Value
      
    #v3print ( '**** GENERAL LOADING', key )

  """
  # ***********************************************************************
  # ***********************************************************************
  def Display_Label ( self ) :
    try :
      if self.CD.Caption :
        self.Caption = wx.StaticText ( self.Dock, -1, self.CD.Caption,
                               pos = ( self.X, self.Y ) )
        dc = wx.ScreenDC()
        dx, dy = dc.GetTextExtent ( self.CD.Caption )
        return self.Caption, dx, dy
    except :
      pass
  """

  # ***************************************
  def Test1 ( self ) :
    v3print ( 'This control has no Test-1' )

  # ***************************************
  def Test2 ( self ) :
    v3print ( 'This control has no Test-2' )

  # ***************************************
  def Test3 ( self ) :
    v3print ( 'This control has no Test-3' )

  # ***************************************
  def GetId ( self ) :
    return 0

  # ***************************************
  def _EP_Add ( self, Dictionairy = False ) :
    self.EP.append ( None )
    self.EP_IsDict.append ( Dictionairy )

  # ***************************************
  def Kill ( self ) :
    pass

  # ***************************************
  def SetValue ( self, value ) :
    pass

  # ***************************************
  def GetValue ( self ) :
    return None

  # ***************************************
  def GetSize ( self ) :
    return ( 0, 0 )

  # ***************************************
  def SetForegroundColour ( self, color ) :
    if self.Caption :
      self.Caption.SetForegroundColour ( color )

  # ***************************************
  def _On_Event ( self, event ) :
    """
Handles simple events.
Because events are sent to each control on a Pane,
Check to see if the event is coming from itself,
in which case handle the event,
otherwise Skip.
"""
    #print '*************** EVENT',event.GetId (),self.GetId (),self.Caption
    if event.GetId () == self.GetId () :
      #v3print ( '_On_Event', type ( self ), self.GetValue () )
      self.P[0] = self.GetValue ()
      self._On_Extra_Event_Handler ( event )
    else :
      event.Skip()

  # ***************************************
  def _On_Extra_Event_Handler ( self, event = None ) :
    """
    This enables debug facilities to hook to a change event
    """
    pass

  # ***************************************
  def _On_Size ( self, event ) :
    event.Skip ()
    w, h = self.Dock.GetClientSize ()
    try :
      self.SetSize     (( w - 5, self.GetSize()[1] ))
    except :
      pass
    try :
      self.SetPosition (( self.X, self.Y ))
    except :
      pass
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Split_Init_Code ( Code_Input, Parent = None, Script_Globals = None ) :
  """
Splits a piece of Python code into an
 - INIT section, including the Parent.Init_Code_After
 - Control Section
 - LOOP section, including the Parent.Loop_Code_After
The Code_Input can be a single string
or a tupple of 2 strings
 - the first string contains the whole text of an editor
 - the second string contains the selected part of the editor's text
At the moment always the whole Code is fetched
  """
  # Code can be a string or
  # a tuple of 2 strings: ( <total code>, <selected code> )
  if isinstance ( Code_Input, str ) :
    Code = Code_Input
  else :
    Code = Code_Input [0]
    """
    if Code_Input[1] :
      Code = Code_Input[1]
    else :
      Code = Code_Input[0]
    """
    
  if not ( Script_Globals ) :
    Script_Globals = globals ()

  # only \n is allowed !!  (see "compile")
  Code = Code.replace('\r\n','\n')
  # remove line continuation, not accepted by exec-statement
  Code = Code.replace('\\\n','')
  # and last line must end with \n   (see "compile")
  Code = Code + '\n'
  Code = Code.split ( '\n' )

  #v3print ( 'INIT1', Init_Code )
  Loop_Code_Wanted = True
  i = 0
  while_found = -1
  while ( i < len ( Code ) ) : # and  ( while_found < 0 ):
    line = Code [i]
    init = line.find ( 'while ')
    if init == 0 :
      while_found = i
      break
    i += 1
  else :
    Loop_Code_Wanted = False
    while_found = len ( Code )

  Init_Code = ''
  VPC_Code  = ''
  #if Parent and Parent.Init_Code_Before :
  #  Init_Code += Parent.Init_Code_Before
  for i in range ( while_found ) :
    if Code[i].strip().startswith ( 'VPC' ) :
      VPC_Code += Code [i] + '\n'
    else :
      Init_Code += Code [i] + '\n'
  if Parent and Parent.Init_Code_After :
    Init_Code += Parent.Init_Code_After
  Init_Code += '\n'

  # first insert a number of empty lines
  # so error messages points to the right line
  Loop_Code = ''
  for i in range ( while_found + 1) :
    Loop_Code += '\n'

  #if Parent and Parent.Loop_Code_Before :
  #  Loop_Code += Parent.Loop_Code_Before
  # get the indentation of the first not empty line after the while
  if Loop_Code_Wanted :
    i = while_found + 1
    indent = 0
    while ( i < len ( Code ) ):
      if Code[i].strip() != '' :
        indent = len ( Code[i] ) - len ( Code[i].lstrip () )
        break
      i += 1
    for i in range ( while_found+1, len ( Code ) ) :
      Loop_Code += Code [i] [ indent : ] + '\n'
  if Parent and Parent.Loop_Code_After :
    Loop_Code += Parent.Loop_Code_After

  return Init_Code, VPC_Code, Loop_Code
# ***********************************************************************


# ***********************************************************************
# This code must be here, otherwise we don't have the global "visual"
# when we run through PG.P_Globals this could be placed anywhere
# ***********************************************************************
class tScenery_Base ( My_Control_Class ):
  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    GUI = """
      self.p1  ,wx.Panel
    """
    self.wxGUI = Create_wxGUI ( GUI, my_parent = 'self.Dock' )
    self.Script_Error = False

    # We also pass the globals to PG,
    # so e.g. VPC controls can reach them
    PG.P_Globals = self.Code_Globals = {}
    self.Init_Code_Before = None
    self.Init_Code_After  = None
    self.Loop_Code_Before = None
    self.Loop_Code_After  = None


  # *********************************************************
  # *********************************************************
  def Start_Script ( self, Code ) :
    Init_Code, self.VPC_Code, self.Loop_Code = \
      Split_Init_Code ( Code, self, self.Code_Globals ) #PG.P_Globals )

    """
    v3print ( '======= INIT ======' )
    v3print ( Init_Code )
    v3print ( '======= VPython Control Code ======' )
    v3print ( self.VPC_Code )
    v3print ( '======= Loop ======' )
    v3print ( self.Loop_Code )
    v3print ( '======= END Loop ======' )
    """

    # Add own Library directory to the namespace
    path = os.path.join ( Application.Dir, PG.Active_Project_Filename, 'Libs' )
    self.Code_Globals [ 'My_Path' ] = path + '/'

    # The init code is executed separately
    # to get the correct line number for error messages
    if self.Init_Code_Before :
      try :
        exec ( self.Init_Code_Before, self.Code_Globals )
      except :
        pass

    try :
      exec ( Init_Code, self.Code_Globals )
      self.Script_Error = False
    except :
      import traceback
      traceback.print_exc ( 5 )
      print ('******** SCENE Code Editor, ERROR: *********')

  # *********************************************************
  # *********************************************************
  def Execute_Script ( self ) :
    # The Pre-Loop code is executed separately
    # to get the correct line number for error messages
    if self.Loop_Code_Before :
      try :
        exec ( self.Loop_Code_Before, self.Code_Globals )
      except :
        pass

    if self.Loop_Code :
      try :
        exec ( self.Loop_Code, self.Code_Globals )
        self.Script_Error = False
      except :
        if not  ( self.Script_Error ) :
          self.Script_Error = True
          import traceback
          traceback.print_exc ( 5 )
# ***********************************************************************


"""
# ***********************************************************************
# ***********************************************************************
Control_Classes = []
Control_Modules = []
my_dir = path_split ( __file__ )[0]
Py_Files = Find_Files ( my_dir, 'control_*.py', RootOnly = True )
#print 'OOO',Py_Files
#print __file__

#import control_general

for module in Py_Files :
  print ' :   ', module
  my_classes = Get_Control_Classes ( module [1] )

  for klass in my_classes :
    print ' :        ', klass
    Control_Classes.append ( klass  )
    Control_Modules.append ( module [1] )
    line = 'from ' + module[1] + ' import t_C_' + klass
    print line
    exec ( line )
# ***********************************************************************
"""

# ***********************************************************************
pd_Module ( __file__ )
#print '***** end base_control ****'


