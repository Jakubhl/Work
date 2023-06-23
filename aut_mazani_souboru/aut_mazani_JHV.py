import os
from pathlib import Path
import datetime
from datetime import datetime as datetime_
import time

def months_total(year_and_month):
    year = str(year_and_month)[:4]
    months = int(year)*12 + int(str(year_and_month)[5:7])
    return months

def get_day(day):
    day = str(day)
    day = day[8:10]
    #neresime vysokou presnost, +- 3 dny...
    if int(day) > 28:
        day = 28

    return int(day)


def refresh():
    with open('mazani_config.txt') as f:
        lines = [line.rstrip() for line in f]
 
    current_date = datetime.datetime.today()
    now = str(current_date)[:10]
    current_months = months_total(current_date)

    main_path = lines[2]
    folders_created = []
    
    if os.path.exists(main_path):
        for files in os.listdir(main_path):
            if os.path.isdir(main_path+"/"+files):
                path = Path(main_path+"/"+files)
                stat_result = path.stat()
                created = datetime_.fromtimestamp(stat_result.st_ctime)
                created = str(created)[:10]
                folders_created.append(files + ", "+created)
                
                created_in_months = months_total(created)
                day_when_delete = get_day(created)


                if current_months >= (created_in_months + int(lines[6])):
                    if get_day(current_date) == get_day(created):
                        print(f"mazu {files}...")
                    else:
                        if get_day(current_date) > get_day(created):
                            when = get_day(current_date) - get_day(created)
                            print(f"Slozka {files} bude odstranena za {when} dny/dní")


        if len(folders_created) != 0:
            print("_________________________________________________________________________________________________________________________\n"
            ,folders_created,"\n")

            if lines[6].isdigit():
                print("aktualni datum: "
                ,now," ,soubory staré: ",lines[6]," mesicu budou odstraneny...\n")
            else:
                print("Na sedmém řádku konfiguračního .txt souboru nebylo definováno stáří složek (v měsících) pro mazání\n")
        else:
            print("V zadane ceste nebyly nalezeny zadne slozky")
    else:
        print("\nZadaná cesta nebyla nalezena\n")


refresh()

while True:
    time.sleep(10)
    refresh()