import os, sys
My_Path = os.path.split ( sys._getframe().f_code.co_filename ) [0]
filename = os.path.join ( '..', 'support', 'demo_gui.py')
execfile ( filename )




