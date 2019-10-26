from signal_workbench import *
import signal_workbench
reload ( signal_workbench ) 


#Test_Signal = Better_ECG
# Example of Remez HighPass Filter design
fsamp = 100    # sample frequency [Hz]
fs    = 1.0    # stopband corner [Hz]
fp    = 5.0    # passband corner [Hz]
att_s = 40.0   # stopband attenuation [dB]
att_p = 0.0    # passband attenuation [dB]
Ntap  = 70     # number of filter taps
               #   must be ODD for bandpass filters
               #   must be EVEN for differentiators

wp = fp / fsamp
ws = fs / fsamp

gp = power ( 10.0, -( att_p / 20 ) )   # 10.0 is essential for accuracy
gs = power ( 10.0, -( att_s / 20 ) )   

bands_lp = ( 0, 0.5-wp, 0.5-ws, 0.5 )
bands_hp = ( 0,     ws,     wp, 0.5 )

gain_lp = ( gp, gs )
gain_hp = ( gs, gp )


"""
print '======== FIR Filters through Remez ========'
print 'LowPass,  bands:', bands_lp, 'gain:', gain_lp
print 'HighPass, bands:', bands_hp, 'gain:', gain_hp
print ''


print 'Filter-1: Ntap = ',Ntap
filt_1 = signal.remez(Ntap, bands_lp, gain_lp)
filt_1 = ([ filt_1, ones(1)])
Hw_1, Ph_1 = Calculate_Filter_Amplitude_Phase( filt_1 , 1)


print 'Filter-2: Ntap = ',Ntap+1
filt_2 = signal.remez(Ntap+1, bands_lp, gain_lp)
filt_2 = ([ filt_2, ones(1)])
Hw_2, Ph_2 = Calculate_Filter_Amplitude_Phase( filt_2 , 1)

print 'Filter-3: Ntap = ',Ntap
filt_3 = signal.remez(Ntap, bands_hp, gain_hp)
filt_3 = ([ filt_3, ones(1)])
Hw_3, Ph_3 = Calculate_Filter_Amplitude_Phase( filt_3 , 1)

print 'Filter-4: Ntap = ',Ntap+1
filt_4 = signal.remez(Ntap+1, bands_hp, gain_hp)
filt_4 = ([ filt_4, ones(1)])
Hw_4, Ph_4 = Calculate_Filter_Amplitude_Phase( filt_4 , 1)

"""
print '======== HighPass Filter ========'
print 'Filter-1: IIR (Butterworth), 0.06*fn, -50dB'
#filt_3 = signal.cheby1(N, 1, Wn, btype='high')
filt_1 = signal.iirdesign( 0.06, 0.002, 1, 50, 0, 'butter')
Hw_1, Ph_1 = Calculate_Filter_Amplitude_Phase( filt_1 , 1)

print 'Filter-2: IRR (Chebychev-1), 0.06*fn, -50dB'
N,Wn = signal.cheb1ord(0.06, 0.002, 1, 50) #wp, ws, gp, gs)
filt_2 = signal.cheby1(N, 1, Wn, btype='high')
Hw_2, Ph_2 = Calculate_Filter_Amplitude_Phase( filt_2 , 1)

print 'Filter-3: FIR (Remez 25), 0.05*fN, -40dB'
#remez(numtaps, bands, desired, weight=None, Hz=1, type='bandpass', maxiter=25, grid_density=16)
filt_3 = signal.remez(25,(0,0.01,0.05,0.5),(0.01,1)) #,Hz=2)
filt_3 = ([ filt_3, ones(1)])
Hw_3, Ph_3 = Calculate_Filter_Amplitude_Phase( filt_3 , 1)

print 'Filter-4: FIR (Remez 25), 0.2*fN, -60dB'
filt_4 = signal.remez(25,(0,0.001,0.2,0.4),(0.001,1),(1,1)) #,Hz=2)
filt_4 = ([ filt_4, ones(1)])
Hw_4, Ph_4 = Calculate_Filter_Amplitude_Phase( filt_4 , 1)


DISPLAY = Hw_1, Hw_2, Hw_3, Hw_4
Display_Params = []
Display_Params.append ([ 'H(w)_1[dB]', -90, 10 ])
Display_Params.append ([ 'H(w)_2[dB]', -90, 10 ])
Display_Params.append ([ 'H(w)_3[dB]', -90, 10 ])
Display_Params.append ([ 'H(w)_4[dB]', -90, 10 ])


# and finally we've to define which signals to export
# and if we need it, the 2-points calibration values


# define passband and stopband frequencies [fraction of Nyquist frequency]
wp = 3.0 * 2/fsamp
ws = 0.1 * 2/fsamp
# define maximum passband and minimum stopband attenuation [dB]
gp = 1
gs = 40

"""
# print the filter parameters
print 'Filter-1: highpass,',wp,'*fNyquist,',-gs,'dB, IRR, Butterworth'
# calculate the filter
filt_1 = signal.iirdesign( wp, ws, gp, gs, ftype ='butter')
# calculate amplitude and phase response (with printing coefficients)
Hw_1, Ph_1 = Calculate_Filter_Amplitude_Phase( filt_1, Print_True)
"""
