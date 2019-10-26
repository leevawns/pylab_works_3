import __init__

"""
import os
import sys
subdirs = [ 'bricks', '../support', '../Templates' ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
"""

from system_support import run, runwait
#import time

# *****************************************************************
# List of all scripts to be invoked in the testrun
# *****************************************************************
TestPrograms = []
TestPrograms.append ( 'aap'      )
TestPrograms.append ( 'btc_test' )


# *****************************************************************
# run all the scripts
# *****************************************************************
for Program in TestPrograms :
  runwait ( [ 'Python', 'PyLab_Works.py',
              '-TestRun', Program ],
              shell = True )

