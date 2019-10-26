import os, sys

# ***********************************************************************
# Searches for all Paths, starting at path
# returns a sorted list of full path names
# ***********************************************************************
def Find_Paths ( path, Py_Paths ) :
  files = os.listdir ( path )
  for file in files :
    new_path = os.path.join ( path, file )
    if os.path.isdir ( new_path ) and \
       ( file != '.svn' ) :              # don't touch svn paths
      Py_Paths.append ( new_path )
      Find_Paths ( new_path, Py_Paths )
  Py_Paths.sort()
# ***********************************************************************


# ***********************************************************************
# extend the system path with ALL paths in the project
# ***********************************************************************
Py_Paths = []
Path = sys._getframe().f_code.co_filename
Path = os.path.split ( Path ) [0]

# Add myself
if not ( Path in sys.path ) :
  sys.path.append ( Path )

Find_Paths ( Path, Py_Paths )
for path in Py_Paths :
  if not ( path in sys.path ) :
    sys.path.append ( path )
# ***********************************************************************

