@echo off
setlocal enabledelayedexpansion

set "max_days=30"
REM Set the root folder to start cleaning from
set "RootFolder=D:\JHV\Kamery\mazani_test"
REM Set the number of files to keep in each folder
set "FilesToKeep=10"

REM ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
REM Calculate the cutoff date based on the max_days variable in the format YYYYMMDD
for /f "tokens=1-3 delims=/" %%a in ('echo %date%') do (
  set "year=%%c"
  set "month=%%a"
  set "day=%%b"
)

set /a "year -= %max_days%"
if %year% lss 0 (
  set /a "year += 1"
  set "month=12"
)
set "CutoffDate=%year%%month%%day%"
echo Working...

@echo off
setlocal enabledelayedexpansion

REM Process root folder
REM Count the number of files in the root folder
set "FileCount=0"
for %%F in ("%RootFolder%\*") do (
    set /a "FileCount+=1"
)

REM Calculate the number of files to delete in the root folder
set /a "FilesToDelete=!FileCount!-!FilesToKeep!"

REM Skip root folder if it has fewer files than FilesToKeep
if !FilesToDelete! lss 0 (
    echo Skipping root folder: %RootFolder% Less than !FilesToKeep! files
) else (
    echo Processing root folder: %RootFolder%

    REM Sort the files in the root folder by modification date in ascending order
    pushd "%RootFolder%"
    (for /f "tokens=1,* delims= " %%A in ('dir /a-d /b /o:d /tw') do (
        set "file=%%B"
        set /a "FilesToDelete-=1"
        if !FilesToDelete! geq 0 (
            if "%%A" neq "" (
                echo Deleting: "%%A"
                del "%%A" /q
            )
        )
    ))
    popd
)

REM Process second-level subfolders
for /d %%D in ("%RootFolder%\*") do (
    set "Subfolder=%%D"
    
    REM Count the number of files in the second-level subfolder
    set "FileCount=0"
    for %%F in ("!Subfolder!\*") do (
        set /a "FileCount+=1"
    )

    REM Calculate the number of files to delete in the second-level subfolder
    set /a "FilesToDelete=!FileCount!-!FilesToKeep!"

    REM Skip second-level subfolders with fewer files than FilesToKeep
    if !FilesToDelete! lss 0 (
        echo Skipping second-level subfolder: !Subfolder! Less than !FilesToKeep! files
    ) else (
        echo Processing second-level subfolder: !Subfolder!

        REM Sort the files in the second-level subfolder by modification date in ascending order
        pushd "!Subfolder!"
        (for /f "tokens=1,* delims= " %%A in ('dir /a-d /b /o:d /tw') do (
            set "file=%%B"
            set /a "FilesToDelete-=1"
            if !FilesToDelete! geq 0 (
                if "%%A" neq "" (
                    rem echo Deleting: "%%A"
                    del "%%A" /q
                )
            )
        ))
        popd
    )

    REM Process third-level subfolders
    for /d %%E in ("!Subfolder!\*") do (
        set "Subfolder=%%E"
        
        REM Count the number of files in the third-level subfolder
        set "FileCount=0"
        for %%F in ("!Subfolder!\*") do (
            set /a "FileCount+=1"
        )

        REM Calculate the number of files to delete in the third-level subfolder
        set /a "FilesToDelete=!FileCount!-!FilesToKeep!"

        REM Skip third-level subfolders with fewer files than FilesToKeep
        if !FilesToDelete! lss 0 (
            echo Skipping third-level subfolder: !Subfolder! Less than !FilesToKeep! files
        ) else (
            echo Processing third-level subfolder: !Subfolder!

            REM Sort the files in the third-level subfolder by modification date in ascending order
            pushd "!Subfolder!"
            (for /f "tokens=1,* delims= " %%A in ('dir /a-d /b /o:d /tw') do (
                set "file=%%B"
                set /a "FilesToDelete-=1"
                if !FilesToDelete! geq 0 (
                    if "%%A" neq "" (
                        rem echo Deleting: "%%A"
                        del "%%A" /q
                    )
                )
            ))
            popd
        )
		REM Process fourth-level subfolders
		for /d %%G in ("!Subfolder!\*") do (
			set "Subfolder=%%G"
			
			REM Count the number of files in the fourth-level subfolder
			set "FileCount=0"
			for %%F in ("!Subfolder!\*") do (
				set /a "FileCount+=1"
			)

			REM Calculate the number of files to delete in the fourth-level subfolder
			set /a "FilesToDelete=!FileCount!-!FilesToKeep!"

			REM Skip fourth-level subfolders with fewer files than FilesToKeep
			if !FilesToDelete! lss 0 (
				echo Skipping fourth-level subfolder: !Subfolder! Less than !FilesToKeep! files
			) else (
				echo Processing fourth-level subfolder: !Subfolder!

				REM Sort the files in the fourth-level subfolder by modification date in ascending order
				pushd "!Subfolder!"
				(for /f "tokens=1,* delims= " %%A in ('dir /a-d /b /o:d /tw') do (
					set "file=%%B"
					set /a "FilesToDelete-=1"
					if !FilesToDelete! geq 0 (
						if "%%A" neq "" (
							rem echo Deleting: "%%A"
							del "%%A" /q
						)
					)
				))
				popd
			)
		REM Process fifth-level subfolders
		for /d %%H in ("!Subfolder!\*") do (
			set "Subfolder=%%H"
			
			REM Count the number of files in the fifth-level subfolder
			set "FileCount=0"
			for %%F in ("!Subfolder!\*") do (
				set /a "FileCount+=1"
			)

			REM Calculate the number of files to delete in the fifth-level subfolder
			set /a "FilesToDelete=!FileCount!-!FilesToKeep!"

			REM Skip fifth-level subfolders with fewer files than FilesToKeep
			if !FilesToDelete! lss 0 (
				echo Skipping fifth-level subfolder: !Subfolder! Less than !FilesToKeep! files
			) else (
				echo Processing fifth-level subfolder: !Subfolder!

				REM Sort the files in the fifth-level subfolder by modification date in ascending order
				pushd "!Subfolder!"
				(for /f "tokens=1,* delims= " %%A in ('dir /a-d /b /o:d /tw') do (
					set "file=%%B"
					set /a "FilesToDelete-=1"
					if !FilesToDelete! geq 0 (
						if "%%A" neq "" (
							rem echo Deleting: "%%A"
							del "%%A" /q
						)
					)
				))
				popd
			)
		)
    )
	)
)

REM Output final progress message
echo Completed: Processed all folders in folder %RootFolder%

endlocal

