 # -verze 2.4 je univerzální vůči počtu formátů souborů
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
import os
import shutil
import re

global prefix_func
prefix_func = "_Func_"
global prefix_Cam
prefix_Cam = "_Cam"


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
#funkce pro overeni spravneho inputu
class input_check:
    def __init__(self,range_from, range_to):
        self.right_input = 0
        self.range_to = range_to
        self.range_from = range_from

    def is_input_right(self):
        wrong_input = 1
        self.right_input = input("Vepište číslo v rozsahu: {}-{}: ".format(self.range_from,self.range_to-1))

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
        print("nalezené typy souborů: ")
        print(files_type_arr)

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
                count = 0
                
            else:
                self.nok_arr.append(files_arr_cut[i])
                nok_count += 1
                shutil.move(path + '/' + files_arr[i] , path + "NOK" + "/" + files_arr[i]) #přesun do NOK složky
                count = 0

        print("soubory nezastoupené všemi formáty, celkem: {}".format(nok_count))
        #print(self.nok_arr)
        #print(self.ok_arr)      



#MAIN//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////        
path = ""
print("Třídění .Normal a .Height souborů...")

# zadejte cestu k souboru:
path_found = 0
while path_found == 0:
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
    else:
        path_found = 1
#vyhledavani slozek se soubory
folder_name = ['3D','Normal','NOK'] #default
folders = []

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

#odstranění prázdných složek včetně základních (exception = 0)
remove_empty_dirs(0)

if not os.path.exists(path + "NOK"):
    os.mkdir(path + "NOK" + "/")

#třídění do polí
v.Sorting_files()

k = input("stisknětě jakýkoliv znak pro zavření")



