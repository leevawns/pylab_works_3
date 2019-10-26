import __init__
from General_Globals import *

# contains OS dependant names

Win = "Windows"

OS_Dependent = {
 'splitunc'         : Win,
 'os.path.splitunc' : Win,
 'iewin'            : Win,
}


# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  for item in OS_Dependent :
    print item, ':', OS_Dependent [ item ]
# ***********************************************************************
pd_Module ( __file__ )
