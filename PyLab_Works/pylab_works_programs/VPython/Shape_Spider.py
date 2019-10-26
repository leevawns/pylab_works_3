#----------------------------------------------------------------------
# readdata.py - This program is meant to be a simple example of how to
#              read data from a file. It reads a plain ASCII text file
#              containing three columns of numbers separated by spaces
#              and treats the numbers in each line as a three
#              dimensional (x,y,z) coordinate for a point on a weird
#              knotlike 3D figure.
#----------------------------------------------------------------------
from visual.graph import *
from string import split

Forward_Up ( None, None, 60 )

# open a file named "data" for reading
file = open(My_Path+"data.txt",'r')

# open a 3D graphics window
window = scene  #display(x=-100,y=400)
 
# put a curve on the graph
thing = curve(radius=1)

# read each line in the file, extract (x,y,z) coordinate data out of it
# and plot
for line in file:
    #split each line into three strings holding each number    
    stringnums = split(line) 

    #convert each string in stringnum to a float
    coordinate = map(float,stringnums)

    #add that point to our 3D "thing"
    thing.append(pos=coordinate)
    

while True :
  rate ( 50 )
