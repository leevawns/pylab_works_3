# ***********************************************************************
# Searches all global classes in a file
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007 Stef Mientki
# mailto:S.Mientki@ru.nl
#
# <Version: 1.0    ,21-07-2007, Stef Mientki
#    - orginal release
# ***********************************************************************

from PyLab_Works_Globals import _, Set_Language
from PyLab_Works_Globals import TIO_NAMES, Test_Conditions
from PyLab_Works_Globals import *


# ***********************************************************************
# Creates a list with all classes defined in my_module
# (Imported classes are not included)
# If the module is NOT on the Pythonpath, my_path must be specified
# ***********************************************************************
def get_classes (my_module, my_path = None):
  import pyclbr
  if my_path != None:
    path = []
    path.append ( my_path )
    my_classes = pyclbr.readmodule_ex ( my_module, path )
  else:
    my_classes = pyclbr.readmodule_ex ( my_module )

  # now order them by linenr
  ordered_list = []
  for item in my_classes:
    if my_classes[item].module == my_module :
      name = my_classes[item].name
      if name [:2] == 't_' :
        ordered_list.append ( ( my_classes[item].lineno, my_classes[item].name [2:]  ) )
        """
        module -- the module name
        name -- the name of the class
        super -- a list of super classes (Class instances)
        methods -- a dictionary of methods
        file -- the file in which the class was defined
        lineno -- the line in the file on which the class statement occurred
        """

  # Sort the list
  ordered_list.sort()

  # now build a list with only brick names
  my_class_names = []
  for item in ordered_list:
    my_class_names.append ( item[1] )
  return my_class_names
# ***********************************************************************


# ***********************************************************************
# Creates a list with all devices defined in my_module
# If the module is NOT on the Pythonpath, my_path must be specified
# ***********************************************************************
def Get_PyLabWorks_Bricks2 ( my_module, my_path = None):
  my_classes = get_classes ( my_module, my_path)
  my_devices = []
  for my_class in my_classes:
    my_devices.append ( my_class )
  return my_devices
# ***********************************************************************

# ***********************************************************************
# Creates a list with all devices defined in my_module
# If the module is NOT on the Pythonpath, my_path must be specified
# ***********************************************************************
def Get_PyLabWorks_Bricks (my_module, my_path = None):
  my_classes = get_classes (my_module, my_path)
  my_devices = []
  for my_class in my_classes:
    my_devices.append ( (my_class , my_module) )
  return my_devices
# ***********************************************************************


# ***********************************************************************
# create a list of brick devices, without the path and fileextension
# ***********************************************************************
def Get_PyLabWorks_Bricks_PyFiles ():
  # find all available devices,
  # by looking for py-files with prefix "brick_"
  import glob
  import os
  path = os.getcwd()
  path = os.path.join ( path, 'bricks')
  my_files = glob.glob( os.path.join (path, 'brick_*.py') )
  py_files = []
  for file in my_files :
    filename = path_split ( file )[1]
    py_files.append ( os.path.splitext ( filename )[0] )
  return py_files
# ***********************************************************************


# ***********************************************************************
# Creates a list with all devices defined in my_path
# If my_path is not specified the current directory is taken
# The produced list looks like  <devicetype>  <file that contains it>
#    [('Button_1', 'device_BUTTONS')]
#    [('LED', 'device_LED')]
#    [('unknown', 'device_unknown')]
# ***********************************************************************
def Get_PyLabWorks_Bricks_All ( my_path = None):
  # find all available devices,
  # by looking for py-files with prefix "brick_"
  import glob
  import os
  if my_path == None:
    path = os.getcwd()
  else:
    path = my_path
  path = os.path.join ( path, 'bricks' )
  my_files = glob.glob( os.path.join (path, 'brick_*.py' ) )

  # in all device files search device-class definitions
  my_devices = []
  for my_file in my_files:
    my_file = path_split ( my_file )
    my_file = os.path.splitext ( my_file [1] )[0]
    my_devices = my_devices + Get_PyLabWorks_Bricks ( my_file, path)

  return my_devices
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Get_PyLabWorks_Bricks_All_Dict ( my_path = None):
  # find all available devices,
  # by looking for py-files with prefix "device_"
  import glob
  import os
  if my_path == None:
    path = os.getcwd()
  else:
    path = my_path
  path = os.path.join ( path, 'bricks' )
  my_files = glob.glob( os.path.join ( path, 'brick_*.py' ) )

  # in all device files search device-class definitions
  my_devices = {}
  for my_file in my_files:
    my_file = path_split ( my_file )
    my_file = os.path.splitext ( my_file [1] )[0]
    my_devices [ my_file ] = Get_PyLabWorks_Bricks2 ( my_file, path)

  return my_devices
# ***********************************************************************




# ***********************************************************************
# ***********************************************************************
def Generate_HTML_Library_Overview ( lang = 'US', Technical_Info = False ) :
  ##from brick import Control_Names
  #Technical_Info = False
  Set_Language ( lang )
  print ('PITY')

  # ***********************************************************************
  # ***********************************************************************
  HTML_Frame_1 = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
  <html><head><title>GUI Controls</title>
  <meta http-equiv="Content-Style-Type" content="text/css">
  <style type="text/css"><!--
  body {
    margin: 5px 5px 5px 5px;
    background-color: #ffffd4; )
  }
  --></style>
  <link type="text/css" href="rvf.css" rel="stylesheet">

  <body>
  <p><span class=rvts1>""" + _(1, 'Library Overview') + """&nbsp; </span>
     <img width=32 height=32 alt="" src="vippi_bricks_323.png"></p>
  <p>""" + _(13, 'Generated on' )

  HTML_Frame_2 = """</p>
  <p>""" + _(2, """This Library overview is automatically generated by Pylab_Works,
  from the local available source files.""") + """</p>
  <p><br></p>
  <hr noshade size=1>
  <p><span class=rvts2>"""+ _(3, 'Library Files') + '</span>&nbsp;&nbsp;&nbsp;&nbsp;' +\
  _(4, '(available languages)') + '</p>'

  HTML_Frame_3 = """<p><br></p>
  <p><span class=rvts2>"""

  HTML_Frame_5 = """<p><br></p>
  <p><span class=rvts2>"""

  HTML_Frame_99 = '</body></html>'
  # ***********************************************************************


  file = open ( 'd:/data_www/pylab_works/pw_lib_overview_'+\
                lang.lower()+'.html', 'w')

  
  import datetime
  line = HTML_Frame_1 + ' ' + str(datetime.date.today()) +\
         ',&nbsp;&nbsp;&nbsp;&nbsp; ' + _(5, 'language') + ' = ' + lang
  if Technical_Info :
    line += ',&nbsp;&nbsp;&nbsp;&nbsp; ' + _(6, 'switches') + ' = Technical'
  file.write ( line )

  # List of Library Files ( and available translations )
  file.write ( HTML_Frame_2 )
  Libraries = Get_PyLabWorks_Bricks_All_Dict ()
  lib_list = sorted ( Libraries.keys() )
  from language_support import Language_IDs
  for Lib in lib_list:
    line = '<p>&nbsp;&nbsp;&nbsp;&nbsp; ' + Lib +\
           '&nbsp;&nbsp;&nbsp;&nbsp;  ( US, '
    for Language in Language_IDs :
      #code = 'lang.' + Lib + '_' + Language
      code = Lib + '_' + Language
      try :
        #print '******** 222',line
        exec ( 'from ' + code + ' import LT')
        line += Language + ', '
      except :
        pass
        #print 'File not found:',code

    # remove the last comma
    line = line [:-2]
    line += ' )</p>\n'
    file.write ( line )

  if Technical_Info :
    # List of IO_Types
    file.write ( '<p><br></p>' )
    line = '<hr noshade size=1>  <p><span class=rvts2>' +\
          _(7, 'IO-Types') + '</span></p>'
    file.write ( line )
    file.write ( '<p>Number must still be changed to real type "TIO_NUMBER" ' + '</p>' )
    for IO_type in TIO_NAMES :
      line = str(IO_type) + ' : ' + TIO_NAMES [IO_type]
      file.write ( '<p>&nbsp;&nbsp;&nbsp;&nbsp;' + line + '</p>' )

    # List of Controls
    file.write ( '<p><br></p>' )
    line = '<hr noshade size=1>  <p><span class=rvts2>' +\
          _(8, 'GUI Controls') + '</span></p>'
    file.write ( line )
    file.write ( '<p>&nbsp;&nbsp;&nbsp;&nbsp; - Still to Implement' + '</p>' )


  for Lib in lib_list:
    file.write ( HTML_Frame_3 + '<hr noshade size=1>' + Lib + '</span></p>' )
    exec ( 'import '+Lib )
    
    # display the latest version + date
    try :
      version_line = eval ( Lib + '._Version_Text' )
      if not ( Technical_Info ) :
        file.write ( '<p>' + _(0, 'version: ') + str(version_line[0][0]) +
                     '&nbsp;&nbsp;&nbsp;&nbsp;' +
                     _(0, 'date: ') + version_line[0][1] + '</p>' )
    except :
      file.write ( '<p>' + _(0,'version unknown') + '</p>' )
      version_line = None

    # find the description for the library as a whole
    try :
      line = eval ( Lib + '.Description' )
      file.write ( '<p>'+ line + '</p>' )
      #print LIB + ' : ' + line
    except :
      pass

    if Technical_Info :
      # find the ICON-file of the library
      try :
        line = eval ( Lib + '.Library_Icon' )
        file.write ( '<p> Icon = '+ line + '</p>' )
      except :
        pass

      # find the Brick color of the library
      try :
        line = eval ( Lib + '.Library_Color' )
        file.write ( '<p> Color = '+ str(line) + '</p>' )
      except :
        #print 'lkop',line
        pass

    # display the history information
    if Technical_Info and version_line :
      try :
        for version in version_line :
          file.write ( '<br>' )
          #file.write ( '<p><span class=rvts3>' + _(9, 'Inputs' ) + ' : </span></p>' )
          file.write ( '<p><span class=rvts3>' +
                       _(0, 'version: ') + str(version[0]) + '</span>' +
                       '&nbsp;&nbsp;&nbsp;&nbsp;' +
                       _(0, 'date: ') + version[1] +
                       '&nbsp;&nbsp;&nbsp;&nbsp;' +
                       _(0, 'author: ') + version[2] + '</p>' )
          # test conditions
          header = '<p>' + _(0, 'Test Conditions:') + '</p>'
          for TC in version [4] :
            if header :
              file.write ( header )
              header = None
            file.write ( '<p>&nbsp;&nbsp;&nbsp;&nbsp; ' + Test_Conditions [TC] + '</p>' )
          line = version[5].lstrip().replace ( '\n', '<br>')
          file.write ( '<p>' + line + ' </p>' )
      except :
        pass

    # display the technical description
    if Technical_Info :
      try :
        line = eval ( Lib + '.__doc__' )
        if line :
          file.write ( '<br><p><span class=rvts3>'+
                       _(0, 'Technical Description' ) +
                       '</span></p>' )
          line = line.lstrip().replace ( '\n', '<br>')
          file.write ( '<p>' + line + ' </p>' )
      except :
        pass

    # Display the Bricks
    for Brick in Libraries [ Lib ]:
      file.write ( HTML_Frame_5+ Brick + '</span></p>\n' )
      line = eval ( Lib + '.t_'+ Brick + '.Description' )
      file.write ( '<p>'+ line + '</p>' )
      #file.write ( '<p><br></p>' )

      if Technical_Info :
        # now create the brick, to evaluate IO's
        line = 'Brick = ' + Lib + '.t_'+ Brick + '( None )'
        exec ( line )

        exec ( 'Inputs = Brick.Inputs' )
        header = False
        for S in  Inputs :
          if not ( header ) :
            file.write ( '<p><span class=rvts3>' + _(9, 'Inputs' ) + ' : </span></p>' )
            header = True
          # Name, type, required, helptext
          Input = Inputs [S]
          line = Input[0]
          if Input[3] != '' :
            line += ', (' + Input[3] + ')'
          line +=  ', type = ' + TIO_NAMES [ Input[1] ]
          if Input[2] :
            line += ', Required'
          file.write ( '<p> &nbsp; &nbsp; - ' + line + '</p>')

        exec ( 'Outputs = Brick.Outputs' )
        header = False
        for S in  Outputs :
          if not ( header ) :
            file.write ( '<p><span class=rvts3>' + _(10, 'Outputs') + ' : </span></p>' )
            header = True
          # Name, type, required, helptext
          Output = Outputs [S]
          line = Output [0]
          if (len(Output) > 2 ) and (Output[2] != '') :
            line += ', (' + Output[2] + ')'
          line +=  ', ' + TIO_NAMES [ Output[1] ]
          file.write ( '<p> &nbsp; &nbsp; - ' + line + '</p>')

        exec ( 'Controls = Brick.Control_Defs' )
        header = False
        for S in  Controls :
          if not ( header ) :
            file.write ( '<p><span class=rvts3>'+_(11, 'GUI Controls')+' : </span></p>' )
            header = True
          # Name, type, required, helptext
          ##line = Control_Names [ S ['Type'] ]
          line = 'UUUUUUUU',  ##Control_Names [ S.Type ]
          #line = str ( S ['Type'] )
          file.write ( '<p> &nbsp; &nbsp; - ' + line + '</p>')

        #file.write ( '<p><span class=rvts3>Parameters : </span></p>' )

        methods = [ 'Generate_Output_Signals' ]
        header = False
        for line in methods :
          exec ( 'result = "' + line + '" in dir ( Brick ) ' )
          if result :
            if not ( header ) :
              file.write ( '<p><span class=rvts3>'+ _(12, 'Methods') +' : </span></p>' )
              header = True
            file.write ( '<p> &nbsp; &nbsp; - ' + line + '</p>')

  file.write ( HTML_Frame_99 )
  file.close ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
if __name__ == "__main__":

  test = [ 2 ]     #3,4 geeft problemen


  if 1 in test :
    devices = Get_PyLabWorks_Bricks_All ()
    for device in devices:
      print ('aa',device)

  if 2 in test :
    Libraries = Get_PyLabWorks_Bricks_All_Dict ()
    lib_list = sorted ( Libraries.keys() )
    for Lib in lib_list:
      print ('****** '+ Lib)
      exec ( 'import '+Lib )
      for Brick in Libraries [ Lib ]:
        print ('*** ', Brick)
        line = eval ( Lib + '.t_'+ Brick + '.Description' )
        print (line)

  if 3 in test :
    import brick_Math
    print (version ( brick_Math ))
  
  if 4 in test :
    print ('OVERVIEW GENERATION')
    #Generate_HTML_Library_Overview ( )
    Generate_HTML_Library_Overview ( 'NL', True)

# ***********************************************************************
