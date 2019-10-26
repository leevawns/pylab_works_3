def Create_MatPlot ( self, i, C ) :
  Control_Pars = self.Create_New_Control ( C, 0, None, 0,0,0, False )
  Control_Pars [ 'Control_SetValue' ] = self.Set_MatPlot_Value

  self.figure = Figure()
  self.Canvas = FigureCanvas ( self, -1, self.figure )
  self.axes = self.figure.add_subplot ( 111 )
  self.lx = None

  if not ( self.parent ) :
    self.MatPlot_Example ( self.Initial_Spin )
  else :
    self.MatPlot_Set_Figure_Pars ()

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
  self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.MatPlot_OnGridColor, self.CP_Grid)
  self.Bind(wx.EVT_COLOURPICKER_CHANGED, self.MatPlot_OnBGColor, self.CP_BG)
  self.Bind(wx.EVT_CHECKBOX, self.MatPlot_OnSet_CBs, self.CB_Grid)
  self.Bind(wx.EVT_CHECKBOX, self.MatPlot_OnSet_CBs, self.CB_Axis)
  self.Bind(wx.EVT_CHECKBOX, self.MatPlot_OnSet_CBs, self.CB_Legend)
  self.Bind(wx.EVT_CHECKBOX, self.MatPlot_OnPolar, self.CB_Polar)
  self.Button_Image.Bind ( wx.EVT_BUTTON, self.MatPlot_OnSaveImage, self.Button_Image )
  if not ( self.parent ) :
    self.Spin.Bind ( wx.EVT_SPINCTRL, self.MatPlot_OnSpinEvent, self.Spin )
    self.Bind ( wx.EVT_CLOSE, self.MatPlot_OnClose )

  #if not ( self.connect ) :
  self.connect = self.Canvas.mpl_connect ( 'motion_notify_event', self.MatPlot_OnMotion )
  # *************************************************************

  # *************************************************************
  # *************************************************************
  self.sizer = wx.BoxSizer ( wx.VERTICAL )
  self.sizer.Add ( self.Canvas, 1, wx.EXPAND )
  self.sizer.Add ( self.Panel, 0 )
  self.SetSizer ( self.sizer )
  #self.Fit()
  # *************************************************************


  """
  self.color_defs = ['red', 'blue', 'black', 'red', 'red']
  self.signal_names = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5']

  self.Nx = 600
  self.alfa = 0

  self.curve = []
  signal = []
  for i in range ( self.Nx ):
    signal.append ( [i,0] )
  from copy import copy
  self.NCurve = C [ 'Range' ]
  self.NCurve = max ( min ( 1, self.NCurve ) , self.NCurve )
  for NC in range ( self.NCurve ) :
    self.curve.append ( copy(signal))
  self.elements = len ( self.curve [0] )
  self.pointer = 0
  """



