import __init__
from language_support import  _

__doc__ = """
"""

# ***********************************************************************
# ***********************************************************************
_Version_Text = [

[ 0.1 , '05-05-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Initial Release
"""],

]
# ***********************************************************************


# ***********************************************************************
from General_Globals import *
import os
# ***********************************************************************

# CASE OF NAMES !!!!!


class win_inifile ( object ):
  def __init__ ( self, filename = None, Force_Identifiers = False ) :
    """
    If filename == None, nothing happens,
    but all methods and attributes are available
    """
    self.Content = {}
    self.Section_List = []
    self.Section = None

    if not ( filename ) :
      return
    
    # ensure filename has a complete path !!
    # because we don't know the active directory when saving
    filepath, filename = path_split ( filename )
    if filepath == '' :
      filepath = os.getcwd ()
    filename = os.path.join ( filepath , filename )
    self.Filename = filename

    def convert ( line ) :
      line = line.lower ()
      if Force_Identifiers :
        line = line.replace ( ' ', '_' )
      return line

    # Read and parse the file
    fh = open ( self.Filename, 'r' )
    lines = fh.readlines ()
    fh.close ()
    for line in lines :
      line = line.strip()
      if line :
        if line.find ( '[' ) == 0 :
          line = convert ( line [ 1:-1 ].strip() )
          self.Content [ line ] = {}
          self.Section = line
          self.Section_List.append ( line )
        else :
          if self.Section :
            line = line.split ( '=' )
            self.Content [ self.Section.lower () ] [ convert ( line [0] ) ] = \
              '='.join (line [1:])

    self.Section = None
    
    #v3print ('OOOIIUU', self.Content )
    #self.Print_All ()

    
  #*******************************************
  def Get_Section ( self, Section = None ):
    if Section :
      self.Section = Section.lower ()

    Name_Value_Pairs = []
    for key, value in self.Content [ self.Section.lower() ].iteritems () :
      Name_Value_Pairs.append ( ( key, value ) )
    return Name_Value_Pairs

  #*******************************************
  def Has_Section ( self, Section ):
    return Section.lower () in self.Section_List

  #*******************************************
  def Sections ( self ) :
    return self.Section_List;

  #*******************************************
  def Names ( self, Section ) :
    return self.Content [ Section.lower () ].keys()

  # *************************************************************
  # General Read procedure should read almost anything
  # Returns Default if not found
  # *************************************************************
  def Read (self, name, default = None ):
    name = name.strip().lower()
    #print 'READ', name,
    if not ( self.Section.lower() in self.Content ) :
      #print 'missing',self.Section.lower(),self.Sections()
      return default
    #print 'found',self.Content [ self.Section.lower() ]
    return self.Content [ self.Section.lower() ].get ( name, default )

  Read_String = Read

  #*******************************************
  def Read_Integer (self, name, default = 0 ):
    value = self.Read ( name, default )
    try :
      value = int ( value )
    except :
      value = default
    return value

  #*******************************************
  def Read_Float (self, name, default = 0.0 ):
    value = self.Read ( name, default )
    try :
      value = float ( value )
    except :
      value = default
    return value

  #*******************************************
  def Read_Bool (self, name, default = False):
    value = self.Read ( name, default )
    #v3print ( 'Read_Bool', self.Section, name, value, )
    try :
      if isinstance ( value, basestring ) :
        try:
          value = int ( value )
        except :
          value = False
      value = bool ( value )
    except :
      value = default
    #v3print ( value )
    return value

  #*******************************************
  def Close ( self ):
    pass
  Flush = Close

  #*******************************************
  def Print_All ( self ) :
    print ('----- FILE:', self.Filename, '-----')
    for Section in self.Section_List :
      v3print ( ' ', Section )
      Names = self.Names ( Section )
      for name in Names:
        try:
          line = self.Content [ Section ].get(name)
        except:
          line = '-- Unknown --'
        v3print ( '   ', name, '=', line )
# ***********************************************************************


# ***********************************************************************
# for test, read and print some ini file
# ***********************************************************************
if __name__ == '__main__':

  Test_Defs ( 1 )

  #******************************************
  # test read vragenlijst informatie
  #******************************************
  if Test ( 1 ) :
    Base_Dir     = 'D:/d_midorg/'
    Protocol_Dir = Base_Dir + 'Protocol/'
    filename = Protocol_Dir + 'VraagLST/ess.vli'

    v3print ( ' FILE:', filename )
    ini = win_inifile ( filename, Force_Identifiers = True )
    ini.Print_All ()


# ***********************************************************************
pd_Module ( __file__ )

