import __init__
from   PyLab_Works_Globals import _

from   numpy import  array, zeros
import numpy
import wx
from   menu_support    import *

XDIV = YDIV = 10
MAX_SCREEN_WIDTH = 1680  # 19" widescreen TFT

from scope_canvas_base import _PlotCanvas_Base

# ***********************************************************************
# ***********************************************************************
class _PlotCanvas_History ( _PlotCanvas_Base ) :
  def __init__(self, dock, parent, Real_Time = False ):
    _PlotCanvas_Base.__init__ ( self, dock, parent, Real_Time )

    self.Signal_Names = []
    self.Selected_Signal = 0

    # create display buffer and define in it the X-coordinates
    self.Buf_max = 2 * MAX_SCREEN_WIDTH
    self.display_buffer = zeros ( [ self.Buf_max, 2 ] )
    self.display_buffer [ : , 0 ] = array ( range ( self.Buf_max ) ) / 2
    self.Buf = zeros ( [ self.Buf_max ] )

    self.hist_gain   = None

    # At this point we can do all actions that really draw !!
    # call OnSize, to make sure the dc-buffer is initialized.
    self.Set_Canvas ( self.BG_Color, self.Grid_Color )
    self._On_Size ( None )


  # *****************************************************************
  # *****************************************************************
  def _On_Show_Popup ( self, event ) :
    # *************************************************************
    # Create popup menu
    # *************************************************************

    menu_items = []
    menu_items.append ( _(0, 'Remove Cursors'   ) )
    menu_items.append ( _(0, 'Dual Cursor'      ) )
    menu_items.append ( _(0, 'Single Expand 1'  ) )
    menu_items.append ( _(0, 'Single Expand 2'  ) )
    menu_items.append ( _(0, 'Single Expand 4'  ) )
    menu_items.append ( _(0, 'Single Expand 8'  ) )
    menu_items.append ( '-' )
    menu_items += self.Signal_Names
    self.Popup_Menu = My_Popup_Menu ( self._OnPopupItemSelected, None,
                                      pre = menu_items )

    for i in range ( 5 ) :
      self.Popup_Menu.SetChecked ( 1+i , False )
    self.Popup_Menu.SetChecked ( 1 + self.CursorType, True )
    for i in range ( len ( self.Signal_Names ) ) :
      self.Popup_Menu.SetChecked ( i+6, self.Selected_Signal == i )

    self.Hit_Pos = self.ScreenToClient ( event.GetPosition () )
    self.PopupMenu ( self.Popup_Menu, pos = self.Hit_Pos )
    self.Popup_Menu.Destroy()

  # *****************************************************************
  # *****************************************************************
  def _OnPopupItemSelected ( self, event ) :
    ID = event.Int
    if ID == 0 :
      self._Draw_Cursor ( 0, -1 )
      self._Draw_Cursor ( 1, -1 )
    elif ID in range ( 1, 6 ) :
      # if moving from dual to single cursor: remove second cursor
      if self.CursorType == 0 :
        self._Draw_Cursor ( 1, -1 )

      self.CursorType = ID - 1

      # redraw the cursor, so the normal scope will be updated
      self._Draw_Cursor ( 0, self.old_Cursor[0] )
    else :
      self.Selected_Signal = ID - 6
      self.My_Parent._On_History_Signal_Selection ( self.Selected_Signal )

  # *****************************************************************
  # Draw selection cursor
  # *****************************************************************
  def _On_Mouse_Left ( self,event ) :
    x = event.GetPosition() [0]
    # if outside signal range, remove the markers
    if x > self.Buf_wp/2 :
      self._Draw_Cursor ( 0, -1 )
      self._Draw_Cursor ( 1, -1 )
      
    # if not yet cursor-1 and just 1 cursor reuired, draw it
    elif ( self.old_Cursor[0] < 0 ) or ( self.CursorType > 0 ) :
      self._Draw_Cursor ( 0, x )
      
    # if not yet cursor-2, draw it
    elif self.old_Cursor[1] < 0 :
      self._Draw_Cursor ( 1, x )
      
    # if both cursors avalaible, find nearest
    else :
      if abs ( self.old_Cursor[0] - x ) < abs ( self.old_Cursor[1] - x ) :
        self._Draw_Cursor ( 0, x )
      else :
        self._Draw_Cursor ( 1, x )

  # *****************************************************************
  # *****************************************************************
  def _On_Mouse_Move ( self, event ):
    """
    Drag Cursor, if left button down
    """
    if event.LeftIsDown ():
      self._On_Mouse_Left ( event )

  # *****************************************************************
  # Remove all cursors
  # *****************************************************************
  def _On_Mouse_Middle (self, event):
    self._Draw_Cursor ( 0, -1 )
    self._Draw_Cursor ( 1, -1 )

  # *****************************************************************
  # Redraw the signals and the grid, when the window is resized
  # *****************************************************************
  def _On_Size( self, event ):
    # after resizing, cursors are lost, so generate them again
    cursor = self.old_Cursor
    self._Redraw_Screen ()
    self.My_Parent._On_History_Signal_Selection ( self.Selected_Signal )
    self._Draw_Cursor ( 0, cursor[0] )
    self._Draw_Cursor ( 1, cursor[1] )

  # *****************************************************************
  # *****************************************************************
  def Add_SignalName ( self, chan, name ):
    while len ( self.Signal_Names ) < chan + 1 :
      self.Signal_Names.append ( 'Signal-' + str ( len ( self.Signal_Names ) + 1 ))
    # Add the name, remove the units part (if any)
    self.Signal_Names [ chan ] = name.replace(']','').split('[')[0]

  # *****************************************************************
  # *****************************************************************
  def Set_Channel_Color ( self, color ) :
    if not ( isinstance ( color, wx.Colour ) ) :
      color = wx.Colour ( color )
    self.Pen = wx.Pen ( color, 1, wx.SOLID )

  # *****************************************************************
  # Adds a dataset
  # *****************************************************************
  def Set_Data ( self, data ) :
    self.Buf_rp = 0
    self.Buf_wp = 0
    self.N_Average = 1 + len ( data ) // self.Size [0]
    N = len ( data ) // self.N_Average
    #v3print ( 'Scopy_Hist: Set_Data', len(data), self.Size [0], self.N_Average, N)

    self.mean_min = 0.0
    self.mean_max = 0.0
    for i in range ( N ) :
      offset = i * self.N_Average
      self.new_Min = data [ offset ]
      self.new_Max = data [ offset ]
      for ii in numpy.arange ( self.N_Average ) :
        self.new_Min = min ( self.new_Min, data [ offset + ii ] )
        self.new_Max = max ( self.new_Max, data [ offset + ii ] )

      self.Buf [ self.Buf_wp ]    = self.new_Min
      self.Buf [ self.Buf_wp + 1] = self.new_Max
      self.mean_min += self.new_Min
      self.mean_max += self.new_Max
      self.Buf_wp += 2

    self.mean_min /= N
    self.mean_max /= N
    self._Redraw_Screen ()

  # *****************************************************************
  # Adds a dataset
  # *****************************************************************
  def Append_Data ( self, data ) :
    #v3print ( 'Hist PlotAppend_Data', len(data) )
    
    New_Points = False
    for i in range ( len ( data ) ) :
      #print ' VVV',self.new_N,len(data)
      if self.new_N == 0 :
        self.new_Min = data[i]
        self.new_Max = data[i]
      else :
        self.new_Min = min ( self.new_Min, data[i] )
        self.new_Max = max ( self.new_Max, data[i] )
      self.new_N += 1

      if self.new_N >= self.N_Average :
        New_Points = True
        self.Buf_wp = int(self.Buf_wp)
        self.Buf [ self.Buf_wp ] = self.new_Min
        self.Buf [ self.Buf_wp + 1] = self.new_Max
        self.Buf_wp += 2

        if self.Buf_wp == 4 * self.display_width :
          N = self.display_width

          # now compress the buffer twice and calculate new mean min/max
          self.mean_min = 0.0
          self.mean_max = 0.0
          for i in numpy.arange ( N ) :
            i = int(i)
            self.Buf [2*i]   = min ( self.Buf [4*i],  self.Buf [4*i+2] )
            self.Buf [2*i+1] = max ( self.Buf [4*i+1],self.Buf [4*i+3] )
            self.mean_min += self.Buf [2*i]
            self.mean_max += self.Buf [2*i+1]
          self.mean_min /= N
          self.mean_max /= N
          self.N_Average *= 2
          self.Buf_wp = 2 * N

          # do a complete Redraw
          self._Redraw_Screen ()
          New_Points = False
          
          # The first time we have to start drawinf after a few samples
        elif not ( self.hist_gain ) and ( self.Buf_wp > 40 ) :
          N = self.Buf_wp / 2
          self.mean_min = 0.0
          self.mean_max = 0.0
          for i in numpy.arange ( N ) :
            i = int(i)
            self.mean_min += self.Buf [2*i]
            self.mean_max += self.Buf [2*i+1]
          self.mean_min /= N
          self.mean_max /= N
          self._Redraw_Screen ()
          New_Points = False

        self.new_N = 0

    # Draw the newly added points
    if New_Points:
      self._Draw_Curves ()

  # *****************************************************************
  # *****************************************************************
  def _Redraw_Screen ( self ) :
    # The Buffer init is done here, to make sure the buffer is always
    # the same size as the Window
    self.Size  = self.GetClientSize()
    self.display_width = ( self.Size [0] // 2 ) -12

    # in the beginning, min and max are about equal to mean
    # so we've to center the signal close to the midscale
    # when compression is large enough
    # we move the signal between 20% and 80%
    if self.N_Average < 30 :
      alfa = 0.5 - 0.003 * (self.N_Average-1)
    else :
      alfa = 0.2
    h =  self.Size[1]

    # Make new offscreen bitmap: this bitmap will always have the
    # current drawing in it, so it can be used to save the image to
    # a file, or whatever.
    self._Buffer = wx.Bitmap ( *self.Size )
    try:
      x1 = self.mean_min
      y1 = (1-alfa) * h
      x2 = self.mean_max
      y2 = alfa * h
      if self.mean_min == self.mean_max :
        #self.hist_gain   = -1
        #self.hist_offset =  h / 2
        self.hist_gain   =  1
        self.hist_offset =  h / 2
        #v3print ( 'hist redraw-0' )
      else :
        #self.hist_gain   =   - (y2-y1)          / (x2-x1)
        #self.hist_offset = h - (x2*y1 - x1*y2 ) / (x2-x1)
        self.hist_gain   =  (y2-y1)          / (x2-x1)
        self.hist_offset =  (x2*y1 - x1*y2 ) / (x2-x1)
        #v3print ( 'hist redraw-1' )
    except:
      pass

    # remove measurement cursors
    self.old_Cursor = [ -1, -1 ]

    self._Draw_Curves ( True )
    # Refresh must be called to garantee a correct visible image
    self.Refresh()

  # *****************************************************************
  # Draws a chunk of newly received data to the display,
  # can also Redraw the complete signal, in case of resize or history drawing
  # *****************************************************************
  def _Draw_Curves ( self, Redraw = False ) :
    # Clipping doesn't make much sense !!
    dc = wx.BufferedDC ( wx.ClientDC ( self ), self._Buffer )

    if Redraw :
      # clear the canvas (pen must have same color as brush)
      dc.SetBrush ( self.Brush )
      dc.SetPen ( wx.Pen ( self.Brush.GetColour() ) )
      dc.DrawRectangle ( 0, 0, self.Size [0], self.Size [1] )
      #self.Pen = wx.Pen ( (0,0,0), 1, wx.SOLID )
      x1 = 0
    else :
      x1 = self.Buf_rp
      self.Buf_rp = self.Buf_wp - 1
    N = self.Buf_wp - x1

    #v3print ( 'Hist: Draw_Curves Redraw =', Redraw, x1, N,
    #          self.Buf_wp, self.Buf_rp )

    dc.SetPen ( self.Pen )
    if self.hist_gain :
      self.display_buffer [ x1 : x1+N, 1 ] = \
        self.hist_gain * self.Buf [ x1 : x1+N ] + self.hist_offset
      dc.DrawLines ( self.display_buffer [ x1 : x1+N ] )

    #dc.EndDrawing()

  # *****************************************************************
  # Draws a measurement cursor at position x,
  # a previous cursor is first removed.
  # Removing all cursors can be done by specifying a negative value for x
  # *****************************************************************
  def _Draw_Cursor ( self, C, x ) :
    dc = wx.BufferedDC ( wx.ClientDC ( self ), self._Buffer )
    dc.SetLogicalFunction ( wx.INVERT )
    dc.SetPen ( wx.Pen ( (0,0,0), 2, wx.SOLID ))
    if self.old_Cursor [C] >= 0 :
      dc.DrawLine ( self.old_Cursor[C], 0, self.old_Cursor[C], self.Size[1] )
    if x>= 0 : dc.DrawLine ( x, 0, x, self.Size[1] )
    #dc.EndDrawing()
    self.old_Cursor[C] = x

    # notify the Parent
    if self.CursorType > 0 :
      expansion = ( 2 ** ( self.CursorType-1 ) )
      delta = ( self.Size[0] - 1 ) / expansion
      self.My_Parent._On_History_Cursor_Selection (
        self.old_Cursor[0] * self.N_Average,
        delta )
    elif ( self.old_Cursor[0] >= 0 ) and \
         ( self.old_Cursor[1] >= 0 ) :
      x0 = self.old_Cursor[0]
      x1 = self.old_Cursor[1]
      if x0 > x1 :
        x = x0
        x0 = x1
        x1 = x
      delta = ( x1 - x0 ) * self.N_Average
      self.My_Parent._On_History_Cursor_Selection ( x0 * self.N_Average, delta )
    else :
      self.My_Parent._On_History_Cursor_Selection ( -1, 0 )

# ***********************************************************************
pd_Module ( __file__ )


