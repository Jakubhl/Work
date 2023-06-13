import os
from pathlib import Path
import datetime
from datetime import datetime as datetime_
import time

def refresh():
    #f = open("mazani_config.txt", "r")
    with open('mazani_config.txt') as f:
        lines = [line.rstrip() for line in f]
 

    #main_path = str(f.read())
    main_path = lines[2]
    folders_created = []
    

    for files in os.listdir(main_path):
        if os.path.isdir(main_path+"/"+files):
            path = Path(main_path+"/"+files)
            stat_result = path.stat()
            created = datetime_.fromtimestamp(stat_result.st_ctime)
            created = str(created)[:10]
            folders_created.append(files + ", "+created)

    current_date = datetime.datetime.today()
    now = str(current_date)[:10]

    print("_________________________________________________________________________________________________________________________\n"
    ,folders_created,"\n")
    print("aktualni datum: "
    ,now," ,soubory starsi nez: ",lines[6]," mesicu budou odstraneny...\n")
    

refresh()

while True:
    time.sleep(10)
    refresh()