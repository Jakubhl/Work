import os
import datetime
from datetime import datetime
import shutil
import re

#supported_formats = []
#file1 = open('supported_formats.txt', 'r')
#Lines = file1.readlines()
#unwanted_chars = ["\n","\"","[","]"]
#for chars in unwanted_chars:
#    if chars in Lines[4]:
#        Lines[4] = Lines[4].replace(chars,"")
    
#list1 = Lines[4].split(",")
#for items in list1:
#    supported_formats.append(str(items))
#supported_formats = ["jpg","bmp","png","ifz"]
# podporovane formaty u adresaru:
to_delete_folder = "Ke_smazani"
supported_date_formats = ["YYYYMMDD","DDMMYYYY","YYMMDD"]
supported_separators = [".","/","_"]
output = []
output_console2 = []



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
        now = datetime.now()
        dt_string = now.strftime("%Y%m%d%H%M%S")
        readable_today = now.strftime("%d.%m.%Y")
        #print(f"\n- Dnes je: {readable_today}")
        return [dt_string,readable_today]

def whole_deleting_function(path_given,more_dirs,del_option,files_to_keep,cutoff_date_given,supported_formats,testing_mode):
    """
    Funkce pro mazání souborů

    vrací záznam výstupních zpráv: output

    vstupními parametry jsou: 
    
    1 path_given (cesta k souborům)\n
    2 more_dirs (zda procházet subsložky)\n
    3 del_option (vybraná možnost mazání)\n
    4 files_to_keep (počet minimálního počtu souborů k ponechání)\n
    5 cutoff_date_given (rozhodovací datum)\n
    6 supported_formats (seznam podporovaných formátů)\n
    7 testing_mode (režim testování)\n
    """
    #files_to_keep = 30
    max_days_old = 365

    def make_dir(name,path):
        if not os.path.exists(path + name): #pokud uz neni vytvorena, vytvor...
            os.mkdir(path + name + "/")

    def collect_to_delete_folder(path):
        """
        Funkce sesbírá soubory ze složky, ve které jsou soubory určené ke smazání z testing módu
        """
        if os.path.exists(path + to_delete_folder):
            for files in os.listdir(path + to_delete_folder):
                if os.path.exists(path + to_delete_folder + "/" + files):
                    shutil.move(path + to_delete_folder + "/" + files , path + files)

    def sync_folders(path):
        folders = []
        for files in os.listdir(path):
            if os.path.isdir(path + files):
                if files != to_delete_folder:
                    folders.append(files)

        return folders
     
    def get_mod_date_of_file(path,file):
        if os.path.isdir(path + file) == False:
            mod_date_timestamp = os.path.getmtime(path + file)
            mod_date = datetime.fromtimestamp(mod_date_timestamp)
            #mod_date_str = mod_date.strftime("%Y%m%d%H%M%S")
            mod_date_str = mod_date.strftime("%Y%m%d")
            return mod_date_str
        else:
            return False

    def calc_cutoffdays():
        current_date = get_current_date()
        current_date = current_date[0]
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
        #output.append(f"- Smažou se soubory starší než: {readable_cutoff_date}\n")
        return [cutoff_date,readable_cutoff_date]
    
    def calc_cutoffdays_given():
        given_day = str(cutoff_date_given[0])
        given_month = str(cutoff_date_given[1])
        if len(given_day) == 1:
            given_day = "0" + given_day
        if len(given_month) == 1:
            given_month = "0" + given_month

        cutoff_date = str(cutoff_date_given[2])+given_month+given_day
        readable_cutoff_date = given_day + "." + given_month + "." + str(cutoff_date_given[2])
        print(cutoff_date,readable_cutoff_date)
        return [cutoff_date,readable_cutoff_date]
    
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
            output.append(f"- Separátor automaticky nastaven na: {found_separator}\nPravděpodobnost správné detekce: {probability} %\n")

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
                for i in range(0,len(supported_date_formats)):
                    if max(count_of_found_formats) == count_of_found_formats[i]:
                        found_format = supported_date_formats[i]
                        probability = (max(count_of_found_formats)/sum(count_of_found_formats))*100
                        probability = "%.2f" % (probability) #prevod na dve desetinna mista
                print(f"- Formát automaticky nastaven na: {found_format}\nPravděpodobnost správné detekce: {probability} %")
                output.append(f"- Formát automaticky nastaven na: {found_format}\nPravděpodobnost správné detekce: {probability} %\n")

                if found_format == supported_date_formats[0]:
                    folders_right_format = folders_format1
                elif found_format == supported_date_formats[1]:
                    folders_right_format = folders_format2
                elif found_format == supported_date_formats[2]:
                    folders_right_format = folders_format3
                return [found_separator,found_format,folders_right_format]
            
            else:
                print(f"- Chyba: V zadané cestě nebyly nalezeny žádné podporované formáty názvu složek {supported_date_formats} pro vybraný způsob mazání")
                output.append(f"- Chyba: V zadané cestě nebyly nalezeny žádné podporované formáty názvu složek {supported_date_formats} pro vybraný způsob mazání\n")
                return [False,False,False]
        else:
            print(f"- Chyba: V zadané cestě nebyly nalezeny žádné podporované separátory v názvu složek {supported_separators} pro vybraný způsob mazání")
            output.append(f"- Chyba: V zadané cestě nebyly nalezeny žádné podporované separátory v názvu složek {supported_separators} pro vybraný způsob mazání\n")
            return [False,False,False]
        
    def del_directories(found_separator,found_format,folders_right_format):
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

        cutoff_days = calc_cutoffdays_given()
        cutoff_days = cutoff_days[0]
        for i in range(0,len(folders_without_separators)):
            #if int(folders_without_separators[i]) < int(cutoff_days[:8]):
            directories_checked +=1
            if int(folders_without_separators[i]) < int(cutoff_days):
                deleted_directores +=1
                if testing_mode == True:
                    print(f"Mazání: {path_given + folders_right_format[i]}")
                if testing_mode == False:
                    print(f"Mazání: {path_given + folders_right_format[i]}")
                    #shutil.rmtree(path_given + folders_right_format[i])
        
        if deleted_directores == 0:
            output.append(f"- Zkontrolováno adresářů: {directories_checked}\n")
            output.append("Nebyly nalezeny žádné adresáře určené ke smazání\n")
        else:
            output.append(f"- Zkontrolováno adresářů: {directories_checked}\n")
            if testing_mode == True:
                output.append(f"Smazalo by se adresářů: {deleted_directores}\n")
            else:
                output.append(f"Smazáno adresářů: {deleted_directores}\n")

    def del_files(path,cutoff_days,option):
        older_files_checked = 0
        newer_files_checked = 0
        files_checked = 0
        deleted_count = 0
        collect_to_delete_folder(path)
        
        if option == 0:
            for files in os.listdir(path):
                mod_date_of_file = get_mod_date_of_file(path,files)
                if mod_date_of_file != False:
                    files_split = files.split(".")
                    if (files_split[len(files_split)-1]) in supported_formats:
                        files_checked +=1
                        if int(mod_date_of_file) < cutoff_days:
                            older_files_checked +=1
                            if older_files_checked > files_to_keep:
                                deleted_count +=1
                                if testing_mode == True:
                                    #print(f"Mazání: {path + files}")
                                    make_dir(to_delete_folder,path)
                                    shutil.move(path + files , path + to_delete_folder + '/' + files)
                                if testing_mode == False:
                                    print(f"Mazání: {path + files}")
                                    #os.remove(path + files)
                                
        if option == 1:
            for files in os.listdir(path):
                mod_date_of_file = get_mod_date_of_file(path,files)
                if mod_date_of_file != False:
                    files_split = files.split(".")
                    if (files_split[len(files_split)-1]) in supported_formats:
                        files_checked +=1
                        if int(mod_date_of_file) < cutoff_days:
                            deleted_count +=1
                            if testing_mode == True:
                                #print(f"Mazání: {path + files}")
                                make_dir(to_delete_folder,path)
                                shutil.move(path + files , path + to_delete_folder + '/' + files)
                            if testing_mode == False:
                                print(f"Mazání: {path + files}")
                                #os.remove(path + files)
                        else:
                            newer_files_checked +=1
                            if newer_files_checked > files_to_keep:
                                deleted_count +=1
                                if testing_mode == True:
                                    #print(f"Mazání: {path + files}")
                                    make_dir(to_delete_folder,path)
                                    shutil.move(path + files , path + to_delete_folder + '/' + files)
                                if testing_mode == False:
                                    print(f"Mazání: {path + files}")
                                    #os.remove(path + files)
        
        #mazani potencionalne prazdne slozky
        number_of_files = 0
        if os.path.exists(path + to_delete_folder):
            for files in os.listdir(path + to_delete_folder):
                number_of_files +=1
            if number_of_files == 0:
                os.rmdir(path+to_delete_folder)

        if deleted_count == 0:
            output.append(f"- Zkontrolováno souborů: {files_checked}\n")
            output.append("- Nebyly nalezeny žádné soubory určené ke smazání\n\n")
        else:
            print(f"Smazáno souborů: {deleted_count}")
            output.append(f"- Zkontrolováno souborů: {files_checked}\n")
            if testing_mode == True:
                output.append(f"Smazalo by se: {deleted_count} souborů\n\n")
            else:
                output.append(f"Smazáno souborů: {deleted_count}\n\n")

        return deleted_count

    def main():
        result_cutoffdays = calc_cutoffdays_given()
        cutoff_days = int(result_cutoffdays[0])
        
        if more_dirs == True: #////////////////////////////////////////////////////////// MORE_DIRS //////////////////////////////////////////////////////////////////////////
            if del_option == 1: #//////////////////////////////////////////////////////// OPTION 1 ///////////////////////////////////////////////////////////////////////////
                total_deleted_count = 0
                print(f"- Probíhá mazání obrázků v cestě: {path_given}\na ve všech podružných složkách (maximum je 6 subsložek)")
                output.append(f"- Probíhá mazání obrázků v cestě: {path_given}\na ve všech podružných složkách (maximum je 6 subsložek)\n")
                print(f"- V každé složce bude zachováno: {files_to_keep} souborů\n")
                output.append(f"- V každé složce bude zachováno: {files_to_keep} souborů\n\n")
                all_paths = subfolders_check()
                for paths in all_paths:
                    output_console2.append(f"{paths}\n")
                    print(f"- Prochazím cestu: {paths}")
                    output.append(f"- Probíhá mazání obrázků v cestě: {paths}\n")
                    deleted = del_files(paths,cutoff_days,0)
                    total_deleted_count = total_deleted_count+deleted
                
                output.append(f"- Mazání dokončeno, celkem smazáno souborů: {total_deleted_count}\n")
            if del_option == 2: #///////////////////////////////////////////////////////// OPTION 2 /////////////////////////////////////////////////////////////////////////////
                total_deleted_count = 0
                all_paths = subfolders_check()
                print(f"- V každé složce bude zachováno: {files_to_keep} souborů, novějších než {result_cutoffdays[1]}\n")
                output.append(f"- V každé složce bude zachováno: {files_to_keep} souborů, novějších než {result_cutoffdays[1]}\n")
                for paths in all_paths:
                    print(f"- Probíhá mazání obrázků v cestě: {paths}")
                    output.append(f"- Probíhá mazání obrázků v cestě: {paths}\n")
                    deleted = del_files(paths,cutoff_days,1)
                    total_deleted_count = total_deleted_count+deleted

                output.append(f"- Mazání dokončeno, celkem smazáno souborů: {total_deleted_count}\n")
            if del_option == 3: #///////////////////////////////////////////////////////// OPTION 3 /////////////////////////////////////////////////////////////////////////////
                print("Pro tuto možnost mazání není možné procházet subadresáře")
                output.append("Pro tuto možnost mazání není možné procházet subadresáře\n")       

        if more_dirs == False: #////////////////////////////////////////////////////////// ONE_PATH //////////////////////////////////////////////////////////////////////////
            if del_option == 1: #////////////////////////////////////////////////////////// OPTION 1 ////////////////////////////////////////////////////////////////////////////
                 # tato moznost provadi mazani pouze starsich a uchovavani nejakeho poctu pouze starsich souboru
                print(f"- Probíhá mazání obrázků v cestě: {path_given}")
                output.append(f"- Probíhá mazání obrázků v cestě: {path_given}\n")
                print(f"- Ve složce bude zachováno: {files_to_keep} souborů\n")
                output.append(f"- Ve složce bude zachováno: {files_to_keep} souborů\n")
                del_files(path_given,cutoff_days,0)
                output.append("- Mazání dokončeno\n")

            if del_option == 2: #///////////////////////////////////////////////////////// OPTION 2 /////////////////////////////////////////////////////////////////////////////
                # tato moznost provadi mazani vsech starsich a redukuje novejsi (vhodne u generovani velkeho poctu obrazku za kratky cas)
                print(f"- Probíhá mazání obrázků v cestě: {path_given}")
                output.append(f"- Probíhá mazání obrázků v cestě: {path_given}\n")
                print(f"- Ve složce bude zachováno: {files_to_keep} souborů, novějších než {result_cutoffdays[1]}\n")
                output.append(f"- Ve složce bude zachováno: {files_to_keep} souborů, novějších než {result_cutoffdays[1]}\n")
                del_files(path_given,cutoff_days,1)
                output.append("- Mazání dokončeno\n")
                
            if del_option == 3: #///////////////////////////////////////////////////////// OPTION 2 /////////////////////////////////////////////////////////////////////////////
                # tato moznost provadi mazani slozek s datumem v jejich nazvu
                format_error = False
                print(f"- Probíhá mazání složek, jejichž název = datum, v cestě: {path_given}")
                output.append(f"- Probíhá mazání složek, jejichž název = datum, v cestě: {path_given}\n")
                result = get_format_dir_name()
                for items in result:
                    if items == False:
                        format_error = True
                if format_error == False:
                    found_separator = result[0]
                    found_format = result[1]
                    folders_right_format = result[2]
                    del_directories(found_separator,found_format,folders_right_format)
                output.append("- Mazání dokončeno\n")

    
    main()
    return output

#whole_deleting_function("C:/Users/kubah/Desktop/JHV/mazani_test/20.10.2023/",False,1)
#whole_deleting_function("C:/Users/kubah/Desktop/JHV/test_images/",True)