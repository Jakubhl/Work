 # -verze 2.4 je univerzální vůči počtu formátů souborů
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
import os
import shutil
import re

global prefix_func
prefix_func = "Func_"
global prefix_Cam
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
        self.nok_arr = []
        self.ok_arr = []
        self.cameras_clear = []
        self.functions_clear = []
        self.sort_by_camera_done = False
        self.sort_by_function_done = False
        self.creating_folders_done = False
        self.moving_files_done = False

    def Collect_files(self):
        for i in range(0,len(folders)):
            for files in os.listdir(path + folders[i]):
                shutil.move(path + folders[i] + "/" + files , path + '/' + files)

    def Sorting_files(self):
        n = 0
        example_folder_name = "221013_092241_0000000842_21_" #&Cam1Img.Height.bmp" #uz pracuju s takto orizlym...
        hide_cnt = 4 #23   # defaultní počet zakrytých znaků při porovnávání normal a height souborů
        hide_cnt_from_start = len(example_folder_name) - int(hide_cnt)
        files_type = ""
        files_type_arr = []
        files_arr_cut = []
        files_arr = []
        files_cut = 0
        nok_count = 0
        cutting_condition = "&"
        count=0

        #zjišťování počtu typů souborů
        for files in os.listdir(path):
            if "&Cam" in files:
                files_type = files.split(".")
                if not files_type[1] in files_type_arr:
                    files_type_arr.append(files_type[1]) 
        print(" - Nalezené typy souborů: ")
        print(files_type_arr)
        print("")

        # výtah z názvu vhodný pro porovnání:
        for files in os.listdir(path):
            if "&Cam" in files:
                files_arr.append(files) #pole s plnými názvy pro přesun
                files_cut = files.split(cutting_condition)
                if len(files_cut[0]) > len(example_folder_name) or len(files_cut[0]) < len(example_folder_name):
                    n = len(files_cut[0]) - len(example_folder_name) # (=43)
                    files_arr_cut.append(files[0:(hide_cnt_from_start + n)])
                    n = 0
                else:
                    files_arr_cut.append(files[0:hide_cnt_from_start])

        for i in range(0,len(files_arr_cut)):
        
            for files in files_arr_cut:
                if files == files_arr_cut[i]:
                    count+=1

            if count == len(files_type_arr): # overeni zda je od vsech typu souboru jeden
                self.ok_arr.append(files_arr_cut[i])
                shutil.move(path + '/' + files_arr[i] , path + folder_name[0] + "/" + files_arr[i]) #přesun do OK složky
                count = 0
                
            else:
                self.nok_arr.append(files_arr_cut[i])
                nok_count += 1
                shutil.move(path + '/' + files_arr[i] , path + folder_name[1] + "/" + files_arr[i]) #přesun do NOK složky
                count = 0

        print(" - NOK soubory nezastoupené všemi formáty, celkem: {}".format(nok_count))
        print("")
        print(files_arr_cut)
        #print(self.nok_arr)
        #print(self.ok_arr)
        
    def sort_by_camera(self):
        cameras = []
        camera_num = 0
        files_split = ""

        for files in os.listdir(path + folder_name[0]): #hledani v OK slozce
            # zjišťování všech čísel kamer
            if "&Cam" in files:
                files_split = files.split("_")
                files_split = files_split[4] # čtvrtá sekce podle _
                camera_num = re.findall(r'\d+', files_split[0:5]) # pocita az s peticifernym cislem kamery
                if not camera_num in cameras:
                    cameras.append(camera_num)
                    cameras.sort()

        print(" - Nalezená čísla kamer: ")
        self.cameras_clear = [str(item).strip("\'\"\[\]") for item in cameras]
        print(self.cameras_clear)
        print("")

        self.sort_by_camera_done = True
        
    def sort_by_function(self):
        functions = []
        func_num = 0
        files_split = ""

        for files in os.listdir(path + folder_name[0]): #hledani v OK slozce
            files_split = files.split("_")
            # zjišťování všech čísel funkci
            if "&Cam" in files: #pouze pro overeni, zda se jedna o uzitecny soubor
                func_num = re.findall(r'\d+', files_split[3]) # čísla, třetí sekce podle _
                if not func_num in functions:
                    functions.append(func_num)
                    functions.sort()

        print(" - Nalezená čísla funkcí: ")
        self.functions_clear = [str(item).strip("\'\"\[\]") for item in functions]
        print(self.functions_clear)
        print("")

        self.sort_by_function_done = True

    def creating_folders(self):
        #vytvareni slozek pro kamery:
        if sort_by == 2:
            for i in range(0,len(self.cameras_clear)):
                new_folder_name = prefix_Cam + self.cameras_clear[i]
                if not os.path.exists(path + new_folder_name):
                    os.mkdir(path + new_folder_name) 
                    if not new_folder_name in folder_name:
                        folder_name.append(new_folder_name)
        if sort_by == 1:
            for i in range(0,len(self.functions_clear)):
                new_folder_name = prefix_func + self.functions_clear[i]
                if not os.path.exists(path + new_folder_name):
                    os.mkdir(path + new_folder_name)
                    if not new_folder_name in folder_name:
                        folder_name.append(new_folder_name)

        self.creating_folders_done = True

    def moving_files(self):
        files_split = ""
        #presun souboru do slozek:
        if sort_by == 2:
            for files in os.listdir(path + folder_name[0]): #v OK slozce
                files_split = files.split("_")
                files_split = files_split[4] # čtvrtá sekce podle _
                files_split = re.findall(r'\d+', files_split[0:5]) # pocita az s peticifernym cislem kamery
                files_split = ' '.join([str(elem) for elem in files_split]) #ziskani stringu z pole
                for items in folder_name:
                    if str((prefix_Cam + files_split)) == items:
                        if not os.path.exists(path + items + "/" + files):
                            shutil.move(path + folder_name[0] + "/" + files, path + items + "/" + files)

        if sort_by == 1:
            for files in os.listdir(path + folder_name[0]): #v OK slozce
                files_split = files.split("_")
                for items in folder_name:
                    if (prefix_func + files_split[3]) == items:
                        if not os.path.exists(path + items + "/" + files):
                            shutil.move(path + folder_name[0] + "/" + files, path + items + "/" + files)

        self.moving_files_done = True
        

#MAIN//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////        
path = ""
print(" - Třídění .Normal a .Height souborů...")
print("")

# zadejte cestu k souboru:
path_found = 0
while path_found == 0:
    #path = input("Zadejte cestu k souborům (pokud se aplikace už nachází v dané složce -> enter): ")

    path = "D:/JHV\Kamery\JHV_Data/L_St_145/A"

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
    else:
        path_found = 1
#vyhledavani slozek se soubory
folder_name = ['OK','NOK'] #default
folders = []
sort_by = 0

#vytvareni zakladnich slozek:
for x in range(0,len(folder_name)):
    if not os.path.exists(path + folder_name[x]):
        os.mkdir(path + folder_name[x] + "/")


#ochrana aby se za nazvy slozek nebral nejaky soubor z kamery, vytvareni seznamu slozek...
print("Analýza složek... ")
for files in os.listdir(path):
    #ignorace ostatnich typu souboru:   
    if not ".exe" in files:
        if not ".bmp" in files:
            if not ".txt" in files:
                if not ".v" in files:
                    folders.append(files)


#naschromáždění souborů na jedno místo
v=verification()
v.Collect_files()

#třídění do polí
v.Sorting_files()

#odstranění prázdných složek včetně základních (exception = 0)
remove_empty_dirs(0)

#uvedeni do advanced modu:
#jakýkoliv jiný znak je brán jako ne:
advanced_mode = input("Advanced mode?: (Y/n)")
if advanced_mode.casefold() == "y":
    print("Třídit podle čísla funkce? (1) ,podle čísla kamery? (2) nebo podle funkce i kamery? (3):")
    #ověření správného vstupu:
    inp = input_check(1, 4)
    sort_by = int(inp.is_input_right())

    if sort_by == 1:
        #while(v.sort_by_function_done != True):
        v.sort_by_function()
        print(" - Třídění podle funkce: hotovo")
        #while(v.creating_folders_done != True):
        v.creating_folders()
        print(" - Vytváření složek: hotovo")
        #while(v.moving_files_done != True):
        v.moving_files()
        print(" - Přesouvání souborů: hotovo")
        print("")
        remove_empty_dirs(0)

    if sort_by == 2:
        #while(v.sort_by_camera_done != True):
        v.sort_by_camera()
        print(" - Třídění podle kamery: hotovo")
        #while(v.creating_folders_done != True):
        v.creating_folders()
        print(" - Vytváření složek: hotovo")
        #while(v.moving_files_done != True):
        v.moving_files()
        print(" - Přesouvání souborů: hotovo")
        print("")
        remove_empty_dirs(0)

print(" - Třídění dokončeno")

#k = input("stisknětě jakýkoliv znak pro zavření")



