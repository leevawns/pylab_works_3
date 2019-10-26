import __init__

# ***********************************************************************
# <Description>
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2008 Stef Mientki
# mailto: ...
# Please let me know if it works or not under different conditions
#
# Version: 1.1    ,18-07-2008, Stef Mientki
# Test Conditions: 2
#    - Babel Fish translation through LXML instead of BeautifulSoap
#    - Babel Fish translation done in a separate thread
#    - Tripple quoted strings on more lines were not correctly read / written
#    - Sources and Babel Fish follows Translation,
#        also when navigation with keyboard
#    - Keywords in Translation editor cleared
#
# Version: 1.0    ,10-04-2008, Stef Mientki
# Test Conditions: 1
#    - orginal release
#
# Test Conditions
# 1. WinXP-SP2, Python 2.4.3, wxPython wx-2.8-msw-ansi
# 2. WinXP-SP2, Python 2.5.2, wxPython 2.8.7.1 (msw-unicode)
# ***********************************************************************

# ***********************************************************************
_ToDo = """
- Disable autocompletion in editors, how ?
"""
# ***********************************************************************

"""
import os
import sys
subdirs = [ '../support', '../Lib_Extensions' ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
"""

# !!! import wx before any support library !!!
# otherwise the IDE won't do auto-suggest
import wx
#from   Scintilla_Python import *
from   Scintilla_support import *

from file_support     import *
from menu_support     import *
from dialog_support   import *
from inifile_support  import *
from gui_support      import *
from language_support import *

#change translator to google
from googletrans import Translator

try :
  import lxml.html
except :
  pass
from urllib.parse import urlencode
from threading import *
import datetime
from importlib import reload

# *************************************************************
# Define notification event for thread completion
# *************************************************************
EVT_RESULT_ID = wx.NewId()
# *************************************************************

# *************************************************************
# *************************************************************
class ResultEvent(wx.PyEvent):
  def __init__(self, data):
    wx.PyEvent.__init__(self)
    self.SetEventType ( EVT_RESULT_ID )
    self.data = data
# *************************************************************


# *************************************************************
# *************************************************************
class Thread_Google_Translation ( Thread ) :
  def __init__ ( self, notify_window, lang, text ) :
    Thread.__init__ ( self )
    self._notify_window = notify_window
    self.lang = lang
    self.text = text
    self.setDaemon (1)
    self.start ()

  def run ( self ) :
    translator = Translator()
    try:
      Google_Result = translator.translate(self.text,src='en',dest = self.lang.lower ())
    except Exception as e:
      Google_Result = None 
    if Google_Result :
      Result = Google_Result
    else :
      Result = translator
    wx.PostEvent(self._notify_window, ResultEvent( Result ))
# *************************************************************


# ***********************************************************************
# ***********************************************************************
class tSource_File ( object ):
  def __init__ ( self, filename ) :
    fh = open ( filename, 'r')
    lines = fh.readlines ()
    fh.close()
    self.used_nrs     = []
    self.double_nrs   = []
    self.double_lines = []
    self.zero_nrs     = 0
    self.Zero_Lines   = []
    self.dict_US      = {}
    expand     = False
    line_nr    = 0
    for line in lines :
      line = line.replace ( '__(', '__ (' )
      line_nr += 1
      if not expand :
        #remove space 
        lin = line.lstrip()
        posi = lin.find ( '_(' )
        if posi >= 0 :
          # get the string-ID
          lin  = lin [ posi + 2 : ]
          posi = lin.find ( ',' )
          try:
            nr   = int ( lin [ : posi ] )
          except Exception as e:
            print(e)
            continue
          lin  = lin [ posi + 1 : ].strip()

          # determine the string separator
          #print 'LIN',lin
          if lin.find ('"""') == 0 : 
            sep = '"""'
          else :
            sep = lin[0]
          # get the text only
          lins = lin.split ( sep )
          text = lins[1] + '\n'

          # if end separator not on this line ...
          expand = len ( lins ) < 3

          if nr != 0 :
            if nr in self.used_nrs :
              if text != self.dict_US[nr][1] :
                self.double_lines.append (
                  [ nr, self.dict_US[nr], [ line_nr, text ] ] )
              if not ( nr in self.double_nrs ):
                self.double_nrs.append ( nr )
            else :
              self.used_nrs.append ( nr )
          else :
            self.Zero_Lines.append (
              [ line_nr, text ] )
            self.zero_nrs += 1
          line_total = text
          if not ( expand ) :
            if nr != 0 :
              self.dict_US [nr] = [ line_nr, line_total ]

      # line continuation
      else :
        if line.find ( sep ) >= 0 :
          if nr != 0 :
            line_total += line.split ( sep )[0] + '\n'
            self.dict_US [nr] = [ line_nr, line_total ]
          expand = False
        else :
          line_total += line
# ***********************************************************************
# ***********************************************************************
# ***********************************************************************
class Translation_Form ( wx.MiniFrame ):
  def __init__ ( self, ini = None ):

    self.Filename_Source = ''
    self.Language_Current = 'NL'
    self.State = 0
    self.current_line_nr = -1
    self.ini = ini

    # restore position and size
    print ('FFF',ini)
    if self.ini :
      self.ini.Section = 'Main'
      pos  = self.ini.Read ( 'Pos'  , ( 50, 50 ) )
      size = self.ini.Read ( 'Size' , ( 500, 700 ) )

      #print 'KKK',os.getcwd()

      self.Filename_Source  = self.ini.Read ( 'File', self.Filename_Source  )
      self.Language_Current = self.ini.Read ( 'Lang', self.Language_Current )

    wx.MiniFrame.__init__(
      self, None, -1, 'Multi Language Control',
      size  = size,
      pos   = pos,
      style = wx.DEFAULT_FRAME_STYLE )

    GUI = """
    Panel_top                        ,PanelVer, 10
      self.Splitter                  ,SplitterVer
        self.Editor_Source           ,Base_STC     ,style = wx.NO_BORDER,size = (-1,50)
        Splitter2                    ,SplitterVer
          self.Editor_Babel          ,wx.TextCtrl  ,style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER, size = (-1,10)
          self.Editor_Translation    ,Base_STC     ,style = wx.NO_BORDER,size = (-1,50)
      Button_Panel                   ,wx.Panel
        self.Button_Auto_Number      ,wx.Button,  label = "Auto Number Zeros"
        self.Button_ReNumber         ,wx.Button,  label = "Re-Number ALL",     pos = (120,0)
        self.Button_Save_Source      ,wx.Button,  label = "Save Source",       pos = (225,0)
        self.Button_Save_Translation ,wx.Button,  label = "Save Translation",  pos = (310,0)
        self.Button_Next_File        ,wx.Button,  label = "Next File",         pos = (400,0)
        self.Button_Language         ,wx.Button,  label = "US", size= (50,-1), pos = (550,0)
        self.Button_Help             ,wx.Button,  label = "Help",              pos = (600,0)
    """
    self.wxGUI = Create_wxGUI ( GUI ) #, IniName = 'self.Ini_File' )

    #Splitter.SetSashPosition ( self.GetSize ()[1] / 2 )
    #wx.CallLater ( 100, self.Splitter.SetSashPosition, self.GetSize ()[1] / 2 )

    self.Button_Language.SetLabel ( self.Language_Current )

    self.Button_Save_Source.Bind     ( wx.EVT_BUTTON,        self.On_Save_Source      )
    self.Button_Auto_Number.Bind     ( wx.EVT_BUTTON,        self.On_Auto_Number      )
    self.Button_Save_Translation.Bind( wx.EVT_BUTTON,        self.On_Save_Translation )
    self.Button_Next_File.Bind       ( wx.EVT_BUTTON,        self.On_Next_File        )
    self.Button_ReNumber.Bind        ( wx.EVT_BUTTON,        self.On_ReNumber         )
    self.Button_Language.Bind        ( wx.EVT_BUTTON,        self.On_Language         )
    self.Button_Help.Bind            ( wx.EVT_BUTTON,        self.On_Help             )

    self.Editor_Source.Bind      ( stc.EVT_STC_MODIFIED, self.On_Source_Modified  )

    self.Editor_Translation.Bind ( stc.EVT_STC_MODIFIED, self.On_Translation_Modified )
    self.Editor_Translation.Bind ( stc.EVT_STC_UPDATEUI, self.On_Update_Translation_UI )
    self.Editor_Translation.Bind ( wx.EVT_LEFT_DOWN,     self.On_Select_Translation )
    #self.Editor_Translation.Bind ( stc.EVT_STC_KEY,      self.On_Translation_Key )
    #self.Editor_Translation.Bind ( wx.EVT_KEY_DOWN,      self.On_Translation_Key )
    self.Editor_Translation.Bind ( wx.EVT_KEY_DOWN,      self.On_Select_Translation )

    self.StatusBar = self.CreateStatusBar ()
    self.StatusBar.SetFieldsCount (3)
    self.StatusBar_Controls = []

    self.Bind ( wx.EVT_CLOSE, self._OnClose )

    ## String
    self.Editor_Source.StyleSetSpec ( stc.STC_P_STRING,       "back:#C0C0C0" )
    # Single quoted string
    self.Editor_Source.StyleSetSpec ( stc.STC_P_CHARACTER,    "back:#C0C0C0" )
    self.Editor_Source.StyleSetSpec ( stc.STC_P_TRIPLE,       "back:#C0C0C0" )
    self.Editor_Source.StyleSetSpec ( stc.STC_P_TRIPLEDOUBLE, "back:#C0C0C0" )
    self.Editor_Source.MarkerDefine ( 31, stc.STC_MARK_BACKGROUND, "#00FF00", "#00FF00")
    self.Editor_Source.EnsureCaretVisible ()
    #self.Editor_Source.AutoCompSetFillUps ( '' )
    #self.Editor_Source.Margin_On ( 2 )

    self.Editor_Translation.MarkerDefine ( 31, stc.STC_MARK_BACKGROUND, "#00FF00", "#00FF00")
    self.Editor_Translation.EnsureCaretVisible()
    self.Editor_Translation.Show_AutoCompletion_List = self.No_AutoCompletion
    self.Editor_Translation.SetKeyWords ( 0, '')

    self.On_Translation_Modified ( None )

    self.Status = []
    self.Status.append ( 'Select File' )
    self.Status.append ( 'Solve Doubles' )
    self.Status.append ( 'Zeros Detected' )
    self.Status.append ( 'Translation' )

    self.Button_Save_Source.Enabled        = False
    self.Button_Save_Translation.Enabled   = False

    # Set up event handler for any thread results
    self.Connect ( -1, -1, EVT_RESULT_ID, self.On_BabelFish_Result )
    self.BabelFish = False

    self.State_Machine ()

  # *************************************************************
  # *************************************************************
  #def On_Translation_Key ( self, event ) :
  #  #print ' KYYYE'
  #  self.Source_Folows_Destination ()
  #  event.Skip ()
    
  # *************************************************************
  # *************************************************************
  def No_AutoCompletion ( self ) :
    pass

  # *************************************************************
  # *************************************************************
  def State_Machine ( self, NewState = 0 ) :
    print("State_Machine")
    if self.State > 0 :
      self.State = NewState
      
    # first disable the special buttons
    self.Button_Auto_Number.Enabled        = False
    self.Button_ReNumber.Enabled           = False
    # Select File
    if self.State == 0 :
      dem = self.Editor_Source.LoadFile ( self.Filename_Source )
      self.On_Source_Modified ( None )

      self.State = self.Run_Source_Check ()


    # *************************************************************
    # now check the state again
    # *************************************************************
    # Zeros detected, wait for user key
    if self.State == 2 :
      self.Button_Auto_Number.Enabled = True
      self.Button_ReNumber.Enabled    = True

    self.StatusBar.SetStatusText ( self.Status [self.State], 0 )

  # *************************************************************
  # *************************************************************
  def Run_Source_Check ( self ) :
    global LT
    self.Editor_Translation.ClearAll ()
    self.Source = tSource_File ( self.Filename_Source )
    N = self.Source.double_nrs
    N = self.Source.zero_nrs
    if len ( self.Source.double_lines ) > 0 :
      self.StatusBar.SetStatusText ( 'ID Conflicts', 2 )
      for item in self.Source.double_lines :
        self.Editor_Translation.AppendText (
          '## *******  ID Conflict = ' + str(item[0]) + '  ********\n')
        self.Editor_Translation.AppendText (
          str(item[1][0])+': ' +  str(item[1][1]) + '\n' )
        self.Editor_Translation.AppendText (
          str(item[2][0])+': ' +  str(item[2][1]) + '\n' )
      return 1
    else :
      if self.Source.zero_nrs > 0 :
        self.Editor_Translation.AppendText (
          '## *******  Zeros detected   ********\n')
        for item in self.Source.Zero_Lines :
          self.Editor_Translation.AppendText (
            str(item[0])+': ' +  str(item[1]) + '\n' )
        return 2
      
      # here the source is OK, so read the language file
      else :
        print ('OK')
        fp, fn = path_split ( self.Filename_Source )
        fn, fe = os.path.splitext ( fn )
        fn = fn + "_" + self.Language_Current
        try :         
          line = "from "+fn+" import LT"
          print(line)
          exec(line,globals())
          print("LT",LT)
        except Exception as e:
          print(e)
          LT = {}
          print ('Translation Not Found, Created New File')

        #self.Editor_Translation.ClearAll ()
        US = self.Source.dict_US
        for i in US :
          line = str ( US[i][0]) + ': ' + str(i) + ': '
          if i in LT:
            """
            if len ( LT[i] ) > len ( LT[i].strip() ) :
              line += '"' + LT[i] + '"'
            else :
              line += LT[i]
            """
            line += LT[i]
          line += '\n'
          self.Editor_Translation.AppendText ( line )
          
        # remove the last newline
        self.Editor_Translation.SetText (
          self.Editor_Translation.GetText()[:-1] )

        # Now we have to reset the modify flag of the editor
        # There doesn't seem to be a normal way,
        # other than saving the file
        # and we have to call GetModify to generate an event
        self.Editor_Translation.SaveFile ( 'temp.temp' )
        self.Editor_Source.GetModify ()

        #self.Button_Save_Translation.Enabled = True
        return 3
      
  # *************************************************************
  # Renumbers the whole file,
  #   - first replace all numbers by zeros
  #   - call On_Auto_Number to fill the numbers in an ordered way
  # Because this might affect existing translations,
  #   we ask a confirmation
  # *************************************************************
  def On_ReNumber ( self, event ) :
    if AskYesNo ( 'Renumbering may affect existing translations\n' +
       'Are you sure ?') :
      # Replace the zero numbers
      # WEIRD: writing to the file changes "\r\n" into "\r\r\n" ???
      # so we remove the "\r",
      # because then "\n" will be translated to "\r\n"
      text = self.Editor_Source.GetText().replace ( '\r', '' )
      text = text.replace ( '__(', '__ (' )
      text = text.split ( '_(' )
      new_text = []
      for line in text :
        line = line.split ( ',' )
        try :
          i = int ( line [0] )
          new_text.append ( ','.join ( line [1:] ) )
        except :
          new_text.append ( ','.join ( line ) )
      new_text = '_(0,'.join ( new_text )

      # save the auto-numbered text
      file = open ( self.Filename_Source, 'w')
      file.write  ( new_text )
      file.close  ()

      # reload the Source-Editor
      self.Editor_Source.LoadFile ( self.Filename_Source )
      self.On_Source_Modified ( None )
      self.On_Auto_Number     ( None )

  # *************************************************************
  # *************************************************************
  def On_Auto_Number ( self, event ) :
    N = self.Source.zero_nrs

    # create unique numers to replace the zeros
    uniq_nrs = list(range ( 1, 1 + N + len ( self.Source.used_nrs ) ))
    for i in self.Source.used_nrs :
      uniq_nrs.remove ( i )

    # Replace the zero numbers
    # WEIRD: writing to the file changes "\r\n" into "\r\r\n" ???
    # so we remove the "\r",
    # because then "\n" will be translated to "\r\n"
    text = self.Editor_Source.GetText().replace ( '\r', '' )
    text = text.replace ( '__(', '__ (' )
    for i in range ( N ) :
      text = text.replace ( '_(0', '_(' + str ( uniq_nrs.pop(0) ), 1)

    # save the auto-numbered text
    file = open ( self.Filename_Source, 'w')
    file.write ( text )
    file.close ()

    self.State_Machine ( 0 )

  # *************************************************************
  # *************************************************************
  def On_Next_File ( self, event ) :
    fp, fn = path_split ( self.Filename_Source )
    New_File = AskFileForOpen (
      fp, fn, '*.py', 'Select Source File' )
    if New_File :
      print("new file : ",New_File)
      self.On_Source_Modified ( event )
      self.On_Translation_Modified ( event )
      self.Filename_Source = New_File
      self.State_Machine ( 0 )

  # *************************************************************
  # *************************************************************
  def On_Language ( self, event ) :
    # get all implemented languages, but remove "US"
    # and you can only remove it ones !!
    pre = Language_IDs
    try:
      US = pre.index ( 'US' )
      del ( pre [ US ] )
    except :
      pass
    
    self.Popup_Menu = My_Popup_Menu ( self._OnPopupItemSelected, None,
      pre =pre )
    selected = pre.index ( self.Language_Current )
    self.Popup_Menu.SetChecked ( selected, True )
    self.PopupMenu ( self.Popup_Menu )

  # *****************************************************************
  # *****************************************************************
  def _OnPopupItemSelected ( self, event ) :
    ID = event.Int
    if self.Language_Current != Language_IDs [ ID ] :
      self.Language_Current = Language_IDs [ ID ]
      self.Button_Language.SetLabel ( self.Language_Current )

      # save modifications
      self.On_Source_Modified ( event )
      self.On_Translation_Modified ( event )

      # Restart statemachine
      self.State_Machine ( 0 )

  # *************************************************************
  # *************************************************************
  def On_Help ( self, event ) :
    Show_Message ( 'No Help Available Yet' )

  # *************************************************************
  # Called when another line in the Translation Editor is selected
  # *************************************************************
  def On_Update_Translation_UI ( self, event ) :
    lnr  = self.Editor_Translation.GetCurrentLine()
    self.Editor_Translation.MarkerDeleteAll ( 31 )
    self.Editor_Translation.MarkerAdd ( lnr, 31 )

  # *************************************************************
  # *************************************************************
  def On_Select_Translation ( self, event ) :
    event.Skip ()
    #self.Source_Folows_Destination ()
    wx.CallAfter ( self.Source_Folows_Destination )

  # *************************************************************
  # *************************************************************
  def Source_Folows_Destination ( self ):
    text    = self.Editor_Translation.GetCurLine()[0]
    lnr     = self.Editor_Translation.GetCurrentLine()
    line_nr = None
    Nlines  = 0
    while not ( line_nr ) and ( lnr >= 0 ) :
      Nlines += 1
      text = text.split(':')
      if len ( text ) > 1 :
        try :
          line_nr = int ( text[0] )
        except :
          line_nr = None
      if ( not line_nr ) :
        lnr -= 1
        text = self.Editor_Translation.GetLine ( lnr )

    if line_nr and ( line_nr != self.current_line_nr ):
      self.current_line_nr = line_nr
      self.Editor_Source.MarkerDeleteAll ( 31 )
      for i in range ( Nlines ) :
        self.Editor_Source.MarkerAdd ( line_nr - 1 - i, 31 )
      # move first to the end, to get the line always in the same position
      self.Editor_Source.GotoLine ( self.Editor_Source.GetLineCount() - 1 )
      self.Editor_Source.GotoLine ( line_nr - self.Editor_Source.LinesOnScreen()/2 )
      self.Editor_Source.EnsureCaretVisible()

      line = self.Editor_Source.GetLine ( line_nr - 1 - i )
      lin = line.lstrip()
      posi = lin.find ( '_(' )
      if posi >= 0 :
        # get the string-ID
        lin  = lin [ posi + 2 : ]
        posi = lin.find ( ',' )
        nr   = int ( lin [ : posi ] )
        lin  = lin [ posi + 1 : ].strip()

        # determine the string separator
        if lin.find ('"""') == 0 : sep = '"""'
        else :                     sep = lin[0]

        # get the text only
        lins = lin.split ( sep )
        text = lins[1] + '\n'

        if not ( self.BabelFish ) and text != "":
          self.BabelFish = True
          wx.CallLater ( 1000, Thread_Google_Translation, self, self.Language_Current, text )

  # *************************************************************
  # *************************************************************
  def On_BabelFish_Result ( self, event ) :
    #self.Editor_Babel.SetLabel ( event.data )
    print("add textlable : ",event.data.text)
    self.Editor_Babel.AppendText ( event.data.text + '\n' )
    self.BabelFish = False

  # *************************************************************
  # *************************************************************
  def On_Source_Modified ( self, event ) :
    if self.Editor_Source.GetModify () :
      self.StatusBar.SetStatusText( 'Source modified', 1 )
    else :
      self.StatusBar.SetStatusText( '', 1 )
    self.Button_Save_Source.Enabled = self.Editor_Source.GetModify ()

  # *************************************************************
  # *************************************************************
  def On_Translation_Modified ( self, event ) :
    if ( self.State == 3 ) and self.Editor_Translation.GetModify () :
      self.StatusBar.SetStatusText( 'Translation modified', 2 )
      self.Button_Save_Translation.Enabled = True
    else :
      self.StatusBar.SetStatusText( '', 2 )

  # *************************************************************
  # *************************************************************
  def On_Save_Source ( self, event ) :
    if self.Editor_Source.GetModify () :
      self.Editor_Source.SaveFile ( self.Filename_Source )
    self.Button_Save_Source.Enabled = False
    self.Run_Source_Check ()
    
  # *************************************************************
  # *************************************************************
  def On_Save_Translation ( self, event ) :
    if self.Editor_Translation.GetModify () :
      global Version
      fp, fn = path_split ( self.Filename_Source )
      fn, fe = os.path.splitext ( fn )
      fn = fn + '_' + self.Language_Current
      filename = os.path.join ( fp, 'lang', fn + '.py' )

      # be sure we've the directory
      Force_Dir (  os.path.join ( fp, 'lang' ) )
      if File_Exists ( filename ) :
        try :
          #print ' import',fn
          exec ( 'import '+ fn,globals())
          Version_Text = eval ( fn + '._Version_Text')
          #print ' aap', Version_Text
          Version = Version_Text [0][0]
          #print ' aap2', Version_Text
        except :
          #print 'ERRRRR'
          Version_Text = []
          Version = 0

      Version += 1
      # get date in normal European notation
      datum = str(datetime.date.today())
      datum = datum.split('-')
      datum = datum[2] + '-' + datum[1] + '-' + datum[0]
      Version_Text.insert ( 0, [ Version, datum ])
      file = open ( filename, 'w')
      #print 'FNNN',filename, Version

      # write the version informatiom
      #file.write ( 'from PyLab_Works_Globals import _')
      file.write ( 'Version_Text = [' + '\n' )
      for version in Version_Text :
        file.write ( '[ ' + str( version[0] ) +
                     ', "' + str( version[1] ) + '"' +
                     ', "' + 'Unknown Author' + '"' +
                     ',' +'\n')
        file.write ( '"Test Conditions:", (),' + '\n')
        file.write ( '"Unknown Changes" ],' + '\n')
      file.write ( ']' + '\n\n' )


      file.write ( '' + '\n' )
      file.write ( '# ' + self.Language_Current + ' language module' + '\n' )
      file.write ( '' + '\n' )
      file.write ( 'LT = {' + '\n' )
      lines = self.Editor_Translation.GetText().split('\n')
      LT = {}
      Line_Buf = ''
      Line_Nr  = 0
      Line_Sep = "'"
      for line in lines :
        text = line.split(':')
        
        # check if new definition found
        if len ( text ) == 3 :

          # if still information in buffer, write it to file
          if Line_Nr > 0 :
            if len ( Line_Buf ) > 2 :
              # remove the last newline,
              # and add again after separator added
              regel = ' ' + str(Line_Nr) + ': '+ \
                      Line_Sep + Line_Buf[:-1] + Line_Sep +',\n'
              print ('111',regel)
              file.write ( regel )
            Line_Buf = ''
            Line_Nr  = 0
            Line_Sep = "'"
            
          # gather information about a new item
          # ignore the first space
          if text[2][0] == ' ':
            text[2] = text[2][1:]
          Line_Buf = text[2] + '\n'
          Line_Nr  = int ( text[1] )
          Line_Sep = "'"

            
        # apparently a line continuation
        else :
          Line_Buf += line + '\n'
          print ('333',Line_Buf)
          Line_Sep = '"""'

      # if still information in buffer, write it to file
      if Line_Nr > 0 :
        if len ( Line_Buf ) > 2 :
          # remove the last newline,
          # and add again after separator added
          regel = ' ' + str(Line_Nr) + ': '+ \
                  Line_Sep + Line_Buf[:-1] + Line_Sep +',\n'
          print ('222',regel)
          file.write ( regel )

      """
      for line in lines :
        text = line.split(':')
        # if key has a value and the value is not just white space
        print 'LONE',line,text
        print len(text),text[2].strip()
        if ( len ( text ) > 2 ) and ( len ( text[2].strip() )) > 0 :
          # ignore the first space
          if text[2][0] == ' ':
            text[2] = text[2][1:]
          ##LT [ text[1] ] = text[2]
          regel = ' ' + text[1] + ": '" + text[2] + "',"
          file.write ( regel  + '\n' )
      """
      file.write ( '}' + '\n' )
      file.close ()
      self.Button_Save_Translation.Enabled = False

  # *************************************************************
  # *************************************************************
  def _OnClose ( self, event ) :
    self.On_Source_Modified ( event )
    self.On_Translation_Modified ( event )

    self.ini.Section = 'Main'
    self.ini.Write ( 'Pos',  self.GetPosition () )
    self.ini.Write ( 'Size', self.GetSize     () )

    filename = Get_Relative_Path ( self.Filename_Source, Application.Dir )
    self.ini.Write ( 'File', filename  )
    self.ini.Write ( 'Lang', self.Language_Current )

    #self.Destroy ()
    event.Skip   ()
# ***********************************************************************


# ***********************************************************************
# demo program
# ***********************************************************************
'''
if __name__ == 'weg__main__':
  app = wx.PySimpleApp ()
  ini = inifile ( 'multi_language.cfg' )
  frame = Translation_Form (ini = ini)
  frame.Show ( True )
  app.MainLoop ()
  ini.Close ()
'''
# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  ini = 'multi_language.cfg'
  My_Main_Application ( Translation_Form, ini )
# ***********************************************************************
# ***********************************************************************
pd_Module ( __file__ )

