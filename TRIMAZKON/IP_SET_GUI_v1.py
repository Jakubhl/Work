import sys
import win32file
import psutil
import os

class initial_tools:
    @classmethod
    def get_all_app_processes(cls):
        pid_list = []
        num_of_apps = 0
        for process in psutil.process_iter(['pid', 'name']):
            # if process.info['name'] == "TRIMAZKON_test.exe":
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
        found_processes = initial_tools.get_all_app_processes()
        if found_processes[0] > 1:
            return True
        else:
            return False
        
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

testing = False

global_recources_load_error = False
global_licence_load_error = False
exe_path = sys.executable
exe_name = os.path.basename(exe_path)
config_filename = "jhv_IP.json"
app_name = "jhv_IP"
app_version = "1.0.2"
trimazkon_version = "4.3.7"
loop_request = False
root = None
print("exe name: ",exe_name)
if testing:
    exe_name = "trimazkon_test.exe"

app_running_status = initial_tools.check_runing_app_duplicity()
print("already opened app status: ",app_running_status)

import customtkinter
import os
import time
from PIL import Image#, ImageTk
# import Deleting_option_v2 as Deleting
import sharepoint_download as download_database
import IP_setting_v6 as IP_setting
import ip_only_tray_v1 as trimazkon_tray
import ip_set_changelog
from tkinter import filedialog
import tkinter as tk
import threading
import ctypes
import win32pipe, pywintypes, psutil#,win32file
import subprocess
from win32api import *
from win32gui import *
import win32con
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import datetime
import wmi
import json
# import struct
import winreg
import pyperclip

class Subwindows:
    @classmethod
    def call_again_as_admin(cls,input_flag:str,window_title,main_title,language_given="cz"):
        def run_as_admin():# Vyžádání admin práv: nefunkční ve vscode
            if not Tools.is_admin():
                pid = "None"
                try:
                    pid = os.getpid()
                except Exception as e:
                    print(e)
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join([input_flag,str(pid)]), None, 1)
                sys.exit()

        def close_prompt(child_root):
            child_root.grab_release()
            child_root.destroy()

        child_root = customtkinter.CTkToplevel()
        child_root.after(200, lambda: child_root.iconbitmap(app_icon))
        child_root.title(window_title)
        label_frame =       customtkinter.CTkFrame(master = child_root,corner_radius=0)
        warning_icon =      customtkinter.CTkLabel(master = label_frame,text = "",image =customtkinter.CTkImage(Image.open(Tools.resource_path("images/warning.png")),size=(50,50)),bg_color="#212121")
        proceed_label =     customtkinter.CTkLabel(master = label_frame,text = main_title,font=("Arial",25),anchor="w",justify="left")
        warning_icon.       pack(pady=10,padx=30,anchor="n",side = "left")
        proceed_label.      pack(pady=5,padx=(0,10),anchor="w",side = "left")

        button_frame =      customtkinter.CTkFrame(master = child_root,corner_radius=0)
        button_yes =        customtkinter.CTkButton(master = button_frame,text = "ANO",font=("Arial",20,"bold"),width = 200,height=50,corner_radius=0,command=lambda: run_as_admin())
        button_no =         customtkinter.CTkButton(master = button_frame,text = "Zrušit",font=("Arial",20,"bold"),width = 200,height=50,corner_radius=0,command=lambda:  close_prompt(child_root))
        button_no.          pack(pady = 5, padx = (0,10),anchor="e",side="right")
        button_yes.         pack(pady = 5, padx = 10,anchor="e",side="right")
        label_frame.        pack(pady=0,padx=0,anchor="w",side = "top",fill="x",expand=True)
        button_frame.       pack(pady=0,padx=0,anchor="w",side = "top",fill="x",expand=True)
        if language_given == "en":
            button_yes.configure(text = "YES")
            button_no.configure(text = "Cancel")
        child_root.update()
        child_root.update_idletasks()
        child_root.focus()
        child_root.focus_force()
        child_root.grab_set()

    @classmethod
    def confirm_window(cls,prompt_message,title_message,language_given="cz"):
        """
        volá se akorát u delete path history
        """
        selected_option = False
        def selected_yes(child_root):# Vyžádání admin práv: nefunkční ve vscode
            child_root.grab_release()
            child_root.destroy()
            nonlocal selected_option
            selected_option = True

        def close_prompt(child_root):
            child_root.grab_release()
            child_root.destroy()
            nonlocal selected_option
            selected_option = False
            
        child_root = customtkinter.CTkToplevel()
        child_root.after(200, lambda: child_root.iconbitmap(app_icon))
        child_root.title(title_message)
        label_frame = customtkinter.CTkFrame(master = child_root,corner_radius=0)
        proceed_label = customtkinter.CTkLabel(master = label_frame,text = prompt_message,font=("Arial",25),anchor="w",justify="left")
        proceed_label.pack(pady=5,padx=10,anchor="w",side = "left")
        button_frame = customtkinter.CTkFrame(master = child_root,corner_radius=0)
        button_yes =   customtkinter.CTkButton(master = button_frame,text = "ANO",font=("Arial",20,"bold"),width = 200,height=50,corner_radius=0,command=lambda: selected_yes(child_root))
        button_no =    customtkinter.CTkButton(master = button_frame,text = "Zrušit",font=("Arial",20,"bold"),width = 200,height=50,corner_radius=0,command=lambda:  close_prompt(child_root))
        button_no      .pack(pady = 5, padx = 10,anchor="e",side="right")
        button_yes     .pack(pady = 5, padx = 10,anchor="e",side="right")
        label_frame    .pack(pady=0,padx=0,anchor="w",side = "top",fill="x",expand=True)
        button_frame   .pack(pady=0,padx=0,anchor="w",side = "top",fill="x",expand=True)
        if language_given == "en":
            button_yes.configure(text = "YES")
            button_no.configure(text = "Cancel")
        child_root.update()
        child_root.update_idletasks()
        child_root.focus()
        child_root.focus_force()
        child_root.grab_set()
        child_root.wait_window()
        return selected_option

    @classmethod
    def licence_window(cls,check_licence_callback,language_given="cz"):
        def close_prompt(child_root):
            child_root.grab_release()
            child_root.destroy()

        def activate_trial():
            Tools.store_installation_date(refresh_callback = check_licence_callback)
            close_prompt(child_root)

        user_HWID = Tools.get_volume_serial()
        prompt_message1 = f"Nemáte platnou licenci pro spuštění aplikace {app_name}."
        prompt_message2 = f"Váš HWID:"
        prompt_message3 = f"\n{user_HWID}\n"
        prompt_message4 = "odešlete na email: "
        prompt_message5 = "jakub.hlavacek@jhv.cz "
        prompt_message6 = "s žádostí o licenci."
        title_message = "Upozornění"

        if language_given == "en":
            prompt_message1 = f"You do not have a valid license to run the application {app_name}."
            prompt_message2 = f"Your HWID:"
            prompt_message3 = f"\n{user_HWID}\n"
            prompt_message4 = "send to email: "
            prompt_message5 = "jakub.hlavacek@jhv.cz "
            prompt_message6 = "with an application for a license."
            title_message = "Notice"
            
        child_root = customtkinter.CTkToplevel(fg_color="#212121")
        child_root.after(200, lambda: child_root.iconbitmap(app_icon))
        child_root.title(title_message)
        label_frame =       customtkinter.CTkFrame(master = child_root,corner_radius=0)
        warning_icon =      customtkinter.CTkLabel(master = label_frame,text = "",image =customtkinter.CTkImage(Image.open(Tools.resource_path("images/warning.png")),size=(50,50)),bg_color="#212121")
        proceed_label =     customtkinter.CTkLabel(master = label_frame,text = prompt_message1,font=("Arial",25,"bold"),anchor="w",justify="left")
        warning_icon.       pack(pady=20,padx=20,anchor="w",side = "left")
        proceed_label.      pack(pady=(5,0),padx=(0,20),anchor="w",side = "left")
        label_frame.        pack(pady=0,padx=0,anchor="w",side = "top",fill="x",expand=True)

        text_widget = tk.Text(master = child_root,background="#212121",borderwidth=0,height=9)
        Tools.add_colored_line(text_widget,text=prompt_message2,color="gray84",font=("Arial",16),no_indent=True)
        Tools.add_colored_line(text_widget,text=prompt_message3,color="white",font=("Arial",16,"bold"),no_indent=True)
        Tools.add_colored_line(text_widget,text=prompt_message4,color="gray84",font=("Arial",16),no_indent=True, sameline=True)
        Tools.add_colored_line(text_widget,text=prompt_message5,color="skyblue",font=("Arial",16),no_indent=True, sameline=True)
        Tools.add_colored_line(text_widget,text=prompt_message6,color="gray84",font=("Arial",16),no_indent=True, sameline=True)
        text_widget.        pack(pady=10,padx=(30,10),anchor="w",side = "top",fill="both",expand=True)
        button_frame =      customtkinter.CTkFrame(master = child_root,corner_radius=0)
        button_copy =       customtkinter.CTkButton(master = button_frame,text = "Kopírovat HWID",font=("Arial",20,"bold"),width = 200,height=50,corner_radius=0,command=lambda: pyperclip.copy(str(user_HWID)))
        button_close =      customtkinter.CTkButton(master = button_frame,text = "Zavřít",font=("Arial",20,"bold"),width = 200,height=50,corner_radius=0,command=lambda:  close_prompt(child_root))
        trial_btn =         customtkinter.CTkButton(master = button_frame,text = "Aktivovat trial verzi (30 dní)",height=50,corner_radius=0, command = lambda: activate_trial(),font=("Arial",24,"bold"))
        button_close.       pack(pady = 5, padx = (0,10),anchor="e",side="right")
        button_copy.        pack(pady = 5, padx = 10,anchor="e",side="right")
        if not Tools.check_trial_existance():
            trial_btn.      pack(pady =5,padx=(0,0),anchor="e",side="right")
        button_frame.       pack(pady=0,padx=0,anchor="w",side = "top",fill="x",expand=True)

        if language_given == "en":
            button_close.configure(text = "Close")
            button_copy.configure(text = "Copy HWID")
            trial_btn.configure(text = "Activate trial version (30 days)")
        child_root.update()
        child_root.update_idletasks()
        # child_root.geometry("800x260")
        child_root.focus()
        child_root.focus_force()
        child_root.grab_set()

    @classmethod
    def download_new_version_window(cls,new_version,given_log,language_given="cz",force_update = False):
        def close_prompt(child_root):
            child_root.grab_release()
            child_root.destroy()

        def download_the_app():
            def call_installer(msi_path):
                cmd = f'timeout /t 2 && {msi_path}'
                subprocess.Popen(["cmd.exe", "/c", cmd],
                                creationflags=subprocess.CREATE_BREAKAWAY_FROM_JOB | subprocess.CREATE_NO_WINDOW)

            wanted_installer = f"TRIMAZKON-{new_version}-win64.msi"
            sharepoint_instance = download_database.database(wanted_installer,download_new_installer=True)
            output = str(sharepoint_instance.output)
            if "úspěšně" in output:
                if language_given == "en":
                    Tools.add_colored_line(console,"New installer successfully downloaded","green",font=("Arial",22),delete_line=True)
                else:
                    Tools.add_colored_line(console,output,"green",font=("Arial",22),delete_line=True)
            else:
                if language_given == "en":
                    Tools.add_colored_line(console,"New installer download failed","red",font=("Arial",22),delete_line=True)
                else:
                    Tools.add_colored_line(console,output,"red",font=("Arial",22),delete_line=True)
            msi_path = f"{initial_path}Installers/{wanted_installer}"
            call_installer(msi_path)
            child_root.after(1000,lambda: Tools.terminate_pid(os.getpid())) #vypnout thread i s tray aplikací

        def ignore_version():
            Tools.save_to_json_config(str(new_version),"app_settings","ignored_version")
            close_prompt(child_root)

        prompt_message1 = f"Je k dispozici nová verze aplikace: {new_version} !"
        prompt_message2 = f"(Instalace nové verze zachová všechna uživatelská nastavení)\nUpgrade log:"
        title_message = "Upozornění"
        if language_given == "en":
            prompt_message1 = f"New app version available: {new_version} !"
            prompt_message2 = f"(Installing the new version will preserve all user settings)\nUpgrade log:"
            title_message = "Notice"
            
        child_root = customtkinter.CTkToplevel(fg_color="#212121")
        child_root.after(200, lambda: child_root.iconbitmap(app_icon))
        child_root.title(title_message)
        top_frame =         customtkinter.CTkFrame(master = child_root,corner_radius=0,fg_color="#212121")
        warning_icon =      customtkinter.CTkLabel(master = top_frame,text = "",image =customtkinter.CTkImage(Image.open(Tools.resource_path("images/warning.png")),size=(50,50)),bg_color="#212121")
        label_frame =       customtkinter.CTkFrame(master = top_frame,corner_radius=0)
        proceed_label =     customtkinter.CTkLabel(master = label_frame,text = prompt_message1,font=("Arial",25,"bold"),anchor="w",justify="left")
        proceed_label2 =    customtkinter.CTkLabel(master = label_frame,text = prompt_message2,font=("Arial",20),anchor="w",justify="left")
        proceed_label.      pack(pady=(5,0),padx=10,anchor="w",side = "top")
        proceed_label2.     pack(pady=(5,0),padx=10,anchor="w",side = "top")
        warning_icon.       pack(pady=30,padx=30,anchor="w",side = "left")
        label_frame.        pack(pady=0,padx=0,anchor="w",side = "right",fill="x")
        top_frame.          pack(pady=0,padx=0,anchor="w",side = "top")
        text_frame =        customtkinter.CTkFrame(master = child_root,corner_radius=0,fg_color="#212121")
        text_widget =       customtkinter.CTkTextbox(master = text_frame,font=("Arial",22),corner_radius=0,wrap= "word",height=300)
        for rows in given_log:
            text_widget.insert(tk.END,str(rows)+"\n")

        console =           tk.Text(master = text_frame,background="black", wrap="none",borderwidth=0,height=0,state=tk.DISABLED,font=("Arial",20))
        text_widget.        pack(pady=(10,0),padx=10,anchor="w",side = "top",fill="both")
        console.            pack(pady=(10,0),padx=10,anchor="w",side = "top",fill="x")
        text_frame.         pack(pady=0,padx=0,anchor="w",side = "top",fill="both",expand = True)
        text_widget.        configure(state="disabled")
        button_frame =      customtkinter.CTkFrame(master = child_root,corner_radius=0)
        button_close =      customtkinter.CTkButton(master = button_frame,text = "Zavřít",font=("Arial",20,"bold"),width = 200,height=50,corner_radius=0,command=lambda:  close_prompt(child_root))
        button_dwnld =      customtkinter.CTkButton(master = button_frame,text = "Stáhnout novou verzi",font=("Arial",20,"bold"),width = 200,height=50,corner_radius=0,command=lambda:  download_the_app())
        button_idc =        customtkinter.CTkButton(master = button_frame,text = "Tato verze mě nezajímá",font=("Arial",20,"bold"),width = 200,height=50,corner_radius=0,command=lambda:  ignore_version())
        button_close.       pack(pady = 10, padx = (0,10),anchor="e",side="right")
        button_dwnld.       pack(pady = 10, padx = (0,10),anchor="e",side="right")
        if not force_update:
            button_idc.         pack(pady = 10, padx = (0,10),anchor="e",side="right")
        button_frame.       pack(pady=0,padx=0,anchor="w",side = "top",fill="x")

        if language_given == "en":
            button_close.configure(text = "Close")
            button_dwnld.configure(text = "Download the new version")
            button_idc.configure(text = "I don't care about this version")
        child_root.update()
        child_root.update_idletasks()
        child_root.geometry(f"800x{child_root._current_height}")
        child_root.focus()
        child_root.focus_force()
        child_root.grab_set()

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

class Tools:
        task_name = "jhv_IP_startup_tray_setup"
        config_json_filename = config_filename
        setting_list_name = "Settings_recources"
        Tray_thread_name = "Main_app_tray_thread"
        registry_key_path = "Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\WindowsTrmzkn"

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
        def resource_path(cls,relative_path):
            """ Get the absolute path to a resource, works for dev and for PyInstaller """
            # if hasattr(sys, '_MEIPASS'):
            #     return os.path.join(sys._MEIPASS, relative_path)
            # return os.path.join(os.path.abspath("."), relative_path)
            BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.abspath(".")
            return os.path.join(BASE_DIR, relative_path)
        
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
            - tooltip_status
            - ignored_version
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
            default_setting_parameters = ip_set_changelog.default_setting_database_param
            # default_labels = ip_set_changelog.default_setting_database

            if os.path.exists(initial_path+cls.config_json_filename):
                try:
                    output_data = []
                    with open(initial_path+cls.config_json_filename, "r") as file:
                        output_data = json.load(file)

                    if not "tooltip_status" in output_data.get("app_settings", {}):
                        Tools.save_to_json_config("ano","app_settings","tooltip_status")
                        output_data["app_settings"].setdefault("tooltip_status", "ano")
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
            - tooltip_status
            - ignored_version
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
                output="Chybí konfigurační soubor config_TRIMAZKON.xlsx s počáteční cestou...\n"
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
        def save_path(cls,console,path_entered,which_settings = ""):
            path_given = path_entered
            path_checked = Tools.path_check(path_given)
            if path_checked != False and path_checked != "/":
                console_input = Tools.save_to_json_config(path_checked,"app_settings","default_path")
                Tools.add_colored_line(console,console_input,"green",None,True)
                if which_settings != "":
                    if which_settings == "convert_option":
                        Tools.add_new_path_to_history(path_checked,"path_history_list_conv")
                    else:
                        Tools.add_new_path_to_history(path_checked,which_settings)

            elif path_checked != "/":
                Tools.add_colored_line(console,f"Zadaná cesta: {path_given} nebyla nalezena, nebude tedy uložena","red",None,True)
            elif path_checked == "/":
                Tools.add_colored_line(console,"Nebyla vložena žádná cesta k souborům","red",None,True)

        @classmethod
        def clear_console(cls,text_widget,from_where=None):
            """
            Vymaže celou consoli
            """
            if from_where == None:
                from_where = 1.0
            text_widget.configure(state=tk.NORMAL)
            text_widget.delete(from_where, tk.END)
            text_widget.configure(state=tk.DISABLED)

        @classmethod
        def check_task_existence_in_TS(cls,taskname):
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
            if "ERROR" in error_data or "CHYBA" in error_data:
                return False
            else:
                return True
        
        @classmethod
        def is_thread_running(cls,name):
            print(threading.enumerate())
            for thread in threading.enumerate():
                if thread.name == name:
                    return True
            return False

        @classmethod
        def tray_startup_cmd(cls):
            """
            Sepnutí aplikace v system tray nabídce

            """
            if Tools.is_thread_running(cls.Tray_thread_name): # Pokud tray aplikace už běží nezapínej novou
                print("tray app is already running")
                return

            print("tray app is not running yet")
            def call_tray_class():
                tray_app_instance = trimazkon_tray.tray_app_service(initial_path,app_icon,exe_name,config_filename)
                tray_app_instance.main()

            blocking_task = threading.Thread(target=call_tray_class,name=cls.Tray_thread_name)
            blocking_task.start()
            print(threading.enumerate())

        @classmethod
        def establish_startup_tray(cls):
            """
            Sets the startup task of switching on the tray application icon
            - if it doesnt exist already
            """
            
            task_presence = Tools.check_task_existence_in_TS(cls.task_name)
            print("task presence: ",task_presence)

            if not task_presence:
                path_app_location = str(initial_path + exe_name)
                task_command = "\"" + path_app_location + " run_tray" + "\" /sc onlogon"
                process = subprocess.Popen(f"schtasks /Create /TN {cls.task_name} /TR {task_command}",
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            creationflags=subprocess.CREATE_NO_WINDOW)
                
                stdout, stderr = process.communicate()
                output_message = "out"+str(stdout) +"err"+str(stderr)
                print(output_message)
                if "Access is denied" in output_message or "stup byl odep" in output_message:
                    return "need_access"
                
            Tools.tray_startup_cmd() # init sepnutí po prvním zavedení tasku
        
        @classmethod
        def remove_task_from_TS(cls,name_of_task):
            cmd_command = f"schtasks /Delete /TN {name_of_task} /F"
            # subprocess.call(cmd_command,shell=True,text=True)

            process = subprocess.Popen(cmd_command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    creationflags=subprocess.CREATE_NO_WINDOW)
                
            stdout, stderr = process.communicate()
            output_message = "out"+str(stdout) +"err"+str(stderr)
            print(output_message)
            if "Access is denied" in output_message:
                return "need_access"

        @classmethod
        def is_admin(cls):
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False

        @classmethod
        def get_init_path(cls):
            initial_path = Tools.path_check(Tools.resource_path(os.getcwd()))
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
        def check_trial_existance(cls):
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, cls.registry_key_path, 0, winreg.KEY_READ)
                return True
            except FileNotFoundError:
                return False
            except Exception:
                return False

        @classmethod
        def check_licence(cls):
            global global_licence_load_error

            check_trial = Tools.check_trial_period()
            if "Trial active" in str(check_trial):
                global_licence_load_error = False
                return check_trial

            with open(Tools.resource_path("public.pem"), "rb") as f:
                public_key = serialization.load_pem_public_key(f.read())

            if os.path.exists(initial_path + "/license.lic"):
                with open(initial_path + "/license.lic", "r") as f:
                    lines = f.readlines()
            else:
                global_licence_load_error = True
                return "verification error"
            licence_data = lines[0].strip()  # První řádek je expirace
            signature = bytes.fromhex(lines[1].strip())  # Druhý řádek je podpis
            try:
                public_key.verify(
                    signature,
                    licence_data.encode(),
                    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                    hashes.SHA256()
                )
                
                exp_date = datetime.datetime.strptime(licence_data.split(":")[1], "%d.%m.%Y")
                hwid_lic = licence_data.split("|")[0]
                if hwid_lic != Tools.get_volume_serial():
                    print("now valid hwid")
                    global_licence_load_error = True
                    return "verification error"

                if exp_date >= datetime.datetime.today():
                    print(f"License valid until: {exp_date.date()}")
                    global_licence_load_error = False
                    return exp_date.date()
                else:
                    global_licence_load_error = True
                    return f"EXPIRED: {exp_date.date()}"

            except Exception as e:
                print("License verification error!", e)
                global_licence_load_error = True
                return "verification error"

        @classmethod
        def get_volume_serial(cls):
            # Get system drive letter (e.g., "C:")
            drive_letter = subprocess.check_output(
                'wmic os get systemdrive', shell=True
            ).decode().split("\n")[1].strip().replace(":", "")
            
            c = wmi.WMI()
            
            # Find the physical disk corresponding to the system drive
            for disk in c.Win32_DiskDrive():
                for partition in disk.associators("Win32_DiskDriveToDiskPartition"):
                    for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                        if logical_disk.DeviceID == f"{drive_letter}:":  # Match the system drive
                            serial_number = disk.SerialNumber.strip()  # Get serial number
                            return serial_number.rstrip(".")

            return None  # Return None if not found

        @classmethod
        def set_zoom(cls,zoom_factor,root):
            try:
                root.after(0, lambda: customtkinter.set_widget_scaling(zoom_factor / 100))
                # customtkinter.set_widget_scaling(zoom_factor / 100)
            except Exception as e:
                print(f"error with zoom scaling: {e}")
            
            root.tk.call('tk', 'scaling', zoom_factor / 100)
    
        @classmethod
        def terminate_pid(cls,pid:int):
            print("pid to terminate: ",pid)

            try:
                process = psutil.Process(pid)
                process.terminate()
                process.wait(timeout=5)
                print(f"Process with PID {pid} terminated.")
            except psutil.NoSuchProcess:
                print(f"No process with PID {pid} found.")
            except psutil.AccessDenied:
                print(f"Permission denied to terminate PID {pid}.")
            except psutil.TimeoutExpired:
                print(f"Process with PID {pid} did not terminate in time.")
        
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
        def store_installation_date(cls,refresh_callback):
            try:
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, cls.registry_key_path)
                install_date = datetime.datetime.now().strftime("%Y-%m-%d")
                winreg.SetValueEx(key, "InstallDate", 0, winreg.REG_SZ, install_date)
                winreg.CloseKey(key)
                print("Installation date stored.")
                refresh_callback()
            except Exception as e:
                print("Error storing installation date:", e)

        @classmethod
        def check_trial_period(cls):
            try:
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, cls.registry_key_path)
                install_date_str, _ = winreg.QueryValueEx(key, "InstallDate")
                install_date = datetime.datetime.strptime(install_date_str, "%Y-%m-%d")
                trial_period = datetime.timedelta(days=30)
                expiration_date = install_date + trial_period
                current_date = datetime.datetime.now()
                winreg.CloseKey(key)

                if current_date > expiration_date:
                    print("Trial expired. Please purchase the full version.")
                    return False
                else:
                    remaining_days = (expiration_date - current_date).days
                    print(f"Trial active. {remaining_days} days remaining.")
                    return f"Trial active. {remaining_days} days remaining."

            except FileNotFoundError:
                print("Installation date not found. Trial might have been tampered with.")
                return False
            except Exception as e:
                print("Error checking trial period:", e)
                return False

        @classmethod
        def open_manual_ip_setting_window(cls):
            def output_callback(output_message):
                WindowsBalloonTip("Proveden pokus o změnu IP adresy",
                    str(output_message),
                    app_icon)
            ip_set_instance = IP_setting.main(None,None,None,initial_path,None,config_filename,True)
            ip_set_instance.IP_tools.manual_ip_setting(app_icon_path=app_icon,output_callback=output_callback)

        @classmethod
        def check_for_new_app_version(cls,language_given = "cz",force_update=False):
            new_version_log_name = "new_version_log.txt"
            version_list = []
            current_app_version = trimazkon_version.replace(".","")
            current_app_version = int(current_app_version)
            print("current version: ",current_app_version)
            sharepoint_instance = download_database.database("",search_for_version=True)
            installer_name_list = sharepoint_instance.output
            if len(installer_name_list) > 0:
                for names in installer_name_list:
                    if names == new_version_log_name:
                        continue
                    name_splitted = names.split("-")
                    if name_splitted[0] == "TRIMAZKON":
                        version_list.append(name_splitted[1])
                    elif testing and name_splitted[0] == "dummy_version":
                        version_list.append(name_splitted[1])

            version_list_int = []
            for versions in version_list:
                versions = versions.replace(".","")
                version_list_int.append(int(versions))

            print("version list: ",version_list_int)
            if len(version_list_int) == 0:
                return "up to date"
            max_sharepoint_version = max(version_list_int)
            if current_app_version < max_sharepoint_version:
                print("new_version_available")
                if language_given == "en":
                    root.title(f"{app_name} v_{app_version} (version is not up to date)")
                else:
                    root.title(f"{app_name} v_{app_version} (neaktuální verze)")
                sharepoint_instance = download_database.database(new_version_log_name,get_new_version_log=True)
                new_version_log = sharepoint_instance.output
                max_sharepoint_version = str(max_sharepoint_version)
                max_sharepoint_version_str = max_sharepoint_version[0]+"."+max_sharepoint_version[1]+"."+max_sharepoint_version[2]
                config_data = Tools.read_json_config()
                if not force_update:
                    if "ignored_version" in config_data["app_settings"]:
                        ignored_version = config_data["app_settings"]["ignored_version"]
                        print(ignored_version, max_sharepoint_version_str)
                        if max_sharepoint_version_str == ignored_version:
                            return
                Subwindows.download_new_version_window(max_sharepoint_version_str,new_version_log,force_update=force_update)
            else:
                return "up to date"

class system_pipeline_communication: # vytvoření pipeline serveru s pipe názvem TRIMAZKON_pipe_ + pid (id systémového procesu)
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

                    if "Establish main menu gui" in received_data:
                        root_existance = self.check_root_existence(root)
                        print("root_status: ",root_existance)
                        # global root

                        if root_existance == True:
                            try:
                                root.deiconify()
                                if Tools.read_json_config()["app_settings"]["maximalized"] == "ano":
                                    root.after(0, lambda:root.state('zoomed'))
                                root.update_idletasks()
                            except Exception as e:
                                print(e)
                            # global menu
                            menu = main_menu(root)
                            root.after(100,lambda: menu.menu(clear_root=True))
                            # menu.menu(clear_root=True)
                        else:
                            start_new_root() # spousteni pres admina, bylo potreba shodit cely processID
                            # self.root.after(0,menu.menu(clear_root=True))

                    elif "Open manual ip setting window" in received_data:
                        manual_ip_thread = threading.Thread(target= Tools.open_manual_ip_setting_window,)
                        manual_ip_thread.start()

                    elif "Open list with del tasks" in received_data:
                        trimazkon_tray_instance = trimazkon_tray.tray_app_service(initial_path,app_icon,exe_name,config_filename)
                        # trimazkon_tray_instance.show_all_tasks(toplevel=True)
                        tasks_thread = threading.Thread(target= trimazkon_tray_instance.show_all_tasks,args=[True,False,False])
                        tasks_thread.start()

                    elif "Open list with del logs" in received_data:
                        trimazkon_tray_instance = trimazkon_tray.tray_app_service(initial_path,app_icon,exe_name,config_filename)
                        # trimazkon_tray_instance.show_task_log(toplevel = True)
                        logs_thread = threading.Thread(target= trimazkon_tray_instance.show_task_log,args=[False,None,False,False,True])
                        logs_thread.start()

                    elif "Open image browser starting with image" in received_data:
                        received_params = received_data.split("|||")
                        # global root
                        root_existance = self.check_root_existence(root)
                        print("root_status: ",root_existance)

                        if root_existance == True:
                            try:
                                # if root.state() == "iconic":
                                root.deiconify()
                                root.update_idletasks()
                            except Exception as e:
                                print(e)
                            # global menu
                            menu = main_menu(root)
                            # root.after(100,lambda: menu.menu(clear_root=True))
                            root.after(200,menu.command_landed,received_params)
                            # menu.menu(clear_root=True)
                        else:
                            start_new_root() # spousteni pres admina, bylo potreba shodit cely processID

                    elif "Shutdown application" in received_data:
                        root.destroy()

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

        if "Establish main menu gui" in str(command):
            message = "Establish main menu gui"
            print("Message sent.",message)
            win32file.WriteFile(handle, message.encode())
        
        elif "Execute file deleting" in str(command):
            message = str(command) + "|||"
            for params in parameters:
                message = message + str(params) + "|||"
            print("Message sent: ",message)
            win32file.WriteFile(handle, message.encode())

        elif "Open manual ip setting window" in str(command):
            message = "Open manual ip setting window"
            print("Message sent.",message)
            win32file.WriteFile(handle, message.encode())

        elif "Open list with del tasks" in str(command):
            message = "Open list with del tasks"
            print("Message sent.",message)
            win32file.WriteFile(handle, message.encode())

        elif "Open list with del logs" in str(command):
            message = "Open list with del logs"
            print("Message sent.",message)
            win32file.WriteFile(handle, message.encode())

        elif "Open image browser starting with image:" in str(command):
            message = str(command) + "|||"
            for params in parameters:
                message = message + str(params) + "|||"
            print("Message sent.",message)
            win32file.WriteFile(handle, message.encode())

        elif "Shutdown application" in str(command):
            message = "Shutdown application"
            print("Message sent.",message)
            win32file.WriteFile(handle, message.encode())

        elif "Edit existing task" in str(command):
            message = str(command) + "|||"
            for params in parameters:
                message = message + str(params) + "|||"
            print("Message sent: ",message)
            win32file.WriteFile(handle, message.encode())

    def start_server(self):
        self.pipe_name = f"TRIMAZKON_pipe_{self.current_pid}"
        running_server = threading.Thread(target=self.server, args=(self.pipe_name,),daemon=True)
        # running_server = threading.Thread(target=self.server, args=(pipe_name,))
        running_server.start()
        time.sleep(0.5)  # Wait for the server to start

    def call_checking(self,command,parameters):
        """
        for every found process with name of an application: send given command
        """
        checking = initial_tools.get_all_app_processes()
        print("SYSTEM application processes: ",checking)
        # if it is running more then one application, execute (root + self.root)
        # if checking[0]>1:
        pid_list = checking[1]
        # try to send command to every process which has application name
        for pids in pid_list:
            if pids != self.current_pid:
                try:
                    pipe_name = f"TRIMAZKON_pipe_{pids}"
                    print("calling client",pipe_name,command,parameters)
                    self.client(pipe_name,command,parameters)
                except Exception:
                    pass
        return True

initial_path = Tools.get_init_path()
print("init path: ",initial_path)
app_icon = Tools.resource_path('images/logo_TRIMAZKON.ico')
app_licence_validity = Tools.check_licence()
load_gui=True

print("SYSTEM: ",sys.argv)
if len(sys.argv) > 1:
    if global_licence_load_error: # jen když je spouštěno přes cmd, neuzavirej smycku...
        load_gui = False
        loop_request = False

    elif sys.argv[1] == "run_tray":
        pipeline_duplex = system_pipeline_communication(exe_name)# potřeba spustit server, protože neběží nic (nikdy nedojde k tomu aby byla spuštěna aplikace)
        Tools.tray_startup_cmd()
        load_gui = False
        if root == None:
            customtkinter.set_appearance_mode("dark")
            customtkinter.set_default_color_theme("dark-blue")
            root=customtkinter.CTk(fg_color="#212121")
            root.geometry("1200x900")
            root.title(f"{app_name} v_{app_version}")
            root.wm_iconbitmap(app_icon)
            root.update_idletasks()
            root.withdraw()
        loop_request = True

    elif sys.argv[1] == "trigger_by_tray":
        load_gui = False
        loop_request = False
        pipeline_duplex_instance = system_pipeline_communication(exe_name,no_server=True) # pokud už je aplikace spuštěná nezapínej server, trvá to...
        pipeline_duplex_instance.call_checking(f"Establish main menu gui",[])
    
    elif sys.argv[1] == "manual_ip_setting":
        load_gui = False
        loop_request = False
        pipeline_duplex_instance = system_pipeline_communication(exe_name,no_server=True) # pokud už je aplikace spuštěná nezapínej server, trvá to...
        pipeline_duplex_instance.call_checking(f"Open manual ip setting window",[])
    
    elif sys.argv[1] == "open_task_list":
        load_gui = False
        loop_request = False
        pipeline_duplex_instance = system_pipeline_communication(exe_name,no_server=True) # pokud už je aplikace spuštěná nezapínej server, trvá to...
        pipeline_duplex_instance.call_checking(f"Open list with del tasks",[])

    elif sys.argv[1] == "open_log_list":
        load_gui = False
        loop_request = False
        pipeline_duplex_instance = system_pipeline_communication(exe_name,no_server=True) # pokud už je aplikace spuštěná nezapínej server, trvá to...
        pipeline_duplex_instance.call_checking(f"Open list with del logs",[])

    elif sys.argv[1] == "app_shutdown":
        load_gui = False
        loop_request = False
        pipeline_duplex_instance = system_pipeline_communication(exe_name,no_server=True)
        pipeline_duplex_instance.call_checking(f"Shutdown application",[])

    elif sys.argv[1] == "edit_existing_task":
        load_gui = False
        loop_request = False
        pipeline_duplex_instance = system_pipeline_communication(exe_name,no_server=True)
        pipeline_duplex_instance.call_checking(f"Edit existing task",sys.argv)

    elif sys.argv[1] == "settings_tray" or sys.argv[1] == "settings_tray_del" or sys.argv[1] == "admin_menu"  or sys.argv[1] == "admin_ip_setting":
        pid = int(sys.argv[2])
        Tools.terminate_pid(pid) #vypnout thread s tray aplikací

#Musi byt az tady, protoze muzu terminatenout aplikaci (vyse v kodu)
app_running_status = initial_tools.check_runing_app_duplicity()
print("already opened app status: ",app_running_status)

if load_gui:
    if len(sys.argv) > 1: # VÝJIMKA: pukud nové spuštění s admin právy načti i gui...
        if sys.argv[0] == sys.argv[1]:
            app_running_status = False

    if not app_running_status:
        pipeline_duplex = system_pipeline_communication(exe_name)# Establishment of pipeline server for duplex communication between running applications
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        root=customtkinter.CTk()
        root.geometry("1200x900")
        root.title(f"{app_name} v_{app_version}")
        root.wm_iconbitmap(Tools.resource_path(app_icon))
        loop_request=True

    else:# předání parametrů v případě spuštění obrázkem (základní obrázkový prohlížeč)
        pipeline_duplex_instance = system_pipeline_communication(exe_name,no_server=True) 
        pipeline_duplex_instance.call_checking(f"Establish main menu gui",[])# předání parametrů pipeline komunikací PUKUD NEJSOU NA VSTUPU ZADNE SYSTEMOVE PARAMETRY, SPOUSTENO PRES ZÁSTUPCE

class main_menu:
    def __init__(self,root):
        self.root = root
        pipeline_duplex.root = self.root # předání rootu do pipeline_duplex až ve chvílí, kdy je jasné, že aplikace není vícekrát spuštěná:
        # config_filename = "config_TRIMAZKON.xlsx"
        # setting_list_name = "Settings_recources"
        # Tools.check_config_file(config_filename,setting_list_name)
        self.config_data = Tools.read_json_config()
        self.database_downloaded = False
        self.ib_running = False
        self.run_as_admin = False
        self.TS_tray_taskname = "jhv_IP_startup_tray_setup"
        #init spínání tray podle nastavení
        if self.config_data["app_settings"]["tray_icon_startup"] == "ano":
            task_success = Tools.establish_startup_tray()
            if str(task_success) == "need_access":
                self.run_as_admin = True
        else: # když nezaškrtnuto aut. spouštění ujisti se, že není nastavené - potřeba taky admin
            if Tools.check_task_existence_in_TS(self.TS_tray_taskname):
                Tools.remove_task_from_TS(self.TS_tray_taskname)
        
    def clear_frames(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
    def call_ip_manager(self):
        self.clear_frames()
        self.root.unbind("<f>")
        IP_manager(self.root)
    
    def call_advanced_option(self,success_message = None):
        self.clear_frames()
        self.root.unbind("<f>")
        Advanced_option(self.root,tray_setting_status_message=success_message)

    def fill_changelog(self,change_log):
        # Iterate through each <string> element and print its text
        for string_element in ip_set_changelog.change_log_list:
            change_log.insert("current lineend",string_element + "\n")
        change_log.see(tk.END)

    def on_closing(self):
        global root
        if Tools.is_admin(): # pokud se vypíná admin app - vypnout i admin tray a zapnout bez práv
            data_read_in_config = Tools.read_json_config()
            if data_read_in_config["app_settings"]["tray_icon_startup"] == "ano":
                task_name = self.TS_tray_taskname #musím přes task scheduler, když to spustím tady bude pořát s adminem... -> duplicita
                try:
                    run_task_command = f'schtasks /Run /TN "{task_name}"'
                    print("Running task with command:", run_task_command)
                    subprocess.run(run_task_command, shell=True)
                except:
                    pass
            Tools.terminate_pid(os.getpid()) #vypnout thread s tray aplikací
        else:
            # self.root.destroy()
            root.withdraw()

    def check_licence(self):
        global app_licence_validity
        app_licence_validity = Tools.check_licence()
        menu.menu(clear_root=True)

    def menu(self,initial=False,catalogue_downloaded = False,zoom_disable = False,clear_root = False): # Funkce spouští základní menu při spuštění aplikace (MAIN)
        """
        Funkce spouští základní menu při spuštění aplikace (MAIN)

        list_of_menu_frames = [frame_with_buttons,frame_with_logo,frame_with_buttons_right]
        """
        print("licence error:",global_licence_load_error)

        if clear_root:
            self.clear_frames()

        self.ib_running = False
        if self.config_data["app_settings"]["maximalized"]  == "ano":
            self.root.after(0, lambda:self.root.state('zoomed')) # max zoom, porad v okne
            
        if self.config_data["app_settings"]["app_zoom_checkbox"]  == "ne" and initial: # pokud není využito nastavení windows
            try:
                root.after(0, lambda: Tools.set_zoom(int(self.config_data["app_settings"]["app_zoom"]),root))
            except Exception as e:
                print("error with menu scaling")

        frame_with_logo = customtkinter.CTkFrame(master=self.root,corner_radius=0)
        # logo = customtkinter.CTkImage(Image.open(initial_path+"images/logo.png"),size=(1200, 100))
        logo = customtkinter.CTkImage(Image.open(Tools.resource_path("images/jhv_logo.png")),size=(300, 100))
        image_logo = customtkinter.CTkLabel(master = frame_with_logo,text = "",image =logo)
        menu_upper_frame = customtkinter.CTkFrame(master=self.root,corner_radius=0,fg_color="#212121")
        frame_with_buttons_right = customtkinter.CTkFrame(master=menu_upper_frame,corner_radius=0)
        frame_with_buttons = customtkinter.CTkFrame(master=menu_upper_frame,corner_radius=0)
        frame_with_logo.pack(pady=0,padx=0,fill="both",expand=False,side = "top")
        image_logo.pack()
        IB_as_def_browser_path = None
        # self.list_of_menu_frames = [frame_with_buttons,frame_with_logo,frame_with_buttons_right]
        
        ip_setting_button =     customtkinter.CTkButton(master= frame_with_buttons, width= 400,height=100, text = "IP setting", command = lambda: self.call_ip_manager(),font=("Arial",25,"bold"))
        advanced_button =       customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Nastavení", command = lambda: self.call_advanced_option(),font=("Arial",25,"bold"))
        change_log_label =      customtkinter.CTkLabel(master=frame_with_buttons_right, width= 600,height=50,font=("Arial",24,"bold"),text="Seznam posledně provedených změn: ")
        change_log =            customtkinter.CTkTextbox(master=frame_with_buttons_right, width= 600,height=550,fg_color="#212121",font=("Arial",20),border_color="#636363",border_width=3,corner_radius=0)
        resources_load_error =  customtkinter.CTkLabel(master=frame_with_buttons_right, width= 600,height=50,font=("Arial",24,"bold"),text="Nepodařilo se načíst konfigurační soubor (config_TRIMAZKON.xlsx)",text_color="red")
        ip_setting_button.      pack(pady = (105,0), padx=20,side="top",anchor="e")
        advanced_button.        pack(pady = (10,0), padx=20,side="top",anchor="e")
        change_log_label.       pack(pady = (50,5), padx=20,side="top",anchor="w")
        change_log.             pack(pady =0,       padx=20,side="top",anchor="w")
        if global_recources_load_error:
            resources_load_error.pack(pady = (5,5), padx=20,side="top",anchor="w")
        frame_with_buttons.pack(pady=0,padx=0,fill="both",expand=True,side = "left")
        frame_with_buttons_right.pack(pady=0,padx=0,fill="both",expand=True,side = "right")
        menu_upper_frame.pack(pady=0,padx=0,fill="both",expand=True,side = "top")

        bottom_ribbon = customtkinter.CTkFrame(master=self.root,corner_radius=0,fg_color="#212121")
        licence_info_frame = customtkinter.CTkFrame(master=bottom_ribbon,corner_radius=0,fg_color="#212121")
        licence_info_label = customtkinter.CTkLabel(master=licence_info_frame,font=("Arial",24,"bold"),text="Licence:")
        licence_info_status = customtkinter.CTkLabel(master=licence_info_frame,font=("Arial",24),text="")
        licence_info_label.pack(pady =5,padx=(5,0),side="left",anchor="w")
        licence_info_status.pack(pady =(7,5),padx=(5,0),side="left",anchor="w")
        licence_info_frame.pack(pady =30,padx=20,side="left",anchor="s")
        bottom_ribbon.pack(pady=0,padx=0,fill="both",side = "bottom",expand=True)

        self.fill_changelog(change_log)
        
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
            self.root.update()
        self.root.bind("<f>",maximalize_window)

        if global_licence_load_error:
            ip_setting_button.configure(state="disabled")
            advanced_button.configure(state="disabled")
            if app_licence_validity == "verification error":
                licence_info_status.configure(text="chyba ověření")
            elif "EXPIRED:" in str(app_licence_validity):
                licence_info_status.configure(text=app_licence_validity.replace("EXPIRED:","platnost vypršela:"))
            insert_licence_btn = customtkinter.CTkButton(master = licence_info_frame, width = 200,height=40, text = "Vložit licenci", command = lambda: os.startfile(initial_path),font=("Arial",24,"bold"))
            trial_btn = customtkinter.CTkButton(master = licence_info_frame,height=40, text = "Aktivovat trial verzi (30 dní)", command = lambda: Tools.store_installation_date(refresh_callback = self.check_licence),font=("Arial",24,"bold"))
            refresh_licence_btn = customtkinter.CTkButton(master = licence_info_frame, width = 40,height=40, text = "🔄", command = lambda: self.check_licence(),font=(None,24))
            insert_licence_btn.pack(pady =(7,5),padx=(15,0),side="left",anchor="w")
            if not Tools.check_trial_existance():
                trial_btn.pack(pady =(7,5),padx=(5,0),side="left",anchor="w")
            refresh_licence_btn.pack(pady =(7,5),padx=(5,0),side="left",anchor="w")
            self.root.after(500, lambda: Subwindows.licence_window(self.check_licence))
        else:
            if "Trial active" in str(app_licence_validity):
                validity_string = str(app_licence_validity)
                validity_string = validity_string.replace("Trial active.","Trial verze platná:")
                validity_string = validity_string.replace("days remaining.","dní")
                licence_info_status.configure(text=f"{validity_string}")
            else:
                licence_info_status.configure(text=f"platná do {app_licence_validity}")
            if initial:
                def check_version_routine():
                    check_version = threading.Thread(target=Tools.check_for_new_app_version,)
                    check_version.start()
                self.root.after(500,check_version_routine)

        # initial promenna aby se to nespoustelo porad do kola pri navratu do menu (system argumenty jsou stále uložené v aplikaci)
        if len(sys.argv) > 1 and initial == True:
            raw_path = str(sys.argv[1])
            #klik na spusteni trimazkonu s admin právy
            if sys.argv[1] == "admin_ip_setting":
                self.call_ip_manager()
            elif sys.argv[1] == "settings_tray":
                self.call_advanced_option(success_message="Automatické spouštění úspěšně nastaveno")
            elif sys.argv[1] == "settings_tray_del":
                self.call_advanced_option(success_message="Automatické spouštění úspěšně odstraněno")
        
        if self.run_as_admin and not global_licence_load_error:
            self.root.after(1000, lambda: Subwindows.call_again_as_admin("admin_menu","Upozornění","Aplikace vyžaduje práva pro nastavení aut. spouštění na pozadí\n     - možné změnit v nastavení\n\nPřejete si znovu spustit aplikaci, jako administrátor?"))
        
        if initial and not global_licence_load_error:
            self.call_ip_manager()
        try:
            root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())
            # self.root.mainloop()
        except Exception as e:
            print("already looped? ",e)
        # self.root.mainloop()

class Advanced_option: # Umožňuje nastavit základní parametry, které ukládá do textového souboru
    """
    Umožňuje nastavit základní parametry, které ukládá do textového souboru
    """
    def __init__(self,root,windowed=None,spec_location=None,path_to_remember = None,last_params = None,tray_setting_status_message = None):
        self.spec_location = spec_location
        self.path_to_remember = path_to_remember
        self.ib_last_params = last_params
        self.windowed = windowed
        self.root = root
        self.tray_setting_status_message = tray_setting_status_message
        self.unbind_list = []
        self.drop_down_prefix_dir_names_list = []
        self.drop_down_static_dir_names_list = []
        self.default_displayed_prefix_dir = "cam"
        self.default_displayed_static_dir = 0
        self.submenu_option = "default_path"
        self.config_data = Tools.read_json_config()
        self.selected_language = self.config_data["app_settings"]["default_language"]
        default_dir_names = ip_set_changelog.default_setting_database_param
        self.default_dir_names = [" (default: "+ default_dir_names[9][0] + ")",
                                " (default: "+ default_dir_names[9][1] + ")",
                                " (default: "+ default_dir_names[9][2] + ")",
                                " (default: "+ default_dir_names[9][3] + ")",
                                " (default: "+ default_dir_names[9][4] + ")",
                                " (default: "+ default_dir_names[9][5] + ")",
                                " (default: "+ default_dir_names[9][6] + ")"
                                ]
        self.creating_advanced_option_widgets()

    def call_menu(self): # Tlačítko menu (konec, návrat do menu)
        """
        Funkce čistí všechny zaplněné rámečky a funguje, jako tlačítko zpět do menu
        """
        self.list_of_frames = [self.top_frame,
                            self.bottom_frame_default_path,
                            self.menu_buttons_frame]
        for frames in self.list_of_frames:
            frames.pack_forget()
            frames.grid_forget()
            frames.destroy()
        
        for binds in self.unbind_list:
            self.root.unbind(binds)
        menu.menu(zoom_disable = True)

    def clear_frame(self,frame): # Smaže widgets na daném framu
        """
        Smaže widgets na daném framu
        """
        try:
            children = frame.winfo_children()
        except Exception:
            return
        for widget in children:
            widget.destroy()

    def maximalized(self): # Nastavení základního spouštění (v okně/ maximalizované)
        option = self.checkbox_maximalized.get()
        if option == 1:
            Tools.save_to_json_config("ano","app_settings","maximalized")
            self.root.after(0, lambda:self.root.state('zoomed'))
        else:
            Tools.save_to_json_config("ne","app_settings","maximalized")
            self.root.after(0, lambda:self.root.state('normal'))
            self.root.after(10, lambda:self.root.geometry("1200x900"))
    
    def tray_startup_setup(self,main_console): # Nastavení základního spouštění (v okně/ maximalizované)
        option = self.tray_checkbox.get()
        if option == 1:
            Tools.save_to_json_config("ano","app_settings","tray_icon_startup")
            new_task_success = Tools.establish_startup_tray()
            if str(new_task_success) == "need_access":
                menu.run_as_admin = True
                Subwindows.call_again_as_admin("settings_tray","Upozornění","Aplikace vyžaduje práva pro nastavení aut. spouštění na pozadí\n\n- přejete si znovu spustit aplikaci, jako administrátor?")
                main_console.configure(text = "Jsou vyžadována admin práva",text_color="red")
            else:
                # Tools.establish_startup_tray()
                menu.run_as_admin = False
                main_console.configure(text = "Automatické spouštění úspěšně nastaveno",text_color="green")

        else:
            Tools.save_to_json_config("ne","app_settings","tray_icon_startup")
            remove_task_success = Tools.remove_task_from_TS("jhv_IP_startup_tray_setup")
            if str(remove_task_success) == "need_access":
                menu.run_as_admin = True
                Subwindows.call_again_as_admin("settings_tray_del","Upozornění","Aplikace vyžaduje práva pro odstranění aut. spouštění na pozadí\n\n- přejete si znovu spustit aplikaci, jako administrátor?")
                main_console.configure(text = "Jsou vyžadována admin práva",text_color="red")
            else:
                menu.run_as_admin = False
                main_console.configure(text = "Automatické spouštění úspěšně odstraněno",text_color="green")

    def set_safe_mode(self): # Nastavení základního spouštění (v okně/ maximalizované)
        option = self.checkbox_safe_mode.get()
        if option == 1:
            Tools.save_to_json_config("ano","sort_conv_settings","sorting_safe_mode")
        else:
            Tools.save_to_json_config("ne","sort_conv_settings","sorting_safe_mode")

    def refresh_main_window(self):
        self.clear_frame(self.root)
        self.clear_frame(self.current_root)
        self.current_root.destroy()

    def setting_widgets(self,exception=False,main_console_text = "",main_console_text_color = "white",submenu_option = None): # samotné možnosti úprav parametrů uložených v config souboru
        """
        Nabídka možností úprav

        0 = default_path
        1 = set_folder_names
        2 = set_default_parametres
        3 = set_supported_formats
        4 = set_image_browser_setting

        """

        if self.tray_setting_status_message != None:
            main_console_text = self.tray_setting_status_message
            main_console_text_color = "green"

        self.clear_frame(self.bottom_frame_default_path)
        config_data = Tools.read_json_config()
        if exception == False:
            cutoff_date = config_data["del_settings"]["default_cutoff_date"]
        else:
            cutoff_date = exception
        
        files_to_keep = config_data["del_settings"]["default_files_to_keep"]
        default_prefix_func=config_data["sort_conv_settings"]["prefix_function"]
        default_prefix_cam =config_data["sort_conv_settings"]["prefix_camera"]
        self.drop_down_prefix_dir_names_list = [(str(default_prefix_cam)+" (pro třídění podle č. kamery)"),(str(default_prefix_func)+" (pro třídění podle č. funkce)")]
        default_max_num_of_pallets=config_data["sort_conv_settings"]["max_pallets"]
        self.drop_down_static_dir_names_list = [
            config_data["sort_conv_settings"]["temp_dir_name"],
            config_data["sort_conv_settings"]["pairs_dir_name"],
            config_data["del_settings"]["to_delete_dir_name"],
            config_data["sort_conv_settings"]["convert_bmp_dir_name"],
            config_data["sort_conv_settings"]["convert_jpg_dir_name"],
            config_data["image_browser_settings"]["copyed_dir_name"],
            config_data["image_browser_settings"]["moved_dir_name"],
        ]
        # pridani defaultniho nazvu pred zmenami do drop down menu
        for i in range(0,len(self.drop_down_static_dir_names_list)):
            self.drop_down_static_dir_names_list[i] += self.default_dir_names[i]

        row_index = 0

        for buttons in self.option_buttons:
            buttons.configure(fg_color = "black")

        def call_browseDirectories(): # Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
            """
            Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
            """
            if select_by_dir.get() == 1:
                output = Tools.browseDirectories("only_dirs")
            else:
                output = Tools.browseDirectories("all")
            if str(output[1]) != "/":
                self.path_set.delete("0","200")
                self.path_set.insert("0", output[1])
                console_input = Tools.save_to_json_config(output[1],"app_settings","default_path") # hlaska o nove vlozene ceste
                default_path_insert_console.configure(text="")
                default_path_insert_console.configure(text = "Aktuálně nastavená základní cesta k souborům: " + str(output[1]),text_color="white")
                main_console.configure(text="")
                main_console.configure(text=console_input,text_color="green")
            else:
                main_console.configure(text = str(output[0]),text_color="red")

        def save_path():
            path_given = str(self.path_set.get())
            path_checked = Tools.path_check(path_given)
            if path_checked != False and path_checked != "/":
                console_input = Tools.save_to_json_config(path_checked,"app_settings","default_path")
                default_path_insert_console.configure(text="")
                default_path_insert_console.configure(text = "Aktuálně nastavená základní cesta k souborům: " + str(path_checked),text_color="white")
                main_console.configure(text="")
                main_console.configure(text=console_input,text_color="green")
            elif path_checked != "/":
                main_console.configure(text="")
                main_console.configure(text=f"Zadaná cesta: {path_given} nebyla nalezena, nebude tedy uložena",text_color="red")
            elif path_checked == "/":
                main_console.configure(text="")
                main_console.configure(text="Nebyla vložena žádná cesta k souborům",text_color="red")
        
        def select_path_by_file():
            select_by_file.select()
            select_by_dir.deselect()

        def select_path_by_dir():
            select_by_dir.select()
            select_by_file.deselect()
   
        def manage_app_zoom(*args):
            app_zoom_percent.configure(text = str(int(*args)) + " %")

        def windows_zoom_setting():
            def get_screen_dpi():
                user32 = ctypes.windll.user32
                user32.SetProcessDPIAware()  # Make sure the process is DPI aware
                hdc = user32.GetDC(0)
                dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)  # 88 is the index for LOGPIXELSX
                return dpi

            if checkbox_app_zoom.get() == 1:
                Tools.save_to_json_config("ano","app_settings","app_zoom_checkbox")
                current_dpi = get_screen_dpi()
                if current_dpi == 96:
                    Tools.set_zoom(100,root)
                elif current_dpi == 120:
                    Tools.set_zoom(125,root)
                elif current_dpi == 144:
                    Tools.set_zoom(150,root)
                app_zoom_slider.configure(state = "disabled",button_color = "gray50",button_hover_color = "gray50")
            else:
                app_zoom_slider.configure(state = "normal",button_color = "#3a7ebf",button_hover_color = "#3a7ebf")
                Tools.save_to_json_config("ne","app_settings","app_zoom_checkbox")
                Tools.set_zoom(int(app_zoom_slider.get()),root)

        def call_delete_path_history():
            confirm_window_label1 = f"Opravdu si přejete odstranit historii vložených cest pro: {drop_down_options.get()}?"
            confirm_window_label2 = "Upozornění"
            if self.selected_language == "en":
                confirm_window_label1 = "Are you sure you want to delete the history of embedded paths?"
                confirm_window_label2 = "Notice"
            confirm = Subwindows.confirm_window(confirm_window_label1,confirm_window_label2,self.selected_language)
            if confirm == True:
                which_settings = mapping_logic[drop_down_options.get()]
                if drop_down_options.get() == path_history_options[1]:
                    Tools.add_new_path_to_history("delete_history_conv",which_settings)
                else:
                    Tools.add_new_path_to_history("delete_history",which_settings)

                main_console.configure(text=f"Historie vložených cest pro: {drop_down_options.get()} byla vymazána",text_color="orange")
                if self.selected_language == "en":
                    main_console.configure(text="The history of inserted paths has been deleted",text_color="orange")

        def call_path_context_menu(event):
            chosen_option = mapping_logic[drop_down_options.get()]
            if drop_down_options.get() == path_history_options[1]:
                path_history = Tools.read_json_config()[chosen_option]["path_history_list_conv"]
            else:
                path_history = Tools.read_json_config()[chosen_option]["path_history_list"]

            def insert_path(path):
                self.path_set.delete("0","200")
                self.path_set.insert("0", path)
            if len(path_history) > 0:
                path_context_menu = tk.Menu(self.root, tearoff=0,fg="white",bg="black")
                for i in range(0,len(path_history)):
                    path_context_menu.add_command(label=path_history[i], command=lambda row_path = path_history[i]: insert_path(row_path),font=("Arial",22,"bold"))
                    if i < len(path_history)-1:
                        path_context_menu.add_separator()
                        
                path_context_menu.tk_popup(context_menu_button2.winfo_rootx(),context_menu_button2.winfo_rooty()+40)
            else:
                main_console.configure(text=f"V historii cest: {drop_down_options.get()} nebylo nic nalezeno",text_color="orange")

        def toggle_tooltip_status():
            if tooltip_checkbox.get() == 1:
                Tools.save_to_json_config("ne","app_settings","tooltip_status")
                main_console.configure(text="Tooltip byl úspěšně zakázán",text_color="green")
            else:
                Tools.save_to_json_config("ano","app_settings","tooltip_status")
                main_console.configure(text="Tooltip byl úspěšně povolen",text_color="green")

        def check_for_updates():
            result = Tools.check_for_new_app_version(force_update=True)
            if str(result) == "up to date":
                main_console.configure(text="Verze aplikace je aktuální",text_color="green")
                if self.selected_language == "en":
                    main_console.configure(text="Application version is up to date",text_color="green")
                new_version_btn.configure(state = "disabled")

        if submenu_option == "default_path":
            path_history_options = ["Třídění souborů","Konvertování souborů","Mazání souborů","Vytváření katalogu","Prohlížeč obrázků"]
            mapping_logic = {
                path_history_options[0]: "sort_conv_settings",
                path_history_options[1]: "sort_conv_settings",
                path_history_options[2]: "del_settings",
                path_history_options[3]: "catalogue_settings",
                path_history_options[4]: "image_browser_settings"
            }
            self.option_buttons[0].configure(fg_color="#212121")
            row_index = 1
            toptop_frame =              customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
            insert_licence_btn =        customtkinter.CTkButton(master = toptop_frame, width = 200,height=40, text = "Otevřít umístění aplikace/ vložit licenci", command = lambda: os.startfile(initial_path),font=("Arial",24,"bold"))
            new_version_btn =           customtkinter.CTkButton(master = toptop_frame, width = 200,height=40, text = "Vyhledat aktualizace", command = lambda: check_for_updates(),font=("Arial",24,"bold"))
            insert_licence_btn.         pack(pady=10,padx=5,side = "left",anchor = "w")
            new_version_btn.            pack(pady=10,padx=5,side = "left",anchor = "w")
            toptop_frame.               pack(pady=(20,0),padx=5,fill="x",expand=False,side = "top")

            first_option_frame =        customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
            self.checkbox_maximalized = customtkinter.CTkCheckBox(master = first_option_frame,height=40,text = "Spouštět v maximalizovaném okně",command = lambda: self.maximalized(),font=("Arial",22,"bold"))
            first_option_frame.         pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
            tray_option_frame =         customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
            self.tray_checkbox =        customtkinter.CTkCheckBox(master = tray_option_frame,height=40,text = "Spouštět TRIMAZKON na pozadí (v systémové nabídce \"tray_icons\") při zapnutí systému Windows?",command = lambda: self.tray_startup_setup(main_console),font=("Arial",22,"bold"))
            tray_option_frame.          pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
            tooltip_option_frame =      customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
            tooltip_checkbox =          customtkinter.CTkCheckBox(master = tooltip_option_frame,height=40,text = "Zakázat \"tooltip\" (okna nápovědy nad tlačítky)",command = lambda: toggle_tooltip_status(),font=("Arial",22,"bold"))
            tooltip_checkbox.           pack(pady=10,padx=10,side = "left",anchor = "w")
            tooltip_option_frame.       pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
            current_zoom = config_data["app_settings"]["app_zoom"]
            new_option_frame =          customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
            new_option_frame.           pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
            zomm_app_label =            customtkinter.CTkLabel(master = new_option_frame,height=20,text = "Nastavte celkové přiblížení aplikace:",justify = "left",font=("Arial",22,"bold"))
            checkbox_app_zoom =         customtkinter.CTkCheckBox(master = new_option_frame,height=40,text = "Použít nastavení Windows",command = lambda: windows_zoom_setting(),font=("Arial",22,"bold"))
            app_zoom_slider =           customtkinter.CTkSlider(master = new_option_frame,width=300,height=15,from_=60,to=200,number_of_steps= 14,command = lambda e: manage_app_zoom(e))
            app_zoom_percent =          customtkinter.CTkLabel(master= new_option_frame,height=20,text = str(current_zoom) + " %",justify = "left",font=("Arial",20))
            zomm_app_label.             grid(column =0,row=0,sticky = tk.W,pady =(10,10),padx=10)
            app_zoom_slider.            grid(column =0,row=1,sticky = tk.W,pady =(10,20),padx=10)
            app_zoom_percent.           grid(column =0,row=1,sticky = tk.W,pady =(10,20),padx=320)
            checkbox_app_zoom.          grid(column =0,row=1,sticky = tk.W,pady =(10,20),padx=400)

            second_option_frame =        customtkinter.CTkFrame(    master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
            label5 =                    customtkinter.CTkLabel(     master = second_option_frame,height=40,text = "Nastavte základní cestu k souborům při spuštění:",justify = "left",font=("Arial",22,"bold"))
            explorer_settings_label =   customtkinter.CTkLabel(     master = second_option_frame,height=40,text = "Nastavení EXPLORERU: ",justify = "left",font=("Arial",20,"bold"))
            select_by_dir =             customtkinter.CTkCheckBox(  master = second_option_frame,height=40,text = "Vybrat cestu zvolením složky",font=("Arial",20),command = lambda: select_path_by_dir())
            select_by_file =            customtkinter.CTkCheckBox(  master = second_option_frame,height=40,text = "Vybrat cestu zvolením souboru (jsou viditelné při vyhledávání)",font=("Arial",20),command = lambda: select_path_by_file())
            # context_menu_button  =  customtkinter.CTkButton(master = second_option_frame, width = 40,height=40, text = "V",font=("Arial",20,"bold"),corner_radius=0,fg_color="#505050")
            self.path_set =             customtkinter.CTkEntry( master = second_option_frame,width=845,height=40,font=("Arial",20),placeholder_text="")
            button_save5 =              customtkinter.CTkButton(master = second_option_frame,width=100,height=40, text = "Uložit", command = lambda: save_path(),font=("Arial",22,"bold"))
            button_explorer =           customtkinter.CTkButton(master = second_option_frame,width=40,height=40, text = "...", command = lambda: call_browseDirectories(),font=("Arial",22,"bold"))
            del_history_label =         customtkinter.CTkLabel(master = second_option_frame,height=40,text = "Výběr skupiny historie cest (vložená cesta se ukládá pod zvolenou kategorii):",justify = "left",font=("Arial",22,"bold"))
            context_menu_button2  =     customtkinter.CTkButton(master = second_option_frame, width = 100,height=40, text = "Náhled",font=("Arial",20,"bold"),corner_radius=0)
            drop_down_options =         customtkinter.CTkOptionMenu(master = second_option_frame,width=350,height=40,values=path_history_options,font=("Arial",20),corner_radius=0)
            del_path_history =          customtkinter.CTkButton(master = second_option_frame,height=40, text = "Smazat historii", command = lambda: call_delete_path_history(),font=("Arial",22,"bold"),corner_radius=0)
            default_path_insert_console=customtkinter.CTkLabel(master = second_option_frame,height=40,text ="",justify = "left",font=("Arial",22),text_color="white")
            console_frame =             customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1,fg_color="black")
            main_console =              customtkinter.CTkLabel(master = console_frame,height=20,text = str(main_console_text),text_color=str(main_console_text_color),justify = "left",font=("Arial",22))
            if self.windowed:
                save_frame =            customtkinter.CTkFrame(     master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
                save_changes_button =   customtkinter.CTkButton(master = save_frame,width=150,height=40, text = "Aplikovat/ načíst změny", command = lambda: self.refresh_main_window(),font=("Arial",22,"bold"))
            self.checkbox_maximalized.  grid(column =0,row=row_index-1,sticky = tk.W,pady =20,padx=10)
            self.tray_checkbox.         grid(column =0,row=row_index-1,sticky = tk.W,pady =20,padx=10)
            label5.                     grid(column =0,row=row_index,sticky = tk.W,pady =(5,0),padx=10)
            explorer_settings_label.    grid(column =0,row=row_index+1,sticky = tk.W,pady =10,padx=10)
            select_by_dir .             grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=250)
            select_by_file.             grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=550)
            # context_menu_button.        grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
            self.path_set.              grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
            button_explorer.            grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=855)
            button_save5.               grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=900)
            del_history_label.          grid(column =0,row=row_index+3,sticky = tk.W,pady =0,padx=10)
            context_menu_button2.       grid(column =0,row=row_index+4,sticky = tk.W,pady =0,padx=10)
            drop_down_options.          grid(column =0,row=row_index+4,sticky = tk.W,pady =0,padx=120)
            del_path_history.           grid(column =0,row=row_index+4,sticky = tk.W,pady =0,padx=480)
            default_path_insert_console.grid(column =0,row=row_index+5,sticky = tk.W,pady =10,padx=10)
            main_console.               grid(column =0,row=row_index+6,sticky = tk.W,pady =10,padx=10)
            # second_option_frame.        pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
            console_frame.              pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
            
            if self.windowed:
                save_changes_button.    pack(pady =5,padx=10,anchor = "e")
                save_frame.             pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top",anchor = "e")
            select_by_dir.select()
            # context_menu_button.bind("<Button-1>", call_path_context_menu)
            context_menu_button2.bind("<Button-1>", call_path_context_menu)

            def save_path_enter_btn(e):
                save_path()
                self.current_root.focus_set()
            self.path_set.bind("<Return>",save_path_enter_btn)

            app_zoom_slider.set(config_data["app_settings"]["app_zoom"])
            app_zoom_slider.update_idletasks()
            if config_data["app_settings"]["app_zoom_checkbox"] == "ano":
                checkbox_app_zoom.select()
                windows_zoom_setting()

            def slider_released(e):
                """
                save after the slider is released - it still opening and closing excel otherwise
                """
                if not checkbox_app_zoom.get() == 1:
                    current_zoom = int(app_zoom_slider.get())
                    Tools.save_to_json_config(current_zoom,"app_settings","app_zoom")
                    Tools.set_zoom(current_zoom,root)

            app_zoom_slider.bind("<ButtonRelease-1>",lambda e: slider_released(e))

            if config_data["app_settings"]["default_path"] != False and config_data["app_settings"]["default_path"] != "/":
                default_path_insert_console.configure(text="Aktuálně nastavená základní cesta k souborům: " + str(config_data["app_settings"]["default_path"]),text_color="white")
                self.path_set.configure(placeholder_text=str(config_data["app_settings"]["default_path"]))
                self.path_set.delete("0","200")
                self.path_set.insert("0", str(config_data["app_settings"]["default_path"]))
            else:
                default_path_insert_console.configure(text="Aktuálně nastavená základní cesta k souborům v konfiguračním souboru je neplatná",text_color="red")
                self.path_set.configure(placeholder_text="Není nastavena žádná základní cesta")
            
            if config_data["app_settings"]["maximalized"] == "ano":
                self.checkbox_maximalized.select()
            else:
                self.checkbox_maximalized.deselect()

            if config_data["app_settings"]["tray_icon_startup"]  == "ano":
                self.tray_checkbox.select()
            else:
                self.tray_checkbox.deselect()

            if config_data["app_settings"]["tooltip_status"]  == "ne":
                tooltip_checkbox.select()

    def creating_advanced_option_widgets(self): # Vytváří veškeré widgets (advance option MAIN)
        if self.windowed:
            self.current_root=customtkinter.CTkToplevel()
            x = self.root.winfo_rootx()
            y = self.root.winfo_rooty()
            self.current_root.geometry(f"1250x900+{x+200}+{y+200}")
            self.current_root.title("Pokročilá nastavení")
            self.current_root.after(200, lambda: self.current_root.iconbitmap(Tools.resource_path(app_icon)))
        else:
            self.current_root = self.root
        self.bottom_frame_default_path   = customtkinter.CTkFrame(master=self.current_root,corner_radius=0,border_width = 0)
        self.top_frame                   = customtkinter.CTkFrame(master=self.current_root,corner_radius=0,border_width = 0)
        self.menu_buttons_frame          = customtkinter.CTkFrame(master=self.current_root,corner_radius=0,fg_color="#636363",height=50,border_width = 0)
        self.top_frame.                 pack(pady=(2.5,0),padx=5,fill="x",expand=False,side = "top")
        self.menu_buttons_frame.        pack(pady=0,padx=5,fill="x",expand=False,side = "top")
        self.bottom_frame_default_path. pack(pady=(0,2.5),padx=5,fill="both",expand=True,side = "bottom")
        
        label0          = customtkinter.CTkLabel(master = self.top_frame,height=20,text = "Nastavte požadované parametry (nastavení bude uloženo i po vypnutí aplikace): ",justify = "left",font=("Arial",22,"bold"))
        main_menu_button =  customtkinter.CTkButton(master = self.menu_buttons_frame, width = 200,height=50,text = "MENU",                  command =  lambda: self.call_menu(),font=("Arial",20,"bold"),corner_radius=0,fg_color="black",hover_color="#212121")
        options0 =          customtkinter.CTkButton(master = self.menu_buttons_frame, width = 200,height=50,text = "Základní nastavení",    command =  lambda: self.setting_widgets(submenu_option="default_path"),font=("Arial",20,"bold"),corner_radius=0,fg_color="#212121",hover_color="#212121")
        label0.             grid(column = 0,row=0,sticky = tk.W,pady =10,padx=10)
        shift_const = 210
        if not self.windowed:
            main_menu_button.grid(column = 0,row=0,pady = (10,0),padx =10,sticky = tk.W)
            shift_const = 0
        options0.           grid(column = 0,row=0,pady = (10,0),padx =220-shift_const,sticky = tk.W)
        self.option_buttons = [options0]

        if self.windowed and not global_recources_load_error:
            if self.spec_location == "image_browser":
                self.setting_widgets(submenu_option="set_image_browser_setting")
            else:
                self.setting_widgets(submenu_option="default_path")
        elif not global_recources_load_error:
            self.setting_widgets(submenu_option="default_path")
        elif global_recources_load_error:
            error_label = customtkinter.CTkLabel(master = self.bottom_frame_default_path,height=20,text = "Nepodařilo se načíst konfigurační soubor config_TRIMAZKON.xlsx (nastavení se nemá kam uložit)",justify = "left",font=("Arial",22,"bold"),text_color="red")
            error_label.grid(column = 0,row=0,pady = (10,0),padx =20,sticky = tk.W)
            options0.configure(state = "disabled")

        def maximalize_window(e):
            # netrigguj fullscreen zatimco pisu do vstupniho textovyho pole
            currently_focused = str(self.current_root.focus_get())
            if ".!ctkentry" in currently_focused:
                return
            if int(self.current_root._current_width) > 1200:
                self.current_root.after(0, lambda:self.current_root.state('normal'))
                self.current_root.geometry("1250x900")
            else:
                self.current_root.after(0, lambda:self.current_root.state('zoomed'))
        self.current_root.bind("<f>",maximalize_window)
        self.unbind_list.append("<f>")

        def unfocus_widget(e):
            self.current_root.focus_set()
        self.current_root.bind("<Escape>",unfocus_widget)
        self.unbind_list.append("<Escape>")

        if self.windowed:
            self.current_root.update()
            self.current_root.update_idletasks()
            self.current_root.focus_force()
            self.current_root.focus()
            # click outside the window - kill it
            self.root.bind("<Button-1>",lambda e: self.current_root.destroy())

class IP_manager: # Umožňuje nastavit možnosti třídění souborů
    """
    Umožňuje měnit statickou IPv4 adresu a spravovat síťové disky

    - pracuje s excelovým souborem, kam ukládá data o projektech a o nastavení\n
    - umožňuje projekty doplňovat poznámkami\n
    - umožňuje odpojit síťový disk\n
    - umožňuje namountit síťový disk a trvale jej přidat do windows exploreru\n
    - poskytuje informaci o aktuální statické ip adrese u daného interfacu\n
    - poskytuje informaci o současně připojených síťových discích\n
    - poskytuje informaci o namountěných offline síťových discích\n
    - vše je ošetřeno timeoutem\n
    """
    def __init__(self,root):
        self.root = root
        self.create_IP_manager_widgets()
    
    def callback(self):
        menu.menu()

    def create_IP_manager_widgets(self):
        if root.wm_state() == "zoomed":
            current_window_size = "max"
        else:
            current_window_size = "min"

        app_data = Tools.read_json_config()
        zoom_factor = app_data["app_settings"]["app_zoom"]

        # IP_setting.IP_assignment(self.root,self.callback,current_window_size,initial_path,zoom_factor)
        IP_setting.main(self.root,self.callback,current_window_size,initial_path,zoom_factor,config_filename)

if load_gui:
    if not app_running_status:
        menu = main_menu(root)
        menu.menu(initial=True)

def start_new_root():
    print("starting new root")
    global menu
    global root
    global app_icon
    global initial_path
    # global app_version
    initial_path = Tools.get_init_path()
    app_icon = Tools.resource_path('images/logo_TRIMAZKON.ico')
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    root=customtkinter.CTk(fg_color="#212121")
    root.geometry("1200x900")
    root.title(f"{app_name} v_{app_version}")
    root.wm_iconbitmap(app_icon)
    root.update_idletasks()
    menu = main_menu(root)
    menu.menu(initial=True)
    root.mainloop()

if loop_request:
        root.mainloop()
