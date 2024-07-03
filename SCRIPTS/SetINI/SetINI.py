program SetINI;

{$APPTYPE CONSOLE}

{$R *.res}

uses
  SysUtils,
  IniFiles;

var
    GIniFileName: string;
    GINIFile: TINIFile;
    GSection: string;
    GParameter: string;
    GValue: string;

begin
    { ParamStr(1) - <>.ini  }
    { ParamStr(2) - <group> }
    { ParamStr(3) - <parameter> }
    { ParamStr(4) - <value> }
    if not (ParamCount in [3..4]) then begin
        WriteLN('SETINI: setini <ini_file> <group> <parameter> <value>');
        end
    else begin
        GINIFileName := SysUtils.ExpandFileName(Paramstr(1));
        GSection := ParamStr(2);
        GParameter := ParamStr(3);
        GValue := ParamStr(4);
        if not FileExists(GINIFileName) then begin
            WriteLN('SETINI: ini_file '+GINIFileName+' not found.');
            end
        else begin
            GINIFile := TINIFile.Create(GINIFileName);
            GINIFile.WriteString(GSection, GParameter, GValue);
            GIniFile.Free;
        end;
    end;
end.
