# ***********************************************************************
# blabla
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007 Stef Mientki
# mailto:S.Mientki@ru.nl
#
# <Version: 2.0    ,-2007, Stef Mientki
#    - available devices added to popup-menu
#
# <Version: 1.0    ,14-07-2007, Stef Mientki
#    - orginal release
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
import time
import wx
import PyLab_Works_Globals as PG

import OGLlike as ogl

from dialog_support import *
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class Shape_Event_Handler(ogl.ShapeEvtHandler):
  # we need to save the shape container
  def __init__(self, container, device):
    ogl.ShapeEvtHandler.__init__(self)
    self.container = container
    self.device = device

  def OnLeftClick(self, x, y, keys=0, attachment=0):
    shape = self.GetShape()
    canvas = shape.GetCanvas()
    dc = wx.ClientDC(canvas)
    canvas.PrepareDC(dc)

    if shape.Selected():
      shape.Select(False, dc)
      canvas.Refresh(False)
    else:
      #redraw = False
      shapeList = canvas.GetDiagram().GetShapeList()
      toUnselect = []

      for s in shapeList:
        if s.Selected():
          # If we unselect it now then some of the objects in
          # shapeList will become invalid (the control points are
          # shapes too!) and bad things will happen...
          toUnselect.append(s)

      shape.Select(True, dc)
      
      if toUnselect:
        for s in toUnselect:
          s.Select(False, dc)

        canvas.Refresh(False)

    #self.UpdateStatusBar(shape)


  # for each shape, we just call the containers popup
  def OnRightClick(self, x, y, keys, *dontcare): #)*dontcare):
    self.container.Popup ( x, y, self.device )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class tPyLabWorks_ShapeCanvas ( ogl.ShapeCanvas ) :

  clipboard=[]

  def __init__(self, parent, Main_Form, pos=(0,0), size=(500,500)):
    #wx.ScrolledWindow.__init__(self,parent,id,pos=(0,0), size=(500,500),style,name)
    ogl.ShapeCanvas.__init__ ( self, parent, pos=(0,0), size=(500,500), Design = True )

    self.parent = parent
    self.Main_Form = Main_Form
    self.SetBackgroundColour ( PG.General_BackGround_Color )

    self.diagram = ogl.Diagram ()
    ## ?????
    self.SetDiagram ( self.diagram )

    self.Devices = []
    maxWidth  = 1000
    maxHeight = 1000
    self.SetScrollbars(20, 20, maxWidth/20, maxHeight/20)
    self.kill_focus_allowed = True
    self.Show(True)


    # find all available devices,
    import PyLab_Works_search_bricks
    self.files = PyLab_Works_search_bricks.Get_PyLabWorks_Bricks_All()

    self.Bind ( wx.EVT_KEY_DOWN,   self.OnKeyDown )
    self.Bind ( wx.EVT_KILL_FOCUS, self.OnKillFocus )

    self.t1 = wx.Timer ( self )
    # the third parameter is essential to allow other timers
    self.Bind ( wx.EVT_TIMER, self.OnTimer, self.t1)
    #self.t1.Start(4000)
  def OnTimer ( self, event ) :
    pass
    
  def Save_Flow_Design ( self, ini ) :
    if ini:
      # Save all device settings
      for Device in PG.Main_Form.Shape_Container.Devices:
        Device.Save_Properties_from_Device_to_File ()

      # Save connections
      section_name = 'Connections'
      #print 'LOOSE CONNECTIONS',1
      #ini.Remove_Section ( section_name )
      ini.Section = section_name
      i = 0
      for shape in self.diagram.shapes :
        #print 'LOOSE CONNECTIONS',2
        if isinstance ( shape, ogl.Connection_Line ) and \
           shape.input and \
           shape.output :
         #print shape.input[0].Parent.Name, shape.input[1]
         #print shape.output[0].Parent.Name, shape.output[1]
         # STORE input, output
         line = shape.output[0].Parent.Name + '/' + str ( shape.output[1] )
         line = line + ',' + shape.input[0].Parent.Name + '/' + str( shape.input[1] )
         ini.Write ( str(i), line )
         i += 1
      #print 'LOOSE CONNECTIONS',3

  def Load_Flow_Design ( self, ini ) :
    # now find all device sections in the hardware file
    # and if not yet in the shape container, add them
    # first import all device libraries
    for item in self.files:
      filnam = item[1], item[0]
      #line = 'from bricks.' + item[1] + ' import t_' +item[0]
      line = 'import '+ item[1]
      #print 'IMPORT: ', line
      exec(line)

    # we want to record the largest ID
    # (for creating unique ID's for newly added Bricks)
    PG.Active_Project_max_ID = 0
    # now check all devices in the hardware configuration file
    for section in ini.Sections ():
      if section.lower().find('device ') == 0:
        Device_Name = section[7:]
        ID = int ( Device_Name [2:] )
        if ID > PG.Active_Project_max_ID :
          PG.Active_Project_max_ID = ID
        for device in self.Devices:
          if Device_Name == device.Name:
            break
        else:
          ini.Section = section
          line = ini.Read ( 'ttype', '' )
          line = line + ' ( self, "' + Device_Name + '" )'
          print ('CREATE:',line)
          exec ( line )

    # Load connections
    ini.Section = 'Connections'
    for nv in ini.Get_Section () :
      line = nv[1].split(',')

      shape_name, Index_In = line[0].split('/')
      Shape_In = self.Find_Shape_By_Name ( shape_name )
      Index_In = int ( Index_In )
      #print line,shape_name,index,shape_In
      shape_name, Index_Out = line[1].split('/')
      Shape_Out = self.Find_Shape_By_Name ( shape_name )
      Index_Out = int ( Index_Out )
      #print line,shape_name,index,shape_Out

      # If a brick has changed, inputs or outputs might have disappeared
      if Shape_In and \
         (( Index_In < 1 ) or ( Index_In >= Shape_In.Parent.N_Inputs ) ) :
        Shape_In = None
      if Shape_Out and \
         (( Index_Out < 1 ) or ( Index_Out >= Shape_Out.Parent.N_Outputs ) ) :
        Shape_Out = None


      if Shape_In and Shape_Out :
        #v3print ( Shape_In.Parent.Name, Shape_In.Parent.Caption)
        #v3print ( Shape_Out.Parent.Name, Shape_Out.Parent.Caption)
        #v3print ( 'OOOOO', Index_In,Shape_In.Parent.N_Inputs,Index_Out,Shape_Out.Parent.N_Outputs )
        #v3print ( Shape_In.Type_Inputs, Shape_Out.Type_Outputs)
        # Create connection line
        CL = ogl.Connection_Line ( self )
        CL.pen[0] = ogl.TIO_Brush [ Shape_In.Type_Inputs [ Index_In ] ].GetColour()
        self.diagram.shapes.insert ( 0, CL)

        CL.setOutput ( Shape_In, Index_In )
        CL._x[0], CL._y[0] = Shape_In.GetPort ( 'input', Index_In )

        CL.setInput ( Shape_Out, Index_Out )
        CL._x[1], CL._y[1] = Shape_Out.GetPort ( 'output', Index_Out )

    self.Refresh ()

  # *************************************************************
  # Called from the tree, to highlight the selected object
  # *************************************************************
  def Select_by_Name ( self, name ):
    for shape in self.diagram.shapes :
      if 'Parent' in dir(shape):
        if shape.Parent.Name == name :
          break
    else:
      return
        
    self.Deselect_All()
    self.select ( shape )
    self.Refresh ()


  def OnKillFocus ( self, event ) :
    if self.kill_focus_allowed :
      self.Deselect_All ()
      self.Refresh ()

  def OnKeyDown ( self, event ) :
    key = event.GetKeyCode()
    #print 'KEY ALLLLLLLL',key
    if key ==127:  # DELETE
      # deleting only allowed in Edit mode
      if PG.State == PG.SS_Edit :
        self.kill_focus_allowed = False
        print ('DDDELLTETE3')
        if len ( self.selectedShapes ) > 0 :
          self.My_Delete_Shapes ( self.selectedShapes )
        else :
          wx.Bell()
          self.kill_focus_allowed = True

      """
      elif key ==67 and event.ControlDown():  # COPY
        del self.clipboard[:]
        for i in self.select():
          self.clipboard.append(i)
      elif key ==86 and event.ControlDown():  # PASTE
        for i in self.clipboard:
          self.AddShape(i.Copy())
      """
      """ DOESN'T WORK, TAB-KEY IS NOT RECEIVED
      elif key == 9: # TAB
        if len(self.diagram.shapes)==0:
          return
        shape = self.select()
        if shape:
          ind = self.diagram.shapes.index(shape[0])
          self.Deselect_All()
          try:
            self.select(self.diagram.shapes[ind+1])
          except:
            self.select(self.diagram.shapes[0])
        else:
          self.select(self.diagram.shapes[0])
      """
    elif key == 322 : # INS
      self.Print_All ()

  def Clear (self):
    # Remove properties form, if available
    for device in self.Devices:
      try:
        device.Properties_Form.Close ()
        device.Properties_Form.Destroy ()
      except:
        pass
    self.diagram.shapes = []
    self.Devices = []
    self.Refresh()


  def MyAddShape(self, Device ): #, x, y, pen, brush, text):
    shape = Device.shape
    self.diagram.AddShape(shape)

    # for each shape, we just call the containers popup
    #def OnRightClick(self, x, y, keys, *dontcare): #)*dontcare):
    #  self.container.Popup ( x, y, self.device )


    self.Devices.append ( Device )

    return shape


  # ************************************
  # Delete device(s)
  # asks for confirmation of deleting the component
  # The Shapes consists of real devices and connections
  # ************************************
  def My_Delete_Shapes ( self, shapes ) :
    real_shapes = []
    names = ''
    for shape in shapes :
      if 'Parent' in dir(shape):
        real_shapes.append (shape)
        names += shape.Parent.Name + ','

    if len (  real_shapes ) > 0 :
      #from dialog_support import *
      line = 'Delete ' + names + '\nAre you sure ?'
      if not ( AskYesNo (line) ) :
        return

    for shape in shapes :
      self.diagram.DeleteShape ( shape )

      #if 'Parent' in dir(shape):
      if shape in real_shapes :
        Brick = shape.Parent

        # Remove from Project Tree
        self.Main_Form.Tree.Remove_Device_From_ProjectTree ( Brick )

        # Remove from GUI, if there is GUI
        if PG.Final_App_Form :
          PG.Final_App_Form.Delete_Pane ( Brick.Name )

        # remove properties form, if available
        try:
          device.Properties_Form.Close ()
          device.Properties_Form.Destroy ()
        except:
          pass

        # Remove from Project File
        Brick.Remove_Device_From_ProjectFile ()

        self.Devices.remove ( Brick )



    # now also remove all loose connections
    # collect all real Bricks
    real_shapes = []
    for shape in self.diagram.shapes :
      if not ( isinstance ( shape, ogl.Connection_Line ) ):
        real_shapes.append ( shape )
        
    # now test all connnection lines
    N = len ( self.diagram.shapes )
    for i in range ( N ) :
      shape = self.diagram.shapes [ N - i - 1 ]
      if isinstance ( shape, ogl.Connection_Line ) :
        #print shape
        if not ( shape.input  ) or \
           not ( shape.output ) or \
           not ( shape.input[0]  in real_shapes ) or \
           not ( shape.output[0] in real_shapes ) :
          #print 'REMOVE SHAPE',shape
          self.diagram.DeleteShape ( shape )

    self.kill_focus_allowed = True
    self.Deselect_All()
    self.Refresh ()
# ***********************************************************************


