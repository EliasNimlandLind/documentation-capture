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
Source: "dist\__init__.exe"; DestDir: "{app}"; DestName: "documentation-capture-application.exe"; Flags: ignoreversion

[Icons]
Name: "{group}\Documentation Capture"; Filename: "{app}\DocumentationCapture.exe"
Name: "{commondesktop}\Documentation Capture"; Filename: "{app}\DocumentationCapture.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons"; Flags: unchecked

[Code]
var
  DirectoryPage, ArrowPage, TextBoxPage, KeybindingsPage: TInputQueryWizardPage;
  ConfigFilePath: string;

procedure InitializeWizard;
begin
  DirectoryPage := CreateInputQueryPage(wpSelectDir,
    'Directory configuration', 'Please enter the directory properties below:',
    '');
  DirectoryPage.Add('Output directory:', False);
  DirectoryPage.Values[0] := 'screenshots/%%Y-%%m-%%d';

  ArrowPage := CreateInputQueryPage(DirectoryPage.ID,
    'Arrow configuration', 'Please enter the arrow properties below:',
    '');
  ArrowPage.Add('Arrow length:', False);
  ArrowPage.Add('Arrow width:', False); 
  ArrowPage.Add('Arrow color:', False);
  ArrowPage.Values[0] := '15';  
  ArrowPage.Values[1] := '3'; 
  ArrowPage.Values[2] := 'FF0000'; 

  TextBoxPage := CreateInputQueryPage(DirectoryPage.ID,
    'Text box configuration', 'Please enter the text box properties below:',
    '');
  TextBoxPage.Add('Text box height:', False);  
  TextBoxPage.Add('Text box color:', False);
  TextBoxPage.Values[0] := '200';   
  TextBoxPage.Values[1] := 'FFFFFF';  
  
  KeybindingsPage := CreateInputQueryPage(DirectoryPage.ID,
    'Keybindings configuration', 'Please enter the keybindings below:',
    '');
  KeybindingsPage.Add('Secondary screenshot capture key:', False);  
  KeybindingsPage.Add('Termination key:', False);
  KeybindingsPage.Values[0] := 'ctrl_1';   
  KeybindingsPage.Values[1] := 'esc'; 
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
  
 if CurPageID = TextBoxPage.ID then
  begin
    if not IsPositiveInteger(TextBoxPage.Values[0]) then
    begin
      MsgBox('Text box height must be a positive number.', mbError, MB_OK);
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
    // Blank line for separation
    ConfigText := 
      '[directories]' + #13#10 +
      'output=' + DirectoryPage.Values[0] + #13#10 +
      ''#13#10 +  
      '[arrow]' + #13#10 +
      'length=' + ArrowPage.Values[0] + #13#10 +
      'width=' + ArrowPage.Values[1] + #13#10 + 
      'color=' + ArrowPage.Values[2] + #13#10 + 
      ''#13#10 +  
      '[text_box]' + #13#10 + 
      'height=' + TextBoxPage.Values[0] + #13#10 +
      'color=' + TextBoxPage.Values[1] + #13#10 + 
      ''#13#10 +  
      '[keybindings]' + #13#10 + 
      'secondary_screenshot_capture_key=' + KeybindingsPage.Values[0] + #13#10 +
      'termination_key=' + KeybindingsPage.Values[1];
    SaveStringToFile(ConfigFilePath, ConfigText, False);
  end;
end;

[UninstallDelete]
Type: files; Name: "{app}\config.ini"
Type: files; Name: "{app}\temp\*.*"
Type: dirifempty; Name: "{app}\temp"
