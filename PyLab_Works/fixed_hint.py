# ***********************************************************************
# <Description>
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2008 <author>
# mailto: ...
# Please let me know if it works or not under different conditions
#
# <Version: x.y    ,dd-mm-yyyy, <author>
# Test Conditions: 1
#    - orginal release
#
# Test Conditions
# 1. WinXP-SP2, Python 2.4.3, wxPython wx-2.8-msw-ansi
# ***********************************************************************

import wx


# ***********************************************************************
# A simple form to test the control
# ***********************************************************************
class Fixed_Hint ( wx.MiniFrame ):
  def __init__ ( self, text='content', caption = ''):
    wx.MiniFrame.__init__(
      self, None, -1, caption,
      size = ( 200, 100 ),
      # simple but sizable and stay on top
      style = wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE )

    self.Text = wx.StaticText (self, -1, text )
    self.Text.SetBackgroundColour ( wx.Colour( 0xD3FBFB ) )

    Sizer = wx.BoxSizer ( wx.VERTICAL )
    Sizer.Add ( self.Text, 1, wx.EXPAND )
    self.SetSizer ( Sizer )

    self.Text.Bind ( wx.EVT_LEFT_DOWN,     self.OnLeftDown )
    self.Bind ( wx.EVT_LEFT_DOWN,     self.OnLeftDown )
    self.Bind ( wx.EVT_LEFT_UP,       self.OnLeftUp )
    self.Bind ( wx.EVT_MOTION,        self.OnMouseMove )
    self.Text.Bind ( wx.EVT_MIDDLE_UP,     self.OnExit )

    self.Text.SetToolTip ( "Middle-click to close the window" )

    self.delta = ( 0, 0 )

    self.Show ( True )

  def OnExit(self, evt):
    self.Close()

  def OnLeftDown(self, evt):
    self.CaptureMouse()
    x, y = self.ClientToScreen(evt.GetPosition())
    originx, originy = self.GetPosition()
    dx = x - originx
    dy = y - originy
    self.delta = ((dx, dy))

  def OnLeftUp(self, evt):
    if self.HasCapture():
      self.ReleaseMouse()

  def OnMouseMove(self, evt):
    if evt.Dragging() and evt.LeftIsDown():
      x, y = self.ClientToScreen(evt.GetPosition())
      fp = (x - self.delta[0], y - self.delta[1])
      self.Move(fp)
# ***********************************************************************


# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  app = wx.App ()
  text= "Multi-line wx.StaticTextadsldkasd asd ada dasl daksd asd as"  \
        "\nline 2\nline 3\n\nafter empty line"
  frame = Fixed_Hint ( text, 'Fixed Hint' )
  app.MainLoop ()
# ***********************************************************************

