import __init__
from General_Globals import *
from gui_support     import *

from numpy import *
import wx

import matplotlib
matplotlib.interactive(False)
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure
from matplotlib.pyplot import gcf, setp


# ***********************************************************************
# ***********************************************************************
class Multi_Control:
  def __init__( self, Owner, initialValue=None, minimum=0., maximum=1.):
    self.minimum = minimum
    self.maximum = maximum
    self.value = self.constrain ( initialValue )
    self.knobs = []
    self.attach ( Owner, False )   # draw gooit roet in het eten
      
  def attach ( self, knob, Initialize = True ) :
    self.knobs += [knob]
    knob.Parameter = self
    if Initialize :
      knob.Set_Knob_Value ( self.value )

  def Set_Value_2_Others ( self, value, knob = None ) :
    self.value = self.constrain ( value )
    for feedbackKnob in self.knobs:
      if feedbackKnob != knob:
        feedbackKnob.Set_Knob_Value ( self.value )
    return self.value

  def constrain(self, value):
    if value <= self.minimum:
      value = self.minimum
    if value >= self.maximum:
      value = self.maximum
    return value
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class MatPlot_Window ( wx.Window ) :
  def __init__(self, *args, **kwargs):
    wx.Window.__init__(self, *args, **kwargs)
    self.signals = []
    self.figure = Figure()
    self.canvas = FigureCanvasWxAgg(self, -1, self.figure)
    self.canvas.callbacks.connect('button_press_event', self.mouseDown)
    self.canvas.callbacks.connect('motion_notify_event', self.mouseMotion)
    self.canvas.callbacks.connect('button_release_event', self.mouseUp)
    self.state = None

    self.Bind(wx.EVT_SIZE, self.sizeHandler)

  def sizeHandler(self, *args, **kwargs):
    self.canvas.SetSize(self.GetSize())

  def mouseDown ( self, event ) :
    self.state = None
    for i, signal in enumerate ( self.signals ) :
      if signal in self.figure.hitlist ( event ) :
        self.state  = i+1
        self.x0     = event.xdata
        self.y0     = event.ydata
        if abs ( self.x0 ) < 1.e-8 :
          self.x0 = 1.e-8

        # get all the initial values
        self.CI = []
        for C in self.Controls :
          self.CI.append ( C.value )
        break

  def mouseUp ( self, event ) :
    self.state = None

  def Set_Knob_Value ( self, value ) :
    XY = self.compute ()
    for i, xy in enumerate ( XY ) :
      setp ( self.signals[i], xdata = xy[0], ydata = xy[1] )
    self.canvas.draw()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class FourierDemoWindow ( MatPlot_Window ) :
  def __init__(self, *args, **kwargs):
    MatPlot_Window.__init__(self, *args, **kwargs)

    self.f0 = Multi_Control ( self, 2.0, minimum = 0.0,  maximum = 6.0 )
    self.A  = Multi_Control ( self, 1.0, minimum = 0.01, maximum = 2.0 )

    self.Controls = [ self.A, self.f0 ]

    xy = self.compute ()

    self.subplot1 = self.figure.add_subplot(211)
    self.subplot1.set_title("Click and drag waveforms to change frequency and amplitude", fontsize=12)
    self.subplot1.set_ylabel("Frequency Domain Waveform X(f)", fontsize = 8)
    self.subplot1.set_xlabel("frequency f", fontsize = 8)
    self.subplot1.text ( 0.05, .95,
      r'$X(f) = \mathcal{F}\{x(t)\}$',
      verticalalignment='top', transform = self.subplot1.transAxes )

    self.subplot2 = self.figure.add_subplot(212)
    self.subplot2.set_ylabel("Time Domain Waveform x(t)", fontsize = 8)
    self.subplot2.set_xlabel("time t", fontsize = 8)
    self.subplot2.text ( 0.05, .95,
      r'$x(t) = a \cdot \cos(2\pi f_0 t) e^{-\pi t^2}$',
      verticalalignment='top', transform = self.subplot2.transAxes )

    color = (1., 0., 0.)
    self.signals += self.subplot1.plot ( xy[0][0], xy[0][1], color=color, linewidth=2)
    self.signals += self.subplot2.plot ( xy[1][0], xy[1][1], color=color, linewidth=2)

    self.subplot1.set_xlim ( [ -6, 6 ] )
    self.subplot1.set_ylim ( [  0, 1 ] )

    self.subplot2.set_xlim ( [ -2, 2 ] )
    self.subplot2.set_ylim ( [ -2, 2 ] )

  def mouseMotion ( s, event ) :
    x, y = event.xdata, event.ydata
    if s.state  and x :
      s.A.Set_Value_2_Others ( s.CI[0]+(s.CI[0]*(y-s.y0)/s.y0), s )

      # Frequency should also be transported to myself
      # so we'll leave the second parameter (self) out !!
      if s.state == 1 :
        s.f0.Set_Value_2_Others ( s.CI[1]+(s.CI[1]*(x-s.x0)/s.x0) )
      elif s.state == 2 :
        if s.CI[1] == 0 :
          s.f0.Set_Value_2_Others ( 0 )
        else :
          s.f0.Set_Value_2_Others ( 1./(1./s.CI[1]+(1./s.CI[1] * (x-s.x0)/s.x0)))

  def compute ( self ) :
    f0 = self.f0.value
    A = self.A.value
    f = arange ( -6.0, 6.0, 0.02 )
    t = arange ( -2.0, 2.0, 0.01 )
    x = A*cos(2*pi*f0*t)*exp(-pi*t**2)
    X = A/2*(exp(-pi*(f-f0)**2) + exp(-pi*(f+f0)**2))
    return (f, X), (t, x)
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
from float_slider import Float_Slider
class Float_Slider_New ( Float_Slider ) :
  def __init__ ( self, *args, **kwargs ) :
    Float_Slider.__init__ ( self, *args, **kwargs )
    self.Completion = self.New_Completion

  def Set_Knob_Value ( self, value ) :
    self.SetValue ( value )

  def New_Completion ( self, value ) :
    self.Parameter.Set_Value_2_Others ( value, self )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class FourierDemoFrame ( My_Frame_Class ) :
  def __init__( self, parent_form = None, ini = None ) :
    My_Frame_Class.__init__ ( self, parent_form, 'Demo', ini, 'Test Form' )

    GUI = """
    main, PanelVer, 10
      self.fourierDemoWindow,  FourierDemoWindow
      main4, wx.Panel
        self.Slider, Float_Slider_New, caption = 'Frequency', minValue = 0, maxValue = 6, format='%5.2f'
        self.Slider2, Float_Slider_New, caption = 'Amplitude', minValue = 0.01, maxValue = 2, format='%5.2f'
    """
    self.wxGUI = Create_wxGUI ( GUI )
    main4.Bind ( wx.EVT_SIZE,   self._On_Size )

    self.fourierDemoWindow.f0.attach ( self.Slider )
    self.fourierDemoWindow.A.attach  ( self.Slider2 )

  def _On_Size ( self, event = None ) :
    w = event.GetSize()[0] / 2
    self.Slider.SetSize       ( ( w, -1 ) )
    self.Slider2.SetSize      ( ( w, -1 ) )
    self.Slider2.SetPosition  ( ( w, -1 ) )
# ***********************************************************************


# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':

  Test_Defs ( 1 )

  if Test ( 1 ) :
    My_Main_Application ( FourierDemoFrame )
# ***********************************************************************
pd_Module ( __file__ )
