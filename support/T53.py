

def Read_Text_Test_T53 () :
  import __init__

  from General_Globals import Module_Absolute_Path
  My_File = Module_Absolute_Path ( '..', 'sounds', 'T53.txt' )
  print 'VVVV', My_File
  
  fh = open ( My_File, 'r')
  lines = fh.readlines ()
  fh.close ()

  for line in lines :
    print line.replace ( '\n', '' ). replace ( '\r', '' )
    
    
if __name__ == "__main__":
  Read_Text_Test_T53 ()

