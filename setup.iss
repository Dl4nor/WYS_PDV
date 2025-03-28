[Setup]
AppName=WYS PDV
AppVersion=1.0
DefaultDirName={pf}\WYS PDV
DefaultGroupName=WYS PDV
OutputDir=.\install
OutputBaseFilename=WYS_PDV_Setup
SetupIconFile=app\assets\icons\wys_real.ico
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: desktopicon; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "build\exe.win-amd64-3.12\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\register_deep_link.exe"; DestDir: "{app}\register_deep_link\"; Flags: ignoreversion

[Icons]
Name: "{group}\WYS PDV"; Filename: "{app}\WYS PDV.exe"; IconFilename: "{app}\assets\icons\wys_real.ico"
Name: "{commondesktop}\WYS PDV"; Filename: "{app}\WYS PDV.exe"; Tasks: desktopicon; IconFilename: "{app}\assets\icons\wys_real.ico"

[Run]
Filename: "{app}\register_deep_link\register_deep_link.exe"; Parameters: "{app}"; Description: "Registrando Deep Link"; Flags: runhidden