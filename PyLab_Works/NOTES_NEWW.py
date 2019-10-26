[Device SN3]
Caption = 'Load File'

[Device SN2]
Caption = 'Rotate'

[Device SN4]
Caption = 'Show'



EXEC SN4 Show
EXEC SN3 Load File
Generate False False True
   transmit from: SN3 1   Value: <wx._core.Image; proxy of <Swig Object of type 'wxImage *' at 0xbce9878> >
              to: SN2 ('In', 1)
   Set IO SN2 <wx._core.Image; proxy of <Swig Object of type 'wxImage *' at 0xbce9878> > In 1
EXEC SN2 Rotate
Generate True False False
   transmit from: SN2 1   Value: <wx._core.Image; proxy of <Swig Object of type 'wxImage *' at 0xbda5d80> >
              to: SN4 ('In', 1)
   Set IO SN4 <wx._core.Image; proxy of <Swig Object of type 'wxImage *' at 0xbda5d80> > In 1
EXEC SN4 Show
Generate True False False
EXEC SN3 Load File
EXEC SN2 Rotate
EXEC SN4 Show
EXEC SN3 Load File
EXEC SN2 Rotate



  def Exec (self):
    if self.NEWW :
      XIn  = copy.copy ( self.In. Modified )
      XOut = copy.copy ( self.Out.Modified )
      self.In. Clear_Modified ()
      self.Out.Clear_Modified ()
      #print 'EXEC', self.Name, self.Caption
      #C = self.In.IO_Par [ indx ]
      if XIn[0] or XOut[0] or self.Par.Modified [0] :
        print 'Generate',XIn[0],XOut[0],self.Par.Modified[0]
        self.Generate_Output_Signals (
          self.In, self.Out, self.Par,
          XIn, XOut, self.Par.Modified )
        self.Par.Clear_Modified ()

      #print 'XIN',XIn, self.Controls,self.In
      if XIn[0] and (len ( self.Controls ) > 0 ):
        print 'Test_For_Changes: call Brick_2_Control',self.In,self.Par
        self.Control_Pane.Brick_2_Control ( self.In )
        print self.Params

      # OLD method
      if self.Params != self.Params_Old :
        self.Generate_Output_Signals (
          self.In, self.Out, self.Params,
          XIn, XOut, self.Par.Modified )
        self.Params_Old = copy.copy ( self.Params )

      self.In.Transmit_Changes  ()
      self.Out.Transmit_Changes ()



# ***********************************************************************
# ***********************************************************************
class t_Dummy ( tLWB_Brick ) :

  Description = """Extended Discription of this Brick"""

  def After_Init (self):
    self.Caption = 'My Caption'

    # Define the input pins
    # <Pin-Name>, <Data_Type>, <Required>, <Description>
    self.Inputs [1] = ['Pin-1 Name', TIO_NUMBER, True, 'Description' ]
    self.Inputs [2] = ['Pin-2 Name', TIO_NUMBER, True, 'Description' ]

    self.Outputs [1] = ['PinOut-1 Name', TIO_NUMBER, 'Description' ]

    # Create the GUI controls
    C = self.Create_New_Control ()
    C [ 'Type' ]         = CT_SOMETHING
    C [ 'Input Channel'] = 2

    # Create the second GUI controls
    C = self.Create_New_Control ()
    C [ 'Type' ]         = CT_SOMETHING

  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    Out[1] = 2 * In[1] + Par[2] + Par[3]
# ***********************************************************************



Brick_1.Out.Receivers[1] =
{
  Brick_1 : ( 'Out', 1 ),
  Brick_2 : ( 'In', 1 ),
  Brick_3 : ( 'In', 1 )
}


Brick_3.In[1].Receivers = Brick_1.Out[1].Receivers

Brick_1.Out.Receivers[1] [Brick_1] = ( 'Out', 1 )


  def Exec (self):
    XIn  = copy.copy ( self.In. Modified )
    XOut = copy.copy ( self.Out.Modified )
    self.In. Clear_Modified ()
    self.Out.Clear_Modified ()

    # Transport Input Parameters to the control
    if XIn[0] and (len ( self.Controls ) > 0 ):
      self.Control_Pane.Brick_2_Control ( self.In )

    # Check for changes
    # and Generate output signals
    if XIn[0] or XOut[0] or self.Par.Modified [0] :
      self.Generate_Output_Signals (
        self.In, self.Out, self.Par,
        XIn, XOut, self.Par.Modified )
      self.Par.Clear_Modified ()

    # Transport changed values to receivers
    self.In.Transmit_Changes  ()
    self.Out.Transmit_Changes ()


