import wx


# ***********************************************************************
class New_Widget ( wx.Panel ) :
  def __init__ ( self, parent ) :
    wx.Panel.__init__ ( self, parent )
    s = self
    p = parent
    s.B = wx.Button ( self, -1, 'Bind' )
    E = wx.EVT_BUTTON

    s.B.Bind ( E, s.On_1, s.B )
    s.  Bind ( E, s.On_2, s.B )
    p.  Bind ( E, s.On_3, s.B )

    print 'Panel  ID', s.GetId ()
    print 'Button ID', s.B.GetId ()

  def On_1 ( self, event ) :
    print 'On_1 ',event.GetId()
    event.Skip()

  def On_2 ( self, event ) :
    print 'On_2 ',event.GetId()
    event.Skip()

  def On_3 ( self, event ) :
    print 'On_3 ',event.GetId()
    event.Skip()

  def Get_ID ( self ):
    return self.B.GetId()

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class tPanel_2 ( wx.MiniFrame ):
  def __init__ ( self ):
    wx.MiniFrame.__init__ (
      self, None,
      style = wx.DEFAULT_FRAME_STYLE )
    s = self
    E = wx.EVT_BUTTON

    # Create a New_Widget instance
    # and catch its events
    s.P = New_Widget ( self )
    s.P.Bind ( E, s.On_1B, s.P )
    s.  Bind ( E, s.On_2B )

  def On_1B ( self, event ) :
    print 'On_1B',event.GetId()
    #event.Skip()

  def On_2B ( self, event ) :
    print 'On_2B',event.GetId()
    event.Skip()
# ***********************************************************************


# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  app = wx.PySimpleApp ()
  frame = tPanel_2 ()
  frame.Show ( True )
  app.MainLoop ()
# ***********************************************************************


"""
  if 'Get_ID' in dir ( Control ) :
    Control_Pars ['ID'] = Control.Get_ID ()
  else:
    Control_Pars ['ID'] = Control.GetId()
"""

