import __init__root

from General_Globals import Module_Absolute_Path
My_File = Module_Absolute_Path ( 'support', 'T53.py' )

Globs = {}
Globs [ '__name__' ] = '__main__'
execfile ( My_File, Globs )
#print Globs