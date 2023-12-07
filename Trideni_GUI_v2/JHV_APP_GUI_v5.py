import customtkinter
import os
import re
from PIL import Image, ImageTk
import Sorting_option_v4 as Trideni
import Deleting_option_v1 as Deleting
import Converting_option_v1 as Converting
from tkinter import filedialog
import tkinter as tk

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root=customtkinter.CTk()
root.geometry("1200x900")
root.wm_iconbitmap('images/JHV.ico')
root.title("Zpracování souborů z průmyslových kamer")
logo_set = False

def read_text_file_data():
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

        path_repaired = Trideni.path_check(inserted_path)

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

        return [supported_formats_sorting,supported_formats_deleting,path_repaired,files_to_keep,cutoff_date,prefix_function,prefix_camera,maximalized,max_pallets]
    else:
        print("Chybí konfigurační soubor Recources.txt")
        return [False,False,False,False,False]

data_read_in_txt = read_text_file_data()
if data_read_in_txt[7] == "ano":
    #root.attributes('-fullscreen', True) #fullscreen bez windows tltacitek
    root.after(0, lambda:root.state('zoomed'))

def write_text_file_data(input_data,which_parameter):
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
    8 new_default_prefix_cam\n
    9 new_default_prefix_func\n
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
        
        if which_parameter == "add_supported_deleting_formats":
            corrected_input = str(input_data)
            for items in unwanted_chars:
                corrected_input = corrected_input.replace(items,"")
            if str(corrected_input) not in supported_formats_deleting:
                supported_formats_deleting.append(str(corrected_input))
                report =  (f"Byl přidán formát: \"{corrected_input}\" do podporovaných formátů pro možnosti mazání")
            else:
                report =  (f"Formát: \"{corrected_input}\" je již součástí podporovaných formátů možností mazání")
            
        if which_parameter == "pop_supported_sorting_formats":
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
            
        if which_parameter == "pop_supported_deleting_formats":
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
        
        if which_parameter == "default_path":
            lines[6] = lines[6].replace("\n","")
            lines[6] = str(input_data)+"\n"
            report = (f"Základní cesta přenastavena na: {str(input_data)}")
        
        if which_parameter == "default_files_to_keep":
            lines[8] = lines[8].replace("\n","")
            lines[8] = str(input_data)+"\n"
        
        if which_parameter == "default_cutoff_date":
            lines[10] = lines[10].replace("\n","")
            lines[10] = str(input_data[0])+"."+str(input_data[1])+"."+str(input_data[2])+"\n"

        if which_parameter == "new_default_prefix_cam":
            lines[12] = lines[12].replace("\n","")
            lines[12] = lines[12].replace("\"","")
            lines[12] = lines[12].replace("/","")
            lines[12] = str(input_data)+"\n"
            report = (f"Základní název složek pro třídění podle kamery přenastaven na: {str(input_data)}")

        if which_parameter == "new_default_prefix_func":
            lines[14] = lines[14].replace("\n","")
            lines[14] = lines[14].replace("\"","")
            lines[14] = lines[14].replace("/","")
            lines[14] = str(input_data)+"\n"
            report = (f"Základní název složek pro třídění podle funkce přenastaven na: {str(input_data)}")

        if which_parameter == "maximalized":
            lines[16] = str(input_data) + "\n"

        if which_parameter == "pallets_set":
            lines[18] = str(input_data) + "\n"

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
def browseDirectories():
    """
    Funkce spouští průzkumníka systému windows pro definování cesty, kde má program pracovat

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

    if(start_path != ""):
        foldername_path = filedialog.askdirectory(initialdir = start_path,
                                            title = "Select a Directory",
                                            )
    else:
        foldername_path = filedialog.askdirectory(initialdir = "/",
                                            title = "Select a Directory",
                                            )

    check = Trideni.path_check(foldername_path)
    corrected_path = check
    
    return [output,corrected_path]

def menu():
    """
    Funkce spouští základní menu při spuštění aplikace
    """
    global logo_set

    if logo_set == False:
        frame_with_logo = customtkinter.CTkFrame(master=root)
        frame_with_logo.pack(pady=10,padx=5,fill="both",expand=False,side = "top")
        #logo = customtkinter.CTkImage(Image.open("images/logo2.bmp"),size=(571, 70))
        logo = customtkinter.CTkImage(Image.open("images/logo.png"),size=(961, 125))
        image_logo = customtkinter.CTkLabel(master = frame_with_logo,text = "",image =logo)
        image_logo.pack()
        logo_set = True

    frame_with_buttons = customtkinter.CTkFrame(master=root)
    frame_with_buttons.pack(pady=0,padx=5,fill="both",expand=True,side = "top")
    list_of_menu_frames = [frame_with_buttons]

    labelx = customtkinter.CTkLabel(master = frame_with_buttons,width=400,height=90,text = "",justify = "left") #jen vyplni volny prostor
    labelx.grid(column =0,row=0,pady =0,padx=0)

    sorting_button = customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Možnosti třídění souborů", command = lambda: Sorting_option(list_of_menu_frames),font=("Arial",25,"bold"))
    sorting_button.grid(column =1,row=2,pady =20,padx=0)
    deleting_button = customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Možnosti mazání souborů", command = lambda: Deleting_option(list_of_menu_frames),font=("Arial",25,"bold"))
    deleting_button.grid(column =1,row=3,pady =0,padx=0)
    convert_button = customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Možnosti konvertování souborů", command = lambda: Converting_option(list_of_menu_frames),font=("Arial",25,"bold"))
    convert_button.grid(column =1,row=4,pady =20,padx=0)
    advanced_button = customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Pokročilé možnosti", command = lambda: Advanced_option(list_of_menu_frames),font=("Arial",25,"bold"))
    advanced_button.grid(column =1,row=5,pady =0,padx=0)

    root.mainloop()

def Advanced_option(list_of_menu_frames):
    """
    Funkce umožňuje nastavit základní parametry, které ukládá do textového souboru
    """
    #cisteni menu widgets
    for frames in list_of_menu_frames: 
        frames.pack_forget()
        frames.grid_forget()
        frames.destroy()
    #cisteni pred vstupem do menu
    def call_menu():
        """
        Funkce čistí všechny zaplněné rámečky a funguje, jako tlačítko zpět do menu
        """
        list_of_frames = [top_frame,bottom_frame_default_path,bottom_frame_with_date,bottom_frame_with_files_to_keep,bottom_frame_sorting_formats,bottom_frame_deleting_formats,main_console_frame]
        for frames in list_of_frames:
            frames.pack_forget()
            frames.grid_forget()
            frames.destroy()
        menu()

    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

    main_console_frame = customtkinter.CTkFrame(master=root)
    main_console_frame.pack(pady=5,padx=5,fill="both",expand=True,side = "bottom")
    bottom_frame_deleting_formats = customtkinter.CTkFrame(master=root,height = 200)
    bottom_frame_deleting_formats.pack(pady=5,padx=5,fill="x",expand=False,side = "bottom")
    bottom_frame_sorting_formats = customtkinter.CTkFrame(master=root,height = 200)
    bottom_frame_sorting_formats.pack(pady=5,padx=5,fill="x",expand=False,side = "bottom")
    bottom_frame_with_files_to_keep = customtkinter.CTkFrame(master=root,height = 200)
    bottom_frame_with_files_to_keep.pack(pady=5,padx=5,fill="x",expand=False,side = "bottom")
    bottom_frame_with_date = customtkinter.CTkFrame(master=root,height = 200)
    bottom_frame_with_date.pack(pady=5,padx=5,fill="x",expand=False,side = "bottom")
    bottom_frame_default_path = customtkinter.CTkFrame(master=root,height = 200)
    bottom_frame_default_path.pack(pady=5,padx=5,fill="x",expand=False,side = "bottom")
    top_frame = customtkinter.CTkFrame(master=root,height = 200)
    top_frame.pack(pady=5,padx=5,fill="x",expand=False,side = "bottom")

    def maximalized():
        option = checkbox_maximalized.get()
        if option == 1:
            write_text_file_data("ano","maximalized")
        else:
            write_text_file_data("ne","maximalized")

    label0 = customtkinter.CTkLabel(master = top_frame,height=20,text = "Nastavte požadované parametry (nastavení bude uloženo i po vypnutí aplikace): ",justify = "left",font=("Arial",16,"bold"))
    label0.grid(column =0,row=0,sticky = tk.W,pady =0,padx=10)
    menu_button = customtkinter.CTkButton(master = top_frame, width = 180, text = "MENU", command = lambda: call_menu(),font=("Arial",20,"bold"))
    menu_button.grid(column =0,row=0,sticky = tk.W,pady =0,padx=1000)
    checkbox_maximalized = customtkinter.CTkCheckBox(master = top_frame, text = "Spouštět v maximalizovaném okně",command = lambda: maximalized())
    checkbox_maximalized.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)
    
    if read_text_file_data()[7] == "ano":
        checkbox_maximalized.select()
    else:
        checkbox_maximalized.deselect()

    def setting_widgets(main_console_text,exception):
        clear_frame(bottom_frame_with_date)
        clear_frame(bottom_frame_with_files_to_keep)
        clear_frame(bottom_frame_sorting_formats)
        clear_frame(bottom_frame_deleting_formats)
        clear_frame(main_console_frame)
        clear_frame(bottom_frame_default_path)

        text_file_data = read_text_file_data()
        if exception == False:
            cutoff_date = text_file_data[4]
        else:
            cutoff_date = exception

        files_to_keep = text_file_data[3]
        default_prefix_cam =text_file_data[5]
        default_prefix_func=text_file_data[6]
        default_max_num_of_pallets=text_file_data[8]

        def call_browseDirectories():
            output = browseDirectories()
            
            if str(output[1]) != "/":
                path_set.delete("0","200")
                path_set.insert("0", output[1])
                console_input = write_text_file_data(output[1],"default_path") # hlaska o nove vlozene ceste
                default_path_insert_console.configure(text = "")
                default_path_insert_console.configure(text = "Aktuálně nastavená základní cesta k souborům: " + str(output[1]))
                main_console.configure(text="")
                main_console.configure(text=console_input)

        def save_path():
            path_given = str(path_set.get())
            path_check = Trideni.path_check(path_given)
            main_console.configure(text="")
            if path_check != False and path_check != "/":
                console_input = write_text_file_data(path_check,"default_path")
                main_console.configure(text=console_input)
                default_path_insert_console.configure(text = "")
                default_path_insert_console.configure(text = "Aktuálně nastavená základní cesta k souborům: " + str(path_check))
            elif path_check != "/":
                main_console.configure(text=f"Zadaná cesta: {path_given} nebyla nalezena, nebude tedy uložena")
        
        row_index = 0
        if text_file_data[2] != False:
            default_path_old = "Aktuálně nastavená základní cesta k souborům: " + str(text_file_data[2])
            placeholder_path = str(text_file_data[2])
        else:
            default_path_old = "Aktuálně nastavená základní cesta k souborům v Recources.txt je neplatná"
            placeholder_path = ""
        label5 = customtkinter.CTkLabel(master = bottom_frame_default_path,height=20,text = "Nastavte základní cestu k souborům při spuštění:",justify = "left",font=("Arial",12,"bold"))
        path_set = customtkinter.CTkEntry(master = bottom_frame_default_path,width=700,height=30,placeholder_text=placeholder_path)
        button_save5 = customtkinter.CTkButton(master = bottom_frame_default_path,width=50,height=30, text = "Uložit", command = lambda: save_path(),font=("Arial",12,"bold"))
        button_explorer = customtkinter.CTkButton(master = bottom_frame_default_path,width=100,height=30, text = "EXPLORER", command = lambda: call_browseDirectories(),font=("Arial",12,"bold"))
        default_path_insert_console=customtkinter.CTkLabel(master = bottom_frame_default_path,height=30,text =default_path_old,justify = "left",font=("Arial",12))
        label5.grid(column =0,row=row_index,sticky = tk.W,pady =0,padx=10)
        path_set.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        button_save5.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=710)
        button_explorer.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=760)
        default_path_insert_console.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)

        def set_default_cutoff_date():
            main_console_text = ""
            input_month = set_month.get()
            if input_month != "":
                if input_month.isdigit():
                    if int(input_month) < 13 and int(input_month) > 0:
                        cutoff_date[1] = int(input_month)
                        main_console.configure(text="")
                        main_console_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        main_console.configure(text="")
                        main_console_text = "Měsíc: " + str(input_month) + " je mimo rozsah"
                else:
                    main_console.configure(text="")
                    main_console_text = "U nastavení měsíce jste nezadali číslo"

            input_day = set_day.get()
            max_days_in_month = Deleting.calc_days_in_month(int(cutoff_date[1]))

            if input_day != "":
                if input_day.isdigit():
                    if int(input_day) <= int(max_days_in_month) and int(input_day) > 0:
                        cutoff_date[0] = int(input_day)
                        main_console.configure(text="")
                        main_console_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        main_console.configure(text="")
                        main_console_text = "Den: " + str(input_day) + " je mimo rozsah"
                else:
                    main_console.configure(text="")
                    main_console_text = "U nastavení dne jste nezadali číslo"

            input_year = set_year.get()
            if input_year != "":
                if input_year.isdigit():
                    if len(str(input_year)) == 2:
                        cutoff_date[2] = int(input_year) + 2000
                        main_console.configure(text="")
                        main_console_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    elif len(str(input_year)) == 4:
                        cutoff_date[2] = int(input_year)
                        main_console.configure(text="")
                        main_console_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        main_console.configure(text="")
                        main_console_text = "Rok: " + str(input_year) + " je mimo rozsah"
                else:
                    main_console.configure(text="")
                    main_console_text = "U nastavení roku jste nezadali číslo"

            write_text_file_data(cutoff_date,"default_cutoff_date")
            setting_widgets(main_console_text,False)

        def set_files_to_keep():
            main_console_text = ""
            input_files_to_keep = files_to_keep_set.get()
            if input_files_to_keep.isdigit():
                if int(input_files_to_keep) >= 0:
                    files_to_keep = int(input_files_to_keep)
                    write_text_file_data(files_to_keep,"default_files_to_keep")
                    main_console.configure(text="")
                    main_console_text = "Základní počet ponechaných starších souborů nastaven na: " + str(files_to_keep)
                    console_files_to_keep.configure(text = "Aktuálně nastavené minimum: "+str(files_to_keep))
                else:
                    main_console.configure(text="")
                    main_console_text = "Mimo rozsah"
            else:
                main_console.configure(text="")
                main_console_text = "Nazadali jste číslo"

            
            setting_widgets(main_console_text,False)

        def insert_current_date():
            today = Deleting.get_current_date()
            today_split = today[1].split(".")
            i=0
            for items in today_split:
                i+=1
                cutoff_date[i-1]=items

            main_console.configure(text="")
            main_console_text = "Bylo vloženo dnešní datum (Momentálně všechny soubory vyhodnoceny, jako starší!)"

            setting_widgets(main_console_text,cutoff_date)

        #widgets na nastaveni zakladniho dne
        label1 = customtkinter.CTkLabel(master = bottom_frame_with_date,height=20,text = "Nastavte základní datum pro vyhodnocení souborů, jako starších:",justify = "left",font=("Arial",12,"bold"))
        set_day = customtkinter.CTkEntry(master = bottom_frame_with_date,width=30,height=30, placeholder_text= cutoff_date[0])
        sep1 = customtkinter.CTkLabel(master = bottom_frame_with_date,height=20,width=10,text = ".",font=("Arial",20))
        set_month = customtkinter.CTkEntry(master = bottom_frame_with_date,width=30,height=30, placeholder_text= cutoff_date[1])
        sep2 = customtkinter.CTkLabel(master = bottom_frame_with_date,height=20,width=10,text = ".",font=("Arial",20))
        set_year = customtkinter.CTkEntry(master = bottom_frame_with_date,width=50,height=30, placeholder_text= cutoff_date[2])
        button_save1 = customtkinter.CTkButton(master = bottom_frame_with_date,width=50,height=30, text = "Uložit", command = lambda: set_default_cutoff_date(),font=("Arial",12,"bold"))
        insert_button = customtkinter.CTkButton(master = bottom_frame_with_date,width=130,height=30, text = "Vložit dnešní datum", command = lambda: insert_current_date(),font=("Arial",12,"bold"))
        label1.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        set_day.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
        sep1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=40)
        set_month.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=50)
        sep2.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=80)
        set_year.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=90)
        button_save1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=140)
        insert_button.grid(column =0,row=row_index+3,sticky = tk.W,pady =0,padx=10)
        
        def set_new_default_prefix(which_folder):
            report = ""
            if which_folder == "cam":
                report = write_text_file_data(set_new_def_prefix_cam.get(),"new_default_prefix_cam")
                main_console.configure(text="")
                main_console.configure(text=report)
            if which_folder == "func":
                report = write_text_file_data(set_new_def_prefix_func.get(),"new_default_prefix_func")
                main_console.configure(text="")
                main_console.configure(text=report)

        #widgets na nastaveni zakladni slozky cam    
        label_folder_cam = customtkinter.CTkLabel(master = bottom_frame_with_date,height=20,text = "Nastavte základní název složky pro třídění podle kamer:",justify = "left",font=("Arial",12,"bold"))
        set_new_def_prefix_cam = customtkinter.CTkEntry(master = bottom_frame_with_date,width=200,height=30, placeholder_text= str(default_prefix_cam))
        button_save_new_def_prefix = customtkinter.CTkButton(master = bottom_frame_with_date,width=50,height=30, text = "Uložit", command = lambda: set_new_default_prefix("cam"),font=("Arial",12,"bold"))
        #console_cam_prefix=customtkinter.CTkLabel(master = bottom_frame_with_date,height=30,text ="",justify = "left",font=("Arial",12))
        label_folder_cam.grid(column =1,row=row_index+1,sticky = tk.W,pady =0,padx=300)
        set_new_def_prefix_cam.grid(column =1,row=row_index+2,sticky = tk.W,pady =0,padx=300)
        button_save_new_def_prefix.grid(column =1,row=row_index+2,sticky = tk.W,pady =0,padx=500)
        #console_cam_prefix.grid(column =1,row=row_index+3,sticky = tk.W,pady =0,padx=300)
    
        #widgets na nastaveni zakladniho poctu files_to_keep
        files_to_keep_console_text ="Aktuálně nastavené minimum: "+str(files_to_keep)
        label2 = customtkinter.CTkLabel(master = bottom_frame_with_files_to_keep,height=20,text = "Nastavte základní počet ponechaných souborů, vyhodnocených jako starších:",justify = "left",font=("Arial",12,"bold"))
        files_to_keep_set = customtkinter.CTkEntry(master = bottom_frame_with_files_to_keep,width=50,height=30, placeholder_text= files_to_keep)
        button_save2 = customtkinter.CTkButton(master = bottom_frame_with_files_to_keep,width=50,height=30, text = "Uložit", command = lambda: set_files_to_keep(),font=("Arial",12,"bold"))
        console_files_to_keep=customtkinter.CTkLabel(master = bottom_frame_with_files_to_keep,height=30,text =files_to_keep_console_text,justify = "left",font=("Arial",12))
        label2.grid(column =0,row=row_index,sticky = tk.W,pady =0,padx=10)
        files_to_keep_set.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        button_save2.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=60)
        console_files_to_keep.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)

        #widgets na nastaveni zakladni slozky func
        label_folder_func = customtkinter.CTkLabel(master = bottom_frame_with_files_to_keep,height=20,text = "Nastavte základní název složky pro třídění podle funkce:",justify = "left",font=("Arial",12,"bold"))
        set_new_def_prefix_func = customtkinter.CTkEntry(master = bottom_frame_with_files_to_keep,width=200,height=30, placeholder_text= str(default_prefix_func))
        button_save_new_def_prefix_func = customtkinter.CTkButton(master = bottom_frame_with_files_to_keep,width=50,height=30, text = "Uložit", command = lambda: set_new_default_prefix("func"),font=("Arial",12,"bold"))
        #console_func_prefix=customtkinter.CTkLabel(master = bottom_frame_with_files_to_keep,height=30,text ="",justify = "left",font=("Arial",12))
        label_folder_func.grid(column =1,row=row_index,sticky = tk.W,pady =0,padx=230)
        set_new_def_prefix_func.grid(column =1,row=row_index+1,sticky = tk.W,pady =0,padx=230)
        button_save_new_def_prefix_func.grid(column =1,row=row_index+1,sticky = tk.W,pady =0,padx=430)
        #console_func_prefix.grid(column =1,row=row_index+2,sticky = tk.W,pady =0,padx=230)
    
        def add_format(which_operation):
            main_console_text = ""
            if which_operation == 0:
                new_format = str(formats_set.get())
                if new_format !="":
                    main_console.configure(text="")
                    main_console_text = write_text_file_data(new_format,"add_supported_sorting_formats")
            if which_operation == 1:
                new_format = str(formats_set2.get())
                if new_format !="":
                    main_console.configure(text="")
                    main_console_text = write_text_file_data(new_format,"add_supported_deleting_formats")
            setting_widgets(main_console_text,False)

        def pop_format(which_operation):
            main_console_text = ""
            if which_operation == 0:
                format_to_delete = str(formats_set.get())
                if format_to_delete !="":
                    main_console.configure(text="")
                    main_console_text = write_text_file_data(format_to_delete,"pop_supported_sorting_formats")
            if which_operation == 1:
                format_to_delete = str(formats_set2.get())
                if format_to_delete !="":
                    main_console.configure(text="")
                    main_console_text = write_text_file_data(format_to_delete,"pop_supported_deleting_formats")

            setting_widgets(main_console_text,False)

        supported_formats_sorting = "Aktuálně nastavené podporované formáty pro možnosti třídění: " + str(text_file_data[0])
        label3 = customtkinter.CTkLabel(master = bottom_frame_sorting_formats,height=20,text = "Nastavte podporované formáty pro možnosti: TŘÍDĚNÍ:",justify = "left",font=("Arial",12,"bold"))
        formats_set = customtkinter.CTkEntry(master = bottom_frame_sorting_formats,width=50,height=30)
        button_save3 = customtkinter.CTkButton(master = bottom_frame_sorting_formats,width=50,height=30, text = "Uložit", command = lambda: add_format(0),font=("Arial",12,"bold"))
        button_pop = customtkinter.CTkButton(master = bottom_frame_sorting_formats,width=70,height=30, text = "Odebrat", command = lambda: pop_format(0),font=("Arial",12,"bold"))
        console_bottom_frame_3=customtkinter.CTkLabel(master = bottom_frame_sorting_formats,height=30,text =supported_formats_sorting,justify = "left",font=("Arial",12))
        label3.grid(column =0,row=row_index,sticky = tk.W,pady =0,padx=10)
        formats_set.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        button_save3.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=60)
        button_pop.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=110)
        console_bottom_frame_3.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)

        def set_max_num_of_pallets():
            input_1 = set_max_pallets.get()
            if input_1.isdigit() == False:
                main_console.configure(text = "")
                main_console.configure(text = "Nezadali jste číslo")
            elif int(input_1) <1:
                main_console.configure(text = "")
                main_console.configure(text = "Mimo rozsah")
            else:
                main_console.configure(text = "")
                main_console.configure(text = f"Počet palet nastaven na: {input_1}")
                write_text_file_data(input_1,"pallets_set")
                
        #widgets na nastaveni zakladniho poctu palet v obehu
        label_pallets = customtkinter.CTkLabel(master = bottom_frame_sorting_formats,height=20,text = "Nastavte základní maximální počet paletek v oběhu:",justify = "left",font=("Arial",12,"bold"))
        set_max_pallets = customtkinter.CTkEntry(master = bottom_frame_sorting_formats,width=100,height=30, placeholder_text= str(default_max_num_of_pallets))
        button_save_max_num_of_pallets = customtkinter.CTkButton(master = bottom_frame_sorting_formats,width=50,height=30, text = "Uložit", command = lambda: set_max_num_of_pallets(),font=("Arial",12,"bold"))
        #console_pallets=customtkinter.CTkLabel(master = bottom_frame_sorting_formats,height=30,text ="",justify = "left",font=("Arial",12))
        label_pallets.grid(column =1,row=row_index,sticky = tk.W,pady =0,padx=260)
        set_max_pallets.grid(column =1,row=row_index+1,sticky = tk.W,pady =0,padx=260)
        button_save_max_num_of_pallets.grid(column =1,row=row_index+1,sticky = tk.W,pady =0,padx=360)
        #console_pallets.grid(column =1,row=row_index+2,sticky = tk.W,pady =0,padx=260)

        supported_formats_deleting = "Aktuálně nastavené podporované formáty pro možnosti mazání: " + str(text_file_data[1])
        label4 = customtkinter.CTkLabel(master = bottom_frame_deleting_formats,height=20,text = "Nastavte podporované formáty pro možnosti: MAZÁNÍ:",justify = "left",font=("Arial",12,"bold"))
        formats_set2 = customtkinter.CTkEntry(master = bottom_frame_deleting_formats,width=50,height=30)
        button_save4 = customtkinter.CTkButton(master = bottom_frame_deleting_formats,width=50,height=30, text = "Uložit", command = lambda: add_format(1),font=("Arial",12,"bold"))
        button_pop2 = customtkinter.CTkButton(master = bottom_frame_deleting_formats,width=70,height=30, text = "Odebrat", command = lambda: pop_format(1),font=("Arial",12,"bold"))
        console_bottom_frame_4=customtkinter.CTkLabel(master = bottom_frame_deleting_formats,height=30,text =supported_formats_deleting,justify = "left",font=("Arial",12))
        label4.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        formats_set2.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
        button_save4.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=60)
        button_pop2.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=110)
        console_bottom_frame_4.grid(column =0,row=row_index+3,sticky = tk.W,pady =0,padx=10)

        main_console_label = customtkinter.CTkLabel(master = main_console_frame,height=50,text ="KONZOLA:",justify = "left",font=("Arial",16,"bold"))
        main_console_label.grid(column =0,row=row_index,sticky = tk.W,pady =0,padx=10)
        main_console = customtkinter.CTkLabel(master = main_console_frame,height=50,text =main_console_text,justify = "left",font=("Arial",16))
        main_console.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)

    setting_widgets("",False)

def Converting_option(list_of_menu_frames):
    """
    Funkce spouští možnosti konvertování typu souborů
    """
    #cisteni menu widgets
    for frames in list_of_menu_frames: 
        frames.pack_forget()
        frames.grid_forget()
        frames.destroy()

    #cisteni pred vstupem do menu
    def call_menu():
        list_of_frames = [frame_path_input,bottom_frame1,bottom_frame2]
        for frames in list_of_frames:
            frames.pack_forget()
            frames.grid_forget()
            frames.destroy()
        menu()

    def convert_files(path):
        selected_format = "bmp"
        if checkbox_bmp.get() == 1:
            selected_format = "bmp"
        if checkbox_jpg.get() == 1:
            selected_format = "jpg"

        Converting.output = []
        Converting.whole_converting_function(path,selected_format)
        output_text = ""
        for i in range(0,len(Converting.output)):
            output_text = output_text + Converting.output[i]
        console.configure(text = output_text)

    def start():
        if checkbox_bmp.get()+checkbox_jpg.get() == 0:
            console.configure(text = "Nevybrali jste žádný formát, do kterého se má konvertovat :-)")
        else:
            path = path_set.get() 
            if path != "":
                check = Trideni.path_check(path)
                if check == False:
                    console.configure(text = "Zadaná cesta: "+str(path)+" nebyla nalezena")
                else:
                    path = check
                    console.configure(text = str(path)+" je OK")
                    convert_files(path)
            else:
                console.configure(text = "Nebyla vložena cesta k souborům")

    #definice ramcu
    frame_path_input = customtkinter.CTkFrame(master=root)
    frame_path_input.pack(pady=5,padx=5,fill="both",expand=False,side = "top")
    bottom_frame2 = customtkinter.CTkScrollableFrame(master=root)
    bottom_frame2.pack(pady=5,padx=5,fill="both",expand=True,side = "bottom")
    bottom_frame1 = customtkinter.CTkFrame(master=root,height = 80)
    bottom_frame1.pack(pady=0,padx=5,fill="x",expand=False,side = "bottom")

    def call_browseDirectories():
        output = browseDirectories()
        if str(output[1]) != "/":
            path_set.delete("0","200")
            path_set.insert("0", output[1])
            console.configure(text="")
            console.configure(text=f"Byla vložena cesta: {output[1]}")

    def selected_bmp():
        checkbox_jpg.deselect()
    def selected_jpg():
        checkbox_bmp.deselect()

    checkbox_bmp = customtkinter.CTkCheckBox(master = bottom_frame1, text = "Konvertovat do formátu .bmp",command=selected_bmp,font=("Arial",16,"bold"))
    checkbox_bmp.pack(pady =20,padx=10,anchor ="w")
    checkbox_jpg = customtkinter.CTkCheckBox(master = bottom_frame1, text = "Konvertovat do formátu .jpg",command=selected_jpg,font=("Arial",16,"bold"))
    checkbox_jpg.pack(pady =20,padx=10,anchor ="w")
    menu_button  = customtkinter.CTkButton(master = frame_path_input, width = 180, text = "MENU", command = lambda: call_menu(),font=("Arial",20,"bold"))
    menu_button.pack(pady =12,padx=10,anchor ="w",side="left")
    path_set     = customtkinter.CTkEntry(master = frame_path_input,placeholder_text="Zadejte cestu k souborům určeným ke konvertování (kde se soubory přímo nacházejí)")
    path_set.pack(pady = 12,padx =0,anchor ="w",side="left",fill="both",expand=True)
    tree         = customtkinter.CTkButton(master = frame_path_input, width = 180,text = "EXPLORER", command = call_browseDirectories,font=("Arial",20,"bold"))
    tree.pack(pady = 12,padx =10,anchor ="w",side="left")

    label   = customtkinter.CTkLabel(master = bottom_frame2,text = "Konvertované soubory budou umístěny do separátní složky\nPodporované formáty: .ifz\nObsahuje-li .ifz soubor více obrázků, budou uloženy v následující syntaxi:\nxxx_0.bmp, xxx_1.bmp ...\nPro správnou funkci programu nesmí cesta obsahovat složky s mezerou v názvu",justify = "left",font=("Arial",16,"bold"))
    label.pack(pady =10,padx=10)
    button  = customtkinter.CTkButton(master = bottom_frame2, text = "KONVERTOVAT", command = start,font=("Arial",20,"bold"))
    button.pack(pady =20,padx=10)
    button._set_dimensions(300,60)
    console = customtkinter.CTkLabel(master = bottom_frame2,text = " ",justify = "left",font=("Arial",15))
    console.pack(pady =10,padx=10)

    checkbox_bmp.select()
    root.mainloop()

def Deleting_option(list_of_menu_frames):
    #cisteni menu widgets
    for frames in list_of_menu_frames: 
        frames.pack_forget()
        frames.grid_forget()
        frames.destroy()

    global more_dirs
    more_dirs = False
    global files_to_keep
    #files_to_keep = 1000
    text_file_data = read_text_file_data()
    files_to_keep = text_file_data[3]
    global cutoff_date
    #cutoff_date = ["01","01","1999"]
    cutoff_date = text_file_data[4]
    supported_formats_deleting = text_file_data[0]

    #cisteni pred vstupem do menu
    def call_menu():
        list_of_frames = [frame_path_input,bottom_frame1,bottom_frame2,frame_right,frame_with_checkboxes]
        for frames in list_of_frames:
            frames.pack_forget()
            frames.grid_forget()
            frames.destroy()
        menu()

    def start():
        if checkbox.get()+checkbox2.get()+checkbox3.get() == 0:
            console.configure(text = "Nevybrali jste žádný způsob mazání :-)")
            info.configure(text = "")

        else:
            path = path_set.get() 
            if path != "":
                check = Trideni.path_check(path)
                if check == False:
                    console.configure(text = "Zadaná cesta: "+str(path)+" nebyla nalezena")
                else:
                    path = check
                    console.configure(text = str(path)+" je OK")
                    del_files(path)
            else:
                console.configure(text = "Nebyla vložena cesta k souborům")

    def del_files(path):
        testing_mode = True
        del_option = 0
        if checkbox.get() == 1:
            del_option = 1
        if checkbox2.get() == 1:
            del_option = 2
        if checkbox3.get() == 1:
            del_option = 3
        if checkbox6.get() == 1:
            more_dirs = True
        else:
            more_dirs = False
        if checkbox_testing.get() == 1:
            testing_mode = True
        else:
            testing_mode = False

        Deleting.output = []

        Deleting.whole_deleting_function(path,more_dirs,del_option,files_to_keep,cutoff_date,supported_formats_deleting,testing_mode)
        output_text = ""
        for i in range(0,len(Deleting.output)):
            output_text = output_text + Deleting.output[i]# + "\n"
        console.configure(text = output_text)

    #definice ramcu
    frame_path_input = customtkinter.CTkFrame(master=root)
    frame_path_input.pack(pady=5,padx=5,fill="both",expand=False,side = "top")
    bottom_frame2 = customtkinter.CTkScrollableFrame(master=root)
    bottom_frame2.pack(pady=0,padx=5,fill="both",expand=True,side = "bottom")
    bottom_frame1 = customtkinter.CTkFrame(master=root,height = 80)
    bottom_frame1.pack(pady=5,padx=5,fill="x",expand=False,side = "bottom")
    checkbox_frame = customtkinter.CTkFrame(master=root,width=400)
    checkbox_frame.pack(pady=0,padx=5,fill="y",expand=False,side="left")
    frame_right = customtkinter.CTkScrollableFrame(master=root)
    frame_right.pack(pady=0,padx=5,fill="both",expand=True,side="right")

    def call_browseDirectories():
        output = browseDirectories()
        if str(output[1]) != "/":
            path_set.delete("0","200")
            path_set.insert("0", output[1])
            console.configure(text="")
            console.configure(text=f"Byla vložena cesta: {output[1]}")

    menu_button = customtkinter.CTkButton(master = frame_path_input, width = 180, text = "MENU", command = lambda: call_menu(),font=("Arial",20,"bold"))
    menu_button.pack(pady =12,padx=10,anchor ="w",side="left")
    path_set = customtkinter.CTkEntry(master = frame_path_input,placeholder_text="Zadejte cestu k souborům z kamery (kde se přímo nacházejí soubory nebo datumové složky)")
    path_set.pack(pady = 12,padx =0,anchor ="w",side="left",fill="both",expand=True)
    tree = customtkinter.CTkButton(master = frame_path_input, width = 180,text = "EXPLORER", command = call_browseDirectories,font=("Arial",20,"bold"))
    tree.pack(pady = 12,padx =10,anchor ="w",side="left")

    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def selected(console_frame_right_1_text,console_frame_right_2_text):
        clear_frame(frame_right)
        console.configure(text = " ")
        #view_image(1)
        checkbox2.deselect()
        checkbox3.deselect()
        info.configure(text = "")
        info.configure(text = f"- Budou smazány soubory starší než nastavené datum, přičemž bude ponechán nastavený počet souborů, vyhodnocených, jako starších\nPodporované formáty: {supported_formats_deleting}",font = ("Arial",16,"bold"),justify="left")
        selected6() #update

        def set_cutoff_date():
            console_frame_right_1_text = ""
            console_frame_right_2_text = ""  
            input_month = set_month.get()
            if input_month != "":
                if input_month.isdigit():
                    if int(input_month) < 13 and int(input_month) > 0:
                        cutoff_date[1] = int(input_month)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Měsíc: " + str(input_month) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "U nastavení měsíce jste nezadali číslo"

            input_day = set_day.get()
            max_days_in_month = Deleting.calc_days_in_month(int(cutoff_date[1]))

            if input_day != "":
                if input_day.isdigit():
                    if int(input_day) <= int(max_days_in_month) and int(input_day) > 0:
                        cutoff_date[0] = int(input_day)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Den: " + str(input_day) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "U nastavení dne jste nezadali číslo"

            input_year = set_year.get()
            if input_year != "":
                if input_year.isdigit():
                    if len(str(input_year)) == 2:
                        cutoff_date[2] = int(input_year) + 2000
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    elif len(str(input_year)) == 4:
                        cutoff_date[2] = int(input_year)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Rok: " + str(input_year) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "U nastavení roku jste nezadali číslo"

            selected(console_frame_right_1_text,console_frame_right_2_text)

        def set_files_to_keep():
            global files_to_keep
            input_files_to_keep = files_to_keep_set.get()
            if input_files_to_keep.isdigit():
                if int(input_files_to_keep) >= 0:
                    files_to_keep = int(input_files_to_keep)
                    console_frame_right_2.configure(text="")
                    console_frame_right_2_text = "Počet ponechaných starších souborů nastaven na: " + str(files_to_keep)
                else:
                    console_frame_right_2.configure(text="")
                    console_frame_right_2_text = "Mimo rozsah"
            else:
                console_frame_right_2.configure(text="")
                console_frame_right_2_text = "Nazadali jste číslo"

            
            selected(console_frame_right_1_text,console_frame_right_2_text)

        def insert_current_date():
            today = Deleting.get_current_date()
            today_split = today[1].split(".")
            i=0
            for items in today_split:
                i+=1
                cutoff_date[i-1]=items

            console_frame_right_1.configure(text="")
            console_frame_right_1_text = "Bylo vloženo dnešní datum (Momentálně všechny soubory vyhodnoceny, jako starší!)"

            selected(console_frame_right_1_text,console_frame_right_2_text)

        today = Deleting.get_current_date()
        row_index = 0
        label0 = customtkinter.CTkLabel(master = frame_right,height=20,text = "Dnešní datum: "+today[1],justify = "left",font=("Arial",16,"bold"))
        label1 = customtkinter.CTkLabel(master = frame_right,height=20,text = "Nastavte datum pro vyhodnocení souborů, jako starších:",justify = "left",font=("Arial",12))
        set_day = customtkinter.CTkEntry(master = frame_right,width=30,height=30, placeholder_text= cutoff_date[0])
        sep1 = customtkinter.CTkLabel(master = frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_month = customtkinter.CTkEntry(master = frame_right,width=30,height=30, placeholder_text= cutoff_date[1])
        sep2 = customtkinter.CTkLabel(master = frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_year = customtkinter.CTkEntry(master = frame_right,width=50,height=30, placeholder_text= cutoff_date[2])
        button_save1 = customtkinter.CTkButton(master = frame_right,width=50,height=30, text = "Uložit", command = lambda: set_cutoff_date(),font=("Arial",12,"bold"))
        insert_button = customtkinter.CTkButton(master = frame_right,width=130,height=30, text = "Vložit dnešní datum", command = lambda: insert_current_date(),font=("Arial",12,"bold"))
        console_frame_right_1=customtkinter.CTkLabel(master = frame_right,height=30,text = console_frame_right_1_text,justify = "left",font=("Arial",12))
        
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

        label2 = customtkinter.CTkLabel(master = frame_right,height=20,text = "Nastavte počet ponechaných souborů, vyhodnocených jako starších:",justify = "left",font=("Arial",12))
        files_to_keep_set = customtkinter.CTkEntry(master = frame_right,width=50,height=30, placeholder_text= files_to_keep)
        button_save2 = customtkinter.CTkButton(master = frame_right,width=50,height=30, text = "Uložit", command = lambda: set_files_to_keep(),font=("Arial",12,"bold"))
        console_frame_right_2=customtkinter.CTkLabel(master = frame_right,height=30,text =console_frame_right_2_text,justify = "left",font=("Arial",12))
        label2.grid(column =0,row=5,sticky = tk.W,pady =0,padx=10)
        files_to_keep_set.grid(column =0,row=6,sticky = tk.W,pady =0,padx=10)
        button_save2.grid(column =0,row=6,sticky = tk.W,pady =0,padx=60)
        console_frame_right_2.grid(column =0,row=7,sticky = tk.W,pady =0,padx=10)
          
    def selected2(console_frame_right_1_text,console_frame_right_2_text):
        clear_frame(frame_right)
        console.configure(text = " ")
        checkbox.deselect()
        checkbox3.deselect()
        info.configure(text = "")
        info.configure(text = f"- Budou smazány VŠECHNY soubory starší než nastavené datum, přičemž budou redukovány i soubory novější\n- Souborů, vyhodnocených, jako novější, bude ponechán nastavený počet\n(vhodné při situacích rychlého pořizování velkého množství fotografií, kde je potřebné ponechat nějaké soubory pro referenci)\nPodporované formáty: {supported_formats_deleting}",font = ("Arial",16,"bold"),justify="left")
        selected6() #update

        def set_cutoff_date():
            input_month = set_month.get()
            if input_month != "":
                if input_month.isdigit():
                    if int(input_month) < 13 and int(input_month) > 0:
                        cutoff_date[1] = int(input_month)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Měsíc: " + str(input_month) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "Nezadali jste číslo"

            input_day = set_day.get()
            max_days_in_month = Deleting.calc_days_in_month(int(cutoff_date[1]))

            if input_day != "":
                if input_day.isdigit():
                    if int(input_day) <= int(max_days_in_month) and int(input_day) > 0:
                        cutoff_date[0] = int(input_day)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Den: " + str(input_day) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "Nezadali jste číslo"

            input_year = set_year.get()
            if input_year != "":
                if input_year.isdigit():
                    if len(str(input_year)) == 2:
                        cutoff_date[2] = int(input_year) + 2000
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    elif len(str(input_year)) == 4:
                        cutoff_date[2] = int(input_year)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Rok: " + str(input_year) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "Nezadali jste číslo"

                        
            selected2(console_frame_right_1_text,console_frame_right_2_text)

        def set_files_to_keep():
            global files_to_keep
            input_files_to_keep = files_to_keep_set.get()
            if input_files_to_keep.isdigit():
                if int(input_files_to_keep) >= 0:
                    files_to_keep = int(input_files_to_keep)
                    console_frame_right_2.configure(text="")
                    console_frame_right_2_text = "Počet ponechaných starších souborů nastaven na: " + str(files_to_keep)
                else:
                    console_frame_right_2.configure(text="")
                    console_frame_right_2_text = "Mimo rozsah"
            else:
                console_frame_right_2.configure(text="")
                console_frame_right_2_text = "Nazadali jste číslo"

            
            selected2(console_frame_right_1_text,console_frame_right_2_text)

        today = Deleting.get_current_date()
        row_index = 0
        label0 = customtkinter.CTkLabel(master = frame_right,height=20,text = "Dnešní datum: "+today[1],justify = "left",font=("Arial",16,"bold"))
        label1 = customtkinter.CTkLabel(master = frame_right,height=20,text = "Nastavte datum pro vyhodnocení souborů, jako starších:",justify = "left",font=("Arial",12))
        set_day = customtkinter.CTkEntry(master = frame_right,width=30,height=30, placeholder_text= cutoff_date[0])
        sep1 = customtkinter.CTkLabel(master = frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_month = customtkinter.CTkEntry(master = frame_right,width=30,height=30, placeholder_text= cutoff_date[1])
        sep2 = customtkinter.CTkLabel(master = frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_year = customtkinter.CTkEntry(master = frame_right,width=50,height=30, placeholder_text= cutoff_date[2])
        button_save1 = customtkinter.CTkButton(master = frame_right,width=50,height=30, text = "Uložit", command = lambda: set_cutoff_date(),font=("Arial",12,"bold"))
        console_frame_right_1=customtkinter.CTkLabel(master = frame_right,height=30,text = console_frame_right_1_text,justify = "left",font=("Arial",12))
        label0.grid(column =0,row=row_index,sticky = tk.W,pady =0,padx=10)
        label1.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        set_day.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
        sep1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=40)
        set_month.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=50)
        sep2.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=80)
        set_year.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=90)
        button_save1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=140)
        console_frame_right_1.grid(column =0,row=row_index+3,sticky = tk.W,pady =0,padx=10)

        label2 = customtkinter.CTkLabel(master = frame_right,height=20,text = "Nastavte počet ponechaných novějších souborů:",justify = "left",font=("Arial",12))
        files_to_keep_set = customtkinter.CTkEntry(master = frame_right,width=50,height=30, placeholder_text= files_to_keep)
        button_save2 = customtkinter.CTkButton(master = frame_right,width=50,height=30, text = "Uložit", command = lambda: set_files_to_keep(),font=("Arial",12,"bold"))
        console_frame_right_2=customtkinter.CTkLabel(master = frame_right,height=30,text =console_frame_right_2_text,justify = "left",font=("Arial",12))
        label2.grid(column =0,row=5,sticky = tk.W,pady =0,padx=10)
        files_to_keep_set.grid(column =0,row=6,sticky = tk.W,pady =0,padx=10)
        button_save2.grid(column =0,row=6,sticky = tk.W,pady =0,padx=60)
        console_frame_right_2.grid(column =0,row=7,sticky = tk.W,pady =0,padx=10)
        
    def selected3(console_frame_right_1_text,console_frame_right_2_text):
        clear_frame(frame_right)
        console.configure(text = " ")
        checkbox2.deselect()
        checkbox.deselect()
        info.configure(text = "")
        info.configure(text = f"- Budou smazány VŠECHNY adresáře (včetně všech subadresářů), které obsahují v názvu podporovaný formát datumu a jsou vyhodnoceny,\njako starší než nastavené datum\nPodporované datumové formáty: {Deleting.supported_date_formats}\nPodporované separátory datumu: {Deleting.supported_separators}",font = ("Arial",16,"bold"),justify="left")
        selected6() #update

        def set_cutoff_date():
            input_month = set_month.get()
            if input_month != "":
                if input_month.isdigit():
                    if int(input_month) < 13 and int(input_month) > 0:
                        cutoff_date[1] = int(input_month)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Měsíc: " + str(input_month) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "Nezadali jste číslo"

            input_day = set_day.get()
            max_days_in_month = Deleting.calc_days_in_month(int(cutoff_date[1]))

            if input_day != "":
                if input_day.isdigit():
                    if int(input_day) <= int(max_days_in_month) and int(input_day) > 0:
                        cutoff_date[0] = int(input_day)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Den: " + str(input_day) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "Nezadali jste číslo"

            input_year = set_year.get()
            if input_year != "":
                if input_year.isdigit():
                    if len(str(input_year)) == 2:
                        cutoff_date[2] = int(input_year) + 2000
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    elif len(str(input_year)) == 4:
                        cutoff_date[2] = int(input_year)
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2])
                    else:
                        console_frame_right_1.configure(text="")
                        console_frame_right_1_text = "Rok: " + str(input_year) + " je mimo rozsah"
                else:
                    console_frame_right_1.configure(text="")
                    console_frame_right_1_text = "Nezadali jste číslo"

                        
            selected3(console_frame_right_1_text,console_frame_right_2_text)

        today = Deleting.get_current_date()
        row_index = 0
        label0 = customtkinter.CTkLabel(master = frame_right,height=20,text = "Dnešní datum: "+today[1],justify = "left",font=("Arial",16,"bold"))
        images2 = customtkinter.CTkLabel(master = frame_right,text = "")
        label1 = customtkinter.CTkLabel(master = frame_right,height=20,text = "Nastavte datum pro vyhodnocení datumu v názvu adresářů, jako staršího:",justify = "left",font=("Arial",12))
        set_day = customtkinter.CTkEntry(master = frame_right,width=30,height=30, placeholder_text= cutoff_date[0])
        sep1 = customtkinter.CTkLabel(master = frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_month = customtkinter.CTkEntry(master = frame_right,width=30,height=30, placeholder_text= cutoff_date[1])
        sep2 = customtkinter.CTkLabel(master = frame_right,height=20,width=10,text = ".",font=("Arial",20))
        set_year = customtkinter.CTkEntry(master = frame_right,width=50,height=30, placeholder_text= cutoff_date[2])
        button_save1 = customtkinter.CTkButton(master = frame_right,width=50,height=30, text = "Uložit", command = lambda: set_cutoff_date(),font=("Arial",12,"bold"))
        console_frame_right_1=customtkinter.CTkLabel(master = frame_right,height=30,text = console_frame_right_1_text,justify = "left",font=("Arial",12))
        directories = customtkinter.CTkImage(Image.open("images/directories.png"),size=(240, 190))

        label0.grid(column =0,row=row_index,sticky = tk.W,pady =0,padx=10)
        images2.grid(column =0,row=row_index,sticky = tk.W,pady =10,padx=500,rowspan=5)
        label1.grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=10)
        set_day.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
        sep1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=40)
        set_month.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=50)
        sep2.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=80)
        set_year.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=90)
        button_save1.grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=140)
        console_frame_right_1.grid(column =0,row=row_index+3,sticky = tk.W,pady =0,padx=10)
        images2.configure(image = directories)

    def selected6():
        if checkbox6.get() == 1:
            if checkbox3.get() == 1:
                info2.configure(text = "- Pro tuto možnost třídění není tato funkce podporována",font=("Arial",16,"bold"))
            else:
                info2.configure(text = "- VAROVÁNÍ: Máte spuštěné možnosti mazání souborů i ve všech subsložkách vložené cesty (max:6 subsložek)",font=("Arial",16,"bold"))
        else:
            info2.configure(text = "")

    frame_with_checkboxes = checkbox_frame

    checkbox = customtkinter.CTkCheckBox(master = frame_with_checkboxes, text = "Mazání souborů starších než: určité datum",command = lambda: selected("",""))
    checkbox.pack(pady =10,padx=10,anchor ="w")
    checkbox2 = customtkinter.CTkCheckBox(master = frame_with_checkboxes, text = "Redukce novějších, mazání souborů starších než: určité datum",command = lambda: selected2("",""))
    checkbox2.pack(pady =10,padx=10,anchor ="w")
    checkbox3 = customtkinter.CTkCheckBox(master = frame_with_checkboxes, text = "Mazání adresářů s názvem ve formátu určitého datumu",command = lambda: selected3("",""))
    checkbox3.pack(pady =10,padx=10,anchor ="w")

    checkbox6 = customtkinter.CTkCheckBox(master = bottom_frame1, text = "Procházet subsložky? (max:6)",command = selected6,font=("Arial",12,"bold"))
    checkbox6.grid(column =0,row=0,sticky = tk.W,pady =5,padx=10)
    info2 = customtkinter.CTkLabel(master = bottom_frame1,text = "",font=("Arial",12,"bold"))
    info2.grid(column =0,row=0,sticky = tk.W,pady =5,padx=250)
    checkbox_testing = customtkinter.CTkCheckBox(master = bottom_frame1, text = "Režim TESTOVÁNÍ (Soubory vyhodnocené ke smazání se pouze přesunou do složky s názvem: \"Ke_smazani\")",font=("Arial",12,"bold"))
    checkbox_testing.grid(column =0,row=1,sticky = tk.W,pady =5,padx=10)
    info = customtkinter.CTkLabel(master = bottom_frame2,text = "",font=("Arial",16,"bold"))
    info.pack(pady = 12,padx =10,anchor="w")
    button = customtkinter.CTkButton(master = bottom_frame2, text = "SPUSTIT", command = start,font=("Arial",20,"bold"))
    button.pack(pady =20,padx=10)
    button._set_dimensions(300,60)
    console = customtkinter.CTkLabel(master = bottom_frame2,text = " ",justify = "left",font=("Arial",15))
    console.pack(pady =10,padx=10)

    #default:
    checkbox.select()
    checkbox_testing.select()
    selected("","")

    root.mainloop()

def Sorting_option(list_of_menu_frames):
    for frames in list_of_menu_frames:
        frames.pack_forget()
        frames.grid_forget()
        frames.destroy()
    global by_which_ID_num
    global more_dirs
    global prefix_Cam
    global prefix_func
    global max_num_of_pallets
    global aut_detect_num_of_pallets
    aut_detect_num_of_pallets = True
    by_which_ID_num = ""   
    more_dirs = False
    text_file_data = read_text_file_data()
    prefix_func = text_file_data[5]
    prefix_Cam = text_file_data[6]
    supported_formats_sorting = text_file_data[0]
    max_num_of_pallets = text_file_data[8]

    def start():
        if checkbox.get()+checkbox2.get()+checkbox3.get()+checkbox4.get()+checkbox5.get() == 0:
            console.configure(text = "Nevybrali jste žádný způsob třídění :-)")
            nothing = customtkinter.CTkImage(Image.open("images/nothing.png"),size=(1, 1))
            images.configure(image = nothing)
            name_example.configure(text = "")

        else:
            path = path_set.get() 
            if path != "":
                check = Trideni.path_check(path)
                if check == False:
                    console.configure(text = "Zadaná cesta: "+str(path)+" nebyla nalezena")
                else:
                    path = check
                    console.configure(text = str(path)+" je OK")
                    sort_files(path)
            else:
                console.configure(text = "Nebyla vložena cesta k souborům")

    def sort_files(path):
        selected_sort = 0
        if checkbox.get() == 1:
            selected_sort = 1
        if checkbox2.get() == 1:
            selected_sort = 2
        if checkbox3.get() == 1:
            selected_sort = 3
        if checkbox4.get() == 1:
            selected_sort = 4
        if checkbox5.get() == 1:
            selected_sort = 5
        if checkbox6.get() == 1:
            more_dirs = True
        else:
            more_dirs = False
        Trideni.output = []
        Trideni.output_console2 = []

        Trideni.whole_sorting_function(path,selected_sort,more_dirs,max_num_of_pallets,by_which_ID_num,prefix_func,prefix_Cam,supported_formats_sorting,aut_detect_num_of_pallets)
        output_text = ""
        output_text2 = ""
        for i in range(0,len(Trideni.output)):
            output_text = output_text + Trideni.output[i] + "\n"
        console.configure(text = output_text)

        for i in range(0,len(Trideni.output_console2)):
            output_text2 = output_text2 + Trideni.output_console2[i] + "\n"
        if output_text2 != "":
            console2.configure(text = output_text2)

    def clear_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def selected(): #tridit podle typu souboru
        clear_frame(frame6)
        console.configure(text = " ")
        view_image(1)
        checkbox2.deselect()
        checkbox3.deselect()
        checkbox4.deselect()
        checkbox5.deselect()

        labelx = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=height_of_frame6+10,text = "",justify = "left",font=("Arial",12))
        labelx.grid(column =0,row=0,pady =0,padx=10)
        
    def selected2(): #tridit polde cisla funkce (ID)
        clear_frame(frame6)
        console.configure(text = " ")
        view_image(2)
        checkbox.deselect()
        checkbox3.deselect()
        checkbox4.deselect()
        checkbox5.deselect()

        def set_prefix():
            global prefix_func
            input_1 = prefix_set.get()
            console_frame6_1.configure(text = f"Prefix nastaven na: {input_1}")
            prefix_func = input_1

        label1 = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=20,text = "Nastavte prefix adresářů:",justify = "left",font=("Arial",12))
        label1.grid(column =0,row=0,pady =0,padx=10)
        prefix_set = customtkinter.CTkEntry(master = frame6,width=150,height=30, placeholder_text= prefix_func)
        prefix_set.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)
        button_save1 = customtkinter.CTkButton(master = frame6,width=50,height=30, text = "Uložit", command = lambda: set_prefix(),font=("Arial",12,"bold"))
        button_save1.grid(column =0,row=1,sticky = tk.E,pady =0,padx=10)
        console_frame6_1=customtkinter.CTkLabel(master = frame6,height=30,text = " ",justify = "left",font=("Arial",12))
        console_frame6_1.grid(column =0,row=2,pady =0,padx=10)

        labelx = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=30,text = "",justify = "left",font=("Arial",12))
        labelx.grid(column =0,row=3,pady =0,padx=10)
        checkbox_advance = customtkinter.CTkCheckBox(master = frame6,height=30, text = "Pokročilá nastavení",command = selected2_advance)
        checkbox_advance.grid(column =0,row=4,pady =0,padx=10)
        labelxx = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=120,text = "",justify = "left",font=("Arial",12))
        labelxx.grid(column =0,row=5,pady =0,padx=10)

    def selected2_advance():
        clear_frame(frame6)

        def set_which_num_of_ID():
            global by_which_ID_num
            input3=num_set.get()
            if input3.isdigit():
                if int(input3) > 0:
                    by_which_ID_num = int(input3)
                    console_frame6_1.configure(text = f"Řídit podle {by_which_ID_num}. čísla v ID")
                else:
                    console_frame6_1.configure(text = "Mimo rozsah")
                    by_which_ID_num = ""
            else:
                console_frame6_1.configure(text = "Nezadali jste číslo")
                by_which_ID_num = ""

        label1           = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=60,
                                        text = "Podle kterého čísla v ID se řídit:\n(např. poslední č. v ID = pozice dílu...)\nvolte první = 1 atd. (prázdné = celé ID)",
                                        justify = "left",font=("Arial",12))
        label1.grid(column =0,row=0,pady =0,padx=10)
        num_set          = customtkinter.CTkEntry(master = frame6,height=30,width=150, placeholder_text= by_which_ID_num)
        num_set.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)
        button_save1     = customtkinter.CTkButton(master = frame6,height=30,width=50, text = "Uložit", command = lambda: set_which_num_of_ID(),font=("Arial",12,"bold"))
        button_save1.grid(column =0,row=1,sticky = tk.E,pady =0,padx=10)
        console_frame6_1 = customtkinter.CTkLabel(master = frame6,height=30,text = " ",justify = "left",font=("Arial",12))
        console_frame6_1.grid(column =0,row=2,pady =0,padx=10)
        
        labelx2     = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=30,text = "",justify = "left",font=("Arial",12))
        labelx2.grid(column =0,row=3,pady =0,padx=10)
        
        button_back = customtkinter.CTkButton(master = frame6,width=100,height=30, text = "Zpět", command = selected2,font=("Arial",12,"bold"))
        button_back.grid(column =0,row=5,pady =0,padx=10)

        labelx3     = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=80,text = "",justify = "left",font=("Arial",12))
        labelx3.grid(column =0,row=6,pady =0,padx=10)
        
    def selected3(): #tridit podle cisla kamery
        clear_frame(frame6)
        console.configure(text = " ")
        view_image(3)   
        checkbox.deselect()
        checkbox2.deselect()
        checkbox4.deselect()
        checkbox5.deselect()

        def set_prefix():
            global prefix_Cam
            input_1 = prefix_set.get()
            console_frame6_1.configure(text = f"Prefix nastaven na: {input_1}")
            prefix_Cam = input_1


        label1              = customtkinter.CTkLabel(master = frame6,height=20,width=width_of_frame6,text = "Nastavte prefix adresářů:",justify = "left",font=("Arial",12))
        label1.grid(column =0,row=0,pady =0,padx=10)
        prefix_set          = customtkinter.CTkEntry(master = frame6,height=30,width=150, placeholder_text= prefix_Cam)
        prefix_set.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)
        button_save1        = customtkinter.CTkButton(master = frame6,height=30,width=50, text = "Uložit", command = lambda: set_prefix(),font=("Arial",12,"bold"))
        button_save1.grid(column =0,row=1,sticky = tk.E,pady =0,padx=10)
        console_frame6_1    = customtkinter.CTkLabel(master = frame6,height=30,text = " ",justify = "left",font=("Arial",12))
        console_frame6_1.grid(column =0,row=2,pady =0,padx=10)

        labelx = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=180,text = "",justify = "left",font=("Arial",12))
        labelx.grid(column =0,row=3,pady =0,padx=10)
        
    def selected4(): #tridit podle obojiho
        clear_frame(frame6)
        console.configure(text = " ")
        view_image(4)
        checkbox.deselect()
        checkbox2.deselect()
        checkbox3.deselect()
        checkbox5.deselect()

        labelx = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=height_of_frame6+10,text = "",justify = "left",font=("Arial",12))
        labelx.grid(column =0,row=0,pady =0,padx=10)
        
    def selected5(): #hledani paru
        clear_frame(frame6)
        console.configure(text = " ")
        view_image(5)
        checkbox.deselect()
        checkbox2.deselect()
        checkbox3.deselect()
        checkbox4.deselect()
        
        def set_pair_variable1():
            global max_num_of_pallets
            input_1 = pallets_set.get()
            if input_1.isdigit() == False:
                console_frame6_1.configure(text = "Nezadali jste číslo")
            elif int(input_1) <1:
                console_frame6_1.configure(text = "Mimo rozsah")
            else:
                console_frame6_1.configure(text = f"Počet palet nastaven na: {input_1}")
                max_num_of_pallets = input_1
                
        def set_aut_detect():
            global aut_detect_num_of_pallets
            if checkbox_aut_detect.get() == 1:
                aut_detect_num_of_pallets = True
            else:
                aut_detect_num_of_pallets = False

        label1              = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=20,text = "Nastavte počet palet v oběhu:",justify = "left",font=("Arial",12))
        pallets_set         = customtkinter.CTkEntry(master = frame6,width=150,height=30, placeholder_text= max_num_of_pallets)
        button_save1        = customtkinter.CTkButton(master = frame6,width=50,height=30, text = "Uložit", command = lambda: set_pair_variable1(),font=("Arial",12,"bold"))
        label_aut_detect    = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=60,text = "Možnost aut. detekce:\n(případ, že v cestě nechybí paleta\ns nejvyšším ID)",justify = "left",font=("Arial",12))
        checkbox_aut_detect = customtkinter.CTkCheckBox(master = frame6,height=30, text = "Automatická detekce",command=set_aut_detect)
        console_frame6_1    = customtkinter.CTkLabel(master = frame6,height=30,text = " ",justify = "left",font=("Arial",12))
        labelx              = customtkinter.CTkLabel(master = frame6,width=width_of_frame6,height=90,text = "",justify = "left",font=("Arial",12))
        label1.grid(column =0,row=0,pady =0,padx=10)
        pallets_set.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)
        button_save1.grid(column =0,row=1,sticky = tk.E,pady =0,padx=10)
        console_frame6_1.grid(column =0,row=2,pady =0,padx=10)
        label_aut_detect.grid(column =0,row=3,pady =0,padx=10)
        checkbox_aut_detect.grid(column =0,row=4,pady =0,padx=10)
        labelx.grid(column =0,row=5,pady =0,padx=10)
        checkbox_aut_detect.select()

    def selected6():
        if checkbox6.get() == 1:
            dirs_more = customtkinter.CTkImage(Image.open("images/more_dirs.png"),size=(553, 111))
            images2.configure(image =dirs_more)   
            console2.configure(text = "nebo poslední složka obsahuje soubory přímo (neroztříděné)",font=("Arial",16,"bold"))
            console2.configure(font=("Arial",12))
        else:
            dirs_one = customtkinter.CTkImage(Image.open("images/dirs_ba.png"),size=(432, 133))
            images2.configure(image =dirs_one)
            console2.configure(text = "nebo obsahuje soubory přímo (neroztříděné)",font=("Arial",16,"bold"))
            console2.configure(font=("Arial",12))

    def view_image(which_one):
        if checkbox.get()+checkbox2.get()+checkbox3.get()+checkbox4.get()+checkbox5.get() == 0:
            nothing = customtkinter.CTkImage(Image.open("images/nothing.png"),size=(1, 1))
            images.configure(image = nothing)
            name_example.configure(text = "")
        else:
            if which_one == 1:
                type_24 = customtkinter.CTkImage(Image.open("images/24_type.png"),size=(447, 170))
                images.configure(image =type_24)
                name_example.configure(text = f"221013_092241_0000000842_21_&Cam1Img  => .Height <=  .bmp\n(Podporované formáty:{supported_formats_sorting})")
            if which_one == 2:
                func_24 = customtkinter.CTkImage(Image.open("images/24_func.png"),size=(725, 170))
                images.configure(image =func_24)
                name_example.configure(text = f"221013_092241_0000000842_  => 21 <=  _&Cam1Img.Height.bmp\n(Podporované formáty:{supported_formats_sorting})")
            if which_one == 3:
                cam_24 = customtkinter.CTkImage(Image.open("images/24_cam.png"),size=(874, 170))
                images.configure(image =cam_24)
                name_example.configure(text = f"221013_092241_0000000842_21_&  => Cam1 <=  Img.Height.bmp\n(Podporované formáty:{supported_formats_sorting})")
            if which_one == 4:
                both_24 = customtkinter.CTkImage(Image.open("images/24_both.png"),size=(900, 170))
                images.configure(image =both_24)
                name_example.configure(text = f"221013_092241_0000000842_  => 21 <=  _&  => Cam1 <=  Img.Height.bmp\n(Podporované formáty:{supported_formats_sorting})")
            if which_one == 5:
                PAIRS = customtkinter.CTkImage(Image.open("images/25basic.png"),size=(530, 170))
                images.configure(image =PAIRS)
                name_example.configure(
                    text = f"Nakopíruje nalezené dvojice souborů do složky s názvem PAIRS\n(např. obsluha vloží dvakrát stejnou paletu po sobě před kameru)\n2023_04_13-07_11_09_xxxx_=> 0020 <=_&Cam2Img.Height.bmp\n(funkce postupuje podle časové známky v názvu souboru, kdy byly soubory pořízeny)\n(Podporované formáty:{supported_formats_sorting})")
    def call_menu():
        list_of_frames = [frame2,frame3,frame4,frame5,frame6]
        for frames in list_of_frames:
            frames.pack_forget()
            frames.grid_forget()
            frames.destroy()
        menu()

    frame2 = customtkinter.CTkFrame(master=root)
    frame2.pack(pady=0,padx=5,fill="both",expand=False,side = "top")
    frame5 = customtkinter.CTkScrollableFrame(master=root)
    frame5.pack(pady=0,padx=5,fill="both",expand=True,side = "bottom")
    frame3 = customtkinter.CTkFrame(master=root,width=400)
    frame3.pack(pady=10,padx=5,fill="y",expand=False,side="left")
    frame4 = customtkinter.CTkScrollableFrame(master=root)
    frame4.pack(pady=10,padx=5,fill="both",expand=True,side="right")

    height_of_frame6 = 250
    width_of_frame6 = 200
    frame6 = customtkinter.CTkFrame(master=root,height=height_of_frame6,width = width_of_frame6)
    frame6.pack(pady=10,padx=0,fill="both",expand=False,side = "bottom")

    def call_browseDirectories():
        output = browseDirectories()
        if str(output[1]) != "/":
            path_set.delete("0","200")
            path_set.insert("0", output[1])
            console.configure(text="")
            console.configure(text=f"Byla vložena cesta: {output[1]}")

    menu_button = customtkinter.CTkButton(master = frame2, width = 180, text = "MENU", command = lambda: call_menu(),font=("Arial",20,"bold"))
    menu_button.pack(pady =12,padx=10,anchor ="w",side="left")
    path_set    = customtkinter.CTkEntry(master = frame2,placeholder_text="Zadejte cestu k souborům z kamery (kde se nacházejí složky se soubory nebo soubory přímo)")
    path_set.pack(pady = 12,padx =0,anchor ="w",side="left",fill="both",expand=True)
    tree        = customtkinter.CTkButton(master = frame2, width = 180,text = "EXPLORER", command = call_browseDirectories,font=("Arial",20,"bold"))
    tree.pack(pady = 12,padx =10,anchor ="w",side="left")

    checkbox    = customtkinter.CTkCheckBox(master = frame3, text = "Třídit podle typů souborů",command = selected)
    checkbox.pack(pady =12,padx=10,anchor ="w")
    checkbox2   = customtkinter.CTkCheckBox(master = frame3, text = "Třídit podle čísla funkce (ID)",command = selected2)
    checkbox2.pack(pady =12,padx=10,anchor ="w")
    checkbox3   = customtkinter.CTkCheckBox(master = frame3, text = "Třídit podle čísla kamery",command = selected3)
    checkbox3.pack(pady =12,padx=10,anchor ="w")
    checkbox4   = customtkinter.CTkCheckBox(master = frame3, text = "Třídit podle čísla funkce i kamery",command = selected4)
    checkbox4.pack(pady =12,padx=10,anchor ="w")
    checkbox5   = customtkinter.CTkCheckBox(master = frame3, text = "Najít dvojice (soubory se stejným ID, v řadě za sebou)",command = selected5)
    checkbox5.pack(pady =12,padx=10,anchor ="w")
    #checkbox_new = customtkinter.CTkCheckBox(master = frame3, text = "Roztřídit do složek podle data",command = selected5)
    #checkbox_new.pack(pady =12,padx=10,anchor ="w")

    checkbox6   = customtkinter.CTkCheckBox(master = frame4, text = "Projít subsložky?",command = selected6)
    checkbox6.pack(pady =12,padx=10,anchor="w")
    images2     = customtkinter.CTkLabel(master = frame4,text = "")
    images2.pack()
    console2    = customtkinter.CTkLabel(master = frame4,text = " ",font=("Arial",12))
    console2.pack(pady =5,padx=10)


    images          = customtkinter.CTkLabel(master = frame5,text = "")
    images.pack()
    name_example    = customtkinter.CTkLabel(master = frame5,text = "",font=("Arial",16,"bold"))
    name_example.pack(pady = 12,padx =10)
    button          = customtkinter.CTkButton(master = frame5, text = "SPUSTIT", command = start,font=("Arial",20,"bold"))
    button.pack(pady =12,padx=10)
    button._set_dimensions(300,60)
    console         = customtkinter.CTkLabel(master = frame5,text = " ",justify = "left",font=("Arial",15))
    console.pack(pady =10,padx=10)


    #default:
    checkbox.select()
    selected()
    view_image(1)
    selected6()

    root.mainloop()

menu()