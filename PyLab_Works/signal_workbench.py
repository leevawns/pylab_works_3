import __init__
from General_Globals import *

"""# ***********************************************************************
import sys
subdirs = [
  '../support',
  ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
# ***********************************************************************
"""
from  language_support import  _

# ***********************************************************************
_Version_Text = [

[ 1.1 , '04-09-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - Read_SenseWear_Tab_File, extended with Sample_Reduction argument
 - Read_SenseWear_Tab_File, improved print info (including missing samples)
""")],

[ 1.0 , '14-07-2007', 'Stef Mientki',
'Test Conditions:', (1,),
_(0, ' - orginal release')]

]
# ***********************************************************************


from scipy import signal #*   # you may not use "scipy."
from numpy import *
import os             # filesize
from struct import *  # pack
from datetime import *
import configparser   # inifile handling

from file_support    import File_Exists, Find_Files
from inifile_support import *

# some global constants
Print_True = 1


"""
There are 2 ways for accessing DataAcquisiton files:
1. Directly read/write all the data,
   special suited for datasets, that can read/write in one stream.

2. Read/write the data (and metadata) from a read-object,
   specially suited for large datasets, where data is read/write in chunks.

Method 1 example:
  Data = Read_Signal_File('d:\data_to_test\output_data.c1')
  Write_Signal_File (Data,'d:\data_to_test\output_data.py_2')

  # or, for getting the sample frequency
  Data, fSamp = Read_Signal_File_Ext('d:\data_to_test\output_data.c1')
  Write_Signal_File_Ext (Data, fSamp, 'd:\data_to_test\output_data.py_2')

  # in both cases Nchan and Nsamp can be calculated from the array dimensions
  Nsamp = data.shape[0]
  Nchan = data.shape[1]

Method 3 example:
  DataFile = Signal_File('d:\data_to_test\output_data.c1')
  Data = DataFile.Read_Data()
  Sample_Frequency = DataFile.fSamp
  Nchan = DataFile.Nchan
  
  DataFile = Signal_File('d:\data_to_test\output_data.c1')
  DataFile.Write_Header(Nchan, fSamp)
  DataFile.Write_Data(Data, false)
  DataFile.Close()
"""

class Signal_File:
  """ Object to read / write DataAcquisition data files,
  build according MID-Poly format (at this moment only version 8 is supported)
  """
  def __init__ (self, filnam):
    self.filename = filnam
    self.header   = False
    
  def Read_Header (self):
    self.datafile = open(self.filename,'rb')       # Readonly Binary
    self.ID_len   = self.datafile.read(1)
    self.ID       = self.datafile.read(8)
    self.version  = fromfile(self.datafile, dtype=int16, count=1)[0]
    self.Nchan    = fromfile(self.datafile, dtype=int  , count=1)[0]
    self.fSamp    = fromfile(self.datafile, dtype=int  , count=1)[0]
                    # int is necessary to prevent the return of a LONG !!
    if self.version == 8 : Var_Size = 4
    else:                  Var_Size = 8
    self.Nsamp    = int((os.path.getsize(self.filename)-19) /Var_Size /self.Nchan)
    self.header   = True

  def Close (self):
    self.datafile.close()

  def Read_Data (self, close = True):
    if not(self.header): self.Read_Header()
    
    # data will be positioned in a 2-dimensional array [ chan_nr, sample]
    """
    if self.version == 8:
      self.data = fromfile(self.datafile, dtype=int ,count=-1)
    else:
      self.data = fromfile(self.datafile, dtype=float ,count=-1)
    """
    if self.version == 8: Var_Type = int
    else:                 Var_Type = float
    self.data = fromfile(self.datafile, dtype=Var_Type ,count=-1)

    self.data = self.data.reshape(size(self.data)/self.Nchan ,self.Nchan)
    self.data = transpose(self.data)

    if close: self.Close()
    return  self.data
    
  def Write_Header (self, Nchan = 1, fSamp = 100):
    self.datafile = open(self.filename,'wb')
    self.datafile.write(pack('c','\x08'))  # length ID-string
    self.datafile.write('MID-poly')        # ID-string
    self.datafile.write(pack('h',9))       # file version
    self.datafile.write(pack('i',Nchan))
    self.datafile.write(pack('i',fSamp))
    #print('test=',Nchan,fSamp)
    self.header = True
    
  def Write_Data (self, Data, close = True):
    if not(self.header):
      # special case, vectors have only 1 dimension
      if Data.ndim == 1: Nchan = 1
      else: Nchan = Data.shape[0]
      self.Write_Header(Nchan)

    Data = transpose(Data)
    Data.tofile (self.datafile)
    if close: self.Close()


# FUNCTIONS *******************************************************************
def Read_Signal_File (filename):
  DataFile = Signal_File(filename)
  return  DataFile.Read_Data()

def Read_Signal_File_Ext (filename):
  DataFile = Signal_File(filename)
  return  DataFile.Read_Data(), DataFile.fSamp

def Write_Signal_File (Data, filename):
  DataFile = Signal_File(filename)
  DataFile.Write_Data (Data)

# same as Write_Signal_File, but also fsamp can be specified
def Write_Signal_File_Ext (Data, fSamp, filename):
  DataFile = Signal_File(filename)
  DataFile.fSamp = fSamp
  DataFile.Write_Data (Data)


# ******************************************************************************
# Read aktometer datafile "filename",
#   if "Print_Info" True, will print header information
# returns
#   data_all     = all recorded days
#   data_OK      = all not-skipped days
#   data_SatSun  = all Saterday/Sundays (of not-skipped days)
#   data_Week    = all week days (of not-skipped days)
# ******************************************************************************
def Read_Akto_File (filename, Calibrated = True, Print_Info = False, Raw = False):
  data, data_ok1, data_zazo, data_week, gain0, offset0 = \
    Read_Akto_File_extra (filename, Calibrated, Print_Info, Raw)
  return data, data_ok1, data_zazo, data_week

# gives extra parameters back for Lonneke yking
def Read_Akto_File_extra (filename, Calibrated = True, Print_Info = False, Raw = False):
  """
  ActiLog V3.0
  22-06-06           // end date
  08:53:26           // end time
  07-06-06           // start date
  13:37:49           // start time
  5 skip 15358
  v 1354a    Thijssen,cgtvm,ak85,do    18-09-8185
  data:
  """

  def Read_Next_Line():
    line = Datafile.readline().rstrip("\n")
    if Print_Info: print (line)
    return line
  
  def Add_Day(Series, New):
    if (Series.ndim == 1) and (Series.shape[0] == 0):
      Series = New
    else: Series = vstack((Series, New))
    return Series

  Datafile = open(filename,'r')       # Readonly
  Read_Next_Line()                    # "ActiLog V3.0"
  date_str = Read_Next_Line()         # end date
  end_date = date( 2000+int(date_str[6:]), int(date_str[3:5]), int(date_str[0:2]))

  Read_Next_Line()                    # end time

  date_str = Read_Next_Line()         # start date
  start_date = date( 2000+int(date_str[6:]), int(date_str[3:5]), int(date_str[0:2]))
  zazo = start_date.weekday()         # 5,6 = Saterday / Sunday
  ndays = (end_date-start_date).days

  time_str = Read_Next_Line()         # start time
  time_5min = 12 * int(time_str[0:2]) + int(time_str[3:5]) // 5

  skip = Read_Next_Line()             # "5 skip 15358" (need not to be present)
  if len(skip)>7:
    skip = int(skip[7:])
  else: skip = 0

  akto_line = Read_Next_Line()        # "v 1354a    Thijssen,cgtvm,ak85,do    18-09-8185"
                                      # "m 0006     set2proef,za              2-2-05  157"
                                      #  012345678901234567890123456789012345678901234XXX
  akto_line = akto_line [45:].strip()
  akto_nr = int(akto_line)
  Read_Next_Line()                    # "data:"

  # get calibration values  MOET NOG CHANGE DIRECTION !!!
  cal_file = ConfigParser.ConfigParser()
  cal_file.readfp(open('D:/data_to_exe/v3yk.ini'))
  gain1 = cal_file.getint(akto_line,'gain1') /100.0
  gain2 = cal_file.getint(akto_line,'gain2') /100.0
  offset1 = cal_file.getint(akto_line,'offset1')
  offset2 = cal_file.getint(akto_line,'offset2')

  snijpunt = 150
  """
  if gain2<>gain1:
    snijpunt = (offset1-offset2)/((1/gain2)-(1/gain1))
    print 'snijpunt=',snijpunt
  """
  if Print_Info: print ('gain12/offset12/snijpunt=',gain1,gain2,offset1,offset2,snijpunt)

  # read the sampled data
  data_all = fromfile(Datafile, dtype=int ,count=-1, sep='\n')

  # akto calibration
  if Calibrated:
    for i in range(0,len(data_all)):
      #old = data_all[i]
      if data_all[i] < snijpunt : data_all[i] = data_all[i]/gain1 - offset1
      else: data_all[i] = data_all[i]/gain2 - offset2
      #print old,data_all[i]
  data_all = clip(data_all,0,600)

  # add begin and end correction so we get a whole number of days
  if not Raw:
    data_all = r_ [ zeros( time_5min ), data_all]
  else: print ('OOOO')
  end_corr = zeros ( 288 * (len(data_all)//288.0 +1) - len(data_all) )
  data_all = r_ [ data_all, end_corr ]

  # convert to Signal WorkBench signals-array
  data_all = data_all.reshape(size(data_all)/288 ,288)

  Datafile.close()

  data_OK   = array([])
  data_SatSun = array([])
  data_Week = array([])
  for i in range(0, ndays):
    if skip & 1: 
      data_OK = Add_Day(data_OK, data_all[i])
      if ((zazo + i)%7) >= 5:
        data_SatSun = Add_Day(data_SatSun, data_all[i])
      else: data_Week = Add_Day(data_Week, data_all[i])
    skip = skip >> 1

  return data_all, data_OK, data_SatSun, data_Week, gain1,offset1

  

# ********************************************************************
# Calculates the energy of an Aktometer signal
# ********************************************************************
def Akto_Energy(signal):
  # find where there is signal
  s = signal > 0

  # find the edges of the activity period
  # because derivate starts after 2 samples
  # we add an extra sample at the beginning
  s2 = r_[([False]),s ]
  afgel = diff( 1 * s2)

  # statemachine that scans the signal
  # and calculates average activity and
  # total energie = mean * time
  state = False
  new = zeros(len(afgel))
  new_T = zeros(len(afgel))
  for i in range( 0, len(afgel) ):
    # wait for an rising edge
    if not(state) and (afgel[i]>0):
      state = True        # set energy burst found
      sum = signal[i]     # initialize the sum of the activity
      T = 1               # duration of this activity burst
      start = i           # remember the start of this burst
    # during activity, sum the signal
    elif state and (afgel[i]==0) :
      sum = sum + signal[i]
      T = T + 1
    # test for a falling edge, indicating end of activity burst
    elif state and (afgel[i]<0) :
      # calculate the total energy and build up the signal
      new_T [start : i] = sum
      # calculate the average energy and build up the signal
      sum = sum / T
      new [start : i] = sum
      state = False

  # and we return the results
  return new,new_T
# ******************************************************************************

# ******************************************************************************
# Read SenseWear Tab-delimited file as exported from Excel
# Here we assume that the Sensewear takes a sample every minute
# To compare with the normal aktometer we've to reduce to 1 sample / 5 min
"""
    0 : Time (GMT+02:00)
    1 : Transverse accel - peaks
    2 : Longitudinal accel - peaks
    3 : Heat flux - average
    4 : Skin temp - average
    5 : Transverse accel - average
    6 : Longitudinal accel - average
    7 : Near-body temp - average
    8 : Transverse accel - MAD
    9 : Longitudinal accel - MAD
    10 : Step Counter
    11 : GSR - average
    12 : Lying down
    13 : Sleep
    14 : Physical Activity
    15 : Energy expenditure
    16 : Sedentary
    17 : Moderate
    18 : Vigorous
    19 : Very Vigorous
    20 : METs
    21 : Timestamps
"""
# ******************************************************************************
def Read_SenseWear_Tab_File (filename, Sample_Reduction = 5, Print_Info = False):
  from time import strptime

  # open the data file and read the column names (and print if desired)
  Datafile = open(filename,'r')
  line = Datafile.readline()
  column_names = line.rstrip('\n').split('\t')
  if Print_Info:
    print ('Column Names:')
    for i,item in enumerate ( column_names ) :
      print ('  ' + str(i) + ' : ' + item)

  # initialize Number of columns and an empty sample-set
  N = len(column_names)
  zero_vals = N * [0]
  SR = Sample_Reduction

  # read the first dataline, to determine the start time
  # (we forget this first sampleset)
  line = Datafile.readline()
  vals = line.rstrip('\n').split('\t')
  start = datetime(*strptime(vals[0][0:16], "%Y-%m-%d %H:%M")[0:6])
  prev_tyd = 0     # time of the previous sample

  # create an empty array
  data = asarray([])
  sample_reduction = asarray([])

  ################################################################
  # TIJDELIJK
  ################################################################
  #start = start - datetime(*strptime('1:00', "%H:%M")[0:6])

  # read and interpretate all lines in file
  for line in Datafile:
    # remove EOL, split the line on tabs
    vals = line.rstrip('\n').split('\t')

    # calculate number of minutes from start
    tyd = datetime(*strptime(vals[0][0:16], "%Y-%m-%d %H:%M")[0:6])
    s = tyd - start
    tyd = s.seconds/60 + s.days*24*60

    # if there are sample-sets missing, fill them empty sample-sets
    # (beware of sample reduction)
    if tyd - prev_tyd > 1:
      zero_vals = (( tyd - prev_tyd )/SR) * N * [0]
      data = r_[data, zero_vals]
      if Print_Info:
        print ('Sensewear Missing Samples:', tyd - prev_tyd - 1, vals[0])

    prev_tyd = tyd    # remember the time of this sample-set
    vals[0] = tyd     # replace the datetime with number of minutes

    # be sure all lines are of equal length
    # (sometimes Excel omits the last columns if they are empty)
    if len(vals) < N:
      vals = vals + ( N- len(vals) )*[0]

    # replace empty strings, otherwise float conversion raises an error
    for i in range(len(vals)):
    	if vals[i] == '' : vals[i] = '0'

    
    # convert the string vector to a float vector
    # VERY STRANGE: the next 2 operation may not be done at once
    vals = asarray(vals)
    vals = vals.astype(float)

    # vector sum before average, does nothing
    #vals[7] = sqrt (vals[8]**2 + vals[9]**2)

    # append new sampleset, with a sample reduction of 5
    sample_reduction = r_ [ sample_reduction, vals ]
    if len(sample_reduction) == SR * N:

      # reshape sample array, for easy ensemble average
      sample_reduction = sample_reduction.reshape(SR, N)
      sample_reduction = sample_reduction.mean(0)

      # add mean value of SAMPLE_REDUCTION sample-sets to the total array
      # and clear the averaging sample-set
      data = r_[data, sample_reduction]
      sample_reduction = asarray([])

  # reshape into N signal vectors
  data = data.reshape(size(data)/N,N)
  data = transpose(data)

  return data
# ******************************************************************************


# ********************************************************************
# extends the last dimension (time-axis) of 1 and 2 dimensional arrays
# to the given length,
# by using the values of the last row (last sample)
# ********************************************************************
def Extend_Last_Dim(ar,lengte):
  if ar.ndim == 1 :
    if len(ar) < lengte: ar = r_ [ar, ar[-1]*ones(lengte - len(ar))]
  else: # the 2-dimensional case
    if ar.shape[0] < lengte:
      # transpose the array, because otherwsie we can't stack !!
      ar = ar.transpose()
      # het the last sample
      last_row = ar[-1,:]
      # extend the (transposed) array
      for i in range(lengte - ar.shape[0]): ar = vstack((ar,last_row))
      # and transpose the array back
      ar = ar.transpose()
  return ar

def Calculate_Filter_Amplitude_Phase (filt_coeff, textinfo=None):
  # calculate complex transfer function:  w = H(w)
  h,w = signal.freqz ( filt_coeff[0], filt_coeff[1] )

  # add a small offset (-140 dB), to prevent error from log(0)
  w_dB = 20 * log10 ( abs(w) + 0.0000001 )

  # make the phase continuously (arctan doesn't work)
  w_Phase = unwrap(arctan2(imag(w),real(w))) / pi
  #w_Phase = arctan2(imag(w),real(w)) #/ pi

  # display filter summary, if needed
  if textinfo != None :
    print ('filter length b[] = ',len(filt_coeff[0]))
    print ('filter length a[] = ',len(filt_coeff[1]),'   a[0] = ',filt_coeff[1][0])
    print ('')
  return w_dB, w_Phase

# #############################################################################
def prn ( V ):
  # local function: print a single row of an array
  def prn_array_row ( R, row ):
    if len(R) <= 6: print ('  Row', row, ':', R)
    else:
      print ('  Row', row, ': [', R[0],R[1],R[2], '...', R[-3], R[-2], R[-1], ']')

  # local function: print a single element of a list
  def prn_list_element ( E ):
    if   type(E) in [int, float, complex]: return '  ' + str(E)
    elif type(E) == list:    return '  [..]'
    elif type(E) == tuple:   return '  (..)'
    elif type(E) == array:   return '  ([..])'
    else:                    return '  ??'

  # Beginning of the function
  print ('')
  if type(V) == int:
    print ('int32 =', V)

  elif type(V) == float:
    print ('float64 =', V)

  elif type(V) == complex:
    print ('complex64 =', V)

  # LIST & TUPPLE
  elif (type(V) == list) | (type(V) == tuple):
    # count the occurances of the different types
    count = {}
    for item in V:
      t = type(item)
      try:             count[t] += 1
      except KeyError: count[t]  = 1

    # Generate the structure of the List / Tupple
    #     count = { <type 'int'> : 2, <type 'tuple'>: 1}
    # skip this     -------   --
    if type(V) == list: line = 'List:'
    else:               line = 'Tuple:'
    #for key in count:   line += '  %s=%d' %('N_'+str(key)[7:-2],count[key])
    for key in count:   line += '  %s=%d' %('N_'+key.__name__,count[key])
    print (line)

    if len(V) < 4:
      line = ''
      for i in range(len(V)): line += prn_list_element (V[i])
      print (line)
    else:
      print (prn_list_element (V[0]),\
            prn_list_element (V[1]),\
            '  .....',\
            prn_list_element (V[-2]),\
            prn_list_element (V[-1]))

  # SCIPY ARRAY
  elif type(V) == ndarray:
    print ('Array', V.shape, V.dtype.name)
    if V.ndim == 1:
      prn_array_row ( V, 0 )
    elif V.ndim == 2:
      if V.shape[0] < 4:
        for i in range(V.ndim): prn_array_row ( V[i,:], i )
      else:
        prn_array_row ( V[0,:], 0 )
        prn_array_row ( V[1,:], 1 )
        print ('  ......')
        prn_array_row ( V[-2,:], V.shape[1]-2 )
        prn_array_row ( V[-1,:], V.shape[1]-1 )

  else:
    line = 'UNKNOWN: ' + type(V)
    print (line)
    line = '  ' + V.__repr__()
    # do something to prevent to long output sequences
    print (line)


"""
# ********************************************************************
# function made to test the stats.linregress function, and it works !!
#    linregress(*args)
#        Calculates a regression line on two arrays, x and y, corresponding to x,y
#        pairs.  If a single 2D array is passed, linregress finds dim with 2 levels
#        and splits data into x,y pairs along that dim.
#        Returns: slope, intercept, r, two-tailed prob, stderr-of-the-estimate
# ********************************************************************
def test_lin_regres(x,y):
  xm = mean( x )
  ym = mean( y )
  sum_xy = 0
  sum_x2 = 0
  sum_y2 = 0
  N = len(x)
  for i in range( N ):
    sum_xy = sum_xy + x[i] * y[i]
    sum_x2 = sum_x2 + x[i] * x[i]
    sum_y2 = sum_y2 + y[i] * y[i]
  b1 = ( sum_xy - N * xm * ym ) / ( sum_x2 - N * xm * xm)
  b0 = ym - b1 * xm
  r = ( sum_xy - N * xm * ym ) / ( sqrt( (sum_x2 / N - xm * xm ) * (sum_y2 / N - ym * ym)) )
  return b1, b0, r/N
# ********************************************************************
"""



# ********************************************************************
# ********************************************************************
def Read_New_Akto_File_RAWWWW ( filename, Print_Info = None ):

  # **********************************************************
  # **********************************************************
  def calc_1 ( setnr ) :
    dset = data_all [setnr].reshape(32,3)
    #print 'Set=', setnr, dset

    x = dset [ :, 0 ]
    y = dset [ :, 1 ]
    z = dset [ :, 2 ]

    diffx = x-mean(x)
    diffz = z-mean(z)

    #print z,mean(x),mean(y),mean(z)
    #print abs(x-mean(x))
    x1 = int ( round ( mean ( abs ( diffx ) ) ) )
    z1 = int ( round ( mean ( abs ( diffz ) ) ) )

    #print diffx
    #print diffz
    #print diffx + diffz
    vect = sqrt ( diffx*diffx + diffz*diffz )
    vect = int ( round ( mean ( vect ) ) )
    return array ( [ x1, z1, x1+z1, vect ] )
  # **********************************************************

  # read the sampled data
  DataFile = open ( filename, 'r' )       # Readonly
  data_all_text = DataFile.read ()
  DataFile.close ()

  # next split will use both the space and eol as a separator
  data_all = data_all_text.split ()
  #print data_all [ : 20 ]

  # skip the header, only if the file was written with patient data
  #data_all = data_all [256 : ]

  # single conversion doesn't seem to be allowed
  data_all = asarray ( data_all ).astype ( int )
  #print data_all[:20]

  # we only want complete sets,
  # only a problem if the file was written with patient data
  set_len = 3 * 32
  N = len ( data_all ) / set_len
  #print 'XXXX',len(data_all)-set_len*N
  data_all = data_all [ : set_len * N ]

  # now reshape so we reach individual set
  data_all = data_all.reshape ( N, set_len )

  #print data_all.shape
  #print data_all [0]

  """
  setnr = 83
  for setnr in range ( 80, 100 ) :
    dset = data_all [setnr].reshape(32,3)
    print 'Set=', setnr, dset
  """
  
  setnr = 83  #set die iets doet



  #for setnr in range ( data_all.shape[0] ):
  #  print calc_1 ( setnr )
  result = calc_1 ( 0 )
  for setnr in range ( N ) :
    ns = calc_1 ( setnr )
    #print ns
    result = r_ [ result, ns ]

  return result



# ********************************************************************
# A raw aktometer file contains all samples !!
# ********************************************************************
def Read_New_Raw_Akto_File ( filename, Print_Info = None ):

  # read the sampled data
  DataFile = open ( filename, 'r' )       # Readonly
  #lines = DataFile.readlines ()
  data_all_text = DataFile.read ()
  DataFile.close ()


  # next split will use both the space and eol as a separator
  data_all = data_all_text.split ()
  #print data_all [ : 20 ]

  # skip the header, only if the file was written with patient data
  #data_all = data_all [256 : ]

  # single conversion doesn't seem to be allowed
  data_all = asarray ( data_all ).astype ( int )
  #print data_all[:20]

  # we only want complete sets,
  # only a problem if the file was written with patient data
  set_len = 3 * 32
  N = len ( data_all ) / set_len

  # take only complete sets
  data_all = data_all [ : set_len * N ]

  # now reshape so we reach individual set
  #data_all = data_all.reshape ( N, set_len )


  N = len ( data_all ) / 3
  data_all = data_all.reshape ( N, 3 )
  data_all = transpose ( data_all )

  #print data_all.shape
  #print data_all [0]

  #print data_all [0][:20]
  x = data_all [0]
  y = data_all [1]
  z = data_all [2]
  #print x[:25]
  #print y[:25]
  #print z[:25]
  return data_all


  
# ********************************************************************
# ********************************************************************
def Read_New_Raw_Akto_Kal_File ( filename, Print_Info = None ):
  # read the sampled data
  DataFile = open ( filename, 'r' )       # Readonly
  data_all_text = DataFile.read ()
  DataFile.close ()

  # split in lines, remove the first lines, combine them again
  data_all_text = data_all_text.replace ( '\r\n', '\n' )
  data_all_text = ' '.join ( data_all_text.split ('\n') [ 9: ] )

  # remove reset markers "255 255 255 128"
  i     = 0
  reset = 0
  while i >= 0:
    i = data_all_text.find ( '255 255 255 ' )
    if i >= 0 :
      ii = data_all_text.find ( ' ', i + 12 )
      data_all_text = data_all_text [ : i ] + data_all_text [ ii+1 : ]
      reset += 1

  # next split will use both the space and eol as a separator
  data_all = data_all_text.split ()

  # single conversion doesn't seem to be allowed
  data_all = asarray ( data_all ).astype ( int )

  # we only want complete sets,
  # only a problem if the file was written with patient data
  set_len = 3 * 32
  N = len ( data_all ) / set_len

  # take only complete sets
  data_all = data_all [ : set_len * N ]

  N = len ( data_all ) / 3
  data_all = data_all.reshape ( N, 3 )
  data_all = transpose ( data_all )

  return data_all, reset

# ********************************************************************
# ********************************************************************
def Calibrate_Akto_V5 ( filename ) :
  Sep_Low  = 116
  Sep_High = 140
  Min_Leng = 300

  Data_Akto, Reset = Read_New_Raw_Akto_Kal_File ( filename, True )

  # now each value will get a value in the range 1,2,3
  region = 2 -1 * ( Data_Akto < Sep_Low  ) + \
              1 * ( Data_Akto > Sep_High )

  # search transitions
  Delta = diff ( region )

  Transition = [0]
  for i in xrange ( len ( Delta [0] ) ) :
    if not ( Delta[0][i] == Delta[1][i] == Delta[2][i] == 0 ) :
      Transition.append ( i )
  # add the end
  Transition.append ( len ( Delta [0] ) )

  Delta = diff ( Transition )
  #print Delta

  XM = []
  YM = []
  ZM = []
  XS = []
  YS = []
  ZS = []
  NRegion = 0
  Region_Len = []
  for i in range ( len ( Transition ) - 1 ) :
    if ( Delta [i] > Min_Leng ) and ( NRegion < 6):
      NRegion += 1
      x1 = Transition [i]
      x2 = Transition [i+1]
      Region_Len.append ( x2-x1 )
      #print 'LL', Transition [i], Transition [i+1]
      X = Data_Akto [ 0 ] [ x1 : x2 ]
      Z = Data_Akto [ 1 ] [ x1 : x2 ]
      Y = Data_Akto [ 2 ] [ x1 : x2 ]
      # Calculate Mean over the different axis
      XM.append ( mean ( X ) )
      YM.append ( mean ( Y ) )
      ZM.append ( mean ( Z ) )
      # and standard deviation
      XS.append ( std ( X ) )
      YS.append ( std ( Y ) )
      ZS.append ( std ( Z ) )

  print ('NRegion must be 6 :', NRegion)

  #*****************************************
  # Calculate mean of 3 regions: -1g, 0g, 1g
  #*****************************************
  def Calc ( MM, result ) :
    MM = array ( MM )

    Good = MM < Sep_Low
    Low = int ( 10 * mean ( MM [ Good ] ) )
    result.append ( Low )

    Good = all ( [ (MM > Sep_Low) ,  (MM < Sep_High) ], axis=0 )
    result.append ( int ( 10 * mean ( MM [ Good ] ) ) )

    Good = MM > Sep_High
    High = int ( 10 * mean ( MM [ Good ] ) )
    result.append ( High )

    result.append ( High - Low )
    
  #*****************************************

  Akto_Nr = os .path.splitext ( path_split ( filename ) [1] ) [0]
  Akto_Nr = Akto_Nr.split('_') [1]
  result = [ int ( Akto_Nr )  ]
  Calc ( XM, result )
  Calc ( YM, result )
  Calc ( ZM, result )

  # Add Reset Count
  result.append ( Reset )
  
  # add the Averaged Standard Deviation
  result.append ( int ( 100 * mean ( XS ) ) )
  result.append ( int ( 100 * mean ( YS ) ) )
  result.append ( int ( 100 * mean ( ZS ) ) )

  # add detected regions
  result += Region_Len
  print (result)
  return result
# ********************************************************************


# ********************************************************************
# A normal Aktometer file
# ********************************************************************
def Read_New_Akto_File ( filename, Print_Info = None ):
  """
  Reads a normal aktometer file (type-5).
  Returns a 2-dimensional array Data_Akto, where
    Data_Akto [ 0 ] = calculated result
    Data_Akto [ 1 ] = raw Z-axis value
    Data_Akto [ 2 ] = raw Y-axis value
    Data_Akto [ 3 ] = control bits
  7-1-2009: factor 0.75 toegevoegd
  7-1-2009: sample period correction added
  7-1-2009: error (waarde 255) geeft een 0 terug
  """
  # read the sampled data
  DataFile = open ( filename, 'r' )       # Readonly
  lines = DataFile.readlines ()
  DataFile.close ()

  Sample_Period = 10
  for i in range ( 20 ) :
    if lines[i].find('data:') >= 0 :
      break
    elif lines[i].startswith ( 'system:' ) :
      Sample_Period = int ( lines[i].split('~')[1] )
  else :  # error
    return None

  # next split will use both the space and eol as a separator
  data_all_text = ''.join ( lines [ i+1 : ] )
  data_all = data_all_text.split ()
  #print data_all [ : 20 ]

  # single conversion doesn't seem to be allowed
  data_all = asarray ( data_all ).astype ( int )
  #print data_all[:20]

  # take only complete sets

  N = len ( data_all ) / 4
  data_all = data_all [ : 4 * N ]
  data_all = data_all.reshape ( -1, 4 )

  data_all = transpose ( data_all )
  #print 'Shape', data_all.shape   # ( 4, 900 )

  #*******************************************************************************
  # ActiLog V3.0, logaritmische expansie.
  #*******************************************************************************)
  def expand3 ( b ) :
    Period_Correction = ( 20.0/8, 10.0/8, 10.0/6, 10.0/8, 1.0,
                          10.0/6, 10.0/7, 10.0/8, 10.0/9, 1.0 )
    if   b < 0x80 : result =   b
    elif b < 0xC0 : result = ( b & 0x3F ) * 2 + 128
    elif b < 0xE0 : result = ( b & 0x1F ) * 4 + 256
    elif b < 0xF0 : result = ( b & 0x0F ) * 8 + 384
    else          : result = ( b & 0x0F ) * 8 + 512
    return round ( result * Period_Correction [ Sample_Period - 1 ] )


  x = data_all [0]
  y = data_all [2]
  z = data_all [1]
  S = data_all [3]
  #print x[:25]
  #print y[:25]
  #print z[:25]

  for i in range ( len ( x ) ) :
    if x[i] < 255 :
      x[i] = int ( 0.85 * ( expand3 ( x[i] ) + expand3 ( y[i] ) ) )
    else :
      x [i] = 0
      
    #y[i] = ( S & 0x80 ) >> 7
    reset_count = 0
  
  x = data_all [0]
  y = data_all [2]
  z = data_all [1]
  #print x[:25]
  #print y[:25]
  #print z[:25]

  return data_all


# ********************************************************************
# ********************************************************************
def Read_ActivePAL ( filename, compression = 1 ) :
  """
  Reads an ActivePAL file (and saves it more compressed).
  If the compressed file already exists, it's read directly.
  This compression in the stored file is only the removing
  of the datetime, and not yet the "compression"  parameter.
  The returned result does include the " compression" parameter.
  """
  import numpy
  filnam, filext = os.path.splitext ( filename )

  # If the compressed file (without datetime) doesn't exists
  # Create it now
  Compressed_Filename = filnam + '.csvc'
  if not ( File_Exists ( Compressed_Filename ) ) :
    Data_PAL = numpy.loadtxt ( filename,
                    comments ='"',
                    delimiter = ',',
                    dtype = int,
                    skiprows = 5,
                    usecols = [1] )
    Data_PAL.tofile ( Compressed_Filename )
    
  # Now read the raw data from the compressed file
  Data_PAL = numpy.fromfile ( Compressed_Filename, dtype=int )
  #Data_PAL = 1.0* Data_PAL
  #print Data_PAL [ : 40 ]
  
  # and if extra compression required, do it
  
  if compression != 1 :
    algorithm = 2
    # we use average sloop method, because
    #   - it's a very easy filter
    #   - it combines low pass filter with derivate calculation
    len3 = 4
    average_sloop = (r_ [ ones(len3), zeros(len3), -1 * ones(len3) ]) / (3.0 * len3)

    New = []
    N = len ( Data_PAL ) / compression
    for i in xrange ( N ) :
      Data = Data_PAL [ i*compression : (i+1)*compression ]

      if algorithm == 1 :
        Mean = Data.mean()
        Energy = abs ( Data - Mean ).mean()
        New.append ( Energy )
        
      elif algorithm == 2 :
        Energy = abs ( diff ( Data ) ).mean()
        New.append ( Energy )


      #if New[-1]>150 :
      #  print New[-1] #Data_PAL [ i*compression : i*compression+10 ]
    Data_PAL = array ( New )

  print (Data_PAL [ : 40 ])
  return Data_PAL
# ********************************************************************


# ********************************************************************
# ********************************************************************
def Read_StepWatch ( filename, compression = 1 ) :
  """
  Reads an StepWatch file (and saves it more compressed).
  If the compressed file already exists, it's read directly.
  This compression in the stored file is only the removing
  of the datetime, and not yet the "compression"  parameter.
  The returned result does include the " compression" parameter.
  """
  import numpy
  #filnam, filext = os.path.splitext ( filename )

  Data_StepWatch = numpy.loadtxt ( filename,
                  comments ='"',
                  delimiter = '\t',
                  dtype = int,
                  skiprows = 1,
                  #usecols = [1]
                  )
  N =Data_StepWatch.size
  """
  print 'S1',N,Data_StepWatch.shape
  for i in range ( Data_StepWatch.shape[0] ) :
    print Data_StepWatch [ i, : ]
  """
  2
  # During reshape, we need the Fortran order !!
  Data_StepWatch = Data_StepWatch.reshape ( N, order = 'F' )
  #print 'S2',N,Data_StepWatch.shape

  ## MIDDELEN NAAR 5 MINUTEN
  S = Data_StepWatch.size
  M = 5
  D = Data_StepWatch
  for i in range ( ( S // M ) - 1 ) :
    D [i] = sum ( D [ M*i : M*i+5 ] )

  # EVEN HEEL SMERIG
  #Data_StepWatch [ :, 0 ]

  return Data_StepWatch [ : S//M]
# ********************************************************************

# ********************************************************************
# ********************************************************************
if __name__ == '__main__':
  from pprint import pprint

  Test_Defs ( 9 )

  if Test(1) :
    filename = "D:/akto_yk/SW_akto/99-2.dat"
    data, data_ok1, data_zazo, data_week = Read_Akto_File(filename, Calibrated=True, Print_Info=True, Raw=True)
    print (data)
  
  if Test(2) :
    filename = 'D:/akto_yk/T3-patient/raw.txt'
    data1 = Read_New_Raw_Akto_File ( filename, True)
    print (data1)

  if Test(3) :
    My_Path = 'D:/akto_yk/Kalibratie_V5/'
    Kal_Files = Find_Files ( My_Path, '*.dat', RootOnly = True )
    #print Kal_Files

    Results = []
    for filename in Kal_Files :
      filename = My_Path + filename[1] + '.dat'
      Results.append ( Calibrate_Akto_V5 ( filename ) )

    filename = My_Path + 'Akto_V5_KAL.tab'
    NewFile = not ( File_Exists ( filename ) )
    if NewFile :
      datafile = open ( filename, 'w' )
      line = 'Akto,Xmin,X0,Xmax,XX2,Ymin,Y0,Ymax,YY2,Zmin,Z0,Zmax,ZZ2,Reset,dX,dY,dZ,R1,R2,R3,R4,R5,R6'
      line = line.replace ( ',', '\t' )
      datafile.write ( line + '\n' )
    else :
      datafile = open ( filename, 'a' )

    filename = My_Path + 'Akto_V5_KAL.cgf'
    ini = inifile ( filename )
    ini.Section = 'Header'
    ini.Write ( 'Akto' , 'Aktometer Nummer'    )
    ini.Write ( 'Xmin' , '(10*) Mean over -1g' )
    ini.Write ( 'X0'   , '(10*) Mean over  0g' )
    ini.Write ( 'Xmax' , '(10*) Mean over +1g' )
    ini.Write ( 'XX2'  , '(10*) Diff over 2g'  )
    ini.Write ( 'Reset', 'Reset counter'       )
    ini.Write ( 'dX'   , '(100*) SD'           )
    ini.Write ( 'R1'   , 'Lengte Range'        )

    ini.Section = 'Calibration'
    for R in Results :
      line = ''
      for item in R :
        line += str ( item ) + '\t'
      datafile.write ( line + '\n' )

      line = ''
      for item in R [ 1 : ] :
        line += str ( item ) + ','
      ini.Write ( str( R[0] ), line )

    ini.Close ()
    datafile.close ()




  if Test(4) :
    nr = '6'
    filename = 'D:/data_actueel/D7_AktoTest/509_t'+nr+'.txt'
    data1 = Read_New_Raw_Akto_File ( filename, True)
    filename = 'D:/data_actueel/D7_AktoTest/512_t'+nr+'.txt'
    data2 = Read_New_Raw_Akto_File ( filename, True)
    
    # make both data arrays equal length
    N1 = len ( data1 )
    N2 = len ( data2 )
    N = min ( N1, N2 )
    if N1 > N2 :
      data1 = data1 [ : N ]
    elif N2 > N1 :
      data2 = data2 [ : N ]

    # join the arrays, so we get a line containing a set from each akto
    #  X1  X2  Z1  Z2  X1+Z1  Z1+Z2  Vect1  Vect2
    data1 = data1.reshape ( N, 1 )
    data2 = data2.reshape ( N, 1 )
    data = hstack ( ( data1, data2 ) )
    data = data.reshape ( N/4, 8 )
    print ('PPPP', data [:4])

    """
    [1 8 9 8]
    [0 0 0 0]
    [3 4 7 5]
    [2 1 3 3]
    [0 1 1 1]

    [1 0 1 1]
    [15  8 23 18]
    [ 4  8 12 10]
    [0 0 0 0]
    [0 0 0 0]

    PPPP [[1 1]
     [8 0]
     [9 1]
     [8 1]]
    """
    # write all data to a file
    filename = 'D:/data_actueel/D7_AktoTest/anal_'+nr+'.txt'
    #data.tofile ( filename )
    DataFile = open ( filename, 'w' )
    DataFile.write ( 'X1-' + nr +'  X2  Z1  Z2  X1+Z1  X2+Z2  Vect1  Vect2\n' )
    #DataFile.write ( pack('i',data) )
    print ('OOOO',data.shape)
    """
    for i in range ( data.shape[0] ) :
      a = string ( data[i] ) [ 1 : -1 ].strip()+'\n'
      DataFile.write ( a )
    """

    ## MIDDELEN NAAR 1 MINUUT
    for i in range ( ( data.shape[0] / 2) - 1 ) :
      a1 = data[2*i]
      a2 = data[2*i+1]
      a = string ( a1+a2 ) [ 1 : -1 ].strip()+'\n'
      DataFile.write ( a )
    DataFile.close ()


  if Test(5) :
    filename = 'D:/akto_yk/T3-patient/test31.dat'
    data1 = Read_New_Akto_File ( filename, True)
    
  #*********************************
  #*********************************
  if Test(6) :
    filename = 'D:/akto_yk/4Daagse2008/4 daagse opslag/6/SW_06.tab'
    Sample_Reduction = 1
    data_SW = Read_SenseWear_Tab_File ( filename, Sample_Reduction, True)
    print (shape   ( data_SW ))
    pprint ( data_SW )

  #*********************************
  #*********************************
  if Test(7) :
    filename = 'D:/akto_yk/4Daagse2008/4 daagse opslag/6/SW_06.tab'
    Sample_Reduction = 1
    data_SW = Read_SenseWear_Tab_File ( filename, Sample_Reduction, True)
    print (shape   ( data_SW ))

    filename = 'D:/akto_yk/4Daagse2008/4D_06.dat'
    data_akto = Read_New_Akto_File ( filename, True )
    print ('Shape:', shape ( data_akto ))

    from array_support import *
    data = Make_2dim_Array ( data_SW, data_akto )
    print (shape ( data ))

  #*********************************
  # Comparison aktometer / ActivePAL
  #*********************************
  if Test(8) :
    filename = 'D:/akto_yk/ActivePAL/thomas_smk.dat'
    data_akto = Read_New_Akto_File ( filename, True )
    print (data_akto [ 0, : 10 ])

    filename = 'D:/akto_yk/ActivePAL/activepalthomas.csv'
    Data_PAL = Read_ActivePAL ( filename, compression = 1200 )
    print (Data_PAL [ : 10])

  #*********************************
  # Comparison aktometer / StepWatch
  #*********************************
  if Test ( 9 ) :
    filename = 'D:/akto_yk/StepWatch/Sandra.tab'
    Data_StepWatch = Read_StepWatch ( filename, compression = 1200 )
    print ('STEP',Data_StepWatch[ 650 : 700])

    filename = 'D:/akto_yk/StepWatch/Sandra.dat'
    data_akto = Read_New_Akto_File ( filename, True )
    #print 'Shape:', shape ( data_akto )
# ********************************************************************
