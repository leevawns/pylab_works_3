#! /usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wx.lib.delayedresult as delayedresult

class MyFrame(wx.Frame):
    def __init__(self, parent, log):
        # Layout
        wx.Frame.__init__(self, parent, -1, title=u"TestFrame")
        self.parent = parent
        self.p = wx.Panel(self,-1)
        sizer = wx.BoxSizer()
        self.button = wx.Button(self.p,-1,label ="Press this button to Go")
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.button)
        self.tc = wx.TextCtrl(self.p, -1, "Hello", style=wx.TE_RIGHT)
        sizer.Add(self.button, 1, wx.ALL|wx.EXPAND|wx.ALIGN_BOTTOM, 2)
        sizer.Add(self.tc, 1, wx.ALL|wx.EXPAND, 3)
        self.p.SetSizer(sizer)
        sizer.Fit(self.p)
        sizer.SetSizeHints(self.p)
        self.Layout()
        self.Centre()

        # Used by the threads
        #############################################
        self.jobID = 0
        self.abortEvent = delayedresult.AbortEvent()
        #############################################

    def OnButton(self,evt):
        print"Go"
        ###################################################
        self.handleGet( fn_Producer = self._resultProducer,
                        argProd = 1000000,
                        fn_Consumer = self._resultConsumer)
        ###################################################

    def handleGet(self, fn_Producer, argProd, fn_Consumer):
        self.abortEvent.clear()
        self.jobID += 1
        print "Starting job %s in producer thread: GUI remains responsive" %self.jobID
        delayedresult.startWorker(fn_Consumer, fn_Producer,
                                  wargs=(self.jobID,self.abortEvent,argProd),
jobID=self.jobID)

    def _resultProducer(self, jobID, abortEvent, argProd):
        """Pretend to be a complex worker function or something that takes
        long time to run due to network access etc. GUI will freeze if this
        method is not called in separate thread."""
        count = 0
        myresult = None

        while not abortEvent() and count < 1:
            count += 1
            print 'Inside the thread, we call the long running task'
            ##########################################################
            myresult = self.LongTask()
            ##########################################################
        return myresult#jobID

    def _resultConsumer(self, delayedResult):
        jobID = delayedResult.getJobID()
        print "From Consumer jobID = ", jobID
        print "From Consumer self.jobID = ", self.jobID
        assert jobID == self.jobID
        try:
            result = delayedResult.get()
        except Exception, exc:
            print "Result for job %s raised exception: %s" % (jobID, exc)
            return
        # output result
        print "Got result for job %s: %s" % (jobID, result)

        # Here, we print the result in the textcontrl
        #############################################
        self.tc.ChangeValue(str(result))
        #############################################

    def LongTask(self):
        """Just something that takes some time: a big randomly issued list
        Returns the first 10 sorted elements of the list (as a string)"""
        import random
        import time
        list_to_sort=[]
        a = time.clock()
        print "Start - Building list"
        for i in range(1,1000000):
            list_to_sort.append(random.randint(1, 1000000))
        print "Sorting list"
        b = time.clock()
        list_to_sort.sort()
        c = time.clock()
        print "Stop"
        print b-a
        print c-b
        return str(list_to_sort[0:10])

if __name__ == '__main__':
    import sys
    app = wx.PySimpleApp()
    frame = MyFrame(None, sys.stdout)
    frame.Show(True)
    app.MainLoop()

# ***********************************************************************
pd_Module ( __file__ )
