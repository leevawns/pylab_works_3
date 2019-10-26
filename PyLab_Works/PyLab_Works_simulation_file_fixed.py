import PyLab_Works_Globals as PG
from numpy import *

#PG.Bricks[0].Exec()
#PG.Bricks[1].Out.Receivers[1] [ PG.Bricks[0] ] = ( 'In', 1 )
#PG.Bricks[1].Exec()


PG.Bricks[0].Exec()

PG.Bricks[1].Out.Receivers[1] [ PG.Bricks[2] ] = ( 'In', 1 )

#PG.Bricks[1].Out.Receivers[1] [ PG.Bricks[2] ] = ( 'In', 1, PG.Bricks[2].In.IO_Par[1].SetValue  )
#      C = self.In.IO_Par [ indx ]
#      if C :
#        # if so, send change to control
#        C.SetValue ( Value )
PG.Bricks[1].Exec()
#PG.Bricks[2].Input_Changed[1] = PG.Bricks[1].Output_Changed[1]
#PG.Bricks[2].In[1] = PG.Bricks[1].Out[1]

PG.Bricks[2].Out.Receivers[1] [ PG.Bricks[0] ] = ( 'In', 1 )

PG.Bricks[2].Exec()
#PG.Bricks[0].Input_Changed[1] = PG.Bricks[2].Output_Changed[1]
#PG.Bricks[0].In[1] = PG.Bricks[2].Out[1]

