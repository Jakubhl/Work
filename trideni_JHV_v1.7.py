import os
import shutil

#verze 1.7 pocita s vice slozkama se stejnymi soubory

path = ""
print("Třídění .Normal a .Height souborů...")

# zadejte cestu k souboru:
#path = input("Zadejte cestu k souboru (pokud se aplikace už nachází v daném souboru -> enter): ")

path = "D:/JHV\Kamery\JHV_Data/L_St_145/A"

#spusteni v souboru, kde se aplikace aktualne nachazi
if path == "":
    path = os.getcwd()

#opravy cesty k souboru:

backslash = "\ "

if backslash[0] in path:
    newPath = path.replace(os.sep, '/')
    path = newPath

if path.endswith('/') == False:
    newPath = path + "/"
    path = newPath

#vyhledavani slozek se soubory
folder_name = ['3D','Normal','NOK'] #default
folders = []
normal_in_file = 0
height_in_file = 0

#ochrana aby se za nazvy slozek nebral nejaky soubor z kamery, vytvareni seznamu slozek...
print("analýza složek... ")
for files in os.listdir(path):
    if len(files)<20:
        #ignorace ostatnich typu souboru:   
        if (".v" or ".exe" or ".txt" or ".bmp") not in files:
            folders.append(files)

zvoleno_normal = 0
zvoleno_height = 0

#hledani, ktera slozka obsahuje jake soubory- nastavi se jako primarni:
for i in range(0,len(folders)):
    jiz_napsano = 0
    normal_in_file = 0
    height_in_file = 0

    for files in os.listdir(path + folders[i]):
        #aby to nekontrolovalo slozku s nok soubory:
        if "NOK" not in folders[i]:
            if ".Normal" in files:
                normal_in_file +=1          
                
            if ".Height" in files:
                height_in_file +=1

    #nasleduje ujistovani, zda je soubor opravdu urcen prevazne pro normal soubory:
    if (normal_in_file>10) and (height_in_file == 0):  
        if zvoleno_normal == 0:
            folder_name[1] = folders[i]
            print("pro .normal soubory byla zvolena složka: ", folders[i])
            zvoleno_normal = +1
        #kdyz jiz zvoleno -> obsah vsech ostatnich slozek presunut do spolecne slozky pro trideni 
        else:
            for files in os.listdir(path + folders[i]):
                shutil.move(path + folders[i] + "/" + files, path + files)        

    #pokude slozk(a/y) obsahuje oba typy souboru zaroven, tak se soubory presunou pro trideni do spolecne slozky
    elif (normal_in_file != 0) and (height_in_file != 0):
        if jiz_napsano == 0:
            print("složka", folders[i], "obsahuje oba typy souborů zároveň !")
            jiz_napsano += 1
        for files in os.listdir(path + folders[i]):
            shutil.move(path + folders[i] + "/" + files , path + '/' + files)

    if (height_in_file>10 and normal_in_file == 0):
        if zvoleno_height == 0:
            folder_name[0] = folders[i]
            print("pro .height soubory byla zvolena složka: ", folders[i])
            zvoleno_height += 1                       
        else:          
            for files in os.listdir(path + folders[i]):
                shutil.move(path + folders[i] + "/" + files , path + '/' + files)
                
    elif (height_in_file != 0) and (normal_in_file != 0):
        if jiz_napsano == 0:
            print("složka", folders[i], "obsahuje oba typy souborů zároveň !")
            jiz_napsano += 1
        for files in os.listdir(path + folders[i]):
            shutil.move(path + folders[i] + "/" + files, path + files)


names = os.listdir(path) # default slozka, kde mohou být soubory mimo složky
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


advanced_mode = input("advanced mode?: (Y/n)")
#if advanced_mode == ('Y' or 'y'):
if advanced_mode.casefold() == "y":
    hide_cnt = input("Zadejte počet zakrytých znaků od konce názvu souboru (defaut: 19, smazané znaky: _21_&Cam1Img.Height): ")


hide_cnt_from_start = len("221013_092241_0000000842_21_&Cam1Img.Height") - int(hide_cnt)

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
        #případ, že není v zadne slozce:
        if os.path.exists(path + arr_normal[i]):
            shutil.move(path + arr_normal[i], path + folder_name[2] + '/' + arr_normal[i]) # -> NOK (solo) dir   
        #pripad, že je ve slozce 3D:               
        #elif os.path.exists(path + folder_name[0] + "/" + arr_normal[i]):
        #    shutil.move(path + folder_name[0] + "/" + arr_normal[i], path + folder_name[2] + '/' + arr_normal[i]) # -> NOK (solo) dir
        #pripad, že je ve slozce normal:
        elif os.path.exists(path + folder_name[1] + "/" + arr_normal[i]):
            shutil.move(path + folder_name[1] + "/" + arr_normal[i], path + folder_name[2] + '/' + arr_normal[i]) # -> NOK (solo) dir
        
    else:
        #pripad, ze je uz ve slozce normal neni treba resit...
        #případ, že není v zadne slozce:
        if os.path.exists(path + arr_normal[i]):
            shutil.move(path + arr_normal[i], path + folder_name[1] + '/' + arr_normal[i]) # -> OK - .Normal dir
        #pripad, že je ve slozce 3D: 
        #elif os.path.exists(path + folder_name[0]+ arr_normal[i]):
        #    shutil.move(path + folder_name[0] + "/"+ arr_normal[i], path + folder_name[1] + '/' + arr_normal[i]) # -> OK z 3D presun do normal

        
for j in range (0,height_count):
    if arr_height_cut[j] not in arr_normal_cut:
        if not os.path.exists(path + folder_name[2]):
            os.makedirs(path + folder_name[2])
        print(arr_height[j] + ' -> NOK')
        nok_count += 1
        if os.path.exists(path + arr_height[j]):
            shutil.move(path + arr_height[j], path + folder_name[2] + '/' + arr_height[j]) # -> NOK (solo) dir
        elif os.path.exists(path + folder_name[0] + "/" + arr_height[j]):
            shutil.move(path + folder_name[0] + "/" + arr_height[j], path + folder_name[2] + '/' + arr_height[j]) # -> NOK (solo) dir
        #elif os.path.exists(path + folder_name[1] + "/" + arr_height[j]):
        #    shutil.move(path + folder_name[1] + "/" + arr_height[j], path + folder_name[2] + '/' + arr_height[j]) # -> NOK (solo) dir
    else:
        if os.path.exists(path + arr_height[j]):
            shutil.move(path + arr_height[j], path + folder_name[0] + '/' + arr_height[j]) # -> OK - .Height, 3D dir
        #elif os.path.exists(path + folder_name[1]+ arr_height[j]):
        #    shutil.move(path +folder_name[1] + "/"+ arr_height[j], path + folder_name[0] + '/' + arr_height[j]) # -> OK - z normal presun do 3D

print("třídění dokončeno ")
print("celkový počet NOK souborů: ",nok_count)
        
#k=input("press close to exit")

#print(folder_name)
#print(arr_normal_cut)