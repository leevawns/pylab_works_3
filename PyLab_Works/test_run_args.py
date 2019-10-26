#test run with args

import os, sys
print 'XXXXXXXXXX',sys.argv
sys.argv.insert ( 1, 'proof_of_concept')
execfile ( 'PyLab_Works.py' )