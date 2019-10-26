import __init__

# ***********************************************************************
from PyLab_Works_Globals import *
from PyLab_Works_Globals import _
from language_support    import Language_IDs
from system_support      import run
from tree_support        import *
from menu_support        import *
from picture_support     import *
from doc_support         import *
from inspect             import *
from Scintilla_support   import *
from pw_winpdb           import Simple_RPDB2_Debugger
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
__doc__ = """  PyLab_Works_Library_Manager
blabla

License: freeware, under the terms of the BSD-license
Copyright (C) 2008 Stef Mientki
mailto:S.Mientki@ru.nl

"""
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
_Version_Text = [
[ 0.1, '23-07-2008', 'Stef Mientki',
'Test Conditions:', ( 2, ),
"""
    - orginal release
""" ]
]
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
from   PyLab_Works_Globals import _
from   numpy import *
import wx
import wx.grid as gridlib
from   wx.lib.expando import ExpandoTextCtrl, EVT_ETC_LAYOUT_NEEDED
import  wx.lib.buttons  as  buttons
#from tree_support import Custom_TreeCtrl_Base
import time

# add some standard library paths
"""
import os
import sys
subdirs = [ '../support' ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
"""
from   inifile_support import *
from   grid_support    import *
from   gui_support     import *


# ***********************************************************************
# ***********************************************************************
def Grid_Add_Files ( dir, Grid ) :
  Py_Files = Find_Files ( dir )
  R = Grid.table.GetNumberRows ()
  Grid.AppendRows ( len ( Py_Files ) )
  for item in Py_Files :
    try :
      Grid.table.SetValue ( R, 0, item[0] )
      Grid.table.SetValue ( R, 1, item[1] )
    except :
      pass
    R += 1
# ***********************************************************************



# ***********************************************************************
class _Fetch_Output ( object ) :
  def __init__ ( self, Log ) :
    self.Memo       = Log
  def write ( self, line ) :
    #line = line.replace ( '\n', '\n>>')
    self.Memo.AppendText ( line )
    self.Memo.GotoPos ( self.Memo.GetTextLength () )
    self.Memo.EnsureCaretVisible()

class _Fetch_Error ( object ) :
  def __init__ ( self, Log ) :
    self.Memo       = Log
    self.prefix     = ''
    self.newline    = True
    self.Trace_Back = False

  # ****************************************************************
  # ****************************************************************
  def write ( self, line ) :
    """
    $$$$ execfile ( self.Source_File )

    $$$$   File "test_IDE.py", line 5, in <module>

    $$$$
    $$$$ cv

    $$$$ NameError
    $$$$ :
    $$$$ name 'cv' is not defined
    $$$$
    """
    # The first Traceback has no '\n',
    # all following Traceback have a '\n'
    # so we always remove the leading '\n'
    line = line.lstrip('\n')
    
    L = len ( line )
    indent = L - len ( line.lstrip () )
    if indent == L :
      if indent != 0 :
        self.prefix = line
      return

    line = self.prefix + line
    L = len ( line )
    indent = L - len ( line.lstrip () )

    #print 'app',indent,self.prefix,self.newline,line
    if ( indent == 0 ) and self.newline and self.Trace_Back :
      line = '#' + line
      L += 1

    B = self.Memo.GetTextLength ()
    self.Memo.AppendText ( line )

    if indent == 0 :
      self.Memo.StartStyling ( B, 0xFF )
      self.Memo.SetStyling   ( L,  self.Memo.GetStyleAt (B) | 0xE0 )
      self.Memo.Colourise ( 0, -1 )
      if self.Trace_Back :
        wx.CallLater ( 200, self._Do_Extra_NewLine )
      self.Trace_Back = line.find ('Traceback') == 0

    self.newline = line.find('\n') >= 0
    self.Memo.GotoPos ( self.Memo.GetTextLength () )
    self.Memo.EnsureCaretVisible()
    self.prefix = ''
    
  # ****************************************************************
  # ****************************************************************
  def _Do_Extra_NewLine ( self ) :
    self.Memo.AppendText ( '\n\n' )
    self.Memo.GotoPos ( self.Memo.GetTextLength () )
    self.Memo.EnsureCaretVisible()
    self.newline = True
# ***********************************************************************


Debug_Button_Start   = ( 1,  0,1,1,1,  1 )
Debug_Button_Break   = ( 1,  0,1,1,1,  1 )
Debug_Button_Running = ( 1,  1,0,0,0,  1 )
Debug_Button_Extern  = ( 0,  0,0,0,0,  0 )


# ***********************************************************************
# This is the demo part, the part you will normally incorporate in your design.
# We have to perform the following tasks:
#   - indicate which signals should become available
#   - how the signals are organized (here a simple 1 level tree is shown,
#     in the animated demo a more complex organization is shown)
#   - how the signals are generated / calculated
# This code also contains some parts that will be normally placed in the
# applications main code, at least somewhere else.
# ***********************************************************************
class my_Test_Form ( wx.MiniFrame ) :

  # *****************************************************************
  # *****************************************************************
  def __init__( self, main_form= None, ini = None ) :

    self.main_form = main_form
    FormStyle = wx.DEFAULT_FRAME_STYLE | wx.TINY_CAPTION_HORIZ
    #if parent:
    #  FormStyle = FormStyle | wx.FRAME_FLOAT_ON_PARENT    # needs a parent

    Pos = ( 100, 100 )
    self.Ini_File = ini
    self.Ini_Section = 'Library Manager'
    if ini :
      ini.Section = self.Ini_Section
      Pos  = ini.Read ( 'Pos',  ( 100, 100 ) )
      Size = ini.Read ( 'Size', ( 600, 400 ) )

    wx.MiniFrame.__init__(
        self, None, -1,
        'PyLab_Works  Library Manager    v' + str ( _Version_Text[0][0] ),
        size  = Size,
        pos   = Pos,
        style = FormStyle)

    BasePath = 'd:/Data_Python/'

    data_values = [
      [ 'Path', 'FileName', 'Version', 'Test Cases', 'Date', 'Languages',
        'Watch 4 Update', 'New Version', 'Test Cases', 'Do Update', 'Dependancies'] ]
    #for i in range (6 ):
    #  data_values.append ( 8*[''])
    #print data_values
    data_types = [
      gridlib.GRID_VALUE_STRING,
      gridlib.GRID_VALUE_STRING,
      gridlib.GRID_VALUE_STRING,
      gridlib.GRID_VALUE_STRING,
      gridlib.GRID_VALUE_STRING,
      gridlib.GRID_VALUE_STRING,
      gridlib.GRID_VALUE_BOOL,
      gridlib.GRID_VALUE_STRING,
      gridlib.GRID_VALUE_STRING,
      gridlib.GRID_VALUE_BOOL,
      gridlib.GRID_VALUE_STRING]

    data_defs = ( MY_GRID_ROW_FIXED, MY_GRID_COL_TYPED )

    TBFLAGS = ( wx.TB_HORIZONTAL
            | wx.NO_BORDER
            | wx.TB_FLAT
            #| wx.TB_TEXT
            #| wx.TB_HORZ_LAYOUT
            )

    GUI = """
    self.SplitV2               ,PanelVer, 01
      panel                    ,wx.Panel
        Button_1               ,wx.Button , label = "Test", size = ( 40, -1 )
        T1                     ,wx.StaticText, label='Language', pos = ( 50, 3 )
        self.Combo_Language    ,wx.ComboBox, pos = ( 98, 0 ), size=(50,-1), choices=Language_IDs, style = wx.CB_DROPDOWN
        self.Techno            ,wx.CheckBox, label="Techno", pos = (150, 3)
      self.SplitV              ,SplitterVer
        self.NBx                ,wx.Notebook   ,style = wx.NO_BORDER
          Panel_dummy1         ,PanelVer, 11  ,name  = 'Bricks'
            self.Grid_Bricks   ,Base_Table_Grid , data_values, data_types, data_defs
          Panel_dummy2         ,PanelVer, 11  ,name  = 'Unwanted'
            self.Grid_UnWanted ,Base_Table_Grid , data_values, data_types, data_defs
          Panel_dummy3         ,PanelVer, 11  ,name  = 'Program'
            self.Grid_Program  ,Base_Table_Grid , data_values, data_types, data_defs
          Panel_dummy4         ,PanelVer, 11  ,name  = 'Private'
            self.Grid_Private  ,Base_Table_Grid , data_values, data_types, data_defs
          Panel_dummy5         ,PanelVer, 11  ,name  = 'New'
            self.Grid_New      ,Base_Table_Grid , data_values, data_types, data_defs
          self.Split_H1        ,SplitterHor   ,name  = "Support"
            self.NB_Tree       ,wx.Notebook
              self.Tree        ,Custom_TreeCtrl_Base  ,name  = 'Py Files'
              Panel_6          ,PanelVer, 01          ,name  = 'Debug'
                run_tb           ,wx.ToolBar
                self.List_Debug  ,wx.ListCtrl   ,style = wx.LC_REPORT
            self.NB            ,GUI_Notebook
       self.Log_Cmd            ,Base_STC
    """
    #exec ( Create_wxGUI ( GUI ) )
    self.wxGUI = Create_wxGUI ( GUI ) #, IniName = 'self.Ini_File' )
    self.Log = self.Log_Cmd

    # Create the menu
    ##Create_Menus ( self )

    # *******************************************************
    # Create the run toolbar
    # *******************************************************
    ToolItems = [
      ( 83, 'Disable Breakpoints'   ),
      (                             ),
      ( 91, 'Pauze  (F9)'           ),
      ( 90, 'Run in Debugger  (F9)' ),
      ( 92, 'Step  (F8)'            ),
      ( 93, 'Step Into  (Ctrl-F8)'  ),
      (                             ),
      ( 22, 'Restart (Shift-F9)'    ),
      (                             ),
      ( 65, 'Run Extern  (Alt-F9)'  ),
    ]
    self.TB = Create_ToolBar_Items  ( run_tb, ToolItems, self.On_ToolBar, self )
    self.TB.Enable_Buttons ( Debug_Button_Start )
    self.Last_Button_Command = None
    # *******************************************************


    # *********************************************************
    self.Editors = []
    self.Image_List = Get_Image_List ()
    self.NB.SetImageList ( self.Image_List )
    self.NB.Bind ( GUI_EVT_CLOSE_PAGE, self.On_EditPage_Close )
    # *********************************************************


    # *************************************************************
    self.List_Debug.InsertColumn ( 0, 'Name'    )
    self.List_Debug.InsertColumn ( 1, 'Value'   )
    self.List_Debug.InsertColumn ( 2, 'History' )
    self.Hist_Dict = {}
    # *************************************************************

    # *************************************************************
    # MEMO settings,
    # we use the extra indicator styles for highlighting.
    # therefor we override the indicator settings
    # *************************************************************
    # only accepts old style indicators,
    # Python Lexer only allows Indicator-2
    self.Log_Cmd.IndicatorSetStyle      ( 2, stc.STC_INDIC_ROUNDBOX )
    self.Log_Cmd.IndicatorSetForeground ( 2, "BLUE" )

    self.Log_Cmd.SetWrapMode ( stc.STC_WRAP_WORD )

    self.Log_Cmd.Execute_Code  = self.Execute_Code
    # *************************************************************

    # *************************************************************
    # *************************************************************
    ##sys.stdout = _Fetch_Output ( self.Log_Cmd )
    sys.stderr = _Fetch_Error  ( self.Log_Cmd )
    # *************************************************************

    self.Combo_Language.SetSelection ( 0 )
    ##self.Log_Cmd.Bind ( wx.EVT_TEXT, self.On_Log_Text )

    # ***************************************************
    Tree = self.Tree
    #Tree.IniFile_2_Tree ( '../support/test_My_Custom_TreeCtrl.cfg' )

    #Tree.On_Sel_Changed = self.On_Tree_Sel_Changed
    import customtreectrl_SM as CT
    Tree.Bind ( CT.EVT_TREE_SEL_CHANGED,      self.On_Tree_Sel_Changed    )

    Tree.DeleteAllItems()
    Tree.root = Tree.AddRoot ( 'Root Node' )
    #Node = Tree.AppendItem ( Tree.root, ' Support'  )
    #Tree.SetItemImage ( Node, 12, CT.TreeItemIcon_Normal )
    #Tree.SetItemImage ( Node, 13, CT.TreeItemIcon_Expanded )

    underscore = '_'  # make it '_' or None
    dir = BasePath + 'support'
    Py_Files = Find_Files ( dir )
    #TreeLines = '[new=0' +'\n'
    TreeLines = '[support=0' +'\n'
    prev_node = Py_Files [0][0]
    for item in Py_Files :
      if item[0] and ( item[1][0] != underscore ) :
        if item[0] != prev_node :
          prev_node = item[0]
          TreeLines += '[support \\ ' + item[0][1:].replace ( '\\', '~' ) + '=0~12~12' + '\n'
      if item[1][0] != underscore :
        TreeLines += item[1] + '=0~12~12' + '\n'
      """
      Tree.AppendItem ( Node, item[1] )
          self.SetPyData ( node, val )
          self.SetItemImage ( node, int( val[1] ), CT.TreeItemIcon_Normal )
          self.SetItemImage ( node, int( val[2] ), CT.TreeItemIcon_Expanded )
          Expand.append ( ( node, bool(int(val[0]) & 2) ))
      """
    #print TreeLines
    Tree.Lines_2_Tree ( TreeLines.split('\n') )
    Tree.ExpandAll()
    Tree.Add_PyFile_Info ( underscore )
    # ***************************************************

    Set_NoteBook_Images ( self.NBx, ( 47, 76 ) )

    self.SplitV.SetSashPosition  ( -80 )
    self.Split_H1.SetSashPosition  ( 300 )

    # Align all columns to the left
    self.Grid_Bricks.SetColLabelAlignment (wx.ALIGN_LEFT, wx.ALIGN_CENTER )
    for col in range ( self.Grid_Bricks.GetNumberCols () ) :
      self.Grid_Bricks.Align_Col ( col, wx.ALIGN_LEFT )
    self.Grid_Bricks.SetSelectionMode ( gridlib.Grid.SelectRows )


    self.SplitV.SetSashPosition  ( -180 )
    self.Split_H1.SetSashPosition  ( 300 )

    # Fill the grid
    R = 0
    """
    from PyLab_Works_search_bricks import *
    Libraries = Get_PyLabWorks_Bricks_All_Dict ()
    lib_list = sorted ( Libraries.keys() )
    for lib in lib_list :
      print 'LIV',lib

      #print 'CCSS',line,self.Grid.table.GetNumberCols ()
      if self.Grid.table.GetNumberRows () <= R :
        self.Grid.AppendRows(1)

      if self.Grid.table.GetNumberRows () > R :
        print 'pliep'
        self.Grid.table.SetValue ( R, 1, lib )
      R += 1
    """


    Attribs = {
      'normal': [ None, None, wx.GREEN ],
      3       : [ None, None, wx.BLUE ],
      }


    # ***************************************************
    Grid = self.Grid_Bricks
    Grid.Define_Attribs ( Attribs )
    
    dir = BasePath + 'PyLab_Works/bricks'
    Py_Files = Find_Files ( dir, 'brick_*.py' )
    #if self.Grid.table.GetNumberRows () <= R :
    Grid.AppendRows ( len ( Py_Files ) )
    print 'BBBB',R,Grid.table.GetNumberRows (),Grid.GetNumberRows ()
    for item in Py_Files :
      Grid.table.SetValue ( R, 0, item[0] )
      Grid.table.SetValue ( R, 1, item[1][6:] )

      # display the latest version + date
      try :
        exec ( 'import '+ item[1] )
        line = item[1] + '._Version_Text'
        version_line = eval ( line )
        Grid.table.SetValue ( R, 2, str ( version_line [0][0] ) )
        Grid.table.SetValue ( R, 3, str ( version_line [0][4] ) )
        Grid.table.SetValue ( R, 4, str ( version_line [0][1] ) )
        
      except :
        # to prevent text overflow into next column
        #Grid.table.SetValue ( R, 2, ' ' )
        pass

      if R == 3 :
        Grid.Set_Row_Color ( R, wx.CYAN )

      line = ''
      for Language in Language_IDs :
        #code = 'lang.' + Lib + '_' + Language
        code = item[1] + '_' + Language
        try :
          #print '******** 222',line
          exec ( 'from ' + code + ' import LT')
          line += Language + ', '
        except :
          pass
          #print 'File not found:',code
      if line :
        line = 'US, ' + line
        Grid.table.SetValue ( R, 5, line )

      R += 1
      #print item
    Grid.Set_Cell_Attrib ( 4, 2, 'normal' )
    Grid.Set_Row_Attrib  ( 8,    'normal' )
    Grid.Set_Col_Attrib  ( 1,    3        )
    # ***************************************************



    # ***************************************************
    """
    def Grid_Add_Files ( dir, Grid ) :
      Py_Files = Find_Files ( dir )
      #if self.Grid.table.GetNumberRows () <= R :
      Grid.AppendRows ( len ( Py_Files ) )
      for item in Py_Files :
        try :
          Grid.table.SetValue ( R, 0, item[0] )
          Grid.table.SetValue ( R, 1, item[1] )
        except :
          pass
        R += 1
    """
    
    Grid = self.Grid_Program
    dir = BasePath + 'PyLab_Works'
    Grid_Add_Files ( dir, Grid )
    dir = BasePath + 'support'
    Grid_Add_Files ( dir, Grid )
    dir = BasePath + 'Lib_Extensions'
    Grid_Add_Files ( dir, Grid )
    dir = BasePath + 'pictures'
    Grid_Add_Files ( dir, Grid )
    dir = BasePath + 'sounds'
    Grid_Add_Files ( dir, Grid )
    dir = BasePath + 'Templates'
    Grid_Add_Files ( dir, Grid )
    dir = BasePath + 'SQL'
    Grid_Add_Files ( dir, Grid )

    """
    Py_Files = Find_Files ( dir )
    #if self.Grid.table.GetNumberRows () <= R :
    Grid.AppendRows ( len ( Py_Files ) )
    for item in Py_Files :
      try :
        Grid.table.SetValue ( R, 0, item[0] )
        Grid.table.SetValue ( R, 1, item[1] )
      except :
        pass
      R += 1
      #print item
    """
    # ***************************************************

    # ***************************************************
    Grid = self.Grid_Private
    Grid = self.Grid_New

    # ***************************************************
    Grid = self.Grid_UnWanted
    dir = BasePath + 'support'
    Py_Files = Find_Files ( dir )
    #if self.Grid.table.GetNumberRows () <= R :
    Grid.AppendRows ( len ( Py_Files ) )
    print 'B',R,Grid.table.GetNumberRows (),Grid.GetNumberRows ()
    for item in Py_Files :
      try :
        Grid.table.SetValue ( R, 0, item[0] )
        Grid.table.SetValue ( R, 1, item[1] )
      except :
        pass
      R += 1
      #print item
    # ***************************************************


    """
    self.MS = tScope_Display ( self, None, ini, True ) ##, root_title = 'No Title' )

    # Modal forms will toggle this,
    # so the main application knows if any modal form is open
    if self.main_form:
      self.main_form.Modal_Open = False


    #self.SendSizeEvent()
    """
    
    self.Grid_Bricks.Bind ( gridlib.EVT_GRID_SELECT_CELL, self.On_Select_Cell )
    self.Bind ( wx.EVT_CLOSE, self.On_Close )

    self.Load_Settings ( self.Ini_File )


    # we create the debugger here
    self.Current_Line = None
    self.Main_File = 'D:/Data_Python_25/PyLab_Works/test_IDE.py'
    self.Debugger = Simple_RPDB2_Debugger ( self ) #, self.Main_File )
    self.Callback_Load_Editor ( self.Main_File )
    self.Debugger_Started = False

  # *******************************************************
  # On a breakpoint, here the local variables are displayed
  # *******************************************************
  def Display_Vars ( self, var_list ) :
    self.List_Debug.DeleteAllItems ()
    for var in var_list :
      if self.Hist_Dict.has_key ( var[0] ) :
        hist = self.Hist_Dict [ var[0] ]
        #self.Hist_Dict[var[0]].insert ( 0, var[1] )
      else :
        hist = ''
        #self.Hist_Dict[var[0]] = [ var[1] ]
      var.append (hist)
      #print 'DISPVARS',var[0], type(var[0]) #hist
      self.List_Debug.Append ( var )

    for var in var_list :
      if self.Hist_Dict.has_key ( var[0] ) :
        print 'INSSRT', self.Hist_Dict[var[0]], var[1][0]
        self.Hist_Dict[var[0]].insert ( 0, var[1] )
      else :
        self.Hist_Dict[var[0]] = [ var[1] ]
    print self.Hist_Dict

  # *******************************************************
  # *******************************************************
  def Notify_BreakPoint_Status ( self, value, filename, lineno ) :
    # Here we step over the function call / return
    # by repeating the last command
    print 'NOTOFY',value
    if value.lower() in  ( 'call', 'return' ) :
      if self.Last_Button_Command == 3  :
        self.Debugger.Step ()
      elif self.Last_Button_Command == 4  :
        self.Debugger.Step_Into ()

    self.Callback_Load_Editor ( filename, lineno )
    self.Last_Button_Command = None

    #header = self.List_Debug.GetColumn ( 0 )
    #header.SetText ( 'Aap' )
    #self.List_Debug.SetColumn ( 0, header )

  # *******************************************************
  # *******************************************************
  def Notify_Status ( self, value ) :
    if value == 'BreakPoint' :
      self.TB.Enable_Buttons ( Debug_Button_Break )
    else :
      self.Restore_Original_Markers ()
      self.TB.Enable_Buttons ( Debug_Button_Running )

  # *******************************************************
  # *******************************************************
  def On_ToolBar ( self, event ) :
    tb = event.GetEventObject()
    tb = self.TB.ToolBar

    _ID   = event.GetId()
    ID    = event.My_Index

    # If this event is launched by an accelerator key
    # the wrong ID might be selected
    # e.g. F9 always presses the break key
    # so let's correct that
    #print '************ Tool',ID,self.TB.Enabled_Tools
    if ( ID == 1 ) and self.TB.Enabled_Tools [2] :
      ID  = 2
      _ID = self.TB.IDs [ ID ]

    #print '************ Tool',ID

    self.Last_Button_Command = ID
    if ID == 0 :
      State = tb.GetToolState ( _ID )
      bmp = self.TB.IL.GetBitmap ( ( 83, 88 )[ State ] )
      tb.SetToolNormalBitmap ( _ID, bmp )

    elif ( ID == 1 ) and ( self.TB.Enabled_Tools [1] ):
      self.Debugger.Break ()
      
    elif ( ID == 2 ) and ( self.TB.Enabled_Tools [2] ):
      if not ( self.Debugger.Started ) and self.Main_File :
        self.Save_Editors_Changes ()
        self.Debugger.Start_Debug_Application ( self.Main_File )
        #self.Last_Button_Command == 2
      else :
        self.Debugger.Go ()

    elif ( ID == 3 ) and ( self.TB.Enabled_Tools [3] ):
      self.Debugger.Step ()

    elif ( ID == 4 ) and ( self.TB.Enabled_Tools [4] ):
      self.Debugger.Step_Into ()

    elif ID == 5 :
      self.Debugger.Restart ()

    elif ID == 6 :
      self.Save_Editors_Changes ()
      dir, filename = path_split( self.Main_File )
      run ( [ 'Python',
              'P:/Python/Lib/site-packages/winpdb-1.3.8/winpdb.py',
              filename ],
            cwd = dir, shell = True)
      #   cwd = 'D:/Data_Python_25/PyLab_Works/',
      self.Log.AppendText (
        '## *** Saved and Running External: ' + filename + '\n' )


      ##self.BP_ALL.Bind      ( wx.EVT_CHECKBOX, self.On_Change_BP_ALL   )
    else :
      pass
    #tb.EnableTool ( ID, not( tb.GetToolEnabled ( ID ) ) )


  # *********************************************************
  # *********************************************************
  def Save_Editors_Changes ( self ) :
    for Edit in self.Editors :
      Edit[0].SaveFile ( Edit[2] )

  # *********************************************************
  # Called by Debugger, when a new file is needed
  # *********************************************************
  def Callback_Load_Editor ( self, filename, lineno = -1 ) :
    print '****** Load', lineno, filename
    lineno -= 1

    # STRANGE STRANGE
    filename = filename.lower()  # ????

    if (len(self.Editors)>0) and (filename == self.Editors[0][2]) and not ( self.Debugger_Started ) :
      print '*********_________&&&&&&',self.Last_Button_Command
      self.Debugger_Started = True
      if self.Last_Button_Command == 2  :
        self.Debugger.Go ()
      elif self.Last_Button_Command == 3  :
        self.Debugger.Step ()
      elif self.Last_Button_Command == 4  :
        self.Debugger.Step_Into ()

    # check if file already open in an editor
    for Edit in self.Editors :
      if filename == Edit [2] :
        break
    else :
      # if not open yet, open it now
      filnams = path_split ( filename )
      filnam  = os.path.splitext ( filnams [1] ) [0]
      self.Log.AppendText ( '## Load: '+ filnam + ',  '  +filnams [0] + '\n' )
      self.Editors.append ( [ Base_STC ( self.NB ), filnam, filename ] )
      Edit = self.Editors [-1]
      self.NB.AddPage ( Edit[0], Edit[1] )
      Edit[0].On_BreakPoint_Change = self.Debugger.CallBack_On_BreakPoint_Change
      Edit[0].Get_Condition = self.Debugger.Get_BreakPoint_Condition

      # for the main file, ask for the breakpoints
      if len ( self.Editors ) == 1 :
        self.All_BreakPoints = Edit[0].LoadFile ( filename )
      # for the other files, support the breakpoints
      else :
        Edit[0].LoadFile ( filename, self.All_BreakPoints )
      Edit[0].FileName = filename
      Edit[0].Margin_On ( 2 )

    # Set Marker on Current Line
    self.Current_Line = [ filename, lineno, Edit[0].MarkerGet ( lineno ), -1 ]
    ##print '***&&&',self.Current_Line
    Edit[0].MarkerDelete ( lineno, -1 )
    Edit[0].MarkerAddSet ( lineno, self.Current_Line [2] & ~Edit[0].Break_Mask )
    if ( self.Current_Line [2] & Edit[0].Break_Mask ) > 0 :
      Edit[0].MarkerAddSet ( lineno, self.Current_Line [2] & 0x7800 )
    else :
      Edit[0].MarkerAdd ( lineno, 10 )
    Edit[0].MarkerAdd   ( lineno, 15 )

    Edit[0].EnsureVisibleEnforcePolicy ( lineno )
    Edit[0].GotoLine ( lineno )

    # Select the correct Edit Page
    for i in range ( self.NB.GetPageCount() ) :
      if self.NB.GetPageText (i) == Edit[1] :
        self.NB.SetSelection (i)
        self.Current_Line [3] = i
        self.NB.SetPageImage ( self.Current_Line [3], 83 )
        break;

    # Enable all editors
    for Edit in self.Editors :
      Edit[0].SetReadOnly ( False )

  # *********************************************************
  # Called by Debugger, when debug starts again, leaving a breakpoint
  # *********************************************************
  def Restore_Original_Markers ( self ) :
    # Delete ALL current line markers
    # restore the markers of the old current line
    if self.Current_Line :
      # Find the previous Editor
      for Old_Edit in self.Editors :
        if Old_Edit[2] == self.Current_Line[0] :
          Old_Edit[0].MarkerDeleteAll ( 10 )
          Old_Edit[0].MarkerDeleteAll ( 15 )
          Old_Edit[0].MarkerAddSet ( self.Current_Line[1], self.Current_Line [2] )
          filnam = path_split ( self.Current_Line [0] ) [1]
          filnam = os.path.splitext ( filnam ) [0]
          self.Current_Line = None

          # Locate the Editor and remove the image from the tab
          for i in range ( self.NB.GetPageCount() ) :
            if self.NB.GetPageText (i) == filnam :
              self.NB.SetPageImage ( i, -1 )
              break;
          break

    # Disable all editors
    for Edit in self.Editors :
      Edit[0].SetReadOnly ( True )

  # *********************************************************
  # *********************************************************
  def On_Close ( self, event ) :
    pass
  
  # *********************************************************
  # If editor modified, save changes
  # Keep editors administration clean
  # The mainfile can't be closed !!
  # *********************************************************
  def On_EditPage_Close ( self, event ) :
    filnam = self.NB.GetPageText ( self.NB.GetSelection () )
    for Edit in self.Editors [ 1:] :
      if filnam == Edit [1] :
        Edit[0].SaveFile ( Edit[2] )
        self.Editors.remove ( Edit )
        break
    else :
      event.Veto()

  # *******************************************************
  # override Scintilla's execute code
  # *******************************************************
  def Execute_Code ( self ) :
    line =  str ( self.Log_Cmd.Code_To_Execute )
    #print 'MEMOCODE:',line
    if line.find ( '>' ) != 0 :
      self.Log_Cmd.AppendText ( '  ==> ' )
    self.Debugger.Put_Command ( line )

  # *************************************************************
  # *************************************************************
  def On_Log_Text ( self, event ) :
    aa = self.Log_Cmd.GetPosition()
    print aa
    aa = self.Log_Cmd.GetLastPosition()
    aa = self.Log_Cmd.GetInsertionPoint()
    print aa
    bb = self.Log_Cmd.PositionToXY ( aa )
    print dir ( event )
    print event.GetExtraLong()
    print event.GetInt()
    print event.GetSelection()
    print event.GetString()
    print self.Log_Cmd.GetLineText ( bb [1] )

  # *************************************************************


  # *************************************************************
  def On_Tree_Sel_Changed ( self, event ) :
    item = event.GetItem ()

    if event.EventObject  == self.Tree :
      #print self.GetItemText ( event.GetItem())
      level, main_parent = self.Tree.Get_Item_Level_MainParent ( item )
      if level == 2 :
        pass


      # ****************************************************************
      # Class or Function
      # ****************************************************************
      elif level == 3 :
        module_node = self.Tree.Get_Parent_At_Level ( item, 2 )
        module_name = self.Tree.GetItemText ( module_node )
        object_name = self.Tree.GetItemText ( item )

        lines = object_name +  '    ( ' + module_name + ' )\n'
        lines = 'file: ' + module_name + '\n'

        PF = Analyze_PyFile ( module_name )

        line = PF.Class_Doc_String ( object_name )
        lines += line

        line = PF.Get_Init_Def ( object_name )
        lines += line

        lines += '\n\n'
        self._Display_Info ( lines )

      # ****************************************************************
      # Method of a Class
      # ****************************************************************
      elif level == 4 :
        module_node = self.Tree.Get_Parent_At_Level ( item, 2 )
        module_name = self.Tree.GetItemText ( module_node )
        class_node = self.Tree.Get_Parent_At_Level ( item, 3 )
        class_name = self.Tree.GetItemText ( class_node )
        object_name = self.Tree.GetItemText ( item )

        lines =  class_name + '.'
        lines += object_name +  '    ( ' + module_name + ')\n'

        PF = Analyze_PyFile ( module_name )

        line = PF.Class_Doc_String ( class_name, object_name )
        lines += line


        line = PF.Get_Init_Def ( class_name, object_name )
        lines += line

        lines += '\n\n'
        self._Display_Info ( lines )

    event.Skip()


  # ****************************************************************
  # ****************************************************************
  def _Display_Info ( self, lines ) :
    L = lines.find ('\n')
    B = self.Log_Cmd.GetTextLength ()
    self.Log_Cmd.AppendText ( lines )
    ##self.Memo.SetLexer ( stc.STC_LEX_NULL )
    self.Log_Cmd.StartStyling ( B, 0xFF )
    self.Log_Cmd.SetStyling   ( L,  self.Log_Cmd.GetStyleAt (B) | 0xE0 )
    #for i in range (32 ) :
    #  self.Log_Cmd.SetStyling   ( L, i | 0xE0 )
    self.Log_Cmd.GotoPos ( self.Memo.GetTextLength () )
    self.Log_Cmd.EnsureCaretVisible()
    self.Log_Cmd.Colourise ( 0, -1 )
    #self.Log_Cmd.Colourise ( B, B+L )  ## not enough !!
    ##self.Log_Cmd.SetLexer ( stc.STC_LEX_PYTHON )
    #wx.CallLater (200, self.on_block,B,L)

  def on_block ( self, B, L ) :
    self.Log_Cmd.StartStyling ( B, 0xFF )
    self.Log_Cmd.SetStyling   ( L,  self.Log_Cmd.GetStyleAt (B) | 0xE0 )
    #for i in range (32 ) :
    #  self.Log_Cmd.SetStyling   ( L, i | 0xE0 )
    #self.Log_Cmd.GotoPos ( self.Log_Cmd.GetTextLength () )
    #self.Log_Cmd.EnsureCaretVisible()


  # ****************************************************************
  # ****************************************************************
  def On_Select_Cell ( self, event ) :
    if event.Col == 1 :
      Lib = 'brick_' + self.Grid_Bricks.table.GetValue ( event.Row, 1 )
      lines = Lib #+ '\n'

      try :
        exec ( 'import '+ Lib )
        line = eval ( Lib + '.Description' )
        print line
        lines += line
      except :
        pass

      lines += '\n\n'
      self._Display_Info ( lines )
      
    event.Skip()


  # *****************************************************************
  # *****************************************************************
  def On_Close ( self, event ) :
    ini = self.Ini_File
    if ini :
      ini.Section = self.Ini_Section
      ini.Write ( 'Pos',  self.GetPosition () )
      ini.Write ( 'Size', self.GetSize () )
      
      self.Save_Settings ( ini )

    self.Debugger.Stop_Debug_Application()
    self.Destroy()
    ##event.Skip ()

  # *****************************************************************
  # *****************************************************************
  def Save_Settings ( self, ini ):
    line = []
    line.append ( self.SplitV.GetSashPosition () )
    line.append ( self.Combo_Language.GetValue () )
    line.append ( self.Techno.GetValue () )
    line.append ( self.Split_H1.GetSashPosition () )
    line.append ( self.NBx.GetSelection () )
    line.append ( self.NB_Tree.GetSelection () )
    ini.Write ( 'CS_', line )

    ini.Write ( 'CS_Bricks',   self.Grid_Bricks.  Get_Settings () )
    ini.Write ( 'CS_UnWanted', self.Grid_UnWanted.Get_Settings () )
    ini.Write ( 'CS_Program',  self.Grid_Program. Get_Settings () )
    ini.Write ( 'CS_Private',  self.Grid_Private. Get_Settings () )
    ini.Write ( 'CS_New',      self.Grid_New.     Get_Settings () )

  # *****************************************************************
  # Loads all form settings
  # *****************************************************************
  def Load_Settings ( self, ini ) :
    if ini :
      ini.Section = self.Ini_Section

      line = ini.Read ( 'CS_', '' )
      try :
        if line :
          self.SplitV.SetSashPosition  ( line [0] )
          self.Combo_Language.SetValue ( line [1] )
          self.Techno.SetValue ( line [2] )
          self.Split_H1.SetSashPosition ( line [3] )
          self.NBx.SetSelection ( line [4] )
          self.NB_Tree.SetSelection ( line [5] )
      except :
        pass

      self.Grid_Bricks.  Do_Settings ( ini.Read ( 'CS_Bricks',   '' ) )
      self.Grid_UnWanted.Do_Settings ( ini.Read ( 'CS_UnWanted', '' ) )
      self.Grid_Program. Do_Settings ( ini.Read ( 'CS_Program',  '' ) )
      self.Grid_Private. Do_Settings ( ini.Read ( 'CS_Private',  '' ) )
      self.Grid_New.     Do_Settings ( ini.Read ( 'CS_New',      '' ) )
      

# ***********************************************************************



# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':
  # starts a wait period of 5 minutes, for a winpdb to attach
  # import rpdb2; rpdb2.start_embedded_debugger('aap')

  app = wx.PySimpleApp ()
  ini = inifile ( os.path.join (os.getcwd(), 'Library_Manager_Test.cfg' ))
  ini.Section = 'Library Manager'

  # Create the scope form and show it
  Main_Form = my_Test_Form ( None, ini )
  Main_Form.Show()

  app.MainLoop ()

  # The inifile can be used by more forms, so we close it here
  ini.Close ()
# ***********************************************************************
pd_Module ( __file__ )

