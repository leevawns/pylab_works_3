import __init__

Kill_Distro       = False #True
MatPlotLib_Wanted = False #True

from   distutils.core import setup
import py2exe
"""
import sys
subdirs = [ '../support',
            '../pictures',
            '../sounds',
            '../Lib_Extensions',
            '../Templates' ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
"""
from file_support import *

#import numpy
#from numpy import numarray
"""
from numarray import Int8
from numarray import *
#import Complex32
# pyd's
import numarray.libnumarray
import numarray.libnumeric
import numarray.memory
import numarray._bytes
import numarray._chararray
import numarray._conv
import numarray._converter
import numarray._ndarray
import numarray._numarray
import numarray._objectarray
import numarray._operator
import numarray._sort
import numarray._ufunc
import numarray._ufuncBool
import numarray._ufuncComplex32
import numarray._ufuncComplex64
import numarray._ufuncFloat32
import numarray._ufuncFloat64
import numarray._ufuncInt16
import numarray._ufuncInt32
import numarray._ufuncInt64
import numarray._ufuncInt8
import numarray._ufuncUInt16
import numarray._ufuncUInt32
import numarray._ufuncUInt8
# py's
import numarray.arrayprint
import numarray.array_persist
import numarray.dotblas
import numarray.generic
import numarray.ieeespecial
import numarray.memmap
import numarray.memorytest
import numarray.numarrayall
import numarray.numarraycore
import numarray.numarrayext
import numarray.numeric
import numarray.numerictypes
import numarray.numinclude
import numarray.numtest
import numarray.objects
import numarray.readonly
import numarray.records
import numarray.safethread
import numarray.strings
#import numarray.teacup
import numarray.testall
import numarray.testdata
import numarray.typeconv
import numarray.ufunc
import numarray._ufuncall
# subpackages
import numarray.convolve
import numarray.convolve.lineshape
import numarray.fft
import numarray.image
import numarray.linear_algebra
import numarray.ma
import numarray.matrix
import numarray.mlab
import numarray.nd_image
import numarray.random_array
"""

import shutil
import glob


# ***********************************************************************
# Some suggests that old build/dist should be cleared
# ***********************************************************************
dist_paths =  [ 'D:/Data_Python_25/PyLab_Works/build',
                'D:/Data_Python_25/PyLab_Works/dist' ]
for path in dist_paths :
  if File_Exists ( path ) :
    shutil.rmtree ( path )
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
data_files   = []
packages     = []
includes     = []
excludes     = []
dll_excludes = []
data_files.append ( ( '', glob.glob ( 'templates_*.*' ) ) )


"""
# ***********************************************************************
# I have used a trick to make py2exe recognize all of numarray's
# modules,  which I suggest be incorporated into the numarray CVS.
# It can be a real  pain to solve this problem the first time you're
# py2exe-ing a script  using numarray and find out that it simply
# doesn't work. I just added  this to numarray's __init__.py:
# ***********************************************************************

  # this is needed for py2exe to be able to include numarray
  def _give_py2exe_hints():
      # pyd's
      import numarray.libnumarray
      import numarray.libnumeric
      import numarray.memory
      import numarray._bytes
      import numarray._chararray
      import numarray._conv
      import numarray._converter
      import numarray._ndarray
      import numarray._numarray
      import numarray._objectarray
      import numarray._operator
      import numarray._sort
      import numarray._ufunc
      import numarray._ufuncBool
      import numarray._ufuncComplex32
      import numarray._ufuncComplex64
      import numarray._ufuncFloat32
      import numarray._ufuncFloat64
      import numarray._ufuncInt16
      import numarray._ufuncInt32
      import numarray._ufuncInt64
      import numarray._ufuncInt8
      import numarray._ufuncUInt16
      import numarray._ufuncUInt32
      import numarray._ufuncUInt8
      # py's
      import numarray.arrayprint
      import numarray.array_persist
      import numarray.dotblas
      import numarray.generic
      import numarray.ieeespecial
      import numarray.memmap
      import numarray.memorytest
      import numarray.numarrayall
      import numarray.numarraycore
      import numarray.numarrayext
      import numarray.numeric
      import numarray.numerictypes
      import numarray.numinclude
      import numarray.numtest
      import numarray.objects
      import numarray.readonly
      import numarray.records
      import numarray.safethread
      import numarray.strings
      import numarray.teacup
      import numarray.testall
      import numarray.testdata
      import numarray.typeconv
      import numarray.ufunc
      import numarray._ufuncall
      # subpackages
      import numarray.convolve
      import numarray.convolve.lineshape
      import numarray.fft
      import numarray.image
      import numarray.linear_algebra
      import numarray.ma
      import numarray.matrix
      import numarray.mlab
      import numarray.nd_image
      import numarray.random_array
# ***********************************************************************
"""



# ***********************************************************************
# For MatPlotLib
# ***********************************************************************
if MatPlotLib_Wanted :
  import matplotlib

  includes.append ( 'matplotlib.numerix.random_array' )

  packages.append ( 'matplotlib' )
  packages.append ( 'pytz' )

  data_files.append ( ( r'mpl-data', glob.glob (
    r'P:/Python/Lib/site-packages/matplotlib/mpl-data/*.*' )))
  data_files.append ( ( r'mpl-data', glob.glob (
    r'P:/Python/Lib/site-packages/matplotlib/mpl-data/matplotlibrc' )))
  data_files.append ( ( r'mpl-data/images', glob.glob (
    r'P:/Python/Lib/site-packages/matplotlib/mpl-data/images/*.*' )))
  data_files.append ( ( r'mpl-data/fonts/afm', glob.glob (
    r'P:/Python/Lib/site-packages/matplotlib/mpl-data/fonts/afm/*.*' )))
  data_files.append ( ( r'mpl-data/fonts/pdfcorefonts', glob.glob (
    r'P:/Python/Lib/site-packages/matplotlib/mpl-data/fonts/pdfcorefonts/*.*' )))
  data_files.append ( ( r'mpl-data/fonts/ttf', glob.glob (
    r'P:/Python/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/*.*' )))

# ***********************************************************************


# excludes are done always
excludes.append ( '_gtkagg'          )
excludes.append ( '_tkagg'           )
excludes.append ( '_agg2'            )
excludes.append ( '_cairo'           )
excludes.append ( '_cocoaagg'        )
excludes.append ( '_fltkagg'         )
excludes.append ( '_gtk'             )
excludes.append ( '_gtkcairo'        )
excludes.append ( 'backend_qt'       )
excludes.append ( 'backend_qt4'      )
excludes.append ( 'backend_qt4agg'   )
excludes.append ( 'backend_qtagg'    )
excludes.append ( 'backend_cairo'    )
excludes.append ( 'backend_cocoaagg' )
excludes.append ( 'Tkconstants'      )
excludes.append ( 'Tkinter'          )
excludes.append ( 'tcl'              )
excludes.append ( "_imagingtk"       )
excludes.append ( "PIL._imagingtk"   )
excludes.append ( "ImageTk"          )
excludes.append ( "PIL.ImageTk"      )
excludes.append ( "FixTk"            )

dll_excludes.append ( 'libgdk-win32-2.0-0.dll'  )
dll_excludes.append ( 'libgdk_pixbuf-2.0-0.dll' )
dll_excludes.append ( 'libgobject-2.0-0.dll'    )
dll_excludes.append ( 'tcl84.dll'               )
dll_excludes.append ( 'tk84.dll'                )
dll_excludes.append ( 'tclpip84.dll'            )


# seems not to be found (imported in brick.py)
# NOT USED ANYMORE includes.append ( 'PyLab_Works_properties' )

# ****** missing /not detected files *********
#   march 2008
#includes.append ( 'signal_workbench' )

#   6 april 2008
includes.append ( 'scipy.signal'     )
includes.append ( 'scipy.__config__' )

includes.append ( 'pygame.locals'    )

includes.append ( 'numpy'            )
##includes.append ( 'numarray' )
#includes.append ( 'numarray.Complex32' )
# ****** END missing /not detected files *********
"""
['AppKit', 'Foundation', 'PyObjCTools', 'StdSuites.Standard_Suite',
'__config__', '_curses', '_wxagg', 'aetools', 'backends.draw_if_interactive',
'backends.new_figure_manager', 'backends.show', 'brick', 'cairo', 'cairo.gtk',
'cephes', 'config.mplConfig', 'config.rcParams', 'config.rcdefaults', 'config.save_config',
'core.abs', 'core.max', 'core.min', 'core.round', 'dotblas', 'enthought.traits',
'enthought.traits.api', 'fcompiler.FCompiler', 'fcompiler.show_fcompilers', 'fltk',
'gobject', 'gtk', 'gtk.glade', 'lib.add_newdoc', 'maskedarray', 'mlab.amax', 'mlab.amin',
'numpy.dft.old', 'numpy.lib.mlab', 'numpy.linalg.old', 'objc', 'pango', 'pre', 'pyExcelerator',
'pyemf', 'run', 'startup', 'testing.NumpyTest', 'testing.ScipyTest', 'validate',
'numarray.Complex', 'numarray.Complex32', 'numarray.Complex64', 'numarray.Float',
'numarray.Float32', 'numarray.Float64', 'numarray.Int', 'numarray.Int16', 'numarray.Int32',
'numarray.Int8', 'numarray.NumArray', 'numarray.UInt16', 'numarray.UInt32', 'numarray.UInt8',
'numarray._dotblas', 'numarray.all', 'numarray.alltrue', 'numarray.asarray',
'numarray.conjugate', 'numarray.dot', 'numarray.fromlist', 'numarray.identity',
'numarray.libteacup', 'numarray.shape', 'numarray.transpose', 'numarray.typecode',
'numarray.zeros', 'numpy.Complex', 'numpy.Complex32', 'numpy.Complex64', 'numpy.Float',
'numpy.Float32', 'numpy.Float64', 'numpy.Int', 'numpy.Int16', 'numpy.Int32', 'numpy.Int8',
'numpy.UInt16', 'numpy.UInt32', 'numpy.UInt8', 'numpy.absolute', 'numpy.arccos',
'numpy.arccosh', 'numpy.arcsin', 'numpy.arcsinh', 'numpy.arctan', 'numpy.arctanh',
'numpy.bitwise_and', 'numpy.bitwise_or', 'numpy.bitwise_xor', 'numpy.cast', 'numpy.ceil',
'numpy.conjugate', 'numpy.core.absolute', 'numpy.core.add', 'numpy.core.bitwise_and',
'numpy.core.bitwise_or', 'numpy.core.bitwise_xor', 'numpy.core.cdouble',
'numpy.core.complexfloating', 'numpy.core.conjugate', 'numpy.core.csingle',
'numpy.core.divide', 'numpy.core.double', 'numpy.core.equal', 'numpy.core.float64',
'numpy.core.greater', 'numpy.core.greater_equal', 'numpy.core.inexact', 'numpy.core.intc',
'numpy.core.invert', 'numpy.core.isfinite', 'numpy.core.left_shift', 'numpy.core.less',
'numpy.core.less_equal', 'numpy.core.maximum', 'numpy.core.multiply', 'numpy.core.not_equal',
'numpy.core.power', 'numpy.core.remainder', 'numpy.core.right_shift', 'numpy.core.sin',
'numpy.core.single', 'numpy.core.sqrt', 'numpy.core.subtract', 'numpy.cosh', 'numpy.divide',
'numpy.e', 'numpy.fabs', 'numpy.float64', 'numpy.float_', 'numpy.floor', 'numpy.floor_divide',
'numpy.fmod', 'numpy.greater', 'numpy.hypot', 'numpy.inexact', 'numpy.int32', 'numpy.invert',
'numpy.isfinite', 'numpy.left_shift', 'numpy.less', 'numpy.log', 'numpy.logical_and',
'numpy.logical_not', 'numpy.logical_or', 'numpy.logical_xor', 'numpy.maximum',
'numpy.minimum', 'numpy.negative', 'numpy.not_equal', 'numpy.power', 'numpy.random.rand',
'numpy.random.randn', 'numpy.remainder', 'numpy.right_shift', 'numpy.sign', 'numpy.single',
'numpy.sinh', 'numpy.tan', 'numpy.tanh', 'numpy.true_divide', 'scipy.special.gammaln',
'wx.BitmapFromImage', 'wx.EmptyIcon']
"""


# ***********************************************************************
# ***********************************************************************



# If run without args, build executables, in quiet mode.
if len(sys.argv) == 1:
    sys.argv.append("py2exe")

#  console = ['PyLab_Works_mainform.py']  ,
setup (
  windows = ['PyLab_Works.py']  ,
  options = {
   'py2exe' : {
      'optimize'     : 0,
      'compressed'   : False,
      'skip_archive' : True,
      #'force_imports': True,
      'includes'     : includes,
      'excludes'     : excludes,
      'dll_excludes' : dll_excludes,
      'packages'     : packages,
               }},
  data_files = data_files
      )


#D:\data_to_test\jalspy>python setup.py py2exe

import subprocess
"""
result = subprocess.call (
  [ 'P:\Program Files\Inno Setup 4\Compil32.exe',
    '/cc',
    'D:\data_to_test\jalspy\PyLab_Works.iss'])
"""
print 'Starting INNO setup'
result = subprocess.call (
  [ 'P:\Program Files\Inno Setup 4\ISCC.exe',
    'D:\Data_Python_25\PyLab_Works\PyLab_Works.iss'])
print 'BUILD Windows',result==0, result

if (result==0) and Kill_Distro :
  for path in dist_paths :
    if File_Exists ( path ) :
      shutil.rmtree ( path )
  print 'piep'
