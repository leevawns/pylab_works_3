
filename2 = "H:\\temp\\M330 V0.xml"
filename1 = "H:\\temp\\M330 V-1.xml"

file1 = open ( filename1, 'r')
file2 = open ( filename2, 'r')


base = []
lines = file1.readlines()
for line in lines:
  i = line.find('EqmId')
  if i>0:
    line = line [i+6:].split()[0]
    base.append (line)


al_gehad =[]
lines = file2.readlines()
for line in lines:
  i = line.find('EqmId')
  if i>0:
    line = line [i+6:].split()[0]
    if (line in base) and not(line in al_gehad):
      al_gehad.append(line)
      print '*******',line

print len(base),len(al_gehad)