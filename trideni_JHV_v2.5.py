#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
import os
import shutil
import re

def whole_function():

    prefix_ID = "ID_"
    prefix_Cam = "Cam"
    max_number_of_pallets = 55

    def remove_empty_dirs(exception):
        removed_count = 0
        folders = sync_folders(path)
        if exception == 1:
            for dirs in folders: # pole folders uz je filtrovano od ostatnich souboru...
                if (dirs != folder_name[0]) and (dirs != folder_name[1]) and (dirs != folder_name[2]):
                    number_of_files = 0
                    if os.path.exists(path + dirs):
                        for files in os.listdir(path + dirs):
                            number_of_files +=1
                        if number_of_files == 0:
                            print("Odstraněna prázdná složka: ", dirs)
                            os.rmdir(path + dirs)
                            removed_count += 1
            if removed_count != 0:
                print("- Přebytečné složky odstraněny")
                print("")
                        
        else:
            for dirs in folders: # pole folders uz je filtrovano od ostatnich souboru...
                number_of_files = 0
                if os.path.exists(path + dirs):
                    for files in os.listdir(path + dirs):
                        number_of_files +=1
                    if number_of_files == 0:
                        print("Odstraněna prázdná složka: ", dirs)
                        os.rmdir(path + dirs)
                        removed_count += 1
            if removed_count != 0:
                print("- Přebytečné složky odstraněny")
                print("")

    #funkce pro overeni spravneho inputu
    class input_check:
        def __init__(self,range_from, range_to):
            self.right_input = 0
            self.range_to = range_to
            self.range_from = range_from

        def is_input_right(self):
            wrong_input = 1
            self.right_input = input("Vepište číslo v rozsahu: {}-{}: ".format(self.range_from,self.range_to-1))
            print("")
            while wrong_input == 1:
                if self.right_input.isdigit():

                    if int(self.right_input) not in range(self.range_from,self.range_to):
                        self.right_input = input("Zadali jste číslo mimo rozsah (vepište číslo v rozsahu: {}-{}): ".format(self.range_from,self.range_to-1))

                    else:
                        wrong_input = 0

                else:
                    self.right_input = input("Nezadali jste číslo (vepište číslo {}-{}): ".format(self.range_from,self.range_to-1))

            return self.right_input

    class verification:
        def __init__(self):
            self.cam_number_digits = 5 + 4 #az peticiferne cislo kamery (+ 4 znaky za &)
            self.error = 0
            self.functions_arr = []
            self.cameras_arr = []
            self.both_arr = []
            self.files_type_arr = []

        def Collect_files(self):
            self.pair_folder = "PAIRS"
            folders = sync_folders(path)
            if self.pair_folder in folders:
                shutil.rmtree(path + self.pair_folder) #vzdy odstrani celou slozku s nakopirovanymi soubory, nevratne
                
            folders = sync_folders(path) #synchronizace pri moznem smazani slozky PAIR
            for i in range(0,len(folders)):
                for files in os.listdir(path + folders[i]):
                    shutil.move(path + folders[i] + "/" + files , path + '/' + files)
            
        def Get_func_number(file_for_analyze):
            files_split = file_for_analyze.split("&")
            files_split = files_split[0] # leva strana od &
            files_split = files_split.split("_") 
            if len(files_split) != 0:
                arr_pos = len(files_split) -2 #-2, protože pole se pocita od nuly a nezajima nas znak _ před &
                func_number = files_split[arr_pos] 

                return func_number
            else:
                print("Chyba: soubor {} neobsahuje rozhodovaci symbol \"_\", potrebny pro urceni cisla funkce".format(file_for_analyze))

        def Get_suffix(self):
            files_type = ""
            #zjišťování počtu typů souborů
            for files in os.listdir(path):
                if ".bmp" in files:
                    files_type = files.split(".")
                    if not files_type[1] in self.files_type_arr:
                        self.files_type_arr.append(files_type[1])

            if self.files_type_arr != []: #pokud byl nalezen
                print(" - Nalezené typy souborů: ")
                print(self.files_type_arr)
                print("")

        def Sorting_files(self):
            n = 0
            files_arr_cut = []
            self.files_arr = []
            files_cut = 0
            nok_count = 0
            ok_count = 0
            cutting_condition = "&"
            count=0
            error_length = 0

            # výtah z názvu vhodný pro porovnání:
            for files in os.listdir(path):
                if ".bmp" in files:
                    self.files_arr.append(files) #pole s plnými názvy pro přesun
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
                    #shutil.move(path + self.files_arr[i] , path + folder_name[0] + "/" + self.files_arr[i]) #přesun do OK složky
                    count = 0
                    
                else:
                    nok_count += 1
                    shutil.move(path + '/' + self.files_arr[i] , path + folder_name[1] + "/" + self.files_arr[i]) #přesun do NOK složky
                    count = 0
            
            if error_length == 1:
                print("Upozornění: délka názvu před \"&\" některých souborů v dané cestě se liší (možná nefunkční manuální definice zakrytých znaků)")
                print("")

            if self.files_arr == []:
                print("Chyba: V ceste: ",path," Nebyly nalezeny žádné soubory")
                self.error = 1

            else:
                print(" - Nepáry, celkem: {}".format(nok_count))
                print(" - OK soubory zastoupené všemi formáty, celkem: {}".format(ok_count))
                print("")
        
        def sort_by_ID(self):
            increment=0
            compare_num = ""
            count = 0
            lost_pallets = []
            round_number = 0
            list_of_pairs_clear = []
            list_of_pair_count = []
            
            
            #hledani vice souboru (dvojic)---------------------------------------------------------------------------
            for files in os.listdir(path): #hledani v OK slozce
                if ".bmp" in files: #pouze pro overeni, zda se jedna o uzitecny soubor
                    numbers = verification.Get_func_number(files)
                    if len(numbers) == 4:
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

                                            numbers = numbers + "_sada_cislo_" + str(round_number)
                                            if len(list_of_pairs) != 0:
                                                if list_of_pairs[len(list_of_pairs)-1] != numbers:
                                                    list_of_pairs.append(numbers)
                                            else:
                                                list_of_pairs.append(numbers)

                                    keep_searching = False #zavolame dalsi cislo...

                                else:
                                    if(count < len(self.files_type_arr)): #ztracena jen pokud tam je mene jak dva soubory
                                        lost_pallets.append(compare_num)
                                    increment+=1
                                    if count >= 4:
                                        list_of_pair_count.append(count) #pocet souboru, ktere musi algoritmus vyhledat
                                    count = 0
                                        
                            else:
                                keep_searching = False
                    else:
                        print("Chyba: delka ID pred znakem: _& neni rovna 4... ",files)

            if len(list_of_pairs_clear) !=0:
                print("- Nalezeny seznam dvojic v rade za sebou podle ID:")
                print(list_of_pairs_clear)
                print("")
                print("- Kazda v poctu souboru:")
                print(list_of_pair_count)
                print("")
            else:
                print("- Dvojice nenalezeny")
                print("")

            if len(lost_pallets) !=0:
                print("- Seznam cisel chybejicich palet v rade za sebou: ")
                print(lost_pallets)
                print("")
            else:
                print("- Chybejici palety nenalezeny")
                print("")

            if len(list_of_pairs) != 0: #jestli nejake vubec jsou...
                #vytvoreni slozky s páry:
                if not os.path.exists(path + self.pair_folder):
                    os.mkdir(path + self.pair_folder)
                j=0
                x=0
                act_round_number = 0
                #kopirovani do zvlastni slozky------------------------------------------------------------------
                for numbers in list_of_pairs:
                    for files in pair_file_list:                    
                        files_splitted = files.split("_")
                        act_round_number = files_splitted[8]
                        q=0
                        files_full_name = ""

                        for characters in files_splitted:#takto slozite pro pripad viceciferneho cisla kola
                            if q<8 and q<1:
                                files_full_name =  files_full_name + characters
                            if q<8 and q>=1:
                                files_full_name =  files_full_name +"_"+ characters
                            q+=1

                        if (numbers[:4] == verification.Get_func_number(files)) and (numbers.split("_")[3] == files.split("_")[8]):
                            if j < int(list_of_pair_count[x]):
                                if not os.path.exists(path + self.pair_folder + '/' + files_full_name):
                                    #shutil.copy(path + folder_name[0] + "/" + files_full_name , path + self.pair_folder + '/' + files_full_name)
                                    shutil.copy(path + files_full_name , path + self.pair_folder + '/' + files_full_name)
                                j+=1  
                    j=0
                    x+=1
            
        def creating_folders(self):
            #podle typu souboru:
            if sort_by == 0:
                for i in range(0,len(self.files_type_arr)):
                    new_folder_name = self.files_type_arr[i]
                    if not os.path.exists(path + new_folder_name):
                        os.mkdir(path + new_folder_name)
                        if not new_folder_name in folder_name:
                            folder_name.append(new_folder_name)

            if sort_by == 4:
                 for i in range(0,len(self.files_type_arr)):
                    new_folder_name = self.files_type_arr[i]
                    if not os.path.exists(path + self.pair_folder + "/" + new_folder_name):
                        os.mkdir(path + self.pair_folder + "/" + new_folder_name)
                        if not new_folder_name in pair_folders:
                            pair_folders.append(new_folder_name)    

        def moving_files(self):
            files_split = ""
            #presun souboru do slozek:
            if sort_by == 0:
                for files in os.listdir(path): #v OK slozce
                    if ".bmp" in files:
                        for items in folder_name: #pro vsechny slozky...
                            if items in files:
                                if not os.path.exists(path + items + "/" + files):
                                    shutil.move(path + files, path + items + "/" + files)



                """if os.path.exists(path + folder_name[0]):
                    for files in os.listdir(path + folder_name[0]): #v OK slozce
                        for items in folder_name: #pro vsechny slozky...
                            if items in files:
                                if not os.path.exists(path + items + "/" + files):
                                    shutil.move(path + folder_name[0] + "/" + files, path + items + "/" + files)
                else:
                    print("")
                    print("Klíčová složka: ",path+folder_name[0] ," nenalezena\n- Vše jsou nepáry?")
                    print("")"""



            if sort_by == 4:
                for files in os.listdir(path + self.pair_folder):
                    if ".bmp" in files:
                        for items in pair_folders:
                            if files.split(".")[1] == items:
                                if not os.path.exists(path + self.pair_folder + "/" +items + "/" + files):
                                    shutil.move(path + self.pair_folder + "/" + files, path + self.pair_folder + "/" +items + "/" + files)

    #MAIN//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////        
    path = ""
    print(" - Třídění souborů z průmyslových kamer...")
    print("")

    # zadejte cestu k souborum:
    path_found = 0
    stop_while = 0
    while path_found == 0 and stop_while == 0:
        print("Upozornění: funguje pouze o 3 slozky vzdalene... (v cestě, kde se nacházejí složky s datumy)")
        print("")
        path = input("Zadejte cestu k souborům (pokud se aplikace už nachází v dané složce -> enter): ")

        #path = "D:/JHV\Kamery\JHV_Data/L_St_145/A"
        #path = "D:\JHV\Kamery\JHV_Data/2023_04_13\A"
        #path = "D:\JHV\Kamery\JHV_Data"

        #spusteni v ceste, kde se aplikace aktualne nachazi
        if path == "":
            path = os.getcwd()

        #opravy cesty k souborům:
        backslash = "\ "

        if backslash[0] in path:
            newPath = path.replace(os.sep, '/')
            path = newPath

        if path.endswith('/') == False:
            newPath = path + "/"
            path = newPath

        if not os.path.exists(path):
            print(path)
            print("Zadaná cesta k souborům nebyla nalezena")
            stop_while = 1 #ochrana proti neustalemu vypisovani
        else:
            path_found = 1

    if path_found == 1:
        folder_name = ['OK','Temp'] 
        basic_folder_name = ['OK','Temp'] #default
        sort_by = 0


          #ochrana aby se za nazvy slozek nebral nejaky soubor z kamery, vytvareni seznamu slozek...
        print("Analýza složek... ")
        def sync_folders(path_to_search):
            folders = []
            unsupported_formats = [".exe",".pdf",".ifz",".bmp",".txt",".v",".xml",".changed",".doc",".docx",".xls",".xlsx",".ppt",".pptx",".csv",".py",".msi"]
            if os.path.exists(path_to_search):
                for files in os.listdir(path_to_search):
                    #ignorace ostatnich typu souboru:
                    unsupported_format =0
                    for suffixes in unsupported_formats:
                        if suffixes in files:
                            unsupported_format +=1
                    if unsupported_format ==0:
                        folders.append(files)
                                        
            return folders
        #STAGE1///////////////////////////////////////////////////
        folders = sync_folders(path)
        path_list_not_found  = []
        path_list_to_sort = []
        for folds in folders:
            count = 0
            for files in os.listdir(path + folds):
                if ".bmp" in files:
                    count+=1
            if count ==0:
                path_list_not_found.append(path + folds)

        #STAGE2///////////////////////////////////////////////////
        path_list_not_found_st2  = []
        paths_to_folders = []
        if len(path_list_not_found) != 0:
            for paths in path_list_not_found:
                folders = sync_folders(paths)
                for folds in folders:
                    count = 0
                    path_x = paths + "/" + folds

                    for files in os.listdir(path_x):
                        if ".bmp" in files:
                            count+=1
                        if (path_x.split("/")[-1] == "A") or (path_x.split("/")[-1] == "B"):
                            count+=1
                            if not path_x + "/" in paths_to_folders:
                                paths_to_folders.append(path_x + "/")


                    if count ==0:
                        path_list_not_found_st2.append(paths + "/"  + folds)
        else:
            print("Chyba: aplikace programovana na pruchod 3 slozek, tzn.: path + \"2023_04_13/A/Height\" \n-Pro primy pristup do slozky zvolte lite verzi programu")

        #STAGE3///////////////////////////////////////////////////
        cont = "n"
        path_list_not_found_st3  = []
        if len(path_list_not_found_st2) != 0:
            for paths in path_list_not_found_st2:
                folders = sync_folders(paths)
                for folds in folders:
                    count = 0
                    for files in os.listdir(paths + "/" + folds):
                        if (".bmp" in files) or (paths.split("/")[-1] == "A") or (paths.split("/")[-1] == "B"):
                            count+=1
                            if paths.split("/")[-1] == "A" or paths.split("/")[-1] == "B":
                                if not paths + "/" in paths_to_folders:
                                    paths_to_folders.append(paths + "/")
                                
                    if count ==0:
                        path_list_not_found_st3.append(paths + "/"  + folds)

            print("")
            #print("soubory pro trideni nalezeny ve slozkach: ",path_list_to_sort)

            print("- Chystam se projit tyto cesty:\n",paths_to_folders)
            print("")
            cont = input("ANO/NE? (enter/n): ") #CONTINUE?
            #print("Seznam slozek pro overeni: ",paths_to_folders)
            print("")
        else:
            print("Chyba: aplikace programovana na pruchod 3 slozek, tzn.: path + \"2023_04_13/A/Height\" \n-Pro primy pristup do slozky zvolte lite verzi programu")

        if cont == "":
            # HLAVNI FOR CYKLUS //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
            for paths in paths_to_folders:
                path=paths
                print("")
                print("//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
                print("- Provadim trideni v ceste: ",path)
                print("//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
                print("")

                pair_folders = []
                list_of_pairs = []
                pair_file_list = []
                #vytvareni zakladnich slozek:
                """for x in range(0,len(basic_folder_name)):
                    if not os.path.exists(path + basic_folder_name[x]):
                        os.mkdir(path + basic_folder_name[x] + "/")"""
                        
                if not os.path.exists(path + basic_folder_name[1]): #vytvareni slozky pro nepary
                    os.mkdir(path + basic_folder_name[1] + "/")
                #vzorek pro automatickou úpravu různě dlouhých jmen (první blok v sorting_files), delší= zakreje méně znaků, kratší = více...
                example_file_name = "221013_092241_0000000842_21_&Cam1Img.Height.bmp"
                                
                example_file_name_cut = example_file_name.split("&")
                example_file_name_cut = example_file_name_cut[0]
                #example_file_name = "221013_092241_0000000842_21_" #&Cam1Img.Height.bmp" #uz pracuju s takto orizlym...
                hide_cnt = 4 #23   # defaultní počet zakrytých znaků při porovnávání normal a height souborů od & doleva
                #naschromáždění souborů na jedno místo

                v=verification()
                v.Collect_files()

                #třídění do polí, zjišťování suffixu
                v.Get_suffix()

                v.creating_folders()
                print(" - Vytváření složek: hotovo")

                v.Sorting_files()

                #odstranění prázdných složek včetně základních (exception = 0)
                remove_empty_dirs(0)

                if v.error == 1:
                    print("Chyba: v zadané cestě: ",path," nebyly nalezeny žádné soubory (nebo chybí rozhodovací symbol: &), třídění ukončeno")

                else:
                    def advance_sort(sort_by):
                        if sort_by == 0:
                            v.creating_folders()
                            print(" - Vytváření složek: hotovo")
                            v.moving_files()
                            print(" - Přesouvání souborů: hotovo")
                            print("")
                            remove_empty_dirs(0)

                        #kontrola dvojic
                        if sort_by == 4:
                            v.sort_by_ID()
                            print(" - Kontrola dvojic: hotovo")
                            if len(list_of_pairs) != 0:
                                v.creating_folders()
                                print(" - Vytváření složek: hotovo")
                                v.moving_files()
                                print(" - Přesouvání souborů: hotovo")
                                print("")
                            else: 
                                print(" - Nebyly nalezeny zadne dvojice")
                                            
                    sort_by = 4
                    advance_sort(sort_by)
                    sort_by = 0
                    advance_sort(sort_by)  # defaultni rozdeleni do slozek
                    print(" - Třídění pro cestu: ",path," dokončeno")

        else:
            print("")
            print("- Trideni zruseno uzivatelem")
            print("")
        repeat = input("Opakovat? (Y/y) nebo stisknětě libovolný znak pro zavření: ")
        if repeat.casefold() == "y":
            whole_function()
            repeat = ""
        

whole_function() #pouze jednou pri spusteni...






