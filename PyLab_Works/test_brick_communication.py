"""
This is a unit to test the communication protocol between bricks
"""

from copy import copy

# ***********************************************************************
# ***********************************************************************
class TIO_Dict ( dict ) :
  """
  Special Dictionairy, that detects changes
  """
  def __init__ ( self, Parent , PIndex ):
    self.Parent = Parent
    self.PIndex = PIndex
    dict.__init__ ( self )

  # Override Assign, so we can set the change flag
  def __setitem__ ( self, key, value ) :
    dict.__setitem__ ( self, key, value )

    # Pass the modify flag to the parent
    self.Parent._Set_Modified ( self.PIndex, value, key )
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class tIOP_List ( list ) :
  #def __init__ ( self, Brick, Name = 'IO', leng = 0, Value = Null ):
  def __init__ ( self, Brick, Modified, Name = 'IO', leng = 0, pre=0 ) :
    self.Brick    = Brick
    self.Modified = Modified    # Points to the modify list of the owner
    self.Name     = Name
    self.Pre      = pre * ' '
    self.N        = leng
    self.NRange   = range ( 1, self.N )

    # Create te List itself
    # Create the Receiver lists
    # THIS:  self.Receivers = leng * [{}]
    # will result in identical directories !!
    list.__init__ ( self )
    self.Receivers = []
    for i in range ( leng ) :
      list.append ( self, None )
      self.Receivers.append ( {} )

    self.Is_Dict = leng * [ None ]
    
  def Set_Dict ( self, indx ) :
    """
    Makes this element an TIO_INTERACTION
    - set Is_Dict
    - if it's the output, add itself to the receiver list
    """
    list.__setitem__ ( self, indx, TIO_Dict( self, indx ) )
    self.Is_Dict [ indx ] = True
    if self.Name.lower() == 'out' :
      self.Receivers [ indx ] [ self.Brick ] = \
        ( self, self.Modified, indx )

  # Override Assign, so we can set the change flag
  def __setitem__ ( self, indx, value ) :
    print ' ***********',self.Brick.Name,self.Name,indx, value
    list.__setitem__ ( self, indx, value )
    self._Set_Modified ( indx, value )

  def _Set_Modified ( self, indx, value, key = None ) :
    """
    Sets the modify flag of the receivers
    - for normal IOs TRUE
    - for TIO_INTERACTION, append the key
    """
    for Key_Brick in self.Receivers [indx] :
      Receiver = self.Receivers [indx] [ Key_Brick ]
      print self.Pre + '-- from', \
           self.Brick.Name + '.' + self.Name+'['+str(indx)+']', \
           'to', Receiver[0].Brick.Name + '.' + \
           Receiver[0].Name +'['+str(Receiver[2])+']'
      if self.Is_Dict [indx] :
        Receiver [1] [indx].append ( key )
      else :
        Receiver [1] [indx] = True
        Receiver [0] [indx] = value
      Receiver[1] [0]    = True
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
class tBrick ( object ) :
  def __init__ ( self, name, pre = 0 ) :
    self.Name = name
    self.Pre  = pre * ' '
    
    NI = NO = 4
    
    # Make our own modify list
    self.In_Modified  = NI * [ False ]
    self.Out_Modified = NO * [ False ]
    # For TIO_INTERACTION we need lists
    self.In_Modified [1] = []
    self.Out_Modified [1] = []

    self.In   = tIOP_List ( self, self.In_Modified,  'In',  NI, pre )
    self.Out  = tIOP_List ( self, self.Out_Modified, 'Out', NO, pre )

    # this Brick also listen to it's OWN output
    self.Out.Set_Dict ( 1 )
    self.In.Set_Dict  ( 1 )

    # for test
    self.Initialized = False

  def Execute ( self ) :
    # Start with some initial values
    if not ( self.Initialized ) and ( self.Name == 'Brick-1' ) :
      self.In[1] [ 'a' ] = 3
      self.In[2]         = 'aap'
      self.In_Modified [0] = True
      self.In_Modified [1].append ( 'a' )
      self.In_Modified [2] = True
    self.Initialized = True

    print
    print self.Pre + '  In  =', self.In
    print self.Pre + '  Out =', self.Out
    print self.Pre + 'EXEC',self.Name

    XIn  = copy ( self.In_Modified  )
    XOut = copy ( self.Out_Modified )

    if XIn [2] :
      print self.Pre + 'EXEC, Output-2 Changed'
      if self.In [2] :
        self.Out [2] = self.In [2] + ' bos'

    if XOut [1] :
      print self.Pre + 'EXEC, Output-1 Changed', XOut[1]
      #if 'b' in self.Out[1] :
      if 'b' in XOut[1] :
        self.In  [1] [ 'c' ] = 3 * self.Out [1] [ 'b' ]
        self.Out [1] [ 'd' ] = 4 * self.Out [1] [ 'b' ]

    if XIn [1] :
      print self.Pre + 'EXEC, Input-1 Changed', XIn[1]
      #if 'a' in self.In[1] :
      if 'a' in XIn[1] :
        self.In  [1] [ 'b' ] = 2 * self.In [1] [ 'a' ]
        self.Out [1] [ 'a' ] = 7 * self.In [1] [ 'a' ]

    # We don't need to know our own changes
    # THIS : self.In_Modified = 4 * [False]
    #   not allowed, creates a new onject !!
    for i in range(4) :
      self.In_Modified  [i] = False
      self.Out_Modified [i] = False
    # For TIO_INTERACTION we need lists
    self.In_Modified [1] = []
    self.Out_Modified [1] = []

    print self.Pre + '  In  =', self.In
    print self.Pre + '  Out =', self.Out
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
if __name__ == '__main__' :

  # Create the Bricks
  Brick1 = tBrick ( 'Brick-1' )
  Brick2 = tBrick ( 'Brick-2', 30 )
  
  # Connect the Bricks
  Brick1.Out.Receivers[1] [ Brick2 ] = ( Brick2.In, Brick2.In_Modified, 1 )
  Brick1.Out.Receivers[2] [ Brick2 ] = ( Brick2.In, Brick2.In_Modified, 2 )

  # Because the connection is a TIO_Dict
  # Both need to point to the same object
  # Becuase there's only 1 Output, we choose that
  Brick2.In[1] = Brick1.Out[1]

  # Run the Bricks
  for i in range ( 3 ):
    Brick1.Execute ()
    Brick2.Execute ()
    
