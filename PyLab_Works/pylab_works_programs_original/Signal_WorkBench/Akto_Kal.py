from signal_workbench import *
import signal_workbench
reload ( signal_workbench ) 

AktoNr = '743'
filename = 'D:/akto_yk/Kalibratie_V5/kal_'+ AktoNr + '.dat'
Data_Akto, Reset = Read_New_Raw_Akto_Kal_File ( filename, True)

DISPLAY = Data_Akto
Display_Params = []
low  = 90
high = 160
Display_Params.append ( [ 'X' , low, high ] )
Display_Params.append ( [ 'Z-'+AktoNr , low, high ] )
Display_Params.append ( [ 'Y' , low, high ] )

