import __init__

# ***********************************************************************
# JALfs SUPER GLOBALS
# These variables should be definied here as MUTABLE !!
#
# Each module that needs access to these variables, should use
#     from JALfs_globals import *
#
# It can then use these variables in the module and 1 deep functionsm by
#     RS232_buffer.append('M2')
# ***********************************************************************



# ***********************************************************************
# first add subdirectories to PythonPath !!
# so the modules in those directories are available
# without referencing the subdir explicitly
# ***********************************************************************
from General_Globals import *

import sys
pd_Module ( 'sys' )


import wx
pd_Module ( 'wx' )
import os
pd_Module ( 'os' )


# ***********************************************************************
# VERY IMPORTANT:
#   SQLlite must be imported before SCIPY * !!!
# ***********************************************************************
import sqlite3
pd_Module ( 'sqlite3' )
#from   scipy import *
#pd_Module ( 'scipy' )
# ***********************************************************************

import wave
pd_Module ( 'wave' )

#from numpy import *
#a = zeros ( 5 )

"""
import pygame
Traceback (most recent call last):
  File "PyLab_Works.py", line 33, in ?
  File "PyLab_Works_Globals.pyc", line 14, in ?
  File "pygame\__init__.pyc", line 147, in ?
  File "pygame\surfarray.pyc", line 12, in ?
  File "pygame\surfarray.pyc", line 10, in __load
  File "Numeric.pyc", line 93, in ?
  File "Precision.pyc", line 26, in ?
  File "Precision.pyc", line 23, in _fill_table
  File "Precision.pyc", line 18, in _get_precisions
TypeError: data type not understood
"""

Test_Conditions = {
 1: 'WinXP-SP2, Python 2.4.3, wxPython wx-2.8-msw-ansi',
 2: 'WinXP-SP2, Python 2.5.2, wxPython 2.8.7.1 (msw-unicode)',
}


# ***********************************************************************
# ***********************************************************************
def version ( module ) :
  return getattr ( module, '_Version_Text' )[0][0]
# ***********************************************************************


# ***********************************************************************
# Application specific libraries, USED BY MANY BRICKS
# ***********************************************************************
from language_support import  _, Set_Language
pd_Module ( 'language_support' )
from utility_support  import *
from file_support     import *
from dialog_support   import *
from gui_support      import *
from math             import pi
# ***********************************************************************


Set_Language ( 'US', True )

Program_Name = 'PyLab Works'
Version_Nr = '0.1'


REQUIRED = True

odd = True   # ONLY FOR TEST !!!

Line_Delay = 0.5
Line_Nr = 1


# JALfs_globals.py
RS232_Buffer = []


#Serial_HW_Read_out_0 = []
JAL_FO = []

Standalone   = None
TestRun      = False
App_Running  = False
Virtual_Time = 0
JSM_count    = 0               # extra counter to increment virtual time
Cycle_Nr     = 0

P_Globals    = {}            # Used to pass around globals of executed scripts

SS_Edit      = wx.ID_ANY
SS_Run       = wx.ID_ANY
SS_Step      = wx.ID_ANY
SS_Stop      = wx.ID_ANY
SS_HighLight = wx.ID_ANY
State        = SS_Edit
State_Do_Init    = True
State_After_Init = None
Brick_Errors = {}

#Reload_Exception = "User wants to reload the JAL file"
class Reload_Exception(Exception):
   """User wants to reload the JAL file"""
   pass
Form_List = []

#Variable for PROGRAM
Main_Form = None # wx.frame
app = None       # wx.app
Final_App_Form = None # frame for application final

Programs_Inifile = None

Active_Project_Inifile = None
Active_Project_Filename = ''
Active_Tree_Project = None
Active_Project_max_ID = -1
Active_Project_SubPath = 'pylab_works_programs'

New_Project_Last_Number = 683


rgb = 235
General_BackGround_Color = wx.Colour ( rgb, rgb, rgb )

#TIO_NAMES = [ 'Number', 'List', 'Array', 'wx.Image', 'CallBack',
#              'String', 'TreeList', 'GridData']
TIO_NUMBER      = 0
TIO_LIST        = 1
TIO_ARRAY       = 2
TIO_IMAGE       = 3
#TIO_CALLBACK    = 4
TIO_STRING      = 5
TIO_TREE        = 6
TIO_GRID        = 7
TIO_INTERACTION = 8

TIO_NAMES = {
  TIO_NUMBER      : 'Number',
  TIO_LIST        : 'List',
  TIO_ARRAY       : 'Array',
  TIO_IMAGE       : 'wx.Image',
  #TIO_CALLBACK    : 'CallBack',
  TIO_STRING      : 'String / StringList',
  TIO_TREE        : 'TreeList',
  TIO_GRID        : 'GridData',
  TIO_INTERACTION : 'IO Communication',
}

#NEWW = True
Simulation_Filename = "PyLab_Works_Simulation_File.py"
Simulation_Filename_Fixed = "PyLab_Works_Simulation_File_fixed.py"
Bricks = []
Execution_HighLight = False
Brick_Execution_Color = wx.Colour ( 255, 0, 255 )


pid_Upload = None
PIC = None
PIC_Time = 0

# the range [0,1,2,...] of normal nets (so no power nets)
N_Normal_Nets = []

# List of all devices (pointers to ..)
Device_List = []

# [ [ (<device_R.tResistor object at 0x01FBCDD0>, 2),
#     (<device_R.tResistor object at 0x01FBCFF0>, 1)],
#   [ (<device_R.tResistor object at 0x01FBCFF0>, 2)],
#   [(<device_R.tResistor object at 0x01FBCDD0>, 1)]]
Net_List = []

# ['N$1', '+5V', 'AGND']
Net_List_Names = []

# Orientation of the Bricks editor,
# default is Vertical: Inputs on Top, Outputs on Bottom
#OGL_Orientation_Hor = None

# placeholders for the original stdout / stderr
_Old_StdOut = [ sys.stdout ]
_Old_StdErr = [ sys.stderr ]
_Old_Std_Viewer = None


# ***********************************************************************
# ***********************************************************************
def Set_StdOut ( Owner_Out ) :
  sys.stdout = Owner_Out
  if Owner_Out in _Old_StdOut :
    _Old_StdOut.remove ( Owner_Out )
  _Old_StdOut.append ( Owner_Out )
  ##print 'SETOUT',_Old_StdOut

# ***********************************************************************
# ***********************************************************************
def Restore_StdOut ( Owner_Out ) :
  if Owner_Out in _Old_StdOut :
    if _Old_StdOut [ -1 ] == Owner_Out :
      sys.stdout = _Old_StdOut [ -2 ]
    _Old_StdOut.remove ( Owner_Out )
  ##print 'RESTORE',_Old_StdOut

# ***********************************************************************
# ***********************************************************************
def Set_StdErr ( Owner_Out ) :
  sys.stderr = Owner_Out
  if Owner_Out in _Old_StdErr :
    _Old_StdErr.remove ( Owner_Out )
  _Old_StdErr.append ( Owner_Out )
  ##print 'SETERR',_Old_StdErr

# ***********************************************************************
# ***********************************************************************
def Restore_StdErr ( Owner_Out ) :
  if Owner_Out in _Old_StdErr :
    if _Old_StdErr [ -1 ] == Owner_Out :
      sys.stderr = _Old_StdErr [ -2 ]
    _Old_StdErr.remove ( Owner_Out )
  ##print 'RESTORE ERR',_Old_StdErr



# ***********************************************************************
# ***********************************************************************
class X_Simple_Par ( object ) :
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
    self.Control.Brick.Par [ self.Control.EP [ index ] ] = value
# ***********************************************************************

XMy_Control_dX2 = 70

# ***********************************************************************
# ***********************************************************************
class XMy_Control_Class ( object ) :
  # *************************************************************
  # Form creation
  # *************************************************************
  def __init__ ( self,  Dock,         # the frame/panel/... where we can put
                                      # the GUI controls that will catch events
                 Brick = None,        # the Brick, with its inputs and outputs
                 Control_Defs = None, #
                 Ini   = None,        # inifile to store and reload settings
                 Test  = False ):     # if True, testmode with buildin examples

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
      self.IniSection = 'Device ' + Name

    self.EP        = [ None  ]
    self.EP_IsDict = [ False ]

    self.P = _Simple_Par ( self )
    
    # weet niet of dit goed gaat
    if not ( 'Load_Settings' in dir ( self ) ) :
      self.Load_Settings = None
    if not ( 'Save_Settings' in dir ( self ) ) :
      self.Save_Settings = None

    self.Dock.Bind ( wx.EVT_SIZE                , self._On_Size  )

    # Bind all simple control events
    self.Dock.Bind ( wx.EVT_BUTTON              , self._On_Event )
    self.Dock.Bind ( wx.EVT_SLIDER              , self._On_Event )
    self.Dock.Bind ( wx.EVT_RADIOBOX            , self._On_Event )
    self.Dock.Bind ( wx.EVT_SPINCTRL            , self._On_Event )
    self.Dock.Bind ( wx.EVT_TEXT_ENTER          , self._On_Event )
    self.Dock.Bind ( wx.EVT_COLOURPICKER_CHANGED, self._On_Event )

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
    if event.GetId () == self.GetId () :
      self.P[0] = self.GetValue ()
      """
      try :
        print 'TTRREE',self.GetId(), event.GetId(),self.GetValue (),self.Brick.Par
      except :
        pass
      print 'TTRREE',self.Brick.Par.Modified
      """
    else :
      event.Skip()

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

#from base_control import *





# ***********************************************************************
# ***********************************************************************
class tDebug_Table ( object ) :

  _Header_Color  = '#aaffaa;'
  _Header_Repeat = 10
  _Colum_Width_0 = '10'

  def __init__ ( self, NBricks = 1, On = False ) :
    # Create a new unique filename
    self.FileName   = Application.Dir + '/test_debug_'
    self.FileNum    = 7
    self._On        = False
    self.Prev_Brick = -1
    self.All_Lines  = []
    self.LineNr     = 1
    if self._On :
      self.Set_On ( Nbricks )

  # **********************************************
  # **********************************************
  def Close ( self ) :
    print('REEERDAR')

  # **********************************************
  # **********************************************
  def Set_On ( self, NBricks = 1 ) :
    if not ( Application.Debug_Table ) :
      return

    # if already running, store / close file
    if self._On :
      # Dump what's in the buffer, unless it's the first line
      if True in self.Changes and self.All_Lines :
        line = '<tr valign=top>\n'
        line += '<td width=' + self._Colum_Width_0 + 'px >' +\
                str ( self.LineNr) + ' / ' + str ( Cycle_Nr ) + '</td>\n'
        self.LineNr += 1
        for i, Text in enumerate ( self.Texts ) :
          text = Text.strip()
          if not ( text ) :
            text = '<br>'
          line += '<td width=100 style="'
          line += 'background-color: #ddffdd;'
          line += '">'
          line += text
          line += '</td>\n'
        line += '</tr>\n'
        self.All_Lines.append ( line )

      fh = open ( Application.Dir + '/debug_table_template.html', 'r')
      lines = fh.read ()
      fh.close ()
      
      import datetime
      datum = datetime.date.today().strftime("%d-%m-%Y")
      lines = lines.replace ( 'datum', datum )

      lines = lines.replace ( '_protocol_', Active_Project_Filename )
      """
Active_Project_Inifile = None
Active_Project_Filename = ''
Active_Tree_Project = None
Active_Project_max_ID = -1
Active_Project_SubPath = 'pylab_works_programs'
"""
      info = ''.join ( self.All_Lines )
      lines = lines.replace ( 'xzxzxz', info )


      fh = open ( self.FileName + str(self.FileNum)+ '.html', 'w')
      lines = fh.write ( lines )
      fh.close ()

      #self.FileNum  +=1

    self._On     = True
    self.NBricks = NBricks
    try :
      if len(self.Texts) != self.NBricks :
        self.Texts     = self.NBricks * [ '' ]
        self.Changes   = self.NBricks * [ False ]
    except :
        self.Texts     = self.NBricks * [ '' ]
        self.Changes   = self.NBricks * [ False ]

    #self.All_Lines = ''
    #self.LineNr    = 1

  # **********************************************
  # **********************************************
  def _Create_Header ( self ) :
    line = '<tr valign=top>\n'
    line += '<td width=' + self._Colum_Width_0 + 'px '
    line += 'style="background-color: ' + self._Header_Color
    line += ';"><p><span class=rvts3>Line</span></p></td>\n'
    for Brick in Bricks :
      text = Brick.Caption + ' / ' + Brick.Name
      if not ( text ) :
        text='<br>'

      line += '<td width=100 style="'
      line += 'background-color: ' + self._Header_Color
      line += '"><p><span class=rvts3>'
      line += text
      line += '</span></p></td>\n'
    line += '</tr>\n'
    self.All_Lines.append ( line )

  # **********************************************
  # Writes information to the buffers / file
  # if Row == True,
  #   first the execute statement is sent to the file
  #   then the buffers are sent to the file
  #   and the buffers are cleared
  # It's safe to call this method at any time,
  # because it will just return if Debugging is Off
  # **********************************************
  def Write ( self, Brick_Nr, Msg = '', Row = False ) :
    if not ( self._On ) :
      return

    # on reaching the first Brick again,
    # create the output for one complete sequence
    #if Brick_Nr == 0 :
    if Row :
      N = ( Brick_Nr - 1 + self.NBricks ) % self.NBricks

      #
      if True in self.Changes :
        # Header
        if ( self.LineNr % self._Header_Repeat ) == 1 :
          self._Create_Header ()

        # First the Execute State
        line = '<tr valign=top>\n'
        line += '<td width=' + self._Colum_Width_0 + 'px >' +\
                str ( self.LineNr) + ' / ' + str ( Cycle_Nr ) + '</td>\n'
        self.LineNr += 1
        for i, Text in enumerate ( self.Texts ) :
          if i != self.Prev_Brick :
            text='<br>'
          else :
            text = Text.strip()
          line += '<td width=100 style="'
          if i == N :
            line += 'background-color: #ffaaaa;'
          line += '">'
          line += text
          line += '</td>\n'
        line += '</tr>\n'
        self.All_Lines.append ( line )

        # Header
        if ( self.LineNr % self._Header_Repeat ) == 1 :
          self._Create_Header ()

        # then the actions
        line = '<tr valign=top>\n'
        line += '<td width=' + self._Colum_Width_0 + 'px >' +\
                str ( self.LineNr) + ' / ' + str ( Cycle_Nr ) + '</td>\n'
        self.LineNr += 1
        for i, Text in enumerate ( self.Texts ) :
          text = Text.strip()
          if not ( text ) or ( i == self.Prev_Brick ):
            text='<br>'
          line += '<td width=100 style="'
          line += '">'
          line += text
          line += '</td>\n'
        line += '</tr>\n'
        self.All_Lines.append ( line )

      # clear all texts
      self.Changes  = self.NBricks * [ False ]
      self.Texts    = self.NBricks * [ '' ]
      self.Prev_Brick = Brick_Nr

    # if new text, set change flag
    if Msg :
      # limit the length of the message
      Msg = Msg [ : 150 ]
      
      # remove htlm tags:  < >
      Msg = Msg.replace ( '<', '&lt;' ).replace ( '>', '&gt;' )
      
      # if special start, highlight the first part
      if Msg.startswith ( '*-*' ):
        Msg = Msg [ 3 : ]
        i = Msg.find ( '=' )
        Msg = '<span class=rvts10>' + Msg [:i] + '</span>' +\
              Msg [i:]
        
      self.Changes [ Brick_Nr ] = True
      self.Texts   [ Brick_Nr ] += Msg + '<br>\n'
# ***********************************************************************
Debug_Table = tDebug_Table ()
# ***********************************************************************




# ***********************************************************************
# ***********************************************************************
def parse_list ( s, start = 0 ) :
  """
  parse a (nested) list into it's components
     line = " A  [  B  [ C+2 ] + 3 ] "
  will result in
     [' C+2 ', '  B  [ C+2 ] + 3 ', ' A  [  B  [ C+2 ] + 3 ] ']
  """
  x = []
  i = start
  while i < len ( s ) :
    c = s [ i ]
    if c == '[' :
      y, i = parse_list ( s, i + 1 )
      x = x + y
    if c == ']' :
      return x + [ s [ start : i ] ], i
    i += 1
  return x + [ s ]
# ***********************************************************************


# ***********************************************************************
from traceback import format_tb, format_exception_only
from sys import exc_info
from re import compile
from inspect import isbuiltin
from keyword import iskeyword

varsplitter = compile ( "[^0-9a-zA-Z_]" )
#varsplitter = compile ( "^0-9a-zA-Z_" )
def format_exception ( my_globals ):
  """
  Add a dump of any variables we can identify from the failing program
  line to the end of the traceback.  The deep mojo for doing this came
  from an example in the Zope core plus documentation in the Python
  Quick Reference.
  """

  def get_meta_data ( vstr, var ) :
    """
    Derive metadata of the variable, like len(), keys()
    """
    result = ''

    if isinstance ( var, dict ) :
      result += 'keys(' + vstr + ') = ' + str ( var.keys () ) + '\n        '

    elif type(var) in ( list, tuple ) :
      result += 'len(' + vstr + ') = ' + str ( len ( var ) ) + '   '
      
    result +=  vstr + ' = ' + str ( var ) + '\n'
    return result

  etype, value, tb = exc_info ()
  plaintb = format_tb ( tb )
  result  = [ 'Traceback (innermost last):\n' ]
  for line in plaintb:
    result.append ( '*****' + line )
    f      = tb.tb_frame
    tb     = tb.tb_next
    locals = f.f_locals
    print('*****',line,'\n    &&&&')

    # remove left part(s) of an assignment
    # [-2] is the code line, containing the error
    line = line.split ( '\n' ) [ -2 ]
    while '=' in line :
      line = line [ line.find ('=')+1 : ]

    # parse the rest of the line
    vars = varsplitter.split ( line )

    dvars = set ()
    self = None
    if 'self' in locals:
      self = locals [ 'self' ]

    # remove empties
    while '' in vars :
      vars.remove ( '' )

    #result.append ( 'PIEP33' + str ( vars ) + '\n' )
    #print 'PIEP33' + str ( vars ) + '\n'
    for i, v in enumerate ( vars ) :
      if v in dvars :
        continue
      dvars.add ( v )

      #print 'HHHYYTT', v
      
      if self and hasattr ( self, v ) :
        #print 'AAP1'
        result.append ( '      self:   %s: %r\n' % ( v, getattr ( self, v ) ) )

      elif v in locals:
        line = '      local:  '
        var = locals [v]
        line += get_meta_data ( v, var )
        result.append ( line )

      elif v in globals () :
        #print 'AAP3'
        result.append ( '      global: %s: %r\n' % ( v, globals () [v] ) )
      elif v in my_globals () :
        #print 'AAP4'
        result.append ( '      my_global: %s: %r\n' % ( v, my_globals () [v] ) )
      else :
        try :
          if eval ( 'isbuiltin ( "'+ v +'")' ) :
            pass # print 'BUILTIN',v
          elif eval ( 'iskeyword ( "'+ v +'")' ) :
            pass #print 'KeyWord',v
        except :
          pass

    #print 'PIEP44'+ str ( vars ) + '\n'

    """
    line = line.replace ( ' ', '' )
    parsed = parse_list ( line )
    result.append ( '\n***** ' + line )

    for elem in parsed :
      # we need to display the length of lists
      if elem.find ( '[' ) > 0 :
        i = 0
        splitted = []
        while '[' in elem [ i : ] :
          i = elem.find ( '[', i )
          splitted.append ( elem [ : i ] )
          LB = 1
          ii = i + 1
          # find belonging right bracket
          while ( ii < len ( elem ) ) and ( LB > 0 ):
            if elem [ii] == '[' :
              LB += 1
            elif elem [ii] == ']' :
              LB -= 1
            ii += 1
          splitted.append ( elem [ i : ii ] )
          if elem [ ii : ] :
            splitted.append ( elem [ ii : ] )
          i += ii + 1
        i = 1
        for item in splitted [ 2 : ] :
          if '[' in item :
            i += 1
        for ii in range ( i ) :
          item = ''.join ( splitted [ : ii+1 ] )
          result.append ( 'len(' + item + ')='+ str ( eval ( 'len(' + item + ')' ))+ ',  ', )

      if elem in locals:
        result.append ( elem + '=' + str ( eval ( elem ) ), globals, locals )
    """
  result.extend ( format_exception_only ( etype, value ) )
  return ''.join ( result )
# ***********************************************************************

# ***********************************************************************
# special debug printing procedure
# ***********************************************************************
def em ( line ):
  print(16 * 'E' + 'rror  ' + line)
  import traceback
  traceback.print_exc ()
  print('-------')
  """
  try :
    #traceback.print_exception ( ) #file = sys.stdout )
    #traceback.print_tb ()
    #traceback.print_last ()
    traceback.print_exc ()
    print '-------'
  except :
    print '+++++'
  """

# ***********************************************************************

# ***********************************************************************
# Write Brick Diagnostics
# ***********************************************************************
def wbd ( Brick, message ):
  # the if-statement might be overdone,
  # but it allows to use "wbd" without testing it self
  if ( not ( Brick ) or Brick.Diagnostic_Mode ) and ( len ( message ) > 0 ) :
    line = ''
    if Brick :
      line = 6 * '*' + ' ' + _(0,'WBD') + ': ('
      line += Brick.Name + ') = ' + Brick.Caption + ' : '
    line += message
    print(line)
# ***********************************************************************

# to see when it comes here:
pd_Module ( __file__ )
