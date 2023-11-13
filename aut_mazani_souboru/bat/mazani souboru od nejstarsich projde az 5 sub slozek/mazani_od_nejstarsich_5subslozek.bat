@echo off
setlocal enabledelayedexpansion

rem nastavte cestu k zakladni slozce obsahujici subslozky, projde az 5 subslozek v zadane ceste
set "RootFolder=C:\Users\kubah\Desktop\JHV\mazani_test"

rem nastavte pocet ponechanych souboru v kazde subslozce, maze se od nejstarsich
set "FilesToKeep=1000"

rem promenna test v hodnote 1 (nebo cokoliv jineho) jen vypise do konzole (nutno spustit pres cmd), ktere soubory se chysta smazat.
rem Hondota test = 0 maze soubory a nevypisuje z duvodu uspory vykonu
set /a test = 1

REM ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

echo Working...

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
				if !test! == 0 (
					del "%%A" /q
				) else (
					echo Deleting: "%%A"
				)
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
                    if !test! == 0 (
						del "%%A" /q
					) else (
						echo Deleting: "%%A"
					)
                )
            )
        ))
        popd
    )

    REM Process third-level subfolders
    for /d %%E in ("!Subfolder!\*") do (
        set "Subfolder2=%%E"
        
        REM Count the number of files in the third-level subfolder
        set "FileCount=0"
        for %%F in ("!Subfolder2!\*") do (
            set /a "FileCount+=1"
        )

        REM Calculate the number of files to delete in the third-level subfolder
        set /a "FilesToDelete=!FileCount!-!FilesToKeep!"

        REM Skip third-level subfolders with fewer files than FilesToKeep
        if !FilesToDelete! lss 0 (
            echo Skipping third-level subfolder: !Subfolder2! Less than !FilesToKeep! files
        ) else (
            echo Processing third-level subfolder: !Subfolder2!

            REM Sort the files in the third-level subfolder by modification date in ascending order
            pushd "!Subfolder2!"
            (for /f "tokens=1,* delims= " %%A in ('dir /a-d /b /o:d /tw') do (
                set "file=%%B"
                set /a "FilesToDelete-=1"
                if !FilesToDelete! geq 0 (
                    if "%%A" neq "" (
                        if !test! == 0 (
							del "%%A" /q
						) else (
							echo Deleting: "%%A"
						)
                    )
                )
            ))
            popd
        )
		REM Process fourth-level subfolders
		for /d %%G in ("!Subfolder2!\*") do (
			set "Subfolder3=%%G"
			
			REM Count the number of files in the fourth-level subfolder
			set "FileCount=0"
			for %%F in ("!Subfolder3!\*") do (
				set /a "FileCount+=1"
			)

			REM Calculate the number of files to delete in the fourth-level subfolder
			set /a "FilesToDelete=!FileCount!-!FilesToKeep!"

			REM Skip fourth-level subfolders with fewer files than FilesToKeep
			if !FilesToDelete! lss 0 (
				echo Skipping fourth-level subfolder: !Subfolder3! Less than !FilesToKeep! files
			) else (
				echo Processing fourth-level subfolder: !Subfolder3!

				REM Sort the files in the fourth-level subfolder by modification date in ascending order
				pushd "!Subfolder3!"
				(for /f "tokens=1,* delims= " %%A in ('dir /a-d /b /o:d /tw') do (
					set "file=%%B"
					set /a "FilesToDelete-=1"
					if !FilesToDelete! geq 0 (
						if "%%A" neq "" (
							if !test! == 0 (
								del "%%A" /q
							) else (
								echo Deleting: "%%A"
							)
						)
					)
				))
				popd
			)
		REM Process fifth-level subfolders
		for /d %%H in ("!Subfolder3!\*") do (
			set "Subfolder4=%%H"
			
			REM Count the number of files in the fifth-level subfolder
			set "FileCount=0"
			for %%F in ("!Subfolder4!\*") do (
				set /a "FileCount+=1"
			)

			REM Calculate the number of files to delete in the fifth-level subfolder
			set /a "FilesToDelete=!FileCount!-!FilesToKeep!"

			REM Skip fifth-level subfolders with fewer files than FilesToKeep
			if !FilesToDelete! lss 0 (
				echo Skipping fifth-level subfolder: !Subfolder4! Less than !FilesToKeep! files
			) else (
				echo Processing fifth-level subfolder: !Subfolder4!

				REM Sort the files in the fifth-level subfolder by modification date in ascending order
				pushd "!Subfolder4!"
				(for /f "tokens=1,* delims= " %%A in ('dir /a-d /b /o:d /tw') do (
					set "file=%%B"
					set /a "FilesToDelete-=1"
					if !FilesToDelete! geq 0 (
						if "%%A" neq "" (
							if !test! == 0 (
								del "%%A" /q
							) else (
								echo Deleting: "%%A"
							)
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


