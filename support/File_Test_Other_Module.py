import __init__

from General_Globals import *
from utility_support import *

# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':

  Test_Defs ( 1 )

  # TIO_Dictionary test
  if Test ( 1 ) :
    Application.Debug_Mode = True
    TIO = TIO_Dict ()
    TIO [ 'aap'] = 'beer'
    TIO [ 33 ]   = 44
    for item in TIO :
      a = TIO [ item ]
