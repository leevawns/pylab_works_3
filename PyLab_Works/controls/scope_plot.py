import __init__

# ***********************************************************************
# ***********************************************************************
from   PyLab_Works_Globals import _
from   numpy import *
import wx
import wx.grid as gridlib
from   wx.lib.expando import ExpandoTextCtrl, EVT_ETC_LAYOUT_NEEDED
import time

from   inifile_support import *
from   utility_support import *
from   dialog_support  import *
from   grid_support    import *
from   menu_support    import *

ct_none     = 0
ct_checkbox = 1
ct_radio    = 2

XDIV = YDIV = 10
MAX_SCREEN_WIDTH = 1680  # 19" widescreen TFT
# ***********************************************************************

from control_scope_channel import _Channel
from scope_canvas_base import _PlotCanvas_Base


# ***********************************************************************
# ***********************************************************************
class _PlotCanvas ( _PlotCanvas_Base ) :
  def __init__(self, dock, parent, Real_Time = False ):
    _PlotCanvas_Base.__init__ ( self, dock, parent, Real_Time )
    #print 'REAL_TIME ??',Real_Time,self.Real_Time
    self.parent = parent

    # some initial values  SHOULD NOT BE HERE !!
    self.grid_x = 10;
    self.grid_y = 10;

    # *************************************************************
    # popup menus
    # *************************************************************
    pre = [
       _(0, 'Remove Cursors'    ),
       _(0, 'Memo Visible'      ),
       _(0, 'Move Memo Here'    ),
       _(0, 'Copy to Clipboard' ),
            '-',
       _(0, 'Linear Expansion'  ),
       _(0, 'Not Transparent'   ),
       _(0, 'Transparency 200'  ),
       _(0, 'Transparency 150'  ),
       _(0, 'Transparency 100'  ),
       _(0, 'Transparency 50'   ) ]
    self.Popup_Menu = My_Popup_Menu ( self._OnPopupItemSelected, None,
      pre =pre )
    self.Transparancy = 0

    # At this point we can do all actions that really draw !!
    # call OnSize, to make sure the dc-buffer is initialized.
    self.Set_Canvas ( self.BG_Color, self.Grid_Color )
    self._On_Size ( None )


  # *****************************************************************
  # *****************************************************************
  def _On_Show_Popup ( self, event ) :
    self.Popup_Menu.SetChecked ( 1, self.Memo_Extra )
    self.Popup_Menu.SetChecked ( 4, self.Linear_Interpolation )
    for i in range ( 5 ) :
      self.Popup_Menu.SetChecked ( 5 + i, self.Transparancy == i )

    self.Hit_Pos = self.ScreenToClient ( event.GetPosition () )
    self.PopupMenu ( self.Popup_Menu, pos = self.Hit_Pos )

  # *****************************************************************
  # *****************************************************************
  def _OnPopupItemSelected ( self, event ) :
    ID = event.Int

    if ID == 0 :
      self._Draw_Cursor ( 0, -1 )
      self._Draw_Cursor ( 1, -1 )

    elif ID == 1 :
      if not ( self.Memo_Extra ) :
        self.Memo_Extra = ExpandoTextCtrl (
          self, size=(100,-1), pos = self.Hit_Pos,
          value = self.Memo_Extra_Text )
      else :
        #print 'YTRFGJKOP',self.Hit_Pos,event.GetId(),self.Memo_Extra.GetId()
        self.Memo_Extra_Text = self.Memo_Extra.GetValue()
        self.Memo_Extra.Destroy ()
        self.Memo_Extra = None

    elif ID == 2 :
      if not ( self.Memo_Extra ) :
        self.Memo_Extra = ExpandoTextCtrl (
          self, size=(100,-1), pos = self.Hit_Pos,
          value = self.Memo_Extra_Text )
      else :
        self.Memo_Extra.SetPosition ( self.Hit_Pos )

    elif ID == 3 :
      import SendKeys
      SendKeys.SendKeys ( '%{PRTSC}' )

    elif ID == 4 :
      self.Linear_Interpolation = not ( self.Linear_Interpolation )
      self.Set_Data ( self.Data ) # _Redraw_Data ()
      #self._Redraw()

    elif ID in range ( 5, 10 ):
      self.Transparancy = ID - 5
      val = 5 + 50 * ( 5 - self.Transparancy )
      self.TopFrame.SetTransparent ( val )

  # *****************************************************************
  # Draw "LEFT" measurement cursor
  # *****************************************************************
  def _On_Mouse_Left ( self, event ) :
    x, y = event.GetPosition ()
    self._Draw_Cursor ( 0, x, y )

  # *****************************************************************
  # Dragging of the measurement cursors
  # *****************************************************************
  def _On_Mouse_Move ( self, event):
    if event.LeftIsDown ():
      self._On_Mouse_Left ( event )
    elif event.MiddleIsDown ():
      self._On_Mouse_Middle ( event )

  # *****************************************************************
  # Draw "RIGHT" measurement cursor
  # *****************************************************************
  def _On_Mouse_Middle ( self, event ) :
    x, y = event.GetPosition ()
    self._Draw_Cursor ( 1, x, y )

  # *****************************************************************
  # *****************************************************************
  def _On_Size( self, event ):
    for chan in range ( len ( self.gain ) ) :
      self._Correct_Gain ( chan )
    self._Redraw_Screen ()

  # *****************************************************************
  # adds a new signal-channel to the plot canvas
  # *****************************************************************
  def Add_Channel ( self ) :
    self.curves.append ( _Channel ( self.Buf_max ) )
    self.gain.append   (1)
    self.offset.append (0)
    self.cal1.append (None)
    self.cal2.append (None)
    self.name.append   ('Signal')

  # *****************************************************************
  # Convenience function that returns the number of displayed signals
  # *****************************************************************
  def Get_NCurve ( self ) :
    return len(self.curves)

  # *****************************************************************
  # Let the main program change one or more parameters of the _Channel
  # *****************************************************************
  def Set_Channel ( self, chan,
                          base_gain = 1.0,
                          base_offset = 0,
                          name = 'Signal',
                          cal1   = None,
                          cal2   = None,
                          delay  = None,
                          color  = None ) :
    # if curves don't exists here, create them
    while self.Get_NCurve() <= chan :
      self.Add_Channel()
    self.name   [chan] = name
    self.cal1   [chan] = cal1
    self.cal2   [chan] = cal2
    self.gain   [chan] = base_gain
    self.offset [chan] = base_offset
    self._Correct_Gain ( chan, delay, color )
    self._Redraw_Screen ()

  # *****************************************************************
  # Called by the timer, to refresh the label values,
  # and by measurement cursors
  # *****************************************************************
  def Get_DataSet ( self, from_end ) :
    #v3print ( 'Scope.Get_DataSet: self.curves =', self.curves )
    if not self.curves : return
    """
    self.old_Cursor = [ -1, -1 ]
    if self.oldx < 0 :
      # Display of realtime signals
      p = ( self.Buf_wp - 1 ) % self.Buf_max
    else:
      # display of measurement cursor
      p = self.Buf_rp - ( self.Dp - self.oldx ) % self.Size [0]
    """
    # Display of realtime signals
    if self.Real_Time :
      p = ( self.Buf_wp - 1 - from_end ) % self.Buf_max
    else :
      p = from_end
    data = []
    for chan, curve in enumerate ( self.curves ) :
      #v3print ( 'Scope.Get_DataSet: chan/ curve =', chan, curve )
      #data.append ( self.gain [ chan ] * curve.Buf [ p ] + \
      #              self.offset [ chan ])
      gain   = self.parent.Signal_Gain   [ chan ]
      if gain :
        offset = self.parent.Signal_Offset [ chan ]
        data.append ( gain * curve.Buf [ p ] + offset )
      else :
        data.append ( curve.Buf [ p ] )
    #v3print ( 'Data', data )
    return data

  # *****************************************************************
  # *****************************************************************
  def _Correct_Gain ( self, chan, delay = None, color = None ) :
    cal1 = self.cal1   [chan]
    cal2 = self.cal2   [chan]
    self.base_gain   = self.gain   [chan]
    self.base_offset = self.offset [chan]
    if (cal1 != None ) and ( cal2 != None ) and (cal1 != cal2):
      w1 = self.GetClientSize ()[1]
      w2 = 0
      gain2   = 1.0 * ( w2 - w1 )                / ( cal2 - cal1 )
      offset2 = 1.0 * ( cal2 * w1 - cal1 * w2  ) / ( cal2 - cal1 )
      gain    = gain2 * self.base_gain,
      offset  = gain2 * self.base_offset + offset2
    else :
      gain   = self.base_gain
      offset = self.base_offset
    self.curves [chan]._Set_Channel ( gain, offset, delay, color )

  # *****************************************************************
  # *****************************************************************
  def Set_Data ( self, data = None ) :
    """
    Sets all the data in none Real-Time mode.
    Is also called in Real-Time mode,
      on resize and history cursor movement.
      In that case data is None,
      because Real-Time data is stored in the curves themself,
      and this function should do nothing.
    """
    if data == None :
      if self.Real_Time :
        return
      try :
        a = self.Data
      except :
        return
    else :
      self.Data = data
    #v3print ( 'Normal Scope, set data', self.Data.shape )

    # M = the number of available channels
    # N = the number of samples in one channel
    M, N = self.Data.shape
    if N < 2 :
      return

    # if delivered number of signals too large,
    # create new channels
    Ncurves = len ( self.curves )
    if M > Ncurves : M = Ncurves
    #while len ( self.curves ) < M :
    #  self.Add_Channel ( )

    #print 'Set_Data',N, self.Size[0],self.curves
    if N >= self.Size[0] :
      N_Average = 1 + N / self.Size[0]
      MaxI = ( N / N_Average ) #* N_Average
      for i,curve in enumerate ( self.curves [ : M ] ) :
        for ii in range ( MaxI ):
          curve.Buf [ii] = 0
          for ai in range ( N_Average ):
            curve.Buf [ii] += self.Data [ i, ii*N_Average + ai ]
          curve.Buf [ii] /= N_Average
    else :
      N_Average = self.Size[0] / N
      MaxI = (N-1) * N_Average
      if self.Linear_Interpolation :
        N_Afloat = 1.0 * N_Average
        for i,curve in enumerate ( self.curves [ : M ] ) :
          # we don't use the last element
          for ii in range ( N-1 ):
            delta = ( self.Data [ i, ii + 1] - self.Data [ i, ii ] ) / N_Afloat
            for ai in range ( N_Average ):
              curve.Buf [ ii * N_Average + ai ] = \
                self.Data [ i, ii ] + ai * delta

      else :
        for i,curve in enumerate ( self.curves [ : M ] ) :
          for ii in range ( N ):
            for ai in range ( N_Average ):
              curve.Buf [ ii * N_Average + ai ] = self.Data [ i, ii ]

    # and draw it
    self.Dp = MaxI
    self._Redraw_Screen ()

  # *****************************************************************
  # Adds MANY dataset to the history buffer
  # data must be a 2-dimensional array
  # *****************************************************************
  def Append_Data ( self, data ) :
    #print 'HHH',type(data),data,data.shape,len ( self.curves )
    # M = the number of available channels
    # N = the number of samples in one channel
    #if data.ndim == 1 :
    #  M = 1
    #  N = data.shape[0]
    #else:
    M, N = data.shape
    if self.Buf_wp + N >= self.Buf_max :
      N1 = self.Buf_max - self.Buf_wp
      N2 = N - N1
    else :
      N1 = N
      N2 = 0

    # if delivered number of signals too large,
    # create new channels
    Ncurves = len ( self.curves )
    if M > Ncurves : M = Ncurves
    #while len ( self.curves ) < M :
    #  self.Add_Channel ( )

    #print N,N1,N2,M,self.Buf_wp,self.Buf_max
    # Here just process the number of available channels (M)
    for i,curve in enumerate ( self.curves [ : M ] ) :
      if len ( curve.Delayed ) > 0 :
        curve.Delayed = r_ [ curve.Delayed [N1:], data [i][:N1]]
        curve.Buf [ self.Buf_wp : self.Buf_wp + N1 ] = curve.Delayed [:N1]
      else :
        curve.Buf [ self.Buf_wp : self.Buf_wp + N1 ] = data [i][:N1]
      """
      if i == 0 :
        self.Delayed = r_ [ self.Delayed [N1:], data [i][:N1]]
        curve.Buf [ self.Buf_wp : self.Buf_wp + N1 ] = self.Delayed [:N1]
      else :
        curve.Buf [ self.Buf_wp : self.Buf_wp + N1 ] = data [i][:N1]
      """
      #print 'EEEEEEEERRRRREEEEOOOORRRR',len(curve.Buf[:N2]),N-N1,curve.Buf.shape,data.shape
      #print N2,self.Buf_max,curve.Buf.shape,curve.Buf [:N2].shape,data [i][ N1 : N ].shape
      curve.Buf [:N2] = data [i][ N1 : N ]

    self.Buf_wp += N
    self.Buf_wp %= self.Buf_max

    # *****************************************************************
    # notify the display update timer, that there's new data available
    # *****************************************************************
    ## self.My_Parent.New_Data = True
    self.Draw_Curves ()

  # *****************************************************************
  # Redraw the signals and the grid, when the window is resized
  # *****************************************************************
  def _Redraw_Screen ( self ) :
    # The Buffer init is done here, to make sure the buffer is always
    # the same size as the Window
    self.Size  = self.GetClientSize()
    #print '_Redraw_Screen, get size',self.Size
    if self.Size [0] * self.Size[1] <= 0 :
      return

    # Make new offscreen bitmap: this bitmap will always have the
    # current drawing in it, so it can be used to save the image to
    # a file, or whatever.
    self._Buffer = wx.Bitmap ( *self.Size )

    # remove measurement cursors (must be done before creating dc)
    #self._Draw_Cursor ( 0, -1 )
    #self._Draw_Cursor ( 1, -1 )
    # don't use _Draw_Cursor, because then a lot of flicker will result
    for C in [0,1] :
      if self.old_Cursor [C] >= 0 :
        self.old_CMemo [C].Destroy()
        self.old_CMemo [C] = None
        self.CMemo_Labels = [ [], [] ]
        self.old_Cursor [C] = -1

    dc = wx.BufferedDC ( wx.ClientDC ( self ), self._Buffer )
    dc.SetBrush ( self.Brush )

    # draw the grid
    self.grid_x = 1.0 * self.Size[0] / XDIV
    self.grid_y = 1.0 * self.Size[1] / YDIV
    self.erase_th = int ( 0.5 * self.grid_x )
    for xi in range ( XDIV ) :
      self._Draw_Grid_Block ( dc, xi )
      self.Erase_Block [xi] = False

    self.Draw_Curves ( True )
    #dc.EndDrawing()
    # Refresh must be called to garantee a correct visible image
    self.Refresh()

  # *****************************************************************
  # Draws a chunk of newly received data to the display,
  # can also Redraw the complete signal, in case of resize
  # *****************************************************************
  def Draw_Curves ( self, Redraw = False ) :
    #print 'Draw_Curves: Redraw, RealTime =', Redraw, self.Real_Time
    if not ( self.curves ) : return

    # Clipping doesn't make much sense !!
    dc = wx.BufferedDC ( wx.ClientDC ( self ), self._Buffer )
    dc.SetBrush ( self.Brush )

    # In case not realtime, simply draw from the start
    if not ( self.Real_Time ) :
      #print 'Block-1'
      N = self.Dp
      x11 = 0
      xbuf = 0
      for curve in self.curves :
        curve._Draw ( dc, N, x11, xbuf )
      return

    #if self.grid_x < 1 : return
    #print 'redraw,',Redraw
    if Redraw : # in case of a total redraw
      #print 'OOOO',self.Dp,self.grid_x, Redraw
      if self.grid_x < 1 : self.grid_x = 10

      x22 = self.Dp
      n = self.Dp % int ( self.grid_x )
      N = self.Size[0] - ( self.grid_x - n )
      if n > self.erase_th :
        N = N - self.grid_x
      # Be sure everything is integer !!
      N = int (N )
      x11 = ( x22 - N ) % self.Size [0]
      xbuf = ( self.Buf_rp - N ) % self.Buf_max
      #print 'Block-2',self.Dp,N,x11,x22,xbuf,self.Buf_wp,self.Buf_rp

    else: # in case of normal draw of small chunks
      x11 = self.Dp
      N =  ( self.Buf_wp - self.Buf_rp ) % self.Buf_max
      # Be sure everything is integer !!
      N = int ( N )
      x22 = ( x11 + N ) % self.Size [0]
      xbuf = self.Buf_rp
      #print 'Block-3',self.Dp,N,x11,x22,xbuf,self.Buf_wp,self.Buf_rp

    x1, x1r = divmod ( x11, int ( self.grid_x ) )
    x2, x2r = divmod ( x22, int ( self.grid_x ) )
    x1_next = ( x1 + 1 ) % XDIV
    if not ( self.Erase_Block [ x1_next ] ) and \
       ( ( x1r > self.erase_th ) or ( x2r > self.erase_th ) or ( x1 != x2 ) ) :
      self._Draw_Grid_Block ( dc, x1_next )

    # draw curves, here wrapping around display end is done,
    # curve._Draw does the wrapping around the history buffer
    if x11 <= x22 :
      for curve in self.curves :
        curve._Draw ( dc, N, x11, xbuf )
    else :
      for curve in self.curves :
        curve._Draw ( dc, self.Size [0] - x11, x11, xbuf )
        curve._Draw ( dc, x22, 0, (xbuf + self.Size[0] - x11) % self.Buf_max )

    if not ( Redraw ) :
      self.Buf_rp = ( self.Buf_wp - 1 ) % self.Buf_max
      self.Dp = ( self.Dp + N - 1 ) % self.Size [0]

    #dc.EndDrawing()

  # *****************************************************************
  # Draws a vertical grid block (and thereby erasing the signals)
  # over 1 X-division.
  # *****************************************************************
  def _Draw_Grid_Block ( self, dc, xi ):
    dc.SetPen ( wx.Pen ( self.Grid_Color, 1 ) )
    rectangles = []
    # we need to do this so complex to be sure the blocks will overlap
    # and thus getting a 1-width line !!
    xi = xi % XDIV
    x = int ( round ( xi * self.grid_x ) )
    w = int ( round ( ( xi + 1 ) * self.grid_x + 1 ) ) - x
    for i in range ( YDIV ) :
      y = int ( round (  i * self.grid_y ) )
      h = int ( round ( (  i + 1 ) * self.grid_y + 1 ) ) - y
      if y+h > self.Size[1]:
        h = self.Size[1]-y
      rectangles.append ( (x, y, w, h))

    dc.DrawRectangleList ( rectangles )
    self.Erase_Block [ xi ] = True
    self.Erase_Block [ (xi + 1 ) % XDIV ] = False

  # *****************************************************************
  # Draws a measurement cursor at position x,
  # a previous cursor is first removed.
  # Removing all cursors can be done by specifying a negative value for x
  # *****************************************************************
  def _Draw_Cursor ( self, C, x, y = None ) :
    dc = wx.BufferedDC ( wx.ClientDC ( self ), self._Buffer )
    #dc.SetLogicalFunction ( wx.XOR )
    dc.SetLogicalFunction ( wx.INVERT )
    dc.SetPen ( wx.Pen ( (0,0,0), 2, wx.SOLID ))
    #dc.SetPen ( wx.Pen ( (255,255,255), 2, wx.SOLID ))

    if self.old_Cursor [C] >= 0 :
      dc.DrawLine ( self.old_Cursor[C], 0, self.old_Cursor[C], self.Size[1] )

    if x >= 0 :
      dc.DrawLine ( x, 0, x, self.Size[1] )

      # calculate the position in the history array
      if self.Real_Time :
        from_end = self.Dp - x
        if x > self.Dp :
          from_end += self.Size[0]
      else :
        from_end = x
        if x >= self.Dp :
          from_end = self.Dp - 1
      data = self.Get_DataSet ( from_end )

      N = len ( self.curves )
      if not ( self.old_CMemo [C] ) :
        self.old_CMemo [C] = wx.Panel ( self )
        self.old_CMemo [C].SetBackgroundColour ( self.BG_Color )

        Sizer = wx.BoxSizer ( wx.VERTICAL )
        self.old_CMemo[C].SetSizer ( Sizer )
        for i in range ( N ) :
          label = wx.StaticText ( self.old_CMemo[C] )
          self.CMemo_Labels[C].append ( label )
          label.SetForegroundColour ( self.curves [i].Pen.GetColour() )
          Sizer.Add ( label, 0, wx.EXPAND )

        # now add 2 extra memos for samp and time measurement
        for i in range ( 2 ) :
          label = wx.StaticText ( self.old_CMemo[C] )
          self.CMemo_Labels[C].append ( label )
          label.SetForegroundColour ( wx.BLACK )
          Sizer.Add ( label, 0, wx.EXPAND )

      # now put in the actual measurement values
      # and determine the max width on the flight
      dc = wx.ScreenDC ()
      w = 0
      for chan in range ( N ) :
        value = self.gain [chan] * data [chan] + self.offset[chan]
        line = nice_number ( value )
        line = self.name[chan] + ' =' + line
        w = max ( w, dc.GetTextExtent (line )[0] )
        #v3print ( 'Label', chan, value, line, w )
        self.CMemo_Labels[C][chan].SetLabel ( line )

      # ***********************************************************
      # ***********************************************************
      # are there 2 cursors ?
      if   (C == 0) and self.old_CMemo[1]:
        x2 = self.old_Cursor[1]
      elif (C == 1) and self.old_CMemo[0]:
        x2 = self.old_Cursor[0]
      else :
        x2 = None

      delta = None

      # ***********************************************************
      # LEFT cursor is always absolute
      # ***********************************************************
      if C == 0 :
        line = 'Time =' + str ( 1.0 * x / 100 ) ;
        w = max ( w, dc.GetTextExtent (line )[0] )
        self.CMemo_Labels[C][N].SetLabel ( line )
        line = 'NSamp =' + str ( x )
        w = max ( w, dc.GetTextExtent (line )[0] )
        self.CMemo_Labels[C][N+1].SetLabel ( line )

        if x2 :  # if also RIGHT cursor available, adapt it
          dx = x2 - x
          delta = '-'
        else :
          delta = None

      # ***********************************************************
      # RIGHT cursor is absolute if there's no LEFT cursor
      # ***********************************************************
      else : # this is the RIGHT cursor
        if x2 :
          dx = x - x2
          delta = '-'
        else :  # if other cursor not available
          dx = x
          delta = ''

      if delta != None:
        line = delta + 'Time =' + str ( 1.0 * dx / 100 ) ;
        w = max ( w, dc.GetTextExtent (line )[0] )
        self.CMemo_Labels[1][N].SetLabel ( line )
        line = delta + 'NSamp =' + str ( dx )
        w = max ( w, dc.GetTextExtent (line )[0] )
        self.CMemo_Labels[1][N+1].SetLabel ( line )

      # Print mean and std over the selected period
      if x2 == None: x2 = 0
      if x > x2 :
        x1 = x2
        x2 = x
      else :
        x1 = x
      if ( x1 >= 0 ) :
        data = []
        for i in range ( x1, x2 ) :
          from_end = i
          if i >= self.Dp :
            from_end = self.Dp - 1
          data.append ( self.Get_DataSet ( from_end ) )
        data = asarray ( data ).astype ( int )
        import numpy
        print ( 'mean / std = ',
                  numpy.mean ( data, 0 ).round().astype ( int ),
                  numpy.std  ( data, 0 ).round().astype ( int ) )


      # ***********************************************************
      # draw the values on the left for the left cursor (if possible)
      # to the right for the right cursor
      # ***********************************************************
      if Platform_Windows :
        w -= 17
      if ( ( C == 0 ) and ( x > w ) ) or \
         ( ( C == 1 ) and ( (x+w) > self.Size[0] )) :
        self.old_CMemo[C].SetPosition ( ( x-w-2, y+5 ) )
      else :
        self.old_CMemo[C].SetPosition ( ( x+2, y+5 ) )
      self.old_CMemo[C].Refresh()
      #if x2:
      N += 2
      self.old_CMemo[C].SetSize ( ( w , N * 13 ) )
      #self.old_CMemo[C].SendSizeEvent ()

    # ***********************************************************
    # remove this cursor
    # ***********************************************************
    else:
      if self.old_CMemo [C]:
        self.old_CMemo [C].Destroy()
        self.old_CMemo [C] = None
        self.CMemo_Labels = [ [], [] ]

    #dc.EndDrawing()
    self.old_Cursor[C] = x
    self.Dock.SetFocus ()

# ***********************************************************************
pd_Module ( __file__ )
