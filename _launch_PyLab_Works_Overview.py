import os, sys

filename = os.path.join ( os.getcwd(),"PyLab_Works/PyLab_Works_Overview.py")
filename = os.path.normpath ( filename )

My_Globs = {}
My_Globs [ '__name__' ] = '__main__'

Work_Path = os.path.join ( os.getcwd(),"PyLab_Works")
os.chdir ( Work_Path )
sys.path.append ( Work_Path )

exec( compile(open(filename, "rb").read(), filename, 'exec'), My_Globs )
