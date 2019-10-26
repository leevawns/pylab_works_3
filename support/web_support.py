import __init__

# ***********************************************************************
from General_Globals import *
from language_support import  _

# ***********************************************************************
__doc__ = """
blabla

License: freeware, under the terms of the BSD-license
Copyright (C) 2008 Stef Mientki
mailto:S.Mientki@ru.nl
"""

# ***********************************************************************
_Version_Text = [

[ 1.1, '10-10-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
  - Read_PuntHoofd_Tree added
""" ) ],

[ 1.0, '10-03-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, """
    - orginal release
""" ) ]
]
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
import webbrowser
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
def Read_PuntHoofd_Tree ( filename ) :
  fh = open ( filename, 'r' )
  html = fh.read ()
  fh.close ()

  Tree = []

  # search the root
  start   = html.find ( '<div>'  )
  start   = html.find ( 'href=',  start )
  finish2 = html.find ( 'target', start )
  root = html [ start + 6 : finish2 - 2]
  Tree.append ( ( 0, root ) )

  start = html.find ( '<!---- New Tree --------->', finish2 )
  start1 = start + 28
  start = start1
  #print start1, html [start1: start1+20]

  found = True
  Indent = 1
  while found :
    Indent_Later = False
    start1  = html.find ( '<div>',       start )
    start2  = html.find ( '<div class=', start )
    #print start1, start2, html[start1:start2]

    # if "<div class" before "<div>" means a new root element
    if 0 <= start2 < start1 :
      Indent_Later = True

    # if "</div>" before "<div>" we jump back to the root
    start2  = html.find ( '</div>', start )
    if 0 <= start2 < start1 :
      Indent -= 1
      start = start2 + 4

    # by now we should be able to find  "<div> ... </div>"
    start1  = html.find ( '<div>',  start  )
    finish1 = html.find ( '</div>', start1 )
    if 0 <= start1 < finish1 :
      start2  = html.find ( 'href=',  start1, finish1 )
      finish2 = html.find ( 'target', start1, finish1 )
      if 0 <= start2 < finish2 :
        root   = html [ start2 + 6 : finish2 - 2]
        Tree.append ( ( Indent, root ) )
    else :
      found = False
    start = finish1 + 4
    if Indent_Later :
      Indent += 1
  return Tree
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def send_mail ( to = None, subject = None, body = None, cc = None ):
  """
  encodes the content as a mailto link as described on
  http://www.faqs.org/rfcs/rfc2368.html
  Examples partly taken from
  http://selfhtml.teamone.de/html/verweise/email.htm
  (Excerpt from http://svn.berlios.de/wsvn/lino/trunk/src/lino/tools/mail.py?op=file&rev=0&sc=0)
  """
  import urllib
  url = "mailto:" + urllib.quote(to.strip(),"@,")
  sep = "?"
  if cc:
    url+= sep + "cc=" + urllib.quote(cc,"@,")
    sep = "&"
  if subject:
    url+= sep + "subject=" + urllib.quote(subject,"")
    sep = "&"
  if body:
    # Also note that line breaks in the body of a message MUST be
    # encoded with "%0D%0A". (RFC 2368)
    body="\r\n".join(body.splitlines())
    url+= sep + "body=" + urllib.quote(body,"")
    sep = "&"
  webbrowser.open(url,new=1)
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def download ( url ):
  import urllib
  print (url)
  return urllib.urlretrieve (url)
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
def PyLab_Works_Google_Files () :
  print ('Retrieving Google Download List ... ',)
  Google_Files = []
  
  url = 'http://code.google.com/p/pylab-works/downloads/list'
  filename, header = download ( url )
  #print 'filename:', filename
  print ('header :', header)

  fh = open ( filename )
  lines = fh.readlines ()
  fh.close()

  # make 1 string of it
  lines = ''.join ( lines )
  #print lines


  """
  For downloadfiles in the list, search for
      <td class="vt id col_0">
       <a href="http://pylab-works.googlecode.com/files/

    control_grid.py

       " style="white-space:nowrap" >control_grid.py</a>
      </td>
      <td class="vt col_1" width="100%" onclick="if (!cancelBubble) _go('detail?name=control_grid.py&amp;can=2&amp;q=')" >
        <a onclick="cancelBubble=true;" href="detail?name=control_grid.py&amp;can=2&amp;q=">

    general purpose grid

        </a>
      </td>
      <td class="vt col_2" onclick="if (!cancelBubble) _go('detail?name=control_grid.py&amp;can=2&amp;q=')" >
        <a onclick="cancelBubble=true;" href="detail?name=control_grid.py&amp;can=2&amp;q=" style="white-space:nowrap">

    Jul 13

        </a></td>
  """

  download_location = 'href="http://pylab-works.googlecode.com/files/'
  # split at the file links
  lines = lines.split ( download_location )

  for line in lines [1:] :
    E = line.find ( '"' )
    filename = [ line [ : E] ]
    #print 'PPP',line[:200],"QQQ",B,E

    # Description
    B = line.find ( 'href', E )
    B = line.find ( '>',    B )
    E = line.find ( '</a>', B )
    filename.append ( line [ B+1: E ] )

    # Upload Date
    B = line.find ( 'href', E )
    B = line.find ( '>',    B )
    E = line.find ( '</a>',    B )
    filename.append ( line [ B+1 : E ] )

    Google_Files.append ( filename )
  print ('... Done')
  return Google_Files
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
if __name__ == "__main__":
  
  test = [3]
  
  if 1 in test :
    send_mail ( 'punthoofd@flappie.nl', 'JALsPy bug report' )
    
  if 2 in test :
    url = 'http://code.google.com/p/pylab-works/downloads/list'
    """
    For downloadfiles in the list, search for
     <a href="http://pylab-works.googlecode.com/files/control_grid.py"
     style="white-space:nowrap">control_grid.py</a>
    """

    #url = 'http://pylab-works.googlecode.com/files/control_grid.py'
    filename, header = download ( url )
    print ('filename:', filename)
    print ('header :', header)


    #filename = 'c:/docume~1/admini~1/locals~1/temp/tmpoqerie'
    fh = open ( filename )
    lines = fh.readlines ()
    fh.close()
    
    #print lines

    # make 1 string of it
    lines = ''.join ( lines )
    # split at the links
    lines = lines.split ( '<a')
    #print lines
    download_location = 'http://pylab-works.googlecode.com/files/'
    DL = len ( download_location )
    for line in lines :
      S = line.find ( download_location )
      if S >= 0 :
        E = line.find ( '"', S )
        print ('*****',line [ S + DL : E])

  if 3 in test :
    Google_Files = PyLab_Works_Google_Files ()
    print ('*****  PyLab_Works files at Google Code *****')
    for file in Google_Files :
      print (file)
      
      
  if 4 in test :
    url = 'http://code.google.com/p/pylab-works/downloads/list'

    import lxml.html
    #from urllib import urlencode
    page = lxml.html.parse(url)

    print (page)
    Babel_Result = []
    ## Babel Fish result: <div style="padding:0.6em;">I want travel with the train</div>
    """
    For downloadfiles in the list, search for
     <a href="http://pylab-works.googlecode.com/files/control_grid.py"
     style="white-space:nowrap">control_grid.py</a>
    """
    #print zzaap'
    for div in page.iter ( 'a href' ) :
      print  (lxml.html.tostring ( div, method = "text" ))  #, with_tail=False)))

    print ('beer')
    for div in page.iter ( 'div' ) :
      style = div.get ( 'style' )
      #if ( style != None )  and  ( 'padding:10px;' in style ) :
      if ( style != None )  and  ( 'padding:0.6em;' in style ) :
        Babel_Result.append(
          lxml.html.tostring ( div, method = "text" ) ) #, with_tail=False))
# ***********************************************************************
pd_Module ( __file__ )
