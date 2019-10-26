

x1 = -10
x2 = 212
y1 = 20
y2 = 120
for ADC in 50000, 90000 :
  Volt = ( ADC - 2048 ) * 5.0 / 2048
  World = y1 + 1.0 * ( y2 - y1 ) * ( Volt - x1 ) / ( x2 - x1 )
  print 'A2V', Volt, World
  
