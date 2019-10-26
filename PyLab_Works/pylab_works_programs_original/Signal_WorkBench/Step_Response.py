step = ones(len(Hw_1))
step[0:10] = 0

SR_1 = signal.lfilter ( filt_1[0], filt_1[1], step )
SR_2 = signal.lfilter ( filt_2[0], filt_2[1], step )
SR_3 = signal.lfilter ( filt_3[0], filt_3[1], step )
SR_4 = signal.lfilter ( filt_4[0], filt_4[1], step )

DISPLAY = SR_1, SR_2, SR_3, SR_4
Display_Params = []
Display_Params.append ([ 'Ph(w)_1[pi*rad]', -1, 1 ])
Display_Params.append ([ 'Ph(w)_2[pi*rad]', -1, 1 ])
Display_Params.append ([ 'Ph(w)_3[pi*rad]', -1, 1 ])
Display_Params.append ([ 'Ph(w)_4[pi*rad]', -1, 1 ])
