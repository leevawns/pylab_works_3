import __init__
from base_control import *

from   PyLab_Works_Globals import _
import PyLab_Works_Globals as PG
import wx
import sys
#from   tree_support import *
from grid_support import Base_Grid
import  wx.grid as gridlib


# ***********************************************************************
#
# You can add new attributes, without declaring them first, like
#   a = s_list ( [3,4] )
#   a.Some_New_Attribute = True
#
# ***********************************************************************
class tGrid_List ( list ) :

  # *********************************************************
  # *********************************************************
  #def __init__ ( self, value = [] ) :
  #  # create the orginal Python list
  #  list.__init__ ( self, value )

  def __init__ ( self, *args ) :
    # create the orginal list
    list.__init__ ( self, args )

    # create some default values
    self.Fixed_Color = 345



    
    # create some default values
    self.Fixed_Color  = wx.GREEN
    self.Fixed_Row    = True
    self.Fixed_Column = False
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class t_C_Grid ( My_Control_Class ):

  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    self.Frame = Frame = self.Dock
    while not ( isinstance ( Frame, wx.Frame )) :
      Frame = Frame.parent
    self.Frame.SetClientSize ( self.Dock.GetBestSize())

    """
    if Brick :
      self.IniSection = 'Device ' + Brick.Name
    else :
      self.IniSection = 'Device Std-Viewer'
    """

    #self.Grid = gridlib.Grid ( Dock, -1 )
    self.Grid = Base_Grid ( self.Dock )

    #self.Grid.SetLabelBackgroundColour ( wx.RED )
    r = g = b = 180
    self.Grid.SetLabelBackgroundColour ( wx.Color ( r,g,b ) )
    columns = [ 'field', 'cid' ]
    self.Grid.CreateGrid ( 0, len ( columns ), gridlib.Grid.SelectRows )
    for i, name in enumerate ( columns ) :
      self.Grid.SetColLabelValue ( i, name )

    self.Grid.SetRowLabelSize ( 0 )
    self.Grid.SetColLabelAlignment ( wx.ALIGN_LEFT, wx.ALIGN_CENTRE )
    self.Grid.EnableGridLines ( False )
    self.Grid.SetColLabelSize ( 20 )

    #self.Grid.SetDefaultRowSize ( 8, True )  ##DONT USE !!
    MH = 8
    self.Grid.SetRowMinimalAcceptableHeight ( MH )
    #self.Grid.SetDefaultRowSize ( MH, True )
    self.Grid.EnableEditing ( False )
    self.Grid.SetCellHighlightPenWidth ( 0 )
    self.Grid.DisableDragRowSize ( )

    #self.Frame.SetClientSize ( self.Dock.GetBestSize()) ##

    # doesn't work here : self.AutoSizeColumns ( True )

    # Create instances of cols, rows, to handle properties
    #self.columns = _Table_Columns ( self )
    #self.rows    = _Table_Rows    ( self )


    # *************************************************************
    # Create the panel with checkboxes
    # *************************************************************
    #self.Panel = wx.Panel ( Dock )

    sizer = wx.BoxSizer ( wx.VERTICAL )
    sizer.Add ( self.Grid, 1, wx.EXPAND )
    #sizer.Add ( self.Panel, 0, wx.EXPAND )
    self.Dock.SetSizer ( sizer )

  # *************************************************************
  # *************************************************************
  def SetValue ( self, value ) :
    if isinstance ( value, tGrid_List ) :
      #print 'YES', value.Fixed_Color
      self.Grid.SetLabelBackgroundColour ( value.Fixed_Color )
    #else : print 'No'

    #print '******* SetValue ',type(value),value
    #for item in value :
    #  print item
    
    self.Grid.AutoSizeRows ( True )

    N = self.Grid.GetNumberRows ()
    if N > 0 : self.Grid.DeleteRows ( numRows = N )
    self.Grid.DeleteCols ( numCols = self.Grid.GetNumberCols () )
    #self.Grid.ClearGrid ()

    # add the column headers
    try :
      i = value[0]
    except :
      return

    self.Grid.AppendCols ( len ( value [0] ) )
    for i, name in enumerate ( value [0] ) :
      self.Grid.SetColLabelValue ( i, name )

    # add all the row data
    for i, row in enumerate ( value [1:] ) :
      self.Grid.AppendRows ( 1 )
      R = self.Grid.GetNumberRows ()
      for C, cell in enumerate ( row ) :
        self.Grid.SetCellValue ( R-1, C, str ( cell ) )

    #self.Grid.ForceRefresh ()
    self.Grid.AutoSizeRows ( True )
    self.Grid.AutoSizeCols ( True )
    self.Grid.ForceRefresh ()

  # *************************************************************
  # *************************************************************
  def Save_Settings ( self, ini, key = None ) :
    if not ( key ) :
      key = 'CS_'
    return
    if ini :
      line = []
      line = ini.Write ( 'CS_', line )

  # *************************************************************
  # *************************************************************
  def Load_Settings ( self, ini, key = None ) :
    if not ( key ) :
      key = 'CS_'
    line = ini.Read ( key, '' )
    if line :
      pass
# ***********************************************************************
