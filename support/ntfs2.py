import os, sys
import win32api
import win32security
import ntsecuritycon as con


import fileperm
all_perms=fileperm.get_perms('\\\\umcfs03\\IDict$\\TO\\Ini_Files\\to.bat')
print all_perms
#{'\\Everyone': 2032127L, 'Domain\\fred': 1179817L, 'BUILTIN\\Users': 1179817L}



FILENAME = "temp.txt"
#os.remove (FILENAME)
FILENAME = "\\\\umcfs03\\IDict$\\TO\\Ini_Files\\to.bat"
FILENAME = "\\\\umcfs03\\IDict$\\TO\\CVSpoli\\Data\\patient"

def show_cacls (filename):
  print
  print
  for line in os.popen ("cacls %s" % filename).read ().splitlines ():
    print line

#
# Find the SIDs for Everyone, the Admin group and the current user
#
#everyone, domain, type = win32security.LookupAccountName ("", "Everyone")
#everyone, domain, type = win32security.LookupAccountName ("", "Iedereen")
#admins, domain, type = win32security.LookupAccountName ("", "Administrators")
#user, domain, type = win32security.LookupAccountName ("", win32api.GetUserName ())
#user, domain, type = win32security.LookupAccountName ("", win32api.GetUserName () )
user, domain, type = win32security.LookupAccountName ("", "z482110" )

#
# Touch the file and use CACLS to show its default permissions
# (which will probably be: Admins->Full; Owner->Full; Everyone->Read)
#
#open (FILENAME, "w").close ()
show_cacls (FILENAME)

FILENAME = "\\\\umcfs03\\IDict$\\TO\\CVSpoli\\Data"
show_cacls (FILENAME)

"""
\\umcfs03\IDict$\TO\CVSpoli\Data\patient UMCN\GG ID TObeheer CVSpoli:(OI)(CI)C
                                         UMCN\GG ID TObeheerders:(OI)(CI)C
                                         UMCN\GG ID TObeheer Gebruikers:(CI)R
                                         UMCN\OU Beheerders Instrumentele Dienst:(OI)(CI)F
                                         INGEBOUWD\Administrators:(OI)(CI)F
                                         UMCN\z571117:F
                                         MAKER EIGENAAR:(OI)(CI)(IO)F
                                         NT AUTHORITY\SYSTEM:(OI)(CI)F



\\umcfs03\IDict$\TO\CVSpoli\Data UMCN\GG ID TObeheer CVSpoli:(OI)(CI)C
                                 UMCN\GG ID TObeheerders:(OI)(CI)C
                                 UMCN\GG ID TObeheer Gebruikers:(CI)R
                                 UMCN\OU Beheerders Instrumentele Dienst:(OI)(CI)F
                                 INGEBOUWD\Administrators:(OI)(CI)F
                                 UMCN\manID02:F
                                 MAKER EIGENAAR:(OI)(CI)(IO)F
                                 NT AUTHORITY\SYSTEM:(OI)(CI)F

"""

#
# Find the DACL part of the Security Descriptor for the file
#
sd = win32security.GetFileSecurity (FILENAME, win32security.DACL_SECURITY_INFORMATION)

#
# Create a blank DACL and add the three ACEs we want
# We will completely replace the original DACL with
# this. Obviously you might want to alter the original
# instead.
#
"""
dacl = win32security.ACL ()
dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.FILE_GENERIC_READ, everyone)
dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.FILE_GENERIC_READ | con.FILE_GENERIC_WRITE, user)
dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.FILE_ALL_ACCESS, admins)

#
# Put our new DACL into the Security Descriptor,
# update the file with the updated SD, and use
# CACLS to show what's what.
#
sd.SetSecurityDescriptorDacl (1, dacl, 0)
win32security.SetFileSecurity (FILENAME, win32security.DACL_SECURITY_INFORMATION, sd)
show_cacls (FILENAME)
"""