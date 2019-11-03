# ***********************************************************************
import __init__
from language_support import _

# ***********************************************************************
__doc__ = """
TreeControl with drag and drop, RM-menu, etc
based on CT.CustomTreeCtrl

License: freeware, under the terms of the BSD-license
Copyright (C) 2008 Stef Mientki
mailto:S.Mientki@ru.nl
"""

# ***********************************************************************
_Version_Text = [
[ 1.6, '13-10-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
 - CollapseAll added
""" ) ],

[ 1.5, '10-10-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
 - Autoread of JALcc trees added
""" ) ],

[ 1.4, '29-07-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
   - Lines_2_Tree     added
   - Add_PyFile_Info  added
""" ) ],

[ 1.3, '05-06-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
   - ',' not longer supported as splitter character
""" ) ],

[ 1.2, '27-05-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
   - Get_Item_Level_MainParent bug if no root or root changed
""" ) ],

[ 1.1, '24-05-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
   - uses '~' instead of ',' as the splitter character
   - uses LAST '=' as name-value splitter
   - old files are still read correctly
   - edit spaces in treenode possible
   - fileextension can be specified (default = '.tree' )
""" ) ],

[ 1.0, '10-03-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
    - orginal release
""" ) ]
]
# ***********************************************************************

import os
import sys

import wx

"""
subdirs = [ '../Lib_Extensions' ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
"""

import customtreectrl_SM as CT


from   inifile_support import inifile
#from   picture_support import Get_Image_List_16
from   file_support    import *
from   menu_support    import *
from   dialog_support  import *
from   doc_support     import *


# ***********************************************************************
# CustomTreeCtrl Demo Implementation
# !!!!!!!! CHANGES to CustomTreeCtrl: !!!!!!!!!!!!
# line 949 removed  "|wx.TE_MULTILINE"
# line 1042 ...

# PyData [0] = X X X X   X X X X
#                            | +--- True = Node Checked (not used at this moment)
#                            +----- True = Node Expanded
# PyData [1] = Normal Node Icon
# PyData [2] = Expanded Node Icon
"""
 |  HitTest(self, point, flags=0)
 |      Calculates which (if any) item is under the given point, returning the tree item
 |      at this point plus extra information flags. Flags is a bitlist of the following:
 |
 |      TREE_HITTEST_ABOVE            above the client area
 |      TREE_HITTEST_BELOW            below the client area
 |      TREE_HITTEST_NOWHERE          no item has been hit
 |      TREE_HITTEST_ONITEMBUTTON     on the button associated to an item
 |      TREE_HITTEST_ONITEMICON       on the icon associated to an item
 |      TREE_HITTEST_ONITEMCHECKICON  on the check/radio icon, if present
 |      TREE_HITTEST_ONITEMINDENT     on the indent associated to an item
 |      TREE_HITTEST_ONITEMLABEL      on the label (string) associated to an item
 |      TREE_HITTEST_ONITEMRIGHT      on the right of the label associated to an item
 |      TREE_HITTEST_TOLEFT           on the left of the client area
 |      TREE_HITTEST_TORIGHT          on the right of the client area
 |      TREE_HITTEST_ONITEMUPPERPART  on the upper part (first half) of the item
 |      TREE_HITTEST_ONITEMLOWERPART  on the lower part (second half) of the item
 |      TREE_HITTEST_ONITEM           anywhere on the item
 |
 |      Note: both the item (if any, None otherwise) and the flag are always returned as a tuple.
 |
"""
# ***********************************************************************

class Custom_TreeCtrl_Base ( CT.CustomTreeCtrl_Modified_SM ) :

  # *************************************************************
  # Creation of the treecontrol
  # *************************************************************
  def __init__( self, parent, root_title = _(0,'No Root Title' ),
                name          = 'CT-Tree',
                No_Image_List = False,
                style_add     = None,
                style_sub     = None ) :

    self.parent = parent

    # *************************************************************
    # tree style to be used
    # *************************************************************
    tree_style = \
                  CT.TR_HAS_BUTTONS \
                 | CT.TR_FULL_ROW_HIGHLIGHT \
                 | CT.TR_HIDE_ROOT \
                 | CT.TR_LINES_AT_ROOT \
                 | CT.TR_SINGLE \
                 | CT.TR_EDIT_LABELS \
                 | wx.WANTS_CHARS \
                 | CT.TR_HAS_VARIABLE_ROW_HEIGHT \
                 | wx.NO_BORDER \
                 #| wx.SUNKEN_BORDER \
    if style_add :
      tree_style |= style_add
    if style_sub :
      tree_style ^= style_sub

    # *************************************************************
    # create the tree and assign imagelist
    # *************************************************************
    CT.CustomTreeCtrl_Modified_SM.__init__ ( self, parent, style = tree_style,
                                 name = name )
    self.No_Image_List = No_Image_List


    self.root = self.AddRoot ( root_title )
    if not ( self.No_Image_List ) :
      self.imagelist = Get_Image_List ()
      self.SetImageList ( self.imagelist )
    self.Item_Copy = False
    self.Move_Action = False

    #self.DeleteAllItems()
    #self.root

    # we also give the root images, so we can use it as copy source
    PyData = []
    PyData.append ( 0 )
    PyData.append ( 78 )
    PyData.append ( 79 )
    self.SetPyData ( self.root, PyData )


    # *************************************************************
    # popup menus
    # *************************************************************
    PU = My_Popup_Menu ( self.OnPopupItemSelected, 2 )
    self.Popup_Menu_Tree = PU

    #self.Bind ( wx.EVT_CONTEXT_MENU, self.OnShowPopup )
    #In Ubuntu context menu doesn't appear
    #self.Bind ( wx.EVT_RIGHT_DOWN, self.OnShowPopup )
    #self.Bind ( wx.EVT_RIGHT_UP, self.OnShowPopup )
    self.Bind ( wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnShowPopup )
    
    """
    default[2] = [
      'Insert New\tIns', 'Edit',
      '-', 'Cut\tCtrl-X', 'Copy\tCtrl-C', 'Paste\tCtrl-V', 'Delete\tDel' ]
    """
    self.Popup_Menu_Tree.SetEnabled ( 4, self.Item_Copy )

    # Create Bindings for the menu events
    self.Bind ( wx.EVT_MENU, self.On_Insert, PU.items [0] ) # Ins
    self.Bind ( wx.EVT_MENU, self.On_Edit,   PU.items [1] ) # Ins
    self.Bind ( wx.EVT_MENU, self.On_Cut,    PU.items [2] ) # ^X
    self.Bind ( wx.EVT_MENU, self.On_Copy,   PU.items [3] ) # ^C
    self.Bind ( wx.EVT_MENU, self.On_Paste,  PU.items [4] ) # ^V
    self.Bind ( wx.EVT_MENU, self.On_Delete, PU.items [5] ) # Del

    # Create bindings for accelerator keys
    aTable = wx.AcceleratorTable ( [ \
        ( wx.ACCEL_NORMAL, wx.WXK_INSERT, PU.IDs[0] ),
        #( wx.ACCEL_NORMAL, wx.WXK_SPACE,  PU.IDs[1] ),
        ( wx.ACCEL_CTRL,   ord('X'),      PU.IDs[2] ),
        ( wx.ACCEL_CTRL,   ord('C'),      PU.IDs[3] ),
        ( wx.ACCEL_CTRL,   ord('V'),      PU.IDs[4] ),
        #( wx.ACCEL_NORMAL, wx.WXK_DELETE, PU.IDs[5] ),
        ])
    self.SetAcceleratorTable ( aTable )

    # *************************************************************
    # Event Bindings
    # *************************************************************
    self.Bind ( wx.EVT_NAVIGATION_KEY,        self.OnTreeNavigate )

    self.Bind ( wx.EVT_KEY_DOWN, self.OnMyKeyDown)

    self.Bind ( CT.EVT_TREE_BEGIN_DRAG,       self.OnBeginDrag )
    self.Bind ( CT.EVT_TREE_END_DRAG,         self.OnEndDrag )

    self.Bind ( wx.EVT_LEFT_DOWN,             self.OnClick )

    
    # *************************************************************
    # Event Bindings, Not Used in this library
    # *************************************************************
    """
    self.Bind ( CT.EVT_TREE_ITEM_GETTOOLTIP,  self.OnToolTip )

    self.Bind ( wx.EVT_KEY_DOWN,              self.OnKeyDown )
    self.Bind ( CT.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginEdit )

    self.Bind ( wx.EVT_MIDDLE_DOWN,           self.OnMiddleDown )
    self.Bind ( wx.EVT_RIGHT_DOWN,            self.OnRightDown )

    self.Bind ( CT.EVT_TREE_SEL_CHANGED,      self.OnChanged )
    self.Bind ( CT.EVT_TREE_SEL_CHANGING,     self.OnChanging )
    self.Bind ( CT.EVT_TREE_ITEM_ACTIVATED,   self.OnActivated )
    self.Bind ( CT.EVT_TREE_STATE_IMAGE_CLICK,self.OnActivated )
    """

    self.Bind ( CT.EVT_TREE_SEL_CHANGED,      self.On_Sel_Changed    )

  # *************************************************************
  # *************************************************************
  def On_Sel_Changed ( self, event ) :
    #print self.GetItemText ( event.GetItem())
    event.Skip()

  # *************************************************************
  # *************************************************************
  def OnMyKeyDown ( self, event ) :
    if not ( self.GetEditControl () ) :
      if event.GetKeyCode() == wx.WXK_DELETE :
        self.Delete_Item ( self.GetSelection () )
      # goto or stay in edit mode
      elif event.GetKeyCode() == wx.WXK_SPACE :
        self.Edit ( self.GetSelection () )
      else :
        event.Skip()
    else :
      event.Skip()

  # *************************************************************
  # *************************************************************
  def On_Delete ( self, event ) :
    if not ( self.GetEditControl () ) :
      self.Delete_Item ( self.GetSelection () )
    else :
      event.Skip()

  # *************************************************************
  # *************************************************************
  def On_Icon_Click ( self, item ) :
    pass

  # *************************************************************
  # *************************************************************
  def OnClick ( self, event ) :
    item, hit = self.HitTest ( event.GetPosition () )
    #print 'Click',item,hit
    if hit and \
       (( hit & CT.TREE_HITTEST_ONITEMICON ) != 0 ) :
      self.On_Icon_Click ( item )
    event.Skip()

  # *************************************************************
  # determines the level of a treenode,
  # and the text of the main parent
  # root: level = 0
  # *************************************************************
  def Get_Item_Level_MainParent ( self, item ) :
    level = 0
    MainParent = ''
    self.root = self.GetRootItem ()
    while item and  ( item != self.root ) :
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

  # *************************************************************
  # *************************************************************
  def CollapseAll ( self ) :
    Root = self.GetRootItem ()
    if self.HasChildren ( Root ):
      item, cookie = self.GetFirstChild ( Root )
      while item :
        item.Collapse ()
        item = self.GetNextSibling ( item )
      self.Refresh ()

  # *************************************************************
  # *************************************************************
  def On_Insert ( self, event ) :
    sel = self.GetSelection ()
    self.Insert_New ( sel )

  # *************************************************************
  # *************************************************************
  def On_Edit ( self, event ) :
    sel = self.GetSelection ()
    self.Edit ( sel )

  # *************************************************************
  # *************************************************************
  def Copy_PyData ( self, Source, Dest ) :
    # now add PyData and icons (deepcopy gives problems)
    PyData = []
    data = self.GetPyData ( Source )
    if data :
      for i in data :
        PyData.append ( i )
    if len (PyData) < 1 : PyData.append ( 0 )
    if len (PyData) < 2 : PyData.append ( 23 )
    if len (PyData) < 3 : PyData.append ( 14 )
    self.SetPyData    ( Dest, PyData )
    self.SetItemImage ( Dest, int(PyData[1]), CT.TreeItemIcon_Normal )
    self.SetItemImage ( Dest, int(PyData[2]), CT.TreeItemIcon_Expanded )

  # *************************************************************
  # *************************************************************
  def Insert_New ( self, sel, hit = None ) :
    # if OnIcon, add as a child
    if hit and \
       (( hit & CT.TREE_HITTEST_ONITEMICON ) != 0 ) :
          NewItem = self.AppendItem ( sel, _(0,'new' ))
          self.Expand ( NewItem )
    else :
      # if no node is selected, just add to the root
      if not ( sel ) :
        sel = self.root
        NewItem = self.AppendItem ( sel, _(0,'new' ))
      else:
        prev = self.GetPrevSibling ( sel )
        if not ( prev ) :
          itemParent = self.GetItemParent ( sel )
          NewItem = self.PrependItem ( itemParent, _(0,'new') )
        else :
          itemParent = self.GetItemParent ( prev )
          NewItem = self.InsertItem ( itemParent, prev, _(0,'new') )
        """
        NewItem = self.InsertItemBefore ( itemParent, sel, _(0,'new') )
        """
    self.Copy_PyData ( sel, NewItem )
    self.SelectItem ( NewItem, True )
    self.Edit ( NewItem )


  # *************************************************************
  # *************************************************************
  def On_Cut ( self, event ) :
    self.Move_Action = True
    self.Item_Copy = self.GetSelection ()

  # *************************************************************
  # *************************************************************
  def On_Copy ( self, event ) :
    self.Move_Action = False
    self.Item_Copy = self.GetSelection ()

  # *************************************************************
  # *************************************************************
  def On_Paste ( self, event ) :
    if self.Item_Copy :
      self.Enumerate_Copy ( self.Item_Copy, self.GetSelection (), False )
      self.Item_Copy = False

  # *************************************************************
  # *************************************************************
  def Delete_Item ( self, item ) :
    line = _(0,'Delete "' + self.GetItemText ( item ) + \
               '" and all its Children\n' \
               'Are you sure ?')
    if AskYesNo (line) :
      # after deleting we want to got the element above it
      prev = self.GetPrevVisible ( item )
      self.Delete ( item )
      self.SelectItem ( prev, True )

  # *************************************************************
  # Stop editing when moved away form this node
  # *************************************************************
  def OnTreeNavigate ( self, event ) :
    if self.GetEditControl():
      self.GetEditControl().AcceptChanges()
      self.GetEditControl().StopEditing()

  # *************************************************************
  # *************************************************************
  def OnShowPopup ( self, event ) :
    print ('RRRRRRRRRRR',event.GetPoint())
    self.Tree_Hit_Pos = event.GetPoint ()
    self.Popup_Menu_Tree.SetEnabled ( 4 , self.Item_Copy )
    self.PopupMenu ( self.Popup_Menu_Tree )

  # *************************************************************
  # *************************************************************
  def OnPopupItemSelected ( self, event ) :
    item, hit = self.HitTest(self.Tree_Hit_Pos)
    #item = self.Right_Clicked_Item
    #hit = None

    i = event.Int
    if   i == 0 : # Insert New
      self.Insert_New ( item, hit )

    elif i == 1 : # Edit
      self.Edit ( item )

    elif i == 2 : # Cut
      self.Move_Action = True
      self.Item_Copy = item

    elif i == 3 : # Copy
      self.Move_Action = False
      self.Item_Copy = item

    elif i == 4 : # Paste
      self.Copy_Item ( item, hit )

    elif i == 5 : # Delete
      self.Delete_Item ( item )

  # *************************************************************
  # *************************************************************
  def OnBeginDrag ( self, event ) :
    self.Item_Copy = event.GetItem ()
    if self.Item_Copy:
      event.Allow()
      # allow the parent to Veto the drag
      # BUT: the parent must implement and Bind an (empty) method
      # otherwise the drag won't start
      event.Skip ()

  # *************************************************************
  # *************************************************************
  def OnEndDrag(self, event):
    x, y = event.GetPoint()
    item, hit = self.HitTest ( wx.Point ( x, y ) )
    self.Move_Action = True
    if item :
      self.Copy_Item ( item, hit )

  # *************************************************************
  # RECURSION !!
  # *************************************************************
  def Enumerate_Copy ( self, source, dest, AsChild = True ) :
    if AsChild : # insert as child of the destination
      NewItem = self.AppendItem ( dest,
                  self.GetItemText ( source )  )
      # be sure the parent will be expanded
      self.Expand ( dest )

    else : #insert before drop target
      itemParent = self.GetItemParent ( dest )
      prev = self.GetPrevSibling ( dest )
      if not ( prev ) :
        NewItem = self.PrependItem (
                  itemParent,
                  self.GetItemText ( source ) )
      else :
        NewItem = self.InsertItem (
                  itemParent, prev,
                  self.GetItemText ( source ) )

    self.Copy_PyData ( source, NewItem )

    if self.HasChildren ( source ):
      item, cookie = self.GetFirstChild ( source )
      while item :
        self.Enumerate_Copy ( item, NewItem, True )
        item = self.GetNextSibling ( item )

  # *************************************************************
  # RECURSION !!
  # *************************************************************
  def Dropped_On_Myself ( self, source, dest ) :
    if dest == source :
      return True
    if self.HasChildren ( source ):
      item, cookie = self.GetFirstChild ( source )
      while item :
        if self.Dropped_On_Myself ( item, dest ) :
          return True
        item = self.GetNextSibling ( item )
    return False

  # *************************************************************
  # *************************************************************
  def Copy_Item ( self, item, hit ):
    # test if not copied / moved to itself or one of it's children
    if self.Dropped_On_Myself ( self.Item_Copy, item ) :
      self.Move_Action = False
      return

    OnIcon = ( hit & CT.TREE_HITTEST_ONITEMICON ) != 0
    self.Enumerate_Copy ( self.Item_Copy, item, OnIcon )
    if self.Move_Action :
      self.Delete ( self.Item_Copy )
      self.Move_Action = False
    self.Item_Copy = None

  # *****************************************************************
  # Transports all parameters from the TREE to the INIFILE.
  # Recursion !! Only used by Tree_2_IniFile.
  # *****************************************************************
  def _Enum_Tree_2_IniFile ( self, treefile, start, line='' ):
    item, cookie = self.GetFirstChild ( start )
    while item :
      state = self.IsItemChecked ( item ) + 2*self.IsExpanded ( item )
      data = self.GetPyData ( item )
      if data :
        if len ( data ) < 1 :
          data.append ( state )
        else :
          data [0] = state
      else :
        data =[]
        data.append ( state )
      dataline =  ''
      for elem in data :
        #dataline += str(elem) + ','
        dataline += str(elem) + '~'
      if len( dataline ) > 0 : dataline = dataline [:-1]
      treefile.write ( line + self.GetItemText ( item ) + '=' + dataline+'\n' )

      if self.HasChildren ( item ) :
        self._Enum_Tree_2_IniFile (
          treefile, item, line + self.GetItemText ( item ) + '~' )
        #  treefile, item, line + self.GetItemText ( item ) + ',' )
      item = self.GetNextSibling ( item )

  # *****************************************************************
  # Transports all parameters from the TREE to the INIFILE.
  # *****************************************************************
  def Tree_2_IniFile ( self, ini_filename, ext = 'tree' ) :
    # inifile doesn't accept double key-values,
    # therefor we use normal text file
    fne, fe = os.path.splitext ( ini_filename )
    treefile = open ( fne + '.' + ext, 'w')

    MainNode = self.root
    MainNode, cookie = self.GetFirstChild ( MainNode )
    while MainNode :
      # Store the expansion of the mainnode
      state = self.IsItemChecked ( MainNode ) + 2*self.IsExpanded ( MainNode )
      treefile.write ( '[' + self.GetItemText ( MainNode ) + '=' +  str ( state ) + '\n' )
      self._Enum_Tree_2_IniFile ( treefile, MainNode )
      MainNode = self.GetNextSibling ( MainNode )
    treefile.close()

  # *****************************************************************
  #
  # *****************************************************************
  def Add_PyFile_Info ( self, underscore = None ) :
    MainNode = self.root
    MainNode, cookie = self.GetFirstChild ( MainNode )
    while MainNode :
      #MainName = self.GetItemText ( MainNode )
      FileNode, cookie = self.GetFirstChild ( MainNode )
      while FileNode :
        # Get classes and functions
        filename = self.GetItemText ( FileNode )
        FL,CL = Get_Classes_And_Functions_Split ( filename, underscore )
        for F in FL :
          newnode = self.AppendItem ( FileNode, F )
          self.SetItemImage ( newnode, 33, CT.TreeItemIcon_Normal )
        for F in CL :
          newnode = self.AppendItem ( FileNode, F )
          self.SetItemImage ( newnode, 34, CT.TreeItemIcon_Normal )

          # For Classes get the methods
          #print '^^^^',filename,F
          CFL = Get_Class_Methods ( filename, F )
          for CF in CFL :
            CFnode = self.AppendItem ( newnode, CF )
            self.SetItemImage ( CFnode, 22, CT.TreeItemIcon_Normal )

        FileNode = self.GetNextSibling ( FileNode)
      MainNode = self.GetNextSibling ( MainNode )

  # *****************************************************************
  # *****************************************************************
  def IniFile_2_Tree ( self, ini_filename, ext = 'tree' ) :
    fne, fe = os.path.splitext ( ini_filename )
    filename = fne + '.'+ ext
    if File_Exists ( filename ) :
      # *****************************************************************
      # parse the inifile to create the tree
      # ****************************************************************
      treefile = open ( filename, 'r')
      lines = treefile.readlines ()
      treefile.close ()
      #print 'TREELINES',lines
      self.Lines_2_Tree ( lines )

  # *****************************************************************
  # *****************************************************************
  def Lines_2_Tree ( self, lines ) :
    Expand = []
    N = 0
    for r in lines :
     if r:
      #print ' lOPII',r
      r = r.rstrip ("\n\r")    # remove CR, LF
      # split at the last "="
      if r.find ('=') > 0 :
        #key, val = r.split('=')
        key, val = r.rsplit ( '=', 1 )
      else :
        key = r
        val = ''
      # newer version uses '~'  instead of ','
      #if ( val.find ('~') >= 0 ) or ( key.find ('~') >=0 ):
      key = key.split ( '~' )
      val = val.split ( '~' )
      #else :
      #  key = key.split ( ',' )
      #  val = val.split ( ',' )
      if len ( val ) < 2 : val.append ( -1 )
      if len ( val ) < 3 : val.append ( -1 )

      if key[0][0] == '[':
        node_name = key[0][1:]
        MainNode = self.AppendItem ( self.root, node_name )
        val[1] = 15
        val[2] = 16
        self.SetPyData ( MainNode, val )
        self.SetItemImage ( MainNode, int( val[1] ), CT.TreeItemIcon_Normal )
        self.SetItemImage ( MainNode, int( val[2] ), CT.TreeItemIcon_Expanded )

        # set the expansion Mainnode that just has finished
        if len(Expand) > 0 :
          nod, exp = Expand[0]
          if exp: self.Expand ( nod )
        Expand = []
        print (val)
        Expand.append ( (MainNode, bool ( int(val[0]) & 2 )) )
        N = 0
        node = NODE = MainNode
      else :
        # keep track of nesting
        if len( key ) == N :
          nod, exp = Expand.pop()
          if exp: self.Expand ( nod )
        elif len( key ) > N :
          NODE = node
          N += 1
        elif len( key ) < N :
          for i in range ( N - len(key) + 1 ):
            nod, exp = Expand.pop()
            if exp: self.Expand (nod)
          for i in range ( N - len(key)):
            NODE = NODE.GetParent()
          N = len ( key )

        node = self.AppendItem ( NODE, key [-1] )
        self.SetPyData ( node, val )
        self.SetItemImage ( node, int( val[1] ), CT.TreeItemIcon_Normal )
        self.SetItemImage ( node, int( val[2] ), CT.TreeItemIcon_Expanded )
        Expand.append ( ( node, bool(int(val[0]) & 2) ))

      # set the expansion last Mainnode that just has finished
      # SMALL BUG: if the last element a node with children,
      # it will never be expanded ???
      if len(Expand) > 0 :
        nod, exp = Expand[0]
        if exp: self.Expand ( nod )
          
  # *****************************************************************
  # *****************************************************************
  def Set_PuntHoofd_Tree ( self, html_tree ) :
    # read a PuntHoofd Tree
    from web_support import Read_PuntHoofd_Tree
    tree_items = Read_PuntHoofd_Tree ( html_tree )

    # Create a root element (real root is not shown
    self.DeleteAllItems()
    self.root = self.AddRoot ( 'Root will not be shown' )
    #Root = Tree.AppendItem ( Tree.root, tree_items[0][1] [ 8 : -5 ] )
    Root = self.root


    #Colors = ( wx.RED, wx.BLUE, "#00FFFF", wx.RED, wx.BLUE, "#00FFFF",wx.RED, wx.BLUE, "#00FFFF",  "#00FFFF",wx.RED, wx.BLUE, "#00FFFF")
    Colors = ( (9,193,9), (0,0,255), (232,145,52), (2,6,166), (255,0,0),
               wx.BLACK, (173,140,107), (9,193,9), (197,199,3), (255,0,0),
               (232,102,238), (160,160,160), (48,179,240), (0,0,255), (48,239,48),
               (15,183,122), wx.BLACK, wx.BLACK, wx.BLACK )
    Color_Index = -1
    #Icons = ( 202, 239, 108, 145, 147, 102, 201, 163, 99, 136, 141, 1, 1, 1 )
    #Icons = ( 202, 239, 121, 145, 147, 102, 201, 163, 163, 99, 136, 141, 1, 1, 1 )
    Icons = ( 538, 239, 121, 145, 147,
              402, 201, 65, 163, 523,
              99, 136, 131, 500, 1,
              1, 1 )

    # Create the Tree elements
    for item in tree_items [ 1: ] :
      #v3print ( 'TTTREITEM', item )
      text =  item [1] [8].upper() + item [1] [ 9 : -5 ]
      if item[0] == 1 :
        Color_Index += 1
        Color_Index %= len ( Colors )
        Lib_Color = Colors [ Color_Index ]
        Icon      = Icons  [ Color_Index ]
        Parent = self.AppendItem ( Root, text )
        self.SetItemBold       ( Parent )
        self.SetItemTextColour ( Parent, Lib_Color )
        self.SetItemImage      ( Parent, Icon ) #15 )
      else :
        Node = self.AppendItem ( Parent, text )
        #self.SetItemTextColour ( Node, Lib_Color )
        self.SetItemImage      ( Node, Icon )

    # expand the main tree
    #Tree.Expand ( Root )

# ***********************************************************************
# ***********************************************************************
# A simple form to test the control
# ***********************************************************************

class Simple_Test_Form ( wx.MiniFrame ):
  def __init__ ( self, ini = None ):
    # restore position and size
    self.ini = ini
    if ini :
      ini.Section = 'Test'
      pos  = ini.Read ( 'Pos'  , ( 50, 50 ) )
      size = ini.Read ( 'Size' , ( 500, 300 ) )

    wx.MiniFrame.__init__(
      self, None, -1, 'Test PyLab Works GUI Control',
      size  = size,
      pos   = pos,
      style = wx.DEFAULT_FRAME_STYLE )

    # *****************************************************************
    Splitter = wx.SplitterWindow ( self )

    # Create the control to be tested and read old settings
    self.Tree = Custom_TreeCtrl_Base ( Splitter )
    self.Tree.On_Icon_Click = self.On_Icon_Click
    if ini: self.Tree.IniFile_2_Tree ( ini.filename )

    self.Editor = wx.TextCtrl ( Splitter, -1,
      "Here iscontrol.\n\n"
      "The quied over the lazy dog...",
      size=(200, 100),
      style = wx.TE_MULTILINE | wx.TE_PROCESS_ENTER | wx.NO_BORDER)
    Splitter.SplitVertically ( self.Tree, self.Editor )
    # *****************************************************************

    self.     Bind ( wx.EVT_CLOSE,           self.OnCloseWindow )
    self.     Bind ( CT.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag   )
    self.Tree.Bind ( CT.EVT_TREE_END_DRAG,   self.OnEndDrag     )
    Splitter.Bind  ( wx.EVT_SPLITTER_DCLICK, self._Block_This )

    self.Tree.Bind ( wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnShowPopup )

  # *************************************************************
  # *************************************************************
  def OnShowPopup ( self, event ) :
    #print 'GGGGGGGGRRRRRRRRRRR',event.GetPoint(), self.Tree.GetItemText(event.GetItem())
    self.Tree_Hit_Pos = event.GetPoint ()
    #self.Popup_Menu_Tree.SetEnabled ( 4 , self.Item_Copy )
    #self.PopupMenu ( self.Popup_Menu_Tree )

  # *************************************************************
  # *************************************************************
  def OnPopupItemSelected ( self, event ) :
    item, hit = self.Tree.HitTest(self.Tree_Hit_Pos)


  # *************************************************************
  # *************************************************************
  def _Block_This ( self, event ) :
    event.Veto ()

  # *************************************************************
  # Change the icon if clicked on it
  # *************************************************************
  def On_Icon_Click ( self, item ) :
    #print ' JOEPIE...', self.Tree.GetItemImage(item)
    if self.Tree.GetItemImage ( item ) == 80 :
      Icon = 83
    else :
      Icon = 80
    self.Tree.SetItemImage ( item, Icon, CT.TreeItemIcon_Normal )
    self.Tree.SetItemImage ( item, Icon, CT.TreeItemIcon_Expanded )

  # *****************************************************************
  # You can block the start of a drag event
  # *****************************************************************
  def OnBeginDrag ( self, event ) :
    #event.Veto()
    pass

  # *****************************************************************
  # You can block the end of a drag event
  # NOTE: the binding must be "self.Tree.Bind"
  # *****************************************************************
  def OnEndDrag ( self, event ) :
    event.Skip()

  def OnCloseWindow ( self, event ) :
    self.Tree.Tree_2_IniFile ( self.ini.filename )
    event.Skip ()

# ***********************************************************************

# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':

  Test_Defs ( 2 )

  if Test ( 1 ) :
    app = wx.App ()
    ini = inifile ( 'test_My_Custom_TreeCtrl.cfg' )
    frame = Simple_Test_Form (ini = ini)
    frame.Show ( True )
    app.MainLoop ()
    ini.Close ()
  
  if Test ( 2 ) :
    app = wx.App ()
    ini = inifile ( 'test_My_Custom_TreeCtrl.cfg' )
    frame = Simple_Test_Form (ini = ini)

    html_tree = '../PyLab_Works/html/pw_demos_tree_index.html'
    frame.Tree.Set_PuntHoofd_Tree ( html_tree )

    frame.Show ( True )
    app.MainLoop ()
    ini.Close ()

# ***********************************************************************
pd_Module ( __file__ )
