import customtkinter
import tkinter as tk
import os
import shutil
from PIL import Image, ImageTk
import threading
import json
import Converting_option_v3 as Converting
import string_database
import psutil
import sys
import win32pipe, win32file, pywintypes
import time
from tkinter import filedialog

testing = False

global_recources_load_error = False
exe_path = sys.executable
exe_name = os.path.basename(exe_path)
config_filename = "TRIMAZKON.json"
app_name = "TMK_image_browser"
app_version = "DEMO"
if testing:
    exe_name = "TMK_image_browser_test.exe"

class Tools:
    config_json_filename = config_filename

    @classmethod
    def resource_path(cls,relative_path):
        """ Get the absolute path to a resource, works for dev and for PyInstaller """
        # if hasattr(sys, '_MEIPASS'):
        #     return os.path.join(sys._MEIPASS, relative_path)
        # return os.path.join(os.path.abspath("."), relative_path)
        BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.abspath(".")
        return os.path.join(BASE_DIR, relative_path)
    
    @classmethod
    def path_check(cls,path_raw,only_repair = None):
        path=path_raw
        backslash = "\\"
        if backslash[0] in path:
            newPath = path.replace(backslash[0], '/')
            path = newPath
        if path.endswith('/') == False:
            newPath = path + "/"
            path = newPath
        #oprava mezery v nazvu
        path = r"{}".format(path)
        if not os.path.exists(path) and only_repair == None:
            return False
        else:
            return path

    @classmethod
    def create_new_json_config(cls,default_value_list,load_values_only = False):
        new_app_settings = {"default_path": default_value_list[2],
                            "maximalized": default_value_list[7],
                            "show_changelog": default_value_list[12],
                            "app_zoom": default_value_list[14],
                            "app_zoom_checkbox": default_value_list[15],
                            "tray_icon_startup": default_value_list[16],
                            # "path_history_list": default_value_list[17],
                            "default_language": default_value_list[17],}
        
        new_sort_conv_settings = {"supported_formats_sorting": default_value_list[0],
                                "prefix_function": default_value_list[5],
                                "prefix_camera": default_value_list[6],
                                "max_pallets": default_value_list[8],
                                "temp_dir_name": default_value_list[9][0],
                                "pairs_dir_name": default_value_list[9][1],
                                "convert_bmp_dir_name": default_value_list[9][3],
                                "convert_jpg_dir_name": default_value_list[9][4],
                                "sorting_safe_mode": default_value_list[10],
                                "path_history_list": default_value_list[18],
                                "path_history_list_conv": default_value_list[18],}
        
        new_del_settings = {"supported_formats_deleting": default_value_list[1],
                            "default_files_to_keep": default_value_list[3],
                            "default_cutoff_date": default_value_list[4],
                            "to_delete_dir_name": default_value_list[9][2],
                            "path_history_list": default_value_list[19],}
        
        new_image_browser_settings = {"selected_option": default_value_list[11][0],
                                    "zoom_step": default_value_list[11][1],
                                    "movement_step": default_value_list[11][2],
                                    "show_image_film": default_value_list[11][3],
                                    "image_film_count": default_value_list[11][4],
                                    "copyed_dir_name": default_value_list[9][5],
                                    "moved_dir_name": default_value_list[9][6],
                                    "path_history_list": default_value_list[20],}
        
        new_catalogue_settings = {"database_filename": default_value_list[13][0],
                                "catalogue_filename": default_value_list[13][1],
                                "metadata_filename": default_value_list[13][2],
                                "subwindow_behav": default_value_list[13][3],
                                "default_export_suffix": default_value_list[13][4],
                                "default_path": default_value_list[13][5],
                                "render_mode": default_value_list[13][6],
                                "path_history_list": default_value_list[21],}
        
        new_ip_settings = {"default_ip_interface": default_value_list[22][0],
                            "favorite_ip_window_status": default_value_list[22][1],
                            "disk_or_ip_window": default_value_list[22][2],
                            "default_window_size": default_value_list[22][3],
                            "init_disk_refresh": default_value_list[22][4],
                            "editable_notes": default_value_list[22][5],
                            "disk_persistent": default_value_list[22][6],
                            "auto_order_when_edit": default_value_list[22][7],
                            "ask_to_delete": default_value_list[22][8],}
        
        output_object = {"app_settings": new_app_settings,
                       "sort_conv_settings": new_sort_conv_settings,
                       "del_settings": new_del_settings,
                       "image_browser_settings": new_image_browser_settings,
                       "catalogue_settings": new_catalogue_settings,
                       "ip_settings": new_ip_settings}
        
        if load_values_only:
            return output_object

        with open(initial_path+cls.config_json_filename, "w") as file:
            json.dump(output_object, file, indent=4)
        
        return output_object

    @classmethod
    def read_json_config(cls): # Funkce vraci data z configu
        """
        Funkce vrací data z konfiguračního souboru

        data jsou v pořadí:

        APP SETTINGS\n
        - default_path
        - maximalized
        - show_changelog
        - app_zoom
        - app_zoom_checkbox
        - tray_icon_startup
        - default_language
        \nSORT AND CONV SETTINGS\n
        - supported_formats_sorting
        - prefix_function
        - prefix_camera
        - max_pallets
        - temp_dir_name
        - pairs_dir_name
        - convert_bmp_dir_name
        - convert_jpg_dir_name
        - sorting_safe_mode
        - path_history_list
        \nDEL SETTINGS\n
        - supported_formats_deleting
        - default_files_to_keep
        - default_cutoff_date
        - to_delete_dir_name
        - path_history_list
        \nIMAGE BROWSER SETTINGS\n
        - selected_option
        - zoom_step
        - movement_step
        - show_image_film
        - image_film_count
        - copyed_dir_name
        - moved_dir_name
        - path_history_list
        \nCATALOGUE SETTINGS\n
        - database_filename
        - catalogue_filename
        - metadata_filename
        - subwindow_behav
        - default_export_suffix
        - default_path
        - render_mode
        - path_history_list
        \nIP SETTINGS\n
        - default_ip_interface
        - favorite_ip_window_status
        - disk_or_ip_window
        - default_window_size
        - init_disk_refresh
        - editable_notes
        - disk_persistent
        - auto_order_when_edit
        - ask_to_delete
        """
        global global_recources_load_error
        default_setting_parameters = string_database.default_setting_database_param
        # default_labels = string_database.default_setting_database

        if os.path.exists(initial_path+cls.config_json_filename):
            try:
                output_data = []
                with open(initial_path+cls.config_json_filename, "r") as file:
                    output_data = json.load(file)

                # print("config data: ", output_data, len(output_data))
                return output_data

            except Exception as e:
                print(f"Nejdřív zavřete soubor {cls.config_json_filename} Chyba: {e}")   
                print("Budou načteny defaultní hodnoty")
                global_recources_load_error = True
                output_array = Tools.create_new_json_config(default_setting_parameters,load_values_only=True)
                return output_array
        else:
            print(f"Chybí konfigurační soubor {cls.config_json_filename}, bude vytvořen")
            output_array = Tools.create_new_json_config(default_setting_parameters)
            return output_array

    @classmethod
    def save_to_json_config(cls,input_data,which_settings,which_parameter,language_force = "cz"): # Funkce zapisuje data do souboru configu
        """
        Funkce zapisuje data do konfiguračního souboru

        vraci vystupni zpravu: report

        which_settings je bud: 
        - app_settings
        - sort_conv_settings
        - del_settings
        - image_browser_settings
        - catalogue_settings
        - ip_settings

        \nwhich_parameter je bud:
        \nAPP_SETTINGS\n
        - default_path
        - maximalized
        - show_changelog
        - app_zoom
        - app_zoom_checkbox
        - tray_icon_startup
        - default_language
        \nSORT_CONV_SETTINGS\n
        - supported_formats_sorting
        - prefix_function
        - prefix_camera
        - max_pallets
        - temp_dir_name
        - pairs_dir_name
        - convert_bmp_dir_name
        - convert_jpg_dir_name
        - sorting_safe_mode
        - path_history_list
        \nDEL_SETTINGS\n
        - supported_formats_deleting
        - default_files_to_keep
        - default_cutoff_date
        - to_delete_dir_name
        - path_history_list
        \nIMAGE_BROWSER_SETTINGS\n
        - selected_option
        - zoom_step
        - movement_step
        - show_image_film
        - image_film_count
        - copyed_dir_name
        - moved_dir_name
        - path_history_list
        \nCATALOGUE_SETTINGS\n
        - database_filename
        - catalogue_filename
        - metadata_filename
        - subwindow_behav
        - default_export_suffix
        - default_path
        - render_mode
        \nIP_SETTINGS\n
        - default_ip_interface
        - favorite_ip_window_status
        - disk_or_ip_window
        - default_window_size
        - init_disk_refresh
        - editable_notes
        - disk_persistent
        - auto_order_when_edit
        - ask_to_delete
        """

        def filter_unwanted_chars(to_filter_data, directory = False,formats = False):
            unwanted_chars = ["\n","\"","\'","[","]"]
            if directory:
                unwanted_chars = ["\n","\"","\'","[","]","\\","/"]
            if formats:
                unwanted_chars = ["\n","\"","\'","[","]"," ",".","/","\\"]

            filtered_data = ""
            for letters in to_filter_data:
                if letters not in unwanted_chars:
                    filtered_data += letters
            return filtered_data
        
        def get_input_data_format():
            if isinstance(input_data,list):
                return input_data
            elif isinstance(input_data,str):
                return str(input_data)
            elif isinstance(input_data,int):
                return int(input_data)
        
        if os.path.exists(initial_path + cls.config_json_filename):
            with open(initial_path+cls.config_json_filename, "r") as file:
                config_data = json.load(file)

            report = ""
            if which_settings == "app_settings":
                if which_parameter == "default_path":
                    report = (f"Základní cesta přenastavena na: {str(input_data)}")
                config_data[which_settings][which_parameter] = get_input_data_format()

            elif which_settings == "sort_conv_settings":
                supported_formats_sorting = config_data[which_settings]["supported_formats_sorting"]
                print("found formats: ", supported_formats_sorting)

                if which_parameter == "add_supported_sorting_formats":
                    corrected_input = filter_unwanted_chars(str(input_data),formats=True)
                    if str(corrected_input) not in supported_formats_sorting:
                        supported_formats_sorting.append(str(corrected_input))
                        report =  (f"Byl přidán formát: \"{corrected_input}\" do podporovaných formátů pro možnosti třídění")
                        if language_force == "en":
                            report =  (f"Added format: \"{corrected_input}\" to supported formats for sorting options")
                        # rewrite_value("supported_formats_sorting",supported_formats_sorting)
                        config_data[which_settings]["supported_formats_sorting"] = supported_formats_sorting
                    else:
                        report =  (f"Formát: \"{corrected_input}\" je již součástí podporovaných formátů možností třídění")
                        if language_force == "en":
                            report =  (f"Format: \"{corrected_input}\" is already part of the supported sorting option formats")
                    
                elif which_parameter == "pop_supported_sorting_formats":
                    # poped = 0
                    found = False
                    range_to = len(supported_formats_sorting)
                    for i in range(0,range_to):
                        if i < range_to:
                            if str(input_data) == supported_formats_sorting[i] and len(str(input_data)) == len(supported_formats_sorting[i]):
                                supported_formats_sorting.pop(i)
                                report =  (f"Z podporovaných formátů možností třídění byl odstraněn formát: \".{input_data}\"")
                                if language_force == "en":
                                    report =  (f"The format \".{input_data}\" has been removed from the supported sorting option formats")
                                found = True
                                # rewrite_value("supported_formats_sorting",supported_formats_sorting)
                                config_data[which_settings]["supported_formats_sorting"] = supported_formats_sorting
                                break

                    if found == False:
                        report =  (f"Formát: \"{input_data}\" nebyl nalezen v podporovaných formátech možností třídění, nemůže tedy být odstraněn")
                        if language_force == "en":
                            report =  (f"The format \".{input_data}\" was not found in the supported sorting option formats, so it cannot be deleted")

                else:
                    config_data[which_settings][which_parameter] = get_input_data_format()

            elif which_settings == "del_settings":
                supported_formats_deleting = config_data[which_settings]["supported_formats_deleting"]
                print("found formats: ", supported_formats_deleting)

                if which_parameter == "add_supported_deleting_formats":
                    corrected_input = filter_unwanted_chars(str(input_data),formats=True)
                    if str(corrected_input) not in supported_formats_deleting:
                        supported_formats_deleting.append(str(corrected_input))
                        report =  (f"Byl přidán formát: \"{corrected_input}\" do podporovaných formátů pro možnosti mazání")
                        if language_force == "en":
                            report =  (f"Added format: \"{corrected_input}\" to supported formats for deletion options")
                        # rewrite_value("supported_formats_deleting",supported_formats_deleting)
                        config_data[which_settings]["supported_formats_deleting"] = supported_formats_deleting
                    else:
                        report =  (f"Formát: \"{corrected_input}\" je již součástí podporovaných formátů možností mazání")
                        if language_force == "en":
                            report =  (f"Format: \"{corrected_input}\" is already part of the supported delete option formats")
                    
                elif which_parameter == "pop_supported_deleting_formats":
                    # poped = 0
                    found = False
                    range_to = len(supported_formats_deleting)
                    for i in range(0,range_to):
                        if i < range_to:
                            if str(input_data) == supported_formats_deleting[i] and len(str(input_data)) == len(supported_formats_deleting[i]):
                                supported_formats_deleting.pop(i)
                                report =  (f"Z podporovaných formátů možností mazání byl odstraněn formát: \".{input_data}\"")
                                if language_force == "en":
                                    report =  (f"The format \".{input_data}\" has been removed from the supported delete option formats")
                                found = True
                                # rewrite_value("supported_formats_deleting",supported_formats_deleting)
                                config_data[which_settings]["supported_formats_deleting"] = supported_formats_deleting
                                break

                    if found == False:
                        report =  (f"Formát: \"{input_data}\" nebyl nalezen v podporovaných formátech možností mazání, nemůže tedy být odstraněn")
                        if language_force == "en":
                            report =  (f"The format \".{input_data}\" was not found in the supported delete option formats, so it cannot be deleted")
                
                else:
                    config_data[which_settings][which_parameter] = get_input_data_format()

            elif which_settings == "image_browser_settings":
                config_data[which_settings][which_parameter] = get_input_data_format()

            elif which_settings == "catalogue_settings":
                config_data[which_settings][which_parameter] = get_input_data_format()

            elif which_settings == "ip_settings":
                config_data[which_settings][which_parameter] = get_input_data_format()
                              
            with open(initial_path+cls.config_json_filename, "w") as file:
                json.dump(config_data, file, indent=4)

            return report
        
        else:
            print("Chybí konfigurační soubor (nelze ukládat změny)")
            return "Chybí konfigurační soubor (nelze ukládat změny)"
   
    @classmethod
    def get_all_app_processes(cls):
        pid_list = []
        num_of_apps = 0
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == exe_name:
                pid_list.append(process.info['pid'])
                num_of_apps+=1
        
        return [num_of_apps,pid_list]

    @classmethod
    def check_runing_app_duplicity(cls):
        """
        Spočte procesy a názvem aplikace, pokud je jich více, jak 2 je již aplikace spuštěná
        - v top případě zajistí aby se nenačítalo gui a pouze zajistí odeslání paramterů pro image browser
        """
        found_processes = Tools.get_all_app_processes()
        print(found_processes)
        if found_processes[0] > 2:
            return True
        else:
            return False
        
    @classmethod
    def add_colored_line(cls,text_widget, text, color,font=None,delete_line = None,no_indent=None,sameline=False):
        """
        Vloží řádek do console
        """
        try:
            text_widget.configure(state=tk.NORMAL)
            if font == None:
                font = ("Arial",16)
            if delete_line != None:
                text_widget.delete("current linestart","current lineend")
                text_widget.tag_configure(color, foreground=color,font=font)
                text_widget.insert("current lineend",text, color)
            else:
                text_widget.tag_configure(color, foreground=color,font=font)
                if no_indent:
                    if sameline:
                        text_widget.insert(tk.END,text, color)
                    else:
                        text_widget.insert(tk.END,text+"\n", color)
                else:
                    if sameline:
                        text_widget.insert(tk.END,"    > "+ text, color)
                    else:
                        text_widget.insert(tk.END,"    > "+ text+"\n", color)

            text_widget.configure(state=tk.DISABLED)
        except Exception as e:
            print(f"Error při psaní do konzole: {e}")

    @classmethod
    def add_new_path_to_history(cls,new_path,which_settings):
        if new_path == "delete_history":
            Tools.save_to_json_config([],which_settings,"path_history_list")
            return
        elif new_path == "delete_history_conv":
            Tools.save_to_json_config([],which_settings,"path_history_list_conv")
            return

        if which_settings == "convert_settings":
            which_settings = "sort_conv_settings"
            parameter_name = "path_history_list_conv"
        else:
            parameter_name = "path_history_list"

        current_paths = Tools.read_json_config()[which_settings][parameter_name]
        if new_path not in current_paths:
            if len(current_paths) > 9:
                current_paths.pop()
            # current_paths.append(str(new_path))
            current_paths.insert(0,str(new_path))
            Tools.save_to_json_config(current_paths,which_settings,parameter_name)

    @classmethod
    def get_init_path(cls):
        initial_path = Tools.path_check(os.getcwd())
        if len(sys.argv) > 1: #spousteni pres cmd (kliknuti na obrazek) nebo task scheduler - mazání
            raw_path = str(sys.argv[0])
            initial_path = Tools.path_check(raw_path,True)
            initial_path_splitted = initial_path.split("/")
            initial_path = ""
            for i in range(0,len(initial_path_splitted)-2):
                initial_path += str(initial_path_splitted[i])+"/"

        initial_path.replace("//","/")
        return initial_path
    
    @classmethod
    def browseDirectories(cls,visible_files,start_path=None): # Funkce spouští průzkumníka systému windows pro definování cesty, kde má program pracovat
        """
        Funkce spouští průzkumníka systému windows pro definování cesty, kde má program pracovat

        Vstupní data:

        0: visible_files = "all" / "only_dirs"\n
        1: start_path = None -optimalni, docasne se ulozi posledni nastavena cesta v exploreru

        Výstupní data:

        0: výstupní chybová hlášení
        1: opravená cesta
        2: nazev vybraneho souboru (option: all)
        """
        corrected_path = ""
        output= ""
        name_of_selected_file = ""

        if start_path == None:
            start_path = Tools.read_json_config()["app_settings"]["default_path"] #defaultni cesta
        else: # byla zadana docasna cesta pro explorer
            checked_path = Tools.path_check(start_path)
            if checked_path == False:
                output = "Změněná dočasná základní cesta pro explorer již neexistuje"
                start_path = Tools.read_json_config()["app_settings"]["default_path"] #defaultni cesta
            else:
                start_path = checked_path

        if start_path != False:
            if not os.path.exists(start_path):
                start_path = ""
                output="Konfigurační soubor obsahuje neplatnou cestu"

        else:
            output="Chybí konfigurační soubor s počáteční cestou...\n"
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
                            name_of_selected_file = parts
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
                            name_of_selected_file = parts
                else:
                    output = "Přes explorer nebyla vložena žádná cesta"

        # pripad vyberu slozek
        if visible_files == "only_dirs":
            if(start_path != ""):
                path_to_directory = filedialog.askdirectory(initialdir = start_path, title = "Vyberte adresář")
                if path_to_directory == None or path_to_directory == "":
                    output = "Přes explorer nebyla vložena žádná cesta"
            else:
                path_to_directory = filedialog.askdirectory(initialdir = "/", title = "Vyberte adresář")
                if path_to_directory == None or path_to_directory == "":
                    output = "Přes explorer nebyla vložena žádná cesta"

        check = Tools.path_check(path_to_directory)
        corrected_path = check
        return [output,corrected_path,name_of_selected_file]

class system_pipeline_communication: # vytvoření pipeline serveru s pipe názvem TMK_image_browser_pipe_ + pid (id systémového procesu)
    """
    aby bylo možné posílat běžící aplikaci parametry:
    - mám otevřené okno ip setting - kliknu na obrázek - jen pošlu parametry
    """
    def __init__(self,exe_name,no_server = False):
        self.root = None #define later (to prevend gui loading when 2 apps opened)
        # self.current_pid = None
        self.exe_name = exe_name
        self.current_pid = os.getpid()
        if not no_server:
            # self.start_server()
            run_server_background = threading.Thread(target=self.start_server,)
            run_server_background.start()

    def check_root_existence(self,root_given):
        try:
            if root_given.winfo_exists():
                return True
        except Exception as e:
            # if "main thread is not in main loop" in str(e):
            # new_root = start_new_root()
            return False

    def server(self,pipe_input):
        """
        Endless loop listening for commands
        """
        pipe_name = fr'\\.\pipe\{pipe_input}'
        while True:
            print(f"Waiting for a {app_name} to connect on {pipe_name}...") 
            pipe = win32pipe.CreateNamedPipe(
                pipe_name,
                win32pipe.PIPE_ACCESS_DUPLEX,
                win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                1,
                512,
                512,
                0,
                None
            )

            win32pipe.ConnectNamedPipe(pipe, None)
            print(f"{app_name} connected.")

            try:
                while True:
                    hr, data = win32file.ReadFile(pipe, 64 * 1024)
                    received_data = data.decode()
                    print(f"Received: {received_data}")
                    try:
                        global root
                    except Exception as e:
                        print(e)

                    try:
                        global menu
                    except Exception as e:
                        print(e)

                    if "Open image browser starting with image" in received_data:
                        received_params = received_data.split("|||")
                        # global root
                        root_existance = self.check_root_existence(root)
                        print("root_status: ",root_existance)

                        if root_existance == True:
                            try:
                                root.deiconify()
                                root.update_idletasks()
                            except Exception as e:
                                print(e)
                            # global menu
                            # menu = main_menu(root)
                            root.after(100,lambda: menu.menu(clear_root=True))
                            root.after(200,menu.command_landed,received_params)

            except pywintypes.error as e:
                if e.args[0] == 109:  # ERROR_BROKEN_PIPE
                    print(f"{app_name} disconnected.")
            finally:
                # Close the pipe after disconnection
                win32file.CloseHandle(pipe)
            # Loop back to wait for new client connections

    def client(self,pipe_name_given,command,parameters):
        """
        odesílá zprávu
        """
        pipe_name = fr'\\.\pipe\{pipe_name_given}'
        print("client_pipe_name: ",pipe_name,command,parameters)
        handle = win32file.CreateFile(
            pipe_name,
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None
        )

        if "Open image browser starting with image:" in str(command):
            message = str(command) + "|||"
            for params in parameters:
                message = message + str(params) + "|||"
            print("Message sent.",message)
            win32file.WriteFile(handle, message.encode())

    def start_server(self):
        self.pipe_name = f"{app_name}_pipe_{self.current_pid}"
        running_server = threading.Thread(target=self.server, args=(self.pipe_name,),daemon=True)
        # running_server = threading.Thread(target=self.server, args=(pipe_name,))
        running_server.start()
        time.sleep(0.5)  # Wait for the server to start

    def call_checking(self,command,parameters):
        """
        for every found process with name of an application: send given command
        """
        checking = Tools.get_all_app_processes()
        print("SYSTEM application processes: ",checking)
        # if it is running more then one application, execute (root + self.root)
        # if checking[0]>1:
        pid_list = checking[1]
        # try to send command to every process which has application name
        for pids in pid_list:
            if pids != self.current_pid:
                try:
                    pipe_name = f"{app_name}_pipe_{pids}"
                    print("calling client",pipe_name,command,parameters)
                    self.client(pipe_name,command,parameters)
                except Exception:
                    pass
        return True

initial_path = Tools.get_init_path()
print("init path: ",initial_path)
app_icon = Tools.resource_path('images/logo_TRIMAZKON.ico')
app_running_status = Tools.check_runing_app_duplicity()
print("already opened app status: ",app_running_status)

if not app_running_status:
    pipeline_duplex = system_pipeline_communication(exe_name)# Establishment of pipeline server for duplex communication between running applications
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    root=customtkinter.CTk()
    root.geometry("1200x900")
    root.title(f"{app_name} v_{app_version}")
    root.wm_iconbitmap(Tools.resource_path(app_icon))
    if Tools.read_json_config()["app_settings"]["maximalized"]  == "ano":
         root.after(0, lambda:root.state('zoomed')) # max zoom, porad v okne


else:# předání parametrů v případě spuštění obrázkem (základní obrázkový prohlížeč)
    pipeline_duplex_instance = system_pipeline_communication(exe_name,no_server=True) # pokud už je aplikace spuštěná nezapínej server, trvá to...
    if len(sys.argv) > 1:
        raw_path = str(sys.argv[1]) #klik na spusteni trimazkonu s admin právy
        if sys.argv[0] != sys.argv[1]: # pokud se nerovnají jedná se nejspíše o volání základního prohlížeče obrázků (spuštění kliknutím na obrázek...)
            IB_as_def_browser_path=Tools.path_check(raw_path,True)
            IB_as_def_browser_path_splitted = IB_as_def_browser_path.split("/")
            IB_as_def_browser_path = ""
            for i in range(0,len(IB_as_def_browser_path_splitted)-2):
                IB_as_def_browser_path += IB_as_def_browser_path_splitted[i]+"/"
            selected_image = IB_as_def_browser_path_splitted[len(IB_as_def_browser_path_splitted)-2]
            pipeline_duplex_instance.call_checking(f"Open image browser starting with image: {IB_as_def_browser_path}, {selected_image}",[IB_as_def_browser_path,selected_image])

class Image_browser: # Umožňuje procházet obrázky a přitom například vybrané přesouvat do jiné složky
    """
    Umožňuje procházet obrázky a přitom například vybrané přesouvat do jiné složky

    - umožňuje: měnit rychlost přehrávání, přiblížení, otočení obrázku
    - reaguje na klávesové zkratky
    """
    def __init__(self,root,IB_as_def_browser_path = None,selected_image = "",path_given = "",params_given = None):
        self.root = root
        self.path_given = path_given
        self.IB_as_def_browser_path = IB_as_def_browser_path
        self.all_images = []
        self.increment_of_image = 0
        self.state = "stop"
        self.rotation_angle = 0.0
        config_data = Tools.read_json_config()
        self.config_path = config_data["app_settings"]["default_path"]
        self.copy_dir = config_data["image_browser_settings"]["copyed_dir_name"]
        self.move_dir = config_data["image_browser_settings"]["moved_dir_name"]
        self.chosen_option = config_data["image_browser_settings"]["selected_option"]
        self.zoom_increment = config_data["image_browser_settings"]["zoom_step"]
        self.drag_increment = config_data["image_browser_settings"]["movement_step"]
        self.number_of_film_images = config_data["image_browser_settings"]["image_film_count"]

        self.image_browser_path = ""
        self.unbind_list = []
        self.image_extensions = ['.jpg', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi',
                    '.png', '.gif', '.bmp', '.tiff', '.tif', '.ico', '.webp',
                    '.raw', '.cr2', '.nef', '.arw', '.dng', ".ifz"]
        self.previous_zoom = 1
        self.selected_image = selected_image
        self.path_for_explorer = None
        self.temp_bmp_folder = "temp_bmp"
        self.ifz_located = None
        self.converted_images = []
        self.increment_of_ifz_image = 0
        self.default_path = ""
        self.previous_height = 0
        self.previous_width = 0
        if config_data["image_browser_settings"]["show_image_film"] == "ne":
            self.image_film = False
        else:
            self.image_film = True
        self.image_queue = [""]*((self.number_of_film_images*2)+1)
        self.flow_direction = ""
        self.ifz_count = 1
        self.count_of_ifz_images_defined = False
        self.name_hide_index = 0
        self.main_image = None
        self.main_image2 = None
        self.drag_option_binded = False
        self.drawing_color = "#000000"
        self.drawing_thickness = 5
        self.draw_mode = "line"
        self.x_growth_multiplier = 0.5
        self.y_growth_multiplier = 0.5
        self.image_dimensions = (0,0)
        self.last_coords = (0,0)
        self.zoom_given = 100
        self.settings_applied = False
        self.loaded_image_status = True
        self.inserted_path_history = config_data["image_browser_settings"]["path_history_list"]
        self.last_frame_dim = [0,0]

        if params_given != None:
            print("params given",params_given)
            coords_given = params_given[0]
            zoom_given = params_given[1]
            self.last_coords = coords_given
            self.zoom_given = zoom_given
            self.settings_applied = True
        self.create_widgets()
        
    def clear_frame(self,frame):
        try:
            children = frame.winfo_children()
        except Exception:
            return
        for widget in children:
            widget.destroy()

    def get_images(self,path):  # Seznam všech obrázků v podporovaném formátu (včetně cesty)
        """
        Seznam všech obrázků v podporovaném formátu (včetně cesty)
        """
        self.ifz_located = None
        list_of_files_to_view = []
        for files in os.listdir(path):
            files_split = files.split(".")
            if ("."+files_split[len(files_split)-1]) in self.image_extensions:
                list_of_files_to_view.append(path + files)
                if ("."+files_split[len(files_split)-1]) == ".ifz":
                    self.ifz_located = True
        return list_of_files_to_view

    def convert_files(self):
        if self.image_film == False:
            name_of_file = self.all_images[self.increment_of_image].split("/")
            name_of_file = name_of_file[len(name_of_file)-1]
            #vytvoreni temp slozky:
            if os.path.exists(self.default_path + self.temp_bmp_folder):
                shutil.rmtree(self.default_path + self.temp_bmp_folder) # vycistit
                os.mkdir(self.default_path + self.temp_bmp_folder)
            else:
                os.mkdir(self.default_path + self.temp_bmp_folder)

            Converting.whole_converting_function(self.default_path,"bmp",self.temp_bmp_folder,None,True,name_of_file)
            self.converted_images = []
            for files in os.listdir(self.default_path + self.temp_bmp_folder):
                if (self.default_path + self.temp_bmp_folder + "/" + files) not in self.converted_images:
                    self.converted_images.append(self.default_path + self.temp_bmp_folder + "/" + files)

        elif self.image_film == True:
            #uvazuje se, ze konvertovane obrazky budou koncit: _x.bmp, kde x bude nabyvat maximalne hodnot 0-8 nebo bez _x ...
            #1) uprava nazvu pro konvertovani
            names_of_files_to_be_converted = []
            num_of_preload_images = len(self.image_queue)-1
            for i in range(0,len(self.image_queue)):
                image_index = int(self.increment_of_image+i-(num_of_preload_images/2))
                if image_index < 0:
                    image_index = len(self.all_images) + image_index
                elif image_index > len(self.all_images)-1:
                    image_index = 0 + (image_index-len(self.all_images))
                name_of_file = self.all_images[image_index].split("/")
                name_of_file = name_of_file[len(name_of_file)-1]
                names_of_files_to_be_converted.append(name_of_file)
            #2) vytvareni temp slozky
            found_files=[]
            if not os.path.exists(self.default_path + self.temp_bmp_folder):
                os.mkdir(self.default_path + self.temp_bmp_folder)
            else:
                for files in os.listdir(self.default_path + self.temp_bmp_folder):
                    if ".bmp" in files and files[-6:-5] == "_":
                        found_files.append(files[:-6])
                    elif ".bmp" in files:
                        found_files.append(files[:-4])
            #3) check jestli uz neni konvertovane
            to_convert =[]
            for i in range(0,len(names_of_files_to_be_converted)):
                if names_of_files_to_be_converted[i][:-4] not in found_files: #_x (x muze nabyvat max hodnoty 8)
                    to_convert.append(names_of_files_to_be_converted[i])

            #4) volani funkce pro konvertovani
            Converting.whole_converting_function(self.default_path,"bmp",self.temp_bmp_folder,None,True,to_convert)

            #5) definice poctu ifz
            if self.count_of_ifz_images_defined == False:
                self.name_hide_index = 0
                largest_ifz_num = 1
                for files in os.listdir(self.default_path + self.temp_bmp_folder):
                    # urcovani poctu ifz v jednom souboru (vykonat pouze jednou pro vsechny soubory
                    if files[-6:-5] == "_":
                        if files[-5:-4].isdigit():
                            if int(files[-5:-4]) +1 > largest_ifz_num:
                                largest_ifz_num = int(files[-5:-4])+1
                    else:
                        #nenalezeny zadne dalsi ifz podobrazky
                        self.name_hide_index = 2
                self.ifz_count = largest_ifz_num
                self.count_of_ifz_images_defined = True

            #6) mazani nepotrebnych
            for files in os.listdir(self.default_path + self.temp_bmp_folder):
                if (str(files[:(-6+self.name_hide_index)])+".ifz") not in names_of_files_to_be_converted:
                    try:
                        os.remove(self.default_path + self.temp_bmp_folder + "/" + files)
                    except Exception:
                        pass
                    # print("deleting",files)

            #8) plneni pole s kompletni cestou ve spravnem poradi...
            self.converted_images = []
            for i in range(0,len(names_of_files_to_be_converted)):
                matches_made = 0
                for files in os.listdir(self.default_path + self.temp_bmp_folder):
                    if ((self.default_path + self.temp_bmp_folder + "/" + files) not in self.converted_images):
                        if names_of_files_to_be_converted[i] == files[:(-6+self.name_hide_index)]+".ifz":
                            self.converted_images.append(self.default_path + self.temp_bmp_folder + "/" + files)   
                            matches_made += 1
                            #pro zefektivnění:
                            if matches_made == self.ifz_count:
                                break
                             
    def make_image_film_widgets(self):
        def mouse_wheel2(e): # posouvat obrazky
            direction = -e.delta
            if direction < 0:
                self.next_image()
            else:
                self.previous_image()
            
        if len(self.image_queue)>len(self.all_images):
            self.image_queue = [""]*(len(self.all_images))
            if len(self.image_queue) % 2 == 0: #nesmi byt sudé...
                self.image_queue.append("") #kdyztak prictu jeste jeden prvek... append
        else:
            self.image_queue = [""]*((self.number_of_film_images*2)+1)
        
        self.left_labels = [""]*int((len(self.image_queue)-1)/2)
        self.right_labels = [""]*int((len(self.image_queue)-1)/2)
        self.clear_frame(self.image_film_frame_left)
        self.clear_frame(self.image_film_frame_right)

        for i in range(0,len(self.left_labels)):
            self.left_labels[len(self.left_labels)-i-1] = customtkinter.CTkLabel(master = self.image_film_frame_left,text = "")
            self.left_labels[len(self.left_labels)-i-1].bind("<MouseWheel>",mouse_wheel2)
            self.left_labels[len(self.left_labels)-i-1].pack(side = "right",padx=5)
            self.right_labels[i] = customtkinter.CTkLabel(master = self.image_film_frame_right,text = "")
            self.right_labels[i].bind("<MouseWheel>",mouse_wheel2)
            self.right_labels[i].pack(side = "left",padx=5)

    def start(self,path): # Ověřování cesty, init, spuštění
        """
        Ověřování cesty, init, spuštění
        """
        path_found = True
        self.count_of_ifz_images_defined = False
        if path == "" or path == "/": #pripad, ze bylo pouzito tlacitko spusteni manualne vlozene cesty a nebo je chyba v config souboru
            path_found = False
            path = self.path_set.get()
            if path != "":
                check = Tools.path_check(path)
                if check == False:
                    Tools.add_colored_line(self.console,"Zadaná cesta: "+str(path)+" nebyla nalezena","red",None,True)
                else:
                    path = check
                    path_found = True
            else:
                Tools.add_colored_line(self.console,"Nebyla vložena cesta k souborům","red",None,True)

        if os.path.isdir(path) == False: # pokud se nejedna o slozku - je mozne, ze je vlozeny nazev souboru pro zobrazeni, jako prvni
            if os.path.exists(path):
                if path.endswith("/"):
                    path = path[0:len(path)-1]
                path_splitted = path.split("/")
                self.selected_image = path_splitted[len(path_splitted)-1]
                new_path = ""
                i = 0
                for frags in path_splitted:
                    i += 1
                    if i < len(path_splitted):
                        new_path = new_path + frags + "/"

                path = new_path
            else:
                path_found = False
                Tools.add_colored_line(self.console,"Zadaná cesta: "+str(path)+" neobsahuje žádné obrázky","red",None,True)
        #automaticky okamzite otevre prvni z obrazku v dane ceste
        if path_found == True:
            if os.path.exists(path):
                #path = path.replace(" ","")
                while path.endswith(" "):
                    path = path[:len(path)-1]

                if path.endswith("/") == False:
                    path = path + "/"
                    self.path_set.delete("0","300")
                    self.path_set.insert("0",path)
                #oprava mezery v nazvu
                full_path = r"{}".format(path)
                path = full_path
                self.path_for_explorer = path
                self.all_images = self.get_images(path)
                if len(self.all_images) != 0:
                    self.image_browser_path = path
                    path_to_add_to_history = self.image_browser_path
                    # Tools.add_colored_line(self.console,f"Vložena cesta: {path}","green",None,True)
                    if self.image_film == True:
                        self.make_image_film_widgets()
                    if self.ifz_located == None:
                        if self.selected_image == "": 
                            #zobrazit hned prvni obrazek po vlozene ceste
                            self.increment_of_image = 0
                        else:
                            #zobrazit obrazek vybrany v exploreru
                            self.increment_of_image = self.all_images.index(path+self.selected_image)

                        self.view_image(self.increment_of_image)
                        if path not in self.inserted_path_history:
                            self.inserted_path_history.insert(0,path)
                            Tools.add_new_path_to_history(path,"image_browser_settings")
                        self.current_image_num.configure(text ="/" + str(len(self.all_images)))
                        self.changable_image_num.delete("0","100")
                        self.changable_image_num.insert("0", str(self.increment_of_image+1))
                    else: # Nejprve prevest do bmp formatu
                        if self.selected_image == "": 
                            #zobrazit hned prvni obrazek po vlozene ceste
                            self.increment_of_image = 0
                        else:
                            #zobrazit obrazek vybrany v exploreru
                            self.increment_of_image = self.all_images.index(path+self.selected_image)
                        self.default_path = r"{}".format(path)
                        path_to_add_to_history = self.default_path
                        self.convert_files()
                        center_image_index = int((len(self.image_queue)-1)/2) * self.ifz_count
                        self.view_image(None,self.converted_images[center_image_index + self.increment_of_ifz_image])
                        self.current_image_num.configure(text ="/" + str(len(self.all_images)))
                        self.changable_image_num.delete("0","100")
                        self.changable_image_num.insert("0", str(self.increment_of_image+1))
                        self.current_image_num_ifz.configure(text ="/" + str(self.ifz_count))
                        self.changable_image_num_ifz.delete("0","100")
                        self.changable_image_num_ifz.insert("0", str(self.increment_of_ifz_image+1))
                    if path_to_add_to_history not in self.inserted_path_history:
                        self.inserted_path_history.insert(0,path_to_add_to_history)
                        Tools.add_new_path_to_history(path_to_add_to_history,"image_browser_settings")
                else:
                    Tools.add_colored_line(self.console,"- V zadané cestě nebyly nalezeny obrázky","red",None,True)
            else:
                Tools.add_colored_line(self.console,"- Vložená cesta je neplatná","red",None,True)

    def call_browseDirectories(self): # Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
        """
        Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
        """
        if self.path_for_explorer != None:
            output = Tools.browseDirectories("all",self.path_for_explorer)
        else:
            output = Tools.browseDirectories("all")
        if str(output[1]) != "/":
            self.path_set.delete("0","200")
            self.path_set.insert("0", output[1])
            Tools.add_colored_line(self.console,f"Byla vložena cesta: {output[1]}","white",None,True)
            self.selected_image = output[2]
            
            if os.path.exists(self.default_path + self.temp_bmp_folder):
                shutil.rmtree(self.default_path + self.temp_bmp_folder) # vycistit
            self.increment_of_ifz_image = 0
            self.changable_image_num_ifz.delete("0","100")
            self.changable_image_num_ifz.insert("0",0)
            # self.image_queue = [""]*((self.number_of_film_images*2)+1)
            if len(self.image_queue)>len(self.all_images):
                self.image_queue = [""]*(len(self.all_images))
                if len(self.image_queue) % 2 == 0: #nesmi byt sudé...
                    self.image_queue.append("") #kdyztak prictu jeste jeden prvek... append
            else:
                self.image_queue = [""]*((self.number_of_film_images*2)+1)
            self.converted_images = []
            self.start(output[1])

    def get_frame_dimensions(self): # Vrací aktuální rozměry rámečku
        """
        Vrací aktuální rozměry rámečku
        """
        whole_app_height = self.root._current_height
        whole_app_width = self.root._current_width
        width = whole_app_width
        self.frame_with_path.update_idletasks()
        self.image_film_frame_center.update_idletasks()
        height = whole_app_height-self.frame_with_path._current_height-30
        if self.image_film == True:
            height = height - self.image_film_frame_center._current_height
        return [width, height]

    def calc_current_format(self,width,height,new_window_status = False,frame_dim_given = None): # Přepočítávání rozměrů obrázku do rozměru rámce podle jeho formátu + zooming
        """
        Přepočítávání rozměrů obrázku do rozměru rámce podle jeho formátu

        -vstupními daty jsou šířka a výška obrázku
        -přepočítávání pozicování obrázku a scrollbarů v závislosti na zoomu
        """

        if new_window_status:
            frame_dimensions = frame_dim_given
        else:
            frame_dimensions = self.get_frame_dimensions()
        self.zoom_slider.update_idletasks()
        zoom = self.zoom_slider.get() / 100
        frame_width, frame_height = frame_dimensions
        image_width = width
        image_height = height
        image_ratio = image_width / image_height

        def rescale_image(): # Vmestnani obrazku do velikosti aktualni velikosti ramce podle jeho formatu
            if image_height > image_width:
                new_height = frame_height
                if image_width > frame_width:
                    new_width = int(new_height * image_ratio)
                else:
                    new_width = frame_width
                    if image_width > frame_width:
                        new_width = image_width
                    new_height = int(new_width / image_ratio)

            elif image_height < image_width:
                new_width = frame_width

                if image_height < frame_height:
                    new_height = int(new_width / image_ratio)
                else:
                    new_height = frame_height
                    if image_height < frame_height:
                        new_height = image_height
                    new_width = int(new_height * image_ratio)

            elif image_height == image_width:
                new_height = frame_height
                new_width = new_height

            #doublecheck
            if new_height > frame_height:
                new_height = frame_height
                new_width = int(new_height * image_ratio)
            if new_width > frame_width:
                new_width = frame_width
                new_height = int(new_width / image_ratio)

            return (new_height,new_width)
        
        new_height, new_width = rescale_image()

        if not new_window_status:
            new_height = new_height * zoom
            new_width = new_width * zoom
            self.previous_zoom = zoom
        
        self.main_frame.update()
        self.zoom_grow_x = max(new_width-self.previous_width,self.previous_width-new_width)
        self.zoom_grow_y = max(new_height-self.previous_height,self.previous_height-new_height)
        self.previous_height = new_height
        self.previous_width = new_width
        return [new_width, new_height]
    
    def view_image(self,increment_of_image,direct_path = None,only_refresh=None,reset = False,reload_buffer = False,only_next_ifz = False,in_new_window=False): # Samotné zobrazení obrázku
        """
        Samotné zobrazení obrázku

        -vstupními daty jsou informace o pozici obrázku v poli se všemi obrázky
        -přepočítávání rotace
        """
        
        if not only_next_ifz:
            self.loaded_image_status = False
        
        def corrupted_image_handling():
            with Image.open(Tools.resource_path("images/loading3.png")) as opened_image:
                rotated_image = opened_image.rotate(180,expand=True)
            resized = rotated_image.resize(size=(800,800))
            error_image = ImageTk.PhotoImage(resized)
            if self.main_frame.winfo_exists(): # kdyz se prepina do menu a bezi sekvence
                self.main_frame.delete("lower")
                self.main_image = self.main_frame.create_image(0, 0, anchor=tk.NW, image=error_image,tag ="raise")
                self.main_frame.tag_lower(self.main_image)
                self.main_frame.update()

        def check_image_growth_boundaries():
            frame_dimensions = self.get_frame_dimensions()
            nonlocal current_coords
            x_growth = self.zoom_grow_x*self.x_growth_multiplier
            y_growth = self.zoom_grow_y*self.y_growth_multiplier
            minus_x_boundary = frame_dimensions[0] - dimensions[0]
            minus_y_boundary = frame_dimensions[1] - dimensions[1]

            if self.x_growth_multiplier > 0: # tzn. jsme s mysi nalevo 1 až 0.5
                if current_coords[0]+x_growth < 0:
                    x_coords = current_coords[0]+x_growth
                else:
                    x_coords = 0
            else: # napravo, -0.5 až -1
                if current_coords[0]+x_growth < minus_x_boundary:
                    x_coords = minus_x_boundary
                else:
                    x_coords = current_coords[0]+x_growth

            if self.y_growth_multiplier > 0: # tzn. jsme s mysi nahore 1 sž 0.5
                if current_coords[1]+y_growth < 0:
                    y_coords = current_coords[1]+y_growth
                else:
                    y_coords = 0
            else: # -0.5 až -1
                if current_coords[1]+y_growth < minus_y_boundary:
                    y_coords = minus_y_boundary
                else:
                    y_coords = current_coords[1]+y_growth

            return (x_coords, y_coords)

        def make_image_strip(main_image):
            try:
                image_center= customtkinter.CTkImage(main_image,size = ((150,150)))
                if self.image_film_frame_center.winfo_exists(): # kdyz se prepina do menu a bezi sekvence
                    self.images_film_center.configure(image = image_center)
                    self.images_film_center.image = image_center
                    self.images_film_center.update_idletasks()
            except Exception as e: 
                print("moc rychle: ",e)
                
            
            if only_refresh == None: # jen pokud rotuju obrazek, aktualizuj prostřední
                def open_image(increment_of_image_given,position):
                    try:
                        if self.ifz_located == None:
                            increment_of_image = increment_of_image_given + position
                            number_of_found_images = len(self.all_images)
                            if increment_of_image < 0:
                                increment_of_image = number_of_found_images + increment_of_image

                            elif increment_of_image > number_of_found_images-1:
                                increment_of_image = 0 + (increment_of_image-number_of_found_images)

                            if len(self.all_images) > abs(increment_of_image):
                                image_to_show = self.all_images[increment_of_image]
                                with Image.open(image_to_show) as current_image:

                                    opened_image = current_image.rotate(self.rotation_angle,expand=True)
                                return opened_image
                            else:
                                return False
                        elif self.ifz_located == True:
                            converted_images_index = (position * self.ifz_count) #+ self.increment_of_ifz_image
                            image_to_show = self.converted_images[converted_images_index + self.increment_of_ifz_image]
                            with Image.open(image_to_show) as current_image:
                                opened_image = current_image.rotate(self.rotation_angle,expand=True)

                            return opened_image
                    except Exception as e:
                        error_message = f"Obrázek: {image_to_show} je poškozen"
                        print(error_message)
                        return False

                if reload_buffer:
                    if len(self.image_queue)>len(self.all_images):
                        self.image_queue = [""]*(len(self.all_images))
                        if len(self.image_queue) % 2 == 0: #nesmi byt sudé...
                            self.image_queue.append("") #kdyztak prictu jeste jeden prvek... append
                    else:
                        self.image_queue = [""]*((self.number_of_film_images*2)+1)

                image_film_dimensions = [80,80]
                half_image_queue = int(len(self.image_queue)/2)

                if "" in self.image_queue: #kdyz jeste nejsou zadne poukladane, preloading
                    #CENTER image preload
                    self.image_queue[half_image_queue] = customtkinter.CTkImage(main_image,size = (image_film_dimensions[0],image_film_dimensions[1]))
                    for i in range(0,half_image_queue): #LEFT
                        current_image = open_image(increment_of_image,-half_image_queue+i)
                        if current_image != False:
                            self.image_queue[i] = customtkinter.CTkImage(current_image,size = (image_film_dimensions[0],image_film_dimensions[1]))
                        
                    for i in range(0,half_image_queue): #RIGHT
                        current_image = open_image(increment_of_image,+i+1)
                        if current_image != False:
                            self.image_queue[i+half_image_queue+1] = customtkinter.CTkImage(current_image,size = (image_film_dimensions[0],image_film_dimensions[1]))
                else:
                    if self.flow_direction == "left":
                        current_image = open_image(increment_of_image,-half_image_queue)
                        if current_image != False:
                            preopened_image = customtkinter.CTkImage(current_image,size = (image_film_dimensions[0],image_film_dimensions[1]))
                            self.image_queue.pop(len(self.image_queue)-1)
                            self.image_queue.insert(0,preopened_image)

                    elif self.flow_direction == "right":
                        current_image = open_image(increment_of_image,half_image_queue)
                        if current_image != False:
                            preopened_image = customtkinter.CTkImage(current_image,size = (image_film_dimensions[0],image_film_dimensions[1]))
                            self.image_queue.append(preopened_image)
                            self.image_queue.pop(0)

                if self.image_film_frame_left.winfo_exists(): # kdyz se prepina do menu a bezi sekvence
                    for i in range(0,half_image_queue):
                        try:
                            self.left_labels[i].configure(image = self.image_queue[i],padx=10)
                            self.left_labels[i].image = self.image_queue[i]
                            self.left_labels[i].update_idletasks()
                        except Exception as e: 
                            print("moc rychle: ",e)
                            

                if self.image_film_frame_right.winfo_exists(): # kdyz se prepina do menu a bezi sekvence
                    for i in range(0,half_image_queue):
                        try:
                            self.right_labels[i].configure(image = self.image_queue[half_image_queue+i+1],padx=10)
                            self.right_labels[i].image = self.image_queue[half_image_queue+i+1]
                            self.right_labels[i].update_idletasks()
                        except Exception as e:
                            print("moc rychle: ",e)                       

        if len(self.all_images) != 0:
            if direct_path == None:
                image_to_show = self.all_images[increment_of_image]
            else:
                image_to_show = direct_path

            try:
                with Image.open(image_to_show) as opened_image:
                    rotated_image = opened_image.rotate(self.rotation_angle,expand=True)
                    width,height = rotated_image.size
            except Exception as e:
                error_message = f"Obrázek: {image_to_show} je poškozen"
                print(error_message)
                if not in_new_window:
                    corrupted_image_handling()
                    return error_message


            if in_new_window:
                def resize_image(event, label, original_image,frame_given = False):
                    if frame_given:
                        frame_dim = [int(event[0]),int(event[1])]
                    else:
                        frame_dim = [int(event.width),int(event.height)]

                    if frame_dim == self.last_frame_dim:
                        return

                    new_width, new_height = original_image.size
                    dimensions = self.calc_current_format(new_width,new_height,True,frame_dim)
                    

                    resized_image = original_image.resize((int(dimensions[0]),int(dimensions[1])))
                    photo = ImageTk.PhotoImage(resized_image)
                    label.configure(image=photo)
                    label.image = photo  # Keep a reference to avoid garbage collect
                    self.last_frame_dim = [frame_dim[0],frame_dim[1]]
                
                child_root = customtkinter.CTkToplevel()
                child_root.after(200, lambda: child_root.iconbitmap(app_icon))
                if self.ifz_located:
                    # self.convert_files()
                    center_image_index = int((len(self.image_queue)-1)/2) * self.ifz_count
                    image_to_show = self.converted_images[center_image_index + self.increment_of_ifz_image]
                   
                child_root.title(image_to_show)
                with Image.open(image_to_show) as opened_image:
                    rotated_image = opened_image.rotate(self.rotation_angle,expand=True)
                photo = ImageTk.PhotoImage(rotated_image)
                label = customtkinter.CTkLabel(child_root, image=photo, text="")
                label.pack(fill="both", expand=True)
                label.image = photo
                child_root.bind("<Configure>", lambda event, window_label = label, window_image = rotated_image: resize_image(event, window_label, window_image))
                child_root.update()
                child_root.update_idletasks()
                child_root.geometry(f"1200x800+{300}+{300}")
                resize_image([1200,800], label, rotated_image,frame_given=True)
                child_root.after(100,child_root.focus_force())
                self.loaded_image_status = True
                return
            
            dimensions = self.calc_current_format(width,height)
            resized = rotated_image.resize(size=(int(dimensions[0]),int(dimensions[1])))
            self.image_dimensions = (int(dimensions[0]),int(dimensions[1]))
            self.tk_image = ImageTk.PhotoImage(resized)
            self.main_frame.itemconfig(self.main_image, image=self.tk_image)
            if self.main_frame.winfo_exists(): # kdyz se prepina do menu a bezi sekvence
                try:
                    current_coords = self.main_frame.coords(self.main_image)
                except Exception:
                    reset = True

                if reset:
                    current_coords = [0,0]
                    self.zoom_grow_x=0
                    self.zoom_grow_y=0

                if not self.settings_applied:
                    x_coords, y_coords = check_image_growth_boundaries()
                else:
                    x_coords, y_coords = self.last_coords
                    self.settings_applied = False

                self.main_frame.update_idletasks()
                self.main_frame.delete("lower")
                self.main_image = self.main_frame.create_image(x_coords, y_coords,anchor=tk.NW, image=self.tk_image,tag = "lower")
                self.main_frame.tag_lower(self.main_image)
                self.last_coords = (x_coords,y_coords)
                # self.main_frame.update()

                if self.image_film == True: #refreshujeme pouze stredovy obrazek jinak i okolni
                    # run_background = threading.Thread(target=make_image_strip, args=(rotated_image,),daemon = True)
                    # run_background = threading.Thread(target=make_image_strip, args=(rotated_image,))
                    # run_background.start()
                    make_image_strip(rotated_image)

        self.loaded_image_status = True

    def next_image(self,silent=False,reload_buffer =False): # Další obrázek v pořadí (šipka vpravo)
        """
        Další obrázek v pořadí (šipka vpravo)
        """
        if not self.loaded_image_status:
            return
        load_status = None
        self.flow_direction = "right"
        number_of_found_images = len(self.all_images)
        if number_of_found_images != 0:
            if self.increment_of_image < number_of_found_images -1:
                self.increment_of_image += 1
            else:
                self.increment_of_image = 0
            
            if self.ifz_located == None:
                load_status = self.view_image(self.increment_of_image,reload_buffer = reload_buffer)
            else:
                self.convert_files()
                center_image_index = int((len(self.image_queue)-1)/2) * self.ifz_count
                load_status = self.view_image(None,self.converted_images[center_image_index + self.increment_of_ifz_image],reload_buffer = reload_buffer)
            
            if self.main_frame.winfo_exists(): # kdyz se prepina do menu a bezi sekvence
                self.current_image_num.configure(text ="/" + str(len(self.all_images)))
                self.changable_image_num.delete("0","100")
                self.changable_image_num.insert("0", str(self.increment_of_image+1))
                if silent == False:
                    if load_status != None:
                        Tools.add_colored_line(self.console,load_status,"orange",None,True)
                    elif self.name_or_path.get() == 1:
                        only_name = str(self.all_images[self.increment_of_image]).split("/")
                        only_name = only_name[int(len(only_name))-1]
                        Tools.add_colored_line(self.console,str(only_name),"white",None,True)
                    else:
                        Tools.add_colored_line(self.console,str(self.all_images[self.increment_of_image]),"white",None,True)

                self.current_image_num_ifz.configure(text ="/" + str(self.ifz_count))
                self.changable_image_num_ifz.delete("0","100")
                self.changable_image_num_ifz.insert("0", str(self.increment_of_ifz_image+1))
    
    def next_ifz_image(self): # Další ifz obrázek v pořadí
        number_of_found_images = self.ifz_count
        if number_of_found_images != 0 and number_of_found_images != 1:
            if self.increment_of_ifz_image < number_of_found_images -1:
                self.increment_of_ifz_image += 1
            else:
                self.increment_of_ifz_image = 0

            center_image_index = int((len(self.image_queue)-1)/2) * self.ifz_count
            # load_status = self.view_image(None,self.converted_images[center_image_index + self.increment_of_ifz_image],True,reload_buffer=True)
            load_status = self.view_image(None,self.converted_images[center_image_index + self.increment_of_ifz_image],reload_buffer=True,only_next_ifz = True)
            if self.main_frame.winfo_exists(): # kdyz se prepina do menu a bezi sekvence
                self.current_image_num_ifz.configure(text ="/" + str(self.ifz_count))
                self.changable_image_num_ifz.delete("0","100")
                self.changable_image_num_ifz.insert("0", str(self.increment_of_ifz_image+1))
                if load_status != None:
                    Tools.add_colored_line(self.console,load_status,"orange",None,True)
                elif self.name_or_path.get() == 1:
                    only_name = str(self.converted_images[center_image_index + self.increment_of_ifz_image]).split("/")
                    only_name = only_name[int(len(only_name))-1]
                    Tools.add_colored_line(self.console,str(only_name),"white",None,True)
                else:
                    Tools.add_colored_line(self.console,str(self.converted_images[center_image_index + self.increment_of_ifz_image]),"white",None,True)

    def previous_image(self): # Předchozí obrázek v pořadí (šipka vlevo)
        """
        Předchozí obrázek v pořadí (šipka vlevo)
        """
        if not self.loaded_image_status:
            return
        self.flow_direction = "left"
        load_status = None
        number_of_found_images = len(self.all_images)
        if number_of_found_images != 0:
            if self.increment_of_image > 0:
                self.increment_of_image -= 1
            else:
                self.increment_of_image = number_of_found_images -1
            
            if self.ifz_located == None:
                load_status = self.view_image(self.increment_of_image)
            else:
                self.convert_files()
                center_image_index = int((len(self.image_queue)-1)/2) * self.ifz_count
                load_status = self.view_image(None,self.converted_images[center_image_index + self.increment_of_ifz_image])
            self.current_image_num.configure(text = "/" + str(len(self.all_images)))
            self.changable_image_num.delete("0","100")
            self.changable_image_num.insert("0", str(self.increment_of_image+1))
            if load_status != None:
                Tools.add_colored_line(self.console,load_status,"orange",None,True)
            elif self.name_or_path.get() == 1:
                only_name = str(self.all_images[self.increment_of_image]).split("/")
                only_name = only_name[int(len(only_name))-1]
                Tools.add_colored_line(self.console,str(only_name),"white",None,True)
            else:
                Tools.add_colored_line(self.console,str(self.all_images[self.increment_of_image]),"white",None,True)

            self.current_image_num_ifz.configure(text ="/" + str(self.ifz_count))
            self.changable_image_num_ifz.delete("0","100")
            self.changable_image_num_ifz.insert("0", str(self.increment_of_ifz_image+1))

    def previous_ifz_image(self): # předešlý ifz obrázek v pořadí
        number_of_found_images = self.ifz_count
        if number_of_found_images != 0 and number_of_found_images != 1:
            if self.increment_of_ifz_image > 0:
                self.increment_of_ifz_image -= 1
            else:
                self.increment_of_ifz_image = number_of_found_images -1     
            
            center_image_index = int((len(self.image_queue)-1)/2) * self.ifz_count
            # load_status = self.view_image(None,self.converted_images[center_image_index + self.increment_of_ifz_image],True,reload_buffer=True)
            load_status = self.view_image(None,self.converted_images[center_image_index + self.increment_of_ifz_image],reload_buffer=True,only_next_ifz = True)
            if self.main_frame.winfo_exists(): # kdyz se prepina do menu a bezi sekvence
                self.current_image_num_ifz.configure(text ="/" + str(self.ifz_count))
                self.changable_image_num_ifz.delete("0","100")
                self.changable_image_num_ifz.insert("0", str(self.increment_of_ifz_image+1))
                if load_status != None:
                    Tools.add_colored_line(self.console,load_status,"orange",None,True)
                elif self.name_or_path.get() == 1:
                    only_name = str(self.converted_images[self.increment_of_ifz_image]).split("/")
                    only_name = only_name[int(len(only_name))-1]
                    Tools.add_colored_line(self.console,str(only_name),"white",None,True)
                else:
                    Tools.add_colored_line(self.console,str(self.converted_images[self.increment_of_ifz_image]),"white",None,True)
  
    def stop(self):
        self.state = "stop"
        self.button_play_stop.configure(text = "SPUSTIT")
        self.button_play_stop.configure(command = lambda: self.play())

    def play(self):
        def load_image_loop():
            speed=self.speed_slider.get()/100
            calculated_time = 2000-speed*2000 # 1% dela necele 2 sekundy, 100%, nula sekund, maximalni vykon
            self.next_image()
            if self.state != "stop":
                self.main_frame.update_idletasks()
                # if self.ifz_located and int(calculated_time) < 200:
                #     calculated_time = 200
                # if int(calculated_time) < 20:
                #     calculated_time = 20
                self.root.after(int(calculated_time),load_image_loop)

        self.state = "running"
        self.button_play_stop.configure(text = "STOP")
        self.button_play_stop.configure(command = lambda: self.stop())

        thread = threading.Thread(target=load_image_loop)
        thread.start()
  
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
            if self.ifz_located == True:
                if len(self.converted_images) != 0:
                    center_image_index = int((len(self.image_queue)-1)/2) * self.ifz_count
                    self.view_image(None,self.converted_images[center_image_index + self.increment_of_ifz_image],True,reset=True)
            else:
                self.view_image(self.increment_of_image,None,True,reset=True)

    def copy_image(self,path): # Tlačítko Kopír., zkopíruje daný obrázek do složky v dané cestě
        """
        Tlačítko Kopír., zkopíruje daný obrázek do složky v dané cestě

        -název složky přednastaven na Kopírované_obrázky
        -vlastnosti obrázku nijak nemění
        """
        image_path = self.all_images[self.increment_of_image]
        image = str(image_path).replace(path,"")
        if not os.path.exists(path + "/" + self.copy_dir):
            os.mkdir(path+ "/" + self.copy_dir)
        if not os.path.exists(path + "/" + self.copy_dir+ "/" + image):
            shutil.copy(path+ "/" + image,path + "/" + self.copy_dir+ "/" + image)
            if self.name_or_path.get() == 1:
                Tools.add_colored_line(self.console,f"Obrázek zkopírován do zvláštní složky: \"{self.copy_dir}\".  ({image})","white",None,True)
            else:
                Tools.add_colored_line(self.console,f"Obrázek zkopírován do zvláštní složky: \"{self.copy_dir}\".  ({image_path})","white",None,True)

        else:
            if self.name_or_path.get() == 1:
                Tools.add_colored_line(self.console,f"Obrázek je již zkopírovaný uvnitř složky: {self.copy_dir}.  ({image})","red",None,True)
            else:
                Tools.add_colored_line(self.console,f"Obrázek je již zkopírovaný uvnitř složky: {self.copy_dir}.  ({image_path})","red",None,True)
                
    def move_image(self): # Tlačítko Přesun., přesune daný obrázek do složky v dané cestě
        """
        Tlačítko Přesun., přesune daný obrázek do složky v dané cestě

        -název složky přednastaven na Přesunuté_obrázky
        """
        image_path = self.all_images[self.increment_of_image]
        image = str(image_path).replace(self.image_browser_path,"")
        if not os.path.exists(self.image_browser_path + "/" + self.move_dir):
            os.mkdir(self.image_browser_path+ "/" + self.move_dir)
        if not os.path.exists(self.image_browser_path + "/" + self.move_dir+ "/" + image):
            shutil.move(self.image_browser_path+ "/" + image,self.image_browser_path + "/" + self.move_dir+ "/" + image)
            if self.name_or_path.get() == 1:
                Tools.add_colored_line(self.console,f"Obrázek přesunut do zvláštní složky: \"{self.move_dir}\".  ({image})","white",None,True)
            else:
                Tools.add_colored_line(self.console,f"Obrázek přesunut do zvláštní složky: \"{self.move_dir}\".  ({image_path})","white",None,True)
            self.all_images.pop(self.increment_of_image) # odstraneni z pole
            self.current_image_num.configure(text ="/" + str(len(self.all_images))) # update maximalniho poctu obrazku
            self.increment_of_image -=1
            self.next_image(True)

    def delete_image(self): # Tlačítko SMAZAT
        image_path = self.all_images[self.increment_of_image]
        image = str(image_path).replace(self.image_browser_path,"")
        if os.path.exists(image_path):
            if self.name_or_path.get() == 1:
                Tools.add_colored_line(self.console,f"Právě byl smazán obrázek: {image}","orange",None,True)
            else:
                Tools.add_colored_line(self.console,f"Právě byl smazán obrázek: {image_path}","orange",None,True)

            os.remove(image_path)
            self.all_images.pop(self.increment_of_image) # odstraneni z pole
            self.current_image_num.configure(text ="/" + str(len(self.all_images))) # update maximalniho poctu obrazku
            self.increment_of_image -=1
            self.next_image(True,reload_buffer=True)

    def rotate_image(self):
        angles = [90.0,180.0,270.0,0.0]
        if self.rotation_angle < 270:
            self.rotation_angle += 90.0
        else:
            self.rotation_angle = 0.0
        if self.ifz_located == True:
            if len(self.converted_images) != 0:
                center_image_index = int((len(self.image_queue)-1)/2) * self.ifz_count
                # self.view_image(None,self.converted_images[center_image_index + self.increment_of_ifz_image],True,reset=True)
                self.view_image(None,self.converted_images[center_image_index + self.increment_of_ifz_image],reset=True,reload_buffer=True)
        else:
            # self.view_image(self.increment_of_image,None,True,reset=True)
            self.view_image(self.increment_of_image,None,reset=True,reload_buffer=True)
    
    def Reset_all(self): # Vrátí všechny slidery a natočení obrázku do původní polohy
        """
        Vrátí všechny slidery a natočení obrázku do původní polohy
        """
        self.rotation_angle = 0.0
        self.zoom_slider.set(100)
        self.update_zoom_slider(100)
        self.speed_slider.set(100)
        self.update_speed_slider(100)
        if self.ifz_located == True:
            if len(self.converted_images) != 0:
                center_image_index = int((len(self.image_queue)-1)/2) * self.ifz_count
                self.view_image(None,self.converted_images[center_image_index + self.increment_of_ifz_image],True,reset=True)
        else:
            self.view_image(self.increment_of_image,None,True,reset=True)
        self.root.update_idletasks()
        self.main_frame.update_idletasks()
    
    def refresh_console_setting(self):
        if self.name_or_path.get() == 1:
            if self.ifz_located == None:
                only_name = str(self.all_images[self.increment_of_image]).split("/")
            else:
                center_image_index = int((len(self.image_queue)-1)/2) * self.ifz_count
                only_name = str(self.converted_images[center_image_index + self.increment_of_ifz_image]).split("/")

            only_name = only_name[int(len(only_name))-1]
            Tools.add_colored_line(self.console,str(only_name),"white",None,True)

        else:
            if self.ifz_located == None:
                Tools.add_colored_line(self.console,str(self.all_images[self.increment_of_image]),"white",None,True)
            else:
                center_image_index = int((len(self.image_queue)-1)/2) * self.ifz_count
                Tools.add_colored_line(self.console,str(self.converted_images[center_image_index + self.increment_of_ifz_image]),"white",None,True)

    def drawing_option_window(self):
        def close_window(window):
            self.main_frame.unbind("<Button-1>")
            self.main_frame.unbind("<B1-Motion>")
            self.main_frame.unbind("<ButtonRelease-1>")
            self.main_frame.unbind("<Motion>")
            self.switch_drawing_mode()
            window.destroy()
        
        def rgb_to_hex(rgb,one_color = False):
            if not one_color:
                return "#%02x%02x%02x" % rgb
            elif one_color == "red":
                return ("#%02x" % rgb) + "0000"
            elif one_color == "green":
                return "#00" + ("%02x" % rgb) + "00"
            elif one_color == "blue":
                return "#0000" + ("%02x" % rgb)
        
        def hex_to_rgb(hex_color):
            # Remove the '#' character if present
            hex_color = hex_color.lstrip('#')
            # Convert the hex string into RGB tuple
            return list(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def update_color(*args):
            nonlocal current_color_frame
            red = int(color_R.get())
            red_hex = rgb_to_hex(red,one_color="red")
            current_color_val.configure(text = str(red))
            color_R.configure(progress_color = red_hex,button_color = red_hex,button_hover_color = red_hex)

            green = int(color_G.get())
            green_hex = rgb_to_hex(green,one_color="green")
            current_color_val2.configure(text = str(green))
            color_G.configure(progress_color = green_hex,button_color = green_hex,button_hover_color = green_hex)

            blue = int(color_B.get())
            blue_hex = rgb_to_hex(blue,one_color="blue")
            current_color_val3.configure(text = str(blue))
            color_B.configure(progress_color = blue_hex,button_color = blue_hex,button_hover_color = blue_hex)

            current_color_frame.configure(fg_color = rgb_to_hex((red,green,blue)))
            self.drawing_color = rgb_to_hex((red,green,blue))
            line_frame.configure(fg_color = self.drawing_color)

        def color_set(rgb):
            color_R.set(rgb[0])
            color_G.set(rgb[1])
            color_B.set(rgb[2])
            update_color("")

        def update_thickness(*args):
            self.drawing_thickness = int(*args)
            current_thickness.configure(text = str(self.drawing_thickness))
            line_frame.configure(height = self.drawing_thickness)
        
        def switch_draw_mode():
            nonlocal draw_circle
            nonlocal draw_line

            if draw_circle.get() == 1:
                self.draw_mode = "circle"
                draw_line.deselect()
            else:
                self.draw_mode = "line"
                draw_circle.deselect()

        def clear_canvas():
            self.main_frame.delete("drawing")

        def draw_cursor(flag = ""):
            image_center_x = self.image_dimensions[0]/2
            image_center_y = self.image_dimensions[1]/2

            if flag =="full":
                cursor_len_x = image_center_x
                cursor_len_y = image_center_y
            else:
                cursor_len_x = 50
                cursor_len_y = 50

            self.main_frame.create_line(image_center_x-cursor_len_x, image_center_y, image_center_x+cursor_len_x, image_center_y, fill=self.drawing_color,tags="drawing",width=self.drawing_thickness)
            self.main_frame.create_line(image_center_x, image_center_y-cursor_len_y, image_center_x, image_center_y+cursor_len_y, fill=self.drawing_color,tags="drawing",width=self.drawing_thickness)


        window = customtkinter.CTkToplevel()
        window.after(200, lambda: window.iconbitmap(app_icon))
        window_height = 500
        window_width = 620
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        window.geometry(f"{window_width}x{window_height}+{x+150}+{y+50}")
        window.title("Možnosti malování")
        
        top_frame =         customtkinter.CTkFrame(master = window,corner_radius=0,height=120,fg_color="gray10")
        current_color_frame = customtkinter.CTkFrame(master = top_frame,corner_radius=0,border_width=2,height=100,width=100,fg_color="gray10")
        slider_frame =      customtkinter.CTkFrame(master = top_frame,corner_radius=0,width=500,fg_color="gray10")
        top_frame.          pack(pady=0,padx=0,fill="x",expand=False,side = "top")
        top_frame.          pack_propagate(0)

        slider_frame.       pack(pady=(10,0),padx=(5,0),expand=False,side = "left")
        slider_frame.       pack_propagate(0)
        current_color_frame.pack(pady=(10,0),padx=10,expand=False,side = "left",anchor = "w")

        frame_R =           customtkinter.CTkFrame(master = slider_frame,height=20,corner_radius=0,border_width=0,fg_color="gray10")
        color_label =       customtkinter.CTkLabel(master = frame_R,text = "R: ",justify = "left",font=("Arial",16,"bold"))
        color_R =           customtkinter.CTkSlider(master=frame_R,width=400,height=15,from_=0,to=255,command= lambda e: update_color(e))
        current_color_val = customtkinter.CTkLabel(master = frame_R,text = "0",justify = "left",font=("Arial",16,"bold"))
        color_label.        pack(pady=5,padx=5,expand=False,side = "left")
        color_R.            pack(pady=5,padx=5,expand=False,side = "left")
        current_color_val.  pack(pady=5,padx=5,expand=False,side = "left")
        color_R.set(0.0)
        
        frame_G =           customtkinter.CTkFrame(master = slider_frame,height=20,corner_radius=0,border_width=0,fg_color="gray10")
        color_label =       customtkinter.CTkLabel(master = frame_G,text = "G: ",justify = "left",font=("Arial",16,"bold"))
        color_G =           customtkinter.CTkSlider(master=frame_G,width=400,height=15,from_=0,to=255,command= lambda e: update_color(e))
        current_color_val2 = customtkinter.CTkLabel(master = frame_G,text = "0",justify = "left",font=("Arial",16,"bold"))
        color_label.        pack(pady=5,padx=5,expand=False,side = "left")
        color_G.            pack(pady=5,padx=5,expand=False,side = "left")
        current_color_val2. pack(pady=5,padx=5,expand=False,side = "left")
        color_G.set(0.0)

        frame_B =           customtkinter.CTkFrame(master = slider_frame,height=20,corner_radius=0,border_width=0,fg_color="gray10")
        color_label =       customtkinter.CTkLabel(master = frame_B,text = "B: ",justify = "left",font=("Arial",16,"bold"))
        color_B =           customtkinter.CTkSlider(master=frame_B,width=400,height=15,from_=0,to=255,command= lambda e: update_color(e))
        current_color_val3 = customtkinter.CTkLabel(master = frame_B,text = "0",justify = "left",font=("Arial",16,"bold"))
        color_label.        pack(pady=5,padx=5,expand=False,side = "left")
        color_B.            pack(pady=5,padx=5,expand=False,side = "left")
        current_color_val3. pack(pady=5,padx=5,expand=False,side = "left")
        color_B.set(0.0)

        bottom_frame =      customtkinter.CTkFrame(master = window,corner_radius=0,fg_color="gray10") 
        common_colors =     customtkinter.CTkFrame(master = bottom_frame,corner_radius=0,border_width=0,fg_color="gray10")
        white_button =      customtkinter.CTkButton(master = common_colors,text="",width = 30,height=30,corner_radius=0,border_width=1,fg_color="#FFFFFF",command=lambda: color_set([255,255,255]))
        black_button =      customtkinter.CTkButton(master = common_colors,text="",width = 30,height=30,corner_radius=0,border_width=1,fg_color="#000000",command=lambda: color_set([0,0,0]))
        red_button =        customtkinter.CTkButton(master = common_colors,text="",width = 30,height=30,corner_radius=0,border_width=1,fg_color="#FF0000",command=lambda: color_set([255,0,0]))
        green_button =      customtkinter.CTkButton(master = common_colors,text="",width = 30,height=30,corner_radius=0,border_width=1,fg_color="#00FF00",command=lambda: color_set([0,255,0]))
        blue_button =       customtkinter.CTkButton(master = common_colors,text="",width = 30,height=30,corner_radius=0,border_width=1,fg_color="#0000FF",command=lambda: color_set([0,0,255]))
        white_button.       pack(pady=5,padx=(5,0),expand=False,side = "left")
        black_button.       pack(pady=5,padx=(5,0),expand=False,side = "left")
        red_button.         pack(pady=5,padx=(5,0),expand=False,side = "left")
        green_button.       pack(pady=5,padx=(5,0),expand=False,side = "left")
        blue_button.        pack(pady=5,padx=(5,0),expand=False,side = "left")
        common_colors.      pack(pady=0,padx=0,expand=False,side = "top",fill="x")
        
        shape_checkboxes =  customtkinter.CTkFrame(master = bottom_frame,corner_radius=0,fg_color="gray10") 
        draw_circle =       customtkinter.CTkCheckBox(master = shape_checkboxes, text = "Kruh",command = lambda: switch_draw_mode(),font=("Arial",20))
        draw_line =         customtkinter.CTkCheckBox(master = shape_checkboxes, text = "Osa",command = lambda: switch_draw_mode(),font=("Arial",20))
        draw_circle.        pack(pady=0,padx=5,expand=False,side = "left")
        draw_line.          pack(pady=0,padx=5,expand=False,side = "left")
        shape_checkboxes.   pack(pady=15,padx=5,expand=False,side = "top",fill="x")

        bottom_frame_label = customtkinter.CTkLabel(master = bottom_frame,text = "Nastavení tloušťky čáry:",justify = "left",font=("Arial",18,"bold"),anchor="w")

        thickness_frame =   customtkinter.CTkFrame(master = bottom_frame,corner_radius=0,fg_color="gray10",height=55) 
        thickness =         customtkinter.CTkSlider(master=thickness_frame,width=450,height=15,from_=1,to=50,command= lambda e: update_thickness(e))
        current_thickness = customtkinter.CTkLabel(master = thickness_frame,text = "0",justify = "left",font=("Arial",16,"bold"))
        line_frame =        customtkinter.CTkFrame(master = thickness_frame,corner_radius=0,fg_color="black",height=1,width = 100) 
        thickness.          pack(pady=5,padx=5,expand=False,side = "left")
        current_thickness.  pack(pady=5,padx=5,expand=False,side = "left")
        line_frame.         pack(pady=5,padx=5,expand=False,side = "left")
        cursor_frame =      customtkinter.CTkFrame(master = bottom_frame,corner_radius=0,fg_color="gray10",height=55)
        cursor_button =     customtkinter.CTkButton(master = cursor_frame,text = "Kurzor uprostřed",font=("Arial",22,"bold"),width = 150,height=40,corner_radius=0,command=lambda: draw_cursor())
        cursor_button2 =    customtkinter.CTkButton(master = cursor_frame,text = "Kurzor uprostřed (celý)",font=("Arial",22,"bold"),width = 150,height=40,corner_radius=0,command=lambda: draw_cursor("full"))
        cursor_button.      pack(pady=5,padx=5,expand=True,side = "left",fill="x")
        cursor_button2.     pack(pady=5,padx=5,expand=True,side = "left",fill="x")

        clear_all =         customtkinter.CTkButton(master = bottom_frame,text = "Vyčistit",font=("Arial",22,"bold"),width = 150,height=40,corner_radius=0,command=lambda: clear_canvas())
        frame_R.            pack(pady=0,padx=0,expand=False,side = "top",fill="x")
        frame_G.            pack(pady=0,padx=0,expand=False,side = "top",fill="x")
        frame_B.            pack(pady=0,padx=0,expand=False,side = "top",fill="x")
        bottom_frame.       pack(pady=0,padx=0,fill="x",expand=False,side = "top")
        bottom_frame_label. pack(pady=5,padx=5,expand=False,side = "top",fill="x",anchor = "w")
        thickness_frame.    pack(pady=(5,0),padx=5,expand=False,side = "top",fill="x")
        thickness_frame.    pack_propagate(0)
        cursor_frame.       pack(pady=(20,5),padx=5,expand=False,side = "top",fill="x")
        clear_all.          pack(pady=5,padx=10,expand=False,side = "top",fill="x")
        current_color_frame.configure(fg_color = self.drawing_color)
        previous_color = hex_to_rgb(self.drawing_color)
        color_R.set(previous_color[0])
        color_G.set(previous_color[1])
        color_B.set(previous_color[2])
        draw_line.select()
        thickness.set(self.drawing_thickness)
        update_thickness(self.drawing_thickness)
        update_color("")

        button_exit = customtkinter.CTkButton(master = window,text = "Zavřít",font=("Arial",22,"bold"),width = 200,height=50,corner_radius=0,command=lambda: close_window(window))
        button_exit.pack(pady = 10, padx = 10,expand=False,side="right",anchor = "e")
        # self.root.bind("<Button-1>",lambda e: close_window(window))
        window.update()
        window.update_idletasks()
        window.transient(self.root)
        window.attributes("-topmost", True)
        window.attributes("-disabled", False)
        # window.focus_force()
        # window.grab_set()
        # window.grab_release()
        # window.focus()

    def switch_drawing_mode(self,initial = False):
        """
        Making binds to canvas\n
        Operation:
        - "drawing"
        - "image"
        """
        self.released = False
        self.start_x = 0
        self.start_y = 0
        self.main_frame.unbind("<Button-1>")
        self.main_frame.unbind("<B1-Motion>")
        self.main_frame.unbind("<ButtonRelease-1>")
        self.main_frame.unbind("<Motion>")

        def bind_drawing():
            def on_click(event):
                # Save the start position
                self.start_x = event.x
                self.start_y = event.y

            def on_drag(event):
                # Clear the canvas (if you want to see only the final shape)
                self.main_frame.delete("temp_shape")
                if self.draw_mode == "line":
                    # Draw a line from the start position to the current position
                    self.main_frame.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.drawing_color, tags="temp_shape",width=self.drawing_thickness)
                elif self.draw_mode == "circle":
                    # Draw an oval (circle) based on the start position and current position
                    self.main_frame.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.drawing_color, tags="temp_shape",width=self.drawing_thickness)

            def on_release(event):
                # Finalize the shape
                self.main_frame.delete("temp_shape")
                if self.draw_mode == "line":
                    # Draw the final line
                    self.main_frame.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.drawing_color,tags="drawing",width=self.drawing_thickness)
                elif self.draw_mode == "circle":
                    # Draw the final circle
                    self.main_frame.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.drawing_color,tags="drawing",width=self.drawing_thickness)
            
            self.main_frame.bind("<Button-1>", on_click)
            self.main_frame.bind("<B1-Motion>", on_drag)
            self.main_frame.bind("<ButtonRelease-1>", on_release)

        def bind_image_dragging():
            def mouse_clicked(e):
                self.main_frame.focus_set()
                self.released = False
                x,y = e.x,e.y

                def get_direction(e):
                    current_coords = self.main_frame.coords(self.main_image) 
                    option = ""
                    if abs(max(e.x,x)-min(e.x,x)) > abs(max(e.y,y)-min(e.y,y)):
                        option = "horizontal"
                    else:
                        option = "vertical"

                    if option == "horizontal":
                        if e.x > x:
                            #right
                            if (current_coords[0] + self.drag_increment) < 0:
                                self.main_frame.coords(self.main_image,current_coords[0]+self.drag_increment,current_coords[1])
                            else:
                                self.main_frame.coords(self.main_image,0,current_coords[1])
                        else:
                            #left
                            if (current_coords[0] - self.drag_increment) > -(self.tk_image.width()-self.main_frame.winfo_width()):
                                self.main_frame.coords(self.main_image,current_coords[0]-self.drag_increment,current_coords[1])
                            else:
                                self.main_frame.coords(self.main_image,-(self.tk_image.width()-self.main_frame.winfo_width()),current_coords[1])

                    if option == "vertical":
                        if e.y > y:
                            #down
                            if (current_coords[1] + self.drag_increment) < 0:
                                self.main_frame.coords(self.main_image,current_coords[0],current_coords[1]+self.drag_increment)
                            else:
                                self.main_frame.coords(self.main_image,current_coords[0],0)
                        else:
                            #up
                            if (current_coords[1] - self.drag_increment) > -(self.tk_image.height()-self.main_frame.winfo_height()):
                                self.main_frame.coords(self.main_image,current_coords[0],current_coords[1]-self.drag_increment)
                            else:
                                self.main_frame.coords(self.main_image,current_coords[0],-(self.tk_image.height()-self.main_frame.winfo_height()))
                    
                    self.main_frame.update()
                    self.last_coords = self.main_frame.coords(self.main_image) 
                    return

                self.main_frame.bind("<Motion>", get_direction)
                if self.released == True:
                    return

                def end_func(e):
                    self.main_frame.unbind("<Motion>")
                    self.main_frame.unbind("<ButtonRelease-1>")
                    self.released = True
                    return

                self.main_frame.bind("<ButtonRelease-1>",end_func)
            self.main_frame.bind("<Button-1>",mouse_clicked)

        if initial:
            bind_image_dragging()
            self.drag_option_binded = True
            return

        if self.drag_option_binded:
            bind_drawing()
            self.drawing_option_window()
            self.drag_option_binded = False

        elif not self.drag_option_binded:
            bind_image_dragging()
            self.drag_option_binded = True

    def create_widgets(self): # Vytvoření veškerých widgets (MAIN image browseru)
        def call_setting_window():
            if self.ifz_located == True:
                path_to_send = self.all_images[self.increment_of_image]
            else:
                try:
                    path_to_send = self.all_images[self.increment_of_image]
                except Exception:
                    path_to_send = ""
            # Advanced_option(self.root,windowed=True,spec_location="image_browser", path_to_remember = path_to_send,last_params = [self.last_coords,self.zoom_slider.get()])
        
        def call_path_context_menu(event):
            def insert_path(path):
                if self.path_set.get() == path:
                    return
                self.path_set.delete("0","200")
                self.path_set.insert("0", path)
                self.start(path)

            if len(self.inserted_path_history) > 0:
                path_context_menu = tk.Menu(self.root, tearoff=0,fg="white",bg="black")
                for i in range(0,len(self.inserted_path_history)):
                    path_context_menu.add_command(label=self.inserted_path_history[i], command=lambda row_path = self.inserted_path_history[i]: insert_path(row_path),font=("Arial",22,"bold"))
                    if i < len(self.inserted_path_history)-1:
                        path_context_menu.add_separator()
                        
                path_context_menu.tk_popup(context_menu_button.winfo_rootx(),context_menu_button.winfo_rooty()+30)

        def call_start():
            self.changable_image_num.delete("0","100")
            self.changable_image_num.insert("0",str(0))
            self.changable_image_num_ifz.delete("0","100")
            self.changable_image_num_ifz.insert("0",str(0))
            self.selected_image = ""
            self.current_image_num_ifz.configure(text = "/0")
            self.current_image_num.configure(text = "/0")
            self.start(self.path_set.get())

        self.frame_with_path =          customtkinter.CTkFrame(master=self.root,height = 200,corner_radius=0)
        menu_button  =                  customtkinter.CTkButton(master = self.frame_with_path, width = 100,height=30, text = "MENU", command = lambda: self.call_menu(),font=("Arial",16,"bold"))
        context_menu_button  =          customtkinter.CTkButton(master = self.frame_with_path, width = 50,height=30, text = "V",font=("Arial",16,"bold"),corner_radius=0,fg_color="#505050")
        self.path_set =                 customtkinter.CTkEntry(master = self.frame_with_path,width = 680,height=30,placeholder_text="Zadejte cestu k souborům (kde se soubory přímo nacházejí)",corner_radius=0)
        manual_path  =                  customtkinter.CTkButton(master = self.frame_with_path, width = 90,height=30,text = "Otevřít", command = lambda: call_start(),font=("Arial",16,"bold"))
        tree         =                  customtkinter.CTkButton(master = self.frame_with_path, width = 120,height=30,text = "EXPLORER", command = self.call_browseDirectories,font=("Arial",16,"bold"))
        button_save_path =              customtkinter.CTkButton(master = self.frame_with_path,width=100,height=30, text = "Uložit cestu", command = lambda: Tools.save_path(self.console,self.path_set.get(),"image_browser_settings"),font=("Arial",16,"bold"))        
        button_open_setting =           customtkinter.CTkButton(master = self.frame_with_path,width=30,height=30, text = "⚙️", command = lambda: call_setting_window(),font=("",16))
        button_drawing =                customtkinter.CTkButton(master = self.frame_with_path,width=30,height=30, text = "Malování", command = lambda: self.switch_drawing_mode(),font=("Arial",16,"bold"))
        # menu_button.                    pack(pady = (5,0),padx =(5,0),side="left",anchor = "w")
        context_menu_button.            pack(pady = (5,0),padx =(5,0),side="left",anchor = "w")
        self.path_set.                  pack(pady = (5,0),padx =(0,0),side="left",anchor = "w")
        manual_path.                    pack(pady = (5,0),padx =(5,0),side="left",anchor = "w")
        tree.                           pack(pady = (5,0),padx =(5,0),side="left",anchor = "w")
        button_save_path.               pack(pady = (5,0),padx =(5,0),side="left",anchor = "w")
        button_open_setting.            pack(pady = (5,0),padx =(5,0),side="left",anchor = "w")
        button_drawing.                 pack(pady = (5,0),padx =(5,0),side="left",anchor = "w")
        self.frame_with_path.           pack(pady=0,padx=0,fill="x",expand=False,side = "top")
        self.frame_with_console =       customtkinter.CTkFrame(master=self.root,height = 200,corner_radius=0)
        self.name_or_path =             customtkinter.CTkCheckBox(master = self.frame_with_console,font=("Arial",16), text = "Název/cesta",command= lambda: self.refresh_console_setting())
        self.console =                  tk.Text(self.frame_with_console, wrap="none", height=0,background="black",font=("Arial",14),state=tk.DISABLED)
        self.name_or_path.              pack(pady = (5,0),padx =10,anchor = "w",side="left")
        self.console.                   pack(pady = (5,0),padx =10,anchor = "w",side="left",fill="x",expand=True)
        self.frame_with_console.        pack(pady=0,padx=0,fill="x",expand=False,side = "top")
        self.frame_with_buttons =       customtkinter.CTkFrame(master=self.root,height = 200,corner_radius=0)
        button_back  =                  customtkinter.CTkButton(master = self.frame_with_buttons, width = 20,height=30,text = "<", command = self.previous_image,font=("Arial",16,"bold"))
        self.changable_image_num =      customtkinter.CTkEntry(master = self.frame_with_buttons,width=45,justify = "left",font=("Arial",16,"bold"))
        self.changable_image_num.delete("0","100")
        self.changable_image_num.insert("0",0)
        self.current_image_num =        customtkinter.CTkLabel(master = self.frame_with_buttons,text = "/0",justify = "left",font=("Arial",16,"bold"))
        button_next  =                  customtkinter.CTkButton(master = self.frame_with_buttons, width = 20,height=30,text = ">", command = self.next_image,font=("Arial",16,"bold"))
        self.button_play_stop  =        customtkinter.CTkButton(master = self.frame_with_buttons, width = 90,height=30,text = "SPUSTIT", command = self.play,font=("Arial",16,"bold"))
        button_copy  =                  customtkinter.CTkButton(master = self.frame_with_buttons, width = 80,height=30,text = "Kopír.", command = lambda: self.copy_image(self.image_browser_path),font=("Arial",16,"bold"))
        rotate_button =                 customtkinter.CTkButton(master = self.frame_with_buttons, width = 80,height=30,text = "OTOČIT", command =  lambda: self.rotate_image(),font=("Arial",16,"bold"))
        speed_label  =                  customtkinter.CTkLabel(master = self.frame_with_buttons,text = "Rychlost:",justify = "left",font=("Arial",12))
        self.speed_slider =             customtkinter.CTkSlider(master = self.frame_with_buttons,width=120,from_=1,to=100,command= self.update_speed_slider)
        self.percent1 =                 customtkinter.CTkLabel(master = self.frame_with_buttons,text = "%",justify = "left",font=("Arial",12))
        zoom_label   =                  customtkinter.CTkLabel(master = self.frame_with_buttons,text = "ZOOM:",justify = "left",font=("Arial",12))
        self.zoom_slider =              customtkinter.CTkSlider(master = self.frame_with_buttons,width=120,from_=100,to=500,command= self.update_zoom_slider)
        self.percent2 =                 customtkinter.CTkLabel(master = self.frame_with_buttons,text = "%",justify = "left",font=("Arial",12))
        reset_button =                  customtkinter.CTkButton(master = self.frame_with_buttons, width = 80,height=30,text = "RESET", command = lambda: self.Reset_all(),font=("Arial",16,"bold"))
        ifz_label =                     customtkinter.CTkLabel(master = self.frame_with_buttons,text = "IFZ:",justify = "left",font=("Arial",12))
        button_back_ifz  =              customtkinter.CTkButton(master = self.frame_with_buttons, width = 20,height=30,text = "<", command = self.previous_ifz_image,font=("Arial",16,"bold"))
        self.changable_image_num_ifz =  customtkinter.CTkEntry(master = self.frame_with_buttons,width=20,justify = "left",font=("Arial",16,"bold"))
        self.changable_image_num_ifz.delete("0","100")
        self.changable_image_num_ifz.insert("0",1)
        self.current_image_num_ifz =    customtkinter.CTkLabel(master = self.frame_with_buttons,text = "/0",justify = "left",font=("Arial",16,"bold"))
        button_next_ifz  =              customtkinter.CTkButton(master = self.frame_with_buttons, width = 20,height=30,text = ">", command = self.next_ifz_image,font=("Arial",16,"bold"))
        button_move =                   customtkinter.CTkButton(master = self.frame_with_buttons, width = 80,height=30,text = "Přesun.", command =  lambda: self.move_image(),font=("Arial",16,"bold"))
        button_delete =                 customtkinter.CTkButton(master = self.frame_with_buttons, width = 80,height=30,text = "SMAZAT", command =  lambda: self.delete_image(),font=("Arial",16,"bold"))
        button_back.                    pack(pady = (5,0),padx =(10,0),anchor = "w",side="left")
        self.changable_image_num.       pack(pady = (5,0),padx =(10,0),anchor = "w",side="left")
        self.current_image_num.         pack(pady = (5,0),padx =(10,0),anchor = "w",side="left")
        button_next.                    pack(pady = (5,0),padx =(10,0),anchor = "w",side="left")
        self.button_play_stop.          pack(pady = (5,0),padx =(10,0),anchor = "w",side="left")
        button_copy.                    pack(pady = (5,0),padx =(5,0),anchor = "w",side="left")
        rotate_button.                  pack(pady = (5,0),padx =(5,0),anchor = "w",side="left")
        speed_label.                    pack(pady = (5,0),padx =(5,0),anchor = "w",side="left")
        self.speed_slider.              pack(pady = (5,0),padx =(5,0),anchor = "w",side="left")
        self.percent1.                  pack(pady = (5,0),padx =(5,0),anchor = "w",side="left")
        zoom_label.                     pack(pady = (5,0),padx =(5,0),anchor = "w",side="left")
        self.zoom_slider.               pack(pady = (5,0),padx =(5,0),anchor = "w",side="left")
        self.percent2.                  pack(pady = (5,0),padx =(5,0),anchor = "w",side="left")
        reset_button.                   pack(pady = (5,0),padx =(5,0),anchor = "w",side="left")
        ifz_label.                      pack(pady = (5,0),padx =(5,0),anchor = "w",side="left")
        button_back_ifz.                pack(pady = (5,0),padx =(5,0),anchor = "w",side="left")
        self.changable_image_num_ifz.   pack(pady = (5,0),padx =(10,0),anchor = "w",side="left")
        self.current_image_num_ifz.     pack(pady = (5,0),padx =(10,0),anchor = "w",side="left")
        button_next_ifz.                pack(pady = (5,0),padx =(10,0),anchor = "w",side="left")
        button_move.                    pack(pady = (5,0),padx =(10,0),anchor = "w",side="left")
        button_delete.                  pack(pady = (5,0),padx =(5,0),anchor = "w",side="left")
        self.frame_with_buttons.        pack(pady=0,padx=(0,0),fill="x",expand=False,side = "top")
        self.background_frame =         customtkinter.CTkFrame(master=self.root,corner_radius=0)
        self.main_frame =               tk.Canvas(master=self.background_frame,bg="black",highlightthickness=0)
        self.image_film_frame_left =    customtkinter.CTkFrame(master=self.root,height = 100,corner_radius=0)
        self.image_film_frame_center =  customtkinter.CTkFrame(master=self.root,height = 100,width = 200,corner_radius=0)
        self.image_film_frame_right =   customtkinter.CTkFrame(master=self.root,height = 100,corner_radius=0)
        self.background_frame.          pack(pady=(10,0),padx=5,ipadx=10,ipady=10,fill="both",expand=True,side = "top")
        if self.image_film == True:
            self.image_film_frame_left. pack(pady=5,expand=True,side = "left",fill="x")
            self.image_film_frame_center.pack(pady=5,padx=10,expand=False,side = "left",anchor = "center")
            self.image_film_frame_right.pack(pady=5,expand=True,side = "left",fill="x")
            self.images_film_center =   customtkinter.CTkLabel(master = self.image_film_frame_center,text = "")
            self.images_film_center.    pack()
        self.main_frame.                pack(pady=0,padx=5,ipadx=10,ipady=10,fill="both",expand=True,side = "bottom",anchor= "center")
        self.name_or_path.select()
        context_menu_button.bind("<Button-1>", call_path_context_menu)

        def jump_to_image(e):
            if self.changable_image_num.get().isdigit():
                inserted_value = int(self.changable_image_num.get())
                if inserted_value >= 1 and inserted_value <= int(len(self.all_images)):
                    self.increment_of_image = inserted_value-1
                    if self.ifz_located == True:
                        self.convert_files()
                        center_image_index = int((len(self.image_queue)-1)/2) * self.ifz_count
                        self.view_image(None,self.converted_images[center_image_index + self.increment_of_ifz_image])
                    else:
                        self.view_image(self.increment_of_image)
            self.changable_image_num.delete("0","100")
            self.changable_image_num.insert("0",self.increment_of_image+1)
            self.root.focus_set() # unfocus    
        self.changable_image_num.bind("<Return>",jump_to_image)

        # nastaveni defaultnich hodnot slideru
        self.zoom_slider.set(self.zoom_given)
        self.update_zoom_slider(self.zoom_given)
        self.speed_slider.set(100)
        self.update_speed_slider(100)
        self.switch_drawing_mode(initial=True)

        def focused_entry_widget():
            currently_focused = str(self.root.focus_get())
            if ".!ctkentry" in currently_focused:
                return True
            else:
                return False
            
        def focused_control_widget():
            currently_focused = str(self.root.focus_get())
            if ".!text" in currently_focused:
                return True
            else:
                return False

        # KEYBOARD BINDING
        def rotate_button_hover(e):
            if int(self.rotation_angle==270):
                rotate_button.configure(text="0°",font=("Arial",15))
            else:
                rotate_button.configure(text=str(int(self.rotation_angle)+90)+"°",font=("Arial",15))
            rotate_button.update_idletasks()
            return
                
        def rotate_button_hover_leave(e):
            rotate_button.configure(text="OTOČIT",font=("Arial",16,"bold"))
        rotate_button.bind("<Enter>",rotate_button_hover)
        rotate_button.bind("<Button-1>",rotate_button_hover)
        rotate_button.bind("<Leave>",rotate_button_hover_leave)

        def move_button_hover(e):
            button_move.configure(text="\"M\"",font=("Arial",16,"bold"))
            button_move.update_idletasks()
            return
                
        def move_button_hover_leave(e):
            button_move.configure(text="Přesun.",font=("Arial",16,"bold"))

        button_move.bind("<Enter>",move_button_hover)
        button_move.bind("<Button-1>",move_button_hover)
        button_move.bind("<Leave>",move_button_hover_leave)

        def copy_button_hover(e):
            button_copy.configure(text="\"C\"",font=("Arial",16,"bold"))
            button_copy.update_idletasks()
            return
                
        def copy_button_hover_leave(e):
            button_copy.configure(text="Kopír.",font=("Arial",16,"bold"))

        button_copy.bind("<Enter>",copy_button_hover)
        button_copy.bind("<Button-1>",copy_button_hover)
        button_copy.bind("<Leave>",copy_button_hover_leave)

        def pressed_space(e):
            if focused_entry_widget(): # pokud nabindovany znak neni vepisovan do entry widgetu
                return
            if self.state != "stop":
                self.state = "stop"
                self.stop()
            else:
                self.state = "running"
                self.play()
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

        def pressed_up(e):
            if focused_entry_widget() or self.ifz_located == None: # pokud nabindovany znak neni vepisovan do entry widgetu nebo nejsou ifz
                return
            self.next_ifz_image()
        self.root.bind("<Up>",pressed_up)
        self.unbind_list.append("<Up>")

        def pressed_down(e):
            if focused_entry_widget() or self.ifz_located == None: # pokud nabindovany znak neni vepisovan do entry widgetu nebo nejsou ifz
                return
            self.previous_ifz_image()
        self.root.bind("<Down>",pressed_down)
        self.unbind_list.append("<Down>")

        def pressed_copy(e):
            if focused_entry_widget() or focused_control_widget(): # pokud nabindovany znak neni vepisovan do entry widgetu
                return
            self.copy_image(self.image_browser_path)
        self.root.bind("<c>",pressed_copy)
        self.unbind_list.append("<c>")

        def pressed_move(e):
            if focused_entry_widget(): # pokud nabindovany znak neni vepisovan do entry widgetu
                return
            self.move_image()
        self.root.bind("<m>",pressed_move)
        self.unbind_list.append("<m>")
        
        def pressed_rotate(e):
            rotate_button_hover(e) #update uhlu zobrazovanem na tlacitku
            if focused_entry_widget(): # pokud nabindovany znak neni vepisovan do entry widgetu
                return
            self.rotate_image()
        self.root.bind("<r>",pressed_rotate)
        self.unbind_list.append("<r>")

        def pressed_delete(e):
            if focused_entry_widget(): # pokud nabindovany znak neni vepisovan do entry widgetu
                return
            self.delete_image()
        self.root.bind("<Delete>",pressed_delete)
        self.unbind_list.append("<Delete>")

        def call_refresh(e):
            self.Reset_all()
        self.root.bind("<F5>",lambda e: call_refresh(e))
        self.unbind_list.append("<F5>")

        #Funkce kolecka mysi: priblizovat nebo posouvat vpred/ vzad
        def mouse_wheel1(e): # priblizovat
            direction = -e.delta

            self.main_frame.update_idletasks()
            self.zoom_slider.update_idletasks()
            frame_dim = self.get_frame_dimensions()
            frame_width = frame_dim[0]
            frame_height = frame_dim[1]

            if e.x <= frame_width/2: # pokud větší, tak budeme růst obrázku přičítat
                self.x_growth_multiplier = 1-((e.x/(frame_width/2)))/2
            elif e.x >= frame_width/2: # pokud větší, tak budeme růst obrázku odečítat
                self.x_growth_multiplier = -((e.x/(frame_width/2))/2)
                if direction > 0:
                    self.x_growth_multiplier = self.x_growth_multiplier *(-1)

            if e.y <= frame_height/2: # pokud větší, tak budeme růst obrázku přičítat
                self.y_growth_multiplier = 1-((e.y/(frame_height/2)))/2
            elif e.y >= frame_height/2: # pokud větší, tak budeme růst obrázku odečítat
                self.y_growth_multiplier = -((e.y/(frame_height/2))/2)
                if direction > 0:
                    self.y_growth_multiplier = self.y_growth_multiplier *(-1)
            
            if direction < 0:
                direction = "in"
                new_value = self.zoom_slider.get()+self.zoom_increment
                if self.zoom_slider._to >= new_value:
                    self.zoom_slider.set(new_value)
                    self.percent2.configure(text=str(int(new_value)) + " %")
                else:
                    self.zoom_slider.set(self.zoom_slider._to) # pro pripad, ze by zbyvalo mene nez 5 do maxima 
            else:
                direction = "out"
                new_value = self.zoom_slider.get()-self.zoom_increment
                if self.zoom_slider._from_ <= new_value:
                    self.zoom_slider.set(new_value)
                    self.percent2.configure(text=str(int(new_value)) + " %")
                else:
                    self.zoom_slider.set(self.zoom_slider._from_) # pro pripad, ze by zbyvalo vice nez 5 do minima
            
            if len(self.all_images) != 0: # update zobrazeni
                if self.ifz_located == True:
                    center_image_index = int((len(self.image_queue)-1)/2) * self.ifz_count
                    self.view_image(None,self.converted_images[center_image_index + self.increment_of_ifz_image],True)
                    #self.view_image(None,self.converted_images[self.increment_of_ifz_image])  
                else:
                    self.view_image(self.increment_of_image,None,True)
        
        def mouse_wheel2(e): # posouvat obrazky
            direction = -e.delta
            if direction < 0:
                self.previous_image()
            else:
                self.next_image()

        self.main_frame.bind("<MouseWheel>",mouse_wheel1)
        self.frame_with_path.bind("<MouseWheel>",mouse_wheel2)
        self.console.bind("<MouseWheel>",mouse_wheel2)
        if self.image_film == True:
            self.image_film_frame_left.bind("<MouseWheel>",mouse_wheel2)
            self.image_film_frame_center.bind("<MouseWheel>",mouse_wheel2)
            self.image_film_frame_right.bind("<MouseWheel>",mouse_wheel2)
            self.images_film_center.bind("<MouseWheel>",mouse_wheel2)
        self.unbind_list.append("<MouseWheel>")
        
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
            self.root.focus_set()
            self.start(self.path_set.get())
        self.path_set.bind("<Return>",save_path_enter_btn)

        def open_path():
            checked_path = Tools.path_check(self.path_for_explorer)
            if checked_path != False and checked_path != "/" and checked_path != "":
                if os.path.exists(checked_path):
                    os.startfile(checked_path)

        def show_context_menu(event):
            context_menu.tk_popup(event.x_root, event.y_root)

        self.main_frame.bind("<Button-3>", show_context_menu)
        context_menu = tk.Menu(self.root, tearoff=0,fg="white",bg="black")
        context_menu.add_command(label="Otevřít cestu", command=lambda: open_path(),font=("Arial",22,"bold"))
        context_menu.add_separator()
        context_menu.add_command(label="Otevřít v novém okně", command=lambda: self.view_image(self.increment_of_image,in_new_window=True),font=("Arial",22,"bold"))
        context_menu.add_separator()
        context_menu.add_command(label="Malovat", command=lambda: self.switch_drawing_mode(),font=("Arial",22,"bold"))
        context_menu.add_separator()
        context_menu.add_command(label="Otočit", command=lambda: self.rotate_image(),font=("Arial",22,"bold"))
        context_menu.add_separator()
        context_menu.add_command(label="Kopírovat", command=lambda: self.copy_image(self.image_browser_path),font=("Arial",22,"bold"))
        context_menu.add_separator()
        context_menu.add_command(label="Přesunout", command=lambda: self.move_image(),font=("Arial",22,"bold"))
        context_menu.add_separator()
        context_menu.add_command(label="Reset", command=lambda: self.Reset_all(),font=("Arial",22,"bold"))
        context_menu.add_separator()
        context_menu.add_command(label="Smazat", command=lambda: self.delete_image(),font=("Arial",22,"bold"))

        #kdyz je vyuzit TRIMAZKON, jako vychozi prohlizec obrazku
        if self.IB_as_def_browser_path != None:
            self.path_set.delete("0","200")
            self.path_set.insert("0", self.IB_as_def_browser_path)
            Tools.add_colored_line(self.console,f"{app_name}, jako výchozí prohlížeč!","white",None,True)
            self.root.update_idletasks()
            self.image_browser_path = self.IB_as_def_browser_path
            self.start(self.IB_as_def_browser_path)

        #hned na zacatku to vleze do defaultni slozky
        elif self.path_given != "":
            self.path_set.delete("0","200")
            self.path_set.insert("0", self.path_given)
            Tools.add_colored_line(self.console,"Nastavené změny uloženy","green",None,True)
            self.root.update_idletasks()
            self.image_browser_path = self.path_given
            self.start(self.path_given)
        else:
            path = self.config_path
            config_data = Tools.read_json_config()
            if len(config_data["image_browser_settings"]["path_history_list"]) != 0:
                path_from_history = config_data["image_browser_settings"]["path_history_list"][0]
                self.path_set.delete("0","200")
                self.path_set.insert("0", path_from_history)
                Tools.add_colored_line(self.console,"Byla vložena cesta z konfiguračního souboru","white",None,True)
                self.root.update_idletasks()
                self.image_browser_path = path_from_history
                self.start(path_from_history)
            elif path != "/" and path != False:
                self.path_set.delete("0","200")
                self.path_set.insert("0", path)
                Tools.add_colored_line(self.console,"Byla vložena cesta z konfiguračního souboru","white",None,True)
                self.root.update_idletasks()
                self.image_browser_path = path
                self.start(path)
            else:
                Tools.add_colored_line(self.console,"Konfigurační soubor obsahuje neplatnou cestu k souborům\n(můžete vložit v pokročilém nastavení)","orange",None,True)

if not app_running_status:
    root.update_idletasks()
    root.update()
    Image_browser(root,None,"")
    root.mainloop()