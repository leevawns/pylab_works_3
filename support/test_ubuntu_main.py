
if __name__ == "__main__":
  import subprocess
  print 'Before'
  PID = subprocess.Popen ( [ 'python', 'test_ubuntu.py' ],
                           stdout = subprocess.PIPE,
                           stderr = subprocess.PIPE,
                           shell=True )
  while PID.poll() == None :
    text = PID.stdout.read()
    if text :
      print text
  print 'After'
