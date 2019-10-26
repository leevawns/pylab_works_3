import os, sys
import win32api
import win32security
import ntsecuritycon as con

FILENAME = "temp.txt"
FILENAME = "\\\\umcfs03\\IDict$\\TO\\Ini_Files\\to.bat"
#FILENAME = "\\\\umcfs03\\IDict$\\TO\\Ini_Files"

#os.remove (FILENAME)

def show_cacls (filename):
  print
  for line in os.popen ("cacls %s" % filename).read ().splitlines ():
    print line

#
# Find the SIDs for Everyone, the Admin group and the current user
#
everyone, domain, type = win32security.LookupAccountName ("", "z571117")
print everyone, domain, type
everyone, domain, type = win32security.LookupAccountName ("", "z482110")
print everyone, domain, type
admins, domain, type = win32security.LookupAccountName ("", "Administrators")
user, domain, type = win32security.LookupAccountName ("", win32api.GetUserName ())

print admins, domain, type
print user, domain, type
#
# Touch the file and use CACLS to show its default permissions
# (which will probably be: Admins->Full; Owner->Full; Everyone->Read)
#
#open (FILENAME, "w").close ()
show_cacls (FILENAME)



#
# Find the DACL part of the Security Descriptor for the file
#
sd = win32security.GetFileSecurity (FILENAME, win32security.DACL_SECURITY_INFORMATION)
print dir(sd)
print sd.GetSecurityDescriptorGroup()
"""
for item in dir ( sd ) :
  print eval ( 'sd.' + item + '()' )
"""

#
# Create a blank DACL and add the three ACEs we want
# We will completely replace the original DACL with
# this. Obviously you might want to alter the original
# instead.
#
dacl = win32security.ACL ()
dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.FILE_GENERIC_READ, everyone)
dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.FILE_GENERIC_READ | con.FILE_GENERIC_WRITE, user)
dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.FILE_ALL_ACCESS, admins)

#"""
# Put our new DACL into the Security Descriptor,
# update the file with the updated SD, and use
# CACLS to show what's what.
#
sd.SetSecurityDescriptorDacl (1, dacl, 0)
win32security.SetFileSecurity (FILENAME, win32security.DACL_SECURITY_INFORMATION, sd)
show_cacls (FILENAME)
#"""
