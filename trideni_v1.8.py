

#verze 1.8 umoznuje analýzu existujících slozek a vyber defautnich slozek pro presun
# - je osetrena situace zadani spatnich znaku do inputu funkci is_input_right

import os
import shutil

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
        print("zadaná cesta k souborům nebyla nalezena")
    else:
        path_found = 1


#vyhledavani slozek se soubory
folder_name = ['3D','Normal','NOK'] #default
folders = []

#ochrana aby se za nazvy slozek nebral nejaky soubor z kamery, vytvareni seznamu slozek...
print("analýza složek... ")
for files in os.listdir(path):
    if len(files)<20:
        #ignorace ostatnich typu souboru:   
        if (".v" or ".exe" or ".txt" or ".bmp") not in files:
            folders.append(files)


dir_height = []
dir_normal = []

#funkce pro overeni spravneho inputu
def is_input_right(range_from, range_to):
    wrong_input = 1
    is_input_right.right_input = input("vepište číslo v rozsahu: {}-{}: ".format(range_from,range_to-1))

    while wrong_input == 1:
        if is_input_right.right_input.isdigit():

            if int(is_input_right.right_input) not in range(range_from,range_to):
                is_input_right.right_input = input("zadali jste číslo mimo rozsah (vepište číslo v rozsahu: {}-{}): ".format(range_from,range_to-1))

            else:
                wrong_input = 0

        else:
            is_input_right.right_input = input("Nezadali jste číslo (vepište číslo {}-{}): ".format(range_from,range_to-1))

    return is_input_right.right_input

#hledani, ktera slozka obsahuje jake soubory- nastavi se jako primarni:
for i in range(0,len(folders)):
    normal_in_file = 0
    height_in_file = 0

    for files in os.listdir(path + folders[i]):
        #aby to nekontrolovalo slozku s nok soubory:
        if "NOK" not in folders[i]:
            if ".Normal" in files:
                normal_in_file +=1          
                
            if ".Height" in files:
                height_in_file +=1               

    #pokude slozk(a/y) obsahuje oba typy souboru zaroven, tak se soubory presunou pro trideni do spolecne slozky
    if (normal_in_file != 0) and (height_in_file != 0):
        for files in os.listdir(path + folders[i]):
            shutil.move(path + folders[i] + "/" + files , path + '/' + files)   
                   
    if (height_in_file != 0) and (normal_in_file != 0):
        for files in os.listdir(path + folders[i]):
            shutil.move(path + folders[i] + "/" + files, path + files)

#nasleduje ujistovani, zda je soubor opravdu urcen prevazne pro normal soubory:
    if (normal_in_file>0) and (height_in_file == 0):
        dir_normal.append(folders[i])

    if (height_in_file>0 and normal_in_file == 0):
        dir_height.append(folders[i])

#Voleni defaultni slozky (pripad vice slozek se stejnymi soubory)--------------------------------------------------------------------------------------------------------

is_selected_normal_dir = 0
is_selected_height_dir = 0

while is_selected_normal_dir == 0:
    if len(dir_normal) > 1:
        print("Seznam složek s .normal soubory: ",dir_normal)
        print("Bylo nalezeno více složek se soubory .normal, zvolte defaultní (vepište číslo 0-{}): ".format(len(dir_normal)-1))
        #voani funkce pro spravnou zadanou hodnotu
        is_input_right(0, len(dir_normal))
        select_normal_dir = is_input_right.right_input

        print("Pro .normal soubory byla zvolena složka: ", dir_normal[int(select_normal_dir)])
        #ruseni nezvolenych slozek (presun souborů ke trideni):
        folder_name[1] = dir_normal[int(select_normal_dir)]
        for i in range (0,len(dir_normal)):
            if i != int(select_normal_dir):
                for files in os.listdir(path + dir_normal[i]):
                    shutil.move(path + dir_normal[i] + "/" + files, path + files)
                #odstraneni prazdne nevyuzite slozky:
                os.rmdir(path + dir_normal[i])
        is_selected_normal_dir = 1
            
    else:
        if len(dir_normal) != 0:
            folder_name[1] = dir_normal[0]
            print("Pro .normal soubory byla zvolena složka: ", dir_normal[0])
            is_selected_normal_dir = 1
        else:
            print("Nebyla nalezena žádná složka s .normal soubory, byla vytvořena automaticky: ",folder_name[1])
            is_selected_normal_dir = 1


while is_selected_height_dir == 0:
    if len(dir_height) > 1:
        print("Seznam složek s .height soubory: ",dir_height)
        print("Bylo nalezeno více složek se soubory .height, zvolte defaultní (vepište číslo 0-{}): ".format(len(dir_height)-1))
        is_input_right(0, len(dir_height))
        select_height_dir = is_input_right.right_input
        
        print("Pro .height soubory byla zvolena složka: ", dir_height[int(select_height_dir)])
        #ruseni nezvolenych slozek (presun souborů ke trideni):
        folder_name[0] = dir_height[int(select_height_dir)]
        for i in range (0,len(dir_height)):
            if i != int(select_height_dir):
                for files in os.listdir(path + dir_height[i]):
                    shutil.move(path + dir_height[i] + "/" + files, path + files)
                #odstraneni prazdne nevyuzite slozky:
                os.rmdir(path + dir_height[i])
        is_selected_height_dir = 1

    else:
        if len(dir_height) != 0:
            folder_name[0] = dir_height[0]
            print("Pro .height soubory byla zvolena složka: ", dir_height[0])
            is_selected_height_dir = 1
        else:
            print("Nebyla nalezena žádná složka s .height soubory, byla vytvořena automaticky: ",folder_name[0])
            is_selected_height_dir = 1


names = os.listdir(path) # slozka zadana v ceste
normal_count = 0         # pro predstavu o velikosti pole
height_count = 0         # pro predstavu o velikosti pole
nok_count = 0            # pocet osamostatnenych souboru
arr_normal_cut = []      # oriznute nazvy souboru v poli
arr_height_cut = []      # oriznute nazvy souboru v poli
arr_normal = []          # original nazvy souboru v poli
arr_height = []          # original nazvy souboru v poli
hide_cnt = 19            # pocet zakrytych znaku pri porovnavani normal a height souboru

#vytvareni slozek, pokud nejsou vytvoreny:
for x in range(0,2):
    if not os.path.exists(path + folder_name[x]):
       os.makedirs(path + folder_name[x])


advanced_mode = input("Advanced mode?: (Y/n)")
example_folder_name = "221013_092241_0000000842_21_&Cam1Img.Height"

if advanced_mode.casefold() == "y":
    print("Zadejte počet zakrytých znaků od konce názvu souboru (defaut: 19, smazané znaky: _21_&Cam1Img.Height): ")
    #kontrola
    is_input_right(0, len(example_folder_name)+1)
    hide_cnt = is_input_right.right_input
    hide_cnt_from_start = len(example_folder_name) - int(hide_cnt)
    print("příklad zkáceného souboru: ", example_folder_name[0:hide_cnt_from_start])

else:
    hide_cnt_from_start = len(example_folder_name) - int(hide_cnt)

#print("making arrays...")

for files in names:
    
    if ".Normal" in files:
        arr_normal.append(files)
        # 221013_092241_0000000842_21_&Cam1Img.Height
        # 0123456789-123456789-123456789-123456789012
        arr_normal_cut.append(files[0:hide_cnt_from_start])
        normal_count+=1

    if ".Height" in files:
        arr_height.append(files)
        arr_height_cut.append(files[0:hide_cnt_from_start])
        height_count+=1

#custom height slozka
if os.path.exists(path + folder_name[0]+ "/"):
    names2 = os.listdir(path + folder_name[0] + "/")
    for files in names2:

        if ".Normal" in files:
            arr_normal.append(files)
            arr_normal_cut.append(files[0:hide_cnt_from_start])
            normal_count+=1

        if ".Height" in files:
            arr_height.append(files)
            arr_height_cut.append(files[0:hide_cnt_from_start])
            height_count+=1

#custom normal slozka
if os.path.exists(path + folder_name[1]+ "/"):
    names3 = os.listdir(path + folder_name[1] + "/")
    for files in names3:

        if ".Normal" in files:
            arr_normal.append(files)
            arr_normal_cut.append(files[0:hide_cnt_from_start])
            normal_count+=1

        if ".Height" in files:
            arr_height.append(files)
            arr_height_cut.append(files[0:hide_cnt_from_start])
            height_count+=1

print("počet .normal souborů: ", normal_count)
print("počet .height souborů: ", height_count)
if normal_count == 0 and height_count == 0:
    print("V zadané cestě nebyly nalezeny žádné soubory")

#print("sorting into folders...")

for i in range (0,normal_count):    
    if arr_normal_cut[i] not in arr_height_cut:
        if not os.path.exists(path + folder_name[2]):
            os.makedirs(path + folder_name[2])
        print(arr_normal[i] + ' -> NOK')
        nok_count += 1
        normal_count -=1
        #případ, že není v zadne slozce:
        if os.path.exists(path + arr_normal[i]):
            shutil.move(path + arr_normal[i], path + folder_name[2] + '/' + arr_normal[i]) # -> NOK (solo) dir   
        elif os.path.exists(path + folder_name[1] + "/" + arr_normal[i]):
            shutil.move(path + folder_name[1] + "/" + arr_normal[i], path + folder_name[2] + '/' + arr_normal[i]) # -> NOK (solo) dir
        
    else:
        #případ, že není v zadne slozce a je ok:
        if os.path.exists(path + arr_normal[i]):
            shutil.move(path + arr_normal[i], path + folder_name[1] + '/' + arr_normal[i]) # -> OK - .Normal dir
        
for j in range (0,height_count):
    if arr_height_cut[j] not in arr_normal_cut:
        if not os.path.exists(path + folder_name[2]):
            os.makedirs(path + folder_name[2])
        print(arr_height[j] + ' -> NOK')
        nok_count += 1
        height_count -=1
        if os.path.exists(path + arr_height[j]):
            shutil.move(path + arr_height[j], path + folder_name[2] + '/' + arr_height[j]) # -> NOK (solo) dir
        elif os.path.exists(path + folder_name[0] + "/" + arr_height[j]):
            shutil.move(path + folder_name[0] + "/" + arr_height[j], path + folder_name[2] + '/' + arr_height[j]) # -> NOK (solo) dir

    else:
        if os.path.exists(path + arr_height[j]):
            shutil.move(path + arr_height[j], path + folder_name[0] + '/' + arr_height[j]) # -> OK - .Height, 3D dir


print("třídění dokončeno ")
print("počet OK .normal souborů: ", normal_count)
print("počet OK .height souborů: ", height_count)
print("celkový počet NOK souborů: ",nok_count)
        
#k=input("press close to exit")


