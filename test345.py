import subprocess
#result = subprocess.call (
#  ['D:\Data_Python25_Dist\program_dummy.exe'])#, shell=True )#, cwd=workingdir )
result = subprocess.call (
  ['D:\Data_Python25_Dist\program_dummy2.exe'], cwd='D:\Data_Python25_Dist')
print 'BUILD Windows',result==0, result
