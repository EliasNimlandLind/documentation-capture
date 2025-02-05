[Setup]
AppName=Documentation Capture
AppVersion=1.0
UsePreviousAppDir=no
DefaultDirName={pf64}\Documentation Capture  
DefaultGroupName=Documentation Capture
OutputBaseFilename=Documentation Capture Setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "src\documentation-capture\__init__.py"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Documentation Capture"; Filename: "{app}\DocumentationCapture.exe"
Name: "{commondesktop}\Documentation Capture"; Filename: "{app}\DocumentationCapture.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons"; Flags: unchecked

[Code]
var
  DirectoryPage, ArrowPage: TInputQueryWizardPage;
  ConfigFilePath: string;

procedure InitializeWizard;
begin
  DirectoryPage := CreateInputQueryPage(wpSelectDir,
    'Directory Configuration', 'Please enter the directory values below:',
    '');
  DirectoryPage.Add('Output directory, e.g., "screenshots/%%Y-%%m-%%d":', False);
  DirectoryPage.Values[0] := 'screenshots/%%Y-%%m-%%d';

  ArrowPage := CreateInputQueryPage(DirectoryPage.ID,
    'Arrow Configuration', 'Please enter the arrow properties:',
    '');
  ArrowPage.Add('Arrow length, e.g., 15:', False);
  ArrowPage.Add('Arrow width, e.g., 3:', False);  
  ArrowPage.Values[0] := '15';  
  ArrowPage.Values[1] := '3';
end;

function IsPositiveInteger(Value: string): Boolean;
begin
  Result := (StrToIntDef(Value, -1) > 0);
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;

  if CurPageID = DirectoryPage.ID then
  begin
    if Trim(DirectoryPage.Values[0]) = '' then
    begin
      MsgBox('Output directory cannot be empty.', mbError, MB_OK);
      Result := False;
      Exit;
    end;
  end;

  if CurPageID = ArrowPage.ID then
  begin
    if not IsPositiveInteger(ArrowPage.Values[0]) then
    begin
      MsgBox('Arrow length must be a positive number.', mbError, MB_OK);
      Result := False;
      Exit;
    end;

    if not IsPositiveInteger(ArrowPage.Values[1]) then
    begin
      MsgBox('Arrow width must be a positive number.', mbError, MB_OK);
      Result := False;
      Exit;
    end;
  end;
end;

procedure CurStepChanged(CurrentStep: TSetupStep);
var
  ConfigText: string;
begin
  if CurrentStep = ssPostInstall then
  begin
    ConfigFilePath := ExpandConstant('{app}\config.ini');  // Uses the user's selected install directory

    // Prepare configuration content
    ConfigText :=
      '[paths]'#13#10 +
      'output_directory=' + DirectoryPage.Values[0] + #13#10 +
      ''#13#10 +  // Blank line for separation
      '[arrow_properties]'#13#10 +
      'arrow_length=' + ArrowPage.Values[0] + #13#10 +
      'arrow_width=' + ArrowPage.Values[1] + #13#10;

    SaveStringToFile(ConfigFilePath, ConfigText, False);
  end;
end;

[UninstallDelete]
Type: files; Name: "{app}\config.ini"
Type: files; Name: "{app}\temp\*.*"
Type: dirifempty; Name: "{app}\temp"
