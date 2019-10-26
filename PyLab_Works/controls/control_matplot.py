import __init__
from base_control import *

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

import operator

# !!! import wx before any support library !!!
# otherwise the IDE won't do auto-suggest
import wx

from dialog_support import *
from inifile_support import *

from numpy import arange, ndarray, sin, cos, tan, pi, linspace , exp, meshgrid

# WXAgg is much faster and more beautiful (aliasing) than WX !!
# BUT WXAgg is no longer supported under wxPython 2.8 !!
# PYLAB can not be used in combination with PY2EXE !!
# so we do all imports manually
import matplotlib
matplotlib.use('WXAgg')
#from matplotlib.backends.backend_wxagg import Toolbar,  FigureManager
from matplotlib.backends.backend_wxagg import FigureManager
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib import rcParams, mlab, cm
#from matplotlib.mlab   import meshgrid
from matplotlib.figure import Figure
from matplotlib.axes   import Subplot



# ***********************************************************************
# ***********************************************************************
class t_C_MatPlot ( My_Control_Class ):
  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    # *************************************************************
    # Create the panel with the plot controls
    # *************************************************************
    self.Panel = wx.Panel ( self.Dock )
    self.CB_Grid = wx.CheckBox ( self.Panel, -1, "Grid", pos = ( 0, 5 ) )
    self.CP_Grid = wx.ColourPickerCtrl ( self.Panel, -1,
                                         pos = ( 40, 1 ) )
    wx.StaticText ( self.Panel, -1, "BackGround-", pos = ( 70, 5 ) )
    self.CP_BG = wx.ColourPickerCtrl ( self.Panel, -1,
                                       pos = ( 130, 1 ) )
    self.CB_Axis   = wx.CheckBox ( self.Panel, -1, "Axis",    pos = ( 160, 5 ) )
    self.CB_Legend = wx.CheckBox ( self.Panel, -1, "Legend",  pos = ( 210, 5 ) )
    self.CB_Polar  = wx.CheckBox ( self.Panel, -1, "Low Res", pos = ( 275, 5 ) )
    self.CB_FFT    = wx.CheckBox ( self.Panel, -1, "FFT",     pos = ( 335, 5 ) )

    bmp = wx.ArtProvider.GetBitmap( wx.ART_COPY, wx.ART_BUTTON, ( 16, 16 ))
    self.Button_ClipBoard = wx.BitmapButton ( self.Panel, -1 , bmp, pos = (375, 0) )
    self.Button_ClipBoard.SetToolTipString ( 'Copy to ClipBoard')

    bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_BUTTON, ( 16, 16 ))
    self.Button_Image = wx.BitmapButton ( self.Panel, -1 , bmp, pos = (405, 0) )
    self.Button_Image.SetToolTipString ( 'Save as PNG-image')

    if self.Test :
      self.Spin = wx.SpinCtrl ( self.Panel, wx.ID_ANY,
                                min = 1, max = 5,
                                pos = ( 435, 2 ), size = ( 40, 20 ) )
      self.Spin.SetToolTipString ( 'Select Demo' )

    # background color of the not used part of the button bar
    self.Dock.SetBackgroundColour ( self.Panel.GetBackgroundColour() )
    # *************************************************************

    # *************************************************************
    # *************************************************************
    # These parameters must be set before the figure is created
    # EASIER to set these parameters from rcParams, than from rc,
    # because you can use deep nested properties
    #rc ('figure.subplot', 'left' = 0.5)  ## not accepted
    rcParams [ 'figure.subplot.top'    ] = 0.95
    rcParams [ 'figure.subplot.bottom' ] = 0.05
    rcParams [ 'figure.subplot.left'   ] = 0.1
    rcParams [ 'figure.subplot.right'  ] = 0.97

    self.figure = Figure()
    self.Canvas = FigureCanvas ( self.Dock, -1, self.figure )
    self.axes = self.figure.add_subplot ( 111 )
    self.axes_2 = None
    self.lx = None
    # *************************************************************


    # *************************************************************
    # Try to reload the settings, otherwise set defaults
    # *************************************************************
    self.Legends = ('signal 1','signal 2')
    self.SignalsX = []
    self.SignalsY = []
    self.Pseudo_Color = False
    if self.Test and self.Ini :
      print ('piep1')
      self.Ini.Section = 'MatPlot'
      #line = self.Ini.Read ( 'Pars', '' )
      self.Load_Settings ( self.Ini )

    if self.Test :
      self.MatPlot_Example ( self.Spin.GetValue () )
    else :
      self.MatPlot_Redraw ()
    # *************************************************************


    # *************************************************************
    # *************************************************************
    Sizer = wx.BoxSizer ( wx.VERTICAL )
    Sizer.Add ( self.Canvas, 1, wx.EXPAND )
    Sizer.Add ( self.Panel, 0 )
    self.Dock.SetSizer ( Sizer )
    #Dock.Fit()
    
    # We need this for Ubuntu, and even then it works limited
    self.Dock.Bind ( wx.EVT_SIZE, self._OnSize )
    # *************************************************************

    # *************************************************************
    # *************************************************************
    self.Dock.Bind ( wx.EVT_COLOURPICKER_CHANGED, self.MatPlot_OnPolar, self.CP_Grid )
    self.Dock.Bind ( wx.EVT_COLOURPICKER_CHANGED, self.MatPlot_OnSet_CBs, self.CP_BG )
    self.Dock.Bind ( wx.EVT_CHECKBOX, self.MatPlot_OnSet_CBs, self.CB_Grid )
    self.Dock.Bind ( wx.EVT_CHECKBOX, self.MatPlot_OnSet_CBs, self.CB_Axis )
    self.Dock.Bind ( wx.EVT_CHECKBOX, self.MatPlot_OnSet_CBs, self.CB_Legend )
    self.Dock.Bind ( wx.EVT_CHECKBOX, self.MatPlot_OnPolar,   self.CB_Polar )
    self.Dock.Bind ( wx.EVT_CHECKBOX, self.MatPlot_OnFFT,     self.CB_FFT )
    self.Button_Image.Bind     ( wx.EVT_BUTTON, self.MatPlot_OnSaveImage, self.Button_Image )
    self.Button_ClipBoard.Bind ( wx.EVT_BUTTON, self.MatPlot_OnCopyClipBoard, self.Button_ClipBoard )

    if self.Test :
      self.Spin.Bind ( wx.EVT_SPINCTRL, self.MatPlot_OnSpinEvent, self.Spin )
      self.Dock.Bind ( wx.EVT_CLOSE, self.MatPlot_OnClose )

    #if not ( self.connect ) :
    self.Dock.connect = self.Canvas.mpl_connect ( 'motion_notify_event', self.MatPlot_OnMotion )
    # *************************************************************

  # *************************************************************
  # We need this for Ubuntu, and even then it works limited
  # *************************************************************
  def _OnSize ( self, event ) :
    event.Skip()
    wx.CallAfter ( self.MatPlot_Redraw ) 

  # *************************************************************
  # *************************************************************
  def Calculate ( self ):
    # input might be one of the following:
    #   1:  <array>
    #   2:  list = [ <array>, [ <signal name>,  <signal color>, <linewidth> ] ]
    #
    # array might be one of the following:
    #   A: a 1-dimensional array  ==>  y(x), x=equidistant
    #   B: a 2-dimensional array, with second dimension = 2  ==>  y = f(x)
    #   C: a 2-dimensional array, with second dimension >> 6  ==> z = f(x,y)
    
    # we can either use signal, which is the input channel that has changed
    # or use the Bricks input channels, so we can use all of them at once
    

    self.SignalsX = []
    self.SignalsY = []
    self.Legends = []

    # for test purposes, we don't have a brick but Test_Inputs
    try :
      Inputs = self.Brick.In
    except :
      Inputs = self.Test_Inputs

    for s, IVV in enumerate ( Inputs [1:] ) :
      if IVV != None :
        #print 'MatPlot',s,len(IVV)
        if not ( operator.isSequenceType ( IVV ) ) or \
           isinstance ( IVV, ndarray ):
          IVV = eval ( '[IVV]' )
          #print 'no sequence'

        # determine the number of arrays
        # if exactly 2, special case: x,y pairs
        NA = 0
        for IV in IVV :
          if isinstance ( IV, ndarray ) :
            NA += 1
          else :
            break

        #print 'NA',NA,IVV[0].shape
        
        # process all signals
        self.Pseudo_Color = False
        if IVV[0].ndim == 2 :
          self.Pseudo_Color = True
          self.SignalsX.append ( IVV [0] )

        elif NA == 1 :
          L = len ( IVV[0] )
          self.SignalsX.append ( linspace ( 0, L-1, L) )
          self.SignalsY.append ( IVV [0] )

        elif NA == 2 :
          self.SignalsX.append ( IVV [0] )
          self.SignalsY.append ( IVV [1] )

        else :
          self.SignalsX.append ( IVV [0] )
          for i,IV in enumerate ( IVV [1:NA] ):
            self.SignalsY.append ( IV )
            
        # add legends
        if NA == 1:
          if ( len(IVV) > NA ) and ( len ( IVV [NA] ) > 0) :
            self.Legends.append ( IVV[NA][0] )
          else :
            self.Legends.append ( 'Signal 1' )
        for i,IV in enumerate ( IVV [1:NA] ):
          if ( len(IVV) > NA ) and ( len ( IVV [NA] ) > i) :
            self.Legends.append ( IVV[NA][i] )
          else :
            self.Legends.append ( 'Signal ' + str(i+1) )

    #print 'Legends',self.Legends
    self.MatPlot_ReCreate_Plot ()
    #print 'MatPlot recreated'


  # *************************************************************
  # *************************************************************
  def MatPlot_ReCreate_Plot ( self ):
    # BUG, "hold" doesn't work in polar, therefore create a new figure

    # helps sometimes .... for polar plot
    ## LUKT NIET MEER rcParams [ 'grid.color' ] = self.Color_2_MatPlot ( self.CP_Grid.GetColour () )

    self.figure.clear()
    self.lx = None

    if not ( self.Pseudo_Color ) :
      self.CB_Polar.SetLabel ('-Polar')

      if self.CB_FFT.GetValue() : config = 212
      else:                       config = 111
      self.axes = self.figure.add_subplot ( config, polar = self.CB_Polar.GetValue () )
      for i,SX in enumerate ( self.SignalsY ) :
        self.axes.plot ( self.SignalsX[0], self.SignalsY[i], )

      if self.CB_FFT.GetValue() :
        self.axes_2 = self.figure.add_subplot ( 211, polar = self.CB_Polar.GetValue () )
        for i,SX in enumerate ( self.SignalsY ) :
          self.axes_2.psd ( self.SignalsY[i], 512, 1,
                            #detrend = mlab.detrend_linear,  #doesn't work
                            #detrend = mlab.detrend_mean,    #doesn't work
                            detrend = mlab.detrend_none,
                            #window = mlab.window_none )     #weird scaling
                            window = mlab.window_hanning )
          # doesn't work:
          # self.axes_2.xlabel = 'aap'
          # self.axes_2.axis ( 0, 0, 50, -50)
      else :
        self.axes_2 = None

    else :  # Pseudo color
      self.CB_FFT.Hide ()
      self.CB_Polar.SetLabel ( '-Low Res' )
      self.axes = self.figure.add_subplot ( 111 )

      if self.CB_Polar.GetValue () :
        cmap = cm.get_cmap ( 'jet', 10 )    # 10 discrete colors
      else :
        cmap = cm.jet
      #cmap = cm.gray
      # IMPORTANT, setting the size explictly,
      # prevents rescaling which sometimes occurs when crosshair is drawn
      s = self.SignalsX[0].shape
      try: # SignalsX might not be available yet
        im = self.axes.imshow ( self.SignalsX[0] , cmap = cmap, extent=(0,s[0],0,s[1]) )

        #im.set_interpolation ( 'nearest' )    # and there are a lot more !!
        #im.set_interpolation ( 'bicubic' )
        im.set_interpolation ( 'bilinear' )
        self.figure.colorbar ( im )
      except: pass

    self.axes.hold ( True )   # needed for measurement cursor
    if self.axes_2 : self.axes_2.hold ( True )
    self.MatPlot_Redraw ()

  # *************************************************************
  # *************************************************************
  def MatPlot_Redraw ( self ) :
    color = self.CP_BG.GetColour()
    color = self.Color_2_MatPlot ( color )
    self.axes.set_axis_bgcolor ( color )
    if self.axes_2 : self.axes_2.set_axis_bgcolor ( color )
    self.figure.set_facecolor  ( color )
    self.figure.set_edgecolor  ( color )

    if self.CB_Axis.GetValue () :
      self.axes.set_axis_on ()
      if self.axes_2 : self.axes_2.set_axis_on ()
    else :
      self.axes.set_axis_off ()
      if self.axes_2 : self.axes_2.set_axis_off ()

    color = self.CP_Grid.GetColour()
    color = self.Color_2_MatPlot ( color )
    self.axes.grid ( self.CB_Grid.GetValue () )
    if self.axes_2 : self.axes_2.grid ( self.CB_Grid.GetValue () )
    # setting the grid color sometimes generates an exception
    # this seems to happen completely random ????
    try:
      if self.CB_Grid.GetValue () :
        self.axes.grid ( color=color )
        if self.axes_2 : self.axes_2.grid ( color=color )
    except:
      pass

    # Polar doesn't support legend (use figlegend)
    if self.Pseudo_Color or not ( self.CB_Polar.GetValue () ) :
      if self.CB_Legend.GetValue () :
        self.axes.legend ( self.Legends )
      else :
        self.axes.legend_ = None
    # FFT plot: no legend
    if self.axes_2 :
      self.axes_2.legend_ = None

    self.Canvas.draw ()

  # *************************************************************
  # create an example image
  # *************************************************************
  def MatPlot_Example ( self, Example ) :
    self.Test_Inputs = [None]
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
      def _func ( x, y ):
        return ( 1- x/2 + x**5 + y**3 ) * exp( -x**2 - y**2 )
      dx, dy = 0.05, 0.05
      x = arange ( -3.0, 3.0, dx )
      y = arange ( -3.0, 3.0, dy )
      X,Y = meshgrid ( x, y )
      self.Test_Inputs.append ( _func ( X, Y ) )

    if len ( self.Test_Inputs ) == 1 :
      temp = []
      temp.append ( x )
      temp.append ( y )
      self.Test_Inputs.append ( temp )

    self.Calculate()


  # *************************************************************
  # *************************************************************
  def MatPlot_OnMotion ( self, event ) :
    if self.CB_Polar.GetValue () and not (self.Pseudo_Color ): return
  
    x, y = event.x, event.y
    # check if within an "axes" but not in a "bar-axes"
    if event.inaxes and isinstance ( event.inaxes, matplotlib.axes.Subplot ) :
      x, y = event.xdata, event.ydata

      if not ( self.lx ) :
        self.minx, self.maxx = event.inaxes.get_xlim ()
        self.miny, self.maxy = event.inaxes.get_ylim ()

        """
        self.lx, = self.axes.plot ( ( self.minx, self.maxx ), ( y, y ), 'k-' )  # the horiz line
        self.ly, = self.axes.plot ( ( x, x ), ( self.miny, self.maxy ), 'k-' )  # the vert line
        self.meas_txt = self.axes.text ( 0.02, 0.02, 'x=%1.2f, y=%1.2f'% ( x, y ),
                                         transform = self.axes.transAxes )
        """
        self.lx, = event.inaxes.plot ( ( self.minx, self.maxx ), ( y, y ), 'k-' )  # the horiz line
        self.ly, = event.inaxes.plot ( ( x, x ), ( self.miny, self.maxy ), 'k-' )  # the vert line
        self.meas_txt = event.inaxes.text ( 0.02, 0.02, 'x=%1.2f, y=%1.2f'% ( x, y ),
                                         transform = event.inaxes.transAxes )
      else :
        # update the crosshair positions
        self.lx.set_data ( ( self.minx, self.maxx ), ( y, y ) )
        self.ly.set_data ( ( x, x ), ( self.miny, self.maxy ) )
        self.meas_txt.set_text ( 'x=%1.2f, y=%1.2f'% ( x, y ) )

    else :
      # Hide the cross hair
      if self.lx :
        self.lx.set_data ( ( x, x ), ( y, y ) )
        self.ly.set_data ( ( x, x ), ( y, y ) )
        self.meas_txt.set_text ( '' )
        self.lx = None
        
    self.Canvas.draw ()

  # *************************************************************
  # *************************************************************
  def MatPlot_OnSet_CBs ( self, event ) :
    self.MatPlot_Redraw ()

  # *************************************************************
  # *************************************************************
  def MatPlot_OnPolar ( self, event ) :
    if self.CB_Polar.GetValue () :  self.CB_FFT.Hide ()
    else :                          self.CB_FFT.Show()
    self.MatPlot_ReCreate_Plot ()

  # *************************************************************
  # *************************************************************
  def MatPlot_OnFFT ( self, event ) :
    if self.CB_FFT.GetValue () :  self.CB_Polar.Hide ()
    else :                        self.CB_Polar.Show()
    self.MatPlot_ReCreate_Plot ()

  # *************************************************************
  # *************************************************************
  def MatPlot_OnSpinEvent ( self, event ) :
    Example = event.GetInt()
    self.MatPlot_Example ( Example )
    
  # *************************************************************
  # *************************************************************
  def MatPlot_OnCopyClipBoard ( self, event ) :
     #canvas = FigureCanvasWxAgg(...)
     self.Canvas.Copy_to_Clipboard ( event = event )

  # *************************************************************
  # *************************************************************
  def MatPlot_OnSaveImage ( self, event ) :
    file = Ask_File_For_Save ( os.getcwd(),
                               FileTypes = '*.png',
                               Title = 'Save Plot as PNG-image' )
    if file :
      self.figure.savefig ( file )

  # *************************************************************
  # Set Grid color of all backgrounds
  # Doing this gives huges problems,
  # therefor we accept that in the polar
  # *************************************************************
  """
  def OnGridColor ( self, event ) :
    rcParams [ 'grid.color' ] = self.Color_2_MatPlot ( self.CP_Grid.GetColour () )

    # Because we need to reload the resources,
    # we force it by recreating to the total plot
    self.Sizer.Remove ( self.Canvas )
    self.figure = Figure ()
    self.Canvas = FigureCanvas ( self.Dock, -1, self.figure )
    self.lx = None
    self.Sizer.Prepend ( self.Canvas, 1, wx.EXPAND )
    self.Sizer.Layout ()
    self.MatPlot_Example ( self.Spin.GetValue () )
  """

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
  def MatPlot_OnClose ( self, event ) :
    if self.Ini and self.Test :
      self.Ini.Section = 'MatPlot'
      self.Ini.Write ( 'Pos',  self.Dock.GetPosition () )
      self.Ini.Write ( 'Size', self.Dock.GetSize () )
      self.Save_Settings ( self.Ini )
    event.Skip ()

  # *************************************************************
  # *************************************************************
  def Save_Settings ( self, ini, key = None ) :
    if ini :
      line = []
      line.append ( tuple ( self.CP_BG.GetColour() ) )
      line.append ( tuple ( self.CP_Grid.GetColour() ) )
      line.append ( self.CB_Grid.GetValue () )
      line.append ( self.CB_Axis.GetValue () )
      line.append ( self.CB_Legend.GetValue () )
      line.append ( self.CB_Polar.GetValue () )
      line.append ( self.CB_FFT.GetValue () )
      if self.Test :
        line.append ( self.Spin.GetValue() )
      if not ( key ) :
        key = 'CS_'
      v3print ( 'MatPlot SAVE', key, '=', line )
      line = ini.Write ( key, line )

  # *************************************************************
  # *************************************************************
  def Load_Settings ( self, ini, key = None ) :
    #print 'llkwp',line
    if not ( key ) :
      key = 'CS_'
    line = ini.Read ( key, '' )
    if line :
      self.CP_BG.SetColour ( line [0] )
      self.CP_Grid.SetColour ( line[1] )
      self.CB_Grid.SetValue ( line[2] )
      self.CB_Axis.SetValue ( line[3] )
      self.CB_Legend.SetValue ( line[4] )
      self.CB_Polar.SetValue ( line[5] )
      self.CB_FFT.SetValue ( line[6] )
      if self.Test :
        self.Spin.SetValue ( line[7] )
    self.MatPlot_ReCreate_Plot ()
    #self.MatPlot_Redraw ()

# ***********************************************************************


# ***********************************************************************
# A simple form to test the control
# ***********************************************************************
class Simple_Test_Form ( wx.MiniFrame ):
  def __init__ ( self, ini = None ):
    # restore position and size
    if ini :
      ini.Section = 'MatPlot'
      pos  = ini.Read ( 'Pos'  , ( 50, 50 ) )
      size = ini.Read ( 'Size' , ( 500, 300 ) )

    wx.MiniFrame.__init__(
      self, None, -1, 'Test PyLab Works GUI Control',
      size  = size,
      pos   = pos,
      style = wx.DEFAULT_FRAME_STYLE )

    print ('JJUUI',ini)
    # Create the control to be tested
    t_C_MatPlot ( self, None, Ini = ini, Test= True )
# ***********************************************************************



# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  app = wx.PySimpleApp ()
  ini = inifile ( 'test_matplot.cfg' )
  frame = Simple_Test_Form (ini = ini)
  frame.Show ( True )
  app.MainLoop ()
  ini.Close ()
# ***********************************************************************
pd_Module ( __file__ )

