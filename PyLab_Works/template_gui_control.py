import __init__
# ***********************************************************************
# <Description>
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007 <author>
# mailto: ...
# Please let me know if it works or not under different conditions
#
# <Version: x.y    ,dd-mm-yyyy, <author>
# Test Conditions: 1
#    - orginal release
#
# Test Conditions
# 1. WinXP-SP2, Python 2.4.3, wxPython wx-2.8-msw-ansi
# ***********************************************************************

"""
import os
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


# ***********************************************************************
# A simple form to test the control
# ***********************************************************************
class Simple_Test_Form ( wx.MiniFrame ):
  def __init__ ( self, ini = None ):
    # restore position and size
    if ini :
      ini.Section = 'Test'
      pos  = ini.Read ( 'Pos'  , ( 50, 50 ) )
      size = ini.Read ( 'Size' , ( 500, 300 ) )

    wx.MiniFrame.__init__(
      self, None, -1, 'Test PyLab Works GUI Control',
      size  = size,
      pos   = pos,
      style = wx.DEFAULT_FRAME_STYLE )

    # Create the control to be tested
    My_New_GUI_Control ( self, True, ini = ini )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class My_New_GUI_Control ( object ) :
  def __init__ ( self,  Dock,     # the frame/panel/... where we can put
                                  # the GUI controls that will catch events
                 Brick,           # the Brick, with its inputs and outputs
                 Test = False,    # if True, testmode with buildin examples
                 ini  = None ):   # inifile to store and reload settings

    self.Dock  = Dock
    self.Brick = Brick
    self.Test  = Test
    self.Ini   = ini

    # create the wx-components here and
    # set as parent : "self.Dock" !!
    # ....

    # *************************************************************
    # Create Sizers,
    # BUT let the parent do the resizing !!
    # *************************************************************
    Sizer = wx.BoxSizer ( wx.VERTICAL )
    Sizer.Add ( self.Html, 1, wx.EXPAND )
    Sizer.Add ( self.Panel, 0 )
    Dock.SetSizer ( Sizer )
    # *************************************************************
# ***********************************************************************



# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  app = wx.PySimpleApp ()
  ini = inifile ( 'test_My_New_GUI_Control.cfg' )
  frame = Simple_Test_Form (ini = ini)
  frame.Show ( True )
  app.MainLoop ()
  ini.Close ()
# ***********************************************************************

