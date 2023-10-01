@echo off
setlocal enabledelayedexpansion

set "max_days=30"
REM Set the root folder to start cleaning from
set "RootFolder=D:\JHV\Kamery\mazani_test4"
REM Set the number of files to keep in each folder
REM keep it -1
set "FilesToKeep=4"



REM Calculate the cutoff date 30 days ago in the format YYYYMMDD
for /f "usebackq delims=" %%A in (`powershell -Command "(Get-Date).AddDays(-%max_days%).ToString('yyyyMMdd')"`) do set "CutoffDate=%%A"

REM Loop through all files in the root folder and its subfolders
for /r "%RootFolder%" %%F in (*) do (
    set "File=%%F"
    
    REM Get the creation date of the file
    for /f "tokens=2 delims==" %%D in ('wmic datafile where "name='!File:\=\\!'" get creationdate /format:list ^| findstr "="') do set "CreationDate=%%D"
    set "CreationDate=!CreationDate:~0,8!"
    
    REM Check if CreationDate is empty (no instances available), continue to next file
    if "!CreationDate!" == "" (
        continue
    )
    
    if !CreationDate! lss !CutoffDate! (
        set "FolderName=%%~dpF"
        set "FolderName=!FolderName:~0,-1!"
        set "FolderName=!FolderName:\=\\!"
        
        REM Count the number of files in the folder
        set "FileCount=0"
        for %%G in ("!FolderName!\*") do (
            set /a "FileCount+=1"
        )
        
        REM Check if there are more than FilesToKeep files in the folder
        if !FileCount! gtr !FilesToKeep! (
            REM Sort the files in the folder by creation date in ascending order
            pushd "!FolderName!"
            (for /f "tokens=1,* delims= " %%A in ('dir /a-d /b /od /tc') do (
                set "file=%%B"
                set /a "FileCount-=1"
                if !FileCount! gtr !FilesToKeep! (
                    if "%%A" neq "" (
                        echo Deleting: "%%A"
                        del "%%A" /q
                    )
                )
            ))
            popd
        )
    )
)

endlocal
