; General Setup file
#define public base     "D:\Data_Python\"
#define public website  "http://pic.flappie.nl/"


; Flexible Part *********************************************************
#define public destination  "C:\Portable\"
#define public prog_path    "P24_Templates"
#define public application  "Scintilla_Templates"
#define public version      "v0_1"
; End Flexible Part *****************************************************


[Setup]
AppName={#application}
OutputDir = {#base}\Installs
OutputBaseFilename={#application}_{#version}
AppVerName={#application}  {#version}
AppCopyright=Copyright (C) 2007..2008 Stef Mientki
AppPublisher=Stef Mientki
AppPublisherURL={#website}
AppSupportURL={#website}
AppUpdatesURL={#website}
DefaultDirName={#destination}
DefaultGroupName={#application}
AllowNoIcons=yes
LicenseFile={#base}\Installs\License.txt
MinVersion=4,4.0


[Messages]
BeveledLabel={#application} ({#version})


; define the desktop shortcuts (which the end-user can select)
[Tasks]
Name: "desktopicon_Main"; \
  Description:      "Create a &desktop icon for Templates"; \
  GroupDescription: "Additional icons:"; MinVersion: 4,4


[Types]
Name: "full";   Description: "Full Installation"
Name: "custom"; Description: "Custom Installation"; Flags: iscustom


; define which components the end-user can (de-)select
[Components]
Name: "Program"; Description: "{#application} {#version}"; Flags: fixed; Types: full custom;


; which source files should be copied to which destination
[Files]
Source: "{#base}{#prog_path}\dist\*.*"; \
  DestDir: "{app}\{#prog_path}"; \
  Flags: ignoreversion recursesubdirs; \
  Components: Program;

; Icon file
Source: "{#base}\{#prog_path}\*.ico"; \
  DestDir: "{app}\{#prog_path}"; \
  Flags: ignoreversion recursesubdirs; \
  Components: Program;

; Images
Source: "{#base}\P24_pictures\*.*"; \
  DestDir: "{app}\P24_pictures\"; \
  Flags: ignoreversion recursesubdirs; \
  Components: Program;
  
[Icons]
; create desktop shortcuts for all users
Name: "{commondesktop}\{#application}"; \
  Filename: "{app}\{#prog_path}\{#application}.exe"; \
  WorkingDir: "{app}\{#prog_path}"; \
  Tasks: desktopicon_Main; \
  IconFilename: "{app}\{#prog_path}\{#application}.ico";

; create shortcut in start/programs for all users
Name: "{commonprograms}\{#application}"; \
  Filename: "{app}\{#prog_path}\{#application}.exe"; \
  WorkingDir: "{app}\{#prog_path}"; \
  IconFilename: "{app}\{#prog_path}\{#application}.ico";
  
[Run]
Filename: "{app}\{#prog_path}\{#application}.exe"; \
  Description: "Launch {#application}"; Flags: postinstall skipifsilent;











