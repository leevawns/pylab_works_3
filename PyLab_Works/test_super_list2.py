
import copy




# ***********************************************************************
#
# You can add new attributes, without declaring them first, like
#   a = s_list ( [3,4] )
#   a.Some_New_Attribute = True
#
# ***********************************************************************
class s_list(list):

  # *********************************************************
  # *********************************************************
  def __init__ ( self, value = [] ) :
    # create the orginal list
    list.__init__ ( self, value )

    # create some default values
    self.Fixed_Color = 345

class s_list2(list):

  # *********************************************************
  # *********************************************************
  def __init__ ( self, *args ) :
    # create the orginal list
    list.__init__ ( self, args )

    # create some default values
    self.Fixed_Color = 345



  """
  # *********************************************************
  # always called instead of the normal mechanism
  # *********************************************************
  def __setattr__ ( self, attr, value ) :
    if   attr == 'x' :
      self._XY_Org [0] = value
    elif attr == 'y' :
      self._XY_Org [1] = value
    else :
      self.__dict__[attr] = value

  # *********************************************************
  # only called when not found with the normal mechanism
  # *********************************************************
  def __getattr__ ( self, attr ) :
    if   attr == 'x' :
      return self._XY_Org [0]
    elif attr == 'y' :
      return self._XY_Org [1]
    else :
      if not ( self.__dict__.has_key ( attr ) ) :
        self.__dict__[attr] = 0
      return self.__dict__[attr]
  """
# ***********************************************************************



    
b = [1,2]
a = s_list(b)
print 's_list',a
print 'dict',a.__dict__

a = s_list ( [3,4] )
a.append (5)
a.fixed_columns = True
print 's_list',a
print 'dict',a.__dict__

if isinstance ( a, s_list ) :
  print 'Yes', a.Fixed_Color
else : print 'NO'

if isinstance ( b, s_list ) :
  print 'Yes', b.Fixed_Color
else : print 'NO'


a = s_list2 ( 3,4,6 )
a.append (5)
a.fixed_columns = True
print 's_list2',a
print 'dict',a.__dict__

a = s_list2 ()
a.append (5)
a.fixed_columns = True
print 's_list2',a
print 'dict',a.__dict__

