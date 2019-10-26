import __init__

import wx
import os
import webbrowser

from  language_support import  _
from  help_support     import Launch_CHM
__doc__ = """
"""

_Version_Text = [

[ 1.3 , '12-05-2008', 'Stef Mientki',
'Test Conditions:', (2,),
"""
 - Help menu extended with chm-files and links from global config
"""],

[ 1.2 , '20-11-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - Create Menus bug solved
 - Create Menus now defined as a class, with more interfaces
""")],

[ 1.1 , '27-07-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - Some code restyling
 - Append_Item added
""")],

[ 1.0 , '14-07-2007', 'Stef Mientki',
'Test Conditions:', (),
_(0, ' - orginal release')]
]
# ***********************************************************************


from gui_support import *
from picture_support import *
from dialog_support  import AskFileForOpen
import copy
import PyLab_Works_Globals as PG

# ***********************************************************************
# ***********************************************************************
class My_Popup_Menu ( wx.Menu ) :

  default = {}

  # edit
  default[0] = [
      _(0,'Cut'), _(0,'Copy'), _(0,'Paste'), _(0,'Delete')]

  # extended edit
  default[1] = [
      '-', _(0,'Cut'), _(0,'Copy'), _(0,'Paste'), _(0,'Delete'), '-' ]

  # tree
  default[2] = [
      _(0,'Insert New\tIns'), _(0,'Edit\tSpace'),
      '-', _(0,'Cut\tCtrl-X'), _(0,'Copy\tCtrl-C'),
      _(0,'Paste\tCtrl-V'), _(0,'Delete\tDel') ]

  # *************************************************************
  # itemset = None,  doesn't use a default set
  # *************************************************************
  def __init__ ( self, OnSelect, itemset = 0, pre = None, post = None ):
    wx.Menu.__init__ ( self )

    # Determine the itemlist = pre + set + after
    items = []
    if pre :
      items = pre
    if isinstance ( itemset, int ) :
      items += self.default [ itemset ]
    if post :
      items += post

    # generate the menu
    self.IDs = []
    self.items = []
    for text in items :
      if text == '-' :
        item = self.AppendSeparator()
      else :
        item = self.Append ( wx.ID_ANY, text )

        # order of these bindings is important
        # to be sure we get it first
        self.Bind ( wx.EVT_MENU, OnSelect, item )
        self.Bind ( wx.EVT_MENU, self.OnSelect, item )

        # only save IDs of real items
        self.IDs.append ( item.GetId() )
        self.items.append ( item )

      #UBUNTU problems: item.SetCheckable ( True )


  # *************************************************************
  # *************************************************************
  def Append_Item ( self, item ) :
    self.AppendItem ( item )
    #UBUNTU problems: item.SetCheckable ( True )

  # *************************************************************
  # *************************************************************
  def Get_Index_by_ID ( self, ID_sel ) :
    for i, ID in enumerate ( self.IDs ) :
      if ID == ID_sel :
        break
    return i

  # *************************************************************
  # *************************************************************
  def Get_Item_by_ID ( self, ID_sel ) :
    i = self.Get_Index_by_ID ( ID_sel )
    return self.items [i]

  # *************************************************************
  # *************************************************************
  def OnSelect ( self, event ) :
    ID_sel = event.GetId ()
    for i, ID in enumerate ( self.IDs ) :
      if ID == ID_sel :
        break
    # return the index
    # event.Int is only used in very special cases (what?)
    # so it's valid to use it here to transport the index
    event.Int = i
    event.Skip ()

  # *************************************************************
  # *************************************************************
  def SetEnabled ( self, index, value = True ) :
    ID = self.IDs [ index ]
    value = bool ( value )
    self.Enable ( ID, value )

  # *************************************************************
  # *************************************************************
  def SetChecked ( self, index, value = True ) :
    item = self.items [ index ]
    if(item.IsCheckable()):
      item.SetCheckable ( True )
      if value :
        item.Check ( True )
      else :
        item.Check ( False )

# ***********************************************************************



default_menus = [
      ['&File',     [ ( '&New/Open\tCtrl+O', 'Open'),
                      ( '&Save\tCtrl+S',     'Save'),
                      ( 'Save &As ...',      'Save_As'),
                      ( '-' ),
                      ( '&Print\tCtrl+P',    'Print'),
                      ( 'Pr&int Preview',    'Print_Preview'),
                      ( 'Page Setup',        'Page_Setup'),
                      ( '-' ),
                      ( '&Export',           'Export'),
                      ( '-' ),
                      ( '&Close',            'Close') ]],
      ['&Edit',     [ ( '&ToDo',             'ToDo'),
                      ( '&Edit',             'Edit') ]],
      ['&Settings', [ ( '&ToDo',             'ToDo') ]],
      ['&View',     [ ( '&ToDo',             'ToDo'),
                      ( '&View',             'View') ]],
      ['&Help',     [ ( 'PyLab_&Works'           ,'PyLab_Works_Help' ),
                      ( 'Many Links'             ,'Flappie_Links'    ),
                      ( '-' ),
                      ( 'Send &Bug Report'       ,'Send_Bug_Report'  ),
                      ( '&Ask OnLine Assistance' ,'Ask_Assistance'   ),
                      ( 'Check For &New Version' ,'Check_New_Version'),
                      ( '&About'                 ,'About'            ) ]]]


# ***********************************************************************
# Dummy Menu Event Handler
# ***********************************************************************
class Menu_Event_Handler:
  def OnMenu_Flappie_Links ( self, event ) :
    webbrowser.open ( 'http://pic.flappie.nl' )

  def OnMenu_PyLab_Works_Help ( self, event ) :
    webbrowser.open ( 'http://pic.flappie.nl' )

  def OnMenu_Check_New_Version ( self, event ) :
    pass

  def OnMenu_About ( self, event ) :
    from wx.lib.wordwrap import wordwrap
    width = 450
    info = wx.adv.AboutDialogInfo()
    info.Name =  'PyLab Works'

    Path = sys._getframe().f_code.co_filename
    Path = os.path.split ( Path ) [0]
    info.SetIcon ( wx.Icon (
      Joined_Paths ( Path,
      '../pictures/ph_32.ico'), wx.BITMAP_TYPE_ICO ) )
    info.Version = PG.Version_Nr
    info.Copyright = "(C) 2007 .. 2008 Stef Mientki"
    info.Description = wordwrap(
      _(0, 'PyLab_Works is easy to use, highly modular,'
      'visual development enviroment,'
      'specially aimed at education and (scientific) research.' )
      , width, wx.ClientDC(self))
    info.WebSite = ("http://pic.flappie.nl/", "Home Page")

    info.Developers = [
      _(0, "Stef Mientki, special thanks to :\n"
      "\n"
      "the people who created Python\n"
      "python-list@python.org\n"
      "wxPython-users-list (especially Robin Dunn)\n"
      "and Erik Lechak for creating OGLlike.py" )
       ]
    licenseText = "for all I added: BSD\n" \
      "Python: Python Software Foundation License (PSFL)\n" \
      "MatPlotLib: Python Software Foundation License (PSFL)\n" \
      "wxPython: L-GPL\n" \
      "openGL: Free Software Foundation License B (BSD / Mozilla)"
    info.License = wordwrap(licenseText, width, wx.ClientDC(self))
    wx.adv.AboutBox ( info )


  def OnMenu_Ask_Assistance ( self, event ) :
    os.system('TeamViewer_Setup.exe')

  def OnMenu_Send_Bug_Report ( self, event ) :
    import win32api
    win32api.ShellExecute(0,'open','mailto: punthoofd@fastmail.fm', None,None,0)
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Class_Menus ( wx.MenuBar, Menu_Event_Handler ) :
  def __init__ ( self, My_Frame, My_Menus = default_menus ) :
    wx.MenuBar.__init__ ( self )
    self.My_Frame = My_Frame
    self.My_Menus = My_Menus
    self.Menu_Owners = {}
    self.My_Frame.Bind ( wx.EVT_MENU, self._Event_Distributor )

    Help_Menu = None
    Menu_Events = dir ( Menu_Event_Handler )
    for menu in My_Menus:
      menu_top = wx.Menu ()

      if menu [0] == '&Help' :
        Help_Menu = menu_top

      for item in menu [ 1 ] :
        if item[0] == '-' :
          menu_item = menu_top.AppendSeparator ()
        else :
          menu_item = menu_top.Append ( wx.ID_ANY, item[0] )

          ## MOET DIT NOG ??
          # assign the menu-ID to "My_Frame.ID_...."
          #   My_Frame.ID_Send_Bug_Report = menu_item.GetId()
          setattr ( self.My_Frame, 'ID_' + item[1], menu_item.GetId() )
          ## einde moet dit nog ??

          # First test if My_Frame has a method for this menu-item
          if hasattr ( self.My_Frame, 'OnMenu_'+item[1] ) :
            OnMenu_Function = getattr ( self.My_Frame, 'OnMenu_'+item[1] )
            # should work both :
            self.My_Frame.Bind ( wx.EVT_MENU, OnMenu_Function, id = menu_item.GetId() )
            #My_Frame.Bind ( wx.EVT_MENU, OnMenu_Function, menu_item )

          else : # Test if myself has a method for this menu-item
            Event = 'OnMenu_'+item[1]
            if Event in Menu_Events :
              self.My_Frame.Bind ( wx.EVT_MENU, eval ( 'self.' + Event ),
                                   id = menu_item.GetId() )
            else :
              menu_item.Enable ( False )

      self.Append ( menu_top, menu[0] )

    # Search CHM files, Add from globals config file
    self.Extra_Help_Items = {}
    if Help_Menu :
      #print 'PPPP3',Application.Application
      Help_Anchor = 2

      # find CHM help files in own program section
      CHM_Files = Find_Files ( '../chm_help', '*.chm', RootOnly = True )
      for file in CHM_Files :
        menu_item = Help_Menu.Insert ( Help_Anchor, wx.ID_ANY, file[1] )
        ID = menu_item.GetId()
        self.My_Frame.Bind ( wx.EVT_MENU, self.OnMenu_Extra_Help, id = ID )
        self.Extra_Help_Items [ ID ] =  \
          os.path.join ( '..', 'chm_help', file [1] + '.chm' ).replace('\\','/')
        Help_Anchor += 1

      # Get items from gloabls config file
      Ini = Application.General_Global_Settings
      Ini.Section = 'Help Paths'
      Sections = Ini.Get_Section ()
      for Section in Sections :
        menu_item = Help_Menu.Insert ( Help_Anchor, wx.ID_ANY, Section[0] )
        ID = menu_item.GetId()
        self.My_Frame.Bind ( wx.EVT_MENU, self.OnMenu_Extra_Help, id = ID )
        self.Extra_Help_Items [ ID ] = Section[1]
        Help_Anchor += 1

    #for item in self.Extra_Help_Items :
    #  v3print ( 'HELP:', item, self.Extra_Help_Items [item] )

    # apply the menubar
    self.My_Frame.SetMenuBar ( self )
    self.My_Frame.Bind ( wx.EVT_MENU_OPEN, self._On_Menu_Popup )
    #self.My_Frame.Bind ( wx.EVT_MENU, self.test1 )

  # *******************************************************
  def OnMenu_Extra_Help ( self, event ) :
    """
    Extra items in the Help-menu
    """
    ID = event.GetId ()
    if ID in self.Extra_Help_Items :
      v3print ( self.Extra_Help_Items [ ID ] )
    
      URL = self.Extra_Help_Items [ ID ].replace ( '\\', '/' )
      if '.chm' in URL :
        Launch_CHM ( URL )

      elif not ( os.path.isfile ( URL ) ) :
        webbrowser.open ( URL )

      else :
        webbrowser.open ( URL )

  # *******************************************************
  def _On_Menu_Popup (self, event ) :
    """
    Searches for the focussed control,
    Steps through all the items in the selected menu
    and Enables the menu-item, if the focussed control supports it
    Or if
    """
    #Control = self.FindFocus()
    # Sometimes event.GetMenu = None !!
    if event.GetMenu () :
      Control = self.My_Frame.FindFocus()
      MO = self.Menu_Owners
      for item in event.GetMenu().GetMenuItems() :
        ID = item.GetId()
        #if MO.has_key ( ID ) :
        if ID in MO :
          item.Enable ( ( Control in MO [ID] [0] ) or \
                        ( self.My_Frame in MO [ID] [0] ) )

  # ************************************************
  def _Event_Distributor ( self, event ) :
    ID = event.GetId ()
    MO = self.Menu_Owners
    if ID in MO :
      Control = self.My_Frame.FindFocus()
      # first test if the event is bound to the mainframe
      if self.My_Frame in MO [ID] [0] :
        i = MO [ID] [0].index ( self.My_Frame )
        MO [ID] [1][i] ( event )
      # if not, test if it's bound to the focussed control
      elif Control in MO [ID] [0] :
        i = MO [ID] [0].index ( Control )
        MO [ID] [1][i] ( event )
    event.Skip ()

  # ************************************************
  def Bind_MenuItem ( self, Menu, Item, Completion ) :
    """
    Bind the function Completion to Menu | Item event
    and enables this menu item.
    It's possible to add new Menus and Items
    """
    #print 'Bind_Menu',Menu,Item,Completion,Completion.im_self
    menu_ID = self.FindMenuItem ( Menu, Item )
    if menu_ID == wx.NOT_FOUND :
      # if menu doesn't exists, create it
      if self.FindMenu ( Menu ) == wx.NOT_FOUND :
        menu_top = wx.Menu ()
        self.Append ( menu_top, Menu )

      menu_ID = self.FindMenuItem ( Menu, Item )
      # if menuitem doesn't exists, create it
      if menu_ID == wx.NOT_FOUND :
        pos = self.FindMenu ( Menu )
        menu_top = self.GetMenu ( pos )
        menu_item = menu_top.Append ( wx.ID_ANY, Item )
        menu_ID = self.FindMenuItem ( Menu, Item )

    if menu_ID != wx.NOT_FOUND :
      menu_item = self.FindItemById ( menu_ID )
      menu_item.Enable ( True )
      #self.My_Frame.Bind ( wx.EVT_MENU, Completion, id = menu_ID )

      # add owner and completion to list
      #Owner = Completion.im_self
      Owner = Completion.__self__
      MO = self.Menu_Owners
      #if not ( MO.has_key ( menu_ID ) ) :
      if not ( menu_ID in MO ) :
        MO [ menu_ID ] = ( [], [] )
      MO = self.Menu_Owners [ menu_ID ]
      if not ( Owner in MO [0] ) :
        MO[0].append ( Owner )
        MO[1].append ( Completion )

      """
      print Completion,Completion.im_self.GetName()
      try :
        print Completion.im_self.Filename,Completion.im_self.GetName()
      except:
        pass
      """
# ***********************************************************************


# ***********************************************************************
# TODO: Toggling should be done on each group within separators
# TODO: different sizes 16/24/32
# TODO: more types than "Toggle"
# ***********************************************************************
class Create_ToolBar_Items ( object ) :
  def __init__ ( self, ToolBar, ToolItems, On_Event, parent, size = 24 ) :
    self.ToolBar    = ToolBar
    self.ToolItems  = ToolItems
    self.User_Event = On_Event
    self.IDs        = []

    tsize = ( size, size )
    self.IL = Get_Image_List ( size )
    ToolBar.SetToolBitmapSize ( tsize )


    # *******************************************************
    # determine the groups and their sizes
    # *******************************************************
    self.groups = []
    counter     = 0
    for item in ToolItems :
      if item :
        counter += 1
      else :
        self.groups.append ( counter )
        counter = 0
    if counter > 0 :
      self.groups.append ( counter )
    #print groups


    # *******************************************************
    # add the toolbar items, select the first one
    # and for groups of size 1, implement the togglebutton
    # *******************************************************
    group = 0
    First = True
    Accel_Table = []
    for item in ToolItems :
      if item :
        bmp = self.IL.GetBitmap ( item[0] )
        ID = wx.NewId()

        if self.groups [ group ] == 1 :
          ToolBar.AddCheckTool ( ID, item[1], bmp, shortHelp = item[1] )
        else :
          ToolBar.AddLabelTool      ( ID, item[1], bmp, shortHelp = item[1] )
          ToolBar.EnableTool ( ID, First )
          First = False
        self.IDs.append ( ID )
        ToolBar.GetParent().Bind ( wx.EVT_TOOL, self.My_On_Click, id = ID )
        
        # test if there's a accelerator key
        b = item[1].split ( '(' )
        if len ( b ) > 1 :
          b = b[1].split ( ')' ) [0]
          if b :
            #print 'ACCEL',b
            b = b.split ( '-' )

            # get all special flags
            Accelerator_Flags = {
               'Ctrl' : wx.ACCEL_CTRL,
               'Shift': wx.ACCEL_SHIFT,
               'Alt'  : wx.ACCEL_ALT }
            flags = wx.ACCEL_NORMAL
            while len(b) > 1 :
              flag = b.pop ( 0 )
              flags |= Accelerator_Flags [ flag ]
              
            # determine the key
            if ( b[0][0] == 'F' ) and ( len ( b[0] ) > 1 ) :
              key = eval ( 'wx.WXK_' + b[0] )
            else :
              key = ord ( b[0][0] )
            
            Accel_Table.append ( ( flags, key, ID ))
            #print 'ACCELERATION',flags, key, ID
            parent.Bind ( wx.EVT_TOOL, self.My_On_Click_Accelerator, id=ID )
            #parent.Bind ( wx.EVT_TOOL, On_Event, id=self.TB.IDs [ 1 ] )
      else :
        ToolBar.AddSeparator ()
        group += 1
        First = True

    # now realize the toolbar
    ToolBar.Realize()

    if Accel_Table :
      #ToolBar.SetAcceleratorTable ( wx.AcceleratorTable ( Accel_Table ) )
      #ToolBar.GetParent().SetAcceleratorTable ( wx.AcceleratorTable ( Accel_Table ) )
      parent.SetAcceleratorTable ( wx.AcceleratorTable ( Accel_Table ) )
    self.Accel_Table = Accel_Table
    
  # *******************************************************
  # *******************************************************
  def Enable_Buttons ( self, values ) :
    if not ( isinstance ( values, list ) ) :
      values = list ( values )
    self.Enabled_Tools = values
    TF = [ False, True ]
    for i in range ( len ( values ) ) :
      self.ToolBar.EnableTool ( self.IDs [i], TF [ values [i] ] )

  # *******************************************************
  # intercepts the key press, calculates the absolute index
  # disables the selected item and
  # enables all the other items in the group
  # calls the user completion routine
  # If the button is "pressed" through an accellerator key,
  # an extra flag is set
  #   (special meant for 2 buttons having the same accellerator key)
  # *******************************************************
  def My_On_Click_Accelerator ( self, event ) :
    event.Accelerator = True
    self.My_On_Click ( event )
    
  def My_On_Click ( self, event ) :
    self.Old_Enabled_Tools = copy.copy ( self.Enabled_Tools )

    event.My_Index = self.IDs.index ( event.GetId () )

    # determine the group
    group = 0
    total = self.groups [ group ]
    while total <= event.My_Index :
      group += 1
      total = total + self.groups [ group ]
    start = total - self.groups [ group ]
    
    # enable every group member except itself
    if self.groups [ group ] > 1 :
      for i in range ( self.groups [ group ] ) :
        self.ToolBar.EnableTool ( self.IDs [ start + i ], True )
        self.Enabled_Tools [ start + i ] = 1
        
      self.ToolBar.EnableTool ( event.GetId (), False )
      self.Enabled_Tools [ event.My_Index ] = 0

    #print start, self.groups [ group ], event.My_Index, group, total, self.groups
    self.User_Event ( event )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Simple_Test_Form ( My_Frame_Class ) :
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Simple GUI Demo', ini )

    # Add a dynamic menu to the menubar
    menu_dynamic_items = []
    for i in range ( 10 ) :
      menu_dynamic_items.append ( ( 'Demo ' + str(i) , 'Demo' + str(i) ) )
    default_menus.insert ( 1, ['Demos', menu_dynamic_items ] )

    GUI = """
    Panel_1        ,SplitterHor, 11
      Panel_2      ,wx.Panel
        label_2    ,wx.StaticText  ,label = "Signal1b", pos = (10, 50)
      Panel_3      ,PanelVer, 01
        tb         ,wx.ToolBar
        Panel_4    ,wx.Panel
          label_4  ,wx.StaticText  ,label = "Signal1b", pos = (10, 50)
    """
    #exec ( Create_wxGUI ( GUI ) )
    self.wxGUI = Create_wxGUI ( GUI ) #, IniName = 'self.Ini_File' )

    # Create the menu
    MenuBar = Class_Menus ( self )

    # *******************************************************
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
    self.TB = Create_ToolBar_Items  ( tb, ToolItems, self.On_ToolBar, self )
    Debug_Button_Init    = ( 1,  0,1,1,1,  0 )
    self.TB.Enable_Buttons ( Debug_Button_Init )
    # *******************************************************

    # Bind events, for the dymanic menu-items, through the whole range
    self.Bind ( wx.EVT_MENU, self.OnMenu_Demos, id=self.ID_Demo0, id2=self.ID_Demo9  )
    MenuBar.Bind_MenuItem ( 'File', 'Save', self._On_Menu_FileSave )

  # ******************************************************
  def OnMenu_numpy_Help ( self, event ) :
    pass

  # ******************************************************
  def OnMenu_Open ( self, event = None ) :
    DefaultLocation = ''
    FileName = AskFileForOpen ( DefaultLocation, FileTypes = '*.py' )
    if FileName :
      print (FileName)

  # ******************************************************
  def _On_Menu_FileSave ( self, event = None ):
    print ('lsdfsa')

  # ******************************************************
  # ******************************************************
  def On_ToolBar ( self, event ) :
    #tb = event.GetEventObject()

    _ID = event.GetId()
    ID  = event.My_Index
    State= self.TB.ToolBar.GetToolState ( _ID )

    #print 'TOOL', ID, State

    if ID == 0 :
      bmp = self.TB.IL.GetBitmap ( ( 83, 88 )[ State ] )
      self.TB.ToolBar.SetToolNormalBitmap ( _ID, bmp )

    else :
      pass
    #tb.EnableTool ( ID, not( tb.GetToolEnabled ( ID ) ) )

  # *******************************************************
  # *******************************************************
  # Action for dynamic events
  def OnMenu_Demos ( self, event ) :
    print (event.GetId() - self.ID_Demo0)
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
if __name__ == '__main__':
  My_Main_Application ( Simple_Test_Form )
# ***********************************************************************
pd_Module ( __file__ )


