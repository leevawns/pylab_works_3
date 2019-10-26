# ***********************************************************************
#from PyLab_Works_Globals  import *
#from PyLab_Works_Globals  import _
#from language_support     import Language_IDs
from gui_support          import *
#from system_support       import run
#from tree_support         import *
#from menu_support         import *
#from picture_support      import *
#from doc_support          import *
#from inspect              import *
from Scintilla_support    import *
#from pw_winpdb            import Simple_RPDB2_Debugger
#from PyLab_Works_Debugger import *
# ***********************************************************************


# ***********************************************************************
# This file is derived from the wxPython demo.
# A major change was made to let the autocompletion work well.
# ***********************************************************************
import  keyword
import  wx
import  wx.stc  as  stc
from file_support import *
from inifile_support import *

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
                 
    self.Code_To_Execute = ''
    self.Code_Globals = {}
    self.Code_Locals  = {}
    self.Main_BPL     = {}
    self.MainFile     = False
    self.Filename     = None

    stc.StyledTextCtrl.__init__(self, parent, ID, pos, size, style)

    self.CmdKeyAssign(ord('B'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
    self.CmdKeyAssign(ord('N'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

    self.Current_Lexer = 1
    self.SetLexer ( self.Available_Lexers [ self.Current_Lexer ] )
    self.SetKeyWords ( 0, " ".join(keyword.kwlist))

    #self.SetLexer ( stc.STC_LEX_SQL )
    #self.SetKeyWords ( 1, "aap beer")

    
    self.SetTabWidth(2)
    self.SetIndent(2)
    #self.SetIndentationGuides(True)

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
    self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
    self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")

    #self.GetLineState()
    #self.GetMaxLineState()
    #self.IndicatorSetStyle()
    #self.GetStyleAt()

    # Python styles
    # Default
    print ('beer',stc.STC_P_DEFAULT,stc.STC_P_TRIPLEDOUBLE)
    #"fore:#000000,face:%(helv)s,size:%(size)d" % faces
    
    
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
    self.AutoCompSetFillUps    ( '. '  )
    self.AutoCompSetIgnoreCase ( False )
    self.AutoCompSetAutoHide   ( True  )

    # *******************************************************
    self.Bind ( stc.EVT_STC_MARGINCLICK, self.OnMarginClick )
    self.Bind ( wx.EVT_KEY_DOWN,         self.On_Key_Down   )
    self.Bind ( stc.EVT_STC_CHARADDED,   self.OnCharAdd     )
    self.Bind ( stc.EVT_STC_UPDATEUI,    self.OnUpdateUI    )
    self.AUTO = None

    #stc.EVT_STC_KEY

  # *******************************************************
  # We take over file saving, so we can save bookmarks and caret
  # *******************************************************
  def SaveFile ( self, filename, BreakPoints = None, MainFile = False ) :
    self.Filename = filename
    if self.GetModify () :
      stc.StyledTextCtrl.SaveFile ( self, filename )
      self.MetaData_Modified = True

    if self.MetaData_Modified :
      BookMarks = {}
      for lineno in range ( self.GetLineCount () ) :
        BM = ( self.MarkerGet ( lineno ) ) & self.BookMark_Mask
        if BM > 0 :
          BookMarks [ BM ] = lineno

      project_file = Change_FileExt ( filename, 'pwp' )
      ini = inifile ( project_file )
      ini.Section = 'Scintilla Editor'

      linenr = self.GetCurrentLine ()
      ini.Write ( 'LineNo', lineno )
      ini.Write ( 'BM',  BookMarks )

      # ReCalculate Breakpoints
      # By editing the file, they might have been moved
      if BreakPoints :
        print ('Recaluc BPS',BreakPoints)
        BP_File = BreakPoints [ self.Filename ]
        BPs = BP_File.keys()
        for BP in BPs :
          lineno = self.MarkerLineFromHandle ( BP_File[BP][3] )
          print (lineno)
          # if lineno as a key has changed
          # remove the record and insert a new one
          # if lineno = -1, it's the current line, so don't change it
          if lineno != -1 :
            if lineno != BP :
              newBP = BP_File [ BP ]
              del BP_File [BP]
              BP_File [ lineno ] = newBP
              print ('Rec BPS',BreakPoints)

            i = 0x0F & ( ( self.MarkerGet ( lineno ) & self.Break_Mask ) >> 11 )
            #BP_File[lineno][1] = i
            BP_File[lineno][1] = ( i != 8 )
            BP_File[lineno][2] = lineno
            #BP_File[lineno][3] = -1

      if MainFile :
        ini.Write ( 'BP', BreakPoints )
        print ('STORE BPS',BreakPoints)

      ini.Close ()
      
  # *******************************************************
  # We take over file loading,
  # so we can restore bookmarks, caret and breakpoints
  # *******************************************************
  def LoadFile ( self, filename, BreakPoints = None ) :
    print (' lllllllllllllllllllLLLLLLLLLLLLLLL')
    self.Filename = filename
    self.MainFile = ( BreakPoints == None )
    # in case of the mainfile, we have to set MetaData changed True
    # to garantee that breakpoint changes in other files are stored
    self.MetaData_Modified = self.MainFile
    stc.StyledTextCtrl.LoadFile ( self, filename )

    project_file = Change_FileExt ( filename, 'pwp' )
    if File_Exists ( project_file ) :
      ini = inifile ( project_file )
      ini.Section = 'Scintilla Editor'
      linenr = ini.Read ( 'LineNo', 0 )
      BookMarks   = ini.Read_Dict ( 'BM' )
      if self.MainFile :
        BreakPoints = ini.Read_Dict ( 'BP' )
        self.Main_BPL = BreakPoints
        ###### Temprorary no loading
        print ('Main_BPL-LOAD',self.Main_BPL)
        ##BreakPoints = self.Main_BPL = {}
      ini.Close ()

      #print 'LINENO START',linenr
      #linenr = 2
      self.GotoLine (linenr)

      for BM in BookMarks :
        self.MarkerAddSet ( int ( BookMarks [BM] ), BM )

      if self.MainFile :
        BP_files = BreakPoints.keys()
        for filnam in BP_files :
          BPs_File = BreakPoints [ filnam ]
          BPs_Keys = BPs_File.keys()
          print ('&&&&&&&&&&&&',BPs_Keys)
          for lineno in BPs_Keys :
            print ('XXX',lineno)
            params = BPs_File [ lineno ]
            print ('RRRDDD',lineno, params, filnam)
            """
            if BPs[lineno][0] != '' :
              if BPs[lineno][1] :
                state = 5
              else :
                state = 4
            else :
              state = 1
            # set in editor only if it concerns this file
            Condition = ''
            if filnam == filename :
              #Condition = self._Set_BP_On ( lineno-1, state, BPs [lineno][0] )
              Condition = self._Set_BP_On ( lineno, state, BPs [lineno][0] )
            #self.On_BreakPoint_Change ( filnam, lineno, state, Condition )
            """

            if filnam == filename :
              # prevent asking for the condition
              if params[1] == 3 :
                self._Set_BP_On ( lineno, 5 )
              else :
                self._Set_BP_On ( lineno, params[1] )
        print (BreakPoints)
        return BreakPoints
      
      # not the main file, so breakpoints are set in Debugger,
      # but not yet in editor
      else :
        for filnam in BreakPoints :
          if filnam == filename :
            BPs = BreakPoints [ filename ]
            for lineno in BPs :
              print ('RRRDDD2',lineno, BPs [ lineno ], filename)
              if BPs[lineno][0] != '' :
                if BPs[lineno][1] :
                  state = 5
                else :
                  state = 4
              else :
                state = 1
              #Condition = self._Set_BP_On ( lineno-1, state, BPs [lineno][0] )
              Condition = self._Set_BP_On ( lineno, state, BPs [lineno][0] )
              #self.On_BreakPoint_Change ( filename, lineno, state, Condition )

    self.Main_BPL = BreakPoints
    
  # *******************************************************
  # *******************************************************
  def _BP_StateMachine ( self, lineno, ControlDown ) :
    self.MetaData_Modified = True
    if ControlDown :
      Condition = self._Set_BP_On ( lineno, 3 )
    else :
      i = ( self.MarkerGet ( lineno ) & self.Break_Mask ) >> 11
      i &= 0x0F
      if   i == 0 :
        Condition = self._Set_BP_On ( lineno, 1 )
      elif i == 1 :
        Condition = self._Set_BP_On ( lineno, 0 )
      elif i == 4 :
        Condition = self._Set_BP_On ( lineno, 4 )
      elif i == 8 :
        Condition = self._Set_BP_On ( lineno, 5 )
    state = 0x0F & ( ( self.MarkerGet ( lineno ) & self.Break_Mask ) >> 11 )
    self.Notify_Debugger_BP_Changed ( self.Filename, lineno, state, Condition )


  # *******************************************************
  # Called when a breakpoint is changed by the user
  # Can be used by the parent to react on the new breakpoint settings
  # *******************************************************
  def Notify_Debugger_BP_Changed ( self, filename, lineno, state, Condition ) :
    pass

  # *******************************************************
  # *******************************************************
  def _Set_BP_On ( self, lineno, bp ) :
    if not ( self.Main_BPL ) :
      return
    
    # if this marker was set before, get its parameters
    # and delete the entry
    #Cur_LineNo  = lineno
    Enabled     = True
    Condition   = ''
    if self.Main_BPL.has_key ( self.Filename ) :
      BPs_File = self.Main_BPL [ self.Filename ]
      BPs_Keys = BPs_File.keys()
      for BP in BPs_Keys :
        params = BPs_File [BP]
        Scite_ID = params[3]
        Old_LineNo = self.MarkerLineFromHandle ( Scite_ID )
        if ( Old_LineNo == -1 ) or \
           ( lineno == Old_LineNo ):
          Condition   = params [0]
          Enabled     = params [1]
          #Org_LinenNo = BP
          Debug_ID    = params [4]
          # Remove BreakPoint from Debugger
          self.Notify_Debugger_BP_Changed ( self.Filename, Debug_ID, 0 )
          del  self.Main_BPL [ self.Filename ][BP]
          break
    else :
      # if this file hasn't have any breakpoints, create an empty dict
      self.Main_BPL [ self.Filename ] = {}
    print ('lllooo',bp,Condition,lineno)
    
    # Condition dialog if necessary
    #    bp = 3 = conditional BP with dialog
    #    bp = 5 = conditional BP without dialog
    if bp == 3 :
      from dialog_support import MultiLineDialog
      Names      = [ 'Condition' ]
      Values     = [ Condition ]
      Ok, Values = MultiLineDialog ( Names, Values, [],
                                    'Set BreakPoint Condition')
      Condition = Values [0]
      if not Ok :
        return Condition
      elif not Values [0] :
        bp = 1
    elif bp == 5 :
      bp = 3
    print ('OK?',Condition)

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
    if bp :
      Scite_ID = self.MarkerAdd ( lineno, 10 + bp )
      self.MarkerAdd ( lineno, 15 + bp )

      Debug_ID = -1
      Debug_Change = 0
      new_BP = [ Condition, Enabled, lineno, Scite_ID, Debug_ID, Debug_Change ]
      self.Main_BPL [ self.Filename ] [lineno] = new_BP

      print ('_Set_NP-33',bp,Scite_ID,self.Main_BPL)
      BPs = self.Main_BPL [ self.Filename ]
      for BP in BPs :
        print ('ADD-BP',BP, BPs [BP])

    print ('Main_BPL-1',self.Main_BPL)
    return Condition

  # *******************************************************
  # We extend AppendText with goto end of document
  # *******************************************************
  def AppendText ( self, text ) :
    stc.StyledTextCtrl.AppendText ( self, text )
    self.DocumentEnd ()

  # *******************************************************
  # to make it more like TextCtrl
  # *******************************************************
  def write ( self, line ) :
    self.AppendText ( line )
    # and goto the end
    self.DocumentEnd()

  def flush ( self ) :
    pass

  # *******************************************************
  # *******************************************************
  def Margin_On ( self, Margin ) :
    if Margin == 0 :
      self.SetMarginWidth ( Margin, 40 )
    else :
      self.SetMarginWidth ( Margin, 12 )

  # *******************************************************
  # *******************************************************
  def Margin_Off ( self, Margin ) :
    self.SetMarginWidth ( Margin, 0 )

  # *******************************************************
  # Create and show the autocompletion list
  # *******************************************************
  def Show_AutoCompletion_List ( self ) :
    # get current line, and position of caret in that line
    line, poskar = self.GetCurLine ()

    # test if caret at the end of a word
    import string
    if len ( line ) > ( poskar + 1 ) :
      End_Of_Word = line [ poskar ] in string.whitespace
    else :
      End_Of_Word = True

    if End_Of_Word:
      # get the complete word jsut before the caret
      line = line [ : poskar ].split()
      word = line [-1]

      # split the word, in case it contains prefixes with a '.'
      pre_word = None
      if word.find('.') >= 0 :
        word = word.split('.')
        pre_word = '.'.join ( word [ : -1 ] )
        word = word [-1]

      # Popup_AutoCompletion_List ( word, pre_word )
      # Only if we have a word or a pre_word !!
      wl = len ( word )
      if (( wl == 0 ) and not ( pre_word )) : return

      # in case of prefixes, get another list, which one ??
      if pre_word :
        kw = dir ( __name__ )
        #kw = dir ( __builtins__ )
        #kw = dir ( pre_word )
      else :
        kw = keyword.kwlist [ : ]
      #print 'WORD,PRE',word,'//',pre_word,'//',line,wl,self.AutoCompActive()

      # limit the list to matches of the already known part of the word
      if word == '' :
        newlist = kw
      else :
        newlist = []
        for item in kw:
          if item.find ( word ) == 0:
            newlist.append (item)

      newlist.sort ()
      self.AutoCompShow ( wl, ' '.join ( newlist ) )
      #self.AutoCompActive()
      #self.AutoCompCancel()
  # *******************************************************


  # *******************************************************
  # This method can be overriden to execute the collected code
  # *******************************************************
  def Execute_Code ( self ) :
    #print 'CODE:',self.Code_To_Execute
    #self.Code_To_Execute = ''
    pass
    
  # *******************************************************
  # *******************************************************
  def Auto_Indent(self):
    cont_kwds = [ 'else', 'elif', 'except' ]
    
    linenr = self.GetCurrentLine ()
    text   = self.GetTextRange ( self.PositionFromLine ( linenr ),
                                 self.GetCurrentPos () )
    indent = self.GetLineIndentation ( linenr )

    # *****************************************************
    # increase indentation if ":" is at the end of the line
    # *****************************************************
    rtext = text.rstrip ()
    if rtext and rtext[-1] == ':' :
      indent += self.GetTabWidth ()

    # *****************************************************
    # If we get an Return-Key on a line with only whitespace
    # *****************************************************
    if text.strip () == u'' :
      # *****************************************************
      # try to decrease the indentation
      # *****************************************************
      if indent > 0 :
        indent -= self.GetTabWidth ()
        for i in range ( self.GetTabWidth () ) :
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
          self.Execute_Code ()
          
    self.EnsureCaretVisible ()


  # *******************************************************
  # *******************************************************
  def On_Key_Down ( self, event ) :
    lineno = self.GetCurrentLine()

    #print 'Press',event.GetKeyCode()
    self.AUTO = None

    CTRL = event.ControlDown ()
    SHIFT = event.ShiftDown ()

    if self.CallTipActive():
      self.CallTipCancel()
    key = event.GetKeyCode()
    if ( key == 32 ) and CTRL :
      pos = self.GetCurrentPos()

      # Tips
      if SHIFT :
        self.CallTipSetBackground("yellow")
        self.CallTipShow(pos, 'lots of of text: blah, blah, blah\n\n'
                         'show some suff, maybe parameters..\n\n'
                         'fubar(param1, param2)')

    # Test for autocompletion:  'A..Z', 'a..z', '_', '.'
    elif ( key in range ( 65, 91  ) ) or \
         ( key in range ( 97, 123 ) ) or \
         ( key == 95 ) or \
         ( key == 46 ) :
      self.AUTO = key
      event.Skip()

    # *******************************************************
    # *******************************************************
    elif CTRL and  ( key in range ( ord('0'), ord ('9') ) ):
      if SHIFT :
        print ('Set BOOKMARK')
        self._Toggle_Bookmark ( lineno )
      else :
        print ('Goto BOOKMARK')

    # *******************************************************
    # Enter / Return, = Autoindent + code execution
    # *******************************************************
    elif key == wx.WXK_RETURN :
      if self.GetSelectedText () :
        self.CmdKeyExecute ( stc.STC_CMD_NEWLINE )
      else :
        self.Auto_Indent ()

    # *******************************************************
    # smart tab removal
    # *******************************************************
    elif key == wx.WXK_BACK :
      CurPos = self.GetCurrentPos ()
      TW = self.GetTabWidth()
      # test if there are enough spaces to remove
      if CurPos >= TW :
        text   = self.GetTextRange ( CurPos - TW, CurPos )
        if text.replace ( ' ', '') == '' :
          for i in text :
            self.CmdKeyExecute ( stc.STC_CMD_DELETEBACK )
          return
      # otherwise, normal handling of backspace
      event.Skip()

    # *******************************************************
    # BreakPoint information
    # *******************************************************
    elif key == wx.WXK_F5 :
      if SHIFT :
        self._Toggle_Bookmark ( lineno )
      else :
        self._BP_StateMachine ( lineno, CTRL )

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
    else:
      event.Skip()

  # *******************************************************
  # *******************************************************
  def OnCharAdd ( self, event ) :
    if self.AUTO :
      # show the autocompletion list, except if the character was a point
      # if it was a point, we need to allow updating first,
      # before popping up the new autocompletion list,
      # this will be done in the Update Event
      if self.AUTO != 46 :
        self.AUTO = None
        self.Show_AutoCompletion_List ( )
    else :
      self.AUTO = None
    event.Skip()

  # *******************************************************
  # *******************************************************
  def OnUpdateUI(self, evt):
    # In case of point insertion (due to a key press !!)
    # we need to show the autocompletion list here
    if self.AUTO and (self.AUTO == 46 ) :
      self.AUTO = None
      self.Show_AutoCompletion_List ( )

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
      self.GotoLine (linenr)
# ***********************************************************************


# ***********************************************************************
# demo program
# ***********************************************************************
class PythonSTC ( stc.StyledTextCtrl ):

  fold_symbols = 2

  def __init__(self, parent, ID = wx.ID_ANY,
               pos=wx.DefaultPosition, size=wx.DefaultSize,
               style=0):
    stc.StyledTextCtrl.__init__(self, parent, ID, pos, size, style)

    self.CmdKeyAssign(ord('B'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
    self.CmdKeyAssign(ord('N'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

    self.Current_Lexer = 0
    self.SetLexer ( stc.STC_LEX_PYTHON )
    self.SetKeyWords ( 0, " ".join(keyword.kwlist))

    #self.SetLexer ( stc.STC_LEX_SQL )
    #self.SetKeyWords ( 1, "aap beer")

    self.SetTabWidth(2)
    self.SetIndent(2)
    #self.SetIndentationGuides(True)

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

    # Setup a margin to hold fold markers
    #self.SetFoldFlags(16)  ###  WHAT IS THIS VALUE?  WHAT ARE THE OTHER FLAGS?  DOES IT MATTER?
    self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
    self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
    self.SetMarginSensitive(2, True)
    self.SetMarginWidth(2, 12)  # 2,3 does have something todo with for and background ??
    self.SetMarginWidth(0, 30)  # 0, symbol
    self.SetMarginWidth(1, 0)  # 1, linenumber
    # lijkt omgekeerd !!!!


    if self.fold_symbols == 0:
      # Arrow pointing right for contracted folders, arrow pointing down for expanded
      self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_ARROWDOWN, "black", "black")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_ARROW, "black", "black")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_EMPTY, "black", "black")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_EMPTY, "black", "black")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_EMPTY,     "white", "black")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY,     "white", "black")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY,     "white", "black")

    elif self.fold_symbols == 1:
      # Plus for contracted folders, minus for expanded
      self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_MINUS, "white", "black")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_PLUS,  "white", "black")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_EMPTY, "white", "black")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_EMPTY, "white", "black")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_EMPTY, "white", "black")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")

    elif self.fold_symbols == 2:
      # Like a flattened tree control using circular headers and curved joins
      self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_CIRCLEMINUS,          "white", "#404040")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_CIRCLEPLUS,           "white", "#404040")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,                "white", "#404040")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNERCURVE,         "white", "#404040")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_CIRCLEPLUSCONNECTED,  "white", "#404040")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "#404040")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNERCURVE,         "white", "#404040")

    elif self.fold_symbols == 3:
      # Like a flattened tree control using square headers
      self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_BOXMINUS,          "white", "#808080")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_BOXPLUS,           "white", "#808080")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,             "white", "#808080")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNER,           "white", "#808080")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_BOXPLUSCONNECTED,  "white", "#808080")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
      self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER,           "white", "#808080")



    # Make some styles,  The lexer defines what each style is used for, we
    # just have to define what each style looks like.  This set is adapted from
    # Scintilla sample property files.

    # Global default styles for all languages
    self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
    self.StyleClearAll()  # Reset all to be like the default

    # Global default styles for all languages
    self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
    self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,  "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
    self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
    self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
    self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")

    # Python styles
    # Default
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
    self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % faces)
    # Class name definition
    self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % faces)
    # Function or method name definition
    self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % faces)
    # Operators
    self.StyleSetSpec(stc.STC_P_OPERATOR, "bold,size:%(size)d" % faces)
    # Identifiers
    self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helv)s,size:%(size)d" % faces)
    # Comment-blocks
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
    self.AutoCompSetFillUps    ( '. '  )
    self.AutoCompSetIgnoreCase ( False )
    self.AutoCompSetAutoHide   ( True  )

    # *******************************************************
    self.Bind ( stc.EVT_STC_MARGINCLICK, self.OnMarginClick )
    self.Bind ( wx.EVT_KEY_DOWN,         self.On_Key_Down   )
    self.Bind ( stc.EVT_STC_CHARADDED,   self.OnCharAdd )
    self.Bind ( stc.EVT_STC_UPDATEUI,    self.OnUpdateUI )
    self.AUTO = None

    #stc.EVT_STC_KEY

  # *******************************************************
  # Create and show the autocompletion list
  # *******************************************************
  def Show_AutoCompletion_List ( self ) :
    # get current line, and position of caret in that line
    line, poskar = self.GetCurLine ()

    # test if caret at the end of a word
    import string
    if len ( line ) > ( poskar + 1 ) :
      End_Of_Word = line [ poskar ] in string.whitespace
    else :
      End_Of_Word = True

    if End_Of_Word:
      # get the complete word jsut before the caret
      line = line [ : poskar ].split()
      word = line [-1]

      # split the word, in case it contains prefixes with a '.'
      pre_word = None
      if word.find('.') >= 0 :
        word = word.split('.')
        pre_word = '.'.join ( word [ : -1 ] )
        word = word [-1]

      # Popup_AutoCompletion_List ( word, pre_word )
      # Only if we have a word or a pre_word !!
      wl = len ( word )
      if (( wl == 0 ) and not ( pre_word )) : return

      # in case of prefixes, get another list, which one ??
      if pre_word :
        kw = dir ( __name__ )
        #kw = dir ( __builtins__ )
        #kw = dir ( pre_word )
      else :
        kw = keyword.kwlist [ : ]
      #print 'WORD,PRE',word,'//',pre_word,'//',line,wl,self.AutoCompActive()

      # limit the list to matches of the already known part of the word
      if word == '' :
        newlist = kw
      else :
        newlist = []
        for item in kw:
          if item.find ( word ) == 0:
            newlist.append (item)

      newlist.sort ()
      self.AutoCompShow ( wl, ' '.join ( newlist ) )
      #self.AutoCompActive()
      #self.AutoCompCancel()
  # *******************************************************



  # *******************************************************
  # *******************************************************
  def On_Key_Down (self, event ) :
    #print 'Press',event.GetKeyCode()
    self.AUTO = None
    
    if self.CallTipActive():
      self.CallTipCancel()
    key = event.GetKeyCode()
    if key == 32 and event.ControlDown():
      pos = self.GetCurrentPos()

      # Tips
      if event.ShiftDown():
        self.CallTipSetBackground("yellow")
        self.CallTipShow(pos, 'lots of of text: blah, blah, blah\n\n'
                         'show some suff, maybe parameters..\n\n'
                         'fubar(param1, param2)')

    # Test for autocompletion:  'A..Z', 'a..z', '_', '.'
    elif ( key in range ( 65, 91  ) ) or \
         ( key in range ( 97, 123 ) ) or \
         ( key == 95 ) or \
         ( key == 46 ) :
      self.AUTO = key
      event.Skip()

    # toggle lexer and keywords
    # TODO:
    #   through a tupple
    #   other completion list
    elif key == wx.WXK_F6 :
      self.Current_Lexer += 1
      self.Current_Lexer %= 2
      print ('F6', self.Current_Lexer)
      
      if self.Current_Lexer == 0 :
        self.SetLexer ( stc.STC_LEX_PYTHON )
        self.SetKeyWords ( 0, " ".join(keyword.kwlist))
        # set color of margin
        self.StyleSetBackground ( 33, '#A0A0A0' )

      elif self.Current_Lexer == 1 :
        self.SetLexer ( stc.STC_LEX_SQL )
        self.SetKeyWords ( 0, "aap beer")
        self.StyleSetBackground ( 33, '#AA00AA' )

      # refresh the complete rendering
      self.Colourise ( 0, -1 )
    else:
      event.Skip()

  # *******************************************************
  # *******************************************************
  def OnCharAdd ( self, event ) :
    if self.AUTO :
      # show the autocompletion list, except if the character was a point
      # if it was a point, we need to allow updating first,
      # before popping up the new autocompletion list,
      # this will be done in the Update Event
      if self.AUTO != 46 :
        self.AUTO = None
        self.Show_AutoCompletion_List ( )
    else :
      self.AUTO = None
    event.Skip()

  # *******************************************************
  # *******************************************************
  def OnUpdateUI(self, evt):
    # In case of point insertion (due to a key press !!)
    # we need to show the autocompletion list here
    if self.AUTO and (self.AUTO == 46 ) :
      self.AUTO = None
      self.Show_AutoCompletion_List ( )

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
  def OnMarginClick(self, evt):
    # fold and unfold as needed
    if evt.GetMargin() == 2:
      if evt.GetShift() and evt.GetControl():
        self.FoldAll()
      else:
        lineClicked = self.LineFromPosition(evt.GetPosition())

        if self.GetFoldLevel(lineClicked) & stc.STC_FOLDLEVELHEADERFLAG:
          if evt.GetShift():
            self.SetFoldExpanded(lineClicked, True)
            self.Expand(lineClicked, True, True, 1)
          elif evt.GetControl():
            if self.GetFoldExpanded(lineClicked):
              self.SetFoldExpanded(lineClicked, False)
              self.Expand(lineClicked, False, True, 0)
            else:
              self.SetFoldExpanded(lineClicked, True)
              self.Expand(lineClicked, True, True, 100)
          else:
            self.ToggleFold(lineClicked)

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
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class my_Test_Form ( wx.MiniFrame ) :

  # *****************************************************************
  # *****************************************************************
  def __init__( self, main_form= None, ini = None ) :

    self.main_form = main_form
    FormStyle = wx.DEFAULT_FRAME_STYLE

    Pos  = ( 100, 100 )
    Size = ( 600, 400 )
    self.Ini_File    = ini
    self.Ini_Section = 'Test Form'
    if ini :
      ini.Section = self.Ini_Section
      Pos  = ini.Read ( 'Pos',  Pos )
      Size = ini.Read ( 'Size', Size )

    wx.MiniFrame.__init__ (
        self, None, -1,
        'PyLab_Works  Scintilla Test',
        size  = Size,
        pos   = Pos,
        style = FormStyle )

    GUI = """
    self.SplitV2               ,PanelVer, 01
      panel                    ,wx.Panel
        Button_1               ,wx.Button , label = "Test", size = ( 40, -1 )
      self.Edit                ,Base_STC
    """
    exec ( Create_wxGUI ( GUI ) )

    # Allow BreakPoints Margin
    self.Edit.Margin_On ( 2 )

    self.Bind ( wx.EVT_CLOSE, self.On_Close )

    # we create the debugger here
    self.Current_Line = None
    self.Main_File = '../PyLab_Works/test_IDE.py'
    #self.Debugger = PW_PDB ( self, self.Set_Debug_Status )
    self.Load_Editor ( self.Main_File )
    
  # *********************************************************
  # *********************************************************
  def On_Close ( self, event ) :
    #self.Debugger.Stop_Debug_Application()

    ini = self.Ini_File
    if ini :
      ini.Section = self.Ini_Section
      ini.Write ( 'Pos',  self.GetPosition () )
      ini.Write ( 'Size', self.GetSize () )

    self.Destroy()

  # *********************************************************
  # *********************************************************
  def Load_Editor ( self, filename, lineno = -1 ) :
    print ('****** Load', lineno, filename)
    lineno -= 1
    pass
  
    # STRANGE STRANGE
    filename = filename.lower()  # ????

    # check if file already open in an editor
    if not ( self.Edit.Filename ) :
      # if not open yet, open it now
      filnams = path_split ( filename )
      filnam  = os.path.splitext ( filnams [1] ) [0]
      print ('## Load: '+ filnam + ',  '  +filnams [0] + '\n')

      self.All_BreakPoints = self.Edit.LoadFile ( filename )
      #self.Debugger.Set_Breakpoint_List ( self.All_BreakPoints )

    """
    # Set Marker on Current Line
    self.Current_Line = [ filename, lineno, Edit[0].MarkerGet ( lineno ), -1 ]

    # if a breakpoint, determine the BreakPoint List entry
    Scite_ID = None
    if ( self.Current_Line [2] & Edit[0].Break_Mask ) > 0 :
      BPL = self.All_BreakPoints
      BP_Files = BPL.keys()
      for file in BP_Files :
        if file == filename :
          BP_File  = BPL [ file ]
          BP_Lines = BP_File.keys()
          # now the line might be moved,
          # but by quering the Scite_ID we must find the current line
          for line in BP_Lines :
            Scite_ID = BP_File [ line ][3]
            if lineno == Edit[0].MarkerLineFromHandle ( Scite_ID ) :
              break
          break


    ##print '***&&&',self.Current_Line
    Edit[0].MarkerDelete ( lineno, -1 )
    Edit[0].MarkerAddSet ( lineno, self.Current_Line [2] & ~Edit[0].Break_Mask )
    if ( self.Current_Line [2] & Edit[0].Break_Mask ) > 0 :
      A = Edit[0].MarkerAddSet ( lineno, self.Current_Line [2] & 0x7800 )
    else :
      A = Edit[0].MarkerAdd ( lineno, 10 )
    New_Scite_ID = Edit[0].MarkerAdd   ( lineno, 15 )

    # store the new Scite_ID in the breakpoint list
    if Scite_ID :
      BPL [ file ] [ line ] [ 3 ] = New_Scite_ID

    self.Current_Line [3] = Scite_ID
    print '***************************',A, Scite_ID

    Edit[0].EnsureVisibleEnforcePolicy ( lineno )
    Edit[0].GotoLine ( lineno )

    # Select the correct Edit Page
    for i in range ( self.NB.GetPageCount() ) :
      if self.NB.GetPageText (i) == Edit[1] :
        self.NB.SetSelection (i)
        #self.Current_Line [3] = i
        #self.NB.SetPageImage ( self.Current_Line [3], 83 )
        self.NB.SetPageImage ( i, 83 )
        break;

    # Enable all editors
    for Edit in self.Editors :
      Edit[0].SetReadOnly ( False )
    self.Log_Cmd.SetFocus ()
    """
    

# ***********************************************************************


# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':
  # starts a wait period of 5 minutes, for a winpdb to attach
  # import rpdb2; rpdb2.start_embedded_debugger('aap')

  app = wx.PySimpleApp ()
  ini = inifile ( os.path.join (os.getcwd(), 'Scintilla.cfg' ))
  ini.Section = 'Scintilla Test'

  # Create the scope form and show it
  Main_Form = my_Test_Form ( None, ini )
  Main_Form.Show()

  app.MainLoop ()

  # The inifile can be used by more forms, so we close it here
  ini.Close ()
# ***********************************************************************

pd_Module ( __file__ )
