import __init__


from language_support import  _
__doc__ = _(0, """
Scintilla Templates Manager,
License: freeware, under the terms of the BSD-license
Copyright (C) 2007 Stef Mientki
mailto:S.Mientki@ru.nl
""" )

# ***********************************************************************
_Version_Text = [

[ 1.1 , '01-01-2008', 'Stef Mientki',
'Test Conditions:', ( 1, ),
_(0, '- if editor open, follow the highlighted item')],


[ 1.0 , '21-12-2007', 'Stef Mientki',
'Test Conditions:', ( 1, ),
_(0, ' - original release')]
]
# ***********************************************************************


# ***********************************************************************
import  wx
import  wx.lib.newevent

from   inifile_support import inifile
from   picture_support import Get_Image_16
from   file_support import *
from   Scintilla_Editor import *
# ***********************************************************************


# ***********************************************************************
# we need a new event type to send a specific message to the device,
# after the table is changed by the user
# ***********************************************************************
#global EVT_SCINTILLA_TEMPLATE_INSERT
Scintilla_Templates_Event, EVT_SCINTILLA_TEMPLATE_INSERT = \
  wx.lib.newevent.NewEvent()
# ***********************************************************************


mouse_help = '\n(Right Click to copy snippet)'


# ***********************************************************************
# ***********************************************************************
class Scintilla_Templates_Form ( wx.Frame ) :
  def __init__ ( self, parent, title,
                 Pos = (50,50),
                 Size = (230,350),
                 Ini = None ):
    FormStyle = wx.DEFAULT_FRAME_STYLE | \
                wx.TINY_CAPTION_HORIZ
                #wx.STAY_ON_TOP
    self.parent = parent
    if self.parent:
      FormStyle = FormStyle | wx.FRAME_FLOAT_ON_PARENT    # needs a parent
    else :
      FormStyle = FormStyle | wx.STAY_ON_TOP
    self.ini = Ini
    self.Closing = False

    # read inifile if available
    self.Last_Editor_Pos = None
    self.Last_Editor_Size = ( 500, 300 )
    AP_start = 0
    if self.ini:
      try :
        self.ini.Section = 'Scintilla Templates'
        Pos = self.ini.Read ( 'Pos', Pos )
        Size = self.ini.Read ( 'Size', Size )
        AP_start = self.ini.Read ( 'Active Page', 0 )
        self.Last_Editor_Pos = self.ini.Read ( 'Editor Pos', None)
        self.Last_Editor_Size = self.ini.Read ( 'Editor Size', None )
      except:
        pass

    wx.Frame.__init__(
        self, parent, -1, title,
        size = Size,
        pos = Pos,
        style = FormStyle
        )

    Path = sys._getframe().f_code.co_filename
    Path = os.path.split ( Path ) [0]
    self.SetIcon ( wx.Icon (
      Joined_Paths ( Path, '../pictures/vippi_bricks_323.ico'),
      wx.BITMAP_TYPE_ICO))

    self.NB = wx.Notebook ( self, -1,
                       size = Size, #( -1, -1 ), #( 600, 400 ),
                       style = wx.BK_LEFT )
    #GUI = """
    #  self.NB  ,wx.Notebook ,style = wx.BK_LEFT
    #"""
    #self.wxGUI = Create_wxGUI ( GUI )


    self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED,  self.OnPageChanged)

    # Test if there's an ordered list available
    #path = path_split ( __file__ ) [0]
    path = sys._getframe().f_code.co_filename
    path = os.path.split ( path ) [0]
    filnam = os.path.join ( path, 'templates_.txt' )
    if File_Exists ( filnam ) :
      datafile = open ( filnam, 'r' )
      page_names = datafile.read()
      page_names = page_names.split('\n')
    else :
      page_names =[]

    # find all templates,
    # by looking for py-files with prefix "template_"
    filnam = os.path .join ( path, 'templates_*.py' )
    #print 'Templatesaa',filnam
    My_Files = glob.glob ( filnam )
    #print My_Files
    # strip off the path, because files should be in main program directory
    Tab_Names = []
    for i, file in enumerate ( My_Files ) :
      My_Files[i] = path_split ( file )[1]
      tab = os.path.splitext ( My_Files[i] ) [0] [10:]
      # if not in the ordered list, add
      if not ( tab in page_names ) :
        page_names.append ( tab )

    # Create all the tabs
    # make an image list (needed for notebook)
    self.image_list = wx.ImageList ( 16, 16)
    self.Pages = []
    self.Editors = []
    self.label = {}
    for page_name in page_names :
      # the None value at the end is a place holder for NCol
      self.Pages.append ( [ wx.Panel ( self.NB ), page_name, None ] )
      self.Editors.append ( None )

      AP = len ( self.Pages ) - 1
      self.NB.AddPage ( self.Pages [AP][0], page_name )
      self.panel.Bind ( wx.EVT_MOTION, self.OnMotion, self.panel)

    self.NB.SetImageList ( self.image_list )
    for AP in range ( len ( page_names ) ) :
      self.Reload_Page ( AP )

    self.Bind ( wx.EVT_SIZE,  self.OnResize )
    self.Bind ( wx.EVT_CLOSE, self.OnClose )

    # set the last selected page
    self.NB.SetSelection ( AP_start )
    self.Set_Page ( AP_start )
    #self.SendSizeEvent()
    #self.OnResize ( None )
    #self.NB.Update ()
    #wx.CallLater ( 500, self.NB.Refresh )
    self.Layout ()
    wx.CallLater ( 1500, self.OnResize, None )
    #wx.CallLater ( 500, self.NB.Update )
    #wx.CallLater ( 1000, self.Layout )
    #wx.CallLater ( 500, self.SendSizeEvent )

  # *****************************************************************
  # *****************************************************************
  def Reload_Page ( self, AP ) :
    # generate the snippet table
    #path = path_split ( __file__ ) [0]
    path = sys._getframe().f_code.co_filename
    path = os.path.split ( path ) [0]
    
    filnam = 'templates_' + self.Pages [AP][1] +'.py'
    filnam = os.path.join ( path, filnam )
    Icon, NCol, snippets = Get_Templates_From_File ( filnam )
    self.Pages [AP][2] = NCol

    if Icon :
      try :
        icon = self.image_list.Add ( Get_Image_16 ( Icon ) )
        self.NB.SetPageImage( AP, icon )
      except :
        pass
    else :
      self.NB.SetPageImage( AP, -1 )

    if NCol :
      self.panel = self.Pages[AP][0]
      
      # remove everything
      for item in self.panel.GetChildren () :
        item.Destroy()

      # add all descriptions to the table
      x = y = 0
      w,h = self.panel.GetSize()
      w = ( w / NCol ) - 5

      N = 0
      for i,snippet in enumerate ( snippets ) :
        x = x + N * ( w + 5 )
        if snippet [0] == '|':
          N += 1
          y = 0
          snip = wx.StaticLine ( self.panel, wx.ID_ANY,
                                 ( 50, 0 ),
                                 ( N,h ))
        else :
          if snippet[0] == '-' :
            snip = wx.StaticLine ( self.panel, wx.ID_ANY,
                                   ( x, 7 + y*15),
                                   ( 7 + ( 1+y ) * 15, 2))
          else :
            snip = wx.StaticText ( self.panel, wx.ID_ANY, snippet[0],
                                   (5 + x, 5 + y*15),
                                   (w, -1) )
            snip.Bind ( wx.EVT_MOTION, self.OnMotion, snip )
            snip.Bind ( wx.EVT_LEFT_DOWN, self.OnLeftDown, snip )
            snip.Bind ( wx.EVT_RIGHT_DOWN, self.OnRightDown, snip )
            if snippet[1] :
              snip.SetToolTipString ( snippet[1] + mouse_help )
            self.label [snip.GetId()] = ( snip, snippet[2] )

          # we use the minsize to store x,y coordinates
          snip.SetMinSize ( ( N, y ) )

          y += 1

  # *****************************************************************
  # *****************************************************************
  def OnEditorClose ( self, event ) :
    # search the page of the closed editor
    for i,item in enumerate ( self.Editors ):
      if item and ( event.GetId() == item.GetId() ) :
        break

    # save the size of the template editor
    self.Last_Editor_Pos  = item.GetScreenPosition()
    self.Last_Editor_Size = item.GetSize()

    # perform the normal actions of the editor
    item.OnClose ( event )

    if not ( self.Closing ) :
      # reload pages
      self.Reload_Page (i)
      self.Editors [i] = None
      self.SendSizeEvent()


  # *****************************************************************
  # *****************************************************************
  def OnResize ( self, event ):
    NCol = self.Pages [ self.Active_Index ][ 2 ]
    w, h = self.panel.GetSize()
    w = ( w / NCol ) - 5

    for item in self.panel.GetChildren() :
      # remember the position is stored in MinSize
      N,M = item.GetMinSize()
      x = 5 + N * ( w + 5 )

      if isinstance ( item, wx.StaticLine ) :
        if item.GetPosition()[1] == 0 :
          item.SetSize ( ( 2, h ) )
          item.SetPosition ( ( x-5, 0 ) )
          d = -1
        else :
          d = 7
      else :
        d = 0
      if d>=0 :
        y = d + M * 15
        item.SetSize ( ( w, -1 ) )
        item.SetPosition ( ( x, y ) )

    if event :
      event.Skip()

  # *****************************************************************
  # Occures just after another TAB is selected
  # *****************************************************************
  def OnPageChanged( self, event ):
    new = event.GetSelection()
    self.Set_Page ( new )
    event.Skip()

  # *****************************************************************
  # *****************************************************************
  def Set_Page ( self, index ) :
    self.Active_Index = index
    self.panel = self.Pages [ self.Active_Index ] [0]
    self.HL = None
    #self.SendSizeEvent()
    wx.CallLater ( 100, self.OnResize, None )


  # *****************************************************************
  # *****************************************************************
  def OnMotion ( self, event ) :
    ID = event.GetId()
    if self.HL == ID :
      return

    if self.HL != self.panel.GetId () :
      try :
        self.label[self.HL][0].SetBackgroundColour (
                                 self.panel.GetBackgroundColour())
        self.label[self.HL][0].Refresh ()
      except :
        pass

    self.HL = ID
    try:
      self.label[ID][0].SetBackgroundColour ( 'Yellow' )
      self.label[ID][0].Refresh ()
      
      """
      # and if editor open, follow
      Edit = self.Editors [self.Active_Index]
      if Edit :
        Edit.Search ( self.label[ID][0].GetLabel () )
      """
    except:
      pass


  # *****************************************************************
  # *****************************************************************
  def OnLeftDown ( self, event ) :
    self.Action_Open ( event )

  # *****************************************************************
  # *****************************************************************
  def OnRightDown ( self, event ):
    self.Action_Copy ( event )
    ##??self.Action_Open ( event )

  # *****************************************************************
  # Post a message to the parent or copy to clipboard
  # *****************************************************************
  def Action_Copy ( self, event ) :
    ID = event.GetId ()
    if self.parent :
      new_evt = Scintilla_Templates_Event (
                  data = self.label[ID][1] )
      wx.PostEvent ( self.parent , new_evt )
    else :
      #print self.label [ID] [1]
      data = wx.TextDataObject ()
      data.SetText ( self.label [ID] [1] )
      if wx.TheClipboard.Open ():
        wx.TheClipboard.SetData ( data )
        wx.TheClipboard.Close ()
      else:
        wx.MessageBox ( "Unable to open the clipboard", "Error" )

  # *****************************************************************
  # Opens the templates if not yet open
  # and goes to the selected label
  # *****************************************************************
  def Action_Open ( self, event ) :
    # get the label_clicked !!
    ID = event.GetId ()
    #label = self.panel.FindWindowById ( ID )
    label = self.label[ID][0]

    NCol = self.Pages [self.Active_Index][2]
    w, h = self.panel.GetSize()
    w = ( w / NCol ) - 5
    N,M = label.GetMinSize()
    x = 5 + N * ( w + 5 )

    x2, y = event.GetPosition ()
    x0, y0 = self.GetPosition ()

    #path = path_split ( __file__ ) [0]
    path = sys._getframe().f_code.co_filename
    path = os.path.split ( path ) [0]
    
    filnam = 'templates_' + self.Pages [self.Active_Index][1] +'.py'
    filnam = os.path.join ( path, filnam )
    Edit = self.Editors [self.Active_Index]
    if Edit :
      Edit.Search ( label.GetLabel () )
    else :
      if self.Last_Editor_Pos:
        pos = self.Last_Editor_Pos
      else:
        pos = ( x + x0 + x2 + 40, y + y0 +30)
      Edit = Scintilla_Editor (
                     None, filnam,             #None so these don't stay on top !
                     label.GetLabel (),
                     size = self.Last_Editor_Size,
                     pos = pos )
      Edit.Show ( True )
      Edit.Bind (wx.EVT_CLOSE, self.OnEditorClose, Edit )
      self.Editors [self.Active_Index] = Edit

  # *****************************************************************
  # *****************************************************************
  def OnClose ( self, event ) :
    if self.ini:
      self.ini.Section = 'Scintilla Templates'
      self.ini.Write ( 'Pos', self.GetPosition() )
      self.ini.Write ( 'Size', self.GetSize() )
      self.ini.Write ( 'Active Page', self.Active_Index )
      try:
        self.ini.Write ( 'Editor Pos', self.Last_Editor_Pos )
        self.ini.Write ( 'Editor Size', self.Last_Editor_Size )
      except:
        pass
      
    # close all editors
    self.Closing = True
    for Edit in self.Editors :
      if Edit:
        Edit.Close();

    event.Skip()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Templates_From_File ( filnam ):
  if not ( File_Exists ( filnam ) ) :
    return None, None, None
  datafile = open ( filnam, 'r' )
  data = datafile.read()
  data = data.split('##')
  
  # test for picture
  if (len(data)>1) and ( data[0].find('#icon')==0) :
    Icon = data[0].split('=')[1].strip()
    data = data [1:]
  else:
    Icon = None

  snippets = []
  NCol = 1
  for item in data :
    lines = item.split('\n')
    description = lines[0].strip()
    hint = None
    code = None
    if description == None :    # ignore empty items
      pass
    elif description == '-' :   # insert horizontal line
      pass
    elif description == '|' :   # insert vertical line (create new column)
      NCol += 1
    else :                      # normal processing of an item
      # Restore the lines to one item, but without the description
      a = '\n'.join ( lines[1:] )
      # Split the hint and the code (hint might be absent)
      line = a.split('"""')
      if len ( line )  == 3 :
        hint = line[1].strip()
        code = line[2].strip()
      else :  # if not hint text available
        code = line[0].strip()
    if description :
      snippets.append ( ( description, hint, code ) )
  return Icon, NCol, snippets
# ***********************************************************************



# ***********************************************************************
# demo program, showing a properties table that can be edited
# ***********************************************************************
if __name__ == '__main__':
  app = wx.PySimpleApp()

  filename = 'Scintilla_Templates_test.ini'
  ini = inifile ( filename )


  frame = Scintilla_Templates_Form ( None, "Program Snippets",
             Ini = ini )
  frame.Show(True)
  app.MainLoop()
  
  ini.Close()
# ***********************************************************************

