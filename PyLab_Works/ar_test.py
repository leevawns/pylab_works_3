import __init__

from numpy import *
from array_support import *

# 1-dimensinal array: 1 Xt-signal of length 5
Ar1  = ones ( 5 )

# 2-dimensional array: 2 Xt-signals of length 4
Ar22 = array ( ( 4 * ones ( 4 ), 7 * ones ( 4 ) ) )






print Ar1.shape, Ar1
print Ar22.shape, Ar22



Data, MetaData = Analyze_TIO_Array ( Ar1, Ar22 )
print Data, MetaData
Data = Make_2dim_Array ( Data )
print Data

Data, MetaData = Analyze_TIO_Array ( Ar22, Ar1 )
print Data, MetaData
Data = Make_2dim_Array ( Data )
print Data


