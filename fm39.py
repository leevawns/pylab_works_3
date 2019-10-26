import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, size=(300,200))
        ##MyPanel(self)

        self.SplitV = wx.SplitterWindow ( self )
        self.P1     = wx.Panel ( self.SplitV )

        self.t      = wx.TextCtrl ( self.SplitV,style = wx.TE_MULTILINE | wx.TE_RICH)
        #self.t      = wx.TextCtrl ( self.SplitV,style = wx.TE_MULTILINE )

        #self.SplitV.SplitHorizontally ( self.P1, self.t )
        self.SplitV.SplitVertically ( self.P1, self.t )

        Sizer = wx.BoxSizer ( )
        Sizer.Add ( self.SplitV, 1, wx.EXPAND )
        self.SetSizer ( Sizer )

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.updateLog)
        self.timer.Start(500)

        self.lineno = 0

    def updateLog(self,evt):
        self.lineno += 1
        if self.lineno <= 100:
            line = 'this is line %s\n' % self.lineno
            self.t.AppendText(line)
            #line='\n'
            #self.t.AppendText(line)
#           self.t.ShowPosition(self.t.LastPosition)
        else:
            self.timer.Stop()


class MyPanel(wx.Panel):
    def __init__(self, frame):
        wx.Panel.__init__(self, frame)
        self.t = wx.TextCtrl(self,size=frame.GetClientSize(),
          style=wx.TE_MULTILINE | wx.TE_RICH2)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER,self.updateLog)
        self.timer.Start(100)

        self.lineno = 0

    def updateLog(self,evt):
        self.lineno += 1
        if self.lineno <= 20:
            line = 'this is line %s\n' % self.lineno
            self.t.AppendText(line)
            line='\n'
            self.t.AppendText(line)
#           self.t.ShowPosition(self.t.LastPosition)
        else:
            self.timer.Stop()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, "Logging Text Control")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

app = MyApp(0)
app.MainLoop()
