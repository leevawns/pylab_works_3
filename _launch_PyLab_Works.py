import os, sys

filename = os.path.join ( os.getcwd(),"PyLab_Works/PyLab_Works.py")
filename = os.path.normpath ( filename )
print("[INFO LAUNCH PROGRAM PyLab_Works]")
My_Globs = {}
My_Globs [ '__name__' ] = '__main__'

#**************************************
# change directory and append path work
#**************************************
Work_Path = os.path.join ( os.getcwd(),"PyLab_Works")
os.chdir ( Work_Path )
sys.path.append ( Work_Path )
#**************************************
# RUN FILE Pylab_Works.py
#**************************************
exec( compile(open(filename, "rb").read(), filename, 'exec'), My_Globs )
