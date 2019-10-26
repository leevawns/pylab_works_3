import __init__

__doc__ = """
License: freeware, under the terms of the BSD-license
Copyright (C) 2008 Stef Mientki
mailto:S.Mientki@ru.nl
"""

_Version_Text = [


[ 1.1 , '05-05-2009', 'Stef Mientki',
'Test Conditions:', (3,),
"""
- Create_Table extended with drop argument
- Ini_DB_Object added
""" ],

[ 1.0 , '01-01-2008', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- orginal release
""" ]
]
# ***********************************************************************

#from   PyLab_Works_Globals import _
#import PyLab_Works_Globals as PG
import os
import sys

from file_support import *
#from _winreg import *
from dialog_support import AskYesNo

_DB_Debug = True #False

DB_TYPE_SQLITE = 0
DB_TYPE_ODBC   = 1

# 'System Table' doesn't work very well !!
_DB_Groups = ( 'Table', 'View', 'Index', 'Trigger',
               'Query', 'Visual_Query'  )
_db_groups = []
for group in _DB_Groups :
  _db_groups.append ( group.lower() )


# ***********************************************************************
# ***********************************************************************
#class Dummy_Ini ( )
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class Ini_DB_Object ( object ) :

  # ******************************************
  # ******************************************
  def __init__ ( self ) :
    self.Tabel_Name               = ''
    self.Extra_Create_Information = None

  # ******************************************
  # ******************************************
  def Read_Attribs ( self, Section, post = '' ) :
    """
    Reads attributes from the inifile.
    For the inifile "key+post" is used as the key value.
    Sets self.Attributes
    """
    self.Ini.Section = Section.lower()
    N = 0
    for key, value in self.Attribs.iteritems() :
      if value[0] == str :
        line = self.Ini.Read_String  ( key+post , value[1] )
        #v3print ( '*******************', key, value[1], line)
      elif value[0] == bool :
        line = self.Ini.Read_Bool    ( key+post , value[1] )
      elif value[0] == int :
        line = self.Ini.Read_Integer ( key+post , value[1] )
      elif value[0] == list :
        line = self.Ini.Read_String  ( key+post , value[1] )
        #EVENTJES
        #if isinstance ( line, basestring ) :
        #  line = line.replace( "'", "\\" )
      else :
        v3print ( 'EEEROR, unknown type ', key, value )

      setattr ( self, key, line )
      #v3print ( 'SET ATTRIB', key, line )

    #for item in dir ( self ) :
    #  v3print ( item, '=', getattr ( self, item ) )

  # ******************************************
  # ******************************************
  def Get_Table_Def ( self, Table_Name = '' ) :
    """
    Creates a Table Definition from self.Attribs,
    This Table Definition can be used to create a database table.
    If ID_Column has a value, the first element of the table
    will be and AutoIncrement Primary Key with that name.
    """
    if Table_Name :
      self.Table_Name = Table_Name
      
    Table_Def = [ self.Table_Name ]
    if self.ID_Column :
      line = self.ID_Column + ' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT'
      Table_Def.append ( line )
    
    keys = self.Attribs.keys ()
    keys.sort()
    N = 0
    for key in keys :
      N = max ( N, len ( key ) )

    for key in keys :
      value = self.Attribs [ key ]
      line =  '"'+ key + '" '

      # make all names equal length
      M = N + 4 - len ( line )
      line += M * ' '

      if value[0] == int :
        line += 'INTEGER'
      elif value[0] == float :
        line += 'REAL'
      else :
        line += 'TEXT'

      # make all names equal length
      M = N + 14 - len ( line )
      line += M * ' '

      if (len ( value ) > 2 ) and value [2] :
        line += ' NOT NULL'

      if (len ( value ) > 3 ) and value [3] :
        line += ' PRIMARY KEY'

      Table_Def.append ( line )

    # if more than 1 primary key in SQLITE,
    # we must the special Primary Key definition
    # but this item can be used for all kind of specials
    try:
      if self.Extra_Create_Information :
        Table_Def.append ( self.Extra_Create_Information )
    except :
      pass

    return Table_Def

  # ******************************************
  # ******************************************
  def Do_SQL_Insert ( self, DB, Table_Name = None ) :
    SQL = self.Get_SQL_Insert ( Table_Name )
    print 'DO_SQL',SQL
    Data, RowID = DB.Do_SQL ( SQL )

    SQL = 'SELECT ' + self.ID_Column + ' FROM "' + Table_Name + '" ' +\
          'WHERE ROWID = ' + str ( RowID )
    Data, RowID = DB.Do_SQL ( SQL )

    # Try to return the found ID-value
    #v3print ( '****** ROWID ', SQL, Data )
    if Data :
      return Data [1][0]

  # ******************************************
  # ******************************************
  def Get_SQL_Insert ( self, Table_Name ) :
    if not ( Table_Name ) :
      Table_Name = self.Table_Name

    # If no primary key,
    # insert number in first column for autoincrement Primary Key
    SQL = 'INSERT OR REPLACE INTO "' + Table_Name + \
          '" VALUES ( Null,'

    keys = self.Attribs.keys ()
    keys.sort()
    for key in keys :
      attr = getattr ( self, key )
      ta = type ( attr )

      if ta == int :
        pass #line += 'INTEGER'
      elif ta == float :
        pass #line += 'REAL'
      else :
        #EVENTHES
        if isinstance ( attr, basestring ) :
          attr = attr.replace ( "'", "\\" )

        attr = "'" + str(attr) + "'"

      #v3print ( '&&' + str(attr) + '&&', type (attr) )
      SQL += str(attr) + ','
    SQL = SQL [ :-1 ] + ')'
    return SQL

  # ******************************************
  # ******************************************
  def Print ( self, Title = None ) :
    if not ( Title ) :
      Title = self.Name
    v3print ( '\n----- ' + Title + ' -----' )

    keys = self.Attribs.keys ()
    keys.sort()

    N = 0
    for key in keys :
      N = max ( N, len ( key ) )

    keys.sort()
    for key in keys :
      line = key
      M = N - len ( key )
      v3print ( ' ', key, M*' ', '=', getattr ( self, key ) )
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class _DB_Column ( object ) :
  def __init__ ( self, field ) :
    self.Name    = field [1]
    self.Type    = field [2]
    self.Null    = field [3] == 0
    self.Default = field [4]
    self.PrimKey = field [5] == 1

  def __repr__ ( self ) :
    line = self.Name
    line += '  '    + self.Type
    if self.PrimKey :
      #line += '  PrimKey=' + str ( self.PrimKey )
      line += '  PrimKey'
    if not ( self.Null ) :
      #line += '  Null='    + str ( self.Null    )
      line += '  NOT-Null'
    if self.Default:
      line += '  Default=' + str ( self.Default )
    return line
    
  #__str__ = __repr__
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class _DB_Table ( object ) :
  def __init__ ( self, dbase, name, fields ) :
    self.Dbase = dbase
    self.Name  = name
    # When reading the metadata of a database,
    # for each table, a Table object is created with
    # DB_Table ( dbase, TableName, Fields )
    # where Fields is a list of column information
    #    CID  ColName   ColType    Not Null  Default   PrimKey
    #  [ ( 0, u'Veld1', u'TEXT',       99,   None,     1 ),
    #    ( 1, u'Veld2', u'TEXT',        0,   None,     0 ),
    #    ( 2, u'Veld3', u'NVARCHAR(3)', 0,   None,     0 ) ]
    self.Columns = []
    if fields :
      """
      self.Columns = {}
      for field in fields :
        self.Columns [ field [1] ] = {
          'Type'    : field [2]      ,
          'Null'    : field [3] == 0 ,
          'Default' : field [4]      ,
          'PrimKey' : field [5] == 1 }
      """
      # Dictionary is not good, because the order is lost !!
      for field in fields :
        self.Columns.append ( _DB_Column ( field ) )
      # Make the table an attribute of the Database object
      # Should be better placed in the Database object
      # The advantage of placing it here,
      #   that it's database-type independant
      setattr ( self.Dbase, self.Name, self )

  # *********************************
  # *********************************
  def __repr__ ( self ) :
    line = '**** Table ' + self.Name
    line += ' of DataBase ' + self.Dbase.DataBase_Name +'\n'
    for col in self.Columns :
      line += '  ' + str ( col ) + '\n'
    return line
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Binding_Table ( object ) :
  def __init__ ( self, DB, col1, col2, col3 = None ) :
    self.DB         = DB
    self.Table_Name = col1 + '_' + col2
    if col3 :
      self.Table_Name += '_' + col3
    
    Table_Def = [ self.Table_Name ]
    Table_Def.append ( '"' + col1 + '" INTEGER  NOT NULL' )
    Table_Def.append ( '"' + col2 + '" INTEGER  NOT NULL' )
    if col3 :
      Table_Def.append ( '"' + col3 + '" INTEGER  NOT NULL' )
    DB.Create_Table ( Table_Def, drop = True )

  def Add ( self, ID1, ID2, ID3 = None ) :
    SQL = 'INSERT OR REPLACE INTO "'+ self.Table_Name + '" VALUES (' + \
           str ( ID1 ) + ',' + str ( ID2 ) + ')'
    if ID3 :
      SQL = SQL [ : -1 ]
      SQL += ',' + str ( ID3 ) + ')'
    self.DB.Do_SQL ( SQL )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class _DataBase ( object ) :

  # *************************************************************
  # Connects to the database
  # *************************************************************
  def __init__ ( self, filename ) :
    self.DataBase_Name = filename
    self._Connect ()
    self.Tables = {}
    self.MetaData = self.Get_MetaData ()
    self.Auto_Commit = True
    
    # Make the tables available as attributes
    #for Table in self.Tables :
    #  setattr ( self, Table, )
    
  def Create_Table ( self, defs, drop = None ) :
    """
    If the table already exists, the drop argument determines what to do
      - None  : ask the user
      - True  : drop the table and create a new one
      - False : keep the current table
    """
    Table_Name = defs [0].replace ( '[', '' ).replace ( ']', '')
    if self.Has_Table ( Table_Name ) :
      #print "EEEEERRRROR, table already exists", Table_Name
      #NoGUI_AskYesNo ( 'Some Question', Title = 'Please answer this question' )

      if drop :
        SQL = 'DROP TABLE "' + Table_Name + '"'
        self.Do_SQL ( SQL )
      elif drop == None :
        return # ask the user
      else :
        return

    """
Table_Def_VraagList = [ '[VraagList33]' ,
  '[Col11]  TEXT   NOT NULL   PRIMARY KEY ' ,
  '[Col4]   TEXT       NULL               ' ,
  '[Col5]   TEXT       NULL               ' ,
  '[Col2]   TEXT       NULL               ' ,
  '[Col3]   TEXT       NULL               ' ]
"""
    # Creation of a new table
    #print 'CREATTETTT'
    SQL = "CREATE TABLE [" + Table_Name + "] ("
    for column in defs [ 1: ] :
      # remove multiple spaces
      while column.find ( '  ' ) >= 0 :
        column = column.replace ( '  ', ' ' )
      column = column.split ( ' ' )
      column[0] = column[0].replace ( '[', '' ).replace ( ']', '')
      column = ' '.join ( column )
      SQL += column + ','
    # replace the last comma with a bracket
    SQL = SQL[:-1] + ')'
    self.Do_SQL ( SQL )
    #self.conn.commit ()

    """ DIT VREET TIJD, ALLEEN DE METADATA VAN DE TABLE REFRESHEN !!!"""
    # Refresh the MetaData
    self.MetaData = self.Get_MetaData ()

  def Print_Metadata ( self ) :
    for group in self.MetaData :
      # only if there's ore than the header
      if len ( self.MetaData [group] ) > 1 :
        v3print ( '*****   Group =', group + 's' )
        # print header
        #v3print ( '      ', self.MetaData [group][0] )
        column_header = self.MetaData [group][0]
        # print elements
        for table in self.MetaData [group] [ 1: ] :
          v3print ( '**** Table =', table[0] )
          for i, item in enumerate ( table [1:-1] ) :
            v3print ( item )
          if table[-1] :
            v3print ( '   ', column_header )
            for i, item in enumerate ( table [ -1 ] ) :
              v3print ( '   ', item )

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class _SQLITE ( _DataBase ) :

  def _Connect ( self ) :
    # ensure filename has a complete path !!
    # because we don't know the active directory when saving
    filepath, filename = path_split ( self.DataBase_Name )
    if filepath == '' :
      filepath = os.getcwd()
    self.filename = os.path.join ( filepath , self.DataBase_Name )

    # *************************************************************
    # file start:  "SQLite format 3"
    import sqlite3
    self.conn = sqlite3.connect ( self.filename )
    # *************************************************************

  # ****************************************************************
  # Executes an SQL statement on the connected database
  # and returns the result
  # the first row of the result is the column header = field name
  # ****************************************************************
  def Do_SQL ( self, SQL ) :
    # create cursor, execute SQL and fetch all results
    cursor = self.conn.cursor ()
    try :
      cursor.execute ( SQL )
      self.Last_RowID = cursor.lastrowid
      #v3print ( 'ROWID =', self.Last_RowID )
    except :
      #if _DB_Debug :
      from PyLab_Works_Globals  import format_exception
      print format_exception ( globals )
      exprint ( 'DEBUG DBASE, SQL =\n', SQL )
      return None, None
    
    if self.Auto_Commit :
      # only SELECT doesn't need a commit
      if not ( SQL.strip().lower().startswith ('select') ) :
        self.conn.commit ()

    result = cursor.fetchall ()

    # we always want a header, also if the table is empty
    try:
      header = []
      for item in cursor.description :
        header.append ( item[0] )
      result.insert ( 0, header )
    except :
      pass
    
    # close cursor and dbase
    cursor.close ()
    #v3print  ( '8888', cursor.description, result, self.Last_RowID )
    return result, self.Last_RowID


  # *************************************************************
  # *************************************************************
  def Has_Table ( self, name ) :
    return name in self.Tables


  # *************************************************************
  # *************************************************************
  def Get_MetaData_Table ( self, Table_Name, Print = False ) :
    cursor = self.conn.cursor()
    SQL = 'Pragma table_info("' + Table_Name + '")'
    cursor.execute ( SQL )
    Table_Info = cursor.fetchall()

    if Print :
      v3print ( '***** Table Info :', Table_Name )
      for Field in Table_Info :
        v3print ( ' ', Field )
      
    return Table_Info

  # *************************************************************
  # *************************************************************
  def Get_MetaData ( self ) :
    cursor = self.conn.cursor()
    SQL = "SELECT * FROM sqlite_master WHERE Type='table' ORDER BY Name"
    cursor.execute ( SQL )
    tables = cursor.fetchall()

    """  CONTENTS OF sql_master
    0- Type     : table / view / ...
    1- name     :
    2- tbl_name : Name of the table       <=====
    3- rootpage : rootpage, internal to SQLite
    4- sql      : The SQL statement,
                 which would create this table. Example:
    """

    result = {}
    self.Tables = {}
    GroupName = 'Table'
    result [ GroupName ] = [
      [ 'Prim Key', 'Name', 'Type', 'NotNull', 'Default' ] ]
    for table in tables :
      # append:   TableName, TableSQL, Children
      result [ GroupName ].append (
        [ table [2], table[4].replace ( '\r', '' ), [] ] )

      # Add Table and all it's information to the dictionary
      # 0 : CID
      # 1 : Column Name
      # 2 : Column Type
      # 3 : Not Null
      # 4 : Default Value
      # 5 : Primary Key

      SQL = 'Pragma table_info("' + table[2] + '")'
      cursor.execute ( SQL )
      fields = cursor.fetchall()

      self.Tables [ table [2] ] = _DB_Table ( self, table [2], fields )

      for field in fields :
        result [ GroupName ] [-1] [-1].append (
          [ field[5], field[1], field[2], field[3], field[4] ] )
          # prim-key, name    , type    , not-null, default


    for GroupName in _DB_Groups [ 1: ] :
      SQL = "SELECT * FROM sqlite_master WHERE Type='" + GroupName.lower() + "' ORDER BY Name"
      cursor.execute ( SQL )
      items = cursor.fetchall()
      result [ GroupName ] = [
        [ 'Name', 'Table-Name ??', 'Index ??', 'Create-SQL' ] ]

      SQL = "SELECT * FROM sqlite_master WHERE Type='" + GroupName.lower() + "' ORDER BY Name"
      cursor.execute ( SQL )
      items = cursor.fetchall()
      for item in items :
        # append:   TableName, TableSQL, Children
        result [ GroupName ].append (
          [ item[1], item[2], [], item[3], item[4] ] )

    #for item in result :
    #  print 'XXLL',item,result[item]
    return result
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class _ODBC ( _DataBase ) :

  def _Connect ( self ) :
    import pyodbc
    v3print ( 'Open ODBC',self.DataBase_Name )
    #self.conn = pyodbc.connect ( "DSN=aap" )
    self.conn = pyodbc.connect ( "DSN=" + self.DataBase_Name )
    self.MetaData = self.Get_MetaData ()

  # ****************************************************************
  # Executes an SQL statement on the connected database
  # and returns the result
  # the first row of the result is the column header = field name
  # ****************************************************************
  def Do_SQL ( self, SQL ) :
    # create cursor, execute SQL and fetch all results
    cursor = self.conn.cursor ()
    print 'ODBC Do_SQL, SQL ='
    print ' **** ', SQL
    cursor.execute ( SQL )
    result = cursor.fetchall ()
    self.Last_RowID = None
    #v3print ( 'ROWID =', self.Last_RowID )

    # get the column headers
    header = []
    for item in cursor.description :
      header.append ( item[0] )
    result.insert ( 0, header )

    # close cursor and dbase
    cursor.close ()
    return result, self.Last_RowID


  # *************************************************************
  # *************************************************************
  def Get_MetaData ( self ) :
    # ****************************************************************
    # Meta data
    # ****************************************************************
    # we need a second cursor, to get the cols of each table
    cursor  = self.conn.cursor()
    cursor2 = self.conn.cursor()

    result = {}
    self.Tables = {}
    skipped = []

    for GroupName in _DB_Groups :
      result [ GroupName ] = [
        [ 'Prim Key', 'Name', 'Type', 'NotNull', 'Default' ] ]

      tables = cursor.tables ()
      for table in cursor.tables():
        #v3print ( 'Table:', table.table_type,table.table_name )
        if table.table_type.lower() == GroupName.lower() :
          #print table.table_name     # TableName
          #print table.table_schem    # None
          #print table.table_cat      # Database_Name / FileName
          #print table.remarks        # None

          # append:   TableName, TableSQL, Children
          result [ GroupName ].append (
            [ table.table_name, 'SQL-Create = ...', [] ] )

          # Get all field attributes
          fields = cursor2.columns ( table = table.table_name )
          """
           cols (
           0: u'C:/Documents and Settings/Administrator/My Documents/db1',
           1: None,
           2: u'Employees',
           3: u'EmployeeID',
           4: 4,
           5: u'COUNTER',
           6: 10,
           7: 4, 0, 10, 0, None, None, 4, None, None, 1, u'NO', 1)
          """
          #self.Tables [ table.table_name ] = \
          #  _DB_Table ( self, table.table_name, fields )

          for field in fields :
            #print 'Fields',field[3],field[5]
            result [ GroupName ] [-1] [-1].append (
              [ 'prim?' , field[3], field[5], '??', 'def?' ] )
              # prim-key, name    , type    , not-null, default
        else :
          if not ( table.table_type.lower() in _db_groups ) and \
             not ( table.table_name in skipped ) :
            #v3print ( 'YYYLL',table.table_type,table.table_name )
            skipped.append ( table.table_name )

    #for GroupName in _DB_Groups [ 1: ] :
    #  result [ GroupName ] = [
    #    [ 'Name', 'Table-Name ??', 'Index ??', 'Create-SQL' ] ]
    # ****************************************************************

    # We can also close the cursor if we are done with it
    cursor.close()

    #for item in result :
    #  print 'XXLL',item,result[item]
    return result
# ***********************************************************************


# ***********************************************************************
# Select the correct DataBase object depending on type of database
# If the filename has no extension, an ODBC database is assumed
# ***********************************************************************
def DataBase ( filename ) :
  result = None
  if not( Platform_Windows ) or os.path.splitext ( filename ) [1] != '' :
    db_kind = DB_TYPE_SQLITE
  else :
    db_kind = DB_TYPE_ODBC

  if db_kind == DB_TYPE_SQLITE :
    result = _SQLITE ( filename )
  else :
    result = _ODBC   ( filename )
  return result
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Find_ODBC () :
  """
  test docstring in db_support.Find_ODBC
  """
  from _winreg import HKEY_CURRENT_USER, HKEY_LOCAL_MACHINE
  from _winreg import CloseKey, EnumKey, EnumValue, OpenKey, QueryInfoKey

  # ****************************************************************
  # ****************************************************************
  def _Find ( Key, SubKey ) :
    #print 'Key/SubKey',Key,SubKey
    key = OpenKey ( Key, SubKey )
    N,v,w = QueryInfoKey ( key )
    for i in range ( N ) :
      DB_Name = EnumKey ( key, i )
      #print 'DB_Name',key,i,DB_Name

      DB_Key = SubKey + '\\' + DB_Name
      #print 'Key/DB_Key',Key,DB_Key

      try:
        key_sub = OpenKey ( Key, DB_Key )
        M, v, w = QueryInfoKey ( key_sub )

        for ii in range ( v ) :
          key_value = EnumValue ( key_sub, ii )
          # NOT YET COMPLETE
          if key_value [0] in [ 'DBQ', 'Database', 'EngineName' ] :
            ODBC_DBs.append ( [ DB_Name, key_value [1] ] )
        CloseKey ( key_sub )
      except :
        if Key == HKEY_CURRENT_USER :
          print 'ODBC Database not found: HKEY_CURRENT_USER', DB_Key
        else :
          print 'ODBC Database not found: HKEY_LOCAL_MACHINE', DB_Key

    CloseKey ( key )
  # ****************************************************************


  ODBC_DBs = []

  # User ODBC dataBases
  Key = HKEY_CURRENT_USER
  SubKey = 'Software\ODBC\ODBC.INI'
  _Find ( Key, SubKey )

  # System ODBC dataBases
  Key = HKEY_LOCAL_MACHINE
  SubKey = 'Software\ODBC\ODBC.INI'
  _Find ( Key, SubKey )

  return ODBC_DBs
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
def Do_Test_2 () :
    DataBase_Name = 'aap'
    DB = DataBase ( DataBase_Name )
    #print
    DB.Get_MetaData ()
    SQL = "SELECT * FROM Employees"
    SQL = "SELECT FirstName, LastName FROM Employees"
    #  ==>  [['FirstName', 'LastName'], (u'jan', u'jannasse'), (u'gert', u'vorst')]
    #print 'XXXX',
    DB.Do_SQL ( SQL )

    #for item in DB.Get_MetaData () :
    #  print item

    for item in DB.MetaData:
      print '****',item[0]
      try :
        for table in item[3] :
          print '******',table[0]
          try :
            for field in table[3] :
              print '********',field[0]
          except :
            pass
      except :
        pass

    for item in DB.MetaData2:
      print '****',item[:-1]
      if len(item) >= 3 :
        for table in item[3] :
          print '******',table[:-1]
          if len(table[3]) >= 3 :
            for field in table[3] :
              print '********',field
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Do_Test_3 () :
    import pyodbc
    DataBase_Name = 'aap'
    DataBase_Name = 'NW'
    conn = pyodbc.connect ( "DSN=" + DataBase_Name )

    # ****************************************************************
    # Meta data
    # ****************************************************************
    # we need a second cursor, to get the cols of each table
    cursor  = conn.cursor()
    cursor2 = conn.cursor()

    tables = cursor.tables ()
    for item in tables :
      # item has:
      #     table_cat
      #     table_schem
      #     table_name
      #     table_type
      #     ???? (None)
      #
      # table_type = [ 'TABLE', 'VIEW', 'SYSTEM TABLE', 'ALIAS', 'SYNONYM',
      #                'GLOBAL TEMPORARY', 'LOCAL TEMPORARY', ... ]
      #
      if item.table_type == 'TABLE' :
        #print 'Table =',item.table_name

        cols = cursor2.columns ( table = item.table_name )
        #for col in cols :
        #  print '  Column =', col.column_name
    # ****************************************************************
    # print cursor.description

    DB.Get_MetaData ()
# ***********************************************************************


from sqlobject import *



Table_Def_VraagList = [ 'VraagList' ,
  '[Col1] TEXT PRIMARY KEY NOT NULL' ,
  '[Col4] TEXT NULL' ,
  '[Col5] TEXT NULL' ,
  '[Col2] TEXT NULL' ,
  '[Col3] TEXT NULL' ]

# ***********************************************************************
# for test, read and print some ini file
# ***********************************************************************
if __name__ == '__main__':

  Test_Defs ( 1 )

  # *******************************
  # *******************************
  if Test ( 1 ) :
    DataBase_Name = '../PyLab_Works/TO_pat.db'
    DB = DataBase ( DataBase_Name )
    Meta_Data = DB.Get_MetaData ()

    for item in _DB_Groups :
      if item in Meta_Data :
        print '*******', item + 's', '********'
        Group = Meta_Data [ item ]
        Header = Group [0]
        for table in Group [1:] :
          print item, ':', table[0]
          print '  ==>', table[1]
          print ' Fields:', Header
          for field in table[2] :
            print '  ', field

    #SQL = "SELECT * FROM Change_PatList"
    #print DB.Get_Data ( SQL )

    #DataBase_Name = 'aap'
    #DB = DataBase ( DataBase_Name )
    #for item in DB.Get_MetaData () :
    #  print item

  # *******************************
  # *******************************
  if Test ( 2 ) : Do_Test_2 ()

  # *******************************
  # basic testing of ODBC databases
  # *******************************
  if Test ( 3 ) : Do_Test_3 ()

  # *******************************
  # *******************************
  if Test ( 4 ) :
    ODBC_DBs = Find_ODBC ()
    for item in ODBC_DBs :
      print item


  """
  if Test ( 5 ) :
    DataBase_Name = 'D:/Data_Python_25/support/test_vl.db'

    #import sqlite3
    #Conn = sqlite3.connect( DataBase_Name )
    #print Conn
    #DataBase_Name = 'test_vl.db'
    sqlhub.processConnection = connectionForURI ( 'sqlite:/' + DataBase_Name )

    class Test_Create ( SQLObject ) :
      class sqlmeta :
        fromDatabase = True

    #TCreate2.createTable ()

  if Test ( 7 ) :
    DataBase_Name = 'D:/Data_Python_25/support/test_vl.db'
    DataBase_Name = 'test_vl.db'
    from elixir import *
    metadata.bind = "sqlite:///" + DataBase_Name
    metadata.bind.echo = True
  """
    
  # *******************************
  # TestOrganizer aggregatie
  # *******************************
  if Test ( 5 ) :
    print 'TO-aggregatie'
    Base_Dir     = 'D:/d_midorg/'
    Protocol_Dir = Base_Dir + 'Protocol/'
    Data_Dir     = Base_Dir + 'mid-data/'

    # Find all vragenlijsten
    VLs = Find_Files ( Protocol_Dir + 'VraagLST/', '*.vli', True )
    for VL in VLs :
      print VL

    # Find all answers to vragenlijst
    # er zijn ook nog de volgende extensies
    #    .mem
    #    .geg
    #    .<number>
    Answer_Dir = Data_Dir + 'VraagLst/' + 'aap/'
    Answers = Find_Files ( Answer_Dir, '*.dat', True )
    for Answer in Answers :
      print Answer

    # Connect to New database
    DataBase_Name = 'D:/Data_Python_25/support/test_vl.db'
    DB = DataBase ( DataBase_Name )
    DB.Get_MetaData ()

    for item in DB.Tables :
      print item

    # if Table doesn't exists, create it now
    Table_Name = 'Test_Create2'
    if not ( Table_Name in DB.Tables ) :
      # Create a table
      SQL = """CREATE TABLE [""" + Table_Name + """] (
[Veld1] TEXT  PRIMARY KEY NOT NULL,
[Veld2] TEXT  NULL,
[Veld3] NVARCHAR(3)  NULL
)
"""
      DB.Do_SQL ( SQL )


    ##   ROWID:=SQL_table.FieldAsInteger(SQL_table.FieldIndex['ID']);
    #VraagList = DB_Table ( DB, Table_Def_VraagList )
    print DB.VraagList


    # Add some records
    SQL = "INSERT INTO 'test_create2' (Veld1,Veld2,Veld3) VALUES ('66','aapje','XX')"
    #DB.Get_Data ( SQL )
    SQL = "SELECT * FROM NewCol"
    cursor = DB.conn.cursor()
    print cursor.execute ( SQL )
    DB.conn.commit ()
    result = cursor.fetchall ()
    cursor.close()
    print 'Done ', result
    
    
# ***********************************************************************
pd_Module ( __file__ )
