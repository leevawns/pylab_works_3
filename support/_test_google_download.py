# -*- coding: utf-8 -*-
import  urllib, urllib2, string, os, time,traceback,threading
from    xml.dom     import minidom
from    types       import *
from    base64      import b64encode

HOME_DIR        =   os.getcwd().replace(";","")+"/"

########################## Cookie code thanks to WEnder ###############################
import cookielib
MyCookies       =   cookielib.LWPCookieJar()
COOKIEFILE      =   HOME_DIR + 'cookies.lwp'
if os.path.isfile(COOKIEFILE)   :   MyCookies.load(COOKIEFILE)
Cookie_Opener   = urllib2.build_opener(urllib2.HTTPCookieProcessor(MyCookies))
urllib2.install_opener(Cookie_Opener)
#######################################################################################

class Download_URL(threading.Thread):
    def __init__(self,win,url,post='',login=''):
        threading.Thread.__init__(self)
        self.win        =   win
        self.url        =   url
        self.post       =   post
        self.login      =   login


    def terminate(self):
        self.join(0.5)


    def run(self):
        try :
            print '--CheckUrl'
            header  = self.checklogin()
            reqst   = urllib2.Request(self.url,self.post,headers=header)
            reqst.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.3) Gecko/20070309 Firefox/2.0.0.3')
            html                = urllib2.urlopen(reqst)
            data                = html.read()
            #self.win.WEBDATA    = data
            self.win            = data
            html.close()
            self.SaveCookie()
        except:
            print header
            import traceback
            #print data
            traceback.print_stack()
            traceback.print_exc()
            #self.win.WEBDATA = None


    def checklogin(self):
        if self.login != '' :
            return {'Authorization':'Basic '+ str(b64encode(self.login))}
        else                :
            return {}


    def SaveCookie(self):
        try :
            print '--SaveCookie'
            MyCookies.save(COOKIEFILE)
        except:
            import traceback
            traceback.print_exc()
            
# ***********************************************************************
# Test application in case this file is runned separatly
# ***********************************************************************
if __name__ == '__main__':
  url = 'http://code.google.com/p/pylab-works/downloads/list'
  win = []
  aap = Download_URL ( win, url, post='', login='')
  aap.start()
  print aap
  print win
# ***********************************************************************
pd_Module ( __file__ )
