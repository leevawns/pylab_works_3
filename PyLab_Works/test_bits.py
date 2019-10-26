
class MyRegClass ( int ) :
  def __init__ ( self, value ) :
    self.Value = value
  def __repr__ ( self ) :
    line = hex ( self.Value )
    line = line [:2] + line [2:].upper()
    return line
  __str__ = __repr__
  
shadow_register = MyRegClass(0xAA)

print shadow_register