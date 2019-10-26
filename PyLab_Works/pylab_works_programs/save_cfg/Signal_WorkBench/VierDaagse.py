from signal_workbench import *
import signal_workbench
reload ( signal_workbench ) 

pat   = (6,18,19,32,33,39,61,66,67,71)
weight = (126,74,71,89,83,95,52,81,62,76)
bmr = ( 2342,1476,1337,1910,1613,1981,1140,1536,1416,1516 )
# zesde proefpersoon van 60 jr naar 61 jaar, maakt toch niet zoveel uit
#bmr = ( 2342,1476,1337,1910,1613,1770,1140,1536,1416,1516 )

# start difference between SW and Akto
SHIFT = (12,22,11,11,19,33,38,27,43,34)

# Copied from and block in and Excel sheet
SLICES = """
2220	2853	3658	4307	5100	5779	6538	7214
2277	2941	3711	4360	5150	5811	6594	7302
2218	2849	3657	4302	4860	4860	6536	7214
2395	2938	3815	4379	5280	5813	6695	7256
2392	2929	3809	4375	5273	5813	6689	7252
993	1435	2433	2835	3866	4266	5252	5681
771	1213	2219	2711	3656	4112	5093	5599
830	1451	2268	2894	3723	4329	5170	5849
857	1235	2358	2748	3739	4104	5179	5579
1078	1586	2525	3028	3965	4465	5397	5965
"""

WHO = """
5171	3409	2893	3608	3013	2722	1753	3318	1874	2679
5318	3332	3000	3748	3175	2476	1951	3345	1928	2658
5554	3388	0	3542	3030	2464	1809	3238	1805	2642
5529	3634	3153	3741	3159	2642	2007	3627	1977	3000
"""

# Excel kopie van EE waarden,
# door deze met 0.85 te vermenigvuldigen
# klopt de waarde beter met def WHO formule
# Door deze string tijdelijk WHO te noemen,
# komt hij in def export file
#EE
EE = """
7854	3963	3665	4081	3724	3570	2084	4916	2744	3840
7295	4066	3524	4104	3931	3467	2346	4846	2888	3533
7436	3409	0	3859	3478	3187	2080	4419	2730	2888
7885	3848	3557	4184	3586	3623	2368	4347	3014	3924
"""
#IOM
IOM = """
5447	2790	2481	3684	3364	3258	1778	2485	2926	2218
5564	2754	0	3780	3489	5044	1861	2493	2978	2207
5754	2781	0	3637	3377	5024	1801	2585	2877	2376
5734	2896	2609	3776	3476	3194	1885	2585	3019	2376
"""

# transform the Slice text string into and array
pats = SLICES.split('\n')
if len ( pats [ 0 ] ) == 0 :
  pats.pop ( 0 )
if len ( pats [ -1 ]) == 0 :
  pats.pop ()
for i in range ( len ( pats ) ) :
  pats [i] = pats[i].split()
      
# transform the WHO_ADJ
Ref = WHO.replace ( '\n', '\t' )
Ref = Ref.split ( '\t') [ 1 : -1 ]
Ref = array ( Ref ).astype ( int )
print Ref
NewRef = []
for i in range ( 10 ) :
  for ii in range ( 4 ) :
    NewRef.append ( Ref [ i + ii * 10 ] )
    #NewRef.append ( 0.85 * Ref [ i + ii * 10 ] )  # for calculating EE
print NewRef

# Read akto and sensewear data from 1 patient
def Read_Loper ( pat_nummer ) :
  path = 'D:/akto_yk/4Daagse2008/_Analyze/'
  filename = path + '4D_' + str(pat[pat_nummer]) + '.dat'
  Data_Akto_All = Read_New_Akto_File ( filename, True )
  Data_X = Data_Akto_All [ 0, SHIFT[pat_nummer]: ]
  Data_Y = Data_Akto_All [ 2, SHIFT[pat_nummer]: ]
  Data_Z = Data_Akto_All [ 1, SHIFT[pat_nummer]: ]

  filename = path + 'SW_' + str(pat[pat_nummer]) + '.tab'
  Data_SW = Read_SenseWear_Tab_File ( filename, 1 )

  return Data_X, Data_Y, Data_Z, Data_SW

def Calc_Energy ( pat_nummer, Data_Akto, Data_SW, kCal, kCal_SW ) :
  per_min = False
  correct_BMR = True
  tijd = 1

  Data_Slice = zeros ( len ( Data_Akto ) )
  pat_slice = array ( pats [ pat_nummer ] ).astype ( int )
  #print pat_slice
  # Data_Akto is already shifted !!
  # But this still works better ?? 
  pat_slice -= SHIFT [ pat_nummer ]
  #W = ( weight [ pat_nummer ] - 30 ) / 7000.0
  #W = ( weight [ pat_nummer ] + 30 ) / 15000.0
  W = weight [ pat_nummer ] / 12000.0
  BMR = 0
  if correct_BMR : 
    BMR = bmr [ pat_nummer ]
    W *= 0.65
  #print pat_slice
  #kCal = []
  for i in range (4) :
    b = pat_slice [ 2 * i     ] 
    e = pat_slice [ 2 * i + 1 ]
    if e > b : 
      if per_min : 
        tijd = e - b
      kCal.append ( BMR + int (round(W*Data_Akto [ b : e ].sum () / tijd ) ))
    else :
      kCal.append ( 0 ) 
    Data_Slice [ b : e ] = 9

  for i in range (4) :
    b = pat_slice [ 2 * i     ] 
    e = pat_slice [ 2 * i + 1 ]
    if e > b : 
      if per_min : 
        tijd = e - b
      kCal_SW.append ( BMR + int (round(120*W*Data_SW [ b : e ].sum () / tijd ) ))
    else :
      kCal_SW.append ( 0 ) 
    Data_Slice [ b : e ] = 9
  print 'Pat / kCal =', pat[pat_nummer], kCal
  
  # for displaying and block
  return Data_Slice

patnr = 0
kCal = []
kCal_SW = []
for patnr in range ( 10 ) :
  Data_X, Data_Y, Data_Z, Data_SW = Read_Loper ( patnr )
  # Akto vectorieel optellen
  #Data_Akto  = sqrt ( Data_X*Data_X + Data_Y*Data_Y )
  # Akto linear optellen en amplitude corrigeren
  #Data_Akto  = 0.75 * ( Data_X + Data_Y )
  Data_Akto  = 0.75 * ( Data_X + Data_Y + Data_Z )
  Data_Akto  = 3.5 * Data_Z
  Data_Akto  = ( Data_X + Data_Y )
  SW_Acc_MAD = sqrt ( Data_SW[8,:] * Data_SW[8,:] + Data_SW[9,:] * Data_SW[9,:] )
  Calc_Energy ( patnr, Data_Akto, SW_Acc_MAD, kCal, kCal_SW )


def write_array ( ar, title = '' ) :
  line = title
  for cell in ar :
    line = line + '\t' + str(cell)
  line += '\n'
  return line
file = open ( 'D:/akto_yk/4Daagse2008/_Analyze/d4d.tab', 'w' )
file.write ( write_array ( kCal,    'Akto'    ) )
file.write ( write_array ( NewRef,  'WHO_ADJ' ) )
file.write ( write_array ( kCal_SW, 'SW'      ) )
file.close ()
print 'Ready'

patnr = 5
pat   = (6,18,19,32,33,39,61,66,67,71)

Data_X, Data_Y, Data_Z, Data_SW = Read_Loper ( patnr )
# Akto vectorieel optellen
#Data_Akto  = sqrt ( Data_X*Data_X + Data_Y*Data_Y )
# Akto linear optellen en amplitude corrigeren
Data_Akto  = 0.75 * ( Data_X + Data_Y )
Data_Slice = Calc_Energy ( patnr, Data_Akto, Data_SW, kCal, kCal_SW )



SW_Acc_MAD = sqrt ( Data_SW[8,:] * Data_SW[8,:] + Data_SW[9,:] * Data_SW[9,:] )
SW_Energy  = Data_SW[15,:]

DISPLAY = SW_Acc_MAD, Data_Akto, Data_Slice
Display_Title = '4-Daagse, nr:%3d G, A, W, L' %(patnr)
Display_Params = []
Display_Params.append ([ 'Acc_MAD',   0, 10   ])
Display_Params.append ([ 'Akto',      0, 1000 ])
Display_Params.append ([ 'Slice',     0, 10   ])

