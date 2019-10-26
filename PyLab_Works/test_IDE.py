from test_IDE_sub import *


#stc.StyledTextCtrl.
#wx.stc.StyledTextCtrl.AcceleratorTable 
#i='hdasda'    
#stc.StyledTextCtrl.Star 


#stc.STC_STYLE_INDENTGUIDE 
#stc.StyledTextCtrl.AddTextRaw (
#aap
#wx.Button.__init__(dsdpsd, xcz, zxc    

#  stc.EVT_STC_CALLTIP_CLICK
#stc.EVT_STC_DWELLSTART 
#stc.EVT_STC_DWELLEND 

#os.path.join((())   
#test_string = """xxxaap"""


class my_Test_Form ( My_Frame_Class ) :

  # *****************************************************************
  # *****************************************************************
  def __init__( self, main_form= None, ini = None ) :

    My_Frame_Class.__init__ ( self, main_form, 'My_Title', ini, 'Test Form' )

    # ***********************************************************************
    from Scintilla_support import Base_STC

    GUI = """
      self.SplitV         ,SplitterVer
        self.Edit         ,Base_STC
        self.Edit2         ,Base_STC
    """
    #from Scintilla_support import Base_STC
    self.wxGUI = Create_wxGUI ( GUI, IniName = 'self.Ini_File' )
    # **********************************************************************
    #print self.wxGUI.code
    # some text
    self.wxGUI.Ready()
    if self.Ini_File :
      self.Ini_File.Section = self.Ini_Section
      self.wxGUI.Save_Settings ()


# ***********************************************************************
if __name__ == '__main__':
  a = 10
  import time
  #a        = wx.stc 
   
  #wx.Config 

  while a < 2000 :
    for i in range ( 10 ) :
      a = 10 * i
      time.sleep(1)
      print (Test_RPDB2 ( a ))
      """
      print i
      print a
      print Test_RPDB2 ( a )



      b = Test_RPDB2 ( a )
      print b
      """

  a = test_string
  while '  ' in a :
    a = a.replace ( '  ', ' ' )
  a = a.replace ( '( ', '(' )
  a = a.replace ( ' (', '(' )
  a = a.replace ( ') ', ')' )
  a = a.replace ( ' )', ')' )
  a = a.replace ( '[ ', ']' )
  a = a.replace ( ' [', ']' )
  a = a.replace ( '] ', ']' )
  a = a.replace ( ' ]', ']' )
  a = a.replace ( '# ', '#' )
  a = a.replace ( ':', '' )

  a = a.split()
  import keyword
  b = []
  for word in a :
    if not ( keyword.iskeyword ( word ) ) and \
       not ( word[0] in '=><*+-/!#0123456789' ) and \
       not ( word in b ) :
      b.append ( word )
  print (b)

  from inspect import *
  a = []
  for word in b :
    line = "type ( "+ word+ ")"
    try :
      print (word, eval ( line ))
      #print eval ( 'getfile ( '+ word+' )' )
    except :
      a.append ( word )
  for word in a :
    b.remove ( word )

  print (b)
  """
  {
    'a': 10, '
     b': 20,
     'Test_RPDB2': <function Test_RPDB2 at 0x00D7F6B0>,
     '__builtins__': <module '__builtin__' (built-in)>,
     '__file__': 'd:/data_python_25/pylab_works/test_ide.py',
     'i': 1,
     '__name__': '__main__',
     '__doc__': None,
{'a': 10, 'b': 20, 'Test_RPDB2': <function Test_RPDB2 at 0x00D7F6B0>, '__builtins
__': <module '__builtin__' (built-in)>, '__file__': 'd:/data_python_25/pylab_w
orks/test_ide.py', 'i': 1, '__name__': '__main__', '__doc__': None, 'test_string
': "\nif __name__ == '__main__':\n a = 10\n while a < 200 :\n  for i in range ( 1
0 ) :\n\n    a = 10 * i\n    a = beer.coaloa.dpd[3][3]\n    print i\n    print a\
n    print Test_RPDB2 (   a )\n    b = Test_RPDB2 ( a )\n    print b\n\n  #cv\n
print 'hello3dttu'\n"}
  """
  #cv
  print ('hello3dttu')
  
  My_Main_Application ( Simple_Test_Form )
