Dirac = zeros ( len ( Hw_1 ) ) 
Dirac [50] = 1.0

hn_1 = signal.lfilter ( filt_1[0], filt_1[1], Dirac )
hn_2 = signal.lfilter ( filt_2[0], filt_2[1], Dirac )
hn_3 = signal.lfilter ( filt_3[0], filt_3[1], Dirac )
hn_4 = signal.lfilter ( filt_4[0], filt_4[1], Dirac )

DISPLAY = hn_1, hn_2, hn_3, hn_4
Display_Params = []
Display_Params.append ([ 'Ph(w)_1[pi*rad]', -1, 1 ])
Display_Params.append ([ 'Ph(w)_2[pi*rad]', -1, 1 ])
Display_Params.append ([ 'Ph(w)_3[pi*rad]', -1, 1 ])
Display_Params.append ([ 'Ph(w)_4[pi*rad]', -1, 1 ])
