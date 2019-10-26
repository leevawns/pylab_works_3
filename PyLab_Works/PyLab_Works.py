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

# ***********************************************************************
# PyData [0] = X X X X   X X X X
#                            | +--- True = Node Checked (not used at this moment)
#                            +----- True = Node Expanded
# PyData [1] = Normal Node Icon
# PyData [2] = Expanded Node Icon
# PyData [3] = depends on the parent of the node (not required)
#                brick in a project : Name of the Brick Instance
# ***********************************************************************
class MyCustomTreeCtrl ( Custom_TreeCtrl_Base ):

  # *************************************************************
  # Creation of the treecontrol
  # *************************************************************
  def __init__(self, parent, parent_form, root_title = 'No Title' ) :
    Custom_TreeCtrl_Base.__init__ ( self, parent)
    self.parent_form = parent_form

    # *************************************************************
    # Event Bindings
    # *************************************************************
    self.Bind ( CT.EVT_TREE_ITEM_GETTOOLTIP,  self.OnToolTip )

    self.Bind ( CT.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginEdit )

    self.Bind ( wx.EVT_MIDDLE_DOWN,           self.OnMiddleDown )

    self.Bind ( CT.EVT_TREE_BEGIN_DRAG,       self.OnBeginDrag )
    self.Bind ( CT.EVT_TREE_END_DRAG,         self.OnEndDrag2 )
    self.Bind ( CT.EVT_TREE_SEL_CHANGED,      self.OnSelectionChanged )

    #self.Bind ( wx.EVT_MOTION , self.OnMouseMoving)
    #self.Bind ( wx.EVT_MOVING , self.OnMouseMoving)

    self.frame_hint = Fixed_Hint("Help","OVERVIEW FUNCTION LIBARRY")

  # *************************************************************
  # if an item of the active project is selected,
  # highlight it on the canvas
  # *************************************************************
  def OnSelectionChanged ( self, event ) :
    item = event.GetItem()
    text = self.GetItemText ( item )
    level, Mainnode = self.Get_Item_Level_MainParent ( item )
    if level > 3 :
      PyData = self.GetPyData ( item )
      if len ( PyData ) > 3 :
        Project = self.Get_Parent_At_Level ( item, 1)
        if self.GetItemText ( Project ) == 'Projects' :
          # get the project name
          Parent = item
          for i in range ( level - 3 ) :
            Parent = Parent.GetParent ()
          if self.GetItemText ( Parent ) == PG.Active_Project_Filename_Only :
            PG.Main_Form.Shape_Container.Select_by_Name ( PyData[3] )

  """
  def OnMouseMoving ( self, event ) :
    pass
    event.Skip()
    #print 'moving'
  """

  # *************************************************************
  # *************************************************************
  def Remove_Device_From_ProjectTree ( self, Device ):
    print("Remove_Device_From_ProjectTree")
    Project_Node = PG.Active_Tree_Project
    item, cookie = self.GetFirstChild ( Project_Node )
    while item :
      PyData = self.GetPyData ( item )
      if PyData [3] == Device.Name :
        self.Delete ( item )
        break
      item = self.GetNextSibling ( item )

  # *************************************************************
  # *************************************************************
  def Open_New_Project ( self ):
    Close_Project()

    path, filename = path_split ( PG.Active_Project_Filename )
    Project_Name = os.path.splitext ( filename )[0]
    #print 'AAAAAA',PG.Active_Project_Filename
    #print 'BBBBBB',Project_Name

    # add a new project to the top of
    # the active projects section in the tree
    node, cookie = self.GetFirstChild ( self.root )
    #print self.GetItemText (node)
    node, cookie = self.GetFirstChild ( node )
    #print self.GetItemText ( node )
    child, cookie = self.GetFirstChild ( node )
    node = self.InsertItemByIndex ( node, 0, Project_Name )
    PG.Active_Tree_Project = node

    PyData = []
    PyData.append ( 0 )
    PyData.append ( 15 )
    PyData.append ( 16 )

    self.SetPyData    ( node, PyData )
    self.SetItemImage ( node, PyData[1], CT.TreeItemIcon_Normal )
    self.SetItemImage ( node, PyData[2], CT.TreeItemIcon_Expanded )

    Load_Project ( Project_Name,
                   PG.Active_Tree_Project )

    # expand the node of the new project
    self.ScrollTo ( node )
    self.EnsureVisible ( node )

  # *************************************************************
  # *************************************************************
  def Insert_Lib_Object ( self, item, x = 50, y = 10 ) :
    print("[INFO] Insert_Lib_Object() fucntion")
    # determine the level ,the parent node, text
    level, Mainnode = self.Get_Item_Level_MainParent ( item )
    text = self.GetItemText (item)
    
    print ('INSERT_LIB',Mainnode,level,text)

    if Mainnode == 'Libraries' :
      if level >= 3:
        # test if we have an active project
        # otherwise ask for a filename
        if not ( PG.Active_Project_Filename ) :
          Location = os.path.join ( Application.Dir,
                                    PG.Active_Project_SubPath )
          PG.Active_Project_Filename = \
            Ask_File_For_Save ( Location,
                                FileTypes = '*.cfg',
                                Title = '' )
          if not ( PG.Active_Project_Filename ) : return

          self.Open_New_Project ()
        # Import <filename>
        line = 'brick_'
        line += self.GetItemText ( item.GetParent() ).replace(' ','_')
        #line = line.lower()
        print("import brick:")
        print(line)
        exec('import ' + line,globals())

        print("Create the object and add to the container")
        line = 'Brick = ' + line
        line += '.t_' + self.GetItemText ( item ).replace(' ','_')
        line += '( PG.Main_Form.Shape_Container, "SN'
        # Create a unique ID
        #line += str ( len ( PG.Main_Form.Shape_Container.Devices) + 1 )
        PG.Active_Project_max_ID += 1
        line += str ( PG.Active_Project_max_ID )

        line += '",Pos = (' + str(x) + ',' + str(y) + ') )'
        print ('insert lib:',line)
        exec(line,globals())

        Lib_PyData = self.GetPyData ( item )
        PyData = []
        PyData.append ( 0 )
        PyData.append ( Lib_PyData [1] )
        PyData.append ( Lib_PyData [1] )
        PyData.append ( Brick.__class__.__name__ )

        # add also to the project in the tree
        node_name = self.GetItemText ( item ) + ' (' + \
                    self.GetItemText ( item.GetParent() ) + ')'
        node = self.AppendItem ( PG.Active_Tree_Project, node_name )
        self.SetPyData    ( node, PyData )
        self.SetItemImage ( node, PyData[1], CT.TreeItemIcon_Normal )
        self.SetItemImage ( node, PyData[2], CT.TreeItemIcon_Expanded )
        self.Expand ( PG.Active_Tree_Project )

        # Add to GUI if visible
        if PG.Final_App_Form :
          # Create the nice library name
          line = Brick.__class__.__module__[6:].replace ( '_', ' ' )
          Brick.Control_Pane = PG.Final_App_Form.Add_Pane (
              Brick,
              Brick.shape.Caption + ' (' + line + ')',
              PG.Active_Project_Inifile )

  # *************************************************************
  # *************************************************************
  def OnMiddleDown ( self, event ):
    print("[INFO] OnMiddleDown function")
    """
    On a Library or a Brick in a Library,
    this will make a sticky note of the doc
    of that Library or Brick.
    """
    # determine the item on which was middle-clicked
    pos = event.GetPosition ()
    item, hit = self.HitTest (pos)

    # now be sure this is the selected item
    self.SelectItem (item, True )

    MainNode = self.Get_Parent_At_Level ( item, 1)

    # If main-parent-node is Libraries and
    # this is an end node, we're on an library function
    # so get the description of that function
    if self.GetItemText ( MainNode ) == 'Libraries' :
      if not ( self.HasChildren ( item ) ):
        MainNode = self.Get_Parent_At_Level ( item, 2)
        lib = self.GetItemText ( MainNode )
        line = 'brick_' + lib.replace( ' ', '_' )
        line = line + '.t_' + self.GetItemText ( item ).replace( ' ', '_' )
        line = line + '.Description'
        #print ('*********',line)
        try :
          line = eval ( line )
        except :
          print('ERROR')
        line = line.strip()
        print("[INFO] : Creat fixed hint 1")
        self.frame_hint.Close()
        self.frame_hint = Fixed_Hint( line, lib + ', ' + self.GetItemText ( item ) )

      else :  # complete library overview
        if self.GetItemText ( item ) != 'Libraries' :
          MainNode = self.Get_Parent_At_Level ( item, 2)
          line = self.Find_All_Descriptions ( self.GetItemText ( MainNode ) )
          print("[INFO] : Creat fixed hint 2")
          self.frame_hint.Close()
          self.frame_hint = Fixed_Hint( line, self.GetItemText ( item ) )


  # *************************************************************
  # Node edit for some nodes
  # *************************************************************
  def OnBeginEdit ( self, event ) :
    print("[INFO] OnBeginEdit function")
    item = event.GetItem ()
    text = self.GetItemText ( item )
    level, Mainnode = self.Get_Item_Level_MainParent ( item )
    # block editing of some of the nodes
    if Mainnode == 'Libraries':
      wx.Bell ()
      event.Veto ()

  """
  # *************************************************************
  # determines the level of a treenode,
  # and the text of the main parent
  # root: level = 0
  # *************************************************************
  def Get_Item_Level_MainParent ( self, item ) :
    level = 0
    MainParent = ''
    while item != self.root :
      if item != self.root :
        MainParent = item
      item = item.GetParent()
      level += 1
    if MainParent : MainParent = self.GetItemText ( MainParent)
    return level, MainParent


  # *************************************************************
  # Find the parent at level=level
  # *************************************************************
  def Get_Parent_At_Level (self, item, level ):
    my_level, Parent = self.Get_Item_Level_MainParent ( item )
    Parent = item
    for i in range ( my_level - level ) :
      Parent = Parent.GetParent ()
    return Parent

  """
  # *************************************************************
  # *************************************************************
  def OnBeginDrag ( self, event ) :
    print("[INFO] OnBeginDrag function")
    self.drag_item = event.GetItem()
    if self.drag_item:
      OK = False
      # editing only allowed in RESET mode
      if PG.State == PG.SS_Edit :
        level,Mainnode = self.Get_Item_Level_MainParent ( self.drag_item )
        if Mainnode == 'Libraries' :
          if level >= 3:
            OK = True

      # if drag is allowed to start
      if OK :
        wx.SetCursor ( wx.Cursor ( wx.CURSOR_BULLSEYE ) )
        event.Allow()
      else :
        wx.Bell
        event.Veto()

  # *************************************************************
  # *************************************************************
  def OnEndDrag2(self, event):
    print("[INFO] OnEndDrag2 function")
    item = event.GetItem()
    if item:
      # this is not a very elegant way, but it works
      # we compare the event-position with the splitter sash-position
      # to determine if it's a tree-drop or a graphical-canvas-drop
      w = self.parent_form.Splitter.GetSashPosition()
      x, y = event.GetPoint()
      if x > w:
        self.Insert_Lib_Object ( self.drag_item, x-w, y+26 )
        #print 'GRAPH-DROP', x-w, y, self.GetItemText(self.drag_item), self.GetItemText(item)
      else :
        pass
    # if the name "OnEndDrag" is used,
    # Skip(0) will call this procedure twice !!
    #event.Skip()

  # *************************************************************
  # *************************************************************
  def Find_All_Descriptions  ( self, module_name ) :
    #print("[INFO] Find_All_Descriptions function")
    module_name = 'brick_' + module_name.replace( ' ', '_' )
    my_classes = get_classes ( module_name )

    exec ( 'import ' + module_name )
    try :
      total = eval ( module_name + '.Description' )
    except :
      total = ''

    for Brick in my_classes :
      line = 't_' + Brick
      total += '\n*** ' + Brick
      line = eval ( module_name + '.t_'+ Brick + '.Description' )
      total += '\n'+ line.strip()

    return total

  # *************************************************************
  # *************************************************************
  def OnToolTip ( self, event ) :
    #print("[INFO] OnToolTip function")
    item = event.GetItem()
    MainNode = self.Get_Parent_At_Level ( item, 1)

    # If main-parent-node is Libraries and
    # this is an end node, we're on an library function
    # so get the description of that function
    if self.GetItemText ( MainNode ) == 'Libraries' :
      if not ( self.HasChildren ( item ) ):
        MainNode = self.Get_Parent_At_Level ( item, 2)
        line = 'brick_' + self.GetItemText ( MainNode ).replace( ' ', '_' )
        line = line + '.t_' + self.GetItemText ( item ).replace( ' ', '_' )
        line = line + '.Description'
        #print '*********',line
        try :
          line = eval ( line )
        except :
          print('EEERRROOORRR')
        line = line.strip()
        line += '\n-- Middle Click for Sticky Note --'
        event.SetToolTip ( wx.ToolTip ( line ) )

      else :  # library overview
        if self.GetItemText ( item ) != 'Libraries' :
          MainNode = self.Get_Parent_At_Level ( item, 2)
          line = self.Find_All_Descriptions ( self.GetItemText ( MainNode ) )
          #frame = Fixed_Hint ( line, self.GetItemText ( item ) )
          line += '\n-- Middle Click for Sticky Note --'
          event.SetToolTip ( wx.ToolTip ( line ) )
  # *****************************************************************
  # *****************************************************************
  def Set_Selected_Item_From_String ( self, line ) :
    print("[INFO] : Set_Selected_Item_From_String function")
    if not ( line ) :
      return None

    # demo1, Active Projects, Projects, TREE ROOT
    line.pop()
    parent, cookie = self.GetFirstChild ( self.root )

    while line :
      itemtext = line.pop()
      item = self.FindItem ( parent, itemtext )
      parent = item
    self.ScrollTo ( item )
    self.EnsureVisible ( item )
    return item

  # *****************************************************************
  # *****************************************************************
  def Get_Selected_Item_As_String ( self, item ) :
    print("[INFO] Get_Selected_Item_As_String function")
    line = []
    while item :
      line.append ( self.GetItemText ( item ) )
      item = self.GetItemParent ( item )
    return line
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class MyDropTarget ( wx.DropTarget ) :
  def __init__ ( self, window ):
    wx.DropTarget.__init__ ( self )
    self.window = window

  def OnDrop ( self, x, y, aap ):
    print('Dropped joepie')
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class Pylab_Work_MainForm ( wx.Frame ) : #, Menu_Event_Handler):

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

    self.Splitter_Left = wx.SplitterWindow ( self.Splitter, 11, style = wx.SP_LIVE_UPDATE)
    #self.Tree = MyCustomTreeCtrl (self.Splitter, self,'TREE ROOT')

    self.Shape_Container = tPyLabWorks_ShapeCanvas (self.Splitter, self, pos=(0,0),size=(500,500))

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
      #PG.Final_App_Form = Pylab_Works_App_Form (self)
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
        'Pylab_Work_MainForm, Save_Settings :',
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
        'Pylab_Work_MainForm, Load_Settings :',
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
        if isinstance ( Lib_Icon, str ) :
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
# ***********************************************************************

# ***********************************************************************
# JALsPy, a JAL simulator
# Simulates JAL code by translating it into Pyon code,
# Simulates Hardware in Analog / Digital /Virtual mode,
# or any combination of these.
# Can import Eagle netlists
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007 Stef Mientki
# mailto:S.Mientki@ru.nl
#
# Problems / Bugs / Limitations / ToDo / To Improve / ..
#  - a lot
#  - exception catching
#
#
# <Version: see JALsPy_globals    ,02-08-2007, Stef Mientki
#    - orginal release
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def Close_Project () :
  #print 'Close'
  if PG.Active_Project_Inifile :
    PG.Active_Project_Inifile.Section = 'Application Window'
    PG.Active_Project_Inifile.Write ( 'Running', PG.State == PG.SS_Run )
    # Save the currunt open project
    PG.Main_Form.Shape_Container.Save_Flow_Design ( PG.Active_Project_Inifile )
    #PG.Active_Project_Inifile.Section = 'Application Window'
    if PG.Final_App_Form :
      PG.Final_App_Form.Save_Settings ( PG.Active_Project_Inifile )
      PG.Final_App_Form.Close()
      PG.Final_App_Form = None
    else :
      PG.Active_Project_Inifile.Section = 'Application Window'
      PG.Active_Project_Inifile.Write ( 'Visible', False )

    PG.Active_Project_Inifile.Close()

  if PG.Active_Tree_Project :
    PG.Main_Form.Tree.SetItemBold ( PG.Active_Tree_Project, False )
    PG.Main_Form.Tree.SetItemTextColour ( PG.Active_Tree_Project, wx.BLACK )
    #PG.Active_Tree_Project = None

  #    PG.Final_App_Form = Pylab_Works_App_Form (self)
  #  PG.Final_App_Form.Show()
# ***********************************************************************

# ***********************************************************************
# Loads a new project and
# if an old project was active save the changes first.
# If no parameter is specified, only the actual file is saved
# and everything is cleared
# ***********************************************************************
def Load_Project ( filename = None, tree_item = None ):
  #PG.State = PG.SS_Edit
  #PG.Main_Form.Update_Buttons ()
  PG.State_Do_Init = True
  PG.State_After_Init = PG.State


  #print ' LOAD_PROJECT1',filename
  Close_Project ()
  PG.Active_Tree_Project = None

  if not ( filename ) : return

  fp, fn = path_split (filename)
  #print fp,'$',fn
  if fp == '' :
    filename = os.path.join ( Application.Dir,
                              PG.Active_Project_SubPath,
                              filename)
  fp, fn = path_split (filename)
  #print 'GGG',filename,fp,fn
  PG.Active_Project_Filename = filename
  PG.Active_Project_Filename_Only = os.path.splitext(fn)[0]
  #v3print ( 'Active Project', PG.Active_Project_Filename_Only )

  # add filename to the mainforms caption
  line = PG.Main_Form.GetLabel()
  line = line [ : line.rfind(')') + 1 ] + '  '
  PG.Main_Form.SetLabel ( line + filename )
  ##PG.Main_Form.Base_Title = len ( line+filename )
  ##print 'HHH',line,'$$$',filename

  PG.Main_Form.Shape_Container.Clear ()
  if filename:
    # Set active project in Tree
    if tree_item :
      PG.Active_Tree_Project = tree_item
      PG.Main_Form.Tree.SetItemBold ( tree_item )
      PG.Main_Form.Tree.SetItemTextColour ( tree_item, wx.RED )

    # split filename / extension
    fne, fe = os.path.splitext (filename)

    config_file = fne + '.cfg'
    ini = PG.Active_Project_Inifile = inifile ( config_file )
    if os.path.exists ( config_file ) :
      #print 'Read Project Config File:', config_file
      PG.Main_Form.Shape_Container.Load_Flow_Design ( ini )

    # Final Application Form
    ini.Section = 'Application Window'
    if not ( ini.Read ('Visible') ) :
      PG.Final_App_Form = None
    else:
      ReCreate_Flow_Code ()

      ini.Section = 'Application Window'
      ##if ini.Read ('Running') or PG.Standalone:
      if ini.Read ('Running') or not (Application.Design_Mode) :
        #print 'Start'
        PG.State = PG.SS_Run
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
output_file   = None
output_lines  = ''
output_bricks = []
Pre_Loop_Code = ''
def output ( indent, line ):
  global output_file, output_lines
  line = (indent-1)*'  ' + line + '\n'
  if output_file :
    output_file.write ( line )
  output_lines += line
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def ReCreate_Flow_Code () :
  print ('********** Recreate FlowCode **********')
  Debug_From()
  if PG.Active_Project_Inifile:
    PG.Main_Form.Shape_Container.Save_Flow_Design ( PG.Active_Project_Inifile )

    #*******************************************************
    # Create a list of Bricks and
    # a list that contains all connected lines
    #*******************************************************
    Bricks = []
    PG.Bricks = []
    Connections = []
    for shape in PG.Main_Form.Shape_Container.diagram.shapes :
      if isinstance ( shape, ogl.Connection_Line ):
        if shape.input and shape.output :
          Connections.append ( shape )
      else :
        Bricks.append ( shape )
        PG.Bricks.append ( shape.Parent )

    #*******************************************************
    #*******************************************************
    PG.Debug_Table.Set_On ( len ( PG.Bricks ) )
    for i, Brick in enumerate ( PG.Bricks ) :
      Brick.Nr = i

    #*******************************************************
    # Test if Bricks have there required inputs connected
    #*******************************************************
    N = len ( Bricks )
    for i in range ( N ):
      Brick = Bricks [ N - 1- i]
      #print 'Brick',Brick,Brick.Parent.N_Inputs,Brick.Parent.__class__.__name__,Brick.Parent.__class__.__module__
      all_connected = True
      for ii in range ( 1, Brick.Parent.N_Inputs ) :
        #print 'ii',ii
        # Test if input required
        #if Brick.Parent.Inputs [ ii + 1] [2] :
        if Brick.Parent.Inputs [ ii ] [2] :
          #test if connected
          for conn in Connections :
            #print 'CCCCC',conn.output, Brick, conn.output[0] == Brick, conn.output[0] is Brick
            if conn.output[0] == Brick :
              break
          else :
            all_connected = False
          if not ( all_connected ) :
            Bricks.remove ( Brick )
            break
      #print 'CONECTED = ', all_connected

    #*******************************************************
    # Generate the Connected outputs, some Bricks use this
    # to determine what they should or should not calculate
    #*******************************************************
    # remove all "output/input connected"
    for Brick in Bricks :
      Brick.Parent.Output_Connected = Brick.Parent.N_Outputs * [ False ]
      Brick.Parent.Input_Connected  = Brick.Parent.N_Inputs  * [ False ]

    # loop through the connections to find the connected outputs
    for conn in Connections :
      Brick = conn.input[0]
      Brick.Parent.Output_Connected [ conn.input[1] ] = True
      Brick = conn.output[0]
      Brick.Parent.Input_Connected  [ conn.output[1] ] = True
      #print 'CONNECTOR',Brick.Parent.Caption
      #print 'BCBC',Brick.Caption,conn


    global output_file, output_lines, output_bricks
    #if PG.NEWW :
    #*******************************************************
    # NEWWWWW
    # Generate the general code
    #*******************************************************
    output_file   = None
    output_lines  = ''
    output_bricks = []
    output ( 1, 'import PyLab_Works_Globals as PG' )
    output ( 1, 'from numpy import *')

    #*******************************************************
    # Generate the code that transports data from Brick to Brick
    #*******************************************************
    for i, Brick in enumerate ( Bricks ):
      started = False
      for ii in range ( 1, Brick.Parent.N_Inputs ) :
        for conn in Connections :
          try:
            if ( conn.output[0] == Brick ) and ( conn.output[1] == ii ) :
              """
              print 'Connection:',
              print conn.input[0].Parent.Caption,conn.input[1],
              print '  == goes to ==  ',
              print conn.output[0].Parent.Caption, conn.output[1]
              """
              j = str( i )
              jj = str ( conn.output[1] )
              oi = Bricks.index (conn.input[0])
              o = str( oi )
              oo = str( conn.input[1] )

              #TODOTODPTODOTOD
              """
              if Brick.Parent.Inputs [ii][1] == PG.TIO_CALLBACK :
                # now for CALLBACK functions,
                # we evaluate the code right away
                # i.e. we connect the output Output_Value
                # to the callback function given by the In
                pass
                #conn.input[0].Parent.Output_Value[conn.input[1]] = \
                #  Brick.Parent.In [ii]

              else :
              """
              if True :
                # GENERATE PG.Bricks[1].Input_Changed[1] = PG.Bricks[0].Output_Changed[1]
                #line = 'PG.Bricks[' + o + '].Out.Receivers[' + oo +\
                #       '] [ PG.Bricks['+ j + '] ] = ( "In",'+ jj + ')'
                temp = 'PG.Bricks['+j+']'
                line = 'PG.Bricks[' + o + '].Out.Receivers[' + oo +\
                       '] [' + temp + '] = ( ' + temp + '.In,' + \
                       temp + '.In_Modified, '+ jj + ')'
                output ( 1, line )

              if Brick.Parent.Inputs [ii][1] == PG.TIO_INTERACTION :
                #print '************** IIIIII'
                temp = 'PG.Bricks['+j+']'
                line = temp + '.In[' + jj + '] =' +\
                      ' PG.Bricks[' + o + '].Out['+ oo + ']'
                output ( 1, line )

              break
          except: # in case of connections, which leads to nothing
            pass

    #*******************************************************
    # generate the excecute commands for each Brick
    #*******************************************************
    #print '**** PRE LOOP CODE\n',output_lines
    global Pre_Loop_Code
    Pre_Loop_Code = deepcopy ( output_lines )

    # MOET DIT VIA EEN FILE
    if Application.TestRun :
      output_file   = open ( PG.Simulation_Filename, 'w' )
      output ( 1, 'try :' )
      output ( 2, 'TestRun_Timer += 1 ')
      output ( 1, 'except :')
      output ( 2, 'TestRun_Timer = 0')

      output ( 1, 'if TestRun_Timer == 100 :')
      output ( 2, 'PG.Final_App_Form.OnClose ( None )' )
      output_file.close()
    #*******************************************************
    # END NEW
    #*******************************************************    
  if not ( PG.Final_App_Form ) :
    filename = path_split ( PG.Active_Project_Filename )[1]
    PG.Final_App_Form = my_App_Form ( PG.Main_Form,title = filename )

    #PG.Final_App_Form.Load_Settings ( ini )
    #PG.Final_App_Form.Show()

    # now check all devices in the hardware configuration file
    # first remove panes that are no longer needed
    panes = PG.Final_App_Form._mgr.GetAllPanes()
    for pane in panes:
      for device in PG.Main_Form.Shape_Container.Devices:
        if pane.name == device.Name:
          break
      else :
        print("DELETE:",pane.name)
        #if pane.IsMovable () :
        PG.Final_App_Form.Delete_Pane ( pane.name )

    # Now add devices that are not yet in the GUI
    for device in PG.Main_Form.Shape_Container.Devices:
      for pane in panes:
        if pane.name == device.Name:
          break
      else :
        # Create the nice library name
        line = device.__class__.__module__[6:].replace ( '_', ' ' )

        device.Control_Pane = PG.Final_App_Form.Add_Pane (device,device.shape.Caption + ' (' + line + ')',PG.Active_Project_Inifile )

    PG.Final_App_Form.Load_Settings ( PG.Active_Project_Inifile )
    PG.Final_App_Form.Show()

    PG.State_Do_Init = True
    PG.State_After_Init = PG.State
    PG.State = PG.SS_Stop
# ***********************************************************************

# ***********************************************************************
# Main program,FOREVER loop
# ***********************************************************************
class Pylab_Works_App ( wx.App ) :

  def OnInit(self):
    if Platform_Windows :
      bmp = wx.Image ('../pictures/vippi_bricks.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    else :
      bmp = wx.Image ('../pictures/vippi_bricks_nt.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    wx.adv.SplashScreen( bmp,
                      wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
                      1000, None,
                      style = wx.NO_BORDER | wx.SIMPLE_BORDER | wx.STAY_ON_TOP )
    wx.Yield ()
    
    return True

  def MainLoop(self):
    # take over the event loop, but save the old one
    #self.My_EventLoop = wx.EventLoop ()
    self.My_EventLoop = wx.GUIEventLoop()
    old = wx.EventLoop.GetActive ()
    wx.EventLoop.SetActive ( self.My_EventLoop )

    PG.App_Running = True
    Previous_Time = time.time()
    Loop_Time = Previous_Time
    Previous_N    = 0
    ######################################

    PG.Cycle_Nr = 1
    PG.State_Do_Init = True
    PG.State_After_Init = PG.State
    PG.State = PG.SS_Stop

    while PG.App_Running :
      if PG.State in [PG.SS_Run, PG.SS_Step]:
        try:
          if not ( ( SIN > 0 ) and ( PG.Execution_HighLight or ( PG.State == PG.SS_Step ))):
            #execfile ( PG.Simulation_Filename, VM_Globals )
            #print("[Test]",Loop_Code)
            exec ( Loop_Code, globals() )
            PG.Cycle_Nr += 1
          else :
            Brick = PG.Bricks [ SI ]
            if Brick.BP_State > 0 :
              Brick.On      = False
              Brick.BP_Flag = True
              Brick._Redraw()
              Brick.BP_Display_Vars ()

            exec ( 'Brick.Exec()', VM_Globals )

            if Brick.BP_State > 0 :
              Brick.BP_Display_Vars ( True )

            SI += 1
            SI %= SIN

            if Brick.BP_State > 0 :
              while ( time.time() - Loop_Time ) < 3 :
                while self.My_EventLoop.Pending():
                  self.My_EventLoop.Dispatch()
                self.ProcessIdle()
                time.sleep ( 0.02 )

              Brick.On      = True
              Brick.BP_Flag = False
              Brick._Redraw()


        except PG.Reload_Exception:
          import traceback
          traceback.print_exc ()
          print('Program aborted in Simulation File')
        except:
          import traceback
          traceback.print_exc ()
          Debug_From ()
          print('Error in Simulation File')

        if PG.State == PG.SS_Step :
          PG.State = PG.SS_Stop
        PG.Main_Form.Update_Buttons ()

      elif PG.State_Do_Init :
        # wait at the start, needed for VPython
        if PG.Cycle_Nr == 1 :
          for i in range ( 5 ):
            while self.My_EventLoop.Pending(): self.My_EventLoop.Dispatch()
            self.My_EventLoop.ProcessIdle()
            time.sleep ( 0.05 )

        ######################################
        VM_Globals = {}
        PG.Brick_Errors = {}
        global Pre_Loop_Code
        exec ( Pre_Loop_Code, VM_Globals )
        """
        print Pre_Loop_Code
        print 'VM_Globals :'
        for key in VM_Globals :
          if key != '__builtins__':
            print 'VMG =', key, ':', VM_Globals [ key ]
        """
        SI = 0
        SIN = len ( PG.Bricks )
        # Should be extended with Post_Code ( test runs)
        #Loop_Code = 'for Brick in PG.Bricks: Brick.Exec()\n'
        #print 'VM:\n',VM_Globals
        Loop_Code = """
for Brick in PG.Bricks:
  Brick.Exec()
"""
        ######################################
        PG.State_Do_Init = False
        PG.State = PG.State_After_Init
      while self.My_EventLoop.Pending(): self.My_EventLoop.Dispatch()
      #self.ProcessIdle()
      self.My_EventLoop.ProcessIdle()

      # normally 50 fps
      ddT = Application.VM_Delay - ( time.time() - Loop_Time )
      if ddT > 0 :
        time.sleep ( ddT )
      Loop_Time = time.time()

      # Every second display fps in statusbar
      # COULD BE USED TO CORRECT THE IDLE TIME !!
      Previous_N += 1
      dT = time.time() - Previous_Time
      if dT > 1.0 :
        line = str ( int ( round ( Previous_N / dT ) ) ) + ' fps'
        Previous_N = 0
        Previous_Time = time.time ()
        try : # Form may already have been removed
          PG.Final_App_Form.SetStatusText ( line, 4 )
        except :
          pass

    print ( 'Finish' )

    # Store debug info
    PG.Debug_Table.Set_On ( )


    # and let the mainform save it's settings
    # this must be done before the subforms are destroyed
    PG.Main_Form.Save_Settings ( PG.Programs_Inifile )
    PG.Programs_Inifile.Section = 'General'
    os.chdir ( Application.Dir )
    if PG.Active_Project_Inifile:
      # relative filenames doesn't work well !!
      # BUT we need relative filenames to be transportable
      # Don't forget to remove the leading backslash
      #print PG.Active_Project_Filename
      #print Application.Dir
      N = len ( os.path.commonprefix (
                 [ Application.Dir, PG.Active_Project_Filename ] ))
      if N == 0 :
        filename = PG.Active_Project_Filename
      else :
        filename = PG.Active_Project_Filename [N+1:]
      filename = filename.replace ( '\\', '/' )
      PG.Programs_Inifile.Write (
          'Project File', filename )

      # the treenode of the active project
      active_treenode = \
        PG.Main_Form.Tree.Get_Selected_Item_As_String (
          PG.Active_Tree_Project )
      PG.Programs_Inifile.Write ( 'Active Tree Item', active_treenode )

      PG.Programs_Inifile.Write ( 'New_Project_Last_Number', PG.New_Project_Last_Number)

    # close other forms, let them save their settings before destroy
    for form in PG.Form_List:
      if form:
        # not every form might have a SaveSettings method !!
        try:
          form.SaveSettings()
        except:
          pass
        form.Close ( True )
        form.Destroy()

    # save the changes of this project
    # AFTER form.SaveSettings,
    # because forms like Scope store their info in the project file !!
    #Save_Project ()
    #PG.Main_Form.Shape_Container.Save_Flow_Design ( PG.Active_Project_Inifile )

    ##pickle.dump( PG.Main_Form.Tree,open('test3344.cfg','w'))
    ## PICKLE CAN'T WORK WITH wx objects

    # close form(s)
    PG.Main_Form.Close()
    PG.Main_Form.Destroy()

    # close the inifile
    if PG.Programs_Inifile: PG.Programs_Inifile.Close ()

    # restore the original event loop
    wx.EventLoop.SetActive(old)

    print(PG.Program_Name, 'has Finished')
# End:class Pylab_Works_App

# ***********************************************************************
#                          MAIN PROGRAM
# ***********************************************************************
if __name__ == "__main__":
  try :
    #PG :import PyLab_Works_Globals as PG
    #Application : Application object <-- General_Globals.py

    # If a config file is specified,
    # we start in application mode
    ##if Application.Config_File :
    ##  PG.Standalone = True
    if not ( Application.Design_Mode ) :
      if not ( Application.Config_File ) :
        Application.Design_Mode = True

    #***********************************
    # Create the GUI application
    #***********************************
    PG.app = Pylab_Works_App( redirect = False )

    #***********************************
    # Create and Show the MainForm
    #***********************************
    PG.Main_Form = Pylab_Work_MainForm ( )

    #*********************************
    # set configure file of program
    #*********************************
    # define the programs configuration file
    Path_current = sys._getframe().f_code.co_filename
    filename_current, ext = os.path.splitext ( Path_current )

    #Read Pylab_Works.cfg
    #ini : object of .ini file, read from .cfg file
    ini = PG.Programs_Inifile = inifile ( filename_current + '.cfg' )
    ini.Section = 'General'
    filename_project_current = ini.Read ( 'Project File', '' )
    filename_project_current = filename_project_current.replace ( '\\', '/' ) #linux

    # frame Load Setting from configure file
    PG.Main_Form.Load_Settings ( ini )

    #********************************
    # Set active treenode from configure file
    #********************************
    print("[INFO] : Active treenode from configure file")
    ini.Section = 'General'
    Active_Tree_Item = PG.Programs_Inifile.Read ( 'Active Tree Item', None )
    tree_item = PG.Main_Form.Tree.Set_Selected_Item_From_String ( Active_Tree_Item )

    #****************************
    # Load the latest project
    #****************************
    if Application.Config_File :
      filename_project_current = Application.Config_File
      tree_item = None
    print("[INFO] : load project current")
    Load_Project ( filename_project_current, tree_item )

    # ***********************************************************************
    # Run the GUI application Forever
    # ***********************************************************************
    PG.app.MainLoop()
    # ***********************************************************************

  except :
    from PyLab_Works_Globals  import format_exception
    print(format_exception ( globals ))

# ***********************************************************************
#                          End Main Program
# ***********************************************************************

