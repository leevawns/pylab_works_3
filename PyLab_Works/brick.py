from General_Globals import *
# ***********************************************************************
# BaseClass
#
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007 Stef Mientki
# mailto:S.Mientki@ru.nl
#
# <Version: 1.0    ,, Stef Mientki
#    - orginal release
# ***********************************************************************


# ***********************************************************************
import wx
import wx.grid as gridlib

import PyLab_Works_Globals as PG
from PyLab_Works_Globals import _
from gui_support         import *
from utility_support     import TIO_Dict, super_dict, super_object

import OGLlike as ogl
import time
import copy
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
class _BP_Form ( My_Frame_Class ):
  def __init__ ( self, ini = None ) :
    My_Frame_Class.__init__ ( self, None, 'Simple GUI Demo', ini )
    print ('HYTREW')
    GUI = """
    SplitVer           ,SplitterVer
      SplitHor         ,MultiSplitterHor
        P1             ,PanelVer ,01
          T1           ,wx.StaticText ,label = 'Var'
          self.SplitC1   ,MultiSplitterVer
            C1R1         ,wx.Panel
             B11         ,wx.Button,  label = "Go"
            C1R2         ,wx.Panel
             B12         ,wx.Button,  label = "Go"
            C1R3         ,wx.Panel
             B13         ,wx.Button,  label = "Go"
        P2             ,PanelVer ,01
          T2           ,wx.StaticText ,label = 'Before'
          self.SplitC2 ,MultiSplitterVer
            self.L21   ,wx.TextCtrl, style = wx.TE_MULTILINE | wx.TE_RICH2
            self.L22   ,wx.TextCtrl, style = wx.TE_MULTILINE | wx.TE_RICH2
            L23        ,wx.TextCtrl, style = wx.TE_MULTILINE | wx.TE_RICH2
        P3             ,PanelVer ,01
          T3           ,wx.StaticText ,label = 'After'
          self.SplitC3 ,MultiSplitterVer
            self.L31   ,wx.TextCtrl, style = wx.TE_MULTILINE | wx.TE_RICH2
            self.L32   ,wx.TextCtrl, style = wx.TE_MULTILINE | wx.TE_RICH2
            L33        ,wx.TextCtrl, style = wx.TE_MULTILINE | wx.TE_RICH2
      BP               ,PanelVer ,01
        P6             ,PanelHor ,01
          T6           ,wx.StaticText ,label = 'BP Condition'
          Cond           ,wx.TextCtrl
        shell          ,wx.TextCtrl, style = wx.TE_MULTILINE
    """
    self.wxGUI = Create_wxGUI ( GUI )
    #print self.wxGUI.code


    #self.SplitC1.Bind ( wx.EVT_SPLITTER_SASH_POS_CHANGED,  self.OnChanged  )
    self.SplitC1.Bind ( wx.EVT_SPLITTER_SASH_POS_CHANGING, self._Split_Change1 )
    self.SplitC2.Bind ( wx.EVT_SPLITTER_SASH_POS_CHANGING, self._Split_Change2 )
    self.SplitC3.Bind ( wx.EVT_SPLITTER_SASH_POS_CHANGING, self._Split_Change3 )

    self.L21.Bind ( wx.EVT_SCROLLWIN, self.OnScroll )
  def OnScroll(self, event):
    print ('PIOPP;')
    """
    clone = event.Clone ()
    clone.SetId ( wxID_FRAME1STYLEDTEXTCTRL2 )
    clone.SetEventObject ( self.styledTextCtrl2 )
    self.GetEventHandler().ProcessEvent(clone)
    """
    event.Skip()


  def _Split_Change1 ( self, event ) :
    i   = event.GetSashIdx()
    pos = event.GetSashPosition()
    self.SplitC2.SetSashPosition ( i, pos )
    self.SplitC3.SetSashPosition ( i, pos )

  def _Split_Change2 ( self, event ) :
    i   = event.GetSashIdx()
    pos = event.GetSashPosition()
    self.SplitC1.SetSashPosition ( i, pos )
    self.SplitC3.SetSashPosition ( i, pos )

  def _Split_Change3 ( self, event ) :
    i   = event.GetSashIdx()
    pos = event.GetSashPosition()
    self.SplitC1.SetSashPosition ( i, pos )
    self.SplitC2.SetSashPosition ( i, pos )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class tIO_Pin ( object ) :
  def __init__ ( self, Parent_List ) :
    self.Parent_List = Parent_List
    self.Receivers   = {}
    self.Value       = None

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class tIOP_List ( list ) :
  """
  This class is derived from the standard list.
  It monitors write action to elements of the list.
  """
  #def __init__ ( self, Brick, Modified, Name = 'IO', leng = 0, Value = Null ):
  def __init__ ( self, Brick, Modified, Name = 'IO', leng = 0, Value = None ):
    self.Brick     = Brick
    self.Modified  = Modified
    self.Name      = Name
    #self.IO_Par    = leng * [ Null  ]
    self.IO_Par    = leng * [ None  ]
    self.Is_Dict   = leng * [ False ]

    # Create te List itself
    # Create the Receiver lists
    # THIS:  self.Receivers = leng * [{}]
    # will result in identical directories !!
    list.__init__ ( self )
    self.Receivers = []
    for i in range ( leng ) :
      list.append ( self, Value )
      self.Receivers.append ( {} )

  # *********************************************
  # *********************************************
  def Set_Dict ( self, indx ) :
    """
    Makes this element an TIO_INTERACTION
    - set Is_Dict
    - if it's the output, add itself to the receiver list
    """
    list.__setitem__ ( self, indx, TIO_Dict( self, indx ) )
    self.Is_Dict [ indx ] = True
    self.Modified [ indx ] = []
    if self.Name.lower() == 'out' :
      self.Receivers [ indx ] [ self.Brick ] = \
        ( self, self.Modified, indx )

  # *********************************************
  # *********************************************
  #def append ( self, Value = Null ) :
  def append ( self, Value = None ) :
    self.Modified.append ( False )
    self.Receivers.append ( {} )
    #self.IO_Par.append ( Null )
    self.IO_Par.append ( None )
    self.Is_Dict.append ( False )
    list.append ( self, Value )

  # *********************************************
  # *********************************************
  def Clear_Modified ( self ) :
    #print 'MOMOMOMO',self.Modified
    for i, item in enumerate ( self.Modified ) :
      if self.Is_Dict [i] :
        self.Modified [i] = []
      else :
        self.Modified [i] = False

  # *********************************************
  # *********************************************
  def __setitem__ ( self, indx, value ) :
    ##print ' TTTTTT',self.Brick.Caption, self.Name, len(self), indx #, value, self.Modified
    list.__setitem__ ( self, indx, value )
    self._Set_Modified ( indx, value )

  # *********************************************
  # *********************************************
  def Set_Modified ( self, indx ) :
    """ Must be called if a complex variable is changed, like NumPy array """
    self._Set_Modified ( indx, self [ indx ] )

  # *********************************************
  # *********************************************
  def _Set_Modified ( self, indx, value, key = None ) :
    # MOET DIT ????????????????????
    if self.Is_Dict [indx] :
      if not ( key in self.Modified [ indx ] ) :
        self.Modified [ indx ].append ( key )
    else :
      self.Modified [ indx ] = True
    self.Modified [ 0    ] = True
    #print ' SSSSSS',self.Brick.Caption, self.Modified
    """
    Sets the modify flag of the receivers
    - for normal IOs TRUE
    - for TIO_INTERACTION, append the key
    """
    for Key_Brick in self.Receivers [indx] :
      Receiver = self.Receivers [indx] [ Key_Brick ]
      if self.Is_Dict [indx] :
        if not ( key in Receiver [1] [ Receiver[2] ] ) :
          Receiver [1] [ Receiver[2] ].append ( key )
      else :
        #Receiver [1] [indx] = True
        #Receiver [0] [indx] = value
        Receiver [1] [ Receiver[2] ] = True
        Receiver [0] [ Receiver[2] ] = value
      Receiver[1] [0]    = True
    if PG.Debug_Table._On :
      if self.Name != 'In' :
        if key :  # if launched by a dictionair
          PG.Debug_Table.Write ( self.Brick.Nr,
            '*-*' + self.Name + '-' + str(indx) + \
            ' { ' + str(key) + ' = ' + str(value) )
        else :
          PG.Debug_Table.Write ( self.Brick.Nr,
            '*-*' + self.Name + '-' + str(indx) + ' = ' + str(value) )
      else :
        PG.Debug_Table.Write ( self.Brick.Nr,
          '*-*' + self.Name + '-' + str(indx) + ' = ' )

  def Transmit_Changes ( self ) :
    if self.Modified [0] :
      for i, changed in enumerate ( self.Modified [ 1 : ] ) :
        if changed :
          for Receiver in self.Receivers [i+1] :
            if Receiver != self.Brick :
              Rec_Pars = self.Receivers [i+1] [ Receiver ]
              print ('   transmit from:', self.Brick.Caption, '/', i+1, '  Value:', self[i+1])
              print ('              to:', Receiver.Caption, '/', Rec_Pars)
              if PG.Debug_Table._On :
                PG.Debug_Table.Write ( self.Brick.Nr,
                  '*-*' + self.Name + '-' + str(i+1) +\
                  '  Send To = ' +\
                  Receiver.Caption + str (Rec_Pars) )

              # DIFFICULT TO fill from the connections
              # SO WE HAVE TO DO THIS ONE TIME
              #if len ( Rec_Pars ) > 2 :
              #  Rec_Pars [2] ( self [i+1] )
              #else :
              Receiver.Set_IO ( self [i+1], *Rec_Pars )
          self.Modified [i+1] = False
      self.Modified [0] = False
# ***********************************************************************





# ***********************************************************************
# ***********************************************************************
class tLWB_Brick ( object ):
  """
  BASE CLASS of all Bricks
  """
  Description = 'No description available'

  # called once at the start of every simulation run
  # usefull for creating non-existing variables
  # this function is automatically called by the constructor __init__
  #wordt nog gebruikt in CBrick :t_unknown maar zou niet moeten
  #def init (self):
  #  pass

  def __init__ ( self,  Container,
                 Name = '',
                 _Dummy_Control  = None,
                 _Dummy_Filename = None,
                 Pos = (-1,-1) ) :
    """ Volgens mij wordt dit niet meer gebruikt
                 Color = (220,220,220),
                 Pos = (-1,-1), Size = (-1,-1),
                 Value = '' ):
    Vervangen door
    """
    #zelfs deze moeten weg kunnen
    Size = (-1,-1)
    ##Pos = (-1,-1)
    self._Dummy_Control  = _Dummy_Control
    self._Dummy_Filename = _Dummy_Filename


    #v3print ( '' )
    #exprint ( '*********  Create Brick *********', Name )

    
    # make the container available for descendants
    self.my_Container = Container
    if Name == '':
      if Container :
        Name = 'Brick_' + str( len ( Container.Devices ) )
      else :
        Name = 'Unknown'
    self.Name = Name
    self.Caption = Name
    
    # This device wants to be executed every loop
    self.Continuous = False

    # if True, extra diagnostic info is printed
    self.Diagnostic_Mode = False

    self.Control_Defs = []

    # to prevent that messages of not implemented methods appear only once
    self.firsttime_Execute = True

    #self.my_nr = 0
    #if Container :
    #  self.my_nr = Container.diagram.GetCount()
    self.Nr = 0

    # in the execution it's used first on the right of an assigment
    # so we've to ensure that it exists
    self.On = True #False
    self.BP_Flag  = False
    self.BP_State = 0
    self.BP_Form  = None

    # IO-pin definitions
    self.Inputs    = {}
    self.Outputs    = {}
    self.N_Inputs  = 0
    self.N_Outputs = 0
    
    self.Center = False
    self.Float = False
    self.Control_Pane = None
    self.Main_Description = True
    ##self.Params = [None]
    ##self.Params_Old = [None]

    # Size must be a list, but default values must be a tupple (immutable)
    self.Size     = list(Size)
    # if size negative, give it a normal value
    if self.Size[0]<0: self.Size[0] = 50
    if self.Size[1]<0: self.Size[1] = 50
    self.Pos = list(Pos)
    self.Changed = True

    # Here get the Library Color from the global of the library file
    module = __import__ ( self.__module__ )
    try :
      self.Library_Color = module.Library_Color
    except :
      self.Library_Color = wx.RED


    # *********************************
    # here the extra initalisation
    # *********************************
    #self.PDiag ( 'before "After_Init"')
    self.After_Init()
    # *********************************

    # *********************************
    # for NEW bricks that don't call After_Init_Default
    # we use temporary this trick
    ##self.After_Init_Default ( self.Caption )

    # *****************************************************
    # Code below must not be placed in After_Control_Create
    # *****************************************************
    NI = self.N_Inputs  = 1 + len ( self.Inputs  )
    NO = self.N_Outputs = 1 + len ( self.Outputs )

    self.In_Modified  = NI * [ False ]
    self.Out_Modified = NO * [ False ]
    self.Par_Modified = NI * [ False ]

    #self.In  = tIOP_List ( self,  self.In_Modified , 'In' , NI, Null )
    #self.Out = tIOP_List ( self,  self.Out_Modified, 'Out', NO, Null )
    #self.Par = tIOP_List ( self,  self.Par_Modified, 'Par', NI, Null )
    self.In  = tIOP_List ( self,  self.In_Modified , 'In' , NI, None )
    self.Out = tIOP_List ( self,  self.Out_Modified, 'Out', NO, None )
    self.Par = tIOP_List ( self,  self.Par_Modified, 'Par', NI, None )
    # *****************************************************

    #self.PDiag ( 'after "After_Init"')
    self.Movable = True
    # *********************************
    try:
      if self.shape: pass
    except:
      self.shape = ogl.Rectangle ( Container, self, self.Pos, self.Caption )
    self.shape.fill = [ self.Library_Color ]

    #print 'SCOPE',self.Name,self.Pos

    # check and correct Inputs
    for input in self.Inputs :
      temp = self.Inputs[input]
      if len( temp ) < 3 : temp.append ( False )
      if len( temp ) < 4 : temp.append ( '' )

    """
    # Create Output_Values, always ???
    try:
      if self.Out :
        pass
    except :
      # Element 0 is not used
      self.Out = [ None ]
      self.Out_Modified = [ False ]
      Output_Copy = False
      for i in range ( 1, self.N_Outputs ) :
        if self.Outputs [i][1] == PG.TIO_INTERACTION :
          self.Out.append ( {} )
          if not ( Output_Copy ) :
            self.Output_Value_Old = {}
            Output_Copy = True
          self.Output_Value_Old [i] = None
        else :
          self.Out.append ( None )
        self.Out_Modified.append ( False )
    #self.PDiag ( 'after "Create Output Values"')
    """
    
    # and create a shallow !! copy to detect input changes
    ##self.Params_Old = copy.deepcopy ( self.Params )

    if self.Description == '' :
      self.Description = self.Name + ' for more details, see the manual'

    # for devices imported from a schematic: (re-)define the IO-pins

    # position is calculated from previous defined elements
    if self.Pos[0]<0: self.Pos[0] = 50
    if self.Pos[1]<0: self.Pos[1] = 50

    # add the shape to the canvas container
    if Container :
      Container.MyAddShape ( self)
      self.Load_Properties_from_File_to_Device()

      # if components are created dynamically, they are not always shown
      # so we explictly redraw the component here
      #self._Redraw()
      Container.Refresh()

    # if Brick is in Diagnostic Mode, display extra information
    if self.Diagnostic_Mode :
      line  = ''
      line += _(1, 'Brick Running in Diagnostic Mode\n')
      line += _(2, '*** Creating Brick ***\n')
      line += _(3, '        <Name> <Type> <Required>\n')

      for input in self.Inputs :
        try :
          line += _(4,'Input  ') + str(input) + ' = '+ str(self.Inputs[input][:-1])
          #line += _(5, ',  Value = ') + str ( self.Input_Value[input] )
          line += _(6, ',  Value = ') + str ( self.In [input] )
        except :
          line += _(7,'Input ERRROR\n')
        line   += '\n'

      line     += '\n'
      for output in self.Outputs :
        try :
          line += _(8,'Output ') + str(output) + ' = '+ str(self.Outputs[output])
          line += _(9, ',  Value = ') + str ( self.Out[output] )
          line += _(10, ',  Changed = ') + str ( self.Out_Modified[output] )
        except :
          line += _(11,'Output ERRROR')
        line   += '\n'

      line     += '\n'
      for i, par in enumerate ( self.Par) : #Params ) :
        line += _(12, 'Par  ') + str(i) + ' = ' + str(par)
        line += '\n'
      line   += '\n'

      for i, Control in enumerate ( self.Control_Defs ) :
        line += 'Control ' + str(i+1) + '\n'
        for param in Control :
          try :
            line += '  '+ str ( param ) + ' = '+  str ( Control [ param ] )
          except :
            line += _(13,'Control ERRROR')
          line   += '\n'
        line     += '\n'
      line       += '\n'

      PG.wbd ( self, line )



  # *******************************************
  # Called after the control is really created
  # *******************************************
  def After_Control_Create ( self ) :
    #print 'OOIUOOO',self.Caption,
    
    # Create special dictionairies if TIO_INTERACTION
    for Input in self.Inputs :
      indx = int ( Input )
      if self.Inputs [Input] [1] == PG.TIO_INTERACTION :
        self.In  [ indx ] = TIO_Dict ( self.In,  indx )
        self.Par [ indx ] = TIO_Dict ( self.Par, indx )
        self.In_Modified [ indx ] = []
        self.In.Set_Dict ( indx )
        self.Par_Modified [ indx ] = []
        self.Par.Set_Dict ( indx )

    for Output in self.Outputs :
      indx = int ( Output )
      if self.Outputs [ Output ] [1] == PG.TIO_INTERACTION :
        self.Out [ indx ] = TIO_Dict ( self.Out, indx )
        self.Out_Modified [ indx ] = []
        self.Out.Set_Dict ( indx )
    # *********************************

    for Control in self.Control_Defs :
      # If more the Brick has more than 1 control
      # at this point not all controls are created
      # so we only perform this action
      # for the controls that really exists
      # which can be seen by the presence of 'Control'
      if 'GUI_Control' in dir ( Control ) :
        C = Control.GUI_Control
        #print 'DDDDD=1',self.Caption,C,dir(C)
        """
        key = 'Input Channel'
        if key in Control  :
          indx = Control [ 'Input Channel' ]
          #print 'DDDDD=1',self.Caption,indx
          if indx :
            C.EP [ 0 ] = indx
            # Fill the default values and
            if  self.Inputs [ indx ] [1] != PG.TIO_INTERACTION :
              self.Par [ Control [ key ] ] = Control.Initial_Value
        """
        if ( 'Input_Channel' in dir ( Control ) ) and \
           Control.Input_Channel :
          #print 'DDDDD=1',self.Caption,indx
          indx = Control.Input_Channel
          C.EP [ 0 ] = indx
          # Fill the default values and
          if  self.Inputs [ indx ] [1] != PG.TIO_INTERACTION :
            self.Par [ Control.Input_Channel ] = Control.Initial_Value

        # for all EP's if not yet assigned, do it now
        for i, EP in enumerate ( C.EP ) :
          #v3print ( ' ****** ',i,EP, self.Par )
          # if the Ep [1 : ] is not yet coupled to a PAR
          # implicit through an input connection,
          # create an extra PAR
          if not ( isinstance ( EP, int ) ) :
            indx = len ( self.Par )
            #print '*****',self.Caption,indx,self.Par
            #self.Par.append ( Null )
            self.Par.append ( None )
            C.EP [i] = indx

          # check if Par should be a dictionairy
          if C.EP_IsDict [i] and isinstance ( C.EP[i], int ) :
            #v3print ( '**** SETDICT',self.Caption,indx,self.Par )
            self.Par.Set_Dict ( C.EP[i] )
          #v3print ( 'NNNNAAA', C.EP, C.EP_IsDict, self.Par  )
  # ************************************
  # ************************************
  def BP_Display_Vars ( self, After = False ) :
    if not ( self.BP_Form ) :
      self.BP_Form = _BP_Form ()
      self.BP_Form.Show ( True )
    HL = wx.TextAttr("RED", "YELLOW")
    if After :
      Txt = self.BP_Form.L31
    else :
      Txt = self.BP_Form.L21
    # Display Inputs
    #start = Txt.GetLastPosition()
    Txt.Clear ()
    start = 0
    Txt.AppendText ( _(14, 'Inputs\n' ) )
    Txt.SetStyle ( 0, start+6, HL )
    
    for input in self.Inputs :
      #Txt.AppendText ( str(input) + ' = ' + str ( self.Input_Value[input] ) +'\n')
      Txt.AppendText ( str(input) + ' = ' + str ( self.In [input] ) +'\n')

    #start = 1 + Txt.GetLastPosition()
    if After :
      Txt = self.BP_Form.L32
    else :
      Txt = self.BP_Form.L22
    # Display Inputs
    Txt.Clear ()
    start = 0
    Txt.AppendText ( _(15, 'Outputs\n' ) )
    Txt.SetStyle ( start, start+7, HL )

    # **********************************************
    # **********************************************
    def Disp ( value ) :
      if isinstance ( value, list ) :
        line = 'List'
        for item in value :
          line += '\n' + str ( item )
        return line
      elif isinstance ( value, tuple ) :
        line = 'Tuple'
        for item in value :
          line += '\n' + str ( item )
        return line
      elif isinstance ( value, dict ) :
        line = '{dict}'
        for key in value :
          line += '\n  ' + str ( key ) + ' = ' + str( value[key] )
        return line
      else :
        return str ( value )+'\n'
    # **********************************************

    for output in self.Outputs :
      start = Txt.GetLastPosition()
      Txt.AppendText ( str(output) + ': ' )
      Txt.SetStyle   ( start, start+2, HL )
      Txt.AppendText ( Disp ( self.Out[output] ) )


  # ************************************
  # ************************************
  def PDiag ( self,
              header = 'Output',
              extra_pars = None ) :
    """
    Prints all kinds of diagnostic information about this Brick.
    """
    print ('*****  ' + header + '  ***** Bricks Diagnostics ****')
    print ('Name / Caption =', self.Name, ' / ', self.Caption)

    try:
      if self.N_Inputs > 1 :
        print ('Inputs:', self.N_Inputs -1)
        for i in range ( 1, self.N_Inputs ) :
          print (i, ':', self.Inputs [ i ])
    except : pass

    try:
      if self.N_Outputs > 1 :
        print ('Outputs:', self.N_Outputs -1)
        for i in range ( 1, self.N_Outputs ) :
          print (i, ':', self.Outputs [ i ])
    except : pass

    try:
      if self.N_Outputs > 1 :
        print ('Output_Values:', self.N_Outputs -1)
        for i in range ( 1, self.N_Outputs ) :
          print (i, ':', self.Out [ i ])
    except : pass


    
    


  # ************************************
  # __init__ of ancestor, will call After_Init
  # ************************************
  def After_Init ( self ):
    pass

  """
  def After_Init_Default ( self, Caption = '' ):
    # the library color, used for bricks and tree, can be changed by the user
    #self.Library_Color = Library_Color
    if Caption :
      self.Caption = Caption

    if self.Center :
      self.Main_Description = False  # Don't use as panel hint

    # calculate number of inputs and outputs
    self.N_Inputs  = len ( self.Inputs ) + 1
    self.N_Outputs = len ( self.Outputs ) + 1

    # generate a list for the input values
    #self.Input_Value = []
    #self.Input_Changed = []
    #for i in range ( self.N_Inputs ) :
    #  #self.Input_Value.append ( None )
    #  self.Input_Changed.append ( False )

    # generate a list for the output values
    #??self.Out = []
    self.Out_Modified = []
    for i in range ( self.N_Outputs ) :
      if (i>0) and (self.Outputs [i][1] == PG.TIO_INTERACTION) :
        self.Out.append ( {} )
      else :
        self.Out_Modified.append ( None )

    # *********************************************
    # NEW
    # *********************************************
    #self.TIOs = TIOs_class ( self )xx
  """

  # ***********************************************************************
  # ***********************************************************************
  def Create_Control ( self, Type = None, Caption = '', Default = None ) :
    CD = Control_Description = super_object () #super_dict ()
    CD.Type          = Type
    CD.Caption       = Caption
    CD.Initial_Value = Default
    CD.Brick         = self
    CD.Input_Channel = None #-1
    CD.NewLine       = True
    self.Control_Defs.append ( CD )
    return CD
  

  # ******************************************************************
  # If inifile specified, remove this device from the ini-file
  # ******************************************************************
  def Remove_Device_From_ProjectFile ( self ):
    if PG.Active_Project_Inifile :
      PG.Active_Project_Inifile.Remove_Section ( 'Device '+ self.Name )

  # ******************************************************************
  # If inifile specified, save the properties of this device in that ini-file
  # ******************************************************************
  def Save_Properties_from_Device_to_File ( self ):
    if PG.Active_Project_Inifile :
      PG.Active_Project_Inifile.Section = 'Device '+ self.Name
      PG.Active_Project_Inifile.Write ( 'Caption',   self.shape.Caption )
      PG.Active_Project_Inifile.Write ( 'X-Pos',     round(self.shape.GetX() ))
      PG.Active_Project_Inifile.Write ( 'Y-Pos',     round(self.shape.GetY() ))
      PG.Active_Project_Inifile.Write ( 'Width',     self.shape.GetWidth() )
      PG.Active_Project_Inifile.Write ( 'Height',    self.shape.GetHeight() )
      PG.Active_Project_Inifile.Write ( 'Color On',  self.Library_Color )
      PG.Active_Project_Inifile.Write ( 'ttype',
        self.__class__.__module__ +'.'+ self.__class__.__name__  )
        
  # ******************************************************************
  # If inifile specified, load the properties of this device from that ini-file
  # ******************************************************************
  def Load_Properties_from_File_to_Device ( self ):
    if PG.Active_Project_Inifile :
      section =  'Device '+ self.Name
      if PG.Active_Project_Inifile.Has_Section ( section ):
        PG.Active_Project_Inifile.Section = section

        self.shape.Caption = PG.Active_Project_Inifile.Read ( 'Caption', self.Caption )
        self.shape.SetX ( PG.Active_Project_Inifile.Read ( 'X-Pos', round(self.shape.GetX()  ) ) )
        self.shape.SetY ( PG.Active_Project_Inifile.Read ( 'Y-Pos', round(self.shape.GetY()  ) ) )
        self.shape.SetWidth ( PG.Active_Project_Inifile.Read ( 'Width', round(self.shape.GetWidth()  ) ) )
        self.shape.SetHeight ( PG.Active_Project_Inifile.Read ( 'Height', round(self.shape.GetHeight()  ) ) )
        self.Library_Color = PG.Active_Project_Inifile.Read ( 'Color On', self.Library_Color )

      self._Redraw()

  # **********************************************************************
  # Test for changes of inputs or parameters
  # and if detected, recalculate output signals
  # also supporting of highlighting during slow stepping
  # **********************************************************************
  def Exec (self):
    try :
      PG.Debug_Table.Write ( self.Nr, Row = True )

      XIn  = copy.copy ( self.In_Modified  )
      XOut = copy.copy ( self.Out_Modified )
      """XIn  = copy.copy ( self.In. Modified )
      XOut = copy.copy ( self.Out.Modified )
      self.In. Clear_Modified ()
      self.Out.Clear_Modified ()
      """
      
      #print 'Exec_CHANGE?  Name, Xin, Xout, Xpar =', \
      #      self.Caption, XIn[0],XOut[0],self.Par.Modified[0]
      #if self.Caption == 'Code Editor' :
      #  print 'Exec_CHANGE?  XOut, Out =', \
      #      self.Caption, self.Out_Modified, self.Out
      #if self.Caption == 'Code Editor' :
      #  print 'Exec_CHANGE?  XOut, Out =', \
      #      self.Caption, self.Out_Modified, self.Out
        #print 'Exec_CHANGE?  XPar, Par =', \
        #    self.Caption, self.Par_Modified, self.Par

      # Transport Input Parameters to the control
      if XIn[0] and (len ( self.Control_Defs ) > 0 ):
        #print 'Test_For_Changes: call Brick_2_Control',self.In,self.Par
        self.Control_Pane.Brick_2_Control ( self.In )
        #print self.Params

      # Check for changes
      # and Generate output signals
      #if self.Par.Modified [0]:
      #print '*********************^^^^^^^^^^^^^^^^'
      #print ' kqkqk',self.Par_Modified,self.Par.Modified
      if XIn[0] or XOut[0] or self.Par_Modified [0] :
        #print 'Generate  Name, Xin, Xout, Xpar ****', self.Caption, XIn[0],XOut[0],self.Par.Modified[0]
        self.Generate_Output_Signals (
          self.In, self.Out, self.Par,
          XIn, XOut, self.Par.Modified )
        #print ' ********** PIEP-33'
        self.Par.Clear_Modified ()
        #print ' ********** PIEP-4'

      if self.Continuous :
        if self.Diagnostic_Mode :
          PG.wbd ( self, _(16, '  ... Run Loop' ))
        self.Run_Loop ()
      #print ' ********** PIEP-77'

    except :
      import sys
      # the third (last) element of exc_info
      # contains the traceback object
      # and might be different each time
      __line = self.Caption + ': ' + str ( sys.exc_info ()[:-1] )
      if not ( __line in PG.Brick_Errors ) :
        PG.Brick_Errors [ __line ] = 0
      PG.Brick_Errors [ __line ] += 1
      if ( PG.Brick_Errors [ __line ] % 5 ) == 1 :
        print ('***** Error Count =', PG.Brick_Errors [ __line ],)
        print ('in:', __line)
        import traceback
        traceback.print_exc ( 5 )

      #from General_Globals import Debug_From
      #Debug_From ()

      # In case of an error we want to be sure
      # to clear the modify flag of PAR
      self.Par.Clear_Modified ()

    self.In.Clear_Modified ()
    self.Out.Clear_Modified ()

    """
    else :
      print '************ OLD DOLD EXEC *******', self.Name, type(self)
      # Set highlighting and record starttime of this Brick
      #if PG.Execution_HighLight: self.Execute_Pre ()

      # reset Output_Changed
      for i,item in enumerate ( self.Out_Modified ) :
        self.Out_Modified [i] = False

      # If all required inputs available and
      # an input or parameter changed then
      # let the brick recalculate it's output signals
      try:
        if self.Test_For_Changes () :
          #print 'Generate_Output_Signals:',self.Name,self.__class__.__name__
          try :
            if self.Diagnostic_Mode :
              PG.wbd ( self, _(17, 'Generating Output Signals ...') )
              PG.wbd ( None, _(18, '  INPUT_VALUES  ',) + str (self.In) )

            self.Generate_Output_Signals ()

            if self.Diagnostic_Mode :
              pass
              PG.wbd ( None, _(19, '  OUTPUT_VALUES ',) + str (self.Out) )
              PG.wbd ( None, _(20, '  OUTPUT_CHANGE ',) + str (self.Out_Modified) )
              PG.wbd ( None, _(21, '  ... Succeeded\n') )
          except :
            if self.Diagnostic_Mode :
              PG.wbd ( None, _(22, '  ... Failed\n') )
            PG.em ( _(23, 'Generate_Output_Signals in ') + self.__class__.__name__ )
        # keep the actual values
        #self.Params_Old = copy.copy ( self.Params )
        self.Params_Old = copy.deepcopy ( self.Params )
      except:
        pass

      if self.Continuous :
        if self.Diagnostic_Mode :
          PG.wbd ( self, _(24, '  ... Run Loop' ))
        self.Run_Loop ()

      #print '   outputs: ',self.Output_Value
    """
    
    # insert some time for GUI processes
    while PG.app.My_EventLoop.Pending(): PG.app.My_EventLoop.Dispatch()
    PG.app.My_EventLoop.ProcessIdle()

    # wait a time and stop highlighting
    #if PG.Execution_HighLight: self.Execute_Post ()
    #print 'EXEC-FIN', self.Name, type(self)
  # **********************************************************************


  # **********************************************************************
  # Tests if all required Inputs are available
  # Tests if changes in Inputs and/or Parameters occurred
  # Does the houskeeping for the history values
  # Returns TRUE, if all required inputs are there and a change occured
  # **********************************************************************
  """
  def Test_For_Changes ( self ) :
    line = ''
    #if Application.Debug_Mode :
    if 'IO-Changes' in Debug_What :
      print ' '
      print '******** TEST CHANGES  ', self.Name,str(type(self)).split('.')[1][2:-2]
      #print '  Inputs: ', self.In [1:]
      print '  In_Modified  :', self.In_Modified [1:]
      print '  Params       :', self.Par [1:]
      print '  Out_Modified :', self.Out_Modified [1:]
      print '  Out          :', self.Out [1:]

    Change = False

    #*********************************************************************
    # Test if all required inputs are available
    #   if NOT, return FALSE
    # And also tests if one of the inputs has changed
    # NOTE: Inputs are in range [ 1 .. ]
    #       Params, Values are in range [ 0 .. ]
    #*********************************************************************
    for Input in  self.Inputs :
      # test if all required inputs available and
      # if any (also not required) input has changed
      #print self.Name,Input,self.Inputs [Input],self.In,self.Output_Value
      #print '**********',Input,self.Inputs[Input]
      if self.Inputs [Input] [2] :
        if self.In [Input] == None:
          if self.Diagnostic_Mode :
            line += _(25, 'Not all required inputs available\n')
          return False
      if self.Input_Changed [Input] :
        if self.Diagnostic_Mode :
          line += _(26, 'Inputs Changed ...\n')
        Change = True
    IC=Change

    # check if parameters/controls are changed by input signals
    try:
      for i, Control in enumerate ( self.Control_Defs ) :
        # Check if input value overrides control value
        C = Control ['Input Channel']
        if C and self.In [C]:
          if self.Diagnostic_Mode  and \
            self.Params [i+1] != self.In [C] :
              line += '  Params[' +str(i+1) + '] = In['+str(i+1)+'] = '
              line += str(self.In [C])+'\n'
          self.Params [i+1] = self.In [C]
    except:
       pass

    # Check for any changes in the parameters
    try:
      if self.Params != self.Params_Old :
        if self.Diagnostic_Mode :
          line += _(27, '  Params Changed ...\n')
        print '**********************PARS CHANGED',self.Name, self.Params
        Change = True
    except:
      print 'Pars_change_error',self.Params
      print 'Pars_change_error',self.Params_Old

    # For special outputs of type TIO_INTERACTION
    # we also need to check these outputs
  """
  """
    for i in self.Outputs :
      if self.Outputs[i][1] == PG.TIO_INTERACTION :
        if self.Output_Value_Old[i] != self.Out[i] :
          print 'qereqwet'
          # create a real copy to detect output changes
          # because this will in general be a dictionary
          self.Output_Value_Old[i] = copy.deepcopy ( self.Out[i] )
          print 'qereqwet $$$$$'
          Change = True
  """
  """
    #*********************************************************************
    # Send changes (input and/or params) to the control
    # Store new values for future comparison
    #*********************************************************************
    if self.Diagnostic_Mode :
       PG.wbd ( self, line )

    if Change  and (len ( self.Control_Defs ) > 0 ):
      #print 'Test_For_Changes: call Brick_2_Control'
      self.Control_Pane.Brick_2_Control ( self.In )

      # should be done after output generation,
      # so output generation can actual use it,
      # to see if there are differences
      # and manipulate them to get called every time
      # WRONG ?? !!
      #self.Params_Old = copy.copy ( self.Params )

    return Change
  # **********************************************************************
  """

  # **********************************************************************
  # **********************************************************************
  #def Set_IO ( self, Value, IO, indx ) :
  def Set_IO ( self, Value, IO, indx ) :
    #print '   Set IO', self.Name, Value, IO, indx
    if IO == 'Out' :
      self.Out [indx] = Value
    else :
      # test if input is connected to a control
      C = self.In.IO_Par [ indx ]
      #if C != Null :
      if C != None :
        # if so, send change to control
        C.SetValue ( Value )
      else :
        self.In [indx] = Value

  # **********************************************************************
  # **********************************************************************
  def Generate_Output_Signals_Debug ( self, In, Out, Par, XIn, XOut, XPar ) :
    """
    This procedure is called only,
    when inputs (or parameters) have changed

    Dummy procedure, can be used during debug:
      self.Generate_Output_Signals = \
        self.Generate_Output_Signals_Debug
    """
    print ('******** Generate_Output_Signals_Debug: ',self.Caption)
    print ('  Xin,  In  ', XIn,  In)
    print ('  XOut, Out ', XOut, Out)
    print ('  XPar, Par ', XPar, Par)
    print ('  In  Connected', self.Input_Connected)
    print ('  Out Connected', self.Output_Connected)
    return

  # **********************************************************************
  # **********************************************************************
  #def Generate_Output_Signals (self):
  def Generate_Output_Signals ( self, In=None, Out=None, Par=None,
                                XIn=None, XOut=None, XPar=None ) :
    if self.firsttime_Execute and ( self.N_Outputs > 1 ):
      self.firsttime_Execute = False
      print ('Generate_Output_Signals not yet implemented for this device:', self.Name)
      print ('  ', self.__class__.__module__ + '.' + self.__class__.__name__,\
            '(' + self.shape.Caption + '//"' + self.Name+ '")')


    PG.Execution = True

  """
  def Execute_Pre ( self ):
    self.On = False
    self._Redraw()
    self.Start_Time = time.time ()

  def Execute_Post ( self ):
    delay = 1.0 - ( time.time() - self.Start_Time)
    if delay > 0 :
      time.sleep ( delay )
    PG.Execution = True
    self.On = True
    self._Redraw()
  """
  
  # ************************************
  # redraw the component
  # ************************************
  def _Redraw (self):
    if self.On :
      self.shape.pen  = [ 'BLACK', 1 ]
    else:
      self.shape.pen  = [ PG.Brick_Execution_Color, 3 ]
    self.my_Container.Refresh ()

# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class t_Dummy_Brick ( tLWB_Brick ) :
  """
  Dummy Brick to test individual Controls
  """
  def After_Init ( self ) :
    # Import the specified control
    # We must do a relaod, to catch changes
    line = 'import ' + self._Dummy_Filename
    exec ( line )

    line = 'reload (' + self._Dummy_Filename + ')'
    exec ( line )

    line = 'from ' + self._Dummy_Filename + ' import ' + self._Dummy_Control
    exec ( line )

    # Create the specified control
    line = 'CD = self.Create_Control ( ' + self._Dummy_Control + ',"Test Label" )'
    exec ( line )

# ***********************************************************************
pd_Module ( __file__ )
