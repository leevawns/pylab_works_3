


import test_upframe2

if __name__ == '__main__':

  var2 = 22
  code = 'print "POLP",var2 \nprint var1\n'
  test_upframe2.Do_Something_In_Parent_NameSpace ( code )
  print var2, var3


  """
  import wx
  app = wx.PySimpleApp ()
  FORM = wx.Frame (None)
  P1 = wx.Panel ( FORM )
  P1.SetForegroundColour (wx.RED)

  var555 = [ 555, 666]
  var1 = 33
  code = 'print var1 + 3 \nprint var44\n'
  test_upframe2.Do_Something_In_Parent_NameSpace ( code )
  test_upframe2.sprint ( locals (), 'LOCALS AFTER' )
  test_upframe2.sprint ( globals (), 'GLOABLS AFTER' )
  #test_upframe2.sprint ( dir() )
  print dir()

  PP11.SetForegroundColour (wx.RED)
  print var2
  print P1
  print PP11
  """