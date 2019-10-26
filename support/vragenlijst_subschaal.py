from db_support            import *

# ***********************************************************************
# ***********************************************************************
class t_Vragenlijst_SubSchaal ( Ini_DB_Object ) :
  def __init__ ( self, parent, indx ) :
    Ini_DB_Object.__init__ ( self )
    self.ID_Column = 'VLSID'

    #                                type  default    NotNull   Primary Key
    self.Attribs = {}
    self.Attribs [ 'Name_'    ] = [ str, '' ,True  ]
    self.Attribs [ 'Afk__'    ] = [ str, '' ,False ]
    self.Attribs [ 'RelName_' ] = [ str, '' ,False ]
    self.Attribs [ 'RelNmin_' ] = [ str, '' ,False ]
    self.Attribs [ 'DiscA'    ] = [ str, '' ,False ]
    self.Attribs [ 'DiscB'    ] = [ str, '' ,False ]
    self.Attribs [ 'VrStA'    ] = [ str, '' ,False ]
    self.Attribs [ 'VrStB'    ] = [ str, '' ,False ]

    self.Ini        = parent.Ini
    self.Table_Name = '_VLS_'+ parent.Name
    #print '$$$$$$$$$$',self.Table_Name
    self.Indx       = indx

    post = str ( self.Indx + 1 )
    self.Read_Attribs ( 'SubSchalen', post )

  #**********************************************
  def Print_Vragenlijst_SubSchaal ( self ) :
    if self.Indx == 0 :
      v3print ( '\n----- SQL Table Definition SubSchalen-----' )
      for item in self.Get_Table_Def () :
        v3print ( ' ', item )

      print "\n  %-15s  %-10s  %-13s  %-13s  %-15s  %-15s" %(
        'Name', 'RelName',
        'Discipline_A',    'Discipline_B',
        'VraagStelling_A', 'VraagStelling_B' )

    print "  %-15s  %-10s  %-13s  %-13s  %-15s  %-15s" %(
        self.Name_, self.RelName_,
        self.DiscA, self.DiscB,
        self.VrStA, self.VrStB )

# ***********************************************************************
