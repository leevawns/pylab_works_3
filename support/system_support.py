import __init__

# ***********************************************************************
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007..2008 Stef Mientki
# mailto:S.Mientki@ru.nl
# ***********************************************************************

# ***********************************************************************
__doc__ = """
"""
# ***********************************************************************


# ***********************************************************************
_Version_Text = [
[ 1.4 , '09-01-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Beep function added
""" ] ,

[ 1.3 , '07-10-2008', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Run_Python added (much simpeler than Run )
- Run_Python_NoWait, set shell different for Windows and Linux
""" ] ,

[ 1.2 , '20-08-2008', 'Stef Mientki',
'Test Conditions:', (1,),
"""
- GetProcessID didn't always return a value
- Kill_Process now return True if succeeded
""" ] ,

[ 1.1 , '15-02-2008', 'Stef Mientki',
'Test Conditions:', (1,),
"""
- GetAllProcesses was static, now made dynamic
""" ] ,

[ 1.0 , '28-12-2007', 'Stef Mientki',
'Test Conditions:', (1,),
' - orginal release' ]
]
# ***********************************************************************




from General_Globals import *
import os
import time
"""
import win32api, win32pdhutil, win32con
import win32pdh, string
"""
import pygame
from pygame.locals import *




# ***********************************************************************
# ***********************************************************************
def Beep ( ID = None ) :
  """
  generates an independant message beep,
  by playing a wave file.
  """
  # DONT CHANGE THE ORDER, JUST APPEND SOUND FILES
  Sounds = [
    'Windows XP Error.wav',        # 0
  ]

  if not ( ID ) or ( ID >= len ( Sounds ) ) :
    ID = 0
  #filename = 'D:/Data_Python_25/sounds/Windows XP Error.wav'
  filename = '../sounds/' + Sounds [ ID ]

  #print ( 'Beep:', filename )
  pygame.mixer.init ()
  soundfile = pygame.mixer.Sound ( filename )
  soundfile.play ()
# ***********************************************************************



"""
Explorer [/n] [/e] [(,)/root,<object>] [/select,<object>]

/n                Opens a new single-pane window for the default
                  selection. This is usually the root of the drive Windows
                   is installed on. If the window is already open, a
                  duplicate opens.

/e                Opens Windows Explorer in its default view.

/root,<object>    Opens a window view of the specified object.


/select,<object>  Opens a window view with the specified folder, file or
                  application selected.

Examples:

   Example 1:     Explorer /select,C:\TestDir\TestApp.exe

      Opens a window view with TestApp selected.

   Example 2:  Explorer /e,/root,C:\TestDir\TestApp.exe

      This opens Explorer with C: expanded and TestApp selected.

   Example 3:  Explorer /root,\\TestSvr\TestShare

      Opens a window view of the specified share.

   Example 4:  Explorer /root,\\TestSvr\TestShare,select,TestApp.exe

      Opens a window view of the specified share with TestApp selected.
"""
# ***********************************************************************
# ***********************************************************************
def GetAllProcesses():
  if os.name != 'nt' :
    pass
  else:
    # THIS IS STATIC !!
    #import win32pdh
    #object = "Process"
    #items, instances = win32pdh.EnumObjectItems(None,None,object, win32pdh.PERF_DETAIL_WIZARD)

    #import sys
    #sys.path.append ('wmi_test')
    import wmi
    w = wmi.WMI()
    processes = w.instances('Win32_Process')
    instances = []
    for process in processes :
      instances.append ( str(process.name) )

    return instances
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def GetProcessID ( name ) :
  if os.name != 'nt' :
    return None
  else:
    import win32pdh
    import time
    object = "Process"
    items, instances = win32pdh.EnumObjectItems(None,None,object, win32pdh.PERF_DETAIL_WIZARD)

    val = None
    if name in instances :
      hq = win32pdh.OpenQuery()
      hcs = []
      item = "ID Process"
      path = win32pdh.MakeCounterPath( (None,object,name, None, 0, item) )
      hcs.append(win32pdh.AddCounter(hq, path))
      win32pdh.CollectQueryData(hq)
      time.sleep(0.01)
      win32pdh.CollectQueryData(hq)

      for hc in hcs:
        type, val = win32pdh.GetFormattedCounterValue(hc, win32pdh.PDH_FMT_LONG)
        win32pdh.RemoveCounter(hc)
      win32pdh.CloseQuery(hq)
    return val
# ***********************************************************************


"""
#THIS IS SLOW !!
def Kill_Process2 ( process ) :
  #get process id's for the given process name
  pids = win32pdhutil.FindPerformanceAttributesByName ( process )
  for p in pids:
    handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, p) #get process handle
    win32api.TerminateProcess(handle,0) #kill by handle
    win32api.CloseHandle(handle)        #close api
"""


# ***********************************************************************
# ***********************************************************************
def Kill_Process_pid ( pid ) :
  if os.name != 'nt' :
    pass
  else:
    import win32api
    import win32con
    handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, 0, pid) #get process handle
    try:
      win32api.TerminateProcess(handle,0) #kill by handle
      win32api.CloseHandle(handle)        #close api
    except:   #the process might already be closed by the user
      pass
# ***********************************************************************


# ***********************************************************************
# A short wait might be necessary to prevent
#getting the pid of the just killed process
##    while Kill_Process ( 'cmd' ) :
##      time.sleep ( 0.1 )
# ***********************************************************************
def Kill_Process ( name ) :
  if os.name != 'nt' :
    return False
  else:
    try:
      pid = GetProcessID ( name )
      #print 'pid',pid
      if pid:
        Kill_Process_pid ( pid )
        return True
      else :
        return False
    except:  #the process might already be closed by the user
      return False
# ***********************************************************************


# ***********************************************************************
# if Name is given try to kill process by pid
# afterwards always try to kill by name
# ***********************************************************************
def Kill_Process_pid_Name ( pid, name ) :
  if os.name != 'nt' :
    pass
  else:
    if pid :
      Kill_Process_pid ( pid )
    # now if the process is started outside this program
    # we kill it this way
    #   which doesn't always succeed !!
    #   especially in the following case
    #     - launched by this program
    #     - killed by user
    #     - launched by user
    Kill_Process ( file )
# ***********************************************************************



# ***********************************************************************
# Convert Relative path/url to Absolute path/url
# all the os/urllib/urlparse procedures seems a bit clumsy
# The following recipy seems to work for file and url
# ***********************************************************************
def Make_Absolute_Path ( path, file ) :
  import  urllib.parse
  # be sure all forward slashes to het urlparse work correctly
  path = path.replace('\\','/')
  file = file.replace('\\','/')
  # if a path on local disk, add "file:///" to let urljoin work ok
  if ( len ( path ) > 2 ) and ( path[1] == ':' ) :
    abs_path = urllib.parse.urljoin( 'file:///' + path, file)
  else :
    abs_path = urllib.parse.urljoin( path, file )
  # if file, remove the "file:///" again
  if abs_path.find ('file:///') == 0 :
    abs_path = abs_path [8:]
    #abs_path = abs_path.replace('/','\\')
  return abs_path
# ***********************************************************************


# ***********************************************************************
# Example:
#   line = Make_Links_Absolute ( line, 'href=', prim_path )
# where:
#   line = html string with possible relative paths on the tag 'href='
#   tag = 'href=', 'src=' or whatever you like
#   prim_path = 'D:\data\test.html', yes it should contain a filename
#               or last backslash ?
# ***********************************************************************
def Make_Links_Absolute ( line, tag, prim_path ) :
  # find all the reference links
  i = 0
  links = []
  N = len(tag) + 1
  while i >= 0 :
    i = line.find ( tag, i+1 )
    if i >= 0 :
      links.append ( i + N )

  # now replace them in reversed order (to keep the indexes correct
  N = len ( links )
  for i in range ( N ) :
    ii = N-i-1
    w = line.find ( '"', links[ii] )
    file = line [ links[ii] : w ]
    abs_path = Make_Absolute_Path ( prim_path, file)
    line = line.replace ( file, abs_path )
    #print prim_path, '|', file, '|', abs_path
    #print 'HREF',line

  return line
# ***********************************************************************



import subprocess
# requires Python 2.4 or higher


# ***********************************************************************
# ***********************************************************************
def _PreProcess_Run_Python ( arguments, cwd = None ) :
  """
  INTERNAL: Runs a Python script.
  "Arguments" starts with the script, followed by the commandline arguments.
  "Arguments" maybe of type string, tuple, list.
  The Python executable should NOT be in the argument list.
  If the script is started from another directory,
  cwd is automatically calcuated.
  Examples:
    Run_Python ( [ 'PyLab_Works.py', 'aap' ] )
    Run_Python ( '../support/multi_language.py' )
  """
  # be sure arguments is of type list
  if not ( isinstance ( arguments, list ) ) :
    if isinstance ( arguments, tuple ) :
      arguments = list ( arguments )
    else :
      arguments = [ arguments ]

  # add "Python" to the beginning of the list
  arguments.insert ( 0, 'python' )

  # if the Current Working Directory cwd is not specified
  # try to set cwd to the path of the first argument
  if not ( cwd ) :
    cwd = path_split ( arguments [1] )[0]
    # if path is an empty string, we must make it None !!
    if not ( cwd ) :
      cwd = None

  return arguments, cwd
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def Run_Python ( arguments, cwd = None ) :
  """
  Runs a Python script and doesn't wait.
  "Arguments" starts with the script, followed by the commandline arguments.
  "Arguments" maybe of type string, tuple, list.
  The Python executable should NOT be in the argument list.
  If the script is started from another directory,
  cwd is automatically calcuated.
  Examples:
    Run_Python ( [ 'PyLab_Works.py', 'aap' ] )
    Run_Python ( '../support/multi_language.py' )
  """
  arguments, cwd = _PreProcess_Run_Python ( arguments, cwd )
  print ( '[[[]]]', arguments, cwd )
  return subprocess.Popen ( arguments,
                            cwd   = cwd ,
                            shell =  ( os.name == 'nt') )

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Run_Python_NoWait ( arguments, cwd = None, stdOUT = None ) :
  """
  Runs a Python script and doesn't wait.
  "Arguments" starts with the script, followed by the commandline arguments.
  "Arguments" maybe of type string, tuple, list.
  The Python executable should NOT be in the argument list.
  If the script is started from another directory,
  cwd is automatically calcuated.
  Examples:
    Run_Python_NoWait ( [ 'PyLab_Works.py', 'aap' ] )
    Run_Python_NoWait ( '../support/multi_language.py' )
  """
  arguments, cwd = _PreProcess_Run_Python ( arguments, cwd )

  # For Windows shell must be True,
  # For Ubuntu, shell must be False
  try :
    PID = subprocess.Popen( arguments,
                          cwd   = cwd ,
                          stdout = subprocess.PIPE,
                          stderr = subprocess.PIPE,
                          shell =  ( os.name == 'nt') )
  except :
    print ('***** ERROR in Run_Python_NoWait ******')
    print ('      arguments  = ', arguments)
  return PID

# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
def Run(filename, cwd=None, show='normal', priority=2, bufsize=0, \
        executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None,\
        close_fds=False, shell=False, env=None, universal_newlines=False, \
        startupinfo=None, creationflags=0):
  #IDLE_PRIORITY         0x00000040 ok
  #BELOW_NORMAL_PRIORITY 0x00004000 ok
  #NORMAL_PRIORITY       0x00000020 ok
  #ABOVE_NORMAL_PRIORITY 0x00008000 ok
  #HIGH_PRIORITY         0x00000080 ok
  #REALTIME_PRIORITY     0x00000100 ok
  #Global Const SW_HIDE = 0
  #Global Const SW_SHOWNORMAL = 1
  #Global Const SW_SHOWMINIMIZED = 2
  #lobal Const SW_SHOWMAXIMIZED = 3
  #if type(show) == basestring:
  if isinstance ( show, str ) :
    window_state = {"hide":0, "normal":1, "minimized":2,"maximized":3,\
                    "hidden":0,"minimize":2,"maximize":3}
    show = window_state[show]
  if show != 1:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = show
  if cwd == "":
    cwd = None
  process_priority =[ 0x40,0x00004000,0x00000020,0x00008000,0x00000080,0x00000100]
  #Run ( "filename" [, "workingdir" [, flag[, standard_i/o_flag]]] )
  return subprocess.Popen(filename, bufsize, executable, stdin, stdout, stderr,\
                          preexec_fn, close_fds, shell, cwd, env,\
                          universal_newlines, startupinfo, \
                          creationflags=(process_priority[priority]|creationflags))
  #subprocess.Popen( filename, shell=shell, cwd=workingdir, creationflags=process_priority[priority], startupinfo=startupinfo)
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
#def RunWait(filename, workingdir=None,show="normal", priority=2, shell=False, env=None, startupinfo=None, creationflags=None ):
def RunWait(filename, cwd=None, show='normal', priority=2, bufsize=0, \
        executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None,\
        close_fds=False, shell=False, env=None, universal_newlines=False, \
        startupinfo=None, creationflags=0):
  #if type(show) == basestring:
  if isinstance ( show, str ) :
    window_state = {"hide":0, "normal":1, "minimized":2,"maximized":3,\
                    "hidden":0,"minimize":2,"maximize":3}
    show = window_state[show]
  if show != 1:
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = show
  if cwd == "":
    cwd = None
  process_priority =[ 0x40,0x00004000,0x00000020,0x00008000,0x00000080,0x00000100]
  return subprocess.call(filename, bufsize, executable, stdin, stdout, stderr,\
                          preexec_fn, close_fds, shell, cwd, env,\
                          universal_newlines, startupinfo, \
                          creationflags=(process_priority[priority]|creationflags))
  #subprocess.call( filename, shell=shell, cwd=workingdir, creationflags=process_priority[priority], startupinfo=startupinfo)

runwait = Runwait = RunWait
run = Run

# ***********************************************************************
##def run(filename, workingdir=None,show="normal", priority=2, shell=False, env=None, startupinfo=None, creationflags=None ):
##  print "use Run, you are using a badly named routine",filename
##  Run(filename, workingdir,show, priority, shell, env, startupinfo, creationflags )
##def runwait(filename, workingdir=None,show="normal", priority=2, shell=False, env=None, startupinfo=None, creationflags=None ):
##  print "use RunWait, you are using a badly named routine",filename
##  RunWait(filename, workingdir,show, priority, shell, env, startupinfo, creationflags )
##def Runwait(filename, workingdir=None,show="normal", priority=2, shell=False, env=None, startupinfo=None, creationflags=None ):
##  print "use RunWait, you are using a badly named routine",filename
##  RunWait(filename, workingdir,show, priority, shell, env, startupinfo, creationflags )
# ***********************************************************************
def setpriority(pid=None,priority=1):
    """ Set The Priority of a Windows Process.  Priority is a value between 0-5 where
        2 is normal priority.  Default sets the priority of the current
        python process but can take any valid process ID. """

    import win32api,win32process,win32con

    priorityclasses = [win32process.IDLE_PRIORITY_CLASS,
                       win32process.BELOW_NORMAL_PRIORITY_CLASS,
                       win32process.NORMAL_PRIORITY_CLASS,
                       win32process.ABOVE_NORMAL_PRIORITY_CLASS,
                       win32process.HIGH_PRIORITY_CLASS,
                       win32process.REALTIME_PRIORITY_CLASS]
    if pid == None:
        pid = win32api.GetCurrentProcessId()
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, pid)
    win32process.SetPriorityClass(handle, priorityclasses[priority])


#run(["notepad.exe"],"","minimized",priority=5)
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
def test_back () :
  Source_File = sys._getframe(1).f_code.co_filename

  # PROBABLY BETTER
  Frame = 1
  while Source_File == '<string>' :
    print ('FRAME UP +++', text)
    Frame += 1
    Source_File = sys._getframe( Frame ).f_code.co_filename

  print ('Source_File', Source_File)

  Source_Path, Source_File = path_split ( Source_File )
  Source_File = os.path.splitext ( Source_File )[0]
  print ('Source_Path', Source_Path)
  print ('Source_File', Source_File)
  Language_File = os.path.join ( Source_Path, 'lang', Source_File + '_NL.py' )
  print ('Language_File', Language_File)
  from file_support import File_Exists
  print (File_Exists ( Language_File ))
  sys.path.append ( os.path.join ( Source_Path, 'lang' ))
  print ('sys.path:')
  import test_syspath_NL
  for item in sys.path :
    print ('  ', item)

  if File_Exists ( Language_File ) :
    Language_File = os.path.splitext ( Language_File ) [0]
    line = 'from ' + Source_File + '_NL' + ' import LT'
    print ('exec:', line)
    try :
      exec ( line )
      print ('LT',LT)
    except :
      print ('Error importing Language File', Language_File)



# ***********************************************************************
# ***********************************************************************
if __name__ == "__main__":

  Test_Defs ( 10 )

  if Test ( 1 ) :
    # ************************************
    # test of Process
    # ************************************
    import subprocess
    pipe = subprocess.Popen('D:/Data_Lego/D7_uploader_programmer/UPD.exe')
    #time.sleep(5)
    print ('PID',pipe.pid)

    a = GetAllProcesses()
    print (a)

    process = 'UPD'
    Kill_Process ( process )

  if Test ( 2 ) :
    for i in range ( 1 ) :
      time.sleep(2)
      a = GetAllProcesses()
      print (a)

  if Test ( 3 ) :
    # ************************************
    # test of Make_Absolute_path
    # ************************************
    file = '../aap.html'
    path = 'http://stef/het/new/oud/pylab_works_demo_graph_calculator.html'
    print (Make_Absolute_Path ( path, file ))
    path = 'file:///d:/stef/het/new/oud/pylab_works_demo_graph_calculator.html'
    print (Make_Absolute_Path ( path, file ))
    path = 'd:/stef/het/new/oud/pylab_works_demo_graph_calculator.html'
    print (Make_Absolute_Path ( path, file ))

    file = 'd:/beer/aap.html'
    path = 'http://stef/het/new/oud/pylab_works_demo_graph_calculator.html'
    print (Make_Absolute_Path ( path, file ))
    path = 'file:///d:/stef/het/new/oud/pylab_works_demo_graph_calculator.html'
    print (Make_Absolute_Path ( path, file ))
    path = 'd:/stef/het/new/oud/pylab_works_demo_graph_calculator.html'
    print (Make_Absolute_Path ( path, file ))

    path = 'D:\DATA_actueel\Stef'
    file = 'test_wxp_img1.gif'
    print (Make_Absolute_Path ( path, file ))
    # | file:///test_wxp_img1.gif

    path = 'D:\data_www\pylab_works'
    file = 'pw_animations_screenshots_img5.png'
    print (Make_Absolute_Path ( path, file ))
    # | D:\data_www\pw_animations_screenshots_img5.png

  if Test ( 4 ) :
    import subprocess
    subprocess.Popen ( [ 'python', 'file_support.py' ] )
    #run( ["tree_support.py"], shell =  ( os.name == 'nt') )

    #run( ["notepad.exe", "test.txt"] )

    Run_Python ( '../support/file_support.py' )

    """
    run ( [ 'Python', '../PyLab_Works/PyLab_Works.py',
            'aap' ],
          cwd = '../PyLab_Works/',
          shell =  ( os.name == 'nt') )
    """

  if Test ( 5 )  :
    import wmi
    w = wmi.WMI ()
    for process in w.Win32_Process ( caption = "cmd.exe" ) : #caption="notepad.exe"):
      print (process)

  if Test ( 6 ) :
     print (RunWait ( "cmd.exe", cwd=None, show='normal', priority=2, bufsize=0, \
        executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None,\
        close_fds=False, shell =  ( os.name == 'nt'), env=None, universal_newlines=False, \
        startupinfo=None, creationflags=0))

  if Test ( 7  ) :
    run ( [ 'Python', 'P:/Python/Lib/site-packages/winpdb-1.3.8/winpdb.py',
            'test_IDE.py' ],
          cwd = '../PyLab_Works/',
          shell =  ( os.name == 'nt') )
  if Test ( 8 ) :
    run ( [ 'Python', 'P:/Python/Lib/site-packages/winpdb-1.3.8/winpdb.py',
            'D:/Data_Python_25/PyLab_Works/test_IDE.py' ],
          shell =  ( os.name == 'nt') )

  if Test ( 9 ) :
    print ('sys.path:')
    for item in sys.path :
      print ('  ', item)
    print ('sys.path[0] = path of the main application file ', sys.path[0])
    print ('os.getcwd()', os.getcwd ())
    print ('__file__', __file__)

    #sys.path.append ( '../PyLab_Works' )
    from test_syspath import test
    test ()

  if Test ( 10 ) :
    beep ()
# ***********************************************************************
pd_Module ( __file__ )

