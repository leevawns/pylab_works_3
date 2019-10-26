import os, sys
Base_Path = sys._getframe().f_code.co_filename
Base_Path = os.path.split ( Base_Path ) [0]
filename = os.path.join ( os.getcwd(), Base_Path,"support/demo_gui.py")
filename = os.path.normpath ( filename )
My_Globs = {}
My_Globs [ '__name__' ] = '__main__'
Work_Path = os.path.join ( os.getcwd(), Base_Path,"support")
os.chdir ( Work_Path )
sys.path.append ( Work_Path )
print "LAUNCH FILENAM", filename
print "CWD:", os.getcwd()
execfile ( filename, My_Globs )
