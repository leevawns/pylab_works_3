# ***********************************************************************
# Standard libraries
# ***********************************************************************
from brick import *
from PyLab_Works_Globals import _
from PyLab_Works_Globals import *
#from base_control        import *
from import_controls import *
from array_support   import Analyze_TIO_Array, class_MetaData

#print 'PG2',dir (PyLab_Works_Globals)
#print 'brick1',dir()
#print 'brick2',dir()

# ***********************************************************************
# If color is ignored, default BLACK is selected
# ***********************************************************************
Library_Color = wx.Colour ( 250, 150, 90 )

# ***********************************************************************
# Library_Icon,

#   - can be an index in the image-list (not recommended)
#   - or the filename of an image in this directory
# ***********************************************************************
Library_Icon = 'camera_edit.png'


Description = """Media Library.
Line 2 of ... """

# ***********************************************************************
# ***********************************************************************
class t_Play_Sound ( tLWB_Brick ):
  Description = """Plays a wav file"""

  def After_Init (self):
    self.Caption =  _(1, 'Play SoundFile')
    self.Inputs [1] = ['FileName or Stream', TIO_ARRAY, True ]

    # Create the GUI controls
    CD = self.Create_Control ( t_C_Slider, 'Volume', 20 )
    CD.Range   = [ 1, 100 ]

    CD = self.Create_Control ( t_C_Buttons, '', 20 )
    CD.Caption = [ 'RePlay', 'Stop' ]

    self.soundfile = None

  # **********************************************************************
  # this procedure is only called when inputs (or parameters) have changed
  # **********************************************************************
  def Generate_Output_Signals ( self, In, Out, Par, XIn, XOut, XPar ) :
    import wave
    import pygame

    print ('PLAY SOUND',XIn,XPar, Par)
    if XIn [1] and (In[1]!=None) : # <========= Krijgt een keer None  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
      if 'soundfile' in dir(self):
        print ('------------------->')
        if type(self.soundfile) == pygame.mixer.Sound:
          self.soundfile.stop()

      filename = In[1]

      if not ( isinstance ( filename, basestring ) ) :
        data, MetaData = Analyze_TIO_Array(In[1])
        data = data[0]
        MetaData = MetaData[0]
        print (type(data),type(MetaData))

        pygame.sndarray.use_arraytype('numpy')
        Frequency = MetaData.Get('Frequency',5000)
        ByteWidth  = MetaData.Get('ByteWidth',1)

        print ('--------------------------->\n\n',ByteWidth,type(data),data)

        if ByteWidth == 1:
          pygame.mixer.pre_init(Frequency, 8, 1)
          pygame.init()
          self.soundfile = pygame.sndarray.make_sound(array(data,uint8))  # < maakt op zich niet uit
        else:
          pygame.mixer.pre_init(Frequency, -8*ByteWidth, 1)
          pygame.init()
          #self.soundfile = pygame.sndarray.make_sound(array(data,'>i'+str(BitWidth)))  # < maakt op zich niet uit
          self.soundfile = pygame.sndarray.make_sound(data.astype('>i'+str(ByteWidth)))  # < maakt op zich niet uit

#        self.soundfile = pygame.sndarray.make_sound(array(data,uint8))
        print (type(self.soundfile))
      else:
        wav      = wave.open ( filename, 'r' )
        fSamp    = wav.getframerate ()
        NChan    = wav.getnchannels ()
        ByteWidth = 8 * wav.getsampwidth ()
        wav.close ()

        # play soundfile
        try :
          import pygame
        except :
          pass
        #from pygame.locals import *
        pygame.mixer.quit ()
        pygame.mixer.init ( fSamp, ByteWidth, NChan )
        self.soundfile = pygame.mixer.Sound ( filename )

      self.soundfile.play ()
      '''
      # If input is not a filename,
      # write the input signal to a wav file
      # and use that wav file
      if not ( isinstance ( filename, basestring ) ) :
        filename = '../../pief_paf.wav'
        wav_result = wave.open ( filename, 'w' )

        Frequency = 5000 #In [1].Get ( 'Frequency', 5000 )
        #print dir(In[1]),In[1].Frequency, Frequency
        #Frequency = 11050 #5000
        print '----x>',In[1][:20]
        wav_result.setparams ( ( 1, 1, Frequency, 1,
                                 'NONE', 'not compressed' ) )
        aaa = ''
        for i in In [1]:
          #aaa = aaa + chr ( int ( i * 256 / 5 ))
          aaa = aaa + chr ( int (i))
        wav_result.writeframes ( aaa )
        wav_result.close ()


      # get soundfile parameters
      wav      = wave.open ( filename, 'r' )
      fSamp    = wav.getframerate ()
      NChan    = wav.getnchannels ()
      BitWidth = 8 * wav.getsampwidth ()
      wav.close ()

      # play soundfile
      try :
        import pygame
      except :
        pass
      #from pygame.locals import *
      pygame.mixer.quit ()
      pygame.mixer.init ( fSamp, BitWidth, NChan )
      self.soundfile = pygame.mixer.Sound ( filename )
      self.soundfile.play ()
      '''
    if self.soundfile :
      # Par[3] == 0 ==> Stop
      # Par[3] == 1 ==> Replay
      if XPar [3] :
        self.soundfile.stop ()
        if Par[3] == 0 :
          self.soundfile.play ()

      # Set Volume
      self.soundfile.set_volume ( Par [2] / 100.0 )
# ***********************************************************************



