import __init__
# ***********************************************************************
# A more windows friendly inifile handler
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007 Stef Mientki
# mailto:S.Mientki@ru.nl
# Please let me know if it works or not under different conditions
#
# <Version: 1.0    ,28-12-2007, Stef Mientki
# Test Conditions: 1
#    - orginal release
#
# Test Conditions
# 1. WinXP-SP2, Python 2.4.3, wxPython wx-2.8-msw-ansi
# ***********************************************************************


from dialog_support import *
from inifile_support import *

import wx

from numpy import arange, ndarray, sin, cos, pi
# KAN NIET MET PY2EXE: from pylab import *

# WXAgg is much faster and more beautiful (aliasing) than WX !!
#matplotlib.use('WX')
#from matplotlib.backends.backend_wx import FigureCanvasWx as FigureCanvas
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from matplotlib.figure import Figure
from matplotlib import rcParams


# ***********************************************************************
# ***********************************************************************
class MatPlot_Simple ( wx.MiniFrame ): #Frame):

  def __init__ ( self, parent,
                 title = '',
                 size = ( 500, 300 ) ,
                 pos = ( 150, 150 ),
                 ini = None ):
    FormStyle = wx.DEFAULT_FRAME_STYLE | \
                wx.TINY_CAPTION_HORIZ
                #wx.STAY_ON_TOP
    self.parent = parent
    self.Ini = ini
    if self.parent:
      FormStyle = FormStyle | wx.FRAME_FLOAT_ON_PARENT    # needs a parent

    if not ( self.parent ) and self.Ini :
      ini.Section = 'MatPlot_Simple'
      pos = ini.Read ( 'Pos' , pos )
      size = ini.Read ( 'Size' , size )

      line = ini.Read ( 'xxx', '' )
      line = eval ( '['+line+']' )
      self.MatPlot_Simple_Load ( line )
    else :
      rcParams [ 'grid.color' ]    = '0.4'

    self.legends = ('aap','beer')
    self.Pseudo_Color = False


    wx.MiniFrame.__init__(
      self, parent, -1, title,
      size = size,
      pos = pos,
      style = FormStyle
      )



    # EASIER to set these parameters from rcParams, than from rc,
    # because you can use deep nested properties
    #from pylab import rc
    #rc ('figure.subplot', 'left' = 0.5)  ## not accepted

    rcParams [ 'figure.subplot.top' ]    = 0.95
    rcParams [ 'figure.subplot.bottom' ] = 0.05
    rcParams [ 'figure.subplot.left' ]   = 0.07
    rcParams [ 'figure.subplot.right' ]  = 0.97

    # *************************************************************
    # Create the panel with the plot controls
    # *************************************************************
    self.Panel = wx.Panel ( self, size=(100,50))
    self.CB_Grid = wx.CheckBox ( self.Panel, -1, "-Grid-", pos = (0, 5) )
    self.CB_Grid.SetValue ( self.Initial_Grid )
    self.CP_Grid = wx.ColourPickerCtrl ( self.Panel, -1,
                                         self.MatPlot_2_Color (rcParams ['grid.color'] ),
                                         pos = (50,1) )
    wx.StaticText ( self.Panel, -1, "BackGround-", pos = (90,5) )
    self.CP_BG = wx.ColourPickerCtrl ( self.Panel, -1,
                                       self.MatPlot_2_Color (self.BG_color),
                                       pos = (155,1) )
    # no support for Axis
    self.CB_Axis = wx.CheckBox ( self.Panel, -1, "-Axis", pos = (195,5) )
    self.CB_Axis.SetValue ( self.Initial_Axis )
    self.CB_Legend = wx.CheckBox ( self.Panel, -1, "-Legend", pos = (250,5) )
    self.CB_Legend.SetValue ( self.Initial_Legend )
    self.CB_Polar = wx.CheckBox ( self.Panel, -1, "-Low Res", pos = (315,5) )
    self.CB_Polar.SetValue ( self.Initial_Polar )

    bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_BUTTON, (16,16))
    self.Button_Image = wx.BitmapButton ( self.Panel, -1 , bmp, pos = (385,0) )
    self.Button_Image.SetToolTipString ( 'Save as PNG-image')

    if not ( self.parent ) :
      self.Spin = wx.SpinCtrl ( self.Panel, wx.ID_ANY,
                                min=1, max=5, initial = self.Initial_Spin,
                                pos=(415,2), size =(40,20) )
      self.Spin.SetToolTipString ( 'Select Demo')

    # background color of the not used part of the button bar
    self.SetBackgroundColour ( self.Panel.GetBackgroundColour() )
    # *************************************************************

    # *************************************************************
    # *************************************************************
    self.figure = Figure()
    self.Canvas = FigureCanvas ( self, -1, self.figure )
    self.axes = self.figure.add_subplot ( 111 )
    self.lx = None

    if not ( self.parent ) :
      self.MatPlot_Example ( self.Initial_Spin )
    else :
      self.Set_Figure_Pars ()
    # *************************************************************

    # *************************************************************
    # *************************************************************
    self.sizer = wx.BoxSizer ( wx.VERTICAL )
    self.sizer.Add ( self.Canvas, 1, wx.EXPAND )
    self.sizer.Add ( self.Panel, 0 )
    self.SetSizer ( self.sizer )
    #self.Fit()
    # *************************************************************

    # *************************************************************
    # *************************************************************
    self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnGridColor, self.CP_Grid)
    self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnBGColor, self.CP_BG)
    self.Bind(wx.EVT_CHECKBOX, self.OnSetGrid, self.CB_Grid)
    self.Bind(wx.EVT_CHECKBOX, self.OnSetAxis, self.CB_Axis)
    self.Bind(wx.EVT_CHECKBOX, self.OnSetLegend, self.CB_Legend)
    self.Bind(wx.EVT_CHECKBOX, self.OnPolar, self.CB_Polar)
    self.Button_Image.Bind ( wx.EVT_BUTTON, self.OnSaveImage, self.Button_Image )
    if not ( self.parent ) :
      self.Spin.Bind ( wx.EVT_SPINCTRL, self.OnSpinEvent, self.Spin )
      self.Bind ( wx.EVT_CLOSE, self.OnClose )

    #if not ( self.connect ) :
    self.connect = self.Canvas.mpl_connect ( 'motion_notify_event', self.on_move )
    # *************************************************************


  # *************************************************************
  # *************************************************************
  def on_move ( self, event ) :
    if self.CB_Polar.GetValue () and not (self.Pseudo_Color ): return
  
    x, y = event.x, event.y
    if event.inaxes :
      ax = event.inaxes
      minx, maxx = ax.get_xlim ()
      miny, maxy = ax.get_ylim ()
      x, y = event.xdata, event.ydata

      if not ( self.lx ) :
        self.lx, = self.axes.plot ( ( minx, maxx ), ( y, y ), 'k-' )  # the horiz line
        self.ly, = self.axes.plot ( ( x, x ), ( miny, maxy ), 'k-' )  # the vert line
        self.meas_txt = self.axes.text ( 0.02, 0.02, '',
                                         transform = self.axes.transAxes )

      # update the crosshair positions
      self.lx.set_data ( ( minx, maxx ), ( y, y ) )
      self.ly.set_data ( ( x, x ), ( miny, maxy ) )
      self.meas_txt.set_text ( 'x=%1.2f, y=%1.2f'% ( x, y ) )

    else :
      # Hide the cross hair
      if self.lx :
        self.lx.set_data ( ( x, x ), ( y, y ) )
        self.ly.set_data ( ( x, x ), ( y, y ) )
        self.meas_txt.set_text ( '' )

    self.Canvas.draw ()

  # *************************************************************
  # *************************************************************
  def OnSpinEvent ( self, event ) :
    Example = event.GetInt()
    self.MatPlot_Example ( Example )
    
  # *************************************************************
  # create an example image
  # *************************************************************
  def MatPlot_Example ( self, Example ) :
    self.Signals = []
    if Example == 1 :  # Sine
      x = arange ( 0.0, 3.0, 0.01 )
      y = sin ( 2 * pi * x )

    elif Example == 2 : # SPIRAL
      t = arange ( 0, 10 * pi, 0.1 )
      x = t * sin ( t )
      y = t * cos ( t )

    elif Example == 3 : # CARDIOID
      t = arange ( 0, 2 * pi, 0.1 )
      x = (1 + cos(t) ) * cos (t)
      y = (1 + cos(t) ) * sin (t)

    elif Example == 4 : # SPIROGRAPH
      phi = linspace ( 0, 4, 100 )
      #r=sin(phi*pi) #
      r = sin ( cos ( tan ( phi ) ) )
      x = phi
      y = 20 * r

    elif Example == 5 : # Pseudo Color
      def func3(x,y):
        return (1- x/2 + x**5 + y**3)*exp(-x**2-y**2)
      dx, dy = 0.05, 0.05
      x = arange(-3.0, 3.0, dx)
      y = arange(-3.0, 3.0, dy)
      X,Y = meshgrid(x, y)
      self.Signals.append ( func3 ( X, Y ) )

    if self.Signals == [] :
      self.Signals.append ( x )
      self.Signals.append ( y )

    # *************************************************************
    # *************************************************************
    self.Pseudo_Color = False
    if len ( self.Signals ) == 1 :
      if isinstance ( self.Signals[0], ndarray ) :
        if ( len ( self.Signals[0].shape ) == 2 ) and \
           ( self.Signals[0].shape[1] > 10 ) :
           self.Pseudo_Color = True
    self.ReCreate_Plot ()

  # *************************************************************
  # MatPlot accepts RGB colors in relative range 0..1,
  # alpha blend is also not accepted
  # *************************************************************
  def Color_2_MatPlot ( self, color ) :
    # if already in MatPlot format, just return the same value
    if isinstance (color, float) or isinstance ( color[0], float ) :
      return color
    # else limit to 3 elements in the range 0.0 ... 1.0
    kleur = []
    for c in  color[:3] :
      kleur.append ( c / 255.0 )
    return kleur


  # *************************************************************
  # MatPlot accepts RGB colors in relative range 0..1,
  # alpha blend is also not accepted
  # *************************************************************
  def MatPlot_2_Color ( self, color ) :
    # if already in normal format, just return the same value
    if isinstance ( color, wx.Color ) :
      return color

    if isinstance ( color, basestring ) :
      try:
        color = float ( color )
      except :
        return color   # named color probably
    if isinstance ( color, float ):
      i = int ( color * 255 )
      kleur = [ i, i, i ]
    else :
      kleur = []
      if isinstance ( color[0], float ) :
        for c in  color[:3] :
          kleur.append  ( int ( 255 * c ) )
      else:
        kleur = color[:3]
    kleur = wx.Color ( *kleur )
    return kleur


  # *************************************************************
  # *************************************************************
  def Set_Figure_Pars ( self ) :
    color = self.BG_color
    if color :
      #if not ( isinstance ( color, wx.Color ) ) and \
      #   not ( isinstance ( color , list ) ) : color = wx.NamedColor ( color )
      color = self.Color_2_MatPlot ( color )
      self.BG_color = color
      self.axes.set_axis_bgcolor ( color )
      self.figure.set_facecolor  ( color )
      self.figure.set_edgecolor  ( color )

      self.axes.grid ( self.CB_Grid.GetValue () )
      if self.CB_Axis.GetValue () :
        self.axes.set_axis_on ()
      else :
        self.axes.set_axis_off ()

      # Polar doesn't support legend (use figlegend)
      if self.Pseudo_Color or not ( self.CB_Polar.GetValue () ) :
        if self.CB_Legend.GetValue () :
          self.axes.legend ( self.legends )
        else :
          self.axes.legend_ = None

      self.Canvas.draw ()

  # *************************************************************
  # Set Grid color of all backgrounds
  # *************************************************************
  def OnGridColor ( self, event ) :
    rcParams [ 'grid.color' ] = self.Color_2_MatPlot ( self.CP_Grid.GetColour () )

    # Because we need to reload the resources,
    # we force it by recreating to the total plot
    self.sizer.Remove(self.Canvas)
    self.figure = Figure()
    self.Canvas = FigureCanvas ( self, -1, self.figure )
    self.axes = self.figure.add_subplot ( 111 )
    self.lx = None
    self.sizer.Prepend ( self.Canvas, 1, wx.EXPAND )
    self.sizer.Layout ()
    self.ReCreate_Plot
    self.MatPlot_Example ( self.Spin.GetValue () )

  # *************************************************************
  # Set Background color of all backgrounds
  # *************************************************************
  def OnBGColor ( self, event ) :
    self.BG_color = self.CP_BG.GetColour ()
    self.Set_Figure_Pars ()

  # *************************************************************
  # *************************************************************
  def OnSetAxis ( self, event ) :
    self.Set_Figure_Pars ()


  # *************************************************************
  # *************************************************************
  def ReCreate_Plot ( self ):
    # BUG, "hold" doesn't work in polar, therefore create a new figure
    self.figure.clear()
    self.lx = None

    if not ( self.Pseudo_Color ) :
      self.CB_Polar.SetLabel ('-Polar')
      self.axes = self.figure.add_subplot ( 111, polar = self.CB_Polar.GetValue () )
      self.axes.hold ( True )   # needed for measurement cursor
      self.axes.plot ( self.Signals[0], self.Signals[1],  )

    else :  # Pseudo color
      self.CB_Polar.SetLabel ('-Low Res')
      self.axes = self.figure.add_subplot ( 111 )

      if self.CB_Polar.GetValue() :
        cmap = cm.get_cmap('jet', 10)    # 10 discrete colors
      else :
        cmap = cm.jet
      #cmap = cm.gray
      im = self.axes.imshow ( self.Signals[0] , cmap=cmap )

      #im.set_interpolation('nearest')
      #im.set_interpolation('bicubic')
      im.set_interpolation('bilinear')
      self.figure.colorbar ( im )

    self.Set_Figure_Pars ()


  # *************************************************************
  # *************************************************************
  def OnPolar ( self, event ) :
    self.ReCreate_Plot ()

  # *************************************************************
  # *************************************************************
  def OnSaveImage ( self, event ) :
    file = Ask_File_For_Save ( os.getcwd(),
                               FileTypes = '*.png',
                               Title = 'Save Plot as PNG-image' )
    if file :
      self.figure.savefig ( file )

  # *************************************************************
  # *************************************************************
  def OnSetLegend ( self, value) :
    self.Set_Figure_Pars ()

  # *************************************************************
  # *************************************************************
  def OnSetGrid ( self, event ) :
    self.Set_Figure_Pars ()

  # *************************************************************
  # *************************************************************
  def OnClose ( self, event ) :
    if self.Ini :
      self.Ini.Section = 'MatPlot_Simple'
      self.Ini.Write ( 'Pos', self.GetPosition() )
      self.Ini.Write ( 'Size', self.GetSize() )
      self.Ini.Write ( 'xxx', self.MatPlot_Simple_Save() )
    event.Skip()

  # *************************************************************
  # *************************************************************
  def MatPlot_Simple_Save ( self ) :
    line = []
    line.append ( self.BG_color )
    print 'GC',rcParams [ 'grid.color' ]
    line.append ( rcParams [ 'grid.color' ] )

    line.append ( self.CB_Grid.GetValue () )
    line.append ( self.CB_Axis.GetValue () )
    line.append ( self.CB_Legend.GetValue () )
    line.append ( self.CB_Polar.GetValue () )
    if not ( self.parent ):
      line.append ( self.Spin.GetValue() )
    return line

  # *************************************************************
  # *************************************************************
  def MatPlot_Simple_Load ( self, line ) :
    self.BG_color = line [0]
    xx = self.MatPlot_2_Color ( self.BG_color )
    rcParams [ 'grid.color' ] = self.Color_2_MatPlot ( line [1] )
    self.Initial_Grid   = line [2]
    self.Initial_Axis   = line [3]
    self.Initial_Legend = line [4]
    self.Initial_Polar = line [5]
    if not ( self.parent ):
      self.Initial_Spin = line [6]
    else :
      self.Initial_Spin = 1
# ***********************************************************************


# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  app = wx.PySimpleApp ()
  ini = inifile ( 'test_matplot.cfg' )
  frame = MatPlot_Simple ( None , ini = ini)
  frame.Show ( True )
  app.MainLoop ()
  ini.Close ()
# ***********************************************************************

