import os
import shutil
import re

#nok_folder = "Temp"
#pair_folder = "PAIRS"
#forbidden_folders = [pair_folder]
output = []
output_console2 = []

class whole_sorting_function:
    def __init__(self,path_given,selected_sort,more_dir,max_num_of_pallets_given,by_which_ID_number,
                prefix_func,prefix_Cam,supported_formats,aut_detect_num_of_pallets,nok_folder_name,
                pairs_folder_name):
        
        self.nok_folder = nok_folder_name
        self.pair_folder = pairs_folder_name
        self.forbidden_folders = [self.pair_folder]
        self.max_num_of_pallets = max_num_of_pallets_given
        self.ID_num_of_digits = 4
        self.path = path_given
        self.sort_option = int(selected_sort-1)
        self.more_dirs = more_dir
        self.num_of_dots = 0 #default - urci se automaticky
        self.by_which_ID_num = by_which_ID_number
        self.prefix_func = prefix_func
        self.prefix_cam = prefix_Cam
        self.supported_formats=supported_formats
        self.aut_detect_num_of_pallets=aut_detect_num_of_pallets
        self.error = False
        self.cam_number_digits = 5 + 4 #az peticiferne cislo kamery (+ 4 znaky za &)
        self.functions_arr = []
        self.cameras_arr = []
        self.both_arr = []
        self.files_type_arr = []
        self.file_list = []

        self.main()

    def make_dir(self,name):
        if not os.path.exists(self.path + name): #pokud uz neni vytvorena, vytvor...
            os.mkdir(self.path + name + "/")

    def sync_folders(self,path):
        folders = []
        if path.endswith('/') == False:
            newPath = path + "/"
            path = newPath

        for files in os.listdir(path):
            if os.path.isdir(path + files):
                if files not in self.forbidden_folders:
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

    def subfolders_check(self):
        #STAGE1///////////////////////////////////////////////////
        num_of_dots_set = False
        folders = self.sync_folders(self.path)
        path_list_not_found  = []
        for folds in folders:
            count = 0
            for files in os.listdir(self.path + folds):
                if num_of_dots_set == False: #automaticke urceni poctu tecek v souboru
                    for formats in self.supported_formats:
                        if ("." + formats) in files:
                            self.num_of_dots = (len(files.split(".")) -1)
                            num_of_dots_set = True
                if num_of_dots_set == True:
                    if len(files.split(".")) == self.num_of_dots+1: #tri bloky rozdelene teckou x.x.bmp/png
                        if files.split(".")[self.num_of_dots] in self.supported_formats:
                            count+=1
            if count ==0:
                path_list_not_found.append(self.path + folds)
        
        print(path_list_not_found)
        
        #STAGE2///////////////////////////////////////////////////
        path_list_not_found_st2  = []
        paths_to_folders = []
        if len(path_list_not_found) != 0:
            for paths in path_list_not_found:
                folders = self.sync_folders(paths)
                print(folders)
                for folds in folders:
                    count = 0
                    path_x = paths + "/" + folds
                    
                    for files in os.listdir(path_x):
                        if num_of_dots_set == False: #automaticke urceni poctu tecek v souboru
                            for formats in self.supported_formats:
                                if ("." + formats) in files:
                                    self.num_of_dots = (len(files.split(".")) -1)
                                    num_of_dots_set = True
                        if num_of_dots_set == True:
                            if len(files.split(".")) == self.num_of_dots+1:
                                if files.split(".")[self.num_of_dots] in self.supported_formats:
                                    count+=1
                                    if os.path.isdir(path_x + "/"):
                                        if not path_x + "/" in paths_to_folders:
                                            paths_to_folders.append(path_x + "/")
                    if count ==0:
                        path_list_not_found_st2.append(paths + "/"  + folds)
        print(path_list_not_found_st2)
        #STAGE3///////////////////////////////////////////////////
        path_list_not_found_st3  = []
        if len(path_list_not_found_st2) != 0:
            for paths in path_list_not_found_st2:
                folders = self.sync_folders(paths)                                                               
                for folds in folders:
                    count = 0
                    for files in os.listdir(paths + "/" + folds):
                        if num_of_dots_set == False: #automaticke urceni poctu tecek v souboru
                            for formats in self.supported_formats:
                                if ("." + formats) in files:
                                    self.num_of_dots = (len(files.split(".")) -1)
                                    num_of_dots_set = True
                        if num_of_dots_set == True:
                            if len(files.split(".")) == self.num_of_dots+1:
                                if files.split(".")[self.num_of_dots] in self.supported_formats:
                                    count+=1
                                    if os.path.isdir(paths + "/"):
                                        if not paths + "/" in paths_to_folders:
                                            paths_to_folders.append(paths + "/")                           
                    if count ==0:
                        path_list_not_found_st3.append(paths + "/"  + folds)
        print(path_list_not_found_st3)
        if len(paths_to_folders) !=0:
            return paths_to_folders 
        else:
            return False

    def Collect_files(self): #vykona se jako prvni
        folders = self.sync_folders(self.path)
        num_of_dots_set = False
        for i in range(0,len(folders)):
            for files in os.listdir(self.path + folders[i]):
                if num_of_dots_set == False: #automaticke urceni poctu tecek v souboru
                    for formats in self.supported_formats:
                        if ("." + formats) in files:
                            self.num_of_dots = (len(files.split(".")) -1)
                            num_of_dots_set = True
                if num_of_dots_set == True:
                    if len(files.split(".")) == self.num_of_dots+1:
                        if files.split(".")[self.num_of_dots] in self.supported_formats:
                            if os.path.exists(self.path + folders[i] + "/" + files):
                                shutil.move(self.path + folders[i] + "/" + files , self.path + '/' + files)

    def Get_cam_number(self,file_for_analyze):
        if "&" in file_for_analyze:
            files_split = file_for_analyze.split("&")
            files_split = files_split[1] # prava strana od &
            files_split = files_split.split(".") #od prvni tecky... neni treba upravovat podle tecek v nazvu souboru
            files_split = files_split[0] # leva strana od tecky
            files_split = re.findall(r'\d+', files_split)
            cam_number = ' '.join([str(elem) for elem in files_split]) #ziskani stringu z pole

            return cam_number
        else:
            #output.append("-Chyba: soubor {} neobsahuje rozhodovaci symbol \"&\"\n".format(file_for_analyze))
            #oprava spamu:
            error_message = "-Chyba: V cestě jsou soubory, které neobsahují rozhodovací symbol \"&\"\n"
            if not error_message in output:
                output.append(error_message)
            return False

    def Get_cam_num_list(self):
        cam_num_list = []
        for files in self.file_list:
            cam_number = self.Get_cam_number(files)
            if (cam_number not in cam_num_list) and (cam_number != False):
                cam_num_list.append(cam_number)
        
        return cam_num_list
        
    def Get_func_number(self,file_for_analyze):
        if "&" in file_for_analyze:
            files_split = file_for_analyze.split("&")
            files_split = files_split[0] # leva strana od &
            files_split = files_split.split("_") 
            if len(files_split) != 0:
                arr_pos = len(files_split) -2 #-2, protože pole se pocita od nuly a nezajima nas znak _ před &
                func_number = files_split[arr_pos] 
                self.ID_num_of_digits = len(func_number) #automaticke urceni poctu cifer v ID
                id_num_of_digits_message = f"- Počet cifer v ID automaticky detekován: {self.ID_num_of_digits}"
                if not id_num_of_digits_message in output:
                    output.append(id_num_of_digits_message)
                if self.by_which_ID_num == "":
                    return func_number
                else:
                    if int(self.by_which_ID_num) <= self.ID_num_of_digits:
                        return func_number[self.by_which_ID_num-1]
                    else:
                        error_message = "-Chyba: Zvolili jste třídit podle cifry, která neodpovídá délce ID souborů\n"
                        if not error_message in output:
                            output.append(error_message)
                        return False
            else:
                #oprava spamu:
                error_message1 = "-Chyba: V cestě jsou soubory, které neobsahují rozhodovací symbol \"_\", potřebný pro určení čísla funkce\n"
                if not error_message1 in output:
                    output.append(error_message1)
                return False
        else:
            error_message2 = "-Chyba: V cestě jsou soubory, které neobsahují rozhodovací symbol \"&\"\n"
            if not error_message2 in output:
                output.append(error_message2)
            return False
        
    def Get_func_list(self):
        func_list = []
        for files in self.file_list:
            func_number = self.Get_func_number(files)
            if (func_number not in func_list) and (func_number != False):
                func_list.append(func_number)
        
        return func_list

    def Get_both_list(self):
        both_list = []
        for files in self.file_list:
            func_number = self.Get_func_number(files)
            cam_number = self.Get_cam_number(files)
            if func_number != False and cam_number != False:
                if self.prefix_func + func_number + "_" + self.prefix_cam + cam_number not in both_list:
                    both_list.append(self.prefix_func + func_number + "_" + self.prefix_cam + cam_number)
        
        return both_list    

    def Get_suffix(self):
        files_type = ""
        num_of_dots_set = False
        #zjišťování počtu typů souborů
        for files in os.listdir(self.path):
            if num_of_dots_set == False: #automaticke urceni poctu tecek v souboru
                for formats in self.supported_formats:
                    if ("." + formats) in files:
                        self.num_of_dots = (len(files.split(".")) -1)
                        num_of_dots_set = True
            
            if num_of_dots_set == True:
                if len(files.split(".")) == (self.num_of_dots+1):
                    if files.split(".")[self.num_of_dots] in self.supported_formats:
                        self.file_list.append(files)
                        files_type = files.split(".")
                        if self.num_of_dots > 1:
                            if not files_type[self.num_of_dots-1] in self.files_type_arr:
                                self.files_type_arr.append(files_type[self.num_of_dots-1])
                        else:
                            if not files_type[self.num_of_dots] in self.files_type_arr:
                                self.files_type_arr.append(files_type[self.num_of_dots])
        if len(self.file_list) == 0:
            output.append("Nebyly nalezeny žádné vhodné soubory ke zpracování\n")

        if self.files_type_arr != []: #pokud byl nalezen
            output.append(f"-Nalezené typy souborů: {self.files_type_arr}\n")

        return self.files_type_arr
            
    def Sorting_files(self,folder_list):
        hide_cnt = self.ID_num_of_digits + 2
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
                if self.sort_option == 0: # podle typu souboru
                    for formats in self.files_type_arr:
                        if self.file_list[i].split(".")[(self.num_of_dots-1)] == formats:
                            
                            if os.path.exists(self.path + self.file_list[i]):
                                shutil.move(self.path + self.file_list[i] , self.path + formats + "/" + self.file_list[i])

                elif self.sort_option == 1: # podle cisla funkce (ID)
                    for func_numbers in folder_list:
                        if self.Get_func_number(self.file_list[i]) == func_numbers:
                            if os.path.exists(self.path + self.file_list[i]):
                                shutil.move(self.path + self.file_list[i] , self.path + self.prefix_func + func_numbers + "/" + self.file_list[i])

                elif self.sort_option == 2: # podle cisla kamery
                    for cam_numbers in folder_list:
                        if self.Get_cam_number(self.file_list[i]) == cam_numbers:
                            if os.path.exists(self.path + self.file_list[i]):
                                shutil.move(self.path + self.file_list[i] , self.path + self.prefix_cam + cam_numbers + "/" + self.file_list[i])

                elif self.sort_option == 3:# podle cisla kamery i podle cisla funkce
                    for both in folder_list:
                        if (self.prefix_func + self.Get_func_number(self.file_list[i]) + "_" + self.prefix_cam + self.Get_cam_number(self.file_list[i])) == both:
                            if os.path.exists(self.path + self.file_list[i]):
                                shutil.move(self.path + self.file_list[i] , self.path + both + "/" + self.file_list[i])
                count = 0
                
            else:
                nok_count += 1
                if len(self.file_list)>i: # protoze kdyz se odstani z pole inkrement zustane vetsi
                    if os.path.exists(self.path + self.file_list[i]):
                        shutil.move(self.path + self.file_list[i] , self.path + self.nok_folder + "/" + self.file_list[i]) #přesun do Temp složky
                    if self.sort_option == 4:
                        self.file_list.pop(i) #ostraneni souboru z pole, aby se s nim dale nepracovalo
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

    def make_tuple(self,array1,array2):
        tuple_array = []
        for i in range(0,len(array1)):
            tuple_array.append((array1[i],array2[i]))
        
        return tuple_array

    def sort_by_ID(self):
        max_number_of_pallets = int(self.max_num_of_pallets)
        list_of_pairs = []
        lost_pallets = []
        list_of_pairs_clear = []
        list_of_pair_count = []
        files_to_copy_part1 = []
        files_to_copy=[]

        compare_num = ""
        count = 0
        round_number = 0
        ref_file = self.file_list[0]
        increment=int(self.Get_func_number(ref_file)) #reference aby palety nezacinaly vzdy on nuly
        
        #hledani vice souboru (dvojic)---------------------------------------------------------------------------
        stop = False
        for files in self.file_list: #hledani v listu se soubory
            if stop == False:
                numbers = self.Get_func_number(files) #tady se automaticky nastavi self.ID_num_of_digits
                keep_searching = True
                while(keep_searching == True): #while cyklus kvuli moznym chybejicim paletkam
                    if round_number > 50000: #zacykleni programu 50000 kol hledani se zda byt dostacujici, vypocetni doba: 5s
                        output.append(f"- Došlo k ZACYKLENÍ programu, nejspíše neodpovídá (v případech manuálního nastavení) nastavení maximálního počtu palet {max_number_of_pallets} (max ID) v oběhu\n- Nebo chybí extrémní množství palet (čísla id nejsou po sobě jdoucí v čase z názvu souboru)")
                        stop = True
                        keep_searching = False
                        
                    if increment>max_number_of_pallets:
                        increment=0
                        round_number +=1
                    if increment < 10:
                        compare_num = ((self.ID_num_of_digits-1)*"0")+str(increment)
                    if increment >= 10:
                        compare_num = ((self.ID_num_of_digits-2)*"0")+str(increment)
                    if increment >= 100:
                        compare_num = ((self.ID_num_of_digits-3)*"0")+str(increment)
                    if increment >= 1000:
                        compare_num = ((self.ID_num_of_digits-4)*"0")+str(increment)
                    if increment >= 10000:
                        compare_num = ((self.ID_num_of_digits-5)*"0")+str(increment)
                    if increment >= 100000:
                        compare_num = ((self.ID_num_of_digits-6)*"0")+str(increment)
                    if increment >= 1000000:
                        compare_num = ((self.ID_num_of_digits-7)*"0")+str(increment)
                    if increment >= 10000000: #max self.ID_num_of_digits = 8
                        compare_num = ((self.ID_num_of_digits-8)*"0")+str(increment)

                    if compare_num == numbers:
                        count +=1

                        files_to_copy_part1.append(files + "_" + str(round_number))
                        
                        if count > len(self.files_type_arr):
                            files_to_copy.append(files + "_" + str(round_number)) #utvareni pole, pro nasledne kopirovani do PAIR slozky
                            for items in files_to_copy_part1:
                                if not items in files_to_copy:
                                    files_to_copy.append(items)

                            if numbers not in list_of_pairs: # blok pro zajisteni pouze jednoho vyskytu v poli v rade V JEDNE SADE (0-max_num_of_pallets)
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
                        if count > len(self.files_type_arr):
                            list_of_pair_count.append(count) #pocet souboru, ktere musi algoritmus vyhledat
                        count = 0
                        files_to_copy_part1 = [] #resetuje se kazde kolo, jsou to ty prvni "podezrele" soubory, ktere se doplni do pole files_to_copy, kdyz jich je vice nez pocet typu souboru
                                        

        if len(list_of_pairs_clear) !=0:
            #output.append(f"- Nalezený seznam dvojic v řadě za sebou podle ID: {list_of_pairs_clear}\n- Každá v počtu souborů: {list_of_pair_count}")
            output_msg = self.make_tuple(list_of_pairs_clear,list_of_pair_count)
            output.append("- Nalezený seznam dvojic v řadě za sebou (ID, počet souborů):")
            output.append(f"{output_msg}")

        else:
            output.append("- V zadané cestě nebyly nalezeny žádné dvojice")

        if len(lost_pallets) ==0:
            output.append("- Žádné chybějící palety nebyly nenalezeny")

        if len(list_of_pairs) != 0: #jestli nejake vubec jsou...
            #vytvoreni slozky s páry:
            if not os.path.exists(self.path + self.pair_folder):
                os.mkdir(self.path + self.pair_folder)
            num_of_files_copied=0
            num_of_files_to_copy=0
            #kopirovani do zvlastni slozky------------------------------------------------------------------
            for numbers in list_of_pairs:
                for files in files_to_copy:                    
                    files_splitted = files.split("_")
                    num_of_character=0
                    files_full_name = ""
                    for characters in files_splitted:#takto slozite pro pripad viceciferneho cisla kola
                        #skladame nazev bez koncovky, kterou jsme pridali z duvodu urceni kola, prvni charakter nema znak _ pred sebou...
                        if num_of_character==0: 
                            files_full_name =  files_full_name + characters
                        if num_of_character>0 and num_of_character<(len(files_splitted)-1):
                            files_full_name =  files_full_name +"_"+ characters
                        num_of_character+=1
                    #priklad numbers: 0026_sada_cislo_24
                    #priklad files.split("_"): ['2023', '11', '15-17', '00', '21', 'PALETKA', '0047', '&Cam2Img.Height.bmp', '41'] -> posledni cislo v poli predstavuje cislo kola
                    if (numbers[:self.ID_num_of_digits] == self.Get_func_number(files)) and (numbers.split("_")[3] == files.split("_")[(len(files_splitted)-1)]):
                        if num_of_files_copied < int(list_of_pair_count[num_of_files_to_copy]):
                            if not os.path.exists(self.path + self.pair_folder + '/' + files_full_name):
                                if os.path.exists(self.path + files_full_name):
                                    shutil.copy(self.path + files_full_name , self.path + self.pair_folder + '/' + files_full_name)
                            num_of_files_copied+=1  
                num_of_files_copied=0
                num_of_files_to_copy+=1

    def main(self):
        if self.more_dirs == True:
            result = self.subfolders_check()
            if result == False:
                output_console2.append("- Chyba: aplikace programovana na pruchod 3 slozek, tzn.: path + \"2023_04_13/A/Height\"\nnebo: path + \"2023_04_13/A/soubory volně mimo složku\"")
                output.append("Chyba: v zadané cestě nebyly nalezeny žádné soubory (nebo chybí rozhodovací symbol: &)\nNebo je vložená cestak souborům ob více, jak jednu složku")
                output.append("Třídění ukončeno")
                return
            else:
                output_console2.append("- Prochazím tyto cesty: ")
                for items in result:
                    output_console2.append(items)

                for paths in result:
                    if os.path.exists(paths):
                        self.path = paths

                        output.append("\nTrideni v: " + paths)
                        self.make_dir(self.nok_folder)
                        folders = self.sync_folders(self.path)
                        
                        if self.sort_option == 0:
                            self.Collect_files()
                            formats_found = self.Get_suffix()
                            for formats in formats_found:
                                self.make_dir(formats)
                            self.Sorting_files(None)
                            folders = self.sync_folders(self.path)
                            self.remove_empty(folders)

                        elif self.sort_option == 1:
                            self.Collect_files()
                            self.Get_suffix()
                            functions_found = self.Get_func_list()
                            for functions in functions_found:
                                self.make_dir(self.prefix_func + functions)
                            self.Sorting_files(functions_found)
                            folders = self.sync_folders(self.path)
                            self.remove_empty(folders)

                        elif self.sort_option == 2:
                            self.Collect_files()
                            self.Get_suffix()
                            cam_numbers_found = self.Get_cam_num_list()
                            for cam_num in cam_numbers_found:
                                self.make_dir(self.prefix_cam + cam_num)
                            self.Sorting_files(cam_numbers_found)
                            folders = self.sync_folders(self.path)
                            self.remove_empty(folders)

                        elif self.sort_option == 3:
                            self.Collect_files()
                            self.Get_suffix()
                            both_found = self.Get_both_list()
                            for both in both_found:
                                self.make_dir(both)
                            self.Sorting_files(both_found)
                            folders = self.sync_folders(self.path)
                            self.remove_empty(folders)

                        elif self.sort_option == 4: #hledani dvojic, collect ze slozek a vytvoreni slozky se vsema dvojicema - potom si mohou dotridit jinym programem
                            self.Collect_files() 
                            self.Get_suffix() #pro ziskani pole se vsema podporovanyma souborama
                            self.Sorting_files(None) #pro presun lichych souboru do nok slozky
                            if self.aut_detect_num_of_pallets == True:
                                ID_list = self.Get_func_list()
                                self.max_num_of_pallets = int(max(ID_list))
                                output.append(f"Maximální počet palet automaticky nastaven na: {self.max_num_of_pallets}")   
                            self.sort_by_ID()
                            folders = self.sync_folders(self.path)
                            self.remove_empty(folders)
                              
        else: #nebylo zaskrtnuto prochazet vice souboru
            self.make_dir(self.nok_folder) #vytvoreni zakladnich slozek
            folders = self.sync_folders(self.path)
            if self.sort_option == 0:
                self.Collect_files()
                formats_found = self.Get_suffix()
                for formats in formats_found:
                    self.make_dir(formats)
                error=self.Sorting_files(None)
                if error == True:
                    return
                folders = self.sync_folders(self.path)
                self.remove_empty(folders)

            elif self.sort_option == 1:
                self.Collect_files()
                self.Get_suffix()
                functions_found = self.Get_func_list()
                for functions in functions_found:
                    self.make_dir(self.prefix_func + functions)
                error=self.Sorting_files(functions_found)
                if error == True:
                    return
                folders = self.sync_folders(self.path)
                self.remove_empty(folders)

            elif self.sort_option == 2:
                self.Collect_files()
                self.Get_suffix()
                cam_numbers_found = self.Get_cam_num_list()
                for cam_num in cam_numbers_found:
                    self.make_dir(self.prefix_cam + cam_num)
                error=self.Sorting_files(cam_numbers_found)
                if error == True:
                    return
                folders = self.sync_folders(self.path)
                self.remove_empty(folders)

            elif self.sort_option == 3:
                self.Collect_files()
                self.Get_suffix()
                both_found = self.Get_both_list()
                for both in both_found:
                    self.make_dir(both)
                error=self.Sorting_files(both_found)
                if error == True:
                    return
                folders = self.sync_folders(self.path)
                self.remove_empty(folders)

            elif self.sort_option == 4:  #hledani dvojic, collect ze slozek a vytvoreni slozky se vsema dvojicema - potom si mohou dotridit jinym programem
                self.Collect_files() 
                self.Get_suffix() #pro ziskani pole se vsema podporovanyma souborama
                error=self.Sorting_files(None) #pro presun lichych souboru do nok slozky
                if error == True:
                    return
                if self.aut_detect_num_of_pallets == True:
                    ID_list = self.Get_func_list()
                    self.max_num_of_pallets = int(max(ID_list))
                    output.append(f"Maximální počet palet automaticky nastaven na: {self.max_num_of_pallets}")   
                self.sort_by_ID()
                folders = self.sync_folders(self.path)
                self.remove_empty(folders)

        if self.error == True:
            output.append("Chyba: v zadané cestě nebyly nalezeny žádné soubory (nebo chybí rozhodovací symbol: &)\nNebo je vložená cestak souborům ob více, jak jednu složku")
            output.append("Třídění ukončeno")
        else:
            sort_options = ["typu souborů","funkce","čísla kamery","funkce i čísla kamery","hledání dvojic"]
            if self.sort_option == 4:
                final_text = "\nOperace: " + sort_options[self.sort_option] + " byla dokončena"
            else:
                final_text = "\nTřídění podle: " + sort_options[self.sort_option] + " bylo dokončeno"                
            output.append(final_text)       
        return output
    