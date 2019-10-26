import __init__
from base_control import *
"""
import sys
subdirs = [ '../support' ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
"""

# !!! import wx before any support library !!!
# otherwise the IDE won't do auto-suggest
import wx

from dialog_support import *
from inifile_support import *
#from utility_support import Split_TIO_ARRAY
from array_support import Analyze_TIO_Array
import wx.lib.plot as plot


# ***********************************************************************
# ***********************************************************************
class t_C_PyPlot ( My_Control_Class ):
  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    self.Canvas = plot.PlotCanvas ( self.Dock )
    self.Canvas.SetEnableGrid ( True )
    self.Canvas.SetEnableLegend ( True )
    self.Canvas.SetYSpec ( 'auto' )
    self.Canvas.SetFontSizeAxis ( 8 )

    # Create the panel with the plot controls
    self.Panel = wx.Panel ( self.Dock, size=(100,50))
    self.CB_Grid = wx.CheckBox ( self.Panel, -1, "-Grid-", pos = (0, 3) )
    self.CB_Grid.SetValue ( True )
    self.CP_Grid = wx.ColourPickerCtrl ( self.Panel, -1, pos = (50,0) )
    wx.StaticText ( self.Panel, -1, "BackGround-", pos = (90,3) )
    self.CP_BG = wx.ColourPickerCtrl ( self.Panel, -1, wx.WHITE, pos = (155,0) )
    # no support for Axis
    self.CB_Axis = wx.CheckBox ( self.Panel, -1, "-Axis", pos = (195,3) )
    self.CB_Axis.SetValue ( True )
    self.CB_Legend = wx.CheckBox ( self.Panel, -1, "-Legend", pos = (250,3) )
    self.CB_Legend.SetValue ( True )

    self.Dock.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnGridColor, self.CP_Grid)
    self.Dock.Bind(wx.EVT_COLOURPICKER_CHANGED, self.OnBGColor, self.CP_BG)
    self.Dock.Bind(wx.EVT_CHECKBOX, self.OnSetGrid, self.CB_Grid)
    self.Dock.Bind(wx.EVT_CHECKBOX, self.OnSetAxis, self.CB_Axis)
    self.Dock.Bind(wx.EVT_CHECKBOX, self.OnSetLegend, self.CB_Legend)

    sizer = wx.BoxSizer (wx.VERTICAL)
    sizer.Add ( self.Canvas, 1, wx.EXPAND )
    sizer.Add ( self.Panel, 0 )
    self.Dock.SetSizer ( sizer )

    self.color_defs = ['red', 'blue', 'black', 'red', 'red']
    self.signal_names = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5']

    self.Legends    = []
    self.Colors     = []
    self.LineWidths = []

    self.Nx = 600
    self.alfa = 0

    self.curve = []
    signal = []
    for i in range ( self.Nx ):
      signal.append ( [i,0] )

    from copy import copy
    self.NCurve = self.CD.Get ( 'Range', 1 )
    print ('NCRuve',self.NCurve,self.CD.Range)
    #self.NCurve = max ( min ( 1, self.NCurve ) , self.NCurve )
    #self.NCurve = min ( max ( 1, self.NCurve ) , self.NCurve )

    if self.NCurve < 1 :
      self.NCurve = 1
    print ('NCRuve',self.NCurve)

    for NC in range ( self.NCurve ) :
      self.curve.append ( copy(signal))

    self.pointer = self.NCurve * [0]

    self.elements = len ( self.curve [0] )

  # ********************************************************
  # PYPLOT ACTIONS
  # ********************************************************
  # Essential, to prevent flicker !!
  # DOESN'T WORK FOR PYPLOT
  #def On_PyPlot_Panel_Erase ( self, event ) :
  #  pass

  # Settings to be saved, which are not stored in the Brick parameters
  def Save_Settings ( self, ini, key = None ) :
    if not ( key ) :
      key = 'CS_'
    if ini :
      line = []
      line.append ( tuple ( self.Canvas.GetGridColour() ) )
      line.append ( tuple ( self.Canvas.GetBackgroundColour() ) )
      line.append ( self.Canvas.GetEnableGrid() )
      line.append ( self.Canvas.GetFontSizeAxis() )
      line.append ( self.Canvas.GetEnableLegend() )
      line = ini.Write ( key, line )

  def Load_Settings ( self, ini, key = None ) :
    if not ( key ) :
      key = 'CS_'
    line = ini.Read ( key, '' )
    if line :
      color = wx.Colour ( *line[0] )
      self.Canvas.SetGridColour ( color )
      self.CP_Grid.SetColour ( color )

      color = wx.Colour ( *line[1] )
      self.Canvas.SetBackgroundColour ( color )
      self.CP_BG.SetColour ( color)

      self.Canvas.SetEnableGrid ( line[2] )
      self.CB_Grid.SetValue ( line[2] )

      self.Canvas.SetFontSizeAxis ( line[3] )
      self.CB_Axis.SetValue ( line[3] != 1 )

      self.Canvas.SetEnableLegend ( line[4] )
      self.CB_Legend.SetValue ( line[4] )
      self.Canvas.Redraw()

  def OnGridColor ( self, event ) :
    self.Canvas.SetGridColour ( self.CP_Grid.GetColour () )
    self.Canvas.Redraw()

  def OnBGColor ( self, event ) :
    # requires a modified PyPlot
    self.Canvas.SetBackgroundColour ( self.CP_BG.GetColour () )
    self.Canvas.Redraw()

  def OnSetGrid ( self, value) :
    self.Canvas.SetEnableGrid ( self.CB_Grid.GetValue () )
    self.Canvas.Redraw()

  def OnSetAxis ( self, value) :
    if self.CB_Axis.GetValue () :
      self.Canvas.SetFontSizeAxis ( 8 )
    else :
      self.Canvas.SetFontSizeAxis ( 1 )
    self.Canvas.Redraw()

  def OnSetLegend ( self, value) :
    self.Canvas.SetEnableLegend ( self.CB_Legend.GetValue () )

  def SetValue ( self, signal ):
    #v3print ( '************** PyPLOT')
    self.line =[]
    SLEN = 0
    pp = 0
    # walk through all the input signals
    for i, Input in enumerate ( self.Brick.In [1:]) :
      if ( Input != None ) and ( i < self.NCurve ) :
        #Signals, Signal_Attribs = Split_TIO_ARRAY ( Input )#, True )
        #v3print ( 'PyPlot', type(Input),len(Input) )
        Signals, Signal_Attribs = Analyze_TIO_Array ( Input )
        #v3print ( 'PyPlot', type(Input),len(Input),type(Signals),len(Signals) )

        for s, Signal in enumerate ( Signals ) :
          #v3print ( 'PyPlot', type(Signal) )
          SLEN = len ( Signal )
          if SLEN :
            P = self.pointer [pp]
            for x in range ( SLEN ) :
              self.curve [pp] [P] = [ P, Signal [x] ]
              P = ( P + 1 ) % self.Nx
            self.pointer [pp] = P
            pp += 1

            while len ( self.Legends ) <= pp :
              self.Legends.append ( 'Signal-' + str(pp) )
              self.Colors.append ( wx.Color (0,0,0) )
              self.LineWidths.append ( 1 )

            if len ( Signal_Attribs ) > s :
              """
              Legend = Signal_Attribs[s].Get ( 'Name', 'Signal-' + str(pp))
              Color  = Signal_Attribs[s].Get ( 'Color', (0,0,0) )
              Width  = Signal_Attribs[s].Get ( 'LineWidth', 1 )
              Color  = wx.Color ( *Color)
              """
              self.Legends [pp] =\
                Signal_Attribs[s].Get ( 'Name', 'Signal-' + str(pp))
              self.Colors  [pp] =\
                wx.Color ( *Signal_Attribs[s].Get ( 'Color', (0,0,0) ) )
              self.LineWidths [pp] =\
                Signal_Attribs[s].Get ( 'LineWidth', 1 )
                
              #v3print ('TTTT',pp,len ( Signal_Attribs ),Color )
              #self.line.append ( plot.PolyLine (
              #  self.curve [i], legend = Legend, colour = Color, width = Width ))
            else :
              #self.line.append ( plot.PolyLine ( self.curve [i] ))
              pass
            
            self.line.append ( plot.PolyLine (
              self.curve [i],
              legend = self.Legends    [pp],
              colour = self.Colors     [pp],
              width  = self.LineWidths [pp] ))
              
    self.Canvas.Draw( plot.PlotGraphics ( self.line ), ( 0, self.Nx ), ( -10, 10 ) )
    self.Canvas.SetShowScrollbars ( False )
    #self.Refresh()
# ***********************************************************************
pd_Module ( __file__ )