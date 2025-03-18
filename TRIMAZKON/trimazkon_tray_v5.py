
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
# from openpyxl import load_workbook
import customtkinter
import tkinter as tk
import pyperclip
import os
import subprocess
import sys
import json
import threading
import IP_setting_v4 as IP_setting
from functools import partial
import win32con
from win32api import *
from win32gui import *

class Tools:
    @classmethod
    def resource_path(cls,relative_path):
        """ Get the absolute path to a resource, works for dev and for PyInstaller """
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    
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
    def read_json_config(cls,initial_path,config_json_filename): # Funkce vraci data z configu
        """
        Funkce vrací data z konfiguračního souboru

        data jsou v pořadí:

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
        \nDELETING SETTINGS\n
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

        if os.path.exists(initial_path+config_json_filename):
            try:
                with open(initial_path+config_json_filename, "r") as file:
                    config_data = json.load(file)

                return config_data

            except Exception as e:
                print(f"Nejdřív zavřete soubor {config_json_filename} Chyba: {e}")
                return []
        else:
            print(f"Chybí konfigurační soubor {config_json_filename}")
            return []

class WindowsBalloonTip:
    """
    Windows system notification (balloon tip).
    """
    _class_registered = False  # Ensures window class is registered only once

    def __init__(self, title, msg, app_icon):
        message_map = {
            win32con.WM_DESTROY: self.OnDestroy,
        }

        hinst = GetModuleHandle(None)
        class_name = "PythonTaskbar"
        try:
            if not WindowsBalloonTip._class_registered:
                # Register the Window class once
                wc = WNDCLASS()
                wc.hInstance = hinst
                wc.lpszClassName = class_name
                wc.lpfnWndProc = message_map
                RegisterClass(wc)
                WindowsBalloonTip._class_registered = True  # Mark as registered
        except Exception:
            wc = WNDCLASS()
            wc.hInstance = hinst
            wc.lpszClassName = class_name
            wc.lpfnWndProc = message_map
            RegisterClass(wc)

        # Create a new window (without re-registering the class)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow(class_name, "Taskbar", style, 
                                 0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 
                                 0, 0, hinst, None)

        UpdateWindow(self.hwnd)

        # Load icon
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            hicon = LoadImage(hinst, app_icon, win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
            hicon = LoadIcon(0, win32con.IDI_APPLICATION)

        # Display notification
        # flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)

        Shell_NotifyIcon(NIM_MODIFY, 
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,
                          hicon, "Balloon tooltip", msg, 200, title))

        # time.sleep(10)  # Display the notification for 10 seconds
        # self.cleanup()

    def cleanup(self):
        """ Removes the notification icon and destroys the window. """
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        DestroyWindow(self.hwnd)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        """ Handles window destruction. """
        self.cleanup()
        PostQuitMessage(0)  # Terminate the app.

class tray_app_service:
    def __init__(self,initial_path,icon_path,exe_name,config_name):
        # self.app_icon = Tools.resource_path(icon_path)
        self.app_icon = icon_path
        self.config_filename = config_name
        self.initial_path = initial_path
        self.main_app_exe_name = exe_name
        self.ip_set_instance = IP_setting.main(None,None,None,initial_path,None,config_name,True)
        self.excel_config_filename = "TRIMAZKON_address_list.xlsx"
        config_data = Tools.read_json_config(self.initial_path,self.config_filename)
        try:
            self.selected_language = config_data["app_settings"]["default_language"]
        except Exception as e:
            print(config_data,e)
            self.selected_language = "cz"
        
    def clear_frame(self,frame):
        for widget in frame.winfo_children():
            if widget.winfo_exists():
                widget.unbind("<Enter>")
                widget.unbind("<Leave>")
                widget.unbind("<Return>")
                widget.unbind("<Button-1>")
                widget.unbind("<Button-3>")
                widget.unbind("<Double-1>")
                widget.unbind("<MouseWheel>")
                widget.destroy()
    
    def on_closing(self,to_close):
        try:
            to_close.destroy()
        except Exception as e:
            print(e)

    def read_config(self):
        """
        TASK SYNTAX:\n
        'name'\n
        'operating_path'\n
        'max_days'\n
        'files_to_keep'\n
        'frequency'\n
        'date_added'\n
        'del_log'\n
        """
        
        self.task_log_list=  []

        with open(self.initial_path + self.config_filename, "r") as file:
            data = json.load(file)

        try:
            task_list = data["task_list"]
        except KeyError:
            task_list = []

        for tasks in task_list:
            if len(tasks["del_log"]) > 0:
                self.task_log_list.append(tasks["del_log"])

        # print("config raw tasks data: ", task_list)
        return task_list

    def save_new_log(self,task_name:str,new_log:str): #musim mit na vstupu nazev tasku abych ho mohl najit a prepsat to u nej
        """
        LOG_SYNTAX:\n
        "del_date"\n
        "files_checked"\n
        "files_older"\n
        "files_deleted"\n
        """
        self.check_task_existence()
        current_tasks = self.read_config()

        for tasks in current_tasks:
            if str(tasks["name"]) == task_name:
                tasks["del_log"].append(new_log) # log mazání (pocet smazanych,datum,seznam smazanych)
                self.save_task_to_config(current_tasks)
                break
        
    def delete_log(self,task_name:str,childroot): #musim mit na vstupu nazev tasku abych ho mohl najit a prepsat to u nej
        self.check_task_existence()
        current_tasks = self.read_config()

        for tasks in current_tasks:
            if str(tasks["name"]) == task_name:
                tasks["del_log"] = []
                self.save_task_to_config(current_tasks)    
                break

        self.show_task_log(root_given=childroot)
        
    def save_task_to_config(self,new_tasks):
        with open(self.initial_path + self.config_filename, "r") as file:
            config_data = json.load(file)

        # settings = data["settings"]
        config_data["task_list"] = new_tasks

        with open(self.initial_path + self.config_filename, "w") as file:
            json.dump(config_data, file, indent=4)

    def delete_task(self,task,root=None,only_scheduler = False):
        """
        if only_scheduler: task = task name directly
        """
        def delete_from_scheduler(name_of_task):
            cmd_command = f"schtasks /Delete /TN {name_of_task} /F"
            subprocess.call(cmd_command,shell=True,text=True)

        if only_scheduler:
            self.check_task_existence()
            delete_from_scheduler(task)
            return
            
        self.check_task_existence()
        all_tasks = self.read_config()
        delete_from_scheduler(task["name"])
        all_tasks.pop(all_tasks.index(task))
        
        self.save_task_to_config(all_tasks)
        try:
            self.show_all_tasks(root_given=root)
        except Exception as e:
            print(e)
            
    def call_edit_task(self,command_given):
        print("calling main app with: ",command_given)
        process = subprocess.Popen(command_given, 
                                    shell=True,
                                    text=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    creationflags=subprocess.CREATE_NO_WINDOW)
        stdout, stderr = process.communicate()
        try:
            stdout_str = stdout.decode('utf-8')
            stderr_str = stderr.decode('utf-8')
            print(stdout_str,stderr_str)
        except Exception as e:
            print(stdout,stderr)
     
    def show_context_menu(self,root,event,widget,task):
        self.check_task_existence()
        # all_tasks = self.read_config()
        context_menu = tk.Menu(root,tearoff=0,fg="white",bg="black",font=("Arial",20,"bold"))
        preset_font=("Arial",18,"bold")
        path = task["operating_path"]

        open_path = "Otevřít cestu"
        copy_path = "Kopírovat cestu"
        execute_task = "Vykonat úkol"
        edit_task = "Upravit úkol"
        delete_task = "Odstranit úkol"
        show_history = "Zobrazit historii mazání"
        delete_history = "Vymazat historii mazání"
        if self.selected_language == "en":
            open_path = "Open path"
            copy_path = "Copy path"
            execute_task = "Execute task"
            edit_task = "Edit task"
            delete_task = "Delete task"
            show_history = "Show deletion history"
            delete_history = "Delete deletion history"

        if widget == "path":
            context_menu.add_command(label=open_path,font=preset_font, command=lambda: os.startfile(path))
            context_menu.add_separator()
            context_menu.add_command(label=copy_path,font=preset_font, command=lambda: pyperclip.copy(path))

        elif widget == "time" or widget == "settings" or widget == "name":
            name_of_task = task["name"]
            path_app_location = str(self.initial_path+"/"+self.main_app_exe_name) 
            print("calling path: ",path_app_location)
            operating_path_TS = str(task["operating_path"])
            cured_path = r"{}".format(operating_path_TS)
            task_command = path_app_location + " deleting " + name_of_task + " \"" + cured_path + "\" " + str(task["max_days"]) + " " + str(task["files_to_keep"])+ " " + str(task["more_dirs"])+ " " + str(task["selected_option"]) + " " + str(task["creation_date"])
            edit_task_command = path_app_location + " edit_existing_task " + name_of_task + " \"" + cured_path + "\" " + str(task["max_days"]) + " " + str(task["files_to_keep"])+ " " + str(task["frequency"])+ " " + str(task["more_dirs"])+ " " + str(task["selected_option"]) + " " + str(task["creation_date"]) + " " + str(root) + " " + str(self.selected_language)
            context_menu.add_command(label=execute_task,font=preset_font,command=lambda: subprocess.call(task_command,shell=True,text=True))
            context_menu.add_separator()
            # context_menu.add_command(label=edit_task,font=preset_font,command=lambda: os.startfile("taskschd.msc"))
            context_menu.add_command(label=edit_task,font=preset_font,command=lambda: self.call_edit_task(edit_task_command))
            context_menu.add_separator()
            context_menu.add_command(label=delete_task,font=preset_font,command=lambda: self.delete_task(task,root))
            context_menu.add_separator()
            context_menu.add_command(label=show_history,font=preset_font,command=lambda: self.show_task_log(True,task_given=task))

        elif widget == "del_log":
            context_menu.add_command(label=open_path,font=preset_font, command=lambda: os.startfile(path))
            context_menu.add_separator()
            context_menu.add_command(label=copy_path,font=preset_font, command=lambda: pyperclip.copy(path))
            context_menu.add_separator()
            context_menu.add_command(label=delete_history,font=preset_font, command=lambda: self.delete_log(task_name=task["name"],childroot=root))

        context_menu.tk_popup(event.x_root, event.y_root)

    def check_task_existence(self):
        """
        Zjistí zda se daný název tasku nachází v TS\n
        - pokud ne (manuálně odmazán z TS), vymaže záznam tasku v config souboru
        """
        def check_task_status(taskname):
            process = subprocess.Popen(f'schtasks /query /tn \"{taskname}\" /v /fo LIST',
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE,
                                                    creationflags=subprocess.CREATE_NO_WINDOW)
            stdout, stderr = process.communicate()
            try:
                stdout_str = stdout.decode('utf-8')
                stderr_str = stderr.decode('utf-8')
                data = str(stdout_str)
                error_data = str(stderr_str)
            except UnicodeDecodeError:
                try:
                    stdout_str = stdout.decode('cp1250')
                    stderr_str = stderr.decode('cp1250')
                    data = str(stdout_str)
                    error_data = str(stderr_str)
                except UnicodeDecodeError:
                    data = str(stdout)
                    error_data = str(stderr)
            if "ERROR" in error_data:
                return False
            else:
                return True
                
        all_tasks = self.read_config()
        non_existent_tasks = []
        for i in range(0,len(all_tasks)):
            taskname = str(all_tasks[i]["name"])
            task_presence = check_task_status(taskname)
            if not task_presence:
                non_existent_tasks.append(taskname)
        print("non existent tasks: ",non_existent_tasks)
        
        if len(non_existent_tasks) > 0:
            for deleted_tasks in non_existent_tasks:
                for tasks in all_tasks:
                    if deleted_tasks == tasks["name"]:
                        print("deleting: ",all_tasks.index(tasks))
                        all_tasks.pop(all_tasks.index(tasks))
                        break
            self.save_task_to_config(all_tasks)

    def show_all_tasks(self,toplevel=False,root_given = False,maximalized=False):
        try:
            self.selected_language = Tools.read_json_config(self.initial_path,self.config_filename)["app_settings"]["default_language"]
        except Exception as e:
            print(e)
        if root_given != False:
            child_root = root_given
            self.clear_frame(child_root)
        else:
            if not toplevel:
                child_root = customtkinter.CTk()
            else:
                child_root = customtkinter.CTkToplevel()
            child_root.after(200, lambda: child_root.iconbitmap(self.app_icon))
            child_root.title("Seznam nastavených úkolů (task scheduler)")
            if self.selected_language == "en":
                child_root.title("List of scheduled tasks (task scheduler)")

        if maximalized:
            child_root.after(0, lambda:child_root.state('zoomed'))
        # main_frame = customtkinter.CTkFrame(master=child_root,corner_radius=0)
        main_frame = customtkinter.CTkScrollableFrame(master=child_root,corner_radius=0)
        self.check_task_existence()
        all_tasks = self.read_config()
        print("all_tasks: ",all_tasks)
        i=0
        for tasks in all_tasks:
            task_name = customtkinter.CTkFrame(master=main_frame,corner_radius=0,border_width=0,height= 50,fg_color="#636363")
            task_name_str = str(tasks["name"])
            task_name_text = customtkinter.CTkLabel(master=task_name,text = "Úkol "+str(i+1) + f" (scheduler název: {task_name_str})",font=("Arial",20,"bold"),anchor="w")
            date_added_str = str(tasks["date_added"])
            task_date_accessed = customtkinter.CTkLabel(master=task_name,text = f"Přidáno: {date_added_str}",font=("Arial",20),anchor="e")
            task_name_text.pack(pady=(5,1),padx=10,anchor="w",side="left")
            task_date_accessed.pack(pady=(5,1),padx=10,anchor="e",side="right")
            task_name.pack(pady=(10,0),padx=5,side="top",fill="x")
            task_name.bind("<Button-3>",lambda e,widget = "name",task=tasks: self.show_context_menu(child_root,e,widget,task))
            task_name_text.bind("<Button-3>",lambda e,widget = "name",task=tasks: self.show_context_menu(child_root,e,widget,task))

            task_frame = customtkinter.CTkFrame(master=main_frame,corner_radius=0,border_width=3,height= 50,border_color="#636363")
            param0_frame = customtkinter.CTkFrame(master=task_frame,corner_radius=0,border_width=0,height= 50)
            param0_subframe1 = customtkinter.CTkFrame(master=param0_frame,corner_radius=0,border_width=2,height= 50,width=230,fg_color="#212121")
            param0_label = customtkinter.CTkLabel(master=param0_subframe1,text = "Typ mazání: ",font=("Arial",20,"bold"),anchor="w")
            param0_label.pack(pady=10,padx=(10,3),anchor="w",side="left")
            param0_subframe2 = customtkinter.CTkFrame(master=param0_frame,corner_radius=0,border_width=2,height= 50,fg_color="#212121")
            param0_label2 = customtkinter.CTkLabel(master=param0_subframe2,text = "",font=("Arial",20),anchor="w")
            param0_label2.pack(pady=10,padx=(10,3),anchor="w",side="left")
            param0_subframe1.pack(side="left")
            param0_subframe1.propagate(0)
            param0_subframe2.pack(side="left",fill="both",expand=True)
            param0_frame.pack(pady=(3,0),padx=3,fill="x",side="top")
            if int(tasks["selected_option"]) == 1:
                param0_label2.configure(text = "Redukce starších souborů")
                if self.selected_language == "en":
                    param0_label2.configure(text = "Reducing older files")
            elif int(tasks["selected_option"]) == 2:
                param0_label2.configure(text = "Redukce novějších, mazání starších souborů")
                if self.selected_language == "en":
                    param0_label2.configure(text = "Reducing newer, deleting older files")
            elif int(tasks["selected_option"]) == 3:
                param0_label2.configure(text = "Mazání adresářů podle názvu")
                if self.selected_language == "en":
                    param0_label2.configure(text = "Deleting directories by name")
            elif int(tasks["selected_option"]) == 4:
                param0_label2.configure(text = "Mazání starších adresářů")
                if self.selected_language == "en":
                    param0_label2.configure(text = "Deleting older directories")
                    
            param1_frame = customtkinter.CTkFrame(master=task_frame,corner_radius=0,border_width=0,height= 50)
            param1_subframe1 = customtkinter.CTkFrame(master=param1_frame,corner_radius=0,border_width=2,height= 50,width=230,fg_color="#212121")
            param1_label = customtkinter.CTkLabel(master=param1_subframe1,text = "Čas spuštění (denně): ",font=("Arial",20,"bold"),anchor="w")
            param1_label.pack(pady=10,padx=(10,3),anchor="w",side="left")
            param1_subframe2 = customtkinter.CTkFrame(master=param1_frame,corner_radius=0,border_width=2,height= 50,fg_color="#212121")
            param1_label2 = customtkinter.CTkLabel(master=param1_subframe2,text = str(tasks["frequency"]),font=("Arial",20),anchor="w")
            param1_label2.pack(pady=10,padx=(10,3),anchor="w",side="left")
            param1_subframe1.pack(side="left")
            param1_subframe1.propagate(0)
            param1_subframe2.pack(side="left",fill="both",expand=True)
            param1_frame.pack(pady=(0,0),padx=3,fill="x",side="top")
            param1_label2.bind("<Button-3>",lambda e,widget = "time",task=tasks: self.show_context_menu(child_root,e,widget,task))
            param1_label.bind("<Button-3>",lambda e,widget = "time",task=tasks: self.show_context_menu(child_root,e,widget,task))
            param1_subframe1.bind("<Button-3>",lambda e,widget = "time",task=tasks: self.show_context_menu(child_root,e,widget,task))
            param1_subframe2.bind("<Button-3>",lambda e,widget = "time",task=tasks: self.show_context_menu(child_root,e,widget,task))

            param2_frame = customtkinter.CTkFrame(master=task_frame,corner_radius=0,border_width=1,height= 50)
            param2_subframe1 = customtkinter.CTkFrame(master=param2_frame,corner_radius=0,border_width=2,height= 50,width=230,fg_color="#212121")
            param2_label = customtkinter.CTkLabel(master=param2_subframe1,text = "Pracuje v: ",font=("Arial",20,"bold"),anchor="w")
            param2_label.pack(pady=10,padx=(10,3),anchor="w",side="left")
            param2_subframe2 = customtkinter.CTkFrame(master=param2_frame,corner_radius=0,border_width=2,height= 50,fg_color="#212121")
            param2_label2 = customtkinter.CTkLabel(master=param2_subframe2,text = str(tasks["operating_path"]),font=("Arial",20),anchor="w")
            param2_label2.pack(pady=10,padx=(10,3),anchor="w",side="left")
            param2_subframe1.pack(side="left")
            param2_subframe1.propagate(0)
            param2_subframe2.pack(side="left",fill="both",expand=True)
            param2_frame.pack(pady=(0,0),padx=3,fill="x",side="top")
            param2_label2.bind("<Button-3>",lambda e,widget = "path",task=tasks: self.show_context_menu(child_root,e,widget,task))
            param2_subframe2.bind("<Button-3>",lambda e,widget = "path",task=tasks: self.show_context_menu(child_root,e,widget,task))
            param2_subframe1.bind("<Button-3>",lambda e,widget = "path",task=tasks: self.show_context_menu(child_root,e,widget,task))

            param4_frame = customtkinter.CTkFrame(master=task_frame,corner_radius=0,border_width=0,height= 50)
            param4_subframe1 = customtkinter.CTkFrame(master=param4_frame,corner_radius=0,border_width=2,height= 50,width=230,fg_color="#212121")
            param4_label = customtkinter.CTkLabel(master=param4_subframe1,text = "Procházet subsložky: ",font=("Arial",20,"bold"),anchor="w")
            param4_label.pack(pady=10,padx=(10,3),anchor="w",side="left")
            param4_subframe2 = customtkinter.CTkFrame(master=param4_frame,corner_radius=0,border_width=2,height= 50,fg_color="#212121")
            param4_label2 = customtkinter.CTkLabel(master=param4_subframe2,text = "",font=("Arial",20),anchor="w")
            param4_label2.pack(pady=10,padx=(10,3),anchor="w",side="left")
            param4_subframe1.pack(side="left")
            param4_subframe1.propagate(0)
            param4_subframe2.pack(side="left",fill="both",expand=True)
            if int(tasks["selected_option"]) != 3 and int(tasks["selected_option"]) != 4: # u adresářů se neprochází subsložky
                param4_frame.pack(pady=(0,0),padx=3,fill="x",side="top")
            if int(tasks["more_dirs"]) == 1:
                param4_label2.configure(text = "ANO")
                if self.selected_language == "en":
                    param4_label2.configure(text = "YES")
            else:
                param4_label2.configure(text = "NE")
                if self.selected_language == "en":
                    param4_label2.configure(text = "NO")

            param3_frame = customtkinter.CTkFrame(master=task_frame,corner_radius=0,border_width=1,height= 50,fg_color="#212121")
            param3_label = customtkinter.CTkLabel(master=param3_frame,text = "Nastavení: ",font=("Arial",20,"bold"),anchor="w")
            older_then_str = str(tasks["max_days"])
            files_to_keep_str = str(tasks["files_to_keep"])
            creation_date = "řídit se podle: data změny"
            creation_date_eng = "to decide by: modification date"
            if int(tasks["creation_date"]) == 1:
                creation_date = "řídit se podle: data vytvoření"
                creation_date_eng = "to decide by: creation date"
            param3_label2 = customtkinter.CTkLabel(master=param3_frame,text = "",font=("Arial",20),anchor="w")
            param3_label.pack(pady=10,padx=(10,0),anchor="w",side="left")
            param3_label2.pack(pady=10,padx=(10,0),anchor="w",side="left")
            param3_frame.pack(pady=(0,3),padx=3,fill="x",side="top")
            if int(tasks["selected_option"]) == 3:
                param3_label2.configure(text = f"starší než: {older_then_str} dní, {creation_date}")
                if self.selected_language == "en":
                    param3_label2.configure(text = f"older then: {older_then_str} days, {creation_date_eng}")
            elif int(tasks["selected_option"]) == 4:
                param3_label2.configure(text = f"starší než: {older_then_str} dní, minimum = {files_to_keep_str} adresářů, {creation_date}")
                if self.selected_language == "en":
                    param3_label2.configure(text = f"older then: {older_then_str} days, minimum = {files_to_keep_str} directories, {creation_date_eng}")
            else:                    
                param3_label2.configure(text = f"starší než: {older_then_str} dní, minimum = {files_to_keep_str} souborů, {creation_date}")
                if self.selected_language == "en":
                    param3_label2.configure(text = f"older then: {older_then_str} days, minimum = {files_to_keep_str} files, {creation_date_eng}")

                
            param3_label.bind("<Button-3>",lambda e,widget = "settings",task=tasks: self.show_context_menu(child_root,e,widget,task))
            param3_label2.bind("<Button-3>",lambda e,widget = "settings",task=tasks: self.show_context_menu(child_root,e,widget,task))
            param3_frame.bind("<Button-3>",lambda e,widget = "settings",task=tasks: self.show_context_menu(child_root,e,widget,task))
            task_frame.pack(pady=(0,0),padx=5,fill="x",side="top")

            if self.selected_language == "en":
                task_name_text.configure(text = "Task "+str(i+1) + f" (scheduler name: {task_name_str})")
                task_date_accessed.configure(text = f"Added: {date_added_str}")
                param0_label.configure(text = "Deletion mode: ")
                param1_label.configure(text = "Start time (daily): ")
                param2_label.configure(text = "Working in: ")
                param4_label.configure(text = "Browse subfolders: ")
                param3_label.configure(text = "Parameters set: ")
            i+=1

        if len(all_tasks) == 0:
            task_label = customtkinter.CTkLabel(master=main_frame,text = "Nejsou nastaveny žádné úkoly...",font=("Arial",22,"bold"),anchor="w")
            task_label.pack(pady=10,padx=10,fill="x",side="top",anchor="w")
            if self.selected_language == "en":
                task_label.configure(text = "No tasks are set...")
            child_root.after(2000, lambda: child_root.destroy())
            
        # main_frame.pack(fill="both",side="top")
        main_frame.pack(fill="both",side="top",expand=True)
        child_root.update()
        child_root.update_idletasks()
        # child_root.geometry(f"{child_root.winfo_width()}x{child_root.winfo_height()+10}")
        child_root.geometry(f"{1200}x{800}")
        child_root.focus_force()
        child_root.focus()
        # child_root.mainloop()
        # child_root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(child_root))
        try:
            child_root.wait_window()
        except Exception:
            pass
        # child_root.after(10, child_root.wait_window())

    def show_task_log(self,specify_task=False,task_given = None,root_given = False,maximalized=False,toplevel = False):
        try:
            self.selected_language = Tools.read_json_config(self.initial_path,self.config_filename)["app_settings"]["default_language"]
        except Exception as e:
            print(e)
        
        if not root_given:
            if not toplevel:
                child_root = customtkinter.CTk()
            else:
                child_root = customtkinter.CTkToplevel()
            child_root.after(200, lambda: child_root.iconbitmap(self.app_icon))
            child_root.title("Záznam o vymazaných souborech")
            if self.selected_language == "en":
                child_root.title("Record of deleted files")
        else:
            child_root = root_given
            self.clear_frame(child_root)
        
        if maximalized:
            child_root.after(0, lambda:child_root.state('zoomed'))
 
        main_frame = customtkinter.CTkScrollableFrame(master=child_root,corner_radius=0)
        self.check_task_existence()
        current_tasks = self.read_config()

        def hide_details(task,given_task_frame,button):
            self.clear_frame(given_task_frame)
            button.configure(text="v")
            given_task_frame.configure(height=0)
            given_task_frame.update()
            given_task_frame.update_idletasks()
            button.unbind("<Button-1>")
            button.bind("<Button-1>",lambda e,tasks = task, log_frame = given_task_frame, button_details = button: show_details(tasks,log_frame,button_details))
            
        def show_details(task,given_task_frame,button,get_log_count = False):
            """
            del_date": f"Datum provedení: {output_data[3]}",
            files_checked": f"Zkontrolováno: {output_data[0]} souborů",
            files_older": f"Starších: {output_data[1]} souborů",
            files_newer": f"Novějších: {output_data[4]} souborů",
            files_deleted": f"Smazáno: {output_data[2]} souborů",
            path_count": f"Prohledáno: {output_data[5]} subsložek",
            """
            all_task_logs = task["del_log"]
            if get_log_count:
                return len(all_task_logs)
            
            date_added_label = "Datum provedení"
            files_checked_label = "Zkontrolováno"
            files_older_label ="Starších"
            files_newer_label = "Novějších"
            files_deleted_label = "Smazáno"
            path_count_label = "Prohledáno subsložek"
            if self.selected_language == "en":
                date_added_label = "Date of execution"
                files_checked_label = "Total checked"
                files_older_label = "Total older"
                files_newer_label = "Total newer"
                files_deleted_label = "Total deleted"
                path_count_label = "Browsed subdirectories"
            
            description_frame = customtkinter.CTkFrame(master=given_task_frame,corner_radius=0,fg_color="#636363")
            description = customtkinter.CTkLabel(master=description_frame,text = "",font=("Arial",20,"bold"),justify="left",anchor="w",)
            description.pack(pady=(0,10),padx=10,side="left")
            description_frame.pack(pady=0,padx=0,fill="x",expand=True,side="top")
            column_headers = customtkinter.CTkFrame(master=given_task_frame,corner_radius=0,border_width=0,height= 50)
            headers_font = ("Arial",18,"bold")
            colum_width = 150
            column_1 = customtkinter.CTkFrame(master=column_headers,corner_radius=0,border_width=2,border_color="#636363",height= 50,width=250)
            column_2 = customtkinter.CTkFrame(master=column_headers,corner_radius=0,border_width=2,border_color="#636363",height= 50,width=colum_width)
            column_3 = customtkinter.CTkFrame(master=column_headers,corner_radius=0,border_width=2,border_color="#636363",height= 50,width=colum_width)
            column_4 = customtkinter.CTkFrame(master=column_headers,corner_radius=0,border_width=2,border_color="#636363",height= 50,width=colum_width)
            column_5 = customtkinter.CTkFrame(master=column_headers,corner_radius=0,border_width=2,border_color="#636363",height= 50,width=colum_width)
            column_6 = customtkinter.CTkFrame(master=column_headers,corner_radius=0,border_width=2,border_color="#636363",height= 50,width=colum_width+70)
            param1_label = customtkinter.CTkLabel(master=column_1,text = date_added_label,font=headers_font)
            param2_label = customtkinter.CTkLabel(master=column_2,text = files_checked_label,font=headers_font)
            param3_label = customtkinter.CTkLabel(master=column_3,text = files_older_label,font=headers_font)
            param4_label = customtkinter.CTkLabel(master=column_4,text = files_newer_label,font=headers_font)
            param5_label = customtkinter.CTkLabel(master=column_5,text = files_deleted_label,font=headers_font)
            param6_label = customtkinter.CTkLabel(master=column_6,text = path_count_label,font=headers_font)
            param1_label.pack(pady=10,padx=10)
            param2_label.pack(pady=10,padx=10)
            param3_label.pack(pady=10,padx=10)
            param4_label.pack(pady=10,padx=10)
            param5_label.pack(pady=10,padx=10)
            param6_label.pack(pady=10,padx=10)
            column_1.pack(pady=0,padx=0,anchor="w",side="left") #datum
            column_2.pack(pady=0,padx=0,anchor="w",side="left") #zkontrolovano
            if int(task["selected_option"]) == 1 or int(task["selected_option"]) == 2 or int(task["selected_option"]) == 4:
                column_3.pack(pady=0,padx=0,anchor="w",side="left") #starsich
            if int(task["selected_option"]) == 2:
                column_4.pack(pady=0,padx=0,anchor="w",side="left") #novejsich
            column_5.pack(pady=0,padx=0,anchor="w",side="left") #smazano
            if int(task["more_dirs"]) == 1 and int(task["selected_option"]) < 3:
                column_6.pack(pady=0,padx=0,anchor="w",side="left") #Prohledáno subsložek
            column_headers.pack(pady=0,padx=0,fill="x",side="top")
            column_1.propagate(0)
            column_2.propagate(0)
            column_3.propagate(0)
            column_4.propagate(0)
            column_5.propagate(0)
            column_6.propagate(0)

            if int(tasks["selected_option"]) == 1:
                description.configure(text = "Redukce starších souborů")
                if self.selected_language == "en":
                    description.configure(text = "Reducing older files")
            elif int(tasks["selected_option"]) == 2:
                description.configure(text = "Redukce novějších, mazání starších souborů")
                if self.selected_language == "en":
                    description.configure(text = "Reducing newer, deleting older files")
            elif int(tasks["selected_option"]) == 3:
                description.configure(text = "Mazání adresářů podle názvu")
                if self.selected_language == "en":
                    description.configure(text = "Deleting directories by name")
            elif int(tasks["selected_option"]) == 4:
                description.configure(text = "Mazání starších adresářů")
                if self.selected_language == "en":
                    description.configure(text = "Deleting older directories")

            for logs in all_task_logs:
                log_row = customtkinter.CTkFrame(master=given_task_frame,corner_radius=0,border_width=0,height= 50)
                log_font = ("Arial",20)
                column_11 = customtkinter.CTkFrame(master=log_row,corner_radius=0,border_width=2,border_color="#636363",fg_color="#212121",height= 50,width=250)
                column_22 = customtkinter.CTkFrame(master=log_row,corner_radius=0,border_width=2,border_color="#636363",fg_color="#212121",height= 50,width=colum_width)
                column_33 = customtkinter.CTkFrame(master=log_row,corner_radius=0,border_width=2,border_color="#636363",fg_color="#212121",height= 50,width=colum_width)
                column_44 = customtkinter.CTkFrame(master=log_row,corner_radius=0,border_width=2,border_color="#636363",fg_color="#212121",height= 50,width=colum_width)
                column_55 = customtkinter.CTkFrame(master=log_row,corner_radius=0,border_width=2,border_color="#636363",fg_color="#212121",height= 50,width=colum_width)
                column_66 = customtkinter.CTkFrame(master=log_row,corner_radius=0,border_width=2,border_color="#636363",fg_color="#212121",height= 50,width=colum_width+70)
                param11_label = customtkinter.CTkLabel(master=column_11,text = str(logs["del_date"]),font=log_font,anchor="w")
                param22_label = customtkinter.CTkLabel(master=column_22,text = str(logs["files_checked"]),font=log_font,anchor="w")
                param33_label = customtkinter.CTkLabel(master=column_33,text = str(logs["files_older"]),font=log_font,anchor="w")
                param44_label = customtkinter.CTkLabel(master=column_44,text = str(logs["files_newer"]),font=log_font,anchor="w")
                param55_label = customtkinter.CTkLabel(master=column_55,text = str(logs["files_deleted"]),font=log_font,anchor="w")
                param66_label = customtkinter.CTkLabel(master=column_66,text = str(logs["path_count"]),font=log_font,anchor="w")
                param11_label.pack(pady=10,padx=10,anchor="w",side="left")
                param22_label.pack(pady=10,padx=10,anchor="w",side="left")
                param33_label.pack(pady=10,padx=10,anchor="w",side="left")
                param44_label.pack(pady=10,padx=10,anchor="w",side="left")
                param55_label.pack(pady=10,padx=10,anchor="w",side="left")
                param66_label.pack(pady=10,padx=10,anchor="w",side="left")
                column_11.pack(pady=0,padx=0,anchor="w",side="left")
                column_22.pack(pady=0,padx=0,anchor="w",side="left")
                if int(task["selected_option"]) == 1 or int(task["selected_option"]) == 2 or int(task["selected_option"]) == 4:
                    column_33.pack(pady=0,padx=0,anchor="w",side="left")
                if int(task["selected_option"]) == 2:
                    column_44.pack(pady=0,padx=0,anchor="w",side="left")
                column_55.pack(pady=0,padx=0,anchor="w",side="left")
                if int(task["more_dirs"]) == 1 and int(task["selected_option"]) < 3:
                    column_66.pack(pady=0,padx=0,anchor="w",side="left")

                log_row.pack(pady=0,padx=0,fill="x",side="top")
                column_11.propagate(0)
                column_22.propagate(0)
                column_33.propagate(0)
                column_44.propagate(0)
                column_55.propagate(0)
                column_66.propagate(0)

            button.configure(text="^")
            button.unbind("<Button-1>")
            button.bind("<Button-1>",lambda e,tasks = task, log_frame = given_task_frame, button_details = button: hide_details(tasks,log_frame,button_details))
        
        i=0
        for tasks in current_tasks:
            if specify_task:
                if tasks["name"] != task_given["name"]:
                    i+=1
                    continue #preskoč když se nejedná o hledaný specifický task
            task_frame = customtkinter.CTkFrame(master=main_frame,corner_radius=0,border_width=0)
            header_frame = customtkinter.CTkFrame(master=task_frame,corner_radius=0,border_width=0,fg_color="#636363")
            task_name_str = str(tasks["name"])
            date_added_str = str(tasks["date_added"])
            task_name_text = customtkinter.CTkLabel(master=header_frame,text = "Úkol "+str(i+1) + f" (scheduler název: {task_name_str}), přidáno: {date_added_str}",font=("Arial",20,"bold"),anchor="w",justify="left")
            empty_log_frame = customtkinter.CTkFrame(master=task_frame,corner_radius=0,border_width=0,height=0)
            button_details = customtkinter.CTkButton(master = header_frame,text = "v",font=("Arial",40,"bold"),width = 50,height=50,corner_radius=0,fg_color="#505050")
            button_details.bind("<Button-1>",lambda e,task = tasks, log_frame = empty_log_frame, button = button_details: show_details(task,log_frame,button))
            task_name_text.pack(pady=(5,1),padx=10,anchor="w",side="left")
            button_details.pack(pady=(5),padx=5,anchor="e",side="right")
            header_frame.pack(pady=0,padx=0,anchor="w",side="top",fill="x")
            empty_log_frame.pack(pady=0,padx=0,side="top",anchor="w",fill="x",expand = True)
            button_details.propagate(0)
            header_frame.bind("<Button-3>",lambda e,widget = "del_log",task=tasks: self.show_context_menu(child_root,e,widget,task))
            task_name_text.bind("<Button-3>",lambda e,widget = "del_log",task=tasks: self.show_context_menu(child_root,e,widget,task))

            task_frame.pack(pady=(10,0),padx=10,side = "top",anchor = "w",fill="x",expand = True)
            i+=1

            if specify_task:
                show_details(tasks,empty_log_frame,button_details) #rovnou otevřít (zobrazit detaily)

            if show_details(tasks,None,None,get_log_count=True) == 0:
                button_details.configure(state="disabled")

            if self.selected_language == "en":
                task_name_text.configure(text = "Task "+str(i+1) + f" (scheduler name: {task_name_str}), added: {date_added_str}")

        if len(self.task_log_list) == 0:
            log_text = customtkinter.CTkLabel(master=main_frame,text = "Nebyl nalezen žádný záznam",font=("Arial",22,"bold"),anchor="w")
            log_text.pack(pady=10,padx=10,fill="x",side="top",anchor="w")
            if self.selected_language == "en":
                log_text.configure(text = "No deletion record found")

            child_root.after(2000, lambda: child_root.destroy())

        main_frame.pack(fill="both",side="top",expand=True)
        child_root.update()
        child_root.update_idletasks()
        child_root.geometry(f"{1200}x{800}")
        # child_root.mainloop()
        # child_root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(child_root))
        try:
            child_root.wait_window()
        except Exception:
            pass
        # child_root.after(10, child_root.wait_window())
        # child_root.wait_window()

    def set_selected_ip(self,interface,no_data,no_data2,ip):
        def callback_from_ip_set(output_msg):
            print("callback from ip: ",output_msg)
            self.create_menu(rebuild=True)

            WindowsBalloonTip("Proveden pokus o změnu IP adresy",
                    str(output_msg),
                    self.app_icon)

        interface_name = str(interface).split(" (")[0]
        print("interface_name: ",interface_name)
        interface_ip = str(interface).split(" (")[1].rstrip(")")
        print("interface ip: ",interface_ip)
        if str(ip) == "DHCP":
            self.ip_set_instance.IP_tools.change_to_DHCP(interface_name,interface_ip,callback_from_ip_set)
        else:
            ip_only = str(ip).split(" | ")[0]
            print("ip_corrected: ",ip_only)
            self.ip_set_instance.IP_tools.change_computer_ip(ip_only,interface_name,interface_ip,self.online_addresses,callback_from_ip_set)

    def create_menu(self,rebuild=False):
        def call_main_app():
            command = self.initial_path +"/"+ self.main_app_exe_name + " trigger_by_tray"
            print("calling main app with: ",command)
            # command = command.replace("/","\\")
            # subprocess.call(command,shell=True,text=True)
            process = subprocess.Popen(command, 
                                        shell=True, 
                                        text=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        creationflags=subprocess.CREATE_NO_WINDOW)
            stdout, stderr = process.communicate()
            try:
                stdout_str = stdout.decode('utf-8')
                stderr_str = stderr.decode('utf-8')
                print(stdout_str,stderr_str)
            except Exception as e:
                print(stdout,stderr)
                # print(e)

        def call_show_all_tasks():
            command = self.initial_path +"/"+ self.main_app_exe_name + " open_task_list"
            print("calling main app with: ",command)
            process = subprocess.Popen(command, 
                                        shell=True, 
                                        text=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        creationflags=subprocess.CREATE_NO_WINDOW)
            stdout, stderr = process.communicate()
            try:
                stdout_str = stdout.decode('utf-8')
                stderr_str = stderr.decode('utf-8')
                print(stdout_str,stderr_str)
            except Exception as e:
                print(stdout,stderr)

        def call_show_all_logs():
            command = self.initial_path +"/"+ self.main_app_exe_name + " open_log_list"
            print("calling main app with: ",command)
            process = subprocess.Popen(command, 
                                        shell=True, 
                                        text=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        creationflags=subprocess.CREATE_NO_WINDOW)
            stdout, stderr = process.communicate()
            try:
                stdout_str = stdout.decode('utf-8')
                stderr_str = stderr.decode('utf-8')
                print(stdout_str,stderr_str)
            except Exception as e:
                print(stdout,stderr)
                

        run_app_label = 'Spustit aplikaci TRIMAZKON'
        show_scheduled_tasks_label = 'Nastavené úkoly'
        deletion_log_label = 'Záznamy o mazání'
        shut_down_label = 'Vypnout'
        set_ip_label = "Nastavit IP: "
        if self.selected_language == "en":
            run_app_label = "Run TRIMAZKON application"
            show_scheduled_tasks_label = "Scheduled tasks"
            deletion_log_label = "Record of deleted files"
            shut_down_label = "Quit"
            set_ip_label = "Set IP: "


        online_interfaces = self.ip_set_instance.IP_tools.fill_interfaces()[1]
        self.online_addresses = self.ip_set_instance.IP_tools.get_current_ip_list(online_interfaces)
        online_interfaces_adr= []
        for i in range(0,len(online_interfaces)):
            online_interfaces_adr.append(str(online_interfaces[i]) + " (" + self.online_addresses[i] + ")")
        favourite_project_list = self.ip_set_instance.IP_tools.get_favourite_ips_addr(self.initial_path + self.excel_config_filename)
        favourite_project_list.insert(0,"DHCP")

        print(online_interfaces_adr)
        print(favourite_project_list)

        self.menu = Menu(MenuItem(run_app_label, lambda: call_main_app()),
                         MenuItem(show_scheduled_tasks_label, lambda: call_show_all_tasks()),
                         MenuItem(deletion_log_label, lambda: call_show_all_logs()),
                         *[MenuItem(set_ip_label + str(interface), 
                                    Menu(*[MenuItem(address, partial(self.set_selected_ip, interface, address)) for address in favourite_project_list])
                                    ) for interface in online_interfaces_adr],
                         MenuItem(shut_down_label, lambda: self.quit_application()),
                        )
        if rebuild:
            self.icon.menu = Menu(*self.menu)                                

    def quit_application(self):
        def call_app_shutdown():
            command = self.initial_path +"/"+ self.main_app_exe_name + " app_shutdown"
            print("calling main app with: ",command)
            process = subprocess.Popen(command,
                                        shell=True,
                                        text=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        creationflags=subprocess.CREATE_NO_WINDOW)
            stdout, stderr = process.communicate()
            try:
                stdout_str = stdout.decode('utf-8')
                stderr_str = stderr.decode('utf-8')
                print(stdout_str,stderr_str)
            except Exception as e:
                print(stdout,stderr)

        self.icon.stop()
        try:
            call_app_shutdown()
            # sys.exit(0)
        except Exception as e:
            print(e)

    def main(self):
        def create_image():
            image = Image.open(self.app_icon)
            return image
        
        self.create_menu()
        self.icon = Icon(
            "TRIMAZKON_tooltip",
            create_image(),
            "TRIMAZKON",
            self.menu
        )
        # icon_thread = threading.Thread(target=self.icon.run,)
        # icon_thread.start()
        self.icon.run() # Run the tray icon






# inst = tray_app_service(r"C:\Users\jakub.hlavacek.local\Desktop\JHV\Work\TRIMAZKON/",Tools.resource_path('images/logo_TRIMAZKON.ico'),"TRIMAZKON.exe","TRIMAZKON.json")
# inst.main()

# trimazkon_tray_instance = tray_app_service(r"C:\Users\jakub.hlavacek.local\Desktop\JHV\Work\TRIMAZKON/",Tools.resource_path('images/logo_TRIMAZKON.ico'),"TRIMAZKON.exe","TRIMAZKON.json")
# trimazkon_tray_instance.show_task_log(toplevel=True)