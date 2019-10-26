import __init__
# THIS MODULE MAY NOT USE _(,
# because the use of Create_wxGUI
# needs to search for the parent frame of gui_support

__doc__ = """
doc_string translated ?
"""

from language_support import  Language_Current, Set_Language, Flag_Object
from language_support import _


_Version_Text = []


# ***********************************************************************
_ToDo = """
 - if component placed on a Notebook is not a wx.Window,
   automatically insert a wx.Panel in between
 - better error message: remove the first 2 lines (non-info),
   and add filename of the calling file
 - PreView-wxGUI in AUI-panes
"""
# ***********************************************************************


# !!! import wx before any support library !!!
# otherwise the IDE won't do auto-suggest
import wx
import wx.lib.agw.flatnotebook as fnb
import wx.html as  html

import  wx.lib.buttons  as  buttons
BmpBut = buttons.GenBitmapButton


from inifile_support import *
# ***********************************************************************
# demo program
# ***********************************************************************
def My_Main_Application ( My_Form,
                          config_file = None,
                          Splash      = None ) :
  # we need an extra import here
  import wx
  app = wx.App ()

  if Splash :
    bmp = Get_Image_Resize ( Splash, 96 )
    wx.SplashScreen ( bmp,
                      wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
                      1000, None,
                      style = wx.NO_BORDER | wx.SIMPLE_BORDER | wx.STAY_ON_TOP )
    wx.Yield ()

  if config_file :
    ini = inifile ( config_file )
  else :
    #v3print ( 'gfdsawer', sys._getframe().f_code.co_filename, sys._getframe(1).f_code.co_filename )
    #ini = inifile ( Change_FileExt ( sys.argv[0], '_Test.cfg' ) )
    ini = inifile ( Change_FileExt ( sys._getframe(1).f_code.co_filename, '_Test.cfg' ) )

  frame = My_Form ( ini = ini )
  frame.Show ( True )

  if Application.WX_Inspect_Mode :
    import wx.lib.inspection
    wx.lib.inspection.InspectionTool().Show()

  app.MainLoop ()
  ini.Close ()
# **********************************************************************

# ***********************************************************************
# ***********************************************************************
class weg_My_HtmlWindow ( html.HtmlWindow ) :

  def Load_CSS ( self, URL, CallBack_Html = None ) :
    import wxp_widgets
    #,style=wx.NO_FULL_REPAINT_ON_RESIZE
    name_to = 'CSS_translated.html'
    wxp_widgets.Translate_CSS ( URL, name_to, CallBack_Html )
    self.LoadPage ( name_to )

    from wxp_widgets import CallBack_Html_Pointer
    if CallBack_Html and not ( CallBack_Html_Pointer ) :
      CallBack_Html_Pointer = CallBack_Html
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
GUI_EVT_CLOSE_PAGE = fnb.EVT_FLATNOTEBOOK_PAGE_CLOSING

class GUI_Notebook ( fnb.FlatNotebook ) :
  def __init__ ( self, parent = None, style = None  ) :
    if style == None :
      style = ( fnb.FNB_NO_X_BUTTON |
                fnb.FNB_X_ON_TAB |
                fnb.FNB_MOUSE_MIDDLE_CLOSES_TABS |
                fnb.FNB_DCLICK_CLOSES_TABS |
                fnb.FNB_DROPDOWN_TABS_LIST |
                fnb.FNB_ALLOW_FOREIGN_DND |
               0 )
    #            fnb.FNB_NO_NAV_BUTTONS |
    #            fnb.FNB_HIDE_ON_SINGLE_TAB |
    fnb.FlatNotebook.__init__ ( self, parent = parent, style = style )
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class My_Frame_Class ( wx.Frame ) :
  # *****************************************************************
  # *****************************************************************
  def __init__( self, main_form = None, Title = '',
                ini = None, Ini_Section = 'MiniFrame' ) :

    self.main_form = main_form
    FormStyle = wx.DEFAULT_FRAME_STYLE | wx.CAPTION
    #if parent:
    #  FormStyle = FormStyle | wx.FRAME_FLOAT_ON_PARENT    # needs a parent

    Pos  = ( 100, 100 )
    Size = ( 600, 400 )
    self.Ini_File    = ini
    self.Ini_Section = Ini_Section
    #from language_support import Language_Current
    if ini :
      ini.Section = self.Ini_Section
      Pos  = ini.Read ( 'Pos',  Pos  )
      Size = ini.Read ( 'Size', Size )
      Language = ini.Read ( 'Language', Language_Current[0] )
      if Language != Language_Current[0] :
        Set_Language ( Language, True )

    wx.Frame.__init__ (
        self, None, -1, Title,
        size  = Size,
        pos   = Pos,
        style = FormStyle )
    try :
      #import site
      #import inspect
      #print inspect.currentframe().f_code.co_filename
      #print site.abs__file__()
      #print ' FNFN', __file__, '$$$', self.__file__, '$$'
      #Icon_File = Joined_Paths ( os.path.split ( __file__ )[0],
      #                           #'../pictures/vippi_bricks_323.ico' )
      #                           'pictures/vippi_bricks_323.ico' )
      Icon_File = Module_Absolute_Path ( '..', 'pictures', 'vippi_bricks_323.ico' )
      self.SetIcon ( wx.Icon ( Icon_File, wx.BITMAP_TYPE_ICO ) )
    except :
      pass
    
    self.Bind ( wx.EVT_CLOSE,  self.__On_Close  )

  # *********************************************************
  # *********************************************************
  def __On_Close ( self, event ) :
    event.Skip ()
    ini = self.Ini_File
    if ini :
      ini.Section = self.Ini_Section
      ini.Write ( 'Pos',      self.GetPosition () )
      ini.Write ( 'Size',     self.GetSize ()     )
      ini.Write ( 'Language', Language_Current[0] )

    # if restart needed (i.e. in case of a language change)
    if Application.Restart :
      from system_support import Run_Python
      Run_Python ( Application.Application )
# ***********************************************************************

# ***********************************************************************
# Here are the definitions for saving and restoring settings
# For each item 2 strings need to be defined:
#   - the string to get the value from the component
#   - the string to set the value of the component
# There are substitues possible:
#   %% will be replaced by the name of the component (as it used in the forms init)
#   %  will be replaced by the value read from the config-file
# ***********************************************************************
_Save_Restore = {
  'Base_STC'          : ( 'Filename',          '%%.LoadFile(%)'        ),
  'wx.CheckBox'       : ( 'GetValue()',        '%%.SetValue(%)'       ),
  'wx.ComboBox'       : ( 'GetStrings()',      'for V in %: %%.Append(V)' ),
  'wx.Notebook'       : ( 'GetSelection()',    '%%.SetSelection(%)'   ),
  'wx.RadioBox'       : ( 'GetSelection()',    '%%.SetSelection(%)'   ),
  'wx.SplitterWindow' : ( 'GetSashPosition()', 'wx.CallLater ( 100, %%.SetSashPosition, % )' ),
  'wx.TextCtrl'       : ( 'GetValue()',        '%%.SetValue(str(%))'  ),
  'wx.ToggleButton'   : ( 'GetValue()',        '%%.SetValue(%)'       ),
}
# ***********************************************************************

# ***********************************************************************
# Special types for which an automatic import will be done
# ***********************************************************************
_Special_Types = {
'Base_STC'             : [ 'from Scintilla_support import Base_STC'         ,0 ],
'Base_Grid'            : [ 'from grid_support import Base_Grid'             ,0 ],
'Base_Table_Grid'      : [ 'from grid_support import Base_Table_Grid'       ,0 ],
'Class_URL_Viewer'     : [ 'from help_support import Class_URL_Viewer'      ,0 ],
'Custom_TreeCtrl_Base' : [ 'from tree_support import Custom_TreeCtrl_Base'  ,0 ],
'Float_Slider'         : [ 'from float_slider import Float_Slider'          ,0 ],
#'iewin.IEHtmlWindow'   : [ 'import wx.lib.iewin as iewin'                   ,0 ],
'MultiSplitterWindow'  : [ 'from wx.lib.splitter import MultiSplitterWindow',0 ],
#'My_HtmlWindow'        : [ 'from gui_support  import My_HtmlWindow'         ,0 ],
'_My_HtmlWindow'     : [ 'from help_support import _My_HtmlWindow'      ,0 ],
'NavCanvas.NavCanvas'  : [ 'from wx.lib.floatcanvas import NavCanvas, FloatCanvas', 0 ],
'_PlotCanvas'          : [ 'from scope_plot import _PlotCanvas'              ,0 ],
'_PlotCanvas_History'  : [ 'from scope_plot_hist import _PlotCanvas_History' ,0 ],
'ScrolledPanel'        : [ 'from wx.lib.scrolledpanel import ScrolledPanel' ,0 ],
'tBase_Scope_with_History' : ['from control_scope_base import tBase_Scope_with_History' ,0],
'wx.html.HtmlWindow'   : [ 'import wx.html'                                 ,0 ],
}
#    import  my_iewin   as iewin
# ***********************************************************************

# ***********************************************************************
# You can specify any additional paramater,
# just in the order they would normally appear
# just DONT specify "self, parent", these are done automatically
#
# Example (see also at the bottom of this module)
#    GUI = """
#    self.NB       ,wx.Notebook   ,style = wx.NO_BORDER
#      self.Grid   ,Base_Table_Grid ,None, data_values, data_types, data_defs
#      Panel2      ,PanelVer, 11  ,name  = "Page2"
#        list1     ,wx.ListCtrl   ,style = wx.LC_REPORT
#    """
#    self.wxGUI = Create_wxGUI ( GUI )
# ***********************************************************************
class Create_wxGUI ( object ) :
  def __init__ ( self,
                 GUI,
                 IniName   = '',
                 my_parent = 'self',
                 code      = ''  ) :

    self.code   = code
    new_globals = []
    Imports     = []
    # Clear the implicit import counter
    for typ in _Special_Types :
      _Special_Types [ typ ] [1] = 0

    # prepare Save / Restore settings parameters
    if IniName :
      IniFile_Read  = IniName + '.Read ( '
      IniFile_Write = IniName + '.Write ( '
      Restore_Settings = ''
      self.Current_Settings = ''

    # Initialize the stack with the input values
    stack = []
    stack.append ( [ 0, my_parent, None, [], '' ] )
    first_element = None

    # traverse to all the lines in the definition
    for lnr, defi in enumerate ( GUI.split('\n') ) :

      # split the line into elements, and stop if not enough elements
      defi = defi.split(',')
      if len ( defi ) < 2 : continue

      # get the first element
      if not ( first_element ) :
        first_element = defi[0].strip()

      # determine the leading spaces
      indent = len ( defi[0] ) - len ( defi[0].lstrip() )

      # remove white space from all elements
      for i,item in enumerate ( defi ) :
        defi[i] = defi[i].strip()

      # special pre-processing of
      #   - SplitterWindow
      #   - Panels + Sizers
      weights = ''
      if defi[1] in [ 'SplitterHor', 'SplitterVer' ] :
        typ = 'wx.SplitterWindow'

      elif defi[1] in [ 'MultiSplitterHor', 'MultiSplitterVer' ] :
        typ = 'MultiSplitterWindow'

      elif defi[1] in [ 'PanelHor', 'PanelVer',
                        'PageHor', 'PageVer' ] :
        typ = 'wx.Panel'

        # get the weight factors (if any) and remove them
        if len ( defi ) > 2 :
          weights = defi[2]
          del defi[2]

      else :
        typ = defi[1]

      # parse the line: <name> <type> <params>
      name = defi[0]
      if len ( defi ) > 2 : params = ','+ ','.join ( defi[2:] )
      else :                params = ''

      # ****************************************************************
      # Also a good position to generate code to save / restore settings
      # Components are only added if the following conditions are met:
      #   - must have a name starting with "self." (otherwise we can't save it)
      #   - must be definied in the _Save_Restore dictionary
      # ****************************************************************
      if IniName and (typ) in _Save_Restore and ( name.find ( 'self.' ) == 0 ) :
        SR = _Save_Restore [ typ ]

        line = 'if ' + IniName + ':'
        Restore_Settings += line + '\n'
        line = '  Value = ' + IniFile_Read + '"' + name [ 5: ] + '", None )'
        Restore_Settings += line + '\n'
        line = '  if Value != None :'
        Restore_Settings += line + '\n'
        Name = name
        line = ('    ' + SR[1] ).replace ( '%%', Name ).replace ( '%', 'Value' )
        Restore_Settings += line + '\n'

        line = 'Value = ' + name + '.' + SR[0]
        self.Current_Settings += line + '\n'
        line = IniFile_Write + '"' + name [ 5: ] + '" , Value )'
        self.Current_Settings += line + '\n'
      # ****************************************************************

      # ****************************************************************
      # test for special types and do an explicit import
      # ****************************************************************
      #print 'Name, typ',name,typ
      if typ in _Special_Types :
        ST = _Special_Types [ typ ]
        #print 'SPECIAL', typ, ST
        if ST [1] == 0 :
          Imports.append ( ST[0] )
          ST [1] = 1
      # ****************************************************************


      # Get parent, by searching a parent (= lesser indent)
      self.code = self._Pop_For_Parent ( indent, stack, self.code )
      if self.code == False : return False
      parent = stack [-1]

      # If parent is one of the special ones,
      # Add all children to it's list
      if parent[2] in [ 'SplitterHor', 'SplitterVer', 'wx.SplitterWindow',
                        'PanelHor', 'PanelVer',
                        'wx.Notebook', 'GUI_Notebook' ] :
        stack [-1][3].append ( name )

      # Add the current component to the stack
      stack.append ( [ indent, name, defi[1], [], weights ])


      #******************************************************************
      # Create the component
      #******************************************************************
      if typ in [ 'MultiSplitterWindow' ] :
        self.code += name + '=' + typ + '( ' + parent[1] + params + ', style=wx.SP_LIVE_UPDATE)\n'
      else :
        self.code += name + '=' + typ + '( ' + parent[1] + params + ')\n'
      #******************************************************************


      if defi[1] in [ 'MultiSplitterVer' ] :
        self.code += name + '.SetOrientation(wx.VERTICAL)\n'


      # if parent is multi-splitter, append component
      if parent[2] in [ 'MultiSplitterWindow', 'MultiSplitterHor', 'MultiSplitterVer' ]:
        self.code += parent[1] + '.AppendWindow' + '( ' + name + ')\n'

      #self.code += 'print "CREATE COMP",'+ name + '\n'

      # now if the component doesn't start with "self",
      # we need to add it to the global list
      if name.strip().find ( 'self.' ) != 0 :
        new_globals.append ( name )

    # While there are still elements on the stack,
    # Remove them and perform the actions (Splitter / Sizers / ...)
    indent = 0
    self.code = self._Pop_For_Parent ( indent, stack, self.code )
    if self.code == False : return False

    # Size the main component on the parent
    # What if more than 1 component on the lowest level ??
    # only if main component is a wx.Window or wx.Sizer
    self.code += 'if isinstance (' + first_element +',wx.Window ) or '
    self.code +=    'isinstance (' + first_element + ',wx.Sizer ) :\n'
    self.code += '  Sizer = wx.BoxSizer ( ) \n'
    self.code += '  Sizer.Add ( ' + first_element + ', 1, wx.EXPAND ) \n'
    self.code += '  ' + my_parent + '.SetSizer ( Sizer ) \n'

    # and add the load setting from ini file
    if IniName :
      self.code += Restore_Settings

    # Add the globals to the code,
    # otherwise they are not (very well) visible in the parents namespace
    if len ( new_globals ) > 0 :
      self.code = 'global ' + ','.join( new_globals ) + '\n' + self.code

    #print 'Imports', Imports
    line = ''
    for item in Imports :
      #print 'Import',item
      line += item + '\n'
    if line :
      self.code = line + self.code

    # now create the components on the form,
    # by executing the code in the parent's frame namespace
    p_locals  = sys._getframe(1).f_locals
    p_globals = sys._getframe(1).f_globals
    try :
      # The exec function is only available from 2.6,
      # but seems to already in 2.5 !!
      # It might be better to use the globals only, because
      #  - in the doc there's a warning when making changes to locals
      #  - it doesn't always work ????
      # No that doesn't work either !!!
      #exec self.code in p_globals, p_locals
      
      
      print ('[PARAMATER CODE]', self.code)

      exec ( self.code, p_globals, p_locals )
      #exec ( self.code, globals())
      #exec ( self.code, p_globals )
    except :
      print('********** ERROR in GUI-string *************')
      for i, line in enumerate ( self.code.split('\n') ) :
        print (i + 1, line)
      print ('**********')
      sys.excepthook ( *sys.exc_info () )

      import inspect
      Frame_Info = inspect.getframeinfo ( sys._getframe (1) )
      print ('Error File :', Frame_Info [0])
      print ('Error Func :', Frame_Info [2])
      print ('Error Line :', Frame_Info [1])
      print ('Error Code :', Frame_Info [3] [ Frame_Info [4] ])

      print ('********** End ERROR in GUI-string *************')

  # ********************************************************
  # ********************************************************
  def Ready ( self ) :
    pass

  # ********************************************************
  # ********************************************************
  def Save_Settings ( self ) :
    # now store the components settings
    # by executing the code in the parent's frame namespace
    p_locals  = sys._getframe(1).f_locals
    p_globals = sys._getframe(1).f_globals
    #v3print ('GUI saving', self.Current_Settings )
    try    : exec ( self.Current_Settings, p_globals, p_locals )
    except : pass

  # ********************************************************
  # ********************************************************
  def _Pop_For_Parent ( self, indent, stack, code ) :
    # Breakdown the stack until we find an element with a smaller indent
    # which is the parent or container
    while ( len ( stack ) > 0 ) and \
          ( stack [-1] [0] >= indent ):
      last = stack.pop()

      # If a SplitterWindow is popped, add the hor/ver setting
      # I don't find the names hor / ver very logical, so I exchanged them !!
      if last[2] in [ 'wx.SplitterWindow', 'SplitterVer', 'SplitterHor' ] :
        if last[2] in [ 'wx.SplitterWindow', 'SplitterVer' ] :
          code += last[1] + '.SplitHorizontally ( '
        elif last[2] in [ 'SplitterHor' ] :
          code += last[1] + '.SplitVertically ( '

        # Add the 2 elements to the Splitter
        # (The extra comma at the end doesn't seem to bother)
        for element in last[3] :
          code += element + ','
        code += ')\n'

        # ERROR
        if len ( last [3] ) != 2 :
          print ('******* ERROR splitter " ' + last[1] + '"does not have 2 controls')
          return False

        # Add minimum panesize
        code += last[1] + '.SetMinimumPaneSize(50)\n'

      # If a Panel with a Sizer is popped from the stack
      # Create the sizer, add all the elements and assign the Sizer
      elif last[2] in [ 'PanelVer', 'PanelHor' ] :

        # Create the Sizer
        if last[2] == 'PanelHor' :
          code += last[1] + '_box = wx.BoxSizer ( wx.HORIZONTAL )\n'
        else :
          code += last[1] + '_box = wx.BoxSizer ( wx.VERTICAL )\n'

        # get weights, and be sure we have enough of them
        weights = last[4]
        while len ( weights ) < len ( last[3] ):
          weights += '1'

        # Add the elements to the Sizer and their weights
        for i,element in enumerate ( last[3] ) :
          code += last[1] + '_box.Add ( ' + element + ','+ \
                  str(weights[i]) + ', wx.EXPAND,5 )\n'

        # Assign the Sizer to its parent
        code += last[1] + '.SetSizer ( ' + last[1] + '_box )\n'

      # Add all elements as Pages to the Notbook
      # imageId is inserted as the page-index-number
      # (it won't harm if no imagelist is assigned)
      elif last[2] in [ 'wx.Notebook', 'GUI_Notebook' ] :
        line = last[1] + '.AddPage ( '
        for i, element in enumerate ( last[3] ) :
          code += 'name = ' + element + '.GetName() \n'

          # Changed to let it run under Ubuntu: don't specify the imageId
          #code += line + element + ', name, imageId = ' + str(i) + ') \n'
          code += line + element + ', name' + ') \n'
        ## Generated code for each page:
        ##   name = Panel1.GetName()
        ##   self.NB.AddPage ( self.Panel1, name, imageId = 0)
        ##   name = Panel2.GetName()
        ##   self.NB.AddPage ( self.Panel2, name, imageId = 1)

    return code
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
def PreView_wxGUI ( Text ) :
  Text = Text.replace ( '\r', '' )
  Lines = Text.split ( '\n' )

  # first locate the instance creation
  for N, line in enumerate ( Lines ) :
    if line.find ( 'Create_wxGUI' ) > 0 :
      line = line.strip ()
      break
  else :
    return

  # parse the line, to find the name and the GUI-string
  i = line.find ( '=' )
  if i >= 0 :
    Name = line [ : i ].strip()
    line = line [ i+1 : ].strip()
  else :
    Name = None
  line = line.replace ( '(', ',' )
  line = line.replace ( ')', ',' )
  #print line
  GUI_String = line.split ( ',' ) [1].strip()

  # see if there is a Ready method
  for X, line in enumerate ( Lines [ N : ] ) :
    #print '***', line
    if line.find ( Name + '.Ready' ) > 0 :
      N += X
      break

  #print 'FIND',Name, GUI_String

  # find the start of the GUI_string
  for M, line in enumerate ( Lines ) :
    i = line.find ( GUI_String )
    if i >= 0 :
      #print i,M
      ii = line.find ( '=', i+1 )
      if ii > 0 :
        ii = line.find ( '"""', ii+1 )
        if ii >= 0 :
          GUI_Code = line [ ii + 3 : ].strip ()
          #print 'STRAT OF GUICODE',GUI_Code
          break
  else :
    return

  for line in Lines [ M+1 : N+1 ] :
    GUI_Code += line + '\n'

  #print 'GC',GUI_Code

  fh = open ( '../support/gui_template_dont_touch.py', 'r' )
  Text = fh.read ()
  fh.close ()

  Text = Text.replace ( '%%%"""', GUI_Code )
  #print 'Final',Text

  filename = '../support/gui_f12_templatetest.py'
  fh = open ( filename, 'w' )
  fh.write ( Text )
  fh.close ()
  from system_support import Run_Python
  Run_Python ( filename )
# ***********************************************************************

from   picture_support import *

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


    GUI = """
    self.Splitter_Plots    ,SplitterVer
      self.Panel           ,PanelVer, 010
        self.Panel_Top     ,PanelHor, 11
          label1           ,wx.StaticText  ,label = "Signal1"
          label2           ,wx.StaticText  ,label = "Signal2"
        self.Panel_X       ,wx.Panel, 11
        self.Panel_Bottom  ,PanelHor
          label11          ,wx.StaticText  ,label = "Signal1b"
          label12          ,wx.StaticText  ,label = "Signal2b"
      Panel_B              ,wx.Panel
        Button_1           ,wx.Button      ,label = "Test"
        Button_2           ,wx.Button      ,label = "Test2", pos = (100,0)
    """

    GUI = """
    self.NB       ,wx.Notebook   ,style = wx.NO_BORDER
      self.Grid   ,Base_Table_Grid ,data_values, data_types, data_defs
      Panel2      ,PanelVer, 11  ,name  = "Page2"
        list1     ,wx.ListCtrl   ,style = wx.LC_REPORT
    """

    ##self.MenuBar = Class_Menus ( self )
    GUI = """
    NB            ,wx.Notebook   ,style = wx.NO_BORDER
      Panel1      ,PanelVer, 1   ,name  = "Hello"
        list1     ,wx.ListCtrl   ,style = wx.LC_REPORT
      Panel2      ,PanelVer, 11  ,name  = "Page2"
        window1   ,wx.Window
        window2   ,wx.Window
    """


    from tree_support import Custom_TreeCtrl_Base
    GUI = """
    self.SplitV            ,SplitterVer, style = wx.SP_LIVE_UPDATE | wx.SP_3DSASH
      self.Split           ,SplitterHor, style = wx.SP_LIVE_UPDATE | wx.SP_3DSASH
        self.Tree          ,Custom_TreeCtrl_Base
        self.NB            ,wx.Notebook, style = wx.NO_BORDER
          p1               ,wx.Panel, style = wx.NO_BORDER
          p2               ,wx.Panel, style = wx.NO_BORDER
      self.Error           ,PanelVer
        self.Log           ,wx.TextCtrl, style = wx.TE_MULTILINE | wx.TE_READONLY
    """

    GUI = """
    self.Split           ,SplitterHor, style = wx.SP_LIVE_UPDATE | wx.SP_3DSASH
      self.Tree          ,Custom_TreeCtrl_Base
      self.Log           ,wx.TextCtrl, style = wx.TE_MULTILINE | wx.TE_READONLY
    """
    """
    sel = self.Tree.root
    NewItem = self.Tree.AppendItem ( sel, 'new' )
    NewItem = self.Tree.AppendItem ( sel, 'new' )
    NewItem = self.Tree.AppendItem ( sel, 'new' )
    self.Tree.Bind ( wx.EVT_RIGHT_DOWN,            self.OnRightDown )
    self.Tree.Bind ( wx.EVT_CONTEXT_MENU, self.OnShowPopup )

    Set_NoteBook_Images ( NB, ( 47, 76 ) )
    """

    GUI = """
    self.NB       ,wx.Notebook   ,style = wx.NO_BORDER
      self.Grid   ,Base_Table_Grid ,data_values, data_types, data_defs
      Panel2      ,PanelVer, 11  ,name  = "Page2"
        list1     ,wx.ListCtrl   ,style = wx.LC_REPORT
    """
    GUI = """
      Panel2      ,PanelVer, 11  ,name  = "Page2"
        list1     ,wx.ListCtrl   ,style = wx.LC_LIST
    """
    """
    list1.Append ( ('aap','beer','colaoa') )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap') )
    list1.Append ( ('aap') )
    list1.Append ( ('aap') )
    list1.Append ( ('aap') )
    list1.Append ( ('aap') )
    list1.Append ( ('aap') )
    list1.Append ( ('aap') )
    list1.Append ( ('aap') )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    list1.Append ( ('aap',) )
    #list1.InsertColumn ( 0, 'col1' )
    #list1.InsertColumn ( 1, 'col2' )
    """


    # ***********************************************************************
    #from   picture_support import *
    bmp_PW    = Get_Image_Resize ( 'vippi_bricks_64.png',          64 )
    bmp_IDE   = Get_Image_Resize ( 'applications-accessories.png', 48 )
    bmp_Lib   = Get_Image_Resize ( 'bieb.png',                     48 )
    bmp_Trans = Get_Image_Resize ( 'romanime0.ico',                48 )

    self.Flags = Flag_Object ()
    bmp_Flag = self.Flags.Get_Flag ( Language_Current[0] )
    if not bmp_Flag.IsOk():
      bmp_Flag = wx.EmptyBitmap(32,22)
      self.clearBmp ( bmp_Flag )

    import wx.html as  html
    #import  my_iewin   as iewin

    #self.NB         ,wx.Notebook   ,style = wx.NO_BORDER
    GUI = """
    self.NB         ,GUI_Notebook
     Panel2         ,PanelHor,  01  ,name  = 'Main'
      Panel_B       ,wx.Panel  ,size =( 120, -1)
        B_PW        ,BmpBut    ,bitmap = bmp_PW            ,pos = (24, 10) ,size = ( 70,70)
        self.B_Flag ,BmpBut    ,bitmap = bmp_Flag          ,pos = ( 0, 62) ,size = ( 20,14)
        B_PW_Run    ,wx.Button ,label = "PyLab Works"      ,pos = ( 0, 80) ,size = ( 120,20)

        B_IDE       ,BmpBut    ,bitmap = bmp_IDE           ,pos = (24,110) ,size=( 70,70)
        B_IDE_Run   ,wx.Button ,label = "IDE"              ,pos = ( 0,180) ,size=(120,20)

        B_Lib       ,BmpBut    ,bitmap = bmp_Lib           ,pos = (24,210) ,size=( 70,70)
        B_Lib_Run   ,wx.Button ,label = "Library Manager"  ,pos = ( 0,280) ,size=(120,20)

        B_Trans     ,BmpBut    ,bitmap = bmp_Trans         ,pos = (24,310) ,size=( 70,70)
        B_Trans_Run ,wx.Button ,label = "Translation Tool" ,pos = ( 0,380) ,size=(120,20)

        st1         ,wx.StaticText,label = 'CommandLine Flags'  ,pos = (5,410)
        cb1         ,wx.CheckBox ,label = 'debug'               ,pos = (5,425)
        cb1         ,wx.CheckBox ,label = 'debugfile'           ,pos = (5,440)
      self.IE       ,iewin.IEHtmlWindow, style = wx.NO_FULL_REPAINT_ON_RESIZE


     self.Split_Demo  ,SplitterHor, name = 'Demos'
       p4           ,PanelVer , 1000       ,name = 'Demos'
        self.Tree     ,Custom_TreeCtrl_Base
        p4b           ,PanelHor ,11       ,name = 'Demos'
          B_Expand    ,wx.Button ,label = "Expand"
          B_Expands    ,wx.Button ,label = "Collapse"
        p4bb           ,PanelHor ,11       ,name = 'Demos'
          B_Expandb    ,wx.ToggleButton ,label = "Application"
          B_Expandsb    ,wx.ToggleButton ,label = "Design"
        B_Restore    ,wx.Button ,label = "Restore Orginal"
       self.Html     ,html.HtmlWindow ,style=wx.NO_FULL_REPAINT_ON_RESIZE


     Split_V2       ,SplitterVer    ,name = 'Tests'
      self.List_Test,wx.ListCtrl    ,style = wx.LC_LIST
      p3            ,PanelHor,10    ,name = 'Demos'
       self.Log     ,wx.TextCtrl    ,style = wx.TE_MULTILINE
       p4           ,wx.Panel       ,name = 'Demos'
        B_Run_Sel   ,wx.Button      ,label = "Run Sel"          ,pos = (0,0)
        B_Run_All   ,wx.Button      ,label = "Run All"          ,pos = (0, 25)
        self.CB_Debug     ,wx.CheckBox ,label = 'debug'               ,pos = (0,50)
        self.CB_DebugFile ,wx.CheckBox ,label = 'debugfile'           ,pos = (0,70)
        self.RB_Tests     ,wx.RadioBox ,label='Tests', choices=['Original', 'All', 'Choice'] ,majorDimension=1 ,pos = (0,90)
        self.Test_Choice  ,wx.TextCtrl                          ,pos = (0,175), size =(75,-1)
    """
    #self.wxGUI = Create_wxGUI ( GUI )
    #from picture_support import Get_Image_List
    #self.NB.AssignImageList ( Get_Image_List () )
    # ***********************************************************************


    # ***********************************************************************
    from tree_support import Custom_TreeCtrl_Base
    GUI = """
    self.SplitV         ,SplitterHor, style = wx.SP_LIVE_UPDATE | wx.SP_3DSASH
      p1               ,wx.Panel, style = wx.NO_BORDER
      p2               ,wx.Panel, style = wx.NO_BORDER
    """
    GUI = """
    self.Splitter      ,SplitterHor
      p1               ,wx.Panel
      p2               ,wx.Panel
    """


    # ***********************************************************************
    # Scope Display with History display
    # ***********************************************************************
    GUI = """
      self.Scope     ,tBase_Scope_with_History
    """
    self.wxGUI = Create_wxGUI ( GUI )
    print (self.wxGUI.code)


    # ***********************************************************************


    # ***********************************************************************
    GUI = """
      self.SplitV         ,SplitterVer
        self.Edit         ,Base_STC
        self.Edit2         ,Base_STC
    """
    #from Scintilla_support import Base_STC
    #self.wxGUI = Create_wxGUI ( GUI )
    # ***********************************************************************

    # ***********************************************************************
    w = 85
    h = 24
    GUI = """
    self.Split                   ,SplitterHor
      self.Edit                  ,Base_STC
      p1                         ,PanelHor  ,01
        p2                       ,wx.Panel
          self.B_Calculate       ,wx.Button     ,label = 'Calculate'      ,pos = (0,0)   ,size = (w,h)
          self.B_Save_Settings   ,wx.Button     ,label = 'Save_Settings'  ,pos = (0,30)  ,size = (w,h)
          self.B_Load_Settings   ,wx.Button     ,label = 'Load_Settings'  ,pos = (0,60)  ,size = (w,h)
          self.B_Kill            ,wx.Button     ,label = 'Kill'           ,pos = (0,90)  ,size = (w,h)
          self.B_ForGroundColor  ,wx.Button     ,label = 'ForGroundColor' ,pos = (0,120) ,size = (w,h)
        p3                       ,PanelVer  ,010
          p5                     ,PanelHor  ,010
            self.B_GetValue      ,wx.Button     ,label = 'Get'                           ,size=(40,h)
            Label_Top            ,wx.StaticText ,label = 'Value'          ,style=wx.ALIGN_CENTER
            self.B_SetValue      ,wx.Button     ,label = 'Set'                           ,size=(40,h)
          self.Value             ,wx.TextCtrl   ,style = wx.TE_MULTILINE
          p4                     ,wx.Panel
            self.B_GetSize       ,wx.Button     ,label = 'GetSize'        ,pos = (0,0)   ,size =(50,h)
            self.L_GetSize       ,wx.StaticText ,label = 'GetSize'        ,pos = (55,5)
            self.B_GetID         ,wx.Button     ,label = 'GetID'          ,pos = (0,25)  ,size =(50,h)
            self.L_GetID         ,wx.StaticText ,label = 'GetID'          ,pos = (55,30)
    """
    #from Scintilla_support import Base_STC
    #self.wxGUI = Create_wxGUI ( GUI )
    # ***********************************************************************


    # ***********************************************************************
    GUI = """
    self.NB       ,wx.Notebook   ,style = wx.NO_BORDER
      p4           ,wx.Panel       ,name = 'Demos'
      Panel2      ,PanelVer, 11  ,name  = "Page2"
        list1     ,wx.ListCtrl   ,style = wx.LC_REPORT
    """
    #self.wxGUI = Create_wxGUI ( GUI )
    # ***********************************************************************

    #print self.wxGUI.code

  def OnRightDown ( self, event ) :
    print ('MOUSE RIGHT')
    #event.Skip()

  def OnShowPopup ( self, event ) :
    print ('POPUP')
    #event.Skip()
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class Test_Dynamic_Form ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Simple GUI Demo', ini )

    GUI = """
    Splitter1         ,SplitterHor
      Panel_Left      ,wx.Panel
        self.N_Button ,wx.TextCtrl
        self.N_Slider ,wx.TextCtrl              ,pos = ( 0, 25 )
        Button_Go     ,wx.Button,  label = "Go" ,pos = ( 0, 50 )
      self.Panel      ,wx.ScrolledWindow
    """
    self.wxGUI = Create_wxGUI ( GUI )
    Button_Go.Bind ( wx.EVT_BUTTON, self._On_Go )
    self.Panel.Bind ( wx.EVT_SIZE, self._On_Size )
    #print self.wxGUI.code
    # ***********************************************************************

    self.Buttons = []
    self.Sliders = []

  def _On_Size ( self, event = None ) :
    x = 0
    w = event.GetSize () [0] - 15
    if len ( self.Buttons ) > 0 :
      x += 75
    w -= x
    for Slider in self.Sliders :
      Slider.SetPosition ( ( x, -1 ) )
      Slider.SetSize     ( ( w, -1 ) )

  def _On_Go ( self, event = None ) :
    N_Button = int ( self.N_Button.GetValue () )
    N_Slider = int ( self.N_Slider.GetValue () )

    # Correct the number of buttons
    N = len ( self.Buttons )
    BH = 25
    BW = 75
    if N_Button < N :
      for i in range ( N - N_Button ) :
        Button = self.Buttons.pop ()
        Button.Hide ()
        del Button
    elif N_Button > N :
      for i in range ( N_Button - N ) :
        N += 1
        Button = wx.Button ( self.Panel, label = 'Button ' + str ( N ),
                             pos= ( 0, (N-1)*BH ) )
        self.Buttons.append ( Button )

    from float_slider import Float_Slider
    N = len ( self.Sliders )
    x = 0
    SH = 55
    if N_Button > 0 :
      x = 75
    if N_Slider < N :
      for i in range ( N - N_Slider ) :
        Slider = self.Sliders.pop ()
        Slider.Hide ()
        del Slider
    elif N_Slider > N :
      for i in range ( N_Slider - N ) :
        N += 1
        Slider = Float_Slider ( self.Panel,
           caption  = 'Slider' + str (N),
           pos = ( x, (N-1) * SH ),
           size = ( self.Panel.GetSize () [0] - x, SH ) )
        if N % 2 > 0 :
          Slider.SetForegroundColour ( wx.BLUE )
          Slider.SetBackgroundColour ( wx.RED )
        self.Sliders.append ( Slider )

    maxH = max ( N_Button * BH, N_Slider * SH )
    self.Panel.SetScrollbars ( 1, 1, 10, maxH )

    # Repositioning and resizing doesn't happen automatically
    # SendSizeEvent doesn't work either
    if maxH > self.Panel.GetSize () [1] :
      Scroll = 15
    else :
      Scroll = 0
    for Slider in self.Sliders :
      Slider.SetSize ( ( self.Panel.GetSize () [0] - x - Scroll, -1 ) )
      Slider.SetPosition ( ( x, -1 ) )
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class Test_Brick_BP_Form ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Simple GUI Demo', ini )

    #    C2R2         ,PanelVer
    GUI = """
    SplitVer           ,SplitterVer
      SplitHor         ,MultiSplitterHor
        P1             ,PanelVer ,01
          T1           ,wx.StaticText ,label = 'Var'
          self.SplitC1   ,MultiSplitterVer
            C1R1         ,wx.Panel
             B11         ,wx.Button,  label = "Go"
            C1R2         ,wx.Panel
             B12         ,wx.Button,  label = "Go"
            C1R3         ,wx.Panel
             B13         ,wx.Button,  label = "Go"
        P2             ,PanelVer ,01
          T2           ,wx.StaticText ,label = 'Before'
          self.SplitC2 ,MultiSplitterVer
            L21        ,wx.TextCtrl, style = wx.TE_MULTILINE
            L22        ,wx.TextCtrl, style = wx.TE_MULTILINE
            L23        ,wx.TextCtrl, style = wx.TE_MULTILINE
        P3             ,PanelVer ,01
          T3           ,wx.StaticText ,label = 'After'
          self.SplitC3  ,MultiSplitterVer
            L31        ,wx.TextCtrl, style = wx.TE_MULTILINE
            L32        ,wx.TextCtrl, style = wx.TE_MULTILINE
            L33        ,wx.TextCtrl, style = wx.TE_MULTILINE
      BP               ,PanelVer ,01
        P6             ,PanelHor ,01
          T6           ,wx.StaticText ,label = 'BP Condition'
          Cond           ,wx.TextCtrl
        shell          ,wx.TextCtrl, style = wx.TE_MULTILINE
    """
    self.wxGUI = Create_wxGUI ( GUI )
    #print self.wxGUI.code


    #self.SplitC1.Bind ( wx.EVT_SPLITTER_SASH_POS_CHANGED,  self.OnChanged  )
    self.SplitC1.Bind ( wx.EVT_SPLITTER_SASH_POS_CHANGING, self._Split_Change1 )
    self.SplitC2.Bind ( wx.EVT_SPLITTER_SASH_POS_CHANGING, self._Split_Change2 )
    self.SplitC3.Bind ( wx.EVT_SPLITTER_SASH_POS_CHANGING, self._Split_Change3 )

  def _Split_Change1 ( self, event ) :
    i   = event.GetSashIdx()
    pos = event.GetSashPosition()
    self.SplitC2.SetSashPosition ( i, pos )
    self.SplitC3.SetSashPosition ( i, pos )

  def _Split_Change2 ( self, event ) :
    i   = event.GetSashIdx()
    pos = event.GetSashPosition()
    self.SplitC1.SetSashPosition ( i, pos )
    self.SplitC3.SetSashPosition ( i, pos )

  def _Split_Change3 ( self, event ) :
    i   = event.GetSashIdx()
    pos = event.GetSashPosition()
    self.SplitC1.SetSashPosition ( i, pos )
    self.SplitC2.SetSashPosition ( i, pos )
# ***********************************************************************

# ***********************************************************************
# ***********************************************************************
class Test_Control_Scope ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Test of Control_Scope', ini )

    import copy
    import wx
    import wx.grid as gridlib
    #from   grid_support    import *
    from   grid_support import MY_GRID_COL_TYPED, MY_GRID_ROW_FIXED, MY_GRID_TYPE_COLOR

    data_values = [
      [ 'Name', 'On', 'NumOn', 'Lower','Upper',
        'AC', 'AC[s]', 'Delay[s]',
        'LineColor', 'LineWidth',
        'World-1', 'Cal-1', 'World-2', 'Cal-2' ] ]
    data_values_default = [
      'Signal i', False, True, -10, 10,
      False, 1, 0,
      (200,0,0), 2, 0, 0, 1, 1 ]


    for i in range (16 ):
      default = copy.copy ( data_values_default )
      default[0] = ' Signal ' + str(i+1) + ' [Volt]'
      A, B = 100, 255

      if i < 3 :
        default [1] = True
        default [8] = ( (i*A)%B, ((i+1)*A)%B, ((i+2)*A)%B )
      data_values.append ( default ) #14*[''])
    #print data_values
    data_types = [
      gridlib.GRID_VALUE_STRING,
      gridlib.GRID_VALUE_BOOL,
      gridlib.GRID_VALUE_BOOL,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_BOOL,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER,
      MY_GRID_TYPE_COLOR,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER,
      gridlib.GRID_VALUE_NUMBER ]
    data_defs = ( MY_GRID_ROW_FIXED, MY_GRID_COL_TYPED )

    Image_List = Get_Image_List ()
    bmp_Pause = Image_List.GetBitmap ( 49 )
    bmp_Run   = Image_List.GetBitmap ( 50 )
    bmp_Plus  = Image_List.GetBitmap ( 56 )
    bmp_Minus = Image_List.GetBitmap ( 57 )
    bmp_Up    = Image_List.GetBitmap ( 45 )
    bmp_Down  = Image_List.GetBitmap ( 44 )
    bmp_Color = Image_List.GetBitmap ( 48 )

    b_size = ( 22, 22 )
    GUI = """
    self.NB            ,wx.Notebook  ,style = wx.BK_LEFT
      self.Splitter      ,SplitterHor  ,name = 'Scope'  ,style = wx.NO_BORDER
        self.Panel_Left    ,wx.Panel
          B_Pause     ,BmpBut  ,bitmap = bmp_Pause  ,pos = (2,2)   ,size = b_size
          B_Run       ,BmpBut  ,bitmap = bmp_Run    ,pos = (2,27)  ,size = b_size
          B_Plus      ,BmpBut  ,bitmap = bmp_Plus   ,pos = (27,2)  ,size = b_size
          B_Minus     ,BmpBut  ,bitmap = bmp_Minus  ,pos = (27,27) ,size = b_size
          B_Up        ,BmpBut  ,bitmap = bmp_Up     ,pos = (52,2)  ,size = b_size
          B_Down      ,BmpBut  ,bitmap = bmp_Down   ,pos = (52,27) ,size = b_size
          B_Color     ,BmpBut  ,bitmap = bmp_Color  ,pos = (77,2)  ,size = b_size
          self.Sel_Signal  ,wx.StaticText, label = '--', pos = ( 77, 27 )
        self.Panel_Right   ,wx.Panel
          self.Scope       ,tBase_Scope_with_History
      self.Grid          ,Base_Table_Grid  ,data_values, data_types, data_defs, name='Settings'
    """
    self.wxGUI = Create_wxGUI ( GUI )
    print (self.wxGUI.code)

    self.Panel_Left.SetBackgroundColour ( wx.BLACK )

    B_Pause.SetToolTipString ( _(0, 'Pause Recording'                    ) )
    B_Run  .SetToolTipString ( _(0, 'Start Recording'                    ) )
    B_Plus .SetToolTipString ( _(0, 'Increase selected signal Amplitude' ) )
    B_Minus.SetToolTipString ( _(0, 'Decrease selected signal Amplitude' ) )
    B_Up   .SetToolTipString ( _(0, 'Shift selected signal Up'           ) )
    B_Down .SetToolTipString ( _(0, 'Shift selected signal Down'         ) )
    B_Color.SetToolTipString ( _(0, 'Set Color of selected signal'       ) )

    self.Sel_Signal.SetForegroundColour ( wx.WHITE )
    self.Sel_Signal.SetToolTipString ( _( 0, 'Selected Signal') )

    Set_NoteBook_Images ( self.NB, ( 47, 67 ) )

    wx.CallLater ( wxGUI_Delay, self.Splitter.SetSashPosition, 102 )
# ***********************************************************************

# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':

  Test_Defs ( 4 )

  if Test ( 1 ) :
    My_Main_Application ( Simple_Test_Form )

  if Test ( 2 ) :
    My_Main_Application ( Test_Dynamic_Form )

  if Test ( 3 ) :
    My_Main_Application ( Test_Brick_BP_Form )

  if Test ( 4 ) :
    My_Main_Application ( Test_Control_Scope )

# ***********************************************************************
pd_Module () #__file__ )
