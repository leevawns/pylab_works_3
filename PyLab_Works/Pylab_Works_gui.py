#! /usr/bin/env python
# order changed to get the right version of VPython (visual)
import __init__
import sys

from General_Globals import *

from numpy    import *
#pd_Module ( 'numpy' )


# ***********************************************************************
# ***********************************************************************
from copy import *
import wx
import wx.adv
import customtreectrl_SM as CT
import time

import os,sys

import PyLab_Works_Globals as PG
from   PyLab_Works_Globals import _

from   file_support    import *
from   dialog_support  import *
from   picture_support import *
from   inifile_support import inifile
from   tree_support    import *
from   menu_support    import *
from   PyLab_Works_shape_container import tPyLabWorks_ShapeCanvas
from   PyLab_Works_appform import *
from   PyLab_Works_search_bricks import *
from   fixed_hint import Fixed_Hint

from scipy.signal import *
from scipy import *
import scipy

import OGLlike as ogl


# ***********************************************************************
# import all bricks libraries
# ***********************************************************************
# doesn't work:
#from bricks import *
print("[INFO : Import ALL bricks lib]")
for brick in Get_PyLabWorks_Bricks_PyFiles () :
  try :
    line = 'import ' + brick
    print(line)
    exec ( line )
    pd_Module ( 'Brick: '+ brick )
  except :
    print('Error importing', brick)
# ***********************************************************************

bw = 56
bh = 22

ID_Open                  = 301
ID_Save                  = 302
ID_Save_As               = 303
ID_Print                 = 304
ID_Print_Preview         = 305
ID_Page_Setup            = 306
ID_Import_Eagle          = 307
ID_Close                 = 308

ID_View_3            = 401
ID_View_NetList          = 402
ID_Demo = 500
ID_Upload_Run_Setting    = 601
ID_Help_Setting          = 602
ID_Upload_Run            = 701

#ID_Dir_Layout            = 801

ID_Help_JALsPy           = 901
ID_Help_JAL              = 902
ID_Send_BugReport        = 903
ID_Check_Version         = 904
ID_About                 = 905

Setting_Help_Names = [ 'JALsPy', 'JAL' ]
class My_MainForm ( wx.Frame ) : #, Menu_Event_Handler):
  def __init__(self, inifile = None):
    # Create the Main_Window
    #   Main_Form
    #      |____ Splitter
    #               |____ Panel_Left
    #               |          |____ Button_1
    #               |          |____ Slider
    #               |
    #               |____ Shape_Container
    #                          |____ Shape
    #
    # *************************************************************
    wx.Frame.__init__( self, None, -1,
      PG.Program_Name + ' (V '+ PG.Version_Nr + ')     no active project   ',
      pos=(0,0), size=(800,600))

    self.closed = False
    #self.inifile = inifile
    self.Modal_Open = False
    self.Custom_Colors = []

    self._printData = wx.PrintData()

    # *************************************************************
    # Define the base menu structure
    # *************************************************************
    menus = [
      ['&File',     [ ( '&New/Open\tCtrl+O', 'Open'    ),
                      ( '&Save\tCtrl+S',     'Save'    ),
                      ( 'Save &As ...',      'Save_As' ),
                      ( '-' ),
                      ( '&Print\tCtrl+P',    'Print'         ),
                      ( 'Pr&int Preview',    'Print_Preview' ),
                      ( 'Page Setup',        'Page_Setup'    ),
                      ( '-' ),
                      ( '&Export',           'Export' ),
                      ( '-' ),
                      ( '&Close',            'Close'  ) ]],
      ['&Edit',     [ ( '&ToDo',             'ToDo'   ),
                      ( '&Edit',             'Edit'   ) ]],
      ['&Settings', [ ( '&ToDo',             'ToDo'   ),
                      ( '&Test',             'Test'   ) ]],
      ['&View',     [ ( '&Hor Layout',       'Dir_Layout'   ),
                      ( '&View',             'View'         ) ]],
      ['&Help',     [ ( 'PyLab_&Works',           'Prog_Help'   ),
                      ( '&Python',                'Python_Help' ),
                      ( '-' ),
                      ( '&Check For New Version', 'Check_New_Version' ),
                      ( 'Send &Bug Report',       'Send_Bug_Report' ),
                      ( 'Ask &OnLine Assistance', 'Ask_Assistance' ),
                      ( '&About',                 'About' ) ]]]

    # Add a dynamic menu to the menubar
    menu_dynamic_items = []
    for i in range ( 10 ) :
      menu_dynamic_items.append ( ( 'Demo ' + str(i) , 'Demo' + str(i) ) )
    menus.insert ( 1, ['Demos', menu_dynamic_items ] )

    # Create the menu
    My_Menus = Class_Menus ( self, My_Menus = menus )


    # Bind events, for the dymanic menu-items, through the whole range
    self.Bind ( wx.EVT_MENU, self.OnMenu_Demos, id=self.ID_Demo0, id2=self.ID_Demo9  )

    self.Bind ( wx.EVT_MENU, self.OnMenu_Dir_Layout, id=self.ID_Dir_Layout )
    self.Bind ( wx.EVT_MENU, self.OnMenu_Test, id=self.ID_Test )
    # *************************************************************



    self.Bind ( wx.EVT_CLOSE, self.OnCloseWindow )
    self.Bind ( wx.EVT_SIZE, self.OnResize )
    #self.Bind(wx.EVT_IDLE,  self.OnIdle)

    #self.SetIcon(wx.Icon('ph_32.ico',wx.BITMAP_TYPE_ICO))
    Path = sys._getframe().f_code.co_filename
    Path = os.path.split ( Path ) [0]
    self.SetIcon ( wx.Icon (
      Joined_Paths ( Path,
      '../pictures/vippi_bricks_323.ico'), wx.BITMAP_TYPE_ICO))

    self.StatusBar = self.CreateStatusBar()
    self.StatusBar.SetFieldsCount(3)
    self.StatusBar.SetStatusWidths([-2, -1, -2])
    self.StatusBar.SetStatusText(' Edit',0)
    self.StatusBar.SetStatusText(' aap',2)
    # *************************************************************



    # *************************************************************
    # first splitter
    # *************************************************************
    self.Splitter = wx.SplitterWindow ( self, 11, style = wx.SP_LIVE_UPDATE)

    self.Splitter_Left = \
      wx.SplitterWindow ( self.Splitter, 11, style = wx.SP_LIVE_UPDATE)
    #self.Tree = MyCustomTreeCtrl (self.Splitter, self,'TREE ROOT')

    self.Shape_Container = tPyLabWorks_ShapeCanvas (
                           self.Splitter, self, pos=(0,0),size=(500,500))

    self.Splitter.SetMinimumPaneSize(20)
    #self.Splitter.SplitVertically( self.Tree, self.Shape_Container, -400)
    self.Splitter.SplitVertically( self.Splitter_Left, self.Shape_Container, -400)
    # *************************************************************

    Panel_Left = wx.Window ( self.Splitter_Left, style = wx.BORDER_SUNKEN)
    Panel_Left.SetBackgroundColour( PG.General_BackGround_Color )
    self.Tree = MyCustomTreeCtrl (self.Splitter_Left, self, 'TREE ROOT')
    self.Splitter_Left.SetMinimumPaneSize(20)
    self.Splitter_Left.SplitHorizontally( Panel_Left ,self.Tree, 26)

    # *************************************************************
    # buttons for simulation control, start at halt
    # *************************************************************
    bw = 50
    bh = 22
    self.B_Edit = wx.ToggleButton(Panel_Left, wx.ID_ANY, "Edit",   pos=(0*bw,0), size=(bw,bh))
    PG.SS_Edit = self.B_Edit.GetId()
    self.B_Run   = wx.ToggleButton(Panel_Left, wx.ID_ANY,   "Run-F9",  pos=(1*bw,0), size=(bw,bh))
    PG.SS_Run = self.B_Run.GetId()
    self.B_Step  = wx.ToggleButton(Panel_Left, wx.ID_ANY,  "Step-F5", pos=(2*bw,0), size=(bw,bh))
    PG.SS_Step = self.B_Step.GetId()
    PG.SS_Stop = PG.SS_Step + 20
    self.B_HighLight  = wx.ToggleButton(Panel_Left, wx.ID_ANY,  "HighLight", pos=(3*bw,0), size=(bw,bh))
    PG.SS_HighLight = self.B_HighLight.GetId()

    Panel_Left.Bind ( wx.EVT_TOGGLEBUTTON, self.OnToggle_B, self.B_Edit )
    Panel_Left.Bind ( wx.EVT_TOGGLEBUTTON, self.OnToggle_B, self.B_Run )
    Panel_Left.Bind ( wx.EVT_TOGGLEBUTTON, self.OnToggle_B, self.B_Step )
    Panel_Left.Bind ( wx.EVT_TOGGLEBUTTON, self.OnToggle_HighLight, self.B_HighLight )

    # Accelerators, these tools are not visisble
    # but we need them for the accelerator shortcut
    Panel_Left.Bind ( wx.EVT_TOOL, self.OnToggle_B, self.B_Step )
    Panel_Left.Bind ( wx.EVT_TOOL, self.OnToggle_B, self.B_Run )
    aTable = wx.AcceleratorTable([\
        ( wx.ACCEL_NORMAL, wx.WXK_F5, PG.SS_Step ),
        ( wx.ACCEL_NORMAL, wx.WXK_F9, PG.SS_Run )
        ])
    Panel_Left.SetAcceleratorTable ( aTable )
    # *************************************************************

    drop_target = MyDropTarget ( self.Shape_Container )
    self.Shape_Container.SetDropTarget ( drop_target )

    # Finally show the mainform
    ##if not (PG.Standalone) :
    if Application.Design_Mode :
      self.Show()

    #self.t1 = wx.Timer(self.Shape_Container)
    # the third parameter is essential to allow other timers
    #self.Shape_Container.Bind(wx.EVT_TIMER, self.OnTimer, self.t1)
    #self.t1.Start(4000)

    self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSplitter)
    #self.Bind ( wx.EVT_SIZE, self.OnResize )

    #from JALsPy_netlist_form  import EVT_JALSPY_NETLIST_WATCHES_CHANGED

    PG.State = PG.SS_Edit
    PG.Execution_HighLight = False #True
    self.B_HighLight.SetValue ( PG.Execution_HighLight )
    self.Update_Buttons()

    # *************************************************************
    # popup menus
    # *************************************************************
    self.Popup_Menu_Tree = My_Popup_Menu ( self.OnPopupItemSelected,
        1, pre = [ _(0,'Set Active Project'),
                   _(0,'Insert New')] )

    #self.Tree.Bind ( wx.EVT_CONTEXT_MENU, self.OnShowPopup )
    #self.Tree.Bind ( wx.EVT_RIGHT_UP, self.OnShowPopup )
    self.Tree.Bind ( wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnShowPopup2 )
    #self.Bind ( wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnShowPopup )


    #self.Splitter.Bind ( wx.EVT_KEY_DOWN, self.OnKeyDown0 )
    #self.Tree.Bind ( wx.EVT_KEY_DOWN, self.OnKeyDown1 )
    #self.Shape_Container.Bind ( wx.EVT_KEY_DOWN, self.OnKeyDown2 )
    #self.Bind ( wx.EVT_KEY_DOWN, self.OnKeyDown4 )

    #from Scintilla_Templates import *  #EVT_SCINTILLA_TEMPLATE_INSERT
    #self.Bind ( EVT_SCINTILLA_TEMPLATE_INSERT, self.OnTemplateInsert)


    #frame = Scintilla_Templates_Form ( self, "PyLab Works Snippets", Pos = (20,20) )
    #frame.Show(True)

  #def OnTemplateInsert ( self, event ) :
  #  print event.my_ID
  #  print 'KLSOSP'

  def OnMenu_Test ( self, event ) :
    from system_support import run
    run ( [ 'Python',
            'PyLab_Works_Test_Bench.py' ],
          shell = True )
    self.OnCloseWindow(event)

  def OnMenu_Dir_Layout ( self, event ) :
    if self.Shape_Container.Orientation_Hor :
      self.Shape_Container.Orientation_Hor = None
    else :
      self.Shape_Container.Orientation_Hor = True
    #if PG.OGL_Orientation_Hor :
    #  PG.OGL_Orientation_Hor = None
    #else :
    #  PG.OGL_Orientation_Hor = True
    self.Shape_Container.Refresh ()

  def OnMenu_Open ( self, event ) :
    #print 'Menu open'
    Location = os.path.join ( Application.Dir,
                              PG.Active_Project_SubPath )
    PG.Active_Project_Filename = \
      Ask_File_For_Save ( Location,
                          FileTypes = '*.cfg',
                          Title = '' )
    if not ( PG.Active_Project_Filename ) : return
    self.Tree.Open_New_Project ()


  def OnMenu_View ( self, event ):
    ReCreate_Flow_Code ()
    """
    if not ( PG.Final_App_Form ) :
      #PG.Final_App_Form = my_App_Form (self)
      #PG.Final_App_Form.Show()
      Create_GUI ( PG.Active_Project_Inifile )
    """
    
  def OnToggle_HighLight ( self, event ) :
    PG.Execution_HighLight = self.B_HighLight.GetValue()

  def OnToggle_B ( self, event ):
    ID = event.GetId()
    #self.Activate_State_Button ( ID )
    #print 'BUTTON',ID
    if ID == PG.SS_Step:
      if   PG.State == PG.SS_Stop: PG.State = PG.SS_Step
      else:                        PG.State = PG.SS_Stop
    else: PG.State = ID
    #print ' piepje6',PG.State
    #JG.app.ProcessIdle()
    self.Update_Buttons ()

  def Update_Buttons ( self ):
    if self.B_Edit.GetValue() and ( PG.State != PG.SS_Edit ) :
      ReCreate_Flow_Code ()

    if   PG.State == PG.SS_Edit:
      self.B_Edit.SetValue ( True )
      self.B_Run.SetValue  ( False )
      self.B_Step.SetValue ( False )
      self.B_Step.SetLabel ( 'Step-F5' )
    elif PG.State == PG.SS_Run:
      self.B_Edit.SetValue ( False )
      self.B_Run.SetValue ( True )
      self.B_Step.SetValue ( False )
      self.B_Step.SetLabel ( 'Stop-F5' )
    else: # PG.State in [PG.SS_Step, PG.SS_Stop]:
      self.B_Edit.SetValue ( False )
      self.B_Run.SetValue  ( False )
      self.B_Step.SetValue ( True )
      self.B_Step.SetLabel ( 'Step-F5' )
    self.StatusBar.SetStatusText( ['Edit','ReadOnly'][PG.State != PG.SS_Edit] )

  # Action for dynamic events
  def OnMenu_Demos ( self, event ) :
    print(event.GetId() - self.ID_Demo0)

  def OnKeyDown0 ( self, event ) :
    print('piep0')
  def OnKeyDown1 ( self, event ) :
    print('piep1')
  def OnKeyDown2 ( self, event ) :
    print('piep2')
  def OnKeyDown4 ( self, event ) :
    print('piep4')

  def OnShowPopup ( self, event ) :
    #v3print ( 'OnContextMenu' )
    #print 'GGGGGGGGRRRRRRRRRRR',event.GetPoint(), self.Tree.GetItemText(event.GetItem())
    #self.Tree_Hit_Pos = event.GetPoint ()

    pos = event.GetPosition ()
    pos = self.Tree.ScreenToClient ( pos )
    self.Tree_Hit_Pos = pos
    #v3print ( 'RM-pos', pos )
    self.Splitter.PopupMenu ( self.Popup_Menu_Tree )

  def OnShowPopup2 ( self, event ) :
    #v3print ( 'OnRightMenuItem' )
    #print 'GGGGGGGGRRRRRRRRRRR',event.GetPoint(), self.Tree.GetItemText(event.GetItem())
    self.Tree_Hit_Pos = event.GetPoint ()

    #pos = event.GetPosition ()
    #pos = self.Tree.ScreenToClient ( pos )
    #self.Tree_Hit_Pos = pos
    #v3print ( 'RM-pos', pos )
    self.Splitter.PopupMenu ( self.Popup_Menu_Tree )

  def OnPopupItemSelected ( self, event ) :
    item = self.Popup_Menu_Tree.FindItemById ( event.GetId () )
    text = item.GetText()
    item, hit = self.Tree.HitTest(self.Tree_Hit_Pos)
    #v3print ( 'Item Selected', item, hit, self.Tree.GetItemText (item))

    i = event.Int
    if i == 0 : # Set Active Project
      PG.State = PG.SS_Edit
      #print ' piepje7',PG.State
      PG.Main_Form.Update_Buttons ()
      Load_Project ( self.Tree.GetItemText (item), item )

    elif i == 1 :  # Insert new
      itemParent = self.Tree.GetItemParent(item)
      PG.New_Project_Last_Number += 1
      line = 'New' + str ( PG.New_Project_Last_Number )
      NewItem = self.Tree.InsertItem ( itemParent, item, line )
      PyData = []
      PyData.append ( 0 )
      PyData.append ( 24 )
      PyData.append ( 13 )
      self.Tree.SetPyData ( NewItem, PyData )
      self.Tree.SetItemImage ( NewItem, PyData[1], CT.TreeItemIcon_Normal )
      self.Tree.SetItemImage ( NewItem, PyData[2], CT.TreeItemIcon_Expanded )

  def Save_Settings ( self, ini ):
    if ( 'Load_Save' in Debug_What ) :
      Debug_Dump_Trace (
        'My_MainForm, Save_Settings :',
        '\ninifile =', ini )

    ini.Section = 'General'
    ini.Write ( 'Pos', self.GetPosition() )
    ini.Write ( 'Size', self.GetSize() )
    ini.Write ( 'Splitter', self.Splitter.GetSashPosition ( ))

    # also save the complete TREE
    # but remove the library node from the Tree
    root = self.Tree.GetRootItem ()
    item, cookie = self.Tree.GetFirstChild ( root )
    item = self.Tree.GetNextSibling ( item )
    item = self.Tree.GetNextSibling ( item )
    item = self.Tree.GetNextSibling ( item )
    self.Tree.Delete ( item )
    self.Tree.Tree_2_IniFile ( ini.filename )

  def Load_Settings ( self, ini ):
    if ( 'Load_Save' in Debug_What ) :
      Debug_Dump_Trace (
        'My_MainForm, Load_Settings :',
        '\ninifile =', ini )

    ini.Section = 'General'
    self.SetPosition( ini.Read ( 'Pos' , (0,0) ) )
    self.SetSize( ini.Read ( 'Size' , (800,600) ) )
    wx.CallLater ( wxGUI_Delay, self.Splitter.SetSashPosition, ini.Read ( 'Splitter', 200 ) )

    PG.New_Project_Last_Number = PG.Programs_Inifile.Read ( 'New_Project_Last_Number', PG.New_Project_Last_Number)

    # Load the tree data
    #print 'TreeFile=',ini.filename
    self.Tree.IniFile_2_Tree ( ini.filename )

    #self.Tree.InsertItemBefore
    root = self.Tree.GetRootItem ()
    item, cookie = self.Tree.GetFirstChild ( root )
    item = self.Tree.GetNextSibling ( item )
    item = self.Tree.GetNextSibling ( item )
    MainNode = self.Tree.InsertItem ( root, item, 'Libraries' )
    # *****************************************************************
    # Add all available libraries
    # *****************************************************************
    bmp = wx.Bitmap ( '../pictures/library.png' )
    Lib_Icon = self.Tree.GetImageList().GetImageCount()
    self.Tree.GetImageList().Add ( bmp )
    self.Tree.SetItemImage ( MainNode, Lib_Icon, CT.TreeItemIcon_Normal )
    self.Tree.SetItemBold ( MainNode )

    Libraries = Get_PyLabWorks_Bricks_All_Dict ()
    lib_list = sorted ( Libraries.keys() )
    for Lib in lib_list:
      # import the library
      line = 'import ' + Lib
      exec ( line )

      # get the color from the library (might not be available)
      try :
        Lib_Color = eval (  Lib + '.Library_Color' )
      except :
        Lib_Color = wx.BLACK

      # get the icon from the library (might not be available)
      try :
        # Lib_Icon can either be a index in the imagelist (not..)
        # or the filename of an image file in 'bricks/'
        Lib_Icon = eval (  Lib + '.Library_Icon' )
        # if filename, import the image in the imagelist
        #print 'LLLLL',Lib_Icon,type(Lib_Icon)
        #if type ( Lib_Icon ) == basestring :
        if isinstance ( Lib_Icon, basestring ) :
          bmp = wx.Bitmap ( 'bricks/' + Lib_Icon )
          Lib_Icon = self.Tree.GetImageList().GetImageCount()
          self.Tree.GetImageList().Add ( bmp )
      except :
        Lib_Icon = -1

      # Add the library Node
      NodeName = Lib [6:].replace('_',' ')
      node = self.Tree.AppendItem ( MainNode, NodeName )
      self.Tree.SetItemBold ( node )
      self.Tree.SetItemTextColour ( node, Lib_Color )
      PyData = []
      PyData.append ( 0 )
      PyData.append ( Lib_Icon )
      PyData.append ( Lib_Icon )
      PyData = deepcopy ( PyData )
      self.Tree.SetPyData ( node, PyData )
      if Lib_Icon >= 0 :
        self.Tree.SetItemImage ( node, Lib_Icon, CT.TreeItemIcon_Normal )
      #self.Tree.SetItemImage ( node, Lib_Icon, CT.TreeItemIcon_Expanded )

      # Add the Bricks to the library node
      for Brick in Libraries [ Lib ]:
        subnode = self.Tree.AppendItem ( node, Brick.replace ( '_', ' ' ) )
        self.Tree.SetItemTextColour ( subnode, Lib_Color )
        PyData = deepcopy ( PyData )
        self.Tree.SetPyData ( subnode, PyData )
        if Lib_Icon >= 0 :
          self.Tree.SetItemImage ( subnode, Lib_Icon, CT.TreeItemIcon_Normal )
        #self.Tree.SetItemImage ( subnode, Lib_Icon, CT.TreeItemIcon_Expanded )
    # *****************************************************************
    # *****************************************************************



  def Resize_All (self, event):
    ID = event.GetId()
    ( w, h ) = self.Splitter.GetClientSize()
    w = self.Splitter.GetSashPosition()

  def OnSplitter (self, event):
    self.Resize_All ( event )

  def OnResize(self, event):
    event.Skip()
    self.Resize_All ( event)

  def OnMenu_Close ( self, event ) :
    self.OnCloseWindow ( event )

  def OnCloseWindow ( self, event ) :
    #v3print ( 'Close main', self.Modal_Open)
    
    if not(self.Modal_Open):
      # Save the settings for each device
      # might be called more than once, therefor we use self.closed !!
      if not ( self.closed ) :
        self.closed = True
        Close_Project ()

      PG.App_Running = False
      if PG.State in [ PG.SS_Step, PG.SS_Stop]:
        PG.State = PG.SS_Run
        #print ' piepje8',PG.State
      #v3print ( 'Set False')
      busy = wx.BusyInfo("One moment please, waiting for threads to die...")
      wx.Yield()
