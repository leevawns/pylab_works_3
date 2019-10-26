from winsys import fs

ROOT = "c:/temp"
#
# For purposes of illustration, just show directories
#
for directory, dirs, files in fs.walk (ROOT):
 dirpath = directory.filepath.relative_to (ROOT)
 indent = "  " * dirpath.count (fs.sep)
 print indent, dirpath
 security = directory.security ()
 for dace in directory.security ().dacl:
   print indent, dace
 print
