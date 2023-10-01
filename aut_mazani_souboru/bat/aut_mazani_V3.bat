@echo off
setlocal enabledelayedexpansion

set "dump_path=D:\JHV\Kamery\mazani_test4"
set "RootFolder=D:\JHV\Kamery\mazani_test4"
set "max_days=30"
set number_of_files=5

set "FileCount=0"
set "FolderCount=0"

for /d /r "%RootFolder%" %%A in (*) do (
	set counter=0
	set FileCount=0
	set /a FolderCount+=1
	rem echo %%A
	echo folder count: !FolderCount!
	
	call :SUB %%A
)
goto :eof

:SUB

for /r %1 %%F in (*) do (
set /a FileCount+=1
rem if !FileCount! gtr %number_of_files% del %%F

rem if !FileCount! gtr %number_of_files% (
	
	rem wmic DATAFILE where Name="%%F" list /format:list
	rem for %%H in (%Filename%) get FileDate


)
echo %1
echo file count: !FileCount!

rem forfiles -p %1 -s -m * -d -%max_days% -c "cmd /c if not !counter! gtr %number_of_files% set /a counter+=1"
rem forfiles -p %1 -s -m * -d -%max_days% -c "cmd /c if !counter! gtr %number_of_files% echo "ok""
forfiles -p %1 -s -m * -d -%max_days% -c ^"cmd /c ^
set /a !counter!=!counter!+1^
&echo coussnter !counter!^"



	
	
endlocal



REM forfiles -p %dump_path% -s -m * -d -%max_days% -c "cmd /c del /q @path"
REM forfiles /S /P %dump_path%  /D -%max_days% /C "cmd /C IF @isdir == TRUE rd /S /Q @path"