import os
import shutil
import re

#globals:
nok_folder = "Temp"
prefix_func = "Func_"
prefix_Cam = "Cam_"
supported_formats = ["bmp","png"]
pair_folder = "PAIRS"
forbidden_folders = [pair_folder]
output = []
output_console2 = []

def path_check(path_raw):
    path=path_raw
    #print("-Třídění souborů z průmyslových kamer...\n")

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
def whole_sorting_function(path_given,selected_sort,more_dir,max_num_of_pallets_given,ID_num_of_digits_given):
    max_num_of_pallets = max_num_of_pallets_given
    ID_num_of_digits = ID_num_of_digits_given
    path = path_given
    sort_option = selected_sort-1
    more_dirs = more_dir

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
                    if files not in forbidden_folders:
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
                output.append("-Chyba: soubor {} neobsahuje rozhodovaci symbol \"&\"\n".format(file_for_analyze))
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
                output.append("-Chyba: soubor {} neobsahuje rozhodovaci symbol \"_\", potrebny pro urceni cisla funkce\n".format(file_for_analyze))
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
                output.append(f"-Nalezené typy souborů: {self.files_type_arr}\n")

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
            
            #if error_length == 1:
                #print("-Upozornění: délka názvu před \"&\" některých souborů v dané cestě se liší (možná nefunkční manuální definice zakrytých znaků)\n")
                
            if self.file_list == []:
                output.append("-Chyba: Nebyly nalezeny žádné soubory\n")
                self.error = True

            else:
                self.error = False
                output.append(" - Nepáry, celkem: {}".format(nok_count))
                output.append(" - OK soubory zastoupené všemi formáty, celkem: {}".format(ok_count))
            return self.error
        
        def sort_by_ID(self, path_given, max_num_of_pallets, ID_num_of_digits):
            path = path_given
            max_number_of_pallets = max_num_of_pallets
            ID_number_of_digits = ID_num_of_digits

            list_of_pairs = []
            pair_file_list = []
            lost_pallets = []
            list_of_pairs_clear = []
            list_of_pair_count = []

            compare_num = ""
            count = 0
            round_number = 0
            ref_file = self.file_list[0]
            increment=int(Sorting.Get_func_number(ref_file)) #reference aby palety nezacinaly vzdy on nuly
            
            #hledani vice souboru (dvojic)---------------------------------------------------------------------------
            mes_send = False #jen jednou za slozku... at nespamuje
            for files in self.file_list: #hledani v listu se soubory
                #if ".bmp" in files: #pouze pro overeni, zda se jedna o uzitecny soubor
                numbers = Sorting.Get_func_number(files)
                if len(numbers) == ID_number_of_digits:
                    keep_searching = True
                    pair_file_list.append(files + "_" + str(round_number))
                    while(keep_searching == True): #while cyklus kvuli moznym chybejicim paletkam
                        if numbers[1] != "9": #nevsimame si cisel 900+
                            if increment>max_number_of_pallets:
                                increment=0
                                round_number +=1
                            if increment < 10:
                                compare_num = "000"+str(increment)
                            if increment >= 10:
                                compare_num = "00"+str(increment)
                            if compare_num == numbers:
                                count +=1
                                
                                if count > len(self.files_type_arr):
                                    if numbers not in list_of_pairs: # blok pro zajisteni pouze jednoho vyskytu v poli v rade V JEDNE SADE (0-55)
                                        if len(list_of_pairs_clear) != 0:
                                            if list_of_pairs_clear[len(list_of_pairs_clear)-1] != numbers:
                                                list_of_pairs_clear.append(numbers)
                                        else:
                                            list_of_pairs_clear.append(numbers)

                                        numbers_with_round = numbers + "_sada_cislo_" + str(round_number)
                                        if len(list_of_pairs) != 0:
                                            if list_of_pairs[len(list_of_pairs)-1] != numbers_with_round:
                                                list_of_pairs.append(numbers_with_round)
                                        else:
                                            list_of_pairs.append(numbers_with_round)

                                keep_searching = False #zavolame dalsi cislo...

                            else:
                                if(count < len(self.files_type_arr)): #ztracena jen pokud tam je mene jak dva soubory
                                    lost_pallets.append(compare_num)
                                increment+=1
                                if count >= len(self.files_type_arr)*2:
                                    list_of_pair_count.append(count) #pocet souboru, ktere musi algoritmus vyhledat
                                count = 0
                                    
                        else:
                            keep_searching = False
                else:
                    if mes_send == False: #at nezaspamuje cely terminal...
                        output.append("- Chyba: délka ID před znakem: _& není rovna ",ID_number_of_digits,"...\n",files,"\n V cestě:",path )
                        mes_send = True

            if len(list_of_pairs_clear) !=0:
                output.append("- Nalezený seznam dvojic v řadě za sebou podle ID:",list_of_pairs_clear,"\n- Každá v počtu souborů:",list_of_pair_count)

            if len(lost_pallets) !=0:
                output.append("- Seznam čísel chybějících palet v řadě za sebou: ",lost_pallets)
            else:
                output.append("- Žádné chybějící palety nubyly nenalezeny")

            if len(list_of_pairs) != 0: #jestli nejake vubec jsou...
                #vytvoreni slozky s páry:
                if not os.path.exists(path + pair_folder):
                    os.mkdir(path + pair_folder)
                j=0
                x=0
                #kopirovani do zvlastni slozky------------------------------------------------------------------
                for numbers in list_of_pairs:
                    for files in pair_file_list:                    
                        files_splitted = files.split("_")
                        q=0
                        files_full_name = ""

                        for characters in files_splitted:#takto slozite pro pripad viceciferneho cisla kola
                            if q<8 and q<1:
                                files_full_name =  files_full_name + characters
                            if q<8 and q>=1:
                                files_full_name =  files_full_name +"_"+ characters
                            q+=1

                        if (numbers[:4] == Sorting.Get_func_number(files)) and (numbers.split("_")[3] == files.split("_")[8]):
                            if j < int(list_of_pair_count[x]):
                                if not os.path.exists(path + pair_folder + '/' + files_full_name): #jestli uz tam jsou nebude je to kopirovat znova...
                                    shutil.copy(path + files_full_name , path + pair_folder + '/' + files_full_name)
                                j+=1  
                    j=0
                x+=1
    def subfolders_check(path_given):
        #STAGE1///////////////////////////////////////////////////
        path = path_given
        fold = Folders(path)
        folders = fold.sync_folders()
        path_list_not_found  = []
        for folds in folders:
            count = 0
            for files in os.listdir(path + folds):
                if len(files.split(".")) == 3: #tri bloky rozdelene teckou x.x.bmp/png
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
        if more_dirs == True:
            result = subfolders_check(path)
            if result == False:
                output_console2.append("- Chyba: aplikace programovana na pruchod 3 slozek, tzn.: path + \"2023_04_13/A/Height\"")
            else:
                output_console2.append("- Prochazím tyto cesty: ")
                for items in result:
                    output_console2.append(items+"\n")

                for paths in result:
                    if os.path.exists(paths):
                        output.append("\nTrideni v: " + paths)
                        folds = Folders(paths)
                        folds.make_dir(nok_folder)
                        folders = folds.sync_folders()

                        s=Sorting(paths)
                        if int(sort_option) == 0:
                            s.Collect_files()
                            formats_found = s.Get_suffix()
                            for formats in formats_found:
                                folds.make_dir(formats)
                            s.Sorting_files("by_format",None)
                            folders = folds.sync_folders()
                            folds.remove_empty(folders)

                        elif int(sort_option) == 1:
                            s.Collect_files()
                            s.Get_suffix()
                            functions_found = s.Get_func_list()
                            for functions in functions_found:
                                folds.make_dir(prefix_func + functions)
                            s.Sorting_files("by_func_number",functions_found)
                            folders = folds.sync_folders()
                            folds.remove_empty(folders)

                        elif int(sort_option) == 2:
                            s.Collect_files()
                            s.Get_suffix()
                            cam_numbers_found = s.Get_cam_num_list()
                            for cam_num in cam_numbers_found:
                                folds.make_dir(prefix_Cam + cam_num)
                            s.Sorting_files("by_cam_number",cam_numbers_found)
                            folders = folds.sync_folders()
                            folds.remove_empty(folders)

                        elif int(sort_option) == 3:
                            s.Collect_files()
                            s.Get_suffix()
                            both_found = s.Get_both_list()
                            for both in both_found:
                                folds.make_dir(both)
                            s.Sorting_files("by_both",both_found)
                            folders = folds.sync_folders()
                            folds.remove_empty(folders)

                        elif int(sort_option) == 4: #hledani dvojic (nejprve podle formatu, pote v kazde slozce hleda dvojice) jnak by neslo kdyby uz byly ve slozkach nebo naopak
                            s.Collect_files() 
                            formats_found = s.Get_suffix()
                            for formats in formats_found:
                                folds.make_dir(formats)
                            s.Sorting_files("by_format",None)
                            folders = folds.sync_folders()
                            folds.remove_empty(folders)
         
                            for formats in formats_found: #hledání bude provedeno ve všech složkách podle suffixu
                                s.Get_suffix() #nutne pro vytvoreni pole se soubory v kazde slozce
                                s.sort_by_ID(path+formats,max_num_of_pallets,ID_num_of_digits)
                            
        else: #nebylo zaskrtnuto prochazet vice souboru

            folds = Folders(path) #definice cesty pro classu folders
            folds.make_dir(nok_folder) #vytvoreni zakladnich slozek
            folders = folds.sync_folders()
            s=Sorting(path)
            if int(sort_option) == 0:
                s.Collect_files()
                formats_found = s.Get_suffix()
                for formats in formats_found:
                    folds.make_dir(formats)
                s.Sorting_files("by_format",None)
                folders = folds.sync_folders()
                folds.remove_empty(folders)

            elif int(sort_option) == 1:
                s.Collect_files()
                s.Get_suffix()
                functions_found = s.Get_func_list()
                for functions in functions_found:
                    folds.make_dir(prefix_func + functions)
                s.Sorting_files("by_func_number",functions_found)
                folders = folds.sync_folders()
                folds.remove_empty(folders)

            elif int(sort_option) == 2:
                s.Collect_files()
                s.Get_suffix()
                cam_numbers_found = s.Get_cam_num_list()
                for cam_num in cam_numbers_found:
                    folds.make_dir(prefix_Cam + cam_num)
                s.Sorting_files("by_cam_number",cam_numbers_found)
                folders = folds.sync_folders()
                folds.remove_empty(folders)

            elif int(sort_option) == 3:
                s.Collect_files()
                s.Get_suffix()
                both_found = s.Get_both_list()
                for both in both_found:
                    folds.make_dir(both)
                s.Sorting_files("by_both",both_found)
                folders = folds.sync_folders()
                folds.remove_empty(folders)

            elif int(sort_option) == 4:  #hledani dvojic (nejprve podle formatu, pote v kazde slozce hleda dvojice) jnak by neslo kdyby uz byly ve slozkach nebo naopak
                s.Collect_files() 
                formats_found = s.Get_suffix()
                for formats in formats_found:
                    folds.make_dir(formats)
                s.Sorting_files("by_format",None)
                folders = folds.sync_folders()
                folds.remove_empty(folders)

                for formats in formats_found: #hledání bude provedeno ve všech složkách podle suffixu
                    s.Get_suffix() #nutne pro vytvoreni pole se soubory v kazde slozce
                    s.sort_by_ID(path+formats,max_num_of_pallets,ID_num_of_digits)

        if s.error == True:
            output.append("Chyba: v zadané cestě nebyly nalezeny žádné soubory (nebo chybí rozhodovací symbol: &)\nNebo je vložená cestak souborům ob více, jak jednu složku")
            output.append("Třídění ukončeno")
        else:
            sort_options = ["typu souborů","funkce","čísla kamery","funkce i čísla kamery","hledání dvojic"]
            if sort_option == 4:
                final_text = "Operace: " + sort_options[sort_option] + " byla provedena"
            else:
                final_text = "Třídění podle: " + sort_options[sort_option] + " bylo provedeno"                
            output.append(final_text)       
            
    main()
    return output