import __init__
# ***********************************************************************

from language_support import  _

__doc__ = _(0, """
doc_string translated ?
""" )

_Version_Text = [

[ 0.1 , '24-10-2008', 'Stef Mientki',
'Test Conditions:', ( 2, ),
_(0, ' - orginal release')]
]


import PyLab_Works_Globals as PG
from   PyLab_Works_Globals  import *
#from   system_support       import Kill_Process_pid
from   menu_support         import Class_Menus, My_Popup_Menu
from   picture_support      import Get_Image_List
import time

# ***********************************************************************
from gui_support          import *
from Scintilla_support    import *
# ***********************************************************************

from PyLab_Works_Debugger import *  #PW_PDB


# *******************************************************
# Find all controls in this file
# Controls are class definitions,
#  derived from the baseclass My_Control_Class
# *******************************************************
def Get_Controls_From_File ( control_filename ) :
  filename = path_split ( control_filename )[1]
  filename = os.path.splitext ( filename )[0]

  import inspect
  from base_control import My_Control_Class

  line = 'import ' + filename + ' as CCC\n'
  try :
    exec ( line )
  except :
    v3print ( 'Error PW_Controls_Manager: importing', control_filename )
  #v3print ( 'Import: ',line )
  #v3print ( CCC )
  Classes = inspect.getmembers ( CCC, inspect.isclass )

  Sel_Classes = []
  import PyLab_Works_Globals as PG
  for klasse in Classes :
    if ( filename == klasse[1].__module__ ) and \
       ( not ( klasse[0].startswith ( '_' ) ) ) :
      base_classes = klasse[1].__bases__
      for bc in base_classes :
        if issubclass ( bc, My_Control_Class ):
          Sel_Classes.append ( klasse )

  Control_Names = []
  Control_Names.append ( ['Name', 'Full Name' ] )
  for Klasse in Sel_Classes :
    Control_Names.append (  [ Klasse[0][4:], Klasse[0] ] )

  return Control_Names
# *******************************************************


# ***********************************************************************
# ***********************************************************************
class Control_IDE_Form ( My_Frame_Class ) :

  # *****************************************************************
  # *****************************************************************
  def __init__( self, main_form= None, ini = None ) :

    self.My_Title = 'PW  Controls IDE    v' + str ( _Version_Text[0][0]) + '     file: '
    My_Frame_Class.__init__ ( self, main_form, self.My_Title, ini, 'MainForm' )

    sampleList = ['zero', 'one', 'two', 'three', 'four', 'five',
                  'this is a long item that needs a scrollbar...',
                  'six', 'seven', 'eight']
    self.last_list_filename = None

    bmp_PW = wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_BUTTON, (16,16))

    self.MenuBar = Class_Menus ( self )

    self.StatusBar = self.CreateStatusBar()
    self.StatusBar.SetFieldsCount(3)
    self.StatusBar.SetStatusWidths([-2, -1, -2])
    self.StatusBar.SetStatusText(' Edit',0)
    self.StatusBar.SetStatusText(' aap',2)
    # *************************************************************
    # *************************************************************

    GUI = """
    self.SplitV1            ,SplitterVer
      self.Split_H1         ,SplitterHor    ,name = 'Tests'
        self.NB             ,wx.Notebook
          self.Edit_Model   ,Base_STC    ,name = '<Model>'

          PLT2              ,PanelVer, 01  ,name  = 'Debug'
            P1              ,wx.Panel
              B_PW            ,BmpBut    ,bitmap = bmp_PW   ,pos = (0,0) ,size = ( 20,20)
              B_PW2           ,BmpBut    ,bitmap = bmp_PW   ,pos = (0,40) ,size = ( 20,20)

            PLT1              ,PanelHor, 11  ,name  = 'Help'
              P2              ,wx.Panel
                Future        ,wx.StaticText ,label = 'Future Use'
              self.Ctrl_List  ,wx.CheckListBox, choices =['One', 'Two']  ,style = wx.LB_SINGLE

        PRight              ,PanelVer ,01
          self.P3           ,wx.Panel
            self.Label_File ,wx.StaticText    ,label = '<FileName>'
          self.Edit         ,Base_STC
          
      self.NB_CMD           ,wx.Notebook      ,style = wx.BK_LEFT
        self.Log_Cmd        ,Base_STC         ,name = 'CMD-Shell'
        self.Html           ,Class_URL_Viewer ,name = 'Help'    ,ini = ini
    """
    self.wxGUI = Create_wxGUI ( GUI, IniName = 'self.Ini_File' )



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
    # methods for editor + shell
    # *************************************************************
    self.Log_Cmd.Function_Key  = self.Function_Key
    self.Edit.Function_Key     = self.Function_Key
    # *************************************************************

    # *************************************************************
    # *************************************************************
    PG.Set_StdOut ( self.Log_Cmd )
    PG.Set_StdErr ( self.Log_Cmd )
    # *************************************************************

    # Allow BreakPoints Margin
    self.Edit.Margin_On ( 2 )

    self.Edit_Model.SetReadOnly ( True )

    self.Bind ( wx.EVT_CLOSE,  self.On_Close  )

    self.Control_Files = Find_Files (
      Application.Dir, mask = 'control_*.py' )

    # *************************************************************
    self.NB.Bind ( wx.EVT_CONTEXT_MENU, self._On_NB_Popup_Show )
    self.NB.Bind ( wx.EVT_NOTEBOOK_PAGE_CHANGED,  self._On_NB_PageChanged )
    #self.NB.Bind ( wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging )
    self.NB.SetToolTipString ( 'hallo' )
    pre = []
    for file in self.Control_Files :
      pre.append ( file [1][8:] )
    self.Control_Files_Popup_Menu = My_Popup_Menu (
      self._On_NB_Popup_Select, None, pre =pre )
    # *************************************************************

    Set_NoteBook_Images ( self.NB,     ( 53, 76  ) )
    Set_NoteBook_Images ( self.NB_CMD, ( 206, 25 ) )

    # *************************************************************
    self.P3        .Bind ( wx.EVT_CONTEXT_MENU, self._On_Label_File_Popup_Show )
    self.Label_File.Bind ( wx.EVT_CONTEXT_MENU, self._On_Label_File_Popup_Show )
    self.Label_File.SetToolTipString ( 'Right Click to change file' )
    pre = [ '<new>' ]
    for file in self.Control_Files :
      pre.append ( file [1][8:] )
    self.Control_Files_Popup_Menu2 = My_Popup_Menu (
      self._On_Label_File_Popup_Select, None, pre =pre )
    # *************************************************************


    # *************************************************************
    # workspace
    # *************************************************************
    self.p_Globals = {}
    self.p_Locals = {}
    # *************************************************************

    # *************************************************************
    # Menu completions
    # *************************************************************
    MB = self.MenuBar.Bind_MenuItem
    MB ( 'File', 'New/Open',      self._On_Menu_FileSave )
    MB ( 'File', 'Save', self._On_Menu_FileSave )
    MB ( 'File', 'Save As',       self._On_Menu_FileSave )
    MB ( 'File', 'Close',         self._On_Menu_FileSave )
    # *************************************************************

    self.Load_Settings ()
    self.Html.Load ( 'html/pw_demos.html' )
    self.Show ()

  # *******************************************************
  def Set_Caption ( self, title, level = None ) :
    self.SetTitle ( self.My_Title + title )

  # *******************************************************
  def _On_Menu_FileSave ( self, event = None ) :
    v3print ( 'SAVE, still tot to' )
    Edit = self.FindFocus()
    if Edit == self.Log_Cmd :
      print 'Log_Cmd'
    elif Edit == self.Edit :
      print 'Edit'

  # *******************************************************
  # *******************************************************
  def _On_NB_PageChanged ( self, event ) :
    event.Skip ()
    old = event.GetOldSelection()
    new = event.GetSelection()
    #self.NB.Bind ( wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging )
    self.NB_hints = [
      'page 1',
      'page 2']
    self.NB.SetToolTipString ( self.NB_hints [ new ] )

  # *******************************************************
  # *******************************************************
  def _Update_Control_List ( self ) :
    # Update list of controls
    filename = os.path.splitext ( path_split ( self.Edit.Filename )[1] )[0]
    if filename != self.last_list_filename :
      self.last_list_filename = filename
      Control_Names = Get_Controls_From_File ( filename )
      Choices = []
      for item in Control_Names [ 1: ] :
        Choices.append ( item [0] )
      self.Ctrl_List.Set ( Choices )

  # *******************************************************
  # *******************************************************
  def _On_NB_Popup_Show ( self, event ) :
    page = self.NB.GetSelection ()
    if page == 0 :
      #pos = event.GetPosition ()
      #pos = self.NB.ScreenToClient ( pos )
      self.NB.PopupMenu ( self.Control_Files_Popup_Menu )
    #self.Tree_Hit_Pos = pos
    #self.Splitter.PopupMenu ( self.Popup_Menu_Tree )

  # *******************************************************
  # *******************************************************
  def _On_NB_Popup_Select (self, event ) :
    filename = self.Control_Files [ event.Int ][1]
    filename += '.py'
    filename = os.path.join ( 'controls', filename )
    self._Open_Model ( filename )
    #item = self.Control_Files_Popup_Menu.FindItemById ( event.GetId () )
    #text = item.GetText()

  # *******************************************************
  # *******************************************************
  def _On_Label_File_Popup_Show ( self, event ) :
    self.Label_File.PopupMenu ( self.Control_Files_Popup_Menu2 )

  # *******************************************************
  # *******************************************************
  def _On_Label_File_Popup_Select (self, event ) :
    filename = self.Control_Files [ event.Int - 1 ][1]
    filename += '.py'
    filename = os.path.join ( 'controls', filename )
    self._Open_Control ( filename )
    #item = self.Control_Files_Popup_Menu.FindItemById ( event.GetId () )
    #text = item.GetText()

  # *******************************************************
  # *******************************************************
  def _Open_Model ( self, filename ) :
    self.Edit_Model.LoadFile ( filename )
    filename = path_split ( filename ) [1]
    filename = os.path.splitext ( filename ) [0]
    self.NB.SetPageText ( 0, filename )

  # *******************************************************
  # *******************************************************
  def _Open_Control ( self, filename ) :
    self.Edit.SaveFile ( self.Edit.Filename )
    
    # Get selected controls and store
    if self.Edit.Filename :
      Selection = []
      for i, item in enumerate ( self.Ctrl_List.GetItems () ) :
        if self.Ctrl_List.IsChecked ( i ) :
          Selection.append ( item )
      old_filename = path_split ( self.Edit.Filename ) [1]
      old_filename = os.path.splitext ( old_filename ) [0]
      self.Selection [ old_filename ] = Selection

    self.Main_File = filename
    self.All_BreakPoints = self.Edit.LoadFile ( self.Main_File )
    filename = path_split ( filename ) [1]
    filename = os.path.splitext ( filename ) [0]
    self.Label_File.SetLabel ( filename )
    #self.Label_File.SetLabel ( filename [ : -3 ] )
    self._Update_Control_List ()

    if filename in self.Selection :
      Selection = self.Selection [ filename ]
      for i, item in enumerate ( self.Ctrl_List.GetItems () ) :
        if item in Selection :
          self.Ctrl_List.Check ( i, True )


  # *******************************************************
  # *******************************************************
  def Function_Key ( self, key ) :
    #Beep ()
    if key == 9 :
      self.SetCursor ( wx.StockCursor ( wx.CURSOR_WAIT ) )

      # save the file otherwise we can't use inspect
      self.Edit.SaveFile ( self.Edit.Filename )
      control_filename = os.path.splitext ( path_split ( self.Edit.Filename )[1] )[0]

      Selection = []
      for i, item in enumerate ( self.Ctrl_List.GetItems () ) :
        if self.Ctrl_List.IsChecked ( i ) :
          Selection.append ( item )

      if len ( Selection ) == 0 :
        self.NB.SetSelection ( 1 )
        self.Ctrl_List.Check ( 0, True )
        Selection.append (  self.Ctrl_List.GetItems ()[0] )

      filename = 'controls_wrapper_dont_touch.py'
      self.p_Globals = {}
      self.p_Globals [ 'Control_Filename' ] = control_filename
      self.p_Globals [ 'Control_Name'     ] = Selection [0]
      #exprint ( self.p_Globals )
      execfile ( filename , self.p_Globals ) #, self.p_Locals )

      self.SetCursor ( wx.StockCursor ( wx.CURSOR_DEFAULT ) )

  # *******************************************************
  # override Scintilla's execute code
  # *******************************************************
  def Execute_Code ( self ) :
    line =  str ( self.Log_Cmd.Code_To_Execute )
    #print 'MEMOCODE:',line
    if line.find ( '>' ) != 0 :
      self.Log_Cmd.AppendText ( '  ==> ' )
      try :
        result = eval ( line, self.p_Globals )
        self.Log_Cmd.AppendText ( str ( result ) +'\n' )
      except :
        result = '\n'
        # split lines, and remove the last (empty) line
        lines = line.split ( '\n' ) [ : -1 ]
        # test if it's an assignment
        i = lines [ -1 ].rfind ( '=' )
        if i > 0 :
          result = lines [ -1 ] [ : i+1 ] + ' '
          self.Log_Cmd.AppendText ( result )
          # get the first var on the left of the assignment
          i = lines [ -1 ].find ( '=' )
          result = 'print ' + lines [ -1 ] [ : i ] + '\n'
          print '$$' + line + result + '$$\n'
        exec ( line + result, self.p_Globals )
      
    #self.Debugger.Put_Command ( line )

  # *******************************************************
  # *******************************************************
  def Set_Debug_Status ( self, Status, Var1 = None, Var2 = None ):
    if Status == DS_RUNNING :
      self.Edit.Leave_Editor_On_BP ()

    elif Status == DS_GET_LINENO :
      Scite_ID = Var2
      return self.Edit.MarkerLineFromHandle ( Scite_ID )

    elif Status == DS_BP :  # Breakpoint reached
      self.Edit.Goto_Editor_On_BP ( Var1, Var2 )
      # Now get all local variables and their history
      self.Debugger.Get_Locals ()

    elif Status == DS_LOCALS :
      print 'VARS: ', Var1

    else :
      print '**** Unknown Debugger Response or Comment *****'
      print Var1, Var2

  # *********************************************************
  # *********************************************************
  def On_Button_BPs ( self, event ) :
    if self.Edit.GetMarginWidth (2) > 0 :
      self.Edit.Margin_Off ( 2 )
    else :
      self.Edit.Margin_On ( 2 )

  # *********************************************************
  # *********************************************************
  def Save_Settings ( self ) :
    if self.Ini_File :
      self.Ini_File.Section = self.Ini_Section

      self.Ini_File.Write ( 'Control_File', self.Edit.Filename )
      self.Ini_File.Write ( 'Control_Selection', self.Selection )
      self.Ini_File.Write ( 'Model_File', self.Edit_Model.Filename )

      self.wxGUI.Save_Settings ()

      # SHOULD BE DONE AUTOMATICALLY by wxGUI_Save_Settings
      self.Html.Save_Settings ( self.Ini_Section )


  # *********************************************************
  # *********************************************************
  def Load_Settings ( self ) :
    if self.Ini_File :
      self.Ini_File.Section = self.Ini_Section
      self.Selection = self.Ini_File.Read_Dict ( 'Control_Selection', {} )
      #v3print ( 'Read Selecetion', self.Selection )
      Control_File   = self.Ini_File.Read ( 'Control_File', 'controls/control_general.py' )
      self._Open_Control ( Control_File )
      Model_File   = self.Ini_File.Read ( 'Model_File', 'controls/control_general.py' )
      self._Open_Model ( Model_File )

      # we create the debugger here
      # and feed the main-file and breakpoints to the debugger
      self.Debugger = PW_PDB ( self, self.Set_Debug_Status )
      self.Debugger.BreakPoints = self.All_BreakPoints
      self.Debugger.Set_Main_File ( self.Main_File )

  # *********************************************************
  # *********************************************************
  def On_Close ( self, event ) :
    event.Skip()
    self.Edit.Leave_Editor_On_BP ()
    self.Debugger.Stop_Debug_Application()

    self.Edit.SaveFile ( self.Main_File, self.All_BreakPoints, True )

    PG.Restore_StdOut ( self.Log_Cmd )
    PG.Restore_StdErr ( self.Log_Cmd )

    self.Save_Settings ()

    #for Control in self.Control_Names :

    #PG.Restore_StdOut ( self.Log_Cmd )
    #PG.Restore_StdErr ( self.Log_Cmd )
    
    print self.Main_File
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
if __name__ == '__main__':
  My_Main_Application ( Control_IDE_Form )
