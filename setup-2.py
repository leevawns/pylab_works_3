import __init__root

#import __init__
from gui_support  import *
from menu_support import *

# ***********************************************************************
# ***********************************************************************
class _Fetch_Output ( object ) :
  def __init__ ( self, Log ) :
    self.Memo  = Log
    self.Star  = False
    self.Count = 0
  def write ( self, line ) :
    #line = line.replace ( '\n', '\n>>')
    if line == '\n' :
      if self.Star :
        return

    if line.startswith ( 'copying ' ) :
      line = '='
      self.Star = True
    elif  line.startswith ( 'byte-compiling ' ) :
      line = '*'
      self.Star = True
    elif  line.startswith ( 'creating ' ) :
      line = '+'
      self.Star = True
    else :
      if self.Star :
        line = '\n' + line
      self.Star = False
      self.Count = 0
      
    if self.Star :
      self.Count += 1
      
    if self.Count > 80 :
      line = '\n' + line
      self.Count = 0

    self.Memo.AppendText ( line )
    #self.Memo.GotoPos ( self.Memo.GetTextLength () )
    #self.Memo.EnsureCaretVisible()
    #self.Memo.DocumentEnd()
    wx.Yield()

  def flush ( self ):
    pass
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Simple_Test_Form ( My_Frame_Class, Menu_Event_Handler ) :
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Simple GUI Demo', ini )
    bmp_IDE   = Get_Image_Resize ( 'applications-accessories.png', 48 )

    GUI = """
    self.Splitter_Ver      ,SplitterVer
      self.Splitter_Hor    ,SplitterHor
        Button_Panel       ,PanelVer, 00000
          self.B_Toggle    ,wx.ToggleButton ,label = "Toggle"

        self.NB_Edit       ,wx.Notebook
          self.Edit        ,Base_STC  ,name = 'Setup'
          self.Edit_Log    ,Base_STC  ,name = 'Log'

      self.NB              ,wx.Notebook   ,style = wx.BK_LEFT
        P1                 ,PanelVer ,10  ,name = 'Shell'
          self.Log         ,Base_STC
        self.Html          ,Class_URL_Viewer ,name = 'Help'
        self.Grid          ,Base_Grid        ,name = 'File'
    """

    self.wxGUI = Create_wxGUI ( GUI, IniName = 'self.Ini_File' )
    #print self.wxGUI.code
    #print self.wxGUI.Current_Settings
    Set_NoteBook_Images ( self.NB, ( 206, 25, 9) )

    # *************************************************************
    self.MenuBar = Class_Menus ( self )
    # *************************************************************

    self.StatusBar = self.CreateStatusBar()
    self.StatusBar.SetFieldsCount(5)
    self.StatusBar_Controls = []
    # *************************************************************

    #sys.stdout = _Fetch_Output ( self.Log )
    #sys.stderr = self.Log
    wx.CallLater ( 500, self.Fetch_Outputs )

    self.Bind          ( wx.EVT_CLOSE,        self.On_Close    )
    #self.B_Toggle.Bind ( wx.EVT_TOGGLEBUTTON, self.On_B_Toggle )
    #self.B_Button.Bind ( wx.EVT_TOGGLEBUTTON, self.On_B_Button )

    self.Edit.Function_Key  = self.Function_Key
    print 'Einde'

  # **************************************************
  def Fetch_Outputs ( self ) :
    sys.stdout = _Fetch_Output ( self.Log )
    sys.stderr = self.Log

  # **************************************************
  def OnMenu_Open ( self, event ) :
    # pass the Open File to the focussed widget
    FW = self.FindFocus ()
    if hasattr ( FW, 'OnMenu_Open' ) :
      FW.OnMenu_Open ()
      if hasattr ( FW, 'Filename' ) and FW.Filename :
        self.Caption =  path_split ( FW.Filename ) [1]

  # *******************************************************
  # *******************************************************
  def Function_Key ( self, key ) :
    if key == 9 :
      self.SetCursor ( wx.StockCursor ( wx.CURSOR_WAIT ) )

      # save the file otherwise we can't use inspect
      self.Edit.SaveFile ( self.Edit.Filename )

      self.Globals = {}
      self.Globals [ 'stdout' ]  = self.Log
      #print 'Execute:', self.Edit.Filename
      execfile ( self.Edit.Filename, self.Globals )

      Filename = 'D:/Data_Python25_Dist/_launch_gui_support.exe.log'
      #Filename = self.Edit.Filename + '.log'
      print '****&&**', Filename
      if File_Exists ( Filename ) :
        self.Edit_Log.LoadFile ( Filename )

      self.SetCursor ( wx.StockCursor ( wx.CURSOR_DEFAULT ) )


  # *****************************************************
  def On_Close ( self, event ) :
    if self.Ini_File :
      self.Ini_File.Section = self.Ini_Section
      self.wxGUI.Save_Settings ()
    event.Skip()

  # ******************************************************
  def On_B_Toggle ( self, event ) :
    self.B_Button.SetValue ( not ( self.B_Toggle.GetValue() ) )
  def On_B_Button ( self, event ) :
    self.B_Toggle.SetValue ( not ( self.B_Button.GetValue () ) )
# ***********************************************************************

# ***********************************************************************
if __name__ == '__main__':
  My_Main_Application ( Simple_Test_Form )
# ***********************************************************************
