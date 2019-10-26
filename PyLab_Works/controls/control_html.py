import __init__

# ***********************************************************************
# Interactive html control for PyLab_Work
# Shows a html page with wxwidgets, so it can be used for
#   - coarse / help info
#   - instruction
#   - storing notes / answers
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2008 Stef Mientki
# mailto:S.Mientki@ru.nl
# Please let me know if it works or not under different conditions
#
# <Version: 1.0    , 13-01-2008, Stef Mientki
# Test Conditions: 1
#    - orginal release
#
# Test Conditions
# 1. WinXP-SP2, Python 2.4.3, wxPython wx-2.8-msw-ansi
# ***********************************************************************



# !!! import wx before any support library !!!
# otherwise the IDE won't do auto-suggest
import wx

from inifile_support import *

import  wx.html as  html
import  wx.lib.wxpTag


# ***********************************************************************
# Here all widgets must be imported, otherwise html can't find them
# ***********************************************************************
import wxp_widgets
import wxp_draw_widget
# ***********************************************************************


# ***********************************************************************
# A simple form to test the control
# ***********************************************************************
class Simple_Test_Form ( wx.MiniFrame ):
  def __init__ ( self, ini = None ):
    self.Ini = ini

    # restore position and size
    size = ( 500, 300 )
    pos = ( 50, 50 )
    if self.Ini :
      self.Ini.Section = 'General'
      pos  = self.Ini.Read ( 'Pos'  , pos )
      size = self.Ini.Read ( 'Size' , size )

    wx.MiniFrame.__init__(
      self, None, -1, 'Test PyLab Works GUI Control',
      size  = size,
      pos   = pos,
      style = wx.DEFAULT_FRAME_STYLE )

    # Create the control to be tested
    Html_Instruction ( self, None, True, self.Ini )
    self.Bind ( wx.EVT_CLOSE, self.OnClose )

  def OnClose ( self, event ) :
    if self.Ini :
      self.Ini.Section = 'General'
      self.Ini.Write ( 'Pos',  self.GetPosition () )
      self.Ini.Write ( 'Size', self.GetSize () )
    event.Skip ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Html_Instruction ( object ) :
  def __init__ ( self,  Dock,     # the frame/panel/... where we can put
                                  # the GUI controls that will catch events
                 Brick,           # the Brick, with its inputs and outputs
                 ini  = None,     # inifile to store and reload settings
                 Test = False ):  # if True, testmode with buildin examples

    self.Dock  = Dock
    self.Brick = Brick
    self.Test  = Test
    self.Ini   = ini

    self.Html = html.HtmlWindow ( self.Dock, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE)
    #self.html.SetRelatedFrame(parent, 'PageTitle : '+ "%s") #self.titleBase + " -- %s")
    #self.html.SetRelatedStatusBar(0)
    self.printer = html.HtmlEasyPrinting()

    self.Panel = wx.Panel ( self.Dock, -1 )
    self.Button_Print = wx.Button ( self.Panel, -1, "Print", pos = ( 0, 0 ) )
    self.Button_Print.Bind ( wx.EVT_BUTTON, self.OnPrint, self.Button_Print )

    # *************************************************************
    # *************************************************************
    Sizer = wx.BoxSizer ( wx.VERTICAL )
    Sizer.Add ( self.Html, 1, wx.EXPAND )
    Sizer.Add ( self.Panel, 0 )
    Dock.SetSizer ( Sizer )
    # *************************************************************

    self.Source_File = 'D:/data_to_test/aap_widget.html'
    """
    name_to = 'CSS_translated.html'
    wxp_widgets.Translate_CSS ( self.Source_File, name_to )
    self.Html.LoadPage ( name_to )
    """
    self.Html.Load_CSS ( self.Source_File )

  # *************************************************************
  # *************************************************************
  def OnPrint(self, event):
    name_to = '_Temp_dest_wxWidget.html'
    fields = self.Html.GetChildren ()
    wxp_widgets.Create_CSS_with_Answers ( fields, self.Source_File, name_to )

    self.printer.GetPrintData().SetPaperId ( wx.PAPER_A4 )
    self.printer.PrintFile ( name_to  )
# ***********************************************************************


# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  app = wx.PySimpleApp ()
  ini = inifile ( 'test_html_window.cfg' )
  frame = Simple_Test_Form ( ini = ini )
  frame.Show ( True )
  app.MainLoop ()
  ini.Close ()
# ***********************************************************************
pd_Module ( __file__ )





