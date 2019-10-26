$Title = "VPython"
$VP = WinGetPos($Title)
For $i = 1 to 5 
  $VP = WinGetPos($Title)
  WinMove($Title,"",$VP[0]+10,$VP[1])
  Sleep(500)
  Next
  
  ;SetParent
