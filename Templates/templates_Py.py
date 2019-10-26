#icon = python.png
## Version - header
# If the module has run standalone and
# is located in a different path from language_support
# be sure we can reach language_support
import sys
subdir = '../support'
if not ( subdir in sys.path ) :
  sys.path.append ( subdir )

from language_support import  _
__doc__ = _(0,"""
Doc string
""")

_Version_Text = [
[ 1.0 , '32-10-2008', 'Stef Mientki',
'Test Conditions:', ( 2,3, ),
_(0, ' - original release')]
]

from General_Globals import *
# ***********************************************************************

## Main GUI
# ***********************************************************************
# ***********************************************************************
class Simple_Test_Form ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Simple GUI Demo', ini )

    GUI = """
    Splitter1       ,SplitterVer
      Panel_Top     ,wx.Panel
      Panel_Bottom  ,wx.Panel
        Button_1    ,wx.Button,  label = "Test"
        Button_2    ,wx.Button,  label = "Test2", pos = (100,0)
    """
    self.wxGUI = Create_wxGUI ( GUI )

# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  My_Main_Application ( Simple_Test_Form )
# ***********************************************************************
pd_Module ( __file__ )


## PyLab_Works GUI
# If the module has run standalone and
# is located in a different path from language_support
# be sure we can reach language_support
import __init__

from language_support import  _
__doc__ = _(0,"""
Doc string
""")

_Version_Text = [
[ 1.0 , '32-10-2008', 'Stef Mientki',
'Test Conditions:', ( 2,3, ),
_(0, ' - original release')]
]

from General_Globals import *
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class Simple_Test_Form ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Simple GUI Demo', ini )

    GUI = """
    Splitter1       ,SplitterVer
      Panel_Top     ,wx.Panel
      Panel_Bottom  ,wx.Panel
        Button_1    ,wx.Button,  label = "Test"
        Button_2    ,wx.Button,  label = "Test2", pos = (100,0)
    """
    self.wxGUI = Create_wxGUI ( GUI )

# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  My_Main_Application ( Simple_Test_Form )
# ***********************************************************************
pd_Module ( __file__ )


##OnSomeEvent
"""
Shows some general aspects of and event handler
"""
  def OnSomeEvent ( self, event ) :
    # valid for all events
    ID = event.GetId()
    # explore the events, not all listed events will hold meaningfull data
    print dir ( event )
    # some common properties
    x, y = event.GetPosition ()
    # if more has to be done by other eventhandlers
    event.Skip()


##OnClose
"""
General actions in and OnClose event
"""
  # *****************************************************************
  # save file, if modified
  # *****************************************************************
  def OnClose ( self, event ) :
    if  self.STC.GetModify () :
      self.STC.SaveFile ( self.filename )
    self.Destroy ()


##2new program
"""
extended hintt description
and more lines of explaining text
"""
# -----------------------------------------------------------------------------
# New Program
# based on RPD
# -----------------------------------------------------------------------------
# include hardware definitions
for i in range (1, 5) :
  print i


##Timer
"""
Creating and timer and starting it
"""
    # Timer to test dynamic updating of grid
    self.Timer = wx.Timer ( self )
    # the third parameter is essential to allow other timers
    self.Bind ( wx.EVT_TIMER, self.OnTimer, self.Timer)
    self.Timer.Start ( 2000 )

##Generating an Event
"""
How to programmatically create an event
"""
    MyWindow.SendSizeEvent()


    new_evt = JALsPy_Properties_Event(  device = self.device, data = new_table.data )
    try: wx.PostEvent ( self.device.my_Container , new_evt )
    except: pass


##Color Conversion
"""Several ways to convert colors"""
  # Converting and tuple (3 or 4 values to a color)
  color = ( 0, 255, 0, 255 )
  color = ( 0, 255, 0 )
  if not ( isinstance ( color, wx.Colour ) ) :
    color = wx.Color ( *color )

  # simple way to reduce intensity
  a = 3
  rgb = [self.Color.Red()/a, self.Color.Green()/a, self.Color.Blue()/a]
  dc.SetBrush   ( wx.Brush (wx.Color(*rgb) ) )


  # from the standard module "colorsys"
  rgb_to_yiq( r, g, b) 
  yiq_to_rgb( y, i, q) 
  rgb_to_hls( r, g, b) 
  hls_to_rgb( h, l, s) 
  rgb_to_hsv( r, g, b) 
  hsv_to_rgb( h, s, v) 

##Clipboard
"""Copy Canvas to Clipboard (text is almost identical)"""
  # *********************************************************
  #  Ctrl-C = copy Canvas to clipboard
  # *********************************************************
  def _On_Key_Down ( self, event ) :
    key = event.GetKeyCode()
    if key == ord('C') and event.ControlDown():
      data = wx.BitmapDataObject()
      data.SetBitmap ( self._Paint_Buffer )
      if wx.TheClipboard.Open () :
        wx.TheClipboard.SetData ( data )
        wx.TheClipboard.Close ()



##Sizers
"""A simple method with boxsizers is described 
that is sufficient in most cases"""
  # Important is that the container is a wx.Panel (and not and wx.Window)
  self.Panel = wx.Panel ( self.Splitter, style = wx.BORDER_SUNKEN )
  
  # Now add components to the container
  self.Panel_Top = wx.Panel ( self.Panel, style = wx.BORDER_SUNKEN )
  self.Panel_Bottom = wx.Panel ( self.Panel, style = wx.BORDER_SUNKEN )

  # Create and BoxSizer and connect it to the container
  Sizer = wx.BoxSizer ( wx.VERTICAL )
  self.Panel.SetSizer ( Sizer )

  # All the components added to the container, must also added to the BoxSizer
  Sizer.Add ( self.Panel_Top, 0, wx.EXPAND )
  Sizer.Add ( self.Panel_Bottom, 0, wx.EXPAND )





##-

## module path
    # DON'T USE: path = os.path.split ( __file__ ) [0]
    path = path_split ( __file__ ) [0]
    filnam = 'templates_.py' 
    filnam = os.path.join ( path, filnam )
##-
##Inspect
"""
getdoc( object) 
  Get the documentation string for an object. All tabs are expanded to spaces. To clean up docstrings that are indented to line up with blocks of code, any whitespace than can be uniformly removed from the second line onwards is removed. 
getcomments( object) 
  Return in a single string any lines of comments immediately preceding the object's source code (for a class, function, or method), or at the top of the Python source file (if the object is a module). 
getfile( object) 
  Return the name of the (text or binary) file in which an object was defined. This will fail with a TypeError if the object is a built-in module, class, or function. 
getmodule( object) 
  Try to guess which module an object was defined in. 
getsourcefile( object) 
  Return the name of the Python source file in which an object was defined. This will fail with a TypeError if the object is a built-in module, class, or function. 
getsourcelines( object) 
  Return a list of source lines and starting line number for an object. The argument may be a module, class, method, function, traceback, frame, or code object. The source code is returned as a list of the lines corresponding to the object and the line number indicates where in the original source file the first line of code was found. An IOError is raised if the source code cannot be retrieved. 
getsource( object) 
  Return the text of the source code for an object. The argument may be a module, class, method, function, traceback, frame, or code object. The source code is returned as a single string. An IOError is raised if the source code cannot be retrieved. 
"""
##pyclbr
##|


## MAIN
"""
A complete template for a new library,
including a main section to run standalone.
"""
import  __init__

# !!! import wx before any support library !!!
# otherwise the IDE won't do auto-suggest
import wx

from dialog_support import *
from inifile_support import *

# ***********************************************************************
# ***********************************************************************
class My_MainForm ( wx.Frame, Menu_Event_Handler):
  def __init__ ( self, ini = None ) :
    # Create the frame, according to some default settings
    wx.Frame.__init__( self, None, -1, "No Title", pos=(0,0), size=(800,600))

    # read settings from inifile
    self.Ini = ini
    if self.Ini :
      self.Load_Settings ( self.Ini )

    # DO YOUR STUFF
    
    # Capture OnClose event to be able to save settings
    self.Closed = False
    self.Bind ( wx.EVT_CLOSE, self.OnCloseWindow )

  def OnCloseWindow ( self, event ) :
    # This might be called more than once,
    # therefor we use self.closed !!
    if not ( self.Closed ) :
      self.Closed = True
      self.Save_Settings ( self.Ini )
    event.Skip ()

  def Save_Settings ( self, ini ):
    ini.Section = 'General'
    ini.Write ( 'Pos',  self.GetPosition() )
    ini.Write ( 'Size', self.GetSize() )
    # do some more saving ....

  def Load_Settings ( self, ini ):
    ini.Section = 'General'
    self.SetPosition ( ini.Read ( 'Pos'  , ( 50,  50  ) ) )
    self.SetSize     ( ini.Read ( 'Size' , ( 800, 600 ) ) )
    # Load some other settings ...



# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  app = wx.PySimpleApp ()
  ini = inifile ( 'test_.....cfg' )
  frame = My_Form ( None, -1, "Window Caption",
                            size=(700, 500),
                            style = wx.DEFAULT_FRAME_STYLE)
  frame.Show ( True )
  app.MainLoop ()
  ini.Close ()
# ***********************************************************************


## MAIN dialog
"""
Create a Dialog Library, with a main section,
Use "MAIN" first, then change the following parts.
"""
# ***********************************************************************
# ***********************************************************************
class My_Dialog ( wx.Dialog ):

  def __init__ ( self, ini = None ) :
    wx.Dialog.__init__ ( self, None, -1, "No Title", pos=(20,20), size=(600,400)
                         # if we don't want the user to scale the window,
                         # remove the next line
                         ,style = wx.DEFAULT_FRAME_STYLE
                         )

    # WHEN USING A TEXTCTRL IN A DIALOG WINDOW,
    # BE SURE TO SET "wx.WANTS_CHARS",
    # OTHERWISE, ARROW KEYS WILL MOVE TO OTHER COMPONENTS
    #self.rtc = rt.RichTextCtrl ( self,
    #             style = wx.VSCROLL|wx.HSCROLL|wx.NO_BORDER \
    #                     |wx.TE_MULTILINE|wx.TE_PROCESS_ENTER \
    #                     |wx.WANTS_CHARS );    # VERY ESSENTIAL TO CATCH ARROW KEYS


# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  app = wx.PySimpleApp ()
  ini = inifile ( 'test_....cfg' )
  dialog = My_Dialog ( None, -1, "Window Caption",
                       size=(500, 400),
                       pos = ( 50,50),
                       style = wx.DEFAULT_FRAME_STYLE)
  result = dialog.ShowModal ()
  print 'Result:',result
  ini.Close ()
  # we don't need the main application to run
  # but instead we need to destroy the dialog
  dialog.Destroy()
# ***********************************************************************



## Spin Button
"""
Insert SpinButton and event handling
"""
    self.Spin = wx.SpinCtrl ( self.Panel_Type, -1, pos=(125,30), size=(50,-1))
    self.Spin.SetRange ( 6, 30 )
    self.Spin.SetValue ( 8 )
    self.Spin.Bind ( wx.EVT_SPINCTRL, self.OnSpinEvent, self.Spin )

  # *************************************************************
  # *************************************************************
  def OnSpinEvent ( self, event ) :
    value = event.GetInt()


## Combo Dropdown list
"""
Insert Combo and event handling
"""

    self.Combo = wx.ComboBox ( self.Panel_Type, 500, "Arial",
                               pos = ( 5, 5 ), size = ( 170, -1 ),
                               choices = a.fonts,
                               style = wx.CB_DROPDOWN
                               #| wx.TE_PROCESS_ENTER
                               #| wx.CB_SORT
                             )
    self.Combo.Bind ( wx.EVT_COMBOBOX, self.OnComboEvent, self.Combo )

  # *************************************************************
  # *************************************************************
  def OnComboEvent ( self, event ) :
    value = event.GetString()


## Color Picker
"""
Insert Color Picker and event handling
"""
    self.CP_Font = wx.ColourPickerCtrl ( self.Panel_Type, -1, 'blue',
                                         pos = (65,30))
    self.CP_Font.Bind ( wx.EVT_COLOURPICKER_CHANGED,
                        self.OnFontColor, self.CP_Font)

  # *************************************************************
  # *************************************************************
  def OnFontColor ( self, event ) :
    # make it a tupple, for easier handling
    color = tuple ( self.CP_Font.GetColour () )


## Text Box
"""
Insert TextBox and event handling
"""
    self.Font_Char = wx.TextCtrl( self.Panel_Type, -1,
                         size=(30, -1), pos = ( 55,90) )
                         #,style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
    self.Font_Char.Bind ( wx.EVT_TEXT, self.OnCharFont, self.Font_Char )

  # *************************************************************
  # *************************************************************
  def OnCharFont ( self, event ) :
    value = event.GetString ()


## CheckListBox
"""
Insert CheckListBox and event handling
"""
    self.lb_Style = wx.CheckListBox ( self.Panel_Type, -1,
      pos = ( 185, 25 ), size = ( 100,100 ),
      choices = ['Bold', 'Italic', 'UnderLine', 'StrikeOut' ] )
    self.lb_Style.Bind ( wx.EVT_CHECKLISTBOX, self.OnStyleEvent, self.lb_Style )

  # *************************************************************
  # *************************************************************
  def OnStyleEvent ( self, event ) :
    # Get the changed index and value:
    # Note: event.Checked() doesn't work !!
    index = event.GetInt()
    print self.lb_Style.IsChecked ( index ) )

    # enumerate over all the items in the checkboxlist
    for i, item in enumerate ( self.lb_Style.GetItems()) :
      print item, '=', self.lb_Style.IsChecked (i)


## RadioBox
"""
Insert RadioBox and event handling
"""
    self.RB = wx.RadioBox(self.Panel_Type, -1, "Title",
              (90,50), wx.DefaultSize,
              ['Normal', 'SuperScript', 'SubScript'] ,
              1 )  # number of columns
    self.RB.SetSelection ( 1 )
    self.RB.Bind ( wx.EVT_RADIOBOX, self.OnEventRB, self.RB )

  # *************************************************************
  # *************************************************************
  def OnRBEvent ( self, event ) :
    value = event.GetInt ()


## Ctrl-V event
"""
Catching Ctrl-V event
"""
    self.Text.Bind ( wx.EVT_KEY_DOWN, self.OnKeyDown )

  # Because Ctrl-V is not supported, we catch it here
  def OnKeyDown ( self, event ) :
    if (event.GetKeyCode() == 86 ) and event.ControlDown() :
      self.Text.Paste()
    event.Skip ()

## File Handling
"""
All kind of file manipulations, see the source code
"""
  result = subprocess.Popen (  [filename, params]  )   #run no-wait
  result = subprocess.call (  [filename, params]  )         # run + wait

  os.remove ( filename )

##-
## Tree Support
## - Create
## - Clear
## - Load / Save
## - Add Nodes
