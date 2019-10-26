      Parent = self.Tree.GetSelection ().GetParent ()
      Parent_Text = self.Tree.GetItemText ( Parent )
      if Parent_Text != 'Non_pylab_works' :
        #print item, flags
        filename = os.path.join ( self.My_Path, 'pylab_works_programs', item+'.cfg' )
        if not ( File_Exists ( filename ) ) :
          line = 'Sorry, cant find file: ' + filename
          Show_Message ( line )
          return

        if Started_From_Myself :
          exefile = 'PyLab_Works'
          arguments = [ exefile, item, flags ]
          PID = subprocess.Popen ( arguments,
                                   shell =  ( os.name == 'nt') )
        else :
          exefile = os.path.join ( '..', 'demos_dummy.exe' )
          arguments = [ exefile, item, flags ]
          PID = subprocess.Popen ( arguments,
                                   shell =  ( os.name == 'nt') )
        # ********************************************************

      else :  # rund of non-demo programs
        if Started_From_Myself :
          filename = item.lower() + '.py'
          file = Find_Files ( '../', mask = filename )
          if file :
            #filename = '../' + file[0][0] + '/' + filename
            filename = os.path.join ( self.My_Path, '..', file[0][0] + '/' + filename )
            filename = os.path.normpath ( filename )
            if flags :
              Run_Python ( [ filename, flags ] )
            else :
              Run_Python ( filename )

        else : # windows installer
          filename = '_launch_' + item.lower() + '.exe'
          file = Find_Files ( os.path.join ( os.getcwd(),'..'), mask = filename )
          print self.My_Path, os.getcwd()
          print 'FILE',file, filename
          if file :
            exefile = os.path.join ( self.My_Path,'..', filename )
            print 'RRRRUNN',exefile
            if flags :
              arguments = [ exefile, flags ]
            else :
              arguments = [ exefile ]
            PID = subprocess.Popen ( arguments,
                                     shell =  ( os.name == 'nt') )





==== demods_dummy
import os, sys
Base_Path = os.getcwd()
sys.path.append ( Base_Path )
execfile ( "PyLab_Works.py" )

===== install
for i, file in enumerate ( Exe_Files ) :
  Exe_Files [i] = file.replace ( '\\', '/' )
  if '/' in Exe_Files [i] :
    path, filename = os.path.split    ( Exe_Files [i] )

    New_File = os.path.join ( Base_Path, '_launch_' + filename )

    fh = open ( New_File, 'w' )
    fh.write ( 'import os, sys\n')
    fh.write ( 'Base_Path = os.getcwd()\n')

    # Add __main__ to dictionairy,
    # otherwise the main section will not be executed
    #fh.write ( "My_File = '" + os.path.split (Exe_Files [i])[1] + "'\n" )
    fh.write ( 'My_Globs = {}\n' )
    fh.write ( "My_Globs [ '__name__' ] = '__main__'\n" )

    # Set the current working directory to the main file directory
    fh.write ( 'Work_Path = os.path.join ( Base_Path,"' + path + '")\n' )
    fh.write ( 'os.chdir ( Work_Path )\n' )
    fh.write ( 'sys.path.append ( Work_Path )\n' )
    fh.write ( 'execfile ( "'+ filename + '", My_Globs )\n' )
    fh.close ()

    Exe_Files [i] = New_File

#Exe_Files = [ 'PyLab_Works/PyLab_Works.py' ]
#Exe_Files = [ 'program_dummy.py' ]

# These are started from "PyLab_Works/" already,
# so leave out the prefix
Exe_Files.append ( os.path.join ( Base_Path, 'demos_dummy.py' ))
Exe_Files.append ( 'support/demo_gui.py' )

