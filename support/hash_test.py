import __init__
import psyco
psyco.full()

from random import randint, choice
from time   import *
if __name__ == '__main__':
  wordline = 'aap beer coala bom explosion attack w911 alkaida koefnoen lamas'
  words = wordline.split ()
  W = len ( words )
  ww = range ( W )
  W -= 1
  
  N = 1000000

  for i in ww :
    words [i] = words [i] + ' '
  start = time ()
  table = { wordline : -33 }
  for i in xrange ( N ) :
    line = ''
    for k in ww :
      line += choice ( words )
    table [ line ] = i
  print ( time() - start )
  start = time ()

  if table.has_key ( wordline ) :
    print table [ wordline ]
  b = map ( table.has_key, xrange ( 100 * N ) )
  """for i in xrange ( N ) :
    if table.has_key ( wordline+str(i) ) :
      print table [ wordline ]
  """
  print ( time() - start )
