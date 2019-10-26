from pyparsing import *

import pprint

"""
# use {}'s for nested lists
nestedItems = nestedExpr("{", "}")
print( (nestedItems+stringEnd).parseString(data).asList() )

# use default delimiters of ()'s
mathExpr = nestedExpr()
print( mathExpr.parseString( "(( ax + by)*C) (Z | (E^F) & D)") )
"""


# ***********************************************************************
from traceback import format_tb, format_exception_only
from sys import exc_info
from re import compile
varsplitter = compile ( "[^0-9a-zA-Z_]" )
#varsplitter = compile ( "^0-9a-zA-Z_" )
def format_exception():
  """
  Add a dump of any variables we can identify from the failing program
  line to the end of the traceback.  The deep mojo for doing this came
  from an example in the Zope core plus documentation in the Python
  Quick Reference.
  """
  etype, value, tb = exc_info ()
  plaintb = format_tb ( tb )
  result  = [ 'Traceback (innermost last):\n' ]
  for line in plaintb:
    result.append ( '*****' + line )
    f = tb.tb_frame
    tb = tb.tb_next
    locals = f.f_locals
    print '*****',line,'\n    &&&&'

    # remove left part(s) of an assignment
    # [-2] is the code line, contianing the error
    line = line.split ( '\n' ) [ -2 ]
    while '=' in line :
      line = line [ line.find ('=')+1 : ]

    # parse the rest of the line
    vars = varsplitter.split ( line )


    dvars = set ()
    self = None
    if 'self' in locals:
      self = locals [ 'self' ]

    # remove empties
    while '' in vars :
      vars.remove ( '' )

    result.append ( 'PIEP3' + str ( vars ) + '\n' )
    for v in vars:
      if v in dvars :
        continue
      dvars.add(v)

      #if '[' in v :
      #  v.split
      if v in locals:
        result.append ('      %s: %r\n' % (v,locals[v]))
      if self and hasattr ( self, v ) :
        result.append ('      self.%s: %r\n' % (v,getattr(self, v)))
      if v in globals () :
        result.append ('      (global) %s: %r\n' % (v,globals()[v]))
    print 'PIEP4'
  result.extend ( format_exception_only ( etype, value ) )
  return ''.join ( result )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
# ***********************************************************************



A = [ 11,22,33,44,55,66,77,88,99,1,2,3,4,5,6]
B = [ 1,2,3,4,5,6,7,8,9]
BB = [[ 1,2,3,4,5,8,9],[ 1,2,3,4,5,8,9],[ 1,2,3,4,5,8,9],[ 1,2,3,4,5,8,9],[ 1,2,3,4,5,8,9]]
C = 3
D = 2
result = A [ B [ C + 2 ] + 1 ]
line = "(A [ B [ C + 2 ] + 1 ])"
#print ( mathExpr.parseString( line ) )
#print result


# ***********************************************************************
# ***********************************************************************
def parse_list ( s, start = 0 ) :
  """
  parse a (nested) list into it's components
     line = " A  [  B  [ C+2 ] + 3 ] "
  will result in
     [' C+2 ', '  B  [ C+2 ] + 3 ', ' A  [  B  [ C+2 ] + 3 ] ']
  """
  x = []
  i = start
  while i < len ( s ) :
    c = s [ i ]
    if c == '[' :
      y, i = parse_list ( s, i + 1 )
      x = x + y
    if c == ']' :
      return x + [ s [ start : i ] ], i
    i += 1
  return x + [ s ]
# ***********************************************************************


def test ( value ) :
  #print 'VALUE', value
  return value * value

lines = []
lines.append ( " A  [  BB  [ C-2 ] [ D-1 ] + 3 ] " )
lines.append ( "   A  [  B  [ C+2 ] + 3 ] " )
lines.append ( " A  [  B  [ C+2 ] + 3 ] " )
lines.append ( " test ( C ) " )
lines.append ( " 3 * C " )


for line in lines :
  line = line.replace ( ' ', '' )
  parsed = parse_list ( line )
  print '\n*****', line
  
  for elem in parsed :
    # we need to display the length of lists
    if elem.find ( '[' ) > 0 :
      i = 0
      splitted = []
      while '[' in elem [ i : ] :
        i = elem.find ( '[', i )
        splitted.append ( elem [ : i ] )
        LB = 1
        ii = i + 1
        # find belonging right bracket
        while ( ii < len ( elem ) ) and ( LB > 0 ):
          if elem [ii] == '[' :
            LB += 1
          elif elem [ii] == ']' :
            LB -= 1
          ii += 1
        splitted.append ( elem [ i : ii ] )
        if elem [ ii : ] :
          splitted.append ( elem [ ii : ] )
        i += ii + 1
      i = 1
      for item in splitted [ 2 : ] :
        if '[' in item :
          i += 1
      for ii in range ( i ) :
        item = ''.join ( splitted [ : ii+1 ] )
        print 'len(' + item + ')='+ str ( eval ( 'len(' + item + ')' ))+ ',  ',

    print elem + '=' + str ( eval ( elem ) )


# ***********************************************************************
from traceback import format_tb, format_exception_only
from sys import exc_info
from re import compile
varsplitter = compile ( "[^0-9a-zA-Z_]" )
#varsplitter = compile ( "^0-9a-zA-Z_" )
def format_exception():
  """
  Add a dump of any variables we can identify from the failing program
  line to the end of the traceback.  The deep mojo for doing this came
  from an example in the Zope core plus documentation in the Python
  Quick Reference.
  """
  etype, value, tb = exc_info ()
  plaintb = format_tb ( tb )
  result  = [ 'Traceback (innermost last):\n' ]
  for line in plaintb:
    result.append ( '*****' + line )
    f = tb.tb_frame
    tb = tb.tb_next
    locals = f.f_locals
    print '*****',line,'\n    &&&&'

    # remove left part(s) of an assignment
    # [-2] is the code line, containing the error
    line = line.split ( '\n' ) [ -2 ]
    while '=' in line :
      line = line [ line.find ('=')+1 : ]

    """
    # parse the rest of the line
    vars = varsplitter.split ( line )

    dvars = set ()
    self = None
    if 'self' in locals:
      self = locals [ 'self' ]

    # remove empties
    while '' in vars :
      vars.remove ( '' )

    result.append ( 'PIEP3' + str ( vars ) + '\n' )
    for v in vars:
      if v in dvars :
        continue
      dvars.add(v)

      #if '[' in v :
      #  v.split
      if v in locals:
        result.append ('      %s: %r\n' % (v,locals[v]))
      if self and hasattr ( self, v ) :
        result.append ('      self.%s: %r\n' % (v,getattr(self, v)))
      if v in globals () :
        result.append ('      (global) %s: %r\n' % (v,globals()[v]))
    print 'PIEP4'
    """
    line = line.replace ( ' ', '' )
    parsed = parse_list ( line )
    result.append ( '\n*****', line )

    for elem in parsed :
      # we need to display the length of lists
      if elem.find ( '[' ) > 0 :
        i = 0
        splitted = []
        while '[' in elem [ i : ] :
          i = elem.find ( '[', i )
          splitted.append ( elem [ : i ] )
          LB = 1
          ii = i + 1
          # find belonging right bracket
          while ( ii < len ( elem ) ) and ( LB > 0 ):
            if elem [ii] == '[' :
              LB += 1
            elif elem [ii] == ']' :
              LB -= 1
            ii += 1
          splitted.append ( elem [ i : ii ] )
          if elem [ ii : ] :
            splitted.append ( elem [ ii : ] )
          i += ii + 1
        i = 1
        for item in splitted [ 2 : ] :
          if '[' in item :
            i += 1
        for ii in range ( i ) :
          item = ''.join ( splitted [ : ii+1 ] )
          result.append ( 'len(' + item + ')='+ str ( eval ( 'len(' + item + ')' ))+ ',  ', )

      result.append ( elem + '=' + str ( eval ( elem ) ) )

  result.extend ( format_exception_only ( etype, value ) )
  return ''.join ( result )
# ***********************************************************************

#...So long as you don't have any brackets inside strings or what not.
#It just admits two special characters, '[' and ']'.
