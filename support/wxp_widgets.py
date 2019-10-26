import __init__
# ***********************************************************************
"""
import sys
subdirs = [ '../support' ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
"""

from General_Globals  import *
from language_support import _

__doc__ = """
"""

# ***********************************************************************
_Version_Text = [
[ 1.2 , '19-10-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - Translate_CSS, improved by replacing unnessary paragraph tags
""")],

[ 1.1 , '10-10-2008', 'Stef Mientki',
'Test Conditions:', (2,),
_(0, """
 - callback to parent implemented, still needs some improvement
 - started with implementation of PW, bitmapbutton, not ready yet
 - Translate_CSS, if source file not available, creates an html error page
""")],

[ 1.0 , '14-03-2008', 'Stef Mientki',
'Test Conditions:', (),
_(0, ' - orginal release')]
]
# ***********************************************************************



"""
import os
import sys
subdirs = [ '../support', ]
for subdir in subdirs:
  if not ( subdir in sys.path) : sys.path.append ( subdir )
"""
import  wx
from system_support import *

_Widget_Number = 0


# ***********************************************************************
# If an event occures,
# it's send back to the owner / main-program by this function
# ***********************************************************************
CallBack_Html_Pointer = None
def _Do_CallBack ( text ):
  if CallBack_Html_Pointer :
    CallBack_Html_Pointer ( text )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class TextBox(wx.Panel):
  def __init__(self, parent, id=-1, size = wx.DefaultSize ) : #, bgcolor=None):
    wx.Panel.__init__(self, parent, id, size = size)
    #self.Text = wx.TextCtrl ( self, -1,
    #                         style = wx.TE_MULTILINE | wx.TE_PROCESS_ENTER )

    import wx.richtext as rt
    
    self.Text = rt.RichTextCtrl ( self,
                 style = wx.VSCROLL|wx.HSCROLL\
                         |wx.TE_MULTILINE|wx.TE_PROCESS_ENTER \
                         |wx.WANTS_CHARS );    # VERY ESSENTIAL TO CATCH ARROW KEYS
    #|wx.NO_BORDER

    # make sure we haven't already added them.
    if not ( rt.RichTextBuffer.FindHandlerByType(rt.RICHTEXT_TYPE_HTML) ) :

      # This would normally go in your app's OnInit method.  I'm
      # not sure why these file handlers are not loaded by
      # default by the C++ richtext code, I guess it's so you
      # can change the name or extension if you wanted...
      rt.RichTextBuffer.AddHandler(rt.RichTextHTMLHandler())
      rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler())

      """
      # ...like this
      rt.RichTextBuffer.AddHandler(rt.RichTextXMLHandler(name="Other XML",
                                                         ext="ox",
                                                         type=99))
      """
      # This is needed for the view as HTML option since we tell it
      # to store the images in the memory file system.
      wx.FileSystem.AddHandler(wx.MemoryFSHandler())


    self.Text.Bind ( wx.EVT_KEY_DOWN, self.OnKeyDown )

    self.sizer = wx.BoxSizer ( wx.VERTICAL )
    self.sizer.Add ( self.Text, 1, wx.EXPAND )
    self.SetSizer ( self.sizer )

  # Because Ctrl-V is not supported, we catch it here
  def OnKeyDown ( self, event ) :
    if (event.GetKeyCode() == 86 ) and event.ControlDown() :
      self.Text.Paste()
    event.Skip ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class PrevNext ( wx.Panel ):
  def __init__(self, parent, id=-1 , size = wx.DefaultSize, Button ='PN' ) :
    wx.Panel.__init__(self, parent, id, size = ( 300, 28 ))
    global _Widget_Number

    if 'P' in Button :
      self.Return_Code1 = _Widget_Number
      _Widget_Number += 1
      btn1 = wx.Button ( self, -1, 'Previous', ( 0, 5 ) )
      self.Bind ( wx.EVT_BUTTON, self.OnClick1, btn1 )

    if 'N' in Button :
      self.Return_Code2 = _Widget_Number
      _Widget_Number += 1
      btn2 = wx.Button ( self, -1, 'Next', ( 90, 5 ) )
      self.Bind ( wx.EVT_BUTTON, self.OnClick2, btn2 )

  def OnClick1 ( self, event ):
    _Do_CallBack ( self.Return_Code1 )

  def OnClick2 ( self, event ):
    _Do_CallBack ( self.Return_Code2 )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class PW ( wx.Panel ):
  def __init__(self, parent, id=-1 , size = wx.DefaultSize, Demo ='non' ) :
    wx.Panel.__init__(self, parent, id, size = ( 32,32 ))

    self.Demo = Demo
    global _Widget_Number
    self.Return_Code1 = _Widget_Number
    _Widget_Number += 1
    btn1 = wx.Button ( self, -1, 'Previous', ( 0, 5 ) )
    self.Bind ( wx.EVT_BUTTON, self.OnClick1, btn1 )

  def OnClick1 ( self, event ):
    _Do_CallBack ( str(self.Return_Code1) + self.Demo )

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Prev ( PrevNext ):
  def __init__(self, parent, id=-1 , size = wx.DefaultSize ) :
    PrevNext.__init__( self, parent, id, size, 'P')
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class Next ( PrevNext ):
  def __init__(self, parent, id=-1 , size = wx.DefaultSize ) :
    PrevNext.__init__( self, parent, id, size, 'N')
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class RadioBox(wx.Panel):
  def __init__(self, parent, id=-1, size = wx.DefaultSize, Labels=None ) : #, bgcolor=None):
    wx.Panel.__init__(self, parent, id, size = size)

    if not ( Labels ):
      Labels = ['zero', 'onefdsf en erg lang nnog ',
                  'six', 'seven', 'eight']
    self.rb = wx.RadioBox(
            self, -1, "", wx.DefaultPosition, wx.DefaultSize,
            Labels , 1 )
    
    # to get the size right,
    # make the height of the panel equal to the RadioBox,
    # before letting the sizer do it's work
    # No make no selection: we select the last, but don't display it
    # Ugly, but it works
    self.SetSize ( ( self.GetSize()[0], self.rb.GetSize()[1] - 25 ) )
    self.rb.SetSelection ( self.rb.GetCount() - 1 )

    sizer = wx.BoxSizer ( wx.VERTICAL )
    sizer.Add ( self.rb, 0, wx.ALL )
    self.SetSizer ( sizer )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class CheckBoxes(wx.Panel):
  def __init__(self, parent, id=-1, size = wx.DefaultSize, Labels=None ) : #, bgcolor=None):
    wx.Panel.__init__(self, parent, id, size = size)


    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add ( (20,10))

    if not ( Labels ):
      Labels = ['zero', 'onefdsf en erg lang nnog ',
                  'six', 'seven', 'eight']
    self.CB = []
    for item in Labels:
      cb = wx.CheckBox(self, -1, item )
      self.CB.append ( cb )
      sizer.Add ( cb )
      sizer.Add ( (20,10))

    # keep track of number of labels
    self.N = len(Labels)

    # to get the size right,
    # make the height of the panel equal to the RadioBox,
    # before letting the sizer do it's work
    self.SetSize ( ( self.GetSize()[0], self.N * 25 ) )
    self.SetSizer(sizer)
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class EditBoxes(wx.Panel):
  def __init__(self, parent, id=-1, size = wx.DefaultSize, Labels=None ) : #, bgcolor=None):
    wx.Panel.__init__(self, parent, id, size = size)

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer2 = wx.BoxSizer(wx.VERTICAL)
    sizer.Add ( (0,5))
    sizer2.Add ( (0,8))

    if not ( Labels ):
      Labels = ['zero', 'onefdsf en erg lang nnog ',
                  'six', 'seven', 'eight']
    self.ED = []
    for item in Labels:
      edit = wx.TextCtrl(self, -1 )
      self.ED.append ( edit )
      sizer.Add ( edit )
      sizer.Add ( (0,5))
      text = wx.StaticText ( self, -1, '    ' + item )
      sizer2.Add ( text )
      sizer2.Add ( (0,13))

    # keep track of number of labels
    self.N = len(Labels)
    
    # to get the size right,
    # make the height of the panel equal to the RadioBox,
    # before letting the sizer do it's work
    self.SetSize ( ( self.GetSize()[0], self.N * 26 ) )

    sizer_total = wx.BoxSizer ( wx.HORIZONTAL )
    sizer_total.Add ( sizer )
    sizer_total.Add ( sizer2 )
    self.SetSizer(sizer_total)
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Translate_HTML_wxp ( source ) :
  #name_from = 'd:/data_to_test/aap_widget.html'
  #source = open (name_from, 'r').read ()
  """
  i = 0
  wxp = []
  while i >= 0 :
    i = source.find ( '<div><table', i+1 )
    if i >= 0 :
      wxp.append ( i )

  i = 0
  wxp_end = []
  while i >= 0 :
    i = source.find ( '</table>\n</div>', i+1 )
    if i >= 0 :
      wxp_end.append ( i )
  """
  
  wxp = []
  wxp_end = []
  i = 0
  ii = 0
  while ii >= 0 :
    prev_i  = i
    prev_ii = ii
    i  = source.find ( '<table',      prev_i  + 1 )
    ii = source.find ( '</table>', prev_ii + 1 )
    #print i,ii
    #print wxp
    #print wxp_end
    if i >= 0 :
      # if start between previous-start and previous-finish
      # or in other words, start is before previous finish,
      # it's nested table, so
      #   - replace the stored start
      #   - keep    the stored finish
      if ( len ( wxp ) > 0 ) and ( i <  wxp_end [-1] ) :
        wxp [-1] = i
      else :
        wxp.append ( i )
        wxp_end.append ( ii )



  #[909, 1575, 2219, 2828, 4298, 4620, 4942]
  #[1535, 2179, 2788, 4258, 4592, 4914, 5240]
  #print wxp
  #print wxp_end

  # remove all that are not wxp definitions
  # and store 'wxp:'
  wxp_wxp = []
  N = len ( wxp )
  for i in range ( N ) :
    ii = N-i-1
    w = source.find ( 'wxp:', wxp[ii], wxp_end[ii] )
    if w >= 0 :
      wxp_wxp.append ( w )
    else :
      del wxp[ii], wxp_end[ii]
  wxp_wxp.reverse()

  #[909, 1575, 2219, 2828, 4298, 4620, 4942]
  #[1535, 2179, 2788, 4258, 4592, 4914, 5240]
  #print wxp
  #print wxp_end
  #print wxp_wxp

  # get wxp
  # <p>wxp: RadioBox</p>
  N = len ( wxp )
  for i in range ( N ) :
    ii = N-i-1
    b = source.find ( '</p>', wxp_wxp[ii] , wxp_end [ii]  )
    wxp_widget = source [ wxp_wxp[ii]+5 : b ].strip()
    #print wxp_widget,wxp_wxp[ii] , wxp_end [ii]
    if wxp_widget in ['RadioBox', 'CheckBoxes' ] :
      # find all radiobox strings
      # <li value=1>tekst1</li>
      # <li>aaa</li>
      wxp_values = []
      x = b
      while x >= 0 :
        #x = source.find ( '<li value=', x+1, wxp_end[ii] )
        x = source.find ( '<li', x+1, wxp_end[ii] )

        if x >= 0 :
          x = source.find ( '>', x+1, wxp_end[ii] )
          y = source.find ( '</li>', x, wxp_end[ii] )
          #wxp_values.append ( source [ x+12 : y ].strip() )
          wxp_values.append ( source [ x+1 : y ].strip() )


      # now replace the Radiobox definition with a real wxp definition
      line = '<wxp module="wxp_widgets" class="'
      line += wxp_widget
      line += '" width=100%>\n'
      line += '<param name="Labels" value="['
      for item in wxp_values :
        line += "'" + item + "',"
      line = line [:-1]
      line += ']">\n</wxp>\n'
      #source = source.replace ( source [ wxp[ii] : wxp_end[ii]+16 ], line )

    elif wxp_widget in [ 'EditBoxes' ] :
      # find all editbox descriptions
      #<p>item 1</p>
      wxp_values = []
      x = b
      while x >= 0 :
        #x = source.find ( '<li value=', x+1, wxp_end[ii] )
        x = source.find ( '<p>', x+1, wxp_end[ii] )

        if x >= 0 :
          y = source.find ( '</p>', x, wxp_end[ii] )
          wxp_values.append ( source [ x+3 : y ].strip() )


      # now replace the Radiobox definition with a real wxp definition
      line = '<wxp module="wxp_widgets" class="'
      line += wxp_widget
      line += '" width=100%>\n'
      line += '<param name="Labels" value="['
      for item in wxp_values :
        line += "'" + item + "',"
      line = line [:-1]
      line += ']">\n</wxp>\n'
      #source = source.replace ( source [ wxp[ii] : wxp_end[ii]+16 ], line )

    elif wxp_widget == 'TextBox' :
      x = source.find ( 'height=', b+1, wxp_end[ii] )
      y = source.find ( 'valign=', x+1, wxp_end[ii] )
      h = source [ x+7 : y ].strip()
      line = '<wxp module="wxp_widgets" class="'
      line += wxp_widget
      line += '" width=100%'
      line += ' height='+ str(h) + '>\n</wxp>\n'
      #<wxp module="wxp_widgets" class="TextBox" width=100% height=200>
      #</wxp>
      #source = source.replace ( source [ wxp[ii] : wxp_end[ii]+16 ], line )

    elif wxp_widget in [ 'Prev', 'Next', 'PrevNext' ] :
      line = '<wxp module="wxp_widgets" class="'
      line += wxp_widget
      line += '">\n</wxp>\n'
      #<wxp module="wxp_widgets" class="Prev" >
      #</wxp>
      
    elif wxp_widget.find ( 'PW' ) == 0 :
      line = '<wxp module="wxp_widgets" class="'
      line += 'PW">\n'
      line += '<param name="Demo" value="'
      line += wxp_widget [ 3 : ]
      #line += '" Demo= "' + 'social'
      line += '">\n</wxp>\n'

    else : # in case of a  wrong definition
      line = '<wxp module="wxp_widgets" class="'
      line += wxp_widget
      line += '">\n</wxp>\n'

    source = source.replace ( source [ wxp[ii] : wxp_end[ii]+16 ], line )

  return source
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Read_CSS ( filename ) :
  CSS_data = open ( filename, 'r' ).readlines ()
  CSS = {}
  PAR = {}
  B = I = U = False
  N = False
  P = False
  for line in CSS_data :
    i = line.find ( 'span.rvts' )
    if i >= 0 :
      ii = line.find ( '/', i )
      N = line[i+9:ii].strip()
      Style = ''
    if N :
      i = line.find ( 'color:' )
      if i>=0 :
        i  = line.find ( '#' )
        ii = line.find ( ';', i )
        Style += ' COLOR=' + line [i:ii].strip()

      i = line.find ( 'font-size:' )
      if i>=0 :
        ii = line.find ( 'pt', i )
        Size = int ( line [ i+11 : ii ].strip() ) / 2
        Size = Size - 2
        if Size < 1 : Size = 1
        elif Size > 7 : Size = 7
        Style += ' size=' + str ( Size )

      i = line.find ( 'font-family:' )
      if i>=0 :
        line = line [ i+13 : ].replace ("'",'').strip()[:-1]
        Style += ' face=' + line

      if line.find ( 'bold' )      > 0 : B = True
      if line.find ( 'italic' )    > 0 : I = True
      if line.find ( 'underline' ) > 0 : U = True

      if line.find ( '}' ) >= 0 :
        CSS [N] = [ Style, B, I, U ]
        B = I = U = N = False

    i = line.find ( '.rvps' )
    if i >= 0 :
      ii = line.find ( '/', i )
      P = line[i+5:ii].strip()
      Paragraph = ''
      #print 'PARA',P,'PARAS'
    if P :
      #print 'P',line
      i = line.find ( 'text-align:' )
      if i >= 0 :
        ii = line.find ( ';', i )
        par = line [ i+12 : ii ].strip()
        if par == 'right' :
          Paragraph += ' DIV ALIGN=RIGHT'
      # <p class=rvps3>
      # <p DIV ALIGN=RIGHT
      if line.find ( '}' ) >= 0 :
        if Paragraph :
          PAR [P] = Paragraph
        P = False
  return CSS, PAR
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Translate_CSS ( name_from, name_to, CallBack_Html = None ) :
  from file_support import File_Exists
  if not ( File_Exists ( name_from ) ) :
    dest = open ( name_to, 'w+')
    dest.write ( 'ERROR in wxp_widgets.Translate_CSS : , file not found : ' + name_from +'\n')
    dest.close()
    return


  prim_path = name_from
  source = open (name_from, 'r').read ()
  source = Translate_HTML_wxp ( source ) .split('\n')
  dest = open ('CSS_translated2.html','w+')
  source2=''
  for line in source:
    source2 += line+'\n'
  dest.write(source2)
  dest.close()

  source = open ('CSS_translated2.html','r').readlines()
  #print source

  dest = open ( name_to, 'w+')
  bg_color = ''
  end_tags = ''
  for line in source :
    #print line

    # *****************************************************
    # Find the background color
    # *****************************************************
    i = line.find ( 'background-color:' )
    if i >= 0 :
      ii = line.find ( ';', i+17 )
      bg_color = line[i+17:ii].strip()
      #print 'BGCOLOR',bg_color,'PP'

    # *****************************************************
    # Read the CSS file
    # *****************************************************
    if line.find ( '"stylesheet"' ) >= 0 :
      #print '**** CSS',line
      i = line.find ( 'href=' )
      if i >= 0 :
        ii = line.find ( '"', i+6 )
        #print '**** CSS-file', line [i+6:ii]
        path, filename = path_split ( name_from )
        CSS_filename = os.path.join ( path, line [i+6 : ii] )
        #print CSS_filename
        CSS, PAR = Read_CSS ( CSS_filename )
        #print 'CSS',CSS
        #print 'PARAGRAPHS',PAR
    else :
      line = Make_Links_Absolute ( line, 'href=', prim_path )
      line = Make_Links_Absolute ( line, 'src=', prim_path )


    # *****************************************************
    # find start of the BODY
    # *****************************************************
    if line.find ( '<body>' ) >= 0 :
      line = '<body'
      if bg_color:
        line += ' bgcolor='+ bg_color
      line += ' TEXT=#000000 LINK="#0000FF" VLINK="#FF0000" ALINK="#000088" >'

    # *****************************************************
    # <SPAN...  Text Attribute
    # *****************************************************
    i = line.find ( '<span class=rvts' )
    if i >= 0 :
      ii = line.find ( '>', i+16 )
      end_tags = ''
      try:
        N = line [ i+16 :ii ]
        #print '**** span',N
        Style = CSS [ N ]
        begin_tags = Style [0]
        if begin_tags :
          begin_tags = '<FONT' + begin_tags + '>'
          end_tags = '</FONT>'
        else :
          end_tags = ''
        if Style[1] :
          begin_tags +='<B>'
          end_tags = '</B>' + end_tags
        if Style[2] :
          begin_tags +='<I>'
          end_tags = '</I>' + end_tags
        if Style[2] :
          begin_tags +='<U>'
          end_tags = '</U>' + end_tags

      except :
        #print 'ERRROR'
        begin_tags = ''
        end_tags = ''

      line = line.replace ( line[i:ii+1], begin_tags )
      #print line

    if line.find ( '</span>' ) >= 0 :
      line = line.replace ( '</span>', end_tags )
      end_tags = ''
      #print '**** end-span',line.strip('\r\n')

    # *****************************************************
    # <SPAN.RVPS ...  Paragraph Attribute
    # *****************************************************
    i = line.find ( '<p class=rvps' )
    if i >= 0 :
      ii = line.find ( '>', i+13 )
      try:
        P = line [ i+13 :ii ]
        Paragraph = PAR [ P ]
        #<p class=rvps3>
        line = line.replace ( line[i+2:ii], Paragraph)
        end_paragraph = ''
      except :
        end_paragraph = ''

    if line.find ( '<p><br></p>' ) < 0 :
      dest.write ( line +'\n')
      #print line.strip ( '\r\n' )
  dest.close()
  
  # remove all standard paragraphs and replace them by an old-style <br>
  dest = open ( name_to, 'r')
  text = dest.read ()
  dest.close ()

  # replace "<p> .. </p>" with ".. <br>"
  new_text = ''
  start = 0
  prev  = 0
  while start >= 0 :
    start  = text.find ( '<p>', start )
    finish = text.find ( '</p>', start )
    if 0 < start < finish :
      new_text += text [ prev : start ] + \
                  text [ start + 3 : finish ] + '<br>'
      start = finish +  4
      prev  = start
    else :
      new_text += text [ prev : ]

  # replace "<p .. </p>" with "<p .. </p><p>
  new_text = new_text.replace ( '</p>', '</p><p>' )

  dest = open ( name_to, 'w')
  text = dest.write ( new_text )
  dest.close ()

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
def Create_CSS_with_Answers ( fields, file_from, file_to ) :
      # read the orginal source file
      source_file = open ( file_from, 'r' )
      source = source_file.read ()
      source_file.close ()

      # for all the fill-in items
      for field in fields : #self.html.GetChildren () :

        # find next wxp in source
        wxp = source.find ( 'wxp:')

        # find the topmost row
        begin =     source.rfind ( '<tr',   0,  wxp )
        end   = 5 + source.find  ( '</tr>', wxp     )

        # depending on type of field handle it
        # **********************************************
        # TEXTBOX
        # **********************************************
        if isinstance ( field, TextBox ):
          # text insertion point
          b = 3 + source.find ( '<p>',  end )
          e = source.find ( '</p>', end)

          # get the content of the editbox
          #if not self.rtc.GetFilename():
          #    self.OnFileSaveAs(evt)
          #    return
          temp_filnam = '_Temp_wxWidget2.html'
          field.Text.SaveFile ( temp_filnam )

          # read the file back and remove top and bottom
          temp_file = open ( temp_filnam, 'r' )
          line = temp_file.read()
          temp_file.close ()
          line = line.replace ( '<html><head></head><body>', '' )
          line = line.replace ( '</body></html>', '' )
          #remove:  <font face="MS Shell Dlg 2" size="1" color="#000000" >
          x = line.find ( '<font' )
          y = 1 + line.find ( '>', x)
          line = line [ : x ] + line [ y : ]

          # correct empty lines, place a "<br></p>" before every "<p ", except the first
          y = 2 + line.find ( '<p ', x )
          y = line.find ( '<p ', y )
          while y >= 0 :
            line = line [ : y ] + '<br></p>' + line [ y : ]
            y = y + 10
            # find next
            y = line.find ( '<p ', y )


          # replace the text
          #line = 'new text'
          source = source [ : b ] + line + source [ e : ]

          # remove the top row (also containing the wxp-tag)
          source = source [ : begin ] + source [ end : ]


        # **********************************************
        # EDIT BOXES
        # **********************************************
        elif isinstance ( field, EditBoxes ):
          cur = end
          for N in range ( field.N ) :
            # text insertion point
            b = source.find ( '<td',   cur )
            b = 1 + source.find ( '>', b )
            e = source.find ( '</td>', cur)

            # replace the text
            line = field.ED[N].GetValue()
            if line :
              line = '<p>'+ line + '</p>'
            else :
              line = '<br>'
            source = source [ : b ] + line + source [ e : ]

            # ignore the next '<td' , '<td>'
            cur = b + 4
            b = source.find ( '<td',   cur )
            e = source.find ( '</td>', b )
            cur = e + 5

          # remove the top row (also containing the wxp-tag)
          source = source [ : begin ] + source [ end : ]

        # **********************************************
        # CHECK BOXES
        # **********************************************
        elif isinstance ( field, CheckBoxes ):
          cur = end
          for N in range ( field.N ) :
            # text insertion point
            b = 4 + source.find ( '<li>',   cur )

            # replace the text
            if  field.CB[N].GetValue() : line = '+ '
            else :                    line = '&nbsp;&nbsp;&nbsp;'
            source = source [ : b ] + line + source [ b : ]
            cur = source.find ( '<li>', b)

          # remove the top row (also containing the wxp-tag)
          source = source [ : begin ] + source [ end : ]

        # **********************************************
        # RADIO BOX
        # **********************************************
        elif isinstance ( field, RadioBox ):
          cur = end
          for N in range ( field.rb.GetCount () - 1) :
            # text insertion point
            b = 3 + source.find ( '<li', cur )
            b = 1 + source.find ( '>',   b )

            # replace the text
            if N == field.rb.GetSelection() : line = '+ '
            else :   line = '-&nbsp;&nbsp;&nbsp;'  #'   '
            source = source [ : b ] + line + source [ b : ]
            cur = source.find ( '<li', b)

          # remove the last list element
          b = source.find ( '<li', cur )
          e = 5 + source.find ( '</li>', cur )
          source = source [ : b ] + source [ e : ]

          # remove the top row (also containing the wxp-tag)
          source = source [ : begin ] + source [ end : ]

        # **********************************************
        # BUTTONS
        # **********************************************
        elif isinstance ( field, PrevNext ) | \
             isinstance ( field, Prev     ) | \
             isinstance ( field, Next     ) :

          # remove the whole button = table
          b =     source.rfind ( '<div>',   0,  wxp )
          e = 6 + source.find  ( '</div>', wxp     )
          source = source [ : b ] + source [ e : ]

        else :
          # remove the top row (also containing the wxp-tag)
          source = source [ : begin ] + source [ end : ]


      filename = '_Temp_dest_wxWidget2.html'
      dest_file = open ( filename, 'w' )
      dest_file.write ( source )
      dest_file.close ()

      Translate_CSS ( filename, file_to )
# ***********************************************************************




# ***********************************************************************
# demo program
# ***********************************************************************
if __name__ == '__main__':
  #name_from = 'd:/data_to_test/aap_widget.html'
  name_from = '../PyLab_Works/html/pw_demos.html'
  source = open (name_from, 'r').read ()
  source = Translate_HTML_wxp ( source )
  print (source)
# ***********************************************************************
pd_Module ( __file__ )

