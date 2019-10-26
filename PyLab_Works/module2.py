VM = {}
exec ("print 'aap'", VM)
for item in VM :
  if item != '__builtins__':
    print item