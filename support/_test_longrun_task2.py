import time
from threading import *
import wx


import lxml.html
from urllib import urlencode
import threading
import datetime

# Button definitions
ID_START = wx.NewId()
ID_STOP = wx.NewId()


# *************************************************************
# Define notification event for thread completion
# *************************************************************
EVT_RESULT_ID = wx.NewId()
# *************************************************************


# *************************************************************
# *************************************************************
class ResultEvent(wx.PyEvent):
  def __init__(self, data):
    wx.PyEvent.__init__(self)
    self.SetEventType ( EVT_RESULT_ID )
    self.data = data
# *************************************************************


# *************************************************************
# *************************************************************
class Thread_BabelFish_Translation ( Thread ) :
  def __init__ ( self, notify_window, lang, text ) :
    Thread.__init__ ( self )
    self._notify_window = notify_window
    self.lang = lang
    self.text = text
    self.setDaemon (1)
    self.start ()

  def run ( self ) :
    BABLEFISH_URL = 'http://babelfish.altavista.com/tr'
    url = BABLEFISH_URL + '?' +\
          urlencode ( { 'trtext' : self.text,
                        'lp'     : 'en_' + self.lang.lower () } )
    page = lxml.html.parse(url)
    Babel_Result = []
    for div in page.iter ( 'div' ) :
      style = div.get ( 'style' )
      #if ( style != None )  and  ( 'padding:10px;' in style ) :
      if ( style != None )  and  ( 'padding:0.6em;' in style ) :
        Babel_Result.append(
          lxml.html.tostring ( div, method = "text" ) ) #, with_tail=False))

    if Babel_Result :
      Result = Babel_Result[0]
    else :
      Result = 'Babel Fish translation Failed'
    
    wx.PostEvent(self._notify_window, ResultEvent( Result ))
# *************************************************************


# *************************************************************
# GUI Frame class that spins off the worker thread
# *************************************************************
class MainFrame(wx.Frame):
  """Class MainFrame."""
  def __init__(self, parent, id):
      """Create the MainFrame."""
      wx.Frame.__init__(self, parent, id, 'Thread Test')

      # Dumb sample frame with two buttons
      wx.Button(self, ID_START, 'Start', pos=(0,0))
      wx.Button(self, ID_STOP, 'Stop', pos=(0,50))
      self.status = wx.StaticText(self, -1, '', pos=(0,100))

      self.Bind(wx.EVT_BUTTON, self.OnStart, id=ID_START)

      # Set up event handler for any worker thread results
      self.Connect ( -1, -1, EVT_RESULT_ID, self.On_BabelFish_Result )


  def OnStart ( self, event ) :
    self.status.SetLabel('Starting computation')
    Thread_BabelFish_Translation ( self, 'NL', 'I want to get to Amsterdam by train')

  def On_BabelFish_Result ( self, event ) :
    self.status.SetLabel('Computation Result: %s' % event.data)



class MainApp(wx.App):
    """Class Main App."""
    def OnInit(self):
        """Init Main App."""
        self.frame = MainFrame(None, -1)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    app = MainApp(0)
    app.MainLoop()
# ***********************************************************************
pd_Module ( __file__ )
