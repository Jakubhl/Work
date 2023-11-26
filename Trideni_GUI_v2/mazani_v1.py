import os
import datetime
from datetime import datetime
import shutil
import re

def whole_deleting_function(path_given,more_dirs,del_option):
    files_to_keep = 20
    max_days_old = 30
    supported_formats = ["jpg","bmp","png","ifz"]

    def sync_folders(path):
        folders = []
        for files in os.listdir(path):
            if os.path.isdir(path + files):
                folders.append(files)

        return folders

    def get_current_date():
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d%H%M%S")
        readable_today = now.strftime("%d.%m.%Y")
        print(f"\n- Dnes je: {readable_today}")
        return dt_string
     
    def get_mod_date_of_file(path,file):
        if os.path.isdir(path + file) == False:
            mod_date_timestamp = os.path.getmtime(path + file)
            mod_date = datetime.fromtimestamp(mod_date_timestamp)
            mod_date_str = mod_date.strftime("%Y%m%d%H%M%S")
            return mod_date_str
        else:
            return False

    def calc_cutoffdays():
        current_date = get_current_date()
        current_year = current_date[0:4]
        current_month = current_date[4:6]
        current_day = current_date[6:8]
        

        cutoffdays = int(current_day) - max_days_old + 1
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
        return cutoff_date
     
    def calc_days_in_month(current_month):
        months_30days = [4,6,9,11]
        if current_month == 2:
            days_in_month = 28
        elif current_month in months_30days:
            days_in_month = 30
        else:
            days_in_month = 31
        return days_in_month

    def subfolders_check():
        paths_stage1 = []
        paths_stage2 = []
        paths_stage3 = []
        paths_stage4 = []
        paths_stage5 = []
        paths_stage6 = []
        all_paths = []
        #STAGE1///////////////////////////////////////////////////
        found_folders = sync_folders(path_given)
        for folders in found_folders:
            if not (path_given + folders+"/") in paths_stage1:     
                paths_stage1.append(path_given + folders+"/")
                all_paths.append(path_given + folders+"/")
            if not (path_given) in all_paths:   
                all_paths.append(path_given)
                
        if len(paths_stage1) != 0:
            #STAGE2///////////////////////////////////////////////////
            for paths_found in paths_stage1:
                found_folders = sync_folders(paths_found)
                for folders in found_folders:
                    if not (paths_found + folders+"/") in paths_stage2:
                        paths_stage2.append(paths_found + folders+"/")
                        all_paths.append(paths_found + folders+"/")
        if len(paths_stage2) != 0:
            #STAGE3///////////////////////////////////////////////////
            for paths_found in paths_stage2:
                found_folders = sync_folders(paths_found)
                for folders in found_folders:
                    if not (paths_found + folders+"/") in paths_stage3:
                        paths_stage3.append(paths_found + folders+"/")
                        all_paths.append(paths_found + folders+"/")
        if len(paths_stage3) != 0:
            #STAGE4///////////////////////////////////////////////////
            for paths_found in paths_stage3:
                found_folders = sync_folders(paths_found)
                for folders in found_folders:
                    if not (paths_found + folders+"/") in paths_stage4:
                        paths_stage4.append(paths_found + folders+"/")
                        all_paths.append(paths_found + folders+"/")
        if len(paths_stage4) != 0:
            #STAGE5///////////////////////////////////////////////////
            for paths_found in paths_stage4:
                found_folders = sync_folders(paths_found)
                for folders in found_folders:
                    if not (paths_found + folders+"/") in paths_stage5:
                        paths_stage5.append(paths_found + folders+"/")
                        all_paths.append(paths_found + folders+"/")
        if len(paths_stage5) != 0:
            #STAGE6///////////////////////////////////////////////////
            for paths_found in paths_stage5:
                found_folders = sync_folders(paths_found)
                for folders in found_folders:
                    if not (paths_found + folders+"/") in paths_stage6:
                        paths_stage6.append(paths_found + folders+"/")
                        all_paths.append(paths_found + folders+"/")

        return all_paths
    
    def get_format_dir_name(): #bude probihat pouze v jedne slozce, nema smysl lezt do subslozek
        folders = []
        count_of_each_separator = [0,0,0]
        supported_separators = [".","/","_"]

        #automaticke zjistovani formatu
        #1) zjistovani separatoru v datu
        folders = sync_folders(path_given)
        for folds in folders:
            for sep in supported_separators:
                if len(folds.split(sep)) == 3:
                    count_of_each_separator[supported_separators.index(sep)] += 1

        if sum(count_of_each_separator) != 0:        
            # vypocitani nejvyssi pravdepodobnosti
            for i in range(0,len(supported_separators)):
                if max(count_of_each_separator) == count_of_each_separator[i]:
                    found_separator = supported_separators[i]
                    probability = (max(count_of_each_separator)/sum(count_of_each_separator))*100
                    probability = "%.2f" % (probability) #prevod na dve desetinna mista
                
            print(f"- Separátor automaticky nastaven na: {found_separator}\nPravděpodobnost správné detekce: {probability} %")

            #2) zjistovani a oprava delky data v nazvu
            folders_format1 = []
            folders_format2 = []
            folders_format3 = []
            folders_right_format = []
            count_of_found_formats = [0,0,0]
            supported_date_formats = ["YYYYMMDD","DDMMYYYY","YYMMDD"]
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
                for i in range(0,len(supported_date_formats)):
                    if max(count_of_found_formats) == count_of_found_formats[i]:
                        found_format = supported_date_formats[i]
                        probability = (max(count_of_found_formats)/sum(count_of_found_formats))*100
                        probability = "%.2f" % (probability) #prevod na dve desetinna mista
                print(f"- Formát automaticky nastaven na: {found_format}\nPravděpodobnost správné detekce: {probability} %")

                if found_format == supported_date_formats[0]:
                    folders_right_format = folders_format1
                elif found_format == supported_date_formats[1]:
                    folders_right_format = folders_format2
                elif found_format == supported_date_formats[2]:
                    folders_right_format = folders_format3
                return [found_separator,found_format,folders_right_format]
            
            else:
                print(f"- Chyba: V zadané cestě nebyly nalezeny žádné podporované formáty názvu složek {supported_date_formats} pro vybraný způsob mazání")
                return [False,False,False]
        else:
            print(f"- Chyba: V zadané cestě nebyly nalezeny žádné podporované separátory v názvu složek {supported_separators} pro vybraný způsob mazání")
            return [False,False,False]
        
    def del_directories(found_separator,found_format,folders_right_format):
        folders_without_separators = []
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
                folder_without_separators = year + folders_split[1] + folders_split[2]
                folders_without_separators.append(folder_without_separators)

        cutoff_days = calc_cutoffdays()
        for i in range(0,len(folders_without_separators)):
            if int(folders_without_separators[i]) < int(cutoff_days[:8]):
                print(f"mazu: {path_given + folders_right_format[i]}")



    def main():
        cutoff_days = calc_cutoffdays()
        print(f"- V každé složce bude zachováno: {files_to_keep} souborů\n")
        if more_dirs == True:
            if del_option == 0:
                print(f"- Probíhá mazání obrázků v cestě: {path_given}\na ve všech podružných složkách (maximum je 6 subsložek)")
                all_paths = subfolders_check()
                for paths in all_paths:
                    print(f"- Prochazím cestu: {paths}")
                    files_checked = 0
                    deleted_count = 0
                    
                    for files in os.listdir(paths):
                        mod_date_of_file = get_mod_date_of_file(paths,files)
                        if mod_date_of_file != False:
                            files_split = files.split(".")
                            if (files_split[len(files_split)-1]) in supported_formats:
                                if mod_date_of_file < cutoff_days:
                                    files_checked = files_checked + 1
                                    if files_checked > files_to_keep:
                                        print(f"mazu: {paths + files}")
                                        #os.remove(paths + files)
                                        deleted_count = deleted_count + 1
                    if deleted_count != 0:
                        print(f"Smazáno souborů: {deleted_count}")

            #if del_option == 1:
                #print(f"- Probíhá mazání složek v cestě: {path_given}\na ve všech podružných složkách (maximum je 6 subsložek)")

        else:
            if del_option == 0:
                print(f"- Probíhá mazání obrázků v cestě: {path_given}")
                files_checked = 0
                deleted_count = 0
                for files in os.listdir(path_given):
                    mod_date_of_file = get_mod_date_of_file(path_given,files)
                    if mod_date_of_file != False:
                        files_split = files.split(".")
                        if (files_split[len(files_split)-1]) in supported_formats:
                            if mod_date_of_file < cutoff_days:
                                files_checked = files_checked + 1
                                if files_checked > files_to_keep:
                                    print(f"mazu: {path_given + files}")
                                    #os.remove(path_given + files)
                                    deleted_count = deleted_count + 1
                if deleted_count != 0:
                    print(f"- Smazáno souborů: {deleted_count}")

            if del_option == 1:
                format_error = False
                print(f"- Probíhá mazání složek, jejichž název = datum, v cestě: {path_given}")
                result = get_format_dir_name()
                for items in result:
                    if items == False:
                        format_error = True
                if format_error == False:
                    found_separator = result[0]
                    found_format = result[1]
                    folders_right_format = result[2]
                    del_directories(found_separator,found_format,folders_right_format)
                

                

    
    main()


whole_deleting_function("C:/Users/kubah/Desktop/JHV/mazani_test/",False,1)
#whole_deleting_function("C:/Users/kubah/Desktop/JHV/test_images/",True)