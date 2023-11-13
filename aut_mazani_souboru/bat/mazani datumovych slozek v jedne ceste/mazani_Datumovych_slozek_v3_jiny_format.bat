@echo off
setlocal enabledelayedexpansion

REM Nastavte cestu ke slozkam, neprochazi subslozky a maze cely obsah slozek!
REM format nazvu slozek ke smazani musi byt xx.xx.xxxx, jinak jsou ignorovany (pr.: 01.01.2023)
set "targetFolder=T:\Kamery\Omron\St160"

REM Nastavte pocet dni, jak stare slozky (mysleno podle stari v nazvu slozky) maji byt smazany
set /a max_days=1000

rem promenna test v hodnote 1 (nebo cokoliv jineho) jen vypise do konzole (nutno spustit pres cmd), ktere soubory se chysta smazat.
rem Hondota test = 0 maze soubory a nevypisuje z duvodu uspory vykonu
set /a test = 1

REM ///////////////////////////////////////////////////////////////////////////////////
echo Working...

REM Get the current date
for /f "tokens=1-4 delims=/ " %%a in ('echo %date%') do (
  set "day=%%a"
  set "month=%%b"
  rem set "month=2"
  set "year=%%c"
)

set /a year = !year! -2000

REM Ensure two digits for day and month
rem if !day! lss 10 (
rem  set "day=0!day!"
rem )
rem if !month! lss 10 (
rem  set "month=0!month!"
rem )

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

REM Loop through the folders in the target directory
for /d %%i in ("%targetFolder%\*") do (
    REM Extract the date portion from the folder name
    set "folderName=%%~nxi"
    for /f "tokens=1-3 delims=." %%a in ('echo !folderName!') do (
        set "folderDate=%%c%%b%%a"
		set "folderDateFormated=!folderDate:~0,2!!folderDate:~3,2!!folderDate:~6,2!"
		rem echo folder date !folderDateFormated!
    )
    
    REM Check if the folder name matches the date format
    if "!!folderDateFormated!!" neq "" (
        REM Compare the folder date with the cutoff date
        if !folderDateFormated! lss !cutoffDate! (
			if !test! == 0 (
				rd /s /q "%%i"
			) else (
				echo Deleting folder: %%i
			)  
        )
    )
)
endlocal


