# -verze 2.4 je univerzální vůči počtu formátů souborů
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
import os
import shutil
import re

prefix_func = "Func_"
prefix_Cam = "Cam"


def remove_empty_dirs(exception):
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
        print("Přebytečné složky odstraněny")
                    
    else:
        for dirs in folders: # pole folders uz je filtrovano od ostatnich souboru...
            number_of_files = 0
            if os.path.exists(path + dirs):
                for files in os.listdir(path + dirs):
                    number_of_files +=1
                if number_of_files == 0:
                    print("Odstraněna prázdná složka: ", dirs)
                    os.rmdir(path + dirs)
        print("Přebytečné složky odstraněny")
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
                shutil.move(path + folders[i] + "/" + files , path + '/' + files)

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
            print("Chyba: soubor {} neobsahuje rozhodovaci symbol \"&\"".format(file_for_analyze))

        
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
                shutil.move(path + '/' + files_arr[i] , path + folder_name[0] + "/" + files_arr[i]) #přesun do OK složky
                count = 0
                
            else:
                nok_count += 1
                shutil.move(path + '/' + files_arr[i] , path + folder_name[1] + "/" + files_arr[i]) #přesun do NOK složky
                count = 0
        
        if error_length == 1:
            print("Upozornění: délka názvu před \"&\" některých souborů v dané cestě se liší (možná nefunkční manuální definice zakrytých znaků)")
            print("")

        if files_arr == []:
            print("Chyba: Nebyly nalezeny žádné soubory")
            self.error = 1

        else:
            print(" - NOK soubory nezastoupené všemi formáty, celkem: {}".format(nok_count))
            print(" - OK soubory zastoupené všemi formáty, celkem: {}".format(ok_count))
            print("")
        
    def sort_by_camera(self):
        camera_num = 0
        for files in os.listdir(path + folder_name[0]): #hledani v OK slozce
            if ".bmp" in files: #pouze pro overeni, zda se jedna o uzitecny soubor
                camera_num = verification.Get_cam_number(files)
                if not camera_num in self.cameras_arr:
                    self.cameras_arr.append(camera_num)
                    self.cameras_arr.sort()
                    
        print(" - Nalezená čísla kamer: ")
        print(self.cameras_arr)
        print("")

        
    def sort_by_function(self):
        func_num = 0
        for files in os.listdir(path + folder_name[0]): #hledani v OK slozce
            if ".bmp" in files: #pouze pro overeni, zda se jedna o uzitecny soubor
                func_num = verification.Get_func_number(files)
                if not func_num in self.functions_arr:
                    self.functions_arr.append(func_num)
                    self.functions_arr.sort()

        print(" - Nalezená čísla funkcí: ")
        print(self.functions_arr)
        print("")

        
    def sort_by_both(self):
        both_name = ""
        for files in os.listdir(path + folder_name[0]): #hledani v OK slozce
            # zjišťování všech čísel kamer
            if ".bmp" in files:#pouze pro overeni, zda se jedna o uzitecny soubor
                func_num = verification.Get_func_number(files)
                camera_num = verification.Get_cam_number(files)
                both_name = prefix_Cam + str(camera_num) + "_" + prefix_func + str(func_num)
                if not both_name in self.both_arr:
                    self.both_arr.append(both_name)
                
        print(" - Složky pro vytvoření")           
        print(self.both_arr)
        print("")

    def creating_folders(self):

        if sort_by == 1:
            for i in range(0,len(self.functions_arr)):
                new_folder_name = prefix_func + self.functions_arr[i]
                if not os.path.exists(path + new_folder_name):
                    os.mkdir(path + new_folder_name)
                    if not new_folder_name in folder_name:
                        folder_name.append(new_folder_name)

        #vytvareni slozek pro kamery:
        if sort_by == 2:
            for i in range(0,len(self.cameras_arr)):
                new_folder_name = prefix_Cam + self.cameras_arr[i]
                if not os.path.exists(path + new_folder_name):
                    os.mkdir(path + new_folder_name) 
                    if not new_folder_name in folder_name:
                        folder_name.append(new_folder_name)

        if sort_by == 3:
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
            for files in os.listdir(path + folder_name[0]): #v OK slozce
                func_num = verification.Get_func_number(files)
                for items in folder_name:
                    if (prefix_func + func_num) == items:
                        if not os.path.exists(path + items + "/" + files):
                            shutil.move(path + folder_name[0] + "/" + files, path + items + "/" + files)

        if sort_by == 2:
            for files in os.listdir(path + folder_name[0]): #v OK slozce
                camera_num = verification.Get_cam_number(files)
                for items in folder_name:
                    if (prefix_Cam + camera_num) == items:
                        if not os.path.exists(path + items + "/" + files):
                            shutil.move(path + folder_name[0] + "/" + files, path + items + "/" + files)
        
        if sort_by == 3:
            for files in os.listdir(path + folder_name[0]): #v OK slozce
                func_num = verification.Get_func_number(files)
                camera_num = verification.Get_cam_number(files)
                for items in folder_name:
                    if (prefix_Cam + camera_num + "_" + prefix_func + func_num) == items:
                        if not os.path.exists(path + items + "/" + files):
                            shutil.move(path + folder_name[0] + "/" + files, path + items + "/" + files)

        

#MAIN//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////        
path = ""
print(" - Třídění souborů z průmyslových kamer...")
print("")

# zadejte cestu k souboru:
path_found = 0
stop_while = 0
while path_found == 0 and stop_while == 0:
    path = input("Zadejte cestu k souborům (pokud se aplikace už nachází v dané složce -> enter): ")

    #path = "D:/JHV\Kamery\JHV_Data/L_St_145/A"

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
    folder_name = ['OK','NOK'] #default
    sort_by = 0

    #vytvareni zakladnich slozek:
    for x in range(0,len(folder_name)):
        if not os.path.exists(path + folder_name[x]):
            os.mkdir(path + folder_name[x] + "/")

    #ochrana aby se za nazvy slozek nebral nejaky soubor z kamery, vytvareni seznamu slozek...
    print("Analýza složek... ")
    def sync_folders():
        folders = []
        for files in os.listdir(path):
            #ignorace ostatnich typu souboru:   
            if not ".exe" in files:
                if not ".bmp" in files:
                    if not ".txt" in files:
                        if not ".v" in files:
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
    v.Collect_files()

    #třídění do polí, zjišťování suffixu
    v.Get_suffix()
    v.Sorting_files()

    #odstranění prázdných složek včetně základních (exception = 0)
    remove_empty_dirs(0)

    if v.error == 1:
        print("Chyba: v zadané cestě nebyly nalezeny žádné soubory (nebo chybí rozhodovací symbol: &), třídění ukončeno")

    else:

        def advance_sort(sort_by):
            if sort_by == 1:
                v.sort_by_function()
                print(" - Třídění podle funkce: hotovo")
                v.creating_folders()
                print(" - Vytváření složek: hotovo")
                v.moving_files()
                print(" - Přesouvání souborů: hotovo")
                print("")
                remove_empty_dirs(0)

            elif sort_by == 2:
                v.sort_by_camera()
                print(" - Třídění podle kamery: hotovo")
                v.creating_folders()
                print(" - Vytváření složek: hotovo")
                v.moving_files()
                print(" - Přesouvání souborů: hotovo")
                print("")
                remove_empty_dirs(0)

            elif sort_by == 3:
                v.sort_by_both()
                print(" - Třídění podle kamery a funkce: hotovo")
                v.creating_folders()
                print(" - Vytváření složek: hotovo")
                v.moving_files()
                print(" - Přesouvání souborů: hotovo")
                print("")
                remove_empty_dirs(0)

        #uvedeni do advanced modu:
        #jakýkoliv jiný znak je brán jako ne:
        advanced_mode = input("Nastavit možnosti podrobnějšího třídění?: (Y/n)")
        if advanced_mode.casefold() == "y":
            print("Třídit podle čísla funkce? (1), podle čísla kamery? (2), podle funkce i kamery? (3) nebo manuálně nastavit počet zakrytých znaků? (4):")
            #ověření správného vstupu:
            inp = input_check(1, 5)
            sort_by = int(inp.is_input_right())
            advance_sort(sort_by)

            if sort_by == 4:
                decrease = 0
                file_name_letters = []
                file_name_letters_position = 28 #default
                file_name_letters_position_arr = []
                print("Zadejte počet zakrytých znaků od & vlevo, default 4: (221013_092241_0000000842  |<=|  _21_&Cam1Img.Height.bmp) ")
                print("")

                for letters in example_file_name_cut:
                    if file_name_letters_position < 10:
                        file_name_letters.append(letters + "|")
                    else:
                        file_name_letters.append(" " + letters + "|") #pridani mezery

                    decrease +=1
                    file_name_letters_position  = len(example_file_name_cut) - decrease
                    file_name_letters_position_arr.append(str(file_name_letters_position + 1) + "|")

                file_name_letters = ''.join([str(elem) for elem in file_name_letters])
                file_name_letters_position_arr = ''.join([str(elem) for elem in file_name_letters_position_arr])

                print("znak:         ", file_name_letters, "&CamxImg.xxxxxx.bmp") 
                print("počet zakrytí:", file_name_letters_position_arr)

                inp = input_check(1, len(example_file_name_cut)+1)
                hide_cnt = int(inp.is_input_right())
                hide_cnt_from_start = len(example_file_name_cut) - int(hide_cnt)
                print("Porovnává se: ", example_file_name_cut[0:hide_cnt_from_start])
                print("")

                v.Collect_files()
                v.Sorting_files()

                advanced_mode = input("Nastavit možnosti podrobnějšího třídění?: (Y/n)")
                if advanced_mode.casefold() == "y":
                    print("Třídit podle čísla funkce? (1), podle čísla kamery? (2), podle funkce i kamery? (3)")
                    #ověření správného vstupu:
                    inp = input_check(1, 4)
                    sort_by = int(inp.is_input_right())
                    advance_sort(sort_by)

        print(" - Třídění dokončeno")

k = input("stisknětě jakýkoliv znak pro zavření")



