import __init__

# ***********************************************************************
"""
doc_support.py :

License: freeware, under the terms of the BSD-license
Copyright (C) 2008 Stef Mientki
mailto:S.Mientki@ru.nl
"""

# ***********************************************************************


# ***********************************************************************
from General_Globals import *
from language_support import _
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
_Version_Text = [
[ 0.1, '28-07-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
    - orginal release
""" ) ]
]
# ***********************************************************************


import os
#import inspect
from inspect import *
import pyclbr


# ***********************************************************************
# ***********************************************************************
def Get_Classes_And_Functions ( my_module, my_paths = [] ):
  """
  Creates a list with all classes and functions defined in my_module
  (Imported items are excluded)
  If the module is NOT on the Pythonpath, my_paths must be specified.
    my_paths is one of the following: empty / string / list of strings
  The returned result consist of
    List (Ordened by Name) :
      Name, LineNr, { '<method>' : linenr }
    Full filename (including full path) of the scanned module
  For functions there are no methods
  """
  
  # if paths is a string, make it a one-item list
  if isinstance ( my_paths, basestring ) :
    my_paths = [ my_paths ]

  My_Classes = pyclbr.readmodule_ex ( my_module, my_paths )
  """ Returns :
  module  -- the module name
  name    -- the name of the class
  super   -- a list of super classes (Class instances)
  methods -- a dictionary of methods: { '<method>' : linenr }
  file    -- the file in which the class was defined
  lineno  -- the line in the file on which the class statement occurred
  """

  # now order them by linenr
  #print my_classes
  Ordened_List = []
  My_File  = None
  for key in My_Classes:
    item = My_Classes [ key ]
    if item.module == my_module :
      # if the filename (including path) not yet read, do it here once
      if not ( My_File ) :
        My_File = item.file
      temp = [ item.name, item.lineno ]
      if isinstance ( item, pyclbr.Class ):
        temp.append ( item.methods )
      Ordened_List.append ( temp )

  Ordened_List.sort ()
  return Ordened_List, My_File
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Classes_And_Functions_Split2 ( my_module, my_paths = [] ):
  """
  Creates a list with all classes and functions defined in my_module
  (Imported items are excluded)
  If the module is NOT on the Pythonpath, my_paths must be specified.
    my_paths is one of the following: empty / string / list of strings
  The returned result consist of
    List (Ordened by Name) :
      Name, LineNr, { '<method>' : linenr }
    Full filename (including full path) of the scanned module
  For functions there are no methods
  """

  # if paths is a string, make it a one-item list
  if isinstance ( my_paths, basestring ) :
    my_paths = [ my_paths ]

  My_Classes = pyclbr.readmodule_ex ( my_module, my_paths )
  """ Returns :
  module  -- the module name
  name    -- the name of the class
  super   -- a list of super classes (Class instances)
  methods -- a dictionary of methods: { '<method>' : linenr }
  file    -- the file in which the class was defined
  lineno  -- the line in the file on which the class statement occurred
  """

  # now order them by linenr
  #print my_classes
  Function_List = []
  Class_List = []
  My_File  = None
  for key in My_Classes:
    item = My_Classes [ key ]
    if item.module == my_module :
      # if the filename (including path) not yet read, do it here once
      if not ( My_File ) :
        My_File = item.file
      if isinstance ( item, pyclbr.Class ):
        Class_List.append ( [ item.name, item.lineno, item.methods ] )
      else :
        Function_List.append ( [ item.name, item.lineno ] )

  Function_List.sort ()
  Class_List.sort ()
  return Function_List, Class_List, My_File
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
def Get_Classes_And_Functions_Split ( my_module, underscore = '_' ):
  """
  Creates a list with all classes and functions defined in my_module
  Much faster than Get_Classes_And_Functions_Split2
  (Imported items are excluded)
  The returned result consist of
    Function List (Ordened by Name),
    Class List    (Ordened by Name)
  """
  Function_List = []
  try :
    exec ( 'import ' + my_module +' as Mod' )
    List = getmembers ( Mod, isfunction )
    for item in List :
      if ( item[0][0] != underscore ) and \
         ( my_module in getfile ( item[1] ) ) :
        Function_List.append ( item[0] )
  except :
    pass

  Class_List = []
  try :
    exec ( 'import ' + my_module +' as Mod' )
    List = getmembers ( Mod, isclass )
    for item in List :
      if ( item[0][0] != underscore ) and \
         ( my_module in getfile ( item[1] ) ) :
        Class_List.append ( item[0] )
  except :
    pass

  return Function_List, Class_List
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
def _Get_My_Object ( my_module, my_class, my_method = None ) :
  try :
    # The 2 solutions below are identical
    #exec ( 'import '+ self.PyFile )
    #CL = eval ( self.PyFile + '.' + my_class )

    exec ( 'from ' + my_module + ' import ' + my_class )
    if my_method :
      CL = eval ( my_class + '.' + my_method )
    else :
      CL = eval ( my_class )
  except :
    return None

  # check if it's not an method imported from another module
  source_file = getfile ( CL )
  if not ( my_module in source_file ) :
    return None

  return CL
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Class_Methods ( my_module, my_class, underscore = '_' ) :
  CL = _Get_My_Object ( my_module, my_class )
  if CL:
    List = getmembers ( CL, ismethod )
    CM = []
    for C in List :
      """ getfile( object)
      Return the name of the (text or binary) file in which an object was defined.
      This will fail with a TypeError if the object is a built-in module, class, or function.
      """
      """
      if ( my_module in getfile ( C[1] ) ) and \
         ( C[0][0] != underscore ):
        CM.append ( C[0] )
      """
      if C[0][0] != underscore :
        try :
          if my_module in getfile ( C[1] ) :
            CM.append ( C[0] )
        except :
          CM.append ( C[0] )
    return CM
  else :
    return None
# ***********************************************************************


# ***********************************************************************
class Analyze_PyFile ( object ) :
  """
  Analyzes the content of a Py file,
  with special support for the Bricks Libraries of PyLab_Works.
  The following items are determined :
    - self.Path
    - self.FileName
    - self.PyFile
    - self.Doc_String
    - self._Version_Text
    - self.Classes
    - self.Functions
    - Class_Doc_String ( my_class )
    - Class_Args ( my_class )
  """
  
  def __init__ ( self, filename, paths = [] ) :
    """
    - filename maybe specified in any way:
        - with or without extension
        - with or without absolute / relative path
    - paths is one of the following:
        - empty / string / list of strings
    """
    self.Path, self.FileName = path_split ( filename )
    self.PyFile = os.path.splitext ( self.FileName )[0]

    exec ( 'import '+ self.PyFile )

    # In general a module/file contains a doc-string.
    self.Doc_String = eval ( self.PyFile + '.__doc__')
    if self.Doc_String:
      self.Doc_String = self.Doc_String.lstrip ('\n').rstrip('\n')

    try :
      self.Version_Text = eval ( self.PyFile + '._Version_Text' )
    except :
      self.Version_Text = ''

    # Classes and Functions
    classes, self.Full_FileName = Get_Classes_And_Functions ( self.PyFile, paths )
    self.Classes   = []
    self.Functions = []
    for item in classes :
      if len ( item ) == 2 :
        self.Functions.append ( item )
      else :
        self.Classes.append ( item )

  """
  # *********************************************************
  # only called when not found with the normal mechanism
  # *********************************************************
  def __getattr__ ( self, attr ) :
    if   attr == 'x' :
      return self._XY_Org [0]
    elif attr == 'y' :
      return self._XY_Org [1]
    else :
      if not ( self.__dict__.has_key ( attr ) ) :
        self.__dict__[attr] = 0
      return self.__dict__[attr]
  """
  

  # *********************************************************
  # *********************************************************
  def Class_Doc_String ( self, my_class, my_method = None ) :
    # Get the object
    CL = _Get_My_Object ( self.PyFile, my_class, my_method )

    if CL :
      line = CL.__doc__
      line = getdoc ( CL )
      if line :
        return line + '\n'
      else :
        return ''
    return ''

  # *********************************************************
  # *********************************************************
  def Get_Init_Def ( self, my_class, my_method = None ) :
    # Get the object
    CL = _Get_My_Object ( self.PyFile, my_class, my_method )

    line = ''
    if CL :
      if isfunction ( CL ) or ismethod ( CL ) :
        source = getsourcelines ( CL )
      else :
        source = getsourcelines ( CL.__init__ )
      line = ''.join ( source [0] )
      line = line [ : line.find ( ':') + 1]
    return line

  # *********************************************************
  # *********************************************************
  def Get_Class_Methods ( self, my_class ) :
    # Get the object
    CL = _Get_My_Object ( self.PyFile, my_class )

    List = None
    if CL :
      List = getmembers ( CL, isfunction )
    return List

  # *********************************************************
  # *********************************************************
  def Class_Args ( self, my_class ) :
    exec ( 'import '+ self.PyFile )
    class_def = eval ( self.PyFile + '.' + my_class )

    #getargspec( func)
    #Get the names and default values of a function's arguments.
    #A tuple of four things is returned: (args, varargs, varkw, defaults).
    #args is a list of the argument names (it may contain nested lists).
    #varargs and varkw are the names of the * and ** arguments or None.
    #defaults is a tuple of default argument values or None
    #if there are no default arguments; if this tuple has n elements,
    #they correspond to the last n elements listed in args.

    return inspect.getargspec ( class_def )
# ***********************************************************************


# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':

  test = [  3 ]
  
  if 1 in test :
    PyFile = 'file_support.py'
    PyFile = 'file_support'
    PyPath = ''

    #PF = Analyze_PyFile ( PyFile, PyPath )
    PF = Analyze_PyFile ( PyFile )

    print ('Tech_Description:', PF.__doc__)
    print ('Version_Text:',     PF._Version_Text)

    print ('Get_Relative_Path DOC:', PF.Class_Doc_String ( 'Get_Relative_Path' ))
    print ('Get_Absolute_Path DOC:', PF.Class_Doc_String ( 'Get_Absolute_Path' ))

    print ('Args',PF.Class_Args ( 'Get_Relative_Path' ))
    
  if 2 in test :
    from db_support import Find_ODBC
    # import db_support   <== not enough !!
    print (getsourcelines ( Find_ODBC ))

    #sys.path.append ( '../PyLab_Works' )
    from brick import tLWB_Brick
    source = getsourcelines ( tLWB_Brick )
    #text = ''.join ( source [0] )
    #print source
    #source[0] = source[0] [ : source[0].find (':')]
    #print source
    print (tLWB_Brick.__doc__)
    print (getdoc(tLWB_Brick))
    print (getfile (tLWB_Brick))
    List = getmembers (tLWB_Brick, ismethod)
    for item in List :
      print (item[0], type(item[1]))
      
    source = getsourcelines ( tLWB_Brick.__init__ )
    text = ''.join ( source [0] )
    text = text [ : text.find ( ':') + 1]
    
    print (text)
    print ('done')
    
  if 3 in test :
    PyFile = 'db_support'
    PyFile = 'doc_support'
    PyPath = 'D:/Data_Python_25/support'

    #PF = Analyze_PyFile ( PyFile, PyPath )
    PF = Analyze_PyFile ( PyFile )

    print ('Get_Relative_Path DOC:', PF.Class_Doc_String ( 'Get_Relative_Path' ))
    print ('Get_Absolute_Path DOC:', PF.Class_Doc_String ( 'Get_Absolute_Path' ))
    print ('Find_ODBC:',             PF.Class_Doc_String ( 'Find_ODBC' ))
    print ('Not_existing:',          PF.Class_Doc_String ( 'Not_Existing' ))

    print ('Init', PF.Get_Init_Def ('_DataBase'))
    print ('Init', PF.Get_Init_Def ('Find_ODBC'))
    
    print (PF.FileName)
    print (PF.Full_FileName)
    print (PF.Functions)
    print (PF.Classes)

    for Class in PF.Classes :
      for Funk in Class [2] :
        print (Funk)
        
    List = getmembers ( Analyze_PyFile, isfunction )
    for item in List :
      print (item)


# ***********************************************************************
pd_Module ( __file__ )
