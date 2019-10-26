import __init__
from language_support import _


_CHM_Links = {
'<default>' : 'P:/Python/Doc/Python25.chm',
'wx'        : 'P:/Python/wxPython2.8 Docs and Demos/docs/wx.chm',
'stc'       : 'P:/Python/wxPython2.8 Docs and Demos/docs/wx.chm',
'win32api'  : 'P:/Python/Lib/site-packages/PyWin32.chm',
}

_CTRL_Links = {
'<default>' : 'P:/Python/Doc/Python25.chm',
}

# ***********************************************************************
"""
For frequent visited sites, this dictionary defines shortcuts, like
  "g" or "g." or "g.<search term>" for google search
For wikipedia a special command exists , in which you can specify the language:
  "wp.<search term>"      language independent
  "wpen.<search term>"    English
  "wpnl.<search term>"    Dutch
Some sites needs different webaddresses with and without query.
In those cases, this table has 2 entries, like
  "mw" mathworld without search query
  "mw_" mathworld with a search term
The search term is in the table indicated with "%%%%"
  %%%% will be replaced by the search query
"""
# ***********************************************************************
_URL_ShortCuts = {
'g'   : 'http://www.google.com/search?q=%%%%',
'gc'  : 'http://www.google.com/codesearch?q=%%%%',
'gp'  : 'http://www.google.com/search?q=python+%%%%',
'lv'  : 'http://zone.ni.com/reference/en-XX/help/371361E-01/',
'ml'  : 'http://www.mathworks.com/access/helpdesk/help/helpdesk.html',
'ml_' : 'http://www.mathworks.com/cgi-bin/texis/webinator/search/'\
        '?db=MSS&prox=page&rorder=750&rprox=750&rdfreq=500&rwfreq=500'\
        '&rlead=250&sufs=0&order=r&is_summary_on=1&query=%%%%'\
        '&query1=pendulum&ResultCount=100&query2=&query3=&notq='\
        '&documentation=Documentation',
'mm'  : 'http://mathworld.wolfram.com',
'mm_' : 'http://mathworld.wolfram.com/search/?query=%%%%',
'mpl' : 'http://matplotlib.sourceforge.net/gallery.html',
'mw'  : 'http://mathworld.wolfram.com',
'mw_' : 'http://mathworld.wolfram.com/search/?query=%%%%',
'n'   : 'http://www.scipy.org/Numpy_Example_List_With_Doc',
'p'   : 'http://www.python.org/doc/',
'pw'  : 'http://pic.flappie.nl',
'sc'  : 'http://www.scipy.org/Documentation',
'vp'  : 'http://vpython.org/webdoc/visual/index.html',
'w32' : 'http://python.net/crew/mhammond/win32/',
'wr'  : 'http://mathworld.wolfram.com',
'wr_' : 'http://mathworld.wolfram.com/search/?query=%%%%',
'wx'  : 'http://www.zetcode.com/wxpython/',
}
# ***********************************************************************



# ***********************************************************************
__doc__ = _(7,"""
Jumps to a help page, either a local file ( chm, html, txt ),
or to a website.
There are 3 different kinds of list,
which for instance could be tight to differnet keys, like
        F1 = Default list, normally conatining the CHM files
  Shift+F1 = Google search
  Ctrl +F1 = An alternative list
The lists in the first and third kind,
can be read from an ini-file.

# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007 Stef Mientki
# mailto:S.Mientki@ru.nl
""")
# ***********************************************************************


# ***********************************************************************
_Version_Text = [

[ 1.1 , '16-11-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(8, """
- Class_URL_Viewer added
- _My_IEHtmlWindow_Ext added
- main section added
""")],


[ 1.0 , '10-10-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(9, ' - orginal release')]
]

_ToDo = """
- language support doesn't work through wxGUI
- close doesn't save
"""
# ***********************************************************************


import os
import sys
import webbrowser
from inifile_support import *
import wx
import wx.html
import wxp_widgets
from gui_support import *

# ***********************************************************************
def Launch_CHM ( CHM, keyword = '' ) :

  if sys.platform == 'win32' :
    import win32help
    Win32_Viewer = 0
    win32help.HtmlHelp ( Win32_Viewer,
                         str(CHM),
                         win32help.HH_DISPLAY_INDEX,
                         str ( keyword ) )
  else :
    import subprocess
    subprocess.Popen( "gnome-open " + CHM , shell = True )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Help_Viewer_Class ( object ) :
  def __init__ ( self, Local_Browser = None ) :  #Ini = None ) :
    self.Local_Browser = Local_Browser

    #**********************************************
    # Still have to work out for others dan windows
    #**********************************************
    #if os.name != 'nt' :
    #  print '********* OMISSION **********'
    #  print 'help_support.py should be rewritten for non-windows sytems'
    #  return
    self.OS = os.name

    # create the base search paths
    self.URL_Google = "http://www.google.com/search?q=python+"


  # ********************************************************************
  # ********************************************************************
  def Find ( self, keyword = '', Pre_Parts = [], typ = 0 ) :

    URL = self.URL_Google + keyword
    #CHM = self.CHM_Base
    CHM = _CHM_Links [ '<default>' ]

    #**********************************************
    # Normal help files
    #**********************************************
    if typ == 0 :
      # try to find the help base of the pre words
      Failed = True
      N = len ( Pre_Parts )
      while Failed and ( N > 0 ):
        key = '.'.join ( Pre_Parts [ : N] )
        print ('NORMAL HELP',key)
        if _CHM_Links.has_key ( key ) :
          CHM = _CHM_Links [ key ]
          Failed = False
          break
        else :
          N -= 1

      # if based on the pre words nothing is found, use the default
      if Failed :
        CHM = _CHM_Links [ '<default>']
      print ('CHM',CHM)
      print (_CHM_Links)
      
    #**********************************************
    # Own links if exists, otherwise Google
    #**********************************************
    elif typ == 1 :
      # try to find the own link on base of the pre words
      Failed = True
      N = len ( Pre_Parts )
      while Failed and ( N > 0 ):
        key = '.'.join ( Pre_Parts [ : N] )
        print ('CTRL HELP',key)
        if _CTRL_Links.has_key ( key ) :
          URL = _CTRL_Links [ key ]
          Failed = False
          break
        else :
          N -= 1

      # if based on the pre words nothing is found, use the default
      if Failed :
        URL = _CTRL_Links [ '<default>']

      # determine the typ of the link:
      # chm-file / text-file / web-page
      # all possible with a browser, except chm
      URL = URL.replace ( '&&&', keyword )
      print ('Result',URL)
      if URL.lower().find('.chm') > 0 :
        CHM = URL
        typ = 0
      else :
        typ = 2

    #**********************************************
    # NOT WINDOWS, always goto html
    #**********************************************
    if self.OS != 'nt' :
      typ = 2


    print ('WWWQQQ', typ)
    #**********************************************
    # Search for standard CHM files
    #**********************************************
    if typ == 0 :
      Launch_CHM ( CHM, keyword )

    #**********************************************
    # Google
    #**********************************************
    else :
      print ('LOCAL VBROWSER?',self.Local_Browser)
      if self.Local_Browser :
        self.Local_Browser.Load ( URL )
      else :
        webbrowser.open ( URL )
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class _My_HtmlWindow ( wx.html.HtmlWindow ) :

  # *************************************************
  # *************************************************
  def LoadUrl ( self, URL ) :
    URL = URL.replace ( 'file:///', '' )
    URL = URL.replace ( '\\', '/' )
    #v3print ( 'LINUX IEWIN', URL )

    #translated_URL = 'CSS_translated.html'
    #wxp_widgets.Translate_CSS ( URL, translated_URL ) #, self.CallBack_Html )
    self.LoadPage ( URL )

  # *************************************************
  # *************************************************
  def Load_CSS ( self, URL, CallBack_Html = None ) :
    """
    name_to = 'CSS_translated.html'
    wxp_widgets.Translate_CSS ( URL, name_to, CallBack_Html )
    self.LoadPage ( name_to )
    """
    self.LoadUrl ( URL )
    
    from wxp_widgets import CallBack_Html_Pointer
    if CallBack_Html and not ( CallBack_Html_Pointer ) :
      CallBack_Html_Pointer = CallBack_Html


# ***********************************************************************
# ***********************************************************************
class _My_IEHtmlWindow_Ext ( wx.Panel ) :
  def __init__ ( self, parent ) : ##, message, caption='', flags=0):
    wx.Panel.__init__ ( self, parent )

    GUI = """
    My_Text   ,wx.StaticText  , pos = ( 30, 30 )
    """
    self.wxGUI = Create_wxGUI ( GUI, IniName = 'self.Ini_File' )
    My_Text.SetLabel ('try multiline\n lbale' )


  def LoadUrl ( self, URL ) :
    webbrowser.open ( URL )
    
# ***********************************************************************





# ***********************************************************************
# For each OS here two versions of the iewin.IEHtmlWindow are defined:
# for windows these are both assigned to the orginal
#    IEHtmlWindow     = iewin.IEHtmlWindow
#    IEHtmlWindow_Ext = iewin.IEHtmlWindow
# for other operating systems, there are created 2 versions,
# One version where wx.html.HtmlWindow ( with premature CSS translation) is used
#    IEHtmlWindow     = _My_IEHtmlWindow
# And another version where a dummy panel with a warning is showed,
# but the input is sent to the default external browser
#    IEHtmlWindow_Ext = _My_IEHtmlWindow_Ext
# ***********************************************************************
print ('*****  WARNING  *****')
print ('       wx.lib.iewin.IEHtmlWindow is only supported under MS-Windows')

# ********************************************
# always import iewin (also on non Windows OS),
# so the event definitions are avalaible
#import  wx.lib.iewin  as iewin
# ********************************************

if Platform_Windows :
  import  wx.lib.iewin  as iewin
  IEHtmlWindow     = iewin.IEHtmlWindow
  IEHtmlWindow_Ext = iewin.IEHtmlWindow
else :
  print ('       Contact the developer of this program')
  IEHtmlWindow     = _My_IEHtmlWindow
  IEHtmlWindow_Ext = _My_IEHtmlWindow_Ext
# ***********************************************************************




# ***********************************************************************
_URL_Dots = {}
_URL_Webs = {}
def _Find_URL_Dots_Webs () :
  """Find all kinds of local help documents"""
  _URL_Dots [ 'python' ] = 'P:/Python/Doc/Python25.chm'

  _URL_Webs [ 'python' ] = 'http://www.python.org'
  _URL_Webs [ 'vpython' ] = 'http://www.python.org'
  
# Execute the procedure
_Find_URL_Dots_Webs ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Class_URL_Viewer ( wx.Panel ):
  def __init__ ( self, Parent, ini = None, name = 'URL_Viewer' ) :
    self.Dock = Parent
    self.Ini_File = ini
    self.My_Name = name
    wx.Panel.__init__ ( self, Parent )

    GUI = """
    MainPanel         ,PanelVer, 01
      P1              ,PanelHor, 000000001
        btn_Home      ,wx.Button     ,label = _(1,'Home')    ,style = wx.BU_EXACTFIT
        btn_Back      ,wx.Button     ,label = '<=='          ,style = wx.BU_EXACTFIT
        btn_Forward   ,wx.Button     ,label = '==>'          ,style = wx.BU_EXACTFIT
        btn_Stop      ,wx.Button     ,label = _(2,'Stop')    ,style = wx.BU_EXACTFIT
        btn_Search    ,wx.Button     ,label = _(3,'Search')  ,style = wx.BU_EXACTFIT
        btn_Refresh   ,wx.Button     ,label = _(4,'Refresh') ,style = wx.BU_EXACTFIT
        btn_Browse    ,wx.Button     ,label = _(6,'Browse')  ,style = wx.BU_EXACTFIT
        self.Loc_Text ,wx.StaticText ,label = _(5,'  Location:')
        self.Combo    ,wx.ComboBox   ,style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER
      self.Panel      ,PanelVer, 11
        self.Html     ,wx.html.HtmlWindow
    """
    # pos doesn't work:    text          ,wx.StaticText ,label = ' Location:' ,pos = ( 20, 25 )
    self.wxGUI = Create_wxGUI ( GUI, IniName = 'self.Ini_File' )

    btn_Home.   Bind ( wx.EVT_BUTTON,   self._On_Button_Home    )
    btn_Back.   Bind ( wx.EVT_BUTTON,   self._On_Button_Back    )
    btn_Forward.Bind ( wx.EVT_BUTTON,   self._On_Button_Forward )
    btn_Stop.   Bind ( wx.EVT_BUTTON,   self._On_Button_Stop    )
    btn_Search .Bind ( wx.EVT_BUTTON,   self._On_Button_Search  )
    btn_Refresh.Bind ( wx.EVT_BUTTON,   self._On_Button_Refresh )
    btn_Browse .Bind ( wx.EVT_BUTTON,   self._On_Button_Browse  )
    self.Combo .Bind ( wx.EVT_COMBOBOX, self._On_Combo_Select   )
    self.Combo .Bind ( wx.EVT_KEY_UP,   self._On_Combo_Key      )
    self.Combo .Bind ( wx.EVT_CHAR,     self._On_Combo_Char     )

    if Platform_Windows :
      # Hook up the event handlers for the IE window
      #IE = self.Html_IE
      IE = self.Html
      #IE.Bind ( iewin.EVT_BeforeNavigate2,   self._On_Before_Navigate2   )
      #IE.Bind ( iewin.EVT_NewWindow2,        self._On_New_Window2        )
      #IE.Bind ( iewin.EVT_DocumentComplete,  self._On_Document_Complete  )
      #IE.Bind ( iewin.EVT_NavigateComplete2, self._On_Document_Complete  )
      #IE.Bind ( iewin.EVT_ProgressChange,    self._On_Progress_Change    )
      #IE.Bind ( iewin.EVT_StatusTextChange,  self._On_Status_Text_Change )
      #IE.Bind ( iewin.EVT_TitleChange,       self._On_Title_Change       )

    self.Open_In_New_Window = None
    #self.Load ( 'http://mathworld.wolfram.com/' )

    # alternative names
    self.LoadUrl = self.Load

  # ********************************************************
  # ********************************************************
  def GetName ( self ) :
    return self.My_Name

  #***************************************************
  def _Display_URL ( self, URL, Local_Html = True ) :
    if Local_Html :
      self.Loc_Text.SetForegroundColour ( wx.RED )
      self.Loc_Text.Refresh()
      self.Html.Show ()
      self.Panel_box.Layout ()

      self.Html.LoadPage ( URL )
      translated_URL = 'CSS_translated.html'
      wxp_widgets.Translate_CSS ( URL, translated_URL ) #, self.CallBack_Html )
      self.Html.LoadPage ( translated_URL )

    else :
      self.Loc_Text.SetForegroundColour ( wx.BLUE )
      self.Loc_Text.Refresh()
      self.Html.Hide ()
      self.Panel_box.Layout ()
      self.Html.LoadPage ( URL )

  #***************************************************
  def Load ( self, URL ) :
    """
    Load some kind of page,
    either in the HtmlWindow or in IE
    """
    #print 'Load', URL
    # to get a uniform picture, replace all slashes with forward slashes
    URL = URL.replace ( '\\', '/' )
    if ( '//'   in URL ) or \
       ( '.pdf' in URL ) or \
       ( '.swf' in URL ) or \
       ( '.txt' in URL ) or \
       ( '.doc' in URL ) or \
       ( '.xls' in URL ) or \
       ( '.ppt' in URL ) :
      self._Display_URL ( URL, False )

    elif '.chm' in URL :
      Launch_CHM ( URL )

    elif not ( os.path.isfile ( URL ) ) :
      URL = 'http://' + URL
      self._Display_URL ( URL, False )

    else :
      self._Display_URL ( URL, True )

    # do history admin
    index = self._URL_In_History ( URL )
    if index :
      self.Combo.SetSelection ( index )
      
  #***************************************************
  def Save_Settings ( self, Ini_Section ) :
    ini = self.Ini_File
    if ini :
      ini.Section = Ini_Section
      self.wxGUI.Save_Settings ()
      #v3print ( 'SAVE AUTOMATIC:', self.wxGUI.Current_Settings )

  #***************************************************
  def _URL_In_History ( self, URL ) :
    """
    Tests if URL in History,
    if so: returns index
    if not: returns None and adds the URL to the ComboBox
    """
    URL = URL.replace ( '\\', '/' )
    #print 'URL_In_History', URL
    History = self.Combo.GetItems ()
    index = None
    if URL in History :
      index = History.index ( URL )
    elif URL + '/' in History :
      index = History.index ( URL + '/' )
    elif ( URL[-1] == '/' ) and ( URL [ : -1 ] in History ):
      index = History.index ( URL [ : -1 ] )
    else :
      self.Combo.Append ( URL )
    return index

  #***************************************************
  def _On_Button_Home ( self, event ) :
    """
    Goto the PyLab Works homepage.
    """
    #self.Html_IE.GoHome()
    self.Load ( 'http://pic.flappie.nl' )

  #***************************************************
  def _On_Button_Back ( self, event ) :
    """
    Goto the previous page ( if any )
    """
    #self.ie.GoBack()
    URL = self.Combo.GetValue ()
    index = self._URL_In_History ( URL )
    if index > 0 :
      History = self.Combo.GetItems ()
      self.Load ( History [ index - 1 ] )

  #***************************************************
  def _On_Button_Forward ( self, event ) :
    """
    Goto the next page ( if any )
    """
    #self.ie.GoForward()
    URL = self.Combo.GetValue ()
    index = self._URL_In_History ( URL )
    if index >= 0 :
      History = self.Combo.GetItems ()
      if index < ( len ( History ) - 1 ) :
        self.Load ( History [ index + 1 ] )

  #***************************************************
  def _On_Button_Stop ( self, event ) :
    """
    Stop the download process in IE
    """
    if Platform_Windows :
      pass
      
  #***************************************************
  def _On_Button_Search ( self, event ) :
    """
    Start a Google search.
    """
    self.Html.LoadPage ( 'http://www.google.com' )

  #***************************************************
  def _On_Button_Refresh ( self, event ) :
    """
    Refresh a IE page
    """
    if Platform_Windows :
      # Doesn't work : self.Html_IE.Refresh ( iewin.REFRESH_COMPLETELY )
      URL = self.Combo.GetValue ()
      self.Html.Load ( URL )

  #***************************************************
  def _On_Button_Browse ( self, event ) :
    """
    Browse local disks
    """
    from dialog_support import AskFileForOpen, FT_DOC_FILES
    FileName = AskFileForOpen ( FileTypes = FT_DOC_FILES )
    if FileName :
      self.Load ( FileName )

  #***************************************************
  def _On_Before_Navigate2 ( self, event ) :
    """
    On moving to a new page, Set wait cursor.
    """
    #print ' On_Nav2', event.URL
    self.SetCursor ( wx.StockCursor ( wx.CURSOR_WAIT ) )
    if not ( event.TargetFrameName                  ) and \
       not ( event.URL.startswith ( 'about:'      ) ) and \
       not ( event.URL.startswith ( 'res:'        ) ) and \
       not ( event.URL.startswith ( 'javascript:' ) ) :
      self._URL_In_History ( event.URL )  # if not in list add !!
      self.Combo.SetValue ( event.URL )
      
  #***************************************************
  def _On_New_Window2 ( self, event ) :
    """
    If the browser wants a new window,
    abort it and load the page manual.
    """
    #print 'On_New_Win', self.Open_In_New_Window
    event.Cancel = True
    # self.Open_In_New_Window is loaded by _On_Status_Text_Change
    wx.CallAfter ( self.Load, self.Open_In_New_Window )

  #***************************************************
  def _On_Document_Complete ( self, event ) :
    """
    When the page is fully donwloaded,
    Set cursor back to normal
    """
    #print '_On_Doc_Compl'
    self.SetCursor ( wx.StockCursor ( wx.CURSOR_DEFAULT ) )

  #***************************************************
  def _On_Progress_Change ( self, event ) :
    """
    Can be used to show download progress
    """
    return
    if event.Progress == event.ProgressMax == 0 :
      print ('***** ', self.Combo.GetValue ())

  #***************************************************
  def _On_Title_Change ( self, event ) :
    """
    Can be used to show Title in statusbar
    """
    return
    print ('Title', event.Text)

  #***************************************************
  def _On_Status_Text_Change ( self, event ) :
    """
    When hoovering over a link (which might be clicked),
    we store the link,
    So we can use this link when a new window is requested.
    """
    if event.Text :
      if event.Text.startswith ( 'http' ) :
        self.Open_In_New_Window = event.Text

  #***************************************************
  def _On_Combo_Select ( self, event ) :
    """
    Load the selected Page
    """
    self.Html.LoadPage ( self.Combo.GetValue () )

  #***************************************************
  def _On_Combo_Key ( self, event ) :
    """
    Load the page defined by the combo string.
    """
    if event.GetKeyCode() == wx.WXK_RETURN :
      URL = self.Combo.GetValue ()
      url = URL.lower ()
      FP = url.find ( '.' )
      Query = url [ FP+1 : ]
      Dots = url.split ( '.' )
      # generate a webpage with all settings
      if URL == '?' :
        # Create a html page of all links in the combo
        #dir = path_split ( __file__ ) [0] + '/'
        dir = sys._getframe().f_code.co_filename
        dir = os.path.split ( dir ) [0] +'/'
        
        dir = dir.replace ( '\\', '/' )

        v3print ( 'URL=? :', dir + 'help_combo_template.html' )

        fh = open ( dir + 'help_combo_template.html', 'r' )
        template = fh.read ()
        fh.close ()
        
        line = ''
        for item in self.Combo.GetStrings() :
          line += '<p>&nbsp; <a class=rvts4 href="' +\
                  item + '">' + \
                  item + '</a></p>'
        print()
        template = template.replace ( 'XXX', line )

        line = ''
        keys = _URL_ShortCuts.keys()
        keys.sort()
        for key in keys:
          line += '<p><span class=rvts10>' + key
          line += '</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
          line += _URL_ShortCuts [ key ] + '</p>'
        template = template.replace ( 'YYY', line )

        line = ''
        keys = _CHM_Links.keys()
        keys.sort()
        for key in keys:
          line += '<p><span class=rvts10>' + key
          line += '</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
          line += _CHM_Links [ key ] + '</p>'
        template = template.replace ( 'ZZZ', line )

        line = ''
        keys = _CTRL_Links.keys()
        keys.sort()
        for key in keys:
          line += '<p><span class=rvts10>' + key
          line += '</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
          line += _CTRL_Links [ key ] + '</p>'
        template = template.replace ( 'VVV', line )

        URL = dir + 'help_combo.html'
        fh = open ( URL, 'w' )
        fh.write ( template )
        fh.close ()
        

      elif ( len ( URL ) > 0 ) :
        # Dot expressions ".python"
        if URL.find ('.') == 0 :
          URL = URL [ 1: ]
          if URL in _URL_Dots :
            URL = _URL_Dots [ URL ]
          else :
            URL = ''

        # Web expressions "web.python"
        elif ( url.find ( 'web.' ) == 0 ) or\
             ( url.find ( 'w.')    == 0 ) :
          url = url [ FP+1 : ]
          if url in _URL_Webs :
            URL = _URL_Webs [ url ]
          else :
            URL = ''
            
        # DotDot expressions "w..http://buienradar.nl"
        # definitions of shortcuts
        elif URL.find ('..') > 0 :
          i = URL.find ( '..' )
          key = URL [ : i ]
          URL = URL [ i+2 : ]
          _URL_ShortCuts [ key ] = URL

        # Shortcuts like "g.pylab_works"
        elif Dots [0] in _URL_ShortCuts :
          URL = _URL_ShortCuts [ Dots [0] ]
          #print Dots
          #print URL
          if ( len ( Dots ) > 1 ) and ( len (Dots[1]) > 0 ) :
            if Dots[0] + '_' in _URL_ShortCuts :
              URL = _URL_ShortCuts [ Dots [0] + '_' ]
              URL = URL.replace ( '%%%%', Dots [1] )
            else :
              URL = URL.replace ( '%%%%', Dots [1] )
          else :
            URL = URL.replace ( '%%%%', '' )

          
        # Wikipedia expressions "wp.python" or "wpnl.python"
        # http://en.wikipedia.org/wiki/Vpython
        # http://en.wikipedia.org/wiki/Special:Search?search=
        elif ( url.find ( 'wp' ) == 0 ) :
          URL = 'http://'
          if FP == 2 :
            URL += 'en'
          else :
            URL += url [ 2:4 ]
          URL += '.wikipedia.org/wiki/'+ Query

      if URL :
        self.Load ( URL )

    else:
      event.Skip()

  #***************************************************
  def _On_Combo_Char ( self, event ) :
    """
    Prevents that Enter does something with combobox
    """
    if event.GetKeyCode () != wx.WXK_RETURN :
      event.Skip()

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Simple_Test_Form ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Simple GUI Demo', ini )

    #from language_support import Set_Language
    #Set_Language ( 'NL', True )

    self.Viewer = Class_URL_Viewer ( self, ini )
    self.Bind ( wx.EVT_CLOSE, self._On_Close )
    
  #***************************************************
  def _On_Close ( self, event ) :
    self.Viewer.Save_Settings ( self.Ini_Section )
    event.Skip ()
# ***********************************************************************


# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':

  Test_Defs ( 3 )

  ini = inifile ( os.path.join ( os.getcwd (), 'help_support_test.cfg' ) )

  #************************************************************************
  # test CHM files
  #************************************************************************
  if Test ( 1 ) :
    Help_Window = Help_Viewer_Class ( ini )
    Help_Window.Find ( u'sys', typ = 0 )
    import time
    #time.sleep(8)
    #Help_Window.Find ( u'os', typ = 0 )

  if Test ( 2 ) :
    Help_Window = Help_Viewer_Class ( ini )
    Help_Window.Find ( u'wx', typ = 1 )

    Help_Window = Help_Viewer_Class ( ini )
    Help_Window.Find ( u'wx', typ = 2 )

  if Test ( 3 ) :
    My_Main_Application ( Simple_Test_Form )
# ***********************************************************************
pd_Module ( __file__ )

