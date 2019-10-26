import __init__
from base_control import *

from   PyLab_Works_Globals import _
import PyLab_Works_Globals as PG
import wx
import sys
from   tree_support import *
from   copy         import copy

DB_TREE_UNCHECKED    = 80  # open square
DB_TREE_TABLE_SELECT = 83  # red
DB_TREE_CHECKED      = 85  # blue
DB_TREE_SORT_ASC     = 89  # purple
DB_TREE_SORT_DESC    = 88  # green


# ***********************************************************************
# ***********************************************************************
class t_C_DB_Tree ( My_Control_Class ):

  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    # Add a few extra Parameter
                         # P[0] = SQL statement  from selection
    self._EP_Add (False) # P[1] = table metadata from selection

    self.Old_Table_Info = None
    self.Old_SQL        = ''

    import customtreectrl_SM as CT
    GUI = """
      self.Tree  ,Custom_TreeCtrl_Base, style_sub = CT.TR_EDIT_LABELS
    """
    self.wxGUI = Create_wxGUI ( GUI, my_parent = 'self.Dock' )

    # *************************************************************
    # event bindings
    # *************************************************************
    #self.Tree.Bind ( CT.EVT_TREE_SEL_CHANGED,      self.OnSelectionChanged )
    self.Tree.Bind ( CT.EVT_TREE_ITEM_ACTIVATED,   self.OnActivated )
    #self.Tree.OnSelectionChanged = self.OnSelectionChanged
    #self.Tree.OnChanged = self.OnSelectionChanged
    self.Tree.On_Icon_Click = self.On_Icon_Click

    # Override popup event, to do nothing
    self.Tree.Bind ( wx.EVT_TREE_ITEM_RIGHT_CLICK, self._No_Action )

  # *************************************************************
  # *************************************************************
  def _No_Action ( self, event ) :
    pass
  
  # *************************************************************
  # *************************************************************
  def Set_Active_Table ( self, sel_item, Activated = False ) :
    level,main_parent = self.Tree.Get_Item_Level_MainParent ( sel_item )

    if (level == 3) :
      current = self.Tree.GetItemImage ( sel_item )
      if current == DB_TREE_UNCHECKED :
        Icon = DB_TREE_CHECKED
      else :
        Icon = DB_TREE_UNCHECKED
        
      if Activated :
        if current == DB_TREE_SORT_ASC :
          Icon = DB_TREE_SORT_DESC
        else :
          Icon = DB_TREE_SORT_ASC
        # clear all to non sorted
        Node, cookie = self.Tree.GetFirstChild ( sel_item.GetParent () )
        while Node :
          if ( self.Tree.GetItemImage ( Node ) == DB_TREE_SORT_ASC ) or \
             ( self.Tree.GetItemImage ( Node ) == DB_TREE_SORT_DESC ) :
            self.Tree.SetItemImage ( Node, DB_TREE_CHECKED, CT.TreeItemIcon_Normal )
          Node = self.Tree.GetNextSibling ( Node )

      # set the selected
      self.Tree.SetItemImage ( sel_item, Icon, CT.TreeItemIcon_Normal )

    table = self.Tree.Get_Parent_At_Level ( sel_item, 2 )
    table_name = self.Tree.GetItemText ( table )
    if ' ' in table_name :
      table_name  = '"' + table_name + '"'

    Icon = DB_TREE_TABLE_SELECT
    # if another was selected clear it (simply clear all)
    if self.Tree.GetItemImage ( table ) == DB_TREE_UNCHECKED :
      MainNode, cookie = self.Tree.GetFirstChild ( self.Tree.root )
      while MainNode :
        Table_View, cookie = self.Tree.GetFirstChild ( MainNode )
        while Table_View :
          self.Tree.SetItemImage ( Table_View, DB_TREE_UNCHECKED, CT.TreeItemIcon_Normal )
          self.Tree.SetItemImage ( Table_View, DB_TREE_UNCHECKED, CT.TreeItemIcon_Expanded )
          Table_View = self.Tree.GetNextSibling ( Table_View )
        MainNode = self.Tree.GetNextSibling ( MainNode )

      self.Tree.SetItemImage ( table, Icon, CT.TreeItemIcon_Normal )
      self.Tree.SetItemImage ( table, Icon, CT.TreeItemIcon_Expanded )
      
    # Generate SQL statement
    Fields     = []
    Sorted     = None
    Reversed   = False
    Node, cookie = self.Tree.GetFirstChild ( table )
    while Node :
      item  = self.Tree.GetItemImage ( Node )
      if item != DB_TREE_UNCHECKED :
        field = self.Tree.GetItemText ( Node )
        if '/' in field :
          field = '"' + field + '"'
        Fields.append ( field )
        if   item == DB_TREE_SORT_ASC :
          Sorted = field
        elif item == DB_TREE_SORT_DESC :
          Sorted = field
          Reversed = True
      Node = self.Tree.GetNextSibling ( Node )
      
    # if no Fields selected, select them all
    if len ( Fields ) == 0 :
      Fields = '*'
    self.SQL = 'SELECT ' + ' ,'.join ( Fields ) + '\n' + \
               'FROM ' + table_name
    if Sorted :
      self.SQL += '\n' + 'ORDER BY ' + Sorted
    if Reversed :
      self.SQL += ' DESC'

    # if SQL changed, send to the output
    if self.SQL != self.Old_SQL :
      self.Old_SQL = self.SQL
      self.P[0] = self.SQL

    # if another table is selected, send to output
    self.Table_Info = self.Tree.GetPyData ( sel_item )
    if self.Table_Info != self.Old_Table_Info :
      self.Old_Table_Info = self.Table_Info
      self.P[1] = self.Table_Info

  # *************************************************************
  # if selection changed, set Params,
  # so Output Value will be changed
  # highlight it on the canvas
  # *************************************************************
  def OnActivated ( self, event ) :
    item = event.GetItem ()
    self.Set_Active_Table ( item, True )

  # *************************************************************
  # Change the icon if clicked on it
  # *************************************************************
  def On_Icon_Click ( self, item ) :
    level,main_parent = self.Tree.Get_Item_Level_MainParent ( item )
    if level > 1 : 
      self.Set_Active_Table ( item )

  # *************************************************************
  # *************************************************************
  def SetValue ( self, Value ) :
    #print '************ DBTREE SETVALUE ***********', Value

    self.MetaData = Value
    Tree = self.Tree
    Tree.DeleteAllItems ()
    Root = Tree.AddRoot ( 'ROOT' )

    def Add_To_Tree ( Parent, item, Icon, PyData = None ) :
      NewItem = Tree.AppendItem ( Parent, item )
      if PyData :
        Tree.SetPyData ( NewItem, PyData )
      import customtreectrl_SM as CT
      Tree.SetItemImage ( NewItem, Icon, CT.TreeItemIcon_Normal )
      Tree.SetItemImage ( NewItem, Icon, CT.TreeItemIcon_Expanded )
      return NewItem

    Parent = Root
    from db_support import _DB_Groups
    Main_Icons = ( 38,
                   58,
                   31,  #42  #31
                   42,  #40  #42
                   25,
                   53 )
                   
    for main_index, Group in enumerate ( _DB_Groups ) :
      if Group in self.MetaData :
        Group_Info = self.MetaData [ Group ]
        Header = Group_Info [0]
        NewItem = Add_To_Tree ( Parent, Group, Main_Icons [ main_index ] )

        #Parent = NewItem
        for table in Group_Info [1:]  :
          # Create metadata about this table
          table_info = copy ( table [2] )
          table_info.insert ( 0,
            [ 'Prim Key', 'Name', 'Type', 'NotNull', 'Default' ] )

          Icon = DB_TREE_UNCHECKED
          NewItem2 = Add_To_Tree ( NewItem, table[0], Icon, table_info )

          Icon = DB_TREE_CHECKED
          for field in table[2] :
            Add_To_Tree ( NewItem2, field[1], Icon, table_info )

  # *************************************************************
  # *************************************************************
  #def GetValue ( self ) :
  #  print '   TREE GETVALUEGRID'
  #  return 'aapls'

  # *************************************************************
  # *************************************************************
  def Save_Settings ( self, ini, key = None ) :
    if not ( key ) :
      key = 'CS_'
    return
    if ini :
      line = []
      line = ini.Write ( key, line )


  # *************************************************************
  # *************************************************************
  def Load_Settings ( self, ini, key = None ) :
    if not ( key ) :
      key = 'CS_'
    line = ini.Read ( key, '' )
    if line :
      pass


# ***********************************************************************
pd_Module ( __file__ )
