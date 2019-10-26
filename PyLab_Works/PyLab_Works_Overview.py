import __init__

# ***********************************************************************

from General_Globals import *
from language_support import  _, Language_Current, Set_Language, Flag_Object
from language_support import *
Set_Language ( 'US', True )
from dialog_support import Show_Message
# ***********************************************************************


# ***********************************************************************
__doc__ = """
"""
# ***********************************************************************


# ***********************************************************************
_Version_Text = [[ 0.1 , '14-07-2007', 'Stef Mientki','Test Conditions:', (2,),_(0, ' - orginal release')]]
# ***********************************************************************

from   help_support    import IEHtmlWindow
from   gui_support     import *
from   file_support    import *
from   inifile_support import *
from   picture_support import *
from   system_support  import Run_Python, Run_Python_NoWait
import time
import wx.html as  html
import wx.lib.wxpTag
# ***********************************************************************
# Here all widgets must be imported, otherwise html can't find them
# ***********************************************************************
import wxp_widgets
import wxp_draw_widget
# ***********************************************************************

My_BackGround_Color = "#FFFFD4"

# ***********************************************************************
# ***********************************************************************
class Pylab_Works_Overview_Form ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    Title = ""
    My_Frame_Class.__init__ ( self, None, Title, ini, 'Test Form' )

    # because the language is known here, translate the title
    Title = _(1, 'PyLab_Works  Launch  Center ') + '    v' + str ( _Version_Text[0][0] )
    self.SetTitle ( Title )

    self.My_Path = sys._getframe().f_code.co_filename
    self.My_Path = os.path.split ( self.My_Path ) [0]

    bmp_PW    = Get_Image_Resize ( 'vippi_bricks_64.png',          64 )
    bmp_IDE   = Get_Image_Resize ( 'applications-accessories.png', 48 )
    bmp_Lib   = Get_Image_Resize ( 'bieb.png',                     48 )
    bmp_Trans = Get_Image_Resize ( 'romanime0.ico',                48 )

    self.Flags = Flag_Object ()
    bmp_Flag = self.Flags.Get_Flag ( Language_Current[0] )
    if not bmp_Flag.IsOk():
      print("not bmp_Flag.IsOk()")
      bmp_Flag = wx.Bitmap(32,22)
      self.clearBmp ( bmp_Flag )

    self.image_list = Get_Image_List ()

    from Scintilla_support import Base_STC
    from tree_support import Custom_TreeCtrl_Base
    import customtreectrl_SM as CT

    NB_Style = (
                 fnb.FNB_NO_X_BUTTON |
                 fnb.FNB_DROPDOWN_TABS_LIST |
                 fnb.FNB_ALLOW_FOREIGN_DND |
                0 )
    #             fnb.FNB_DCLICK_CLOSES_TABS |
    #             fnb.FNB_MOUSE_MIDDLE_CLOSES_TABS |
    #             fnb.FNB_X_ON_TAB |

    # Button height must be 25 for Ubuntu !!
    # DONT use a FlatNotebook because it misses some essential parts
    #self.NB         ,GUI_Notebook   ,style = NB_Style
    #  self.IE       ,iewin.IEHtmlWindow, style = wx.NO_FULL_REPAINT_ON_RESIZE
    #  self.IE             ,My_HtmlWindow
    GUI = """
    self.NB         ,wx.Notebook
     Panel2         ,PanelHor,  01  ,name  = _(2, 'Main')
      Panel_B       ,wx.Panel  ,size =( 120, -1)
        B_PW        ,BmpBut    ,bitmap = bmp_PW            ,pos = (24, 10) ,size = ( 70,70)
        self.B_Flag ,BmpBut    ,bitmap = bmp_Flag          ,pos = ( 0, 62) ,size = ( 20,14)
        B_PW_Run    ,wx.Button ,label = "PyLab Works"      ,pos = ( 0, 80) ,size = ( 120,25)

        B_IDE       ,BmpBut    ,bitmap = bmp_IDE           ,pos = (24,110) ,size=( 70,70)
        B_IDE_Run   ,wx.Button ,label = "IDE"              ,pos = ( 0,180) ,size=(120,25)

        B_Lib       ,BmpBut    ,bitmap = bmp_Lib           ,pos = (24,210) ,size=( 70,70)
        B_Lib_Run   ,wx.Button ,label = _(7,'Library Manager')  ,pos = ( 0,280) ,size=(120,25)

        B_Trans     ,BmpBut    ,bitmap = bmp_Trans         ,pos = (24,310) ,size=( 70,70)
        B_Trans_Run ,wx.Button ,label = _(8, 'Translation Tool') ,pos = ( 0,380) ,size=(120,25)

        st1         ,wx.StaticText,label = 'CommandLine Flags'  ,pos = (5,410)
        self.cb_debug         ,wx.CheckBox ,label = 'debug'               ,pos = (5,425)
        self.cb_debugfile         ,wx.CheckBox ,label = 'debugfile'           ,pos = (5,440)
      self.Html_main             ,_My_HtmlWindow
     self.Split_Demo         ,SplitterHor, name = 'Demos'
       p4                    ,PanelVer , 1000       ,name = 'Demos'
        self.Tree            ,Custom_TreeCtrl_Base, style_sub = CT.TR_EDIT_LABELS
        p4b                  ,PanelHor ,11    ,name = 'Demos'
          self.B_Expand      ,wx.Button       ,label = "Expand"
          self.B_Collapse    ,wx.Button       ,label = "Collapse"
        p4bb                 ,PanelHor ,11    ,name = 'Demos'
          self.B_Application ,wx.ToggleButton ,label = "Application"
          self.B_Design      ,wx.ToggleButton ,label = "Design"
        self.B_Restore       ,wx.Button       ,label = "Restore Orginal"
       self.Html_demo             ,_My_HtmlWindow

     self.Split_Test       ,SplitterVer    ,name = _(4,'Tests')
      self.List_Test,wx.ListCtrl    ,style = wx.LC_LIST
      p3            ,PanelHor,10    ,name = 'Demos'
       self.Log     ,wx.TextCtrl    ,style = wx.TE_MULTILINE
       p4           ,wx.Panel       ,name = 'Demos'
        B_Run_Sel   ,wx.Button      ,label = "Run Sel"          ,pos = (0,0)
        B_Run_All   ,wx.Button      ,label = "Run All"          ,pos = (0, 25)
        self.CB_Debug     ,wx.CheckBox ,label = 'debug'               ,pos = (0,50)
        self.CB_DebugFile ,wx.CheckBox ,label = 'debugfile'           ,pos = (0,70)
        self.RB_Tests     ,wx.RadioBox ,label='Tests', choices=['Original', 'All', 'Choice'] ,majorDimension=1 ,pos = (0,90)
        self.Test_Choice  ,wx.TextCtrl                          ,pos = (0,175), size =(75,-1)
    """
    self.wxGUI = Create_wxGUI ( GUI, IniName = 'self.Ini_File' )

    self.B_Expand.Bind      ( wx.EVT_BUTTON,       self.On_B_Expand      )
    self.B_Collapse.Bind    ( wx.EVT_BUTTON,       self.On_B_Collapse    )
    self.B_Application.Bind ( wx.EVT_TOGGLEBUTTON, self.On_B_Application )
    self.B_Design.Bind      ( wx.EVT_TOGGLEBUTTON, self.On_B_Design      )
    self.B_Restore.Bind     ( wx.EVT_BUTTON,       self.On_B_Restore     )

    self.Tree.SetBackgroundColour( My_BackGround_Color )
    self.Tree.SetToolTip ( _(0, 'Press Enter or F9 to launch the selected demo' ) )
    self.Tree.SetImageList ( self.image_list ) #, wx.IMAGE_LIST_SMALL)
    html_tree = '../PyLab_Works/html/pw_demos_tree_index.html'
    #v3print ('polppy',os.getcwd(),os.path.normpath(os.path.join(os.getcwd(),'../PyLab_Works/html/pw_demos_tree_index.html')))
    self.Tree.Set_PuntHoofd_Tree ( html_tree )
    #self.Tree.SetItemImage ( 3, 23 )
    self.Tree.Bind ( wx.EVT_TREE_SEL_CHANGED, self.On_Select_Demo )
    self.Tree.Bind ( wx.EVT_TREE_KEY_DOWN,    self.On_Tree_Key    )
    self.Tree.Bind ( wx.EVT_LEFT_DCLICK,      self.On_Tree_DoubleClick )
    
    #self.Tree.Bind ( wx.EVT_RIGHT_DOWN,            self.OnRightDown )
    #self.Tree.Bind ( wx.EVT_CONTEXT_MENU, self.OnShowPopup )

    #self.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggle, b)

    """self.Source_File = 'html/pw_demos.html'
    name_to = 'CSS_translated.html'
    wxp_widgetsTranslate_CSS ( self.Source_File, name_to, self.CallBack_Html )
    self.Html.LoadPage ( name_to )
    """
    self.Html_demo.Load_CSS ( 'html/pw_demos.html', self.CallBack_Html )

    B_PW.SetToolTip        ( _(10, 'Display Information about PyLab Works' ) )
    B_PW_Run.SetToolTip    ( _(11, 'Launch PyLab Works' ) )
    self.B_Flag.SetToolTip ( _(0,  'Change the language' ) )

    B_IDE.SetToolTip       ( _(12, 'Display Information about IDE' ) )
    B_IDE_Run.SetToolTip   ( _(13, 'Launch IDE' ) )

    B_Lib.SetToolTip       ( _(14, 'Display Information about Library Manager' ) )
    B_Lib_Run.SetToolTip   ( _(15, 'Launch Library Manager' ) )

    B_Trans.SetToolTip     ( _(16, 'Display Information about Translation Tool' ) )
    B_Trans_Run.SetToolTip ( _(17, 'Launch Translation Tool' ) )
    # *****************************************************************

    st1.              SetToolTip ( _(0, 'Set Runtime Flags' ) )
    self.cb_debug.    SetToolTip ( _(0, 'Set Runtime Flags' ) )
    self.cb_debugfile.SetToolTip ( _(0, 'Set Runtime Flags' ) )

    # *****************************************************************
    self.NB.SetImageList ( self.image_list )
    self.NB.SetPageImage ( 0, 21 )
    self.NB.SetPageImage ( 1, 66 )
    self.NB.SetPageImage ( 2, 40 )

    self.NB.SetSelection (0)
    self.NB.SetToolTip ( _(0, 'Display General Information about this Notebook tab' ) )
    self.NB.Bind ( wx.EVT_NOTEBOOK_PAGE_CHANGED,  self.OnPageChanged   )
    self.NB.Bind ( wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging  )
    self.NB.Bind ( wx.EVT_LEFT_DOWN,              self.On_NB_Left_Down )
    # *****************************************************************

    self.List_Test.SetImageList ( self.image_list, wx.IMAGE_LIST_SMALL)
    self.List_Test.SetBackgroundColour ( My_BackGround_Color )
    self.Log.SetBackgroundColour  ( My_BackGround_Color )
    self.Test_Files          = []
    self.List_Test_Click_Pos = None
    self.List_Test_N         = None
    self.Test_Run            = False
    self.Test_All            = False
    self.Test_Flags          = ''
    self.List_Test.Bind ( wx.EVT_LIST_ITEM_ACTIVATED, self.On_List_Test_Activated )
    self.List_Test.Bind ( wx.EVT_LIST_ITEM_SELECTED,  self.On_List_Test_Selected  )
    self.List_Test.Bind ( wx.EVT_LEFT_DOWN,           self.On_List_Test_Click     )
    B_Run_Sel.Bind      ( wx.EVT_BUTTON,              self.B_Run_Sel_Click        )
    B_Run_All.Bind      ( wx.EVT_BUTTON,              self.B_Run_All_Click        )
    self.Bind           ( wx.EVT_IDLE,                self.On_Idle                )


    self.Bind ( wx.EVT_CLOSE,  self.On_Close  )

    B_PW.Bind        ( wx.EVT_BUTTON,  self.B_PW_Click    )
    B_IDE.Bind       ( wx.EVT_BUTTON,  self.B_IDE_Click   )
    B_Lib.Bind       ( wx.EVT_BUTTON,  self.B_Lib_Click   )
    B_Trans.Bind     ( wx.EVT_BUTTON,  self.B_Trans_Click )
    self.B_Flag.Bind ( wx.EVT_BUTTON,  self.B_Flag_Click  )

    B_PW_Run.Bind    ( wx.EVT_BUTTON,  self.B_PW_Run_Click    )
    B_IDE_Run.Bind   ( wx.EVT_BUTTON,  self.B_IDE_Run_Click   )
    B_Lib_Run.Bind   ( wx.EVT_BUTTON,  self.B_Lib_Run_Click   )
    B_Trans_Run.Bind ( wx.EVT_BUTTON,  self.B_Trans_Run_Click )

    # show the first page
    self.On_NB_Left_Down ()

  #def NB_Right_Down ( self, event ) :
  #  print 'Meft'

    #from wx.lib import langlistctrl
    #langlistctrl.ap()

  # ******************************************************
  # ******************************************************
  def On_Tree_DoubleClick ( self, event ) :
    self.Launch_Demo ()

  # ******************************************************
  # ******************************************************
  def On_Tree_Key ( self, event ) :
    if event.GetKeyCode() in ( 13, wx.WXK_F9 ) :
      self.Launch_Demo ()
  # ******************************************************
  # ******************************************************
  def Launch_Demo ( self ) :
    wx.BeginBusyCursor()

    item = self.Tree.GetItemText ( self.Tree.GetSelection () ).lower()
    flags = ''
    if self.B_Design.GetValue () :
      if flags : flags += ' '
      flags += '-design'

    # ********************************************************
    # Different treatment when run from Py2EXE dummy
    # ********************************************************
    #v3print ( 'SYSSARG', sys.argv )
    Start_App = os.path.split ( sys.argv[0] )[1]
    My_Path = sys._getframe().f_code.co_filename
    My_Path = os.path.split ( My_Path )[1]
    #v3print ( 'StartaApp/My_Path', Start_App, My_Path )
    Started_From_Myself = Start_App == My_Path

    Parent = self.Tree.GetSelection ().GetParent ()
    Parent_Text = self.Tree.GetItemText ( Parent )
    if Parent_Text != 'Non_pylab_works' :
      filename = os.path.join ( 'pylab_works_programs', item + '.cfg' )
      filename = Get_Abs_Filename_Case ( filename )
      #v3print ( ' ConfigFile =', filename )

      if not ( filename ) : #File_Exists ( filename ) ) :
        line = 'Sorry, cant find file: ' + filename
        Show_Message ( line )
        return
      
      if Started_From_Myself :
        exefile = 'PyLab_Works.py'
        arguments = [ 'python', exefile, item, flags ]
        PID = subprocess.Popen ( arguments,
                                 shell =  ( os.name == 'nt') )
      else :
        exefile = os.path.join ( '..', 'demos_dummy.exe' )
        item = os.path.split ( filename )[1]
        item = os.path.splitext ( item ) [0]
        arguments = [ exefile, item, flags ]
        PID = subprocess.Popen ( arguments,
                                 shell =  ( os.name == 'nt') )
      # ********************************************************

    else :  # rund of non-demo programs
      if Started_From_Myself :
        filename = item.lower() + '.py'
        file = Find_Files ( '../', mask = filename )
        if file :
          #filename = '../' + file[0][0] + '/' + filename
          filename = os.path.join ( self.My_Path, '..', file[0][0] + '/' + filename )
          filename = os.path.normpath ( filename )
          if flags :
            Run_Python ( [ filename, flags ] )
          else :
            Run_Python ( filename )

      else : # windows installer
        filename = '_launch_' + item.lower() + '.exe'
        file = Find_Files ( os.path.join ( os.getcwd(),'..'), mask = filename )
        #print self.My_Path, os.getcwd()
        #print 'FILE',file, filename
        if file :
          filename = 'from_launch_demo_gui.exe'
          exefile = os.path.join ( self.My_Path,'..', filename )
          #print 'RRRRUNN',exefile
          if flags :
            arguments = [ exefile, flags ]
          else :
            arguments = [ exefile ]
          PID = subprocess.Popen ( arguments,
                                   shell =  ( os.name == 'nt') )


    time.sleep ( 5 )
    wx.EndBusyCursor()

  # ******************************************************
  # ******************************************************
  def On_B_Expand ( self, event ) :
    self.Tree.ExpandAll()

  # ******************************************************
  # ******************************************************
  def On_B_Collapse ( self, event ) :
    self.Tree.CollapseAll ()

  # ******************************************************
  # ******************************************************
  def On_B_Application ( self, event ) :
    self.B_Design.SetValue ( not ( self.B_Application.GetValue() ) )

  # ******************************************************
  # ******************************************************
  def On_B_Design ( self, event ) :
    self.B_Application.SetValue ( not ( self.B_Design.GetValue () ) )

  # ******************************************************
  # ******************************************************
  def On_B_Restore ( self, event ) :
    from shutil import copyfile
    item = self.Tree.GetItemText ( self.Tree.GetSelection () ).lower()
    source = os.path.join ( self.My_Path, 'pylab_works_programs_original', item+'.cfg' )
    source = os.path.normpath ( source )
    dest   = os.path.join ( self.My_Path, 'pylab_works_programs', item+'.cfg' )
    dest   = os.path.normpath ( dest )
    copyfile ( source, dest )

  # ******************************************************
  # ******************************************************
  def On_Select_Demo ( self, event ) :
    item = event.GetItem()
    text = self.Tree.GetItemText ( item ).lower()
    level, Mainnode = self.Tree.Get_Item_Level_MainParent ( item )
    dir = '../PyLab_Works/html/'
    if level == 1 :
      #URL = dir + 'pw_tree_' + text + '.html'
      URL = 'html/pw_demos.html'
    else :
      URL = dir + 'pw_demo_' + text + '.html'

    """
    name_to = 'CSS_translated.html'
    wxp_widgets.Translate_CSS ( URL, name_to ) #, self.CallBack_Html )
    self.Html.LoadPage ( name_to )
    """
    self.Html_demo.Load_CSS ( URL )

  # ******************************************************
  # SEE DEBUGGER< WE PROBABLY NEED A STREAM IN FRONT OF
  # ******************************************************
  def On_Idle ( self, event ) :
    event.Skip ()
    if self.Test_Run :

      """
      print 'IDEL',self.Test_PID,
      if self.Test_PID :
        print self.Test_PID.poll()
      else :
        print ' '
      """
      if self.Test_PID and ( self.Test_PID.poll() == None ) :
        #if self.Test_PID.poll() == None :
        #print 'yyp'
        #text = self.Test_PID.stdout.readline () #(100)
        text = self.Test_PID.stdout.read () #(100)
        #print 'lkodp', len ( text )
        #time.sleep(0.1)

        if text :
          self.Log.AppendText ( text )

      else :
        print()
        line = '\n************************ Running '
        for i in range ( self.Test_Prev, self.List_Test.GetItemCount () ) :
          LI = self.List_Test.GetItem ( i )
          Icon = LI.GetImage ()
          if Icon == 16 :
            self.Test_Dir = self.List_Test.GetItemText ( i )
          elif Icon == 83 :
            #script = os.path.join ( self.Test_Dir, self.List_Test.GetItemText ( i ) + '.py' )
            #script = script.replace ( '\\', '/' )
            script = Joined_Paths ( self.Test_Dir, self.List_Test.GetItemText ( i ) + '.py' )

            #self.List_Test.Focus ()
            #self.List_Test.Select ( i_prev, False )
            self.List_Test.Focus ( i )
            self.List_Test.Refresh ()
            #time.sleep(0.02)
            #self.ProcessIdle()
            self.Test_Prev = i + 1
            self.Log.AppendText ( line + script )
            self.Log.AppendText ( '\n************************ Flags : ' + self.Test_Flags + '\n' )

            print ('RPW',script, self.Test_Flags)
            self.Test_PID = Run_Python_NoWait ( [ script, self.Test_Flags ] )
            time.sleep(0.1)
            break
        else :
          self.Test_Run = False
          self.Test_All = False
          line = '\n************************ Tests have finished '
          self.Log.AppendText ( line )

  # ******************************************************
  # ******************************************************
  def B_Run_Sel_Click ( self, event ) :
    self.Test_Flags = ''
    if self.CB_Debug.GetValue() :
      self.Test_Flags += ' -debug'
    if self.CB_DebugFile.GetValue() :
      self.Test_Flags += ' -debugfile'
    tests = self.RB_Tests.GetSelection ()
    if tests == 1 :
      self.Test_Flags += ' -testall'
    elif tests == 2 :
      self.Test_Flags += ' -test' + self.Test_Choice.GetValue ()
    self.Test_PID  = None
    self.Test_Prev = 0
    self.Test_Run  = True

  # ******************************************************
  # ******************************************************
  def B_Run_All_Click ( self, event ) :
    self.Test_All  = True
    self.B_Run_Sel_Click ( event )

  # ******************************************************
  # ******************************************************
  def On_List_Test_Click ( self, event ) :
    event.Skip()
    self.List_Test_Click_Pos = event.GetPosition ()

    if self.List_Test_N and \
       self.List_Test_OnIcon ( self.List_Test_N ) :
      self.Toggle_List_Test_Item ( self.List_Test_N )

  # ******************************************************
  # ******************************************************
  def On_List_Test_Selected ( self, event ) :
    N = event.GetIndex ()
    self.List_Test_N = N
    if  self.List_Test_Click_Pos :
      if self.List_Test_OnIcon ( N ) :
        self.Toggle_List_Test_Item ( N )
    self.List_Test_Click_Pos = None

  # ******************************************************
  # ******************************************************
  def On_List_Test_Activated ( self, event ) :
    event.Skip ()
    N = event.GetIndex ()
    self.Toggle_List_Test_Item ( N )

  # ******************************************************
  # ******************************************************
  def List_Test_OnIcon ( self, N ) :
    if  self.List_Test_Click_Pos :
      X, Y = self.List_Test_Click_Pos
      Icon = self.List_Test.GetItemRect ( N, wx.LIST_RECT_ICON )
      if ( Icon[0] <= X <= (Icon[0]+Icon[2]) ) and \
         ( Icon[1] <= Y <= (Icon[1]+Icon[3]) ) :
        return True
    return False

  # ******************************************************
  # ******************************************************
  def Toggle_List_Test_Item ( self, N ) :
    LI = self.List_Test.GetItem ( N )

    Icon = LI.GetImage ()
    if Icon == 80 :
      Icon = 83
      Color = wx.RED
    elif Icon == 83 :
      Icon = 80
      Color = wx.BLUE
    else :
      return

    LI.SetTextColour ( Color )
    self.List_Test.SetItem ( LI )
    self.List_Test.SetItemImage ( N, Icon )


  # ******************************************************
  # ******************************************************
  def On_NB_Left_Down ( self, event = None ) :
    page = self.NB.GetSelection()
    if page == 0 :
      file = os.path.join ( Application.Dir, 'html', 'pw_launch_main.html' )
      URL = 'file:///'+ file
      self.Html_main.LoadUrl ( URL )
    elif page == 1 :
      file = os.path.join ( Application.Dir, 'html', 'pw_demos.html' )
      """
      name_to = 'CSS_translated.html'
      wxp_widgets.Translate_CSS ( self.Source_File, name_to, self.CallBack_Html )
      """
      self.Html_demo.Load_CSS ( file, self.CallBack_Html )

    if event :
      event.Skip ()

  # ******************************************************
  # ******************************************************
  def OnPageChanging ( self, event ) :
    old = event.GetOldSelection()
    new = event.GetSelection()
    #v3print ( 'BBB',old,new )
    #v3print ( 'changing',self.NB.GetSelection() )
    event.Skip ()

  # ******************************************************
  # ******************************************************
  def OnPageChanged ( self, event ) :
    old = event.GetOldSelection()
    new = event.GetSelection()
    #v3print ( 'CCC',old,new )

    if not ( self.Test_Files ) and ( new == 2 ) :
      wx.BeginBusyCursor()
      Dir = path_split ( Application.Dir ) [0]
      #Dir = Get_Absolute_Path ( Dir )
      Find_Files_1 ( Dir, self.Test_Files )

      Last_Dir = None
      for item in self.Test_Files :

        if item [0] != Last_Dir :
          Last_Dir = item [0]
          Rel_Dir  = Get_Relative_Path ( Last_Dir, Dir )
          # Ourselfs is one level deeper !!
          self.List_Test.Append ( ( '../'+ Rel_Dir, ) )
          N = self.List_Test.GetItemCount ()
          self.List_Test.SetItemImage ( N-1, 16 )
          #LI = self.List_Test.GetItem ( N-1 )
          #LI.SetTextColour ( '#FF00FF' ) #wx.RED )
          #self.List_Test.SetItem ( LI )

        self.List_Test.Append ( ( os.path.splitext (item [1])[0],) )

        filename = os.path.join ( item [0], item [1] )
        file = open ( filename, 'r' )
        line = file.read()
        file.close ()
        N = self.List_Test.GetItemCount ()
        LI = self.List_Test.GetItem ( N-1 )
        if line.find ('__main__') >= 0 :
          LI.SetTextColour ( ( 0, 0, 250 ) )
          self.List_Test.SetItem ( LI )
          self.List_Test.SetItemImage ( N-1, 80 )
        else :
          LI.SetTextColour ( ( 200, 200, 200 ) )
          self.List_Test.SetItem ( LI )

      self.List_Test.SetColumnWidth ( 0, 140 )
      wx.EndBusyCursor()
    event.Skip ()

  # ******************************************************
  # CallBack from a button in the demos form
  # ******************************************************
  def CallBack_Html ( self, ID ) :
    print ('********* BEEER', ID)
    if ID == 0 :
      Run_Python ( [ 'PyLab_Works.py', 'aap' ] )

  # ******************************************************
  # ******************************************************
  def B_PW_Run_Click ( self, event ) :
    Run_Python ( [ 'PyLab_Works.py' ] )

  # ******************************************************
  # ******************************************************
  def B_IDE_Run_Click ( self, event ) :
    Run_Python ( 'PyLab_Works_Debugger.py' )

  # ******************************************************
  # ******************************************************
  def B_Lib_Run_Click ( self, event ) :
    Run_Python ( 'PyLab_Works_Library_Manager.py' )

  # ******************************************************
  # ******************************************************
  def B_Trans_Run_Click ( self, event ) :
    Run_Python ( '../support/multi_language.py' )

  # ******************************************************
  # ******************************************************
  def B_PW_Click ( self, event ) :
    file = os.path.join ( Application.Dir, 'html', 'pw_launch_pw.html' )
    URL = 'file:///'+ file
    self.Html_main.LoadUrl ( URL )

  # ******************************************************
  # ******************************************************
  def B_IDE_Click ( self, event ) :
    file = os.path.join ( Application.Dir, 'html', 'pw_launch_ide.html' )
    URL = 'file:///'+ file
    self.Html_main.LoadUrl ( URL )

  # ******************************************************
  # ******************************************************
  def B_Lib_Click ( self, event ) :
    file = os.path.join ( Application.Dir, 'html', 'pw_launch_lib.html' )
    URL = 'file:///'+ file
    self.Html_main.LoadUrl ( URL )

  # ******************************************************
  # ******************************************************
  def B_Trans_Click ( self, event ) :
    file = os.path.join ( Application.Dir, 'html', 'pw_launch_trans.html' )
    URL = 'file:///'+ file
    self.Html_main.LoadUrl ( URL )

  # ******************************************************
  # ******************************************************
  def B_Flag_Click ( self, event ) :
    #global Language_Current
    print ('LANGUAGE FLAG', Language_Current[0])
    if Language_Current[0] == 'NL' :
      Language = 'US'
    else :
      Language = 'NL'
      
    bmp_Flag = self.Flags.Get_Flag ( Language )
    if not bmp_Flag.IsOk () :
      bmp_Flag = wx.Bitmap ( 32, 22 )
      self.clearBmp ( bmp_Flag )
      
    self.B_Flag.SetBitmapLabel ( bmp_Flag )
    
    Set_Language ( Language )

  # ******************************************************
  # ******************************************************
  def On_Close ( self, event ) :
    if self.Ini_File :
      self.Ini_File.Section = self.Ini_Section
      self.wxGUI.Save_Settings ()

    event.Skip()

# ***********************************************************************
# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  My_Main_Application ( Pylab_Works_Overview_Form )
# ***********************************************************************
#pd_Module ( __file__ )
