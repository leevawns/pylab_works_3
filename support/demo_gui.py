import __init__
from gui_support import *

# ***********************************************************************
# ***********************************************************************
class Simple_Test_Form ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Simple GUI Demo', ini )
    bmp_IDE   = Get_Image_Resize ( 'applications-accessories.png', 48 )
    GUI2 = """
    self.Splitter          ,SplitterHor
      Panel2               ,PanelVer, 01
        p1                 ,wx.Panel
          B_IDE            ,BmpBut          ,bitmap = bmp_IDE  ,pos = (24,10) ,size=( 70,70)
          B_IDE_Run        ,wx.Button       ,label = "IDE"     ,pos = ( 0,80) ,size=(120,20)
        p2                 ,PanelVer, 00001
          p3               ,PanelHor, 11
            self.B_Toggle  ,wx.ToggleButton ,label = "Toggle"
            self.B_Button  ,wx.ToggleButton ,label = "Button"
          self.CB_CheckBox ,wx.CheckBox     ,label = 'Checkbox'
          self.CB_Another  ,wx.CheckBox     ,label = 'Another'
          self.RB_Test     ,wx.RadioBox     ,label = 'Tests', choices=['Original', 'All', 'Choice'] ,majorDimension=1 ,pos = (0,90)
          self.Text        ,wx.TextCtrl     ,style = wx.TE_MULTILINE
      self.NB              ,wx.Notebook     ,style = wx.NO_BORDER
        p4                 ,wx.Panel        ,name = 'First'
        p5                 ,wx.Panel        ,name = 'Second'
    """


    GUI = """
    self.Splitter   ,SplitterHor
      self.Text     ,wx.TextCtrl     ,style = wx.TE_MULTILINE
      self.NB       ,wx.Notebook
        p4          ,wx.Panel        ,name = 'First'
        p5          ,wx.Panel        ,name = 'Second'
    """
    self.wxGUI = Create_wxGUI ( GUI2, IniName = 'self.Ini_File' )


    self.Bind          ( wx.EVT_CLOSE,        self.On_Close    )
    #self.B_Toggle.Bind ( wx.EVT_TOGGLEBUTTON, self.On_B_Toggle )
    #self.B_Button.Bind ( wx.EVT_TOGGLEBUTTON, self.On_B_Button )

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

if __name__ == '__main__':
  My_Main_Application ( Simple_Test_Form )
