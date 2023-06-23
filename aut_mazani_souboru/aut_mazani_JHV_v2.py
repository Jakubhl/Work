import os
from pathlib import Path
import datetime
from datetime import datetime as datetime_
import time


class date_info:
    def __init__(self,date):
        self.date = str(date)[:10]
        self.year = self.date.split("-")[0]
        self.month = self.date.split("-")[1]
        self.day = self.date.split("-")[2]
        self.day = self.day[:2]
        self.months = 0
    
    def months_total(self):
        self.months = int(self.year)*12 + int(self.month)
        return self.months

    def get_day(self):
        #neresime vysokou presnost, +- 3 dny...
        if int(self.day) > 28:
            self.day = 28
        return int(self.day)





def refresh():
    with open('mazani_config.txt') as f:
        lines = [line.rstrip() for line in f]
    
    main_path = lines[2]
    folder_list = []

    current_date = datetime.datetime.today()
    current_months = date_info(current_date).months_total()
    current_day = date_info(current_date).get_day()
    
    if os.path.exists(main_path):
        if lines[6].isdigit():
            now = date_info(current_date).date
            print(f"_________________________________________________________________________________________________________________________\nKontrola č.: {control_count}")
            print("Aktualni datum: ",now," ,soubory staré: ",lines[6]," mesic/mesicu budou odstraneny...")
  
            for files in os.listdir(main_path):
                if os.path.isdir(main_path+"/"+files):
                    path = Path(main_path+"/"+files)
                    stat_result = path.stat()
                    date_created = datetime_.fromtimestamp(stat_result.st_ctime)
                    date_created = date_info(date_created).date

                    folder_list.append(files + ",created: "+date_created)
                    
                    created_in_months = date_info(date_created).months_total()
                    day_created = date_info(date_created).get_day()

                    if current_months >= (created_in_months + int(lines[6])):
                        if current_day == day_created:
                            print(f"mazu {files}...")
                            #os.rmtree(main_path+"/"+files)
                        
                        elif current_day > day_created:
                            days_left = 28-(current_day - day_created)
                            print(f"Slozka \"{files}\" bude odstranena za {days_left} dny/dní, ({date_info(date_created).year}-{str(int(date_info(date_created).month)+int(lines[6]))}-{day_created})")

            if len(folder_list) != 0:
                print("_________________________________________________________________________________________________________________________\nSeznam nalezenych slozek:\n"
                ,folder_list,"\n")
                   
            else:
                print("V zadane ceste nebyly nalezeny zadne slozky")
        else:
            print("Na sedmém řádku konfiguračního .txt souboru nebylo definováno stáří složek (v měsících) pro mazání\n")
    else:
        print("\nZadaná cesta nebyla nalezena\n")

#time.sleep(86400)

control_count = 1
refresh()

while True:
    time.sleep(10)
    #time.sleep(86400)
    control_count +=1
    refresh()