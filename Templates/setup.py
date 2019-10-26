import __init__
from distutils.core import setup
import py2exe

"""
import sys
import os
subdirs = [ '../support', '../pictures', '../Lib_Extensions' ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
"""
#import matplotlib


# If run without args, build executables, in quiet mode.
if len(sys.argv) == 1:
    sys.argv.append("py2exe")

import glob

#  console = ['scintilla_templates.py'],
setup (
  windows = ['scintilla_templates.py'],
  data_files = [
    ( '', glob.glob ( 'templates_*.*' ))
      ])



import subprocess
"""
result = subprocess.call (
  [ 'P:\Program Files\Inno Setup 4\Compil32.exe',
    '/cc',
    'D:\data_to_test\jalspy\PyLab_Works.iss'])
"""
result = subprocess.call (
  [ 'P:\Program Files\Inno Setup 4\ISCC.exe',
    'scintilla_templates.iss'])

print 'BUILD',result==0

if result==0 :
  import shutil
  shutil.rmtree ( '/build' )
  shutil.rmtree ( '/dist' )
  print 'piep'