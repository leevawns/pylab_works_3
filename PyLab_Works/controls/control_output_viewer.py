import __init__
from base_control import *

from   PyLab_Works_Globals import _
import PyLab_Works_Globals as PG
import wx
import sys
from   gui_support     import *
#from   grid_support    import *
from   picture_support import Get_Image_List
from   menu_support    import My_Popup_Menu
import  wx.grid as gridlib


# ***********************************************************************
# ***********************************************************************
class t_C_Cmd_Shell ( My_Control_Class ):
  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )
    self.Icon = 206

    GUI = """
    P1                 ,PanelVer ,10  ,name = 'Shell'
      self.Log         ,Base_STC
      P2               ,wx.Panel
        self.CB_StdOut ,wx.CheckBox   ,label='StdOut' ,pos = ( 0, 0 )
        self.CB_StdErr ,wx.CheckBox   ,label='StdErr' ,pos = ( 60, 0 )
        self.CB_AutoC  ,wx.CheckBox   ,label='AutoComplete' ,pos = ( 120, 0 )
    """
    self.wxGUI = PG.Create_wxGUI ( GUI, my_parent = 'self.Dock' )

    self.Log.Set_Wrap ()
    self.Log.Execute_Code  = self.Execute_Code

    self.Dock.Bind ( wx.EVT_CHECKBOX, self.Toggle_StdOut, self.CB_StdOut )
    self.Dock.Bind ( wx.EVT_CHECKBOX, self.Toggle_StdErr, self.CB_StdErr )

    self.FileName = None

  # ********************************************************
  # ********************************************************
  def GetName ( self ) :
    return 'Shell'

  # *******************************************************
  # override Scintilla's execute code
  # *******************************************************
  def Execute_Code ( self ) :
    line =  str ( self.Log.Code_To_Execute )
    #print 'MEMOCODE:',line

    if line.find ( '>' ) == 0 :
      # command handling not yet supported
      pass

    else :
      if line.find ( '?' ) == 0 :
        line = 'help(' + line [ 1: ] + ')'
      if line.find ( 'help' ) != 0 :
        self.Log.AppendText ( '  ==> ' )
      #print 'oooiii',line,'$$'
      #print line
      try :
        result = eval ( line, PG.P_Globals )
        self.Log.AppendText ( str ( result ) +'\n' )
      except :
        result = '\n'
        # split lines, and remove the last (empty) line
        lines = line.split ( '\n' ) [ : -1 ]
        # test if it's an assignment
        i = lines [ -1 ].rfind ( '=' )
        if i > 0 :
          result = lines [ -1 ] [ : i+1 ] + ' '
          self.Log.AppendText ( result )
          # get the first var on the left of the assignment
          i = lines [ -1 ].find ( '=' )
          result = 'print ' + lines [ -1 ] [ : i ] + '\n'
          #print '$$' + line + result + '$$\n'
        exec ( line + result, PG.P_Globals )

  # *************************************************************
  # *************************************************************
  def Toggle_StdOut ( self, event = None ) :
    print ('XXFFGG')
    if self.CB_StdOut.GetValue () :
      PG.Set_StdOut ( self.Log )
    else :
      PG.Restore_StdOut ( self.Log )


  # *************************************************************
  # *************************************************************
  def Toggle_StdErr ( self, event = None ) :
    if self.CB_StdErr.GetValue () :
      PG.Set_StdErr ( self.Log )
    else :
      PG.Restore_StdErr ( self.Log )


  # *************************************************************
  def Kill ( self ) :
    PG.Restore_StdOut ( self.Log )
    PG.Restore_StdErr ( self.Log )

  # *************************************************************
  # This function is called by stdout / stderr
  # *************************************************************
  def write ( self, line ) :
    # Do not put a print statement here !!
    self.Log.AppendText ( line )

  # *************************************************************
  # *************************************************************
  def Set_FileName ( self, FileName ) :
    if FileName != self.FileName :
      self.Save_Settings ( Dont_Create_New = True )
      self.FileName = FileName
      self.Load_Settings ()

  # *************************************************************
  def Save_Settings ( self, ini = None, key = None, Dont_Create_New = False ) :
    """ Save the content of the Logged Data
    and the settings into files."""
    if not ( key ) :
      key = 'CS_'
    print ('kkkLOP')
    # Dont store anything, if nothing known
    if Dont_Create_New and \
       not ( self.Log.Filename ) and \
       not ( self.FileName ) :
      return

    from file_support import Force_Dir
    path = os.path.join ( Application.Dir, PG.Active_Project_Filename )
    path = os.path.normpath ( path)
    Force_Dir ( path, init = True )

    # Try to get a name to store logged data
    if not ( self.FileName ) :
      if self.Log.Filename :
        self.FileName = self.Log.Filename
      else :
        from dialog_support import Ask_File_For_Save
        filename = Ask_File_For_Save (
          DefaultLocation = path,
          DefaultFile = 'new.pcmd',
          FileTypes = '*.pcmd',
          Title = 'Save CMD_Shell as ...' )
        if filename :
          self.FileName = self.Log.Filename = filename

    # Store Logged data and re-assign inifile
    if self.FileName :
      filename = Change_FileExt ( self.FileName, 'pcmd')
      self.Log.SaveFile ( filename )
      filename = Change_FileExt ( self.FileName, 'pwp')
      ini = inifile ( filename )
      ini.Section = ' CMD-Shell'

    # Store other settings in inifile
    print ('POLP',ini)
    if ini :
      line = []
      line.append ( self.CB_StdOut.GetValue () )
      line.append ( self.CB_StdErr.GetValue () )
      line.append ( self.CB_AutoC.GetValue () )
      ini.Write ( key, line )

      ##Help_Files = self.Html.Combo.GetItems ()
      ##ini.Write ( 'CS_Help_Files', Help_Files )
      ##ini.Write ( 'CS_Help_Actual', self.Html.Combo.GetValue () )

    # if inifile was reassigned, close it
    if self.FileName :
      ini.Close ()

  # *************************************************************
  # *************************************************************
  def Load_Settings ( self, ini = None, key = None ) :
    """ Restore logged data and settings from files.
    """
    print (' LJDGYSDU load setiing')
    if not ( self.FileName ) :
      if self.Log.Filename :
        self.FileName = self.Log.Filename

    # Restore Logged data and re-assign inifile
    if self.FileName :
      filename = Change_FileExt ( self.FileName, 'pcmd')
      self.Log.LoadFile ( filename )
      filename = Change_FileExt ( self.FileName, 'pwp')
      ini = inifile ( filename )
      ini.Section = ' CMD-Shell'
    else :
      self.Log.ClearAll ()
    self.Log.DocumentEnd ()

    if ini :
      # *********************************************
      # read the normal settings
      # *********************************************
      if not ( key ) :
        key = 'CS_'
      line = ini.Read ( key, [] )
      print ('XXFFGG33', line)
      while len (line) < 3 :
        line.append ( False )
      if line :
        self.CB_StdOut.SetValue ( line[0] )
        self.CB_StdErr.SetValue ( line[1] )
        self.CB_AutoC.SetValue  ( line[2] )
        if line[0] : self.Toggle_StdOut ( None )
        if line[1] : self.Toggle_StdErr ( None )

      """
      Help_Files = ini.Read ( key + 'Help_Files', [] )
      for URL in Help_Files :
        self.Html._URL_In_History ( URL )
      URL = ini.Read ( key + 'Help_Actual', '' )
      if URL :
        self.Html.Load ( URL )
      else :
        self.Html.Load ( 'http://www.python.org' )
      """
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_C_Doc_Viewer ( My_Control_Class ):
  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )
    self.Icon = 25

    GUI = """
    self.Html          ,Class_URL_Viewer   ,name='Help'
    """
    self.wxGUI = PG.Create_wxGUI ( GUI, my_parent = 'self.Dock' )

    self.FileName = None
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class tCMD_Shell_Doc_DOESNT_SUCCEED ( My_Control_Class ):
  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    GUI = """
    self.NB              ,wx.Notebook   ,style = wx.BK_LEFT
      self.CMD_Shell     ,tCMD_Shell
      self.Html          ,tDoc_Viewer
    """
    self.wxGUI = PG.Create_wxGUI ( GUI, my_parent = 'self.Dock' )

    self.My_Group = [ self.CMD_Shell, self.Html ]

    Set_NoteBook_Images ( self.NB, ( self.CMD_Shell.Ico, self.Html.Icon ) )

    self.FileName = None

  # *******************************************************
  def Kill ( self ) :
    for member in self.My_Group :
      if ('Kill' in dir ( member ) ) and \
         ismethod ( member.Kill ) :
        member.Kill ()

  # *******************************************************
  def Set_FileName ( self, FileName ) :
    for member in self.My_Group :
      if ('Set_FileName' in dir ( member ) ) and \
         ismethod ( member.Set_FileName ) :
        member.Set_FileName ( FileName )

  # *******************************************************
  def Save_Settings ( self, ini = None, key = None, Dont_Create_New = False ) :
    if not ( key ) :
      key = 'CS_'
    for member in self.My_Group :
      if ('Save_Settings' in dir ( member ) ) and \
          ismethod ( member.Save_Settings ) :
        member.Save_Settings ( ini, Dont_Create_New )

  # *******************************************************
  def Load_Settings ( self, ini = None, key = None ) :
    if not ( key ) :
      key = 'CS_'
    for member in self.My_Group :
      if ('Load_Settings' in dir ( member ) ) and \
         ismethod ( member.Load_Settings ) :
        member.Load_Settings ( ini )

# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class t_C_Cmd_Shell_Doc ( My_Control_Class ):
  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    GUI = """
    self.NB              ,wx.Notebook   ,style = wx.BK_LEFT
      P1                 ,PanelVer ,10  ,name = 'Shell'
        self.Log         ,Base_STC
        P2               ,wx.Panel
          self.CB_StdOut ,wx.CheckBox   ,label='StdOut' ,pos = ( 0, 0 )
          self.CB_StdErr ,wx.CheckBox   ,label='StdErr' ,pos = ( 60, 0 )
          self.CB_AutoC  ,wx.CheckBox   ,label='AutoComplete' ,pos = ( 120, 0 )
      self.Html          ,Class_URL_Viewer ,name = 'Help'
      self.Grid          ,Base_Grid        ,name = 'File'
    """
    self.wxGUI = PG.Create_wxGUI ( GUI, my_parent = 'self.Dock' )

    self.Log.Set_Wrap ()
    self.Log.Execute_Code  = self.Execute_Code

    #self.Html.Load_CSS ( 'html/pw_demos.html' )
    #self.Html.LoadUrl ( 'html/pw_demos.html' )
    Set_NoteBook_Images ( self.NB, ( 206, 25, 9) )


    # *******************************************************
    # *******************************************************
    self.Grid.SetLabelBackgroundColour ( ( 200, 200, 200 ) )
    columns = [ 'field' ]
    #self.Grid.CreateGrid ( 0, len ( columns ), gridlib.Grid.SelectRows )
    #self.Grid.SetSelectionMode ( gridlib.Grid.SelectCells )
    self.Grid.CreateGrid ( 1, 1, gridlib.Grid.SelectCells )

    for i, name in enumerate ( columns ) :
      self.Grid.SetColLabelValue ( i, name )

    self.Grid.SetRowLabelSize ( 0 )
    self.Grid.SetColLabelAlignment ( wx.ALIGN_LEFT, wx.ALIGN_CENTRE )
    self.Grid.SetColLabelSize ( 20 )

    #self.Grid.SetDefaultRowSize ( 8, True )  ##DONT USE !!
    MH = 8
    self.Grid.SetRowMinimalAcceptableHeight ( MH )
    self.Grid.EnableEditing ( True ) #False )
    self.Grid.DisableDragRowSize ( )

    # Create instances of cols, rows, to handle properties
    #self.columns = _Table_Columns ( self )
    #self.rows    = _Table_Rows    ( self )
    # *******************************************************

    self.Dock.Bind ( wx.EVT_CHECKBOX, self.Toggle_StdOut, self.CB_StdOut )
    self.Dock.Bind ( wx.EVT_CHECKBOX, self.Toggle_StdErr, self.CB_StdErr )

    self.FileName      = None
    self.Grid_FileName = None

    # Bug in combination of NoteBook and AUI-Pane
    # depending on number of tabs, sizing is not correctly
    # So after everything has settled we resize again
    wx.CallLater ( 500, self.NB.SendSizeEvent )
    self.Grid.Bind ( gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell )

    # *************************************************************
    # find all Python files, and split them into categories
    # place these in the grid
    # *************************************************************
    path = os.path.join ( Application.Dir, PG.Active_Project_Filename )
    print ('**************%%%%%%%%%%***', Application.Dir, PG.Active_Project_Filename, path)
    Py_Files = []
    Find_Files_1 ( path , Py_Files, mask = '*.py', RootOnly = True )

    file_groups = {}
    Misc = 'Misc'
    file_groups [ Misc ] = []
    for file in Py_Files :
      filnam = os.path.splitext ( file[1]) [0]
      if filnam != '__init__' :
        i = filnam.find ( '_' )
        if i > 0 :
          group = filnam [ : i ]
          if not ( group in file_groups ) :
            file_groups [ group ] = []
          file_groups [ group ] .append ( filnam [ i+1 : ] )
        else :
          file_groups [ Misc ].append ( filnam )
        
    if len ( file_groups [ Misc ] ) == 0 :
      del file_groups [ Misc ]

    MaxRows = 0
    for file in file_groups :
      NRow = len ( file_groups [ file ] )
      MaxRows = max ( NRow, MaxRows )

    C = self.Grid.GetNumberCols ()
    MaxCols = len ( file_groups )
    if MaxCols > C :
      self.Grid.AppendCols ( MaxCols - C )
    else :
      self.Grid.DeleteCols ( numCols = ( C - MaxCols ) )

    R = self.Grid.table.GetNumberRows ()
    if MaxRows > R :
      self.Grid.AppendRows ( MaxRows - R )
    else :
      self.Grid.DeleteRows ( numRows = ( R - MaxRows ) )

    C = 0
    Keys = file_groups.keys()
    Keys.sort()
    for file in Keys :
      self.Grid.SetColLabelValue ( C, file )
      R = 0
      files = file_groups [ file ]
      files.sort ()
      for filnam in files :
        self.Grid.table.SetCellValue ( R, C, filnam )
        R += 1
      C += 1
    # *************************************************************

    # TIJDELIJK
    #self.CB_StdOut.SetValue ( True )
    #self.Toggle_StdOut ()
    #self.Toggle_StdErr ()

  # *******************************************************
  # *******************************************************
  def OnSelectCell(self, evt):
    """
    If a cell in the grid is selected,
    the new filename is sent to the input channel,
    which might be connected to a code-editor.
    """
    evt.Skip()
    col = evt.GetCol ()
    row = evt.GetRow ()
    value = self.Grid.GetCellValue ( row, col )
    # If we realy selected a file,
    # pass it to the Brick
    if value :
      prefix = self.Grid.GetColLabelValue ( col )
      if prefix != 'Misc' :
        value = prefix + '_' + value
      filename = value + '.py'
      if filename != self.Grid_FileName :
        self.Grid_FileName = filename
        path = os.path.join ( Application.Dir, PG.Active_Project_Filename )
        self.Brick.Par [ self.EP[0] ][ 'CodeFile_To_Open' ] = os.path.join ( path, filename )

  # *******************************************************
  # override Scintilla's execute code
  # *******************************************************
  def Execute_Code ( self ) :
    line =  str ( self.Log.Code_To_Execute )
    #print 'MEMOCODE:',line

    if line.find ( '>' ) == 0 :
      # command handling not yet supported
      pass
    
    else :
      if line.find ( '?' ) == 0 :
        line = 'help(' + line [ 1: ] + ')'
      if line.find ( 'help' ) != 0 :
        self.Log.AppendText ( '  ==> ' )
      #print 'oooiii',line,'$$'
      #print line
      try :
        result = eval ( line, PG.P_Globals )
        self.Log.AppendText ( str ( result ) +'\n' )
      except :
        result = '\n'
        # split lines, and remove the last (empty) line
        lines = line.split ( '\n' ) [ : -1 ]
        # test if it's an assignment
        i = lines [ -1 ].rfind ( '=' )
        if i > 0 :
          result = lines [ -1 ] [ : i+1 ] + ' '
          self.Log.AppendText ( result )
          # get the first var on the left of the assignment
          i = lines [ -1 ].find ( '=' )
          result = 'print ' + lines [ -1 ] [ : i ] + '\n'
          #print '$$' + line + result + '$$\n'
        exec ( line + result, PG.P_Globals )


  # *************************************************************
  # *************************************************************
  def Set_FileName ( self, FileName ) :
    if FileName != self.FileName :
      if ( 'Load_Save' in Debug_What ) :
        Debug_Dump_Trace (
          'tCMD_Shell_Doc ( My_Control_Class ) Set_FileName',
          '\n      self.FileName =', self.FileName,
          '\n      FileName      =', FileName )

      self.Save_Settings ( Dont_Create_New = True )
      self.FileName = FileName
      self.Load_Settings ()

  # *************************************************************
  # *************************************************************
  def Toggle_StdOut ( self, event = None ) :
    if self.CB_StdOut.GetValue () :
      PG.Set_StdOut ( self.Log )
    else :
      PG.Restore_StdOut ( self.Log )

  # *************************************************************
  # *************************************************************
  def Toggle_StdErr ( self, event = None ) :
    if self.CB_StdErr.GetValue () :
      PG.Set_StdErr ( self.Log )
    else :
      PG.Restore_StdErr ( self.Log )


  # *************************************************************
  def Kill ( self ) :
    PG.Restore_StdOut ( self.Log )
    PG.Restore_StdErr ( self.Log )

  # *************************************************************
  # This function is called by stdout / stderr
  # *************************************************************
  def write ( self, line ) :
    # Do not put a print statement here !!
    self.Log.AppendText ( line )


  # *************************************************************
  def Save_Settings ( self, ini = None, key = None, Dont_Create_New = False ) :
    """ Save the content of the Logged Data
    and the settings into files."""
    if not ( key ) :
      key = 'CS_'
    if ( 'Load_Save' in Debug_What ) :
      Debug_Dump_Trace (
        'tCMD_Shell_Doc ( My_Control_Class ) Save Settings',
        '\ninifile         =', ini,
        '\nLog.Filename    =', self.Log.Filename,
        '\nself.FileName   =', self.FileName,
        '\nDont_Create_New =', Dont_Create_New )

    # Dont store anything, if nothing known
    if Dont_Create_New and \
       not ( self.Log.Filename ) and \
       not ( self.FileName ) :
      return

    from file_support import Force_Dir
    path = os.path.join ( Application.Dir, PG.Active_Project_Filename)
    path = os.path.normpath ( path)
    Force_Dir ( path, init = True )

    # Try to get a name to store logged data
    if not ( self.FileName ) :
      if self.Log.Filename :
        self.FileName = self.Log.Filename
      else :
        from dialog_support import Ask_File_For_Save
        filename = Ask_File_For_Save (
          DefaultLocation = path,
          DefaultFile = 'new.pcmd',
          FileTypes = '*.pcmd',
          Title = 'Save CMD_Shell as ...' )
        if filename :
          self.FileName = self.Log.Filename = filename

    # Store Logged data and re-assign inifile
    if self.FileName :
      filename = Change_FileExt ( self.FileName, 'pcmd')
      self.Log.SaveFile ( filename )
      filename = Change_FileExt ( self.FileName, 'pwp')
      ini = inifile ( filename )
      ini.Section = ' CMD-Shell'

    # Store other settings in inifile
    if ini :
      line = []
      line.append ( self.CB_StdOut.GetValue () )
      line.append ( self.CB_StdErr.GetValue () )
      line.append ( self.CB_AutoC.GetValue () )
      ini.Write ( key, line )

      Help_Files = self.Html.Combo.GetItems ()
      ini.Write ( key + 'Help_Files', Help_Files )

      ini.Write ( key + 'Help_Actual', self.Html.Combo.GetValue () )

    # if inifile was reassigned, close it
    if self.FileName :
      ini.Close ()
    
  # *************************************************************
  # *************************************************************
  def Load_Settings ( self, ini = None, key = None ) :
    """
    Restore logged data and settings from files.
    """
    if ( 'Load_Save' in Debug_What ) :
      Debug_Dump_Trace (
        'tCMD_Shell_Doc ( My_Control_Class ) Load Settings from :',
        '\ninifile       =', ini,
        '\nLog.Filename  =', self.Log.Filename,
        '\nself.FileName =', self.FileName )

    if not ( self.FileName ) :
      if self.Log.Filename :
        self.FileName = self.Log.Filename

    # Restore Logged data and re-assign inifile
    if self.FileName :
      filename = Change_FileExt ( self.FileName, 'pcmd')
      self.Log.LoadFile ( filename )
      filename = Change_FileExt ( self.FileName, 'pwp')
      ini = inifile ( filename )
      ini.Section = ' CMD-Shell'
    else :
      self.Log.ClearAll ()
    self.Log.DocumentEnd ()

    #print 'IIIINi',ini.Filename

    if ini :
      # *********************************************
      # read the normal settings
      # *********************************************
      if not ( key ) :
        key = 'CS_'
      line = ini.Read ( key, [] )
      print ('rtwwwtt',line,ini.Filename)
      while len (line) < 3 :
        line.append ( False )
      if line :
        self.CB_StdOut.SetValue ( line[0] )
        self.CB_StdErr.SetValue ( line[1] )
        self.CB_AutoC.SetValue  ( line[2] )
        if line[0] : self.Toggle_StdOut ( None )
        if line[1] : self.Toggle_StdErr ( None )

      Help_Files = ini.Read ( key + 'Help_Files', [] )
      for URL in Help_Files :
        self.Html._URL_In_History ( URL )

      # for the moment we only start on windows
      if Platform_Windows :
        URL = ini.Read ( key + 'Help_Actual', '' )
        if URL :
          self.Html.Load ( URL )
        else :
          self.Html.Load ( 'http://www.python.org' )

# ***********************************************************************
