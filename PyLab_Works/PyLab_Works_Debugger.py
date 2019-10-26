import __init__
from language_support import _

# ***********************************************************************
_Version_Text = [

[ 1.0 , '10-10-2008', 'Stef Mientki',
'Test Conditions:', ( 2,),
_(0, ' - orginal release')]

]
import PyLab_Works_Globals as PG
from PyLab_Works_Globals  import *
from General_Globals import *
from system_support import Kill_Process_pid
import time
import wx.adv
# ***********************************************************************
from gui_support          import *
from Scintilla_support    import *
# ***********************************************************************
AR_SET_BP       = 2
AR_CLEAR_BP     = 3

DS_COMMENT      = 1
DS_BP           = 2
DS_LOCALS       = 4
DS_GET_LINENO   = 5
DS_RUNNING      = 6
# ***********************************************************************
class PW_PDB ( object ) :
  # *********************************************************
  # *********************************************************
  def __init__ ( self,
                 Parent,   # we need parent to attach process
                 CB_Debug_Status  = None ) :

    self.Parent     = Parent
    self.CB_Status  = CB_Debug_Status
    self.FileName   = None
    self.Started    = False
    self.Process    = None
    #self.Expected_Answer = -1
    self.BreakPoints = {}
    self.pid         = None
    self.Running     = False
    self.Var_Hist    = {}
    self.Last_BP_FileName = None
    
    self.Parent.Bind ( wx.EVT_IDLE, self._On_Idle_Parent )

  # *********************************************************
  # *********************************************************
  def Set_Main_File ( self, FileName ) :
    self.FileName = FileName.replace ( '\\', '/' )


  # *********************************************************
  # *********************************************************
  def _Update_BreakPoint_List ( self ) :

    # *********************************************************
    # Add 1 breakpoint from the breakpoint list to the debugger
    # *********************************************************
    def _Add_BreakPoint ( FileName, LineNo ) :
      BP = self.BreakPoints [ FileName ] [ LineNo ]

      line = 'break '
      line += FileName + ': '
      line += str ( LineNo + 1 )
      if BP.Condition :
        line += ',' + BP.Condition
      self.Process.GetOutputStream().write( line + '\n' )

      # fetch the reaction of pdb :
      #   break d:\data_python_25\pylab_works\test_IDE.py: 10
      #   *** Blank or comment
      text = self._Get_Response ()
      if text.find ( 'Blank or comment') >= 0 :
        BP.Debug_ID = -1
      else :
        i = text.find ( 'Breakpoint' )
        text = text [ i+11 : ]
        BP.Debug_ID  = int ( text.split()[0] )

    # *********************************************************
    # Delete 1 breakpoint from the breakpoint list to the debugger
    # *********************************************************
    def _Delete_BreakPoint ( FileName, LineNo ) :
      BP = self.BreakPoints [ FileName ] [ LineNo ]
      line = 'clear ' + str ( BP.Debug_ID )
      self.Process.GetOutputStream().write( line + '\n' )

      #  fetch the reaction of pdb, which will look like :
      #Deleted breakpoint NN
      #(Pdb)
      text = self._Get_Response ()
      BP.Debug_ID = -1

    # *********************************************************
    # Transport all changes in the breakpoint list to the debugger
    # *********************************************************
    for FileName in self.BreakPoints :
      BP_Files = self.BreakPoints [ FileName ]
      for LineNo in BP_Files :
        BP = BP_Files [ LineNo ]

        # make the changes in the debugger
        if not ( BP.BP_Status in ( BPS_ACTIVE, BPS_IGNORE ) ) :
          if BP.BP_Status in ( BPS_DELETED, BPS_CHANGED ) :
            _Delete_BreakPoint ( FileName, LineNo )
            #print '****        DEL BP', BP.BP_Status
            #Print_BP_List ( self.BreakPoints )
          if BP.BP_Status in ( BPS_ADDED, BPS_CHANGED ) :
            _Add_BreakPoint ( FileName, LineNo )
            #print '****        Add BP', BP.BP_Status
            #Print_BP_List ( self.BreakPoints )

          # flag that changes have been made
          if BP.BP_Status == BPS_DELETED :
            BP.BP_Status = BPS_IGNORE
          else :
            BP.BP_Status = BPS_ACTIVE
          
  # *********************************************************
  # *********************************************************
  def Start_Debug_Application ( self ) :
    if not ( self.Started ) and self.FileName :
      cmd = 'python -u -m pdb ' + self.FileName
      self.Process = wx.Process ( self.Parent )
      #self.Process.OnTerminate = self.My_Terminate
      self.Process.Redirect()
      self.pid = wx.Execute ( cmd, wx.EXEC_ASYNC, self.Process )

      # wait till pdb reacts
      text = self._Get_Response ()

      """SyntaxError: ('invalid syntax',
      ('d:/data_python_25/pylab_works/test_IDE.py',
       12, 2, 'wx.Button.__init__(dsdpsd, xcz, zxc    \n'))
       > <string>(1)<module>()
       (Pdb)
      """
      if text.find ( ' SyntaxError:' ) :
        self.Stop_Debug_Application ()
        i = text.find ( '(' )
        i = text.find ( '(', i+1 )
        text = text [ i+2 : ]
        i = text.find ( "'" )
        FileName = text [ : i ]
        self.Last_BP_FileName = FileName

        text = text [ i+2 : ]
        i = text.find ( ',' )
        LineNo = int ( text [ : i ] )
        text = text [ i+1 : ]
        i = text.find ( ',' )
        PosNo = int ( text [ : i ] )

        self.CB_Status ( DS_BP, FileName, LineNo - 1 )
        line = 'Syntax Error, Line = ' + str(LineNo)
        line += '  Pos = ' + str ( PosNo ) + '\n'
        line += '  File = ' + FileName + '\n'
        self.CB_Status ( DS_COMMENT, line )

      else :
        self._Update_BreakPoint_List ()
        self.Started = True

  # *********************************************************
  # If no BreakPoint list is specified,
  # the previous BreakPoint list is used
  # *********************************************************
  def Restart ( self, event = None ) :
    if self.Process :
      print ('Restart')
      self.Break ()
    self.Start_Debug_Application ( )
    self.Go ()

  # *********************************************************
  # *********************************************************
  def Stop_Debug_Application ( self ) :
    self.Started = False
    if self.Process :
      self.Process.GetOutputStream().write( 'quit\n' )
      self.Process = None
      time.sleep ( 1 )
      Kill_Process_pid ( self.pid )
      self.pid     = None

  # *********************************************************
  # Tries to stop the running application
  # PDB doesn't support this, so we just kill the application
  # Extra parameter "event", so the procedure can be bind directly
  # *********************************************************
  def Break ( self, event = None ) :
    if self.Process :
      self.Stop_Debug_Application ()

  # *********************************************************
  # First waits till Debugger has reached a breakpoint,
  # Then Updates BreakPoints
  # And set running flag
  # *********************************************************
  def _Init_Running ( self ) :
    if not ( self.Process ) :
      self.Start_Debug_Application ()
    if self.Process and not ( self.Running ):
      self.CB_Status ( DS_RUNNING, self.Last_BP_FileName )
      self._Update_BreakPoint_List ()
      self.Running = True
      return True

  # *********************************************************
  # *********************************************************
  def Go ( self, event = None ) :
    print ('GOGOGO')
    if self._Init_Running () :
      self.Process.GetOutputStream().write( 'cont\n' )

  # *********************************************************
  # *********************************************************
  def Step ( self, event = None ) :
    if self._Init_Running () :
      self.Process.GetOutputStream().write( 'next\n' )

  # *********************************************************
  # *********************************************************
  def Step_Into ( self, event = None ) :
    if self._Init_Running () :
      self.Process.GetOutputStream().write( 'step\n' )

  # *********************************************************
  # Time out should be added !!
  # *********************************************************
  def _Get_Response ( self ) :
    while True :
      time.sleep ( 0.02 )
      stream = self.Process.GetInputStream ()
      if stream.CanRead () :
        Line  = stream.read ()

        # sometimes preceeded by:
        #   (Pdb)
        if Line.find ( '(Pdb)' ) == 0 :
          Line = Line [ 6 : ]

        return Line

  # *********************************************************
  # *********************************************************
  def Get_Locals ( self ) :
    if self.Process :
      self.Process.GetOutputStream().write( 'dir()\n' )

      #   ['Test_RPDB2', '__builtins__', '__file__', '__name__', 'a']\n(Pdb)
      Dir = self._Get_Response ()
      Dir = Dir.split ( '\n' )[0]
      Dir = Dir.replace ( '[', '' )
      Dir = Dir.replace ( ']', '' )
      Dir = Dir.replace ( "'", '' )
      Dir = Dir.split( ',' )

      NewDir = []
      for item in Dir :
        item = item.strip()
        if ( len ( item ) > 0 ) and ( item[0] != '_' ) :
          NewDir.append ( item )
      Dir = NewDir

      Vars = {}
      NewDir = []
      for item in Dir :
        self.Process.GetOutputStream().write( 'whatis ' + item + '\n' )
        line = self._Get_Response ()
        # "Function Test_RPDB2\n(Pdb)
        line = line.split('\n')[0]
        if line[0] == '<' :
          b = 1 + line.find ( "'" )
          e = line.find ( "'", b )
          line = line [ b : e ]
          if line != 'module' :
            Vars [ item ] = [ line ]
            NewDir.append ( item )
      Dir = NewDir

      # now get the values
      for item in Dir :
        self.Process.GetOutputStream().write( 'pp ' + item + '\n' )
        line = self._Get_Response ()
        line  = line.split('\n')[0].strip()
        Vars [ item ].insert ( 0, line )

      # Create a list of Variables
      #   Name   Value   Type  History
      for key in Vars :
        var = Vars [ key ]
        var_line = [ key, var[0], var[1] ]
        if self.Var_Hist.has_key ( key ) :
          hist = self.Var_Hist [ key ]
        else :
          hist = ''
        var_line.append ( hist )

      # Update the history
      for key in Vars :
        var = Vars [ key ]
        if self.Var_Hist.has_key ( key ) :
          new = var[0] + ','
          if self.Var_Hist [ key ].find ( new ) != 0 :
            self.Var_Hist [ key ] = var[0] + ',' +self.Var_Hist [ key ]
        else :
          self.Var_Hist [ key ] = var[0] + ','

      # notify and tansport var-list
      self.CB_Status ( DS_LOCALS, Vars )

  # *********************************************************
  # *********************************************************
  def Put_Command ( self, line ) :
    #print '==PUT',line
    if self.Process :
      if line.find ( '>' ) == 0 :
        self.Process.GetOutputStream().write( line [ 1: ] )
        if line[1]=='q' :
          self.Process = None
          self.Started = False
      else :
        #print 'OOOO',line
        self.Process.GetOutputStream().write( line + '\n' )
        #self.Process.GetOutputStream().write( 'eval ' + line + '\n' )
        #self.Eval_Error = 'exec ' + line + '\n'


  # *********************************************************
  # *********************************************************
  def _On_Idle_Parent ( self, event ) :
    if self.Started and \
       self.Process and \
       self.Process.IsInputOpened() :
      stream = self.Process.GetInputStream()
      if stream.CanRead():
        text  = stream.read()

        #print '******** ONIDLE', text
        #print '******** ONIDLE END **********'

        #*********************************************
        # Uncaught exception, transport text and set dummy BP
        #*********************************************
        if text.find ( 'Uncaught exception' ) >= 0 :
          self.Stop_Debug_Application ()
          self.CB_Status ( DS_COMMENT, text )
          self.CB_Status ( DS_BP )
          return
        #*********************************************

        
        
        lines = text.split ( '\n' )
        for line in lines :

          if line.find ( '> ') == 0 :
            self.Running = False
            # NOTICE LOWERCASE !!
            #   > d:\data_python_25\pylab_works\test_ide.py(10)<module>()
            #   > d:\data_python_25\pylab_works\test_ide_sub.py(3)Test_RPDB2()
            i = line.find ( '(' )

            FileName = line [ 2 : i ]
            self.Last_BP_FileName = FileName

            ii = line.find ( ')', i )
            lineno = int ( line [ i+1 : ii ] )

            # If the editor has changed the line might be moved
            # so let's ask the editor
            # in case of step etc. there don't need to be a BP
            try :
              BP = self.BreakPoints [ FileName ] [ lineno - 1 ]
              lineno = self.CB_Status ( DS_GET_LINENO, FileName, BP.Scite_ID )
            except :
              lineno -= 1
            
            self.CB_Status ( DS_BP, FileName, lineno )

          elif line.find ( '-> ') == 0 :
            pass
          elif line.find ( '(Pdb)') == 0 :
            pass
          elif line.find ( '--Call--') == 0 :
            # Step over Call and Return
            #? self.Process.GetOutputStream().write( 's\n' )
            pass
          elif line.find ( '--Return--') == 0 :
            pass
          elif line.strip() == '' :
            pass

          else :
            self.CB_Status ( DS_COMMENT, line + '\n')
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
# ***********************************************************************
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
class PyLab_Works_Debugger_Form ( My_Frame_Class ) :

  # *****************************************************************
  # *****************************************************************
  def __init__( self, main_form= None, ini = None ) :

    Title = 'PyLab_Works Debugger Test    v' + str ( _Version_Text[0][0] )
    My_Frame_Class.__init__ ( self, main_form, Title, ini, 'Test Form' )

    GUI = """
    self.SplitV2          ,PanelVer, 01
      panel               ,PanelHor, 000000
        Button_BPs        ,wx.Button , label = 'Toggle BPs'
        Button_Pause      ,wx.Button , label = 'Pause'
        Button_Run        ,wx.Button , label = 'Run'
        Button_Step       ,wx.Button , label = 'Step'
        Button_Step_Into  ,wx.Button , label = 'Step Into'
        Button_Restart    ,wx.Button , label = 'Restart'
      self.Split          ,SplitterVer
        self.Edit         ,Base_STC,size = (-1,200)
        self.Log_Cmd      ,Base_STC
    """
    self.wxGUI = Create_wxGUI ( GUI ) #, IniName = 'self.Ini_File' )

    
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
    PG.Set_StdOut ( _Fetch_Output ( self.Log_Cmd ) )
    PG.Set_StdErr ( _Fetch_Output ( self.Log_Cmd ) )
    # *************************************************************

    # Allow BreakPoints Margin
    self.Edit.Margin_On ( 2 )

    # Opne the mian-file and read its breakpoints
    self.Main_File = 'test_IDE.py'
    self.All_BreakPoints = self.Edit.LoadFile ( self.Main_File )

    # we create the debugger here
    # and feed the main-file and breakpoints to the debugger
    self.Debugger = PW_PDB ( self, self.Set_Debug_Status )
    self.Debugger.BreakPoints = self.All_BreakPoints
    self.Debugger.Set_Main_File ( self.Main_File )

    self.Bind ( wx.EVT_CLOSE,  self.On_Close  )
    self.Bind ( wx.EVT_BUTTON, self.On_Button_BPs,      Button_BPs       )
    self.Bind ( wx.EVT_BUTTON, self.Debugger.Break,     Button_Pause     )
    self.Bind ( wx.EVT_BUTTON, self.Debugger.Go,        Button_Run       )
    self.Bind ( wx.EVT_BUTTON, self.Debugger.Step,      Button_Step      )
    self.Bind ( wx.EVT_BUTTON, self.Debugger.Step_Into, Button_Step_Into )
    self.Bind ( wx.EVT_BUTTON, self.Debugger.Restart,   Button_Restart   )

  # *******************************************************
  # *******************************************************
  def Function_Key ( self, key ) :
    print ('FK',key)
    #if key == 11 :  # F12

  # *******************************************************
  # override Scintilla's execute code
  # *******************************************************
  def Execute_Code ( self ) :
    line =  str ( self.Log_Cmd.Code_To_Execute )
    print ('MEMOCODE:',line)
    if line.find ( '>' ) != 0 :
      self.Log_Cmd.AppendText ( '  ==> ' )
      try :
        result = eval ( line  )
        self.Log_Cmd.AppendText ( str ( result ) +'\n' )
      except :
        print ('****,Error')
        exec ( line )
      
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
      print ('VARS: ', Var1)

    else :
      print ('**** Unknown Debugger Response or Comment *****')
      print (Var1, Var2)

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

    ini = self.Ini_File
    if ini :
      ini.Section = self.Ini_Section
      ini.Write ( 'Pos',  self.GetPosition () )
      ini.Write ( 'Size', self.GetSize () )

    PG.Restore_StdOut ( _Fetch_Output ( self.Log_Cmd ) )
    PG.Restore_StdErr ( _Fetch_Output ( self.Log_Cmd ) )

    event.Skip ()
# ***********************************************************************
# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':
  app = wx.App ()

  bmp = Get_Image_Resize ( 'applications-accessories.png', 96 )
  wx.adv.SplashScreen ( bmp,
                    wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
                    500, None,
                    style = wx.NO_BORDER | wx.SIMPLE_BORDER | wx.STAY_ON_TOP )
  wx.Yield ()

  ini = inifile ( os.path.join (os.getcwd(), 'Scintilla.cfg' ))
  ini.Section = 'Scintilla Test'
  Main_Form = PyLab_Works_Debugger_Form ( None, ini )

  # test of wrong case of filename
  if True :
    import rlcompleter

    line = 'wx.W'

    #a = rlcompleter.Completer( locals () )
    a = rlcompleter.Completer( globals() )
    print ('k',a.global_matches( 'w' ))
    print ('k',a.global_matches( 'wx.' ))

    State = 0
    while a.complete ( line, State ) and ( State < 10 ):
      print (a.complete ( line, State ))
      State += 1
  Main_Form.Show()

  app.MainLoop ()

  # The inifile can be used by more forms, so we close it here
  ini.Close ()
# ***********************************************************************
pd_Module ( __file__ )
