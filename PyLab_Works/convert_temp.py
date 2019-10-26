import os
filename = '../support/test_My_Custom_TreeCtrl.tree'
filename2=os.path.splitext ( filename )[0]+'.aap'
source = open (filename,'r')
dest   = open (filename2,'w')
lines = source.read()
lines = lines.replace(',','~')
dest.write(lines)
dest.close()
source.close()