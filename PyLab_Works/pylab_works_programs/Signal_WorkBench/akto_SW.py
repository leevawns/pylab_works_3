SW_Acc_MAD = sqrt ( Data_SW[8,:] * Data_SW[8,:] + Data_SW[9,:] * Data_SW[9,:] )
DISPLAY = SW_Energy, SW_Acc_MAD

Display_Params = []
Display_Params.append ([ 'Acc_MAD',  0, 10 ])
Display_Params.append ([ 'Akto' ,  0, 10 ])