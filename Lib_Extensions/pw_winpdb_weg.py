# ***********************************************************************
from pw_winpdb_core    import *
from Scintilla_support import Base_STC
from inifile_support   import inifile
from picture_support   import *
from gui_support       import *

# ***********************************************************************
# Interface between RPDB2 and GUI
# ***********************************************************************
class Simple_RPDB2_Debugger ( CJobs ) :

  def __init__ ( self, parent, filename = None ) :

    # **************************************************************
    # This procedure is called by rpdb2, so it must be local procedure,
    # otherwise we get the self argument extra
    # **************************************************************
    def StartClient ( command_line, fAttach, fchdir,
                      pwd, fAllowUnencrypted, fRemote, host ) :
      self.my_rpd2_pwd               = pwd
      self.my_rpd2_fAllowUnencrypted = fAllowUnencrypted
      self.my_rpd2_fRemote           = fRemote
      self.my_rpd2_host              = host
    # **************************************************************

    self.GUI                   = parent
    self.BP_Initialized        = False
    self.Get_Locals            = False
    self.Get_Locals_First_Time = True
    self.filename              = None
    self.Started               = False

    rpdb2.main ( StartClient )
    self.sm = rpdb2.CSessionManager ( self.my_rpd2_pwd,
                                      self.my_rpd2_fAllowUnencrypted,
                                      self.my_rpd2_fRemote,
                                      self.my_rpd2_host )

    #wx.SystemOptions.SetOptionInt ( "mac.window-plain-transition", 1 )
    CJobs.__init__ ( self )

    self.m_async_sm           = CAsyncSessionManager ( self.sm, self )
    self.m_source_manager     = CSourceManager       ( self, self.sm )
    self.m_stack              = None
    self.m_state              = rpdb2.STATE_DETACHED
    self.m_fembedded_warning  = True
    self.m_last_position_time = 0

    self.m_queue = Queue.Queue()

    # *********************************************************
    # Bind all the callback functions
    # *********************************************************
    callbacks = (
      ( self.update_state,               rpdb2.CEventState              ),
      ( self.update_stack,               rpdb2.CEventStack              ),
      ( self.update_frame,               rpdb2.CEventStackFrameChange   ),
      ( self.update_unhandled_exception, rpdb2.CEventUnhandledException ),
      ( self.update_conflicting_modules, rpdb2.CEventConflictingModules ),
      )
    ##  ( self.update_bp,                  rpdb2.CEventBreakpoint         ),
    for cb in callbacks :
      self.sm.register_callback (
        cb[0], { cb[1] : {} }, fSingleUse = False )

    # *********************************************************
    # test if parent has all the necessary controls
    # *********************************************************
    print '************'
    print self.GUI.Log
    print self.GUI.Log.write
    print self.GUI.Log.flush
    print self.GUI.SetCursor
    ##print self.GUI.Callback_Load_Editor
    print self.GUI.Notify_BreakPoint_Status  #BP_Status
    print self.GUI.Notify_Status
    print self.GUI.Raise
    ##print self.GUI.Restore_Original_Markers
    print self.GUI.Display_Vars
    print '************'

    wx.CallAfter ( self.Start_Debug_Application, filename )

  # *********************************************************
  # *********************************************************
  def Start_Debug_Application ( self, filename ) :
    if not ( self.filename ) and filename :
      self.filename = filename
      self.m_async_sm.launch ( True, filename )
      self.Started = True

  # *********************************************************
  # *********************************************************
  def Stop_Debug_Application ( self ) :
    self.Started = False
    try:
      self.sm.stop_debuggee ()
    except:
      pass

    ##self.m_console.join()   ## hangs the shutdown !!
    self.shutdown_jobs()

    # *********************************************************
    from system_support import Kill_Process, GetAllProcesses

    # we might search als cmd.exe, which commandline contains:
    #   "rpdb2.py"  and  "--debugee --pwd="
    #print GetAllProcesses()
    # and for the python process, ParentProcessID = PID of the cmd.exe
    while Kill_Process ( 'cmd' ) :
      time.sleep ( 0.1 )
    while Kill_Process ( 'python' ) :
      time.sleep ( 0.1 )


  # *********************************************************
  # *********************************************************
  def Put_Command ( self, line ) :
    if line.find ( '>' ) == 0 :
      self.m_queue.put ( line [ 1: ] + '\n' )
    else :
      self.m_queue.put ( 'eval ' + line + '\n' )
      self.Eval_Error = 'exec ' + line + '\n'

  # *********************************************************
  # *********************************************************
  def Get_Breakpoints ( self ) :
    return self.sm.get_breakpoints()

  # *********************************************************
  # *********************************************************
  def Set_Breakpoint ( self, filename, lineno, enable, condition ) :
    print 'Set_Breakpoint',lineno,enable,condition,filename
    self.m_async_sm.set_breakpoint (
        filename, '', lineno, enable, condition )

  # *********************************************************
  # Delete Breakpoint with the specified id,
  # if no id is specified, all breakpoints are removed
  # *********************************************************
  def Delete_Breakpoint_by_ID ( self, id = None ) :
    if id :
      self.m_async_sm.delete_breakpoint ( [id], False )
    else :
      self.m_async_sm.delete_breakpoint ( [], True )

  # *********************************************************
  # Delete Breakpoint from file,line,
  # if no line is specified, all breakpoints are removed
  # *********************************************************
  def Delete_Breakpoint ( self, filename = None, lineno = None ) :
    if lineno :
      bpl = self.Get_Breakpoints ()
      for bp in bpl.values():
        if ( bp.m_filename == filename ) and ( bp.m_lineno == lineno ) :
          self.Delete_Breakpoint_by_ID ( bp.m_id )
    else :
      self.Delete_Breakpoint_by_ID ()

  # *********************************************************
  # *********************************************************
  def Get_BreakPoint_Condition ( self, filename, lineno ) :
    bpl = self.Get_Breakpoints ()
    lineno += 1
    for bp in bpl.values():
      print 'WWWW',bp.m_lineno, lineno,bp.m_filename
      if ( bp.m_filename == filename ) and ( bp.m_lineno == lineno ):
        return bp.m_expr
    return u''

  # *********************************************************
  # Taken over from Scintilla: when the user changes a breakpoint
  # *********************************************************
  def CallBack_On_BreakPoint_Change ( self, filename, lineno, state, Condition = '' ) :
    if state == 0 :
      self.Delete_Breakpoint ( filename, lineno )

    else :
      if state == 1 :
        self.Set_Breakpoint ( filename, lineno, True, Condition )

      elif state == 4 :
        self.Set_Breakpoint ( filename, lineno, True, Condition )

      elif state == 8 :
        self.Set_Breakpoint ( filename, lineno, False, Condition )


  # *********************************************************
  # *********************************************************
  def Go ( self, *args, **kwargs ) :
    print 'GO'
    if self.filename :
      wx.CallAfter ( self.m_async_sm.request_go )

  # *********************************************************
  # *********************************************************
  def Step ( self, *args, **kwargs ) :
    print 'STEP'
    if self.filename :
      wx.CallAfter ( self.m_async_sm.request_next )

  # *********************************************************
  # *********************************************************
  def Step_Into ( self, *args, **kwargs ) :
    print 'INTO'
    if self.filename :
      wx.CallAfter ( self.m_async_sm.request_step )

  # *********************************************************
  # *********************************************************
  def Break ( self, *args, **kwargs ) :
    if self.filename :
      wx.CallAfter ( self.m_async_sm.request_break )

  # *********************************************************
  # *********************************************************
  def Restart ( self, *args, **kwargs ) :
    if self.filename :
      self.Started = False
      try:
        self.sm.stop_debuggee ()
      except:
        pass

      wx.CallAfter ( self.m_async_sm.restart )

  # *********************************************************
  # *********************************************************
  def Set_Cursor ( self, cursor ) :
    self.GUI.SetCursor ( wx.StockCursor ( cursor ) )

  # *********************************************************
  # Procudures for stdin / stdout
  # *********************************************************
  def readline(self):
    _str = self.m_queue.get()
    return _str
  def flush ( self ) :
    pass

  # *********************************************************
  # We take over stdout, so we can filter it,
  # do and exec after an eval failure
  # *********************************************************
  def write ( self, line ) :
    if self.Get_Locals :
      self.Get_Locals = False
      line = line.strip() [ 1 : -1 ]
      varlist = []
      #print line
      m1 = line. find ( ':' )
      b1 = 0
      a = 0
      while m1 > 0 and a < 10:
        m2 = line.find ( ': ', m1 + 1 )
        b2 = line.find ( ',', m1, m2 )
        #print b1,m1,b2,m2, line [m1:m2]
        
        var = line [ b1 : m1 ].strip ()
        if var[0] == "'" :
          var = var [ 1 : -1 ].strip ()
          
        if b2 < 0 : b2 = len ( line ) + 2
        val = line [ m1+1 : b2 ].strip ()
        if val[0] == "'" :
          val = val [ 1 : -1 ].strip ()

        #print 'III', var + ' = ' + val
        if ( var.find ( '__' ) != 0 ) and \
           ( val.find ('<function') < 0 ) and \
           ( val.find ('<module') < 0 ) :
          varlist.append ( [ var, val ] )
          #print '******^^^^^',eval(var)
          
        #print 'ITEM', line [ b1 : m1 ] + ' = ' + line [ m1+ 1 : b2 ].strip()
        b1 = b2 + 1
        m1 = m2
        a += 1

      # Display all local vars
      varlist.sort()
      for item in varlist :
        print item[0] + ' = ' + item[1]

      # IS CALLAFTER NODIG ??
      wx.CallAfter ( self.GUI.Display_Vars, varlist )
      return
    
    if line.strip() == '' :
      return
    if line.find ( rpdb2.STR_OUTPUT_WARNING ) == 0 :
      return
    if line.find ( '*** Debuggee is waiting') == 0 :
      return
  
    #print '$$',line,'%%%'
    if line.find ( rpdb2.CONSOLE_INTRO [: 30] ) == 0 :
      ##CONSOLE_INTRO = ("""RPDB2 - The Remote Python Debugger, version %s,
      ##Copyright (C) 2005-2008 Nir Aides.
      ##Type "help", "copyright", "license", "credits" for more information.""" % (RPDB_VERSION))
      b =  8 + line.find ( 'version' )
      e = line.find ( '.' )
      line = line [b:e].replace ( '\n', '  ' )
      self.GUI.Log.write ( '## **** ' + line +  ' ****\n')

    elif line.find ( "<type 'exceptions" ) == 0 :
      if self.Eval_Error :
        self.m_queue.put ( self.Eval_Error )

        # test if line contains an assignment, e.g. "ff = a + 3"
        line = self.Eval_Error
        self.Eval_Error = ''
        i = line.find ( '=' )
        if i > 0 :
          # then also perform an evaluation of the result
          self.m_queue.put ( 'eval ' + line [ 5:i ] +'\n')
          self.GUI.Log.write ( line[5:i] + ' = ')

      else :
        # more than 1 '\n' !!
        self.GUI.Log.write ( '#' + line.strip ( '\n' ) +'\n')
    else :
      self.GUI.Log.write ( line )

  # *********************************************************
  # *********************************************************
  def update_stack ( self, event ) :
    print '***** Update Stack'
    self.m_stack = event.m_stack
    wx.CallAfter ( self.do_update_stack, event.m_stack )
  def do_update_stack ( self, _stack ) :
    self.m_stack = _stack
    index = self.sm.get_frame_index ()
    self.do_update_frame ( index )

  # *********************************************************
  # *********************************************************
  def update_frame ( self, event ) :
    print '***** Update Frame'
    wx.CallAfter ( self.do_update_frame, event.m_frame_index )
  def do_update_frame ( self, index ) :
    print '***** Update Frame_completion'
    s = self.m_stack [ rpdb2.DICT_KEY_STACK ]
    e = s [ - ( 1 + index ) ]

    filename = e [0]
    lineno   = e [1]

    fBroken  = self.m_stack [ rpdb2.DICT_KEY_BROKEN ]
    _event   = self.m_stack [ rpdb2.DICT_KEY_EVENT ]
    __event  = [ 'running', [ 'call',  _event][index == 0]][fBroken]

    self.m_last_position_time = time.time()

    # *********************************************************
    # INITIALIZATION, HERE
    #   - ALL BREAKPONTS ARE KILLED
    #   - Console manager is created and started
    # *********************************************************
    if not (self.BP_Initialized) :
      self.BP_Initialized = True
      self.Delete_Breakpoint_by_ID ()

      self.GUI.Log.flush = self.flush
      self.m_console = rpdb2.CConsole (
                         self.sm,
                         stdin = self,
                         stdout = self, fSplit = True)
      self.m_console.start()

    #self.GUI.Callback_Load_Editor ( filename, lineno )
    self.GUI.Notify_BreakPoint_Status ( __event, filename, lineno )

  # *********************************************************
  # *********************************************************
  def Initialize ( self ):
    self.update_state ( rpdb2.CEventState ( self.sm.get_state() ) )

  # *********************************************************
  # *********************************************************
  def update_state ( self, event ):
    print '***** Update State',self.m_state
    wx.CallAfter ( self.do_update_state, event)
  def do_update_state(self, event):
    print '***** Update State Completion',self.m_state
    old_state = self.m_state
    self.m_state = event.m_state

    if self.m_state == rpdb2.STATE_DETACHED:
      self.m_fembedded_warning = True
      self.m_source_manager._clear()

    if self.m_state == rpdb2.STATE_BROKEN:
      self.GUI.Raise()

      if self.m_fembedded_warning and self.sm.get_server_info().m_fembedded:
        self.m_fembedded_warning = False
        warning = STR_EMBEDDED_WARNING
        if not warning in g_ignored_warnings:
          dlg = wx.MessageDialog(self.GUI, MSG_WARNING_TEMPLATE % (warning, ), MSG_WARNING_TITLE, wx.OK | wx.CANCEL | wx.YES_DEFAULT | wx.ICON_WARNING)
          res = dlg.ShowModal()
          dlg.Destroy()
          if res == wx.ID_CANCEL:
            g_ignored_warnings[warning] = True
            
    state_text = self.m_state
    if state_text == rpdb2.STATE_BROKEN:
      state_text = 'BreakPoint'
      ##self.GUI.Restore_Original_Markers ()
      if self.Get_Locals_First_Time :
        self.Get_Locals_First_Time = False
      else :
        self.Get_Locals = True
        self.m_queue.put ( 'eval locals ()' + '\n' )
    self.GUI.Notify_Status ( state_text )
    ##self.GUI.Restore_Original_Markers ()

  # *********************************************************
  # *********************************************************
  def update_unhandled_exception(self, event):
    wx.CallAfter(self.notify_unhandled_exception)
  def notify_unhandled_exception(self):
    dlg = wx.MessageDialog(self.GUI, MSG_WARNING_UNHANDLED_EXCEPTION, MSG_WARNING_TITLE, wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
    res = dlg.ShowModal()
    dlg.Destroy()
    if res != wx.ID_YES:
      return
    self.m_async_sm.set_analyze(True)

  # *********************************************************
  # *********************************************************
  def update_conflicting_modules(self, event):
    wx.CallAfter(self.notify_conflicting_modules, event)
  def notify_conflicting_modules(self, event):
    s = ', '.join(event.m_modules_list)
    if not g_fUnicode:
        s = rpdb2.as_string(s, wx.GetDefaultPyEncoding())

    dlg = wx.MessageDialog(self.GUI, rpdb2.STR_CONFLICTING_MODULES % s, MSG_WARNING_TITLE, wx.OK | wx.ICON_WARNING)
    dlg.ShowModal()
    dlg.Destroy()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Demo_Frame ( wx.MiniFrame ):
  def __init__ ( self, Ini = None ):

    self.Ini = Ini
    self.Section = 'Demo_Frame'
    Pos  = ( 0,   650 )
    Size = ( 500, 400 )
    if self.Ini :
      self.Ini.Section = self.Section
      Pos  = self.Ini.Read ( 'Pos',  Pos  )
      Size = self.Ini.Read ( 'Size', Size )
      
    wx.MiniFrame.__init__ ( self, None, -1, 'Test winPDB',
                            size = Size, pos = Pos, style = wx.DEFAULT_FRAME_STYLE )

    GUI = """
      Panel                ,PanelHor, 01
        Panel2             ,wx.Panel,    style = wx.NO_BORDER
          Button_Attach    ,wx.Button,   label = "Attach"
          Button_Go        ,wx.Button,   label = "Go",        pos = ( 0, 30 )
          Button_Break     ,wx.Button,   label = "Break",     pos = ( 0, 60 )
          Button_Step      ,wx.Button,   label = "Step",      pos = ( 0, 90 )
          Button_Step_Into ,wx.Button,   label = "Step Into", pos = ( 0, 120 )
          Button_Restart   ,wx.Button,   label = "Restart",   pos = ( 0, 150 )
          self.BP_ALL      ,wx.CheckBox,                      pos = ( 0, 180 )
          self.Status      ,wx.TextCtrl,                      pos = ( 0, 210 )
          self.BP_Status   ,wx.TextCtrl,                      pos = ( 0, 240 )
        self.SplitterV     ,SplitterVer
          self.NB          ,GUI_Notebook
          self.Log         ,wx.TextCtrl, style = wx.TE_MULTILINE
    """
    exec ( Create_wxGUI ( GUI, Print = True) )
    self.Show ( True )

    wx.CallLater ( wxGUI_Delay, self.SplitterV.SetSashPosition, self.Ini.Read ( 'Splitter', -100 ) )

    # *********************************************************
    self.Editors = []
    self.ImageList = Get_Image_List ()
    self.NB.SetImageList ( self.Image_List)
    # *********************************************************

    self.Current_Line = None

    # we create the debugger here
    filename = 'D:/Data_Python_25/PyLab_Works/PyLab_Works_Library_Manager.py'
    filename = 'D:/Data_Python_25/PyLab_Works/test_IDE.py'
    self.Debugger = Simple_RPDB2_Debugger ( self, filename )

    # after creating the debugger,
    # we can bind the buttons directly to the Debugger methods
    Button_Attach.Bind    ( wx.EVT_BUTTON,   self.On_Button_Attach   )
    Button_Go.Bind        ( wx.EVT_BUTTON,   self.Debugger.Go        )
    Button_Step.Bind      ( wx.EVT_BUTTON,   self.Debugger.Step      )
    Button_Break.Bind     ( wx.EVT_BUTTON,   self.Debugger.Break     )
    Button_Step_Into.Bind ( wx.EVT_BUTTON,   self.Debugger.Step_Into )
    Button_Restart.Bind   ( wx.EVT_BUTTON,   self.Debugger.Restart   )
    self.BP_ALL.Bind      ( wx.EVT_CHECKBOX, self.On_Change_BP_ALL   )

    self.Bind             ( wx.EVT_CLOSE,      self.On_Close     )
    self.Log.Bind         ( wx.EVT_TEXT_ENTER, self.On_Enter_Key )
    self.NB.Bind          ( GUI_EVT_CLOSE_PAGE, self.On_EditPage_Close )


  # *********************************************************
  # *********************************************************
  def On_Change_BP_ALL ( self, event ) :
    print event.IsChecked ()

  # *********************************************************
  # Lines starting with
  #   >    tries to evaluate / execute the rest of the line
  #   >   rest of the line is standard commands to rpdb2
  # *********************************************************
  def On_Enter_Key ( self, event ) :
    IP = self.Log.GetInsertionPoint()
    IP = self.Log.PositionToXY ( IP )
    line = self.Log.GetLineText ( IP [1] )
    if line.find ( '>' ) == 0 :
      self.Debugger.Put_Command ( line )

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

  # *********************************************************
  # if Debugger not started with a filename,
  # it's not really started,
  # so we can do it manual
  # *********************************************************
  def On_Button_Attach ( self, event ) :
    filename = 'D:/Data_Python_25/PyLab_Works/test_IDE.py'
    self.Debugger.Start_Debug_Application ( filename )

  # *********************************************************
  # Called by Debugger, when a new file is needed
  # *********************************************************
  def Callback_Load_Editor ( self, filename, lineno = -1 ) :
    print '****** Load', lineno, filename
    lineno -= 1

    # check if file already open in an editor
    for Edit in self.Editors :
      if filename == Edit [2] :
        break
    else :
      # if not open yet, open it now
      filnams = path_split ( filename )
      filnam  = os.path.splitext ( filnams [1] ) [0]
      self.Log.AppendText ( filnam + ':    '  +filnams [0] + '\n' )
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
    # First Close all editors, except the last one
    for Edit in self.Editors [ 1: ] :
      Edit[0].SaveFile ( Edit[2] )

    # Close the main editor and store all breakpoints
    bpl = self.Debugger.Get_Breakpoints ()
    for Edit in self.Editors [ :1 ] :
      Edit[0].SaveFile ( Edit[2], bpl )

    if self.Ini :
      self.Ini.Section = self.Section
      self.Ini.Write ( 'Pos',  self.GetPosition () )
      self.Ini.Write ( 'Size', self.GetSize     () )
      self.Ini.Write ( 'Splitter', self.SplitterV.GetSashPosition () )

    self.Debugger.Stop_Debug_Application()
    self.Destroy()
# ***********************************************************************



# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':

  test = [1]
  
  # **************************************************************
  # **************************************************************
  if 1 in test :
    filename = 'inifile_debugger_test.ini'
    Ini = inifile ( filename )
    Ini.Section = 'Test'

    app = wx.PySimpleApp ()
    Demo_Frame ( Ini )
    app.MainLoop ()

    Ini.Close ()

# ***********************************************************************
