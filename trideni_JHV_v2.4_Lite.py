# -verze 2.4 je univerzální vůči počtu formátů souborů
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
import os
import shutil
import re


def whole_function():

    prefix_func = "Func_"
    prefix_Cam = "Cam"


    def remove_empty_dirs(exception):
        removed_count = 0
        folders = sync_folders()
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
                            removed_count +=1
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
                        removed_count +=1
            if removed_count != 0:
                print(" - Přebytečné složky odstraněny")
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
            folders = sync_folders()
            
            for i in range(0,len(folders)):
                for files in os.listdir(path + folders[i]):
                    if ".bmp" in files:
                        shutil.move(path + folders[i] + "/" + files , path + '/' + files)     

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
            files_arr = []
            files_cut = 0
            nok_count = 0
            ok_count = 0
            cutting_condition = "&"
            count=0
            error_length = 0

            # výtah z názvu vhodný pro porovnání:
            for files in os.listdir(path):
                if ".bmp" in files:
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
                    #shutil.move(path + '/' + files_arr[i] , path + files_arr[i]) #přesun do zakladni složky
                    count = 0
                    
                else:
                    nok_count += 1
                    shutil.move(path + '/' + files_arr[i] , path + folder_name[0] + "/" + files_arr[i]) #přesun do Temp složky
                    count = 0
            
            #if error_length == 1:
                #print("Upozornění: délka názvu před \"&\" některých souborů v dané cestě se liší (možná nefunkční manuální definice zakrytých znaků)")
                #print("")

            if files_arr == []:
                print("Chyba: Nebyly nalezeny žádné soubory")
                self.error = 1

            else:
                print(" - Nepáry, celkem: {}".format(nok_count))
                print(" - OK soubory zastoupené všemi formáty, celkem: {}".format(ok_count))
                print("")

        def creating_folders(self):
            #podle typu souboru:
            if sort_by == 1:
                for i in range(0,len(self.files_type_arr)):
                    new_folder_name = self.files_type_arr[i]
                    if not os.path.exists(path + new_folder_name):
                        os.mkdir(path + new_folder_name)
                        if not new_folder_name in folder_name:
                            folder_name.append(new_folder_name)        
                    else:
                        if not new_folder_name in folder_name:
                            folder_name.append(new_folder_name)      
        def moving_files(self):
            files_split = ""
            #presun souboru do slozek:
            if sort_by == 1:
                for files in os.listdir(path):
                    if ".bmp" in files:
                        for items in folder_name:
                            if items in files:
                                if not os.path.exists(path + items + "/" + files):
                                    shutil.move(path + files, path + items + "/" + files)     

    #MAIN//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////        
    path = ""
    print(" - Třídění souborů z průmyslových kamer...")
    print("")

    # zadejte cestu k souboru:
    path_found = 0
    stop_while = 0
    while path_found == 0 and stop_while == 0:
        path = input("Zadejte cestu k souborům (pokud se aplikace už nachází v dané složce -> enter): ")

        #path = "D:\JHV\Kamery\JHV_Data/2023_04_13\A"

        #spusteni v souboru, kde se aplikace aktualne nachazi
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
            print("Zadaná cesta k souborům nebyla nalezena")
            stop_while = 1 #ochrana proti neustalemu vypisovani
        else:
            path_found = 1

    if path_found == 1:
        folder_name = ['Temp'] #default
        sort_by = 0

        #vytvareni zakladnich slozek:
        def make_folders():
            if not os.path.exists(path + folder_name[0]):
                os.mkdir(path + folder_name[0] + "/")

        make_folders()
        #ochrana aby se za nazvy slozek nebral nejaky soubor z kamery, vytvareni seznamu slozek...
        print("Analýza složek... ")
        def sync_folders():
            folders = []
            unsupported_formats = [".exe",".pdf",".ifz",".bmp",".txt",".v",".xml",".changed",".doc",".docx",".xls",".xlsx",".ppt",".pptx",".csv",".py",".msi"]
            if os.path.exists(path):
                for files in os.listdir(path):
                    #ignorace ostatnich typu souboru:
                    unsupported_format =0
                    for suffixes in unsupported_formats:
                        if suffixes in files:
                            unsupported_format +=1
                    if unsupported_format ==0:
                        folders.append(files)
            return folders

        folders = sync_folders()
        #vzorek pro automatickou úpravu různě dlouhých jmen (první blok v sorting_files), delší= zakreje méně znaků, kratší = více...
        example_file_name = ""
        for i in range(0, len(folders)):
            for files in os.listdir(path+folders[i]):
                if ".bmp" in files:
                    if example_file_name == "":
                        example_file_name = files
                        
        example_file_name_cut = example_file_name.split("&")
        example_file_name_cut = example_file_name_cut[0]
        #example_file_name = "221013_092241_0000000842_21_" #&Cam1Img.Height.bmp" #uz pracuju s takto orizlym...
        hide_cnt = 4 #23   # defaultní počet zakrytých znaků při porovnávání normal a height souborů od & doleva

        #naschromáždění souborů na jedno místo
        v=verification()
      
        if v.error == 1:
            print("Chyba: v zadané cestě nebyly nalezeny žádné soubory (nebo chybí rozhodovací symbol: &), třídění ukončeno")

        else:

            def advance_sort(sort_by):
                if sort_by == 1:
                    
                    v.Collect_files()
                    v.Get_suffix()
                    v.Sorting_files()
         
                    v.creating_folders()
                    print(" - Vytváření složek: hotovo")
                    v.moving_files()
                    print(" - Přesouvání souborů: hotovo")
                    print("")

                    remove_empty_dirs(0)

            sort_by = 1
            advance_sort(sort_by)

            print(" - Třídění dokončeno")
            print("")

    #repeat = input("Opakovat? (Y/y) nebo stisknětě libovolný znak pro zavření: ")
    #if repeat.casefold() == "y":
    #    whole_function()
    #    repeat = ""

whole_function() #pouze jednou pri spusteni...






