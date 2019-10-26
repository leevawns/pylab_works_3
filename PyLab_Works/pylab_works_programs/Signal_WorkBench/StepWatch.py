from signal_workbench import *
import signal_workbench
reload ( signal_workbench ) 

filename = 'D:/akto_yk/StepWatch/Sandra.dat'
Data_Akto = Read_New_Akto_File ( filename, True )

filename = 'D:/akto_yk/StepWatch/Sandra.tab'
Data_StepWatch = Read_StepWatch ( filename, compression = 1200 )
#print 'STEP',Data_StepWatch.shape #[ : 10]

DISPLAY = Data_Akto[ 0, 963: 2000], Data_StepWatch
#DISPLAY = Data_Akto[ 0, : ], Data_StepWatch
Display_Params = []
Display_Params.append ( [ 'Akto',       0, 700 ] )
Display_Params.append ( [ 'StepWatch' , 0, 700  ] )

