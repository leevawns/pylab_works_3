

# ***********************************************************************
# ***********************************************************************
def Read_VraagList_Answers ( filename ) :
  fh = open ( filename, 'r')
  lines = fh.readlines ()
  fh.close ()
  i = 1
  VTs = []
  Section = False
  for line in lines :
    if not Section :
      if line.startswith ( '~' + str ( i )) :
        Section = True
    else :
      if not ( line.startswith ( '~' ) ) :
        VTs.append ( line.strip() )
        Section = False
      else :
        VTs.append ( '' )
      i += 1
  if Section :
    VTs.append ( '' )
  return VTs
# ***********************************************************************

