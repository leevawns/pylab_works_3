import os, sys
My_Path = sys._getframe().f_code.co_filename
sys.path.append ( My_Path )
print 'pop',My_Path
for path in sys.path :
  print path