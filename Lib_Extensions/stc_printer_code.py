# ***********************************************************************
# ***********************************************************************
class STCPrintout(wx.Printout):
  def __init__( self, stc, PrintData=None,
                MarginTopLeft = (10,10),
                MarginBottomRight = (10,10),
                filename = ''):
    wx.Printout.__init__(self)
    self.stc = stc
    self.filename = filename
    self.PrintData = PrintData
    self.MarginTopLeft = MarginTopLeft
    self.MarginBottomRight = MarginBottomRight

  def HasPage ( self, page ) :
    return ( page <= self.NumPages )

  def GetPageInfo ( self ) :
    return ( 1, self.NumPages, 1, 32000 )

  def Calculate_Scale ( self, dc ) :
    PPI_Printer_X, PPI_Printer_Y = self.GetPPIPrinter ()
    PPI_Screen_X,  PPI_Screen_Y  = self.GetPPIScreen ()
    PS_Scale = 1.0 * PPI_Printer_Y / PPI_Screen_Y

    pw, ph = self.GetPageSizePixels ()
    dw, dh = dc.GetSize ()
    self.Scale = PS_Scale * dh / ph
    dc.SetUserScale ( self.Scale, self.Scale )
    self.UnitsMM = 1.0 * PPI_Printer_Y /  ( PS_Scale * 25.4 )

    self.x1 = self.MarginTopLeft[0] * self.UnitsMM
    self.y1 = self.MarginTopLeft[1] * self.UnitsMM
    self.x2 = dc.DeviceToLogicalXRel ( dw ) - \
              self.MarginBottomRight[0] * self.UnitsMM
    self.y2 = dc.DeviceToLogicalYRel ( dh ) - \
              self.MarginBottomRight[1] * self.UnitsMM
    self.PageHeight = self.y2 - self.y1
    #print 'XY', int(self.x1), int(self.y1), int(self.x2), int(self.y2)
    #print 'Scales', self.Scale, self.UnitsMM, PS_Scale
    #print 'ps',pw,ph,dw,dh

    # font for page titles
    dc.SetFont( wx.FFont( 10, wx.ROMAN ) )
    self.LineHeight = dc.GetCharHeight()
    self.LinesPerPage = int ( self.PageHeight / self.LineHeight )
    #print ' PREPARE' , self.LineHeight, int(self.PageHeight) ,self.LinesPerPage

    self.NumPages, m = divmod ( self.stc.GetLineCount(), self.LinesPerPage )
    if m: self.NumPages += 1

    # to get all the lines on the preview, we need to set magnification
    # we'll be able to see all lines,
    # but depending on the scaling, the view is good or reasonable
    self.stc.SetPrintMagnification (-2)

  def OnPreparePrinting ( self ) :
    dc = self.GetDC()
    self.Calculate_Scale (dc)

  def OnPrintPage(self, page):
    import datetime
    dc = self.GetDC()
    self.Calculate_Scale (dc)

    # font might be destroyed by STC rendering !!
    dc.SetFont( wx.FFont( 10, wx.ROMAN ) )
    dc.SetTextForeground ("black")

    # print filename on top
    if self.filename:
      tlw, tlh = dc.GetTextExtent(self.filename)
      dc.DrawText ( self.filename, self.x1, self.y1 - tlh -10 )

    # print date and pagenumber at the bottom
    t = datetime.date.today()
    pageLabel = t.strftime("%d-%m-%Y")
    dc.DrawText ( pageLabel, self.x1, self.y2 )

    pageLabel = 'Page: ' + str(page) + '/' + str(self.NumPages)
    plw, plh = dc.GetTextExtent(pageLabel)
    dc.DrawText ( pageLabel, self.x2 - plw, self.y2 )

    # render stc into dc
    stcStartPos = self.stc.PositionFromLine   ( (page-1) * self.LinesPerPage     )
    stcEndPos   = self.stc.GetLineEndPosition (  page    * self.LinesPerPage - 1 )
    maxWidth = 32000

    self.stc.SetPrintColourMode ( stc.STC_PRINT_COLOURONWHITEDEFAULTBG )
    # first rectangle is rendering rectangle, second is the page rectangle
    # so why not use for both the rendering rectangle
    rect = wx.Rect ( self.x1, self.y1, self.x2, self.y2 )
    ep = self.stc.FormatRange(1, stcStartPos, stcEndPos, dc, dc, rect, rect )

    #print 'R1',int(self.x1),int(self.y1),maxWidth,int(self.y2-self.y1),self.stc.GetPrintMagnification()

    """
    # FOR TEST, draw outline
    dc.SetPen ( wx.Pen ( "black", 0 ) )
    dc.SetBrush ( wx.TRANSPARENT_BRUSH )
    r = wx.RectPP ( ( self.x1, self.y1 ), ( self.x2, self.y2 ) )
    dc.DrawRectangleRect ( r )
    #dc.SetClippingRect ( r )
    """

    """
    # warn when fewer characters than expected are rendered by the stc when
    # printing
    if not self.IsPreview():
      if ep < stcEndPos:
        JG.em ( 'Printing page %s: not enough chars rendered, diff: %s')%(page, stcEndPos-ep)
    return True
    """
# ***********************************************************************



  def OnMenu_Print ( self, event ) :
    pdd = wx.PrintDialogData ()
    pdd.SetPrintData ( self._printData )
    printer = wx.Printer ( pdd )
    printout = STCPrintout ( self.Code_Editor,
                             self._printData,
                             self._print_margins_TopLeft,
                             self._print_margins_BottomRight,
    		                     JG.Active_JAL_File )

    if not printer.Print ( self, printout ) :
      JG.em ( 'Print' )
    else:
      self.printData = wx.PrintData ( printer.GetPrintDialogData().GetPrintData() )
    printout.Destroy()

  def OnMenu_Print_Preview ( self, event ) :
    filename = JG.Active_JAL_File
    po1 = STCPrintout ( self.Code_Editor,
                        self._printData,
                        self._print_margins_TopLeft,
                        self._print_margins_BottomRight,
                        filename )
    po2 = STCPrintout ( self.Code_Editor,
                        self._printData,
                        self._print_margins_TopLeft,
                        self._print_margins_BottomRight,
                        filename )
    printPreview = wx.PrintPreview ( po1, po2, self._printData )
    printPreview.SetZoom ( self._print_zoom)
    if not printPreview.Ok():
      JG.em ( 'Print Preview' )
      return

    frame = wx.PreviewFrame ( printPreview, self, "Print Preview   " + filename )
    frame.Initialize ()
    frame.Maximize ()
    frame.Show ( True )
    print 'pipo'

  def OnMenu_Page_Setup ( self, event ) :
    # there seems to be 3 almost identical datasets:
    #    PrintData, PrintDialogData, PageSetupDialogData
    # PageSetupDialogData, seems to have the best overall set
    # but for example no orientation :-(

    # Create dataset, and copy the relevant data
    #   from printData and margins into this dataset
    dlgData = wx.PageSetupDialogData ( self._printData )
    dlgData.SetDefaultMinMargins ( True )
    dlgData.SetMarginTopLeft ( self._print_margins_TopLeft )
    dlgData.SetMarginBottomRight ( self._print_margins_BottomRight )

    # start page setup dialog
    printDlg = wx.PageSetupDialog ( self, dlgData )
    if printDlg.ShowModal () == wx.ID_OK :
      # if ok, copy data back into globals
      dlgData = printDlg.GetPageSetupData ()
      self._printData = wx.PrintData ( dlgData.GetPrintData () )
      self._print_margins_TopLeft = dlgData.GetMarginTopLeft ()
      self._print_margins_BottomRight = dlgData.GetMarginBottomRight ()

      # store data in inifile

    printDlg.Destroy()

