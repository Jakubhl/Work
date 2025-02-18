@echo off
REM Get the directory where this batch file is located
set "scriptPath=%~dp0"

REM Optionally, remove the trailing backslash if needed
if "%scriptPath:~-1%"=="\" set "scriptPath=%scriptPath:~0,-1%"

REM Run the PowerShell command to add the exclusion
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Add-MpPreference -ExclusionPath '%scriptPath%'"

echo Already set exclusionpaths:

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Get-MpPreference | Select-Object -ExpandProperty ExclusionPath"

pause