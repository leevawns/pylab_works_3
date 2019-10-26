from signal_workbench import *
import signal_workbench
reload ( signal_workbench ) 

print 'beer'
filename = 'D:/akto_yk/T3-patient/raw.txt'
filename = 'D:/akto_yk/T3-patient/675.txt'
filename = 'D:/akto_yk/_akto_minimod_sensewear/test_5-6/675.txt'

filename = 'D:/Data_actueel/D7_AktoTest/driehoek_vierkant_akto.txt'
Data = Read_New_Raw_Akto_File ( filename, True )

#filename = 'D:/akto_yk/_akto_minimod_sensewear/test8/test33_short.dat'
#filename = 'D:/akto_yk/_akto_minimod_sensewear/test-3/test32_short.dat'
#Data = Read_New_Akto_File ( filename, True )

#filename = 'D:/akto_yk/T3-patient/test31.dat'
#Data = Read_New_Akto_File ( filename, True )

print 'aap',Data
DISPLAY = Data [:3,:] 

Display_Params = []
Display_Params.append ([ 'X',   0, 450 ])
Display_Params.append ([ 'Z', -50, 400 ])
Display_Params.append ([ 'Y',  50, 500 ])

