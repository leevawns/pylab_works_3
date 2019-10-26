import __init__

# ***********************************************************************
from General_Globals import *
from  language_support import  _

_Version_Text = [

[ 1.1 , '5-09-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - added unpacking, to merge a tupple of unequal length elements)
""")],

[ 1.0 , '14-07-2007', 'Stef Mientki',
'Test Conditions:', (1,),
_(0, ' - orginal release')]

]
# ***********************************************************************


from numpy import *
#from utility_support import s_list



# ***********************************************************************
# ***********************************************************************
class class_MetaData ( object ) :
  def Get ( self, Attrib, Default ) :
    try :
      return getattr ( self, Attrib )
    except :
      return Default
# ***********************************************************************


"""
# ***********************************************************************
# ***********************************************************************
class t_signal_attr ( object ) :

  def __getattr__ ( self, attr ) :
    if not ( self.__dict__.has_key ( attr ) ) :
      self.__dict__[attr] = None
    return self.__dict__[attr]

  def Get ( self, Attrib, Default ) :
    try :
      return getattr ( self, Attrib )
    except :
      return Default
# ***********************************************************************
"""

# ***********************************************************************
# Joins all kind of signals to one 2-dimensional array
# Signals may be one of the following types,
# or any combination of these types
# and input signals may have different lengths (padded with zeros)
#   - tuple
#   - list
#   - vector  ( any direction )
#   - array   ( any orientation )
# The output array looks like this
"""
[[ 1  2  3  4  5]         <== signal 1
 [11 22 33 44 55]         <== signal 2
 [ 7  8  9 10 11]
 [ 1  2  3  0  0]]        <== signal 4, was only 3 elements long
"""
# ***********************************************************************
def Make_2dim_Array ( *args ):
  # unpack variables, sometimes it's tuple(tuple(data))
  # if we don't unpack and the elements have different sizes
  # the procedure won't work
  #while ( len(args) == 1 ) and ( type(args[0]) == tuple ) :
  #  args = args [0]
  while ( len(args) == 1 ) and ( type(args[0]) in ( list, tuple ) ) :
    args = args [0]

  # make a list, because a tuple can't be modified
  args = list ( args )

  result =[]
  max_size = 0
  for i,arg in enumerate ( args ) :
    #print 'TYPE',i,type(arg)
    # if list or tuple, make it a vector
    if type ( arg ) != ndarray :
      args [i] = array ( arg )

    # if a vector, make it a 2-dimensional array
    if args[i].ndim == 1 :
      args[i] = args[i].reshape (1,-1)
    
    # if first dimension is larger than second, transpose
    elif  args[i].shape[0] >  args[i].shape [1] :
      args[i] = transpose ( args[i] )

    # find the maximum of the last dimension
    max_size = max ( max_size, args[i].shape[-1] )

  # make all last dimensions equal, by adding zeros
  for i,arg in enumerate ( args ) :
    N = arg.shape[-1]
    if N < max_size :
      extend =  zeros ( ( arg.shape[0], max_size - N ), dtype=int )
      args[i] = hstack ( ( arg, extend ) )

  # now join all the arguments to
  # a homogenous 2-dimensional array
  result = args [0]
  for arg in args [1:] :
    result = vstack ( ( result, arg ) )

  #print
  #print 'input =',len(args), type(args[0]), args
  #print 'result=',type(result),result.shape, result
  return result
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Analyze_TIO_Array ( *args ) :
  """
Splits the given data (in the form of TIO_ARRAY)
into data and metadata.
The data may be specified in any order, like

  A, A, M, A
     or
  A, M, ( A, A ), (A, M )

where
  A = ndarray of any dimensions
  M = 1 set of MetaData

  """
  if not ( args ) :
    return

  # initalize the container elements
  data     = []
  metadata = []

  #************************************************
  #************************************************
  def parse_args ( arg ) :
    if isinstance ( arg, ndarray ) :
      data.append ( arg )
      return
    elif isinstance ( arg, class_MetaData ) :
      metadata.append ( arg )
      return
    else :
      for elem in arg :
        parse_args ( elem )
  #************************************************

  parse_args ( args )

  #make it 2-dimensional ???

  #v3print ( 'TIO_Array analyse:', len ( data ), len ( metadata ) )
  return data, metadata
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Analyze_TIO_Array_WEG ( *args ) :
  """
Splits the given data (in the form of TIO_ARRAY)
into data and metadata.
The data may be specified in any order,
the type of the indivual data elements,
determine what kind of information it represents.
  - array   : the real data to be used
  - integer : the dimension of the data
  - tupple  : metadata of 1 signal of the data
  - string  : title of the window
One-level of nesting of identical elements
( data and metadata only )
into tuples or lists is allowed.
In the latter case the type of the first element
of the tuple/list determines the type of information.
  """
  if not ( args ) :
    return
  
  # initalize the container elements
  data     = []
  metadata = []
  #data_dim = 1
  #title    = ''

  # unpack lists and tupples at the outer most level
  #exprint ( 'XXX0', len(args), type(args) )
  while args                and \
        ( len (args) == 1 ) and \
        ( type ( args ) in  ( list, tuple ) ) :
    args = args[0]
  #v3print ( 'XXX0', len(args), type(args) )
  if not ( args ) :
    return

  # For a single array, put it in a list
  if isinstance (args,ndarray):
    args = [args]

  for arg in args :
    #v3print ( 'TIO_Array Analysis.arg', type (arg),isinstance ( arg, ndarray ) )
    if isinstance ( arg, ndarray ) :
      data.append ( arg )
    elif isinstance ( arg, class_MetaData ) :
      metadata.append ( arg )
    else :
      for sub in arg :
        #v3print ( 'TIO_Array Analysis.sub', type (arg) )
        if isinstance ( sub, ndarray ) :
          data.append ( sub )
        elif isinstance ( sub, class_MetaData ) :
          metadata.append ( sub )

  #make it 2-dimensional ???

  # return the results
  #v3print ( 'TIO_Array analyse: len/dim/meta/title =', len(data), metadata )
  #return data, data_dim, metadata, title
  #v3print ( 'TIO_Array analyse:', len ( data ), len ( metadata ) )
  return data, metadata

# ***********************************************************************




  
# ***********************************************************************
# part from a table copied from an Excel sheet
# ***********************************************************************
SLICES = """
3660	4293	5098	5747	6540	7219	7978	8654
3717	4381	5151	5800	6590	7251	8034	8742
3658	4289	5097	5742	6300	6300	7976	8654
3835	4378	5255	5819	6720	7253	8135	8696
3832	4369	5249	5815	6713	7253	8129	8692
2433	2875	3873	4275	5306	5706	6692	7121
2211	2653	3659	4151	5096	5552	6533	7039
2270	2891	3708	4334	5163	5769	6610	7289
2297	2675	3798	4188	5179	5544	6619	7019
2518	3026	3965	4468	5405	5905	6837	7405
"""
# ***********************************************************************


# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':

  Test_Defs ( 4 )

  a_tuple = (7,8,9,10,11)
  a_list = [1,2,3,4,5]
  a_vector = array ( a_list )

  b_list = [11,22,33,44,55]
  b_vector = array ( b_list )

  a_array = array ( a_vector )
  b_array = array ( b_list )
  ab_array = vstack (( a_vector, b_vector ))

  # **********************************
  # **********************************
  if Test ( 1 ) :
    print (Make_2dim_Array ( a_tuple ))
    print(Make_2dim_Array ( a_list ))
    print(Make_2dim_Array ( a_vector ))
    print(Make_2dim_Array ( a_list,ab_array, a_tuple, a_list  ))

  # **********************************
  # **********************************
  if Test ( 2 ) :
    a_list2 = a_list [:-2]
    extend = Make_2dim_Array ( a_list,ab_array, a_tuple, a_list2  )
    print (extend)
    print (extend [ :, 2:4 ])

  #*********************************
  # Cut/Paste a selection from Excel
  #*********************************
  if Test ( 3 ) :
    pats = SLICES.split('\n')
    if len ( pats [ 0 ] ) == 0 :
      pats.pop ( 0 )
    if len ( pats [ -1 ]) == 0 :
      pats.pop ()
    for i in range ( len ( pats ) ) :
      pats[i] = pats[i].split()
      print (i, pats[i])
      
    pat_slice = array ( pats [0] ).astype ( int )
    print (pat_slice)

  # **********************************
  # Array, Numpy-Array, S_Array
  # **********************************
  if Test ( 4 ) :
    a = []
    for i in range ( 10 ) :
      a.append (i)
    v3print ( '  List', type(a), a )

    b = array ( [1,2,3] )

    e = MetaData ()
    e.Frequency = 14400
    
    f = MetaData ()
    
    v3print ( a )
    v3print ( b )
    v3print ( e, e.Frequency,e .Get ( 'Frequency', 20 ) )
    v3print ( f, f.Get ( 'Frequency', 1000) )
    
    A = a,a,e,b,f
    
    
    for x in A :
      v3print ( type(a) )
      

    v3print ( A )
    
    



# ***********************************************************************
pd_Module ( __file__ )
