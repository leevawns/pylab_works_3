# Vragenlijst Class
from db_support            import *
from win_inifile_support   import *
from vragenlijst_constants import *
from vragenlijst_vraag     import *
from vragenlijst_subschaal import *


# ***********************************************************************
# ***********************************************************************
class t_Vragenlijst ( Ini_DB_Object ) :
  def __init__ ( self, filename = None ) :
    self.Ini       = win_inifile ()
    self.Name      = 'Dummy'
    self.Path      = None
    self.IsRead    = False
    self.ID_Column = 'VLID'

    #                                type  default    NotNull   Primary Key
    self.Attribs = {}
    self.Attribs [ 'Name'        ] = [ str,  '???'      ,True  ]
    self.Attribs [ 'Module'      ] = [ str,  'Vragenlijst' ,True  ]
    self.Attribs [ 'Versie'      ] = [ str,  '???'      ,True  ]
    self.Attribs [ 'Titel'       ] = [ str,  'No Title' ,True  ]
    self.Attribs [ 'SPSS_Prefix' ] = [ str,  '_'        ,True  ]
    self.Attribs [ 'Font_Name'   ] = [ str,  'Arial'    ,True  ]
    self.Attribs [ 'Font_Size'   ] = [ int,  12         ,True  ]
    self.Attribs [ 'Font_Color'  ] = [ int,  0          ,True  ]
    self.Attribs [ 'Font_Style'  ] = [ int,  0          ,True  ]
    self.Attribs [ 'Disc_Expl'   ] = [ str,  ''         ,True  ]
    self.Attribs [ 'Vrst_Expl'   ] = [ str,  ''         ,True  ]
    self.Attribs [ 'Kind_Layout' ] = [ bool, False      ,True  ]
    self.Attribs [ 'Vraag_N'     ] = [ int,  0          ,True  ]
    self.Attribs [ 'SubSchaal_N' ] = [ int,  0          ,False ]

    self.Vraag         = []
    self.SubSchaal     = []
    self.SPSS_FullName = []
    self.SPSS_RelName  = []
    self.SPSS_RelNmin  = []

    if filename :
      self._Read ( filename )

    self.Dummy_Vraag           = t_Vraag                 ( self, 0 )
    self.Dummy_SubSchaal       = t_Vragenlijst_SubSchaal ( self, 0 )

  # ******************************************
  # ******************************************
  def _Read ( self, filename ) :
    self.Ini = win_inifile ( filename, Force_Identifiers = True )

    #**************************************
    # Try to read all the attributes from the inifile
    #**************************************
    self.Read_Attribs ( 'Algemeen')

    #**************************************
    # Correct self.Name
    #**************************************
    self.Path, Name  = path_split    ( filename )
    self.Name        = os.path.splitext ( Name     )[0]
    self.Table_Name  = '_V_' + self.Name

    #**************************************
    # Determine the number of questions
    #**************************************
    Sections = self.Ini.Sections ()
    for i in range ( vraag_maxn_max ) :
      if not ( 'vraag_' + str ( i+1 ) in Sections  ) :
        self.Vraag_N = i
        self.Vraag   = ( i+1 ) * [ None ]
        break
    else :
      return

    #**************************************
    # SubSchalen
    #**************************************
    section = 'SubSchalen'
    if section.lower() in self.Ini.Sections () :
      _ss = self.Ini.Get_Section ( section )

      # Get number of SubSchalen
      self.SubSchaal_N = 0
      for item in _ss :
        if item[0].lower() == 'aantal' :
          self.SubSchaal_N = int ( item[1] )
          break

      self.SubSchaal = self.SubSchaal_N * [ None ]
      for i in range ( self.SubSchaal_N ) :
        self.SubSchaal [i] = t_Vragenlijst_SubSchaal ( self, i )
        self.SPSS_FullName.append ( self.SubSchaal [i].Name_ )

    #**************************************
    # Read all Vragen
    #**************************************
    for i in range ( self.Vraag_N ) :
      self.Vraag [i+1] = t_Vraag ( self, i+1 )

    self.IsRead = True

  # ******************************************
  # ******************************************
  def Print_All ( self ) :
    if not ( self.IsRead ) : return

    self.Print ( 'Vragenlijst : '+ self.Name )
    self.Print_Vragen ()
    self.Print_SubSchalen ()

    v3print ( '----- SQL Table Definition VragenLijst -----' )
    for item in self.Get_Table_Def () :
      v3print ( ' ', item )

  # ******************************************
  # ******************************************
  def Print_Vragen ( self ) :
    if not ( self.IsRead ) : return
  
    v3print  ( '\n----- Vragen -----' )
    for Vraag in self.Vraag :
      if Vraag :
        Vraag.Print_Vraag ()

  # ******************************************
  # ******************************************
  def Print_SubSchalen ( self ) :
    if not ( self.IsRead ) : return
  
    print '\n----- SubSchalen -----'
    for SS in self.SubSchaal :
      SS.Print_Vragenlijst_SubSchaal ()
# ***********************************************************************


# ***********************************************************************
# ***********************************************************************
if __name__ == '__main__':

  Test_Defs ( 1 )

  #******************************************
  # test read vragenlijst informatie
  #******************************************
  if Test ( 1 ) :
    Base_Dir     = 'D:/d_midorg/'
    Protocol_Dir = Base_Dir + 'Protocol/'
    filename     = Protocol_Dir + 'VraagLST/ess.vli'

    v3print ( '  Vragenlijst:', filename )
    VL = t_Vragenlijst ( filename )

    VL.Print_All ()
    """
    VL.Print ( 'Algemeen Vragenlijst ' + VL.Name )
    VL.Print_Subschalen ()
    VL.Print_Vragen     ()

    print VL.Get_Table_Def ()
    """