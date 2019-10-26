#from scipy import *
from signal_workbench import *
import signal_workbench
reload ( signal_workbench ) 

# Example of Remez HighPass Filter design
fsamp = 100    # sample frequency [Hz]
fs    = 1.0    # stopband corner [Hz]
fp    = 5.0    # passband corner [Hz]
att_s = 40.0   # stopband attenuation [dB]
att_p = 0.0    # passband attenuation [dB]
Ntap  = 71     # number of filter taps
               #   must be ODD for bandpass filters
               #   must be EVEN for differentiators
                 
# transform user frequencies to relative Nyquist frequencies
ws = fs / fsamp
wp = fp / fsamp
bands = ( 0, ws, wp, 0.5 )

# transform logarithmic user gain to linear gain
gs = power( 10.0, -(att_s / 20))   
gp = power( 10.0, -(att_p / 20))
gain = (gs, gp)

# design the filter
filt_hp = signal.remez ( Ntap, bands, gain)
# add vector for denominator, to get a standard filter matrix (b,a)
filt_hp = ([ filt_hp, ones(1)])


print '======== FIR Filters through Remez ========'
print 'LowPass,  bands:', bands, 'gain:', gain
print 'HighPass, bands:', bands, 'gain:', gain
print ''

print 'Filter-1: Ntap = ',Ntap
Hw_1, Ph_1 = Calculate_Filter_Amplitude_Phase( filt_hp , 1)

DISPLAY = Hw_1, Ph_1

Display_Params = []
Display_Params.append (['H(w)[dB]',-90,10])
Display_Params.append (['phi[pi-rad]',-40,0])

#filt_1 = signal.remez(Ntap, bands_lp, gain_lp)
#filt_1 = ([ filt_1, ones(1)])
#Hw_1, Ph_1 = Calculate_Filter_Amplitude_Phase( filt_1 , 1)























