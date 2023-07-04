import os
import shutil
import re

#globals:
nok_folder = "Temp"
prefix_func = "Func_"
prefix_Cam = "Cam_"
supported_formats = ["bmp","png"]

def path_check(path_raw):
    path=path_raw
    print("-Třídění souborů z průmyslových kamer...\n")

    #opravy cesty k souborům:
    backslash = "\ "
    if backslash[0] in path:
        newPath = path.replace(os.sep, '/')
        path = newPath

    if path.endswith('/') == False:
        newPath = path + "/"
        path = newPath

    if not os.path.exists(path):
        return False

    else:
        return path

class Folders:

    def __init__(self,path):
        self.path = path

    def make_dir(self,name):
        if not os.path.exists(self.path + name): #pokud uz neni vytvorena, vytvor...
            os.mkdir(self.path + name + "/")

    def sync_folders(self):
        folders = []
        for files in os.listdir(self.path):
            if os.path.isdir(self.path + files):
                folders.append(files)

        return folders

    def remove_empty(self,folders):
        removed_count = 0
        for dirs in folders: # pole folders uz je filtrovano od ostatnich souboru...
            number_of_files = 0
            if os.path.exists(self.path + dirs):
                for files in os.listdir(self.path + dirs):
                    number_of_files +=1
                if number_of_files == 0:
                    print(f"-Odstraněna prázdná složka: {dirs}")
                    os.rmdir(self.path + dirs)
                    removed_count +=1
        if removed_count != 0:
            print("-Přebytečné složky odstraněny\n")

class Sorting:
    def __init__(self,path):
        self.error = False
        self.path = path
        self.cam_number_digits = 5 + 4 #az peticiferne cislo kamery (+ 4 znaky za &)
        self.functions_arr = []
        self.cameras_arr = []
        self.both_arr = []
        self.files_type_arr = []
        self.file_list = []

    def Collect_files(self):
        #folds = Folders(self.path)
        folders = Folders(self.path).sync_folders()

        for i in range(0,len(folders)):
            for files in os.listdir(self.path + folders[i]):
                if len(files.split(".")) == 3:
                    if files.split(".")[2] in supported_formats:
                        if os.path.exists(self.path + folders[i] + "/" + files):
                            shutil.move(self.path + folders[i] + "/" + files , self.path + '/' + files)

    def Get_cam_number(file_for_analyze):
        if "&" in file_for_analyze:
            files_split = file_for_analyze.split("&")
            files_split = files_split[1] # prava strana od &
            files_split = files_split.split(".")
            files_split = files_split[0] # leva strana od tecky
            files_split = re.findall(r'\d+', files_split)
            cam_number = ' '.join([str(elem) for elem in files_split]) #ziskani stringu z pole

            return cam_number
        else:
            print("-Chyba: soubor {} neobsahuje rozhodovaci symbol \"&\"\n".format(file_for_analyze))
            return False

    def Get_cam_num_list(self):
        cam_num_list = []
        for files in self.file_list:
            cam_number = Sorting.Get_cam_number(files)
            if (cam_number not in cam_num_list) and (cam_number != False):
                cam_num_list.append(cam_number)
        
        return cam_num_list
        
    def Get_func_number(file_for_analyze):
        files_split = file_for_analyze.split("&")
        files_split = files_split[0] # leva strana od &
        files_split = files_split.split("_") 
        if len(files_split) != 0:
            arr_pos = len(files_split) -2 #-2, protože pole se pocita od nuly a nezajima nas znak _ před &
            func_number = files_split[arr_pos] 

            return func_number
        else:
            print("-Chyba: soubor {} neobsahuje rozhodovaci symbol \"_\", potrebny pro urceni cisla funkce\n".format(file_for_analyze))
            return False

    def Get_func_list(self):
        func_list = []
        for files in self.file_list:
            func_number = Sorting.Get_func_number(files)
            if (func_number not in func_list) and (func_number != False):
                func_list.append(func_number)
        
        return func_list

    def Get_both_list(self):
        both_list = []
        for files in self.file_list:
            func_number = Sorting.Get_func_number(files)
            cam_number = Sorting.Get_cam_number(files)
            if func_number != False and cam_number != False:
                if prefix_func + func_number + "_" + prefix_Cam + cam_number not in both_list:
                    both_list.append(prefix_func + func_number + "_" + prefix_Cam + cam_number)
        
        return both_list    

    def Get_suffix(self):
        files_type = ""
        #zjišťování počtu typů souborů
        for files in os.listdir(self.path):
            if len(files.split(".")) == 3:
                if files.split(".")[2] in supported_formats:
                    self.file_list.append(files)
                    files_type = files.split(".")
                    if not files_type[1] in self.files_type_arr:
                        self.files_type_arr.append(files_type[1])

        if self.files_type_arr != []: #pokud byl nalezen
            print(f"-Nalezené typy souborů: {self.files_type_arr}\n")

        return self.files_type_arr
            
    def Sorting_files(self,sort_option,folder_list):
        n = 0
        hide_cnt = 4
        files_arr_cut = []
        files_cut = 0
        nok_count = 0
        ok_count = 0
        cutting_condition = "&"
        count=0
        error_length = 0

        # výtah z názvu vhodný pro porovnání:
        for files in self.file_list:
            files_cut = files.split(cutting_condition)
            files_cut = files_cut[0]
            hide_cnt_from_start = len(files_cut) - int(hide_cnt)
            files_arr_cut.append(files_cut[0:(hide_cnt_from_start)])        

        for i in range(0,len(files_arr_cut)):

            for files in files_arr_cut:
                if len(files) != len(files_arr_cut[i]):
                    error_length = 1
                if files == files_arr_cut[i]:
                    count+=1
            
            if count == len(self.files_type_arr): # overeni zda je od vsech typu souboru jeden
                ok_count += 1
                if sort_option == "by_format":
                    for formats in self.files_type_arr:
                        if self.file_list[i].split(".")[1] == formats:
                            if os.path.exists(self.path + self.file_list[i]):
                                shutil.move(self.path + self.file_list[i] , self.path + formats + "/" + self.file_list[i])

                elif sort_option == "by_func_number":
                    for func_numbers in folder_list:
                        if Sorting.Get_func_number(self.file_list[i]) == func_numbers:
                            if os.path.exists(self.path + self.file_list[i]):
                                shutil.move(self.path + self.file_list[i] , self.path + prefix_func + func_numbers + "/" + self.file_list[i])

                elif sort_option == "by_cam_number":
                    for cam_numbers in folder_list:
                        if Sorting.Get_cam_number(self.file_list[i]) == cam_numbers:
                            if os.path.exists(self.path + self.file_list[i]):
                                shutil.move(self.path + self.file_list[i] , self.path + prefix_Cam + cam_numbers + "/" + self.file_list[i])

                elif sort_option == "by_both":
                    for both in folder_list:
                        if (prefix_func + Sorting.Get_func_number(self.file_list[i]) + "_" + prefix_Cam + Sorting.Get_cam_number(self.file_list[i])) == both:
                            if os.path.exists(self.path + self.file_list[i]):
                                shutil.move(self.path + self.file_list[i] , self.path + both + "/" + self.file_list[i])
                count = 0
                
            else:
                nok_count += 1
                if os.path.exists(self.path + self.file_list[i]):
                    shutil.move(self.path + self.file_list[i] , self.path + nok_folder + "/" + self.file_list[i]) #přesun do Temp složky
                #del self.file_list[i]
                count = 0
        
        if error_length == 1:
            print("-Upozornění: délka názvu před \"&\" některých souborů v dané cestě se liší (možná nefunkční manuální definice zakrytých znaků)\n")
            
        if self.file_list == []:
            print("-Chyba: Nebyly nalezeny žádné soubory\n")
            self.error = True

        else:
            print(f"-Nepáry, celkem: {nok_count}\n-OK soubory zastoupené všemi formáty, celkem: {ok_count}\n")

        return self.error

def subfolders_check(path_given):
    #STAGE1///////////////////////////////////////////////////
    path = path_given
    fold = Folders(path)
    folders = fold.sync_folders()
    path_list_not_found  = []
    for folds in folders:
        count = 0
        for files in os.listdir(path + folds):
            if len(files.split(".")) == 3:
                if files.split(".")[2] in supported_formats:
                    count+=1
        if count ==0:
            path_list_not_found.append(path + folds)
    
    #STAGE2///////////////////////////////////////////////////
    path_list_not_found_st2  = []
    paths_to_folders = []
    if len(path_list_not_found) != 0:
        for paths in path_list_not_found:
            fold = Folders(paths + "/")
            folders = fold.sync_folders()
            for folds in folders:
                count = 0
                path_x = paths + "/" + folds
                
                for files in os.listdir(path_x):
                    if len(files.split(".")) == 3:
                        if files.split(".")[2] in supported_formats:
                            count+=1
                            if os.path.isdir(path_x + "/"):
                                if not path_x + "/" in paths_to_folders:
                                    paths_to_folders.append(path_x + "/")
                if count ==0:
                    path_list_not_found_st2.append(paths + "/"  + folds)
    #STAGE3///////////////////////////////////////////////////
    path_list_not_found_st3  = []
    if len(path_list_not_found_st2) != 0:
        for paths in path_list_not_found_st2:
            fold = Folders(paths+ "/")
            folders = fold.sync_folders()                                                               
            for folds in folders:
                count = 0
                for files in os.listdir(paths + "/" + folds):
                    if len(files.split(".")) == 3:
                        if files.split(".")[2] in supported_formats:
                            count+=1
                            if os.path.isdir(paths + "/"):
                                if not paths + "/" in paths_to_folders:
                                    paths_to_folders.append(paths + "/")                           
                if count ==0:
                    path_list_not_found_st3.append(paths + "/"  + folds)

    if len(paths_to_folders) !=0:
        return paths_to_folders 
    else:
        return False

def main():
    path_raw = ""
    path_raw = input("Zadejte cestu k souborům (pokud se aplikace už nachází v dané složce -> enter): ")
    #path_raw = "D:\JHV\Kamery\JHV_Data/"

    #spusteni v souboru, kde se aplikace aktualne nachazi
    if path_raw == "":
        path_raw = os.getcwd()
        path = path_check(path_raw)
    else:
        path = path_check(path_raw)

    if path == False:
        print("Zadaná cesta k souborům nebyla nalezena\n")
        main() #opakovat znovu...
    else:
        folds = Folders(path) #definice cesty pro classu folders
        folds.make_dir(nok_folder) #vytvoreni zakladnich slozek
        folders = folds.sync_folders()

        s=Sorting(path)
        s.Collect_files()
        formats_found = s.Get_suffix()

        for formats in formats_found:
            folds.make_dir(formats)

        error = s.Sorting_files("by_format",None)
        folds.remove_empty(folders)
        folders = folds.sync_folders()
        
        if error == True:
            print("-Zkouším, zda nejsem v adresáři s více složkami (například v adresáři se složkami s datumy)")
            result = subfolders_check(path)
            if result == False:
                print("-Ne, nejsem...\nTřídění ukončeno\n")
            else:
                print(f"Ano, jsem... Mám spustit třídění pro všechny nalezené cesty?\n\n{result}\n")
                confirm = input("[y/Y] / [libovolný znak pro ukončení]:")
                if confirm.casefold() == "y":
                    for paths in result:
                        if os.path.exists(paths):
                            print(f"Probíhá třídění v cestě: {paths}")
                            folds = Folders(paths)
                            folds.make_dir(nok_folder)
                            folders = folds.sync_folders()

                            s=Sorting(paths)
                            s.Collect_files()
                            formats_found = s.Get_suffix()

                            for formats in formats_found:
                                folds.make_dir(formats)

                            s.Sorting_files("by_format",None)
                            folds.remove_empty(folders)

        if error != True:
            advanced_mode = input("Nastavit možnosti podrobnějšího třídění?: [Y/y] / [libovolný znak pro uzavření]: ")
            if advanced_mode.casefold() == "y":
                picked = False
                while(picked == False):
                    sort_option = input("Třídit podle formátu? (0) čísla funkce? (1), podle čísla kamery? (2), podle funkce i kamery? (3)\n")
                    s=Sorting(path) #refresh promennych
                    if int(sort_option) == 0:
                        s.Collect_files()
                        formats_found = s.Get_suffix()
                        for formats in formats_found:
                            folds.make_dir(formats)
                        s.Sorting_files("by_format",None)
                        folds.remove_empty(folders)
                        picked = True

                    elif int(sort_option) == 1:
                        s.Collect_files()
                        functions_found = s.Get_func_list()
                        for functions in functions_found:
                            folds.make_dir(prefix_func + functions)
                        s.Sorting_files("by_func_number",functions_found)
                        folds.remove_empty(folders)
                        picked = True

                    elif int(sort_option) == 2:
                        s.Collect_files()
                        cam_numbers_found = s.Get_cam_num_list()
                        for cam_num in cam_numbers_found:
                            folds.make_dir(prefix_Cam + cam_num)
                        s.Sorting_files("by_cam_number",cam_numbers_found)
                        folds.remove_empty(folders)
                        picked = True

                    elif int(sort_option) == 3:
                        s.Collect_files()
                        both_found = s.Get_both_list()
                        for both in both_found:
                            folds.make_dir(both)
                        s.Sorting_files("by_both",both_found)
                        folds.remove_empty(folders)
                        picked = True
                    else:
                        print("-Mimo rozsah, zkuste znovu")
            else:
                print("-Třídění ukončeno")

main()