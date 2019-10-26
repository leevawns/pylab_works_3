import os
from General_Globals import *

# ***********************************************************************
# ***********************************************************************

def test () :
    print 'sys.path:'
    for item in sys.path :
      print '  ', item
    print 'sys.path[0] = path of the main application file ', sys.path[0]
    print 'os.getcwd()', os.getcwd ()
    print '__file__', __file__
    
    sys.path.append ( '../support' )
    from system_support import test_back
    test_back ()
# ***********************************************************************
pd_Module ( __file__ )

