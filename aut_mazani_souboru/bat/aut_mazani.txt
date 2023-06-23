@echo off

set dump_path=D:\JHV\Kamery\Work\aut_mazani_souboru\mazani_test

set max_days=30

forfiles -p %dump_path% -s -m * -d -%max_days% -c "cmd /c del /q @path"
forfiles /S /P %dump_path%  /D -%max_days% /C "cmd /C IF @isdir == TRUE rd /S /Q @path"