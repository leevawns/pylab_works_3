import __init__
from base_control        import *

import os

import PyLab_Works_Globals as PG
from   PyLab_Works_Globals import _
import wx

from   dialog_support import *
from   file_support   import Get_Relative_Path

from float_slider import Float_Slider

# ***********************************************************************
# FileDialog,
# can also display a choice list of ODBC databases ( if self.ODBC = True )
# Range = one of the constants definied in
#         ../support/dialog_support.py
#       or
#         a general file dialog mask, e.g.
#         'dBase Files(*.db)|*.db|All Files(*.*)|*.*'
# ***********************************************************************
class t_C_File_Open ( My_Control_Class ):

  def __init__ ( self, *args, **kwargs ):
    print ( 't_C_File_Open.__init__' )
    My_Control_Class.__init__ ( self, *args, **kwargs )

    if self.CD.Caption :
      self.Caption = wx.StaticText (
        self.Dock, -1, ' '+ self.CD.Caption,
        pos = ( self.X, self.Y ) )
      self.dY += 15
      self.Y  += self.dY

    bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_BUTTON, (16,16))
    self.Button = wx.BitmapButton ( self.Dock, -1 , bmp,
                                    pos = ( self.X, self.Y ) )
    self.Button.Bind ( wx.EVT_BUTTON, self.On_FileOpen_Event, self.Button )

    w, h = self.Button.GetSize()
    self.X += w
    self.Text = wx.TextCtrl (
      self.Dock, -1,
      size  = ( -1, h ),
      pos   = ( self.X, self.Y ),
      style = wx.TE_PROCESS_ENTER )  # to catch ENTER-key

    self.dX = -1
    self.dY += h

    # generates an event on a CR
    self.Text.Bind ( wx.EVT_TEXT_ENTER, self.OnEnter )

    self.Last_Path = Application.Dir
    self.ODBC      = False

    self.SetValue  = self.Text.SetValue
    #SetLabel DOESN'T work under Ubuntu

  # *************************************************************
  # *************************************************************
  def SetSize ( self, w_h ) :
    (w,h) = w_h
    self.Text.SetSize ( ( w - self.X, -1 ))

  # *************************************************************
  # *************************************************************
  def GetSize ( self ) :
    return ( self.dX, self.dY )

  # *************************************************************
  # *************************************************************
  def GetValue ( self ) :
    filename = self.Text.GetValue ()
    try :
      return Get_Relative_Path ( filename, Application.Dir )
    except :
      return None

  # *************************************************************
  # *************************************************************
  def OnEnter ( self, event ) :
    Rel_FileName = self.GetValue ()
    self.P[0] = Rel_FileName
    self.SetValue ( Rel_FileName )

  # *************************************************************
  # *************************************************************
  def On_FileOpen_Event ( self, event ):
    if self.ODBC :
      from db_support import Find_ODBC
      ODBC_DBs = Find_ODBC ()
      ODBC_DBs.insert ( 0, [ 'ODBC Name', 'Filename'])

      HelpText = """
The list below, shows both the
  - user   databases ( HKEY_CURRENT_USER\Software\ODBC\ODBC.INI  )
  - system databases ( HKEY_LOCAL_MACHINE\Software\ODBC\ODBC.INI )
  """

      OK, File = ListDialog ( ODBC_DBs,
                              'Select ODBC Database',
                              HelpText )
      print (ODBC_DBs,OK,File)
      if OK :
        self.SetValue ( File )
        self.P[0] = File


    else :    # No ODBC, just a normal file dialog
      FileTypes = self.CD.Get ( 'Range', FT_DBASE_FILES )

      Default_Path = self.Last_Path
      Default_File = ''

      Filename = self.GetValue ()
      if Filename :
        path, file = path_split ( self.GetValue() )
        file, ext  = os.path.splitext ( file )
        if ext :
          Default_Path = path
          Default_File = '*' + ext

      File = AskFileForOpen ( Default_Path, Default_File, FileTypes )

      if File:
        Rel_FileName = Get_Relative_Path ( File, Application.Dir )
        self.SetValue ( Rel_FileName )
        self.P[0] = Rel_FileName
        self.Last_Path = path_split ( Rel_FileName )

  # *************************************************************
  # *************************************************************
  def SetForegroundColour ( self, color ) :
    self.Text.SetForegroundColour    ( color )
    self.Caption.SetForegroundColour ( color )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_C_Image_Show ( My_Control_Class ):

  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    self.Image = None
    self.Bmp   = None

    self.Dock.Bind ( wx.EVT_SIZE,             self.On_Image_Panel_Resize  )
    self.Dock.Bind ( wx.EVT_PAINT,            self.On_Image_Panel_Paint )
    self.Dock.Bind ( wx.EVT_ERASE_BACKGROUND, self.On_Image_Panel_Erase )

  # *************************************************************
  # *************************************************************
  def SetValue ( self, value ) :
    self.Image = value
    self.Image_Renew ()

  # *************************************************************
  # *************************************************************
  def On_Image_Panel_Paint ( self, event ):
    if self.Bmp is None:
      self.Image = wx.Image (100,100, True )
      self.Image_Renew ()
    dc = wx.BufferedPaintDC ( self.Dock )
    dc.Clear ()
    dc.DrawBitmap ( self.Bmp, 0, 0 )

  # *************************************************************
  # Essential, to prevent flicker !!
  # *************************************************************
  def On_Image_Panel_Erase ( self, event ) :
    pass

  # *************************************************************
  # *************************************************************
  def On_Image_Panel_Resize ( self, event ):
    event.Skip ()
    self.Image_Renew ()

  # *************************************************************
  # *************************************************************
  def Image_Renew ( self ):
    if self.Image :
      import picture_support
      self.Bmp = picture_support.Image_2_BMP_Resize ( self.Image,
                                                      self.Dock.GetClientSize() )
      self.Dock.Refresh ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_C_Buttons ( My_Control_Class ):

  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    if self.CD.Caption :
      Captions = self.CD.Caption
    else :
      Captions = 'Button'

    # Captions must be a list or tuple
    if isinstance ( Captions, str ) :
      Captions = [ Captions ]

    self.Buttons = []
    w, h = 50, 24
    for Caption in Captions :
      Button = wx.Button ( self.Dock, -1, Caption,
                           pos = ( self.X, self.Y ),
                           size = ( w, h ) )
      self.Buttons.append ( Button )
      self.X += w + 2

    self.dX = len ( Captions ) * ( w + 2 )
    self.dY = h

  # ******************************************
  # ******************************************
  def _On_Event ( self, event ) :
    """ Override, We need to detect the key pressed """
    event.Skip ()
    ID = event.GetId ()
    # Find the key that was pressed
    for i, Button in enumerate ( self.Buttons ) :
      if Button.GetId () == ID :
        self.P[0] = i
        break

  # ******************************************
  # ******************************************
  def GetSize ( self ) :
    """ Return size of the fixed multi-widget component """
    return self.dX, self.dY

  # ******************************************
  # ******************************************
  def SetForegroundColour ( self, color ) :
    for Button in self.Buttons :
      Button.SetForegroundColour ( color )

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_C_Slider ( Float_Slider, My_Control_Class ):

  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    R0, R1 = self.CD.Get ( 'Range', ( 1, 100 ) )

    Float_Slider.__init__ ( self, self.Dock,
                               caption  = self.CD.Caption,
                               minValue = R0,
                               maxValue = R1,
                               log      = self.CD.Get ( 'Log'   , False ),
                               format   = self.CD.Get ( 'Format', None  ) )

    
  # ******************************************
  # ******************************************
  def GetSize ( self ) :
    w, h = Float_Slider.GetSize ( self )
    return ( -1, h )
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class t_C_RadioBox ( wx.RadioBox, My_Control_Class ):

  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    NCol  = self.CD.Get ( 'NCol', 1 )
    Range = self.CD.Get ( 'Range', ( 'First', 'Second', 'Third' ) )

    wx.RadioBox.__init__ ( self,
            self.Dock, -1, self.CD.Caption,
            ( self.X-5, self.Y ), wx.DefaultSize,
            Range, NCol, wx.RA_SPECIFY_COLS )

    self.GetValue = self.GetSelection

  # ******************************************
  # ******************************************
  def SetValue ( self, value ) :
    if isinstance ( value, int ) :
      self.SetSelection ( value )

  # ******************************************
  # ******************************************
  def GetSize ( self ) :
    w, h = wx.RadioBox.GetSize ( self )
    return ( -1, h )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_C_Spin_Button ( wx.SpinCtrl, My_Control_Class ):

  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    if self.CD.Caption :
      self.Caption = wx.StaticText ( self.Dock, -1, self.CD.Caption,
                                     pos = ( self.X, self.Y + 3 ) )
      self.dX += My_Control_dX2

    self.w, self.h = 60, 22
    self.X += self.dX
    wx.SpinCtrl.__init__ ( self, self.Dock, wx.ID_ANY )
    try :
      self.SetRange ( self.CD.Range[0], self.CD.Range[1] )
    except :
      self.SetRange ( -10, 10 )

    self.dX += self.w
    self.dY += self.h
    
  # ******************************************
  # ******************************************
  def GetSize ( self ) :
    """ Return size of the fixed multi-widget component """
    return self.dX, self.dY

  # ******************************************
  # ******************************************
  def _On_Size ( self, event ):
    """ Sizing doesn't work well in init, so do it here """
    event.Skip ()
    self.SetSize     ( ( self.w, self.h ))
    self.SetPosition ( ( self.X, self.Y ))

  # *************************************************************
  def SetForegroundColour ( self, color ) :
    self.Caption.SetForegroundColour (       color )
    wx.SpinCtrl.SetForegroundColour  ( self, color )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_C_Text_Control ( wx.TextCtrl, My_Control_Class ):
  """ Display a label and an EditBox. """
  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    self.Type = str

    if self.CD.Caption :
      self.Caption = wx.StaticText ( self.Dock, -1, self.CD.Caption,
                                     pos = ( self.X, self.Y + 2 ) )
      dc = wx.ScreenDC()
      self.dX = dc.GetTextExtent ( self.CD.Caption )[0]
      self.dX = max ( self.dX, My_Control_dX2 )
      self.X += self.dX

    # determine our Size
    w        = 60
    self.dX += w + 10
    self.dY  = 24

    # wx.TE_PROCESS_ENTER is needed to catch ENTER-key
    wx.TextCtrl.__init__ ( self, self.Dock, -1,
                           size  = ( w,      self.dY ),
                           pos   = ( self.X, self.Y  ),
                           style = wx.TE_PROCESS_ENTER )

    # Focus lost or an Enter will activate the value
    self.Bind ( wx.EVT_KILL_FOCUS, self._On_Event )

  # ******************************************
  # ******************************************
  def GetSize ( self ) :
    """ Return size of the fixed multi-widget component """
    return self.dX, self.dY
  
  # ******************************************
  # ******************************************
  def _On_Size ( self, event ) :
    """ Override, we don't want sizing """

  # ******************************************
  # ******************************************
  def SetForegroundColour ( self, color ) :
    self.Caption.SetForegroundColour (       color )
    wx.TextCtrl.SetForegroundColour  ( self, color )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_C_LED ( My_Control_Class ):

  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    if self.CD.Caption :
      Caption = self.CD.Caption
    else :
      Caption = 'LED'

    self.Caption = wx.StaticText ( self.Dock, -1, Caption,
                                   pos = ( self.X, self.Y ) )
    self.Caption.SetBackgroundColour ( 'Yellow' )

    dc = wx.ScreenDC()
    self.dX, self.dY = dc.GetTextExtent ( self.CD.Caption )

  # ******************************************
  # ******************************************
  def GetSize ( self ) :
    """ Labels don't return a correct size """
    return self.dX, self.dY
# ***********************************************************************


# ***********************************************************************
# Becuase we want to position the variable text,
# we don't derive this directly from StaticText
# ***********************************************************************
class t_C_Static_Text ( My_Control_Class ):

  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    #self.dX, self.dY = 20,20 #self.CP.GetSize()
    self.dX += 5

    if self.CD.Caption :
      self.Caption = wx.StaticText ( self.Dock, -1, self.CD.Caption,
                                     pos = ( self.X, self.Y ) )

      dc = wx.ScreenDC()
      dx, dy = dc.GetTextExtent ( self.CD.Caption )
      self.dX += dx
      self.dY += dy

    self.Var_Text = wx.StaticText ( self.Dock, -1,
                             '??',
                             pos = ( self.X + 30, self.Y + 30) )

    self.Type = str
    self.GetValue = self.Var_Text.GetLabel

    if self.CD.FontSize :
      self.Var_Text.SetFont ( wx.FFont( self.CD.FontSize, wx.ROMAN ))
    if self.CD.FontColor :
      self.Var_Text.SetForegroundColour ( self.CD.FontColor )

  # *************************************
  # *************************************
  def SetValue ( self, Value ) :
    if not ( isinstance ( Value, str ) ) :
      Value = str ( Value )
    self.Var_Text.SetLabel ( Value )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_C_Color_Picker ( My_Control_Class ):

  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    self.CP = wx.ColourPickerCtrl ( self.Dock, -1, wx.RED,
                                    pos = ( self.X, self.Y ) )

    self.dX, self.dY = self.CP.GetSize()
    self.dX += 5

    if self.CD.Caption :
      self.Caption = wx.StaticText ( self.Dock, -1, self.CD.Caption,
                                     pos = ( self.X + self.dX, self.Y ) )

      dc = wx.ScreenDC()
      dx, dy = dc.GetTextExtent ( self.CD.Caption )
      self.dX += dx

    # SetValue, GetValue have different names
    self.SetValue = self.CP.SetColour
    self.GetValue = self.CP.GetColour

  # *************************************
  # *************************************
  def GetId ( self ) :
    # Return the slider's ID, so events can trigger on that
    return self.CP.GetId ()

  # ******************************************
  # ******************************************
  def GetSize ( self ) :
    """ Return size of the fixed multi-widget component """
    return self.dX, self.dY
# ***********************************************************************


pd_Module ( __file__ )
