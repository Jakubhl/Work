@echo off

set dump_path=D:\JHV\Kamery\Work\aut_mazani_souboru\mazani_test

set max_days=30

forfiles -p %dump_path% -s -m * -d -%max_days% -c "cmd /c del /q @path"
forfiles -p %dump_path% -s -m * -d -%max_days% -c "cmd /c rmdir /s /q @path"