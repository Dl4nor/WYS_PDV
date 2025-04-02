[Setup]
AppName=WYS PDV
AppVersion=1.0
DefaultDirName={commonpf}\WYS PDV
DefaultGroupName=WYS PDV
OutputDir=.\install
OutputBaseFilename=WYS_PDV_Setup
SetupIconFile=app\assets\icons\wys_real.ico
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: desktopicon; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\WYS_PDV.exe"; DestDir: "{app}\dist\"; DestName: "WYS_PDV.exe"; Flags: ignoreversion
Source: "dist\register_deep_link.exe"; DestDir: "{app}\dist\"; Flags: ignoreversion
Source: "build\main\*"; DestDir: "{app}\build\main\"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "app\assets\*"; DestDir: "{app}\assets\"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\WYS PDV"; Filename: "{app}\dist\WYS_PDV.exe"; IconFilename: "{app}\assets\icons\wys_real.ico"
Name: "{commondesktop}\WYS PDV"; Filename: "{app}\dist\WYS_PDV.exe"; Tasks: desktopicon; IconFilename: "{app}\assets\icons\wys_real.ico"

[Run]
Filename: "{app}\dist\register_deep_link.exe"; Parameters: """{app}"""; Description: "Registrando Deep Link"; Flags: runhidden

[UninstallDelete]
Type: filesandordirs; Name: "{localappdata}\WYS_PDV"

[Registry]
Root: HKCU; Subkey: "SOFTWARE\Classes\wyspdv"; Flags: uninsdeletekey

