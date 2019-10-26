"""
@summary: UnitTests for the PyGoogleDesktop Interface


@author: Jack G. Atkinson Jr.
@organization: Doxa Logos Technologies, Inc.
@copyright: (c) 2008, Doxa Logos Technologies, Inc.
@license: BSD-Style (see license.txt)
@version: 1.0
@requires: Python 2.4 and the win32all extensions for Python 2.4 on Windows.
Will not work unless Google Desktop Search 1.0 or later is installed.
"""
import sys
sys.path.append ( 'P:/Python/Scripts' )

import pygoogledesktop
import unittest
import sys

class TestPyGDS(unittest.TestCase):

   def setUp(self):
       self.desc = {"title":'TestPyGDS', "description":'Unit testing the PyGDS module',
                 "icon":"%SystemRoot%\system32\SHELL.DLL,134"}
       self.guid = '{8917033D-5D79-4c69-B133-E60D4CA6BF43}'
       self.pyGDS = pygoogledesktop.PyGDS()
       #register the app
       self.cookie = self.pyGDS.RegisterAppQueryAPI(self.guid,self.desc,True)
       self.failIfEqual(self.cookie,None)
       return


   def tearDown(self):
       #unregister the app
       self.pyGDS.UnRegisterApp(self.guid)
       return

   def testQuery(self):
       self.pyGDS.EnableDebug()
       #perform a query
       results = self.pyGDS.DoQuery(self.cookie,"PacketAmcpClass",'File')
       self.failIfEqual(results,None)
       return

   def testQueryHTTP(self):
       self.pyGDS.EnableDebug()
       results = self.pyGDS.DoQueryHTTP("PacketAmcpClass George \"Jay Atkinson\"",numResults=100,category='file')

   def testQueryHTTPAll(self):
       self.pyGDS.EnableDebug()
       results = self.pyGDS.DoQueryHTTP("PacketAmcpClass",numResults=0,category='file')

if __name__ == '__main__':
   unittest.main()
