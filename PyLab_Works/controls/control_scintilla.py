import __init__
from base_control import *

import sys
import os

import PyLab_Works_Globals as PG
from   PyLab_Works_Globals import *
from   PyLab_Works_Globals import _
import wx
import wx.stc  as  stc
import customtreectrl_SM as CT
#from   Scintilla_Python import *
#for path in sys.path :
#  print '  ', path
from   Scintilla_support import *
from   gui_support      import Create_wxGUI


from file_support import *
from array_support import class_MetaData


# ***********************************************************************
# ***********************************************************************
class tScintilla_Editor_Base ( object ):
  #def __init__ ( self, *args, **kwargs ):
  def __init__ ( self,  Dock,        # the frame/panel/... where we can put
                                     # the GUI controls that will catch events
                 Brick = None,       # the Brick, with its inputs and outputs
                 Ini   = None,       # inifile to store and reload settings
                 Test  = False,      # if True, testmode with buildin examples
                 Name  = 'MyName' ): # so we can use it directly in a NoteBook

    self.TopFrame = wx.GetTopLevelParent ( Dock )
    self.Dock  = Dock
    self.Brick = Brick
    self.Test  = Test
    self.Ini   = Ini

    GUI = """
      self.STC  ,Base_STC
    """
    self.wxGUI = Create_wxGUI ( GUI, my_parent = 'self.Dock' )

    self.STC.My_Control = self
    self.STC.Execute_Code = self.Execute_Code

    self.STC.Bind ( wx.EVT_KEY_DOWN,      self.On_KeyPress )
    self.STC.Bind ( stc.EVT_STC_MODIFIED, self.On_Modified )

    from Scintilla_Templates import EVT_SCINTILLA_TEMPLATE_INSERT
    self.TopFrame.Bind ( EVT_SCINTILLA_TEMPLATE_INSERT, self.On_TemplateInsert)

    # we want a StatusBar Field
    self.My_StatusBar_Field = len ( self.TopFrame.StatusBar_Controls )
    self.TopFrame.StatusBar_Controls.append ( self )

  # ********************************************************
  # ********************************************************
  def Get_FileName ( self ) :
    return self.STC.Filename

  # ********************************************************
  # ********************************************************
  def GetName ( self ) :
    return self.Name

  # ********************************************************
  # ********************************************************
  def Execute_Code ( self, Key, Force_Modified = False ) :
    """
Normally the code will only be executed if the code in
the editor has been modified by the user.
After loading another file, the modify flag is not set,
in that case you can force the execution by
setting Force_Modified to True.
"""

    if ( self.STC.GetModify () and ( Key != wx.WXK_RETURN )) or\
       Force_Modified :
      self.Brick.Par [ self.EP[0] ] = [ self.STC.GetText         (),
                                        self.STC.GetSelectedText (),
                                        self.STC.Get_Last_Lines  () ]
      # reset modify flag
      self.STC.SaveFile ( self.STC.Filename )
      #self.Brick.Par [ self.EP[1] ] ['FileName'] = self.STC.Filename
      #v3print ( 'saap',self.Brick.Par,self.EP )
      #self.Brick.Par [ self.EP[1] ].'FileName' = self.STC.Filename
      self.On_Modified ()

      key = 'CMD_Shell'
      if key in self.Brick.Par [ self.EP[1] ] :
        self.STC.Local_Browser = self.Brick.Par [ self.EP[1] ] [ key ].Html

  # ********************************************************
  # ********************************************************
  def On_KeyPress ( self, event ) :
    if event.GetKeyCode() == wx.WXK_F9 :
      self.Execute_Code ( wx.WXK_F9 )
    else :
      # let the orginal process do it's work !!
      event.Skip() # needed to perform collapse / expand !!

  # ********************************************************
  # ********************************************************
  def On_Modified ( self, event = None ) :
    if self.STC.GetModify () :
      self.TopFrame.StatusBar.SetStatusText( 'CE modified', self.My_StatusBar_Field )
    else :
      self.TopFrame.StatusBar.SetStatusText( 'Code Editor', self.My_StatusBar_Field )

  # ********************************************************
  # ********************************************************
  def On_TemplateInsert ( self, event ) :
    #print '********** $$$$$$$$$$ #######'
    off = self.STC.GetCurLine()[1] * ' '
    L = self.STC.LineFromPosition ( self.STC.GetCurrentPos () )
    offset = ''
    for line in event.data.split('\n') :
      print (L,offset + line)
      self.STC.InsertText(-1, offset + line + '\n')
      offset = off
      L += 1
      self.STC.GotoLine ( L )

  # ********************************************************
  # ********************************************************
  def Save_Settings ( self, ini, key = None ) :
    #v3print ( 'SAVE SCINTE')
    if ( 'Load_Save' in Debug_What ) :
      Debug_Dump_Trace (
        'tScintilla_Editor ( My_Control_Class ) Save Settings to :', ini )

    if ini :
      # *********************************************
      # Save the content of the CMD-Shell into a file
      # *********************************************
      #from file_support import Force_Dir
      path = os.path.join ( Application.Dir, PG.Active_Project_Filename )
      path = os.path.normpath ( path)
      Force_Dir ( path, init = True )

      filename = None
      if not ( self.STC.Filename ) or \
         ( self.STC.Filename == 'Temp.Temp' ) :
        from dialog_support import Ask_File_For_Save, FT_PY_FILES
        filename = Ask_File_For_Save (
          DefaultLocation = path,
          DefaultFile = 'new.py',
          FileTypes = FT_PY_FILES,
          Title = 'Save Code as ...' )
        if filename :
          self.STC.SaveFile ( filename )
      else :
        self.STC.SaveFile ( self.STC.Filename )
      #v3print ( 'Scintilla Filename', self.STC.Filename )
      """
# create the ojects and initialize them
def init ():
  #import visual
  self.ball    = visual.sphere(radius=2)
  self.ball.x  = 0
  self.ball.y  = 150
  self.ball.vx = 1
  self.ball.vy = 0

# simulation that runs continuously
#import visual
ball = self.ball
dt   = 0.1

ball.x   = ball.x + ball.vx * dt
ball.vx *= 0.997

ball.y   = ball.y - ball.vy * dt
if ( ball.y <= 0 ) and ( ball.vy > 0 ) :
  ball.vy = -0.8 * ball.vy
  ball.y  = 0
else :
  ball.vy = ball.vy + 9.8 * dt


      """
      # *********************************************
      # Store other settings in inifile
      # *********************************************
      filename = Get_Rel_Path ( self.STC.Filename )
      if not ( key ) :
        key = 'CS_Code_File'
      #ini.Write ( key , filename )
      ini.Write ( key + '1' , filename )
      try :
        line = []
        # try to store position and size of templates
        x,y = self.STC.Templates_Form.GetPosition()
        line.append(x)
        line.append(y)
        x,y = self.STC.Templates_Form.GetSize()
        line.append(x)
        line.append(y)
      except :
        line = ''
      if line :
        ini.Write ( key + '2', line )

  # ********************************************************
  # ********************************************************
  def Load_Settings ( self, ini, key = None) :
    """
    line = ini.Read ( 'CS_', '' )
    self.Brick.Params[1] = line
    if line :
      #print 'UUYYTT',line,type(line)
      self.STC.SetText ( line )
      # reset modify flag
      self.STC.SaveFile ( 'Temp.Temp' )
      self.On_Modified ()
    """

    if not ( key ) :
      key = 'CS_Code_File'

    # *********************************************
    # read the Code file
    # *********************************************
    filename = ini.Read ( key + '1', None )
    #v3print ( 'UUUUUUUUUU',key, filename )

    # ToDo ....
    line = ini.Read ( key + '2', '' )
    if line :
      pass

    if ( 'Load_Save' in Debug_What ) :
      Debug_Dump_Trace (
        'tScintilla_Editor ( My_Control_Class ) Load Settings',
        '\ninifile  =', ini,
        '\nline     =', line,
        '\nfilename =', filename )

    if filename :
      filename = Get_Abs_Path ( filename )
      self.STC.LoadFile ( filename )
      #print 'PPPYGGY',self.EP, self.Brick.Par
      """
      if self.EP[0] :
        self.Brick.Par [ self.EP[0] ] = self.STC.GetText ()
      if self.EP[1] :
        print 'yyudg',type(self.EP[1]),type(self.Brick.Par[2])
        self.Brick.Par [ self.EP[1] ]['FileName'] = filename
      """
      self.P[0] = self.STC.GetText ()
      #self.P[1]['FileName'] = filename
      if self.EP[1] :
        #print 'yyudg',type(self.Brick.Par[2])
        self.Brick.Par [ self.EP[1] ]['FileName'] = filename
      self.On_Modified ()


# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
#class t_C_Code_Editor ( My_Control_Class, tScintilla_Editor_Base ):
class t_C_Code_Editor ( tScintilla_Editor_Base, My_Control_Class ):
  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    # Add an extra Dictionair to the Par
    self._EP_Add ( True )
    #for item in self.Brick.Par :
    #  print ' AAAA',type(item)

    #for item in self.EP :
    #  print ' 77AAAA',type(item)

    tScintilla_Editor_Base.__init__ ( self, *args, **kwargs )

    #for item in self.EP :
    #  print ' 77BBBBB',type(item)

  #def Save_Settings ( self, ini, key ) :
  #  print 'DUMMY SCITE'
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
#class t_C_MultiTab_Editor ( My_Control_Class, tScintilla_Editor_Base ):
class t_C_MultiTab_Editor ( tScintilla_Editor_Base, My_Control_Class ):
  def __init__ ( self, *args, **kwargs ):
    My_Control_Class.__init__ ( self, *args, **kwargs )

    tScintilla_Editor_Base.__init__ ( self, *args, **kwargs )

    # Add an extra Dictionair to the Par
    self._EP_Add ( True )
    
# ***********************************************************************



# add some standard library paths
"""
import sys
subdirs = [ '../support' ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
"""
#from   picture_support import Get_Image_List_16
from   picture_support import Get_Image_16


def sprint ( dic, text='' ) :
  print ('*******************',text)
  i = 0
  for key in dic :
    print (i,str(dic[key])[:80])
    if type ( dic[key] ) == dict :
      for k in dic[key] :
        if k == 'IndexError' :
          break
        print (' ..  ', k, '=', str(dic[key][k])[:80])
    i += 1
    #if i >10 :
    #  break
  print

# ***********************************************************************
# ***********************************************************************
from signal_workbench import *
import signal_workbench
"""
class tSignal_WorkBench ( object ) :
  def __init__ ( self,  Dock,     # the frame/panel/... where we can put
                                  # the GUI controls that will catch events
                 Brick = None,    # the Brick, with its inputs and outputs
                 ini   = None,    # inifile to store and reload settings
                 Test  = False ): # if True, testmode with buildin examples
"""
class t_C_Signal_WorkBench ( My_Control_Class ) :
  def __init__ ( self, *args, **kwargs ):

    My_Control_Class.__init__ ( self, *args, **kwargs )

    """
    Frame = Dock
    while not ( isinstance ( Frame, wx.Frame )) :
      Frame = Frame.GetParent()

    self.Dock = Dock
    self.Frame = Frame
    self.Brick = Brick
    self.Test  = Test
    self.Ini   = ini
    if Brick :
      self.IniSection = 'Device ' + Brick.Name
    else :
      self.IniSection = 'Device Scintilla'
    """
    #BECAUSE BELOW ARE THE INPUT VALUES USED
    Dock = self.Dock
    self.Frame = Frame = self.TopFrame
    Brick = self.Brick
    Test = self.Test
    ini = self.Ini


    # *****************************************************************
    # Create the GUI
    # *****************************************************************
    GUI = """
    self.SplitV            ,SplitterVer
      self.Split           ,SplitterHor
        self.Tree          ,Custom_TreeCtrl_Base
        self.NB            ,wx.Notebook
          p1               ,wx.Panel, name = "Scope"
            self.Editor    ,tScintilla_Editor_Base ,Brick=Brick, Ini=ini, Test=Test
          p2               ,wx.Panel, name = "Test"
      self.Error           ,PanelVer
        self.Log           ,wx.TextCtrl, style = wx.TE_MULTILINE
    """
    self.wxGUI = Create_wxGUI ( GUI, IniName = 'self.Ini', my_parent = 'Dock' )
    # *****************************************************************


    # *************************************************************
    Set_NoteBook_Images ( self.NB, ( 47, 76 ) )
    # *****************************************************************


    # *****************************************************************
    # Take over the Output and Error logging
    # *****************************************************************
    PG.Set_StdOut ( self.Log )
    PG.Set_StdErr ( self.Log )

    # *************************************************************
    # Tree initialization
    # *************************************************************
    self.Tree.On_Icon_Click = self.On_Icon_Click
    self.Tree.Bind ( CT.EVT_TREE_SEL_CHANGING, self.On_Changing )
    self.Tree.Bind ( CT.EVT_TREE_SEL_CHANGED,  self.On_Changed )


    self.Tree.Bind ( wx.EVT_KEY_DOWN,      self.On_Key_Press )
    self.Editor.STC.Bind ( wx.EVT_KEY_DOWN,      self.On_Key_Press )

    self.Frame.Bind ( CT.EVT_TREE_BEGIN_DRAG, self.OnBeginDrag )
    self.Tree.Bind  ( CT.EVT_TREE_END_DRAG,   self.OnEndDrag   )
    self.Frame.Bind ( wx.EVT_CLOSE,           self.OnClose     )

    # We don't need to bind the Close event,
    # because the parent will call "Notify_Closed"

  # *****************************************************************
  # *****************************************************************
  def OnClose ( self, event ) :
    PG.Restore_StdOut ( self.Log )
    PG.Restore_StdErr ( self.Log )


    nodename = self.Tree.GetItemText ( self.Tree.GetSelection () )
    if self.Editor.STC.GetModify() :
      self.Save_Editor ( nodename )

    # Save component settings
    self.Ini.Section = self.IniSection
    self.wxGUI.Save_Settings ()

    event.Skip ()

  # *****************************************************************
  # You can block the start of a drag event
  # *****************************************************************
  def OnBeginDrag ( self, event ) :
    #event.Veto()
    pass

  # *****************************************************************
  # You can block the end of a drag event
  # NOTE: the binding must be "self.Tree.Bind"
  # *****************************************************************
  def OnEndDrag ( self, event ) :
    event.Skip()


  # *************************************************************
  # RECURSION !!
  # *************************************************************
  def Run_Script ( self, node, recursive ) :
    from control_scope_base import tScope_Display_Light

    nodename = self.Tree.GetItemText ( node )
    print ('************  RUN SCRIPT    ' + nodename)

    self.tree_globs [ 'DISPLAY'        ] = None   # Signals
    self.tree_globs [ 'Display_Params' ] = None   # Signal Parameters
    self.tree_globs [ 'Display_Title'  ] = None   # Window Caption
    self.tree_globs [ 'Auto'           ] = True   # AutoScale

    filename = self.Get_Editor_Filename ( nodename )
    execfile ( filename, self.tree_globs )

    # Update Display if output and display is On
    Display_On = ( self.Tree.GetItemImage ( node ) == 78 )
    Display_Data   = self.tree_globs [ 'DISPLAY'        ]
    Display_Params = self.tree_globs [ 'Display_Params' ]
    Display_Title  = self.tree_globs [ 'Display_Title'  ]

    if Display_On and ( Display_Data != None ) :
      PyData = self.Tree.GetPyData ( node )
      if len ( PyData ) < 4 :
        PyData.append ( tScope_Display_Light ( self, node ) )
        self.Tree.SetPyData ( node, PyData )

      # Create a list of MetaData
      MetaData = []
      for par in Display_Params :
        Signal_Attr = class_MetaData ()
        Signal_Attr.SignalName = par.pop(0)
        if len (par) >= 2 :
          bottom = par.pop(0)
          top    = par.pop(0)
          Signal_Attr.DisplayRange = ( bottom, top )
        MetaData.append ( Signal_Attr )

      #PyData[3].Scope.Add_Data ( Display_Data, Display_Params, Display_Title )
      PyData[3].Scope.Add_Data ( Display_Data, MetaData )


    # process children through recursion
    if recursive and self.Tree.HasChildren ( node ) :
      item, cookie = self.Tree.GetFirstChild ( node )
      while item :
        self.Run_Script ( item, recursive )
        item = self.Tree.GetNextSibling ( item )

  # *************************************************************
  # if a display is closed, remove from treenode.pydata
  # *************************************************************
  def Notify_Closed ( self, node ) :
    # restore standard output and error loggers
    PG.Restore_StdOut ( self.Log )
    PG.Restore_StdErr ( self.Log )

    try :
      PyData = self.Tree.GetPyData ( node )
      if len ( PyData ) > 3 :
        display_form = PyData.pop()
        self.Tree.GetPyData ( node, PyData )
    except :
      pass

  # *************************************************************
  # *************************************************************
  def On_Key_Press (self, event ) :
    if event.GetKeyCode() == wx.WXK_F9 :
      #print event.ShiftDown ()
      #print dir(event)

      # save last editor window if modified
      nodename = self.Tree.GetItemText ( self.Tree.GetSelection () )
      if self.Editor.STC.GetModify() :
        self.Save_Editor ( nodename )

      # create the namespace for the simulation
      # but leave it untouched if it's already created and filled
      try :
        test = self.tree_globs
      except :
        self.tree_globs = {}

      node = self.Tree.GetSelection ()
      recursive = event.ShiftDown ()
      self.Run_Script ( node, recursive )

    else :
      event.Skip ()

  # *************************************************************
  # *************************************************************
  def Get_Editor_Filename ( self, nodename ):
    path = path_split ( PG.Active_Project_Filename )[0]
    path = os.path.join ( path, 'Signal_WorkBench' )
    return os.path.join ( path, nodename + '.py' )

  # *************************************************************
  # *************************************************************
  def Save_Editor ( self, filename ) :
    path = path_split ( PG.Active_Project_Filename )[0]
    path = os.path.join ( path, 'Signal_WorkBench' )
    if self.Editor.STC.GetModify() :
      filename = os.path.join ( path, filename + '.py' )
      print ('    Save', filename)
      if not( File_Exists ( path ) ) :
        os.makedirs ( path )
      self.Editor.STC.SaveFile ( filename )
      # for some strange reason, On_Modify is not called from here
      # doesn't exists: self.Editor.STC.SetModify ( False )
      # So we call On_Modify our selfs
      self.Editor.On_Modified ()

  # *************************************************************
  # *************************************************************
  def On_Changing ( self, event ) :
    # after a drag operation, there's no GetOldItem !!
    try:
      filename = self.Tree.GetItemText ( event.GetOldItem () )
      self.Save_Editor ( filename )
    except :
      pass

    #path = path_split ( PG.Active_Project_Filename )[0]
    #path = os.path.join ( path, 'Signal_WorkBench' )
    #filename = self.Tree.GetItemText ( event.GetItem () )
    #filename = os.path.join ( path, filename + '.py' )
    filename = self.Get_Editor_Filename ( self.Tree.GetItemText ( event.GetItem () ))
    if File_Exists ( filename ) :
      #print '   Load', filename
      self.Editor.STC.LoadFile ( filename )
    else :
      #print '   Clear'
      self.Editor.STC.ClearAll ()

    # Because the above actions will fire a modify event
    # which is not correct, we correct this in the On_Changed event

    #self.Editor.STC.SetSavePoint()  # prevent modify event, doesn't work
    #event.Skip ()

  # *************************************************************
  # Be sure the statusbar is displayed correctly after load/clear
  # *************************************************************
  def On_Changed ( self, event ) :
    self.Editor.On_Modified ( event )

  # *************************************************************
  # *************************************************************
  def On_Icon_Click ( self, item ) :
    PyData = self.Tree.GetPyData ( item )
    Display_On = ( PyData[1] == 78 )
    if Display_On :
      PyData[1] = 79
    else :
      PyData[1] = 78
    PyData[2] = PyData[1]
    self.Tree.SetPyData    ( item, PyData )
    self.Tree.SetItemImage ( item, int(PyData[1]), CT.TreeItemIcon_Normal )
    self.Tree.SetItemImage ( item, int(PyData[2]), CT.TreeItemIcon_Expanded )


  # *************************************************************
  # *************************************************************
  def Test22 ( self, event ) :
    #print 'Test22'
    event.Skip()

  # *************************************************************
  # RECURSION !!
  # *************************************************************
  def Remove_Dynamical_Refs ( self, node ) :
    try :
      PyData = self.Tree.GetPyData ( node )
      if len ( PyData ) > 3 :
        while len ( PyData ) > 3 :
          display_form = PyData.pop()
          display_form.Close ( True )
          display_form.Destroy()
        self.Tree.GetPyData ( node, PyData )
    except :
      pass

    if self.Tree.HasChildren ( node ) :
      item, cookie = self.Tree.GetFirstChild ( node )
      while item :
        self.Remove_Dynamical_Refs ( item )
        item = self.Tree.GetNextSibling ( item )

  # *************************************************************
  # *************************************************************
  def Save_Settings ( self, ini, key = None ) :
    if ini :
      fne, fe = os.path.splitext ( ini.filename )
      filename = fne + '_' + self.Brick.Name + fe
      print ('WRITE-TREE',filename)
      self.Remove_Dynamical_Refs ( self.Tree.GetRootItem() )
      self.Tree.Tree_2_IniFile ( filename )

  # *************************************************************
  # *************************************************************
  def Load_Settings ( self, ini, key = None ) :
    if ini :
      fne, fe = os.path.splitext ( ini.filename )
      filename = fne + '_' + self.Brick.Name + fe
      print ('READ-TREE',filename)
      self.Tree.IniFile_2_Tree ( filename )

# ***********************************************************************



