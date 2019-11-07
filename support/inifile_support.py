import __init__

__doc__ = """
# ***********************************************************************
# A more windows friendly inifile handler
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007 Stef Mientki
# mailto:S.Mientki@ru.nl
# Please let me know if it works or not under different conditions
#
"""

# ***********************************************************************
# ***********************************************************************
_Version_Text = []
# ***********************************************************************


# ***********************************************************************
#import ConfigParser
import os
from configobj import ConfigObj
import pickle
from wx import Colour
# ***********************************************************************
from path_support import *
# CASE OF NAMES !!!!!

class inifile ( ConfigObj ):
  def __init__ ( self, filename, Force_Strings = False ) :
    """
    # under Ubuntu a filename with both
    # forward and backward slashes seems to give trouble
    # already in path_split
    """
    filepath, filename = path_split ( filename )

    # ensure filename has a complete path !!
    # because we don't know the active directory when saving
    if filepath == '' :
      filepath = os.getcwd ()
    filename = os.path.join ( filepath , filename )

    self.Filename = filename
    self.Force_Strings = Force_Strings

    # the following change give a huge improvent,
    # all kind of variables like list,float,int,etc can be written/read directly
    # only tupples seems sometimes to fail, but they are catched in this wrapper
    ##ConfigObj.__init__ ( self, filename , list_values = False,
    ##                     write_empty_values = True )
    try:
      ConfigObj.__init__ ( self, filename , list_values = True
                                        , write_empty_values = True
                                        , unrepr = not ( Force_Strings) )
                                          #stringify = False )
    except :
     import traceback
     lines = traceback.format_exc ().split('\n')
     traceback.print_exc ()
     # last line contains 'First error at line 4.'
     #   or               'First error at line "4".'
     line = lines [-2].strip()
     line = line.replace ( '"' , '' )
     line = line.replace ( '.' , '' )
     line = line.strip ()

     linenr = int ( line.split (' ')[-1] )
     fh = open ( filename, 'r' )
     lines = fh.readlines ()
     fh.close ()
     print('  File:', filename)
     print('  Line =', linenr, ':', lines [ linenr -1 ].strip())
     print('  Mode : Force_Strings =', Force_Strings)

    self.newlines = '\r\n'   # not strictly necessary
    self.Section = ''
    self.Modified = False
    
    # we create a default section so we can tests like "if ini:"
    self.Section = 'empty'
    self.Write ( 'empty', 0)
    self.Section = ''

    
  """
  [('My_Float', '7.1234'), ('My_Integer', '123'), ('My_List', '(11,22,33)')]
  """
  def Get_Section ( self, Section = None ):
    if Section :
      self.Section = Section
    Name_Value_Pairs = []
    if not ( self.Has_Section( self.Section ) ) : return Name_Value_Pairs
    sectie = self[self.Section]
    for key in sectie:
      Name_Value_Pairs.append ( ( key, sectie[key]) )
    return Name_Value_Pairs


  def Has_Section (self, section):
    return section in self.sections

  def Remove_Section (self, section):
    try:
      del self[section]
    except:
      pass
    # if the selected section is the section being removed,
    # clear the selection
    if section == self.Section:
      self.Section = ''
    self.Modified = True

  def Sections ( self ) :
    return self.sections;

  def Names ( self, section ) :
    return self[section].keys()

  # *************************************************************
  # General Read procedure should read almost anything
  # Returns Default if not found
  # *************************************************************
  def Read (self, name, default = None ):
    if not ( self.Has_Section( self.Section ) ) : return default
    name = name.strip()
    line = self [ self.Section ].get ( name )
    #print 'TFGR',name,line
    # apparently tupples are not decoded, so try it here
    if isinstance ( line, str ) :
      try :
        line = eval ( line )
      except :
        pass
    if line != None : return line
    else: return default

  # Returns Default if not found
  def Read_String (self, name, default= '' ):
    if not ( self.Force_Strings ) :
      print('    DEPRECIATED PROCEDURE Read_String, USE Read instead !')
    if not ( self.Has_Section( self.Section ) ) :
      return default
    name = name.strip()
    #print 'RRR',name
    #print self.Section
    line = self [ self.Section ].get ( name )

    if line :
      if isinstance ( line, list ) :
        line = ', '.join ( line )
      return line
    else :
      return default

  def Read_Integer (self, name, default = 0 ):
    if not ( self.Force_Strings ) :
      print('    DEPRECIATED PROCEDURE Read_Integer, USE Read instead !')
    if not ( self.Has_Section( self.Section ) ) : return default
    name = name.strip()
    try:
      return self[self.Section].as_int(name)
    except:
      # now try to read as float
      try:
        return int(round(self[self.Section].as_float(name)))
      except:
        return default

  def Read_Float (self, name, default = 0.0 ):
    print('    DEPRECIATED PROCEDURE Read_Float, USE Read instead !')
    if not ( self.Has_Section( self.Section ) ) : return default
    name = name.strip()
    try:
      return self[self.Section].as_float(name)
    except:
      return default

  def Read_Bool (self, name, default = False):
    if not ( self.Force_Strings ) :
      print('    DEPRECIATED PROCEDURE Read_Bool, USE Read instead !')
    name = name.strip()
    try:
      return self[self.Section].as_bool(name)
    except:
      return default

  # ***************************************************************
  # Improved Read_List, but doesn't work so well, e.g. the next line
  #    Arial, 10, True, (0, 0, 250, 255),
  # gives an error " 'Arial' not defined "
  # ***************************************************************
  def Read_List2_weg (self, name, default = [] ):
    print('    DEPRECIATED PROCEDURE Read_List2, USE Read instead !')
    if not ( self.Has_Section( self.Section ) ) : return default
    name = name.strip()
    _str = self.Read_String ( name, None)
    print('AAA',_str)
    _list = eval ( '['+_str+']' )
    return _list

  # ***************************************************************
  # Reading tuples (e.g. color) back is quit anoying,
  # we get a string, which must be converted to a tupple
  # ***************************************************************
  def Read_List (self, name, default = [] ):
    print('    DEPRECIATED PROCEDURE Read_List, USE Read instead !')
    if not ( self.Has_Section( self.Section ) ) : return default
    name = name.strip()
    _str = self.Read_String ( name, None)

    #print 'READ_LIST',_str,type(_str)
    # when inifile is in memory, items written as a list,
    # will also return a list !!
    if type(_str) == list: return _str
  
    if type(_str) == tuple: return list(_str)

    if _str :
      _str = _str.replace( '(' , '' )
      _str = _str.replace( ')' , '' )
      _str = _str.replace( '[' , '' )
      _str = _str.replace( ']' , '' )
      _str = _str.split ( ',' )

    # because default is a color property
    # we are not allowed to parse it (and we don't need to do)
    if _str :
      _list = []
      for item in _str:
        item = item.strip()
        try:
          _list.append ( int( item ) )
        except:
          try:
            _list.append ( float( item ) )
          except:
            if item == 'None':
              _list.append ( None )
            elif item == 'True':
              _list.append ( True )
            elif item == 'False':
              _list.append ( False )
            else:
              _list.append ( item.replace ( "'" , "" ) )
    else:
      _list = default
    return _list

  # ***************************************************************
  # ***************************************************************
  def Read_Tuple (self, name, default = () ):
    print('    DEPRECIATED PROCEDURE Read_Tuple, USE Read instead !')
    return tuple(self.Read_List ( name, default ))

  # ***************************************************************
  # ***************************************************************
  def Read_Dict ( self, name, default = {} ) :
    if not ( self.Has_Section( self.Section ) ) :
      return default
    line = self [ self.Section ].get ( name )
    #print 'read dict line:',line
    try :
      if line :
        return pickle.loads ( line )
    except :
      pass
    return default

  # ***************************************************************
  # ***************************************************************
  def Write (self, name, value):
    #print 'ININI',self.filename,self.Section,name,value
    name = name.strip()
    if not( self.Has_Section ( self.Section ) ):
      self [ self.Section ] = {}

    if isinstance ( value, dict ) :
      self [ self.Section ][ name ] = pickle.dumps ( value )
    elif (type(value) in [ bool, int, str, bytes, float, list, tuple ] ) \
       or ( value == None ) :
      #or ( value == None ) \
      #or ( value == Null ) :
      self[self.Section][name] = value

    # wx.Colour can not be read back,
    # so we've to make it a tuple
    elif isinstance ( value, Colour ) :
      temp = tuple ( value ) +  ( value.Alpha(), )
      self[self.Section][name] = temp

    else :
      try :
        # try to convert to tuple,
        # but can just as well be written/read as a tuple
        value = tuple ( value )
        self[self.Section][name] = value
      except :
        self[self.Section][name] = str(value)
    self.Modified = True

  def Close ( self ):
    """
    Close / Flush the data to file.
    After this action, the inifile still exists and can be used,
    """
    if self.Modified:
      self.write()
    self.Modified = False

  Flush = Close

  def Print_All ( self ) :
    print('----- FILE:', self.filename, '-----')
    for sectie in self.sections : #self.Sections():
      line = '[' + sectie +']'
      print(line)
      Names = self.Names (sectie)
      for name in Names:
        try:
          line = self[sectie].get(name)
        except:
          line = '-- Unknown --'
        print('   ', name, '=',line)
# ***********************************************************************


#from General_Globals import *

# ***********************************************************************
# for test, read and print some ini file
# ***********************************************************************
#if __name__ == '__main__':
#  pass
  '''
  print("Testing inifile support")
  Test_Defs ( 9 )

  import wx
  from dialog_support import *
  app = wx.App ()

  print("test read")
  if Test ( 1 ) :
    FileType = "Ini Files (*.ini)|*.ini|"\
               "All Files (*.*)|*.*"
    filename = AskFileForOpen ( FileTypes = FileType )
    if filename:
      print(' FILE:', filename)
      ini = inifile ( filename )
      for items in ini.sections():
        line = '[' + items +']'
        print(line)
        names = ini.options(items)
        ini.Section = items
        for name in names:
          print('   ', name, '=', ini.Read_String(name, '-- Unknown --'))

  if Test ( 2 ) :
    # test write / read
    filename = 'test_inifile_support.ini'
    ini = inifile (filename)
    ini.Ssection = 'general'
    tup = [ 'aap',1,2,3,4 ]
    ini.Write ('aap',tup)
    ini.Close()

    tup = None
    ini = inifile (filename)
    ini.Section = 'general'
    tup = ini.Read_String ('aap')
    tup = list(tup)
    print('Read', type(tup), tup)
    tup = ini.Read_Tuple ('aap')
    print('Read', tup)
    tup = ini.Read_List ('aap')
    print('Read', tup)

  if Test ( 3 ) :
    filename='testapp_JALsPy.ini'
    filename='JALsPy.ini'
    filename=os.getcwd()
    filename=os.path.join(os.getcwd(),'..','JAL','demo_read_ti59_rom.cfg')

    ini = inifile ( filename )
    ini.Print_All ()

    ini.Section = 'Test All'
    print('Has Section (Test All) :', ini.Has_Section ('Test All'))
    print('Get Section', ini.Get_Section())
    print('Read_String :', ini.Read_String ( 'My_String' ))
    print('Read_Integer:', ini.Read_String ( 'My_Integer' ))
    print('Read_Float  :', ini.Read_String ( 'My_Float' ))
    print('Read_List   :', ini.Read_String ( 'My_List' ))


    print('Read_Float (as String)  :', ini.Read_String  ( 'My_Float' ))
    print('Read_Float (as Integer) :', ini.Read_Integer ( 'My_Float' ))
    print('Read_Float (as List)    :', ini.Read_List    ( 'My_Float' ))
    print('Read_Float (as Tuple)   :', ini.Read_Tuple   ( 'My_Float' ))
    print('Read_Float (as Boolean) :', ini.Read_Bool    ( 'My_Float' ))

    ini.Section = 'General'
    print('Read_Float              :', ini.Read_Float   ( 'Tusec' ))
    print('Read_Float (as String)  :', ini.Read_String  ( 'Tusec' ))
    print('Read_Float (as Integer) :', ini.Read_Integer ( 'Tusec' ))
    print('Read_Float (as List)    :', ini.Read_List    ( 'Tusec' ))
    print('Read_Float (as Tuple)   :', ini.Read_Tuple   ( 'Tusec' ))
    print('Read_Float (as Boolean) :', ini.Read_Bool    ( 'Tusec' ))

    ini.Section = 'Device SN1'
    line = ini.Read_String ( 'Caption' )
    print('Read_String :', ini.Read_String ( 'Caption','aap' ))
    print(line,type(line))


    ini.Remove_Section('aap')
    ini.Close()

    ini = None
    if ini:
        print('ok',type(ini))
    else:
        print('wrong',type(ini))
    ini = ConfigObj (filename)
    if ini:
        print('ok',type(ini))
    else:
        print('wrong',type(ini))

  if Test ( 4 ) :
    filename='inifile_support_test.ini'
    ini = inifile ( filename )
    ini.Section = 'Test'

    # tupple and list will be written exactly the same
    ini.Write ( 'None', None )
    ini.Write ( 'NoneList', [ None ])
    ini.Write ( 'list',       [ 1, 2, 3, 4, 5 ] )
    ini.Write ( 'tuple',  (1, 2, 3, 4, 5) )
    a =[[ 1, 2, 3, 4, 5 ], (1,2),[1,(2,3),[6]]]
    ini.Write ( 'nested', a )
    ini.Close()

    # *********** and read all back

    ini = inifile ( filename )
    ini.Section = 'Test'
    print(ini.Read ( 'None', None ))
    print(ini.Read ( 'NoneList', None))
    print(ini.Read ( 'list',    None ))
    print(ini.Read ( 'tuple',   None ))
    print(ini.Read ( 'nested',  None ))
    
    print(ini.Read ( 'None' ))
    print(ini.Read ( 'NoneList' ))
    print(ini.Read ( 'list' ))
    print(ini.Read ( 'tuple' ))
    print(ini.Read ( 'nested' ))
    print(a)
    ini.Close()

  if Test ( 5 ) :
    filename='inifile_support_test.ini'
    ini = inifile ( filename )
    ini.Section = 'Test'

    ini.Print_All ()

    keys = ['tuple_tuple', 'list_list', 'string_tuple', 'string_list' ]
    for key in keys :
      item = ini.Read_String ( key )
      print(key + ', Read_String:', type(item), item)
      item = ini.Read_Tuple ( key )
      print(key + ', Read_Tuple: ', type(item), item)
      item = ini.Read_List ( key )
      print(key + ', Read_List:  ', type(item), item)
      print()
    ini.Close()

  if Test ( 6 ) :
    filename = 'inifile_support_test.ini'
    ini = inifile ( filename )
    ini.Section = 'Test'

    # tupple and list will be written exactly the same
    ini.Write ( 'None',
    'layout2|name=SN20;caption=Signal WorkBench (Plotting);state=17152;dir=5;layer=0;row=0;pos=0;prop=100000;bestw=100;besth=40;minw=100;minh=40;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1|dock_size(5,0,0)=102|'
 )
    ini.Write ( 'Test',
    u'layout2|name=SN20;caption=Signal WorkBench (Plotting);state=17152;dir=5;layer=0;row=0;pos=0;prop=100000;bestw=100;besth=40;minw=100;minh=40;maxw=-1;maxh=-1;floatx=-1;floaty=-1;floatw=-1;floath=-1|dock_size(5,0,0)=102|'
 )

    ini.Write ( 'Test3','aap')
    ini.Write ( 'Test4',u'aap')

    ini.Close()

  if Test ( 7 ) :
    # special to correct errors in config files due to missing "unicode"
    filename = '../PyLab_Works/pylab_works_programs/2D_Scene.cfg'
    ini = inifile ( filename )
    ini.Section = 'Device SN9'
    line = ini.Read ( 'CS_', None )
    newline = ''
    for c in line :
      newline += c
    print(newline)
    ini.Write ( 'CS_', newline )

    ini.Close()

  # ***************************************************************
  # test writing and reading Dictionairy
  # ***************************************************************
  if Test ( 8 ) :
    filename = 'inifile_support_test.ini'
    ini = inifile ( filename )
    ini.Section = 'Test Dict'
    ini.Write ( 'Dict', {33: 'aap', 45: [34, 56, 'hjk'] } )
    ini.Close ()

    ini = inifile ( filename )
    ini.Section = 'Test Dict'
    #print 'Dictionairy readback:'
    aap = ini.Read_Dict ( 'Dict' )
    print(type(aap), aap)
    ini.Close

  # ***************************************************************
  # test writing and reading Null
  # ***************************************************************
  if Test ( 9 ) :
    filename = 'inifile_support_test.ini'
    ini = inifile ( filename )
    ini.Section = 'Test Dict'
    ini.Write ( 'AAP', None )
    ini.Write ( 'AAPNone', None )
    ini.Write ( 'Dict', {33: 'aap', 45: [34, 56, 'hjk'] } )
    #ini.Write ( 'DictNulls', {33: Null, 45: [34, 56, 'hjk'] } )
    ini.Close ()

    ini = inifile ( filename )
    ini.Section = 'Test Dict'
    #print 'Dictionairy readback:'
    aap = ini.Read_Dict ( 'Dict' )
    print (type(aap), aap)
    aap = ini.Read ( 'AAP' )
    print (type(aap), aap)
    aap = ini.Read ( 'AAPNone' )
    print (type(aap), aap)
    ini.Close
  '''
# ***********************************************************************
#pd_Module ( __file__ )

