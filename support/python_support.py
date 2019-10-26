import __init__

# ***********************************************************************
# License: freeware, under the terms of the BSD-license
# Copyright (C) 2007..2008 Stef Mientki
# mailto:S.Mientki@ru.nl
# ***********************************************************************

# ***********************************************************************
__doc__ = """
"""
# ***********************************************************************


# ***********************************************************************
_Version_Text = [

[ 1.0 , '07-11-2008', 'Stef Mientki',
'Test Conditions:', (1,),
' - orginal release' ]
]
# ***********************************************************************




from General_Globals import *

# ***********************************************************************
# ***********************************************************************
def Get_Python_Objects ():
    import gc

    # Recursively expand slist's objects
    # into olist, using seen to track
    # already processed objects.
    def _getr(slist, olist, seen):
      for e in slist:
        if id(e) in seen:
          continue
        seen[id(e)] = None
        olist.append(e)
        tl = gc.get_referents(e)
        if tl:
          _getr(tl, olist, seen)

    """Return a list of all live Python
    objects, not including the list itself."""
    gcl = gc.get_objects()
    olist = []
    seen = {}
    # Just in case:
    seen[id(gcl)] = None
    seen[id(olist)] = None
    seen[id(seen)] = None
    # _getr does the real work.
    _getr(gcl, olist, seen)
    return olist
# ***********************************************************************



# ***********************************************************************
# ***********************************************************************
if __name__ == "__main__":

  Test_Defs ( 1, 2 )

  # ************************************
  # ************************************
  if Test ( 1 ) :
    Objects = Get_Python_Objects ()
    for i in range ( 10 ) :
      print Objects [i]


  # ************************************
  # DOESN"T WORK ??
  # ************************************
  if Test ( 2 ) :
    import sys, traceback
    try:
        raise ValueError
    except ValueError:
        start = traceback.extract_tb(sys.exc_info()[2])[-1]
    print 'Started from', start

# ***********************************************************************
pd_Module ( __file__ )

