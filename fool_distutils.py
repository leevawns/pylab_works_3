
"""
from system_support import Run_Python
Run_Python ( 'support/gui_support.py', cwd = 'support/' )
print 'finished-1'
"""

"""
import subprocess
subprocess.Popen ( ['python', 'support/gui_support.py' ] )
#
#                            cwd   = cwd ,
#                            shell =  ( os.name == 'nt') )
"""

import __init__root
execfile ( 'support/gui_support.py' )
print 'finished-2'
import site
print site.abs__file__()
import gui_support
print gui_support.__file__, __file__

# This will give the current filename,
# including a relative or absolute path
import inspect
print inspect.currentframe().f_code.co_filename



#print site.path