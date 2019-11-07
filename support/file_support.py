import __init__

"""
General purpose file / directory handling procedures
"""


from General_Globals import *
from language_support import _
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
_Version_Text = [

[ 1.3, '29-04-2009', 'Stef Mientki',
'Test Conditions:', (2,) ,
"""
- Get_Relative_Path and Get_Rel_Path required that the file existed, not anymore
""" ],

[ 1.2, '05-03-2009', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Find_Files now leaves svn directories untouched
""") ],

[ 1.1, '05-02-2009', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Find_Files now removes empty filenames
""") ],

[ 1.0, '17-01-2009', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Get_Rel_Path   added
  - Get_Abs_Path   added
""") ],

[ 0.9, '21-12-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Find_Files_1 extended with 'RootOnly'
""") ],

[ 0.8, '23-11-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Get_Windows_Filename renamed to Get_PDB_Windows_Filename
  - Get_PDB_Windows_Filename bugs solved
""") ],

[ 0.7, '19-10-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Get_Relative_Path, returns source, if on another drive (windows)
""") ],

[ 0.6, '07-10-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Find_Files and Find_Files_1, now returns a sorted result
  - Get_Relative_Path, didn't account for case-insensitivity on Windows systems
  - Get_Relative_Path, double backslashes translated to forward slash
  - Get_Absolute_Path_REMOVED_FOR_THE_MOMENT (Linux problems and not necessary for windows)
""") ],

[ 0.5, '31-09-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Change_FileExt, improved, so you can extend the filename
                    Change_FileExt ( Filename, '_extra.cfg' )
""") ],

[ 0.4, '31-09-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Get_Windows_Filename: Crashed when used with non-existing filename
""") ],

[ 0.3, '24-09-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Get_Windows_Filename added
""") ],

[ 0.2, '20-08-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - Change_FileExt added
""") ],

[ 0.1, '27-02-2008', 'Stef Mientki',
'Test Conditions:', (2,) , _(0, """
  - orginal release
""") ],
]
# ***********************************************************************

import os
import sys
import fnmatch
import glob

#from dialog_support import AskYesNo

# ***********************************************************************
# ***********************************************************************
def Change_FileExt ( filename, new_ext ) :
  if new_ext.find ( '.' ) < 0 :
    new_ext = '.' + new_ext
  return os.path.splitext ( filename )[0] + new_ext
# ***********************************************************************

class test_class ( object ):
  def __init__ ( self ):
    """
    testclass docstring
    """
    pass

# ***********************************************************************
# ***********************************************************************
# generates a full path, from a path relative to the calling module
# example:
#   Image_Path = Get_Absolute_Path ( '../pictures' )
# ***********************************************************************
def Get_Absolute_Path_REMOVED_FOR_THE_MOMENT ( Relative_Path ) :
  # find from which file this function is called
  SourceFile = sys._getframe(1).f_code.co_filename
  Path, File = path_split ( SourceFile )
  Path = os.path.join ( Path, Relative_Path )
  # remove the intermediate /../
  return os.path.normpath ( Path )
# ***********************************************************************

# ***********************************************************************
# R.Barran 30/08/2004
# ***********************************************************************
def Get_Relative_Path ( target, base=os.getcwd()):
  """
  Return a relative path to the target from either the current dir or an optional base dir.
  Base can be a directory specified either as absolute or relative to current dir.
  """
  # in case of an empty string
  if not ( target ) :
    return ''

  if not os.path.isdir(base):
      raise OSError('Base is not a directory or does not exist: '+base)

  base_list = (os.path.abspath(base)).split(os.sep)
  print("base_list",base_list)
  target_list = (os.path.abspath(target)).split(os.sep)
  print("target_list",target_list)

  # On the windows platform the target may be on a completely different drive from the base.
  if os.name in ['nt','dos','os2'] and (base_list[0].upper() != target_list[0].upper() ):
    #raise OSError, 'Target is on a different drive to base. Target: '+target_list[0].upper()+', base: '+base_list[0].upper()
    return target

  # Starting from the filepath root, work out how much of the filepath is
  # shared by base and target.
  for i in range(min(len(base_list), len(target_list))):
    if os.name in ['nt','dos','os2'] :
      if base_list[i].upper() != target_list[i].upper(): break
    else :
      if base_list[i] != target_list[i]: break
  else:
      # If we broke out of the loop, i is pointing to the first differing path elements.
      # If we didn't break out of the loop, i is pointing to identical path elements.
      # Increment i so that in all cases it points to the first differing path elements.
      i+=1

  rel_list = [os.pardir] * (len(base_list)-i) + target_list[i:]
  if rel_list :
    dir_ = os.path.join(*rel_list)
    dir_ = dir_.replace ( '\\', '/' )
    return dir_
  else :
    return ''
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def Get_Rel_Path ( target ) :
  """
  Creates a path, relative to the applications path
  """
  print(print ( 'Get_Rel_Path:', target, Application.Dir ))
  return Get_Relative_Path ( target, Application.Dir )
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def Get_Abs_Path ( target ) :
  """
  Creates a path, absolute to the applications path
  """
  return os.path.join ( Application.Dir, target )
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def Main_Module_Filename () :
  return sys.argv[0]
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def File_Exists (filename):
  if filename :
    return os.path.exists ( filename)
  else :
    return None
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def Get_PDB_Windows_Filename ( FileName ) :
  """
On windows systems,
  Translates the Filename to the correct case
  the preceding absolute or relative path is converted to lower case !!
  Used to translate filenames coming from PDB and similar packages
On other OS, it just returns the unmodified string
  """
  if os.name == 'nt' :
    """
    # path will be translated to lowercase
    # and we want only forward slashes
    FileName = FileName.lower ().replace ( '\\', '/' )

    # Do a search with some degrees of freedom
    # otherwise glob.glob just returns the original string !!
    Result = glob.glob ( FileName [:-1] + '*')

    if Result:
      for R in Result :
        if R.lower().replace( '\\', '/' ) == FileName :
          return R.replace ( '\\', '/' )
    """
    #install pywin32 before
    import win32file
    filename = FileName.lower ().replace ( '\\', '/' )
    Path, File = path_split ( filename )
    try:
      File = win32file.FindFilesW ( FileName )
    except :
      return None #FileName
    if Path :
      Path += '/'
    #print 'PPBBDD',FileName, Path, File
    if File :
      return Path.lower() + File[0] [8]
    else :
      return FileName

  return FileName
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def File_Delete ( filename ):
  if File_Exists ( filename ) :
    os.remove ( filename )
# ***********************************************************************

# ***********************************************************************
# removes a tree (path), even if it contains files
# ***********************************************************************
def Tree_Delete ( path ) :
  if AskYesNo ( Question = 'Delete Directory: '+path,
                Title    = 'Please read carefully ' ) :
    import shutil
    shutil.rmtree ( path )
# ***********************************************************************

# ***********************************************************************
def Force_Dir ( path, init = False ) :
  """
  Forces a directory and
  can create a default __init__.py file if not exists and init = True
  """
  if not( File_Exists ( path ) ) :
    os.makedirs ( path )
  if init :
    initfile = os.path.join ( path, '__init__.py')
    if not ( File_Exists ( initfile ) ) :
      file = open ( initfile, 'w' )
      file.write ( '# This is a Python package.' )
      file.close ()
# ***********************************************************************

# ***********************************************************************
# Searches for all (Python) files, starting at path
# Returns a list of tuples,
# whereas each tuple contains
#   - the path
#   - the filename
"""
"""
# ***********************************************************************
def Find_Files_1 ( path , Py_Files, mask = '*.py', RootOnly = False ) :
  if File_Exists ( path ) :
    files = os.listdir ( path )
    for file in files :
      if os.path.isfile ( os.path.join ( path, file ) ) :
        #if os.path.splitext ( file ) [1] == mask :
        if fnmatch.fnmatch ( file, mask ) :
          #print file
          Py_Files.append ( [ path, file ] )
      elif not ( RootOnly ) :
        # Dont touch SVN directories !!
        if file != '.svn' :
          new_path = os.path.join ( path, file )
          Find_Files_1 ( new_path, Py_Files, mask )
    Py_Files.sort()
# ***********************************************************************

# ***********************************************************************
# Searches for all (Python files), starting at path
# Returns a list of tuples,
# whereas each tuple contains
#   - the path
#   - the filename
# ***********************************************************************
def Find_Files ( dir, mask = '*.py', RootOnly = False  ) :
  Py_Files = []
  Find_Files_1 ( dir, Py_Files, mask, RootOnly )

  # ********************************************
  # Sort the filelist and
  #   remove the basepath
  #   remove file extension
  # ********************************************
  Py_Files.sort()
  N = len (dir)
  for i,item in enumerate ( Py_Files ) :
    Py_Files [i][0] = Py_Files [i][0][N:]
    Py_Files [i][1] = os.path.splitext ( Py_Files[i][1] )[0]

  # remove empty
  empty = [ '', '' ]
  if empty in Py_Files :
    Py_Files.remove ( empty )

  return Py_Files
# ***********************************************************************
def Find_Files_Ext ( dir, mask = '*.py', RootOnly = False  ) :
  """
  Returns a listof found files.
  """
  Py_Files = []
  Find_Files_1 ( dir, Py_Files, mask, RootOnly )

  # ********************************************
  # Sort the filelist and
  #   remove the basepath
  #   remove file extension
  # ********************************************
  Py_Files.sort()
  N = len (dir)
  for i,item in enumerate ( Py_Files ) :
    Py_Files [i][0] = Py_Files [i][0][N:]
    Py_Files [i][1] = Py_Files[i][1]

  # remove empty
  empty = [ '', '' ]
  if empty in Py_Files :
    Py_Files.remove ( empty )

  return Py_Files
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def Get_Abs_Filename_Case ( Filename, RootOnly = True ) :
  """
  Find the right case of the filename,
  (the absolute or relative path must be in the correct case)
  and returns the filename in the correct case,
  with the absolute path.
  """
  # Test if absolute or relative path
  if Platform_Windows :
    Relative = ( len ( Filename ) < 2 ) or ( Filename[1] != ':' )
  else :
    Relative = not ( os.path.isabs ( Filename ) )

  # If relative path, make it absolute
  if Relative :
    # get path of file, from which this function was called
    SourceFile = sys._getframe(1).f_code.co_filename
    SourcePath, SourceFile = path_split ( SourceFile )
    print ( ' SourcePath', SourcePath )

    Filename = os.path.join ( SourcePath, Filename )
    print ( ' Filename', Filename)
    Filename = os.path.normpath ( Filename )
    print ( ' Filename', Filename)

  Filename = os.path.normpath ( Filename )
  print ( ' Filename', Filename)
  Filename = Filename.replace ( '\\', '/' )
  print ( ' Filename', Filename)

  Path, Filename = os.path.split ( Filename )
  Filename = Filename.lower ()
  print ( 'Path, Filename', Path, Filename)
  Files = Find_Files_Ext ( Path, mask = '*.*', RootOnly = True  )
  for File in Files :
    #print ( File )
    if File[1].lower () == Filename :
      #print ( 'Found:', File[1] )
      return os.path.join ( Path, File[1] ).replace ( '\\', '/' )
  else :
    return
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
if __name__ == "__main__":
  
  Test_Defs ( 10 )
  
  # test of paths join / normalize
  if Test ( 1 ) :
    print(Joined_Paths ( 'D:\\Data_Python_25' ))
    print(Joined_Paths ( 'D:\\Data_Python_25\\' ))
    print(Joined_Paths ( 'D:/Data_Python_25' ))
    print(Joined_Paths ( 'D:/Data_Python_25/' ))

    print(Joined_Paths ( 'D:/Data_Python_25' , 'support', 'plot' ))
    print(Joined_Paths ( 'D:/Data_Python_25/' , 'support', 'plot' ))
    print(Joined_Paths ( 'D:/Data_Python_25/' , 'support/', 'plot\\' ))
    print(Joined_Paths ( 'D:\\Data_Python_25/' , 'support/', 'plot\\' ))
    print(Joined_Paths ( 'D:/Data_Python_25\\' , 'support/', 'plot\\' ))
    print(Joined_Paths ( 'D:/Data_Python_25/' , 'support\\', 'plot\\' ))

    print(Joined_Paths ( '/Data_Python_25/' , 'support/', 'plot\\' ))
    print(Joined_Paths ( '\\Data_Python_25\\' , 'support/', 'plot\\' ))

    print(Joined_Paths ( 'D:/Data_Python_25/support/plot' , '..', '..' ))
    print(Joined_Paths ( 'D:/Data_Python_25/support/plot' , '../..', '..' ))
    print(Joined_Paths ( 'D:/Data_Python_25\\support/plot' , '..\\', '..' ))

  if Test (2 ) :
    Force_Dir ('../PyLab_Works/land/duits/nl/aap', True )
    
  if Test ( 3 ) :
    print("****** files = glob.glob ( '../*.py' )")
    files = glob.glob ( '../*.py' )
    for file in files :
      print(os.path.isfile(file),file)

    print("******* os.listdir ( '../' )")
    print(os.listdir ( '../' ))

    print("****** files = os.listdir ( '../' )")
    files = os.listdir ( '../' )
    #for file in files :
    #  print file

  if Test ( 4 ) :
    print("****** Find_Files ( '../PyLab_Works' )")
    dir = '../PyLab_Works'
    Py_Files = Find_Files ( dir )
    for item in Py_Files :
      print(item)

    print("****** Find_Files_1 ( '../PyLab_Works' )")
    dir = '../PyLab_Works'
    Py_Files = []
    Find_Files_1 ( dir, Py_Files )
    for item in Py_Files :
      print(item)

  if Test ( 5 ) :
    print(Get_Relative_Path ( '../pictures/pict.png', Application.Dir ))
    print(Get_Relative_Path ( 'D:/Data_Python_25/pictures/pict.png', Application.Dir ))
    print(Get_Relative_Path ( 'P:/portable/aap.txt', Application.Dir ))
    print(Get_Relative_Path ( 'P:/portable/aap.txt', "lang" ))
    print(Application.Dir)

    aap = Get_Relative_Path ( 'D:/Data_Python_25/pictures/pict.png', Application.Dir )
    aap = Get_Relative_Path ( aap )
    print(Get_Relative_Path ( aap ))

  # test of search text in file
  if Test ( 6 ) :
    import time
    dir = '../PyLab_Works'
    dir = 'P:\Python'

    start = time.time ()
    Py_Files = Find_Files ( dir )
    for item in Py_Files :
      #print '****', item
      if item [0].find('\\') == 0 :
        item[0] = item[0][1:]
        #print '****', item
      filename = os.path.join ( dir, item[0], item[1]) + '.py'
      file = open ( filename, 'r' )
      line = file.read()
      file.close ()
      if line.find ('SetValue') >= 0 :
        print(filename)
    print(time.time()-start)
    """ OUTPUT OF FINDSTR:  findstr /n /s /I  strsearched  *.py
    Lib\test\test_sundry.py:53:import rlcompleter
    Lib\test\test___all__.py:132:        self.check_all("rlcompleter")
    Lib\test\test___all__.py:168:        # rlcompleter needs special consideration;
    it import readline which
    Lib\test\test___all__.py:171:            self.check_all("rlcompleter")

    P:\Python>
    """

  # test of wrong case of filename
  if Test ( 7 ) :
    FileName = '../PyLab_Works/PyLab_Works_Globals.py'
    print('1', Get_PDB_Windows_Filename ( FileName ))
    print('2', Get_PDB_Windows_Filename ( FileName.lower () ))
    print('3', Get_PDB_Windows_Filename ( FileName.upper () ))
    FileName = 'D:/Data_Python_25/PyLab_Works/pylab_sworks_programs/VPython_Code/new.pcmd'
    print('1', Get_PDB_Windows_Filename ( FileName ))
    print('2', Get_PDB_Windows_Filename ( FileName.lower () ))
    print('3', Get_PDB_Windows_Filename ( FileName.upper () ))

  # test completer
  if Test ( 8 ) :
    import rlcompleter
    import wx
    import wx.stc as stc
    
    
    a = rlcompleter.Completer ( globals () )
    #print 'k',a.global_matches( 'a' )
    #print 'k',a.global_matches( 'test_class.' )
    #print a.complete( 'wx.',0)

    line = 'wx.A'
    result = ''
    State = 0
    while  a.complete ( line, State ) :
      result += ' ' + a.complete ( line, State )
      #print a.complete ( line, State )
      State += 1
    print(result)
   

  # speed test string vs list
  if Test ( 9 ) :
    import time
    start = time.time ()
    line = ''
    for i in xrange ( 10000000 ) :
      line += ' ' + 'aap'
    print(time.time () - start)

    start = time.time ()
    line = []
    for i in xrange ( 10000000 ) :
      line.append ( 'aap' )
    line = ' '.join ( line )
    print(time.time () - start)

  if Test ( 10 ) :
    filename = '../PyLab_Works/pylab_works_programs/2D_Scene_Ball1/ball1_save.py'
    filename = Get_Abs_Filename_Case ( filename )
    print ( 'Found:', filename )

# ***********************************************************************
pd_Module ( __file__ )

