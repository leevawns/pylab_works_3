from General_Globals import *
#from language_support import  _
from language_support import  _, Language_Current, Set_Language, Flag_Object

__doc__ = """
"""

_Version_Text = [

[ 1.2 , '13-10-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - In Notebook creation, removed the imageId, gave problems under Ubuntu
 - changed name of GUI_NoteBook to GUI_Notebook
 - my_MiniFrame removed (it's better to maintain just one: My_Frame_Class)
""")],

[ 1.1 , '27-08-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - GUI_NoteBook added
""")],

[ 1.0 , '14-07-2007', 'Stef Mientki',
'Test Conditions:', (),
_(0, ' - orginal release')]
]


# !!! import wx before any support library !!!
# otherwise the IDE won't do auto-suggest
import wx
import wx.lib.flatnotebook as fnb

import  wx.lib.buttons  as  buttons
BmpBut = buttons.GenBitmapButton


from inifile_support import *
# ***********************************************************************
# demo program
# ***********************************************************************
def My_Main_Application ( My_Form, config_file = None ) :
  # we need an extra import here
  import wx

  app = wx.PySimpleApp ()
  if config_file :
    ini = inifile ( config_file )
  else :
    ini = inifile ( Change_FileExt ( sys.argv[0], '_Test.cfg' ) )

  frame = My_Form ( ini )
  frame.Show ( True )

  if Application.WX_Inspect_Mode :
    import wx.lib.inspection
    wx.lib.inspection.InspectionTool().Show()

  app.MainLoop ()
  ini.Close ()
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
    FormStyle = wx.DEFAULT_FRAME_STYLE | wx.TINY_CAPTION_HORIZ

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
    self.SetIcon ( wx.Icon (
      Joined_Paths ( os.path.split ( __file__ )[0],
      '../pictures/vippi_bricks_323.ico'), wx.BITMAP_TYPE_ICO ) )

    self.Bind ( wx.EVT_CLOSE,  self.__On_Close  )

  # *********************************************************
  # *********************************************************
  def __On_Close ( self, event ) :
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

    event.Skip ()
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
  'wx.CheckBox'       : ( 'GetValue()',        '%%.SetValue(%)'       ),
  'wx.Notebook'       : ( 'GetSelection()',    '%%.SetSelection(%)'   ),
  'wx.RadioBox'       : ( 'GetSelection()',    '%%.SetSelection(%)'   ),
  'wx.SplitterWindow' : ( 'GetSashPosition()', 'wx.CallLater ( wxGUI_Delay, %%.SetSashPosition, % )' ),
  'wx.TextCtrl'       : ( 'GetValue()',        '%%.SetValue(str(%))'  ),
  'wx.ToggleButton'   : ( 'GetValue()',        '%%.SetValue(%)'       ),
}
# ***********************************************************************


# ***********************************************************************
# You can specify any additional paramater,
# just in the order they would normally appear
# just DONT specify "self, parent", these are done automatically
#
# Example (see also at the bottom of this module)
#    GUI = """
#    self.NB       ,wx.Notebook   ,style = wx.NO_BORDER
#      self.Grid   ,Base_Table_Grid , data_values, data_types, data_defs
#      Panel2      ,PanelVer, 11  ,name  = "Page2"
#        list1     ,wx.ListCtrl   ,style = wx.LC_REPORT
#    """
#    exec ( Create_wxGUI ( GUI ) )
# ***********************************************************************
def Create_wxGUI ( GUI, my_parent = 'self', Print = None,
                   code ='', Sizer = False, Ini = None ) :

  # ********************************************************
  # ********************************************************
  def Pop_For_Parent ( indent, stack, code ) :

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
          print '******* ERROR splitter " ' + last[1] + '"does not have 2 controls'
          return False

        # Add minimum panesize
        code += last[1] + '.SetMinimumPaneSize(20)\n'

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
                  str(weights[i]) + ', wx.EXPAND )\n'

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

  # ********************************************************
  # ********************************************************
  # prepare Save / Restore settings parameters
  if Ini :
    IniFile_Read = Ini + '.Read ( '
    IniFile_Write = Ini + '.Write ( '
    Restore_Settings = ''
    Save_Settings    = ''

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
    if Ini and \
      _Save_Restore.has_key ( typ ) and \
       ( name.find ( 'self.' ) == 0 ) :
      SR = _Save_Restore [ typ ]

      line = 'Value = ' + IniFile_Read + '"' + name [ 5: ] + '", None )'
      Restore_Settings += line + '\n'
      line = 'if Value != None :'
      Restore_Settings += line + '\n'
      Name = name
      line = ('  ' + SR[1] ).replace ( '%%', Name ).replace ( '%', 'Value' )
      Restore_Settings += line + '\n'

      line = 'Value = ' + name + '.' + SR[0]
      Save_Settings += line + '\n'
      line = IniFile_Write + '"' + name [ 5: ] + '" , Value )'
      Save_Settings += line + '\n'
    # ****************************************************************


    # Get parent, by searching a parent (= lesser indent)
    code = Pop_For_Parent ( indent, stack, code )
    if code == False : return False
    parent = stack [-1]

    # If parent is one of the special ones,
    # Add all children to it's list
    if parent[2] in [ 'SplitterHor', 'SplitterVer', 'wx.SplitterWindow',
                      'PanelHor', 'PanelVer',
                      'wx.Notebook', 'GUI_Notebook' ] :
      stack [-1][3].append ( name )

    # Add the current component to the stack
    stack.append ( [ indent, name, defi[1], [], weights ])

    # Create the component
    #print name,'$',typ,'$',parent[1], '$',params
    #print name,typ,parent,params
    code += name + '=' + typ + '( ' + parent[1] + params + ')\n'

  # While there are still elements on the stack,
  # Remove them and perform the actions (Splitter / Sizers / ...)
  indent = 0
  code = Pop_For_Parent ( indent, stack, code )
  if code == False : return False

  # Size the main component on the parent
  # What if more than 1 component on the lowest level ??
  code += 'Sizer = wx.BoxSizer ( ) \n'
  code += 'Sizer.Add ( ' + first_element + ', 1, wx.EXPAND ) \n'
  code += my_parent + '.SetSizer ( Sizer ) \n'

  """
  """
  
  if Print :
    print '******* GUI-code *******'
    print code
    print
    if Ini :
      print '******* GUI-code-SETTINGS *******'
      print 'Restore', Restore_Settings
      print 'Save',Save_Settings
      print

  if Ini :
    return code, Restore_Settings, Save_Settings
  else :
    return code

# ***********************************************************************

from   picture_support import *

# ***********************************************************************
# ***********************************************************************
class Simple_Test_Form ( wx.MiniFrame ):
  def __init__ ( self, ini = None ) :
    wx.MiniFrame.__init__( self, None, style = wx.DEFAULT_FRAME_STYLE  )

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
          Label_Top        ,wx.StaticText
        self.Scope_Normal  ,PlotCanvas         ,self
        self.Panel_Bottom  ,PanelHor
          Label_Bottom     ,wx.StaticText
      self.Scope_History   ,PlotCanvas_History ,self
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
      self.Grid   ,Base_Table_Grid , data_values, data_types, data_defs
      Panel2      ,PanelVer, 11  ,name  = "Page2"
        list1     ,wx.ListCtrl   ,style = wx.LC_REPORT
    """

    ##Create_Menus ( self )
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

    from   picture_support import Get_Image_16
    NB.SetImageList ( image_list )
    Set_NoteBook_Images ( self.NB, ( 201, 207) )
    """

    GUI = """
    self.NB       ,wx.Notebook   ,style = wx.NO_BORDER
      self.Grid   ,Base_Table_Grid , data_values, data_types, data_defs
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
    bmp_PW    = Get_Image_Resize ( '../PyLab_workss/vippi_bricks_64.png',                      64 )
    bmp_IDE   = Get_Image_Resize ( '../pictures/applications-accessories.png', 48 )
    bmp_Lib   = Get_Image_Resize ( '../pictures/bieb.png',                     48 )
    bmp_Trans = Get_Image_Resize ( '../pictures/romanime0.ico',                48 )

    self.Flags = Flag_Object ()
    bmp_Flag = self.Flags.Get_Flag ( Language_Current[0] )
    if not bmp_Flag.Ok():
      bmp_Flag = wx.EmptyBitmap(32,22)
      self.clearBmp ( bmp_Flag )

    import wx.html as  html
    import  my_iewin   as iewin

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
    #exec ( Create_wxGUI ( GUI ) )
    #from picture_support import Get_Image_List
    #self.NB.AssignImageList ( Get_Image_List () )
    # ***********************************************************************


    # ***********************************************************************
    from tree_support import Custom_TreeCtrl_Base
    GUI = """
    self.SplitV            ,SplitterVer, style = wx.SP_LIVE_UPDATE | wx.SP_3DSASH
      p1               ,wx.Panel, style = wx.NO_BORDER
      p2               ,wx.Panel, style = wx.NO_BORDER
    """
    #print Create_wxGUI(GUI)
    #exec ( Create_wxGUI ( GUI ) )
    ## MAG WEG ??wx.CallLater ( 100, self.SplitV.SetSashPosition, -10 )
    # ***********************************************************************

    # ***********************************************************************
    GUI = """
      self.SplitV         ,SplitterVer
        self.Edit         ,Base_STC
        self.Edit2         ,Base_STC
    """
    print Create_wxGUI ( GUI )
    from Scintilla_support import Base_STC
    exec ( Create_wxGUI ( GUI ) )
    # ***********************************************************************


    # ***********************************************************************
    GUI = """
    self.NB       ,wx.Notebook   ,style = wx.NO_BORDER
      p4           ,wx.Panel       ,name = 'Demos'
      Panel2      ,PanelVer, 11  ,name  = "Page2"
        list1     ,wx.ListCtrl   ,style = wx.LC_REPORT
    """
    #exec ( Create_wxGUI ( GUI ) )
    # ***********************************************************************


  def OnRightDown ( self, event ) :
    print 'MOUSE RIGHT'
    #event.Skip()

  def OnShowPopup ( self, event ) :
    print 'POPUP'
    #event.Skip()
# ***********************************************************************


# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  My_Main_Application ( Simple_Test_Form )
# ***********************************************************************
pd_Module ( __file__ )
