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

# !!! import wx before any support library !!!
# otherwise the IDE won't do auto-suggest
import wx
from math import log10
from General_Globals import *

# ***********************************************************************
class Float_Slider ( wx.Panel ) :
  def __init__ ( self, parent,
                 id = -1,
                 caption = '',
                 log   = False,
                 format = '%1.0f',
                 value = None,
                 minValue = 1,
                 maxValue = 100,
                 pos = wx.DefaultPosition,
                 size = ( -1, 55 ), #wx.DefaultSize,
                 style = wx.SL_HORIZONTAL | wx.SL_TOP | wx.SL_TICKS,
                 validator = wx.DefaultValidator,
                 name = wx.SliderNameStr ) :

    # remember the extra settings
    self.My_Parent = parent
    self.Log = log
    if not ( format ) :
      format = '%1.0f'
    self.Format = format
    self.From_The_Outside = False

    self.Min = minValue
    self.Max = maxValue
    if log :
      # prevent math overflows in case of log
      if minValue <= 0 : minValue = 1
      if maxValue <= minValue : maxValue = minValue + 1
      # calculate some convenient variables
      self.Min = log10 ( minValue )
      self.Max = log10 ( maxValue )
    self.Gain = 100.0 / ( self.Max - self.Min )

    wx.Panel.__init__ ( self, parent,
                        pos = pos,
                        size = size )


    if log:
      caption += '  (log)'

    if caption :
      self.Caption = wx.StaticText ( self, -1, caption )
      self.yt = self.Caption.GetSize()[1]
    else :
      self.Caption = None
      self.yt = 0

    # determine the maximum size of min/max labels
    dc = wx.ScreenDC()
    smin = self.Format %(minValue)
    smax = self.Format %(maxValue)
    self.smax = dc.GetTextExtent(smax)[0]
    self.maxw = 10 + max (( dc.GetTextExtent(smin)[0], self.smax ))

    # create the labels and position them as far as it's meaningful
    self.minv = wx.StaticText ( self, -1, smin,
                                pos = ( 5, self.yt ))

    self.maxv = wx.StaticText ( self, -1, smax,
                                pos = ( 50, self.yt ),
                                style = wx.ALIGN_RIGHT )

    self.valv = wx.StaticText ( self, -1, '',
                                pos = ( 100, self.yt ))
    # Doesn't work well !!  style = wx.ALIGN_CENTER )

    # remove sider labels, if any, because we make them ourself
    if wx.SL_LABELS | style :
      style = style &  ( ~wx.SL_LABELS )

    # create the slider
    # ???? we've to use a weird y-position ????
    # define the slider range in percentage
    slider_min = 0
    slider_max = 100
    self.Slider = wx.Slider (
                       self, -1,
                       0, slider_min, slider_max,
                       pos = ( 0, self.yt + self.minv.GetSize()[1]),
                       size = ( size[0], -1 ) ,
                       style = style )

    if not ( value ) :
      value = ( self.Min + self.Max ) / 2.0
      if self.Log :
        value = 10 ** value
    self.Completion = None
    self.SetValue ( value )

    # define line and page size, otherwise weird mouse behaviour
    self.Slider.SetLineSize(1)
    self.Slider.SetPageSize(1)
    #self.Slider.SetTickFreq ( ( slider_max - slider_min ) / 10, 1 )
    self.Slider.SetTickFreq ( ( slider_max - slider_min ) / 10)

    self.Slider.Bind ( wx.EVT_SLIDER, self.OnSlider, self.Slider )

  # *************************************
  # *************************************
  def Set_Params ( self, caption, minValue, maxValue, Value,
                   LinLog, Format, Completion ) :
    self.Format = Format
    self.Completion = Completion
    log = LinLog.lower().startswith ( 'log' )
    if log:
      caption += '  (log)'
    self.Caption.SetLabel ( caption )

    self.Min = minValue
    self.Max = maxValue
    if log :
      # prevent math overflows in case of log
      if minValue <= 0 : minValue = 1
      if maxValue <= minValue : maxValue = minValue + 1
      # calculate some convenient variables
      self.Min = log10 ( minValue )
      self.Max = log10 ( maxValue )
    self.Gain = 100.0 / ( self.Max - self.Min )

    smin = self.Format % ( minValue )
    smax = self.Format % ( maxValue )
    self.minv.SetLabel ( smin )
    self.maxv.SetLabel ( smax )

    self.SetValue ( Value )

  # *************************************
  # *************************************
  def SetValue ( self, value ) :
    #if not ( value ) :
    #  return
    #Debug_From ( 2 )
    #print 'Float-Slider setvalue', value
    
    self.From_The_Outside = True

    if self.Log:
      log_value = log10 ( value )
      log_value = min ( log_value, self.Max )
      log_value = max ( log_value, self.Min )
      self.Slider.Value = int ( self.Gain * ( log_value - self.Min ) )
    else :
      value = min ( value, self.Max )
      value = max ( value, self.Min )
      self.Slider.Value = int ( self.Gain * ( value - self.Min ) )

    self.Display_Value ( value )

  # *************************************
  # handle the slider movement
  # *************************************
  def OnSlider ( self, event ) :
    if self.Log:
      value = self.Min + self.Slider.Value / self.Gain
      self.Display_Value ( 10 ** value )
    else :
      value = self.Min + self.Slider.Value / self.Gain
      self.Display_Value ( value )
    event.Skip ()

  # *************************************
  # *************************************
  def GetId ( self ) :
    # Return the slider's ID, so events can trigger on that
    return self.Slider.GetId ()

  # *************************************
  # performs the formatting of the value label
  # *************************************
  def Display_Value ( self, value ) :
    a = self.Format % ( value )
    self.valv.SetLabel ( a )

    if not ( self.From_The_Outside ) and self.Completion :
      self.Completion ( value )

    self.From_The_Outside = False

  # *************************************
  # Return the ID of the slider to the parent
  # *************************************
  def Get_ID ( self ):
    return self.Slider.GetId()

  # *************************************
  # *************************************
  def GetSize ( self ) :
    return ( 100, 60 )

  # *************************************
  # Set the text colors of all text attributes
  # *************************************
  def SetForegroundColour ( self, color ) :
    if self.Caption :
      self.Caption.SetForegroundColour ( color )
    self.minv.SetForegroundColour      ( color )
    self.valv.SetForegroundColour      ( color )
    self.maxv.SetForegroundColour      ( color )

  # *************************************
  # *************************************
  def SetSize ( self, Size ) :
    wx.Panel.SetSize ( self, Size )
    wx.CallAfter ( self._Scale_Components, Size )

  # *************************************
  # *************************************
  def _Scale_Components ( self, Size ) :
    if self.Caption :
      self.Caption.SetPosition ( ( 5, 0 ) )

    w = Size [0]
    self.Slider.SetSize     ( ( w, -1 ) )
    self.Slider.SetPosition ( ( 0, -1 ) )
    self.minv.SetPosition   ( ( 5, -1 ) )

    self.valv.SetSize       ( ( 50      , -1 ) )
    self.valv.SetPosition   ( ( w/2 - 25, -1 ) )

    self.maxv.SetPosition   ( ( w - self.smax, -1 ) )
    self.Refresh ()

  # *************************************
  # *************************************
  def GetValue ( self ) :
    if self.Log :
      value = self.Min + self.Slider.Value / self.Gain
      return 10**value
    else :
      value = self.Min + self.Slider.Value / self.Gain
      return value
# ***********************************************************************


# ***********************************************************************
# A simple form to test the control
# ***********************************************************************
class Simple_Test_Form ( wx.MiniFrame ):
  def __init__ ( self, ini = None ):
    wx.MiniFrame.__init__(
      self, None, -1, 'Demo Float / Log  - Slider',
      style = wx.DEFAULT_FRAME_STYLE )

    Panel = wx.Panel ( self )
    self.Panel_Left = wx.Panel ( Panel )
    #self.Panel_Right = wx.Panel ( Panel )
    self.Panel_Right = wx.ScrolledWindow ( Panel, style=wx.VSCROLL ) # wx.Panel ( Panel )

    self.Slider = Float_Slider ( self.Panel_Right,
                               caption = 'Frequency',
                               minValue = 1,
                               maxValue = 1000,
                               log = True )
    self.Slider.SetForegroundColour ( wx.BLUE )

    self.Slider2 = Float_Slider ( self.Panel_Right,
                               caption = 'Slider-2',
                               minValue = 1,
                               maxValue = 10,
                               format   = '%3.1f',
                               pos      = ( 0, 100 ) )

    Button = wx.Button ( self.Panel_Left, -1, "Start",
                         pos = ( 0, 0 ),
                         ) #size = (-1, 50) )
    Button.Bind ( wx.EVT_BUTTON, self.OnButton )
    self.Slider.Bind ( wx.EVT_SLIDER, self.OnSlider, self.Slider )

    """
    Sizer = wx.BoxSizer ( wx.VERTICAL )
    Sizer.Add ( self.Slider, 0, wx.EXPAND )
    Sizer.Add ( self.Slider2, 0 , wx.EXPAND )
    Sizer.Add ( Button, 0, wx.EXPAND )
    Panel.SetSizer ( Sizer )
    self.S_Buttons = wx.BoxSizer ( wx.VERTICAL )
    self.S_Buttons.Add ( Button, 0, wx.EXPAND )
    self.Panel_Left.SetSizer ( self.S_Buttons )

    self.S_Sliders = wx.BoxSizer ( wx.VERTICAL )
    self.S_Sliders.Add ( self.Slider, 0, wx.EXPAND )
    self.S_Sliders.Add ( self.Slider2, 0, wx.EXPAND )
    self.Panel_Right.SetSizer ( self.S_Sliders )
    """

    Sizer = wx.BoxSizer ( wx.HORIZONTAL )
    Sizer.Add ( self.Panel_Left, 0, wx.EXPAND )
    Sizer.Add ( self.Panel_Right, 1, wx.EXPAND )
    Panel.SetSizer ( Sizer )

    self.Panel_Right.SetScrollbars(1,1,10,600)
    #self.Panel_Right.SetVirtualSize ( ( -1, 600 ) )
    self.Panel_Right.Bind ( wx.EVT_SIZE,   self._On_Size )

  def _On_Size ( self, event = None ) :
    w = event.GetSize()[0] - 15
    self.Slider.SetSize  ( ( w, -1 ) )
    self.Slider2.SetSize ( ( w, -1 ) )

  def OnButton ( self, event ) :
    self.Slider.SetValue ( 100 )
    self.Slider2.SetValue ( 20 )

    self.Slider.Set_Params ( 'AAP', 3, 3000, 300, 'Log', '%5.2f', None )
    self.Slider2.Set_Params ( 'VB', 0, 20, 12, 'Lin', '%5.1f', None )

  def OnSlider ( self, event ) :
    x=self.Slider.GetValue()
    print ('Slider %3.2f' % (x))
    x=self.Slider2.GetValue()
    print ('Slider %3.2f' % (x))
    event.Skip ()
# ***********************************************************************


# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  app = wx.PySimpleApp ()
  frame = Simple_Test_Form ()
  frame.Show ( True )
  app.MainLoop ()
# ***********************************************************************

