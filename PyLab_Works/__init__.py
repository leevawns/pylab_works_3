# This __init__ module should be used
# in every path of the project
# except the "lang" directories
# Deploy.py will copy this __init__ to all necessary locations

# Get my own path
import os, sys
My_Path = sys._getframe().f_code.co_filename
# Search the top directory, which contains "__init__root.py"
Found = False
More  = True
while not ( Found ) and More :
  My_Path = os.path.split ( My_Path ) [0]
  filename = os.path.join ( My_Path, '__init__root.py' )
  Found = os.path.exists ( filename )
  More = My_Path[0] and ( len ( My_Path ) > 3 )

# Stop if no __init__root found
if not ( Found ) :
  print ('Can''t find "__init__root.py"')
  print ('The program will be aborted')
  sys.exit ()
print(sys.path)
# Add the path of __init__root to PythonPath
if My_Path not in sys.path :
  sys.path.append ( My_Path )
print(sys.path)
#  Get the whole rest of the project, including myself
import __init__root

