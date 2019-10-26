from scipy import *   # you may not use "scipy."
import scipy          # you have to use "scipy."


#*************************************************************************
class BP_analysis:
  """ Analysis a bloodpressure wave
  
  USAGE:
    
# create a bloodpressure analyse instance
BP_analyse = bloodpressure_analysis (len(IOI), fsamp)

# perform an analysis
BP_analyse.execute(IOI)

# do something with the results
History.execute (
  BP_analyse.BP_Filtered(),
  BP_analyse.BP_Sys(),
  BP_analyse.BP_Dias(),
  BP_analyse.BP_MAP(),
  BP_analyse.BP_HR(),
  BP_analyse.BP_RR(),
  BP_analyse.BP_diff()
  )
  """
  
  def __init__ (self, fsamp):
    self.fsamp = fsamp
    
    #*************************************************************************
    # define the BloodPressure filter
    # filter length of 10 is determined empirically
    #*************************************************************************
    filter_alfa = 2 * pi * 8 / fsamp
    #filter_alfa = 2 * pi * 5 / fsamp
    filter_a = [1, filter_alfa-1]
    filter_b = filter_alfa
    #self.BP_filter = chunk_filter (filter_b, filter_a, 10)
    #b = 0.1
    #a = b - 1
    #self.BP_filter = Continous_Filter ( filter_b, filter_alfa-1 )
    self.BP_filter = Continous_Filter ( filter_b, filter_a )
    #*************************************************************************

    #*************************************************************************
    # here we create a bloodpressure derivation filter
    # we use average sloop method, because
    #   - it's a very easy filter
    #   - it combines low pass filter with derivate calculation
    # define the filter length
    #   for 100Hz sampling 3(*3) works well
    len3 = 4
    average_sloop = (r_ [ ones(len3), zeros(len3), -1 * ones(len3) ]) / (3.0 * len3)

    #self.BP_difference = chunk_filter ( average_sloop, 1.0, 3 * len3 )
    self.BP_difference = Continous_Filter ( average_sloop, 1.0 )
    #print aap
    #*************************************************************************

    #*************************************************************************
    self._detect_prev = False    # assure, no detection on the first sample
    self._Min_prev    = 0
    self._Max_prev    = 0
    self._Mean_prev   = 0
    self._RR_prev     = 1

    self._Dias_prev   = 0
    self._Sys_prev    = 0
    self._new_RR      = 0
    self._Sum_prev    = 0

    self.P_Dias       = zeros ( fsamp )
    self.MAP          = zeros ( fsamp )
    self.P_Sys        = zeros ( fsamp )
    self.RR           = zeros ( fsamp )
    
    self.P_Filtered   = zeros ( fsamp )
    self.P_diff       = zeros ( fsamp )
    self._peaks       = zeros ( fsamp )
    
    self.Input        = []
    self.OUT_p        = 0
    #*************************************************************************

  def HR_min      (self,value): self.HR_min      = value
  def HR_max      (self,value): self.HR_max      = value
  def PSys_min    (self,value): self.PSys_min    = value
  def PSys_max    (self,value): self.PSys_max    = value
  def PDias_min   (self,value): self.PDias_min   = value
  def PDias_max   (self,value): self.PDias_max   = value
  def LowPass     (self,value): self.LowPass     = value
  def Treshold    (self,value): self.Treshold    = value
  def Filter_50Hz (self,value): self.Filter_50Hz = value

  def BP_Filtered (self): return self.P_Filtered
  def BP_Sys      (self): return self.P_Sys
  def BP_Dias     (self): return self.P_Dias
  def BP_MAP      (self): return self.MAP
  def BP_HR       (self): return self.fsamp / self.RR
  def BP_RR       (self): return self.RR
  def BP_diff     (self): return self.P_diff

  def execute ( self, BP_in ):
    NIN = len ( BP_in )
    #print 'NIN',NIN , len ( self.Input )
    
    for sample in BP_in :
      #print 'sample',sample
      # append each sample to the input list
      self.Input.append ( sample )
      
      if len ( self.Input ) == self.fsamp :

        # make an array of the input list and clear the list
        BP = array ( self.Input )
        self.Input = []

        # move what we've already calculated into the output buffer
        OUT_P_Sys      = self.P_Sys           [ self.OUT_p : ].copy()
        OUT_P_Dias     = self.P_Dias          [ self.OUT_p : ].copy()
        OUT_MAP        = self.MAP             [ self.OUT_p : ].copy()
        OUT_RR         = self.RR              [ self.OUT_p : ].copy()
        OUT_P_Filtered = self.P_Filtered      [ self.OUT_p : ].copy()
        NIN -= ( self.fsamp - self.OUT_p )
        self.OUT_p = 0

        try:
          # filter the bloodpressure signal
          self.P_Filtered = self.BP_filter.execute( BP )

          # average sloop difference on the bloodpressure
          self.P_diff = self.BP_difference.execute( BP )

          # BP_detect = (Derivate>0) AND (Signal>TresHold)
          BP_detect = ( self.P_diff > 0 )   &   ( self.P_Filtered > 75000 )
          #BP_detect = ( self.P_diff > 0 )   &   ( self.P_Filtered > 100 )

          # find falling edges = peak position and
          # save last detection point for next chunk
          detect = r_[ ([ self._detect_prev ]) , BP_detect[:-1] ]  &  ~BP_detect
          self._detect_prev = BP_detect[-1]

          # determine the peak indices,
          # because .nonzero returns a tupple, we take the first element of the tuple
          # because we will add an element at the beginning of the signals
          #   we have to shift the peaks 1 place to the right
          # because for end-slice-indexing, it's easier to have "i+1"
          #   so we shift an extra place to the right
          self._peaks = r_[ (detect).nonzero()[0], ([len(BP)]) ] + 1

          # generate signals to determine min, mean, max
          # the signal are composed by the specific value from the previous session
          # and the newly filtered signal from this session
          _signal_for_min = r_[ ([self._Min_prev]), self.P_Filtered ]
          _signal_for_sum = r_[ ([self._Sum_prev]), self.P_Filtered ]
          _signal_for_max = r_[ ([self._Max_prev]), self.P_Filtered ]

          # prepare the values for the loop
          self._Min_prev = self._Dias_prev
          self._Max_prev = self._Sys_prev

          prev_i = 0
          for i in self._peaks :
            # generate the signals
            self.P_Dias [ prev_i : i ] = self._Min_prev
            self.P_Sys  [ prev_i : i ] = self._Max_prev
            self.MAP    [ prev_i : i ] = self._Mean_prev
            self.RR     [ prev_i : i ] = self._RR_prev

            # calulate the new values
            if i < self._peaks[-1]:
              self._Sum_prev  = sum ( _signal_for_sum [ prev_i : i ])
              self._RR_prev   = self._new_RR + i - prev_i
              self._Mean_prev = self._Sum_prev / self._RR_prev
              self._new_RR    = 0
            else:
              self._Dias_prev = self._Min_prev
              self._Sys_prev  = self._Max_prev
              self._Sum_prev  = sum ( _signal_for_sum [ prev_i : i ])
              self._new_RR    = self._new_RR + i - prev_i - 1

            self._Min_prev = min ( _signal_for_min  [ prev_i : i ] )
            self._Max_prev = max ( _signal_for_max  [ prev_i : i ] )

            # update lower index
            prev_i = i
        except:
          print 'range=',prev_i,i,len(_signal_for_min)

    N = len ( BP_in )

    # extend the return buffer
    if NIN > 0 :
      old_p = self.OUT_p
      self.OUT_p += NIN
      # in case the boundary is crossed, we should add the missing part
      if NIN < N:
        OUT_P_Sys      = r_[ OUT_P_Sys, self.P_Sys   [ old_p : self.OUT_p]]
        OUT_P_Dias     = r_[ OUT_P_Dias, self.P_Dias [ old_p : self.OUT_p]]
        OUT_MAP        = r_[ OUT_MAP, self.MAP       [ old_p : self.OUT_p]]
        OUT_RR         = r_[ OUT_RR, self.RR         [ old_p : self.OUT_p]]
        OUT_P_Filtered = r_[ OUT_P_Filtered, self.P_Filtered [ old_p : self.OUT_p]]
      else :
        OUT_P_Sys      = self.P_Sys           [ old_p : self.OUT_p]
        OUT_P_Dias     = self.P_Dias          [ old_p : self.OUT_p]
        OUT_MAP        = self.MAP             [ old_p : self.OUT_p]
        OUT_RR         = self.RR              [ old_p : self.OUT_p]
        OUT_P_Filtered = self.P_Filtered      [ old_p : self.OUT_p]

    OUTPUT = r_ [ OUT_P_Sys,
                  OUT_P_Dias,
                  OUT_MAP,
                  60 * self.fsamp / OUT_RR,
                  OUT_RR,
                  OUT_P_Filtered ].reshape ( 6, N )

    #print 'OUT',OUTPUT, OUTPUT.shape
    return OUTPUT
  
  def Get_Signal_Names ( self ) :
    return [ 'Psys', 'Pdias', 'MAP', 'BPM', 'RR', 'BP-filt' ]
  
#*************************************************************************


#*************************************************************************
class chunk_generator_sine:
  """ Generates a chunked sinewave signal with random noise.

  USAGE:
SineWave = chunk_generator_sine ( N_sine, len(Signal) )
SineWave = chunk_generator_sine ( N_sine, len(Signal), 20000, 2, 0.2 )
Signal = SineWave.execute()
  """

  def __init__ (self, Nsine, length = 100, amplitude = 1, base = 0, noise = 0 ):
    self.Nsine     = Nsine       # number of sines in a chunk
    self.length    = length + 1  # length of the chunk [samples]
    self.amplitude = amplitude   # amplitude of sine (and base)
    self.base      = base        # base or offset
    self.noise     = noise       # noise factor
    self.NR        = 0

  def execute (self):
    signal = self.amplitude * (
                self.base +
                self.noise * rand(self.length) +
                sin( linspace ( 2 * pi * ( self.NR     ) * self.Nsine,
                                2 * pi * ( self.NR + 1 ) * self.Nsine,
                                self.length )))
    self.NR += 1
    # to get nice concatenation, we've generated 1 sample too much
    return  ( signal [:-1] )
#*************************************************************************



#*************************************************************************
class chunk_filter:
  """  CHUNK replacement for "signal.lfilter"
  """
  
  def __init__ (self, coef_b, coef_a, history_len):
    self.coef_a = coef_a
    # be sure coef_b is an array
    if isscalar ( coef_b ) :self.coef_b = [coef_b]
    else                   :self.coef_b = coef_b
    self.history = zeros(history_len)

  def execute (self, Signal_IN):
    # add the history part to the beginning of the current signal
    Extended_Signal = r_ [self.history, Signal_IN]
    #print 'Extended',Extended_Signal

    # store the last part of the current signal for the next calculation
    self.history =  Extended_Signal [ len(Signal_IN) : ]
    #print 'History',self.history

    # perform the filtering
    Extended_Signal = signal.lfilter (self.coef_b, self.coef_a, Extended_Signal)
    #print 'Result',Extended_Signal

    # skip the first part, because the filter isn't fully active there
    # and we need to asure that the IO length remains constant
    Signal_OUT = Extended_Signal [ len(self.history) : ]
    return (Signal_OUT)
#*************************************************************************


#*************************************************************************
class chunk_accumulate:
  """
  Accumulates any number of array chunks.
  Each time the execute function is called,
    the new arrays are added to the history.
  The arrays don't have to be of the same length,
    although normally the will be of the same length.
  Each time the execution function is called,
    not all parameters need to be preset,
    although normally they will all be present.
    
  USAGE:
History = chunk_accumulate()          # create an instance
History.execute( Signal1, Signal2 )   # accumulate the data (caled more than once)
plot( History.accumulated(0),'r')     # use the accumulated data
plot( History.accumulated(1),'r')
  """
  
  def __init__ (self):
    self.N = 1
    self.sequence = []

  def accumulated (self, index):
    return  self.sequence[index]

  def execute (self, *args):
    # if number of history elements too small, increase it
    if self.N < len(args):
      for i in range ( self.N, len(args)+1 ):
        self.sequence.append([])
      self.N = len(args)

    # add new array to the history
    for i in range(self.N):
      self.sequence[i] = r_ [ self.sequence[i], args[i] ]
#*************************************************************************


#*************************************************************************
def plot_list(mylist):
  # KAN NIET MET PY2EXE:  from pylab import plot, legend, show, hold
  default_color = ('r','b','c','m','g','y','k')

  legends = []
  hold(True)

  for i,item in enumerate(mylist):
    if len(mylist[i]) >= 4: color = mylist[i][3]
    else:                   color = default_color[ i % len(default_color) ]
    if len(mylist[i]) >= 3: mask = mylist[i][2]
    else:                   mask = 1
    if len(mylist[i]) >= 2: name = mylist[i][1]
    else:                   name = 'Signal-' + str(i)

    if mask > 0:
      plot( mylist[i][0], color)
      legends.append( name )

  legend(legends)
  hold(False)
  show()
#*************************************************************************


#*************************************************************************
class chunk_plot:
  """
  Plots a number of arrays.
  Input can be: list of arrays, tupple of arrays, individual arrays
  Color and Legends are set by default, but can be changed.
  
  USAGE:
Plot = chunk_plot()
Plot.color = ('k','k','k','m','g','y','k')
Plot.legend = ('aap','beer','coala')
Plot.plot ( History.accumulated(0),
             History.accumulated(1),
             History.accumulated(2),
             History.accumulated(3) )

  """
  def __init__(self):
    self.color  = ('r','b','c','m','g','y','k')
    self.legend = []
    self.mask   = []
    #for i in range(len(self.color)): self.legend = self.legend + ['Signal-'+str(i)]

  def colors (self, color) : self.color  = color
  def legend (self, legend): self.legend = legend
  def mask   (self, mask)  : self.mask   = mask

  def plot(self, *args):
    # KAN NIET MET PY2EXE: from pylab import plot, legend, show, hold
    if type(args[0])  in [list, tuple]: mylist=args[0]
    else:                               mylist=args

    # check if there enough legends and masks
    ii = len(mylist) - len(self.mask)
    for i in range(ii) : self.mask.append(1)
    ii = len(mylist) - len(self.legend)
    for i in range(ii) : self.legend.append('Signal-' + str(len(self.legend)+1))
    hold(True)

    # both statements work
    #for all in zip(list, color):  plot(*all)
    legends = []
    for i,item in enumerate(mylist):
      if self.mask[i] > 0:
        plot( item, self.color[ i % len(self.color) ])
        legends.append( self.legend[i] )

    legend(legends)
    hold(False)
    show()
    
#*************************************************************************



"""
#*************************************************************************
# CHUNK replacement xfor "signal.lfilter"
#*************************************************************************
def chunk_Filter2 (coef_b, coef_a, Signal_IN, Signal_Prev):
  # add the previous part to the beginning of the current signal
  Extended_Signal = r_ [Signal_Prev, Signal_IN]

  # store the last part of the current signal for the next calculation
  Signal_Prev =  Extended_Signal [ len(Signal_IN) : ]

  # perform the filtering
  Extended_Signal = signal.lfilter (coef_b, coef_a, Extended_Signal)

  # skip the first part, because the filter isn't fully active there
  # and we need to asure that the IO length remains constant
  Signal_OUT = Extended_Signal [ len(Signal_Prev) : ]
  return (Signal_OUT, Signal_Prev)
#*************************************************************************

# ===== USAGE =====

# create the filter coefficients
BP_average_len = 3
BP_average = (r_ [ ones(BP_average_len), zeros(BP_average_len),
              -1 * ones(BP_average_len) ]) / (3.0 * BP_average_len)

# we need to define a previous part of the correct length
# because the first time, this previous part is used on the right side of an assignment
BP_Average_prev = zeros( 3 * BP_average_len )

# execute the function
dBP_dt2, BP_Average_prev = chunk_Filter2 (BP_average, 1, IOI, BP_Average_prev)

# ===== USAGE =====

BP_filter_alfa = 2 * pi * 8 / 100
BP_filter_len = 10
BP_filter_a = ( [1, BP_filter_alfa-1] )
BP_filter_b = ( [BP_filter_alfa] )
BP_filter_prev = zeros( BP_filter_len )

"""


#*************************************************************************
"""
The filter function is implemented as a direct II transposed structure.
This means that the filter implements

a[0]*y[n] = b[0]*x[n] + b[1]*x[n-1] + ... + b[nb]*x[n-nb]
                      - a[1]*y[n-1] - ... - a[na]*y[n-na]
                      
At this moment a[0] is ignored and assumed to be equal 1.
"""
#*************************************************************************
class Continous_Filter:

  # coef_a contains as a first value "a[0]=1" (the result factor)
  def __init__ ( self, coef_b, coef_a ):
    if isscalar ( coef_a ) : self.coef_a = None
    else :
      # be sure coef_a is an array (otherwise we can't make it negative)
      if not ( isinstance ( coef_a, ndarray ) ) :
        # and remove the first element a[0] * Result =
        if len ( coef_a ) == 1 :
          self.coef_a = None
        else :
          coef_a = array ( coef_a )
          self.coef_a = -coef_a[1:]

    if isscalar ( coef_b ) :self.coef_b = array ( [coef_b] )
    else                   :self.coef_b = coef_b

    # create history buffers for X and Y
    self.x = zeros ( len ( self.coef_b ) )
    if self.coef_a : self.y = zeros ( len ( self.coef_a ) )
    
  # ******************************************************
  # direct execution, no explicit delay
  # ******************************************************
  def execute (self, Signal_IN):
    # initialize the final result
    Signal_OUT = zeros (0)
    # be sure Signal_IN is iterable
    if isscalar ( Signal_IN ) : x_new = array([Signal_IN ] )
    # now step through all new input samples
    for x_new in Signal_IN :
      # add a new sample and let the oldest sample out
      self.x = r_ [ self.x [1:], x_new ]
      if self.coef_a :
        # process the IIR filter
        y_new = dot ( self.coef_a, self.y ) + dot ( self.coef_b, self.x )
        # add the new value and let the oldest value out
        self.y = r_ [ self.y [1:], y_new ]
      else :
        y_new = dot ( self.coef_b, self.x )
      # add the new value to the final result
      Signal_OUT = r_ [ Signal_OUT, y_new ]

    return (  Signal_OUT )
#*************************************************************************


# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  # LowPassFilter
  #   Ynew = b * [Xold,X]  + ( 1 - b ) * Yold
  b = 0.1
  a = b - 1
  BP_filter = Continous_Filter ( b, a )

  len3 = 4
  average_sloop = (r_ [ ones(len3), zeros(len3), -1 * ones(len3) ]) / (3.0 * len3)
  BP_filter = Continous_Filter ( average_sloop, 1.0 )

  # test a Step function
  Signal = ones (100 )
  
  # calculate the step response
  Filtered = BP_filter.execute ( Signal )
  print Filtered
  print shape(Filtered)


  len3 = 4
  average_sloop = (r_ [ ones(len3), zeros(len3), -1 * ones(len3) ]) / (3.0 * len3)
  BP_filter = chunk_filter ( average_sloop, 1.0, 3 * len3 )

  # test a Step function
  Signal = ones (100 )

  # calculate the step response
  Filtered = BP_filter.execute ( Signal )
  print Filtered
  print shape(Filtered)
