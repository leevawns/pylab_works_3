import __init__
from General_Globals import *
from file_support    import Find_Files
from inifile_support import inifile


# ***********************************************************************
# ***********************************************************************
def Get_Control_Classes ( my_module, my_path = None ):
  import pyclbr
  if my_path != None:
    path = []
    path.append ( my_path )
    my_classes = pyclbr.readmodule_ex ( my_module, path )
  else:
    my_classes = pyclbr.readmodule_ex ( my_module )
    #my_classes = pyclbr.readmodule_ex ( my_module,
    #  [ 'D:/Data_Python_25/PyLab_Works/controls', 'D:/Data_Python_25/PyLab_Works'])

  # now order them by linenr
  ordered_list = []
  for item in my_classes:
    if my_classes[item].module == my_module :
      name = my_classes [ item ].name
      if name [:4] == 't_C_' :
        ordered_list.append ( ( my_classes[item].lineno,
                                my_classes[item].name [4:]  ) )
        """
        module -- the module name
        name -- the name of the class
        super -- a list of super classes (Class instances)
        methods -- a dictionary of methods
        file -- the file in which the class was defined
        lineno -- the line in the file on which the class statement occurred
        """

  # Sort the list
  ordered_list.sort()

  # now build a list with only brick names
  my_class_names = []
  for item in ordered_list:
    my_class_names.append ( item [1] )
  return my_class_names
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
#my_dir = path_split ( __file__ )[0]
my_dir = sys._getframe().f_code.co_filename
my_dir = os.path.split ( my_dir ) [0]

ini_filename = 'control_list.cfg'
ini_filename = os.path.join ( my_dir, ini_filename )
ini = inifile ( ini_filename )
ini.Section = 'Controls'
control_list = ini.Read_Dict ( 'Dict' )
print(control_list)

Py_Files = Find_Files ( my_dir, 'control_*.py', RootOnly = True )
for file in Py_Files :
  filename = os.path.join ( my_dir, file[1] + '.py' )
  last_modified = int ( os.path.getmtime ( filename ) )

  print ( 'Generate Control Imports', file[1] )
  if not ( file[1] in control_list ) or \
    ( control_list [ file[1] ] [0] != last_modified ) :

    my_classes = Get_Control_Classes ( file [1] )
    control_list [ file[1] ] = [ last_modified, my_classes ]
    #print last_modified, file[1]

ini.Write ( 'Dict', control_list )
ini.Close ()
#print control_list

# Now import all controls

filename = os.path.join ( my_dir, 'import_controls_dynamic.py' )
fh = open ( filename, 'w' )
#fh.write ( 'print "DYN", dir()\n' )
#fh.write ( 'import __init__\n')
for file in control_list :
  if len ( control_list [ file ][1] ) > 0 :
    fh.write ( 'try :\n')
    for klass in control_list [ file ][1] :
      line = '  from ' + file + ' import t_C_' + klass + '\n'
      fh.write ( line )
    fh.write ( 'except :\n')
    fh.write ( '  print ("Can\'t import from, ' + file +'")'+ '\n')
    fh.write ( '  import traceback\n' )
    fh.write ( '  traceback.print_exc ()\n')
    
#fh.write ( 'print "DYN", dir()\n' )
fh.close ()

"""
fh = open ( filename, 'r' )
lines = fh.readlines ()
for line in lines :
  print 'OPOP',line.replace ( '\n', '' )
fh.close ()
"""

#print 'CONTROLS', dir()
#Doesn't work anymore !!
#from import_controls_dynamic import *
#execfile ( filename )
exec(open(filename).read())
#print 'CONTROLS', dir()
# ***********************************************************************
pd_Module ( __file__ )
