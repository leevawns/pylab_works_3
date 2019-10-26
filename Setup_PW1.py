#import __init__root
Kill_Distro       = False #True
MatPlotLib_Wanted = False #True

from   distutils.core import setup
import py2exe
import subprocess



import sys

# Only keep the first argument ( for the basepath )
sys.argv = [ sys.argv [0] ]
#print 'SSSWWWERT',sys.argv

#sys.stdout = stdout
#sys.stderr = stdout
#print sys.path
from file_support import *
import shutil
#import glob


# ***********************************************************************
# Some suggests that old build/dist should be cleared
# ***********************************************************************
#My_Path = os.path.split ( __file__ ) [0]
My_Path = sys._getframe().f_code.co_filename
My_Path = os.path.split ( My_Path ) [0]
Build_Path = os.path.join ( My_Path, 'build' )
Dist_Path  = 'D:\\Data_Python25_Dist' #os.path.join ( My_Path, 'dist'  )
if File_Exists  ( Build_Path ) :
  shutil.rmtree ( Build_Path )
if File_Exists  ( Dist_Path ) :
  shutil.rmtree ( Dist_Path )
# ***********************************************************************
Exe_Files    = []
Data_Dirs    = []
Data_Files   = []
Packages     = []
includes     = []
excludes     = []
dll_excludes = []


Exe_Files.append ( 'T53_main.py' )
Exe_Files.append ( 'support/gui_support.py' )
Exe_Files.append ( 'PyLab_Works/PyLab_Works.py' )

Data_Dirs.append ( 'chm_help' )
Data_Dirs.append ( 'data' )
Data_Dirs.append ( 'Lib_Extensions' )
Data_Dirs.append ( 'pictures' )
Data_Dirs.append ( 'PyLab_Works' )
Data_Dirs.append ( 'sounds' )
Data_Dirs.append ( 'support' )
Data_Dirs.append ( 'Templates' )

def Add_Data_Files ( subpath ) :
  global Data_Files
  for root, dirs, files in os.walk ( subpath ) :
    sampleList = []
    if files:
      for filename in files:
        if '.pyc' not in filename :
          sampleList.append ( os.path.join ( root, filename ))
    if sampleList:
      Data_Files.append (( root, sampleList ))

for SubPath in Data_Dirs :
  Add_Data_Files ( SubPath )
  
#Data_Files.append ( ( 'support', [ 'D:\\Data_Python_25\\support\\aap2.png' ] ) )

# Change back-slashes in forward-slashes
# if the filename contains forward-slashes,
# create a launch file

for i, file in enumerate ( Exe_Files ) :
  Exe_Files [i] = file.replace ( '\\', '/' )
  if '/' in Exe_Files [i] :
    path, filename = os.path.split    ( Exe_Files [i] )
    #name, ext      = os.path.splitext ( filename )

    print  Exe_Files[i].split('/')
    #My_File  = Module_Absolute_Path (  *Exe_Files[i].split('/')  )
    New_File = '_launch_' + filename

    fh = open ( New_File, 'w' )
    fh.write ( 'from General_Globals import Module_Absolute_Path\n' )

    # Add __main__ to dictionairy,
    # otherwise the main section will not be executed
    fh.write ( "My_File = '" + os.path.split (Exe_Files [i])[1] + "'\n" )
    fh.write ( 'Globs = {}\n' )
    fh.write ( "Globs [ '__name__' ] = '__main__'\n" )
    
    # Set the current working directory to the main file directory
    fh.write ( 'import os\n')
    fh.write ( "os.chdir('" + os.path.split ( Exe_Files[i] )[0] + "')\n" )

    fh.write ( 'execfile ( My_File, Globs )\n' )
    fh.close ()

    Exe_Files [i] = New_File

Exe_Files = [ 'PyLab_Works/PyLab_Works.py' ]

# ***********************************************************************
# ***********************************************************************
Data_Files.append ( ( '', glob.glob ( 'templates_*.*' ) ) )


# -----  2 june 2009  -----
includes.append ( 'control_scope_base' )

#   6 april 2008
#includes.append ( 'scipy.signal'     )
#includes.append ( 'scipy.__config__' )

#includes.append ( 'pygame.locals'    )

#includes.append ( 'numpy'            )



# If run without args, build executables, in quiet mode.
if len(sys.argv) == 1:
    sys.argv.append("py2exe")

#print Dist_Path
#print Exe_Files
#print Data_Files
#print Packages

#  console = ['PyLab_Works_mainform.py']  ,
if True :
  Options = {
       'py2exe' : {
          'dist_dir'     : Dist_Path,
          'optimize'     : 0,
          'compressed'   : False,
          'skip_archive' : True,
          #'force_imports': True,
          'includes'     : includes,
          'excludes'     : excludes,
          'dll_excludes' : dll_excludes,
          'packages'     : Packages
       }}
  #print Options
  try:
    setup (
      windows    = Exe_Files,
      data_files = Data_Files,
      options    = Options,
        )
  except :
    import traceback
    traceback.print_exc ()
    print 'Setup Failed'

print 'Remove Build directory'
if File_Exists  ( Build_Path ) :
  shutil.rmtree ( Build_Path )

# TestRun
for File in Exe_Files :
  Executable = Change_FileExt ( File, 'exe' )
  Executable = os.path.split ( Executable ) [1]
  Executable = Joined_Paths ( Dist_Path, Executable )
  print Executable
  result = subprocess.call ( [ Executable ] )
  print 'BUILD Windows',Executable, result==0, result


print 'Starting INNO setup'
"""
result = subprocess.call (
  [ 'P:\Program Files\Inno Setup 4\ISCC.exe',
    'D:\Data_Python_25\PyLab_Works\PyLab_Works.iss'])
print 'BUILD Windows',result==0, result

if (result==0) and Kill_Distro :
  for path in dist_paths :
    if File_Exists ( path ) :
      shutil.rmtree ( path )
  print 'piep'
"""