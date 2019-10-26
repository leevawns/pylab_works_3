import os, sys
import platform

# ***********************************************************************
# Functions that give problems accross OSs
# Always use these functions instead of the orginals !!
# ***********************************************************************
def path_split ( filename ) :
  # under Ubuntu a filename with both
  # forward and backward slashes seems to give trouble
  # already in os.path.split
  if platform.system() == "Linux":
    filename = filename.replace ( '\\','/')

  return os.path.split ( filename )
# ***********************************************************************
#
# ***********************************************************************
def Joined_Paths ( *args ) :
  """
  Joins (if more than 1 argument) strings to one path.
  Normalizes the path.
  Changes the path to all forward slashes.
  Each subpath string is allowed to be terminated with a (back-) slash.
  """
  args = list ( args )
  for i,arg in enumerate ( args ) :
    args [i] = args[i].replace ( '\\', '/' )

  result = os.path.join ( *args )
  result = os.path.normpath ( result )
  result = result.replace ( '\\', '/' )
  return result
# ***********************************************************************
#
# ***********************************************************************
def Module_Absolute_Path ( *args ) :
  """
  Calculate an absolute filename or path,
  from arguments relative to the module.
  Example:
    My_File = Module_Absolute_Path ( '..', 'sounds', 'T53.txt' )
  will generate, the normalized form of :
    <modules path> / .. / sounds / T53.txt
  """
  # find from which file this function is called
  My_Path = sys._getframe(1).f_code.co_filename
  My_Path = os.path.split ( My_Path ) [0]
  My_File = os.path.join ( My_Path, *args )
  My_File = os.path.normpath ( My_File )
  return My_File