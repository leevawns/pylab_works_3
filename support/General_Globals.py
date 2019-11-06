import __init__

# ***********************************************************************
# This lowest level library should not import language support !!
# So it also can't use translated doc-strings
# ***********************************************************************
__doc__ = """
This is very low level module,
to support several basic settings and debug features.
Every PyLab_Works module should import this module as the first import
in general even before the language translation module.
(Sorry, because it's low level, this string can't be translated.)
"""
# ***********************************************************************

import os, sys
import platform
import time

from path_support import *
#check platform windows: true or false
Platform_Windows = sys.platform == "win32"

# ***********************************************************************
# Delay used for wx.CallLater
# ***********************************************************************
wxGUI_Delay = 100
if not ( Platform_Windows ) :
  wxGUI_Delay = 500
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def What_DO_I_Call ( Thing, Limit_Lines = None ) :
  import inspect
  SL = inspect.getsourcelines ( Thing )
  print ( 'Thing = ', Thing.__name__, '\n',
            '  File =', inspect.getmodule ( Thing ), '\n',
            '  Line Number =', SL[1] )
  for line in SL[0] [ : Limit_Lines ] :
    print ( line.rstrip() )
# ***********************************************************************

# ***********************************************************************
# WHAT TO DEBUG ( if Debug flag on )
# Just (un-)comment the following lines
# ***********************************************************************
Debug_What = set ()
Debug_What.add ( 'Load_Save' )
Debug_What.add ( 'TIO-Read' )
Debug_What.add ( 'TIO-Write' )
# ***********************************************************************
# And in the following lines, just change the number
# if necessary
# At the moment we allow:
#   0 = not deep
#   1 = deeper
#   2 = deepest
# ***********************************************************************
Debug_How_Deep = {}
Debug_How_Deep [ 'TIO_Read' ] = 2
Debug_How_Deep [ 'Brick' ] = 2
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def Debug_Dump ( *args ) :
  from inifile_support import inifile
  
  Pre   = '\n++ '
  After = ' '
  line = ''
  for item in args :
    if isinstance ( item, inifile ) :
      line += item.Filename
    else :
      line += item.__str__()
    line += After
  line = line.replace ( '\n','\n    ')

  line = Pre + line
  print(line)
# ***********************************************************************
# ***********************************************************************
def Debug_Dump_Trace ( *args ) :
  print("\n[Debug_Dump_Trace]")
  Debug_Dump ( *args )
  Debug_From ( 3 )
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def Debug_From ( Level = 2 ) :
  print("[ Debug_From ]")
  """
  Display information about the CALLER
  """
  NDeep = 10
  My_Dir = path_split ( Application.Dir ) [0]
  My_File = False
  #Level = 1 #4
  pre = '   '
  while not ( My_File ) and ( Level < 20 ):
    try:
      F = sys._getframe ( Level )
      path, filename = path_split ( F.f_code.co_filename )
      if path.startswith ( My_Dir ) :
        for i in range ( NDeep ) :
          #'%5d' %( int(value) )
          print(pre + 'Called from : %5d,' %(F.f_lineno), filename)

          # Stop when top level of the application found
          if filename == Application.FileName :
            break

          Level += 1
          #pre += '  '
          F = sys._getframe ( Level )
          filename = path_split ( F.f_code.co_filename )[1]
        return

      Level += 1
    except :
      return
  print("  **** Debug, can't find CALLER, level =", Level)
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def exprint ( *args ) :
  """
  Print procedure with Traceback.
  """
  for arg in args :
    print(arg,)
  print
  print ('____________ Print Traceback ____________')
  Debug_From ()
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class Application_Object ( object ) :
  def __init__ ( self ) :
    """
    -debug
    -debugfile
    -debugtable
    -demo
    -design
    -editflags,    Let the user edit the flags + clipboard copy,
                   Not yet implemented
    -original
    -TestRun
    -testall
    -testxxx,      where xxx is series of digits
    -vmdelayxxxx,  where xxxx is delay in msec
    -wx_inspect
    """
    #print("[INFO OF APPLICATION OBJECT]")
    self.Application = sys.argv[0]
    #print("[Name of .py file import general_globals] : ",self.Application)
    self.Dir = os.getcwd ()
    #print("Dir : ", self.Dir)
    self.FileName = path_split ( self.Application ) [1]
    self.FileName_Only, ext = os.path.splitext ( self.FileName )
    self.Config_File = None

    # Set some global debug vars
    # _pd : flag debug: true or false
    # _pd_nr : debug number, int
    # _pd_pd_pre : '--' signal debug,string
    # _pd_FileName : path debug file : string, .../FileName_debug.txt
    # _pd_flags : sys.argv
    # _pd_file : flag debugfile, true or false
    # _pd_testall : flag debug all, true or false
    global _pd, _pd_nr, _pd_pd_pre, _pd_FileName, _pd_flags, _pd_file, _pd_testall
    _pd_nr = 0
    print('********************** ALARM ***********************')
    print('************** create Application object *************')
    _pd_FileName = os.path.join ( self.Dir, self.FileName_Only + '_debug.txt')
    
    # determine the commandline flags
    _pd_pd_pre = '-- '
    _pd_flags = sys.argv
    _pd =         ( '-debug'     in sys.argv [ 1 : ] ) or ( '-debugfile' in sys.argv [ 1 : ] )
    _pd_file =    ( '-debugfile' in sys.argv [ 1 : ] )
    
    _pd_testall = ( '-testall'   in sys.argv [ 1 : ] ) 
    # Find the numeric flags
    self.VM_Delay = 19 / 1000.0    #normally 50 fps
    for arg in sys.argv [ 1 : ] :
      # find strings ala "-test127"
      if arg.startswith ( '-test' ) and ( arg [ 5 : ].isdigit ) :
        tests = []
        for digit in arg [ 5 : ] :
          tests.append ( int ( digit ) )
        Test_Defs ( tests )
      elif arg.startswith ( '-vmdelay' ) and ( arg [ 8 : ].isdigit ) :
        self.VM_Delay = int ( arg [ 8: ] ) / 1000.0

    # Get the config file
    for arg in sys.argv [ 1 : ] :
      if arg[0] != '-' :
        self.Config_File = arg
        break

    self.Debug_Mode      = _pd
    self.Demo_Mode       = '-demo'       in sys.argv [ 1 : ]
    self.Debug_Table     = '-debugtable' in sys.argv [ 1 : ]
    self.Orgininal       = '-original'   in sys.argv [ 1 : ]
    self.WX_Inspect_Mode = '-wx_inspect' in sys.argv [ 1 : ]
    self.Design_Mode     = '-design'     in sys.argv [ 1 : ]

    # special: Uppercase characters !!
    # This parameter is intended for automatic test runs
    self.TestRun = '-TestRun' in sys.argv [ 1 : ]

    self.Restart = False
# ***********************************************************************

# ***********************************************************************
# Create the application Object
Application = Application_Object ()
# ***********************************************************************
Application._VPython_Version = 5
# ***********************************************************************
# ***********************************************************************
_GG_Test_Defs = []
_GG_Start_Time = None
# ***********************************************************************
def Test_Defs ( *args ) :
  global _GG_Test_Defs, _GG_Start_Time
  for arg in args :
    _GG_Test_Defs.append ( arg )
  _GG_Start_Time = time.time()
# ***********************************************************************
def Test ( *args ) :
  global _GG_Test_Defs, _pd_testall
  if _pd_testall :
    print ( '***** Test ', args, '*****' )
    return True
  for arg in args :
    if arg in _GG_Test_Defs :
      print ( '***** Test ', args, '*****' )
      return True
  else :
    return False
# ***********************************************************************
def Test_Time () :
  """
  Can be used to print the elapsed timer after all tests have run
  """
  print ( '==> Elapsed Time [s] =', int ( time.time() - _GG_Start_Time ) )
# ***********************************************************************
def _pd_pre () :
  global _pd_nr
  _pd_nr += 1
  return _pd_pd_pre + str ( _pd_nr ) + ': '
# ***********************************************************************
def pd ( line_user )  :
  line_user = _pd_pre() + line_user
  if _pd:
    if _pd_file :
      if _pd_nr == 1 :
        from datetime import date
        import os
        print(sys.argv[0])
        print(os.path.basename(sys.argv[0]))

        line = '\n' + 80 * '*' + '\n'
        line += str ( date.today () )
        line += '  OS: ' + os.name + ' / ' + sys.platform
        line += '\nPython: ' + sys.version
        line += '\n' + 'Command Line: ' + str ( sys.argv [ 1 : ] )

        fh = open ( _pd_FileName, 'a' )
        fh.write ( line  + '\n')
        fh.close ()

      # now write the normal information
      fh = open ( _pd_FileName, 'a' )
      fh.write ( line_user + '\n')
      fh.close ()
    print(line_user)
    
    """
    for Path in sys.path :
      if not ( Path.startswith ( 'P:') ) :
        print Path
    """
# ***********************************************************************
def pd_Module ( line = None ):
  """
  This procedure will print the imported module, if debug mode is on.
  Usage, at the bottom of each module, place the following line:
    pd_Module ( __file__ )

  Or for standard library files, for which you're interested, e.g. numpy
    import numpy
    pd_Module ( 'Numpy' )
    
  For modules launched with execfile, "__file__" doesn't exist,
  so you'll get an error message when the program closes.
  Therefor it's also allowed to use the function without parameter
    pd_Module ()
  In which case the procedure will evaluate the filename.
  Unfortunately in the latter case you can't see if the 'py' file
  or the 'pyc'-file is loaded.
  """
  if not ( line ) :
    line = sys._getframe(1).f_code.co_filename
  pd ( 'Imported : ' + os.path.normpath ( line ) )
# ***********************************************************************

# ***********************************************************************
# At this moment we may call other libraries of our own
# so here we can extend our Application object
# ***********************************************************************
# Get the General Inifile
from inifile_support import inifile

Path = sys._getframe().f_code.co_filename
Path = os.path.split ( Path ) [0]

filnam = os.path.join ( Path, 'General_Global_Settings.cfg' )
Application.General_Global_Settings = inifile ( filnam )
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
if __name__ == '__main__':
    #test()
    pass
# ***********************************************************************

pd_Module ( __file__ )
