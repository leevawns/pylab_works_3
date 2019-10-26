# MUST BE THE FIRST ONE ???????
import visual
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


# ***********************************************************************
_ToDo = """
"""
# ***********************************************************************

import PyLab_Works_Globals as PG
from PyLab_Works_Globals  import *
from system_support import Beep, Kill_Process_pid, Run
from menu_support   import Class_Menus, My_Popup_Menu
import time

# ***********************************************************************
from gui_support          import *
from Scintilla_support    import *
# ***********************************************************************

from PyLab_Works_Debugger import *  #PW_PDB


# *****************************************************************
# *****************************************************************
def Check_Html_File ( Source_File, Dest_Path ) :
  """
  Checks if a base HTML-file is available in the PyJamas
  output directory.
  If the HTML-file isn't available, it will be created.

  If a CSS-file with the same name is available
  in the output directory, a reference to this CSS-file
  is included.

  If no CSS-file is found, this function will look for a special
  CSS-file in the output directory, with the name
  "pyjamas_default.css", and if found it will be referenced
  in the generated HTML-file.
  """

  Base_Html = """
<html>
  <head>
    <meta name="pygwt:module" content="$$XXX$$">
    $$YYY$$
    <title>$$ZZZ$$</title>
  </head>
  <body bgcolor="white">
    <script language="javascript" src="pygwt.js"></script>
  </body>
</html>
"""

  filename = path_split    ( Source_File )[1]
  filename = os.path.splitext ( filename    )[0]
  FileName = os.path.join     ( Dest_Path, filename + '.html' )

  # if not html file in output directory, create one
  if not ( os.path.exists ( FileName ) ) :
    Base_Html = Base_Html.replace ( '$$XXX$$', filename )

    if os.path.exists (
         os.path.join ( Dest_Path, filename + '.css' ) ) :
      Base_Html = Base_Html.replace ( '$$YYY$$',
        "<link rel='stylesheet' href='" + filename + ".css'>" )

    elif os.path.exists (
           os.path.join ( Dest_Path, 'pyjamas_default.css' ) ) :
      Base_Html = Base_Html.replace ( '$$YYY$$',
        "<link rel='stylesheet' href='pyjamas_default.css'>" )

    else :
      Base_Html = Base_Html.replace ( '$$YYY$$', '' )

    Base_Html = Base_Html.replace ( '$$ZZZ$$',
      'PyJamas Auto Generated HTML-file ' + filename )

    fh = open ( FileName, 'w' )
    fh.write ( Base_Html )
    fh.close ()
# *****************************************************************


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


# ***********************************************************************
# ***********************************************************************
class Control_IDE_Form ( My_Frame_Class ) :

  # *****************************************************************
  # *****************************************************************
  def __init__( self, main_form= None, ini = None ) :

    Title = 'PW  Controls IDE    v' + str ( _Version_Text[0][0] )
    My_Frame_Class.__init__ ( self, main_form, Title, ini, 'MainForm' )

    sampleList = ['zero', 'one', 'two', 'three', 'four', 'five',
                  'this is a long item that needs a scrollbar...',
                  'six', 'seven', 'eight']

    self.Path = 'P:/Python/Lib/site-packages/pyjamas_0.4p1/examples/kitchensink/'
    self.Path = 'P:/Python/Lib/site-packages/pyjamas_0.4p1/examples/formpanel/'
    self.Path = 'P:/Python/Lib/site-packages/pyjamas_0.4p1/examples/aap/'
    #self.Path = 'P:/Python/Lib/aap/'
    self.Path = 'D:/Data_Python_25/PyJamas_Projects/to_test1/'

    #bmp_PW    = Get_Image_16 ( 'vippi_bricks_64.png' )
    bmp_PW = wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_BUTTON, (16,16))

    self.MenuBar = Class_Menus ( self )

    self.StatusBar = self.CreateStatusBar()
    self.StatusBar.SetFieldsCount(3)
    self.StatusBar.SetStatusWidths([-2, -1, -2])
    self.StatusBar.SetStatusText(' Edit',0)
    self.StatusBar.SetStatusText(' aap',2)
    # *************************************************************
    # *************************************************************

    #        self.Html       ,My_HtmlWindow
    GUI = """
    self.SplitV1            ,SplitterVer
      self.Split_H1         ,SplitterHor    ,name = 'Tests'
        self.NB             ,wx.Notebook
          Panel_dummy2      ,PanelVer, 11  ,name  = 'Help'
            self.Html       ,iewin.IEHtmlWindow, style = wx.NO_FULL_REPAINT_ON_RESIZE

          Panel_dummy3      ,PanelVer, 11  ,name  = 'Debug'
            B_PW            ,BmpBut    ,bitmap = bmp_PW   ,pos = (0,0) ,size = ( 20,20)
            CFiles          ,wx.ComboBox , choices=sampleList, size=(160,-1), style=wx.CB_DROPDOWN
          self.P_model      ,PanelVer, 11  ,name  = '<FileName>'
            self.Edit_Model ,Base_STC

        PRight              ,PanelVer ,01
          self.P3           ,wx.Panel
            self.Label_File ,wx.StaticText  , label = '<FileName>'
          self.Edit         ,Base_STC
      self.Log_Cmd          ,Base_STC
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
    self._Open_Model ( 'control_ogl.py' )
    #self._Open_Control ( 'control_adc_BU.py' )
    #self._Open_Control ( 'control_vpython.py' )
    #self._Open_Control ( 'control_ogl.py' )
    self._Open_Control ( 'control_html.py' )

    # we create the debugger here
    # and feed the main-file and breakpoints to the debugger
    self.Debugger = PW_PDB ( self, self.Set_Debug_Status )
    self.Debugger.BreakPoints = self.All_BreakPoints
    self.Debugger.Set_Main_File ( self.Main_File )

    self.Bind ( wx.EVT_CLOSE,  self.On_Close  )
    #self.Bind ( wx.EVT_BUTTON, self.On_Button_BPs,      Button_BPs       )
    #self.Bind ( wx.EVT_BUTTON, self.Debugger.Break,     Button_Pause     )
    #self.Bind ( wx.EVT_BUTTON, self.Debugger.Go,        Button_Run       )
    #self.Bind ( wx.EVT_BUTTON, self.Debugger.Step,      Button_Step      )
    #self.Bind ( wx.EVT_BUTTON, self.Debugger.Step_Into, Button_Step_Into )
    #self.Bind ( wx.EVT_BUTTON, self.Debugger.Restart,   Button_Restart   )

    ##self.Control_Names = []
    self.Control_Files = Find_Files (
      self.Path ,
      mask = '*.py', RootOnly = True )
    print self.Path
    print self.Control_Files

    # *************************************************************
    self.NB.Bind ( wx.EVT_CONTEXT_MENU, self._On_NB_Popup_Show )
    self.NB.Bind ( wx.EVT_NOTEBOOK_PAGE_CHANGED,  self._On_NB_PageChanged )
    #self.NB.Bind ( wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging )
    self.NB.SetToolTipString ( 'hallo' )
    pre = []
    for file in self.Control_Files :
      pre.append ( file [1] )
    #voegt lege items aan popup, waardoor knalt
    self.Control_Files_Popup_Menu = My_Popup_Menu (
      self._On_NB_Popup_Select, None, pre =pre )
    # *************************************************************

    # *************************************************************
    self.P3        .Bind ( wx.EVT_CONTEXT_MENU, self._On_Label_File_Popup_Show )
    self.Label_File.Bind ( wx.EVT_CONTEXT_MENU, self._On_Label_File_Popup_Show )
    self.Label_File.SetToolTipString ( 'Right Click to change file' )
    pre = [ '<new>' ]
    for file in self.Control_Files :
      pre.append ( file [1] )
    self.Control_Files_Popup_Menu2 = My_Popup_Menu (
      self._On_Label_File_Popup_Select, None, pre =pre )
    # *************************************************************


    #self.Source_File = 'html/pw_demos.html'
    #name_to = 'CSS_translated.html'
    #wxp_widgets.Translate_CSS ( self.Source_File, name_to, self.CallBack_Html )
    #self.Html.Load_CSS ( 'html/pw_demos.html' )

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

    self.Show ()


  # *******************************************************
  def _On_Menu_FileSave ( self, event = None ) :
    print 'SAVE'
    Edit = self.FindFocus()
    if Edit == self.Log_Cmd :
      print 'Log_Cmd'
    elif Edit == self.Edit :
      print 'Edit'
    elif Edit == self.Edit_Model :
      print 'Edit_Model'

  # *******************************************************
  # *******************************************************
  def _On_NB_PageChanged ( self, event ) :
    event.Skip ()
    old = event.GetOldSelection()
    new = event.GetSelection()
    #self.NB.Bind ( wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging )
    self.NB_hints = [
      'page 1',
      'page 2',
      'Right click to lad another model']
    self.NB.SetToolTipString ( self.NB_hints [ new ] )

  # *******************************************************
  # *******************************************************
  def _On_NB_Popup_Show ( self, event ) :
    page = self.NB.GetSelection ()
    if page == 2 :
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
    self._Open_Control ( filename )
    #item = self.Control_Files_Popup_Menu.FindItemById ( event.GetId () )
    #text = item.GetText()

  # *******************************************************
  # *******************************************************
  def _Open_Model ( self, filename ) :
    print filename
    self.Edit_Model.LoadFile ( filename )
    self.NB.SetPageText ( 2, filename [ : -3] )

  # *******************************************************
  # *******************************************************
  def _Open_Control ( self, filename ) :
    self.Edit.SaveFile ( self.Edit.Filename )
    #self.Edit_Model.LoadFile ( filename )
    print filename
    self.Main_File = self.Path + filename
    self.All_BreakPoints = self.Edit.LoadFile ( self.Main_File )
    self.Label_File.SetLabel ( filename [ : -3 ] )

  # *******************************************************
  # *******************************************************
  def Function_Key ( self, key ) :
    print 'FK',key
    if key == 9 :
      # save the file otherwise we can't use inspect
      self.Edit.SaveFile ( self.Edit.Filename )

      """
      control_filename = os.path.splitext ( path_split ( self.Edit.Filename )[1] )[0]

      filename = 'controls_wrapper_dont_touch.py'
      self.p_Globals = { 'control_filename' : control_filename }
      print self.p_Globals
      execfile ( filename , self.p_Globals ) #, self.p_Locals )
      """

      Path, FileName = path_split       ( self.Edit.Filename )
      Path, FileName = path_split       ( self.Edit.Filename )
      File, Ext      = os.path.splitext ( FileName           )

      Output = 'D:/output/'

      ##Builder = os.path.join ( Path, '../../builder/build.py' )
      Builder = 'P:/Python/Lib/site-packages/pyjamas-0.5/pyjs/build.py'
      """
File "P:/Python/Lib/site-packages/pyjamas-0.5/pyjs/build.py", line 60, in read_boilerplate
    return open(join(data_dir, "builder/boilerplate", filename)).read()
IOError: [Errno 2] No such file or directory: 'P:\\Python\\share\\pyjamas\\builder/boilerplate\\pygwt.js'
"""

      Builder = 'P:/Python/Lib/site-packages/pyjamas-0.5/build/lib/pyjs/build.py'

      #Builder = 'P:/Python/Lib/site-packages/pyjamas-0.5/build/bdist.win32/egg/pyjs/build.py'
      """
  File "P:/Python/Lib/site-packages/pyjamas-0.5/build/bdist.win32/egg/pyjs/build.py", line 60, in read_boilerplate
    return open(join(data_dir, "builder/boilerplate", filename)).read()
IOError: [Errno 2] No such file or directory: 'P:\\Python\\share\\pyjamas\\builder/boilerplate\\pygwt.js'


../examples/browserdetect/BrowserDetect.html
../../examples/browserdetect/BrowserDetect.html

==============
P:\Python\Lib\site-packages\Pyjamas-0.5\pyjs>build ../examples/browserdetect/Bro
wserDetect.html
Building '../examples/browserdetect/BrowserDetect.html' to output directory 'P:\
Python\Lib\site-packages\Pyjamas-0.5\pyjs\output'
Creating output directory
Warning: Module HTML file ../examples/browserdetect/BrowserDetect.html.html has
been auto-generated
Copying: pygwt.js
Traceback (most recent call last):
  File "P:\Python\Lib\site-packages\Pyjamas-0.5\pyjs\build.py", line 675, in <mo
dule>
    main()
  File "P:\Python\Lib\site-packages\Pyjamas-0.5\pyjs\build.py", line 672, in mai
n
    options.cache_buster)
  File "P:\Python\Lib\site-packages\Pyjamas-0.5\pyjs\build.py", line 215, in bui
ld
    pygwt_js_template = read_boilerplate(data_dir, "pygwt.js")
  File "P:\Python\Lib\site-packages\Pyjamas-0.5\pyjs\build.py", line 60, in read
_boilerplate
    return open(join(data_dir, "builder/boilerplate", filename)).read()
IOError: [Errno 2] No such file or directory: 'P:\\Python\\share\\pyjamas\\build
er/boilerplate\\pygwt.js'

P:\Python\Lib\site-packages\Pyjamas-0.5\pyjs>
=========
"""
      Builder = 'P:/Python/Lib/site-packages/pyjamas_0.4p1/builder/build.py'


      URL = 'about:blank'
      self.Html.LoadUrl ( URL )
      URL = Output  +  Change_FileExt ( FileName, 'html' )
      ##File_Delete ( URL )

      print
      print '**** PyJamas on:', self.Edit.Filename
      EventLoop = wx.EventLoop.GetActive ()
      while EventLoop.Pending():
        EventLoop.Dispatch()

      #  app_platforms = ['IE6', 'Opera', 'OldMoz', 'Safari', 'Mozilla']
      PID = Run_Python_NoWait (
        [ Builder, self.Edit.Filename, '-o'+ Output,
          '-PIE6,Mozilla' ],
        stdOUT = self.Log_Cmd )

      while PID.poll() == None :
        text = PID.stdout.read()
        if text :
          print text
        text = PID.stderr.read()
        if text :
          print '****** Error: ',text
      print '**** PyJamas Generator Ready'

      # If no html-file available, create one
      Check_Html_File ( self.Edit.Filename, Output )

      URL = 'file:///'+ Output + Change_FileExt ( FileName, '.html' )
      print '***** PyJamas_Result:', URL
      #self.Html.LoadUrl ( URL )

      Mozilla = '"P:/portable/FirefoxPortable_Old2/App/firefox/firefox.exe" %F'
      Safari  = '"P:/Program Files/Safari/Safari.exe" %F'
      IE      = '"C:/Program Files/Internet Explorer/iexplore.exe" %F'

      Browsers = [ Mozilla ] #, IE ]

      Beep ()
      for Browser in Browsers :
        command = Browser.replace ( '%F', URL )
        Run ( command )

      self.Html.LoadUrl ( URL )

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
          #print '$$' + line + result + '$$\n'
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
  def On_Close ( self, event ) :
    self.Edit.Leave_Editor_On_BP ()
    self.Debugger.Stop_Debug_Application()

    self.Edit.SaveFile ( self.Main_File, self.All_BreakPoints, True )

    if self.Ini_File :
      self.Ini_File.Section = self.Ini_Section
      self.wxGUI.Save_Settings ()
    event.Skip()
    #for Control in self.Control_Names :

    PG.Restore_StdOut ( self.Log_Cmd )
    PG.Restore_StdErr ( self.Log_Cmd )

    event.Skip ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
if __name__ == '__main__':
  My_Main_Application ( Control_IDE_Form, Splash = 'meter.png' )
