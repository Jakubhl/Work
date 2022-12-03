# -verze 2.3 umožňuje v advanced módu třídění podle čísla kamery, podle cisla funkce i oboje zaroven
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
import os
import shutil
import re

#pri zmene prefixu je nutne mit prejmenovane slozky tak, aby neobsahovali stary prefix... jinak jej to bude brat jako zakladni nazev slozek
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

class basic_sorting:
    def __init__(self):
        self.dir_height = []
        self.dir_normal = []
        self.analyzing_done = 0
        self.picking_done = 0
        self.moving_done = 0

    def analyzing_directories(self):

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
            #hledani, ktera slozka obsahuje jake soubory- nastavi se jako primarni:
            #pokude slozk(a/y) obsahuje oba typy souboru zaroven, tak se soubory presunou pro trideni do spolecne slozky
            if (normal_in_file != 0) and (height_in_file != 0):
                for files in os.listdir(path + folders[i]):
                    shutil.move(path + folders[i] + "/" + files , path + '/' + files)   
                        
            if (height_in_file != 0) and (normal_in_file != 0):
                for files in os.listdir(path + folders[i]):
                    shutil.move(path + folders[i] + "/" + files, path + files)

        #nasleduje ujistovani, zda je slozka opravdu urcena prevazne pro normal/height soubory:
            if normal_in_file>0 and height_in_file == 0:
                if folders[i] not in self.dir_normal:
                    self.dir_normal.append(folders[i])

            if height_in_file>0 and normal_in_file == 0:
                if folders[i] not in self.dir_height:
                    self.dir_height.append(folders[i])
        print("Analýza složek dokončena")
        self.analyzing_done = 1
        return self.analyzing_done
#Voleni defaultni slozky (pripad vice slozek se stejnymi soubory)--------------------------------------------------------------------------------------------------------
    def picking_default_dirs(self):
        is_selected_normal_dir = 0
        is_selected_height_dir = 0
        global names

        while is_selected_normal_dir == 0:
            if len(self.dir_normal) > 1:
                print("Seznam složek s .normal soubory: ",self.dir_normal)
                print("Bylo nalezeno více složek se soubory .normal, zvolte defaultní (vepište číslo 0-{}): ".format(len(self.dir_normal)-1))
                #voani funkce pro spravnou zadanou hodnotu
                inp = input_check(0, len(self.dir_normal))
                select_normal_dir = inp.is_input_right()

                print("Pro .normal soubory byla zvolena složka: ", self.dir_normal[int(select_normal_dir)])
                #ruseni nezvolenych slozek (presun souborů ke trideni):
                folder_name[1] = self.dir_normal[int(select_normal_dir)]
                for i in range (0,len(self.dir_normal)):
                    if i != int(select_normal_dir):
                        for files in os.listdir(path + self.dir_normal[i]):
                            shutil.move(path + self.dir_normal[i] + "/" + files, path + files)                
                is_selected_normal_dir = 1
                    
            else:
                if len(self.dir_normal) != 0:
                    folder_name[1] = self.dir_normal[0]
                    print("Pro .normal soubory byla zvolena složka: ", self.dir_normal[0])
                    is_selected_normal_dir = 1
                else:
                    print("Nebyla nalezena žádná složka s .normal soubory, byla vytvořena automaticky: ",folder_name[1])
                    is_selected_normal_dir = 1


        while is_selected_height_dir == 0:
            if len(self.dir_height) > 1:
                print("Seznam složek s .height soubory: ",self.dir_height)
                print("Bylo nalezeno více složek se soubory .height, zvolte defaultní (vepište číslo 0-{}): ".format(len(self.dir_height)-1))
                inp = input_check(0, len(self.dir_height))
                select_height_dir = inp.is_input_right()
                
                print("Pro .height soubory byla zvolena složka: ", self.dir_height[int(select_height_dir)])
                #ruseni nezvolenych slozek (presun souborů ke trideni):
                folder_name[0] = self.dir_height[int(select_height_dir)]
                for i in range (0,len(self.dir_height)):
                    if i != int(select_height_dir):
                        for files in os.listdir(path + self.dir_height[i]):
                            shutil.move(path + self.dir_height[i] + "/" + files, path + files)
                is_selected_height_dir = 1

            else:
                if len(self.dir_height) != 0:
                    folder_name[0] = self.dir_height[0]
                    print("Pro .height soubory byla zvolena složka: ", self.dir_height[0])
                    is_selected_height_dir = 1
                else:
                    print("Nebyla nalezena žádná složka s .height soubory, byla vytvořena automaticky: ",folder_name[0])
                    is_selected_height_dir = 1
        #vytváření složek, pokud již nejsou vytvořeny:
        for x in range(0,2):
            if not os.path.exists(path + folder_name[x]):
                os.makedirs(path + folder_name[x])

        names = [path + "/" ,path + folder_name[0] + "/",path + folder_name[1] + "/"]
        self.picking_done = 1
        return self.picking_done

    def moving_files(self):
        global normal_count
        global height_count
        global nok_count

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

        print("Třídění dokončeno")
        print("Počet zkontrolovaných souborů: ", normal_count + height_count)
        print("Počet OK .normal souborů: ", normal_count)
        print("Počet OK .height souborů: ", height_count)
        print("Celkový počet NOK souborů: ",nok_count)
        #odstranění prázdných složek kromě základních (exception = 1)
        remove_empty_dirs(1)
        self.moving_done = 1
        return self.moving_done

class sort_by_camera:
    def __init__(self):
        self.moving_done = 0
        self.Cam_number = []

    def analyzing_cameras(self):       

        for i in range(0,len(names)):
            for files in os.listdir(names[i]):
                if ".Normal" in files: #hledam dvojici - staci jeden typ souboru
                    files_split = files.split('_')
                    cam_num_found = re.findall(r'\d+', files_split[4])#čísla, čtvrtá sekce podle _
                    for number in cam_num_found:
                        cam_num_found = int(number)
                    if not cam_num_found in self.Cam_number:  
                        self.Cam_number.append(cam_num_found)
                        # rovnani od nejmensiho cisla:
                        Cam_number2 = [0 for k in range(len(self.Cam_number))]
                        for q in range(0,len(self.Cam_number)):
                            Cam_number2[q] = min(self.Cam_number)
                            self.Cam_number.pop(self.Cam_number.index(Cam_number2[q]))
                        self.Cam_number = Cam_number2

        #zjistovani poctu jednotlivych dvojic -> neslo najednou s predeslou sekvenci protoze nebyl uplne sestaven Cam_number   
        # 30 nul v poli:
        cam_cnt = [0 for i in range(30)]
        for i in range(0,len(names)):
            for files in os.listdir(names[i]):
                if ".Normal" in files:
                    files_split = files.split('_')
                    cam_num_found = re.findall(r'\d+', files_split[4])#čísla, čtvrtá sekce podle _
                    for number in cam_num_found:
                        cam_num_found = int(number)

                    for j in range(0,len(self.Cam_number)): #musím to míz zde jelikož potřebuju Cam_num_found
                        if cam_num_found == self.Cam_number[j]:
                            cam_cnt[j] += 1

        #sort_by_camera.cam_cnt = cam_cnt
        cam_cnt = cam_cnt[0:len(self.Cam_number)]
        if int(len(self.Cam_number)) > 1 and int(len(self.Cam_number)) <5:
            print("Byly nalezeny",len(self.Cam_number) ,"kamery, číslo:     ",self.Cam_number)
        elif int(len(self.Cam_number)) > 4:
            print("Bylo nalezeno",len(self.Cam_number) ,"kamer, číslo:      ",self.Cam_number)
        elif int(len(self.Cam_number)) == 1:
            print("Byla nalezena jedna kamera číslo:       ",self.Cam_number)
        else:
            print("Chyba, Nebyly nalezeny žádné soubory")

        print("Počet dvojic souborů z dané kamery:", cam_cnt)  
        print("Analýza dokončena")

    # vytváření složek podle kamer:
    def creating_folders(self):
        self.normal_folders = []
        self.height_folders = []
        folder0_base = ""
        folder1_base = ""
           
        #pro Height
        if prefix_func in folder_name[0]:
            x = re.search(prefix_func,folder_name[0])
            delete_chars = x.span(0)[0]
            folder0_base = folder_name[0][0:delete_chars]
            
        else:
            folder0_base = folder_name[0]

        if prefix_Cam in folder0_base:
            x = re.search(prefix_Cam,folder0_base)
            delete_chars = x.span(0)[0]
            folder0_base = folder0_base[0:delete_chars]
                       
        #pro Normal
        if prefix_func in folder_name[1]:
            x = re.search(prefix_func,folder_name[1])
            delete_chars = x.span(0)[0]
            folder1_base = folder_name[1][0:delete_chars]
            
        else:
            folder1_base = folder_name[1]  

        if prefix_Cam in folder1_base:
            x = re.search(prefix_Cam,folder1_base)
            delete_chars = x.span(0)[0]
            folder1_base = folder1_base[0:delete_chars]     
        
        #vytvareni novych slozek
        for j in range(0,len(self.Cam_number)):
           
            new_folder_name1 = folder1_base + prefix_Cam + str(self.Cam_number[j])
            new_folder_name0 = folder0_base + prefix_Cam + str(self.Cam_number[j])

            if not os.path.exists(path + new_folder_name0):
                os.mkdir(path + new_folder_name0 + "/")
                print("Byla vytvořena nová složka:",new_folder_name0,",pro .height soubory z kamery číslo: ", self.Cam_number[j])
                if not new_folder_name0 in self.height_folders:
                    self.height_folders.append(new_folder_name0)
                if not new_folder_name0 in folders:
                    folders.append(new_folder_name0)
                
            else:
                new_folder_name0 = folder0_base + prefix_Cam + str(self.Cam_number[j])
                if not new_folder_name0 in self.height_folders:
                    self.height_folders.append(new_folder_name0)
                if not new_folder_name0 in folders:
                    folders.append(new_folder_name0)
        
            if not os.path.exists(path + new_folder_name1):
                os.mkdir(path + new_folder_name1 + "/")
                print("Byla vytvořena nová složka:",new_folder_name1,",pro .normal soubory z kamery číslo: ", self.Cam_number[j])
                if not new_folder_name1 in self.normal_folders:
                    self.normal_folders.append(new_folder_name1)
                if not new_folder_name1 in folders:
                    folders.append(new_folder_name1)
                
            else:
                new_folder_name1 = folder1_base + prefix_Cam + str(self.Cam_number[j])
                if not new_folder_name1 in self.normal_folders:
                    self.normal_folders.append(new_folder_name1)
                if not new_folder_name1 in folders:
                    folders.append(new_folder_name1)
            
        print("Vytváření nových složek dokončeno")    

    def moving_files(self):
        #presun vsech souboru na jedno misto
        for x in range(0,2):
            src = os.listdir(path + folder_name[x])
            for files in src:
                if ".bmp" in files:
                    shutil.move(path + folder_name[x] + "/" + files, path + files)


        for i in range(0,len(self.Cam_number)):
            for j in range(0,len(arr_normal)):
                folder = arr_normal[j]
                if "Cam" in arr_normal[j]:
                    x = re.search("Cam",folder)
                    delete_chars = x.span(0)[1]
                    Cam_number_normal_folder = folder[delete_chars:]#smaze to pred cislem kamery
                    Cam_number_normal_folder = Cam_number_normal_folder.replace("Img.Normal.bmp", "")
                    if len(str(self.Cam_number[i])) == len(str(Cam_number_normal_folder)):
                        if ("Cam" + str(self.Cam_number[i])) in arr_normal[j]:
                            if os.path.exists(path + arr_normal[j]):
                                #Cam number jsou serazeny stejne jako normal/height slozky proto i pro folders a pro cam
                                shutil.move(path + arr_normal[j], path + self.normal_folders[i] + "/" + arr_normal[j])

            for j in range(0,len(arr_height)):
                folder = arr_height[j]
                if "Cam" in arr_height[j]:
                    x = re.search("Cam",folder)
                    delete_chars = x.span(0)[1]
                    Cam_number_height_folder = folder[delete_chars:]#smaze to pred cislem kamery
                    Cam_number_height_folder = Cam_number_height_folder.replace("Img.Height.bmp", "")
                    if len(str(self.Cam_number[i])) == len(str(Cam_number_height_folder)):
                        if ("Cam" + str(self.Cam_number[i])) in arr_height[j]:
                            if os.path.exists(path + arr_height[j]):
                                shutil.move(path + arr_height[j], path + self.height_folders[i] + "/" + arr_height[j])
        print("Přesun souborů dokončen")
        self.moving_done = 1
        return self.moving_done

class sort_by_function:
    def __init__(self):
        self.moving_done = 0
        self.Func_number = []
        
    def analyzing_functions(self):       
        # pro normal, jelikoz v pripade funkce je u kaydeho typu jina
        for i in range(0,len(names)):
            for files in os.listdir(names[i]):
                if ".Normal" in files: #hledam dvojici - staci jeden typ souboru
                    files_split = files.split('_')
                    func_num_found = re.findall(r'\d+', files_split[3])#čísla, treti sekce podle _
                    for number in func_num_found:
                        func_num_found = int(number)
                    if not func_num_found in self.Func_number:  
                        self.Func_number.append(func_num_found)
                        # rovnani od nejmensiho cisla:
                        Func_number2 = [0 for k in range(len(self.Func_number))]
                        for q in range(0,len(self.Func_number)):
                            Func_number2[q] = min(self.Func_number)
                            self.Func_number.pop(self.Func_number.index(Func_number2[q]))
                        self.Func_number = Func_number2
        # pro height
                if ".Height" in files: #hledam dvojici - staci jeden typ souboru
                    files_split = files.split('_')
                    func_num_found = re.findall(r'\d+', files_split[3])#čísla, treti sekce podle _
                    for number in func_num_found:
                        func_num_found = int(number)
                    if not func_num_found in self.Func_number:  
                        self.Func_number.append(func_num_found)
                        # rovnani od nejmensiho cisla:
                        Func_number2 = [0 for k in range(len(self.Func_number))]
                        for q in range(0,len(self.Func_number)):
                            Func_number2[q] = min(self.Func_number)
                            self.Func_number.pop(self.Func_number.index(Func_number2[q]))
                        self.Func_number = Func_number2

        #zjistovani poctu jednotlivych dvojic -> neslo najednou s predeslou sekvenci protoze nebyl uplne sestaven Func_number   
        # 30 nul v poli:
        func_cnt = [0 for i in range(30)]
        for i in range(0,len(names)):
            for files in os.listdir(names[i]):
                if ".Normal" in files:
                    files_split = files.split('_')
                    func_num_found = re.findall(r'\d+', files_split[3])#čísla, treti sekce podle _
                    for number in func_num_found:
                        func_num_found = int(number)
                    for j in range(0,len(self.Func_number)): 
                        if func_num_found == self.Func_number[j]:
                            func_cnt[j] += 1

                if ".Height" in files:
                    files_split = files.split('_')
                    func_num_found = re.findall(r'\d+', files_split[3])#čísla, treti sekce podle _
                    for number in func_num_found:
                        func_num_found = int(number)
                    for j in range(0,len(self.Func_number)): 
                        if func_num_found == self.Func_number[j]:
                            func_cnt[j] += 1

        func_cnt = func_cnt[0:len(self.Func_number)]
        if int(len(self.Func_number)) > 1 and int(len(self.Func_number)) <5:
            print("Byly nalezeny",len(self.Func_number) ,"funkce, číslo:        ",self.Func_number)
        elif int(len(self.Func_number)) > 4:
            print("Bylo nalezeno",len(self.Func_number) ,"funkcí, číslo:        ",self.Func_number)
        elif int(len(self.Func_number)) == 1:
            print("Byla nalezena jedna funkce číslo:        ",self.Func_number)
        else:
            print("Chyba, Nebyly nalezeny žádné soubory")

        print("Počet dvojic souborů pro danou funkci:", func_cnt)  
        print("Analýza dokončena")

    # vytváření složek podle kamer:
    def creating_folders(self):
        self.normal_folders = []
        self.height_folders = []
        folder0_base = ""
        folder1_base = ""

        #pro Height
        if prefix_Cam in folder_name[0]:
            x = re.search(prefix_Cam,folder_name[0])
            delete_chars = x.span(0)[0]
            folder0_base = folder_name[0][0:delete_chars]   
        else:
            folder0_base = folder_name[0]
            
        if prefix_func in folder0_base:
            x = re.search(prefix_func,folder0_base)
            delete_chars = x.span(0)[0]
            folder0_base = folder0_base[0:delete_chars]
            
        #pro Normal
        if prefix_Cam in folder_name[1]:
            x = re.search(prefix_Cam,folder_name[1])
            delete_chars = x.span(0)[0]
            folder1_base = folder_name[1][0:delete_chars]
        else:
            folder1_base = folder_name[1]   

        if prefix_func in folder1_base:
            x = re.search(prefix_func,folder1_base)
            delete_chars = x.span(0)[0]
            folder1_base = folder1_base[0:delete_chars]
  
        #vytvareni novych slozek
        for j in range(0,len(self.Func_number)):
           
            new_folder_name1 = folder1_base + prefix_func + str(self.Func_number[j])
            new_folder_name0 = folder0_base + prefix_func + str(self.Func_number[j])

            if not os.path.exists(path + new_folder_name0):
                os.mkdir(path + new_folder_name0 + "/")
                print("Byla vytvořena nová složka:",new_folder_name0,",pro .height soubory s funkcí číslo: ", self.Func_number[j])
                if not new_folder_name0 in self.height_folders:
                    self.height_folders.append(new_folder_name0)
                if not new_folder_name0 in folders:
                    folders.append(new_folder_name0)
            else:
                new_folder_name0 = folder0_base + prefix_func + str(self.Func_number[j])
                if not new_folder_name0 in self.height_folders:
                    self.height_folders.append(new_folder_name0)
                if not new_folder_name0 in folders:
                    folders.append(new_folder_name0)
        
            if not os.path.exists(path + new_folder_name1):
                os.mkdir(path + new_folder_name1 + "/")
                print("Byla vytvořena nová složka:",new_folder_name1,",pro .normal soubory s funkcí číslo: ", self.Func_number[j])
                if not new_folder_name1 in self.normal_folders:
                    self.normal_folders.append(new_folder_name1)
                if not new_folder_name1 in folders:
                    folders.append(new_folder_name1)
                
            else:
                new_folder_name1 = folder1_base + prefix_func + str(self.Func_number[j])
                if not new_folder_name1 in self.normal_folders:
                    self.normal_folders.append(new_folder_name1)
                if not new_folder_name1 in folders:
                    folders.append(new_folder_name1)
            
        print("Vytváření nových složek dokončeno")    

    def moving_files(self):
        #presun vsech souboru na jedno misto
        for x in range(0,2):
            src = os.listdir(path + folder_name[x])
            for files in src:
                if ".bmp" in files:
                    shutil.move(path + folder_name[x] + "/" + files, path + files)


        for i in range(0,len(self.Func_number)):
            for j in range(0,len(arr_normal)):
                folder = arr_normal[j]
                files_split = folder.split('_')
                func_num_found = re.findall(r'\d+', files_split[3])#čísla, treti sekce podle _
                for number in func_num_found:
                    func_num_found = int(number)

                Func_number_normal_folder = func_num_found
                if len(str(self.Func_number[i])) == len(str(Func_number_normal_folder)):
                    if ("_" + str(self.Func_number[i]) + "_") in arr_normal[j]:
                        if os.path.exists(path + arr_normal[j]):
                            #Func number jsou serazeny stejne jako normal/height slozky proto i pro folders a pro cam
                            shutil.move(path + arr_normal[j], path + self.normal_folders[i] + "/" + arr_normal[j])

            for j in range(0,len(arr_height)):
                folder = arr_height[j]
                files_split = folder.split('_')
                func_num_found = re.findall(r'\d+', files_split[3])#čísla, treti sekce podle _
                for number in func_num_found:
                    func_num_found = int(number)

                Func_number_height_folder = func_num_found
                if len(str(self.Func_number[i])) == len(str(Func_number_height_folder)):
                    if ("_" + str(self.Func_number[i]) + "_") in arr_height[j]:
                        if os.path.exists(path + arr_height[j]):
                            shutil.move(path + arr_height[j], path + self.height_folders[i] + "/" + arr_height[j])

        print("Přesun souborů dokončen")
        self.moving_done = 1
        return self.moving_done

class sort_by_both:
    def __init__(self):
        self.moving_done = 0
        self.Func_number = []
        self.Cam_number = []
        
    def analyzing_functions(self):       
        # pro normal, jelikoz v pripade funkce je u kaydeho typu jina
        for i in range(0,len(names)):
            for files in os.listdir(names[i]):
                if ".Normal" in files: #hledam dvojici - staci jeden typ souboru
                    files_split = files.split('_')
                    func_num_found = re.findall(r'\d+', files_split[3])#čísla, treti sekce podle _
                    for number in func_num_found:
                        func_num_found = int(number)
                    if not func_num_found in self.Func_number:  
                        self.Func_number.append(func_num_found)
                        # rovnani od nejmensiho cisla:
                        Func_number2 = [0 for k in range(len(self.Func_number))]
                        for q in range(0,len(self.Func_number)):
                            Func_number2[q] = min(self.Func_number)
                            self.Func_number.pop(self.Func_number.index(Func_number2[q]))
                        self.Func_number = Func_number2
        # pro height
                if ".Height" in files: #hledam dvojici - staci jeden typ souboru
                    files_split = files.split('_')
                    func_num_found = re.findall(r'\d+', files_split[3])#čísla, treti sekce podle _
                    for number in func_num_found:
                        func_num_found = int(number)
                    if not func_num_found in self.Func_number:  
                        self.Func_number.append(func_num_found)
                        # rovnani od nejmensiho cisla:
                        Func_number2 = [0 for k in range(len(self.Func_number))]
                        for q in range(0,len(self.Func_number)):
                            Func_number2[q] = min(self.Func_number)
                            self.Func_number.pop(self.Func_number.index(Func_number2[q]))
                        self.Func_number = Func_number2

        #zjistovani poctu jednotlivych dvojic -> neslo najednou s predeslou sekvenci protoze nebyl uplne sestaven Func_number   
        # 30 nul v poli:
        func_cnt = [0 for i in range(30)]
        for i in range(0,len(names)):
            for files in os.listdir(names[i]):
                if ".Normal" in files:
                    files_split = files.split('_')
                    func_num_found = re.findall(r'\d+', files_split[3])#čísla, treti sekce podle _
                    for number in func_num_found:
                        func_num_found = int(number)
                    for j in range(0,len(self.Func_number)): 
                        if func_num_found == self.Func_number[j]:
                            func_cnt[j] += 1

                if ".Height" in files:
                    files_split = files.split('_')
                    func_num_found = re.findall(r'\d+', files_split[3])#čísla, treti sekce podle _
                    for number in func_num_found:
                        func_num_found = int(number)
                    for j in range(0,len(self.Func_number)): 
                        if func_num_found == self.Func_number[j]:
                            func_cnt[j] += 1

        func_cnt = func_cnt[0:len(self.Func_number)]
        if int(len(self.Func_number)) > 1 and int(len(self.Func_number)) <5:
            print("Byly nalezeny",len(self.Func_number) ,"funkce, číslo:        ",self.Func_number)
        elif int(len(self.Func_number)) > 4:
            print("Bylo nalezeno",len(self.Func_number) ,"funkcí, číslo:        ",self.Func_number)
        elif int(len(self.Func_number)) == 1:
            print("Byla nalezena jedna funkce číslo:        ",self.Func_number)
        else:
            print("Chyba, Nebyly nalezeny žádné soubory")

        print("Počet dvojic souborů pro danou funkci:", func_cnt)  
    
    def analyzing_cameras(self):       

        for i in range(0,len(names)):
            for files in os.listdir(names[i]):
                if ".Normal" in files: #hledam dvojici - staci jeden typ souboru
                    files_split = files.split('_')
                    cam_num_found = re.findall(r'\d+', files_split[4])#čísla, čtvrtá sekce podle _
                    for number in cam_num_found:
                        cam_num_found = int(number)
                    if not cam_num_found in self.Cam_number:  
                        self.Cam_number.append(cam_num_found)
                        # rovnani od nejmensiho cisla:
                        Cam_number2 = [0 for k in range(len(self.Cam_number))]
                        for q in range(0,len(self.Cam_number)):
                            Cam_number2[q] = min(self.Cam_number)
                            self.Cam_number.pop(self.Cam_number.index(Cam_number2[q]))
                        self.Cam_number = Cam_number2

        #zjistovani poctu jednotlivych dvojic -> neslo najednou s predeslou sekvenci protoze nebyl uplne sestaven Cam_number   
        # 30 nul v poli:
        cam_cnt = [0 for i in range(30)]
        for i in range(0,len(names)):
            for files in os.listdir(names[i]):
                if ".Normal" in files:
                    files_split = files.split('_')
                    cam_num_found = re.findall(r'\d+', files_split[4])#čísla, čtvrtá sekce podle _
                    for number in cam_num_found:
                        cam_num_found = int(number)

                    for j in range(0,len(self.Cam_number)): #musím to míz zde jelikož potřebuju Cam_num_found
                        if cam_num_found == self.Cam_number[j]:
                            cam_cnt[j] += 1

        #sort_by_camera.cam_cnt = cam_cnt
        cam_cnt = cam_cnt[0:len(self.Cam_number)]
        if int(len(self.Cam_number)) > 1 and int(len(self.Cam_number)) <5:
            print("Byly nalezeny",len(self.Cam_number) ,"kamery, číslo:     ",self.Cam_number)
        elif int(len(self.Cam_number)) > 4:
            print("Bylo nalezeno",len(self.Cam_number) ,"kamer, číslo:      ",self.Cam_number)
        elif int(len(self.Cam_number)) == 1:
            print("Byla nalezena jedna kamera číslo:       ",self.Cam_number)
        else:
            print("Chyba, Nebyly nalezeny žádné soubory")

        print("Počet dvojic souborů z dané kamery:", cam_cnt)  
        print("Analýza dokončena")
    # vytváření složek podle kamer:
    def creating_folders(self):
        self.normal_folders = []
        self.height_folders = []
        self.folder0_base = ""
        self.folder1_base = ""

        #pro Height
        if prefix_Cam in folder_name[0]:
            x = re.search(prefix_Cam,folder_name[0])
            delete_chars = x.span(0)[0]
            self.folder0_base = folder_name[0][0:delete_chars]   
        else:
            self.folder0_base = folder_name[0]
            
        if prefix_func in self.folder0_base:
            x = re.search(prefix_func,self.folder0_base)
            delete_chars = x.span(0)[0]
            self.folder0_base = self.folder0_base[0:delete_chars]

        #pro Normal
        if prefix_Cam in folder_name[1]:
            x = re.search(prefix_Cam,folder_name[1])
            delete_chars = x.span(0)[0]
            self.folder1_base = folder_name[1][0:delete_chars]
        else:
            self.folder1_base = folder_name[1]   

        if prefix_func in self.folder1_base:
            x = re.search(prefix_func,self.folder1_base)
            delete_chars = x.span(0)[0]
            self.folder1_base = self.folder1_base[0:delete_chars]
            
        
        #vytvareni novych slozek
        for j in range(0,len(self.Func_number)):
            for i in range(0,len(self.Cam_number)):
                new_folder_name1 = self.folder1_base + prefix_Cam + str(self.Cam_number[i])+ prefix_func + str(self.Func_number[j])
                new_folder_name0 = self.folder0_base + prefix_Cam + str(self.Cam_number[i])+ prefix_func + str(self.Func_number[j])

                if not os.path.exists(path + new_folder_name0):
                    os.mkdir(path + new_folder_name0 + "/")
                    print("Byla vytvořena nová složka:",new_folder_name0,",pro .height soubory s funkcí číslo: ", self.Func_number[j],"pro kameru: ",self.Cam_number[i])
                    if not new_folder_name0 in self.height_folders:
                        self.height_folders.append(new_folder_name0)
                    if not new_folder_name0 in folders:
                        folders.append(new_folder_name0)
                else:
                    new_folder_name0 = self.folder0_base + prefix_func + str(self.Func_number[j])
                    if not new_folder_name0 in self.height_folders:
                        self.height_folders.append(new_folder_name0)
                    if not new_folder_name0 in folders:
                        folders.append(new_folder_name0)
            
                if not os.path.exists(path + new_folder_name1):
                    os.mkdir(path + new_folder_name1 + "/")
                    print("Byla vytvořena nová složka:",new_folder_name1,",pro .normal soubory s funkcí číslo: ", self.Func_number[j],"pro kameru: ",self.Cam_number[i])
                    if not new_folder_name1 in self.normal_folders:
                        self.normal_folders.append(new_folder_name1)
                    if not new_folder_name1 in folders:
                        folders.append(new_folder_name1)
                    
                else:
                    new_folder_name1 = self.folder1_base + prefix_func + str(self.Func_number[j])
                    if not new_folder_name1 in self.normal_folders:
                        self.normal_folders.append(new_folder_name1)
                    if not new_folder_name1 in folders:
                        folders.append(new_folder_name1)
            
        print("Vytváření nových složek dokončeno")    

    def moving_files(self):
        #presun vsech souboru na jedno misto
        for x in range(0,2):
            src = os.listdir(path + folder_name[x])
            for files in src:
                if ".bmp" in files:
                    shutil.move(path + folder_name[x] + "/" + files, path + files)

        for i in range(0,len(self.Func_number)):
            for q in range(0,len(self.Cam_number)):
                #pro normal
                for j in range(0,len(arr_normal)):
                    folder = arr_normal[j]
                    files_split = folder.split('_')
                    func_num_found = re.findall(r'\d+', files_split[3])#čísla, treti sekce podle _
                    for number in func_num_found:
                        func_num_found = int(number)
                    cam_num_found = re.findall(r'\d+', files_split[4])
                    for number in cam_num_found:
                        cam_num_found = int(number)
            
                    if len(str(self.Func_number[i])) == len(str(func_num_found)):
                        if ("_" + str(self.Func_number[i]) + "_") in arr_normal[j]:
                            if len(str(self.Cam_number[q])) == len(str(cam_num_found)):
                                if ("Cam" + str(self.Cam_number[q])) in arr_normal[j]:
                                    if os.path.exists(path + arr_normal[j]):
                                        dest_dir_normal =  self.folder1_base + prefix_Cam + str(self.Cam_number[q])+ prefix_func + str(self.Func_number[i])
                                        shutil.move(path + arr_normal[j], path + dest_dir_normal + "/" + arr_normal[j])
                #pro height:
                for j in range(0,len(arr_height)):
                    folder = arr_height[j]
                    files_split = folder.split('_')
                    func_num_found = re.findall(r'\d+', files_split[3])#čísla, treti sekce podle _
                    for number in func_num_found:
                        func_num_found = int(number)
                    cam_num_found = re.findall(r'\d+', files_split[4])
                    for number in cam_num_found:
                        cam_num_found = int(number)
            
                    if len(str(self.Func_number[i])) == len(str(func_num_found)):
                        if ("_" + str(self.Func_number[i]) + "_") in arr_height[j]:
                            if len(str(self.Cam_number[q])) == len(str(cam_num_found)):
                                if ("Cam" + str(self.Cam_number[q])) in arr_height[j]:
                                    if os.path.exists(path + arr_height[j]):
                                        dest_dir_height =  self.folder0_base + prefix_Cam + str(self.Cam_number[q])+ prefix_func + str(self.Func_number[i])
                                        shutil.move(path + arr_height[j], path + dest_dir_height + "/" + arr_height[j])


        print("Přesun souborů dokončen")
        self.moving_done = 1
        return self.moving_done
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

arr_normal_cut = []      # oriznute nazvy souboru v poli
arr_height_cut = []      # oriznute nazvy souboru v poli
arr_normal = []          # original nazvy souboru v poli
arr_height = []          # original nazvy souboru v poli
normal_count = 0         # pro predstavu o velikosti pole
height_count = 0         # pro predstavu o velikosti pole
nok_count = 0            # pocet osamostatnenych souboru
n = 0
example_folder_name = "221013_092241_0000000842_21_&Cam1Img.Height.bmp"
hide_cnt = 23   # defaultní počet zakrytých znaků při porovnávání normal a height souborů
hide_cnt_from_start = len(example_folder_name) - int(hide_cnt)

b = basic_sorting()
b.analyzing_directories()
b.picking_default_dirs()

for i in range (0,len(names)):
    for files in os.listdir(names[i]):
        # ošetření proti delším/ kratším souborům např.: trojciferná funkce nebo dvojciferná kamera
        
        if ".Normal" in files:
            arr_normal.append(files)
            if len(files) > len(example_folder_name) or len(files) < len(example_folder_name):
                n = len(files) - len(example_folder_name) # (=43)
            arr_normal_cut.append(files[0:(hide_cnt_from_start + n)])
            normal_count+=1
        n = 0

        if ".Height" in files:
            arr_height.append(files)
            if len(files) > len(example_folder_name) or len(files) < len(example_folder_name):
                n = len(files) - len(example_folder_name) # (=43)
            arr_height_cut.append(files[0:(hide_cnt_from_start + n)])
            height_count+=1
        n = 0

if normal_count == 0 and height_count == 0:
    print("V zadané cestě nebyly nalezeny žádné soubory")
else:
    print("Prověřuje se",normal_count+height_count,"souborů...")
    print("Počet .normal souborů: ", normal_count)
    print("Počet .height souborů: ", height_count)


b.moving_files()

#uvedeni do advanced modu:
#jakýkoliv jiný znak je brán jako ne:
advanced_mode = input("Advanced mode?: (Y/n)")
if advanced_mode.casefold() == "y":
    print("Třídit podle čísla funkce? (1) ,podle čísla kamery? (2) nebo podle funkce i kamery? (3):")
    #ověření správného vstupu:
    inp = input_check(1, 4)
    sort_by = inp.is_input_right()


    if int(sort_by) == 1:
        f=sort_by_function()
        f.analyzing_functions()
        f.creating_folders()
        m = f.moving_files()
        if m == 1:
            remove_empty_dirs(0)

    if int(sort_by) == 2:  
        s=sort_by_camera()
        s.analyzing_cameras()
        s.creating_folders()
        mm = s.moving_files()
        if mm == 1:
            remove_empty_dirs(0)
    
    if int(sort_by) == 3:
        bo=sort_by_both()
        bo.analyzing_cameras()
        bo.analyzing_functions()
        bo.creating_folders()
        mmm = bo.moving_files()
        if mmm == 1:
            remove_empty_dirs(0)

k=input("Press close to exit")