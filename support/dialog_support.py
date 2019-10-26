import __init__

# ***********************************************************************
from language_support import _

__doc__ = """
License: freeware, under the terms of the BSD-license
Copyright (C) 2008 Stef Mientki
mailto:S.Mientki@ru.nl
"""

_Version_Text = [

[ 1.4 , '11-04-2009', 'Stef Mientki',
'Test Conditions:', (3,),
"""
 - Color_Dialog now alwaays returns None, if canceled
"""],

[ 1.3 , '06-12-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - Multiline dialog, if just 1 preset item, OK-button gets focus
""")],

[ 1.2 , '23-11-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - ColorDialog added
 - Ask_File_For_Save, now also accepts an integer for the filetype
""")],

[ 1.1 , '10-03-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, ' - AskYesNo, now returns True or False')],

[ 1.0 , '09-04-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, ' - orginal release')]
]
# ***********************************************************************


from General_Globals import *

# ***********************************************************************
# ***********************************************************************
import wx
import os

global MLD_FILE, MLD_PATH
MLD_FILE = 1
MLD_PATH = 2

FT_IMAGE_FILES = 1
FT_ALL_FILES   = 2
FT_DBASE_FILES = 3
FT_PY_FILES    = 4
FT_DOC_FILES   = 5


_FT_IMAGE_FILES =\
   'All Image Files|*.ani;*.bmp;*.cur;*.gif;*.ico;*.iff;'\
                   '*.jp;*.pcx;*.png;*.pnm;*.tif;*.xpm'\
  '|ANI format|*.ani'\
  '|BMP format|*.bmp'\
  '|CUR format|*.cur'\
  '|GIF format|*.gif'\
  '|ICO format|*.ico'\
  '|IFF format|*.iff'\
  '|JPG format|*.jp*'\
  '|PCX format|*.pcx'\
  '|PNG format|*.png'\
  '|PNM format|*.pnm'\
  '|TIF format|*.tif*'\
  '|XPM format|*.xpm'\
  '|All Files (*.*)|*.*'

_FT_ALL_FILES =\
  'All Files (*.*)|*.*'

_FT_DBASE_FILES =\
  'dBase Files (*.db)|*.db|' \
  'All Files (*.*)|*.*'


_FT_PY_FILES =\
  'Python Files (*.py)|*.py|' \
  'All Files (*.*)|*.*'

_FT_DOC_FILES =\
  'HTML Files (*.html)|*.html|' \
  'Text Files (*.txt)|*.txt|'\
  'PDF Files (*.pdf)|*.pdf|'\
  'Flash Files (*.swf)|*.swf|'\
  'Windows Help Files (*.chm)|*.chm|'\
  'Doc Files (*.doc*)|*.doc*|'\
  'Excel Files (*.xls*)|*.xls*|'\
  'PowerPoint Files (*.ppt*)|*.ppt*|'\
  'All Files (*.*)|*.*'

_FT_Collection = {
  FT_IMAGE_FILES : _FT_IMAGE_FILES,
  FT_ALL_FILES   : _FT_ALL_FILES,
  FT_DBASE_FILES : _FT_DBASE_FILES,
  FT_PY_FILES    : _FT_PY_FILES,
  FT_DOC_FILES   : _FT_DOC_FILES,
  }

# ***********************************************************************
# ***********************************************************************
_Color_Set = []
def Color_Dialog ( Parent = None, Color = None ) :
  colordlg = wx.ColourDialog ( Parent )
  colordlg.GetColourData().SetChooseFull ( True )

  global _Color_Set
  if _Color_Set :
    for i,color in enumerate ( _Color_Set ) :
      colordlg.GetColourData().SetCustomColour ( i, color )

  colordlg.GetColourData().SetColour ( Color )
  Color = None
  if colordlg.ShowModal() == wx.ID_OK:
    Color = colordlg.GetColourData().GetColour()

    _Color_Set = []
    for i in range ( 16 ):
      _Color_Set.append ( colordlg.GetColourData().GetCustomColour (i) )

  colordlg.Destroy()
  return Color
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Show_Message (  text ) :
  dialog = wx.MessageDialog ( None, text, style = wx.OK )
  dialog.ShowModal()
  dialog.Destroy ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def _Wrap_No_GUI ( target ):
  """
  Decorator that creates an wx.App is it's not yet there,
  so wx functions can be used in terminal mode applications.
  The actions that are performed:
    - Create the wx.App, it it doesn't exist
    - run the normal wx-dialog function (or any other wx-form)
    - Kill the application if it was created here
  """
  def wrapper ( *args, **kwargs ) :
    ##v3print ( 'BEFORE', target.__name__ )
    # Create the Application if it doesn't exists
    _dummy_app = None
    if not (wx.GetApp () ):
      _dummy_app = wx.PySimpleApp ()

    # perform the called target function
    result = target ( *args, **kwargs )

    # Destroy the wx.App, if it was created here
    ##v3print ( 'AFTER', target.__name__ )
    if _dummy_app :
      _dummy_app.Destroy ()
      _dummy_app = None

    # return the result to the calling application
    return result

  # ???? don't know what this is for ????
  return wrapper
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
@_Wrap_No_GUI
def AskYesNo ( Question = 'Some Question', Title = 'Please answer this question' ) :
  """
  Yes-No Dialog,  returns :
    True   if Yes is pressed
    False  if No  is pressed
  """
  dialog = wx.MessageDialog ( None, Question, Title,
                              wx.YES_NO | wx.ICON_QUESTION)
  answer = dialog.ShowModal() == wx.ID_YES
  dialog.Destroy ()
  return answer
# ***********************************************************************


# ***********************************************************************
# Asks to select a directory
# ***********************************************************************
def AskDirectory ( DefaultLocation = '', Title = '' ) :
  dialog = wx.DirDialog ( None, Title, defaultPath = DefaultLocation )
  
  if dialog.ShowModal () == wx.ID_OK:
    File =  dialog.GetPath()
  else:
    File = None

  dialog.Destroy ()
  return File
# ***********************************************************************


# ***********************************************************************
# Asks for 1 file for saving information
# ***********************************************************************
def Ask_File_For_Save ( DefaultLocation = '', DefaultFile = '',
                        FileTypes = '*.*',    Title = '' ) :

  if isinstance ( FileTypes, int ) :
    FileTypes = _FT_Collection [ FileTypes ]
  dialog = wx.FileDialog ( None, Title,
           defaultDir = DefaultLocation,
           defaultFile = DefaultFile,
           wildcard = FileTypes,
           style = wx.FD_SAVE ,
           )
  if dialog.ShowModal () == wx.ID_OK:
    File =  dialog.GetPath()
  else:
    File = None

  dialog.Destroy ()
  return File
# ***********************************************************************


# ***********************************************************************
# Asks for 1 file to open
#    FileTypes = 'PNG format|*.png'
#                '|BMP format|*.bmp'
#                '|All Files (*.*)|*.*'
# ***********************************************************************
def AskFileForOpen ( DefaultLocation = '', DefaultFile = '',
                     FileTypes = '*.*', Title = '' ) :
  if isinstance ( FileTypes, int ) :
    FileTypes = _FT_Collection [ FileTypes ]

  dialog = wx.FileDialog ( None,
           Title,
           defaultDir = DefaultLocation,
           defaultFile = DefaultFile,
           wildcard = FileTypes,
           style = wx.FD_OPEN ,
           )
  if dialog.ShowModal () == wx.ID_OK:
    File =  dialog.GetPath()
  else:
    File = None

  dialog.Destroy ()
  return File
# ***********************************************************************


# ***********************************************************************
# Same as AskFileForOpen, but can open multi files
# ***********************************************************************
def AskFilesForOpen ( DefaultLocation = '', DefaultFile = '',
                     FileTypes = '*.*', Title = '' ) :
                       
  dialog = wx.FileDialog ( None, Title,
           defaultDir = DefaultLocation,
           defaultFile = DefaultFile,
           wildcard = FileTypes,
           style = wx.FD_OPEN | wx.FD_MULTIPLE,
           )

  if dialog.ShowModal () == wx.ID_OK:
    Files = dialog.GetFilenames ()
    Path = dialog.GetPath ()
  else:
    Files = None
    Path = None

  dialog.Destroy ()
  return Files, Path
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class _MultiLineDialog ( wx.Dialog ):
  def __init__ ( self, Names, Values, Types,
                 Title = 'Edit Values Below',
                 Help = '',
                 width = -1,
                 pos = wx.DefaultPosition ) :
    #import _images
    style = wx.DEFAULT_FRAME_STYLE | \
                    wx.SUNKEN_BORDER | \
                    wx.CLIP_CHILDREN | \
                    wx.STAY_ON_TOP
    wx.Dialog.__init__( self, None, title = Title,
                        size = ( width, -1 ),
                        pos = pos,
                        style = style )

    if Help:
      help = wx.StaticText ( self, -1, Help )

    # be sure we have enough values
    while len(Values) < len (Names) : Values.append ( '' )
    while len(Types)  < len (Names) : Types.append ( None )
    self.Values = Values
    self.Types = Types
    self.T = []
    grid = wx.FlexGridSizer ( len(Names), 3, 10, 10 )
    for i, item in enumerate ( Names ) :
      print(i,Names[i],Types[i])

      B = wx.StaticText ( self, -1, Names[i]  )
      grid.Add ( B, flag = wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL )

      if   Types[i] == bool:
        self.T.append ( wx.CheckBox ( self, -1, '' ) )
        self.T[i].SetValue ( self.Values[i] )
        grid.Add ( self.T[i], 0, wx.ALIGN_LEFT | wx.ALL, 0)
        grid.Add ( wx.StaticText ( self, -1, ''  ) )

      else :
        #if type ( self.Values[i] ) != basestring :
        if not ( isinstance ( self.Values[i], str ) ) :
          self.Values[i] = str ( self.Values [i] )
        if width == -1 : S = (400,24)
        else :           S = (width,24)
        self.T.append ( wx.TextCtrl   ( self, -1, self.Values[i], size = S ))
        grid.Add ( self.T[i], flag = wx.EXPAND )

        if Types[i] == MLD_FILE :
          bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_BUTTON, (16,16))
          B = wx.BitmapButton ( self, i ,bmp)
          grid.Add ( B, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
          self.Bind ( wx.EVT_BUTTON, self.OnButton, id=i )
        elif Types[i] == MLD_PATH :
          bmp = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_BUTTON, (16,16))
          B = wx.BitmapButton ( self, i ,bmp)
          grid.Add ( B, 0, wx.ALIGN_CENTRE|wx.ALL, 0)
          self.Bind ( wx.EVT_BUTTON, self.OnButton, id=i )
        else:
          grid.Add ( wx.StaticText ( self, -1, ''  ) )
    grid.AddGrowableCol ( 1 )

    Buttons = wx.StdDialogButtonSizer ()
    Button_OK = wx.Button ( self, wx.ID_OK )
    Buttons.AddButton ( Button_OK )
    Buttons.AddButton ( wx.Button ( self, wx.ID_CANCEL ) )
    Buttons.Realize()

    Sizer = wx.BoxSizer ( wx.VERTICAL )
    if Help:
      Sizer.Add ( help, 0, wx.ALL, 5 )
      Sizer.Add ( wx.StaticLine ( self ), 0, wx.EXPAND | wx.ALL, 5)
    Sizer.Add ( grid, 0, wx.EXPAND | wx.ALL, 10 )
    Sizer.Add ( Buttons, 0, wx.EXPAND | wx.ALL, 10 )
    self.SetSizer ( Sizer )
    Sizer.Fit ( self )
    
    # if just 1 element with a preset value
    # than give ok_button focus
    # (specially for search dialog)
    if ( len ( Names ) == 1 ) and \
       isinstance ( self.T[0], wx.TextCtrl ) and \
       ( self.T[0].GetValue () ) :
      Button_OK.SetFocus ()
  # **********************************************************************
  # **********************************************************************
  def ShowModal ( self ) :
    if wx.Dialog.ShowModal ( self ) == wx.ID_OK:
      result = []
      for item in self.T:
        result.append ( item.GetValue () )
      return True, result
    else:
      return False, self.Values

  # **********************************************************************
  # **********************************************************************
  def OnButton ( self, event ) :
    ID = event.GetId()
    if self.Types[ID] == MLD_FILE :
      filepath, filename = path_split ( self.T[ID].GetValue() )
      filename= AskFileForOpen ( filepath, filename )
    elif self.Types[ID] == MLD_PATH :
      filename= AskDirectory ( self.T[ID].GetValue() )
    if filename: self.T[ID].SetValue ( filename )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def MultiLineDialog ( Names = [''], Values = [''], Types = [],
                      Title = 'Unknown Title',
                      HelpText = None,
                      width = -1,
                      pos = wx.DefaultPosition ):
  dlg = _MultiLineDialog ( Names, Values, Types, Title, HelpText, width, pos )
  OK, Values = dlg.ShowModal()
  dlg.Destroy()
  return OK, Values
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
import  wx.lib.mixins.listctrl  as  listmix
class _ExtraListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class _ListDialog ( wx.Dialog ):
  def __init__ ( self, List_Values, 
                 Title = 'Edit Values Below',
                 Help = '',
                 width = -1,
                 pos = wx.DefaultPosition ) :
    style = wx.DEFAULT_FRAME_STYLE | \
                    wx.SUNKEN_BORDER | \
                    wx.CLIP_CHILDREN | \
                    wx.STAY_ON_TOP
    wx.Dialog.__init__( self, None, title = Title,
                        size = ( width, -1 ),
                        pos = pos,
                        style = style )

    if Help:
      help = wx.StaticText ( self, -1, Help )

    #self.List = wx.ListCtrl(self, -1,
    self.List = _ExtraListCtrl(self, -1,
                             style=wx.LC_REPORT
                             #| wx.BORDER_SUNKEN
                             | wx.BORDER_NONE
                             | wx.LC_EDIT_LABELS
                             | wx.LC_SORT_ASCENDING
                             #| wx.LC_NO_HEADER
                             #| wx.LC_VRULES
                             #| wx.LC_HRULES
                             #| wx.LC_SINGLE_SEL
                             )
    # fill the list
    for i,cols in enumerate ( List_Values [0] ) :
      self.List.InsertColumn ( i, cols )
    for item in List_Values [1:] :
      self.List.Append (  ( item[0], item[1] ) )

    Buttons = wx.StdDialogButtonSizer ()
    Buttons.AddButton ( wx.Button ( self, wx.ID_OK ) )
    Buttons.AddButton ( wx.Button ( self, wx.ID_CANCEL ) )
    Buttons.Realize()

    Sizer = wx.BoxSizer ( wx.VERTICAL )
    if Help:
      Sizer.Add ( help, 0, wx.ALL, 5 )
      Sizer.Add ( wx.StaticLine ( self ), 0, wx.EXPAND | wx.ALL, 5)
    Sizer.Add ( self.List, 1, wx.EXPAND | wx.ALL, 10 )
    Sizer.Add ( Buttons, 0, wx.EXPAND | wx.ALL, 10 )
    self.SetSizer ( Sizer )
    Sizer.Fit ( self )

    # Doubleclick or ENTER will also select and end the modal dialog
    self.List.Bind ( wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated ) 

  # **********************************************************************
  # **********************************************************************
  def ShowModal ( self ) :
    if wx.Dialog.ShowModal ( self ) == wx.ID_OK:
      item = self.List.GetFirstSelected()
      if item >= 0 :
        return True, self.List.GetItemText(item)
    return False, None
  
  # **********************************************************************
  # Doubleclick or ENTER will also select and end the modal dialog
  # **********************************************************************
  def OnItemActivated ( self, event ) :
    print('Active')
    self.EndModal ( wx.ID_OK )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def ListDialog ( List_Values, Title,
                      HelpText = None,
                      width = -1,
                      pos = wx.DefaultPosition ):
  dlg = _ListDialog ( List_Values, Title, HelpText, width, pos )
  OK, Values = dlg.ShowModal()
  dlg.Destroy()
  return OK, Values
# ***********************************************************************



# ***********************************************************************
# for test, read and print some ini file
# ***********************************************************************
if __name__ == '__main__':
  app = wx.PySimpleApp ()

  # **************************************************
  # Generate a sorted fontlist
  # **************************************************
  fonts = wx.FontEnumerator ()
  fonts.EnumerateFacenames ()
  fontList = fonts.GetFacenames ()
  fontList.sort()
  # **************************************************


  Test_Defs ( 8 )

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 0 ) :
    Names = [ 'Compiler', 'CheckBox', 'Library Path', 'CMD line', 'Uploader', 'CMD line']
    Values = []
    Types = [ MLD_FILE, bool, MLD_PATH, None, MLD_FILE]
    HelpText = \
"""\
The following substitutes are valid
  %F = JAL source file  (JAL compiler) / Generated Hex file  (uploader)
  %L = JAL library path (JAL compiler)
Commandline examples
  -long-start -d  -clear -s%L %F  (JAL compiler)
  %F uploader 115200  (UPD)\
"""
    OK, Values = MultiLineDialog ( Names, Values, Types,
                                   'Compile and Upload Settings',
                                   HelpText )
                                   # width = 200 )
    if OK: print(Values)

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 1 ) :
    Names  = [ 'For All Signals', 'AutoScale', 'Upper Value', 'Lower Value' ]
    Values = [  False,             True,        200,           20 ]
    Types  = [  bool,              bool ]
    OK, Values = MultiLineDialog ( Names, Values, Types,
                                   'Set Border Values',
                                   width = 70 )
    if OK: print(Values)

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 2 ) :
    # *******************
    # Single FileOpen test
    # *******************
    FileType = "Python Files (*.py)|*.py|"\
               "All Files (*.*)|*.*"
    File = AskFileForOpen ( FileTypes = FileType )
    if File:
      print(File)
    else:
      print('wrong')

  if Test ( 3 ) :
    # *******************
    # Multi FileOpen test
    # *******************
    FileType = "Python Files (*.py)|*.py|"\
               "All Files (*.*)|*.*"
    Files, Path = AskFilesForOpen ( FileTypes = FileType )
    if Files:
      print(Path, Files)
    else:
      print('wrong')

  if Test ( 5 ) :
    # *******************
    # Yes-No test
    # *******************
    if AskYesNo ('Is this ok') :
      print('Yes')
    else:
      print('No')


  # ***********************************************************************
  # ***********************************************************************
  if Test ( 6 ):
    from db_support import Find_ODBC
    ODBC_DBs = Find_ODBC ()
    ODBC_DBs.insert ( 0, [ 'ODBC Name', 'Filename'])

    HelpText = \
"""\
The list below, shows both the
  - user databases ( HKEY_CURRENT_USER\Software\ODBC\ODBC.INI  )
  - system databases ( HKEY_LOCAL_MACHINE\Software\ODBC\ODBC.INI )"""


    OK, Values = ListDialog ( ODBC_DBs,
                              'Select ODBC Database',
                              HelpText )
                              # width = 200 )
    if OK: print(Values)

  # ***********************************************************************
  # ***********************************************************************
  if Test ( 7 ) :
    print(fontList)

  # ***********************************************************************
  # Search Dialog
  # ***********************************************************************
  if Test ( 8 ) :
    Prev_Search = 'Find'
    OK, Values = MultiLineDialog ( Values = [ Prev_Search ],
                                   Title  = 'Enter Search String',
                                   width  = 200 )
    if OK:
      Prev_Search = Values [0]
    print(Prev_Search)

  # ***********************************************************************
  # Search Dialog
  # ***********************************************************************
  if Test ( 9 ) :
    color = Color_Dialog ()
    print(color)
    color = Color_Dialog ()
    print(color)

# ***********************************************************************
pd_Module ( __file__ )
