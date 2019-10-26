
def do_more ( code ) :
      nonvar = [3,4]
      while len ( nonvar ) > 0 :
        nonvar.pop()
      return code + 'print "OK"\nvar2 = 67\nXXX=45\nPP11 = wx.Panel ( FORM )\n'

def sprint ( dic, text='' ) :
  print '*******************',text
  i = 0
  for key in dic :
    print i,str(dic[key])[:80]
    if type ( dic[key] ) == dict :
      for k in dic[key] :
        if k == 'IndexError' :
          break
        print ' ..  ', k, '=', str(dic[key][k])[:80]
    i += 1
    #if i >10 :
    #  break
  print

  
class Do_Something_In_Parent_NameSpace ( object ) :
  def __init__ ( self, code ) :
    
    import sys
    p_locals  = sys._getframe(1).f_locals
    p_globals = sys._getframe(1).f_globals
    code += 'var3 = 33\n'
    code += 'print "inside"\n'
    #exec ( code, p_globals, p_locals )
    try :
      exec code in p_globals, p_locals
      #exec ( code, p_globals, p_locals )
    except :

      #print 'ERROR', sys.exc_info()
      sys.excepthook( *sys.exc_info())


    """
    def do_more ( code ) :
      nonvar = [3,4]
      while len ( nonvar ) > 0 :
        nonvar.pop()
      return code + 'print "OOOOOOK"\n'
    """
    
    """
    code = do_more ( code )
    
    import sys
    p_locals  = sys._getframe(1).f_locals
    #for var in locals():
    #  print var
    sprint ( locals () , 'CLASS BEFORE')
    #sprint ( p_locals )
    #sprint ( sys._getframe(2).f_locals )
    
    p_globals = sys._getframe(1).f_globals
    #sprint ( globals () )
    #sprint ( p_globals )
    #sprint ( sys._getframe(2).f_globals )

    try :
      #exec ( code, p_globals, p_locals )
      exec code in p_globals, p_locals
    except :
      print 'ERROR'

    sprint ( locals () , 'CLASS BEFORE')
    #sprint ( p_locals )
    #sprint ( sys._getframe(2).f_locals )

    #sprint ( globals () )
    #sprint ( p_globals )
    #sprint ( sys._getframe(2).f_globals )
    """
    
"""
Command Line : -design
0 <module 'sys' (built-in)>
1 <test_upframe2.Do_Something_In_Parent_NameSpace object at 0x
2 {'code': 'print var1 + 3 \n', 'pyscripter': <module 'pyscrip
3 print var1 + 3
print "OK"
var2 = 67


0 print var1 + 3

1 <module 'pyscripter' (built-in)>
2 33
3 {'IndexError': <type 'exceptions.IndexError'>, 'all': <built
4 __main__
5 D:\Data_Python_25\support\test_upframe.py
6 None
7 <module 'test_upframe2' from 'D:\Data_Python_25\support\test

0 <module '__main__' from 'C:\Documents and Settings\Administr
1 {'code': 'print var1 + 3 \n', 'pyscripter': <module 'pyscrip
2 <?.RemotePythonInterpreter instance at 0x00AF1D00>
3 <code object <module> at 00AFED10, file "D:\Data_Python_25\s
4 <module 'sys' (built-in)>
5 <module 'imp' (built-in)>
6 {'pyscripter': <module 'pyscripter' (built-in)>, '__builtins
7 {'code': 'print var1 + 3 \n', 'pyscripter': <module 'pyscrip
8 <module '__main__' from 'D:\Data_Python_25\support\test_upfr
9 <module 'types' from 'P:\Python\lib\types.pyc'>
10 True
"""