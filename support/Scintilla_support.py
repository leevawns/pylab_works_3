import __init__
from language_support import  _


# ***********************************************************************

__doc__ = _(0, """
doc_string translated ?
""" )

_Version_Text = [

[ 1.1 , '11-11-2008', 'Stef Mientki',
'Test Conditions:', ( 2, ),
_(0, """
 - Base_STC, now uses the name defined in the init (e.g. for Notebook pages)
""")],

[ 1.0 , '02-11-2008', 'Stef Mientki',
'Test Conditions:', ( 2, ),
_(0, """
 - Background color changes automatically when ReadOnly mode changes
""")],

[ 0.1 , '24-10-2007', 'Stef Mientki',
'Test Conditions:', ( 2, ),
_(0, ' - orginal release')]
]

# ***********************************************************************

_ToDo = """
- preview a control: find the correct class (class within file + name starting with ?)
"""

# ***********************************************************************


# ***********************************************************************
from   General_Globals import *
from   gui_support     import *
from   dialog_support  import *
import help_support
import PyLab_Works_Globals as PG
# ***********************************************************************


# ***********************************************************************
# This file is derived from the wxPython demo.
# A major change was made to let the autocompletion work well.
# ***********************************************************************
import wx
import wx.stc  as  stc
import keyword
from   file_support    import *
from   inifile_support import *



BPS_ADDED   =  0   # just added by the Editor   ==> BPS_ACTIVE
BPS_DELETED = -1   # just deleted by the Editor ==> BPS_IGNORE
BPS_CHANGED = -5
BPS_ACTIVE  = -2   # Activated by the Debugger
BPS_IGNORE  = -3   # Deleted by the Debugger
BPS_CURRENT = -4



faces = { 'times': 'Times New Roman',
              'mono' : 'Courier New',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 10,
              'size2': 8,
             }
faces = { 'times': 'Courier New',
              'mono' : 'Courier New',
              'helv' : 'Courier New',
              'other': 'Courier New',
              'size' : 10,
              'size2': 8,
             }


# ***********************************************************************
# ***********************************************************************
#     Debug_Line : Condition, Enabled, Scite_Line, Scite_ID, Debug_ID
class BP_Class ( object ) :
  def __init__ ( self, Debug_Line, Condition = '', Enabled = True, Scite_ID = -1  ) :
    self.Scite_Line = Debug_Line
    self.Condition  = Condition
    self.Enabled    = Enabled
    self.Scite_ID   = Scite_ID
    self.Debug_ID   = -1            # [ 1.. ]
    self.BP_Status  = BPS_ADDED
    self.Current_Markers = None
  
  def __repr__ ( self ) :
    return \
      '  C='    + str ( self.Condition  ) + \
      '  En='    + str ( self.Enabled    ) + \
      '  SL='    + str ( self.Scite_Line ) + \
      '  SID='   + str ( self.Scite_ID   ) + \
      '  DID='   + str ( self.Debug_ID   ) + \
      '  State=' + str ( self.BP_Status  ) + \
      '  CM='    + str ( self.Current_Markers )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Print_BP_List ( BPL ) :
  print ('****** BreakPoints')
  for File in BPL :
    print ('  **** File = ' + File)
    for Line in BPL [ File ] :
      print ('    ** ', Line, ':', BPL [ File ] [ Line ])
# ***********************************************************************



# August 2008, this new base STC should replace
# all previous defined Scintilla editors
# ***********************************************************************
class Base_STC ( stc.StyledTextCtrl ):

  Available_Lexers = ( stc.STC_LEX_NULL,
                       stc.STC_LEX_PYTHON,
                       stc.STC_LEX_SQL )

  def __init__(self, parent, ID = wx.ID_ANY,
               pos   = wx.DefaultPosition,
               size  = wx.DefaultSize,
               style = wx.NO_BORDER,
               name  = 'STC Edit' ) :

    self.Panel_Name        = name
    self.Ouder             = parent
    self.TopFrame          = wx.GetTopLevelParent ( parent )
    self.Code_To_Execute   = ''
    self.Execute_History   = []
    self.Execute_History_p = -1
    self.Code_Globals      = {}
    self.Code_Locals       = {}
    self.Main_BPL          = {}
    self.MainFile          = False
    self.Filename          = None
    self.Current_Line      = None
    self.Prev_SearchText   = ''
    self.Help_Viewer       = None
    self.Local_Browser     = None
    self.MetaData_Modified = False
    
    stc.StyledTextCtrl.__init__(self, parent, ID, pos, size, style)

    self.CmdKeyAssign(ord('B'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
    self.CmdKeyAssign(ord('N'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

    self.Current_Lexer = 1
    self.SetLexer ( self.Available_Lexers [ self.Current_Lexer ] )
    self.SetKeyWords ( 0, " ".join(keyword.kwlist))

    #self.SetLexer ( stc.STC_LEX_SQL )
    #self.SetKeyWords ( 1, "aap beer")

    
    self.SetTabWidth ( 2 )
    self.SetUseTabs  ( False )
    self.SetIndent   ( 2 )
    self.SetIndentationGuides ( True )
    #self.SetTabIndents ( True )
    #self.SetBackSpaceUnIndents ( True )

    self.SetProperty("fold", "1")
    self.SetProperty("tab.timmy.whinge.level", "1")
    self.SetMargins(0,0)

    self.SetViewWhiteSpace(False)
    #self.SetBufferedDraw(False)
    #self.SetViewEOL(True)
    #self.SetEOLMode(stc.STC_EOL_CRLF)
    #self.SetUseAntiAliasing(True)

    #self.SetEdgeMode(stc.STC_EDGE_BACKGROUND)
    self.SetEdgeMode ( stc.STC_EDGE_LINE )
    self.SetEdgeColumn(78)

    # only allow Modify-events on text changes
    self.SetModEventMask ( stc.STC_MOD_INSERTTEXT | stc.STC_MOD_DELETETEXT)

    # *************************************************************
    # We define 4 margins here (5 are possible), initial meant for
    #   - line number
    #   - bookmark
    #   - breakpoint information  (default off)
    #   - folding
    # *************************************************************
    self.BookMark_Mask = 0x000003FF
    self.Break_Mask    = 0x000FFC00            #~stc.STC_MASK_FOLDERS ^ BookMark_Mask
    self.Rest_Mask     = 0x01F00000
    self.SetMarginWidth     ( 0, 40 )  # Linenumber
    self.SetMarginSensitive ( 0, True )

    self.SetMarginWidth     ( 1, 12 )  # Bookmarks
    self.SetMarginType      ( 1, stc.STC_MARGIN_SYMBOL )
    self.SetMarginMask      ( 1, self.BookMark_Mask )
    self.SetMarginSensitive ( 1, True )

    self.SetMarginWidth     ( 2, 0 )  # BreakPoints
    self.SetMarginType      ( 2, stc.STC_MARGIN_SYMBOL )
    self.SetMarginMask      ( 2, self.Break_Mask )
    self.SetMarginSensitive ( 2, True )

    self.SetMarginWidth     ( 3, 12 )  # Folding
    self.SetMarginType      ( 3, stc.STC_MARGIN_SYMBOL )
    self.SetMarginMask      ( 3, stc.STC_MASK_FOLDERS  )
    self.SetMarginSensitive ( 3, True )
    # *************************************************************

    # *************************************************************
    # *************************************************************
    MD = self.MarkerDefine

    # BookMarks 1.. 9, 0
    self.BookMarks = 10 * [ None ]
    FG = "#FFFFFF"
    BG = "#00CA00"
    MD ( 0, stc.STC_MARK_CHARACTER + ord('1'), FG, BG )
    MD ( 1, stc.STC_MARK_CHARACTER + ord('2'), FG, BG )
    MD ( 2, stc.STC_MARK_CHARACTER + ord('3'), FG, BG )
    MD ( 3, stc.STC_MARK_CHARACTER + ord('4'), FG, BG )
    MD ( 4, stc.STC_MARK_CHARACTER + ord('5'), FG, BG )
    MD ( 5, stc.STC_MARK_CHARACTER + ord('6'), FG, BG )
    MD ( 6, stc.STC_MARK_CHARACTER + ord('7'), FG, BG )
    MD ( 7, stc.STC_MARK_CHARACTER + ord('8'), FG, BG )
    MD ( 8, stc.STC_MARK_CHARACTER + ord('9'), FG, BG )
    MD ( 9, stc.STC_MARK_CHARACTER + ord('0'), FG, BG )

    # BreakPoints
    STCM_CURRENT     = 10
    STCM_BP          = 11
    STCM_BP_DIS      = 12
    STCM_BP_COND     = 13
    STCM_BP_DIS_COND = 14

    FG = "#FFFFFF"
    BG = "#FF0000"
    MD ( STCM_CURRENT,     stc.STC_MARK_SHORTARROW,  BG, BG )
    MD ( STCM_BP,          stc.STC_MARK_CIRCLEMINUS, "#39F1A1", BG )
    MD ( STCM_BP_DIS,      stc.STC_MARK_CIRCLEMINUS, FG, "#FFDDDD" )
    MD ( STCM_BP_COND,     stc.STC_MARK_CIRCLEPLUS,  "#9CBEFC", BG )
    MD ( STCM_BP_DIS_COND, stc.STC_MARK_CIRCLEPLUS,  FG, "#FFDDDD" )

    # Background color for BreakPoints
    MD ( STCM_CURRENT + 5,     stc.STC_MARK_BACKGROUND, "#000000", "#FF0000" )
    MD ( STCM_BP + 5,          stc.STC_MARK_BACKGROUND, "#000000", "#39F1A1" )
    MD ( STCM_BP_DIS + 5,      stc.STC_MARK_BACKGROUND, "#000000", "#FFDDDD" )
    MD ( STCM_BP_COND + 5,     stc.STC_MARK_BACKGROUND, "#000000", "#9CBEFC" )
    MD ( STCM_BP_DIS_COND + 5, stc.STC_MARK_BACKGROUND, "#000000", "#FFDDDD" )

    """
    stc.STC_MARK_ARROW
    STC_MARKER_MAX = _stc.STC_MARKER_MAX
    STC_MARK_CIRCLE = _stc.STC_MARK_CIRCLE
    STC_MARK_ROUNDRECT = _stc.STC_MARK_ROUNDRECT
    STC_MARK_ARROW = _stc.STC_MARK_ARROW
    STC_MARK_SMALLRECT = _stc.STC_MARK_SMALLRECT
    STC_MARK_SHORTARROW = _stc.STC_MARK_SHORTARROW
    STC_MARK_EMPTY = _stc.STC_MARK_EMPTY
    STC_MARK_ARROWDOWN = _stc.STC_MARK_ARROWDOWN
    STC_MARK_MINUS = _stc.STC_MARK_MINUS
    STC_MARK_PLUS = _stc.STC_MARK_PLUS
    STC_MARK_VLINE = _stc.STC_MARK_VLINE
    STC_MARK_LCORNER = _stc.STC_MARK_LCORNER
    STC_MARK_TCORNER = _stc.STC_MARK_TCORNER
    STC_MARK_BOXPLUS = _stc.STC_MARK_BOXPLUS
    STC_MARK_BOXPLUSCONNECTED = _stc.STC_MARK_BOXPLUSCONNECTED
    STC_MARK_BOXMINUS = _stc.STC_MARK_BOXMINUS
    STC_MARK_BOXMINUSCONNECTED = _stc.STC_MARK_BOXMINUSCONNECTED
    STC_MARK_LCORNERCURVE = _stc.STC_MARK_LCORNERCURVE
    STC_MARK_TCORNERCURVE = _stc.STC_MARK_TCORNERCURVE
    STC_MARK_CIRCLEPLUS = _stc.STC_MARK_CIRCLEPLUS
    STC_MARK_CIRCLEPLUSCONNECTED = _stc.STC_MARK_CIRCLEPLUSCONNECTED
    STC_MARK_CIRCLEMINUS = _stc.STC_MARK_CIRCLEMINUS
    STC_MARK_CIRCLEMINUSCONNECTED = _stc.STC_MARK_CIRCLEMINUSCONNECTED
    STC_MARK_BACKGROUND = _stc.STC_MARK_BACKGROUND
    STC_MARK_DOTDOTDOT = _stc.STC_MARK_DOTDOTDOT
    STC_MARK_ARROWS = _stc.STC_MARK_ARROWS
    STC_MARK_PIXMAP = _stc.STC_MARK_PIXMAP
    STC_MARK_FULLRECT = _stc.STC_MARK_FULLRECT
    STC_MARK_CHARACTER = _stc.STC_MARK_CHARACTER
    STC_MARKNUM_FOLDEREND = _stc.STC_MARKNUM_FOLDEREND
    STC_MARKNUM_FOLDEROPENMID = _stc.STC_MARKNUM_FOLDEROPENMID
    STC_MARKNUM_FOLDERMIDTAIL = _stc.STC_MARKNUM_FOLDERMIDTAIL
    STC_MARKNUM_FOLDERTAIL = _stc.STC_MARKNUM_FOLDERTAIL
    STC_MARKNUM_FOLDERSUB = _stc.STC_MARKNUM_FOLDERSUB
    STC_MARKNUM_FOLDER = _stc.STC_MARKNUM_FOLDER
    STC_MARKNUM_FOLDEROPEN = _stc.STC_MARKNUM_FOLDEROPEN
    """
    # *************************************************************

    # *************************************************************
    # Define folding markers
    # Like a flattened tree control using
    # circular headers and curved joins
    # *************************************************************
    MD ( stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_CIRCLEMINUS,          "white", "#404040" )
    MD ( stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_CIRCLEPLUS,           "white", "#404040" )
    MD ( stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,                "white", "#404040" )
    MD ( stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNERCURVE,         "white", "#404040" )
    MD ( stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_CIRCLEPLUSCONNECTED,  "white", "#404040" )
    MD ( stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "#404040" )
    MD ( stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNERCURVE,         "white", "#404040" )
    # *************************************************************


    # Make some styles,  The lexer defines what each style is used for, we
    # just have to define what each style looks like.  This set is adapted from
    # Scintilla sample property files.

    # Global default styles for all languages
    self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
    self.StyleClearAll()  # Reset all to be like the default


    # *************************************************************
    # Define the indicator attributes
    #    .StartStyling ( Start, 0xFF )
    #    .SetStyling   ( Lengte,  StyleNr | Indicator )
    # Indicator bits, are the 3 most significant bits: 0xE0
    # only accepts old style indicators,
    # Python Lexer only allows Indicator-2
    # *************************************************************
    self.IndicatorSetStyle      ( 0, stc.STC_INDIC_PLAIN )
    self.IndicatorSetForeground ( 0, "GREEN")

    self.IndicatorSetStyle      ( 1, stc.STC_INDIC_ROUNDBOX )
    self.IndicatorSetForeground ( 1, "BLUE")

    self.IndicatorSetStyle      ( 2, stc.STC_INDIC_SQUIGGLE )
    self.IndicatorSetForeground ( 2, "RED")
    #self.IndicatorSetStyle      ( 0, stc.STC_INDIC_DIAGONAL )
    #self.IndicatorSetStyle      ( 0, stc.STC_INDIC_TT )
    # *************************************************************


    # Global default styles for all languages
    self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
    self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,  "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
    self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
    # NOTE: no spaces before "bold" allowed !!
    self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,  "fore:#0000FF,back:#C0FFFF,bold")
    self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,    "fore:#FF0000,back:#FFC0C0,bold")
    # unknown: self.StyleSetSpec(stc.STC_STYLE_BRACEMATCH,    "fore:#000000,back:#FF0000,bold")
    self.StyleSetSpec(stc.STC_STYLE_INDENTGUIDE, "fore:#BBBBBB,back:#FFFFFF")

    #self.GetLineState()
    #self.GetMaxLineState()
    #self.IndicatorSetStyle()
    #self.GetStyleAt()


    # Python styles
    # Default
    #print 'beer',stc.STC_P_DEFAULT,stc.STC_P_TRIPLEDOUBLE
    #"fore:#000000,face:%(helv)s,size:%(size)d" % faces
    
    #aap = [ stc.STC_P_COMMENTLINE, stc.STC_P_STRING]
    #print aap
    self.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
    # Comments
    self.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
    # Number
    self.StyleSetSpec(stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % faces)
    # String
    self.StyleSetSpec(stc.STC_P_STRING, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
    # Single quoted string
    self.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#7F007F,face:%(helv)s,size:%(size)d" % faces)
    # Keyword
    self.StyleSetSpec(stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % faces)
    # Triple quotes
    self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % faces)
    # Triple double quotes
    self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#7F8000,size:%(size)d" % faces)
    # Class name definition
    self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % faces)
    # Function or method name definition
    self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces)
    # Operators
    self.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)
    # Identifiers
    self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
    # Comment-blocks ##
    self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%(size)d" % faces)
    # End of line where string is not closed
    self.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)

    self.SetCaretForeground("BLUE")

    #register some images for use in the AutoComplete box.
    #self.RegisterImage(1, _images.getSmilesBitmap())
    #self.RegisterImage(2,
    #    wx.ArtProvider.GetBitmap(wx.ART_NEW, size=(16,16)))
    #self.RegisterImage(3,
    #    wx.ArtProvider.GetBitmap(wx.ART_COPY, size=(16,16)))

    # settings for autocompletion
    #self.ClearRegisteredImages()
    self.AutoCompSetFillUps    ( '\n(.'  )
    # DOESN'T WORK: self.AutoCompStops         ( '\t' )
    self.AutoCompSetIgnoreCase ( False )
    self.AutoCompSetAutoHide   ( True  )

    # *******************************************************
    self.Bind ( stc.EVT_STC_MARGINCLICK,        self.OnMarginClick )
    self.Bind ( wx.EVT_KEY_DOWN,                self.On_Key_Down   )
    self.Bind ( stc.EVT_STC_CHARADDED,          self.OnCharAdd     )
    #self.Bind ( stc.EVT_STC_AUTOCOMP_SELECTION, self.OnAutoComplete )
    self.Bind ( stc.EVT_STC_UPDATEUI,    self.OnUpdateUI    )

    # Fetch the text from the Templates module
    #print 'SSSTT',sys.path
    from Scintilla_Templates import EVT_SCINTILLA_TEMPLATE_INSERT
    self.Bind ( EVT_SCINTILLA_TEMPLATE_INSERT, self.On_Text_From_Templates )


    self.CallTipSetBackground ( (225,225,255)) #"Yellow" ) #( 0x60, 0x60, 0x80) ) #"BLUE" )
    self.CallTipSetForegroundHighlight ( "Red")

    # These are nomallly set during KEYDOWN,
    #   AutoCompletion_Key holds the key
    #   if AutoCompletion_Later == False
    #     Autocompletion list is generated in the ADDCHAR
    #   otherwise it's generated in the GUI_update
    self.AutoCompletion_Key   = None
    self.AutoCompletion_Later = False
    self.Verify_Later         = True
    self.Verify_LineNo        = -1

    self.Error_Line = None
    self.Error_Pos  = 0

    self.Function_Key_Count = True
    self.Execute_Code_Count = True

    #stc.EVT_STC_KEY

    #sys.path.append ( 'P:/Python/Lib/site-packages/wx-2.8-msw-unicode/wx/tools/Editra/src/autocomp' )
    #import pycomp
    #self.Auto_Completer = pycomp.Completer ( self )

    # Doesn't work well, we'll do it manual
    #self.AutoCompSetCancelAtStart ( False )
    #print 'YYYYY',self.AutoCompGetCancelAtStart()
 


    # *******************************************************
    # Try to bind to standard menu items
    # *******************************************************
    try :
      MB = self.TopFrame.MenuBar.Bind_MenuItem
      MB ( 'File', 'New/Open'      ,self.OnMenu_Open     )
      MB ( 'File', 'Print'         ,self._On_Menu_Print         )
      MB ( 'File', 'Print Preview' ,self._On_Menu_Print_Preview )
      MB ( 'File', 'Page Setup'    ,self._On_Menu_Page_Setup    )
    except :
      pass
    # *******************************************************

    # *******************************************************
    # Some default printer settings
    # *******************************************************
    self._printData = wx.PrintData()
    self._print_margins_TopLeft     = (10,10) #ini.Read ( 'TopLeft', ( 10, 10 ) )
    self._print_margins_BottomRight = (10,10) #ini.Read ( 'BottomRight', ( 10, 10 ) )
    self._print_zoom = 100 #ini.Read ( 'Zoom', 100 )

    # default -1, is "best", but terribly slow
    self._printData.SetQuality (2)
    # *******************************************************



  # **************************************************
  def Set_Wrap ( self, On = True ) :
    """Turns Word-wrap on or off."""
    if On :
      self.SetWrapMode ( stc.STC_WRAP_WORD )
      self.SetWrapVisualFlags ( stc.STC_WRAPVISUALFLAG_START | \
                                stc.STC_WRAPVISUALFLAG_END )
      #self.SetWrapStartIndent (4)
    else :
      self.SetWrapMode ( stc.STC_WRAP_NONE )


  # **************************************************
  def OnMenu_Open ( self, event = None ):
    DefaultLocation = ''
    if self.Filename :
      DefaultLocation = path_split ( self.Filename )[0]

    FileName = AskFileForOpen ( DefaultLocation, FileTypes = '*.py' )
    if FileName :
      self.SaveFile ( self.Filename )
      self.LoadFile ( FileName )
    if event :
      event.Skip ()

  # *******************************************************
  def Change_File ( self, FileName ) :
    #print 'ChangeFileamxx',FileName
    self.SaveFile ( self.Filename )
    self.LoadFile ( FileName )
    self.Execute_Code ( None, True )

  # *******************************************************
  def GetName ( self ) :
    return self.Panel_Name
  
  # *******************************************************
  def SetReadOnly ( self, ReadOnly = True ) :
    """Take over, so we can change the background color"""
    stc.StyledTextCtrl.SetReadOnly ( self, ReadOnly )
    if ReadOnly :
      color = "back:#F0F0F0"
    else :
      color = "back:#FFFFFF"
    self.StyleSetSpec ( stc.STC_STYLE_DEFAULT, color )
    for style in range ( 32 ) :
      self.StyleSetSpec ( style, color )

    
  # *******************************************************
  # *******************************************************
  def Set_Error_Line ( self, line = -1, pos = 0 ) :
    # remove the previous error line
    if self.Error_Line == None: self.Error_Line = 0
    if self.Error_Line >= 0:
      buf_pos = self.PositionFromLine ( self.Error_Line )
      self.StartStyling ( buf_pos, stc.STC_INDICS_MASK)
      self.SetStyling   ( self.Error_Pos, 0 )

    self.Error_Line = line
    self.Error_Pos  = pos
    
    # if new error line, display it
    if self.Error_Line >= 0 :
      buf_pos = self.PositionFromLine ( self.Error_Line )
      self.StartStyling ( buf_pos, stc.STC_INDICS_MASK)
      self.SetStyling   ( self.Error_Pos, stc.STC_INDIC2_MASK)

  # *******************************************************
  # We take over file saving, so we can save bookmarks and caret
  # *******************************************************
  def SaveFile ( self, filename, BreakPoints = None, MainFile = False ) :
    if ( 'Load_Save' in Debug_What ) :
      Debug_Dump_Trace (
        'Base_STC, SaveFile :',
        '\nfilename    =', filename,
        '\nBreakPoints =', BreakPoints,
        '\nMainFile    =', MainFile )

    if not ( filename ) :
      return
    self.Filename =  Get_PDB_Windows_Filename ( filename )
    
    if self.GetModify () :
      stc.StyledTextCtrl.SaveFile ( self, filename )
      self.MetaData_Modified = True

    project_file = Change_FileExt ( filename, 'pwp' )
    ini = inifile ( project_file )
    ini.Section = 'Scintilla Editor'

    #lineno = self.GetCurrentLine ()
    lineno = self.GetFirstVisibleLine() #+ 1
    ini.Write ( 'LineNo', lineno )

    if self.MetaData_Modified :
      BookMarks = {}
      for lineno in range ( self.GetLineCount () ) :
        BM = ( self.MarkerGet ( lineno ) ) & self.BookMark_Mask
        if BM > 0 :
          BookMarks [ BM ] = lineno
      ini.Write ( 'BM',  BookMarks )

      if BreakPoints :
        #self.Hide_BreakPoint_Markers ()

        # ReCalculate Breakpoints
        # By editing the file, they might have been moved
        for File in BreakPoints.keys() :
          if File == self.Filename :
            BPL = BreakPoints [ File ]
            for Debug_Line in BPL.keys() :
              BP = BPL [ Debug_Line ]
              if BP.BP_Status in ( BPS_DELETED, BPS_IGNORE ) :
                del BreakPoints [ File ] [ Debug_Line ]
              else :
                Scite_Line = self.MarkerLineFromHandle ( BP.Scite_ID )
                #print 'SCITELINE',Scite_Line,BP.Scite_ID
                if Scite_Line < 0 :
                  Scite_Line = Debug_Line
                if Scite_Line != Debug_Line :
                  BreakPoints [ File ] [ Scite_Line ] = \
                    BP_Class ( Debug_Line, BP.Condition, BP.Enabled )
                  del BreakPoints [ File ] [ Debug_Line ]

        if MainFile :
          # recalculate a new dictionairy with brute force
          #print BreakPoints
          New_BP = {}
          for File in BreakPoints :
            New_BP [ File ] = {}
            BPL = BreakPoints [ File ]
            for Debug_Line in BPL :
              BP = BPL [ Debug_Line ]
              New_BP [ File ] [ Debug_Line ] = [ BP.Condition, BP.Enabled ]
          #print 'SAVED BP', New_BP
          ini.Write ( 'BP', New_BP )

    ini.Close ()


  # *******************************************************
  # We take over file loading,
  # so we can restore bookmarks, caret and breakpoints
  # *******************************************************
  def LoadFile ( self, filename, BreakPoints = {} ) :
    if ( 'Load_Save' in Debug_What ) :
      Debug_Dump_Trace (
        'Base_STC, LoadFile :',
        '\nfilename    =', filename,
        '\nBreakPoints =', BreakPoints )

    self.Filename = filename
    #print 'SCITE:',self.Filename

    # Set caption of mainform, special: only if a py_file
    self.TopFrame.SetTitle ( self.Filename )
    if os.path.splitext ( self.Filename )[1].lower() == '.py' :
      if hasattr ( self.TopFrame, 'Set_Caption' ) :
        self.TopFrame.Set_Caption ( path_split ( self.Filename ) [1] )

    self.MainFile = not ( BreakPoints )
    # in case of the mainfile, we have to set MetaData changed True
    # to garantee that breakpoint changes in other files are stored
    self.MetaData_Modified = self.MainFile
    # if the editor is readonly, it won't load a file
    RO = self.GetReadOnly ()
    self.SetReadOnly ( False )
    if File_Exists ( filename ) :
      #print 'SCITE:',self.Filename
      stc.StyledTextCtrl.LoadFile ( self, filename )
    else :
      print ('NO-SCITE:',self.Filename)
      self.ClearAll ()
      
    self.SetReadOnly ( RO )

    project_file = Change_FileExt ( filename, 'pwp' )
    if File_Exists ( project_file ) :
      ini = inifile ( project_file )
      ini.Section = 'Scintilla Editor'
      linenr = ini.Read ( 'LineNo', 0 )

      BookMarks   = ini.Read_Dict ( 'BM' )

      if self.MainFile :
        BreakPoints = ini.Read_Dict ( 'BP' )
        New_BP = {}
        for File in BreakPoints :
          New_BP [ File ] = {}
          BPL = BreakPoints [ File ]
          for Debug_Line in BPL :
            Condition, Enabled = BPL [ Debug_Line ]
            BP = BPL [ Debug_Line ]
            New_BP [ File ] [Debug_Line ] = \
              BP_Class ( Debug_Line, Condition, Enabled )
        self.Main_BPL = BreakPoints = New_BP
        #Print_BP_List ( self.Main_BPL )

      ini.Close ()
      self.EnsureVisibleEnforcePolicy ( linenr )
      self.GotoLine (linenr)

      for BM in BookMarks :
        self.MarkerAddSet ( int ( BookMarks [BM] ), BM )

    # Set pointer to Breakpoint list
    self.Main_BPL = BreakPoints
    # Display BreakPoints
    self.Show_BreakPoint_Markers ()

    # and for the main source file, return the BreakPoint List
    #Print_BP_List ( self.Main_BPL )
    return self.Main_BPL

    
  # *********************************************************
  # Called when debug starts again
  # *********************************************************
  def Leave_Editor_On_BP ( self ) :
    # Delete ALL current line markers
    # restore the markers of the old current line
    if self.Current_Line :
      self.MarkerDeleteAll ( 10 )
      self.MarkerDeleteAll ( 15 )
      #self.Edit.MarkerAddSet ( self.Current_Line[1], self.Current_Line [2] )
      CL = self.Current_Line
      BP = self.Main_BPL [ CL[0] ] [ CL[1] ]
      #print 'ACTIE',CL,BP
      #ACTIE C=  En=True  SL=7  SID=15  DID=3  State=-2  CM=67584
      #ACTIE C=  En=True  SL=8  SID=20  DID=-1  State=-4  CM=None

      if BP.Current_Markers :
        self.MarkerAddSet ( BP.Scite_Line, BP.Current_Markers & ~self.Break_Mask )
        #self.Edit.MarkerAddSet ( lineno, self.Current_Line [2] & ~self.Edit.Break_Mask )
        if ( BP.Current_Markers & self.Break_Mask ) > 0 :
          self.MarkerAddSet ( BP.Scite_Line, BP.Current_Markers & 0x7800 )

          # first remove all bp markers at this line
          i = 0x0F & ( ( BP.Current_Markers & self.Break_Mask ) >> 11 )
          n = 1
          while i > 0 :
            if i & 1 :
              break
            n += 1
            i = i >> 1

          #New_Scite_ID = self.Edit.MarkerAdd ( lineno, 15 )
          BP.Scite_ID = self.MarkerAdd ( BP.Scite_Line, 10 + n )
          self.MarkerAdd ( BP.Scite_Line, 15 + n )
          BP.BP_Status = BPS_ACTIVE

        else :
          self.MarkerAdd ( lineno, 10 )
          BP.BP_Status = BPS_IGNORE

      else :  # no real BP markers on this line, so remove the BP
        del self.Main_BPL [ CL[0] ] [ CL[1] ]

        
      self.Current_Line = None

    # Disable all editors
    self.SetReadOnly ( True )

  # *********************************************************
  # Called by Debugger, when a BP is reached
  # *********************************************************
  def Goto_Editor_On_BP ( self, filename, lineno = -1 ) :
    # Store filename in a uniform case
    filename = Get_PDB_Windows_Filename ( filename )

    # Set Marker on Current Line
    self.Current_Line = [ filename, lineno ] #, self.Edit.MarkerGet ( lineno ), -1 ]
    Current_Markers = self.MarkerGet ( lineno )

    if filename in self.Main_BPL :
      if lineno in self.Main_BPL [ filename ] :
        self.Main_BPL [ filename ] [ lineno ].Current_Markers = Current_Markers
    else :
      self.Main_BPL [ filename ] = {}
      
    try :
      self.Main_BPL [ filename ] [ lineno ].Current_Markers = Current_Markers
    except :
      self.Main_BPL [ filename ] [ lineno ] = BP_Class ( lineno )
      self.Main_BPL [ filename ] [ lineno ].BP_Status = BPS_CURRENT

    """
    # if a breakpoint, determine the BreakPoint List entry
    Scite_ID = None
    if ( self.Current_Line [2] & self.Edit.Break_Mask ) > 0 :
      BPL = self.All_BreakPoints
      for file in BPL :
        if file == filename :
          BP_File  = BPL [ file ]
          # now the line might be moved,
          # but by quering the Scite_ID we must find the current line
          for line in BP_File :
            Scite_ID = BP_File [ line ].Scite_ID
            if lineno == self.Edit.MarkerLineFromHandle ( Scite_ID ) :
              break
          break
    """

    self.MarkerDelete ( lineno, -1 )
    self.MarkerAddSet ( lineno, Current_Markers & ~self.Break_Mask )
    if ( Current_Markers & self.Break_Mask ) > 0 :
      self.MarkerAddSet ( lineno, Current_Markers & 0x7800 )
    else :
      self.MarkerAdd ( lineno, 10 )
    New_Scite_ID = self.MarkerAdd ( lineno, 15 )
    self.Main_BPL [ filename ] [ lineno ] .Scite_ID = New_Scite_ID

    #Print_BP_List ( self.Main_BPL )
    
    """
    # store the new Scite_ID in the breakpoint list
    # Debug_Line : Condition, Enabled, Scite_Line, Scite_ID, Debug_ID
    if Scite_ID :
      BPL [ file ] [ line ].Scite_Line = lineno
      BPL [ file ] [ line ].Scite_ID   = New_Scite_ID
    """

    self.EnsureVisibleEnforcePolicy ( lineno )
    self.GotoLine ( lineno )

    self.SetReadOnly ( False )

  # *******************************************************
  # *******************************************************
  def _BP_StateMachine ( self, lineno, ControlDown ) :
    self.MetaData_Modified = True
    if ControlDown :   # Edit Conditional BreakPoint
      self._Set_BP_On ( lineno, 3 )
    else :
      i = 0x0F & ( self.MarkerGet ( lineno ) & self.Break_Mask ) >> 11
      if   i == 0 :   # Add new BreakPoint
        self._Set_BP_On ( lineno, 1 )
      elif i == 1 :   # Remove normal BreakPoint
        self._Set_BP_On ( lineno, 0 )
      elif i == 4 :   # Enable Conditional BreakPoint
        self._Set_BP_On ( lineno, 4 )
      elif i == 8 :   # Disable Conditional BreakPoint
        self._Set_BP_On ( lineno, 5 )

  # *******************************************************
  # *******************************************************
  def _Set_BP_On ( self, lineno, state ) :
    if self.GetMarginWidth ( 2 ) <= 0 :
      return

    # if this marker was set before, get its parameters
    Org_LineNo = lineno
    Enabled    = True
    Condition  = ''
    Debug_ID   = -1
    Status     = BPS_ADDED
    if self.Filename in self.Main_BPL :
      BPs_File = self.Main_BPL [ self.Filename ]
      for Line in BPs_File :
        BP = BPs_File [ Line ]

        if lineno == BP.Scite_Line :
          #if not ( BP.BP_Status in ( BPS_IGNORE, BPS_DELETED ) ) :
          if BP.BP_Status != BPS_IGNORE :
            Org_LinenNo = Line
            Condition   = BP.Condition
            Enabled     = BP.Enabled
            Debug_ID    = BP.Debug_ID
            if state == 0 :
              BP.BP_Status = BPS_DELETED
            else :
              Status      = BPS_CHANGED
          break
    else :
      # if this file hasn't have any breakpoints, create an empty dict
      self.Main_BPL [ self.Filename ] = {}

    # Condition dialog if necessary
    #    state = 3 = conditional BP with dialog
    #    state = 5 = conditional BP without dialog
    if state == 3 :
      from dialog_support import MultiLineDialog
      Names      = [ 'Condition' ]
      Values     = [ Condition ]
      Ok, Values = MultiLineDialog ( Names, Values, [],
                                    'Set BreakPoint Condition')
      Condition = Values [0]
      if not Ok :
        return Condition
      elif not Values [0] :
        state = 1
    elif state == 5 :
      state = 3

    # first remove all bp markers at this line
    i = 0x0F & ( ( self.MarkerGet ( lineno ) & self.Break_Mask ) >> 11 )
    n = 1
    while i > 0 :
      if i & 1 :
        self.MarkerDelete ( lineno, 10 + n )
        self.MarkerDelete ( lineno, 15 + n )
      n += 1
      i = i >> 1

    # then set the new breakpoint
    Scite_ID = None
    if state :
      Scite_ID = self.MarkerAdd ( lineno, 10 + state )
      self.MarkerAdd ( lineno, 15 + state )
      if Condition :
        Enabled = not ( Enabled )
      new_BP = BP_Class ( lineno, Condition, Enabled, Scite_ID )
      new_BP.BP_Status = Status
      self.Main_BPL [ self.Filename ] [Org_LineNo] = new_BP

    return

  # *******************************************************
  # We extend AppendText with goto end of document
  # *******************************************************
  def AppendText ( self, text ) :
    stc.StyledTextCtrl.AppendText ( self, text )
    self.DocumentEnd ()

  # *******************************************************
  # to make it more like TextCtrl
  # *******************************************************
  #"""
  def write ( self, line ) :
    self.AppendText ( line )
    # and goto the end
    self.DocumentEnd()
    wx.Yield()
    #wx.Yield()

  def flush ( self ) :
    pass
  #"""
  
  # *******************************************************
  # *******************************************************
  def Hide_BreakPoint_Markers ( self ) :
    if self.Filename in self.Main_BPL:
      BPL = self.Main_BPL [ self.Filename ]
      #Debug_Lines = BPL.keys ()
      #for Debug_Line in Debug_Lines :
      for Debug_Line in BPL.keys () :
        #Scite_ID = BPL [ Debug_Line ] [3]
        BP = BPL [ Debug_Line ]
        Scite_Line = self.MarkerLineFromHandle ( BP.Scite_ID )
        #BPL [ Debug_Line ] [2] = Scite_Line
        i = 0x0F & ( ( self.MarkerGet ( Scite_Line ) & self.Break_Mask ) >> 11 )
        n = 1
        while i > 0 :
          if i & 1 :
            self.MarkerDelete ( Scite_Line, 10 + n )
            self.MarkerDelete ( Scite_Line, 15 + n )
          n += 1
          i = i >> 1

  # *******************************************************
  # *******************************************************
  def Show_BreakPoint_Markers ( self ) :
    if self.Filename in self.Main_BPL:
      BPL = self.Main_BPL [ self.Filename ]
      for Debug_Line in BPL.keys () :
        bp = 1
        BP = BPL [ Debug_Line ]
        if BP.Condition :
          bp = 3
          if not ( BP.Enabled ) :
            bp = 4
        BP.Scite_ID = self.MarkerAdd ( Debug_Line, 10 + bp )
        self.MarkerAdd ( Debug_Line, 15 + bp )

  # *******************************************************
  # *******************************************************
  def Margin_On ( self, Margin ) :
    if Margin == 0 :
      self.SetMarginWidth ( Margin, 40 )
    else :
      self.SetMarginWidth ( Margin, 12 )
    if Margin == 2 :
      self.Show_BreakPoint_Markers ()

  # *******************************************************
  # *******************************************************
  def Margin_Off ( self, Margin ) :
    self.SetMarginWidth ( Margin, 0 )
    if Margin == 2 :
      self.Hide_BreakPoint_Markers ()

  # *******************************************************
  """  Autocompletion :
  The order of events is :
    - KeyDown
    -   OnAutoCompleter, here the autocompletion can be killed
    - AddChar, doesn't occure for special keys
    -   Show AutoCompletion List
    - Update GUI
  
  """
  # *******************************************************


  # *******************************************************
  # *******************************************************
  def On_Text_From_Templates ( self, event ) :
    print ('******************* TEXT ************')
    print (event.data)
    """
      new_evt = Scintilla_Templates_Event (
                  data = self.label[ID][1] )
      wx.PostEvent ( self.parent , new_evt )
    """
    
  # *******************************************************
  # *******************************************************
  def On_Key_Down ( self, event ) :
    lineno = self.GetCurrentLine()

    self.AutoCompletion_Key   = None
    self.AutoCompletion_Later = False

    CTRL = event.ControlDown ()
    SHIFT = event.ShiftDown ()

    #if self.CallTipActive():
    #  self.CallTipCancel()
    key = event.GetKeyCode()

    #print 'KB',CTRL,key,ord('F')

    # *******************************************************
    # *******************************************************
    if CTRL and ( key == wx.WXK_UP ) : # Ctrl-
      if self.Execute_History_p > 0 :
        self.Execute_History_p -= 1
        line = self.Execute_History [ self.Execute_History_p ]
        self.AppendText ( '\n'+line.rstrip() )
    elif CTRL and ( key == wx.WXK_DOWN ) : # Ctrl-
      if len ( self.Execute_History )-1 > self.Execute_History_p :
        self.Execute_History_p += 1
        line = self.Execute_History [ self.Execute_History_p ]
        self.AppendText ( '\n'+line.rstrip() )


    # *******************************************************
    # F1       = Context Sensitive Help
    # Ctrl-F1  = alternative list
    # Shift-F1 = normally used for google search
    # *******************************************************
    elif key == wx.WXK_F1 :
      Pos = self.GetCurrentPos()
      OnlyWordChars = False
      start  = self.WordStartPosition ( Pos, OnlyWordChars )
      finish = self.WordEndPosition   ( Pos, OnlyWordChars )
      Caret_Word = self.GetTextRange ( start, finish )

      linenr = self.GetCurrentLine ()
      Line_Left_Pos  = self.PositionFromLine ( linenr )
      Line_Right_Pos = self.PositionFromLine ( linenr + 1 ) - 1
      Line = self.GetTextRange ( Line_Left_Pos, Line_Right_Pos )

      Line_Pos = Pos - Line_Left_Pos

      for L in range ( Line_Pos, -1, -1 ) :
        if Line [ L ] in ' ,()[]' :
          L += 1
          break

      for R in range ( Line_Pos, len ( Line ) ) :
        if Line [ R ] in ' ,()[]' :
          break

      Line = Line [ L:R]
      Line_Parts = Line.split ( '.' )
      print ('Firstword',Line_Parts)
      print ('cur-word',type(Caret_Word),Caret_Word)
      print (Line+'$$$')
      print ('F1', Line [ L:R]+'$$$')

      if not ( self.Help_Viewer ) :
        self.Help_Viewer = help_support.Help_Viewer_Class ( self.Local_Browser )
      else :
        self.Help_Viewer.Local_Browser = self.Local_Browser
      typ = 0
      if SHIFT :
        typ = 2
      if CTRL :
        typ = 1
      self.Help_Viewer.Find ( Caret_Word, Line_Parts, typ )
      
      
    # *******************************************************
    #         F3 = Find Next
    # Shift + F3 = Find Previous
    # Ctrl  + F3 = Goto first Error
    # *******************************************************
    elif key == wx.WXK_F3 :
      #print 'F3', CTRL,SHIFT
      if SHIFT :
        self.Search_Text ( False )
      elif CTRL :
        if self.Verify_LineNo >= 0 :
          self.EnsureVisibleEnforcePolicy ( self.Verify_LineNo )
          self.GotoLine                   ( self.Verify_LineNo )
      else :
        self.Search_Text ()

    # *******************************************************
    # BreakPoint information
    # *******************************************************
    elif key == wx.WXK_F5 :
      if SHIFT :
        self._Toggle_Bookmark ( lineno )
      else :
        self._BP_StateMachine ( lineno, CTRL )

    # *******************************************************
    # *******************************************************
    elif key == wx.WXK_F7 :
      # without knowing if already a property window exists for this device
      # we try to position / focus the window
      # if it doesn't exist (anymore) it's (re-)created
      try:
        # positioning doesn't work nice
        #self.device.Properties_Form.SetPosition ( self.popup_position )
        self.Templates_Form.SetFocus()

      except:
        from Scintilla_Templates import Scintilla_Templates_Form
        import sys
        # create the properties form and show it
        data = [1,2]
        self.Templates_Form = Scintilla_Templates_Form (
            self.TopFrame, 'PyLab Works Snippets',
            Ini = None )
        self.Templates_Form.Show ( True )


    # *******************************************************
    # *******************************************************
    elif CTRL :
      # ********************************************
      # CTRL-0123456789
      # ********************************************
      if  key in range ( ord('0'), ord ('9') ) :
        if SHIFT :
          print ('Set BOOKMARK')
          self._Toggle_Bookmark ( lineno )
        else :
          print ('Goto BOOKMARK')

      # ********************************************
      # CTRL-FFFFFFFFFFFF
      # ********************************************
      elif key == ord ('F') :
        if self.GetSelectedText () :
          self.Prev_SearchText = self.GetSelectedText ()
        else :
          Pos = self.GetCurrentPos()
          OnlyWordChars = False
          start  = self.WordStartPosition ( Pos, OnlyWordChars )
          finish = self.WordEndPosition   ( Pos, OnlyWordChars )
          self.Prev_SearchText = self.GetTextRange ( start, finish )

        OK, Values = MultiLineDialog ( Values = [ self.Prev_SearchText ],
                                       Title  = 'Enter Search String',
                                       width  = 200 )
        if OK:
          self.Prev_SearchText = Values [0]
          self.Search_Text ()

      # ********************************************
      # ********************************************
      else :
        event.Skip()

    # *******************************************************
    # Start Autocompletion List:  'A..Z', 'a..z', '_', '.'
    # *******************************************************
    elif ( key in range ( ord ( 'A' ), ord ( 'Z' ) +1 )) or \
         ( key in range ( ord ( 'a' ), ord ( 'a' ) +1 )) or \
         ( key in range ( ord ( '0' ), ord ( '9' ) +1 )) or \
         ( key ==         ord ( '_' ) ) :
      self.AutoCompletion_Key   = key
      self.AutoCompletion_Later = False
      event.Skip()

    # *******************************************************
    # Start Autocompletion List, but after screen is updated
    # *******************************************************
    elif ( key == ord ( '.' )  ) or \
         ( key == wx.WXK_RIGHT ) or \
         ( key == wx.WXK_LEFT  ) :
      self.AutoCompletion_Key   = key
      self.AutoCompletion_Later = True
      event.Skip()

    # *******************************************************
    # If AutoCompletion List visble
    #   do the autocomplete and add extra space
    # else
    #   Enter = Autoindent + code execution
    # *******************************************************
    elif key == wx.WXK_RETURN :
      if self.GetSelectedText () :
        self.CmdKeyExecute ( stc.STC_CMD_NEWLINE )
      else :
        if self.AutoCompActive () :
          # do autocompletion here and add extra space
          self.AutoCompComplete ()
          self.AddText ( ' ' )
        else :
          self.Auto_Indent ()

    # *******************************************************
    # TAB was entered while AutoCompletion list visible
    # *******************************************************
    elif key == wx.WXK_TAB :
      if self.AutoCompActive () :
        self.AutoCompCancel ()
      event.Skip()


    # *******************************************************
    # BackSpace: smart tab removal
    # *******************************************************
    elif key == wx.WXK_BACK :
      #print ' BL'
      CurPos = self.GetCurrentPos ()
      TW = self.GetTabWidth()
      # test if there are enough spaces to remove
      if CurPos >= TW :
        text   = self.GetTextRange ( CurPos - TW, CurPos )
        if text.replace ( ' ', '') == '' :
          for i in text :
            self.CmdKeyExecute ( stc.STC_CMD_DELETEBACK )
        else :
          event.Skip()
      else :
        #print ' BAKSPACE'
        #self.CmdKeyExecute ( stc.STC_CMD_DELETEBACK )
        event.Skip()

      # start autocompletion after insertion
      self.AutoCompletion_Key   = key
      self.AutoCompletion_Later = True
      if not ( self.Verify_Later ) :
        self.Verify_Later = True


    # *******************************************************
    # toggle lexer and keywords
    # TODO:
    #   through a tupple
    #   other completion list
    # *******************************************************
    elif key == wx.WXK_F6 :
      self.Current_Lexer += 1
      self.Current_Lexer %= len ( self.Available_Lexers )
      self.SetLexer ( self.Available_Lexers [ self.Current_Lexer ] )
      print ('F6', self.Current_Lexer, len ( self.Available_Lexers ))

      if self.Current_Lexer == 0 :
        self.SetKeyWords ( 0, "" )
        # set color of margin
        self.StyleSetBackground ( 33, '#FFA0A0' )

      if self.Current_Lexer == 1 :
        #self.SetLexer ( stc.STC_LEX_PYTHON )
        self.SetKeyWords ( 0, " ".join(keyword.kwlist))
        # set color of margin
        self.StyleSetBackground ( 33, '#A0A0A0' )

      elif self.Current_Lexer == 2 :
        #self.SetLexer ( stc.STC_LEX_SQL )
        self.SetKeyWords ( 0, "aap beer")
        self.StyleSetBackground ( 33, '#AA00AA' )

      # refresh the complete rendering
      self.Colourise ( 0, -1 )

    # *******************************************************
    # F12       is GUI pre-view
    # Shift-F12 is GUI in AUI panes  (ToDo)
    # *******************************************************
    elif key == wx.WXK_F12 :
      PreView_wxGUI ( self.GetText () )


    # *******************************************************
    # *******************************************************
    elif key in range ( wx.WXK_F1, wx.WXK_F13 ) :
      self.Function_Key ( key - wx.WXK_F1 + 1 )


    # *******************************************************
    # *******************************************************
    else:
      event.Skip()

  # *******************************************************
  # After a character is added, start NORMAL autocompletion
  # *******************************************************
  def OnCharAdd ( self, event ) :
    if self.AutoCompletion_Key and not ( self.AutoCompletion_Later ) :
      #print 'CAHRADD'
      self.AutoCompletion_Key = None
      self.Show_AutoCompletion_List ( )
    event.Skip()
    if not ( self.Verify_Later ) :
      self.Verify_Later = True

  # *******************************************************
  # *******************************************************
  def Verify_Code ( self ) :
    import modified_py_compile
    try:
      #py_compile.compile ( self.Main_File, doraise = True )
      modified_py_compile.compile ( self.GetText(),doraise = True )

    except modified_py_compile.PyCompileError as msg:
      lineno = msg.args[2][1][1]
      pos    = msg.args[2][1][2]
      if not ( pos ) :
        BP = self.PositionFromLine ( lineno )
        EP = self.GetLineEndPosition ( lineno )
        pos = EP - BP

      if isinstance ( pos, int ) :
        self.Verify_LineNo = lineno - 1
        self.Set_Error_Line ( self.Verify_LineNo, pos )
      else :
        # SyntaxError: ('non-keyword arg after keyword arg',
        #  ('<Active Editor Page>', 153, None, None))
        print ('WEIRD ERROR', msg)
      #print 'Syntax Error', lineno, pos
    else :
      self.Verify_LineNo = -1
      self.Set_Error_Line ()


  # *******************************************************
  # After updating the screen, start DELAYED autocompletion
  # *******************************************************
  def OnUpdateUI(self, evt):
    # In case of point insertion (due to a key press !!)
    # we need to show the autocompletion list here
    if self.AutoCompletion_Key and self.AutoCompletion_Later :
      self.AutoCompletion_Key = None
      self.Show_AutoCompletion_List ( )

    if self.Verify_Later and not ( self.AutoCompActive () ) :
      self.Verify_Code ()
      self.Verify_Later = None

    self.Get_CallTip_Info ()
    
    # check for matching braces
    braceAtCaret = -1
    braceOpposite = -1
    charBefore = None
    caretPos = self.GetCurrentPos()

    if caretPos > 0:
      charBefore = self.GetCharAt(caretPos - 1)
      styleBefore = self.GetStyleAt(caretPos - 1)

    # check before
    if charBefore and chr(charBefore) in "[]{}()" and styleBefore == stc.STC_P_OPERATOR:
      braceAtCaret = caretPos - 1

    # check after
    if braceAtCaret < 0:
      charAfter = self.GetCharAt(caretPos)
      styleAfter = self.GetStyleAt(caretPos)

      if charAfter and chr(charAfter) in "[]{}()" and styleAfter == stc.STC_P_OPERATOR:
        braceAtCaret = caretPos

    if braceAtCaret >= 0:
      braceOpposite = self.BraceMatch(braceAtCaret)

    if braceAtCaret != -1  and braceOpposite == -1:
      self.BraceBadLight(braceAtCaret)
    else:
      self.BraceHighlight(braceAtCaret, braceOpposite)
      #pt = self.PointFromPosition(braceOpposite)
      #self.Refresh(True, wxRect(pt.x, pt.y, 5,5))
      #print pt
      #self.Refresh(False)

  # *******************************************************
  # *******************************************************
  def Get_Last_Lines ( self ) :
    Result = ''
    
    # first search for the last not empty line
    Ready = False
    Last = self.GetLineCount () - 1
    while not ( Ready ) and ( Last >= 0 ) :
      Line = self.GetLine ( Last )
      if Line.strip() :
        Result = Line
        Ready = True
      else :
        Last -= 1

    # search for the empty line before that
    Ready = False
    Start = Last - 1
    while not ( Ready ) and ( Start >= 0 ) :
      Line = self.GetLine ( Start )
      if Line.strip() :
        Result = Line + Result
        Start -= 1
      else :
        Ready = True

    return Result



        
    

  # *******************************************************
  # *******************************************************
  def _Get_Word_Left ( self ) :
    # get current line, and position of caret in that line
    line, poskar = self.GetCurLine ()

    # test if caret at the end of a word
    import string
    if len ( line ) > ( poskar + 1 ) :
      # if the caret is followed by white space
      # and not preceeded by whitespace
      End_Of_Word = not ( line [ poskar -1 ] in string.whitespace ) and \
                        ( line [ poskar ]    in string.whitespace )
    else :
      # if the caret is the last character of the line
      # and not preceeded by whitespace
      End_Of_Word = ( poskar > 0 ) and \
                    not ( line [ poskar -1 ] in string.whitespace )

    if not ( End_Of_Word ) :
      return

    # get the complete word just before the caret
    line = line [ : poskar ].split()
    if len ( line ) == 0 :
      return
    
    return line [-1]

  # *******************************************************
  # *******************************************************
  def _Hide_CallTip ( self ) :
    if self.CallTipActive () :
      self.CallTipCancel ()
      self.CallTip_LineNo = -1

  # *******************************************************
  # *******************************************************
  def _Get_Word_Left_Bracket ( self ) :
    # get current line, and position of caret in that line
    line, poskar = self.GetCurLine ()

    bracket1 = line.find ( '(' )
    bracket2 = line.find ( ')', bracket1 )
    if bracket2 < 0 :
      bracket2 = len ( line )
    if ( bracket1 <  0       ) or \
       ( bracket1 >= poskar  ) or \
       ( poskar   >  bracket2 ) :
      self._Hide_CallTip ()
      return

    Left_Part  = line [ : bracket1 ].rstrip()
    Right_Part = line [ bracket1+1 : bracket2 ]

    # get the complete word just before the caret
    Left_Part = Left_Part.split()
    if len ( Left_Part ) == 0 :
      self._Hide_CallTip ()
      return

    # determine the argument index
    poskar = poskar - bracket1 - 1
    ArgNo = 0
    i     = 0
    while i < poskar :
      Next = Right_Part.find ( ',', i )
      if Next < 0 :
        break
      else :
        if poskar <= Next :
          break
        i = Next + 1
        ArgNo += 1
        
    return Left_Part [-1], ArgNo, poskar

  # *******************************************************
  # *******************************************************
  def Get_CallTip_Info ( self ) :
    result = self._Get_Word_Left_Bracket ()
    if not ( result ) :
      return
    word, ArgNo, Offset = result

    if word :
      from completer_support import Get_CallTip_Completion
      line = Get_CallTip_Completion ( word, ArgNo )

      if line :
        pos = self.GetCurrentPos()
        self.CallTipShow ( pos - Offset, line )

        # find the argument in the CallTip
        start  = line.find ( '('        )
        Finish = line.find ( ')', start )
        if ( start < 0 ) or ( Finish < 0 ) :
          return
        
        # and HighLight the selected argument
        finish = line.find ( ',', start+1 )
        for i in range ( ArgNo ) :
          start  = finish
          finish = line.find ( ',', start+1 )
        #print 'SF',start,finish
        if ( finish < 0 ) or ( finish > Finish ):
          finish = Finish
        self.CallTipSetHighlight ( start+1, finish )

  # *******************************************************
  # Create and show the autocompletion list
  # *******************************************************
  def Show_AutoCompletion_List ( self ) :
    word = self._Get_Word_Left ()
    """
    # get current line, and position of caret in that line
    line, poskar = self.GetCurLine ()

    # test if caret at the end of a word
    import string
    if len ( line ) > ( poskar + 1 ) :
      # if the caret is followed by white space
      # and not preceeded by whitespace
      End_Of_Word = not ( line [ poskar -1 ] in string.whitespace ) and \
                        ( line [ poskar ]    in string.whitespace )
    else :
      # if the caret is the last character of the line
      # and not preceeded by whitespace
      End_Of_Word = not ( line [ poskar -1 ] in string.whitespace )

    if not ( End_Of_Word ) :
      return
    
    # get the complete word just before the caret
    print len ( line ), poskar,'$$$'
    line = line [ : poskar ].split()
    if len ( line ) == 0 :
      return
    word = line [-1]
    """
    
    if word :
      from completer_support import Get_Completions
      Result = Get_Completions ( word )
      if Result :
        self.AutoCompShow ( *Result )
  # *******************************************************


  # *******************************************************
  # This method can be overriden to execute the collected code
  # *******************************************************
  def Execute_Code ( self, Force_Modified = False ) :
    if Application.Debug_Mode and self.Execute_Code_Count :
      print ('>>>>>>> Debugger should override "Execute_Code"')
      self.Execute_Code_Count = False

  # *******************************************************
  # This method can be overriden to get non-handeld function keys
  # *******************************************************
  def Function_Key ( self, key ) :
    if Application.Debug_Mode and self.Function_Key_Count :
      print ('>>>>>>> Debugger should override "Function_Key"', key)
      self.Function_Key_Count = False
    
  # *******************************************************
  # *******************************************************
  def Auto_Indent(self):
    cont_kwds = [ 'else', 'elif', 'except' ]

    linenr = self.GetCurrentLine ()
    BP = self.PositionFromLine ( linenr )
    CP = self.GetCurrentPos ()
    EP = self.GetLineEndPosition ( linenr )

    text   = self.GetTextRange ( BP, CP )
    text_r = self.GetTextRange ( CP, EP )

    indent = self.GetLineIndentation ( linenr )
    caret  = CP-BP

    # *****************************************************
    # increase indentation if ":" is at the end of the line
    # *****************************************************
    rtext = text.rstrip ()
    if rtext and rtext[-1] == ':' :
      indent += self.GetTabWidth ()

    # *****************************************************
    # if text on the right of the caret,
    # just insert \n and the same indent
    # *****************************************************
    if text_r.strip() :
      addline = '\n' + indent * u' '
      self.AddText ( addline )

    # *****************************************************
    elif indent <= self.GetTabWidth () :
      self.AddText ( '\n' )
    else :
      # *****************************************************
      # If we get an Return-Key on a line with only whitespace
      # *****************************************************
      if text.strip () == u'' :
        # *****************************************************
        # try to decrease the indentation     )
        # *****************************************************
        if indent > 0 :
          remove = self.GetTabWidth ()
          if remove > caret :
            remove = caret
          indent -= remove
          for i in range ( remove ) :
            self.CmdKeyExecute ( stc.STC_CMD_DELETEBACK )
        # *****************************************************
        # or just add the whitespace to the editor
        # *****************************************************
        else :
          addline = '\n' + text
          self.AddText ( addline )

      # *****************************************************
      # if not only whitespace, the Return-Key will generate
      # a new line with the same indentation as the last line
      # *****************************************************
      else :
        addline = '\n' + indent * u' '
        self.AddText ( addline )


    # *******************************************************
    # if the Return-Key resulted in an new indent == 0
    # So we can execute the code
    # *******************************************************
    if ( indent == 0 ):
      text = self.GetTextRange ( self.GetCurrentPos (),
                                 self.GetTextLength () )
      # ***************************************
      # and the text after the current position
      # consists only of white space
      # ***************************************
      if text.strip() == '' :
        linenr = self.GetCurrentLine ()

        # ***************************************
        # gather the complete code before
        # the current line = last line
        # ***************************************
        ready = False
        total = ''
        while not ( ready ) :
          linenr -= 1
          line = self.GetLine ( linenr )
          #print 'GET',linenr, self.GetLineIndentation ( linenr ), line, '***'

          # ******************************************
          # Beginning found, if an empty line is found
          # ******************************************
          if line.strip () == '' :
            ready = True

          # *******************************************
          # Beginning found, if indentation of line = 0
          # *******************************************
          elif self.GetLineIndentation ( linenr ) == 0 :
            pos = line.find (':')
            #print 'LINE',line,pos
            if ( pos < 0 ) or \
               not ( line [ : pos ].strip() in cont_kwds ) :
              total = line + total
              ready = True
              
          # *******************************************
          # if not yet beginning found, just add the text
          # also stop when the beginning of document is reached
          # *******************************************
          if not ( ready ) :
            total = line + total
            if linenr < 0 :
              ready = True

        # *******************************************
        # Now if we really have code, execute it
        # *******************************************
        #print 'TOTAL',total,'$$$$'
        if total.strip () != '' :
          self.Code_To_Execute = total
          # But first store it in the buffer
          self.Execute_History.append ( self.Code_To_Execute )
          self.Execute_History_p = len ( self.Execute_History ) - 1
          self.Execute_Code ( wx.WXK_RETURN )

    #Edit[0].EnsureVisibleEnforcePolicy ( lineno )
    self.EnsureCaretVisible ()


  # *******************************************************
  # *******************************************************
  def _Toggle_Bookmark ( self, lineno ) :
    self.MetaData_Modified = True
    if ( self.MarkerGet ( lineno ) ) & self.BookMark_Mask > 0 :
      Mask = ( self.MarkerGet ( lineno ) ) & self.BookMark_Mask
      BM = 0
      while Mask > 0 :
        if Mask & 1 :
          self.MarkerDelete ( lineno, BM )
          #self.BookMarks [BM] = None
          self.BookMarks.pop ( BM )
        Mask = Mask >> 1
        BM += 1
    else :
      # find a free bookmark, otherwise
      for i, BM in enumerate ( self.BookMarks ):
        if not ( BM ) :
          self.MarkerAdd ( lineno, i )
          self.BookMarks [i] = lineno
          break

  # *******************************************************
  # *******************************************************
  def OnMarginClick(self, event):
    lineno = self.LineFromPosition(event.GetPosition())

    # Handle Breakpoints
    if event.GetMargin() in ( 0, 1, 2 ) :
      if event.GetShift() :
        self._Toggle_Bookmark ( lineno )
      else :
        self._BP_StateMachine ( lineno, event.GetControl() )

    # fold and unfold as needed
    elif event.GetMargin() == 3:
      if event.GetShift() and event.GetControl():
        self.FoldAll()
      else:
        lineClicked = self.LineFromPosition(event.GetPosition())

        if self.GetFoldLevel( lineno ) & stc.STC_FOLDLEVELHEADERFLAG:
          if event.GetShift():
            self.SetFoldExpanded( lineno , True)
            self.Expand( lineno , True, True, 1)
          elif event.GetControl():
            if self.GetFoldExpanded ( lineno ):
              self.SetFoldExpanded( lineno, False)
              self.Expand( lineno, False, True, 0)
            else:
              self.SetFoldExpanded( lineno, True)
              self.Expand( lineno, True, True, 100)
          else:
            self.ToggleFold( lineno )

    else :
      print ('MARGIN',event.GetMargin())
      
  # *******************************************************
  # *******************************************************
  def FoldAll(self):
    lineCount = self.GetLineCount()
    expanding = True

    # find out if we are folding or unfolding
    for lineNum in range(lineCount):
      if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
        expanding = not self.GetFoldExpanded(lineNum)
        break

    lineNum = 0

    while lineNum < lineCount:
      level = self.GetFoldLevel(lineNum)
      if level & stc.STC_FOLDLEVELHEADERFLAG and \
         (level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:

        if expanding:
          self.SetFoldExpanded(lineNum, True)
          lineNum = self.Expand(lineNum, True)
          lineNum = lineNum - 1
        else:
          lastChild = self.GetLastChild(lineNum, -1)
          self.SetFoldExpanded(lineNum, False)

          if lastChild > lineNum:
              self.HideLines(lineNum+1, lastChild)

      lineNum = lineNum + 1

  # *******************************************************
  # *******************************************************
  def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
    lastChild = self.GetLastChild(line, level)
    line = line + 1

    while line <= lastChild:
      if force:
        if visLevels > 0:
          self.ShowLines(line, line)
        else:
          self.HideLines(line, line)
      else:
        if doExpand:
          self.ShowLines(line, line)

      if level == -1:
        level = self.GetFoldLevel(line)

      if level & stc.STC_FOLDLEVELHEADERFLAG:
        if force:
          if visLevels > 1:
            self.SetFoldExpanded(line, True)
          else:
            self.SetFoldExpanded(line, False)

          line = self.Expand(line, doExpand, force, visLevels-1)

        else:
          if doExpand and self.GetFoldExpanded(line):
            line = self.Expand(line, True, force, visLevels-1)
          else:
            line = self.Expand(line, False, force, visLevels-1)
      else:
        line = line + 1

    return line


  # *****************************************************************
  # *****************************************************************
  def Search_Text ( self, down = True ) :
    self.SearchAnchor()
    if down :
      # assume we're on a previous found item
      # therefor advance curosr 1 position
      pos = self.GetCurrentPos ()
      self.GotoPos ( pos + 1 )
      self.SearchAnchor()
      result = self.SearchNext ( 0, self.Prev_SearchText )
    else :
      result = self.SearchPrev ( 0, self.Prev_SearchText )

    if result != -1 :
      pos = self.GetCurrentPos ()
      linenr = self.LineFromPosition ( pos )
      self.EnsureVisibleEnforcePolicy ( linenr )
      self.GotoPos ( pos )
    else :
      #import curses
      #curses.beep()
      if down :
        self.GotoPos ( pos )


  # *****************************************************************
  # search text in document, Copied from ... NOT TESTED
  # *****************************************************************
  def Search ( self, searchtext='', gotoline=-1 ):
    if searchtext :
      # first go to the end of the document,
      # search backwards, so the result will be on top of display
      self.DocumentEnd()
      self.SearchNext ( 0, searchtext )
      if self.GetCurrentPos() > 0 :
        linenr = self.LineFromPosition ( self.GetCurrentPos () )
      else :
        # if searchtext not found, try linenumber
        linenr = gotoline
    else :
      # goto linenr ?
      linenr = gotoline

    if linenr >= 0 :
      self.EnsureVisibleEnforcePolicy ( linenr )
      self.GotoLine (linenr)
      

  def _On_Menu_Print ( self, event ) :
    FileName = self.Filename
    if not ( FileName ) :
      FileName = 'NoName'

    #stc.STC_PRINT_COLOURONWHITE
    #
    self.SetPrintColourMode ( stc.STC_PRINT_COLOURONWHITE)

    pdd = wx.PrintDialogData ()
    pdd.SetPrintData ( self._printData )
    printer  = wx.Printer ( pdd )
    printout = STCPrintout ( self,
                             self._printData,
                             self._print_margins_TopLeft,
                             self._print_margins_BottomRight,
    		                     FileName )
    #print printer
    #print printer.GetPrintDialogData().
    #return
  
  
    if not printer.Print ( self, printout ) :
      PG.em ( 'Print' )
    else:
      self.printData = wx.PrintData ( printer.GetPrintDialogData().GetPrintData() )
    printout.Destroy()
    event.Skip ()

  def _On_Menu_Print_Preview ( self, event ) :
    FileName = self.Filename
    if not ( FileName ) :
      FileName = 'NoName'
    po1 = STCPrintout ( self,
                        self._printData,
                        self._print_margins_TopLeft,
                        self._print_margins_BottomRight,
                        FileName )
    po2 = STCPrintout ( self,
                        self._printData,
                        self._print_margins_TopLeft,
                        self._print_margins_BottomRight,
                        FileName )
    self.PrintPreview = wx.PrintPreview ( po1, po2, self._printData )
    self.PrintPreview.SetZoom ( self._print_zoom)
    if not self.PrintPreview.Ok():
      PG.em ( 'Print Preview' )
      return

    self.Preview = wx.PreviewFrame ( self.PrintPreview, self.TopFrame,
                                     "Print Preview   " + FileName )
    self.Preview.Bind ( wx.EVT_CLOSE, self._On_Close_Preview_Window )
    self.Preview.Initialize ()
    self.Preview.Maximize ()
    self.Preview.Show ( True )
    event.Skip ()

  # closing the printpreview is used to capture the user settings
  def _On_Close_Preview_Window ( self, event ):
    self._print_zoom = self.PrintPreview.GetZoom()
    event.Skip()

  def _On_Menu_Page_Setup ( self, event ) :
    # there seems to be 3 almost identical datasets:
    #    PrintData, PrintDialogData, PageSetupDialogData
    # PageSetupDialogData, seems to have the best overall set
    # but for example no orientation :-(

    # Create dataset, and copy the relevant data
    #   from printData and margins into this dataset
    dlgData = wx.PageSetupDialogData ( self._printData )
    dlgData.SetDefaultMinMargins ( True )
    dlgData.SetMarginTopLeft ( self._print_margins_TopLeft )
    dlgData.SetMarginBottomRight ( self._print_margins_BottomRight )

    # start page setup dialog
    printDlg = wx.PageSetupDialog ( self, dlgData )
    if printDlg.ShowModal () == wx.ID_OK :
      # if ok, copy data back into globals
      dlgData = printDlg.GetPageSetupData ()
      self._printData = wx.PrintData ( dlgData.GetPrintData () )
      self._print_margins_TopLeft = dlgData.GetMarginTopLeft ()
      self._print_margins_BottomRight = dlgData.GetMarginBottomRight ()

      # store data in inifile

    printDlg.Destroy()

    print ('Paper ID / Size:', self._printData.GetPaperId (), self._printData.GetPaperSize ())
    print ('Margins:', self._print_margins_TopLeft, self._print_margins_BottomRight)
    print ('Orientation / BIN: ', self._printData.GetOrientation (), self._printData.GetBin ())
    print ('Quality:', self._printData.GetQuality ())
    """
    Paper ID / Size: 13 (210, 297)
    Margins: (40, 10) (20, 30)
    Orientation / BIN:  1 2
    """
    event.Skip ()
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class STCPrintout(wx.Printout):
  def __init__( self, stc, PrintData=None,
                MarginTopLeft = (10,10),
                MarginBottomRight = (10,10),
                filename = ''):
    wx.Printout.__init__(self)
    self.stc = stc
    self.filename = filename
    self.PrintData = PrintData
    self.MarginTopLeft = MarginTopLeft
    self.MarginBottomRight = MarginBottomRight

  def HasPage ( self, page ) :
    return ( page <= self.NumPages )

  def GetPageInfo ( self ) :
    return ( 1, self.NumPages, 1, 32000 )

  def Calculate_Scale ( self, dc ) :
    PPI_Printer_X, PPI_Printer_Y = self.GetPPIPrinter ()
    PPI_Screen_X,  PPI_Screen_Y  = self.GetPPIScreen ()
    PS_Scale = 1.0 * PPI_Printer_Y / PPI_Screen_Y

    pw, ph = self.GetPageSizePixels ()
    dw, dh = dc.GetSize ()
    self.Scale = PS_Scale * dh / ph
    dc.SetUserScale ( self.Scale, self.Scale )
    self.UnitsMM = 1.0 * PPI_Printer_Y /  ( PS_Scale * 25.4 )

    self.x1 = self.MarginTopLeft[0] * self.UnitsMM
    self.y1 = self.MarginTopLeft[1] * self.UnitsMM
    self.x2 = dc.DeviceToLogicalXRel ( dw ) - \
              self.MarginBottomRight[0] * self.UnitsMM
    self.y2 = dc.DeviceToLogicalYRel ( dh ) - \
              self.MarginBottomRight[1] * self.UnitsMM
    self.PageHeight = self.y2 - self.y1
    print ('XY', int(self.x1), int(self.y1), int(self.x2), int(self.y2))
    print ('Scales', self.Scale, self.UnitsMM, PS_Scale)
    print ('ps',pw,ph,dw,dh)

    # font for page titles
    dc.SetFont( wx.FFont( 10, wx.ROMAN ) )
    self.LineHeight = dc.GetCharHeight()
    print (self.PageHeight, self.LineHeight)
    self.LinesPerPage = int ( self.PageHeight / self.LineHeight )
    #print ' PREPARE' , self.LineHeight, int(self.PageHeight) ,self.LinesPerPage

    self.NumPages, m = divmod ( self.stc.GetLineCount(), self.LinesPerPage )
    if m: self.NumPages += 1

    # to get all the lines on the preview, we need to set magnification
    # we'll be able to see all lines,
    # but depending on the scaling, the view is good or reasonable
    self.stc.SetPrintMagnification (0)

  def OnPreparePrinting ( self ) :
    dc = self.GetDC()
    self.Calculate_Scale (dc)

  def OnPrintPage(self, page):
    import datetime
    dc = self.GetDC()
    self.Calculate_Scale (dc)

    # font might be destroyed by STC rendering !!
    dc.SetFont( wx.FFont( 10, wx.ROMAN ) )
    dc.SetTextForeground ("black")

    # print filename on top
    if self.filename:
      tlw, tlh = dc.GetTextExtent(self.filename)
      dc.DrawText ( self.filename, self.x1, self.y1 - tlh -10 )

    # print date and pagenumber at the bottom
    t = datetime.date.today()
    pageLabel = t.strftime("%d-%m-%Y")
    dc.DrawText ( pageLabel, self.x1, self.y2 )

    pageLabel = 'Page: ' + str(page) + '/' + str(self.NumPages)
    plw, plh = dc.GetTextExtent(pageLabel)
    dc.DrawText ( pageLabel, self.x2 - plw, self.y2 )

    # render stc into dc
    stcStartPos = self.stc.PositionFromLine   ( (page-1) * self.LinesPerPage     )
    stcEndPos   = self.stc.GetLineEndPosition (  page    * self.LinesPerPage - 1 )
    maxWidth = 32000

    self.stc.SetPrintColourMode ( stc.STC_PRINT_COLOURONWHITEDEFAULTBG )
    # first rectangle is rendering rectangle, second is the page rectangle
    # so why not use for both the rendering rectangle
    rect = wx.Rect ( self.x1, self.y1, self.x2, self.y2 )
    ep = self.stc.FormatRange(1, stcStartPos, stcEndPos, dc, dc, rect, rect )

    #print 'R1',int(self.x1),int(self.y1),maxWidth,int(self.y2-self.y1),self.stc.GetPrintMagnification()

    """
    # FOR TEST, draw outline
    dc.SetPen ( wx.Pen ( "black", 0 ) )
    dc.SetBrush ( wx.TRANSPARENT_BRUSH )
    r = wx.RectPP ( ( self.x1, self.y1 ), ( self.x2, self.y2 ) )
    dc.DrawRectangleRect ( r )
    #dc.SetClippingRect ( r )
    """

    """
    # warn when fewer characters than expected are rendered by the stc when
    # printing
    if not self.IsPreview():
      if ep < stcEndPos:
      PG.em ( 'Printing page %s: not enough chars rendered, diff: %s')%(page, stcEndPos-ep)
    return True
    """
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class my_Test_Form ( My_Frame_Class ) :

  # *****************************************************************
  # *****************************************************************
  def __init__( self, main_form= None, ini = None ) :
    Title = 'PyLab_Works Scintilla Test    v' + str ( _Version_Text[0][0] )
    My_Frame_Class.__init__ ( self, main_form, Title, ini, 'Test Form' )

    GUI = """
    self.PVer                  ,PanelVer, 01
      panel                    ,wx.Panel
        Button_1               ,wx.Button , label = "Toggle BPs"
      self.Edit                ,Base_STC
    """
    self.Ini_File = ini
    if ini : IniName = 'self.Ini_File'
    self.wxGUI = Create_wxGUI ( GUI, IniName = IniName )

    # Allow BreakPoints Margin
    self.Edit.Margin_On ( 2 )

    self.Bind ( wx.EVT_CLOSE,  self.On_Close  )
    self.Bind ( wx.EVT_BUTTON, self.On_Button )

    # we create the debugger here
    self.Main_File = 'G:/OPENSOURCE/Data_Python_3/PyLab_Works/test_IDE.py'
    self.All_BreakPoints = self.Edit.LoadFile ( self.Main_File )
    print("check loader",self.All_BreakPoints)
    self.Edit.StartStyling ( 40, stc.STC_INDICS_MASK)
    self.Edit.SetStyling   ( 10, stc.STC_INDIC2_MASK)


  # *********************************************************
  # *********************************************************
  def On_Button ( self, event ) :
    if self.Edit.GetMarginWidth (2) > 0 :
      self.Edit.Margin_Off ( 2 )
    else :
      self.Edit.Margin_On ( 2 )

  # *********************************************************
  # *********************************************************
  def On_Close ( self, event ) :
    print ('Scite Close')
    self.Edit.SaveFile ( self.Main_File, self.All_BreakPoints, True )

    ini = self.Ini_File
    if ini :
      ini.Section = self.Ini_Section
      ini.Write ( 'Pos',  self.GetPosition () )
      ini.Write ( 'Size', self.GetSize () )
      self.wxGUI.Save_Settings ()

    event.Skip ()
# ***********************************************************************


# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':
  app = wx.App ()
  ini = inifile ( os.path.join (os.getcwd(), 'Scintilla.cfg' ))
  ini.Section = 'Scintilla Test'

  Main_Form = my_Test_Form ( None, ini )
  Main_Form.Show()

  app.MainLoop ()

  # The inifile can be used by more forms, so we close it here
  ini.Close ()
# ***********************************************************************
pd_Module ( __file__ )

