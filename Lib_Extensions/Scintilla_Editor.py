import __init__
# ***********************************************************************
# Displays a Scintilla Editor in a separate window that floats on parent.
# You can specify the file that should be opened.
# You can specify the line where the editor should jump to,
# either by a search text or a linenumber.
# Searchtext has a higher priority than linenumber,
# but if searchtext didn't succeed, jump to linenumber is done.
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007 Stef Mientki
# mailto:S.Mientki@ru.nl
# Please let me know if it works or not under different conditions
#
# <Version: 1.0    ,21-12-2007, Stef Mientki
# Test Conditions: 1
#    - orginal release
#
# Test Conditions
# 1. WinXP-SP2, Python 2.4.3, wxPython wx-2.8-msw-ansi
# ***********************************************************************


# ***********************************************************************
# add some standard library paths
# ***********************************************************************
"""
import sys
subdirs = [ '../support' ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
"""
from   file_support import *

#from   Scintilla_Python import *
from   Scintilla_support import *
import  wx
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Scintilla_Editor ( wx.MiniFrame ) :
  def __init__ ( self, parent,
                 filename,
                 searchtext = '',
                 gotoline = -1,
                 size = ( 500, 300 ) ,
                 pos = ( 150, 150 ) ):
    FormStyle = wx.DEFAULT_FRAME_STYLE | \
                wx.TINY_CAPTION_HORIZ
                #wx.STAY_ON_TOP
    self.parent = parent
    self.filename = filename
    if self.parent:
      FormStyle = FormStyle | wx.FRAME_FLOAT_ON_PARENT    # needs a parent

    wx.MiniFrame.__init__(
      self, parent, -1, self.filename,
      size = size,
      pos = pos,
      style = FormStyle
      )
    #self.STC = PythonSTC ( self, wx.ID_ANY )
    self.STC = Base_STC ( self, wx.ID_ANY )

    # try to load the file
    if File_Exists ( self.filename ) :
      self.STC.LoadFile ( self.filename )
      #self.Search ( searchtext, gotoline )

    # detect close event
    self.Bind ( wx.EVT_CLOSE, self.OnClose )

  # *****************************************************************
  # search text in document
  # *****************************************************************
  def Search ( self, searchtext='', gotoline=-1 ):
    if searchtext :
      # first go to the end of the document,
      # search backwards, so the result will be on top of display
      self.STC.DocumentEnd()
      self.STC.SearchNext ( 0, searchtext )
      if self.STC.GetCurrentPos() > 0 :
        linenr = self.STC.LineFromPosition ( self.STC.GetCurrentPos () )
      else :
        # if searchtext not found, try linenumber
        linenr = gotoline
    else :
      # goto linenr ?
      linenr = gotoline

    if linenr >= 0 :
      self.STC.GotoLine (linenr)

  # *****************************************************************
  # save file, if modified
  # *****************************************************************
  def OnClose ( self, event ):
    if  self.STC.GetModify () :
      self.STC.SaveFile ( self.filename )
    self.Destroy ()
# ***********************************************************************


# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  app = wx.PySimpleApp()
  Main_File = '../PyLab_Works/test_IDE.py'
  frame = Scintilla_Editor ( None, Main_File )
  frame.Show(True)
  app.MainLoop()
# ***********************************************************************

