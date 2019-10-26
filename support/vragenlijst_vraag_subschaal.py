from db_support            import *
from vragenlijst_constants import *

# ***********************************************************************
# ***********************************************************************
class t_Vraag_SubSchaal ( Ini_DB_Object ) :
  def __init__ ( self, parent, SPSS = None ) :
    self.Vraag = parent
    self.SPSS  = SPSS
    
    Ini_DB_Object.__init__ ( self )
    self.ID_Column = 'VSID'

    #                                type  default    NotNull   Primary Key
    self.Attribs = {}
    for i in range ( keuze_antwoorden_maxn + 1 ) :
      line = 'SS_' + str(i)
      self.Attribs [ line ] = [ str, '' , False  ]
      setattr ( self, line, '' )
      
    self.Ini        = self.Vraag.Ini
    self.Table_Name = '_VVS_'+ self.Vraag.Vragenlijst.Name

    # Read the SubSchaal Values
    if SPSS :
      self._Read ()
    else :
      self.Values = ( keuze_antwoorden_maxn + 1 ) * ['']



  #**********************************************
  #**********************************************
  def _Read ( self ) :
    self.Values = ( keuze_antwoorden_maxn + 1 ) * ['']
    for SV in range ( self.Vraag.Aantal_SubVragen + 1 ) :
      line = str(SV) + '_' + self.SPSS
      SubSchaal = self.Ini.Read_String ( line, None )
      if SubSchaal :
        self.Values [ SV ] = SubSchaal
        setattr ( self, 'SS_' + str (SV ), str ( SubSchaal ) )

    if self.Not_Empty () :
      v3print ( '   -- Vraag / SubSchaal =', self.Vraag.Indx, '/', self.SPSS, self.Values )
    
  #**********************************************
  #**********************************************
  def Not_Empty ( self ) :
    return ''.join ( self.Values )

  #**********************************************
  #**********************************************
  def Print ( self ) :
    print 'TODO t_Vraag_SubSchaal'

# ***********************************************************************
