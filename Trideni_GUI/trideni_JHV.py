# -verze 2.4 je univerzální vůči počtu formátů souborů
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
import os
import shutil
import re


prefix_func = "Func_"
prefix_Cam = "Cam"
folder_name = ['OK','Temp'] #default
output = []
output_console2 = []
hide_cnt = 4

def path_check(path_raw):
    #path = ""
    path=path_raw
    print(" - Třídění souborů z průmyslových kamer...")
    print("")

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
        #print("Zadaná cesta k souborům nebyla nalezena")
        #stop_while = 1 #ochrana proti neustalemu vypisovani
    else:
        return path


def whole_sorting_function(path_given,selected_sort,more_dir):
    path = path_given
    sort_by = selected_sort
    paths_to_folders = []
    more_dirs = more_dir
    def remove_empty_dirs(exception):
        removed_count = 0
        folders = sync_folders(path)
        if exception == 1:
            for dirs in folders: # pole folders uz je filtrovano od ostatnich souboru...
                if (dirs != folder_name[0]) and (dirs != folder_name[1]) and (dirs != folder_name[2]):
                    number_of_files = 0
                    if os.path.isdir(path + dirs):
                        for files in os.listdir(path + dirs):
                            number_of_files +=1
                        if number_of_files == 0:
                            os.rmdir(path + dirs)
                            removed_count +=1
                                
        else:
            for dirs in folders: # pole folders uz je filtrovano od ostatnich souboru...
                number_of_files = 0
                if os.path.isdir(path + dirs):
                    for files in os.listdir(path + dirs):
                        number_of_files +=1
                    if number_of_files == 0:
                        os.rmdir(path + dirs)
                        removed_count +=1

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
            folders = sync_folders(path)
            for i in range(0,len(folders)):
                if os.path.isdir(path + folders[i]):
                    for files in os.listdir(path + folders[i]):
                        if (".bmp" or ".png") in files:
                            if os.path.exists(path + folders[i] + "/" + files):
                                shutil.move(path + folders[i] + "/" + files , path + '/' + files)

            #vytvareni zakladnich slozek:
            for x in range(0,len(folder_name)):
                if not os.path.exists(path + folder_name[x]):
                    os.mkdir(path + folder_name[x] + "/")             

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
                #print("Chyba: soubor {} neobsahuje rozhodovaci symbol \"&\"".format(file_for_analyze))
                output.append("Chyba, některé soubory neobsahují rozhodovaci symbol \"&\", potřebný pro určení čísla kamery")
            
        def Get_func_number(file_for_analyze):
            files_split = file_for_analyze.split("&")
            files_split = files_split[0] # leva strana od &
            files_split = files_split.split("_") 
            if len(files_split) != 0:
                arr_pos = len(files_split) -2 #-2, protože pole se pocita od nuly a nezajima nas znak _ před &
                func_number = files_split[arr_pos] 

                return func_number
            else:
                #print("Chyba: soubor {} neobsahuje rozhodovaci symbol \"_\", potrebny pro urceni cisla funkce".format(file_for_analyze))
                output.append("Chyba, některé soubory neobsahují rozhodovaci symbol \"_\", potřebný pro určení čísla funkce")

        def Get_suffix(self):
            files_type = ""
            #zjišťování počtu typů souborů
            for files in os.listdir(path):
                if (".bmp" or ".png") in files:
                    files_type = files.split(".")
                    if not files_type[1] in self.files_type_arr:
                        self.files_type_arr.append(files_type[1])

            if self.files_type_arr != []: #pokud byl nalezen
                output.append("Nalezené typy souborů: " + str(self.files_type_arr))

        def Sorting_files(self):
            n = 0
            files_arr_cut = []
            files_arr = []
            files_cut = 0
            nok_count = 0
            ok_count = 0
            cutting_condition = "&"
            count=0
            error_length = 0
            #sync folders a prohledat folders protoze jinak to jde i ob dve slozky
            # výtah z názvu vhodný pro porovnání:
            for files in os.listdir(path):
                if (".bmp" or ".png") in files:
                    files_arr.append(files) #pole s plnými názvy pro přesun
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
                    if os.path.exists(path + '/' + files_arr[i]):
                        shutil.move(path + '/' + files_arr[i] , path + folder_name[0] + "/" + files_arr[i]) #přesun do OK složky
                    count = 0
                    
                else:
                    nok_count += 1
                    if os.path.exists(path + '/' + files_arr[i]):
                        shutil.move(path + '/' + files_arr[i] , path + folder_name[1] + "/" + files_arr[i]) #přesun do Temp složky
                    count = 0

            if files_arr == [] and more_dirs == False:
                #output.append("Chyba: Nebyly nalezeny žádné soubory")
                self.error = 1

            else:
                self.error = 0
                output.append(" - Nepáry, celkem: {}".format(nok_count))
                output.append(" - OK soubory zastoupené všemi formáty, celkem: {}".format(ok_count))
            
        def sort_by_camera(self):
            camera_num = 0
            for files in os.listdir(path + folder_name[0]): #hledani v OK slozce
                if (".bmp" or ".png") in files: #pouze pro overeni, zda se jedna o uzitecny soubor
                    camera_num = verification.Get_cam_number(files)
                    if not camera_num in self.cameras_arr:
                        self.cameras_arr.append(camera_num)
                        self.cameras_arr.sort()
                        
            """print(" - Nalezená čísla kamer: ")
            print(self.cameras_arr)
            print("")"""

            
        def sort_by_function(self):
            func_num = 0
            for files in os.listdir(path + folder_name[0]): #hledani v OK slozce
                if (".bmp" or ".png") in files: #pouze pro overeni, zda se jedna o uzitecny soubor
                    func_num = verification.Get_func_number(files)
                    if not func_num in self.functions_arr:
                        self.functions_arr.append(func_num)
                        self.functions_arr.sort()

            """print(" - Nalezená čísla funkcí: ")
            print(self.functions_arr)
            print("")"""

            
        def sort_by_both(self):
            both_name = ""
            for files in os.listdir(path + folder_name[0]): #hledani v OK slozce
                # zjišťování všech čísel kamer
                if (".bmp" or ".png") in files:#pouze pro overeni, zda se jedna o uzitecny soubor
                    func_num = verification.Get_func_number(files)
                    camera_num = verification.Get_cam_number(files)
                    both_name = prefix_Cam + str(camera_num) + "_" + prefix_func + str(func_num)
                    if not both_name in self.both_arr:
                        self.both_arr.append(both_name)
                    
        def creating_folders(self):
            #podle typu souboru:
            if sort_by == 1:
                for i in range(0,len(self.files_type_arr)):
                    new_folder_name = self.files_type_arr[i]
                    if not os.path.exists(path + new_folder_name):
                        os.mkdir(path + new_folder_name)
                        if not new_folder_name in folder_name:
                            folder_name.append(new_folder_name)

            if sort_by == 2:
                for i in range(0,len(self.functions_arr)):
                    new_folder_name = prefix_func + self.functions_arr[i]
                    if not os.path.exists(path + new_folder_name):
                        os.mkdir(path + new_folder_name)
                        if not new_folder_name in folder_name:
                            folder_name.append(new_folder_name)

            #vytvareni slozek pro kamery:
            if sort_by == 3:
                for i in range(0,len(self.cameras_arr)):
                    new_folder_name = prefix_Cam + self.cameras_arr[i]
                    if not os.path.exists(path + new_folder_name):
                        os.mkdir(path + new_folder_name) 
                        if not new_folder_name in folder_name:
                            folder_name.append(new_folder_name)

            if sort_by == 4:
                for i in range(0,len(self.both_arr)):
                    new_folder_name = self.both_arr[i]
                    if not os.path.exists(path + new_folder_name):
                        os.mkdir(path + new_folder_name) 
                        if not new_folder_name in folder_name:
                            folder_name.append(new_folder_name)

        def moving_files(self):
            files_split = ""
            #presun souboru do slozek:
            if sort_by == 1:
                if os.path.exists(path + folder_name[0]):
                    for files in os.listdir(path + folder_name[0]): #v OK slozce
                        for items in folder_name:
                            if items in files:
                                if os.path.exists(path + folder_name[0] + "/" + files):
                                    if not os.path.exists(path + items + "/" + files):
                                        shutil.move(path + folder_name[0] + "/" + files, path + items + "/" + files)
                else:
                    output.append("Třídění ukončeno - vše jsou Nepáry (u souborů nebyly zastoupeny všechny formáty nalezené v cestě)")
            if sort_by == 2:
                if os.path.exists(path + folder_name[0]):
                    for files in os.listdir(path + folder_name[0]): #v OK slozce
                        func_num = verification.Get_func_number(files)
                        for items in folder_name:
                            if (prefix_func + func_num) == items:
                                if os.path.exists(path + folder_name[0] + "/" + files):
                                    if not os.path.exists(path + items + "/" + files):
                                        shutil.move(path + folder_name[0] + "/" + files, path + items + "/" + files)
                else:
                    output.append("Třídění ukončeno - vše jsou Nepáry (u souborů nebyly zastoupeny všechny formáty nalezené v cestě)")
            if sort_by == 3:
                if os.path.exists(path + folder_name[0]):
                    for files in os.listdir(path + folder_name[0]): #v OK slozce
                        camera_num = verification.Get_cam_number(files)
                        for items in folder_name:
                            if (prefix_Cam + camera_num) == items:
                                if os.path.exists(path + folder_name[0] + "/" + files):
                                    if not os.path.exists(path + items + "/" + files):
                                        shutil.move(path + folder_name[0] + "/" + files, path + items + "/" + files)
                else:
                    output.append("Třídění ukončeno - vše jsou Nepáry (u souborů nebyly zastoupeny všechny formáty nalezené v cestě)")
            if sort_by == 4:
                if os.path.exists(path + folder_name[0]):
                    for files in os.listdir(path + folder_name[0]): #v OK slozce
                        func_num = verification.Get_func_number(files)
                        camera_num = verification.Get_cam_number(files)
                        for items in folder_name:
                            if (prefix_Cam + camera_num + "_" + prefix_func + func_num) == items:
                                if os.path.exists(path + folder_name[0] + "/" + files):
                                    if not os.path.exists(path + items + "/" + files):
                                        shutil.move(path + folder_name[0] + "/" + files, path + items + "/" + files)
                else:
                    output.append("Třídění ukončeno - vše jsou Nepáry (u souborů nebyly zastoupeny všechny formáty nalezené v cestě)")
    #ochrana aby se za nazvy slozek nebral nejaky soubor z kamery, vytvareni seznamu slozek...

    def sync_folders(path_to_sync):
        folders = []
        for files in os.listdir(path_to_sync):
            if path_to_sync.endswith("/"):
                if os.path.isdir(path_to_sync + files):
                    folders.append(files)
            else:
                if os.path.isdir(path_to_sync +"/"+ files):
                    folders.append(files)
        return folders
    
    def advance_sort():
        #v=verification()
        if sort_by == 1:
            v.creating_folders()
            v.moving_files()
            remove_empty_dirs(0)

        if sort_by == 2:
            v.sort_by_function()
            v.creating_folders()
            v.moving_files()
            remove_empty_dirs(0)

        if sort_by == 3:
            v.sort_by_camera()
            v.creating_folders()
            v.moving_files()
            remove_empty_dirs(0)

        if sort_by == 4:
            v.sort_by_both()
            v.creating_folders()
            v.moving_files()
            remove_empty_dirs(0)


    if more_dirs == True:
        #STAGE1///////////////////////////////////////////////////
        path = path_given
        folders = sync_folders(path)
        path_list_not_found  = []
        path_list_to_sort = []
        for folds in folders:
            count = 0
            for files in os.listdir(path + folds):
                if (".bmp" in files) or (".png" in files):
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
                        if (".bmp" in files) or (".png" in files):
                            count+=1
                            if os.path.isdir(path_x + "/"):
                                if not path_x + "/" in paths_to_folders:
                                    paths_to_folders.append(path_x + "/")


                    if count ==0:
                        path_list_not_found_st2.append(paths + "/"  + folds)
                
        else:
            output_console2.append("- Chyba: aplikace programovana na pruchod 3 slozek, tzn.: path + \"2023_04_13/A/Height\"")
            print("- Chyba: aplikace programovana na pruchod 3 slozek, tzn.: path + \"2023_04_13/A/Height\"")

        #STAGE3///////////////////////////////////////////////////
        path_list_not_found_st3  = []
        if len(path_list_not_found_st2) != 0:
            for paths in path_list_not_found_st2:
                folders = sync_folders(paths)                                                                           
                for folds in folders:
                    count = 0
                    for files in os.listdir(paths + "/" + folds):
                        if (".bmp" in files) or (".png" in files):
                            count+=1
                            #if paths.split("/")[-1] == "A" or paths.split("/")[-1] == "B":
                            if os.path.isdir(paths + "/"):
                                if not paths + "/" in paths_to_folders:
                                    paths_to_folders.append(paths + "/")
                                
                    if count ==0:
                        path_list_not_found_st3.append(paths + "/"  + folds)

        if len(paths_to_folders) !=0:
            output_console2.append("- Prochazím tyto cesty: ")
            for items in paths_to_folders:
                output_console2.append(items+"\n")
            

            #cont = input("ANO/NE? (enter/n): \n") #CONTINUE?
        else:
            output_console2.append("- Chyba: aplikace programovana na pruchod 3 slozek, tzn.: path + \"2023_04_13/A/Height\"")
            print("- Chyba: aplikace programovana na pruchod 3 slozek, tzn.: path + \"2023_04_13/A/Height\"")

        # HLAVNI FOR CYKLUS //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////    
        for paths in paths_to_folders:
            if paths.endswith("/"):
                path=paths
            else:
                path = paths + "/"
            print("\n//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
            output.append("\nTrideni v: " + path)
            print(f"- Provadim trideni v ceste: {path}")
            print("//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n")
            #MAIN///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
            v=verification()
            folders = sync_folders(path)
            #naschromáždění souborů na jedno místo
            
            v.Collect_files()

            #třídění do polí, zjišťování suffixu
            v.Get_suffix()
            v.Sorting_files()

            #odstranění prázdných složek včetně základních (exception = 0)
            remove_empty_dirs(0)
            #basic_sort()
            if v.error == 1:
                output.append("Chyba: v zadané cestě nebyly nalezeny žádné soubory (nebo chybí rozhodovací symbol: &)\nNebo je vložená cestak souborům ob více, jak jednu složku")
                output.append("Třídění ukončeno")
            else:
                advance_sort()
                sort_options = ["","typu souborů","funkce","čísla kamery","funkce i čísla kamery"]
                final_text = "Třídění podle: " + sort_options[selected_sort] + " bylo provedeno"
                output.append(final_text)

    else:        
        #MAIN///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        v=verification()
        folders = sync_folders(path)
        #naschromáždění souborů na jedno místo
        
        v.Collect_files()

        #třídění do polí, zjišťování suffixu
        v.Get_suffix()
        v.Sorting_files()

        #odstranění prázdných složek včetně základních (exception = 0)
        remove_empty_dirs(0)
        #basic_sort()
        if v.error == 1:
            output.append("Chyba: v zadané cestě nebyly nalezeny žádné soubory (nebo chybí rozhodovací symbol: &)\nNebo je vložená cestak souborům ob více, jak jednu složku")
            output.append("Třídění ukončeno")
        else:
            advance_sort()
            sort_options = ["","typu souborů","funkce","čísla kamery","funkce i čísla kamery"]
            final_text = "Třídění podle: " + sort_options[selected_sort] + " bylo provedeno"
            output.append(final_text)


    return output









