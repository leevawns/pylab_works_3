import __init__
from   PyLab_Works_Globals import _

from   numpy import  array, zeros
import wx
from   menu_support    import *

XDIV = YDIV = 10
MAX_SCREEN_WIDTH = 1680  # 19" widescreen TFT



# ***********************************************************************
# ***********************************************************************
class _PlotCanvas_Base ( wx.Window ) :

  #def __init__(self, dock, parent, Real_Time = False, Buf_max = MAX_SCREEN_WIDTH ):
  def __init__ ( self, dock, parent, Real_Time ):
    # we need wx.WANTS_CHARS, to catch arrow keys and tab
    wx.Window.__init__ ( self, dock, style = wx.WANTS_CHARS )

    self.Dock      = dock
    self.My_Parent = parent
    self.Real_Time = Real_Time

    self.TopFrame  = wx.GetTopLevelParent ( self.Dock )
    self.Buf_max   = MAX_SCREEN_WIDTH

    # set curser as cross-hairs
    #self.SetCursor(wx.CROSS_CURSOR)
    self.old_Cursor      = [ -1, -1 ]
    self.CursorType      = 0

    # NORMAL ONLY
    self.old_CMemo       = [ None, None ]
    self.CMemo_Labels    = [ [], [] ]
    self.Memo_Extra      = None
    self.Memo_Extra_Text = ''
    self.Erase_Block     = XDIV * [ False ]
    # Create Placeholder for signal curves
    self.curves = []
    self.gain   = []
    self.offset = []
    self.name   = []
    self.cal1   = []
    self.cal2   = []
    self.Dp     = 0

    # Create Placeholder for signal curves
    self.Buf_rp = 0
    self.Buf_wp = 0


    # start values for MinMax display
    self.new_N     = 0
    self.N_Average = 1
    self.Linear_Interpolation = False

    self.Bind ( wx.EVT_CONTEXT_MENU, self._On_Show_Popup   )
    self.Bind ( wx.EVT_KEY_DOWN,     self._On_Key_Down     )
    self.Bind ( wx.EVT_LEFT_DOWN,    self._On_Mouse_Left   )
    self.Bind ( wx.EVT_MOTION,       self._On_Mouse_Move   )
    self.Bind ( wx.EVT_MIDDLE_DOWN,  self._On_Mouse_Middle )
    self.Bind ( wx.EVT_SIZE,         self._On_Size         )
    self.Bind ( wx.EVT_PAINT,        self._On_Paint        )

    self.BG_Color = wx.Colour( 249, 249, 217 )
    gc = 200
    self.Grid_Color = wx.Colour ( gc, gc, gc )




  # *****************************************************************
  # *****************************************************************
  def _On_Key_Down ( self, event ) :
    print ('Toets..........',event.GetKeyCode())
    #if event.GetKeyCode() != wx.WXK_LEFT : event.Skip()

  # *****************************************************************
  # Draw the buffer to screen
  # *****************************************************************
  def _On_Paint ( self, event ):
    dc = wx.BufferedPaintDC ( self )

  # *****************************************************************
  # Let the main program change one or more parameters of the PlotCanvas
  # *****************************************************************
  def Set_Canvas ( self, BG_Color = None, grid_color = None ) :
    if grid_color :
      if not isinstance ( grid_color, wx.Colour ) :
        grid_color = wx.NamedColor ( grid_color )
      self.Grid_Color = grid_color
    if BG_Color :
      if not isinstance ( BG_Color, wx.Colour ) :
        BG_Color = wx.NamedColor ( BG_Color )
      self.BG_Color = BG_Color
      self.Brush = wx.Brush ( BG_Color )
    self.Pen = wx.Pen ( self.Grid_Color, 1, wx.SOLID )
    self._Redraw_Screen ()


# ***********************************************************************
pd_Module ( __file__ )
