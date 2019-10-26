#Class Vraag
from db_support            import *
from win_inifile_support   import *
from vragenlijst_constants import *
from vragenlijst_vraag_subschaal import t_Vraag_SubSchaal
import os


# ***********************************************************************
# ***********************************************************************
class t_Vraag ( Ini_DB_Object ) :

  def __init__ ( self, parent, indx ) :
    self.Vragenlijst = parent
    Ini_DB_Object.__init__ ( self )
    #self.Primary_Key = None
    self.ID_Column = 'VID'

    #                                type  default    NotNull   Primary Key
    self.Attribs = {}
    self.Attribs [ 'VraagSoort'              ] = [ str,  '0:Unknown'   ,True  ]
    self.Attribs [ 'Vraag_Hoogte'            ] = [ int,  100   ,True  ]
    self.Attribs [ 'Antwoord_Afstand'        ] = [ int,  0     ,False ]
    #self.Attribs [ 'Versie_684_1'            ] = [ bool, False ,False ]
    self.Attribs [ 'Explicit'                ] = [ bool, False ,False ]
    self.Attribs [ 'Vraag_Sound'             ] = [ str,  ''    ,False ]

    self.Attribs [ 'Font1_Name'              ] = [ str,  ''    ,False ]
    self.Attribs [ 'Font1_Size'              ] = [ int,  12    ,False ]
    self.Attribs [ 'Font1_Color'             ] = [ int,  0     ,False ]
    self.Attribs [ 'Font1_Style'             ] = [ int,  0     ,False ]

    # komt voor bij vraag 4
    self.Attribs [ 'Font2_Name'              ] = [ str,  ''    ,False ]
    self.Attribs [ 'Font2_Size'              ] = [ int,  None  ,False ]
    self.Attribs [ 'Font2_Color'             ] = [ int,  None  ,False ]
    self.Attribs [ 'Font2_Style'             ] = [ int,  None  ,False ]

    # komt voor bij vraag 6
    self.Attribs [ 'Aantal_SubVragen'        ] = [ int,  5     ,True  ]
    self.Attribs [ 'Nummers_Zichtbaar'       ] = [ bool, False  ,False ]
    self.Attribs [ 'SplitBlok'               ] = [ int,  0     ,False ]
    self.Attribs [ 'Aantal_BlokAntwoorden'   ] = [ int,  5     ,True  ]
    self.Attribs [ 'Ruimte_Tussen_SubVragen' ] = [ int,  0     ,False ]
    self.Attribs [ 'Kolom_Offset_Number'     ] = [ int,  1     ,False ]

    self.Attribs [ 'Vars_Integer'            ] = [ list, 0     ,False ]
    self.Attribs [ 'Vars_Boolean'            ] = [ list, 0     ,False ]
    self.Attribs [ 'Overslaan'               ] = [ list, 0     ,False ]

    self.Attribs [ 'RapportRegel_1'          ] = [ str,  ''    ,False ]
    self.Attribs [ 'RapportRegel_2'          ] = [ str,  ''    ,False ]

    self.Ini  = parent.Ini
    self.Table_Name = '_VV_'+ parent.Name
    self.Indx = indx
    self.Read_Attribs ( 'Vraag_' + str ( indx ) )

    self.Dummy_Vraag_SubSchaal = t_Vraag_SubSchaal ( self )

    # Get the vraagsoort as a number
    self.VraagSoort_Nr        = int ( self.VraagSoort.split(':')[0] )

    # allerlei positionerings variabelen wegschrijven
    # Extra Integers are not read correctly through the Attributes
    self.Vars_Integer = 8 * [ 0 ]
    for i in range ( 8 ) :
      self.Vars_Integer [i] = self.Ini.Read_Integer ( 'Integer_' + str(i+1), 0 )

    # default antwoord zetten
    if self.Vars_Integer [7] != 0 :
      self.Antwoord_Num1 = \
        round ( self.Vars_Integer [0] +
                self.Vars_Integer [2] *
                  ( self.Vars_Integer[1] - self.Vars_Integer[0] ) /
                self.Vars_Integer [7] )
    else :
      self.Antwoord_Num1 = self.Vars_Integer [0]

    self.Vars_Boolean = 9 * [ False ]
    for i in range ( 9 ) :
      self.Vars_Boolean [i] = self.Ini.Read_Bool ( 'Boolean_' + str(i+1), False )
    #print '*******VB',self.Vars_Boolean
    #print self.Ini.Print_All ()

    # Vraag proberen te lezen vanuit RTF
    if self.Vragenlijst.Path :
      filename = self.Vragenlijst.Name + '_' + str ( self.Indx ) + '.rtf'
      filename = os.path.join ( self.Vragenlijst.Path, filename )
      #print 'RTF-file',filename
      if os.path.exists ( filename ) :
        pass

    #else :
    # maar nu even altijd
    self.Vraag = ''
    for i in range ( max_vraag_lines ) :
      line = self.Ini.Read_String ( 'VraagRegel_' + str ( i+1), '' )
      self.Vraag += line + '\n'
    # strip the white space on the right
    self.Vraag = self.Vraag.rstrip ()

    self.Vraag_Rapport = ''
    for i in range ( max_rapport_lines ) :
      line = self.Ini.Read_String ( 'RapportRegel_' + str ( i+1), '' )
      self.Vraag_Rapport += line + '\n'
    # strip the white space on the right
    self.Vraag_Rapport = self.Vraag_Rapport.rstrip ()



    # Antwoorden
    self.Keuze_Antwoord   = {}
    self.Rapport_Antwoord = {}
    self.Answer_Image     = {}
    for i in range ( keuze_antwoorden_maxn ) :
      if not ( i in self.Keuze_Antwoord ) :
        self.Keuze_Antwoord [i] = ''
        self.Rapport_Antwoord [i] = ''
        #print 'Create',type(self.Keuze_Antwoord [i])
      for ii in range ( max_regels_per_keuze ) :
        line = self.Ini.Read_String ( 'Antwoord_' + str(i+1) + '/' + str(ii+1), '');
        #convert_from_inifile_compatible(line);
        if isinstance ( line, list ) :
          line = ','.join ( line )
        #print 'Create',type(self.Keuze_Antwoord [i]),type(line),indx,i,ii,line
        self.Keuze_Antwoord [i] += line + '\n'

        line = self.Ini.Read_String ( 'Rapport_' + str(i+1) + '/' + str(ii+1), '');
        #convert_from_inifile_compatible(line);
        if isinstance ( line, list ) :
          line = ','.join ( line )
        #print 'Create',type(self.Keuze_Antwoord [i]),type(line),indx,i,ii,line
        self.Rapport_Antwoord [i] += line + '\n'

        self.Answer_Image [i] = self.Ini.Read_String ( 'Image_' + str(i+1), '' )

      self.Keuze_Antwoord [i] = self.Keuze_Antwoord [i].rstrip ()
      self.Rapport_Antwoord [i] = self.Rapport_Antwoord [i].rstrip ()

      # Add to Attribs for database generation
      key = 'Keuze_Antwoord_'   + str(i)
      self.Attribs [ key ] = [ str, '', True ]
      # and add a reference with the same name to the array element
      setattr ( self, key, self.Keuze_Antwoord [i] )

      # also for rapport antwoord
      key = 'Rapport_Antwoord_'   + str(i)
      self.Attribs [ key ] = [ str, '', True ]
      setattr ( self, key, self.Rapport_Antwoord [i] )

    # kolom teksten alleen opbergen als niet leeg,
    # er mogen tussenliggende antwoorden ontbreken
    self.Column_Text      = {}
    for i in range ( 1, verzamel_max_antwoorden + 1 ) :
      line = 'Kolom_' + str(i)
      self.Column_Text [i] = self.Ini.Read_String ( line,'');
      self.Attribs [ line ] = [ str, '', False ]
      setattr ( self, line, self.Column_Text[i] )

    # Subschalen voor deze vraag
    self.SubSchalen = {}
    for SPSS in self.Vragenlijst.SPSS_FullName :
      self.SubSchalen [ SPSS ] = t_Vraag_SubSchaal ( self, SPSS )

    """
    # Element nul wordt gebruikt als default voor alle antwoorden
    for SV in range ( self.Aantal_SubVragen + 1 ) :
      print 'Vraag / SubVraag', self.Indx, SV
      for SPSS in self.Vragenlijst.SPSS_FullName :
        line = str(SV) + '_' + SPSS
        #print '****^^^^****',line
        SubSchaal = self.Ini.Read_String ( line, None )
        if SubSchaal :
          #self.SubSchalen [ SV ].append ( SPSS + '=' + SubSchaal )
          self.SubSchalen [ SV ] [ SPSS ] = SubSchaal
          print ' SUBSCHAAL', SPSS, '=', SubSchaal
          #self.SubSchalen.append ( line + '=' + SubSchaal )
          # parse subschaal en opbergen
          #empty = parse_subschaal ( SubSchaal, a,b, ar )
          #if not empty :
          #  SubSchalen ...
          #print '*********** SUBSCHAAL', SubSchaal
    """
    """
1 sen=1 0
1 totaal=1 0
10 ago=1 0
10 totaal=1 0
2 som=1 0
2 totaal=1 0
          """
        
    # Overslaan
    self.Overslaan = keuze_antwoorden_maxn * [ '' ]
    for i in range ( keuze_antwoorden_maxn ) :
      line = '1/' +  str(i+1) + ' Skip'
      regel = self.Ini.Read_String ( line, '' )
      if regel :
        self.Overslaan [i] = line + '=' + regel




  def Print_Vraag ( self ) :
    self.Print ( 'Vraag : ' + str ( self.Indx ) )
    #print '  Default Antwoord =', self.Antwoord_Num1

    for A in self.Keuze_Antwoord :
      if self.Keuze_Antwoord [A] :
        line = '  Antw ' + str(A+1) + ' = ' + str ( self.Keuze_Antwoord [A] )
        line = line.replace ( '\n', '\r\n          ' )
        print line

    print ''
    for A in self.Rapport_Antwoord :
      if self.Rapport_Antwoord [A] :
        line = '  Antw Rapport' + str(A+1) + ' = ' + str ( self.Rapport_Antwoord [A] )
        line = line.replace ( '\n', '\r\n          ' )
        print line

    for i, CT in enumerate ( self.Column_Text ) :
      line = self.Column_Text [ CT ]
      if line :
        print '  kolom', CT, '=', line


    print '  Subschalen, aantal = '
    for SS in self.SubSchalen :
      print '    ' + SS

    print ''
    print '  Overslaan = ', self.Overslaan

    if self.Indx == 1 :
      Table_Def = self.Get_Table_Def ()
      v3print ( '\n----- SQL Table Definition -----' )
      for item in Table_Def :
        v3print ( ' ', item )

# ***********************************************************************



