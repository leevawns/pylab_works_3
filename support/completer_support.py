import __init__

# ***********************************************************************
from language_support import _
from General_Globals  import *
# ***********************************************************************


# ***********************************************************************
_Version_Text = [

[ 1.1 , '31-09-2008', 'Stef Mientki',
'Test Conditions:', (2, ),
_(0, ' - Get_CallTip_Completion  added')],

[ 1.0 , '28-09-2008', 'Stef Mientki',
'Test Conditions:', (2, ),
_(0, ' - orginal release')]
]
# ***********************************************************************


# ***********************************************************************
#from visual import *
#import visual

import rlcompleter
from inspect import *

Special_Imports = {
  'DOM' : [ 'pyjamas' ],
  'pyjamas' : [ 'pyjamas', 'pyjamas.ui'],
  'wx'  : [ 'wx.gizmos', 'wx.grid', 'wx.lib', 'wx.stc' ],
  'stc' : [ 'wx.stc as stc' ]
}
# ***********************************************************************


# ***********************************************************************
# Determines the type of the partial string
# Returns     in caes of
#    int         56
#    str         'a string'
#    False       uncompleted string:  'a string
#    None        otherwise
# ***********************************************************************
def _Find_Type ( Part) :
  if ( Part.find ("'") >= 0 ) :
    start  = Part.find ( "'" )
    finish = Part.find ( "'", start + 1 )
    if finish < start :
      return False
    return str
  else :
    try :
      Typ = eval ( 'type ( '  + Part + ')' )
      # on integer, just return: "integer." will become a float
      if Typ == int :
        return int
    except :
      return None
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_Completions ( word ) :
  #print '********* start completion of :', word

  # *********************************************
  # parse the specified word
  # *********************************************
  Left_Part  = None
  Right_Part = word
  N_Parts    = 1
  if word.find('.') >= 0 :
    Word_Parts = word.split('.')
    N_Parts    = len ( Word_Parts )
    Left_Part  = '.'.join ( Word_Parts [ : -1 ] )
    Right_Part = Word_Parts [ -1 ]

  # *********************************************
  # Handle special type like integer / string
  # *********************************************
  Typ = None
  if not ( Left_Part ) :
    Typ = _Find_Type ( Right_Part )
    if Typ in ( False, int, str ) :
      return None
  else :
    Typ = _Find_Type ( Left_Part )
    if Typ in ( False, int ) :
      return None

    # if not a special type, import left_part
    if not ( Typ ) :

      # *********************************************
      # special import packages that can't be detected
      # *********************************************
      if Special_Imports.has_key ( Word_Parts [0] ) :
        Imports = Special_Imports [ Word_Parts [0] ]
        for module in Imports :
          try :
            print ('Special import :', module)
            exec ( 'import ' + module ,globals())
            Failed = False
          except :
            pass

      # *********************************************
      # import the necessary module
      # because we don't know how many parts on the left of the word
      # are module / path information ( instead of class information)
      # we start with the largest left part,
      # and each time we don't succeed we try one part less
      # *********************************************
      Failed = True
      N      = N_Parts
      while Failed and ( N > 1 ) :
        N -= 1
        module = '.'.join ( Word_Parts [ : N ] )
        try :
          exec ( 'import ' + module ,globals())
          Failed = False
        except :
          pass

  if Typ == str :
    Completion_Line = u'str.'
  else :
    Completion_Line = word
  RL = len ( Right_Part )
  #print 'CLine', Typ, RL, Completion_Line

  # *********************************************
  # Determine lenght of left part
  # *********************************************
  if Left_Part :
    LL = len ( Left_Part ) + 1
  else :
    LL = 0

  # *********************************************
  # get the completions
  # *********************************************
  Completer = rlcompleter.Completer ( locals () )
  State     = 0
  Result    = []
  #print 'UUU',Completion_Line, State
  try:
    Next      = Completer.complete ( Completion_Line, State )
    while Next :
      if Typ == str :
        if Next [ 4 ] != '_' :
          Result.append ( Next.replace ( 'str.', '' ) )
      else :
        # remove the part before the dot = left_part
        line = Next [ LL : ]
        # accept only items not starting with '_'  except '__init__'
        if line and ( ( line == '__init__' ) or ( line [ 0 ] != '_' ) ) :
          Result.append ( line )
      State  += 1
      Next = Completer.complete ( Completion_Line, State )
  except :
    pass

  # *********************************************
  # join the result and return
  # *********************************************
  if not ( Result ) :
    return None
  Result.sort()
  Result = ' '.join ( Result )
  return ( RL, Result )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_CallTip_Completion ( word, Arg_Index = 0 ) :
  #print '********* start CallTip of :', word
  pass

  """
  # *********************************************
  # get rid of everything starting at '(...'
  # and return if no left bracket
  # *********************************************
  i = word.find('(')
  if i < 0 :
    return
  word = word [ : i].strip()
  """

  # *********************************************
  # parse the specified word
  # *********************************************
  Word_Parts = word.split('.')
  N_Parts    = len ( Word_Parts )

  # *********************************************
  # special import packages that can't be detected
  # *********************************************
  if Word_Parts [0] in Special_Imports:
    Imports = Special_Imports [ Word_Parts [0] ]
    for module in Imports :
      try :
        #print 'Special import :', module
        exec ( 'import ' + module,globals() )
        Failed = False
      except :
        pass

  # *********************************************
  # import the necessary module
  # because we don't know how many parts on the left of the word
  # are module / path information ( instead of class information)
  # we start with the largest left part,
  # and each time we don't succeed we try one part less
  # *********************************************
  Failed = True
  N      = N_Parts
  while Failed and ( N > 0 ) :
    module = '.'.join ( Word_Parts [ : N ] )
    N -= 1
    try :
      exec ( 'import ' + module ,globals())
      Failed = False
    except :
      pass

  from wx.py import introspect
  import inspect

  # *********************************************
  # Get the object
  # *********************************************
  try:
    object = eval ( word, locals() )
  except:
    return None

  # *********************************************
  # get the objects name
  # *********************************************
  name = ''
  object, dropSelf = introspect.getBaseObject(object)
  try:
    name = object.__name__
  except AttributeError:
    pass

  # *********************************************
  # get arguments
  # *********************************************
  tip1 = ''
  argspec = ''
  if inspect.isbuiltin(object):
      # Builtin functions don't have an argspec that we can get.
      pass
  elif inspect.isfunction(object):
      # tip1 is a string like: "getCallTip(command='', locals=None)"
      argspec = apply(inspect.formatargspec, inspect.getargspec(object))
      if dropSelf:
          # The first parameter to a method is a reference to an
          # instance, usually coded as "self", and is usually passed
          # automatically by Python; therefore we want to drop it.
          temp = argspec.split(',')
          if len(temp) == 1:  # No other arguments.
              argspec = '()'
          elif temp[0][:2] == '(*': # first param is like *args, not self
              pass
          else:  # Drop the first argument.
              argspec = '(' + ','.join(temp[1:]).lstrip()
      tip1 = name + argspec


  # *********************************************
  # get doc
  # *********************************************
  doc = ''
  if callable(object):
    try:
      doc = inspect.getdoc(object)
    except:
      pass
  if doc:
      # tip2 is the first separated line of the docstring, like:
      # "Return call tip text for a command."
      # tip3 is the rest of the docstring, like:
      # "The call tip information will be based on ... <snip>
      firstline = doc.split('\n')[0].lstrip()
      if tip1 == firstline or firstline[:len(name)+1] == name+'(':
          tip1 = ''
      else:
          tip1 += '\n\n'
      docpieces = doc.split('\n\n')
      tip2 = docpieces[0]
      tip3 = '\n\n'.join(docpieces[1:])
      tip = '%s%s\n\n%s' % (tip1, tip2, tip3)
  else:
      tip = tip1

  #calltip = (name, argspec[1:-1], tip.strip())
  return tip.strip()

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
if __name__ == "__main__":

  test = [ 2 ]

  if 1 in test :
    #print Get_Completions ( 'wx.' )
    print (Get_Completions ( 'wx.s' ))
    print (Get_Completions ( 'wx.g' ))
    print (Get_Completions ( 'wx.stc.wx' ))
    #print Get_Completions ( 'wx.stc.StyledTextCtrl.' )
    print (Get_Completions ( 'wx.stc.StyledTextCtrl.Is' ))
    print (Get_Completions ( "'Aapje" ))
    print (Get_Completions ( "'Aapje'" ))
    print (Get_Completions ( "'Aapje'." ))
    print (Get_Completions ( '68' ))
    print (Get_Completions ( '68.' ))
    print (Get_Completions ( '68.4' ))
    #print Get_Completions ( 'stc.' ))
    print (Get_Completions ( 'w' ))

  if 2 in test :
    print (Get_CallTip_Completion ( 'os.path.join', 1 ))
    #print Get_CallTip_Completion ( 'sys.')
    #print Get_CallTip_Completion ( 'sys.path.isdir(')
# *******************************************************


"""
********* start completion of : wx.s
(1, 'stc')
********* start completion of : wx.g
(1, 'gizmos grid')
********* start completion of : wx.stc.wx
(2, 'wx wxEVT_STC_AUTOCOMP_SELECTION wxEVT_STC_CALLTIP_CLICK ...
********* start completion of : wx.stc.StyledTextCtrl.Is
(2, 'IsBeingDeleted IsDoubleBuffered IsEnabled IsExposed ...
********* start completion of : 'Aapje
None
********* start completion of : 'Aapje'
None
********* start completion of : 'Aapje'.
(0, u'capitalize center count decode encode endswith ...
********* start completion of : 68
None
********* start completion of : 68.
None
********* start completion of : 68.4
None
********* start completion of : w
(1, 'while with word')
"""

# ***********************************************************************
pd_Module ( __file__ )
