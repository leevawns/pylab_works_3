import __init__root
import os, sys
from file_support    import File_Delete, Find_Files
from General_Globals import Joined_Paths, v3print

# Get my path
Path = sys._getframe().f_code.co_filename
Path = os.path.split ( Path ) [0]


# ***********************************************************************
# ***********************************************************************
def Remove_pyx_Files () :
  """
  Removes all pyc,pyo files
  from this path and all it's subpaths.
  """

  v3print ( '\n***** PYC Files *****', Path )
  PYC = Find_Files ( Path, '*.pyc' )
  for file in PYC :
    filename = Joined_Paths ( Path + file[0], file[1] + '.pyc' )
    v3print ( filename )
    File_Delete ( filename )

  v3print ( '\n***** PYO Files *****' )
  PYO = Find_Files ( Path, '*.pyo' )
  for file in PYO :
    filename = Joined_Paths ( Path + file[0], file[1] + '.pyc' )
    v3print ( filename )
    File_Delete ( filename )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Garantee_Init () :
  from shutil import copyfile
  v3print ( '\n***** Copy __init__.py to All *****' )

  Excludes = ( 'chm_help', 'lang', 'setup_dummy', 'html',
               'pylab_works_programs', 'pylab_works_programs_original',
               'Installs', 'data', 'bricks', 'controls' )


  Source = os.path.join ( Path, '__init__.py' )

  for root, dirs, files in os.walk ( Path ) :
    if dirs :
      for dir in dirs :
        if ( dir not in Excludes ) and \
           ( root.find ( 'pylab_works_programs') < 0 ):
          Dest = os.path.join ( root, dir, '__init__.py' )
          copyfile ( Source, Dest )
          #v3print  ( 'Copy __init__.py to:', root, dir )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
if __name__ == "__main__":
  Remove_pyx_Files ()

  Garantee_Init ()
  
  File_Delete ( os.path.join ( Path, 'PyLab_Works',
                'language_support_error_log.txt' ))
                
  File_Delete ( os.path.join ( Path, 'PyLab_Works',
                'PyLab_Works_Overview_debug.txt' ))

  File_Delete ( os.path.join ( Path, 'PyLab_Works',
                'test_debug_*.html' ))