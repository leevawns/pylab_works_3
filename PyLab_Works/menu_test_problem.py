
import wx

# ***********************************************************************
# ***********************************************************************
class Simple_Test_Form ( wx.MiniFrame ):
  def __init__ ( self, ini = None ):
    wx.MiniFrame.__init__( self, None, style = wx.DEFAULT_FRAME_STYLE  )

    self.PU1 = wx.Menu ()
    self.item1 = self.PU1.Append (wx.ID_ANY, 'test1' )

    self.PU2 = wx.Menu ()
    item = self.PU2.AppendCheckItem (wx.ID_ANY, 'test2' )
    #item.SetCheckable ( True )
    item.Check ( True )

    self.Bind ( wx.EVT_CONTEXT_MENU, self._OnShowPopup )
    self.Bind ( wx.EVT_MENU,         self.OnSelect, item )

    self.Show()

  def _OnShowPopup ( self, event ) :
    x =  self.ScreenToClient ( event.GetPosition () ) [0]
    if x < 100 :
      self.item1.SetCheckable ( True )
      self.item1.Check ( True )
      self.PopupMenu ( self.PU1)
    else :
      self.PopupMenu ( self.PU2)

  def OnSelect ( self, event ) :
    print 'Menu Item Selected'



# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  app = wx.PySimpleApp ()
  frame = Simple_Test_Form ()
  app.MainLoop ()
# ***********************************************************************

