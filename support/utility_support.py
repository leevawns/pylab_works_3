import __init__

from General_Globals import *
from numpy import *

"""
# ***********************************************************************
# ***********************************************************************
class s_list ( list ) :
  def Get ( self, Attrib, Default ) :
    try :
      return getattr ( self, Attrib )
    except :
      return Default
# ***********************************************************************
"""




# ***********************************************************************
# ***********************************************************************
class super_dict ( dict ) : #, object ) :
  pass

class super_object ( object ) :
  """Object with some features of a dictionair"""
  def Get ( self, arg, default ) :
    """Mimicks the "get" function of a dictionair."""
    try :
      return getattr ( self, arg )
    except :
      # If the property doesn't exist,
      # Create it now
      setattr ( self, arg, default )
      return default



# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get ( Base, Attrib, Default ) :
  try :
    return getattr ( Base, Attrib )
  except :
    return Default
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def nice_number ( value ) :
  if   abs ( value ) >= 100 :
    line = '%5d' %( int(value) )
  elif abs ( value ) >= 10 :
    line = '%5.1f' %( value )
  else:
    line = '%5.2f' %( value )
  return line
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
_types = ['int   ', 'float ', 'string' ]
def _Type_Enumerate_weg ( value, pre, counters ) :
  pre += '--'
  if type ( value ) in [ list, tuple ] :
    counters.append ( [ 0, 0 ] )
    print(pre, type ( value ).__name__)
    for item in value :
      _Type_Enumerate ( item, pre, counters )
    count = counters.pop ()
    for i,c in enumerate ( count ) :
      if c > 0 :
        print(pre + '--', _types[i], '=', c)
  else :
    if type ( value ) == int :
      counters [-1][0] += 1
    if type ( value ) == float :
      counters [-1][1] += 1
    #print pre, type (value).__name__, counters[-1]



# ***********************************************************************
# ***********************************************************************
def _Type_Enumerate ( value, pre, counters ) :
  pre += '--'
  typ = type ( value )
  last = counters [-1]

  if typ in [ list, tuple, array ] :
    if ( last [0] > 0):
      print(pre, last[1].__name__.ljust(6), '=', last[0])
      counters.pop()

    counters.append ( [ 0, None ] )
    print(pre, typ.__name__)
    for item in value :
      _Type_Enumerate ( item, pre, counters )

    last = counters.pop ()
    if last [0] > 0 :
      print(pre + '--', last[1].__name__.ljust(6),'=',last[0])

  else :
    if last [1] == typ :
      last [0] += 1
    else :
      if last[0] > 0:
        print(pre, last[1].__name__.ljust(6),'=',last[0])
      last[0] = 1
      last[1] = typ


# ***********************************************************************
# ***********************************************************************
def Type_Enumerate ( value ) :
  _Type_Enumerate ( value, '|', [0, [0,None]] )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class TIO_Dict ( dict ) :
  """
  Dictionary that can print or log debug info.
  The following methods will be logged:
  - Create
  - Read
  - Write
  """
  def _Log ( self, *args ) :
    #if 'TIO' in Debug_What :
    if self.Max_Log_Count > 0 :
      Debug_Dump_Trace ( 'TIO_Dict\n', *args )
      self.Max_Log_Count -= 1
      if self.Max_Log_Count == 0 :
         Debug_Dump ( 'TIO_Dict, ****** max limit exceeded ******')

  #def __init__ ( self, Parent = None, PIndex = -1 ):
  def __init__ ( self, Parent, PIndex ):
    self.Parent = Parent
    self.PIndex = PIndex
    self.Max_Log_Count = 100
    dict.__init__ ( self )
    ##self.Modified = False
    if ( 'TIO-Read' in Debug_What ) :
      self._Log ( 'Create' )

  def __setitem__ ( self, key, value ) :
    dict.__setitem__ ( self, key, value )
    ##self.Modified = True
    # Pass the modify flag to the parent
    self.Parent._Set_Modified ( self.PIndex, value, key )
    if ( 'TIO-Write' in Debug_What ) :
      self._Log ( 'Write:', key, '=', value )

  # Override, because we want to log during debug
  def __getitem__ ( self, key ) :
    value = dict.__getitem__ ( self, key )
    if ( 'TIO-Read' in Debug_What ) :
      self._Log ( 'Read: ', key, '=', value )
    return value
# ***********************************************************************


# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':

  Test_Defs ( 4 )

  # **********************************
  # **********************************
  if Test ( 1 ) :
    a = [2,3,(3,4,'strif','sdas',50.,4.5),[45.,89,'stri'],(5)]
    Type_Enumerate ( a  )
    
  # **********************************
  # TIO_Dictionary test
  # **********************************
  if Test ( 2 ) :
    class tParent ( object ):
      def __init__ ( self ) :
        pass
      def _Set_Modified ( self, PIndex, value, key ) :
        pass
    TIO_Parent = tParent ()

    Application.Debug_Mode = True
    TIO = TIO_Dict ( TIO_Parent, 1 ) ;
    TIO [ 'aap'] = 'beer'
    TIO [ 'aap'] = 'beer'
    TIO [ 33 ]   = 44
    for item in TIO :
      a = TIO [ item ]

  # **********************************
  # **********************************
  if Test ( 3 ) :
    SD = super_dict ()
    SD [ 'aap' ] = 44
    SD [ 44    ] = 33
    SD.type = 'aap'
    print(SD, dir ( SD ), SD.type)

    SD = super_object ()
    SD.aap = 44
    SD.type = 'aap'
    print(SD, dir ( SD ), SD.type)
    print(SD.Get ( 'aap', 684 ), SD.Get ( 'beer', 685))

  # **********************************
  # t_signal_attr
  # **********************************
  if Test ( 4 ) :
    signal_attr = t_signal_attr ()
    signal_attr.Color = 'Color'
    v3print ( signal_attr.Color )
    v3print ( signal_attr.Not_Existing )
    
    for item in dir() :
      if item[0].isupper () :
        print(item, type ( eval ( item ) ),eval(item))
    print(type(WRAP))
# ***********************************************************************
pd_Module ( __file__ )

