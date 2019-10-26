import __init__
# ***********************************************************************
import  wx
import  wx.grid as gridlib
#from PyLab_Works_Globals import *
from language_support import _
# ***********************************************************************


__doc__ = """
# ***********************************************************************
# Creates a form that displays all the device properties
# and lets the user edit these properties
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007 Stef Mientki
# mailto:S.Mientki@ru.nl
"""


_Version_Text = [

[ 2.2 , '10-04-2009', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- Color type cells, didn't color upon init, bug fixed
""" ],


[ 2.1 , '27-07-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - New Base_Grid should be used as the base of all Grids
 - Added Get_Settings and Do_Settings,
   to save and reload the user settings in an config file
 - Setting Column Attributes improved to work around bug in wxPython
 - Added faciltity to define a set of attributes and
   to use them with new procedures for setting Cell, Row and Col Attributes
 - export Grid data to a tab-delimited file, through RM-menu
""")],

[ 2.0 , '10-12-2007', 'Stef Mientki',
'Test Conditions:', (),
_(0, '  - changed behavior of STAY ON TOP properties form')],

[ 1.0 , '14-07-2007', 'Stef Mientki',
'Test Conditions:', (),
_(0, ' - orginal release')]
]
# ***********************************************************************


import  os

import  wx.lib.newevent

from dialog_support import AskFileForOpen, Ask_File_For_Save
from inifile_support import *
from menu_support import *
# ***********************************************************************


# ***********************************************************************
# We want to edit colors directly through a colordialog
# ***********************************************************************
#global MY_GRID_TYPE_COLOR, MY_GRID_PINS
MY_GRID_TYPE_COLOR     = 'color'
MY_GRID_TYPE_FILE      = 'file'
MY_GRID_PINS           = 'pins'

MY_GRID_NONE_FIXED     = 0
MY_GRID_ROW_FIXED      = 1
MY_GRID_ROW_COL_FIXED  = 2
MY_GRID_COL_ROW_FIXED  = 2
MY_GRID_COL_FIXED      = 3

MY_GRID_ROW_TYPED      = 0
MY_GRID_COL_TYPED      = 1

# ***********************************************************************


# ***********************************************************************
# Largely taken from the standard example
# ***********************************************************************
class CustomDataTable ( gridlib.GridTableBase ) :
  def __init__ ( self, data, data_types, data_defs ) :
    gridlib.GridTableBase.__init__ ( self )
    self.data       = data
    self.data_types = data_types
    self.data_defs  = data_defs

    if data_defs [1] in [ MY_GRID_COL_FIXED, MY_GRID_ROW_COL_FIXED ] :
      self.CF = 1
    else :
      self.CF = 0

    if data_defs [1] in [ MY_GRID_ROW_FIXED, MY_GRID_ROW_COL_FIXED ] :
      self.RF = 1
    else :
      self.RF = 0

  # ****************************************************************
  # excluding an possible fixed row !!
  # ****************************************************************
  def GetNumberRows ( self ) :
    return len ( self.data [ self.RF : ] )

  # ****************************************************************
  # excluding an possible fixed column !!
  # ****************************************************************
  def GetNumberCols ( self ) :
    return len ( self.data [0] [ self.CF : ] )

  # ****************************************************************
  # ****************************************************************
  def Correct_RC ( self, row, col ) :
    if self.data_defs [1] in [ MY_GRID_COL_FIXED, MY_GRID_ROW_COL_FIXED ] :
      col += 1
    if self.data_defs [1] in [ MY_GRID_ROW_FIXED, MY_GRID_ROW_COL_FIXED ] :
      row += 1
    return row, col

  # ****************************************************************
  # ****************************************************************
  def IsEmptyCell ( self, row, col ) :
    R, C = self.Correct_RC ( row, col )
    try:
      return not ( self.data [R] [C] )
    except IndexError:
      return True

  # ****************************************************************
  # ****************************************************************
  def GetValue ( self, row, col ) :
    R, C = self.Correct_RC ( row, col )
    try:
      #print 'TYPE',self.data_types[C],self.data [R] [C]
      Val = self.data [R] [C]
      if isinstance ( Val, str )  and \
         ( self.data_types [C] != gridlib.GRID_VALUE_STRING ) :
        #print 'OOOO',C,self.data_types[C], Val
        Val = Val.strip ()
        if Val != '' :
          if   self.data_types[C] == gridlib.GRID_VALUE_BOOL :
            Val = bool ( Val )
          elif self.data_types[C] == gridlib.GRID_VALUE_NUMBER :
            Val = int ( Val )
          elif self.data_types[C] == MY_GRID_TYPE_COLOR :
            Val = tuple ( Val )
          elif self.data_types[C] == gridlib.GRID_VALUE_FLOAT :
            Val = float ( Val )
          elif self.data_types[C] == gridlib.GRID_VALUE_CHOICE :
            Val = Val
          else :
            Val = Val
        else :
          if   self.data_types[C] == gridlib.GRID_VALUE_BOOL :
            Val = False
          elif self.data_types[C] == gridlib.GRID_VALUE_NUMBER :
            Val = 0
          elif self.data_types[C] == MY_GRID_TYPE_COLOR :
            Val = tuple ( wx.RED )
          elif self.data_types[C] == gridlib.GRID_VALUE_FLOAT :
            Val = 0
          elif self.data_types[C] == gridlib.GRID_VALUE_CHOICE :
            Val = 0
          else :
            Val = Val

      #print '----',C,self.data_types[C], Val
      return Val
    except IndexError:
      return ''

  # ****************************************************************
  # ****************************************************************
  def SetValue ( self, row, col, value ) :
    R, C = self.Correct_RC ( row, col )
    self.data [R] [C] = value
    
    # for some special cases, lets update the grid
    typ = self.GetRawTypeName ( row, col )
    if typ in [ MY_GRID_TYPE_COLOR ] :
      self.GetView().Update_Colors( row, col )


  """
  # ****************************************************************
  # never called with the starnge AppendRows in Grid !!
  # ****************************************************************
  def AppendRows ( self, NumRows = 1, updateLabels = True ) : #*args, **kwargs):
    #print 'A',self.table.GetNumberRows (), self.GetNumberRows ()
    NC = self.GetNumberCols ()
    self.data.append ( NC * [''])
    return True
  """


  # ****************************************************************
  # Called when the grid needs to display labels
  # ****************************************************************
  def GetColLabelValue ( self, col ) :
    R, C = self.Correct_RC ( 0, col )
    return self.data [0] [C]

  # ****************************************************************
  # ****************************************************************
  def GetRowLabelValue ( self, row ) :
    R, C = self.Correct_RC ( row, 0 )
    return self.data [R] [0]

  # ****************************************************************
  # ****************************************************************
  def GetRawTypeName(self, row, col):
    if self.data_defs [0] == MY_GRID_ROW_TYPED :
      return self.data_types [row]
    else :
      return self.data_types [col]

  # ****************************************************************
  # ****************************************************************
  def GetTypeName(self, row, col):
    typ = self.GetRawTypeName ( row, col )
    if typ in [ MY_GRID_TYPE_COLOR,
                 MY_GRID_TYPE_FILE,
                 MY_GRID_PINS ] :
      return gridlib.GRID_VALUE_STRING
    else:
      return typ

  # ****************************************************************
  # ****************************************************************
  def CanGetValueAs ( self, row, col, typeName ) :
    if self.data_defs[0] == MY_GRID_ROW_TYPED :
      DataType = self.data_types [row].split(':')[0]
    else :
      DataType = self.data_types [col].split(':')[0]
    if typeName == DataType:
      return True
    else:
      return False

  # ****************************************************************
  # ****************************************************************
  def CanSetValueAs ( self, row, col, typeName ) :
    return self.CanGetValueAs ( row, col, typeName )
# ***********************************************************************

# ***********************************************************************
# This extends the gridlib.Grid with :
#   - standard RM-menu
# ***********************************************************************
class Base_Grid ( gridlib.Grid ) :
  def __init__ ( self, parent, table = None, name = 'Base Grid' ) :
    gridlib.Grid.__init__ ( self, parent, -1 )
    self.parent = parent
    self.My_Name = name
    # If used with a table,
    # most calls will be done to the table instead of the grid
    # WATCH OUT: not all calls are identical
    if table :
      self.table  = table
    else :
      self.table = self

    self.SetMargins ( 0, 0 )
    self.DefaultCellOverflow = False



    # *************************************************************
    # popup menus
    # *************************************************************
    pre = [ _(0, 'Export (tab delim)' ),
          ]
    self.Popup_Menu = My_Popup_Menu ( self.On_Popup_Item_Selected, None,
      pre = pre )
    self.Transparancy = 0
    self.Bind ( gridlib.EVT_GRID_CELL_RIGHT_CLICK, self.On_Show_Popup )
    #self.Bind ( wx.EVT_CONTEXT_MENU, self.On_Show_Popup )
    # *************************************************************

    # ****************************************************************
    # EVENT BINDINGS
    # ****************************************************************
    #self.Bind ( gridlib.EVT_GRID_COL_SIZE,        self.OnColSize )
    self.Bind ( gridlib.EVT_GRID_EDITOR_SHOWN,    self.OnEditorShown )

    # EVT_GRID_EDITOR_HIDDEN is fired twice at the end of an edit session
    # while EVT_GRID_CELL_CHANGE is fired only once
    self.Bind ( gridlib.EVT_GRID_CELL_CHANGED,     self.OnEditorChange )

    self.Bind ( gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnLeftClick )
    if self.table != self :
      self.Bind ( gridlib.EVT_GRID_SELECT_CELL,     self.onCellSelected )
    self.Bind ( gridlib.EVT_GRID_EDITOR_CREATED,  self.onEditorCreated )

  # ********************************************************
  # ********************************************************
  def GetName ( self ) :
    return self.My_Name

  # *****************************************************************
  # *****************************************************************
  def On_Show_Popup ( self, event ) :
    self.Hit_Pos = event.GetPosition ()
    self.PopupMenu ( self.Popup_Menu, pos = self.Hit_Pos )

  # *****************************************************************
  # *****************************************************************
  def On_Popup_Item_Selected ( self, event ) :
    ID = event.Int
    if ID == 0 :
      file = Ask_File_For_Save ( os.getcwd(),
                                 FileTypes = '*.tab',
                                 Title = _(0, 'Save Table as TAB-delimited file' ))
      if file :
        file = open ( file, 'w' )
        if self.table == self :
          GetValue = self.GetCellValue
        else :
          GetValue = self.table.GetValue

        for R in range ( self.table.GetNumberRows () ) :
          line = ''
          for C in range ( self.table.GetNumberCols () ) :
            line += str ( GetValue ( R, C ) ) +  '\t'
          file.write ( line +'\n')


        """ for R in range ( self.table.GetNumberRows () ) :
            line = ''
            for C in range ( self.table.GetNumberCols () ) :
              line += str ( self.table.GetValue ( R, C ) ) +  '\t'
            file.write ( line +'\n')
        else :
          for R in range ( self.GetNumberRows () ) :
            line = ''
            for C in range ( self.GetNumberCols () ) :
              line += str ( self.GetCellValue ( R, C ) ) +  '\t'
            file.write ( line +'\n')
        """
        file.close ()

  # *****************************************************************
  # *****************************************************************
  def Get_Settings ( self ) :
    line = []
    for C in range ( self.table.GetNumberCols () ) :
      line.append ( self.GetColSize (C) )
    return line

  # *****************************************************************
  # *****************************************************************
  def Do_Settings ( self, line ) :
    if line :
      for C in range ( self.table.GetNumberCols () ) :
        self.SetColSize ( C, int ( line [C] ) )

  # ****************************************************************
  # v
  # ****************************************************************
  def Align_Col ( self, col,
                  align_hor = wx.ALIGN_LEFT,
                  align_ver = wx.ALIGN_CENTER ) :
    attr1 = gridlib.GridCellAttr()
    attr1.SetAlignment ( align_hor, align_ver )
    attr1.IncRef()       # Robin Dunn !!
    self.SetColAttr ( col, attr1 )

  # ****************************************************************
  # ****************************************************************
  def AppendRows ( self, NumRows = 1 ) :
    if self.table == self :
      gridlib.Grid.AppendRows ( self, NumRows )
    else :
      # apparently in this construction table.AppendRows is NOT called
      # so we add the lines here
      NC = self.table.GetNumberCols ()
      for i in range ( NumRows ) :
        self.table.data.append ( NC * [''] )
      self.ProcessTableMessage(wx.grid.GridTableMessage ( self.table,
        wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED, NumRows ) )

  # ****************************************************************
  # ****************************************************************
  def GetRowValue ( self, Row ) :
    """
    This is a docstring from GetRowValue
    """
    RowValue = []
    if self.table == self :
      GetValue = self.GetCellValue
    else :
      GetValue = self.table.GetValue
    for i in range ( self.table.GetNumberCols () ) :
      RowValue.append ( GetValue ( Row, i ) )
    return RowValue

  # ****************************************************************
  # ****************************************************************
  def OnLeftClick ( self, event ) :
    if self.table != self :
      if self.table.GetTypeName ( event.Row, event.Col ) == \
           gridlib.GRID_VALUE_BOOL :
        wx.CallLater ( 100, self.toggleCheckBox )
    event.Skip()

  # ****************************************************************
  # ****************************************************************
  def onCheckBox ( self, event ) :
    self.afterCheckBox ( event.IsChecked () )

  # ****************************************************************
  # ****************************************************************
  def toggleCheckBox ( self ) :
    # this doesn't work always,
    # sometimes "cb" is not yet known !!
    try :
      self.cb.Value = not self.cb.Value
      self.afterCheckBox ( self.cb.Value )
    except :
      pass

  # ****************************************************************
  # ****************************************************************
  def afterCheckBox ( self, IsChecked ) :
    self.table.data [self.GridCursorRow + self.table.RF] \
                    [self.GridCursorCol + self.table.CF] = IsChecked
    self.OnEditorChange ( None )

  # ****************************************************************
  # ****************************************************************
  def onCellSelected ( self, event ) :
    if self.table != self :
      if self.table.GetTypeName ( event.Row, event.Col ) in \
            [ gridlib.GRID_VALUE_BOOL, MY_GRID_TYPE_COLOR, MY_GRID_TYPE_FILE ] :
        wx.CallAfter ( self.EnableCellEditControl )
    event.Skip ()


  # ****************************************************************
  # called by table.SetValue, to change the active background color
  # ****************************************************************
  def Update_Colors ( self, R, C ) :
    RD = R + self.table.RF
    CD = C + self.table.CF
    if self.table.data [RD] [CD] :
      self.SetCellBackgroundColour ( R, C, self.table.data [RD] [CD] )
    else : # if empty string, leave it white
      self.SetCellBackgroundColour ( R, C, wx.WHITE )
    self.ForceRefresh()

  # ****************************************************************
  # Attribs = {
  #   'normal': [ font, textcolor, bgcolor ],
  #   3       : [ font, textcolor, bgcolor ],
  #   }
  # ****************************************************************
  def Define_Attribs ( self, Attribs ) :
    self.Attribs = Attribs
    for Attrib in Attribs :
      attr = gridlib.GridCellAttr()
      A = Attribs [ Attrib ]
      if A[0] :
        attr.SetFont ( A[0] )
      #else :
      #  attr.SetFont ( self.GetCellFont ( 0, 0 ) )
      if A[1] :
        attr.SetTextColour ( A[1] )
      if A[2] :
        attr.SetBackgroundColour ( A[2] )
      A.append ( attr )

  # ****************************************************************
  # ****************************************************************
  def Set_Cell_Attrib ( self, Col, Row, Attrib ) :
    try :
      A = self.Attribs [ Attrib ]
      if A[0] :
        self.SetCellFont ( Row, Col, A[0] )
      if A[1] :
        self.SetCellTextColour ( Row, Col, A[1] )
      if A[2] :
        self.SetCellBackgroundColour ( Row, Col, A[2] )
      self.ForceRefresh()
    except :
      pass

  # ****************************************************************
  # ****************************************************************
  def Set_Row_Attrib ( self, Row, Attrib ) :
    attr = self.Attribs [ Attrib ][-1]
    self.SetRowAttr ( Row, attr)
    self.ForceRefresh()

  # ****************************************************************
  # ****************************************************************
  def Set_Col_Attrib ( self, Col, Attrib ) :
    attr = self.Attribs [ Attrib ][-1]
    self.SetColAttr ( Col, attr)
    attr.IncRef()    # Robin Dunn !!
    self.ForceRefresh()

  # ****************************************************************
  # ****************************************************************
  def Set_Row_Color ( self, Row, Color ) :
    # attribute objects let you keep a set of formatting values
    # in one spot, and reuse them if needed
    attr = gridlib.GridCellAttr()
    attr.SetFont ( self.GetCellFont ( Row, 0 ) )
    #attr.SetTextColour ( wx.BLACK )
    attr.SetBackgroundColour ( Color )

    # you can set cell attributes for the whole row (or column)
    self.SetRowAttr ( Row, attr)
    self.ForceRefresh()

  # ****************************************************************
  # NOTE: OnEditorShown occurs before OnEditorCreated !!
  # ****************************************************************
  def OnEditorShown(self, event):
    if self.table == self :
      event.Skip ()
      return

    R = event.GetRow()
    C = event.GetCol()
    RD = R + self.table.RF
    CD = C + self.table.CF

    if self.table.GetRawTypeName ( R, C )  == MY_GRID_TYPE_COLOR :
      # we manualy create a begin edit event
      #self.OnEditorCreated(event)

      # start the global color dialog
      # First block closing of the application
      #if self.Set_Modal_Open :
      #  self.Set_Modal_Open ( True )
        
      try:
        from dialog_support import Color_Dialog
        color = Color_Dialog ( self, self.table.data [RD] [CD] )
        # get the new color and store it
        self.table.data [RD] [CD] = color
        self.SetCellBackgroundColour ( R, C, self.table.data [RD] [CD] )
        self.ForceRefresh()

        # manualy generate an EditorChange event
        self.OnEditorChange(event)
        """
        colordlg = wx.ColourDialog ( self )
        colordlg.GetColourData().SetChooseFull(True)
        if self.Custom_Colors:
          cc = self.Custom_Colors
          for i in range ( len ( cc ) ):
            colordlg.GetColourData().SetCustomColour ( i, cc[i] )

        colordlg.GetColourData().SetColour ( self.table.data [RD] [CD] )
        if colordlg.ShowModal() == wx.ID_OK:
          # get the new color and store it
          self.table.data [RD] [CD] = colordlg.GetColourData().GetColour().Get()
          self.SetCellBackgroundColour ( R, C, self.table.data [RD] [CD] )
          self.ForceRefresh()

          # manualy generate an EditorChange event
          self.OnEditorChange(event)

        if self.Custom_Colors :
          cc = []
          for i in range ( 16 ):
            cc.append ( colordlg.GetColourData().GetCustomColour ( i ) )
          self.Custom_Colors = cc
        colordlg.Destroy()
        """
      finally:
        # unlock possibility to close the application
        #if self.Set_Modal_Open : self.Set_Modal_Open ( False )
        pass

      # prevent further actions for this event
      event.Veto()

    elif self.table.GetRawTypeName ( R, C )  == MY_GRID_TYPE_FILE :
      # start the global file dialog
      # First block closing of the application
      if self.Set_Modal_Open : self.Set_Modal_Open ( True )
      try:
        ##filepath, filename = path_split ( self.table.data [R] [1] )
        filepath, filename = path_split ( self.table.data [RD] [CD] )
      except:
        ##filepath = PG.Program_Directory
        filepath = os.getcwd ()
        filename = ''

      filename = AskFileForOpen ( filepath, filename,
                                  FileTypes = '*.dat', Title = 'Select File' )
      if filename:
        self.table.data [RD] [CD] = filename

        self.ForceRefresh()

        # manualy generate an EditorChange event
        self.OnEditorChange(event)

        # unlock possibility to close the application
        if self.Set_Modal_Open : self.Set_Modal_Open ( False )

      # prevent further actions for this event
      event.Veto()

    # proceed with normal event handle
    else:
      event.Skip()

  # ****************************************************************
  # NOTE: OnEditorShown occurs before OnEditorCreated !!
  # ****************************************************************
  def onEditorCreated(self,event):
    if self.table == self :
      event.Skip ()
      return
    
    R = event.GetRow()
    C = event.GetCol()

    if self.table.GetRawTypeName ( R, C )  == gridlib.GRID_VALUE_BOOL :
      self.cb = event.Control
      self.cb.WindowStyle |= wx.WANTS_CHARS
      self.cb.Bind ( wx.EVT_KEY_DOWN, self.onKeyDown )
      self.cb.Bind ( wx.EVT_CHECKBOX, self.onCheckBox )

    elif self.table.GetRawTypeName ( R, C ) in \
           [ MY_GRID_TYPE_COLOR,  MY_GRID_TYPE_FILE ] :
      pass
    # proceed with normal event handle
    else:
      event.Skip()


  # ****************************************************************
  # ****************************************************************
  def onKeyDown ( self, event ) :
    if event.KeyCode == wx.WXK_UP :
      if self.GridCursorRow > 0:
        self.DisableCellEditControl ()
        self.MoveCursorUp ( False )
    elif event.KeyCode == wx.WXK_DOWN :
      if self.GridCursorRow < ( self.NumberRows - 1 ) :
        self.DisableCellEditControl ()
        self.MoveCursorDown ( False )
    elif event.KeyCode == wx.WXK_LEFT :
      if self.GridCursorCol > 0 :
        self.DisableCellEditControl ()
        self.MoveCursorLeft ( False )
    elif event.KeyCode == wx.WXK_RIGHT :
      if self.GridCursorCol < ( self.NumberCols - 1 ) :
        self.DisableCellEditControl ()
        self.MoveCursorRight ( False )
    else :
      event.Skip ()

  # testen bij meer colomns
  """
  def OnColSize ( self, event ) :
    #if event.GetRowOrCol() == 0 :
    self.ColSize0 ()
    event.Skip ()
  """

  # ****************************************************************
  # This is weird behavior of wxPython
  # if we don't leave room for a scrollbar,
  # the scrollbar will appear !!
  # Robin Dunn says: This is a problem with how the wx.ScrolledWindow is implemented.
  # Since it has fixed size scroll increments it always rounds the virtual size
  # up to an even multiple of the scroll increment,
  # so unless your virtual size is already an even multipl
  # you end up with needing a bit of extra unexpected space
  # in order to make the scrollbars be unnecessary.
  # ****************************************************************
  """
  def ColSize0 ( self ) :
    N = self.GetNumberCols () - 1
    if self.table.CF :
      w = self.GetRowLabelSize ()
    else :
      w = 0
    for col in range ( N ) :
      w += self.GetColSize ( col )
    self.SetColSize ( N, self.parent.GetSize()[0] - w - 20 )
  """

  # ****************************************************************
  # Notify the parent/owner that some data properties have changed
  # ****************************************************************
  def OnEditorChange ( self, event ) :
    if self.table == self :
      event.Skip ()
      return

    if self.Notify_Params_Changed :
      self.Notify_Params_Changed ( self.GetTable().data )
# ***********************************************************************

# ***********************************************************************
# the improved handling of boolean editing, is taken from Frank Millman
#   http://wiki.wxpython.org/Change_wxGrid_CheckBox_with_one_click
# ***********************************************************************
#class CustTableGrid ( gridlib.Grid ):
class Base_Table_Grid ( Base_Grid ):
  #def __init__ ( self, parent, Device,
  def __init__ ( self, parent,
                 data, data_types, data_defs,
                 ##custom_colors = None,
                 ##Set_Modal_Open = None,
                 name = 'Table Grid',
                 Notify_Params_Changed = None ) :
                   
    self.table                 = CustomDataTable ( data, data_types, data_defs )
    #gridlib.Grid.__init__(self, parent, -1)
    Base_Grid.__init__ ( self, parent, self.table, name = name )
    ##self.device                = Device
    ##self.Custom_Colors         = custom_colors
    ##self.Set_Modal_Open        = Set_Modal_Open
    self.Notify_Params_Changed = Notify_Params_Changed

    # attach table (ownership = True to auto destroy)
    self.SetTable ( self.table, True )

    if data_defs [1] in [ MY_GRID_COL_FIXED, MY_GRID_ROW_COL_FIXED ]:
      self.SetRowLabelSize ( 40 )
    else :
      self.SetRowLabelSize ( 0 )
    if data_defs [1] in [ MY_GRID_ROW_FIXED, MY_GRID_ROW_COL_FIXED ]:
      self.SetColLabelSize ( 16 )
    else :
      self.SetColLabelSize ( 0 )
    self.SetRowLabelAlignment (wx.ALIGN_LEFT, wx.ALIGN_CENTER )
    self.SetColLabelAlignment (wx.ALIGN_RIGHT, wx.ALIGN_CENTER )

    #self.AutoSizeRows (True)
    #self.DeleteRows()
    #self.ClearGrid()

    # due to a bug / limitation in wxPython
    # numbers are always aligned right
    # so therefor we align everyhting right
    attr1 = gridlib.GridCellAttr()
    attr1.SetAlignment ( wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
    #attr1.SetAlignment ( wx.ALIGN_LEFT, wx.ALIGN_CENTER_VERTICAL)
    #attr1.SetAlignment ( wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
    for col in range ( self.GetNumberCols () ) :
      self.SetColAttr ( col, attr1 )
      attr1.IncRef()    # Robin Dunn !!

      for row in range ( self.GetNumberRows () ) :
        typ = self.table.GetRawTypeName ( row, col )
        if typ in [ MY_GRID_TYPE_COLOR ] :
          self.table.GetView().Update_Colors( row, col )
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class tProperties_Form(wx.Frame):
  def __init__ ( self, parent, device,
                 data, data_types, data_defs,
                 title, Pos = (50,50) ):
    self.device = device
    self.data   = data
    
    # the initial height/width of the form is derived from
    # the number of elements corrected for fixed row/col
    N = len ( data )
    if data_defs [1] in [ MY_GRID_ROW_FIXED, MY_GRID_ROW_COL_FIXED ]:
      N += 1
    h = 55 + 17 * N
    
    N = len ( data [0] )
    if data_defs [1] in [ MY_GRID_COL_FIXED, MY_GRID_ROW_COL_FIXED ]:
      N += 1
    w = 40 + 40 * N


    FormStyle = wx.DEFAULT_FRAME_STYLE | \
                wx.TINY_CAPTION_HORIZ
                #wx.STAY_ON_TOP
    if parent:
      FormStyle = FormStyle | wx.FRAME_FLOAT_ON_PARENT    # needs a parent

    wx.Frame.__init__(
        self, parent, -1, title,
        size = ( w, h ),
        pos = Pos,
        style = FormStyle
        )

    Program_Custom_Colors = []
    panel = wx.Panel ( self, -1, style=0, size=[200,200] )
    ##self.grid = Base_Table_Grid ( panel, device,
    self.grid = Base_Table_Grid ( panel,
                                data, data_types, data_defs,
                                'Name',
                                self.Notify_Params_Changed
                                )
    box = wx.BoxSizer ( wx.VERTICAL )
    box.Add ( self.grid, 1, wx.GROW | wx.ALL, 0 )
    panel.SetSizer ( box )

    # Binding to the panel instead of the form works better
    #panel.Bind ( wx.EVT_SIZE, self.OnResize )

    # Timer to test dynamic updating of grid
    self.Timer = wx.Timer ( self )
    # the third parameter is essential to allow other timers
    self.Bind ( wx.EVT_TIMER, self.OnTimer, self.Timer )
    #self.Timer.Start ( 2000 )


  def OnTimer ( self, event ) :
    #print self.data [1] [1]
    self.data [1] [1] += 1
    self.Device_Refresh_Properties ( self.data )

  # *********************************************************
  # called by the device's container, if properties like position changes
  # in this case the table information will be updated
  # *********************************************************
  def Device_Refresh_Properties (self, data ):
    for R in range ( len(data)):
      try:    self.grid.GetTable().SetValue ( R, 1, data[R][1] )
      except: pass
    self.grid.Refresh()

  def Set_Modal_Open ( self, modal_open = True ):
    print ('Set_Modal_Open', modal_open)
  
  def Notify_Params_Changed ( self, data ) :
    print ('Notify_Params_Changed')

  """
  def OnResize ( self, event ) :
    event.Skip ()
    self.grid.ColSize0 ()
  """
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class Test_Form ( wx.Frame ) :
  def __init__ ( self ) :
    wx.Frame.__init__( self, None )

    GUI = """
    self.NB              ,wx.Notebook   ,style = wx.BK_LEFT
      self.Grid          ,Base_Grid        ,name = 'File'
    """
    self.wxGUI = PG.Create_wxGUI ( GUI, my_parent = 'self' )

    self.Grid.CreateGrid ( 10, 5 ) #, gridlib.Grid.SelectCells )
    self.Grid.SetCellValue ( 2, 1, 'aap' )

    # *******************************************************
    # *******************************************************
    self.Grid.SetLabelBackgroundColour ( wx.RED )
    columns = [ 'field' ]
    #self.Grid.SetColLabelValue ( 0, 'beer')
    #self.Grid.CreateGrid ( 0, len ( columns ), gridlib.Grid.SelectRows )
    #self.Grid.SetSelectionMode ( gridlib.Grid.SelectCells )
    ##self.Grid.CreateGrid ( 1, 1, gridlib.Grid.SelectCells )

    for i, name in enumerate ( columns ) :
      self.Grid.SetColLabelValue ( i, name )


    self.Grid.SetRowLabelSize ( 0 )
    self.Grid.SetColLabelAlignment ( wx.ALIGN_LEFT, wx.ALIGN_CENTRE )
    self.Grid.SetColLabelSize ( 20 )

    #self.Grid.SetDefaultRowSize ( 8, True )  ##DONT USE !!
    MH = 8
    #self.Grid.SetRowMinimalAcceptableHeight ( MH )
    #self.Grid.SetDefaultRowSize ( MH, True )
    self.Grid.EnableEditing ( True ) #False )
    ##self.Grid.SetCellHighlightPenWidth ( 0 )
    self.Grid.DisableDragRowSize ( )

    #self.Grid.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectCell)
    """
    """
  # *******************************************************
  # *******************************************************
  def OnSelectCell(self, evt):
    #self.log.write("OnSelectCell: (%d,%d) %s\n" %
    #               (evt.GetRow(), evt.GetCol(), evt.GetPosition()))

    # Another way to stay in a cell that has a bad value...
    row = self.Grid.GetGridCursorRow()
    col = self.Grid.GetGridCursorCol()
    value = self.Grid.GetCellValue(row, col)
    print ('CELL',value)
    """
    if self.IsCellEditControlEnabled():
        self.HideCellEditControl()
        self.DisableCellEditControl()


    if value == 'no good 2':
        return  # cancels the cell selection
    """
    evt.Skip()
# ***********************************************************************

# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':
  
  Test_Defs ( 1 )

  # ****************************************************************
  # ****************************************************************
  if Test ( 1 ) :
    app = wx.SimpleApp ()
    data_collection = 2

    # ****************************************************************
    # Fixed first Row,
    # Typed defined by Columns
    # ****************************************************************
    if data_collection == 1 :
      data_values = [
        [ 'Name',     'Enabled',  'X0',  'Gain',  'Color',  'LineType', 'FileName' ],
        [ 'Signal 1',  True,      30,    0.2,     wx.RED,   'Solid',    'D:/test.dat'],
        [ 'Signal 2',  False,     50,    0.25344, wx.BLUE,  'Dash-Dot', ''],
        [ 'Signal 3',  True,      70,    2,       wx.GREEN, 'Solid',    ''] ]
      data_types = [
        gridlib.GRID_VALUE_STRING,
        gridlib.GRID_VALUE_BOOL,
        gridlib.GRID_VALUE_NUMBER,
        gridlib.GRID_VALUE_FLOAT + ':6,2',
        MY_GRID_TYPE_COLOR,
        gridlib.GRID_VALUE_CHOICE + ':Solid,Das-Dot,Dash,Dot',
        MY_GRID_TYPE_FILE ]
      data_defs = ( MY_GRID_ROW_FIXED, MY_GRID_COL_TYPED )

    # ****************************************************************
    # Fixed first Row & first Column,
    # Typed defined by ROW
    # ****************************************************************
    elif data_collection == 2 :
      data_values = [
        [ 'xxx',      'Value'   ],
        [ 'Size',      30       ],
        [ 'Float',     23.45674 ],
        [ 'Color',     wx.RED   ],
        [ 'File',      ''       ],
        [ 'Bool',      True     ],
        [ 'Choice',    'all'    ] ]
      data_types = [
        gridlib.GRID_VALUE_NUMBER,
        gridlib.GRID_VALUE_FLOAT + ':6,2',
        MY_GRID_TYPE_COLOR,
        MY_GRID_TYPE_FILE,
        gridlib.GRID_VALUE_BOOL,
        gridlib.GRID_VALUE_CHOICE + ':JAL,Delphi,Python,other']
      data_defs = ( MY_GRID_ROW_TYPED, MY_GRID_ROW_COL_FIXED )

    ini = inifile ( os.path.join ( os.getcwd (), 'grid_support_test.cfg' ) )
    frame = tProperties_Form ( None, None,
                               data_values, data_types, data_defs,
                               "Properties LEDa", Pos = ( 20, 20 ) )
    frame.Show ()
    app.MainLoop ()

  # ****************************************************************
  # ****************************************************************
  if Test ( 2 ) :
    app = wx.PySimpleApp ()
    frame = Test_Form ( )
    frame.Show ()
    app.MainLoop ()

# ***********************************************************************
pd_Module ( __file__ )

