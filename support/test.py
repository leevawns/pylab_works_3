print dir()
from file1 import *
print dir ()


filename = 'file2.py'
fh = open ( filename, 'w' )
fh.write ( 'class class2 ( object ) :\n' )
fh.write ( '  pass\n' )
fh.write ( 'try:\n')
fh.write ( '  from file3 import class3\n')
fh.write ( 'except :\n')
fh.write ( '  print "piep"\n')
fh.close ()

#from file2 import *
execfile ( filename )
print dir()