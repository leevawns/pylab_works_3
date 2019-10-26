from signal_workbench import *
import signal_workbench
reload ( signal_workbench ) 

filename = 'D:/akto_yk/ActivePAL/thomas_smk.dat'
Data_Akto = Read_New_Akto_File ( filename, True )

filename = 'D:/akto_yk/ActivePAL/activepalthomas.csv'
Data_PAL = Read_ActivePAL ( filename, 1200 ) 

DISPLAY = Data_Akto[ 0, 1378: ], Data_PAL 
Display_Params = []
Display_Params.append ( [ 'Akto', 0, 700 ] )
Display_Params.append ( [ 'PAL' , 0, 50  ] )

