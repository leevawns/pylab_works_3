import __init__

# ***********************************************************************
__doc__ = """
# Supports Internationalization
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007 .. 2008 Stef Mientki
# mailto:S.Mientki@ru.nl
"""
# ***********************************************************************


# ***********************************************************************
_Version_Text = [

[ 1.2 , '17-11-2008', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- now language support also works when Create_wxGUI is used
""" ] ,

[ 1.1 , '18-10-2008', 'Stef Mientki',
'Test Conditions:', (2,),
"""
- improved import of language files
""" ] ,

[ 1.0 , '28-01-2008', 'Stef Mientki',
'Test Conditions:', (1,),
' - orginal release' ]
]
# ***********************************************************************



# 'US' is the default, so we don't need it here
#Language_This_Module = 'US'     # the language used in this file

import os
import sys
import wx

from path_support import *
from General_Globals import *

#add vietnames language
Language_IDs = [ 'NL', 'RO', 'US','VI']

# TO PREVENT PROBLEMS WITH GLOBALITY, WE USE A LIST INSTEAD OF A STRING!!
Language_Current = ['US']
#global Language_Current

_LT = {}
_LT_missing = []
_LT_Errors  = []


No_Language_File = 'No Translation Found\n'


# ***********************************************************************
# The first time the flag " First_Time" should be set to true,
# to prevent the user warning
# ***********************************************************************
def Set_Language ( New_Language,  First_Time = False ) :
  #***********************************************
  from dialog_support import AskYesNo,Show_Message
  #***********************************************
  if New_Language in Language_IDs :
    global Language_Current
    Language_Current [0] = New_Language

    # find from which file this function is called
    SourceFile = sys._getframe (1).f_code.co_filename
    # Ignore gui_support
    if 'gui_support.py' in SourceFile :
      SourceFile = sys._getframe (2).f_code.co_filename
    #print('New Language =', New_Language, ' Set from :', os.path.normpath ( SourceFile ))
    if not ( First_Time ):
      Title   = _(1, 'Change the language:' )
      Message = _(2, 'Language Setting has been changed,\n' +
                     'Only after a restart of the application\n' +
                     'All (available) translations will become active.\n\n' +
                     'Restart Now ?' )
      if AskYesNo ( Message, Title ) :
        Application.Restart = True
        #wx.GetApp().GetTopWindow().Close ()

  else :
    Show_Message ( 'Language  "' + New_Language + '"  not supported')
  #print ' Set Current Language = ', Language_Current
# ***********************************************************************


# ***********************************************************************
# The Function that does the translation
# ***********************************************************************
def _(ID, text ):
  LC = Language_Current[0]
  
  # if string has no ID
  ##   print '___',ID,text, Language_Current
  if ID == 0 :
    #log ( ID, text, 'ID = 0')
    return text

  # find from which file this function is called
  SourceFile = sys._getframe(1).f_code.co_filename
  # Get the file from which this procedure was called
  Frame = 1
  while SourceFile == '<string>' :
    print ('FRAME UP +++', text)
    Frame += 1
    SourceFile = sys._getframe( Frame ).f_code.co_filename

  # ignore gui_support
  if 'gui_support.py' in SourceFile :
    print("gui support")
    Frame += 1
    SourceFile = sys._getframe( Frame ).f_code.co_filename

  Path, File = path_split ( SourceFile )
  FileName = os.path.splitext (File) [0]

  # if in missing list
  if FileName in _LT_missing :
    print('_______MISSING',ID,FileName,SourceFile)
    return text

  # if selected language is identical to module language
  Language_This_Module = 'US'
  ## print 'Language / Module-Language =', LC, Language_This_Module
  if LC == Language_This_Module :
    return text

  # if not yet in dictionary
  if not ( FileName in _LT) :
    # if language file doesn't exist, return
    from file_support   import File_Exists
    Lang_Path = os.path.join ( Path, 'lang')
    Lang_File = os.path.join ( Lang_Path, FileName + '_' + LC + '.py')
    if not ( File_Exists ( Lang_File ) ) :
      _LT_missing.append ( FileName )
      print ('_______MISSING LANGUAGE FILE ',ID,Lang_File)
      return text
    # be sure the path is in the Python path
    if not ( Lang_Path in sys.path ) :
      sys.path.append ( Lang_Path )
    # import the language file
    try :
      exec( "from " + FileName + "_" + LC + " import LT",globals())
      try :
        _LT [ FileName ] = LT
      except Exception as e:
        _LT_missing.append ( FileName )
        log ( ID, text, 'Can\'t find "LT"')

    # if import of language file failed
    except Exception as e:
      _LT_missing.append ( FileName )
      print('Can\'t find language file')
      log ( ID, text, 'Can\'t find language file')


  # here the language table of this file is added to the dictionary
  # or the file is added to the missing list
  if FileName in _LT_missing :
    #print ' Missing Translation File:', FileName + '_' + LC
    return text
  else:
    try :
      #print '************** 333',ID,text
      return _LT [ FileName ] [ ID ]
    except :
      print 
      print ('**************, not found')
      log ( ID, text, 'ID not found')
      return text

  ##print sys._getframe().f_code.co_name    # me, i.e. "_"
  ##print sys._getframe(1).f_code.co_name    # my caller
  ##print sys._getframe(1).f_code.co_filename  # my callers filename
  return 'piep, the program shouldn''t come here'


# ***********************************************************************
# NO MORE LOGGING FOR THE MOMENT
# ***********************************************************************
def log ( ID, text, message ) :
  line = str(ID) + '\t' + text
  if not ( line  in _LT_Errors ) :
    _LT_Errors.append ( line )
    # find from which file this function is called
    SourceFile = sys._getframe(2).f_code.co_filename
    Path, File = path_split ( SourceFile )
    FileName = os.path.splitext (File) [0]

    # \r\n gives problems when appending ??
    line = Language_Current[0] + '\t' + FileName + '\t' + \
           message + '\t' + line + '\n'
    _LT_Log.write ( line )
    _LT_Log.flush ()
    #_LT_Log.close ()
    #print 'ERROR:',line
# ***********************************************************************

# ***********************************************************************
# Finalization, doesn't work reliable
# ***********************************************************************
def _Close_Log () :
  #print('CLOSE LANGUAGE LOG FILE')
  _LT_Log.close ()
# ***********************************************************************

# ***********************************************************************
# Initialization
# ***********************************************************************
_LT_Log = open ('language_support_error_log.txt', 'a')
import atexit
atexit.register ( _Close_Log )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Flag_Object ( object ) :
  def __init__ ( self ) :
    from wx.lib.art import flagart, img2pyartprov
    self.FlagArtProvider = img2pyartprov.Img2PyArtProvider(flagart,artIdPrefix='wx.ART_')
    wx.ArtProvider.Push ( self.FlagArtProvider )

  def Get_Flag ( self, Language_ID, size = ( 20, 14 ) ) :
    print("Language_ID = ", Language_ID)
    bmp_Flag = wx.ArtProvider.GetBitmap (
                 'wx.ART_'+ Language_ID, wx.ART_OTHER, size )
    return bmp_Flag
# ***********************************************************************


# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':
  app = wx.App ()
  Set_Language ( 'US')
  print("Testing Language")
  print(_(3,'hello'))
  print(_(4,'hello'))
  print( _(5,'bye'))
  print(_(6,'good morning'))
  print(_(8,'good evening'))

  #print  (dir())
  print (__file__)
  print (__name__)

  print(_LT_missing)
  print(_LT)
  print(_LT_Errors)
  #print(Module_Absolute_Path("test","extender.tet"))
# ***********************************************************************
pd_Module ( __file__ )

