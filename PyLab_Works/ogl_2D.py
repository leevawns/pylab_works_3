# ***********************************************************************
# Extension of OGLlike with animations
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2008 Stef Mientki
# mailto: ...
# Please let me know if it works or not under different conditions
#
# <Version: 1.0    , 19-04-2008,  Stef Mientki
# Test Conditions: 1
#    - orginal release
#
# Test Conditions
# 1. WinXP-SP2, Python 2.4.3, wxPython wx-2.8-msw-ansi
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
"""
  Diagram
  ShapeCanvas ( wx.ScrolledWindow )
  ShapeEvtHandler
    Shape
      PointShape
        Node
          INode
          ONode
          ResizeableNode
        ResizeableNode_2D
      LineShape
        Connection_Line
      t_BaseShape
        Rectangle
--------------------------------- below = ogl_2D
      Axis_Shape
      Grid_Shape
      Rot_Shape
        Circle_Shape
          Button_Shape
        Rectangle_Shape
        Free_Shape
        Points_Shape
          Function_Shape
        Line_Shape
          Arrow_Shape
        Text_Shape
"""
# ***********************************************************************

from OGLlike import *
from numpy import arange
from numpy import arctan, pi, sqrt, sin, cos, tan


# ***********************************************************************
# ***********************************************************************
class Axis_Shape ( Shape ) :
  def __init__( self, Canvas, x = 0, y = 0 ):
    # accept both single values and tuples of xy-values
    if isinstance ( x, tuple ) or \
       isinstance ( x, list ):
      y = x [1]
      x = x [0]
    self.Canvas = Canvas
    Shape.__init__ ( self, Canvas, [x] ,  [y] )
    self.Color         = wx.BLUE
    self.Line_Width    = 2

  # *********************************************************
  # *********************************************************
  def draw ( self, dc ) :
    Shape.draw ( self, dc )
    dc.SetPen ( wx.Pen ( self.Color, self.Line_Width ) )

    x = self.Canvas.W2Sx ( self._x[0] )
    dc.DrawLine ( x, self.Canvas.W2Sy (self.Canvas.WCb),
                  x, self.Canvas.W2Sy (self.Canvas.WCt) )
    y = self.Canvas.W2Sy ( self._y[0] )
    dc.DrawLine ( self.Canvas.W2Sx (self.Canvas.WCl), y,
                  self.Canvas.W2Sx (self.Canvas.WCr), y )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Grid_Shape ( Shape ) :
  def __init__( self, Canvas, delta = 10, Angle = None ):
    self.Canvas = Canvas
    self.D = delta
    Shape.__init__ ( self, Canvas, [0] ,  [0] )
    if Angle :
      self.rot = Angle
    else :
      self.rot = 0
    self.Color = wx.GREY_PEN.GetColour()
    self.Line_Width = 1
    
  # *********************************************************
  # *********************************************************
  def draw ( self, dc ) :
    Shape.draw ( self, dc )
    dc.SetPen ( wx.Pen ( self.Color, self.Line_Width ) )

    WCL =self.Canvas.WCl
    WCR =self.Canvas.WCr
    WCB =self.Canvas.WCb
    WCT =self.Canvas.WCt

    # vertical lines
    N      = abs ( WCL - WCR ) / self.D
    Offset = WCL + self.D + WCL % self.D
    tgx    = self.Canvas.W2S_w ( self.Canvas.WCt * tan ( self.rot ) )
    tgy    = self.D          * tan ( self.rot )
    for i in range ( N ) :
      x = self.Canvas.W2Sx ( Offset + i * self.D )
      if self.rot == 0 :
        dc.DrawLine ( x, self.Canvas.W2Sy (self.Canvas.WCb),
                      x, self.Canvas.W2Sy (self.Canvas.WCt) )
      else :
        dc.DrawLine ( x, self.Canvas.W2Sy ( i * tgy ),
                      x + tgx, self.Canvas.W2Sy (self.Canvas.WCt) )

    # horizontal lines
    N = abs ( WCB - WCT ) / self.D
    Offset = WCB + self.D + WCB % self.D
    for i in range ( N ) :
      y = self.Canvas.W2Sy ( Offset + i * self.D )
      if self.rot == 0 :
        dc.DrawLine ( self.Canvas.W2Sx (self.Canvas.WCl), y,
                      self.Canvas.W2Sx (self.Canvas.WCr), y )
      else :
        dc.DrawLine ( self.Canvas.W2Sx ( i * tgy ), y,
                      self.Canvas.W2Sx (self.Canvas.WCr), y - tgx )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Rot_Shape ( Shape ) :
  def __init__ ( self, Container_Canvas ) : #, x, y ) :
    self.shape_filled = True    # False if a not filled line-shape
    self.rot = 0
    self.Calc_xy()

    self.Corner_x      = 0
    self.Corner_y      = 0
    self.Trails        = []
    self.Trails_Corner = []
    
    self.Color         = wx.BLUE
    self.Line_Width    = 1

    # *********************************************************
    # Create the shape and change some initial values
    # *********************************************************
    Shape.__init__ ( self, Container_Canvas, self._x, self._y )
    self.Resizeable = True
    self.Selectable = True
    self.Control    = False
    self.value      = 1

  # *********************************************************
  # always called instead of the normal mechanism
  # *********************************************************
  def __setattr__ ( self, attr, value ) :
    if   attr == 'x' :
      self._XY_Org [0] = value
    elif attr == 'y' :
      self._XY_Org [1] = value
    else :
      self.__dict__[attr] = value

  # *********************************************************
  # only called when not found with the normal mechanism
  # *********************************************************
  def __getattr__ ( self, attr ) :
    if   attr == 'x' :
      return self._XY_Org [0]
    elif attr == 'y' :
      return self._XY_Org [1]
    else :
      if not (  attr in self.__dict__ ) :
        self.__dict__[attr] = 0
      return self.__dict__[attr]

  # *********************************************************
  # *********************************************************
  def Get_Init_Pars ( self, LB, WH, RT, RPhi ) :
    if RPhi :
      R   = RPhi [0]
      phi = RPhi [1]
    else :
      if not ( RT ) :
        RT = ( LB [0] + WH [0], LB [1] + WH [1] )

      W = RT [0] - LB [0]
      H = RT [1] - LB [1]

      R = sqrt ( W ** 2 + H ** 2 )
      if W == 0 :
        phi = pi / 2
      else :
        phi = arctan ( 1.0 * H / W )

    return R, phi

  # *********************************************************
  # *********************************************************
  def Calc_xy ( self ) :
    P       = []
    self._x = []
    self._y = []

    # store the first point for the corner trail
    self.Corner_x = self._XY_Org[0] + \
      self._R_Phi[0][0] * cos ( self._R_Phi[0][1] + self.rot )
    self.Corner_y = self._XY_Org[1] + \
      self._R_Phi[0][0] * sin ( self._R_Phi[0][1] + self.rot )

    # transform all the points
    for point in self._R_Phi :
      x = self.Canvas.W2Sx ( self._XY_Org[0] +
                            point[0] * cos ( point[1] + self.rot ) )
      y = self.Canvas.W2Sy ( self._XY_Org[1] +
                            point[0] * sin ( point[1] + self.rot ) )
      self._x.append ( x )
      self._y.append ( y )
      P.append ( ( x, y ) )
    return P

  # *********************************************************
  # Screen Width to world coordinates
  # *********************************************************
  def S2W_w ( self, x ) :
    return  1.0* x * ( self.Canvas.WCr - self.Canvas.WCl ) /self.Canvas._W

  # *********************************************************
  # Screen Height to world coordinates
  # *********************************************************
  def S2W_h ( self, y ) :
    return   -y * ( self.Canvas.WCt - self.Canvas.WCb) / self.Canvas._H

  # *********************************************************
  # after a drag, correct the origin
  # *********************************************************
  def move ( self, x, y ) :
    #print 'piepjes'
    self._XY_Org [0] += self.S2W_w ( x )
    self._XY_Org [1] += self.S2W_h ( y )

  # *********************************************************
  # *********************************************************
  def draw ( self, dc ) :
    Shape.draw ( self, dc )
    P = self.Calc_xy ()
    dc.SetBrush ( wx.Brush ( self.Color ) )
    dc.SetPen ( wx.Pen ( wx.BLACK, self.Line_Width ) )
    if self.shape_filled :
      dc.DrawPolygon( P )
    else :
      dc.SetPen ( wx.Pen ( self.Color, self.Line_Width ) )
      p0 = P[0]
      for p1 in P [1:] :
        dc.DrawLine ( p0[0], p0[1], p1[0], p1[1] )
        p0 = p1

    self._Draw_Trails ( dc )
    
  # *********************************************************
  # *********************************************************
  def Add_Trail ( self ) :
    if self.Trail :
      self.Trails.append ( ( self._XY_Org [0], self._XY_Org [1] ) )
    if self.Trail_Corner :
      self.Trails_Corner.append ( ( self.Corner_x, self.Corner_y ) )

  # *********************************************************
  # *********************************************************
  def _Draw_Trails ( self, dc ) :
    # draw the center trail
    for O in self.Trails :
      dc.DrawCircle ( self.Canvas.W2Sx ( O[0] ),
                      self.Canvas.W2Sy ( O[1] ), 3 )

    # draw the corner trail
    for O in self.Trails_Corner:
      dc.DrawCircle ( self.Canvas.W2Sx ( O[0] ),
                      self.Canvas.W2Sy ( O[1] ), 2 )

  # *********************************************************
  # *********************************************************
  def HitTest ( self, x, y ) :
    if ( x < min ( self._x ) ) or \
       ( x > max ( self._x ) ) or \
       ( y < min ( self._y ) ) or \
       ( y > max ( self._y ) ) :
      return False
    else :
      # If it's a control, don't allow select,
      # but toggle the value
      if self.Control :
        if self.value == 0 :
          self.value = 1
        else :
          self.value = 0
        return False
      
      return True
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Circle_Shape ( Rot_Shape ) :
  def __init__( self, Canvas,  Radius = 30, Center =[50,50] ):
    self._XY_Org = list ( Center )
    self._R_Phi = []
    self._R_Phi.append ( ( Radius, -pi / 2 ) )  # bottom is corner trail
    self._R_Phi.append ( ( Radius, 0       ) )
    self._R_Phi.append ( ( Radius, pi / 2  ) )
    self._R_Phi.append ( ( Radius, pi      ) )

    self.Canvas = Canvas
    Rot_Shape.__init__ ( self, Canvas )
    self.Trail        = True

  # *********************************************************
  # *********************************************************
  def draw ( self, dc ) :
    Shape.draw  ( self, dc )
    P = self.Calc_xy ()

    # for controls, color is depending on it's value
    if self.Control and ( self.value == 0 ) :
      a = 2
      rgb = [self.Color.Red()/a, self.Color.Green()/a, self.Color.Blue()/a]
      dc.SetBrush   ( wx.Brush (wx.Color(*rgb) ) )
    else :
      dc.SetBrush   ( wx.Brush ( self.Color ) )

    dc.DrawCircle ( self.Canvas.W2Sx ( self._XY_Org [0] ),
                    self.Canvas.W2Sy ( self._XY_Org [1] ),
                    self.Canvas.W2S_w ( self._R_Phi [0] [0] ) )
    self._Draw_Trails ( dc )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Button_Shape ( Circle_Shape ) :
  def __init__( self, *args, ** kwargs ) : #Canvas,  Radius = 30, Center =[50,50] ):
    Circle_Shape.__init__ ( self, *args, **kwargs )
    self.Control = True
    self.Color = wx.GREEN
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Rectangle_Shape ( Rot_Shape ) :
  def __init__( self, Canvas,
                LB   = ( 0, 0 ),
                WH   = ( 50, 10 ),
                RT   = None,
                RPhi = None ):


    R, phi = self.Get_Init_Pars ( LB, WH, RT, RPhi )
    R = 0.5 * R
    self._XY_Org = [ LB [0] + R * cos ( phi ),
                     LB [1] + R * sin ( phi ) ]

    self._R_Phi = []
    self._R_Phi.append ( ( R, pi + phi ) )  # left bottom is first point
    self._R_Phi.append ( ( R,    - phi ) )
    self._R_Phi.append ( ( R,      phi ) )
    self._R_Phi.append ( ( R, pi - phi ) )

    self.Canvas = Canvas
    Rot_Shape.__init__ ( self, Canvas )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Free_Shape ( Rot_Shape ) :
  def __init__( self, Canvas, Points ) :
    self._XY_Org = xy = [ Points [0] [0], Points [0] [1] ]
    self._R_Phi = [ ( 0, pi ) ]
    for p in Points [ 1 : ] :
      W = p[0] - xy[0]
      H = p[1] - xy[1]
      R = sqrt ( W ** 2 + H ** 2 )
      if W == 0 :
        Phi = pi / 2
      else :
        Phi = arctan ( 1.0 * H / W )
      self._R_Phi.append ( ( R, Phi ) )

    self.Canvas = Canvas
    Rot_Shape.__init__ ( self, Canvas )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Points_Shape ( Rot_Shape ) :
  def __init__( self, Canvas, Points ) :

    # translate the points to XY-org and R-Phi array
    self._XY_Org = xy = [ Points [0] [0], Points [0] [1] ]
    self._R_Phi = [ ( 0, pi ) ]
    for p in Points [ 1 : ] :
      W = p[0] - xy[0]
      H = p[1] - xy[1]
      R = sqrt ( W ** 2 + H ** 2 )
      if W == 0 :
        Phi = pi / 2
      else :
        Phi = arctan ( 1.0 * H / W )
      self._R_Phi.append ( ( R, Phi ) )

    self.Canvas = Canvas
    Rot_Shape.__init__ ( self, Canvas )
    self.shape_filled = False

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Function_Shape ( Points_Shape ) :
  def __init__( self, Canvas, Curve, XRange ) :
    # execute the function, to get the results
    line  = 'x = arange ( *XRange ) \n'
    line += 'y = ' + Curve +'\n'
    line += 'print y \n'
    #print line
    exec (line)

    # put the results into Points
    Points = []
    for i, xi in enumerate ( x ) :
      Points.append ( (xi, y[i] ) )

    Points_Shape.__init__ ( self, Canvas, Points )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Line_Shape ( Rot_Shape ) :
  def __init__( self, Canvas,
                LB   = ( 0, 0 ),
                WH   = ( 50, 10 ),
                RT   = None,
                RPhi = None ):


    R, phi = self.Get_Init_Pars ( LB, WH, RT, RPhi )

    self._XY_Org = [ LB [0], LB [1] ]
    self._R_Phi  = []
    self._R_Phi.append ( ( 0, pi + phi ) )  # left bottom is first point
    self._R_Phi.append ( ( R,      phi ) )


    self.Canvas = Canvas
    Rot_Shape.__init__ ( self, Canvas )
    self.shape_filled = False

    self.Color      = wx.RED
    self.Line_Width = 4

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Arrow_Shape ( Line_Shape ) :

  # *********************************************************
  # *********************************************************
  def draw ( self, dc ) :
    Rot_Shape.draw ( self, dc )

    # draw an arrow point
    R = 4 + 2 * self.Line_Width

    P = [ ( self._x[1], self._y[1] ) ]

    Phi = 1.1 * pi +  ( self._R_Phi [1][1] + self.rot )
    x2 = self.Canvas.W2Sx (
      self._XY_Org [0] +
      self._R_Phi [1][0] * cos (self.rot + self._R_Phi[1][1]) +
      R * cos ( Phi ) )
    y2 = self.Canvas.W2Sy (
      self._XY_Org [1] +
      self._R_Phi [1][0] * sin (self.rot + self._R_Phi[1][1]) +
      R * sin ( Phi ) )
    P.append ( ( x2, y2 ) )
    #dc.DrawLine ( x1, y1, x2, y2)

    Phi = 0.9 * pi +  ( self._R_Phi [1][1] + self.rot )
    x2 = self.Canvas.W2Sx (
      self._XY_Org [0] +
      self._R_Phi [1][0] * cos (self.rot + self._R_Phi[1][1]) +
      R * cos ( Phi ) )
    y2 = self.Canvas.W2Sy (
      self._XY_Org [1] +
      self._R_Phi [1][0] * sin (self.rot + self._R_Phi[1][1]) +
      R * sin ( Phi ) )
    P.append ( ( x2, y2 ) )
    #dc.DrawLine ( x1, y1, x2, y2)

    dc.SetBrush   ( wx.Brush ( dc.GetPen().GetColour() ) )
    dc.DrawPolygon( P )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Text_Shape ( Rot_Shape ) :
  def __init__( self, Canvas, line, LB = [0,0] ):
    self.text    = line
    self._XY_Org = [ LB [0], LB [1] ]
    self.Canvas  = Canvas

    # we need some coordinates here otherwise init crashes
    self._R_Phi  = []
    self._R_Phi.append ( ( 0,  0    ) )
    self._R_Phi.append ( ( 30, pi/4 ) )
    Rot_Shape.__init__ ( self, Canvas )

    self.Color         = wx.BLUE
    self.Line_Width    = 1

  def draw ( self, dc ) :
    fs = 5 + 6 * self.Line_Width
    dc.SetFont ( wx.Font ( fs, wx.SWISS, wx.NORMAL, wx.NORMAL ) )
    dc.SetTextForeground ( self.Color )
    te = dc.GetTextExtent ( self.text )

    # calculate the upper-right corner
    self._R_Phi  = []
    self._R_Phi.append ( ( 0,  0    ) )
    R = self.S2W_w ( sqrt ( te[0]**2 + te[1]**2 ) )
    self._R_Phi.append ( ( R, arctan ( 1.0 * te[1] / te[0] ) ) )

    self.Calc_xy ()
    x = self.Canvas.W2Sx ( self._XY_Org [0] )

    # Text is defined from the upper-left corner
    # but we want to define it from the lower-left corner
    y = self.Canvas.W2Sy ( self._XY_Org [1] ) - te[1]
    
    # rotation is specified in radians, but we need degrees here
    rot = 180 * self.rot / pi
    dc.DrawRotatedText ( self.text, x, y, rot )
# ***********************************************************************


