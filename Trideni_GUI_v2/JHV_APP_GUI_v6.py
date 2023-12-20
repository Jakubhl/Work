import customtkinter
import os
import time
from PIL import Image, ImageTk
import Sorting_option_v5 as Trideni
import Deleting_option_v1 as Deleting
import Converting_option_v1 as Converting
from tkinter import filedialog
import tkinter as tk
import threading
import shutil

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root=customtkinter.CTk()
root.geometry("1200x900")
root.wm_iconbitmap('images/JHV.ico')
#root.title("Zpracování souborů z průmyslových kamer")
root.title("TRIMAZKON v_3.0")
#logo_set = False

def split_text_to_rows(long_string:str,max_chars_on_row:int):
    letter_number = 0
    separated_strings = []
    row_str = ""
    for letters in long_string:
        row_str+=letters
        if letter_number >= max_chars_on_row:
            separated_strings.append(row_str)
            row_str = ""
            letter_number = -1
        letter_number+=1
    # a pridat zbytek:
    separated_strings.append(row_str)
    long_string = ""
    for items in separated_strings:
        long_string += (items + "\n")
    
    return long_string

def path_check(path_raw):
    path=path_raw
    backslash = "\ "
    if backslash[0] in path:
        newPath = path.replace(os.sep, '/')
        path = newPath

    if path.endswith('/') == False:
        newPath = path + "/"
        path = newPath

    if not os.path.exists(path):
        return False

    else:
        return path

def read_text_file_data(): # Funkce vraci data z textoveho souboru Recources.txt
    """
    Funkce vraci data z textoveho souboru Recources.txt

    data jsou v poradi:

    0 supported_formats_sorting\n
    1 supported_formats_deleting\n
    2 path_repaired\n
    3 files_to_keep\n
    4 cutoff_date\n
    5 prefix_function\n
    6 prefix_camera\n
    7 maximalized\n
    8 max_pallets\n
    9 static_dirs_names\n
    """

    if os.path.exists('Recources.txt'):
        cutoff_date = ["","",""]
        with open('Recources.txt','r',encoding='utf-8',errors='replace') as recources_file:
            Lines = recources_file.readlines()
        supported_formats_sorting = []
        supported_formats_deleting = []
        unwanted_chars = ["\n","\"","[","]"]
        for chars in unwanted_chars:
            if chars in Lines[2]:
                Lines[2] = Lines[2].replace(chars,"")
            if chars in Lines[4]:
                Lines[4] = Lines[4].replace(chars,"")
            
        found_formats = Lines[2].split(",") 
        for items in found_formats:
            supported_formats_sorting.append(str(items))
        found_formats = Lines[4].split(",")
        for items in found_formats:
            supported_formats_deleting.append(str(items))
        
        inserted_path = Lines[6].replace("\n","")
        inserted_path = str(inserted_path)

        path_repaired = path_check(inserted_path)

        Lines[8] = Lines[8].replace("\n","")
        files_to_keep = int(Lines[8])
        
        Lines[10] = Lines[10].replace("\n","")
        cutoffdate_splitted = Lines[10].split(".")
        i=0
        for items in cutoffdate_splitted:
            i+=1
            cutoff_date[i-1] = items

        Lines[12] = Lines[12].replace("\n","")
        Lines[12] = Lines[12].replace("\"","")
        Lines[12] = Lines[12].replace("/","")
        if str(Lines[12]) != "":
            prefix_function = Lines[12]
        else:
            prefix_function = "Func_"

        Lines[14] = Lines[14].replace("\n","")
        Lines[14] = Lines[14].replace("\"","")
        Lines[14] = Lines[14].replace("/","")
        if str(Lines[14]) != "":
            prefix_camera = Lines[14]
        else:
            prefix_camera = "Cam_"

        #spoustet v maximalizovanem okne?
        Lines[16] = Lines[16].replace("\n","")
        if str(Lines[16]) != "":
            maximalized = Lines[16]
        else:
            maximalized = "ne"
        #maximalni pocet palet v obehu
        Lines[18] = Lines[18].replace("\n","")
        if str(Lines[18]) != "":
            max_pallets = int(Lines[18])
        else:
            max_pallets = 55

        # cteme nekolik nazvu slozek:
        static_dirs_names = []
        for i in range(20,32,2):
            Lines[i] = Lines[i].replace("\n","")
            Lines[i] = Lines[i].replace("\"","")
            Lines[i] = Lines[i].replace("/","")
            static_dirs_names.append(Lines[i])
            

        return [supported_formats_sorting,supported_formats_deleting,path_repaired,files_to_keep,cutoff_date,
                prefix_function,prefix_camera,maximalized,max_pallets,static_dirs_names]
    else:
        print("Chybí konfigurační soubor Recources.txt")
        return [False]*10

def write_text_file_data(input_data,which_parameter): # Funkce zapisuje data do textoveho souboru Recources.txt
    """
    Funkce zapisuje data do textoveho souboru Recources.txt

    vraci vystupni zpravu: report

    which_parameter je bud: 
    
    1 add_supported_sorting_formats\n
    2 add_supported_deleting_formats\n
    3 pop_supported_sorting_formats\n
    4 pop_supported_deleting_formats\n
    5 default_path\n
    6 default_files_to_keep\n
    7 default_cutoff_date\n
    8 new_default_prefix_func\n
    9 new_default_prefix_cam\n
    10 maximalized\n
    11 pallets_set\n
    """
    unwanted_chars = ["\"","\n"," ","."]
    if os.path.exists('Recources.txt'):
        report = ""
        with open('Recources.txt', 'r',encoding='utf-8',errors='replace') as recources:
            lines = recources.readlines()

        supported_formats_sorting = []
        supported_formats_deleting = []
        found_formats = lines[2].split(",")
        for items in found_formats:
            items = items.replace("\n","")
            supported_formats_sorting.append(str(items))
        found_formats = lines[4].split(",")
        for items in found_formats:
            items = items.replace("\n","")
            supported_formats_deleting.append(str(items))

        if which_parameter == "add_supported_sorting_formats":
            corrected_input = str(input_data)
            for items in unwanted_chars:
                corrected_input = corrected_input.replace(items,"")
            if str(corrected_input) not in supported_formats_sorting:
                supported_formats_sorting.append(str(corrected_input))
                report = (f"Byl přidán formát: \"{corrected_input}\" do podporovaných formátů pro možnosti třídění")
            else:
                report =  (f"Formát: \"{corrected_input}\" je již součástí podporovaných formátů možností třídění")
        
        elif which_parameter == "add_supported_deleting_formats":
            corrected_input = str(input_data)
            for items in unwanted_chars:
                corrected_input = corrected_input.replace(items,"")
            if str(corrected_input) not in supported_formats_deleting:
                supported_formats_deleting.append(str(corrected_input))
                report =  (f"Byl přidán formát: \"{corrected_input}\" do podporovaných formátů pro možnosti mazání")
            else:
                report =  (f"Formát: \"{corrected_input}\" je již součástí podporovaných formátů možností mazání")
            
        elif which_parameter == "pop_supported_sorting_formats":
            poped = 0
            found = False
            range_to = len(supported_formats_sorting)
            for i in range(0,range_to):
                if i < range_to:
                    if str(input_data) == supported_formats_sorting[i] and len(str(input_data)) == len(supported_formats_sorting[i]):
                        supported_formats_sorting.pop(i)
                        poped+=1
                        range_to = range_to - poped
                        report =  (f"Z podporovaných formátů možností třídění byl odstraněn formát: \"{input_data}\"")
                        found = True
            if found == False:
                report =  (f"Formát: \"{input_data}\" nebyl nalezen v podporovaných formátech možností třídění, nemůže tedy být odstraněn")
            
        elif which_parameter == "pop_supported_deleting_formats":
            poped = 0
            found = False
            range_to = len(supported_formats_deleting)
            for i in range(0,range_to):
                if i < range_to:
                    if str(input_data) == supported_formats_deleting[i] and len(str(input_data)) == len(supported_formats_deleting[i]):
                        supported_formats_deleting.pop(i)
                        poped+=1
                        range_to = range_to - poped
                        report =  (f"Z podporovaných formátů možností mazání byl odstraněn formát: \".{input_data}\"")
                        found = True
            if found == False:
                report =  (f"Formát: \"{input_data}\" nebyl nalezen v podporovaných formátech možností mazání, nemůže tedy být odstraněn")
        
        elif which_parameter == "default_path":
            lines[6] = lines[6].replace("\n","")
            lines[6] = str(input_data)+"\n"
            report = (f"Základní cesta přenastavena na: {str(input_data)}")
        
        elif which_parameter == "default_files_to_keep":
            lines[8] = lines[8].replace("\n","")
            lines[8] = str(input_data)+"\n"
        
        elif which_parameter == "default_cutoff_date":
            lines[10] = lines[10].replace("\n","")
            lines[10] = str(input_data[0])+"."+str(input_data[1])+"."+str(input_data[2])+"\n"

        elif which_parameter == "new_default_prefix_func":
            lines[12] = lines[12].replace("\n","")
            lines[12] = lines[12].replace("\"","")
            lines[12] = lines[12].replace("\\","")
            lines[12] = lines[12].replace("/","")
            lines[12] = str(input_data).replace(" ","")+"\n"
            report = (f"Základní prefix názvu složek pro třídění podle funkce přenastaven na: {str(input_data)}")

        elif which_parameter == "new_default_prefix_cam":
            lines[14] = lines[14].replace("\n","")
            lines[14] = lines[14].replace("\"","")
            lines[14] = lines[14].replace("\\","")
            lines[14] = lines[14].replace("/","")
            lines[14] = str(input_data).replace(" ","")+"\n"
            report = (f"Základní prefix názvu složek pro třídění podle kamery přenastaven na: {str(input_data)}")

        elif which_parameter == "maximalized":
            lines[16] = str(input_data) + "\n"

        elif which_parameter == "pallets_set":
            lines[18] = str(input_data) + "\n"

        elif which_parameter == "new_default_static_dir_name":
            input_data_splitted = str(input_data).split(" | ")
            input_data = input_data_splitted[0]
            increment = int(input_data_splitted[1])
            lines_with_names = [20,22,24,26,28,30]
            increment = lines_with_names[increment]
            
            lines[increment] = lines[increment].replace("\n","")
            lines[increment] = lines[increment].replace("\"","")
            lines[increment] = lines[increment].replace("\\","")
            lines[increment] = lines[increment].replace("/","")
            lines[increment] = str(input_data).replace(" ","")+"\n"
            
        #navraceni poli zpet do stringu radku:
        lines[2] = ""
        lines[4] = ""
        for items in supported_formats_sorting:
            if lines[2] == "":
                lines[2] = lines[2] + str(items)
            else:
                lines[2] = lines[2] + "," + str(items)
        for items in supported_formats_deleting:
            if lines[4] == "":
                lines[4] = lines[4] + str(items)
            else:
                lines[4] = lines[4] + "," + str(items)
        lines[2] = lines[2]+"\n"
        lines[4] = lines[4]+"\n"

        # Write the modified lines back to the file
        with open('Recources.txt', 'w',encoding='utf-8',errors='replace') as recources2:
            recources2.writelines(lines)

        return report
    else:
        print("Chybí konfigurační soubor Recources.txt")
        return "Chybí konfigurační soubor Recources.txt"

#definice EXPLORERU
def browseDirectories(visible_files): # Funkce spouští průzkumníka systému windows pro definování cesty, kde má program pracovat
    """
    Funkce spouští průzkumníka systému windows pro definování cesty, kde má program pracovat

    Vstupní data:

    0: visible_files = "all" / "only_dirs"

    Výstupní data:

    0: výstupní chybová hlášení
    1: opravená cesta
    """
    corrected_path = ""
    output= ""
    text_file_data = read_text_file_data()
    start_path = str(text_file_data[2]) #defaultni cesta
    if start_path != False:
        if not os.path.exists(start_path):
            start_path = ""
            output="Konfigurační soubor obsahuje neplatnou cestu"

    else:
        output="Chybí konfigurační soubor Recources.txt s počáteční cestou...\n"
        start_path=""

    # pripad vyberu files, aby byly viditelne
    if visible_files == "all":
        if(start_path != ""):
            foldername_path = filedialog.askopenfile(initialdir = start_path,title = "Klikněte na soubor v požadované cestě")
            path_to_directory= ""
            if foldername_path != None:
                path_to_file = str(foldername_path.name)
                path_to_file_split = path_to_file.split("/")
                i=0
                for parts in path_to_file_split:
                    i+=1
                    if i<len(path_to_file_split):
                        if i == 1:
                            path_to_directory = path_to_directory + parts
                        else:
                            path_to_directory = path_to_directory +"/"+ parts
            else:
                output = "Přes explorer nebyla vložena žádná cesta"
        else:           
            foldername_path = filedialog.askopenfile(initialdir = "/",title = "Klikněte na soubor v požadované cestě")
            path_to_directory= ""
            if foldername_path != None:
                path_to_file = str(foldername_path.name)
                path_to_file_split = path_to_file.split("/")
                i=0
                for parts in path_to_file_split:
                    i+=1
                    if i<len(path_to_file_split):
                        if i == 1:
                            path_to_directory = path_to_directory + parts
                        else:
                            path_to_directory = path_to_directory +"/"+ parts
            else:
                output = "Přes explorer nebyla vložena žádná cesta"

    # pripad vyberu slozek
    if visible_files == "only_dirs":
        if(start_path != ""):
            path_to_directory = filedialog.askdirectory(initialdir = start_path, title = "Vyberte adresář")
            if path_to_directory == None:
                output = "Přes explorer nebyla vložena žádná cesta"
        else:
            path_to_directory = filedialog.askdirectory(initialdir = "/", title = "Vyberte adresář")
            if path_to_directory == None:
                output = "Přes explorer nebyla vložena žádná cesta"

    check = path_check(path_to_directory)
    corrected_path = check
    
    return [output,corrected_path]

def menu(): # Funkce spouští základní menu při spuštění aplikace (MAIN)
    """
    Funkce spouští základní menu při spuštění aplikace (MAIN)

    -obsahuje 2 rámce:

    list_of_menu_frames = [frame_with_buttons,frame_with_logo]
    """

    data_read_in_txt = read_text_file_data()
    if data_read_in_txt[7] == "ano":
        #root.attributes('-fullscreen', True) #fullscreen bez windows tltacitek
        root.after(0, lambda:root.state('zoomed')) # max zoom, porad v okne

    frame_with_logo = customtkinter.CTkFrame(master=root)
    #logo = customtkinter.CTkImage(Image.open("images/logo2.bmp"),size=(571, 70))
    logo = customtkinter.CTkImage(Image.open("images/logo.png"),size=(1200, 100))
    image_logo = customtkinter.CTkLabel(master = frame_with_logo,text = "",image =logo)
    frame_with_buttons = customtkinter.CTkFrame(master=root)
    frame_with_logo.pack(pady=0,padx=5,fill="both",expand=False,side = "top")
    image_logo.pack()
    frame_with_buttons.pack(pady=5,padx=5,fill="both",expand=True,side = "top")

    list_of_menu_frames = [frame_with_buttons,frame_with_logo]
    
    def call_sorting_option(list_of_menu_frames):
        root.unbind("<f>")
        Sorting_option(root,list_of_menu_frames)
    def call_deleting_option(list_of_menu_frames):
        root.unbind("<f>")
        Deleting_option(root,list_of_menu_frames)
    def call_convert_option(list_of_menu_frames):
        root.unbind("<f>")
        Converting_option(root,list_of_menu_frames)
    def call_view_option(list_of_menu_frames):
        root.unbind("<f>")
        Image_browser(root,list_of_menu_frames)
    def call_advanced_option(list_of_menu_frames):
        root.unbind("<f>")
        Advanced_option(root,list_of_menu_frames)
    
    sorting_button  = customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Možnosti třídění souborů", command = lambda: call_sorting_option(list_of_menu_frames),font=("Arial",25,"bold"))
    deleting_button = customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Možnosti mazání souborů", command = lambda: call_deleting_option(list_of_menu_frames),font=("Arial",25,"bold"))
    convert_button  = customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Možnosti konvertování souborů", command = lambda: call_convert_option(list_of_menu_frames),font=("Arial",25,"bold"))
    viewer_button   = customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Procházet obrázky", command = lambda: call_view_option(list_of_menu_frames),font=("Arial",25,"bold"))
    advanced_button = customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Pokročilé možnosti", command = lambda: call_advanced_option(list_of_menu_frames),font=("Arial",25,"bold"))

    sorting_button.pack(pady =(50,10),padx=0,side="top",anchor="n")
    deleting_button.pack(pady =0,padx=0,side="top",anchor="n")
    convert_button.pack(pady =10,padx=0,side="top",anchor="n")
    viewer_button.pack(pady =0,padx=0,side="top",anchor="n")
    advanced_button.pack(pady =10,padx=0,side="top",anchor="n")

    def maximalize_window(e):
        # netrigguj fullscreen zatimco pisu do vstupniho textovyho pole
        currently_focused = str(root.focus_get())
        if ".!ctkentry" in currently_focused:
            return
        if int(root._current_width) > 1200:
            root.after(0, lambda:root.state('normal'))
            root.geometry("1200x900")
        else:
            root.after(0, lambda:root.state('zoomed'))
    root.bind("<f>",maximalize_window)
    root.mainloop()

class Image_browser: # Umožňuje procházet obrázky a přitom například vybrané přesouvat do jiné složky
    """
    Umožňuje procházet obrázky a přitom například vybrané přesouvat do jiné složky

    - umožňuje: měnit rychlost přehrávání, přiblížení, otočení obrázku
    - reaguje na klávesové zkratky
    """
    def __init__(self,root,list_of_menu_frames):
        self.root = root
        self.list_of_menu_frames = list_of_menu_frames
        self.all_images = []
        self.increment_of_image = 0
        self.state = "stop"
        self.previous_scrollbar_x = 0
        self.previous_scrollbar_y = 0
        self.rotation_angle = 0.0
        text_file_data = read_text_file_data()
        list_of_dir_names = text_file_data[9]
        self.copy_dir = list_of_dir_names[5]
        #self.copy_dir = "Vybrané_obrázky"
        self.image_browser_path = ""
        self.unbind_list = []
        self.image_extensions = ['.jpg', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi',
                    '.png', '.gif', '.bmp', '.tiff', '.tif', '.ico', '.webp',
                    '.raw', '.cr2', '.nef', '.arw', '.dng']
        
        self.previous_image_dimensions = 0,0
        self.previous_zoom = 1
        self.create_widgets()
        self.interrupt = self.interrupt_viewing(self)
        
    def call_menu(self): # Tlačítko menu (konec, návrat do menu)
        """
        Funkce čistí všechny zaplněné rámečky a funguje, jako tlačítko zpět do menu
        """
        list_of_frames = [self.main_frame,self.frame_with_path,self.background_frame]
        for frames in list_of_frames:
            frames.pack_forget()
            frames.grid_forget()
            frames.destroy()

        for keys in self.unbind_list:
            self.root.unbind(keys)
        #self.path_set.unbind("<Return>")
        menu()
    
    def get_images(self,path):  # Seznam všech obrázků v podporovaném formátu (včetně cesty)
        """
        Seznam všech obrázků v podporovaném formátu (včetně cesty)
        """
        list_of_files_to_view = []
        for files in os.listdir(path):
            files_split = files.split(".")
            if ("."+files_split[len(files_split)-1]) in self.image_extensions:
                list_of_files_to_view.append(path + files)

        return list_of_files_to_view

    def start(self,path): # Ověřování cesty, init, spuštění
        """
        Ověřování cesty, init, spuštění
        """
        path_found = True
        if path == "" or path == "/": #pripad, ze bylo pouzito tlacitko spusteni manualne vlozene cesty a nebo je chyba v config souboru
            path_found = False
            path = self.path_set.get() 
            if path != "":
                check = path_check(path)
                if check == False:
                    self.console.configure(text = "Zadaná cesta: "+str(path)+" nebyla nalezena",text_color="red")
                else:
                    path = check
                    path_found = True
            else:
                self.console.configure(text = "Nebyla vložena cesta k souborům",text_color="red")

        #automaticky okamzite otevre prvni z obrazku v dane ceste
        if path_found == True:
            if os.path.exists(path):
                self.all_images = self.get_images(path)
                if len(self.all_images) != 0:
                    self.image_browser_path = path
                    self.view_image(0) #zobrazit hned prvni obrazek po vlozene ceste
                    self.increment_of_image = 0
                    self.current_image_num.configure(text = str(self.increment_of_image+1) + "/" + str(len(self.all_images)))
                    self.console.configure(text = f"Vložena cesta: {path}",text_color="green")
                else:
                    self.console.configure(text = "- V zadané cestě nebyly nalezeny obrázky",text_color="red")
            else:
                self.console.configure(text = "- Vložená cesta je neplatná",text_color="red")
    
    def call_browseDirectories(self): # Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
        """
        Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
        """
        output = browseDirectories("all")
        if str(output[1]) != "/":
            self.path_set.delete("0","200")
            self.path_set.insert("0", output[1])
            self.console.configure(text=f"Byla vložena cesta: {output[1]}",text_color="white")
            self.start(output[1]) 

    def get_frame_dimensions(self): # Vrací aktuální rozměry rámečku
        """
        Vrací aktuální rozměry rámečku
        """
        whole_app_height = self.root._current_height
        whole_app_width = self.root._current_width
        width = whole_app_width
        height = whole_app_height - 129.6
        #print(f"Frame Dimensions: {width} x {height}")
        return [width, height]
              
    def calc_current_format(self,width,height): # Přepočítávání rozměrů obrázku do rozměru rámce podle jeho formátu + zooming
        """
        Přepočítávání rozměrů obrázku do rozměru rámce podle jeho formátu

        -vstupními daty jsou šířka a výška obrázku
        -přepočítávání pozicování obrázku a scrollbarů v závislosti na zoomu
        """
        frame_dimensions = self.get_frame_dimensions()
        zoom = self.zoom_slider.get() / 100
        frame_width, frame_height = frame_dimensions
        image_width = width
        image_height = height
        image_ratio = image_width / image_height
        
        # Vmestnani obrazku do velikosti aktualni velikosti ramce podle jeho formatu
        if image_height > image_width:
            new_height = frame_height
            new_width = int(new_height * image_ratio)

            if new_width > frame_width:
                new_width = frame_width
                new_height = int(new_width / image_ratio)
        else:
            new_width = frame_width
            new_height = int(new_width / image_ratio)

            if new_height > frame_height:
                new_height = frame_height
                new_width = int(new_height * image_ratio)

        new_height = new_height * zoom
        new_width = new_width * zoom

        # Pocitani delek scrollbaru
        scrollbar_length_x = min(1.0, frame_width / new_width)
        scrollbar_length_y = min(1.0, frame_height / new_height)
        current_h_scrollbar = self.horizontal_scrollbar.get()
        current_v_scrollbar = self.vertical_scrollbar.get()

        # uprava scrollbaru pri zoomovani
        if zoom > self.previous_zoom: # zda priblizujeme nebo oddalujeme
            new_slider_start = current_h_scrollbar[0]-((scrollbar_length_x+current_h_scrollbar[0])-current_h_scrollbar[1])
            self.horizontal_scrollbar.set(new_slider_start,current_h_scrollbar[1]) # nastaveni scrollbaru podle zoomu
            self.images.place_configure(relx=-(new_slider_start*(self.zoom_slider.get()/100)))
            
            new_slider_start = current_v_scrollbar[0]-((scrollbar_length_y+current_v_scrollbar[0])-current_v_scrollbar[1])
            self.vertical_scrollbar.set(new_slider_start,current_v_scrollbar[1]) # nastaveni scrollbaru podle zoomu
            self.images.place_configure(rely=-(new_slider_start*(self.zoom_slider.get()/100)))

        elif zoom < self.previous_zoom:
            if (scrollbar_length_x+current_h_scrollbar[0]) <= 1.0:
                self.horizontal_scrollbar.set(current_h_scrollbar[0],scrollbar_length_x+current_h_scrollbar[0])
            else:
                new_slider_start = current_h_scrollbar[0]-((scrollbar_length_x+current_h_scrollbar[0])-1)
                self.horizontal_scrollbar.set(new_slider_start,1.0) # nastaveni scrollbaru podle zoomu
                self.images.place_configure(relx=-(new_slider_start*(self.zoom_slider.get()/100))) # posun obrazku podle scrollbaru

            if (scrollbar_length_y+current_v_scrollbar[0]) <= 1.0:
                # pri oddalovani nejprve zvetsujeme scrollbar smerem dolu:
                self.vertical_scrollbar.set(current_v_scrollbar[0], scrollbar_length_y+current_v_scrollbar[0]) 
            else: #kdyz je vetsi, jak 1, coz je maximalni souradnice konce scrollbaru
                # kdyz uz scrollbar dosahuje az dolu, musime uz hybat s obrazkem a zvetsovat scrollbar smerem nahoru podle toho, o kolik byl posunut
                new_slider_start = current_v_scrollbar[0]-((scrollbar_length_y+current_v_scrollbar[0])-1)
                self.vertical_scrollbar.set(new_slider_start,1.0) # nastaveni scrollbaru podle zoomu
                self.images.place_configure(rely=-(new_slider_start*(self.zoom_slider.get()/100))) # posun obrazku podle scrollbaru

        self.previous_zoom = zoom
        #print(f"New Dimensions: {new_width} x {new_height}")
        return [new_width, new_height]

    def view_image(self,increment_of_image): # Samotné zobrazení obrázku
        """
        Samotné zobrazení obrázku

        -vstupními daty jsou informace o pozici obrázku v poli se všemi obrázky
        -přepočítávání rotace
        """
        if len(self.all_images) != 0:
            image_to_show = self.all_images[increment_of_image]
            with Image.open(image_to_show) as current_image:
                current_image = current_image.rotate(self.rotation_angle,expand=True)
                width,height = current_image.size
            
            dimensions = self.calc_current_format(width,height)
            displayed_image = customtkinter.CTkImage(current_image,size = (dimensions[0],dimensions[1]))
            self.images.configure(image = displayed_image)
            self.images.image = displayed_image
            self.root.update_idletasks()

    def next_image(self): # Další obrázek v pořadí (šipka vpravo)
        """
        Další obrázek v pořadí (šipka vpravo)
        """
        number_of_found_images = len(self.all_images)
        if number_of_found_images != 0:
            if self.increment_of_image < number_of_found_images -1:
                self.increment_of_image += 1
            else:
                self.increment_of_image = 0
            self.view_image(self.increment_of_image)
            self.current_image_num.configure(text = str(self.increment_of_image+1) + "/" + str(len(self.all_images)))
            self.console.configure(text = str(self.all_images[self.increment_of_image]),text_color="white")
    
    def previous_image(self): # Předchozí obrázek v pořadí (šipka vlevo)
        """
        Předchozí obrázek v pořadí (šipka vlevo)
        """
        number_of_found_images = len(self.all_images)
        if number_of_found_images != 0:
            if self.increment_of_image > 0:
                self.increment_of_image -= 1
            else:
                self.increment_of_image = number_of_found_images -1
            self.view_image(self.increment_of_image)
            self.current_image_num.configure(text = str(self.increment_of_image+1) + "/" + str(len(self.all_images)))
            self.console.configure(text = str(self.all_images[self.increment_of_image]),text_color="white")

    class interrupt_viewing: # Pro možnosti vykonávání subprocessu na pozadí
        """
        Pro možnosti vykonávání subprocessu na pozadí

        -bez této třídy by nebylo možné, během běžící sekvence obrázků, reagovat na tlačítka
        """
        def __init__(self,parent):
            self.parent = parent

        def images_loop(self):
            self.stop_flag = False  # Reset the stop flag
            thread = threading.Thread(target=self.long_running_task)
            thread.start()

        def long_running_task(self):
            number_of_found_images = len(self.parent.all_images)
            for i in range(0,number_of_found_images):
                if self.stop_flag:
                    break
                self.parent.next_image()
                speed=self.parent.speed_slider.get()/100
                calculated_time = 2-speed*2 # 1% dela necele 2 sekundy, 100%, nula sekund, maximalni vykon
                time.sleep(calculated_time)
            else:
                return 

        def stop_loop(self):
            self.stop_flag = True
  
    def stop(self):
        self.state = "stop"
        self.interrupt.stop_loop()

    def call_image_loop(self): # Volání třídy pro vykonávání subprocessu
        self.state = ""
        self.interrupt.images_loop()

    def update_speed_slider(self,*args):
        new_value = int(*args)
        self.percent1.configure(text = "")
        self.percent1.configure(text=str(new_value) + " %")

    def update_zoom_slider(self,*args):
        new_value = int(*args)
        self.percent2.configure(text = "")
        self.percent2.configure(text=str(new_value) + " %")
        # update image po zoomu
        if len(self.all_images) != 0:
            self.view_image(self.increment_of_image)

    def copy_image(self,path): # Tlačítko ULOŽIT, zkopíruje daný obrázek do složky v dané cestě
        """
        Tlačítko ULOŽIT, zkopíruje daný obrázek do složky v dané cestě

        -název složky přednastaven na Vybrané_obrázky
        -vlastnosti obrázku nijak nemění
        """
        image_path = self.all_images[self.increment_of_image]
        image = str(image_path).replace(path,"")
        if not os.path.exists(path + "/" + self.copy_dir):
            os.mkdir(path+ "/" + self.copy_dir)
        if not os.path.exists(path + "/" + self.copy_dir+ "/" + image):
            shutil.copy(path+ "/" + image,path + "/" + self.copy_dir+ "/" + image)
            self.console.configure(text = f"Obrázek zkopírován do zvláštní složky: \"{self.copy_dir}\".  ({image})",text_color="white")
        else:
            self.console.configure(text = f"Obrázek je již zkopírovaný uvnitř složky: {self.copy_dir}.  ({image})",text_color="red")

    def rotate_image(self):
        angles = [90.0,180.0,270.0,0.0]
        if self.rotation_angle < 270:
            self.rotation_angle += 90.0
        else:
            self.rotation_angle = 0.0
        self.view_image(self.increment_of_image)

    def Reset_all(self): # Vrátí všechny slidery a natočení obrázku do původní polohy
        """
        Vrátí všechny slidery a natočení obrázku do původní polohy
        """
        self.rotation_angle = 0.0
        self.zoom_slider.set(100)
        self.update_zoom_slider(100)
        self.speed_slider.set(100)
        self.update_speed_slider(100)
        #self.increment_of_image = 0
        #view_image(self.increment_of_image)
        #self.current_image_num.configure(text = str(self.increment_of_image+1) + "/" + str(len(self.all_images)))
        #console.configure(text = str(self.all_images[self.increment_of_image]))
        self.root.update_idletasks()
    
    def on_vertical_scroll(self,*args): # pohyb obrázkem v závislosti na vertikálním slideru
        new_y_coordinate = args[1]
        self.main_frame.yview_moveto(new_y_coordinate)
        self.images.place_configure(rely=-(new_y_coordinate*(self.zoom_slider.get()/100)))

    def on_horizontal_scroll(self,*args): # pohyb obrázkem v závislosti na horizontálním slideru
        new_x_coordinate = args[1]
        self.main_frame.xview_moveto(new_x_coordinate)
        self.images.place_configure(relx=-(new_x_coordinate*(self.zoom_slider.get()/100)))

    def create_widgets(self): # Vytvoření veškerých widgets (MAIN image browseru)
        #cisteni menu widgets
        for frames in self.list_of_menu_frames: 
            frames.pack_forget()
            frames.grid_forget()
            frames.destroy()
        
        self.frame_with_path = customtkinter.CTkFrame(master=self.root,height = 200)
        self.background_frame = customtkinter.CTkFrame(master=self.root)
        self.main_frame      = customtkinter.CTkCanvas(master=self.background_frame,background="black",highlightthickness=0)
        self.frame_with_path.pack(pady=5,padx=5,fill="x",expand=False,side = "top")
        self.background_frame.pack(pady=0,padx=5,ipadx=10,ipady=10,fill="both",expand=True,side = "bottom")

        self.vertical_scrollbar = customtkinter.CTkScrollbar(self.background_frame, orientation="vertical", command=self.on_vertical_scroll)
        self.vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_frame.configure(yscrollcommand=self.vertical_scrollbar.set)
        self.horizontal_scrollbar = customtkinter.CTkScrollbar(self.background_frame, orientation="horizontal", command=self.on_horizontal_scroll)
        self.horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.main_frame.configure(xscrollcommand=self.horizontal_scrollbar.set)
        self.main_frame.pack(pady=0,padx=5,ipadx=10,ipady=10,fill="both",expand=True,side = "bottom",anchor= "center")
        self.main_frame.configure(scrollregion=self.background_frame.bbox("all"))

        menu_button  = customtkinter.CTkButton(master = self.frame_with_path, width = 150,height=30, text = "MENU", command = lambda: self.call_menu(),font=("Arial",16,"bold"))
        self.path_set = customtkinter.CTkEntry(master = self.frame_with_path,width = 680,height=30,placeholder_text="Zadejte cestu k souborům (kde se soubory přímo nacházejí)")
        manual_path  = customtkinter.CTkButton(master = self.frame_with_path, width = 120,height=30,text = "Otevřít", command = lambda: self.start(self.path_set.get()),font=("Arial",16,"bold"))
        tree         = customtkinter.CTkButton(master = self.frame_with_path, width = 120,height=30,text = "EXPLORER", command = self.call_browseDirectories,font=("Arial",16,"bold"))
        self.console = customtkinter.CTkLabel(master = self.frame_with_path,text = "",height=15,justify = "left",font=("Arial",12),text_color="white")
        button_back  = customtkinter.CTkButton(master = self.frame_with_path, width = 20,height=30,text = "<", command = self.previous_image,font=("Arial",16,"bold"))
        self.current_image_num = customtkinter.CTkLabel(master = self.frame_with_path,text = "0",justify = "left",font=("Arial",16,"bold"))
        button_next  = customtkinter.CTkButton(master = self.frame_with_path, width = 20,height=30,text = ">", command = self.next_image,font=("Arial",16,"bold"))
        button_play  = customtkinter.CTkButton(master = self.frame_with_path, width = 100,height=30,text = "SPUSTIT", command = self.call_image_loop,font=("Arial",16,"bold"))
        button_stop  = customtkinter.CTkButton(master = self.frame_with_path, width = 100,height=30,text = "STOP", command = self.stop,font=("Arial",16,"bold"))
        button_save  = customtkinter.CTkButton(master = self.frame_with_path, width = 100,height=30,text = "ULOŽIT", command = lambda: self.copy_image(self.image_browser_path),font=("Arial",16,"bold"))
        rotate_button = customtkinter.CTkButton(master = self.frame_with_path, width = 100,height=30,text = "OTOČIT", command =  lambda: self.rotate_image(),font=("Arial",16,"bold"))
        speed_label  = customtkinter.CTkLabel(master = self.frame_with_path,text = "Rychlost:",justify = "left",font=("Arial",12))
        self.speed_slider = customtkinter.CTkSlider(master = self.frame_with_path,width=120,from_=1,to=100,command= self.update_speed_slider)
        self.percent1 = customtkinter.CTkLabel(master = self.frame_with_path,text = "%",justify = "left",font=("Arial",12))
        zoom_label   = customtkinter.CTkLabel(master = self.frame_with_path,text = "ZOOM:",justify = "left",font=("Arial",12))
        self.zoom_slider = customtkinter.CTkSlider(master = self.frame_with_path,width=120,from_=100,to=500,command= self.update_zoom_slider)
        self.percent2 = customtkinter.CTkLabel(master = self.frame_with_path,text = "%",justify = "left",font=("Arial",12))
        reset_button = customtkinter.CTkButton(master = self.frame_with_path, width = 100,height=30,text = "RESET", command = self.Reset_all,font=("Arial",16,"bold"))

        menu_button.grid(column = 0,row=0,pady = 5,padx =0,sticky = tk.W)
        self.path_set.grid(column = 0,row=0,pady = 5,padx =160,sticky = tk.W)
        manual_path.grid(column = 0,row=0,pady = 5,padx =850,sticky = tk.W)
        tree.grid(column = 0,row=0,pady = 5,padx =975,sticky = tk.W)
        self.console.grid(column = 0,row=1,pady = 5,padx =10,sticky = tk.W)
        button_back.grid(column = 0,row=2,pady = 5,padx =10,sticky = tk.W)
        self.current_image_num.grid(column = 0,row=2,pady = 5,padx =40,sticky = tk.W)
        button_next.grid(column = 0,row=2,pady = 5,padx =130,sticky = tk.W)
        button_play.grid(column = 0,row=2,pady = 5,padx =160,sticky = tk.W)
        button_stop.grid(column = 0,row=2,pady = 5,padx =265,sticky = tk.W)
        button_save.grid(column = 0,row=2,pady = 5,padx =370,sticky = tk.W)
        rotate_button.grid(column = 0,row=2,pady = 5,padx =475,sticky = tk.W)
        speed_label.grid(column = 0,row=2,pady = 5,padx =580,sticky = tk.W)
        self.speed_slider.grid(column = 0,row=2,pady = 5,padx =630,sticky = tk.W)
        self.percent1.grid(column = 0,row=2,pady = 5,padx =755,sticky = tk.W)
        zoom_label.grid(column = 0,row=2,pady = 5,padx =800,sticky = tk.W)
        self.zoom_slider.grid(column = 0,row=2,pady = 5,padx =840,sticky = tk.W)
        self.percent2.grid(column = 0,row=2,pady = 5,padx =960,sticky = tk.W)
        reset_button.grid(column = 0,row=2,pady = 5,padx =1005,sticky = tk.W)
        
        self.images = customtkinter.CTkLabel(master = self.main_frame,text = "")
        self.images.place(x=5,y=5)

        # nastaveni defaultnich hodnot slideru
        self.zoom_slider.set(100)
        self.update_zoom_slider(100)
        self.speed_slider.set(100)
        self.update_speed_slider(100)

        def focused_entry_widget():
            currently_focused = str(self.root.focus_get())
            if ".!ctkentry" in currently_focused:
                return True
            else:
                return False

        # KEYBOARD BINDING
        def button_hover(e):
            #rotate_button.configure(text=str(int(self.rotation_angle))+"° + 90°",font=("Arial",15))
            if int(self.rotation_angle==270):
                rotate_button.configure(text="0°",font=("Arial",15))
            else:
                rotate_button.configure(text=str(int(self.rotation_angle)+90)+"°",font=("Arial",15))
            rotate_button.update_idletasks()
            return
                
        def button_hover_leave(e):
            rotate_button.configure(text="OTOČIT",font=("Arial",16,"bold"))
        rotate_button.bind("<Enter>",button_hover)
        rotate_button.bind("<Button-1>",button_hover)
        rotate_button.bind("<Leave>",button_hover_leave)

        def pressed_space(e):
            if focused_entry_widget(): # pokud nabindovany znak neni vepisovan do entry widgetu
                return
            if self.state != "stop":
                self.state = "stop"
                self.interrupt.stop_loop()
            else:
                self.state = ""
                self.interrupt.images_loop()
        self.root.bind("<space>",pressed_space)
        self.unbind_list.append("<space>")

        def unfocus_widget(e):
            self.root.focus_set()
        self.root.bind("<Escape>",unfocus_widget)
        self.unbind_list.append("<Escape>")

        def pressed_left(e):
            if focused_entry_widget(): # pokud nabindovany znak neni vepisovan do entry widgetu
                return
            self.previous_image()
        self.root.bind("<Left>",pressed_left)
        self.unbind_list.append("<Left>")

        def pressed_right(e):
            if focused_entry_widget(): # pokud nabindovany znak neni vepisovan do entry widgetu
                return
            self.next_image()
        self.root.bind("<Right>",pressed_right)
        self.unbind_list.append("<Right>")

        def pressed_save(e):
            if focused_entry_widget(): # pokud nabindovany znak neni vepisovan do entry widgetu
                return
            self.copy_image(self.image_browser_path)
        self.root.bind("<s>",pressed_save)
        self.unbind_list.append("<s>")

        def pressed_rotate(e):
            button_hover(e) #update uhlu zobrazovanem na tlacitku
            if focused_entry_widget(): # pokud nabindovany znak neni vepisovan do entry widgetu
                return
            self.rotate_image()
        self.root.bind("<r>",pressed_rotate)
        self.unbind_list.append("<r>")

        def mouse_wheel(e):
            direction = -e.delta
            if direction < 0:
                #direction = "in"
                new_value = self.zoom_slider.get()+10
                if self.zoom_slider._to >= new_value:
                    self.zoom_slider.set(new_value)
                    self.percent2.configure(text=str(int(new_value)) + " %")
                else:
                    self.zoom_slider.set(self.zoom_slider._to) # pro pripad, ze by zbyvalo mene nez 5 do maxima 
            else:
                #direction = "out"
                new_value = self.zoom_slider.get()-10
                if self.zoom_slider._from_ <= new_value:
                    self.zoom_slider.set(new_value)
                    self.percent2.configure(text=str(int(new_value)) + " %")
                else:
                    self.zoom_slider.set(self.zoom_slider._from_) # pro pripad, ze by zbyvalo vice nez 5 do minima  

            if len(self.all_images) != 0: # update zobrazeni
                self.view_image(self.increment_of_image)      
        self.root.bind("<MouseWheel>",mouse_wheel)
        self.unbind_list.append("<MouseWheel>")
        
        self.released = False
        def mouse_clicked(e):
            self.images.focus_set()
            self.released = False
            x,y = e.x,e.y
            def get_direction(e):
                option = ""
                if abs(max(e.x,x)-min(e.x,x)) > abs(max(e.y,y)-min(e.y,y)):
                    option = "horizontal"
                else:
                    option = "vertical"
                if option == "horizontal":
                    if e.x > x:
                        #right
                        current_horizontal_value = self.horizontal_scrollbar.get()
                        if (current_horizontal_value[0] - 0.01) > 0.00:
                            args_tuple_h = (0,current_horizontal_value[0]-0.01)
                            self.on_horizontal_scroll(*args_tuple_h)
                            self.horizontal_scrollbar.set(current_horizontal_value[0]-0.01,current_horizontal_value[1]-0.01)      
                    else:
                        #left
                        current_horizontal_value = self.horizontal_scrollbar.get()
                        if (current_horizontal_value[1] + 0.01) < 1.00:
                            args_tuple_h = (0,current_horizontal_value[0]+0.01)
                            self.on_horizontal_scroll(*args_tuple_h)
                            self.horizontal_scrollbar.set(current_horizontal_value[0]+0.01,current_horizontal_value[1]+0.01)

                if option == "vertical":
                    if e.y > y:
                        #down
                        current_vertical_value = self.vertical_scrollbar.get()
                        if (current_vertical_value[0] - 0.01) > 0.00:
                            args_tuple_v = (0,current_vertical_value[0]-0.01)
                            self.on_vertical_scroll(*args_tuple_v)
                            self.vertical_scrollbar.set(current_vertical_value[0]-0.01,current_vertical_value[1]-0.01)
                    else:
                        #up
                        current_vertical_value = self.vertical_scrollbar.get()
                        if (current_vertical_value[1] + 0.01) < 1.00:
                            args_tuple_v = (0,current_vertical_value[0]+0.01)
                            self.on_vertical_scroll(*args_tuple_v)
                            self.vertical_scrollbar.set(current_vertical_value[0]+0.01,current_vertical_value[1]+0.01)
                return

            self.images.bind("<Motion>", get_direction)
            if self.released == True:
                return

            def end_func(e):
                self.images.unbind("<Motion>")
                self.images.unbind("<ButtonRelease-1>")
                self.released = True

            self.images.bind("<ButtonRelease-1>",end_func)
        self.images.bind("<Button-1>",mouse_clicked)

        def maximalize_window(e):
            # netrigguj fullscreen zatimco pisu do vstupniho textovyho pole
            if focused_entry_widget(): # pokud nabindovane pismeno neni vepisovano do entry widgetu
                return
            if int(self.root._current_width) > 1200:
                self.root.after(0, lambda:self.root.state('normal'))
                self.root.geometry("1200x900")
            else:
                self.root.after(0, lambda:self.root.state('zoomed'))
        self.root.bind("<f>",maximalize_window)
        self.unbind_list.append("<f>")

        def save_path_enter_btn(e):
            self.start(self.path_set.get())
        self.path_set.bind("<Return>",save_path_enter_btn)

        #hned na zacatku to vleze do defaultni slozky
        text_file_data = read_text_file_data()
        path = text_file_data[2]
        if path != "/" and path != False:
            self.path_set.delete("0","200")
            self.path_set.insert("0", path)
            self.console.configure(text="Byla vložena cesta z konfiguračního souboru Recources.txt",text_color="white")
            self.root.update_idletasks()
            self.image_browser_path = path
            self.start(path)
        else:
            self.console.configure(text = "Konfigurační soubor Recources.txt obsahuje neplatnou cestu, vložte manuálně",text_color="orange")

class Advanced_option: # Umožňuje nastavit základní parametry, které ukládá do textového souboru
    """
    Umožňuje nastavit základní parametry, které ukládá do textového souboru
    """
    def __init__(self,root,list_of_menu_frames):
        self.list_of_menu_frames = list_of_menu_frames
        self.root = root
        self.unbind_list = []
        self.drop_down_prefix_dir_names_list = []
        self.drop_down_static_dir_names_list = []
        self.default_displayed_prefix_dir = "cam"
        self.default_displayed_static_dir = 0
        self.default_dir_names = [" (default: Temp)"," (default: PAIRS)"," (default: Ke_smazani)",
                                  " (default: Konvertovane_BMP)"," (default: Konvertovane_JPG)",
                                  " (default: Vybrane_obrazky)"]
        self.creating_advanced_option_widgets()
    
    def call_menu(self): # Tlačítko menu (konec, návrat do menu)
        """
        Funkce čistí všechny zaplněné rámečky a funguje, jako tlačítko zpět do menu
        """
        self.list_of_frames = [self.top_frame,self.bottom_frame_default_path,self.bottom_frame_with_date,self.bottom_frame_with_files_to_keep,
                               self.bottom_frame_sorting_formats,self.bottom_frame_deleting_formats,self.main_console_frame,
                               self.list_of_menu_frames[1]]
        for frames in self.list_of_frames:
            frames.pack_forget()
            frames.grid_forget()
            frames.destroy()
        
        for binds in self.unbind_list:
            self.root.unbind(binds)
        #self.path_set.unbind("<Return>")
        menu()

    def clear_frame(self,frame): # Smaže widgets na daném framu
        """
        Smaže widgets na daném framu
        """
        for widget in frame.winfo_children():
            widget.destroy()  

    def maximalized(self): # Nastavení základního spouštění (v okně/ maximalizované)
        option = self.checkbox_maximalized.get()
        if option == 1:
            write_text_file_data("ano","maximalized")
        else:
            write_text_file_data("ne","maximalized")

    def setting_widgets(self,exception): # samotné možnosti úprav parametrů uložených v textové souboru
        """
        samotné možnosti úprav parametrů uložených v textové souboru
        """
        self.clear_frame(self.bottom_frame_with_date)
        self.clear_frame(self.bottom_frame_with_files_to_keep)
        self.clear_frame(self.bottom_frame_sorting_formats)
        self.clear_frame(self.bottom_frame_deleting_formats)
        #self.clear_frame(self.main_console_frame)
        self.clear_frame(self.bottom_frame_default_path)

        text_file_data = read_text_file_data()
        # refresh widgets s nastavenou exception:
        if exception == False:
            cutoff_date = text_file_data[4]
        else:
            cutoff_date = exception
        
        files_to_keep = text_file_data[3]
        default_prefix_func=text_file_data[5]
        default_prefix_cam =text_file_data[6]
        self.drop_down_prefix_dir_names_list = [(str(default_prefix_cam)+" (pro třídění podle č. kamery)"),(str(default_prefix_func)+" (pro třídění podle č. funkce)")]
        default_max_num_of_pallets=text_file_data[8]
        self.drop_down_static_dir_names_list = text_file_data[9]
        # pridani defaultniho nazvu pred zmenami do drop down menu
        for i in range(0,len(self.drop_down_static_dir_names_list)):
            self.drop_down_static_dir_names_list[i] += self.default_dir_names[i]

        def call_browseDirectories(): # Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
            """
            Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
            """
            output = browseDirectories("all")
            if str(output[1]) != "/":
                self.path_set.delete("0","200")
                self.path_set.insert("0", output[1])
                console_input = write_text_file_data(output[1],"default_path") # hlaska o nove vlozene ceste
                default_path_insert_console.configure(text = "Aktuálně nastavená základní cesta k souborům: " + str(output[1]),text_color="white")
                self.main_console.configure(text=console_input,text_color="green")
            else:
                default_path_insert_console.configure(text = str(output[0]),text_color="red")

        def save_path():
            path_given = str(self.path_set.get())
            path_check = path_check(path_given)
            if path_check != False and path_check != "/":
                console_input = write_text_file_data(path_check,"default_path")
                self.main_console.configure(text=console_input,text_color="green")
                default_path_insert_console.configure(text = "Aktuálně nastavená základní cesta k souborům: " + str(path_check),text_color="white")
            elif path_check != "/":
                self.main_console.configure(text=f"Zadaná cesta: {path_given} nebyla nalezena, nebude tedy uložena",text_color="red")
            elif path_check == "/":
                self.main_console.configure(text="Nebyla vložena žádná cesta k souborům",text_color="red")
                
        row_index = 0
        label5 = customtkinter.CTkLabel(master = self.bottom_frame_default_path,height=20,text = "Nastavte základní cestu k souborům při spuštění:",justify = "left",font=("Arial",12,"bold"))
        self.path_set = customtkinter.CTkEntry(master = self.bottom_frame_default_path,width=700,height=30,placeholder_text="")
        button_save5 = customtkinter.CTkButton(master = self.bottom_frame_default_path,width=50,height=30, text = "Uložit", command = lambda: save_path(),font=("Arial",12,"bold"))
        button_explorer = customtkinter.CTkButton(master = self.bottom_frame_default_path,width=100,height=30, text = "EXPLORER", command = lambda: call_browseDirectories(),font=("Arial",12,"bold"))
        default_path_insert_console=customtkinter.CTkLabel(master = self.bottom_frame_default_path,height=30,text ="",justify = "left",font=("Arial",12),text_color="white")
        label5.grid(column =0,row=row_index,sticky = tk.W,pady =0,padx=10)
        self.path_set.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        button_save5.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=710)
        button_explorer.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=760)
        default_path_insert_console.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)

        def save_path_enter_btn(e):
            save_path()
        self.path_set.bind("<Return>",save_path_enter_btn)
        if text_file_data[2] != False and text_file_data[2] != "/":
            default_path_insert_console.configure(text="Aktuálně nastavená základní cesta k souborům: " + str(text_file_data[2]),text_color="white")
            self.path_set.configure(placeholder_text=str(text_file_data[2]))
            self.path_set.delete("0","200")
            self.path_set.insert("0", str(text_file_data[2]))
        else:
            default_path_insert_console.configure(text="Aktuálně nastavená základní cesta k souborům v Recources.txt je neplatná",text_color="red")
            self.path_set.configure(placeholder_text="Není nastavena žádná základní cesta")

        def set_default_cutoff_date():
            input_month = set_month.get()
            if input_month != "":
                if input_month.isdigit():
                    if int(input_month) < 13 and int(input_month) > 0:
                        cutoff_date[1] = int(input_month)
                        max_days_in_month = Deleting.calc_days_in_month(int(cutoff_date[1]))
                        if int(cutoff_date[0]) > max_days_in_month:
                            cutoff_date[0] = str(max_days_in_month)
                        self.main_console.configure(text="Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2]),text_color="green")
                    else:
                        self.main_console.configure(text="Měsíc: " + str(input_month) + " je mimo rozsah",text_color="red")
                else:
                    self.main_console.configure(text="U nastavení měsíce jste nezadali číslo",text_color="red")

            input_day = set_day.get()
            max_days_in_month = Deleting.calc_days_in_month(int(cutoff_date[1]))

            if input_day != "":
                if input_day.isdigit():
                    if int(input_day) <= int(max_days_in_month) and int(input_day) > 0:
                        cutoff_date[0] = int(input_day)
                        self.main_console.configure(text="Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2]),text_color="green")
                    else:
                        self.main_console.configure(text="Den: " + str(input_day) + " je mimo rozsah",text_color="red")
                else:
                    self.main_console.configure(text="U nastavení dne jste nezadali číslo",text_color="red")

            input_year = set_year.get()
            if input_year != "":
                if input_year.isdigit():
                    if len(str(input_year)) == 2:
                        cutoff_date[2] = int(input_year) + 2000
                        self.main_console.configure(text="Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2]),text_color="green")
                    elif len(str(input_year)) == 4:
                        cutoff_date[2] = int(input_year)
                        self.main_console.configure(text="Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2]),text_color="green")
                    else:
                        self.main_console.configure(text="Rok: " + str(input_year) + " je mimo rozsah",text_color="red")
                else:
                    self.main_console.configure(text="U nastavení roku jste nezadali číslo",text_color="red")

            write_text_file_data(cutoff_date,"default_cutoff_date")
            self.setting_widgets(False)

        def set_files_to_keep():
            input_files_to_keep = files_to_keep_set.get()
            if input_files_to_keep.isdigit():
                if int(input_files_to_keep) >= 0:
                    files_to_keep = int(input_files_to_keep)
                    write_text_file_data(files_to_keep,"default_files_to_keep")
                    self.main_console.configure(text="Základní počet ponechaných starších souborů nastaven na: " + str(files_to_keep),text_color="green")
                    console_files_to_keep.configure(text = "Aktuálně nastavené minimum: "+str(files_to_keep),text_color="white")
                else:
                    self.main_console.configure(text="Mimo rozsah",text_color="red")
            else:
                self.main_console.configure(text="Nazadali jste číslo",text_color="red")

            self.setting_widgets(False)

        def insert_current_date():
            today = Deleting.get_current_date()
            today_split = today[1].split(".")
            i=0
            for items in today_split:
                i+=1
                cutoff_date[i-1]=items

            self.main_console.configure(text="Bylo vloženo dnešní datum (Momentálně všechny soubory vyhodnoceny, jako starší!)",text_color="orange")
            self.setting_widgets(cutoff_date)

        #widgets na nastaveni zakladniho dne
        label1 = customtkinter.CTkLabel(master = self.bottom_frame_with_date,height=20,text = "Nastavte základní datum pro vyhodnocení souborů, jako starších:",justify = "left",font=("Arial",12,"bold"))
        set_day = customtkinter.CTkEntry(master = self.bottom_frame_with_date,width=30,height=30, placeholder_text= cutoff_date[0])
        sep1 = customtkinter.CTkLabel(master = self.bottom_frame_with_date,height=20,width=10,text = ".",font=("Arial",20))
        set_month = customtkinter.CTkEntry(master = self.bottom_frame_with_date,width=30,height=30, placeholder_text= cutoff_date[1])
        sep2 = customtkinter.CTkLabel(master = self.bottom_frame_with_date,height=20,width=10,text = ".",font=("Arial",20))
        set_year = customtkinter.CTkEntry(master = self.bottom_frame_with_date,width=50,height=30, placeholder_text= cutoff_date[2])
        button_save1 = customtkinter.CTkButton(master = self.bottom_frame_with_date,width=50,height=30, text = "Uložit", command = lambda: set_default_cutoff_date(),font=("Arial",12,"bold"))
        insert_button = customtkinter.CTkButton(master = self.bottom_frame_with_date,width=130,height=30, text = "Vložit dnešní datum", command = lambda: insert_current_date(),font=("Arial",12,"bold"))
        label1.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        set_day.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
        sep1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=40)
        set_month.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=50)
        sep2.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=80)
        set_year.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=90)
        button_save1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=140)
        insert_button.grid(column =0,row=row_index+3,sticky = tk.W,pady =0,padx=10)

        def new_date_enter_btn(e):
            set_default_cutoff_date()
        set_day.bind("<Return>",new_date_enter_btn)
        set_month.bind("<Return>",new_date_enter_btn)
        set_year.bind("<Return>",new_date_enter_btn)
        
        def set_new_default_prefix(which_folder):
            report = ""
            inserted_prefix = str(set_new_def_prefix.get()).replace(" ","")
            if len(inserted_prefix) != 0:
                if inserted_prefix != str(default_prefix_cam) and inserted_prefix != str(default_prefix_func):
                    if which_folder == "cam":
                        report = write_text_file_data(inserted_prefix,"new_default_prefix_cam")
                        self.default_displayed_prefix_dir = "cam"
                    if which_folder == "func":
                        report = write_text_file_data(inserted_prefix,"new_default_prefix_func")
                        self.default_displayed_prefix_dir = "func"
                    self.main_console.configure(text=report,text_color="green")
                    self.setting_widgets(False) # refresh
                else:
                    self.main_console.configure(text = "Zadané jméno je již zabrané",text_color="red")
            else:
                self.main_console.configure(text = "Nutný alespoň jeden znak",text_color="red")
                
        def change_prefix_dir(*args):
            if str(*args) == str(self.drop_down_prefix_dir_names_list[1]):
                button_save_new_def_prefix.configure(command=lambda: set_new_default_prefix("func"))
                set_new_def_prefix.configure(placeholder_text = str(default_prefix_func))
                set_new_def_prefix.delete("0","100")
                set_new_def_prefix.insert("0", str(default_prefix_func))
            elif str(*args) == str(self.drop_down_prefix_dir_names_list[0]):
                button_save_new_def_prefix.configure(command=lambda: set_new_default_prefix("cam"))
                set_new_def_prefix.configure(placeholder_text = str(default_prefix_cam))
                set_new_def_prefix.delete("0","100")
                set_new_def_prefix.insert("0", str(default_prefix_cam))

        # upravovani prefixu slozek, default: pro trideni podle kamer
        label_folder_prefixes      = customtkinter.CTkLabel(master = self.bottom_frame_with_date,height=20,text = "Vyberte prefix složky, u které chcete změnit základní název:",justify = "left",font=("Arial",12,"bold"))
        drop_down_dir_names        = customtkinter.CTkOptionMenu(master = self.bottom_frame_with_date,width=250,values=self.drop_down_prefix_dir_names_list,command= change_prefix_dir)
        set_new_def_prefix         = customtkinter.CTkEntry(master = self.bottom_frame_with_date,width=200,height=30, placeholder_text= str(default_prefix_cam))
        button_save_new_def_prefix = customtkinter.CTkButton(master = self.bottom_frame_with_date,width=50,height=30, text = "Uložit", command = lambda: set_new_default_prefix("cam"),font=("Arial",12,"bold"))
        label_folder_prefixes.grid(column =1,row=row_index+1,sticky = tk.W,pady =0,padx=300)
        set_new_def_prefix.grid(column =1,row=row_index+2,sticky = tk.W,pady =0,padx=300)
        button_save_new_def_prefix.grid(column =1,row=row_index+2,sticky = tk.W,pady =0,padx=500)
        drop_down_dir_names.grid(column =1,row=row_index+3,sticky = tk.W,pady =0,padx=300)
        set_new_def_prefix.insert("0", str(default_prefix_cam))
        def prefix_enter_btn(e):
            if str(drop_down_dir_names.get()) == str(self.drop_down_prefix_dir_names_list[0]):
                set_new_default_prefix("cam")
            elif str(drop_down_dir_names.get()) == str(self.drop_down_prefix_dir_names_list[1]):
                set_new_default_prefix("func")
        set_new_def_prefix.bind("<Return>",prefix_enter_btn)
        #  nastaveni defaultniho vyberu z drop-down menu
        if self.default_displayed_prefix_dir == "cam":
            change_prefix_dir(self.drop_down_prefix_dir_names_list[0])
            drop_down_dir_names.set(self.drop_down_prefix_dir_names_list[0])
        elif self.default_displayed_prefix_dir == "func":
            change_prefix_dir(self.drop_down_prefix_dir_names_list[1])
            drop_down_dir_names.set(self.drop_down_prefix_dir_names_list[1])

        #widgets na nastaveni zakladniho poctu files_to_keep
        files_to_keep_console_text ="Aktuálně nastavené minimum: "+str(files_to_keep)
        label2 = customtkinter.CTkLabel(master = self.bottom_frame_with_files_to_keep,height=20,text = "Nastavte základní počet ponechaných souborů, vyhodnocených jako starších:",justify = "left",font=("Arial",12,"bold"))
        files_to_keep_set = customtkinter.CTkEntry(master = self.bottom_frame_with_files_to_keep,width=50,height=30, placeholder_text= files_to_keep)
        button_save2 = customtkinter.CTkButton(master = self.bottom_frame_with_files_to_keep,width=50,height=30, text = "Uložit", command = lambda: set_files_to_keep(),font=("Arial",12,"bold"))
        console_files_to_keep=customtkinter.CTkLabel(master = self.bottom_frame_with_files_to_keep,height=30,text =files_to_keep_console_text,justify = "left",font=("Arial",12))
        label2.grid(column =0,row=row_index,sticky = tk.W,pady =0,padx=10)
        files_to_keep_set.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        button_save2.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=60)
        console_files_to_keep.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
        def files_to_keep_enter_btn(e):
            set_files_to_keep()
        files_to_keep_set.bind("<Return>",files_to_keep_enter_btn)

        def set_new_default_dir_name():
            inserted_new_name = str(set_new_def_folder_name.get()).replace(" ","")
            report = ["Základní název složky pro nepáry (soubory nezastoupenými všemi nalezenými formáty) změněn na: ",
                      "Základní název složky pro nalezené dvojice změněn na: ",
                      "Základní název složky se soubory, které jsou určené ke smazání změněn na: ",
                      "Základní název složky pro soubory převedené do .bmp formátu změněn na: ",
                      "Základní název složky pro soubory převedené do .jpg formátu změněn na: ",
                      "Základní název složky pro zkopírované (uložené) vybrané obrázky z prohlížeče změněn na: "]
            colisions = 0
            
            if len(inserted_new_name) != 0:
                for i in range(0,len(self.drop_down_static_dir_names_list)):
                    neme_list_without_suffix = str(self.drop_down_static_dir_names_list[i]).replace(str(self.default_dir_names[i]),"")
                    if inserted_new_name == neme_list_without_suffix:
                        colisions += 1        
                if colisions == 0:
                    #zjistujeme, co mame navolene
                    for i in range(0,len(self.drop_down_static_dir_names_list)):
                        
                        if str(drop_down_static_dir_names.get()) == str(self.drop_down_static_dir_names_list[i]):
                            # zasilame k zapsani informaci o nastavenem vstupu a soucasne i pozici v poli
                            write_text_file_data(inserted_new_name+" | "+str(i),"new_default_static_dir_name")
                            self.default_displayed_static_dir = i
                            neme_list_without_suffix = inserted_new_name.replace(str(self.default_dir_names[i]),"")
                            self.main_console.configure(text=report[i]+neme_list_without_suffix,text_color="green")
                            self.setting_widgets(False) # refresh
                else:
                    self.main_console.configure(text = "Zadané jméno je již zabrané",text_color="red")
            else:
                self.main_console.configure(text = "Nutný alespoň jeden znak",text_color="red")
                
        def change_static_dir(*args):
            for i in range(0,len(self.drop_down_static_dir_names_list)):
                if str(self.drop_down_static_dir_names_list[i]) == str(*args):
                    neme_list_without_suffix = str(self.drop_down_static_dir_names_list[i]).replace(str(self.default_dir_names[i]),"")
                    set_new_def_folder_name.configure(placeholder_text = neme_list_without_suffix)
                    set_new_def_folder_name.delete("0","100")
                    set_new_def_folder_name.insert("0", neme_list_without_suffix)
                    
        #widgets na nastaveni jmen statickych slozek
        label_folder_name_change = customtkinter.CTkLabel(master = self.bottom_frame_with_files_to_keep,height=20,text = "Vyberte složku, u které chcete změnit základní název",justify = "left",font=("Arial",12,"bold"))
        set_new_def_folder_name = customtkinter.CTkEntry(master = self.bottom_frame_with_files_to_keep,width=200,height=30, placeholder_text= str(default_prefix_func))
        button_save_new_name = customtkinter.CTkButton(master = self.bottom_frame_with_files_to_keep,width=50,height=30, text = "Uložit", command = lambda: set_new_default_dir_name(),font=("Arial",12,"bold"))
        drop_down_static_dir_names = customtkinter.CTkOptionMenu(master = self.bottom_frame_with_files_to_keep,width=250,values=self.drop_down_static_dir_names_list,command= change_static_dir)
        label_folder_name_change.grid(column =1,row=row_index,sticky = tk.W,pady =0,padx=230)
        set_new_def_folder_name.grid(column =1,row=row_index+1,sticky = tk.W,pady =0,padx=230)
        button_save_new_name.grid(column =1,row=row_index+1,sticky = tk.W,pady =0,padx=430)
        drop_down_static_dir_names.grid(column =1,row=row_index+2,sticky = tk.W,pady =0,padx=230)
        drop_down_increment = self.default_displayed_static_dir
        corrected_default_input = str(self.drop_down_static_dir_names_list[drop_down_increment]).replace(str(self.default_dir_names[drop_down_increment]),"")
        set_new_def_folder_name.insert("0", corrected_default_input)
        def static_dir_enter_btn(e):
            set_new_default_dir_name()
        set_new_def_folder_name.bind("<Return>",static_dir_enter_btn)
        # nastaveni defaultniho vyberu z drop-down menu
        drop_down_static_dir_names.set(self.drop_down_static_dir_names_list[drop_down_increment])
        
        def add_format(which_operation):
            if which_operation == 0:
                new_format = str(formats_set.get())
                if new_format !="":
                    main_console_text = write_text_file_data(new_format,"add_supported_sorting_formats")
                    self.main_console.configure(text=main_console_text,text_color="white")
                    
            if which_operation == 1:
                new_format = str(formats_set2.get())
                if new_format !="":
                    main_console_text = write_text_file_data(new_format,"add_supported_deleting_formats")
                    self.main_console.configure(text=main_console_text,text_color="white")
            self.setting_widgets(False)

        def pop_format(which_operation):
            if which_operation == 0:
                format_to_delete = str(formats_set.get())
                if format_to_delete !="":
                    main_console_text = write_text_file_data(format_to_delete,"pop_supported_sorting_formats")
                    self.main_console.configure(text=main_console_text,text_color="white")
            if which_operation == 1:
                format_to_delete = str(formats_set2.get())
                if format_to_delete !="":
                    main_console_text = write_text_file_data(format_to_delete,"pop_supported_deleting_formats")
                    self.main_console.configure(text=main_console_text,text_color="white")

            self.setting_widgets(False)

        supported_formats_sorting = "Aktuálně nastavené podporované formáty pro možnosti třídění: " + str(text_file_data[0])
        label3 = customtkinter.CTkLabel(master = self.bottom_frame_sorting_formats,height=20,text = "Nastavte podporované formáty pro možnosti: TŘÍDĚNÍ:",justify = "left",font=("Arial",12,"bold"))
        formats_set = customtkinter.CTkEntry(master = self.bottom_frame_sorting_formats,width=50,height=30)
        button_save3 = customtkinter.CTkButton(master = self.bottom_frame_sorting_formats,width=50,height=30, text = "Uložit", command = lambda: add_format(0),font=("Arial",12,"bold"))
        button_pop = customtkinter.CTkButton(master = self.bottom_frame_sorting_formats,width=70,height=30, text = "Odebrat", command = lambda: pop_format(0),font=("Arial",12,"bold"))
        console_bottom_frame_3=customtkinter.CTkLabel(master = self.bottom_frame_sorting_formats,height=30,text =supported_formats_sorting,justify = "left",font=("Arial",12))
        label3.grid(column =0,row=row_index,sticky = tk.W,pady =0,padx=10)
        formats_set.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        button_save3.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=60)
        button_pop.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=110)
        console_bottom_frame_3.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)

        def set_max_num_of_pallets():
            input_1 = set_max_pallets.get()
            if input_1.isdigit() == False:
                self.main_console.configure(text = "Nezadali jste číslo",text_color="red")
            elif int(input_1) <1:
                self.main_console.configure(text = "Mimo rozsah",text_color="red")
            else:
                self.main_console.configure(text = f"Počet palet nastaven na: {input_1}",text_color="green")
                write_text_file_data(input_1,"pallets_set")
                
        #widgets na nastaveni zakladniho poctu palet v obehu
        label_pallets = customtkinter.CTkLabel(master = self.bottom_frame_sorting_formats,height=20,text = "Nastavte základní maximální počet paletek v oběhu:",justify = "left",font=("Arial",12,"bold"))
        set_max_pallets = customtkinter.CTkEntry(master = self.bottom_frame_sorting_formats,width=100,height=30, placeholder_text= str(default_max_num_of_pallets))
        button_save_max_num_of_pallets = customtkinter.CTkButton(master = self.bottom_frame_sorting_formats,width=50,height=30, text = "Uložit", command = lambda: set_max_num_of_pallets(),font=("Arial",12,"bold"))
        label_pallets.grid(column =1,row=row_index,sticky = tk.W,pady =0,padx=275)
        set_max_pallets.grid(column =1,row=row_index+1,sticky = tk.W,pady =0,padx=275)
        button_save_max_num_of_pallets.grid(column =1,row=row_index+1,sticky = tk.W,pady =0,padx=375)
        
        def new_max_pallets_enter_btn(e):
            set_max_num_of_pallets()
        set_max_pallets.bind("<Return>",new_max_pallets_enter_btn)

        supported_formats_deleting = "Aktuálně nastavené podporované formáty pro možnosti mazání: " + str(text_file_data[1])
        label4 = customtkinter.CTkLabel(master = self.bottom_frame_deleting_formats,height=20,text = "Nastavte podporované formáty pro možnosti: MAZÁNÍ:",justify = "left",font=("Arial",12,"bold"))
        formats_set2 = customtkinter.CTkEntry(master = self.bottom_frame_deleting_formats,width=50,height=30)
        button_save4 = customtkinter.CTkButton(master = self.bottom_frame_deleting_formats,width=50,height=30, text = "Uložit", command = lambda: add_format(1),font=("Arial",12,"bold"))
        button_pop2 = customtkinter.CTkButton(master = self.bottom_frame_deleting_formats,width=70,height=30, text = "Odebrat", command = lambda: pop_format(1),font=("Arial",12,"bold"))
        console_bottom_frame_4=customtkinter.CTkLabel(master = self.bottom_frame_deleting_formats,height=30,text =supported_formats_deleting,justify = "left",font=("Arial",12))
        label4.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        formats_set2.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
        button_save4.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=60)
        button_pop2.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=110)
        console_bottom_frame_4.grid(column =0,row=row_index+3,sticky = tk.W,pady =0,padx=10)

    def creating_advanced_option_widgets(self): # Vytváří veškeré widgets (advance option MAIN)
        #cisteni menu widgets
        #for frames in list_of_menu_frames: 
        self.list_of_menu_frames[0].pack_forget()
        self.list_of_menu_frames[0].grid_forget()
        self.list_of_menu_frames[0].destroy()

        self.main_console_frame          = customtkinter.CTkFrame(master=self.root)
        self.bottom_frame_deleting_formats = customtkinter.CTkFrame(master=self.root,height = 200)
        self.bottom_frame_sorting_formats = customtkinter.CTkFrame(master=self.root,height = 200)
        self.bottom_frame_with_files_to_keep = customtkinter.CTkFrame(master=self.root,height = 200)
        self.bottom_frame_with_date      = customtkinter.CTkFrame(master=self.root,height = 200)
        self.bottom_frame_default_path   = customtkinter.CTkFrame(master=self.root,height = 200)
        self.top_frame                   = customtkinter.CTkFrame(master=self.root,height = 200)
        self.main_console_frame.pack(pady=5,padx=5,fill="both",expand=True,side = "bottom")
        self.bottom_frame_deleting_formats.pack(pady=5,padx=5,fill="x",expand=False,side = "bottom")
        self.bottom_frame_sorting_formats.pack(pady=5,padx=5,fill="x",expand=False,side = "bottom")
        self.bottom_frame_with_files_to_keep.pack(pady=5,padx=5,fill="x",expand=False,side = "bottom")
        self.bottom_frame_with_date.pack(pady=5,padx=5,fill="x",expand=False,side = "bottom")
        self.bottom_frame_default_path.pack(pady=5,padx=5,fill="x",expand=False,side = "bottom")
        self.top_frame.pack(pady=5,padx=5,fill="x",expand=False,side = "bottom")

        label0          = customtkinter.CTkLabel(master = self.top_frame,height=20,text = "Nastavte požadované parametry (nastavení bude uloženo i po vypnutí aplikace): ",justify = "left",font=("Arial",20,"bold"))
        menu_button     = customtkinter.CTkButton(master = self.top_frame, width = 180, text = "MENU", command = lambda: self.call_menu(),font=("Arial",20,"bold"))
        self.checkbox_maximalized = customtkinter.CTkCheckBox(master = self.top_frame, text = "Spouštět v maximalizovaném okně",command = lambda: self.maximalized())
        menu_button.grid(column =0,row=0,sticky = tk.W,pady =0,padx=10)
        label0.grid(column =0,row=0,sticky = tk.W,pady =0,padx=210)
        self.checkbox_maximalized.grid(column =0,row=2,sticky = tk.W,pady =10,padx=10)

        main_console_label = customtkinter.CTkLabel(master = self.main_console_frame,height=50,text ="KONZOLA:",justify = "left",font=("Arial",16,"bold"))
        main_console_label.grid(column =0,row=0,sticky = tk.W,pady =0,padx=10)
        self.main_console = customtkinter.CTkLabel(master = self.main_console_frame,height=50,text ="",justify = "left",font=("Arial",16))
        self.main_console.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)

        if read_text_file_data()[7] == "ano":
            self.checkbox_maximalized.select()
        else:
            self.checkbox_maximalized.deselect()

        self.setting_widgets(False)

        def maximalize_window(e):
            # netrigguj fullscreen zatimco pisu do vstupniho textovyho pole
            currently_focused = str(self.root.focus_get())
            if ".!ctkentry" in currently_focused:
                return
            if int(self.root._current_width) > 1200:
                self.root.after(0, lambda:self.root.state('normal'))
                self.root.geometry("1200x900")
            else:
                self.root.after(0, lambda:self.root.state('zoomed'))
        self.root.bind("<f>",maximalize_window)
        self.unbind_list.append("<f>")

        def unfocus_widget(e):
            #print(self.root.focus_get())
            self.root.focus_set()
        self.root.bind("<Escape>",unfocus_widget)
        self.unbind_list.append("<Escape>")

class Converting_option: # Spouští možnosti konvertování typu souborů
    """
    Spouští možnosti konvertování typu souborů

    -Spouští přes příkazový řádek command, který je vykonáván v externí aplikaci s dll knihovnami
    """
    def __init__(self,root,list_of_menu_frames):
        self.root = root
        self.list_of_menu_frames = list_of_menu_frames
        text_file_data = read_text_file_data()
        list_of_folder_names = text_file_data[9]
        self.bmp_folder_name = list_of_folder_names[3]
        self.jpg_folder_name = list_of_folder_names[4]
        self.create_convert_option_widgets()
    
    def call_menu(self): # Tlačítko menu (konec, návrat do menu)
        """
        Funkce čistí všechny zaplněné rámečky a funguje, jako tlačítko zpět do menu
        """
        list_of_frames = [self.frame_path_input,self.bottom_frame1,self.bottom_frame2,self.list_of_menu_frames[1]]
        for frames in list_of_frames:
            frames.pack_forget()
            frames.grid_forget()
            frames.destroy()

        self.root.unbind("<f>")
        menu()

    def convert_files(self,path): # zde se volá externí script
        selected_format = "bmp"
        if self.checkbox_bmp.get() == 1:
            selected_format = "bmp"
        if self.checkbox_jpg.get() == 1:
            selected_format = "jpg"

        Converting.output = []
        Converting.whole_converting_function(path,selected_format,self.bmp_folder_name,self.jpg_folder_name)
        output_text = ""
        for i in range(0,len(Converting.output)):
            if len(Converting.output[i]) > 170: # kdyz by se vypis nevesel na obrazovku
                Converting.output[i] = split_text_to_rows(Converting.output[i],170)
            output_text = output_text + Converting.output[i]
        if output_text != "":
            if "Konvertování bylo dokončeno" in output_text:
                self.console.configure(text = output_text,text_color = "green")
            else:
                self.console.configure(text = output_text,text_color = "red")

    def start(self):# Ověřování cesty, init, spuštění
        """
        Ověřování cesty, init, spuštění
        """
        if self.checkbox_bmp.get()+self.checkbox_jpg.get() == 0:
            self.console.configure(text = "Nevybrali jste žádný formát, do kterého se má konvertovat :-)",text_color="red")
        else:
            path = self.path_set.get() 
            if path != "":
                check = path_check(path)
                if check == False:
                    self.console.configure(text = "Zadaná cesta: "+str(path)+" nebyla nalezena",text_color="red")
                else:
                    path = check
                    self.console.configure(text = f"Probíhá konvertování souborů v cestě: {path}",text_color="white")
                    self.console.update_idletasks()
                    self.root.update_idletasks()
                    self.convert_files(path)
            else:
                self.console.configure(text = "Nebyla vložena cesta k souborům",text_color="red")

    def call_browseDirectories(self): # Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
        """
        Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
        """
        output = browseDirectories("all")
        if str(output[1]) != "/":
            self.path_set.delete("0","200")
            self.path_set.insert("0", output[1])
            self.console.configure(text=f"Byla vložena cesta: {output[1]}",text_color="green")
        else:
            self.console.configure(text = str(output[0]),text_color="red")

    def selected_bmp(self):
        self.checkbox_jpg.deselect()
        self.label.configure(text=f"Konvertované soubory budou vytvořeny uvnitř separátní složky: \"{self.bmp_folder_name}\"\nPodporované formáty: .ifz\nObsahuje-li .ifz soubor více obrázků, budou uloženy v následující syntaxi:\nxxx_0.bmp, xxx_1.bmp ...\nPro správnou funkci programu nesmí cesta obsahovat složky s mezerou v názvu")
    
    def selected_jpg(self):
        self.checkbox_bmp.deselect()
        self.label.configure(text=f"Konvertované soubory budou vytvořeny uvnitř separátní složky: \"{self.jpg_folder_name}\"\nPodporované formáty: .ifz\nObsahuje-li .ifz soubor více obrázků, budou uloženy v následující syntaxi:\nxxx_0.bmp, xxx_1.bmp ...\nPro správnou funkci programu nesmí cesta obsahovat složky s mezerou v názvu")

    def create_convert_option_widgets(self):  # Vytváří veškeré widgets (convert option MAIN)
        #cisteni menu widgets
        #for frames in self.list_of_menu_frames: 
        self.list_of_menu_frames[0].pack_forget()
        self.list_of_menu_frames[0].grid_forget()
        self.list_of_menu_frames[0].destroy()

        #definice ramcu
        self.frame_path_input = customtkinter.CTkFrame(master=self.root)
        self.bottom_frame2    = customtkinter.CTkScrollableFrame(master=self.root)
        self.bottom_frame1    = customtkinter.CTkFrame(master=self.root,height = 80)
        self.frame_path_input.pack(pady=5,padx=5,fill="both",expand=False,side = "top")
        self.bottom_frame2.pack(pady=5,padx=5,fill="both",expand=True,side = "bottom")
        self.bottom_frame1.pack(pady=0,padx=5,fill="x",expand=False,side = "bottom")

        self.checkbox_bmp = customtkinter.CTkCheckBox(master = self.bottom_frame1, text = "Konvertovat do formátu .bmp",command=self.selected_bmp,font=("Arial",16,"bold"))
        self.checkbox_jpg = customtkinter.CTkCheckBox(master = self.bottom_frame1, text = "Konvertovat do formátu .jpg",command=self.selected_jpg,font=("Arial",16,"bold"))
        self.checkbox_bmp.pack(pady =20,padx=10,anchor ="w")
        self.checkbox_jpg.pack(pady =20,padx=10,anchor ="w")

        menu_button  = customtkinter.CTkButton(master = self.frame_path_input, width = 180, text = "MENU", command = lambda: self.call_menu(),font=("Arial",20,"bold"))
        self.path_set = customtkinter.CTkEntry(master = self.frame_path_input,placeholder_text="Zadejte cestu k souborům určeným ke konvertování (kde se soubory přímo nacházejí)")
        tree         = customtkinter.CTkButton(master = self.frame_path_input, width = 180,text = "EXPLORER", command = self.call_browseDirectories,font=("Arial",20,"bold"))
        menu_button.pack(pady =12,padx=10,anchor ="w",side="left")
        self.path_set.pack(pady = 12,padx =0,anchor ="w",side="left",fill="both",expand=True)
        tree.pack(pady = 12,padx =10,anchor ="w",side="left")

        self.label   = customtkinter.CTkLabel(master = self.bottom_frame2,text = f"Konvertované soubory budou vytvořeny uvnitř separátní složky: \"{self.bmp_folder_name}\"\nPodporované formáty: .ifz\nObsahuje-li .ifz soubor více obrázků, budou uloženy v následující syntaxi:\nxxx_0.bmp, xxx_1.bmp ...\nPro správnou funkci programu nesmí cesta obsahovat složky s mezerou v názvu",justify = "left",font=("Arial",16,"bold"))
        button  = customtkinter.CTkButton(master = self.bottom_frame2, text = "KONVERTOVAT", command = self.start,font=("Arial",20,"bold"))
        self.console = customtkinter.CTkLabel(master = self.bottom_frame2,text = "",justify = "left",font=("Arial",15))
        self.label.pack(pady =10,padx=10)
        button.pack(pady =20,padx=10)
        button._set_dimensions(300,60)
        self.console.pack(pady =10,padx=10)
        # default:
        self.checkbox_bmp.select()

        read_file_data = read_text_file_data()
        recources_path = read_file_data[2]
        if recources_path != False and recources_path != "/":
            self.path_set.delete("0","200")
            self.path_set.insert("0", str(recources_path))
            self.console.configure(text="Byla vložena cesta z konfiguračního souboru Recources.txt",text_color="white")
        else:
            self.console.configure(text="Konfigurační soubor Recources.txt obsahuje neplatnou cestu k souborům",text_color="orange")

        def maximalize_window(e):
            # netrigguj fullscreen zatimco pisu do vstupniho textovyho pole
            currently_focused = str(self.root.focus_get())
            if ".!ctkentry" in currently_focused:
                return
            if int(self.root._current_width) > 1200:
                self.root.after(0, lambda:self.root.state('normal'))
                self.root.geometry("1200x900")
            else:
                self.root.after(0, lambda:self.root.state('zoomed'))
        self.root.bind("<f>",maximalize_window)

class Deleting_option: # Umožňuje mazat soubory podle nastavených specifikací
    """
    Umožňuje mazat soubory podle nastavených specifikací

    -obsahuje i režim testování, kde soubory pouze přesune do složky ke smazání
    -umožňuje procházet více subsložek
    
    """
    def __init__(self,root,list_of_menu_frames):
        text_file_data = read_text_file_data()
        self.root = root
        self.list_of_menu_frames = list_of_menu_frames
        self.more_dirs = False
        self.unbind_list = []
        self.supported_formats_deleting = text_file_data[0]
        self.files_to_keep = text_file_data[3]
        self.cutoff_date = text_file_data[4]
        list_of_folder_names = text_file_data[9]
        self.to_delete_folder_name = list_of_folder_names[2]
        self.console_frame_right_1_text = "","white"
        self.console_frame_right_2_text = "","white"

        self.create_deleting_option_widgets()
 
    def call_menu(self): # Tlačítko menu (konec, návrat do menu)
        """
        Funkce čistí všechny zaplněné rámečky a funguje, jako tlačítko zpět do menu
        """
        list_of_frames = [self.frame_path_input,self.bottom_frame1,self.bottom_frame2,self.frame_right,self.frame_with_checkboxes,self.list_of_menu_frames[1]]
        for frames in list_of_frames:
            frames.pack_forget()
            frames.grid_forget()
            frames.destroy()
        
        for binds in self.unbind_list:
            self.root.unbind(binds)
        #self.path_set.unbind("<Return>")
        menu()

    def start(self):# Ověřování cesty, init, spuštění
        """
        Ověřování cesty, init, spuštění
        """
        if self.checkbox.get()+self.checkbox2.get()+self.checkbox3.get() == 0:
            self.console.configure(text = "Nevybrali jste žádný způsob mazání :-)",text_color="red")
            self.info.configure(text = "")

        else:
            path = self.path_set.get() 
            if path != "":
                check = path_check(path)
                if check == False:
                    self.console.configure(text = "Zadaná cesta: "+str(path)+" nebyla nalezena",text_color="red")
                else:
                    path = check
                    if self.checkbox_testing.get() != 1:
                        if self.checkbox6.get() == 1 and self.checkbox3.get() != 1: # sublozky u adresaru
                            confirm_prompt_msg = f"Opravdu si přejete spustit navolené mazání souborů v cestě:\n{path}\na procházet přitom i SUBSLOŽKY?"
                        elif self.checkbox3.get() == 1:
                            confirm_prompt_msg = f"Opravdu si přejete spustit navolené mazání ADRESÁŘŮ v cestě:\n{path}"
                        else:
                            confirm_prompt_msg = f"Opravdu si přejete spustit navolené mazání souborů v cestě:\n{path}"
                        confirm = tk.messagebox.askokcancel("Potvrzení", confirm_prompt_msg)
                    else: # pokud neni zapnut rezim testovani
                        confirm = True

                    if confirm == True:
                        self.console.configure(text = "Provádím navolené možnosti mazání v cestě: " + str(path),text_color="white")
                        self.console.update_idletasks()
                        self.root.update_idletasks()
                        self.del_files(path)
                    else:
                        self.console.configure(text = "Zrušeno uživatelem",text_color="red")
            else:
                self.console.configure(text = "Nebyla vložena cesta k souborům",text_color="red")

    def del_files(self,path): # zde se volá externí script: Deleting
        testing_mode = True
        del_option = 0
        if self.checkbox.get() == 1:
            del_option = 1
        if self.checkbox2.get() == 1:
            del_option = 2
        if self.checkbox3.get() == 1:
            del_option = 3
        if self.checkbox6.get() == 1:
            self.more_dirs = True
        else:
            self.more_dirs = False
        if self.checkbox_testing.get() == 1:
            testing_mode = True
        else:
            testing_mode = False

        Deleting.output = []

        Deleting.whole_deleting_function(path,self.more_dirs,del_option,self.files_to_keep,self.cutoff_date,self.supported_formats_deleting,
                                         testing_mode,self.to_delete_folder_name)
        output_text = ""
        for i in range(0,len(Deleting.output)):
            if len(Deleting.output[i]) > 170: # kdyz by se vypis nevesel na obrazovku
                Deleting.output[i] = split_text_to_rows(Deleting.output[i],170)
            output_text = output_text + Deleting.output[i]# + "\n"
        if "Mazání dokončeno" in output_text:
            self.console.configure(text = output_text,text_color = "green")
        else:
            self.console.configure(text = output_text,text_color = "red")
    
    def call_browseDirectories(self): # Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
        """
        Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
        """
        if self.checkbox6.get() == 1: # pokud je zvoleno more_dirs v exploreru pouze slozky...
            output = browseDirectories("only_dirs")
        else:
            output = browseDirectories("all")
        if str(output[1]) != "/":
            self.path_set.delete("0","200")
            self.path_set.insert("0", output[1])
            self.console.configure(text=f"Byla vložena cesta: {output[1]}",text_color="green")
        else:
            self.console.configure(text = str(output[0]),text_color="red")

    def clear_frame(self,frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def selected(self,clear:bool): # První možnost mazání, od nejstarších
        """
        Nastavení widgets pro první možnost mazání

        -vstup: console text a barva textu

        -Budou smazány soubory starší než nastavené datum, přičemž bude ponechán nastavený počet souborů, vyhodnocených, jako starších\n
        -Podporované formáty jsou uživatelem nastavené a uložené v textovém souboru
        """
        self.clear_frame(self.frame_right)
        self.console.configure(text = "")
        self.checkbox2.deselect()
        self.checkbox3.deselect()
        self.info.configure(text = f"- Budou smazány soubory starší než nastavené datum, přičemž bude ponechán nastavený počet souborů, vyhodnocených, jako starších\nPodporované formáty: {self.supported_formats_deleting}",font = ("Arial",16,"bold"),justify="left")
        self.selected6() #update

        if clear == True:
            self.console_frame_right_1_text = "","white"
            self.console_frame_right_2_text = "","white"

        def set_cutoff_date():
            input_month = set_month.get()
            if input_month != "":
                if input_month.isdigit():
                    if int(input_month) < 13 and int(input_month) > 0:
                        self.cutoff_date[1] = int(input_month)
                        max_days_in_month = Deleting.calc_days_in_month(int(self.cutoff_date[1]))
                        if int(self.cutoff_date[0]) > max_days_in_month:
                            self.cutoff_date[0] = str(max_days_in_month)
                        self.console_frame_right_1_text = "Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green"
                    else:
                        self.console_frame_right_1_text = "Měsíc: " + str(input_month) + " je mimo rozsah","red"
                else:
                    self.console_frame_right_1_text = "U nastavení měsíce jste nezadali číslo","red"

            input_day = set_day.get()
            max_days_in_month = Deleting.calc_days_in_month(int(self.cutoff_date[1]))

            if input_day != "":
                if input_day.isdigit():
                    if int(input_day) <= int(max_days_in_month) and int(input_day) > 0:
                        self.cutoff_date[0] = int(input_day)
                        self.console_frame_right_1_text = "Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green"
                    else:
                        self.console_frame_right_1_text = "Den: " + str(input_day) + " je mimo rozsah","red"
                else:
                    self.console_frame_right_1_text = "U nastavení dne jste nezadali číslo","red"

            input_year = set_year.get()
            if input_year != "":
                if input_year.isdigit():
                    if len(str(input_year)) == 2:
                        self.cutoff_date[2] = int(input_year) + 2000
                        self.console_frame_right_1_text = "Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green"
                    elif len(str(input_year)) == 4:
                        self.cutoff_date[2] = int(input_year)
                        self.console_frame_right_1_text = "Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green"
                    else:
                        self.console_frame_right_1_text = "Rok: " + str(input_year) + " je mimo rozsah","red"
                else:
                    self.console_frame_right_1_text = "U nastavení roku jste nezadali číslo","red"

            self.selected(False)

        def set_files_to_keep():
            input_files_to_keep = files_to_keep_set.get()
            if input_files_to_keep.isdigit():
                if int(input_files_to_keep) >= 0:
                    self.files_to_keep = int(input_files_to_keep)
                    self.console_frame_right_2_text = "Počet ponechaných starších souborů nastaven na: " + str(self.files_to_keep),"green"
                else:
                    self.console_frame_right_2_text = "Mimo rozsah","red"
            else:
                self.console_frame_right_2_text = "Nazadali jste číslo","red"

            self.selected(False)

        def insert_current_date():
            today = Deleting.get_current_date()
            today_split = today[1].split(".")
            i=0
            for items in today_split:
                i+=1
                self.cutoff_date[i-1]=items

            self.console_frame_right_1_text = "Bylo vloženo dnešní datum (Momentálně všechny soubory vyhodnoceny, jako starší!)","orange"

            self.selected(False)

        console_1_text, console_1_color = self.console_frame_right_1_text

        today = Deleting.get_current_date()
        row_index = 0
        label0      = customtkinter.CTkLabel(master = self.frame_right,height=20,text = "Dnešní datum: "+today[1],justify = "left",font=("Arial",16,"bold"))
        label1      = customtkinter.CTkLabel(master = self.frame_right,height=20,text = "Nastavte datum pro vyhodnocení souborů, jako starších:",justify = "left",font=("Arial",12))
        set_day     = customtkinter.CTkEntry(master = self.frame_right,width=30,height=30, placeholder_text= self.cutoff_date[0])
        sep1        = customtkinter.CTkLabel(master = self.frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_month   = customtkinter.CTkEntry(master = self.frame_right,width=30,height=30, placeholder_text= self.cutoff_date[1])
        sep2        = customtkinter.CTkLabel(master = self.frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_year    = customtkinter.CTkEntry(master = self.frame_right,width=50,height=30, placeholder_text= self.cutoff_date[2])
        button_save1 = customtkinter.CTkButton(master = self.frame_right,width=50,height=30, text = "Uložit", command = lambda: set_cutoff_date(),font=("Arial",12,"bold"))
        insert_button = customtkinter.CTkButton(master = self.frame_right,width=130,height=30, text = "Vložit dnešní datum", command = lambda: insert_current_date(),font=("Arial",12,"bold"))
        console_frame_right_1 = customtkinter.CTkLabel(master = self.frame_right,height=30,text = console_1_text,justify = "left",font=("Arial",12),text_color=console_1_color)
        label0.grid(column =0,row=row_index,sticky = tk.W,pady =0,padx=10)
        label1.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        set_day.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
        sep1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=40)
        set_month.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=50)
        sep2.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=80)
        set_year.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=90)
        button_save1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=140)
        insert_button.grid(column =0,row=row_index+3,sticky = tk.W,pady =0,padx=10)
        console_frame_right_1.grid(column =0,row=row_index+4,sticky = tk.W,pady =0,padx=10)
        def new_date_enter_btn(e):
            set_cutoff_date()
        set_day.bind("<Return>",new_date_enter_btn)
        set_month.bind("<Return>",new_date_enter_btn)
        set_year.bind("<Return>",new_date_enter_btn)
        
        console_2_text, console_2_color = self.console_frame_right_2_text
        label2          = customtkinter.CTkLabel(master = self.frame_right,height=20,text = "Nastavte počet ponechaných souborů, vyhodnocených jako starších:",justify = "left",font=("Arial",12))
        files_to_keep_set = customtkinter.CTkEntry(master = self.frame_right,width=50,height=30, placeholder_text= self.files_to_keep)
        button_save2    = customtkinter.CTkButton(master = self.frame_right,width=50,height=30, text = "Uložit", command = lambda: set_files_to_keep(),font=("Arial",12,"bold"))
        console_frame_right_2 = customtkinter.CTkLabel(master = self.frame_right,height=30,text =console_2_text,justify = "left",font=("Arial",12),text_color=console_2_color)
        label2.grid(column =0,row=5,sticky = tk.W,pady =0,padx=10)
        files_to_keep_set.grid(column =0,row=6,sticky = tk.W,pady =0,padx=10)
        button_save2.grid(column =0,row=6,sticky = tk.W,pady =0,padx=60)
        console_frame_right_2.grid(column =0,row=7,sticky = tk.W,pady =0,padx=10)
        def new_FTK_enter_btn(e):
            set_files_to_keep()
        files_to_keep_set.bind("<Return>",new_FTK_enter_btn)
          
    def selected2(self,clear:bool): # Druhá možnost mazání, mazání všech starých, redukce nových
        """
        Nastavení widgets pro druhou možnost mazání

        -Budou smazány VŠECHNY soubory starší než nastavené datum, přičemž budou redukovány i soubory novější\n
        -Souborů, vyhodnocených, jako novější, bude ponechán nastavený počet\n
        -(vhodné při situacích rychlého pořizování velkého množství fotografií, kde je potřebné ponechat nějaké soubory pro referenci)\n
        -Podporované formáty jsou uživatelem nastavené a uložené v textovém souboru
        """
        self.clear_frame(self.frame_right)
        self.console.configure(text = "")
        self.checkbox.deselect()
        self.checkbox3.deselect()
        self.info.configure(text = f"- Budou smazány VŠECHNY soubory starší než nastavené datum, přičemž budou redukovány i soubory novější\n- Souborů, vyhodnocených, jako novější, bude ponechán nastavený počet\n(vhodné při situacích rychlého pořizování velkého množství fotografií, kde je potřebné ponechat nějaké soubory pro referenci)\nPodporované formáty: {self.supported_formats_deleting}",font = ("Arial",16,"bold"),justify="left")
        self.selected6() #update

        if clear == True:
            self.console_frame_right_1_text = "","white"
            self.console_frame_right_2_text = "","white"

        def set_cutoff_date():
            input_month = set_month.get()
            if input_month != "":
                if input_month.isdigit():
                    if int(input_month) < 13 and int(input_month) > 0:
                        self.cutoff_date[1] = int(input_month)
                        max_days_in_month = Deleting.calc_days_in_month(int(self.cutoff_date[1]))
                        if int(self.cutoff_date[0]) > max_days_in_month:
                            self.cutoff_date[0] = str(max_days_in_month)
                        self.console_frame_right_1_text = "Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green"
                    else:
                        self.console_frame_right_1_text = "Měsíc: " + str(input_month) + " je mimo rozsah","red"
                else:
                    self.console_frame_right_1_text = "Nezadali jste číslo","red"

            input_day = set_day.get()
            max_days_in_month = Deleting.calc_days_in_month(int(self.cutoff_date[1]))

            if input_day != "":
                if input_day.isdigit():
                    if int(input_day) <= int(max_days_in_month) and int(input_day) > 0:
                        self.cutoff_date[0] = int(input_day)
                        self.console_frame_right_1_text = "Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green"
                    else:
                        self.console_frame_right_1_text = "Den: " + str(input_day) + " je mimo rozsah","red"
                else:
                    self.console_frame_right_1_text = "Nezadali jste číslo","red"

            input_year = set_year.get()
            if input_year != "":
                if input_year.isdigit():
                    if len(str(input_year)) == 2:
                        self.cutoff_date[2] = int(input_year) + 2000
                        self.console_frame_right_1_text = "Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green"
                    elif len(str(input_year)) == 4:
                        self.cutoff_date[2] = int(input_year)
                        self.console_frame_right_1_text = "Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green"
                    else:
                        self.console_frame_right_1_text = "Rok: " + str(input_year) + " je mimo rozsah","red"
                else:
                    self.console_frame_right_1_text = "Nezadali jste číslo","red"

                        
            self.selected2(False)

        def set_files_to_keep():
            input_files_to_keep = files_to_keep_set.get()
            if input_files_to_keep.isdigit():
                if int(input_files_to_keep) >= 0:
                    self.files_to_keep = int(input_files_to_keep)
                    self.console_frame_right_2_text = "Počet ponechaných starších souborů nastaven na: " + str(self.files_to_keep),"green"
                else:
                    self.console_frame_right_2_text = "Mimo rozsah","red"
            else:
                self.console_frame_right_2_text = "Nazadali jste číslo","red"

            self.selected2(False)

        def insert_current_date():
            today = Deleting.get_current_date()
            today_split = today[1].split(".")
            i=0
            for items in today_split:
                i+=1
                self.cutoff_date[i-1]=items

            self.console_frame_right_1_text = "Bylo vloženo dnešní datum (Momentálně všechny soubory vyhodnoceny, jako starší!)","orange"

            self.selected2(False)

        
        console_frame_right_1_text, console_frame_right_1_color = self.console_frame_right_1_text
        today = Deleting.get_current_date()
        row_index = 0
        label0      = customtkinter.CTkLabel(master = self.frame_right,height=20,text = "Dnešní datum: "+today[1],justify = "left",font=("Arial",16,"bold"))
        label1      = customtkinter.CTkLabel(master = self.frame_right,height=20,text = "Nastavte datum pro vyhodnocení souborů, jako starších:",justify = "left",font=("Arial",12))
        set_day     = customtkinter.CTkEntry(master = self.frame_right,width=30,height=30, placeholder_text= self.cutoff_date[0])
        sep1        = customtkinter.CTkLabel(master = self.frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_month   = customtkinter.CTkEntry(master = self.frame_right,width=30,height=30, placeholder_text= self.cutoff_date[1])
        sep2        = customtkinter.CTkLabel(master = self.frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_year    = customtkinter.CTkEntry(master = self.frame_right,width=50,height=30, placeholder_text= self.cutoff_date[2])
        button_save1 = customtkinter.CTkButton(master = self.frame_right,width=50,height=30, text = "Uložit", command = lambda: set_cutoff_date(),font=("Arial",12,"bold"))
        insert_button = customtkinter.CTkButton(master = self.frame_right,width=130,height=30, text = "Vložit dnešní datum", command = lambda: insert_current_date(),font=("Arial",12,"bold"))
        console_frame_right_1=customtkinter.CTkLabel(master = self.frame_right,height=30,text = console_frame_right_1_text,justify = "left",font=("Arial",12),text_color=console_frame_right_1_color)
        label0.grid(column =0,row=row_index,sticky = tk.W,pady =0,padx=10)
        label1.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        set_day.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
        sep1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=40)
        set_month.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=50)
        sep2.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=80)
        set_year.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=90)
        button_save1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=140)
        insert_button.grid(column =0,row=row_index+3,sticky = tk.W,pady =0,padx=10)
        console_frame_right_1.grid(column =0,row=row_index+4,sticky = tk.W,pady =0,padx=10)
        def new_date_enter_btn(e):
            set_cutoff_date()
        set_day.bind("<Return>",new_date_enter_btn)
        set_month.bind("<Return>",new_date_enter_btn)
        set_year.bind("<Return>",new_date_enter_btn)
        
        console_frame_right_2_text, console_frame_right_2_color = self.console_frame_right_2_text
        label2          = customtkinter.CTkLabel(master = self.frame_right,height=20,text = "Nastavte počet ponechaných novějších souborů:",justify = "left",font=("Arial",12))
        files_to_keep_set = customtkinter.CTkEntry(master = self.frame_right,width=50,height=30, placeholder_text= self.files_to_keep)
        button_save2    = customtkinter.CTkButton(master = self.frame_right,width=50,height=30, text = "Uložit", command = lambda: set_files_to_keep(),font=("Arial",12,"bold"))
        console_frame_right_2=customtkinter.CTkLabel(master = self.frame_right,height=30,text =console_frame_right_2_text,justify = "left",font=("Arial",12),text_color=console_frame_right_2_color)
        label2.grid(column =0,row=5,sticky = tk.W,pady =0,padx=10)
        files_to_keep_set.grid(column =0,row=6,sticky = tk.W,pady =0,padx=10)
        button_save2.grid(column =0,row=6,sticky = tk.W,pady =0,padx=60)
        console_frame_right_2.grid(column =0,row=7,sticky = tk.W,pady =0,padx=10)
        def new_FTK_enter_btn(e):
            set_files_to_keep()
        files_to_keep_set.bind("<Return>",new_FTK_enter_btn)
        
    def selected3(self,clear:bool): # Třetí možnost mazání, mazání datumových adresářů
        """
        Nastavení widgets pro třetí možnost mazání

        Budou smazány VŠECHNY adresáře (včetně všech subadresářů), které obsahují v názvu podporovaný formát datumu a jsou vyhodnoceny,jako starší než nastavené datum\n
        -Podporované datumové formáty jsou ["YYYYMMDD","DDMMYYYY","YYMMDD"] a podporované datumové separátory: [".","/","_"]

        """
        self.clear_frame(self.frame_right)
        self.console.configure(text = "")
        self.checkbox2.deselect()
        self.checkbox.deselect()
        self.info.configure(text = f"- Budou smazány VŠECHNY adresáře (včetně všech subadresářů), které obsahují v názvu podporovaný formát datumu a jsou vyhodnoceny,\njako starší než nastavené datum\nPodporované datumové formáty: {Deleting.supported_date_formats}\nPodporované separátory datumu: {Deleting.supported_separators}",font = ("Arial",16,"bold"),justify="left")
        self.selected6() #update

        if clear == True:
            self.console_frame_right_1_text = "","white"
            self.console_frame_right_2_text = "","white"

        def set_cutoff_date():
            input_month = set_month.get()
            if input_month != "":
                if input_month.isdigit():
                    if int(input_month) < 13 and int(input_month) > 0:
                        self.cutoff_date[1] = int(input_month)
                        max_days_in_month = Deleting.calc_days_in_month(int(self.cutoff_date[1]))
                        if int(self.cutoff_date[0]) > max_days_in_month:
                            self.cutoff_date[0] = str(max_days_in_month)
                        self.console_frame_right_1_text = "Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green"
                    else:
                        self.console_frame_right_1_text = "Měsíc: " + str(input_month) + " je mimo rozsah","red"
                else:
                    self.console_frame_right_1_text = "Nezadali jste číslo","red"

            input_day = set_day.get()
            max_days_in_month = Deleting.calc_days_in_month(int(self.cutoff_date[1]))

            if input_day != "":
                if input_day.isdigit():
                    if int(input_day) <= int(max_days_in_month) and int(input_day) > 0:
                        self.cutoff_date[0] = int(input_day)
                        self.console_frame_right_1_text = "Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green"
                    else:
                        self.console_frame_right_1_text = "Den: " + str(input_day) + " je mimo rozsah","red"
                else:
                    self.console_frame_right_1_text = "Nezadali jste číslo","red"

            input_year = set_year.get()
            if input_year != "":
                if input_year.isdigit():
                    if len(str(input_year)) == 2:
                        self.cutoff_date[2] = int(input_year) + 2000
                        self.console_frame_right_1_text = "Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green"
                    elif len(str(input_year)) == 4:
                        self.cutoff_date[2] = int(input_year)
                        self.console_frame_right_1_text = "Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green"
                    else:
                        self.console_frame_right_1_text = "Rok: " + str(input_year) + " je mimo rozsah","red"
                else:
                    self.console_frame_right_1_text = "Nezadali jste číslo","red"

                        
            self.selected3(False)

        def insert_current_date():
            today = Deleting.get_current_date()
            today_split = today[1].split(".")
            i=0
            for items in today_split:
                i+=1
                self.cutoff_date[i-1]=items

            self.console_frame_right_1_text = "Bylo vloženo dnešní datum (Momentálně všechny adresáře vyhodnoceny, jako starší!)","orange"

            self.selected3(False) #refresh

        console_frame_right_1_text, console_frame_right_1_color = self.console_frame_right_1_text
        today = Deleting.get_current_date()
        row_index = 0
        label0          = customtkinter.CTkLabel(master = self.frame_right,height=20,text = "Dnešní datum: "+today[1],justify = "left",font=("Arial",16,"bold"))
        images2         = customtkinter.CTkLabel(master = self.frame_right,text = "")
        label1          = customtkinter.CTkLabel(master = self.frame_right,height=20,text = "Nastavte datum pro vyhodnocení datumu v názvu adresářů, jako staršího:",justify = "left",font=("Arial",12))
        set_day         = customtkinter.CTkEntry(master = self.frame_right,width=30,height=30, placeholder_text= self.cutoff_date[0])
        sep1            = customtkinter.CTkLabel(master = self.frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_month       = customtkinter.CTkEntry(master = self.frame_right,width=30,height=30, placeholder_text= self.cutoff_date[1])
        sep2            = customtkinter.CTkLabel(master = self.frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_year        = customtkinter.CTkEntry(master = self.frame_right,width=50,height=30, placeholder_text= self.cutoff_date[2])
        button_save1    = customtkinter.CTkButton(master = self.frame_right,width=50,height=30, text = "Uložit", command = lambda: set_cutoff_date(),font=("Arial",12,"bold"))
        insert_button = customtkinter.CTkButton(master = self.frame_right,width=130,height=30, text = "Vložit dnešní datum", command = lambda: insert_current_date(),font=("Arial",12,"bold"))
        console_frame_right_1 = customtkinter.CTkLabel(master = self.frame_right,height=30,text = console_frame_right_1_text,justify = "left",font=("Arial",12),text_color=console_frame_right_1_color)
        directories     = customtkinter.CTkImage(Image.open("images/directories.png"),size=(240, 190))
        label0.grid(column =0,row=row_index,sticky = tk.W,pady =0,padx=10)
        images2.grid(column =0,row=row_index,sticky = tk.W,pady =10,padx=500,rowspan=5)
        label1.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        set_day.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
        sep1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=40)
        set_month.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=50)
        sep2.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=80)
        set_year.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=90)
        button_save1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=140)
        insert_button.grid(column =0,row=row_index+3,sticky = tk.W,pady =0,padx=10)
        console_frame_right_1.grid(column =0,row=row_index+4,sticky = tk.W,pady =0,padx=10)
        images2.configure(image = directories)
        def new_date_enter_btn(e):
            set_cutoff_date()
        set_day.bind("<Return>",new_date_enter_btn)
        set_month.bind("<Return>",new_date_enter_btn)
        set_year.bind("<Return>",new_date_enter_btn)

    def selected6(self): # checkbox s dotazem procházet subsložky
        """
        checkbox s dotazem procházet subsložky
        """
        if self.checkbox6.get() == 1:
            if self.checkbox3.get() == 1:
                self.info2.configure(text = "- Pro tuto možnost třídění není tato funkce podporována",font=("Arial",16,"bold"),text_color="white")
            else:
                self.info2.configure(text = "- VAROVÁNÍ: Máte spuštěné možnosti mazání obrázkových souborů i ve všech subsložkách vložené cesty (max:6 subsložek)",font=("Arial",16,"bold"),text_color="yellow")
        else:
            self.info2.configure(text = "")

    def create_deleting_option_widgets(self):  # Vytváří veškeré widgets (delete option MAIN)
        #cisteni menu widgets
        #for frames in self.list_of_menu_frames: 
        self.list_of_menu_frames[0].pack_forget()
        self.list_of_menu_frames[0].grid_forget()
        self.list_of_menu_frames[0].destroy()

        #definice ramcu
        self.frame_path_input = customtkinter.CTkFrame(master=self.root)
        self.bottom_frame2   = customtkinter.CTkScrollableFrame(master=self.root)
        self.bottom_frame1   = customtkinter.CTkFrame(master=self.root,height = 80)
        checkbox_frame  = customtkinter.CTkFrame(master=self.root,width=400)
        self.frame_right     = customtkinter.CTkScrollableFrame(master=self.root)
        self.frame_path_input.pack(pady=5,padx=5,fill="both",expand=False,side = "top")
        self.bottom_frame2.pack(pady=0,padx=5,fill="both",expand=True,side = "bottom")
        self.bottom_frame1.pack(pady=5,padx=5,fill="x",expand=False,side = "bottom")
        checkbox_frame.pack(pady=0,padx=5,fill="y",expand=False,side="left")
        self.frame_right.pack(pady=0,padx=5,fill="both",expand=True,side="right")
        
        menu_button = customtkinter.CTkButton(master = self.frame_path_input, width = 180, text = "MENU", command = lambda: self.call_menu(),font=("Arial",20,"bold"))
        self.path_set    = customtkinter.CTkEntry(master = self.frame_path_input,placeholder_text="Zadejte cestu k souborům z kamery (kde se přímo nacházejí soubory nebo datumové složky)")
        tree        = customtkinter.CTkButton(master = self.frame_path_input, width = 180,text = "EXPLORER", command = self.call_browseDirectories,font=("Arial",20,"bold"))
        menu_button.pack(pady =12,padx=10,anchor ="w",side="left")
        self.path_set.pack(pady = 12,padx =0,anchor ="w",side="left",fill="both",expand=True)
        tree.pack(pady = 12,padx =10,anchor ="w",side="left")

        self.frame_with_checkboxes = checkbox_frame
        self.checkbox  = customtkinter.CTkCheckBox(master = self.frame_with_checkboxes, text = "Mazání souborů starších než: určité datum",command = lambda: self.selected(True))
        self.checkbox2 = customtkinter.CTkCheckBox(master = self.frame_with_checkboxes, text = "Redukce novějších, mazání souborů starších než: určité datum",command = lambda: self.selected2(True))
        self.checkbox3 = customtkinter.CTkCheckBox(master = self.frame_with_checkboxes, text = "Mazání adresářů s názvem ve formátu určitého datumu",command = lambda: self.selected3(True))
        self.checkbox.pack(pady =10,padx=10,anchor ="w")
        self.checkbox2.pack(pady =10,padx=10,anchor ="w")
        self.checkbox3.pack(pady =10,padx=10,anchor ="w")

        self.checkbox6       = customtkinter.CTkCheckBox(master = self.bottom_frame1, text = "Procházet subsložky? (max:6)",command = self.selected6,font=("Arial",12,"bold"))
        self.info2           = customtkinter.CTkLabel(master = self.bottom_frame1,text = "",font=("Arial",12,"bold"))
        self.checkbox_testing = customtkinter.CTkCheckBox(master = self.bottom_frame1, text = f"Režim TESTOVÁNÍ (Soubory vyhodnocené ke smazání se pouze přesunou do složky s názvem: \"{self.to_delete_folder_name}\")",font=("Arial",12,"bold"))
        self.checkbox6.grid(column =0,row=0,sticky = tk.W,pady =5,padx=10)
        self.info2.grid(column =0,row=0,sticky = tk.W,pady =5,padx=250)
        self.checkbox_testing.grid(column =0,row=1,sticky = tk.W,pady =5,padx=10)

        self.info    = customtkinter.CTkLabel(master = self.bottom_frame2,text = "",font=("Arial",16,"bold"))
        button  = customtkinter.CTkButton(master = self.bottom_frame2, text = "SPUSTIT", command = self.start,font=("Arial",20,"bold"))
        self.console = customtkinter.CTkLabel(master = self.bottom_frame2,text = " ",justify = "left",font=("Arial",15))
        self.info.pack(pady = 12,padx =10,anchor="w")
        button.pack(pady =20,padx=10)
        button._set_dimensions(300,60)
        self.console.pack(pady =10,padx=10)

        #default:
        self.checkbox.select()
        self.checkbox_testing.select()
        self.selected(False)

        read_file_data = read_text_file_data()
        recources_path = read_file_data[2]
        if recources_path != False and recources_path != "/":
            self.path_set.delete("0","200")
            self.path_set.insert("0", str(recources_path))
            self.console.configure(text="Byla vložena cesta z konfiguračního souboru Recources.txt",text_color="white")
        else:
            self.console.configure(text="Konfigurační soubor Recources.txt obsahuje neplatnou cestu k souborům",text_color="orange")

        def maximalize_window(e):
            # netrigguj fullscreen zatimco pisu do vstupniho textovyho pole
            currently_focused = str(self.root.focus_get())
            if ".!ctkentry" in currently_focused:
                return
            if int(self.root._current_width) > 1200:
                self.root.after(0, lambda:self.root.state('normal'))
                self.root.geometry("1200x900")
            else:
                self.root.after(0, lambda:self.root.state('zoomed'))
        self.root.bind("<f>",maximalize_window)
        self.unbind_list.append("<f>")

        def unfocus_widget(e):
            #print(self.root.focus_get())
            self.root.focus_set()
        self.root.bind("<Escape>",unfocus_widget)
        self.unbind_list.append("<Escape>")
        self.path_set.bind("<Return>",unfocus_widget)

class Sorting_option: # Umožňuje nastavit možnosti třídění souborů
    """
    Umožňuje nastavit možnosti třídění souborů

    -možnosti s ukázkou očekávané syntaxe názvu souboru i s visualizací\n
    -umožňuje operace s ID daného obrázku\n
    -umožňuje hledání chybějících ID v řadě za sebou (na lince několik palet s výrobkem)
    """
    def __init__(self,root,list_of_menu_frames):
        self.root = root
        self.list_of_menu_frames = list_of_menu_frames
        self.aut_detect_num_of_pallets = True
        self.by_which_ID_num = ""   
        self.more_dirs = False
        self.unbind_list = []
        text_file_data = read_text_file_data()
        self.supported_formats_sorting = text_file_data[0]
        self.prefix_func = text_file_data[5]
        self.prefix_Cam = text_file_data[6]
        self.max_num_of_pallets = text_file_data[8]
        list_of_folder_names = text_file_data[9]
        self.nok_folder_name = list_of_folder_names[0]
        self.pairs_folder_name = list_of_folder_names[1]
        self.create_sorting_option_widgets()
    
    def start(self):# Ověřování cesty, init, spuštění
        """
        Ověřování cesty, init, spuštění
        """
        if self.checkbox.get()+self.checkbox2.get()+self.checkbox3.get()+self.checkbox4.get()+self.checkbox5.get() == 0:
            self.console.configure(text = "Nevybrali jste žádný způsob třídění :-)",text_color="red")
            nothing = customtkinter.CTkImage(Image.open("images/nothing.png"),size=(1, 1))
            self.images.configure(image = nothing)
            self.name_example.configure(text = "")

        else:
            path = self.path_set.get() 
            if path != "":
                check = path_check(path)
                if check == False:
                    self.console.configure(text = "Zadaná cesta: "+str(path)+" nebyla nalezena",text_color="red")
                else:
                    path = check
                    self.console.configure(text ="Provádím nastavenou možnost třídění v cestě: "+str(path),text_color="white")
                    self.console.update_idletasks()
                    self.root.update_idletasks()
                    self.sort_files(path)
            else:
                self.console.configure(text = "Nebyla vložena cesta k souborům",text_color="red")

    def sort_files(self,path): # Volání externího scriptu
        selected_sort = 0
        if self.checkbox.get() == 1:
            selected_sort = 1
        if self.checkbox2.get() == 1:
            selected_sort = 2
        if self.checkbox3.get() == 1:
            selected_sort = 3
        if self.checkbox4.get() == 1:
            selected_sort = 4
        if self.checkbox5.get() == 1:
            selected_sort = 5
        if self.checkbox6.get() == 1:
            self.more_dirs = True
        else:
            self.more_dirs = False
        Trideni.output = []
        Trideni.output_console2 = []

        Trideni.whole_sorting_function(path,selected_sort,self.more_dirs,self.max_num_of_pallets,self.by_which_ID_num,
                                       self.prefix_func,self.prefix_Cam,self.supported_formats_sorting,self.aut_detect_num_of_pallets,
                                       self.nok_folder_name,self.pairs_folder_name)
        output_text = ""
        output_text2 = ""
        for i in range(0,len(Trideni.output)):
            if len(Trideni.output[i]) > 170: # kdyz by se vypis nevesel na obrazovku
                Trideni.output[i] = split_text_to_rows(Trideni.output[i],170)
            output_text = output_text + Trideni.output[i] + "\n"
        if "bylo dokončeno" in output_text or "byla dokončena" in output_text:
            self.console.configure(text = output_text,text_color="green")
        else:
            self.console.configure(text = output_text,text_color="red")

        for i in range(0,len(Trideni.output_console2)):
            output_text2 = output_text2 + Trideni.output_console2[i] + "\n"
        if output_text2 != "":
            if "Chyba" in output_text2:
                self.console2.configure(text = output_text2,text_color="red")
            else:
                self.console2.configure(text = output_text2,text_color="green")
        self.console2.update_idletasks()

    def clear_frame(self,frame): # mazání widgets v daném framu
        for widget in frame.winfo_children():
            widget.destroy()

    def selected(self): #Třídit podle typu souboru
        """
        Nastavení widgets pro třídění podle typu souboru (základní)
        """
        self.clear_frame(self.frame6)
        self.view_image(1)
        self.console.configure(text = "")
        self.checkbox2.deselect()
        self.checkbox3.deselect()
        self.checkbox4.deselect()
        self.checkbox5.deselect()

        labelx = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=self.height_of_frame6+10,text = "",justify = "left",font=("Arial",12))
        labelx.grid(column =0,row=0,pady =0,padx=10)
        
    def selected2(self): #Třídit podle čísla funkce (ID)
        """
        Nastavení widgets pro třídění podle čísla funkce
        """
        self.clear_frame(self.frame6)
        self.view_image(2)
        self.console.configure(text = "")
        self.checkbox.deselect()
        self.checkbox3.deselect()
        self.checkbox4.deselect()
        self.checkbox5.deselect()

        def set_prefix():
            input_1 = str(prefix_set.get()).replace(" ","")
            if len(input_1) != 0:
                if input_1 != self.prefix_Cam:
                    console_frame6_1.configure(text = f"Prefix nastaven na: {input_1}",text_color="green")
                    self.prefix_func = input_1
                    prefix_set.delete("0","100")
                    prefix_set.insert("0", input_1)
                else:
                    console_frame6_1.configure(text = "Jméno zabrané pro třídění podle kamer",text_color="red")
            else:
                console_frame6_1.configure(text = "Nutný alespoň jeden znak",text_color="red")

        label1          = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=20,text = "Nastavte prefix adresářů:",justify = "left",font=("Arial",12))
        prefix_set      = customtkinter.CTkEntry(master = self.frame6,width=150,height=30, placeholder_text= self.prefix_func)
        button_save1    = customtkinter.CTkButton(master = self.frame6,width=50,height=30, text = "Uložit", command = lambda: set_prefix(),font=("Arial",12,"bold"))
        console_frame6_1 = customtkinter.CTkLabel(master = self.frame6,height=30,text = " ",justify = "left",font=("Arial",12))
        label1.grid(column =0,row=0,pady =0,padx=10)
        prefix_set.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)
        button_save1.grid(column =0,row=1,sticky = tk.E,pady =0,padx=10)
        console_frame6_1.grid(column =0,row=2,pady =0,padx=10)
        prefix_set.insert("0", str(self.prefix_func))
        def prefix_enter_btn(e):
            set_prefix()
        prefix_set.bind("<Return>",prefix_enter_btn)

        labelx          = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=30,text = "",justify = "left",font=("Arial",12))
        checkbox_advance = customtkinter.CTkCheckBox(master = self.frame6,height=30, text = "Pokročilá nastavení",command = self.selected2_advance)
        labelxx         = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=120,text = "",justify = "left",font=("Arial",12))
        labelx.grid(column =0,row=3,pady =0,padx=10)
        checkbox_advance.grid(column =0,row=4,pady =0,padx=10)
        labelxx.grid(column =0,row=5,pady =0,padx=10)

    def selected2_advance(self): # Třídit podle určitého čísla v ID
        """
        Nastavení widgets pro třídění podle určitého čísla v ID
        """
        self.clear_frame(self.frame6)

        def set_which_num_of_ID():
            input3=num_set.get()
            if input3.isdigit():
                if int(input3) > 0:
                    self.by_which_ID_num = int(input3)
                    console_frame6_1.configure(text = f"Řídit podle {self.by_which_ID_num}. čísla v ID",text_color="white")
                else:
                    console_frame6_1.configure(text = "Mimo rozsah",text_color="red")
                    self.by_which_ID_num = ""
            else:
                console_frame6_1.configure(text = "Nezadali jste číslo",text_color="red")
                self.by_which_ID_num = ""

        label1           = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=60,
                                        text = "Podle kterého čísla v ID se řídit:\n(např. poslední č. v ID = pozice dílu...)\nvolte první = 1 atd. (prázdné = celé ID)",
                                        justify = "left",font=("Arial",12))
        num_set          = customtkinter.CTkEntry(master = self.frame6,height=30,width=150, placeholder_text= self.by_which_ID_num)
        button_save1     = customtkinter.CTkButton(master = self.frame6,height=30,width=50, text = "Uložit", command = lambda: set_which_num_of_ID(),font=("Arial",12,"bold"))
        console_frame6_1 = customtkinter.CTkLabel(master = self.frame6,height=30,text = " ",justify = "left",font=("Arial",12))
        labelx2          = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=30,text = "",justify = "left",font=("Arial",12))
        button_back      = customtkinter.CTkButton(master = self.frame6,width=100,height=30, text = "Zpět", command = self.selected2,font=("Arial",12,"bold"))
        labelx3          = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=80,text = "",justify = "left",font=("Arial",12))
        label1.grid(column =0,row=0,pady =0,padx=10)
        num_set.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)
        button_save1.grid(column =0,row=1,sticky = tk.E,pady =0,padx=10)
        console_frame6_1.grid(column =0,row=2,pady =0,padx=10)  
        labelx2.grid(column =0,row=3,pady =0,padx=10)
        button_back.grid(column =0,row=5,pady =0,padx=10)
        labelx3.grid(column =0,row=6,pady =0,padx=10)
        def which_id_num_enter_btn(e):
            set_which_num_of_ID()
        num_set.bind("<Return>",which_id_num_enter_btn)
        
    def selected3(self): #Třídit podle čísla kamery
        """
        Nastavení widgets pro třídění podle čísla kamery
        """
        self.clear_frame(self.frame6)
        self.console.configure(text = "")
        self.view_image(3)   
        self.checkbox.deselect()
        self.checkbox2.deselect()
        self.checkbox4.deselect()
        self.checkbox5.deselect()

        def set_prefix():
            input_1 = str(prefix_set.get()).replace(" ","")
            if len(input_1) != 0:
                if input_1 != self.prefix_func:
                    console_frame6_1.configure(text = f"Prefix nastaven na: {input_1}",text_color="green")
                    self.prefix_Cam = input_1
                    prefix_set.delete("0","100")
                    prefix_set.insert("0", input_1)
                else:
                    console_frame6_1.configure(text = "Jméno zabrané pro třídění podle funkce",text_color="red")
            else:
                console_frame6_1.configure(text = "Nutný alespoň jeden znak",text_color="red")

        label1       = customtkinter.CTkLabel(master = self.frame6,height=20,width=self.width_of_frame6,text = "Nastavte prefix adresářů:",justify = "left",font=("Arial",12))
        prefix_set   = customtkinter.CTkEntry(master = self.frame6,height=30,width=150, placeholder_text= self.prefix_Cam)
        button_save1 = customtkinter.CTkButton(master = self.frame6,height=30,width=50, text = "Uložit", command = lambda: set_prefix(),font=("Arial",12,"bold"))
        console_frame6_1 = customtkinter.CTkLabel(master = self.frame6,height=30,text = " ",justify = "left",font=("Arial",12))
        labelx       = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=180,text = "",justify = "left",font=("Arial",12))
        label1.grid(column =0,row=0,pady =0,padx=10)
        prefix_set.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)
        button_save1.grid(column =0,row=1,sticky = tk.E,pady =0,padx=10)
        console_frame6_1.grid(column =0,row=2,pady =0,padx=10)
        labelx.grid(column =0,row=3,pady =0,padx=10)
        prefix_set.insert("0", str(self.prefix_Cam))
        def prefix_enter_btn(e):
            set_prefix()
        prefix_set.bind("<Return>",prefix_enter_btn)
        
    def selected4(self): #Třídit podle obojího (funkce, kamery)
        """
        Nastavení widgets pro třídění podle funkce i čísla kamery
        """
        self.clear_frame(self.frame6)
        self.console.configure(text = "")
        self.view_image(4)
        self.checkbox.deselect()
        self.checkbox2.deselect()
        self.checkbox3.deselect()
        self.checkbox5.deselect()

        labelx = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=self.height_of_frame6+10,text = "",justify = "left",font=("Arial",12))
        labelx.grid(column =0,row=0,pady =0,padx=10)
        
    def selected5(self): #hledani paru
        """
        Nastavení widgets pro hledání dvakrát vyfocených výrobků za sebou se stejným ID

        - nalezené dvojice nakopíruje do složky
        """
        self.clear_frame(self.frame6)
        self.console.configure(text = "")
        self.view_image(5)
        self.checkbox.deselect()
        self.checkbox2.deselect()
        self.checkbox3.deselect()
        self.checkbox4.deselect()
        
        def set_max_pallet_num():
            input_1 = pallets_set.get()
            if input_1.isdigit() == False:
                console_frame6_1.configure(text = "Nezadali jste číslo",text_color="red")
            elif int(input_1) <1:
                console_frame6_1.configure(text = "Mimo rozsah",text_color="red")
            else:
                console_frame6_1.configure(text = f"Počet palet nastaven na: {input_1}",text_color="white")
                self.max_num_of_pallets = input_1
                
        def set_aut_detect():
            if checkbox_aut_detect.get() == 1:
                self.aut_detect_num_of_pallets = True
            else:
                self.aut_detect_num_of_pallets = False

        label1              = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=20,text = "Nastavte počet palet v oběhu:",justify = "left",font=("Arial",12))
        pallets_set         = customtkinter.CTkEntry(master = self.frame6,width=150,height=30, placeholder_text= self.max_num_of_pallets)
        button_save1        = customtkinter.CTkButton(master = self.frame6,width=50,height=30, text = "Uložit", command = lambda: set_max_pallet_num(),font=("Arial",12,"bold"))
        label_aut_detect    = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=60,text = "Možnost aut. detekce:\n(případ, že v cestě nechybí paleta\ns nejvyšším ID)",justify = "left",font=("Arial",12))
        checkbox_aut_detect = customtkinter.CTkCheckBox(master = self.frame6,height=30, text = "Automatická detekce",command=set_aut_detect)
        console_frame6_1    = customtkinter.CTkLabel(master = self.frame6,height=30,text = " ",justify = "left",font=("Arial",12))
        labelx              = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=90,text = "",justify = "left",font=("Arial",12))
        label1.grid(column =0,row=0,pady =0,padx=10)
        pallets_set.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)
        button_save1.grid(column =0,row=1,sticky = tk.E,pady =0,padx=10)
        console_frame6_1.grid(column =0,row=2,pady =0,padx=10)
        label_aut_detect.grid(column =0,row=3,pady =0,padx=10)
        checkbox_aut_detect.grid(column =0,row=4,pady =0,padx=10)
        labelx.grid(column =0,row=5,pady =0,padx=10)
        checkbox_aut_detect.select()

        def max_pallets_num_enter_btn(e):
            set_max_pallet_num()
        pallets_set.bind("<Return>",max_pallets_num_enter_btn)

    def selected6(self): # checkbox na přepínání: procházet/ neprocházet subsložky
        if self.checkbox6.get() == 1:
            dirs_more = customtkinter.CTkImage(Image.open("images/more_dirs.png"),size=(553, 111))
            self.images2.configure(image =dirs_more)   
            self.console2.configure(text = "Zadaná cesta/ 1.složka/ 2.složka/ složky se soubory\nnebo: Zadaná cesta/ 1.složka/ 2.složka/ soubory volně, neroztříděné",font=("Arial",14,"bold"),text_color="white")
        else:
            dirs_one = customtkinter.CTkImage(Image.open("images/dirs_ba.png"),size=(432, 133))
            self.images2.configure(image =dirs_one)
            self.console2.configure(text = "Zadaná cesta/ složky se soubory\nnebo: Zadaná cesta/ soubory volně, neroztříděné",font=("Arial",14,"bold"),text_color="white")

    def view_image(self,which_one): # zobrazení ilustračního obrázku
        """
        zobrazení ilustračního obrázku
        """
        if self.checkbox.get()+self.checkbox2.get()+self.checkbox3.get()+self.checkbox4.get()+self.checkbox5.get() == 0:
            nothing = customtkinter.CTkImage(Image.open("images/nothing.png"),size=(1, 1))
            self.images.configure(image = nothing)
            self.name_example.configure(text = "")
        else:
            if which_one == 1:
                type_24 = customtkinter.CTkImage(Image.open("images/24_type.png"),size=(447, 170))
                self.images.configure(image =type_24)
                self.name_example.configure(text = f"221013_092241_0000000842_21_&Cam1Img  => .Height <=  .bmp\n(Podporované formáty:{self.supported_formats_sorting})")
            if which_one == 2:
                func_24 = customtkinter.CTkImage(Image.open("images/24_func.png"),size=(725, 170))
                self.images.configure(image =func_24)
                self.name_example.configure(text = f"221013_092241_0000000842_  => 21 <=  _&Cam1Img.Height.bmp\n(Podporované formáty:{self.supported_formats_sorting})")
            if which_one == 3:
                cam_24 = customtkinter.CTkImage(Image.open("images/24_cam.png"),size=(874, 170))
                self.images.configure(image =cam_24)
                self.name_example.configure(text = f"221013_092241_0000000842_21_&  => Cam1 <=  Img.Height.bmp\n(Podporované formáty:{self.supported_formats_sorting})")
            if which_one == 4:
                both_24 = customtkinter.CTkImage(Image.open("images/24_both.png"),size=(900, 170))
                self.images.configure(image =both_24)
                self.name_example.configure(text = f"221013_092241_0000000842_  => 21 <=  _&  => Cam1 <=  Img.Height.bmp\n(Podporované formáty:{self.supported_formats_sorting})")
            if which_one == 5:
                PAIRS = customtkinter.CTkImage(Image.open("images/25basic.png"),size=(530, 170))
                self.images.configure(image =PAIRS)
                self.name_example.configure(
                    text = f"Nakopíruje nalezené dvojice souborů do složky s názvem PAIRS\n(např. obsluha vloží dvakrát stejnou paletu po sobě před kameru)\n2023_04_13-07_11_09_xxxx_=> 0020 <=_&Cam2Img.Height.bmp\n(funkce postupuje podle časové známky v názvu souboru, kdy byly soubory pořízeny)\n(Podporované formáty:{self.supported_formats_sorting})")
    
    def call_menu(self): # Tlačítko menu (konec, návrat do menu)
        """
        Funkce čistí všechny zaplněné rámečky a funguje, jako tlačítko zpět do menu
        """
        list_of_frames = [self.frame2,self.frame3,self.frame4,self.frame5,self.frame6,self.list_of_menu_frames[1]]
        for frames in list_of_frames:
            frames.pack_forget()
            frames.grid_forget()
            frames.destroy()
        
        for binds in self.unbind_list:
            self.root.unbind(binds)

        #self.path_set.unbind("<Return>")
        menu()
    
    def call_browseDirectories(self): # Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
        """
        Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
        """
        if self.checkbox6.get() == 1: # pokud je zvoleno more_dirs v exploreru pouze slozky...
            output = browseDirectories("only_dirs")
        else:
            output = browseDirectories("all")
        if str(output[1]) != "/":
            self.path_set.delete("0","200")
            self.path_set.insert("0", output[1])
            self.console.configure(text=f"Byla vložena cesta: {output[1]}",text_color="green")
        else:
            self.console.configure(text = str(output[0]),text_color="red")

    def create_sorting_option_widgets(self):  # Vytváří veškeré widgets (sorting option MAIN)
        # cisteni menu widgets:
        self.list_of_menu_frames[0].pack_forget()
        self.list_of_menu_frames[0].grid_forget()
        self.list_of_menu_frames[0].destroy()
        # nastaveni framu
        self.frame2 = customtkinter.CTkFrame(master=self.root)
        self.frame5 = customtkinter.CTkScrollableFrame(master=self.root)
        self.frame3 = customtkinter.CTkFrame(master=self.root,width=400)
        self.frame4 = customtkinter.CTkScrollableFrame(master=self.root)
        self.frame2.pack(pady=0,padx=5,fill="both",expand=False,side = "top")
        self.frame5.pack(pady=0,padx=5,fill="both",expand=True,side = "bottom")
        self.frame3.pack(pady=10,padx=5,fill="y",expand=False,side="left")
        self.frame4.pack(pady=10,padx=5,fill="both",expand=True,side="right")

        self.height_of_frame6 = 250
        self.width_of_frame6 = 200
        self.frame6 = customtkinter.CTkFrame(master=self.root,height=self.height_of_frame6,width = self.width_of_frame6)
        self.frame6.pack(pady=10,padx=0,fill="both",expand=False,side = "bottom")

        menu_button = customtkinter.CTkButton(master = self.frame2, width = 180, text = "MENU", command = lambda: self.call_menu(),font=("Arial",20,"bold"))
        self.path_set    = customtkinter.CTkEntry(master = self.frame2,placeholder_text="Zadejte cestu k souborům z kamery (kde se nacházejí složky se soubory nebo soubory přímo)")
        tree        = customtkinter.CTkButton(master = self.frame2, width = 180,text = "EXPLORER", command = self.call_browseDirectories,font=("Arial",20,"bold"))
        menu_button.pack(pady =5,padx=10,anchor ="w",side="left")
        self.path_set.pack(pady = 5,padx =0,anchor ="w",side="left",fill="both",expand=True)
        tree.pack(pady = 5,padx =10,anchor ="w",side="left")

        self.checkbox    = customtkinter.CTkCheckBox(master = self.frame3, text = "Třídit podle typů souborů",command = self.selected)
        self.checkbox2   = customtkinter.CTkCheckBox(master = self.frame3, text = "Třídit podle čísla funkce (ID)",command = self.selected2)
        self.checkbox3   = customtkinter.CTkCheckBox(master = self.frame3, text = "Třídit podle čísla kamery",command = self.selected3)
        self.checkbox4   = customtkinter.CTkCheckBox(master = self.frame3, text = "Třídit podle čísla funkce i kamery",command = self.selected4)
        self.checkbox5   = customtkinter.CTkCheckBox(master = self.frame3, text = "Najít dvojice (soubory se stejným ID, v řadě za sebou)",command = self.selected5)
        self.checkbox.pack(pady =12,padx=10,anchor ="w")
        self.checkbox2.pack(pady =12,padx=10,anchor ="w")
        self.checkbox3.pack(pady =12,padx=10,anchor ="w")
        self.checkbox4.pack(pady =12,padx=10,anchor ="w")
        self.checkbox5.pack(pady =12,padx=10,anchor ="w")

        self.checkbox6   = customtkinter.CTkCheckBox(master = self.frame4, text = "Projít subsložky?",command = self.selected6)
        self.images2     = customtkinter.CTkLabel(master = self.frame4,text = "")
        self.console2    = customtkinter.CTkLabel(master = self.frame4,text = " ",font=("Arial",12))
        self.checkbox6.pack(pady =12,padx=10,anchor="w")
        self.images2.pack()
        self.console2.pack(pady =5,padx=10)

        self.images       = customtkinter.CTkLabel(master = self.frame5,text = "")
        self.name_example = customtkinter.CTkLabel(master = self.frame5,text = "",font=("Arial",16,"bold"))
        button            = customtkinter.CTkButton(master = self.frame5, text = "SPUSTIT", command = self.start,font=("Arial",20,"bold"))
        self.console      = customtkinter.CTkLabel(master = self.frame5,text = " ",justify = "left",font=("Arial",15))
        self.images.pack()
        self.name_example.pack(pady = 12,padx =10)
        button.pack(pady =12,padx=10)
        button._set_dimensions(300,60)
        self.console.pack(pady =10,padx=10)

        #default nastaveni:
        self.checkbox.select()
        self.selected()
        self.view_image(1)
        self.selected6()
        #predvyplneni cesty pokud je platna v configu
        read_file_data = read_text_file_data()
        recources_path = read_file_data[2]
        if recources_path != False and recources_path != "/":
            self.path_set.delete("0","200")
            self.path_set.insert("0", str(recources_path))
            self.console.configure(text="Byla vložena cesta z konfiguračního souboru Recources.txt",text_color="white")
        else:
            self.console.configure(text="Konfigurační soubor Recources.txt obsahuje neplatnou cestu k souborům",text_color="orange")

        def maximalize_window(e):
            # netrigguj fullscreen zatimco pisu do vstupniho textovyho pole
            currently_focused = str(self.root.focus_get())
            if ".!ctkentry" in currently_focused:
                return
            if int(self.root._current_width) > 1200:
                self.root.after(0, lambda:self.root.state('normal'))
                self.root.geometry("1200x900")
            else:
                self.root.after(0, lambda:self.root.state('zoomed'))
        self.root.bind("<f>",maximalize_window)

        def unfocus_widget(e):
            #print(self.root.focus_get())
            self.root.focus_set()
        self.root.bind("<Escape>",unfocus_widget)
        self.unbind_list.append("<Escape>")
        self.path_set.bind("<Return>",unfocus_widget)
menu()

