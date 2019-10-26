import __init__

# ***********************************************************************
# ***********************************************************************
from   PyLab_Works_Globals import _
from   numpy import *
import wx
import wx.grid as gridlib
from   wx.lib.expando import ExpandoTextCtrl, EVT_ETC_LAYOUT_NEEDED
import time

# add some standard library paths
"""
import os
import sys
subdirs = [ '../support' ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
"""
from   inifile_support import *
from   utility_support import *
from   dialog_support  import *
from   grid_support    import *

ct_none     = 0
ct_checkbox = 1
ct_radio    = 2

XDIV = YDIV = 10
MAX_SCREEN_WIDTH = 1680  # 19" widescreen TFT
# ***********************************************************************




# ***********************************************************************
# Class defining 1 signal-channel, this class has history buffer
# ***********************************************************************
class _Channel ( object ) :

  def __init__( self, Buf_max ) :
    # create display buffer and define in it the X-coordinates
    self.display_buffer = zeros ( [ MAX_SCREEN_WIDTH, 2 ] )
    self.display_buffer [ : , 0 ] = array ( range ( MAX_SCREEN_WIDTH ) )
    self.Buf_Len = self.Buf_max = Buf_max

    # define raw data buffer, also used for history, so make it >= display buffer
    self.Buf = zeros ( [ self.Buf_Len ] )
    # and a special delay buffer
    self.Delayed = zeros (0)

    self._Set_Channel ( color = 'red' )
    self.tot_gain   = 1
    self.tot_offset = 0

  # *****************************************************************
  # Let the main program change one or more parameters of the _Channel
  # *****************************************************************
  def _Set_Channel ( self, gain   = None,
                           offset = None,
                           delay  = None,
                           color  = None ) :
    if gain :
      self.tot_gain = gain
    if offset :
      self.tot_offset = offset
    if delay :
      self.Delayed = zeros ( delay )
    if color :
      #v3print ( '**** STE CHANNEL', color )
      if not isinstance ( color, wx.Colour ) : color = wx.Colour( color )
      #v3print ( '**** STE CHANNEL', color )
      self.Pen = wx.Pen ( color, 1, wx.SOLID )

  # *****************************************************************
  # draw 1 curve, here wrapping around history buffer is done,
  # The calling function performs the wrapping around the display edge
  # *****************************************************************
  def _Draw ( self, dc, N, x1, xbuf ):
    dc.SetPen ( self.Pen )
    if ( xbuf + N ) >= self.Buf_max :
      N1 = self.Buf_max - xbuf
      self.display_buffer [ x1 : x1+N1, 1 ] = \
        self.tot_gain * self.Buf [ xbuf : xbuf+N1 ] + self.tot_offset
      self.display_buffer [ x1+N1 : x1+N, 1 ] = \
        self.tot_gain * self.Buf [ 0 : N-N1 ] + self.tot_offset
    else:
      self.display_buffer [ x1:x1+N, 1 ] = \
        self.tot_gain * self.Buf[ xbuf : xbuf+N ] + self.tot_offset
    dc.DrawLines ( self.display_buffer [ x1:x1+N ] )
# ***********************************************************************
