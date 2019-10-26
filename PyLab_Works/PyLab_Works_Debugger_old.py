
from PyLab_Works_Globals  import *
from system_support import Kill_Process_pid
import time

# ***********************************************************************
from gui_support          import *
from Scintilla_support    import *
# ***********************************************************************


#AR_STARTED  = 1
AR_SET_BP   = 2
AR_CLEAR_BP = 3
#AR_LOCALS   = 4

DS_COMMENT    = 1
DS_BP         = 2
DS_DEL_BP     = 3
DS_LOCALS     = 4
DS_GET_LINENO = 5


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
    self.Expected_Answer = -1
    self.BreakPoints = {}
    self.pid         = None
    self.Running     = False
    self.FileNames   = {}    # Because pdb makes all lowercase

    self.Parent.Bind ( wx.EVT_IDLE, self._On_Idle_Parent )

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

      # fetch the reaction of pdb
      text = self._Get_Response ()
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
      print '*** DELETED ****', text

    # *********************************************************
    # Transport all changes in the breakpoint list to the debugger
    # *********************************************************
    for FileName in self.BreakPoints :
      # store the filenames also in the correct case
      if not ( FileName.lower() in self.FileNames ) :
        self.FileNames [ FileName.lower () ] = FileName
      BP_Files = self.BreakPoints [ FileName ]
      for LineNo in BP_Files :
        BP = BP_Files [ LineNo ]

        # make the changes in the debugger
        
        if BP.BP_Status in ( BPS_DELETED, BPS_CHANGED ) :
          _Delete_BreakPoint ( FileName, LineNo )
          print 'DEL BP', BP.BP_Status
          Print_BP_List ( self.BreakPoints )
        if BP.BP_Status in ( BPS_ADDED, BPS_CHANGED ) :
          _Add_BreakPoint ( FileName, LineNo )
          print 'Add BP', BP.BP_Status
          Print_BP_List ( self.BreakPoints )

        # flag that changes have been made
        if BP.BP_Status == BPS_DELETED :
          BP.BP_Status = BPS_IGNORE
        else :
          BP.BP_Status = BPS_ACTIVE
          
  # *********************************************************
  # *********************************************************
  def Start_Debug_Application ( self, FileName ) :
    if not ( self.Started ) and FileName :
      self.FileName = FileName.replace ( '\\', '/' )
      cmd = 'python -u -m pdb ' + self.FileName
      self.Process = wx.Process ( self.Parent )
      #self.Process.OnTerminate = self.My_Terminate
      self.Process.Redirect()
      self.pid = wx.Execute ( cmd, wx.EXEC_ASYNC, self.Process )

      # wait till pdb reacts
      text = self._Get_Response ()

      self._Update_BreakPoint_List ()
      self.Started = True

  # *********************************************************
  # If no BreakPoint list is specified,
  # the previous BreakPoint list is used
  # *********************************************************
  def Restart ( self, BreakPoint_List = None ) :
    print ' Restart', self.Process, self.Running
    if self.Process :
      print ' YES'
      self.Break ()
    if BreakPoint_List :
      self.Set_Breakpoint_List ( BreakPoint_List )
    self.Start_Debug_Application ( self.FileName )
    self.Go ()

  # *********************************************************
  # *********************************************************
  def Stop_Debug_Application ( self ) :
    print '**** STOP DEBUG', self.Running
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
    print ' Break', self.Process, self.Running
    if self.Process :
      self.Stop_Debug_Application ()

  # *********************************************************
  # *********************************************************
  def _Debug_Set_BP ( self, FileName, LineNo ) :
    self._Update_BreakPoint_List ()
    return
  
    BP = self.BreakPoints [ FileName ] [ LineNo ]
    line = 'break '
    line += FileName + ': '
    line += str ( LineNo + 1 )
    if BP.Condition :
      line += ',' + BP.Condition
    self.Process.GetOutputStream().write( line + '\n' )

    # fetch the reaction of pdb
    text = self._Get_Response ()
    #print 'PDB-response',text
    # Response
    #    Breakpoint 1 at d:\data_python_25\pylab_works\test_ide.py:9
    # sometimes preceeded by:
    #   (Pdb)
    #print '$$$',text.split(),'%%%'
    i = text.find ( 'BreakPoint' )
    text = text [ i+11 : ]
    #print '$$$',text.split(),'%%%'
    BP.Debug_ID = int ( text.split()[0] )


  # *********************************************************
  # First waits till Debugger has reached a breakpoint,
  # Then Updates BreakPoints
  # And set running flag
  # *********************************************************
  def _Update_BPs ( self ) :
    if self.Process and not ( self.Running ):
      self._Update_BreakPoint_List ()
      self.Running = True
      return True

  # *********************************************************
  # *********************************************************
  def Go ( self, event = None ) :
    if self._Update_BPs () :
      self.Process.GetOutputStream().write( 'cont\n' )

  # *********************************************************
  # *********************************************************
  def Step ( self, event = None ) :
    if self._Update_BPs () :
      self.Process.GetOutputStream().write( 'next\n' )

  # *********************************************************
  # *********************************************************
  def Step_Into ( self, event = None ) :
    if self._Update_BPs () :
      self.Process.GetOutputStream().write( 'step\n' )

  # *********************************************************
  # *********************************************************
  def _Get_Response ( self ) :
    while True :
      time.sleep ( 0.02 )
      stream = self.Process.GetInputStream ()
      if stream.CanRead () :
        Line  = stream.read ()

        """
        # sometimes preceeded by:
        #   (Pdb)
        if Line.find ( '(Pdb)' ) == 0 :
          Line = Line [ 6 : ]
        """
        
        return Line

  # *********************************************************
  # *********************************************************
  def Get_Locals ( self ) :
    if self.Process :
      #self.Expected_Answer = AR_LOCALS
      self.Process.GetOutputStream().write( 'dir()\n' )

      #   ['Test_RPDB2', '__builtins__', '__file__', '__name__', 'a']\n(Pdb)
      # sometimes preceeded by:
      #   (Pdb) [
      Dir = self._Get_Response ()
      #print 'DIR',Dir
      Dir = Dir.split ( '\n' )[0]
      if Dir.find ( '(Pdb)' ) == 0 :
        Dir = Dir [ 6 : ]
      Dir = Dir.replace ( '[', '' )
      Dir = Dir.replace ( ']', '' )
      Dir = Dir.replace ( "'", '' )
      Dir = Dir.split( ',' )

      NewDir = []
      for item in Dir :
        item = item.strip()
        if item[0] != '_' :
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
        #print '==ONIDLE'
        text  = stream.read()

        lines = text.split ( '\n' )
        for line in lines :

          if line.find ( '> ') == 0 :
            self.Running = False

            # NOTICE LOWERCASE !!
            #   > d:\data_python_25\pylab_works\test_ide.py(10)<module>()
            #   > d:\data_python_25\pylab_works\test_ide_sub.py(3)Test_RPDB2()
            i = line.find ( '(' )
            FileName = line [ 2 : i ]
            ii = line.find ( ')', i )
            lineno = int ( line [ i+1 : ii ] )

            # If the editor has changed the line might be moved
            # so let's ask the editor
            FileName = self.FileNames [ FileName ]
            #print self.BreakPoints, FileName, lineno
            BP = self.BreakPoints [ FileName ] [ lineno - 1 ]
            #lineno = self.CB_Status ( DS_GET_LINENO, BP [3] )
            lineno = self.CB_Status ( DS_GET_LINENO, BP.Scite_ID )

            #print 'BP reached',BP,FileName, lineno
            self.CB_Status ( DS_BP, FileName, lineno )
            #self.CB_Status ( DS_COMMENT, 'uidyt\n' )

            """
            elif ( self.Expected_Answer == AR_SET_BP ) and \
               ( line.find ('Breakpoint') == 0 ) :
              #   Breakpoint 1 at d:\data_python_25\pylab_works\test_ide.py:8
              # Doesn't succeed if Breakpoint set on an empty line
              #   *** Blank or comment
              line = line.split()
              bp_nr = int ( line [1] )
              FileName = line [3]
              i = FileName.find ( ':', 3 )
              lineno = int (  FileName [ i+1 : ].strip() )
              FileName = FileName [ : i ]
              ##self.CB_Comment ( '\n== BP found' )
              ##self.CB_Comment ( '\nFileName =' +FileName )
              ##self.CB_Comment ( '\nlineno =' +str(lineno) )
              if self.BreakPoints.has_key ( -1 ) :
                if ( self.BreakPoints [ -1 ] [0].lower() == FileName ) and \
                   ( self.BreakPoints [ -1 ] [1] == lineno ) :
                  self.BreakPoints [ bp_nr ] = self.BreakPoints [ -1 ]
                  del self.BreakPoints [-1]
              ##for item in self.BreakPoints :
              ##  print '++', item, self.BreakPoints[item]
              self.Expected_Answer = -1
            """

          #   Deleted breakpoint 1
          #elif ( self.Expected_Answer == AR_CLEAR_BP ) and \
          #   ( line.find ('Deleted breakpoint') == 0 ) :
          elif ( line.find ('Deleted breakpoint') == 0 ) :
            #print 'KK',self.Expected_Answer,line [ 18 : ]
            BP = int ( line [ 18 : ].strip() )
            #print BP, self.BreakPoints
            self.CB_Status ( DS_DEL_BP, self.BreakPoints [BP][0],
                                        self.BreakPoints [BP][1] )
            #del self.BreakPoints [ BP ]

          elif line.find ( '-> ') == 0 :
            pass
          elif line.find ( '(Pdb)') == 0 :
            pass
          elif line.find ( '--Call--') == 0 :
            pass
          elif line.find ( '--Return--') == 0 :
            pass
          elif line.strip() == '' :
            pass

          else :
            #self.CB_Comment ( line + '\n')
            self.CB_Status ( DS_COMMENT, line + '\n')

          """
          if line.find ( '<bp>' ) == 0 :
            i = line.find ( '\t' )
            FileName = line [ 4 : i ]
            lineno   = int ( line [ i+1 : ].strip() )

            self.CB_Status ( 1, FileName, lineno )

          # Step over Call and Return
          elif ( line.find ( '--Call--' )   == 0 ) or \
               ( line.find ( '--Return--' ) == 0 ) :
            self.Process.GetOutputStream().write( 's\n' )

          elif line :
            self.CB_Comment ( line )
          """
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Simple_Test_Form ( My_Frame_Class ) :

  # *****************************************************************
  # *****************************************************************
  def __init__( self, main_form= None, ini = None ) :

    Title = 'PyLab_Works Debugger Test    v' + str ( _Version_Text[0][0] )
    My_Frame_Class.__init__ ( self, main_form, Title, ini, 'Test Form' )

    GUI = """
    Main_Panel           ,PanelVer, 01
      panel               ,PanelHor, 000000
        Button_BPs        ,wx.Button , label = 'Toggle BPs'
        Button_Pause      ,wx.Button , label = 'Pause'
        Button_Run        ,wx.Button , label = 'Run'
        Button_Step       ,wx.Button , label = 'Step'
        Button_Step_Into  ,wx.Button , label = 'Step Into'
        Button_Restart    ,wx.Button , label = 'Restart'
      self.SplitV         ,SplitterVer
        self.Edit         ,Base_STC
        self.Edit2         ,Base_STC
    """
    #exec ( Create_wxGUI ( GUI ) )
    self.wxGUI = Create_wxGUI ( GUI ) #, IniName = 'self.Ini_File' )

    # Allow BreakPoints Margin
    self.Edit.Margin_On ( 2 )

    # we create the debugger here
    self.Current_Line = None
    self.Main_File = 'D:/Data_Python_25/PyLab_Works/test_IDE.py'
    self.Debugger = PW_PDB ( self, self.Set_Debug_Status )
    self.All_BreakPoints = self.Edit.LoadFile ( self.Main_File )
    self.Var_Hist = {}

    self.Bind ( wx.EVT_CLOSE,  self.On_Close  )
    self.Bind ( wx.EVT_BUTTON, self.On_Button_BPs,       Button_BPs       )
    self.Bind ( wx.EVT_BUTTON, self.On_Button_Break,     Button_Pause     )
    self.Bind ( wx.EVT_BUTTON, self.On_Button_Run,       Button_Run       )
    self.Bind ( wx.EVT_BUTTON, self.On_Button_Step,      Button_Step      )
    self.Bind ( wx.EVT_BUTTON, self.On_Button_Step_Into, Button_Step_Into )
    self.Bind ( wx.EVT_BUTTON, self.On_Button_Restart,   Button_Restart   )

  # *******************************************************
  # *******************************************************
  def Set_Debug_Status ( self, Status, Filename = None, Lineno = None ):
    #Print 'Set_Debu
    if Status == DS_COMMENT :
      pass #print Filename

    elif Status == DS_GET_LINENO :
      Scite_ID = Filename
      #print '===',Scite_ID,self.Edit.MarkerLineFromHandle ( Scite_ID )
      return self.Edit.MarkerLineFromHandle ( Scite_ID )

    elif Status == DS_BP :  # Breakpoint reached
      #self.TB.Enable_Buttons ( Debug_Button_Break )
      self.Load_Editor ( Filename, Lineno )
      self.Debugger.Get_Locals ()

    elif Status == DS_LOCALS :
      self.Display_Vars ( Filename )

    elif Status == DS_DEL_BP :
      #print ' DEL BP' ,Filename,Lineno
      for Edit in self.Editors :
        if Filename == Edit [2] :
          #Lineno -= 1
          # first remove all bp markers at this line
          i = 0x0F & ( ( Edit[0].MarkerGet ( Lineno-1 ) & Edit[0].Break_Mask ) >> 11 )
          n = 1
          while i > 0 :
            if i & 1 :
              Edit[0].MarkerDelete ( Lineno-1, 10 + n )
              Edit[0].MarkerDelete ( Lineno-1, 15 + n )
            n += 1
            i = i >> 1

          #print '****A',Filename,Lineno,self.Current_Line
          if ( self.Current_Line [0] == Filename ) and \
             ( self.Current_Line [1] == Lineno - 1   ) :
            Marker = Edit[0].MarkerGet ( Lineno - 1 ) & Edit[0].Break_Mask
            self.Current_Line = [ Filename, Lineno - 1, Marker ] #, -1 ]
          break

    else :
      self.TB.Enable_Buttons ( Debug_Button_Running )
    #print 'Set_Debug_Status', Status, Filename, Lineno

  # *********************************************************
  # Called by Debugger, when debug starts again, leaving a breakpoint
  # *********************************************************
  def Restore_Original_Markers ( self ) :
    # Delete ALL current line markers
    # restore the markers of the old current line
    if self.Current_Line :
      self.Edit.MarkerDeleteAll ( 10 )
      self.Edit.MarkerDeleteAll ( 15 )
      #self.Edit.MarkerAddSet ( self.Current_Line[1], self.Current_Line [2] )
      CL = self.Current_Line
      BP = self.All_BreakPoints [ CL[0] ] [ CL[1] ]

      self.Edit.MarkerAddSet ( BP.Scite_Line, BP.Current_Markers & ~self.Edit.Break_Mask )
      #self.Edit.MarkerAddSet ( lineno, self.Current_Line [2] & ~self.Edit.Break_Mask )
      if ( BP.Current_Markers & self.Edit.Break_Mask ) > 0 :
        self.Edit.MarkerAddSet ( BP.Scite_Line, BP.Current_Markers & 0x7800 )

        # first remove all bp markers at this line
        i = 0x0F & ( ( BP.Current_Markers & self.Edit.Break_Mask ) >> 11 )
        n = 1
        while i > 0 :
          if i & 1 :
            break
          n += 1
          i = i >> 1

        #New_Scite_ID = self.Edit.MarkerAdd ( lineno, 15 )
        BP.Scite_ID = self.Edit.MarkerAdd ( BP.Scite_Line, 10 + n )
        self.Edit.MarkerAdd ( BP.Scite_Line, 15 + n )
        BP.BP_Status = BPS_ACTIVE

      else :
        self.Edit.MarkerAdd ( lineno, 10 )
        BP.BP_Status = BPS_IGNORE




      self.Current_Line = None

    # Disable all editors
    self.Edit.SetReadOnly ( True )

  # *********************************************************
  # Called by Debugger, when a new file is needed
  # *********************************************************
  def Load_Editor ( self, filename, lineno = -1 ) :
    # Set Marker on Current Line
    self.Current_Line = [ filename, lineno ] #, self.Edit.MarkerGet ( lineno ), -1 ]
    Current_Markers = self.Edit.MarkerGet ( lineno )

    if self.All_BreakPoints.has_key ( filename ) :
      if self.All_BreakPoints [ filename ]. has_key ( lineno ) :
        self.All_BreakPoints [ filename ] [ lineno ].Current_Markers = Current_Markers

    try :
      self.All_BreakPoints [ filename ] [ lineno ].Current_Markers = Current_Markers
    except :
      self.All_BreakPoints [ filename ] [ lineno ] = BP_Class ( lineno )
      self.All_BreakPoints [ filename ] [ lineno ].BP_Status = BPS_CURRENT
    
    """
    # if a breakpoint, determine the BreakPoint List entry
    Scite_ID = None
    if ( self.Current_Line [2] & self.Edit.Break_Mask ) > 0 :
      BPL = self.All_BreakPoints
      for file in BPL :
        if file == filename :
          BP_File  = BPL [ file ]
          # now the line might be moved,
          # but by quering the Scite_ID we must find the current line
          for line in BP_File :
            Scite_ID = BP_File [ line ].Scite_ID
            if lineno == self.Edit.MarkerLineFromHandle ( Scite_ID ) :
              break
          break
    """
    
    self.Edit.MarkerDelete ( lineno, -1 )
    self.Edit.MarkerAddSet ( lineno, Current_Markers & ~self.Edit.Break_Mask )
    if ( Current_Markers & self.Edit.Break_Mask ) > 0 :
      self.Edit.MarkerAddSet ( lineno, Current_Markers & 0x7800 )
    else :
      self.Edit.MarkerAdd ( lineno, 10 )
    New_Scite_ID = self.Edit.MarkerAdd ( lineno, 15 )
    self.All_BreakPoints [ filename ] [ lineno ] .Scite_ID = New_Scite_ID

    """
    # store the new Scite_ID in the breakpoint list
    # Debug_Line : Condition, Enabled, Scite_Line, Scite_ID, Debug_ID
    if Scite_ID :
      BPL [ file ] [ line ].Scite_Line = lineno
      BPL [ file ] [ line ].Scite_ID   = New_Scite_ID
    """
    
    self.Edit.EnsureVisibleEnforcePolicy ( lineno )
    self.Edit.GotoLine ( lineno )

    self.Edit.SetReadOnly ( False )

  # *******************************************************
  # On a breakpoint, here the local variables are displayed
  # *******************************************************
  def Display_Vars ( self, var_list ) :
    #print 'OOOPPPUUU',type(var_list),var_list

    vars = var_list.keys()
    for key in vars :
      var = var_list [ key ]
      var_line = [ key, var[0], var[1] ]
      if self.Var_Hist.has_key ( key ) :
        hist = self.Var_Hist [ key ]
      else :
        hist = ''

      var_line.append ( hist )
      #print 'VARS', var_line

    for key in vars :
      var = var_list [ key ]
      if self.Var_Hist.has_key ( key ) :
        new = var[0] + ','
        if self.Var_Hist [ key ].find ( new ) != 0 :
          self.Var_Hist [ key ] = var[0] + ',' +self.Var_Hist [ key ]
      else :
        self.Var_Hist [ key ] = var[0] + ','
    #print self.Var_Hist

  # *******************************************************
  # *******************************************************
  def Start_Debugger ( self ) :
    if not ( self.Debugger.Started ) :
      self.Debugger.BreakPoints = self.All_BreakPoints
      self.Debugger.Start_Debug_Application ( self.Main_File )

    self.Restore_Original_Markers ()

  # *********************************************************
  # *********************************************************
  def On_Button_Run ( self, event ) :
    self.Start_Debugger ()
    self.Debugger.Go ()

  # *********************************************************
  # *********************************************************
  def On_Button_Step ( self, event ) :
    self.Start_Debugger ()
    self.Debugger.Step ()

  # *********************************************************
  # *********************************************************
  def On_Button_Step_Into ( self, event ) :
    self.Start_Debugger ()
    self.Debugger.Step_Into ()

  # *********************************************************
  # *********************************************************
  def On_Button_Break ( self, event ) :
    self.Start_Debugger ()
    self.Debugger.Break ()

  # *********************************************************
  # *********************************************************
  def On_Button_Restart ( self, event ) :
    #self.Start_Debugger ()
    self.Restore_Original_Markers ()
    self.Debugger.Restart ()

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
    print 'A',self.All_BreakPoints
    self.Restore_Original_Markers ()
    self.Debugger.Stop_Debug_Application()

    print 'B',self.All_BreakPoints
    self.Edit.SaveFile ( self.Main_File, self.All_BreakPoints, True )
    print 'C',self.All_BreakPoints

    ini = self.Ini_File
    if ini :
      ini.Section = self.Ini_Section
      ini.Write ( 'Pos',  self.GetPosition () )
      ini.Write ( 'Size', self.GetSize () )

    event.Skip ()
# ***********************************************************************


# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  My_Main_Application ( Simple_Test_Form )
# ***********************************************************************
pd_Module ( __file__ )
