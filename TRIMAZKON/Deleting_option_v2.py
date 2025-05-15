import os
import datetime
from datetime import datetime
import shutil
import time

#to_delete_folder = "Ke_smazani"
supported_date_formats = ["YYYYMMDD","DDMMYYYY","YYMMDD"]
supported_separators = [".","/","_"]

def calc_days_in_month(current_month):
    months_30days = [4,6,9,11]
    if current_month == 2:
        days_in_month = 28
    elif current_month in months_30days:
        days_in_month = 30
    else:
        days_in_month = 31
        
    return days_in_month

def get_current_date():
        """
        - [0] = ymdhms
        - [1] = dmy
        - [2] = date_timestamp
        """
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d%H%M%S")
        readable_today = now.strftime("%d.%m.%Y")
        date_timestamp = now.strftime("%d.%m.%Y %H:%M:%S")
        #print(f"\n- Dnes je: {readable_today}")
        return [dt_string,readable_today,date_timestamp]

def get_max_days(cutoff_date):
    day = int(cutoff_date[0])
    month = int(cutoff_date[1])
    year = int(cutoff_date[2])
    current_date = get_current_date()
    current_day, current_month, current_year = current_date[1].split(".")
    year_div = int(current_year) - year
    month_div = int(current_month) - month
    month_div += year_div*12
    day_div = int(current_day) - day
    for _ in range(0,month_div):
        day_div += calc_days_in_month(month)
        month +=1
        if month > 12:
            month=1

    return day_div

def get_cutoff_date(days):
    current_date = get_current_date()
    current_day, current_month, current_year = current_date[1].split(".")
    day = int(current_day)
    month = int(current_month)
    year = int(current_year)
    while days > 0:
        day -= 1
        if day == 0:
            month -= 1
            if month == 0:
                month = 12
                year -= 1
            day = calc_days_in_month(month)
        days -= 1
    return [day,month,year]

class whole_deleting_function:
    """
    Funkce pro mazání souborů

    vrací záznam výstupních zpráv: self.output

    vstupními parametry jsou: 
    
    1 path_given (cesta k souborům)\n
    2 more_dirs (zda procházet subsložky)\n
    3 del_option (vybraná možnost mazání)\n
    4 files_to_keep (počet minimálního počtu souborů k ponechání)\n
    5 cutoff_date_given (rozhodovací datum)\n
    6 supported_formats (seznam podporovaných formátů)\n
    7 testing_mode (režim testování)\n
    8 jmeno slozky pro prevedeni souboru urcenych ke smazani\n
    9 určovat stáří souboru podle modification date nebo podle creation date
    """
    def __init__(self,
                 path_given,
                 more_dirs,
                 del_option,
                 files_to_keep,
                 cutoff_date_given,
                 supported_formats,
                 testing_mode,
                 to_delete_folder_name,
                 creation_date=False,
                 only_analyze = False):
        self.path = path_given
        self.max_days_old = 365
        self.to_delete_folder = to_delete_folder_name
        self.supported_date_formats = supported_date_formats
        self.supported_separators = supported_separators
        self.output = []
        self.output_eng = []
        self.output_console2 = []
        self.more_dirs = more_dirs
        self.del_option = del_option
        self.files_to_keep = files_to_keep
        self.cutoff_date_given = cutoff_date_given
        self.supported_formats = supported_formats
        self.testing_mode = testing_mode
        self.only_analyze = only_analyze
        self.creation_date = creation_date
        self.newer_files_checked = 0
        self.files_checked = 0
        self.files_deleted = 0
        self.older_files_checked = 0
        self.directories_checked = 0
        self.directories_deleted = 0
        self.directories_older= 0
        self.finish = False

    def make_dir(self,name,path):
        if not os.path.exists(path + name): #pokud uz neni vytvorena, vytvor...
            os.mkdir(path + name + "/")

    def collect_to_delete_folder(self,path):
        """
        Funkce sesbírá soubory ze složky, ve které jsou soubory určené ke smazání z testing módu
        """
        if os.path.exists(path + self.to_delete_folder):
            for files in os.listdir(path + self.to_delete_folder):
                if os.path.exists(path + self.to_delete_folder + "/" + files):
                    shutil.move(path + self.to_delete_folder + "/" + files , path + files)

    def sync_folders(self,path):
        folders = []
        for files in os.listdir(path):
            if os.path.isdir(path + files):
                if files != self.to_delete_folder:
                    folders.append(files)

        return folders
     
    def get_mod_date_of_file(self,path,file,dir=False):
        if os.path.isdir(path + file) == False or dir == True:
            mod_date_timestamp = os.path.getmtime(path + file)
            mod_date = datetime.fromtimestamp(mod_date_timestamp)
            #mod_date_str = mod_date.strftime("%Y%m%d%H%M%S")
            mod_date_str = mod_date.strftime("%Y%m%d")
            return mod_date_str
        else:
            return False
        
    def get_creation_date_of_file(self,file,dir=False):
        if os.path.isdir(self.path + file) == False or dir == True:
            creation_date_timestamp = os.path.getctime(self.path + file)
            creation_date = datetime.fromtimestamp(creation_date_timestamp)
            # creation_date_str = mod_date.strftime("%Y%m%d%H%M%S")
            creation_date_str = creation_date.strftime("%Y%m%d")
            return creation_date_str
        else:
            return False

    def calc_cutoffdays(self):
        current_date = get_current_date()
        current_date = current_date[0]
        current_year = current_date[0:4]
        current_month = current_date[4:6]
        current_day = current_date[6:8]
        

        cutoffdays = int(current_day) - self.max_days_old + 1
        done = False
        while done == False:
            days_in_month = calc_days_in_month(int(current_month))
            cutoffdays = cutoffdays + days_in_month
            if current_month ==1:
                current_month = 12
                current_year = int(current_year) - 1
            else:
                current_month = int(current_month) - 1
            if cutoffdays > 0:
                done = True

        if len(str(current_month)) < 2:
            current_month = "0" + str(current_month)
        if len(str(cutoffdays)) < 2:
            current_day = "0" + str(current_day)

        cutoff_date = str(current_year) + str(current_month) + str(cutoffdays) + current_date[8:]
        readable_cutoff_date = str(cutoffdays) + "." + str(current_month) + "." + str(current_year)
        print(f"- Smažou se soubory starší než: {readable_cutoff_date}")
        #self.output.append(f"- Smažou se soubory starší než: {readable_cutoff_date}\n")
        return [cutoff_date,readable_cutoff_date]
    
    def calc_cutoffdays_given(self):
        given_day = str(self.cutoff_date_given[0])
        given_month = str(self.cutoff_date_given[1])
        if len(given_day) == 1:
            given_day = "0" + given_day
        if len(given_month) == 1:
            given_month = "0" + given_month

        cutoff_date = str(self.cutoff_date_given[2])+given_month+given_day
        readable_cutoff_date = given_day + "." + given_month + "." + str(self.cutoff_date_given[2])
        print(cutoff_date,readable_cutoff_date)
        return [cutoff_date,readable_cutoff_date]
    
    def subfolders_check(self):
        paths_stage1 = []
        paths_stage2 = []
        paths_stage3 = []
        paths_stage4 = []
        paths_stage5 = []
        paths_stage6 = []
        all_paths = []
        #STAGE1///////////////////////////////////////////////////
        found_folders = self.sync_folders(self.path)
        for folders in found_folders:
            if not (self.path + folders+"/") in paths_stage1:     
                paths_stage1.append(self.path + folders+"/")
                all_paths.append(self.path + folders+"/")
            if not (self.path) in all_paths:   
                all_paths.append(self.path)
                
        if len(paths_stage1) != 0:
            #STAGE2///////////////////////////////////////////////////
            for paths_found in paths_stage1:
                found_folders = self.sync_folders(paths_found)
                for folders in found_folders:
                    if not (paths_found + folders+"/") in paths_stage2:
                        paths_stage2.append(paths_found + folders+"/")
                        all_paths.append(paths_found + folders+"/")
        if len(paths_stage2) != 0:
            #STAGE3///////////////////////////////////////////////////
            for paths_found in paths_stage2:
                found_folders = self.sync_folders(paths_found)
                for folders in found_folders:
                    if not (paths_found + folders+"/") in paths_stage3:
                        paths_stage3.append(paths_found + folders+"/")
                        all_paths.append(paths_found + folders+"/")
        if len(paths_stage3) != 0:
            #STAGE4///////////////////////////////////////////////////
            for paths_found in paths_stage3:
                found_folders = self.sync_folders(paths_found)
                for folders in found_folders:
                    if not (paths_found + folders+"/") in paths_stage4:
                        paths_stage4.append(paths_found + folders+"/")
                        all_paths.append(paths_found + folders+"/")
        if len(paths_stage4) != 0:
            #STAGE5///////////////////////////////////////////////////
            for paths_found in paths_stage4:
                found_folders = self.sync_folders(paths_found)
                for folders in found_folders:
                    if not (paths_found + folders+"/") in paths_stage5:
                        paths_stage5.append(paths_found + folders+"/")
                        all_paths.append(paths_found + folders+"/")
        if len(paths_stage5) != 0:
            #STAGE6///////////////////////////////////////////////////
            for paths_found in paths_stage5:
                found_folders = self.sync_folders(paths_found)
                for folders in found_folders:
                    if not (paths_found + folders+"/") in paths_stage6:
                        paths_stage6.append(paths_found + folders+"/")
                        all_paths.append(paths_found + folders+"/")

        return all_paths
    
    def get_format_dir_name(self): #bude probihat pouze v jedne slozce, nema smysl lezt do subslozek
        folders = []
        count_of_each_separator = [0,0,0]
        #automaticke zjistovani formatu
        #1) zjistovani separatoru v datu
        folders = self.sync_folders(self.path)
        for folds in folders:
            for sep in self.supported_separators:
                if len(folds.split(sep)) == 3:
                    count_of_each_separator[self.supported_separators.index(sep)] += 1

        if sum(count_of_each_separator) != 0:        
            # vypocitani nejvyssi pravdepodobnosti
            for i in range(0,len(self.supported_separators)):
                if max(count_of_each_separator) == count_of_each_separator[i]:
                    found_separator = self.supported_separators[i]
                    probability = (max(count_of_each_separator)/sum(count_of_each_separator))*100
                    probability = "%.2f" % (probability) #prevod na dve desetinna mista
                
            #print(f"- Separátor automaticky nastaven na: {found_separator}\nPravděpodobnost správné detekce: {probability} %")
            self.output_eng.append(f"- Separator automatically set to: {found_separator}. Probability of correct detection: {probability} %")
            self.output.append(f"- Separátor automaticky nastaven na: {found_separator}. Pravděpodobnost správné detekce: {probability} %")
            
            #2) zjistovani a oprava delky data v nazvu
            folders_format1 = []
            folders_format2 = []
            folders_format3 = []
            folders_right_format = []
            count_of_found_formats = [0,0,0]
            for folds in folders:
                folds_split = folds.split(found_separator)
                if len(folds_split) == 3:
                    if len(folds_split[0]) == 1:
                        folds_split[0] ="0"+ folds_split[0]
                    if len(folds_split[1]) == 1:
                        folds_split[1] ="0"+ folds_split[1]
                    if len(folds_split[2]) == 1:
                        folds_split[2] ="0"+ folds_split[2]
                    
                    folder_corrected = folds_split[0] + found_separator + folds_split[1] + found_separator + folds_split[2]
                    folds_split = folder_corrected.split(found_separator)
                        
                    if len(folder_corrected) == 10: #20.02.2022 nebo 20.02.22
                        for i in range(0,len(folds_split)):
                            if len(folds_split[i]) == 4:
                                if i == 0:
                                    #format = "YYYYMMDD"
                                    count_of_found_formats[0] += 1
                                    folders_format1.append(folds) #chceme neopravene aby je bylo mozne vyhledat
                                else:
                                    #format = "DDMMYYYY"
                                    count_of_found_formats[1] += 1
                                    folders_format2.append(folds)
                    elif len(folder_corrected) == 8:
                        #format = "YYMMDD"
                        count_of_found_formats[2] += 1
                        folders_format3.append(folds)
            if sum(count_of_found_formats) != 0:
                for i in range(0,len(self.supported_date_formats)):
                    if max(count_of_found_formats) == count_of_found_formats[i]:
                        found_format = self.supported_date_formats[i]
                        probability = (max(count_of_found_formats)/sum(count_of_found_formats))*100
                        probability = "%.2f" % (probability) #prevod na dve desetinna mista
                #print(f"- Formát automaticky nastaven na: {found_format}\nPravděpodobnost správné detekce: {probability} %")
                self.output_eng.append(f"- Format automatically set to: {found_format}. Probability of correct detection: {probability} %")
                self.output.append(f"- Formát automaticky nastaven na: {found_format}. Pravděpodobnost správné detekce: {probability} %")


                if found_format == self.supported_date_formats[0]:
                    folders_right_format = folders_format1
                elif found_format == self.supported_date_formats[1]:
                    folders_right_format = folders_format2
                elif found_format == self.supported_date_formats[2]:
                    folders_right_format = folders_format3
                return [found_separator,found_format,folders_right_format]
            
            else:
                #print(f"- Chyba: V zadané cestě nebyly nalezeny žádné podporované formáty názvu složek {self.supported_date_formats} pro vybraný způsob mazání")
                self.output_eng.append(f"- Error: no supported folder name formats {self.supported_date_formats} were found in the specified path for the selected deletion option")
                self.output.append(f"- Chyba: V zadané cestě nebyly nalezeny žádné podporované formáty názvu složek {self.supported_date_formats} pro vybraný způsob mazání")
                
                return [False,False,False]
        else:
            #print(f"- Chyba: V zadané cestě nebyly nalezeny žádné podporované separátory v názvu složek {self.supported_separators} pro vybraný způsob mazání")
            self.output_eng.append(f"- Error: no supported folder name separators {self.supported_separators} were found in the specified path for the selected deletion option")
            self.output.append(f"- Chyba: V zadané cestě nebyly nalezeny žádné podporované separátory v názvu složek {self.supported_separators} pro vybraný způsob mazání")

            return [False,False,False]
        
    def del_directories(self,found_separator,found_format,folders_right_format):
        folders_without_separators = []
        deleted_directores = 0
        directories_checked = 0
        for folds in folders_right_format:
            folders_split = folds.split(found_separator)
            if found_format == "DDMMYYYY":
                if len(folders_split[0]) == 1:
                    folders_split[0] = "0"+folders_split[0]
                if len(folders_split[1]) == 1:
                    folders_split[1] = "0"+folders_split[1]
                folder_without_separators = folders_split[2] + folders_split[1] + folders_split[0]
                folders_without_separators.append(folder_without_separators)
            elif found_format == "YYYYMMDD":
                if len(folders_split[1]) == 1:
                    folders_split[1] = "0"+folders_split[1]
                if len(folders_split[2]) == 1:
                    folders_split[2] = "0"+folders_split[2]
                folder_without_separators = folders_split[0] + folders_split[1] + folders_split[2]
                folders_without_separators.append(folder_without_separators)
            elif found_format == "YYMMDD":
                year = "20" + folders_split[0]
                if len(folders_split[1]) == 1:
                    folders_split[1] = "0"+folders_split[1]
                if len(folders_split[2]) == 1:
                    folders_split[2] = "0"+folders_split[2]
                folder_without_separators = year + folders_split[1] + folders_split[2]
                folders_without_separators.append(folder_without_separators)

        cutoff_days = self.calc_cutoffdays_given()
        cutoff_days = cutoff_days[0]

        for i in range(0,len(folders_without_separators)):
            #if int(folders_without_separators[i]) < int(cutoff_days[:8]):
            directories_checked +=1
            if int(folders_without_separators[i]) < int(cutoff_days):
                deleted_directores +=1
                if self.testing_mode == True:
                    if not self.only_analyze:
                        self.make_dir(self.to_delete_folder,self.path)
                        try:
                            shutil.move(self.path + folders_right_format[i] , self.path + self.to_delete_folder + '/' + folders_right_format[i])
                        except Exception as e:
                            print("Nastala chyba: ",e)
                        print(f"Mazání: {self.path + folders_right_format[i]}")
                if self.testing_mode == False:
                    shutil.rmtree(self.path + folders_right_format[i])
        
        self.directories_deleted += deleted_directores
        self.directories_checked += directories_checked

        if deleted_directores == 0:
            self.output_eng.append(f"- Directories checked: {directories_checked}")
            self.output_eng.append("No directories found to be deleted")
            self.output.append(f"- Zkontrolováno adresářů: {directories_checked}")
            self.output.append("Nebyly nalezeny žádné adresáře určené ke smazání")
        else:
            self.output_eng.append(f"- Directories checked: {directories_checked}")
            self.output.append(f"- Zkontrolováno adresářů: {directories_checked}")

            if self.testing_mode == True:
                self.output_eng.append(f"It would delete directories: {deleted_directores}")
                self.output.append(f"Smazalo by se adresářů: {deleted_directores}")
            else:
                self.output_eng.append(f"Directories deleted: {deleted_directores}")
                self.output.append(f"Smazáno adresářů: {deleted_directores}")

    def del_dirs_option4(self):
        """
        deletion based on directory age
        - creation date
        - modification date
        """
        deleted_directores = 0
        directories_checked = 0
        older_directories=0
        folder_list = [entry.name for entry in os.scandir(self.path) if entry.is_dir()]
        cutoff_days = self.calc_cutoffdays_given()
        cutoff_days = cutoff_days[0]
        
        for i in range(0,len(folder_list)):
            directories_checked +=1
            if self.creation_date:
                folder_date = self.get_creation_date_of_file(folder_list[i],dir=True)
            else:
                folder_date = self.get_mod_date_of_file(self.path,folder_list[i],dir=True)

            if int(folder_date) < int(cutoff_days):
                older_directories +=1
                if older_directories > self.files_to_keep:
                    deleted_directores +=1
                    if self.testing_mode == True:
                        if not self.only_analyze:
                            self.make_dir(self.to_delete_folder,self.path)
                            try:
                                shutil.move(self.path + folder_list[i] , self.path + self.to_delete_folder + '/' + folder_list[i])
                            except Exception as e:
                                print("Nastala chyba: ",e)
                            print(f"Mazání: {self.path + folder_list[i]}")
                    elif self.testing_mode == False:
                        shutil.rmtree(self.path + folder_list[i])
        self.directories_older += older_directories
        self.directories_deleted += deleted_directores
        self.directories_checked += directories_checked

        if deleted_directores == 0:
            self.output_eng.append(f"- Directories checked: {directories_checked}")
            self.output_eng.append("No directories found to be deleted")
            self.output.append(f"- Zkontrolováno adresářů: {directories_checked}")
            self.output.append("Nebyly nalezeny žádné adresáře určené ke smazání")
        else:
            self.output_eng.append(f"- Directories checked: {directories_checked}")
            self.output.append(f"- Zkontrolováno adresářů: {directories_checked}")
            if self.testing_mode == True:
                self.output_eng.append(f"It would delete directories: {deleted_directores}")
                self.output.append(f"Smazalo by se adresářů: {deleted_directores}")
            else:
                self.output_eng.append(f"Directories deleted: {deleted_directores}")
                self.output.append(f"Smazáno adresářů: {deleted_directores}")

    def del_files(self,path,cutoff_days,option):
        older_files_checked = 0
        newer_files_checked = 0
        files_checked = 0
        deleted_count = 0
        self.collect_to_delete_folder(path)
        
        if option == 0:
            for files in os.listdir(path):
                if self.creation_date:
                    date_of_file = self.get_creation_date_of_file(files)
                else:
                    date_of_file = self.get_mod_date_of_file(path,files)
                if date_of_file != False:
                    files_split = files.split(".")
                    file_extension = files_split[-1].lower()
                    if file_extension in self.supported_formats:
                        files_checked +=1
                        if int(date_of_file) < cutoff_days:
                            older_files_checked +=1
                            if older_files_checked > self.files_to_keep:
                                deleted_count +=1
                                if self.testing_mode == True:
                                    #print(f"Mazání: {path + files}")
                                    if not self.only_analyze:
                                        self.make_dir(self.to_delete_folder,path)
                                        shutil.move(path + files , path + self.to_delete_folder + '/' + files)
                                if self.testing_mode == False:
                                    os.remove(path + files)
        
        def check_min_file_age(path):
            date_array=[]
            for files in os.listdir(path):
                if self.creation_date:
                    date_of_file = self.get_creation_date_of_file(files)
                else:
                    date_of_file = self.get_mod_date_of_file(path,files)
                if date_of_file != False:
                    if not int(date_of_file) in date_array:
                        date_array.append(int(date_of_file))
            if len(date_array)>0:
                return max(date_array)
            else:
                return []
        if option == 1:
            # pokud jsou všechny starší vydej varování - a zruš:
            min_file_age = check_min_file_age(path)
            if min_file_age != []:
                if check_min_file_age(path) <= cutoff_days and not self.only_analyze:
                    return "warning data loss"
            for files in os.listdir(path):
                if self.creation_date:
                    date_of_file = self.get_creation_date_of_file(files)
                else:
                    date_of_file = self.get_mod_date_of_file(path,files)
                if date_of_file != False:
                    files_split = files.split(".")
                    file_extension = files_split[-1].lower()
                    if file_extension in self.supported_formats:
                        files_checked +=1
                        if int(date_of_file) < cutoff_days:
                            deleted_count +=1
                            if self.testing_mode == True:
                                #print(f"Mazání: {path + files}")
                                if not self.only_analyze:
                                    self.make_dir(self.to_delete_folder,path)
                                    shutil.move(path + files , path + self.to_delete_folder + '/' + files)
                            if self.testing_mode == False:
                                os.remove(path + files)
                        else:
                            newer_files_checked +=1
                            if newer_files_checked > self.files_to_keep:
                                deleted_count +=1
                                if self.testing_mode == True:
                                    #print(f"Mazání: {path + files}")
                                    if not self.only_analyze:
                                        self.make_dir(self.to_delete_folder,path)
                                        shutil.move(path + files , path + self.to_delete_folder + '/' + files)
                                if self.testing_mode == False:
                                    os.remove(path + files)
        
        #mazani potencionalne prazdne slozky
        number_of_files = 0
        if os.path.exists(path + self.to_delete_folder):
            for files in os.listdir(path + self.to_delete_folder):
                number_of_files +=1
            if number_of_files == 0:
                os.rmdir(path+self.to_delete_folder)
        
        self.files_checked += files_checked
        self.files_deleted += deleted_count
        self.newer_files_checked += newer_files_checked
        self.older_files_checked += older_files_checked

        if deleted_count == 0:
            self.output_eng.append(f"- Files checked: {files_checked}")
            self.output_eng.append("- No files found for deletion\n")
            self.output.append(f"- Zkontrolováno souborů: {files_checked}")
            self.output.append("- Nebyly nalezeny žádné soubory určené ke smazání\n")
        else:
            print(f"Smazáno souborů: {deleted_count}")
            self.output_eng.append(f"- Files checked: {files_checked}")
            self.output.append(f"- Zkontrolováno souborů: {files_checked}")

            if self.testing_mode == True:
                self.output_eng.append(f"It would erase: {deleted_count} files\n")
                self.output.append(f"Smazalo by se: {deleted_count} souborů\n")
            else:
                self.output_eng.append(f"Files deleted: {deleted_count}\n")
                self.output.append(f"Smazáno souborů: {deleted_count}\n")

        return deleted_count

    def main(self):
        result_cutoffdays = self.calc_cutoffdays_given()
        cutoff_days = int(result_cutoffdays[0])
        
        if self.more_dirs == True: #////////////////////////////////////////////////////////// MORE_DIRS //////////////////////////////////////////////////////////////////////////
            if not self.only_analyze:
                self.output_eng.append(f"- Deleting images in the path: {self.path}  and in all subfolders (maximum 6 subfolders) is in progress")
                self.output.append(f"- Probíhá mazání obrázků v cestě: {self.path} a ve všech podružných složkách (maximum je 6 subsložek)")

            if self.del_option == 1: #//////////////////////////////////////////////////////// OPTION 1 ///////////////////////////////////////////////////////////////////////////
                total_deleted_count = 0
                #print(f"- Probíhá mazání obrázků v cestě: {self.path}\na ve všech podružných složkách (maximum je 6 subsložek)")
                #print(f"- V každé složce bude zachováno: {self.files_to_keep} souborů\n")
                if not self.only_analyze:
                    self.output_eng.append(f"- It will be left in each folder: {self.files_to_keep} older files")
                    self.output.append(f"- V každé složce bude zachováno: {self.files_to_keep} starších souborů")

                all_paths = self.subfolders_check()
                for paths in all_paths:
                    self.output_console2.append(f"{paths}\n")
                    #print(f"- Prochazím cestu: {paths}")
                    if not self.only_analyze:
                        self.output_eng.append(f"- Deleting images in the path: {paths} is in progress")
                        self.output.append(f"- Probíhá mazání obrázků v cestě: {paths}")
                    else:
                        self.output_eng.append(f"- Analyzing path: {paths}")
                        self.output.append(f"- Analyzuje se: {paths}")

                    deleted = self.del_files(paths,cutoff_days,0)
                    if deleted == "warning data loss":
                        if not self.only_analyze:
                            self.output_eng.append(f"- All files in this folder are older than the set date (nothing would be left) - cancelled")
                            self.output.append(f"- V této složce jsou všechny soubory starší, než nastvené datum (nebylo by nic ponecháno) - zrušeno")
                        deleted = 0
                    total_deleted_count = total_deleted_count+deleted
                
                if not self.only_analyze:
                    self.output_eng.append(f"- Deletion complete, total files deleted: {total_deleted_count}\n")
                    self.output.append(f"- Mazání dokončeno, celkem smazáno souborů: {total_deleted_count}\n")
                else:
                    self.output_eng.append(f"- Analyzing completed, it would delete files in total: {total_deleted_count}\n")
                    self.output.append(f"- Analýza ukončena, celkem by se smazalo souborů: {total_deleted_count}\n")
                
            if self.del_option == 2: #///////////////////////////////////////////////////////// OPTION 2 /////////////////////////////////////////////////////////////////////////////
                total_deleted_count = 0
                all_paths = self.subfolders_check()
                #print(f"- V každé složce bude zachováno: {self.files_to_keep} souborů, novějších než {result_cutoffdays[1]}")
                if not self.only_analyze:
                    self.output_eng.append(f"- Each folder will maintain: {self.files_to_keep} files, newer then {result_cutoffdays[1]}")
                    self.output.append(f"- V každé složce bude zachováno: {self.files_to_keep} souborů, novějších než {result_cutoffdays[1]}")

                for paths in all_paths:
                    #print(f"- Probíhá mazání obrázků v cestě: {paths}")
                    if not self.only_analyze:
                        self.output_eng.append(f"- Deleting images in the path: {paths} is in progress")
                        self.output.append(f"- Probíhá mazání obrázků v cestě: {paths}")
                    else:
                        self.output_eng.append(f"- Analyzing path: {paths}")
                        self.output.append(f"- Analyzuje se: {paths}")

                    deleted = self.del_files(paths,cutoff_days,1)
                    if deleted == "warning data loss":
                        if not self.only_analyze:
                            self.output_eng.append(f"- All files in this folder are older than the set date (nothing would be left) - cancelled")
                            self.output.append(f"- V této složce jsou všechny soubory starší, než nastvené datum (nebylo by nic ponecháno) - zrušeno")
                        deleted = 0
                    total_deleted_count = total_deleted_count+deleted

                if not self.only_analyze:
                    self.output_eng.append(f"- Deletion complete, total files deleted: {total_deleted_count}\n")
                    self.output.append(f"- Mazání dokončeno, celkem smazáno souborů: {total_deleted_count}\n")
                else:
                    self.output_eng.append(f"- Analyzing completed, it would delete files in total: {total_deleted_count}\n")
                    self.output.append(f"- Analýza ukončena, celkem by se smazalo souborů: {total_deleted_count}\n")

            if self.del_option == 3: #///////////////////////////////////////////////////////// OPTION 3 /////////////////////////////////////////////////////////////////////////////
                #print("Pro tuto možnost mazání není možné procházet subadresáře")
                self.output_eng.append("It is not possible to browse subdirectories for this deletion option\n")
                self.output.append("Pro tuto možnost mazání není možné procházet subadresáře\n")

        if self.more_dirs == False: #////////////////////////////////////////////////////////// ONE_PATH //////////////////////////////////////////////////////////////////////////
            if self.del_option == 1: #////////////////////////////////////////////////////////// OPTION 1 ////////////////////////////////////////////////////////////////////////////
                 # tato moznost provadi mazani pouze starsich a uchovavani nejakeho poctu pouze starsich souboru
                #print(f"- Probíhá mazání obrázků v cestě: {self.path}")
                if not self.only_analyze:
                    self.output_eng.append(f"- Deleting images in the path: {self.path} is in progress")
                    self.output_eng.append(f"- The folder will maintain: {self.files_to_keep} older files")
                    self.output.append(f"- Probíhá mazání obrázků v cestě: {self.path}")
                    self.output.append(f"- Ve složce bude zachováno: {self.files_to_keep} starších souborů")

                del_status = self.del_files(self.path,cutoff_days,0)
                if not self.only_analyze:
                    if del_status == "warning data loss":
                        self.output_eng.append(f"- All files in this folder are older than the set date (nothing would be left) - cancelled")
                        self.output.append(f"- V této složce jsou všechny soubory starší, než nastvené datum (nebylo by nic ponecháno) - zrušeno")
                    self.output_eng.append("- Deleting complete\n")
                    self.output.append("- Mazání dokončeno\n")

            elif self.del_option == 2: #///////////////////////////////////////////////////////// OPTION 2 /////////////////////////////////////////////////////////////////////////////
                # tato moznost provadi mazani vsech starsich a redukuje novejsi (vhodne u generovani velkeho poctu obrazku za kratky cas)
                #print(f"- Probíhá mazání obrázků v cestě: {self.path}")
                if not self.only_analyze:
                    self.output_eng.append(f"- Deleting images in the path: {self.path} is in progress")
                    self.output_eng.append(f"- The folder will maintain: {self.files_to_keep} files, newer then {result_cutoffdays[1]}")
                    self.output.append(f"- Probíhá mazání obrázků v cestě: {self.path}")
                    self.output.append(f"- Ve složce bude zachováno: {self.files_to_keep} souborů, novějších než {result_cutoffdays[1]}")
                del_status = self.del_files(self.path,cutoff_days,1)
                if not self.only_analyze:
                    if del_status == "warning data loss":
                        self.output_eng.append(f"- All files in this folder are older than the set date (nothing would be left) - cancelled")
                        self.output.append(f"- V této složce jsou všechny soubory starší, než nastvené datum (nebylo by nic ponecháno) - zrušeno")
                    self.output_eng.append("- Deleting complete\n")
                    self.output.append("- Mazání dokončeno\n")
                
            elif self.del_option == 3: #///////////////////////////////////////////////////////// OPTION 3 /////////////////////////////////////////////////////////////////////////////
                # tato moznost provadi mazani slozek s datumem v jejich nazvu
                format_error = False
                #print(f"- Probíhá mazání složek, jejichž název = datum, v cestě: {self.path}")
                if not self.only_analyze:
                    self.output_eng.append(f"- Deleting folders with name = date in the path: {self.path} is in progress")
                    self.output.append(f"- Probíhá mazání složek, jejichž název = datum, v cestě: {self.path}")
                result = self.get_format_dir_name()
                for items in result:
                    if items == False:
                        format_error = True
                if format_error == False:
                    found_separator = result[0]
                    found_format = result[1]
                    folders_right_format = result[2]
                    self.del_directories(found_separator,found_format,folders_right_format)
                if not self.only_analyze:
                    self.output_eng.append("- Deleting complete\n")
                    self.output.append("- Mazání dokončeno\n")
            
            elif self.del_option == 4: #///////////////////////////////////////////////////////// OPTION 4 /////////////////////////////////////////////////////////////////////////////
                # tato moznost provadi mazani slozek podle jejich stáří
                if not self.only_analyze:
                    self.output_eng.append(f"- Deleting folders older then the set date in the path: {self.path} is in progress")
                    self.output.append(f"- Probíhá mazání složek, starších než nastavené datum, v cestě: {self.path}")
                self.del_dirs_option4()
                if not self.only_analyze:
                    self.output_eng.append("- Deleting complete\n")
                    self.output.append("- Mazání dokončeno\n")

        self.finish = True
        # print(self.output)
        
        if self.del_option == 3 or self.del_option == 4:
            return [self.directories_checked,self.directories_older,self.directories_deleted,get_current_date()[2],0,1] # pro případ spouštění přes cmd prompt, jinak sem nedojde přes finish
        else:
            return [self.files_checked,self.older_files_checked,self.files_deleted,get_current_date()[2],self.newer_files_checked,len(self.subfolders_check())] # pro případ spouštění přes cmd prompt, jinak sem nedojde přes finish
        
# wdf_inst =whole_deleting_function("C:\\Users\\jakub.hlavacek.local\\Pictures\\Screenshots\\",True,1,100,[25,1,2025],["bmp","png"],True,"Ke_smazani",False,True)
# wdf_inst.main()
