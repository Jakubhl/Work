@echo off
setlocal enabledelayedexpansion
set disk = D:
set dump_path=D:\JHV\Kamery\mazani_test2

set max_days=30
set number_of_files=5



for /d %%H in (*) do (
	echo %%~fH

	set path_with_files = "%%~fH"
	rem echo %path_with_files%
	
	REM for /f %%A in ('dir ^| find "File(s)"') do set cnt=%%A
	rem dir /a:-d /s /b %%~fD | find /c ":\" > tempFile.txt
	rem SET /p FilesCount=<tempFile.txt
	rem forfiles -p %path_with_files% /f %%A in ('dir *.ifz ^| find "File(s)"') /c "cmd /c set cnt=%%A /q @path"
	rem for %%a in (%%~fD+"/") do set /A cnt+=1
		
	SET cnt=0
	FOR /f "tokens=*" %%G IN ('dir %%~fH /b') DO (call :subroutine "%%G")
	rem GOTO :eof
	

	:subroutine
	echo %cnt%:%1
	set /a cnt+=1
	set file_to_rem = %%~fH and %1
	
	rem preskoci to par souboru v dane slozce, az potom zacne mazat
	
    if %cnt% gtr %number_of_files% echo vice
		echo ahojda
		rem forfiles -p %%~fD -s -m * -d -%max_days% -c "cmd /c del /q @path"
		rem )

	rem echo File count = %cnt%

)
GOTO :eof
	




REM forfiles -p %dump_path% -s -m * -d -%max_days% -c "cmd /c del /q @path" do set /a cnt-=1
REM forfiles /S /P %dump_path%  /D -%max_days% /C "cmd /C IF @isdir == TRUE rd /S /Q @path"