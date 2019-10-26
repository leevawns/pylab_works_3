import __init__

from language_support import  _

# ***********************************************************************
__doc__ = _(0, """
doc_string translated ?
""" )
# ***********************************************************************
_Version_Text = [

[ 0.1 , '04-11-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, ' - orginal release')]
]
# ***********************************************************************
_ToDo = """
"""
# ***********************************************************************

from General_Globals import *
import win32gui
import win32api
import win32con
import fnmatch

# ***********************************************************************
# ***********************************************************************
def Find_Window ( Name ) :
  return  win32gui.FindWindow ( None, Name )

# ***********************************************************************
# ***********************************************************************
def Find_Windows ( Name ) :
  return Get_TopLevel_Windows ( Name )

# ***********************************************************************
# ***********************************************************************
def Get_TopLevel_Windows ( Name = '*' ) :
  """
  Searches for "relevant" top windows,
    returns tuples of ( handle, Title )
  """
  Top_Windows = []
  win32gui.EnumWindows (_windowEnumerationHandler, Top_Windows)
  Wins = []
  for TW in Top_Windows :
    if fnmatch.fnmatch ( TW[1], Name ) and \
       not ( TW [1] in [ '',
       'Default IME', 'M', 'CiceroUIWndFrame',
       'graphballoon', 'balloon',
       'DDE Server Window',  ] ) :
      Wins.append ( TW )
  return Wins

# ***********************************************************************
# ***********************************************************************
def Get_Child_Windows ( Handle ) :
  #VP = win32gui.FindWindow ( None, 'Test PyLab Works GUI Control' )
  Child_Windows = []
  PP = None
  # Unexpected behavior, you must use TRY !!
  try:
    win32gui.EnumChildWindows ( Handle, _windowEnumerationHandler, Child_Windows )
  except :
    pass
  Wins = []
  for TW in Child_Windows :
    if TW [1] :
      Wins.append ( TW )
  return Wins

# ***********************************************************************
# ***********************************************************************
def _windowEnumerationHandler(hwnd, resultList):
    """
    Callback procedure
    Pass to win32gui.EnumWindows() to generate list of window handle,
    window text tuples.
    """
    resultList.append((hwnd, win32gui.GetWindowText(hwnd)))



# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':

  Test_Defs ( 1, 2, 3, 4 )
  Name = 'support'

  if Test ( 1 ) :
    WH = Find_Window ( Name )
    print 'Find Window :', Name , '=', WH

  if Test ( 2 ) :
    Windows = Get_TopLevel_Windows ()
    for Win in Windows :
      print 'Top Window', Win

  if Test ( 3 ) :
    WH = Find_Window ( Name )
    Windows = Get_Child_Windows ( WH )
    for Win in Windows :
      print '  Child Window :', Win

  if Test ( 4 ) :
    Windows = Find_Windows ( 'Py*' )
    for Win in Windows :
      print '  Find Windows :', Win

# ***********************************************************************
pd_Module ( __file__ )
