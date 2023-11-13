@echo off
setlocal enabledelayedexpansion

Rem nastavte cestu, nezpracovava subfoldery
set "targetFolder=C:\Users\kubah\Desktop\JHV\mazani_test\1.9.2023"

REM Nastavte, kolik dni stare soubory chcete ponechat
set /a max_days=20

REM nastavte, kolik souboru, vyhodnocenych, jako starsi, si prejete ponechat
set /a files_to_keep=1000

rem promenna test v hodnote 1 (nebo cokoliv jineho) jen vypise do konzole (nutno spustit pres cmd), ktere soubory se chysta smazat.
rem Hondota test = 0 maze soubory a nevypisuje z duvodu uspory vykonu
set /a test = 1

REM ///////////////////////////////////////////////////////////////////////////////////
echo Working...

REM Get the current date
for /f "tokens=1-4 delims=/ " %%a in ('echo %date%') do (
  set "day=%%c"
  set "month=%%b"
  rem set "month=2"
  set "year=%%d"
)

REM Ensure two digits for day and month
if !day! lss 10 (
  set "day=0!day!"
)
if !month! lss 10 (
  set "month=0!month!"
)

REM Reorder the date format to DDMMYYYY
set "currentdate=!year!!month!!day!"
echo Current Date: !currentdate!

set /a cutoffDays =!day!-!max_days! + 1


rem calculate the cutoff date
:calccutoff
if !month! == 2 (
	set /a daysinmonth=28
) else if !month! == 4 (
	set /a daysinmonth=30
) else if !month! == 6 (
	set /a daysinmonth=30
) else if !month! == 9 (
	set /a daysinmonth=30
) else if !month! == 11 (
	set /a daysinmonth=30
) else (
	set /a daysinmonth=31
)

if !cutoffDays! lss 1 (
	set /a cutoffDays = !cutoffDays! + !daysinmonth!
	if !month! == 1 (
		set /a month = 12
		set /a year = !year! - 1
	) else (
		set /a month = !month! - 1
	)
)
goto :back

rem repeat if cutoffday is still lesser then zero
:back
if !cutoffDays! lss 1 (
	goto :calccutoff
) else (
	goto :back2
)


:back2
rem repair the format
if !day! lss 10 (
  set "day=0!day!"
)
if !month! lss 10 (
  set "month=0!month!"
)
if !cutoffDays! lss 10 (
  set "cutoffDays=0!cutoffDays!"
)

set /a cutoffDate = !year!!month!!cutoffDays!
echo Cutoff date: !cutoffDate!

set /a oldfilescount = 0
REM Loop through the files in the target directory
for %%F in ("%targetFolder%\*.*") do (
    REM Get the date modified of the file
    for %%a in ("%%F") do set "fileModifiedDate=%%~ta"
    REM Format the date in YYYYMMDD format
    set "fileDate=!fileModifiedDate:~6,4!!fileModifiedDate:~0,2!!fileModifiedDate:~3,2!"
	
    REM Check if the file date matches the cutoff date
    if "!fileDate!" lss "!cutoffDate!" (
		set /a oldfilescount = !oldfilescount! + 1
		
        if !oldfilescount! gtr !files_to_keep! (
			if !test! == 0 (
				del "%%F"
			) else (
				echo Deleting file: %%F
			)
		) 
    )
)
endlocal


