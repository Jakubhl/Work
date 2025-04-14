import sys
import win32file
from psutil import process_iter as psutil_process_iter
from os.path import basename as os_path_basename
from os.path import exists as os_path_exists
from os import getpid as os_get_pid

class initial_tools:
    @classmethod
    def get_all_app_processes(cls):
        pid_list = []
        num_of_apps = 0
        for process in psutil_process_iter(['pid', 'name']):
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
        if not os_path_exists(path) and only_repair == None:
            return False
        else:
            return path

testing = False

global_recources_load_error = False
global_licence_load_error = False
exe_path = sys.executable
exe_name = os_path_basename(exe_path)
config_filename = "TRIMAZKON.json"
app_name = "TRIMAZKON"
app_version = "4.3.3"
loop_request = False
root = None
print("exe name: ",exe_name)
if testing:
    exe_name = "trimazkon_test.exe"

app_running_status = initial_tools.check_runing_app_duplicity()
print("already opened app status: ",app_running_status)
open_image_only = False
if len(sys.argv) > 1 and app_running_status == True:
    used_cmd_calls = ["deleting","trigger_by_tray","run_tray","open_task_list","open_log_list","app_shutdown","edit_existing_task","settings_tray","settings_tray_del","admin_menu","installer_call","manual_ip_setting"]
    if str(sys.argv[1]) not in used_cmd_calls:
        if sys.argv[0] != sys.argv[1]:
            open_image_only = True

if not open_image_only:
    import customtkinter
    import os
    import time
    from PIL import Image, ImageTk
    import Sorting_option_v5 as Trideni
    import Deleting_option_v2 as Deleting
    import Converting_option_v3 as Converting
    import catalogue_maker_v5 as Catalogue
    import sharepoint_download as download_database
    import IP_setting_v6 as IP_setting
    import trimazkon_tray_v5 as trimazkon_tray
    import string_database
    from tkinter import filedialog
    import tkinter as tk
    import threading
    import shutil
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
            label_frame = customtkinter.CTkFrame(master = child_root,corner_radius=0)
            proceed_label = customtkinter.CTkLabel(master = label_frame,text = main_title,font=("Arial",25),anchor="w",justify="left")
            proceed_label.pack(pady=5,padx=10,anchor="w",side = "left")
            button_frame = customtkinter.CTkFrame(master = child_root,corner_radius=0)
            button_yes =    customtkinter.CTkButton(master = button_frame,text = "ANO",font=("Arial",20,"bold"),width = 200,height=50,corner_radius=0,command=lambda: run_as_admin())
            button_no =     customtkinter.CTkButton(master = button_frame,text = "Zrušit",font=("Arial",20,"bold"),width = 200,height=50,corner_radius=0,command=lambda:  close_prompt(child_root))
            button_no       .pack(pady = 5, padx = 10,anchor="e",side="right")
            button_yes      .pack(pady = 5, padx = 10,anchor="e",side="right")
            label_frame    .pack(pady=0,padx=0,anchor="w",side = "top",fill="x",expand=True)
            button_frame    .pack(pady=0,padx=0,anchor="w",side = "top",fill="x",expand=True)
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
        def licence_window(cls,language_given="cz"):
            def close_prompt(child_root):
                child_root.grab_release()
                child_root.destroy()

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
            label_frame = customtkinter.CTkFrame(master = child_root,corner_radius=0)
            proceed_label = customtkinter.CTkLabel(master = label_frame,text = prompt_message1,font=("Arial",25,"bold"),anchor="w",justify="left")
            proceed_label.pack(pady=(5,0),padx=10,anchor="w",side = "left")
            label_frame    .pack(pady=0,padx=0,anchor="w",side = "top",fill="x",expand=True)

            text_widget = tk.Text(master = child_root,background="#212121",borderwidth=0,height=9)
            Tools.add_colored_line(text_widget,text=prompt_message2,color="gray84",font=("Arial",16),no_indent=True)
            Tools.add_colored_line(text_widget,text=prompt_message3,color="white",font=("Arial",16,"bold"),no_indent=True)
            Tools.add_colored_line(text_widget,text=prompt_message4,color="gray84",font=("Arial",16),no_indent=True, sameline=True)
            Tools.add_colored_line(text_widget,text=prompt_message5,color="skyblue",font=("Arial",16),no_indent=True, sameline=True)
            Tools.add_colored_line(text_widget,text=prompt_message6,color="gray84",font=("Arial",16),no_indent=True, sameline=True)
            text_widget    .pack(pady=10,padx=(30,10),anchor="w",side = "top",fill="both",expand=True)

            button_frame = customtkinter.CTkFrame(master = child_root,corner_radius=0)
            button_close =    customtkinter.CTkButton(master = button_frame,text = "Zavřít",font=("Arial",20,"bold"),width = 200,height=50,corner_radius=0,command=lambda:  close_prompt(child_root))
            button_close     .pack(pady = 5, padx = 10,anchor="e",side="right")
            button_frame   .pack(pady=0,padx=0,anchor="w",side = "top",fill="x",expand=True)

            if language_given == "en":
                button_close.configure(text = "Close")
            child_root.update()
            child_root.update_idletasks()
            child_root.geometry("800x260")
            child_root.focus()
            child_root.focus_force()
            child_root.grab_set()

        @classmethod
        def save_new_task(cls, selected_option_given, by_creation_date, path_given, cutoff_date_given, files_to_keep_given, dirs_to_keep_given, more_dirs, task_name_given = None, edit_status = False,root_given = None,frequency_given = None, selected_language="cz",wait_request=False,main_root = None):  
            selected_option_given = int(selected_option_given)
            if int(more_dirs) == 0:
                more_dirs = False
            elif int(more_dirs) == 1:
                more_dirs = True
            
            if int(by_creation_date) == 0:
                by_creation_date = False
            elif int(by_creation_date) == 1:
                by_creation_date = True
            
            def call_browse_directories():
                """
                Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
                """
                path_from_history = None
                try:
                    path_from_history = Tools.read_json_config()["del_settings"]["path_history_list"][0]
                except Exception:
                    pass
                if os.path.exists(str(operating_path.get())):
                    output = Tools.browseDirectories("only_dirs",start_path=str(operating_path.get()))
                elif os.path.exists(path_from_history):
                    output = Tools.browseDirectories("only_dirs",start_path=path_from_history)
                else:
                    output = Tools.browseDirectories("only_dirs")
                if str(output[1]) != "/":
                    operating_path.delete(0,300)
                    operating_path.insert(0, str(output[1]))
                    Tools.add_new_path_to_history(str(output[1]),"del_settings")
                    if selected_language == "en":
                        Tools.add_colored_line(console,"The path where the task will be executed has been inserted.","green",None,True)
                    else:
                        Tools.add_colored_line(console,"Byla vložena cesta pro vykonávání úkolu","green",None,True)

                print(output[0])
                window.focus()
                window.focus_force()

            def save_task_to_config():
                if check_entry("",hour_format=True,input_char=str(frequency_entry.get())) == False:
                    return
                
                if Tools.path_check(operating_path.get()) == False:
                    if selected_language == "en":
                        Tools.add_colored_line(console,"Inserted path does not exist or is corrupted","red",None,True)
                    else:
                        Tools.add_colored_line(console,"Vložená cesta neexistuje nebo je chybná","red",None,True)
                    return
                    
                def get_task_name(current_tasks):
                    if edit_status:
                        return task_name_given
                    names_taken = []
                    new_task_name = "TRIMAZKON_del_task_xx"
                    for tasks in current_tasks:
                        names_taken.append(tasks["name"])
                    for i in range(1,100):
                        name_suggestion = "TRIMAZKON_del_task_" + str(i)
                        if name_suggestion in names_taken:
                            continue
                        if Tools.check_task_existence_in_TS(name_suggestion):
                            continue
                        new_task_name = name_suggestion
                        break
                    return new_task_name

                def set_up_task_in_ts():
                    def check_freq_format(freq_input):
                        input_splitted = freq_input.split(":")
                        if len(str(input_splitted[0])) == 1:
                            corrected = "0"+str(input_splitted[0]) +":"+ str(input_splitted[1])
                            return corrected
                        else:
                            return freq_input
                            
                    task_name = str(new_task["name"])
                    repaired_freq_param = check_freq_format(str(new_task["frequency"]))
                    path_app_location = str(initial_path+"/"+exe_name)
                    operating_path_TS = str(new_task["operating_path"])
                    full_path = r"{}".format(operating_path_TS)
                    full_path = full_path.replace(" ","-|-") # mezery zakodovat na specialni znak
                    # task_command = "\""+ path_app_location+ " deleting " + task_name + " " + str(new_task["operating_path"]) + " " + str(new_task["max_days"]) + " " + str(new_task["files_to_keep"]) + "\" /SC DAILY /ST " + repaired_freq_param
                    task_command = "\""+ path_app_location+ " deleting " + task_name + " " + full_path + " " + str(new_task["max_days"]) + " " + str(new_task["files_to_keep"]) + " " + str(new_task["more_dirs"]) + " " + str(new_task["selected_option"]) + " " + str(new_task["creation_date"]) + "\" /SC DAILY /ST " + repaired_freq_param
                    process = subprocess.Popen(f"schtasks /Create /TN {task_name} /TR {task_command}",
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                creationflags=subprocess.CREATE_NO_WINDOW)
                    stdout, stderr = process.communicate()
                    try:
                        stdout_str = stdout.decode('utf-8')
                        data = str(stdout_str)
                    except UnicodeDecodeError:
                        try:
                            stdout_str = stdout.decode('cp1250')
                            data = str(stdout_str)
                        except UnicodeDecodeError:
                            data = str(stdout)
                    output_message = "out"+str(stdout) +"err"+str(stderr)
                    print(output_message)
                    if "SUCCESS" in stdout_str:
                        # os.startfile("taskschd.msc")
                        return True
                    else:
                        return False

                current_tasks = trimazkon_tray_instance.read_config()
                print("current tasks: ",current_tasks)

                new_task = {'name': get_task_name(current_tasks),
                            'operating_path': Tools.path_check(operating_path.get()),
                            'max_days': older_then_entry.get(),
                            'files_to_keep': minimum_file_entry.get(),
                            'frequency': frequency_entry.get(),
                            'more_dirs': subfolder_checkbox.get(),
                            'selected_option': selected_option_given,
                            'date_added': str(Deleting.get_current_date()[2]),
                            'del_log': [],
                            'creation_date': checkbox_creation_date.get(),
                            }

                try:
                    if edit_status: # delete the task before changes
                        for i in range(0,len(current_tasks)):
                            if current_tasks[i]["name"] == task_name_given:
                                print("popped: ",current_tasks[i]["name"])
                                current_tasks.pop(i)
                                break
                        trimazkon_tray_instance.delete_task(task_name_given,only_scheduler=True)
                        print("deleted from scheduler",task_name_given)

                    success_status = set_up_task_in_ts()
                    if success_status:
                        if selected_language == "en":
                            Tools.add_colored_line(console,"The new task has been saved and entered into the task scheduler","green",None,True)
                            if edit_status:
                                Tools.add_colored_line(console,"The task changes has been saved and updated in task scheduler","green",None,True)
                        else:
                            Tools.add_colored_line(console,"Nový úkol byl uložen a zaveden do task scheduleru","green",None,True)
                            if edit_status:
                                Tools.add_colored_line(console,"Změny úkolu byly uloženy a aktualizovány v task scheduleru","green",None,True)

                        current_tasks.append(new_task)
                        trimazkon_tray_instance.save_task_to_config(current_tasks)
                        if edit_status:
                            try:
                                root_given_obj = root.nametowidget(root_given)
                                trimazkon_tray_instance.show_all_tasks(root_given=root_given_obj) # refresh s novým nastavením
                                window.after(10,window.focus_force())
                                
                            except Exception as e:
                                print("chyba pri aktualizovani okna u editu tasku",e)
                    else:
                        if selected_language == "en":
                            Tools.add_colored_line(console,"Unexpected error, failed to set a new task","red",None,True)
                            if edit_status:
                                Tools.add_colored_line(console,"Unexpected error, failed to save edited task","red",None,True)
                        else:
                            Tools.add_colored_line(console,"Neočekávaná chyba, nepovedlo se nastavit nový úkol","red",None,True)
                            if edit_status:
                                Tools.add_colored_line(console,"Neočekávaná chyba, nepovedlo se uložit editovaný úkol","red",None,True)
                except Exception as e:
                    if selected_language == "en":
                        Tools.add_colored_line(console,f"Please close the configuration file ({e})","red",None,True)
                    else:
                        Tools.add_colored_line(console,f"Prosím zavřete konfigurační soubor ({e})","red",None,True)

            def refresh_cutoff_date():
                older_then_entry.update()
                older_then_entry.update_idletasks()
                try:
                    cutoffdate_list = Deleting.get_cutoff_date(int(older_then_entry.get()))
                    new_date = "(starší než: "+str(cutoffdate_list[0])+"."+str(cutoffdate_list[1])+"."+str(cutoffdate_list[2])+")"
                    if selected_language == "en":
                        new_date = "(older then: "+str(cutoffdate_list[0])+"."+str(cutoffdate_list[1])+"."+str(cutoffdate_list[2])+")"
                    if older_then_label3.cget("text") != new_date:
                        older_then_label3.configure(text = new_date)
                except Exception:
                    pass

            def check_entry(event,number=False,hour_format=False,input_char=None,flag=""):
                if flag == "cutoff":
                    window.after(100, lambda: refresh_cutoff_date())
                if event != "":
                    if event.keysym == "BackSpace" or event.keysym == "Return":
                        return

                if number:
                    if not event.char.isdigit():
                        if selected_language == "en":
                            Tools.add_colored_line(console,"Enter only numbers","red",None,True)
                        else:
                            Tools.add_colored_line(console,"Vkládejte pouze čísla","red",None,True)
                        event.widget.insert(tk.INSERT,"")
                        return "break"  # Stop the event from inserting the original character
                    
                elif hour_format:
                    separator_err_msg = "Neplatný formát času, chybí separátor (vkládejte ve formátu: 00:00)"
                    time_format_err_msg = "Neplatný formát času (vkládejte ve formátu: 00:00)"
                    bad_chars_err_msg = "Neplatné znaky u času (vkládejte ve formátu: 00:00)"
                    out_of_range_err_msg = "Neplatný formát času, mimo rozsah (vkládejte ve formátu: 00:00)"
                    if selected_language == "en":
                        separator_err_msg = "Invalid time format, missing separator (insert in format: 00:00)"
                        time_format_err_msg = "Invalid time format (enter in format: 00:00)"
                        bad_chars_err_msg = "Invalid characters for time (enter in format: 00:00)"
                        out_of_range_err_msg = "Invalid time format, out of range (insert in format: 00:00)"

                    if not ":" in input_char:
                        Tools.add_colored_line(console,separator_err_msg,"red",None,True)
                        return False
                    elif len(input_char.split(":")) != 2:
                        Tools.add_colored_line(console,time_format_err_msg,"red",None,True)
                        return False
                    elif len(str(input_char.split(":")[1])) != 2:
                        Tools.add_colored_line(console,time_format_err_msg,"red",None,True)
                        return False
                    elif not input_char.split(":")[0].isdigit() or not input_char.split(":")[1].isdigit():
                        Tools.add_colored_line(console,bad_chars_err_msg,"red",None,True)
                        return False
                    elif int(input_char.split(":")[0]) > 23 or int(input_char.split(":")[0]) < 0 or int(input_char.split(":")[1]) > 59 or int(input_char.split(":")[1]) < 0:
                        Tools.add_colored_line(console,out_of_range_err_msg,"red",None,True)
                        return False
                
            def call_path_context_menu(event):
                path_history = Tools.read_json_config()["del_settings"]["path_history_list"]
                def insert_path(path):
                    operating_path.delete("0","200")
                    operating_path.insert("0", path)
                if len(path_history) > 0:
                    path_context_menu = tk.Menu(window, tearoff=0,fg="white",bg="black")
                    for i in range(0,len(path_history)):
                        path_context_menu.add_command(label=path_history[i], command=lambda row_path = path_history[i]: insert_path(row_path),font=("Arial",22,"bold"))
                        if i < len(path_history)-1:
                            path_context_menu.add_separator()
                            
                    path_context_menu.tk_popup(context_menu_button.winfo_rootx(),context_menu_button.winfo_rooty()+50)

            def set_decision_date(input_arg):
                """
                input_arg:
                - creation
                - modification
                """
                nonlocal by_creation_date
                if input_arg == "creation":
                    by_creation_date = True
                    checkbox_modification_date.deselect()

                elif input_arg == "modification":
                    by_creation_date = False
                    checkbox_creation_date.deselect()

            window = customtkinter.CTkToplevel()
            window.after(200, lambda: window.iconbitmap(app_icon))
            window.title("Nastavení nového úkolu")
            if edit_status:
                window.title("Editování úkolu: "+str(task_name_given))

            if selected_language == "en":
                window.title("Setting up a new task")
                if edit_status:
                    window.title("Editing task: "+str(task_name_given))
            trimazkon_tray_instance = trimazkon_tray.tray_app_service(initial_path,app_icon,exe_name,config_filename)
            parameter_frame = customtkinter.CTkFrame(master = window,corner_radius=0)
            selected_option = customtkinter.CTkLabel(master = parameter_frame,text = "Zvolená možnost mazání: ",font=("Arial",25,"bold"))
            path_label_frame = customtkinter.CTkFrame(master = parameter_frame,corner_radius=0,fg_color="#212121")
            path_label = customtkinter.CTkLabel(master = path_label_frame,text = "Zadejte cestu, kde bude úkol spouštěn:",font=("Arial",22))
            path_label.pack(pady = (10,0),padx = (10,0),side="left",anchor="w")
            subfolder_checkbox = customtkinter.CTkCheckBox(master = path_label_frame, text = "Procházet subsložky? (max: 6)",font=("Arial",20,"bold"))
            if selected_option_given != 3 and selected_option_given != 4:
                subfolder_checkbox.pack(pady = (10,0),padx = (0,10),side="right",anchor="e")
                if more_dirs:
                    subfolder_checkbox.select()

            path_frame = customtkinter.CTkFrame(master = parameter_frame,corner_radius=0,fg_color="#212121")
            context_menu_button  =  customtkinter.CTkButton(master = path_frame, width = 50,height=50, text = "V",font=("Arial",20,"bold"),corner_radius=0,fg_color="#505050")
            operating_path = customtkinter.CTkEntry(master = path_frame,font=("Arial",20),height=50,corner_radius=0)
            explorer_btn = customtkinter.CTkButton(master = path_frame,text = "...",font=("Arial",22,"bold"),width = 50,height=50,corner_radius=0,command=lambda: call_browse_directories())
            selected_option.pack(pady = (10,0),padx = (10,0),side="top",anchor="w")
            path_label_frame.pack(side="top",anchor="w",fill="x",expand = True)
            context_menu_button.pack(pady = (10,0),padx = (10,0),side="left",anchor="w")
            operating_path.pack(pady = (10,0),padx = (0,0),side="left",anchor="w",expand = True,fill="x")
            explorer_btn.pack(pady = (10,0),padx = (0,10),side="left",anchor="w")
            path_frame.pack(side="top",anchor="w",fill="x",expand = True)
            context_menu_button.bind("<Button-1>", call_path_context_menu)

            decision_date_frame = customtkinter.CTkFrame(master=parameter_frame,corner_radius=0,fg_color="#212121")
            decision_date_label = customtkinter.CTkLabel(master = decision_date_frame,text = "Řídit se podle: ",justify = "left",font=("Arial",20,"bold"))
            checkbox_creation_date = customtkinter.CTkCheckBox(master =decision_date_frame, text = "data vytvoření",font=("Arial",18),command=lambda:set_decision_date("creation"))
            checkbox_modification_date = customtkinter.CTkCheckBox(master =decision_date_frame, text = "data poslední změny (doporučeno)",font=("Arial",18),command=lambda:set_decision_date("modification"))
            decision_date_label.pack(pady = (10,10),padx =(10,0),side="left",anchor="w")
            checkbox_creation_date.pack(pady = (10,10),padx =(10,0),side="left",anchor="w")
            checkbox_modification_date.pack(pady = (10,10),padx =(10,0),side="left",anchor="w")
            decision_date_frame.pack(pady = (0,0),padx =0,side="top",anchor="w",fill="x")
            if by_creation_date:
                checkbox_creation_date.select()
            else:
                checkbox_modification_date.select()

            older_then_frame = customtkinter.CTkFrame(master = parameter_frame,corner_radius=0)
            older_then_label = customtkinter.CTkLabel(master = older_then_frame,text = "Odstanit soubory starší než:",font=("Arial",22,"bold"))
            older_then_entry = customtkinter.CTkEntry(master = older_then_frame,font=("Arial",20),width=100,height=40,corner_radius=0)
            older_then_label2 = customtkinter.CTkLabel(master = older_then_frame,text = "dní",font=("Arial",22,"bold"))
            older_then_label3 = customtkinter.CTkLabel(master = older_then_frame,text = "",font=("Arial",22,"bold"))
            older_then_label.pack(pady = (10,0),padx = (10,10),side="left")
            older_then_entry.pack(pady = (10,0),padx = (0,0),side="left")
            older_then_label2.pack(pady = (10,0),padx = (10,0),side="left")
            older_then_label3.pack(pady = (10,0),padx = (10,10),side="left")
            older_then_frame.pack(side="top",fill="x",anchor="w")
            older_then_entry.bind("<Key>",lambda e: check_entry(e,number=True,flag="cutoff"))

            minimum_file_frame = customtkinter.CTkFrame(master = parameter_frame,corner_radius=0)
            minimum_file_label = customtkinter.CTkLabel(master = minimum_file_frame,text = "Ponechat souborů:",font=("Arial",22,"bold"))
            minimum_file_entry = customtkinter.CTkEntry(master = minimum_file_frame,font=("Arial",20),width=100,height=40,corner_radius=0)
            minimum_file_label.pack(pady = (10,0),padx = (10,10),side="left")
            minimum_file_entry.pack(pady = (10,0),padx = (0,10),side="left")
            if selected_option_given != 3:
                minimum_file_frame.pack(side="top",fill="x",anchor="w")
            minimum_file_entry.bind("<Key>",lambda e: check_entry(e,number=True))

            frequency_frame = customtkinter.CTkFrame(master = parameter_frame,corner_radius=0)
            frequency_label = customtkinter.CTkLabel(master = frequency_frame,text = "Frekvence: denně, ",font=("Arial",22,"bold"))
            frequency_entry = customtkinter.CTkEntry(master = frequency_frame,font=("Arial",20),width=100,height=40,corner_radius=0)
            frequency_label2 = customtkinter.CTkLabel(master = frequency_frame,text = "hodin (př.: 0:00, 6:00, 14:30)",font=("Arial",22,"bold"))
            frequency_label.pack(pady = (10,0),padx = (10,10),side="left",anchor="w")
            frequency_entry.pack(pady = (10,0),padx = (0,0),side="left",anchor="w")
            frequency_label2.pack(pady = (10,0),padx = (10,10),side="left",anchor="w")
            frequency_frame.pack(side="top",fill="x",anchor="w")
            console = tk.Text(parameter_frame, wrap="none", height=0, width=30,background="black",font=("Arial",22),state=tk.DISABLED)
            console.pack(pady = 10,padx =10,side="top",anchor="w",fill="x")

            button_frame =   customtkinter.CTkFrame(master = window,corner_radius=0)
            show_tasks_btn = customtkinter.CTkButton(master = button_frame, width = 300,height=50,text = "Zobrazit nastavené úkoly", command =  lambda: trimazkon_tray_instance.show_all_tasks(toplevel=True),font=("Arial",20,"bold"),corner_radius=0)
            save_task_btn =  customtkinter.CTkButton(master = button_frame, width = 300,height=50,text = "Uložit nový úkol", command =  lambda: save_task_to_config(),font=("Arial",20,"bold"),corner_radius=0)
            cancel_btn =  customtkinter.CTkButton(master = button_frame, width = 300,height=50,text = "Zavřít", command =  lambda: window.destroy(),font=("Arial",20,"bold"),corner_radius=0)
            cancel_btn.   pack(pady=10,padx=(10,10),side="right",anchor="e")
            save_task_btn.   pack(pady=10,padx=(10,0),side="right",anchor="e")
            if not edit_status:
                show_tasks_btn.  pack(pady=10,padx=(10,0),side="right",anchor="e")
            parameter_frame.pack(side="top",fill="both")
            button_frame.pack(side="top",fill="x")
            operating_path.insert("0",path_given)
            if edit_status:
                max_days = cutoff_date_given
                frequency_entry.insert("0",frequency_given)
                save_task_btn.configure(text = "Uložit změny")
            else:
                max_days = Deleting.get_max_days(cutoff_date_given)
                frequency_entry.insert("0","12:00")
            older_then_entry.insert("0",max_days)
            minimum_file_entry.insert("0",files_to_keep_given)
            if selected_option_given == 4:
                minimum_file_entry.delete("0","200")
                minimum_file_entry.insert("0",dirs_to_keep_given)
            
            refresh_cutoff_date()

            if selected_language == "en":
                path_label.configure(text = "Specify the path where the task will run:")
                subfolder_checkbox.configure(text = "Browse subfolders? (max: 6)")
                older_then_label.configure(text = "Remove files older than:")
                older_then_label2.configure(text = "days")
                minimum_file_label.configure(text = "Keep files:")
                frequency_label.configure(text = "Frequency: daily, ")
                frequency_label2.configure(text = "hours (ex.: 0:00, 6:00, 14:30)")
                show_tasks_btn.configure(text = "Show set tasks")
                save_task_btn.configure(text = "Save new task")
                if edit_status:
                    save_task_btn.configure(text = "Apply changes")
                cancel_btn.configure(text = "Close")
                decision_date_label.configure(text = "To decide by: ")
                checkbox_modification_date.configure(text = "date modified (recommended)")
                checkbox_creation_date.configure(text = "date created")
                
            if selected_option_given == 1:
                selected_option.configure(text = f"Zvolená možnost mazání: {selected_option_given}. (Redukce starších souborů)")
                if selected_language == "en":
                    selected_option.configure(text = f"Selected delete option: {selected_option_given}. (Reducing older files)")
            elif selected_option_given == 2:
                selected_option.configure(text = f"Zvolená možnost mazání: {selected_option_given}. (Redukce novějších, mazání starších souborů)")
                if selected_language == "en":
                    selected_option.configure(text = f"Selected delete option: {selected_option_given}. (Reducing newer, deleting older files)")
            elif selected_option_given == 3:
                selected_option.configure(text = f"Zvolená možnost mazání: {selected_option_given}. (Mazání adresářů podle názvu)")
                older_then_label.configure(text = "Odstanit adresáře starší než:")
                if selected_language == "en":
                    selected_option.configure(text = f"Selected delete option: {selected_option_given}. (Deleting directories by name)")
                    older_then_label.configure(text = "Remove directories older than:")
            elif selected_option_given == 4:
                selected_option.configure(text = f"Zvolená možnost mazání: {selected_option_given}. (Mazání starších adresářů)")
                older_then_label.configure(text = "Odstanit adresáře starší než:")
                minimum_file_label.configure(text = "Ponechat adresářů:")
                if selected_language == "en":
                    selected_option.configure(text = f"Selected delete option: {selected_option_given}. (Deleting older directories)")
                    older_then_label.configure(text = "Remove directories older than:")
                    minimum_file_label.configure(text = "Keep directories:")
            window.update()
            window.update_idletasks()
            # window_width = window.winfo_width()
            # if window_width < 1200:
            #     window_width = 1200
            window.geometry(f"{1200}x{window.winfo_height()}")
            window.after(10,window.focus_force())
            window.focus()
            try:
                main_root.bind("<Button-1>",lambda e: window.destroy())
            except Exception:
                pass
            if wait_request:
                window.deiconify()
                window.wait_window()
        
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
        task_name = "TRIMAZKON_startup_tray_setup"
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
        def deleting_via_cmd(cls,param_given = []):
            if len(param_given) == 0:
                print("deleting system entry: ",sys.argv)
                task_name = str(sys.argv[2])
                deleting_path = str(sys.argv[3])
                max_days = int(sys.argv[4])
                files_to_keep = int(sys.argv[5])
                more_dirs = int(sys.argv[6])
                selected_option = int(sys.argv[7])
                by_creation_date = int(sys.argv[8])
            else:
                print("deleting system entry: ",param_given)
                task_name = str(param_given[0])
                deleting_path = str(param_given[1])
                max_days = int(param_given[2])
                files_to_keep = int(param_given[3])
                more_dirs = int(param_given[4])
                selected_option = int(param_given[5])
                by_creation_date = int(param_given[6])

            deleting_path = deleting_path.replace("-|-"," ") # dekodovat mezery
            cutoff_date = Deleting.get_cutoff_date(days=max_days)
            config_data = Tools.read_json_config()
            supported_formats_deleting = config_data["del_settings"]["supported_formats_deleting"]
            to_delete_folder_name = config_data["del_settings"]["to_delete_dir_name"]

            if more_dirs == 0:
                more_dirs = False
            else:
                more_dirs = True

            if by_creation_date == 0:
                by_creation_date = False
            else:
                by_creation_date = True

            del_instance = Deleting.whole_deleting_function(
                deleting_path,
                more_dirs=more_dirs,
                del_option=selected_option,
                files_to_keep=files_to_keep,
                cutoff_date_given=cutoff_date,
                supported_formats=supported_formats_deleting,
                testing_mode=False,
                to_delete_folder_name=to_delete_folder_name,
                creation_date=by_creation_date
                )
            output_data = del_instance.main()
            # output_message = f"|||Datum provedení: {output_data[3]}||Zkontrolováno: {output_data[0]} souborů||Starších: {output_data[1]} souborů||Smazáno: {output_data[2]} souborů"
            if selected_option == 1:
                new_log = {"del_date": output_data[3],
                        "files_checked": output_data[0],
                        "files_older": output_data[1],
                        "files_newer": "",
                        "files_deleted": output_data[2],
                        "path_count": output_data[5],
                        }
                output_message = f"Provedeno: {output_data[3]}\nZkontrolováno: {output_data[0]} souborů\nStarších: {output_data[1]} souborů\nSmazáno: {output_data[2]} souborů"
                output_message_eng = f"Date of execution: {output_data[3]}\nTotal checked: {output_data[0]} files\nTotal older: {output_data[1]} files\nTotal deleted: {output_data[2]} files"

            elif selected_option == 2:
                new_log = {"del_date": output_data[3],
                        "files_checked": output_data[0],
                        "files_older": output_data[1],
                        "files_newer": output_data[4],
                        "files_deleted": output_data[2],
                        "path_count": output_data[5],
                        }
                output_message = f"Provedeno: {output_data[3]}\nZkontrolováno: {output_data[0]} souborů\nStarších: {output_data[1]} souborů, novějších: {output_data[4]} souborů\nSmazáno: {output_data[2]} souborů"
                output_message_eng = f"Date of execution: {output_data[3]}\nTotal checked: {output_data[0]} files\nTotal older: {output_data[1]} files, newer: {output_data[4]} files\nTotal deleted: {output_data[2]} files"

            elif selected_option == 3:
                new_log = {"del_date": output_data[3],
                        "files_checked": output_data[0],
                        "files_older": "",
                        "files_newer": "",
                        "files_deleted": output_data[2],
                        "path_count": "",
                        }
                
                output_message = f"Provedeno: {output_data[3]}\nZkontrolováno: {output_data[0]} adresářů\nSmazáno: {output_data[2]} adresářů"
                output_message_eng = f"Date of execution: {output_data[3]}\nTotal checked: {output_data[0]} directories\nTotal deleted: {output_data[2]} directories"

            elif selected_option == 4:
                new_log = {"del_date": output_data[3],
                        "files_checked": output_data[0],
                        "files_older": output_data[1],
                        "files_newer": "",
                        "files_deleted": output_data[2],
                        "path_count": "",
                        }
                output_message = f"Provedeno: {output_data[3]}\nZkontrolováno: {output_data[0]} adresářů\nStarších: {output_data[1]} adresářů\nSmazáno: {output_data[2]} adresářů"
                output_message_eng = f"Date of execution: {output_data[3]}\nTotal checked: {output_data[0]} directories\nTotal older: {output_data[1]} directories\nTotal deleted: {output_data[2]} directories"

            if more_dirs:
                output_message += f", prohledáno: {output_data[5]} subsložek"
                output_message_eng += f", browsed: {output_data[5]} subdirectories"

            print(output_message,output_message_eng)
            title_message = "Bylo provedeno automatické mazání"
            selected_language = "cz"
            try:
                selected_language = Tools.read_json_config()[11]
            except Exception as e:
                print(e)
            if selected_language == "en":
                title_message = "Automatic deletion has been performed"
                output_message = output_message_eng
            icon_path = app_icon
            trimazkon_tray_instance = trimazkon_tray.tray_app_service(initial_path,icon_path,exe_name,config_filename)
            trimazkon_tray_instance.save_new_log(task_name,new_log)
            WindowsBalloonTip(title_message,
                                str(output_message),
                                icon_path)
        
            return output_message

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

class system_pipeline_communication: # vytvoření pipeline serveru s pipe názvem TRIMAZKON_pipe_ + pid (id systémového procesu)
    """
    aby bylo možné posílat běžící aplikaci parametry:
    - mám otevřené okno ip setting - kliknu na obrázek - jen pošlu parametry
    """
    def __init__(self,exe_name,no_server = False):
        self.root = None #define later (to prevend gui loading when 2 apps opened)
        # self.current_pid = None
        self.exe_name = exe_name
        self.current_pid = os_get_pid()
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

                    elif "Execute file deleting" in received_data:
                        received_params = received_data.split("|||")
                        print("received_params: ",received_params)
                        params_to_send = [received_params[1],received_params[2],received_params[3],received_params[4],received_params[5],received_params[6],received_params[7]]
                        print("params to send: ",params_to_send)
                        del_thread = threading.Thread(target=Tools.deleting_via_cmd,args=[params_to_send],name="Deleting_thread")
                        del_thread.start()

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

                    elif "Edit existing task" in received_data:
                        received_params = received_data.split("|||")
                        print("received_params: ",received_params)
                        wait_request = False
                        try:
                            if root.state() == "iconic":
                                wait_request = True
                            print(root.state())
                        except Exception as e:
                            print(e)

                        def call_long_task():
                            Subwindows.save_new_task(received_params[9],
                                                 received_params[10],
                                                 received_params[4],
                                                 received_params[5],
                                                 received_params[6],
                                                 received_params[6],
                                                 received_params[8],
                                                 received_params[3],
                                                 edit_status=True,
                                                 root_given=received_params[11],
                                                 frequency_given=received_params[7],
                                                 selected_language=received_params[12],
                                                 wait_request = wait_request,
                                                 main_root= root,
                                                 )
                        
                        save_task_thread = threading.Thread(target= call_long_task)
                        save_task_thread.start()

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

if not open_image_only:
    initial_path = Tools.get_init_path()
    print("init path: ",initial_path)
    app_icon = Tools.resource_path('images/logo_TRIMAZKON.ico')
    app_licence_validity = Tools.check_licence()
    load_gui=True

    print("SYSTEM: ",sys.argv)
    if len(sys.argv) > 1 and not global_licence_load_error:
        if sys.argv[1] == "deleting":
            del_thread = threading.Thread(target=Tools.deleting_via_cmd,name="Deleting_thread")
            del_thread.start()
            load_gui = False

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

        elif sys.argv[1] == "settings_tray" or sys.argv[1] == "settings_tray_del" or sys.argv[1] == "admin_menu":
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
                else:
                    pipeline_duplex_instance.call_checking(f"Establish main menu gui",[])
            else:
                pipeline_duplex_instance.call_checking(f"Establish main menu gui",[])# předání parametrů pipeline komunikací PUKUD NEJSOU NA VSTUPU ZADNE SYSTEMOVE PARAMETRY, SPOUSTENO PRES ZÁSTUPCE

elif open_image_only: # snaha o co nejrichlejsi odeslani parametrů na server
    pipeline_duplex_instance = system_pipeline_communication(exe_name,no_server=True) # pokud už je aplikace spuštěná nezapínej server, trvá to...
    raw_path = str(sys.argv[1])
    IB_as_def_browser_path=initial_tools.path_check(raw_path,True)
    IB_as_def_browser_path_splitted = IB_as_def_browser_path.split("/")
    IB_as_def_browser_path = ""
    for i in range(0,len(IB_as_def_browser_path_splitted)-2):
        IB_as_def_browser_path += IB_as_def_browser_path_splitted[i]+"/"
    selected_image = IB_as_def_browser_path_splitted[len(IB_as_def_browser_path_splitted)-2]
    pipeline_duplex_instance.call_checking(f"Open image browser starting with image: {IB_as_def_browser_path}, {selected_image}",[IB_as_def_browser_path,selected_image])

if not open_image_only:

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
            self.TS_tray_taskname = "TRIMAZKON_startup_tray_setup"
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
            
        def call_sorting_option(self):
            self.clear_frames()
            self.root.unbind("<f>")
            Sorting_option(self.root)

        def call_view_option(self,path_given = None,selected_image = ""):
            self.clear_frames()
            self.root.unbind("<f>")
            self.IB_class = Image_browser(self.root,path_given,selected_image)
            self.ib_running = True

        def call_ip_manager(self):
            self.clear_frames()
            self.root.unbind("<f>")
            IP_manager(self.root)
        
        def call_catalogue_maker(self):
            self.clear_frames()
            self.root.unbind("<f>")
            Catalogue_maker(self.root)

        def call_advanced_option(self,success_message = None):
            self.clear_frames()
            self.root.unbind("<f>")
            Advanced_option(self.root,tray_setting_status_message=success_message)

        def fill_changelog(self,change_log):
            # Iterate through each <string> element and print its text
            for string_element in string_database.change_log_list:
                change_log.insert("current lineend",string_element + "\n")
            change_log.see(tk.END)

        def command_landed(self,params):
            """
            tato funkce přijímá příkazy z pipeline serveru
            """
            print("received in menu: ",params)
            print("Image browser running status: ",self.ib_running)
            if self.ib_running == False:
                for widget in self.root.winfo_children():
                    widget.destroy()
                self.root.unbind("<Button-1>")
                self.call_view_option(params[1],params[2])
            else:
                print("previous path: ",self.IB_class.image_browser_path)
                print("previous path: ",self.IB_class.IB_as_def_browser_path)
                print("previous image: ",self.IB_class.selected_image)
                print("new path: ",params[1])
                print("new image: ",params[2])

                for widget in self.root.winfo_children():
                    widget.destroy()
                self.root.unbind("<Button-1>")
                self.call_view_option(params[1],params[2])

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
            logo = customtkinter.CTkImage(Image.open(Tools.resource_path("images/logo.png")),size=(1200, 100))
            image_logo = customtkinter.CTkLabel(master = frame_with_logo,text = "",image =logo)
            menu_upper_frame = customtkinter.CTkFrame(master=self.root,corner_radius=0,fg_color="#212121")
            frame_with_buttons_right = customtkinter.CTkFrame(master=menu_upper_frame,corner_radius=0)
            frame_with_buttons = customtkinter.CTkFrame(master=menu_upper_frame,corner_radius=0)
            frame_with_logo.pack(pady=0,padx=0,fill="both",expand=False,side = "top")
            image_logo.pack()
            IB_as_def_browser_path = None
            
            manage_images =         customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Obrázky (správa)", command = lambda: self.call_sorting_option(),font=("Arial",25,"bold"))
            viewer_button =         customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Prohlížeč obrázků", command = lambda: self.call_view_option(),font=("Arial",25,"bold"))
            ip_setting_button =     customtkinter.CTkButton(master= frame_with_buttons, width= 400,height=100, text = "IP setting", command = lambda: self.call_ip_manager(),font=("Arial",25,"bold"))
            catalogue_button =      customtkinter.CTkButton(master= frame_with_buttons, width= 400,height=100, text = "Katalog", command = lambda: self.call_catalogue_maker(),font=("Arial",25,"bold"))
            advanced_button =       customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Nastavení", command = lambda: self.call_advanced_option(),font=("Arial",25,"bold"))
            change_log_label =      customtkinter.CTkLabel(master=frame_with_buttons_right, width= 600,height=50,font=("Arial",24,"bold"),text="Seznam posledně provedených změn: ")
            change_log =            customtkinter.CTkTextbox(master=frame_with_buttons_right, width= 600,height=550,fg_color="#212121",font=("Arial",20),border_color="#636363",border_width=3,corner_radius=0)
            resources_load_error =  customtkinter.CTkLabel(master=frame_with_buttons_right, width= 600,height=50,font=("Arial",24,"bold"),text="Nepodařilo se načíst konfigurační soubor (config_TRIMAZKON.xlsx)",text_color="red")
            manage_images.          pack(pady =(105,0), padx=20,side="top",anchor="e")
            viewer_button.          pack(pady = (10,0), padx=20,side="top",anchor="e")
            ip_setting_button.      pack(pady = (10,0), padx=20,side="top",anchor="e")
            catalogue_button.       pack(pady = (10,0), padx=20,side="top",anchor="e")
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
                manage_images.configure(state="disabled")
                viewer_button.configure(state="disabled")
                ip_setting_button.configure(state="disabled")
                catalogue_button.configure(state="disabled")
                advanced_button.configure(state="disabled")
                if app_licence_validity == "verification error":
                    licence_info_status.configure(text="chyba ověření")
                elif "EXPIRED:" in str(app_licence_validity):
                    licence_info_status.configure(text=app_licence_validity.replace("EXPIRED:","platnost vypršela:"))
                insert_licence_btn = customtkinter.CTkButton(master = licence_info_frame, width = 200,height=40, text = "Vložit licenci", command = lambda: os.startfile(initial_path),font=("Arial",24,"bold"))
                trial_btn = customtkinter.CTkButton(master = licence_info_frame,height=40, text = "Aktivovat trial verzi (30 dní)", command = lambda: Tools.store_installation_date(refresh_callback = self.check_licence),font=("Arial",24,"bold"))
                refresh_licence_btn = customtkinter.CTkButton(master = licence_info_frame, width = 40,height=40, text = "🔄", command = lambda: self.check_licence(),font=(None,24))
                insert_licence_btn.pack(pady =(7,5),padx=(15,0),side="left",anchor="w")
                trial_btn.pack(pady =(7,5),padx=(5,0),side="left",anchor="w")
                refresh_licence_btn.pack(pady =(7,5),padx=(5,0),side="left",anchor="w")
                self.root.after(500, lambda: Subwindows.licence_window())
            else:
                if "Trial active" in str(app_licence_validity):
                    validity_string = str(app_licence_validity)
                    validity_string = validity_string.replace("Trial active.","Trial verze platná:")
                    validity_string = validity_string.replace("days remaining.","dní")
                    licence_info_status.configure(text=f"{validity_string}")
                else:
                    licence_info_status.configure(text=f"platná do {app_licence_validity}")

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

                elif sys.argv[1] != "admin_menu" and sys.argv[1] != "trigger_by_tray" and sys.argv[1] != "installer_call": # pokud se nerovnají jedná se nejspíše o volání základního prohlížeče obrázků (spuštění kliknutím na obrázek...)
                    IB_as_def_browser_path=Tools.path_check(raw_path,True)
                    IB_as_def_browser_path_splitted = IB_as_def_browser_path.split("/")
                    IB_as_def_browser_path = ""
                    for i in range(0,len(IB_as_def_browser_path_splitted)-2):
                        IB_as_def_browser_path += IB_as_def_browser_path_splitted[i]+"/"
                    root.update()
                    self.root.update()
                    selected_image = IB_as_def_browser_path_splitted[len(IB_as_def_browser_path_splitted)-2]
                    self.call_view_option(IB_as_def_browser_path,selected_image)
            
            if self.run_as_admin and not global_licence_load_error:
                self.root.after(1000, lambda: Subwindows.call_again_as_admin("admin_menu","Upozornění","Aplikace vyžaduje práva pro nastavení aut. spouštění na pozadí\n     - možné změnit v nastavení\n\nPřejete si znovu spustit aplikaci, jako administrátor?"))
            try:
                root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())
                # self.root.mainloop()
            except Exception as e:
                print("already looped? ",e)
            # self.root.mainloop()

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
            
        def call_menu(self): # Tlačítko menu (konec, návrat do menu)
            """
            Funkce čistí všechny zaplněné rámečky a funguje, jako tlačítko zpět do menu
            """
            #kdyby probihala sekvence obrazku:
            if self.state == "running":
                self.stop()

            list_of_frames = [self.main_frame,self.frame_with_path,self.frame_with_console,self.frame_with_buttons,self.background_frame,self.image_film_frame_center,self.image_film_frame_right,self.image_film_frame_left]
            for frames in list_of_frames:
                frames.pack_forget()
                frames.grid_forget()
                frames.destroy()

            for keys in self.unbind_list:
                self.root.unbind(keys)
            
            if os.path.exists(self.default_path + self.temp_bmp_folder):
                shutil.rmtree(self.default_path + self.temp_bmp_folder) # vycistit
            menu.menu()
        
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
                            # self.default_path = Tools.path_check(path)
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
            
            def corrupted_image_handling(error_message = None):
                with Image.open(Tools.resource_path("images/loading3.png")) as opened_image:
                    rotated_image = opened_image.rotate(180,expand=True)
                    width,height = rotated_image.size
                    # width,height = 800, 800

                if error_message != None:
                    self.main_frame.delete("error_message")
                    self.main_frame.create_text(
                        800,  # x coordinate
                        400,  # y coordinate
                        text=error_message,      # the text to show
                        fill="orange",    # same color as your cursor
                        font=("Arial", 30),         # font and size
                        tags="error_message"              # same tag, so it can be deleted with others
                    )

                return (rotated_image, width, height)

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
                            error_image, width, height = corrupted_image_handling()
                            return error_image

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
                    self.main_frame.delete("error_message")

                except Exception as e:
                    error_message = f"Obrázek:\n{image_to_show}\nje poškozený"
                    print(error_message)
                    if not in_new_window:
                        rotated_image, width, height = corrupted_image_handling(error_message)
                        # return error_message

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
                Advanced_option(self.root,windowed=True,spec_location="image_browser", path_to_remember = path_to_send,last_params = [self.last_coords,self.zoom_slider.get()])
            
            def call_path_context_menu(event):
                def insert_path(path):
                    if self.path_set.get() == path:
                        return
                    self.path_set.delete("0","200")
                    self.path_set.insert("0", path)
                    self.selected_image = "" #muze byt vlozet z otevreni pres obrazek kdyz oteviram jinou cestu přes historii musim init
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
            menu_button.                    pack(pady = (5,0),padx =(5,0),side="left",anchor = "w")
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
                Tools.add_colored_line(self.console,"TRIMAZKON, jako výchozí prohlížeč!","white",None,True)
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
            default_dir_names = string_database.default_setting_database_param
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
                remove_task_success = Tools.remove_task_from_TS("TRIMAZKON_startup_tray_setup")
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
            if self.spec_location == "image_browser":
                Image_browser(root=self.root,path_given=self.path_to_remember,params_given=self.ib_last_params)
            elif self.spec_location == "converting_option":
                Converting_option(self.root)
            elif self.spec_location == "deleting_option":
                Deleting_option(self.root)
            elif self.spec_location == "sorting_option":
                Sorting_option(self.root)

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

            def set_default_cutoff_date():
                input_month = set_month.get()
                if input_month != "":
                    if input_month.isdigit():
                        if int(input_month) < 13 and int(input_month) > 0:
                            cutoff_date[1] = int(input_month)
                            max_days_in_month = Deleting.calc_days_in_month(int(cutoff_date[1]))
                            if int(cutoff_date[0]) > max_days_in_month:
                                cutoff_date[0] = str(max_days_in_month)
                            main_console.configure(text="")
                            main_console.configure(text="Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2]),text_color="green")
                        else:
                            main_console.configure(text="")
                            main_console.configure(text="Měsíc: " + str(input_month) + " je mimo rozsah",text_color="red")
                    else:
                        main_console.configure(text="")
                        main_console.configure(text="U nastavení měsíce jste nezadali číslo",text_color="red")

                input_day = set_day.get()
                max_days_in_month = Deleting.calc_days_in_month(int(cutoff_date[1]))

                if input_day != "":
                    if input_day.isdigit():
                        if int(input_day) <= int(max_days_in_month) and int(input_day) > 0:
                            cutoff_date[0] = int(input_day)
                            main_console.configure(text="")
                            main_console.configure(text="Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2]),text_color="green")
                        else:
                            main_console.configure(text="")
                            main_console.configure(text="Den: " + str(input_day) + " je mimo rozsah",text_color="red")
                    else:
                        main_console.configure(text="")
                        main_console.configure(text="U nastavení dne jste nezadali číslo",text_color="red")

                input_year = set_year.get()
                if input_year != "":
                    if input_year.isdigit():
                        if len(str(input_year)) == 2:
                            cutoff_date[2] = int(input_year) + 2000
                            main_console.configure(text="")
                            main_console.configure(text="Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2]),text_color="green")
                        elif len(str(input_year)) == 4:
                            cutoff_date[2] = int(input_year)
                            main_console.configure(text="")
                            main_console.configure(text="Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2]),text_color="green")
                        else:
                            main_console.configure(text="")
                            main_console.configure(text="Rok: " + str(input_year) + " je mimo rozsah",text_color="red")
                    else:
                        main_console.configure(text="")
                        main_console.configure(text="U nastavení roku jste nezadali číslo",text_color="red")

                Tools.save_to_json_config(cutoff_date,"del_settings","default_cutoff_date")
                self.setting_widgets(False, main_console._text,main_console._text_color,submenu_option="set_default_parametres")

            def set_files_to_keep():
                nonlocal main_console
                input_files_to_keep = files_to_keep_set.get()
                if input_files_to_keep.isdigit():
                    if int(input_files_to_keep) >= 0:
                        files_to_keep = int(input_files_to_keep)
                        Tools.save_to_json_config(files_to_keep,"del_settings","default_files_to_keep")
                        main_console.configure(text="")
                        main_console.configure(text="Základní počet ponechaných starších souborů nastaven na: " + str(files_to_keep),text_color="green")
                        console_files_to_keep.configure(text = "Aktuálně nastavené minimum: "+str(files_to_keep),text_color="white")
                    else:
                        main_console.configure(text="")
                        main_console.configure(text="Mimo rozsah",text_color="red")
                else:
                    main_console.configure(text="")
                    main_console.configure(text="Nazadali jste číslo",text_color="red")

                self.setting_widgets(False,main_console._text,main_console._text_color,submenu_option="set_default_parametres")

            def insert_current_date():
                today = Deleting.get_current_date()
                today_split = today[1].split(".")
                i=0
                for items in today_split:
                    i+=1
                    cutoff_date[i-1]=items
                main_console.configure(text="")
                main_console.configure(text="Bylo vloženo dnešní datum (Momentálně všechny soubory vyhodnoceny, jako starší!)",text_color="orange")
                self.setting_widgets(cutoff_date,main_console._text,main_console._text_color,submenu_option="set_default_parametres")

            def set_new_default_prefix(which_folder):
                report = ""
                inserted_prefix = str(set_new_def_prefix.get()).replace(" ","")
                if len(inserted_prefix) != 0:
                    if inserted_prefix != str(default_prefix_cam) and inserted_prefix != str(default_prefix_func):
                        if which_folder == "cam":
                            report = Tools.save_to_json_config(inserted_prefix,"sort_conv_settings","prefix_camera")
                            self.default_displayed_prefix_dir = "cam"
                        if which_folder == "func":
                            report = Tools.save_to_json_config(inserted_prefix,"sort_conv_settings","prefix_function")
                            self.default_displayed_prefix_dir = "func"
                        main_console.configure(text="")
                        main_console.configure(text=report,text_color="green")
                        self.setting_widgets(False,main_console._text,main_console._text_color,submenu_option="set_folder_names") # refresh
                    else:
                        main_console.configure(text="")
                        main_console.configure(text = "Zadané jméno je již zabrané",text_color="red")
                else:
                    main_console.configure(text="")
                    main_console.configure(text = "Nutný alespoň jeden znak",text_color="red")
                    
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

            def set_new_default_dir_name():
                inserted_new_name = str(set_new_def_folder_name.get()).replace(" ","")
                report = ["Základní název složky pro nepáry (soubory nezastoupenými všemi nalezenými formáty) změněn na: ",
                        "Základní název složky pro nalezené dvojice změněn na: ",
                        "Základní název složky se soubory, které jsou určené ke smazání změněn na: ",
                        "Základní název složky pro soubory převedené do .bmp formátu změněn na: ",
                        "Základní název složky pro soubory převedené do .jpg formátu změněn na: ",
                        "Základní název složky pro zkopírované obrázky z prohlížeče obrázků změněn na: ",
                        "Základní název složky pro přesunuté obrázky z prohlížeče obrázků změněn na: "]
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
                                if i == 0:
                                    Tools.save_to_json_config(inserted_new_name,"sort_conv_settings","temp_dir_name")
                                elif i == 1:
                                    Tools.save_to_json_config(inserted_new_name,"sort_conv_settings","pairs_dir_name")
                                elif i == 2:
                                    Tools.save_to_json_config(inserted_new_name,"del_settings","to_delete_dir_name")
                                elif i == 3:
                                    Tools.save_to_json_config(inserted_new_name,"sort_conv_settings","convert_bmp_dir_name")
                                elif i == 4:
                                    Tools.save_to_json_config(inserted_new_name,"sort_conv_settings","convert_jpg_dir_name")
                                elif i == 5:
                                    Tools.save_to_json_config(inserted_new_name,"image_browser_settings","copyed_dir_name")
                                elif i == 6:
                                    Tools.save_to_json_config(inserted_new_name,"image_browser_settings","moved_dir_name")

                                self.default_displayed_static_dir = i
                                neme_list_without_suffix = inserted_new_name.replace(str(self.default_dir_names[i]),"")
                                main_console.configure(text="")
                                main_console.configure(text=report[i]+neme_list_without_suffix,text_color="green")
                                self.setting_widgets(False,main_console._text,main_console._text_color,submenu_option="set_folder_names") # refresh
                    else:
                        main_console.configure(text="")
                        main_console.configure(text = "Zadané jméno je již zabrané",text_color="red")
                else:
                    main_console.configure(text="")
                    main_console.configure(text = "Nutný alespoň jeden znak",text_color="red")
                    
            def change_static_dir(*args):
                for i in range(0,len(self.drop_down_static_dir_names_list)):
                    if str(self.drop_down_static_dir_names_list[i]) == str(*args):
                        neme_list_without_suffix = str(self.drop_down_static_dir_names_list[i]).replace(str(self.default_dir_names[i]),"")
                        set_new_def_folder_name.configure(placeholder_text = neme_list_without_suffix)
                        set_new_def_folder_name.delete("0","100")
                        set_new_def_folder_name.insert("0", neme_list_without_suffix)
            
            def add_format(which_operation):
                if which_operation == 0:
                    new_format = str(formats_set.get())
                    if new_format !="":
                        main_console_text_add = Tools.save_to_json_config(new_format,"sort_conv_settings","add_supported_sorting_formats")
                        main_console.configure(text="")
                        main_console.configure(text=main_console_text_add,text_color="white")
                        
                if which_operation == 1:
                    new_format = str(formats_deleting_input.get())
                    if new_format !="":
                        main_console_text_add = Tools.save_to_json_config(new_format,"del_settings","add_supported_deleting_formats")
                        main_console.configure(text="")
                        main_console.configure(text=main_console_text_add,text_color="white")
                self.setting_widgets(False,main_console._text,main_console._text_color,submenu_option="set_supported_formats")

            def pop_format(which_operation):
                if which_operation == 0:
                    format_to_delete = str(formats_set.get())
                    if format_to_delete !="":
                        main_console_text_pop = Tools.save_to_json_config(format_to_delete,"sort_conv_settings","pop_supported_sorting_formats")
                        main_console.configure(text="")
                        main_console.configure(text=main_console_text_pop,text_color="white")
                if which_operation == 1:
                    format_to_delete = str(formats_deleting_input.get())
                    if format_to_delete !="":
                        main_console_text_pop = Tools.save_to_json_config(format_to_delete,"del_settings","pop_supported_deleting_formats")
                        main_console.configure(text="")
                        main_console.configure(text=main_console_text_pop,text_color="white")

                self.setting_widgets(False,main_console._text,main_console._text_color,submenu_option="set_supported_formats")

            def set_max_num_of_pallets():
                nonlocal main_console
                input_1 = set_max_pallets.get()
                if input_1.isdigit() == False:
                    main_console.configure(text="")
                    main_console.configure(text = "Nezadali jste číslo",text_color="red")
                elif int(input_1) <1:
                    main_console.configure(text="")
                    main_console.configure(text = "Mimo rozsah",text_color="red")
                else:
                    main_console.configure(text="")
                    main_console.configure(text = f"Počet palet nastaven na: {input_1}",text_color="green")
                    Tools.save_to_json_config(input_1,"sort_conv_settings","max_pallets")
            
            def update_zoom_increment_slider(*args):
                if config_data["image_browser_settings"]["zoom_step"] != int(*args):
                    label_IB4.configure(text = str(int(*args)) + " %")
                    config_data["image_browser_settings"]["zoom_step"] = int(*args)

            def update_drag_movement_slider(*args):
                if config_data["image_browser_settings"]["movement_step"] != int(*args):
                    label_IB6.configure(text = str(int(*args)) + " px")
                    config_data["image_browser_settings"]["movement_step"] = int(*args)

            def on_off_image_film():
                if switch_image_film.get() == 1:
                    Tools.save_to_json_config("ano","image_browser_settings","show_image_film")
                    config_data["image_browser_settings"]["show_image_film"] = "ano"
                else:
                    Tools.save_to_json_config("ne","image_browser_settings","show_image_film")
                    config_data["image_browser_settings"]["show_image_film"] = "ne"

            def change_image_film_number(*args):
                input_number = int(*args)
                num_of_image_film_images.configure(text = str(input_number) + " obrázků na každé straně")

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
                first_option_frame =        customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
                self.checkbox_maximalized = customtkinter.CTkCheckBox(master = first_option_frame,height=40,text = "Spouštět v maximalizovaném okně",command = lambda: self.maximalized(),font=("Arial",22,"bold"))
                first_option_frame.         pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")

                tray_option_frame =         customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
                self.tray_checkbox =        customtkinter.CTkCheckBox(master = tray_option_frame,height=40,text = "Spouštět TRIMAZKON na pozadí (v systémové nabídce \"tray_icons\") při zapnutí systému Windows?",command = lambda: self.tray_startup_setup(main_console),font=("Arial",22,"bold"))
                tray_option_frame.          pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")

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
                self.path_set =             customtkinter.CTkEntry(     master = second_option_frame,width=845,height=40,font=("Arial",20),placeholder_text="")
                button_save5 =              customtkinter.CTkButton(    master = second_option_frame,width=100,height=40, text = "Uložit", command = lambda: save_path(),font=("Arial",22,"bold"))
                button_explorer =           customtkinter.CTkButton(    master = second_option_frame,width=40,height=40, text = "...", command = lambda: call_browseDirectories(),font=("Arial",22,"bold"))

                del_history_label =         customtkinter.CTkLabel(master = second_option_frame,height=40,text = "Mazání historie cest pro jednotlivé možnosti:",justify = "left",font=("Arial",22,"bold"))
                context_menu_button2  =     customtkinter.CTkButton(master = second_option_frame, width = 100,height=40, text = "Náhled",font=("Arial",20,"bold"),corner_radius=0)
                drop_down_options =         customtkinter.CTkOptionMenu(master = second_option_frame,width=350,height=40,values=path_history_options,font=("Arial",20),corner_radius=0)
                del_path_history =          customtkinter.CTkButton(master = second_option_frame,height=40, text = "Smazat historii", command = lambda: call_delete_path_history(),font=("Arial",22,"bold"),corner_radius=0)

                default_path_insert_console=customtkinter.CTkLabel(     master = second_option_frame,height=40,text ="",justify = "left",font=("Arial",22),text_color="white")
                console_frame =             customtkinter.CTkFrame(     master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1,fg_color="black")
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
                second_option_frame.        pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
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

            if submenu_option == "set_folder_names":
                self.option_buttons[1].configure(fg_color="#212121")
                #upravovani prefixu slozek, default: pro trideni podle kamer
                first_option_frame =            customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
                first_option_frame.             pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
                label_folder_prefixes           = customtkinter.CTkLabel(master = first_option_frame,height=40,text = "1. Vyberte prefix složky, u které chcete změnit základní název:",justify = "left",font=("Arial",22,"bold"))
                drop_down_dir_names             = customtkinter.CTkOptionMenu(master = first_option_frame,width=290,height=40,values=self.drop_down_prefix_dir_names_list,font=("Arial",20),command= change_prefix_dir)
                set_new_def_prefix              = customtkinter.CTkEntry(master = first_option_frame,width=200,height=40,font=("Arial",20), placeholder_text= str(default_prefix_cam))
                button_save_new_def_prefix      = customtkinter.CTkButton(master = first_option_frame,width=100,height=40, text = "Uložit", command = lambda: set_new_default_prefix("cam"),font=("Arial",22,"bold"))
                label_folder_prefixes.          grid(column =0,row=row_index+1,sticky = tk.W,pady =10,padx=10)
                set_new_def_prefix.             grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
                button_save_new_def_prefix.     grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=215)
                drop_down_dir_names.            grid(column =0,row=row_index+3,sticky = tk.W,pady =5,padx=10)

                set_new_def_prefix.insert("0", str(default_prefix_cam))
                def prefix_enter_btn(e):
                    if str(drop_down_dir_names.get()) == str(self.drop_down_prefix_dir_names_list[0]):
                        set_new_default_prefix("cam")
                    elif str(drop_down_dir_names.get()) == str(self.drop_down_prefix_dir_names_list[1]):
                        set_new_default_prefix("func")
                    self.current_root.focus_set()
                set_new_def_prefix.bind("<Return>",prefix_enter_btn)
                #nastaveni defaultniho vyberu z drop-down menu
                if self.default_displayed_prefix_dir == "cam":
                    change_prefix_dir(self.drop_down_prefix_dir_names_list[0])
                    drop_down_dir_names.set(self.drop_down_prefix_dir_names_list[0])
                elif self.default_displayed_prefix_dir == "func":
                    change_prefix_dir(self.drop_down_prefix_dir_names_list[1])
                    drop_down_dir_names.set(self.drop_down_prefix_dir_names_list[1])
                
                #widgets na nastaveni jmen statickych slozek
                second_option_frame =           customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
                second_option_frame.            pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
                label_folder_name_change        = customtkinter.CTkLabel(master = second_option_frame,height=40,text = "2. Vyberte složku, u které chcete změnit základní název",justify = "left",font=("Arial",22,"bold"))
                set_new_def_folder_name         = customtkinter.CTkEntry(master = second_option_frame,width=200,height=40,font=("Arial",20), placeholder_text= str(default_prefix_func))
                button_save_new_name            = customtkinter.CTkButton(master = second_option_frame,width=100,height=40, text = "Uložit", command = lambda: set_new_default_dir_name(),font=("Arial",22,"bold"))
                drop_down_static_dir_names      = customtkinter.CTkOptionMenu(master = second_option_frame,width=290,height=40,values=self.drop_down_static_dir_names_list,font=("Arial",20),command= change_static_dir)
                console_frame                   = customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1,fg_color="black")
                console_frame.                  pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
                main_console                    = customtkinter.CTkLabel(master = console_frame,height=20,text = str(main_console_text),text_color=str(main_console_text_color),justify = "left",font=("Arial",22))
                if self.windowed:
                    save_frame =                customtkinter.CTkFrame(     master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
                    save_frame.                 pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top",anchor = "e")
                    save_changes_button =           customtkinter.CTkButton(master = save_frame,width=150,height=40, text = "Aplikovat/ načíst změny", command = lambda: self.refresh_main_window(),font=("Arial",22,"bold"))
                label_folder_name_change.       grid(column =0,row=row_index+4,sticky = tk.W,pady =10,padx=10)
                set_new_def_folder_name.        grid(column =0,row=row_index+5,sticky = tk.W,pady =0,padx=10)
                button_save_new_name.           grid(column =0,row=row_index+5,sticky = tk.W,pady =0,padx=215)
                drop_down_static_dir_names.     grid(column =0,row=row_index+6,sticky = tk.W,pady =5,padx=10)
                main_console.                   grid(column =0,row=row_index+7,sticky = tk.W,pady =10,padx=10)
                if self.windowed:
                    save_changes_button.        pack(pady =5,padx=10,anchor = "e")

                drop_down_increment = self.default_displayed_static_dir
                corrected_default_input = str(self.drop_down_static_dir_names_list[drop_down_increment]).replace(str(self.default_dir_names[drop_down_increment]),"")
                set_new_def_folder_name.insert("0", corrected_default_input)
                def static_dir_enter_btn(e):
                    set_new_default_dir_name()
                    self.current_root.focus_set()
                set_new_def_folder_name.bind("<Return>",static_dir_enter_btn)
                #nastaveni defaultniho vyberu z drop-down menu
                drop_down_static_dir_names.set(self.drop_down_static_dir_names_list[drop_down_increment])

            if submenu_option == "set_default_parametres":
                self.option_buttons[2].configure(fg_color="#212121")
                #widgets na nastaveni zakladniho poctu palet v obehu
                first_option_frame =                customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
                first_option_frame.                 pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
                label_pallets =                     customtkinter.CTkLabel(master = first_option_frame,height=50,text = "1. Nastavte základní maximální počet paletek v oběhu:",justify = "left",font=("Arial",22,"bold"))
                set_max_pallets =                   customtkinter.CTkEntry(master = first_option_frame,width=100,height=50,font=("Arial",20), placeholder_text= str(default_max_num_of_pallets))
                button_save_max_num_of_pallets =    customtkinter.CTkButton(master = first_option_frame,width=100,height=50, text = "Uložit", command = lambda: set_max_num_of_pallets(),font=("Arial",22,"bold"))
                label_pallets.                      grid(column =0,row=row_index+1,sticky = tk.W,pady =10,padx=10)
                set_max_pallets.                    grid(column =0,row=row_index+2,sticky = tk.W,pady =(0,10),padx=10)
                button_save_max_num_of_pallets.     grid(column =0,row=row_index+2,sticky = tk.W,pady =(0,10),padx=115)
                def new_max_pallets_enter_btn(e):
                    set_max_num_of_pallets()
                    self.current_root.focus_set()
                set_max_pallets.bind("<Return>",new_max_pallets_enter_btn)

                #widgets na nastaveni zakladniho poctu files_to_keep
                files_to_keep_console_text ="Aktuálně nastavené minimum: "+str(files_to_keep)
                second_option_frame =                customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
                second_option_frame.                 pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
                label_files_to_keep =               customtkinter.CTkLabel(master = second_option_frame,height=50,text = "2. Nastavte základní počet ponechaných souborů, vyhodnocených jako starších:",justify = "left",font=("Arial",22,"bold"))
                files_to_keep_set =                 customtkinter.CTkEntry(master = second_option_frame,width=100,height=50,font=("Arial",20), placeholder_text= files_to_keep)
                button_save2 =                      customtkinter.CTkButton(master = second_option_frame,width=100,height=50, text = "Uložit", command = lambda: set_files_to_keep(),font=("Arial",22,"bold"))
                console_files_to_keep=              customtkinter.CTkLabel(master = second_option_frame,height=50,text =files_to_keep_console_text,justify = "left",font=("Arial",22))
                label_files_to_keep.                grid(column =0,row=row_index+3,sticky = tk.W,pady =10,padx=10)
                files_to_keep_set.                  grid(column =0,row=row_index+4,sticky = tk.W,pady =0,padx=10)
                button_save2.                       grid(column =0,row=row_index+4,sticky = tk.W,pady =0,padx=115)
                console_files_to_keep.              grid(column =0,row=row_index+5,sticky = tk.W,pady =(0,10),padx=10)
                def files_to_keep_enter_btn(e):
                    set_files_to_keep()
                    self.current_root.focus_set()
                files_to_keep_set.bind("<Return>",files_to_keep_enter_btn)
                
                #widgets na nastaveni zakladniho dne
                third_option_frame =                customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
                third_option_frame.                 pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
                label_set_default_date =            customtkinter.CTkLabel(master = third_option_frame,height=50,text = "3. Nastavte základní datum pro vyhodnocení souborů, jako starších:",justify = "left",font=("Arial",22,"bold"))
                set_day =                           customtkinter.CTkEntry(master = third_option_frame,width=40,height=50,font=("Arial",20), placeholder_text= cutoff_date[0])
                sep1 =                              customtkinter.CTkLabel(master = third_option_frame,height=50,width=10,text = ".",font=("Arial",22))
                set_month =                         customtkinter.CTkEntry(master = third_option_frame,width=40,height=50,font=("Arial",20), placeholder_text= cutoff_date[1])
                sep2 =                              customtkinter.CTkLabel(master = third_option_frame,height=50,width=10,text = ".",font=("Arial",22))
                set_year =                          customtkinter.CTkEntry(master = third_option_frame,width=60,height=50,font=("Arial",20), placeholder_text= cutoff_date[2])
                button_save_date =                  customtkinter.CTkButton(master = third_option_frame,width=100,height=50, text = "Uložit", command = lambda: set_default_cutoff_date(),font=("Arial",22,"bold"))
                insert_button =                     customtkinter.CTkButton(master = third_option_frame,width=285,height=50, text = "Vložit dnešní datum", command = lambda: insert_current_date(),font=("Arial",22,"bold"))
                console_frame =                     customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1,fg_color="black")
                console_frame.                      pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
                main_console =                      customtkinter.CTkLabel(master = console_frame,height=20,text = str(main_console_text),text_color=str(main_console_text_color),justify = "left",font=("Arial",22))
                if self.windowed:
                    save_frame =                    customtkinter.CTkFrame(     master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
                    save_frame.                     pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top",anchor = "e")
                    save_changes_button =               customtkinter.CTkButton(master = save_frame,width=150,height=40, text = "Aplikovat/ načíst změny", command = lambda: self.refresh_main_window(),font=("Arial",22,"bold"))
                label_set_default_date.             grid(column =0,row=row_index+6,sticky = tk.W,pady =10,padx=10)
                set_day.                            grid(column =0,row=row_index+7,sticky = tk.W,pady =0,padx=10)
                sep1.                               grid(column =0,row=row_index+7,sticky = tk.W,pady =0,padx=55)
                set_month.                          grid(column =0,row=row_index+7,sticky = tk.W,pady =0,padx=70)
                sep2.                               grid(column =0,row=row_index+7,sticky = tk.W,pady =0,padx=115)
                set_year.                           grid(column =0,row=row_index+7,sticky = tk.W,pady =0,padx=130)
                button_save_date.                   grid(column =0,row=row_index+7,sticky = tk.W,pady =0,padx=195)
                insert_button.                      grid(column =0,row=row_index+8,sticky = tk.W,pady =5,padx=10)
                main_console.                       grid(column =0,row=row_index+9,sticky = tk.W,pady =10,padx=10)
                if self.windowed:
                    save_changes_button.            pack(pady =5,padx=10,anchor = "e")

                def new_date_enter_btn(e):
                    set_default_cutoff_date()
                    self.current_root.focus_set()
                set_day.bind("<Return>",new_date_enter_btn)
                set_month.bind("<Return>",new_date_enter_btn)
                set_year.bind("<Return>",new_date_enter_btn)

            if submenu_option == "set_supported_formats":
                self.option_buttons[3].configure(fg_color="#212121")
                #widgets pro nastavovani podporovanych formatu
                supported_formats_deleting = "Aktuálně nastavené podporované formáty pro možnosti mazání: " + str(config_data["del_settings"]["supported_formats_deleting"])
                first_option_frame =                customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=20,corner_radius=0,border_width=1)
                first_option_frame.                 pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
                label_supported_formats_deleting =  customtkinter.CTkLabel(master = first_option_frame,height=50,text = "1. Nastavte podporované formáty pro možnosti: MAZÁNÍ:",justify = "left",font=("Arial",22,"bold"))
                formats_deleting_input =            customtkinter.CTkEntry(master = first_option_frame,height=50,font=("Arial",20),width=200)
                button_save4 =                      customtkinter.CTkButton(master = first_option_frame,width=50,height=50, text = "Uložit", command = lambda: add_format(1),font=("Arial",22,"bold"))
                button_pop2 =                       customtkinter.CTkButton(master = first_option_frame,width=70,height=50, text = "Odebrat", command = lambda: pop_format(1),font=("Arial",22,"bold"))
                console_bottom_frame_4=             customtkinter.CTkLabel(master = first_option_frame,height=50,text =supported_formats_deleting,justify = "left",font=("Arial",22))
                label_supported_formats_deleting.   grid(column =0,row=row_index+1,sticky = tk.W,pady =10,padx=10)
                formats_deleting_input.             grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
                button_save4.                       grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=215)
                button_pop2.                        grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=290)
                console_bottom_frame_4.             grid(column =0,row=row_index+3,sticky = tk.W,pady =0,padx=10)

                supported_formats_sorting = "Aktuálně nastavené podporované formáty pro možnosti třídění: " + str(config_data["sort_conv_settings"]["supported_formats_sorting"])
                second_option_frame =               customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=20,corner_radius=0,border_width=1)
                second_option_frame.                pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
                label3 =                            customtkinter.CTkLabel(master = second_option_frame,height=50,text = "2. Nastavte podporované formáty pro možnosti: TŘÍDĚNÍ:",justify = "left",font=("Arial",22,"bold"))
                formats_set =                       customtkinter.CTkEntry(master = second_option_frame,width=200,height=50,font=("Arial",20))
                button_save3 =                      customtkinter.CTkButton(master = second_option_frame,width=50,height=50, text = "Uložit", command = lambda: add_format(0),font=("Arial",22,"bold"))
                button_pop =                        customtkinter.CTkButton(master = second_option_frame,width=70,height=50, text = "Odebrat", command = lambda: pop_format(0),font=("Arial",22,"bold"))
                console_bottom_frame_3=             customtkinter.CTkLabel(master = second_option_frame,height=50,text =supported_formats_sorting,justify = "left",font=("Arial",22))
                console_frame =                     customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1,fg_color="black")
                console_frame.                      pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
                main_console =                      customtkinter.CTkLabel(master = console_frame,height=20,text = str(main_console_text),text_color=str(main_console_text_color),justify = "left",font=("Arial",22))
                if self.windowed:
                    save_frame =                    customtkinter.CTkFrame(     master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
                    save_frame.                     pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top",anchor = "e")
                    save_changes_button =               customtkinter.CTkButton(master = save_frame,width=150,height=40, text = "Aplikovat/ načíst změny", command = lambda: self.refresh_main_window(),font=("Arial",22,"bold"))
                label3.                             grid(column =0,row=row_index+4,sticky = tk.W,pady =10,padx=10)
                formats_set.                        grid(column =0,row=row_index+5,sticky = tk.W,pady =0,padx=10)
                button_save3.                       grid(column =0,row=row_index+5,sticky = tk.W,pady =0,padx=215)
                button_pop.                         grid(column =0,row=row_index+5,sticky = tk.W,pady =0,padx=290)
                console_bottom_frame_3.             grid(column =0,row=row_index+6,sticky = tk.W,pady =0,padx=10)
                main_console.                       grid(column =0,row=row_index+7,sticky = tk.W,pady =10,padx=10)
                if self.windowed:
                    save_changes_button.            pack(pady =5,padx=10,anchor = "e")

                def add_or_rem_formats(e):
                    self.current_root.focus_set()
                formats_deleting_input.bind("<Return>",add_or_rem_formats)
                formats_set.bind("<Return>",add_or_rem_formats)

            if submenu_option == "set_image_browser_setting":
                self.option_buttons[4].configure(fg_color="#212121")
                text_increment = str(config_data["image_browser_settings"]["zoom_step"]) + " %"
                text_movement = str(config_data["image_browser_settings"]["movement_step"]) + " px"
                text_image_film = str(config_data["image_browser_settings"]["image_film_count"]) + " obrázků na každé straně"
                second_option_frame =       customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=20,corner_radius=0,border_width=1)
                second_option_frame.        pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
                label_IB3 =                 customtkinter.CTkLabel(master = second_option_frame,height=20,text = "1. Nastavte o kolik procent se navýší přiblížení jedním krokem kolečka myši:",justify = "left",font=("Arial",22,"bold"))
                zoom_increment_set =        customtkinter.CTkSlider(master=second_option_frame,width=300,height=15,from_=5,to=100,number_of_steps= 19,command= update_zoom_increment_slider)
                label_IB4 =                 customtkinter.CTkLabel(master = second_option_frame,height=20,text = text_increment,justify = "left",font=("Arial",20))
                third_option_frame =        customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=20,corner_radius=0,border_width=1)
                third_option_frame.         pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
                label_IB5 =                 customtkinter.CTkLabel(master = third_option_frame,height=20,text = "2. Nastavte velikost kroku při posouvání levým tlačítkem myši:",justify = "left",font=("Arial",22,"bold"))
                zoom_movement_set =         customtkinter.CTkSlider(master=third_option_frame,width=300,height=15,from_=10,to=100,number_of_steps= 18,command= update_drag_movement_slider)
                label_IB6 =                 customtkinter.CTkLabel(master = third_option_frame,height=20,text = text_movement,justify = "left",font=("Arial",20))
                forth_option_frame =        customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=20,corner_radius=0,border_width=1)
                forth_option_frame.         pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
                label_image_film =          customtkinter.CTkLabel(master = forth_option_frame,height=20,text = "3. Upravte nastavení filmu obrázků:",justify = "left",font=("Arial",22,"bold"))
                switch_image_film =         customtkinter.CTkCheckBox(master = forth_option_frame, text = "Zapnuto",command = lambda: on_off_image_film(),font=("Arial",20))
                num_of_image_film_images_slider = customtkinter.CTkSlider(master=forth_option_frame,width=300,height=15,from_=1,to=15,command= change_image_film_number)
                num_of_image_film_images =  customtkinter.CTkLabel(master = forth_option_frame,height=20,text = text_image_film,justify = "left",font=("Arial",20))
                console_frame =             customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1,fg_color="black")
                console_frame.              pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
                main_console =              customtkinter.CTkLabel(master = console_frame,height=20,text = str(main_console_text),text_color=str(main_console_text_color),justify = "left",font=("Arial",22))
                if self.windowed:
                    save_frame =            customtkinter.CTkFrame(     master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
                    save_frame.             pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top",anchor = "e")
                    save_changes_button =   customtkinter.CTkButton(master = save_frame,width=150,height=40, text = "Aplikovat/ načíst změny", command = lambda: self.refresh_main_window(),font=("Arial",22,"bold"))
                label_IB3.                  grid(column =0,row=row_index+6,sticky = tk.W,pady =10,padx=10)
                zoom_increment_set.         grid(column =0,row=row_index+7,sticky = tk.W,pady =(10,20),padx=10)
                label_IB4.                  grid(column =0,row=row_index+7,sticky = tk.W,pady =(10,20),padx=320)
                label_IB5.                  grid(column =0,row=row_index+8,sticky = tk.W,pady =10,padx=10)
                zoom_movement_set.          grid(column =0,row=row_index+9,sticky = tk.W,pady =(10,20),padx=10)
                label_IB6.                  grid(column =0,row=row_index+9,sticky = tk.W,pady =(10,20),padx=320)
                label_image_film.           grid(column =0,row=row_index+10,sticky = tk.W,pady =10,padx=10)
                switch_image_film.          grid(column =0,row=row_index+11,sticky = tk.W,pady =0,padx=10)
                num_of_image_film_images_slider.grid(column =0,row=row_index+12,sticky = tk.W,pady =(10,20),padx=10)
                num_of_image_film_images.   grid(column =0,row=row_index+12,sticky = tk.W,pady =(10,20),padx=320)
                main_console.               grid(column =0,row=row_index+13,sticky = tk.W,pady =10,padx=10)
                if self.windowed:
                    save_changes_button.    pack(pady =5,padx=10,anchor = "e")

                zoom_increment_set.set(config_data["image_browser_settings"]["zoom_step"])
                zoom_movement_set.set(config_data["image_browser_settings"]["movement_step"])
                num_of_image_film_images_slider.set(config_data["image_browser_settings"]["image_film_count"])

                def slider_released(e,parameter):
                    """
                    save after the slider is released - it still opening and closing excel otherwise
                    """
                    if parameter == "zoom_increment":
                        Tools.save_to_json_config(int(zoom_increment_set.get()),"image_browser_settings","zoom_step")
                    elif parameter == "zoom_move":
                        Tools.save_to_json_config(int(zoom_movement_set.get()),"image_browser_settings","movement_step")
                    elif parameter == "IB_image_num":
                        Tools.save_to_json_config(int(num_of_image_film_images_slider.get()),"image_browser_settings","image_film_count")

                zoom_increment_set.bind("<ButtonRelease-1>",lambda e: slider_released(e,"zoom_increment"))
                zoom_movement_set.bind("<ButtonRelease-1>",lambda e: slider_released(e,"zoom_move"))
                num_of_image_film_images_slider.bind("<ButtonRelease-1>",lambda e: slider_released(e,"IB_image_num"))
                if config_data["image_browser_settings"]["show_image_film"] == "ano":
                    switch_image_film.select()

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
            options1 =          customtkinter.CTkButton(master = self.menu_buttons_frame, width = 200,height=50,text = "Názvy složek",          command =  lambda: self.setting_widgets(submenu_option="set_folder_names"),font=("Arial",20,"bold"),corner_radius=0,fg_color="black",hover_color="#212121")
            options2 =          customtkinter.CTkButton(master = self.menu_buttons_frame, width = 200,height=50,text = "Počáteční parametry",   command =  lambda: self.setting_widgets(submenu_option="set_default_parametres"),font=("Arial",20,"bold"),corner_radius=0,fg_color="black",hover_color="#212121")
            options3 =          customtkinter.CTkButton(master = self.menu_buttons_frame, width = 200,height=50,text = "Podporované formáty",   command =  lambda: self.setting_widgets(submenu_option="set_supported_formats"),font=("Arial",20,"bold"),corner_radius=0,fg_color="black",hover_color="#212121")
            options4 =          customtkinter.CTkButton(master = self.menu_buttons_frame, width = 200,height=50,text = "Prohlížeč obrázků",     command =  lambda: self.setting_widgets(submenu_option="set_image_browser_setting"),font=("Arial",20,"bold"),corner_radius=0,fg_color="black",hover_color="#212121")
            label0.             grid(column = 0,row=0,sticky = tk.W,pady =10,padx=10)
            shift_const = 210
            if not self.windowed:
                main_menu_button.grid(column = 0,row=0,pady = (10,0),padx =10,sticky = tk.W)
                shift_const = 0
            options0.           grid(column = 0,row=0,pady = (10,0),padx =220-shift_const,sticky = tk.W)
            options1.           grid(column = 0,row=0,pady = (10,0),padx =430-shift_const,sticky = tk.W)
            options2.           grid(column = 0,row=0,pady = (10,0),padx =640-shift_const,sticky = tk.W)
            options3.           grid(column = 0,row=0,pady = (10,0),padx =850-shift_const,sticky = tk.W)
            options4.           grid(column = 0,row=0,pady = (10,0),padx =1070-shift_const,sticky = tk.W)
            self.option_buttons = [options0,options1,options2,options3,options4]

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
                options1.configure(state = "disabled")
                options2.configure(state = "disabled")
                options3.configure(state = "disabled")
                options4.configure(state = "disabled")


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

    class Converting_option: # Spouští možnosti konvertování typu souborů
        """
        Spouští možnosti konvertování typu souborů

        -Spouští přes příkazový řádek command, který je vykonáván v externí aplikaci s dll knihovnami
        """
        def __init__(self,root):
            self.root = root
            self.config_data = Tools.read_json_config()
            self.bmp_folder_name = self.config_data["sort_conv_settings"]["convert_bmp_dir_name"]
            self.jpg_folder_name = self.config_data["sort_conv_settings"]["convert_jpg_dir_name"]
            self.temp_path_for_explorer = None
            self.create_convert_option_widgets()
        
        def call_extern_function(self,list_of_frames,function:str): # Tlačítko menu (konec, návrat do menu)
            """
            Funkce čistí všechny zaplněné rámečky a funguje, jako tlačítko zpět do menu\n
            function:
            - menu
            - sorting
            - deleting
            - (converting)
            """
            for frames in list_of_frames:
                frames.pack_forget()
                frames.grid_forget()
                frames.destroy()

            if function == "menu":
                menu.menu()
            elif function == "sorting":
                Sorting_option(self.root)
            elif function == "deleting":
                Deleting_option(self.root)

        def convert_files(self,path): # zde se volá externí script
            selected_format = "bmp"
            if self.checkbox_bmp.get() == 1:
                selected_format = "bmp"
            if self.checkbox_jpg.get() == 1:
                selected_format = "jpg"

            def trigger_progress_bar(interval):
                for i in range(1, 101):
                    time.sleep(interval/100)
                    self.loading_bar.set(value = i/100)
                    self.root.update_idletasks()
                    root.update_idletasks()
                    self.bottom_frame2.update_idletasks()

            def call_converting_main(whole_instance):
                whole_instance.main()
            running_program = Converting.whole_converting_function(
                path,
                selected_format,
                self.bmp_folder_name,
                self.jpg_folder_name
            )

            run_background = threading.Thread(target=call_converting_main, args=(running_program,))
            run_background.start()

            completed =False
            condition_met = False
            previous_len = 0
            while not running_program.finish or completed == False:
                time.sleep(0.05)
                if running_program.processing_time != 0 and not condition_met:
                    new_row = "Očekávaná doba procesu: " + str(running_program.processing_time) + " s"
                    Tools.add_colored_line(self.console,str(new_row),"white")
                    run_background_loading = threading.Thread(target=trigger_progress_bar(running_program.processing_time))
                    run_background_loading.start()
                    condition_met = True
                if int(len(running_program.output)) > previous_len:
                    new_row = str(running_program.output[previous_len])
                    if "Konvertování bylo dokončeno" in new_row:
                        Tools.add_colored_line(self.console,str(new_row),"green",("Arial",15,"bold"))
                    elif "cesta neobsahuje" in new_row:
                        Tools.add_colored_line(self.console,str(new_row),"red",("Arial",15,"bold"))
                    else:
                        Tools.add_colored_line(self.console,str(new_row),"white")
                    self.console.update_idletasks()
                    self.root.update_idletasks()
                    previous_len +=1
                    
                self.console.see(tk.END)

                if running_program.finish and (int(len(running_program.output)) == previous_len):
                    completed = True
                
            self.console.update_idletasks()
            run_background.join()

        def start(self):# Ověřování cesty, init, spuštění
            """
            Ověřování cesty, init, spuštění
            """
            Tools.clear_console(self.console)
            self.console.update_idletasks()
            if self.checkbox_bmp.get()+self.checkbox_jpg.get() == 0:
                Tools.add_colored_line(self.console,"Nevybrali jste žádný formát, do kterého se má konvertovat :-)","red")
            else:
                path = self.path_set.get() 
                if path != "":
                    check = Tools.path_check(path)
                    if check == False:
                        Tools.add_colored_line(self.console,"Zadaná cesta: "+str(path)+" nebyla nalezena","red")
                    else:
                        path = check
                        Tools.add_colored_line(self.console,f"Probíhá konvertování souborů v cestě: {path}","white")
                        self.console.update_idletasks()
                        self.root.update_idletasks()
                        self.convert_files(path)
                else:
                    Tools.add_colored_line(self.console,"Nebyla vložena cesta k souborům","red")

        def call_browseDirectories(self): # Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
            """
            Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
            """
            if self.temp_path_for_explorer == None:
                output = Tools.browseDirectories("all")
            else:
                output = Tools.browseDirectories("all",self.temp_path_for_explorer)

            if str(output[1]) != "/":
                self.path_set.delete("0","200")
                self.path_set.insert("0", output[1])
                Tools.add_new_path_to_history(str(output[1]),which_settings="convert_settings")
                Tools.add_colored_line(self.console,f"Byla vložena cesta: {output[1]}","green")
                self.temp_path_for_explorer = output[1]
            else:
                Tools.add_colored_line(self.console,str(output[0]),"red")

        def selected_bmp(self):
            self.checkbox_jpg.deselect()
            self.label.configure(text=f"Konvertované soubory budou vytvořeny uvnitř separátní složky: \"{self.bmp_folder_name}\"\nPodporované formáty: .ifz\nObsahuje-li .ifz soubor více obrázků, budou uloženy v následující syntaxi:\nxxx_0.bmp, xxx_1.bmp ...")
        
        def selected_jpg(self):
            self.checkbox_bmp.deselect()
            self.label.configure(text=f"Konvertované soubory budou vytvořeny uvnitř separátní složky: \"{self.jpg_folder_name}\"\nPodporované formáty: .ifz\nObsahuje-li .ifz soubor více obrázků, budou uloženy v následující syntaxi:\nxxx_0.bmp, xxx_1.bmp ...")

        def create_convert_option_widgets(self):  # Vytváří veškeré widgets (convert option MAIN)
            def call_path_context_menu(event):
                path_history = Tools.read_json_config()["sort_conv_settings"]["path_history_list_conv"]
                def insert_path(path):
                    self.path_set.delete("0","200")
                    self.path_set.insert("0", path)
                if len(path_history) > 0:
                    path_context_menu = tk.Menu(self.root, tearoff=0,fg="white",bg="black")
                    for i in range(0,len(path_history)):
                        path_context_menu.add_command(label=path_history[i], command=lambda row_path = path_history[i]: insert_path(row_path),font=("Arial",22,"bold"))
                        if i < len(path_history)-1:
                            path_context_menu.add_separator()
                            
                    path_context_menu.tk_popup(context_menu_button.winfo_rootx(),context_menu_button.winfo_rooty()+50)

            def call_start():
                self.start()# musí se čekat, jinak crash kvůli loading baru
                # run_conv_background = threading.Thread(target=self.start,)
                # run_conv_background.start()
                # run_conv_background.join()

            frame_with_logo =       customtkinter.CTkFrame(master=self.root,corner_radius=0)
            logo =                  customtkinter.CTkImage(Image.open(Tools.resource_path("images/logo.png")),size=(1200, 100))
            image_logo =            customtkinter.CTkLabel(master = frame_with_logo,text = "",image =logo)
            frame_with_logo.        pack(pady=0,padx=0,fill="both",expand=False,side = "top")
            image_logo.pack()
            frame_with_cards =      customtkinter.CTkFrame(master=self.root,corner_radius=0,fg_color="#636363",height=100)
            self.frame_path_input = customtkinter.CTkFrame(master=self.root,corner_radius=0)
            self.bottom_frame2 =    customtkinter.CTkFrame(master=self.root,corner_radius=0)
            self.bottom_frame1 =    customtkinter.CTkFrame(master=self.root,height = 80,corner_radius=0)
            frame_with_cards.       pack(pady=0,padx=0,fill="both",expand=False,side = "top")
            self.frame_path_input.  pack(pady=(0,5),padx=5,fill="both",expand=False,side = "top")

            list_of_frames = [self.frame_path_input,self.bottom_frame1,self.bottom_frame2,frame_with_cards,frame_with_logo]
            shift_const = 250
            menu_button =       customtkinter.CTkButton(master = frame_with_cards, width = 250,height=50,text = "MENU",                  command =  lambda: self.call_extern_function(list_of_frames,function="menu"),
                                                        font=("Arial",20,"bold"),corner_radius=0,fg_color="black",hover_color="#212121")
            sorting_button =    customtkinter.CTkButton(master = frame_with_cards, width = 250,height=50,text = "Třídění souborů",      command =  lambda: self.call_extern_function(list_of_frames,function="sorting"),
                                                        font=("Arial",20,"bold"),corner_radius=0,fg_color="black",hover_color="#212121")
            deleting_button =   customtkinter.CTkButton(master = frame_with_cards, width = 250,height=50,text = "Mazání souborů",        command =  lambda: self.call_extern_function(list_of_frames,function="deleting"),
                                                        font=("Arial",20,"bold"),corner_radius=0,fg_color="black",hover_color="#212121")
            converting_button = customtkinter.CTkButton(master = frame_with_cards, width = 250,height=50,text = "Konvertování souborů",
                                                        font=("Arial",20,"bold"),corner_radius=0,fg_color="#212121",hover_color="#212121")
            menu_button.        grid(column = 0,row=0,pady = (10,0),padx =260-shift_const,sticky = tk.W)
            sorting_button.     grid(column = 0,row=0,pady = (10,0),padx =520-shift_const,sticky = tk.W)
            deleting_button.    grid(column = 0,row=0,pady = (10,0),padx =780-shift_const,sticky = tk.W)
            converting_button.  grid(column = 0,row=0,pady = (10,0),padx =1040-shift_const,sticky = tk.W)

            self.checkbox_bmp =     customtkinter.CTkCheckBox(master = self.bottom_frame1, text = "Konvertovat do formátu .bmp",command=self.selected_bmp,font=("Arial",16,"bold"))
            self.checkbox_jpg =     customtkinter.CTkCheckBox(master = self.bottom_frame1, text = "Konvertovat do formátu .jpg",command=self.selected_jpg,font=("Arial",16,"bold"))
            self.checkbox_bmp.      pack(pady =10,padx=10,anchor ="w")
            self.checkbox_jpg.      pack(pady =10,padx=10,anchor ="w")
            self.bottom_frame1.     pack(pady=0,padx=5,fill="x",expand=False,side = "top")
            context_menu_button  =  customtkinter.CTkButton(master =self.frame_path_input, width = 50,height=50, text = "V",font=("Arial",20,"bold"),corner_radius=0,fg_color="#505050")
            self.path_set =         customtkinter.CTkEntry(master = self.frame_path_input,font=("Arial",18),height=50,placeholder_text="Zadejte cestu k souborům určeným ke konvertování (kde se soubory přímo nacházejí)",corner_radius=0)
            tree         =          customtkinter.CTkButton(master = self.frame_path_input,height=50,text = "EXPLORER", command = self.call_browseDirectories,font=("Arial",20,"bold"),corner_radius=0)
            button_save_path =      customtkinter.CTkButton(master = self.frame_path_input,height=50,text = "Uložit cestu", command = lambda: Tools.save_path(self.console,self.path_set.get(),"convert_option"),font=("Arial",20,"bold"),corner_radius=0)
            button_open_setting =   customtkinter.CTkButton(master = self.frame_path_input,width=50,height=50,text = "⚙️", command = lambda: Advanced_option(self.root,windowed=True,spec_location="converting_option"),font=(None,20),corner_radius=0)
            context_menu_button.    pack(pady = 10,padx = (10,0), anchor ="w",side="left")
            self.path_set.          pack(pady = 10,padx = (0,0), anchor ="w",side="left",fill="x",expand=True)
            tree.                   pack(pady = 10,padx = 5,anchor ="w",side="left")
            button_save_path.       pack(pady = 10,padx = (0,0),anchor ="w",side="left")
            button_open_setting.    pack(pady = 10,padx = (5,10),anchor ="w",side="left")
            self.label   =          customtkinter.CTkLabel(master = self.bottom_frame2,text = f"Konvertované soubory budou vytvořeny uvnitř separátní složky: \"{self.bmp_folder_name}\"\nPodporované formáty: .ifz\nObsahuje-li .ifz soubor více obrázků, budou uloženy v následující syntaxi:\nxxx_0.bmp, xxx_1.bmp ...",justify = "left",font=("Arial",18,"bold"))
            button  =               customtkinter.CTkButton(master = self.bottom_frame2, text = "KONVERTOVAT", command = lambda: call_start(),font=("Arial",20,"bold"))
            self.loading_bar =      customtkinter.CTkProgressBar(master = self.bottom_frame2, mode='determinate',width = 800,height =20,progress_color="green",corner_radius=0)
            self.console =          tk.Text(self.bottom_frame2, wrap="word",background="black",font=("Arial",16))
            self.label.             pack(pady =10,padx=10)
            button.                 pack(pady =20,padx=10)
            button.                 _set_dimensions(300,60)
            self.loading_bar.       pack(pady = 5,padx = 5)
            self.loading_bar.       set(value = 0)
            self.console.           pack(pady =10,padx=(10,0),side = "left",fill="both",expand=True)
            self.bottom_frame2.     pack(pady=5,padx=5,fill="both",expand=True,side = "top")
            context_menu_button.bind("<Button-1>", call_path_context_menu)
            self.checkbox_bmp.select()
            scrollbar = tk.Scrollbar(self.bottom_frame2, command=self.console.yview)
            scrollbar.pack(pady =10,side="right", fill="y")
            self.console.config(yscrollcommand=scrollbar.set)
            self.console.configure(state=tk.DISABLED)

            recources_path = self.config_data["app_settings"]["default_path"]
            config_data = Tools.read_json_config()
            if len(config_data["sort_conv_settings"]["path_history_list_conv"]) != 0:
                path_from_history = config_data["sort_conv_settings"]["path_history_list_conv"][0]
                self.path_set.delete("0","200")
                self.path_set.insert("0", path_from_history)
                Tools.add_colored_line(self.console,"Byla vložena cesta z konfiguračního souboru","white",None,True)
                self.root.update_idletasks()
            elif recources_path != False and recources_path != "/":
                self.path_set.delete("0","200")
                self.path_set.insert("0", str(recources_path))
                Tools.add_colored_line(self.console,"Byla vložena cesta z konfiguračního souboru","white")
            else:
                Tools.add_colored_line(self.console,"Konfigurační soubor obsahuje neplatnou cestu k souborům (můžete vložit v pokročilém nastavení)","orange")

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
                self.root.focus_set()
            self.path_set.bind("<Return>",unfocus_widget)

    class Deleting_option: # Umožňuje mazat soubory podle nastavených specifikací
        """
        Umožňuje mazat soubory podle nastavených specifikací

        -obsahuje i režim testování, kde soubory pouze přesune do složky ke smazání
        -umožňuje procházet více subsložek
        
        """

        def __init__(self,root):
            self.root = root
            self.unbind_list = []
            self.config_data = Tools.read_json_config()
            self.supported_formats_deleting = self.config_data["del_settings"]["supported_formats_deleting"]
            self.files_to_keep = self.config_data["del_settings"]["default_files_to_keep"]
            self.cutoff_date = self.config_data["del_settings"]["default_cutoff_date"]
            self.to_delete_folder_name = self.config_data["del_settings"]["to_delete_dir_name"]
            self.selected_language = self.config_data["app_settings"]["default_language"]
            self.temp_path_for_explorer = None
            self.selected_option = 1
            self.more_dirs = False
            self.testing_mode = True
            self.by_creation_date = False
            self.directories_to_keep = 10
            self.create_deleting_option_widgets()
    
        def call_extern_function(self,list_of_frames=[],function=""): # Tlačítko menu (konec, návrat do menu)
            """
            Funkce čistí všechny zaplněné rámečky a funguje, jako tlačítko zpět do menu\n
            function:
            - menu
            - sorting
            - deleting
            - converting
            """
            
            for frames in list_of_frames:
                frames.pack_forget()
                frames.grid_forget()
                frames.destroy()
            
            for binds in self.unbind_list:
                self.root.unbind(binds)

            self.clear_frame(self.root)

            if function == "menu":
                menu.menu()
            elif function == "sorting":
                Sorting_option(self.root)
            elif function == "converting":
                Converting_option(self.root)

        def start(self,only_analyze=False):# Ověřování cesty, init, spuštění
            """
            Ověřování cesty, init, spuštění
            """
            Tools.clear_console(self.console)
            path = self.path_set.get() 
            if path != "":
                check = Tools.path_check(path)
                if check == False:
                    Tools.add_colored_line(self.console,"Zadaná cesta: "+str(path)+" nebyla nalezena","red")
                else:
                    path = check
                    if only_analyze:
                        info_msg = "- Provádím analýzu souborů v cestě: " + str(path) + "\n"
                        if self.selected_language == "en":
                            info_msg = "- Analyzing files in the path: " + str(path) + "\n"
                        Tools.add_colored_line(self.console,info_msg,"orange")
                        self.console.update_idletasks()
                        self.root.update_idletasks()
                        self.del_files(path,only_analyze)
                        return

                    if self.checkbox_testing.get() != 1:
                        if self.more_dirs == True and self.selected_option != 3: # sublozky, ne u adresaru...
                            confirm_prompt_msg = f"Opravdu si přejete spustit navolené mazání souborů v cestě:\n{path}\na procházet přitom i SUBSLOŽKY?"
                            if self.selected_language == "en":
                                confirm_prompt_msg = f"Do you really want to start the custom deletion of files in the path:\n{path}\nand browse SUBFOLDERS?"
                        elif self.selected_option == 3:
                            confirm_prompt_msg = f"Opravdu si přejete spustit navolené mazání ADRESÁŘŮ v cestě:\n{path}"
                            if self.selected_language == "en":
                                confirm_prompt_msg = f"You really want to start the custom deletion of DIRECTORIES in the path:\n{path}"
                        else:
                            confirm_prompt_msg = f"Opravdu si přejete spustit navolené mazání souborů v cestě:\n{path}"
                            if self.selected_language == "en":
                                confirm_prompt_msg = f"Do you really want to start the custom deletion of files in the path:\n{path}"
                        # confirm = tk.messagebox.askokcancel("Potvrzení", confirm_prompt_msg)
                        if self.selected_language == "en":
                            confirm = Subwindows.confirm_window(confirm_prompt_msg,"Notice",self.selected_language)
                        else:
                            confirm = Subwindows.confirm_window(confirm_prompt_msg,"Upozornění",self.selected_language)
                    else: # pokud je zapnut rezim testovani
                        confirm = True

                    if confirm == True:
                        info_msg = "- Provádím navolené možnosti mazání v cestě: " + str(path) + "\n"
                        if self.selected_language == "en":
                            info_msg = "- I perform the selected deletion options in the path: " + str(path) + "\n"
                        Tools.add_colored_line(self.console,info_msg,"orange")

                        self.console.update_idletasks()
                        self.root.update_idletasks()
                        self.del_files(path)
                    else:
                        cancel_msg = "Zrušeno uživatelem"
                        if self.selected_language == "en":
                            cancel_msg = "Cancelled by user"
                        Tools.add_colored_line(self.console,cancel_msg,"red")
            else:
                no_path_msg = "Nebyla vložena cesta k souborům"
                if self.selected_language == "en":
                    no_path_msg = "The path to the files has not been inserted"
                Tools.add_colored_line(self.console,no_path_msg,"red")

        def del_files(self,path,only_analyze = False): # zde se volá externí script: Deleting
            del_option = self.selected_option
            files_to_keep = self.files_to_keep
            if self.checkbox_testing.get() == 1:
                testing_mode = True
            else:
                testing_mode = False

            more_dirs = self.more_dirs
            if self.selected_option == 3:
                more_dirs = False

            def call_deleting_main(whole_instance):
                whole_instance.main()

            if self.selected_option == 4:
                files_to_keep = self.directories_to_keep

            only_analyze_status = False
            if only_analyze:
                testing_mode = True
                only_analyze_status = True


            running_deleting = Deleting.whole_deleting_function(
                path,
                more_dirs,
                del_option,
                files_to_keep,
                self.cutoff_date,
                self.supported_formats_deleting,
                testing_mode,
                self.to_delete_folder_name,
                creation_date = self.by_creation_date,
                only_analyze = only_analyze_status
                )

            run_del_background = threading.Thread(target=call_deleting_main, args=(running_deleting,))
            run_del_background.start()
            completed = False
            previous_len = 0
            output_messages = running_deleting.output
            if self.selected_language == "en":
                output_messages = running_deleting.output_eng

            while not running_deleting.finish or completed == False:
                time.sleep(0.01)
                if int(len(output_messages)) > previous_len:
                    new_row = str(output_messages[previous_len])
                    if "Mazání dokončeno" in new_row or "Zkontrolováno" in new_row or "Deleting complete" in new_row or "checked" in new_row:
                        Tools.add_colored_line(self.console,str(new_row),"green",("Arial",15,"bold"))
                    elif "Chyba" in new_row or "Nebyly nalezeny" in new_row or "- zrušeno" in new_row or "Error" in new_row or "No directories found" in new_row or "No files found" in new_row or "cancelled" in new_row:
                        Tools.add_colored_line(self.console,str(new_row),"red",("Arial",15,"bold"))
                    elif "Smazalo by se" in new_row or "Smazáno" in new_row or "It would delete" in new_row or "deleted" in new_row:
                        Tools.add_colored_line(self.console,str(new_row),"orange",("Arial",15,"bold"))
                    else:
                        Tools.add_colored_line(self.console,str(new_row),"white")
                    self.console.update_idletasks()
                    self.console.see(tk.END)
                    self.root.update_idletasks()
                    previous_len +=1

                if running_deleting.finish and (int(len(output_messages)) == previous_len):
                    completed = True
            
            run_del_background.join()

        def call_browseDirectories(self): # Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
            """
            Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
            """
            self.temp_path_for_explorer = self.path_set.get()
            if self.more_dirs or self.selected_option == 3 or self.selected_option == 4: # pokud je zvoleno more_dirs v exploreru pouze slozky...
                output = Tools.browseDirectories("only_dirs",self.temp_path_for_explorer)
            else:
                output = Tools.browseDirectories("all",self.temp_path_for_explorer)
            if str(output[1]) != "/":
                self.path_set.delete("0","200")
                self.path_set.insert("0", output[1])
                Tools.add_new_path_to_history(str(output[1]),which_settings="del_settings")
                if self.selected_language == "en":
                    Tools.add_colored_line(self.console,f"The path has been added: {output[1]}","green")
                else:
                    Tools.add_colored_line(self.console,f"Byla vložena cesta: {output[1]}","green")
                self.temp_path_for_explorer = output[1]
            else:
                if self.selected_language == "en":
                    if str(output[0]) == "Přes explorer nebyla vložena žádná cesta":
                        Tools.add_colored_line(self.console,"No path was inserted via explorer","red")
                else:
                    Tools.add_colored_line(self.console,str(output[0]),"red")

        def clear_frame(self,frame):
            for widget in frame.winfo_children():
                widget.destroy()

        def selected(self,option): # První možnost mazání, od nejstarších
            """
            Vstup:\n
            - option = 1:
                - Redukce souborů starších než: nastavené datum
            - option = 2:
                - Redukce novějších, mazání souborů starších než: nastavené datum\n
            -Podporované formáty jsou uživatelem nastavené a uložené v konfiguračním souboru
            """
            self.clear_frame(self.changable_frame)
            
            def set_cutoff_date():
                # if set_month.get() == self.cutoff_date[1] and set_day.get() == self.cutoff_date[0] and set_day.get() == self.cutoff_date[2]
                input_month = set_month.get()
                if input_month != "":
                    if input_month.isdigit():
                        if int(input_month) < 13 and int(input_month) > 0:
                            self.cutoff_date[1] = int(input_month)
                            max_days_in_month = Deleting.calc_days_in_month(int(self.cutoff_date[1]))
                            if int(self.cutoff_date[0]) > max_days_in_month:
                                self.cutoff_date[0] = str(max_days_in_month)
                            if self.selected_language == "en":
                                Tools.add_colored_line(console,"Date changed to: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green",None,True)
                            else:
                                Tools.add_colored_line(console,"Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green",None,True)
                            max_days_entry.delete(0,"100")
                            max_days_entry.insert(0,Deleting.get_max_days(self.cutoff_date))
                        else:
                            if self.selected_language == "en":
                                Tools.add_colored_line(console,"Month: " + str(input_month) + " is out of range","red",None,True)
                            else:
                                Tools.add_colored_line(console,"Měsíc: " + str(input_month) + " je mimo rozsah","red",None,True)
                    else:
                        if self.selected_language == "en":
                            Tools.add_colored_line(console, "You did not enter a number for the month settings","red",None,True)
                        else:
                            Tools.add_colored_line(console, "U nastavení měsíce jste nezadali číslo","red",None,True)

                input_day = set_day.get()
                max_days_in_month = Deleting.calc_days_in_month(int(self.cutoff_date[1]))

                if input_day != "":
                    if input_day.isdigit():
                        if int(input_day) <= int(max_days_in_month) and int(input_day) > 0:
                            self.cutoff_date[0] = int(input_day)
                            if self.selected_language == "en":
                                Tools.add_colored_line(console, "Date changed to: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green",None,True)
                            else:
                                Tools.add_colored_line(console, "Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green",None,True)
                            max_days_entry.delete(0,"100")
                            max_days_entry.insert(0,Deleting.get_max_days(self.cutoff_date))
                        else:
                            if self.selected_language == "en":
                                Tools.add_colored_line(console, "Day: " + str(input_day) + " is out of range","red",None,True)
                            else:
                                Tools.add_colored_line(console, "Den: " + str(input_day) + " je mimo rozsah","red",None,True)
                    else:
                        if self.selected_language == "en":
                            Tools.add_colored_line(console, "You did not enter a number for the day settings","red",None,True)
                        else:
                            Tools.add_colored_line(console, "U nastavení dne jste nezadali číslo","red",None,True)

                input_year = set_year.get()
                if input_year != "":
                    if input_year.isdigit():
                        if len(str(input_year)) == 2:
                            self.cutoff_date[2] = int(input_year) + 2000
                            if self.selected_language == "en":
                                Tools.add_colored_line(console,"Date changed to: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green",None,True)
                            else:
                                Tools.add_colored_line(console,"Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green",None,True)

                            max_days_entry.delete(0,"100")
                            max_days_entry.insert(0,Deleting.get_max_days(self.cutoff_date))
                        elif len(str(input_year)) == 4:
                            self.cutoff_date[2] = int(input_year)
                            if self.selected_language == "en":
                                Tools.add_colored_line(console,"Date changed to: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green",None,True)
                            else:
                                Tools.add_colored_line(console,"Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green",None,True)
                            max_days_entry.delete(0,"100")
                            max_days_entry.insert(0,Deleting.get_max_days(self.cutoff_date))
                        else:
                            if self.selected_language == "en":
                                Tools.add_colored_line(console, "Year: " + str(input_year) + " is out of range","red",None,True)
                            else:
                                Tools.add_colored_line(console, "Rok: " + str(input_year) + " je mimo rozsah","red",None,True)
                    else:
                        if self.selected_language == "en":
                            Tools.add_colored_line(console, "You did not enter a number for the year setting","red",None,True)
                        else:
                            Tools.add_colored_line(console, "U nastavení roku jste nezadali číslo","red",None,True)

            def set_files_to_keep():
                input_files_to_keep = files_to_keep_set.get()
                if input_files_to_keep.isdigit():
                    if int(input_files_to_keep) >= 0:
                        self.files_to_keep = int(input_files_to_keep)
                        if self.selected_language == "en":
                            Tools.add_colored_line(console, "Number of older files left set to: " + str(self.files_to_keep),"green",None,True)
                        else:
                            Tools.add_colored_line(console, "Počet ponechaných starších souborů nastaven na: " + str(self.files_to_keep),"green",None,True)

                        if option == 1:
                            summary_label.configure(text = f"Ponechány tedy budou všechny soubory NOVĚJŠÍ než nastavené datum a současně bude ponecháno: {self.files_to_keep} STARŠÍCH souborů.")
                            if self.selected_language == "en":
                                summary_label.configure(text = f"So all files LATER than the set date will be kept and at the same time: {self.files_to_keep} OLDER files will be kept.")

                        else:
                            summary_label.configure(text =f"Budou SMAZÁNY VŠECHNY soubory STARŠÍ než nastavené datum, přičemž budou redukovány i soubroy NOVĚJŠÍ na počet: {self.files_to_keep} souborů\n(pokud jsou v dané cestě všechny soubory starší, mazání se neprovede)")
                            if self.selected_language == "en":
                                summary_label.configure(text =f"ALL files OLDER than the set date will be DELETED, while files newer than the set date will be reduced to the number of: {self.files_to_keep} files\n(if all files in the path are older, the deletion will not be performed)")
                    else:
                        if self.selected_language == "en":
                            Tools.add_colored_line(console, "Out of range","red",None,True)
                        else:
                            Tools.add_colored_line(console, "Mimo rozsah","red",None,True)
                else:
                    if self.selected_language == "en":
                        Tools.add_colored_line(console, "You didn't enter a number","red",None,True)
                    else:
                        Tools.add_colored_line(console, "Nazadali jste číslo","red",None,True)

            def insert_current_date():
                today = Deleting.get_current_date()
                today_split = today[1].split(".")
                i=0
                for items in today_split:
                    i+=1
                    self.cutoff_date[i-1]=items
                set_day.delete(0,"100")
                set_month.delete(0,"100")
                set_year.delete(0,"100")
                set_day.insert(0,self.cutoff_date[0])
                set_month.insert(0,self.cutoff_date[1])
                set_year.insert(0,self.cutoff_date[2])
                max_days_entry.delete(0,"100")
                max_days_entry.insert(0,Deleting.get_max_days(self.cutoff_date))
                if self.selected_language == "en":
                    Tools.add_colored_line(console, "Today's date has been inserted (currently all files are evaluated as older!)","orange",None,True)
                else:
                    Tools.add_colored_line(console, "Bylo vloženo dnešní datum (Momentálně všechny soubory vyhodnoceny, jako starší!)","orange",None,True)

            def save_before_execution():
                input_month = set_month.get()
                if input_month != "":
                    if input_month.isdigit():
                        if int(input_month) < 13 and int(input_month) > 0:
                            self.cutoff_date[1] = int(input_month)
                            max_days_in_month = Deleting.calc_days_in_month(int(self.cutoff_date[1]))
                            if int(self.cutoff_date[0]) > max_days_in_month:
                                self.cutoff_date[0] = str(max_days_in_month)

                input_day = set_day.get()
                max_days_in_month = Deleting.calc_days_in_month(int(self.cutoff_date[1]))
                if input_day != "":
                    if input_day.isdigit():
                        if int(input_day) <= int(max_days_in_month) and int(input_day) > 0:
                            self.cutoff_date[0] = int(input_day)

                input_year = set_year.get()
                if input_year != "":
                    if input_year.isdigit():
                        if len(str(input_year)) == 2:
                            self.cutoff_date[2] = int(input_year) + 2000
                        elif len(str(input_year)) == 4:
                            self.cutoff_date[2] = int(input_year)

                input_files_to_keep = files_to_keep_set.get()
                if input_files_to_keep.isdigit():
                    if int(input_files_to_keep) >= 0:
                        self.files_to_keep = int(input_files_to_keep)

            def set_max_days(flag=""):
                if flag == "cutoff":
                    new_cutoff = Deleting.get_cutoff_date(int(max_days_entry.get()))
                    set_day.delete(0,"100")
                    set_month.delete(0,"100")
                    set_year.delete(0,"100")
                    set_day.insert(0,new_cutoff[0])
                    set_month.insert(0,new_cutoff[1])
                    set_year.insert(0,new_cutoff[2])
                    set_cutoff_date()
                elif flag == "max_days":
                    set_cutoff_date()
                    # max_days_entry.delete(0,"100")
                    # max_days_entry.insert(0,Deleting.get_max_days(self.cutoff_date))
            
            def update_entry(event,flag=""):
                if flag == "cutoff":
                    self.root.after(100, lambda: set_max_days(flag))
                elif flag == "max_days":
                    self.root.after(100, lambda: set_max_days(flag))
                elif flag == "ftk":
                    self.root.after(100, lambda: set_files_to_keep())

            def search_subfolders():
                if subfolder_checkbox.get() == 1:
                    self.more_dirs = True
                    if self.selected_language == "en":
                        subfolder_warning.configure(text = "- WARNING: You have image file deletion options running in all subfolders of the embedded path (max: 6 subfolders)",font=("Arial",18,"bold"),text_color="yellow")
                        return
                    subfolder_warning.configure(text = "- VAROVÁNÍ: Máte spuštěné možnosti mazání obrázkových souborů i ve všech subsložkách vložené cesty (max: 6 subsložek)",font=("Arial",18,"bold"),text_color="yellow")
                else:
                    self.more_dirs = False
                    subfolder_warning.configure(text = "")

            def set_testing_mode():
                if self.checkbox_testing.get() == 1:
                    self.testing_mode = True
                else:
                    self.testing_mode = False

            def set_decision_date(input_arg):
                """
                input_arg:
                - creation
                - modification
                """

                if input_arg == "creation":
                    self.by_creation_date = True
                    checkbox_modification_date.deselect()

                elif input_arg == "modification":
                    self.by_creation_date = False
                    checkbox_creation_date.deselect()

            top_frame = customtkinter.CTkFrame(master=self.changable_frame,corner_radius=0,fg_color="#212121",height=240)
            title_and_date_frame= customtkinter.CTkFrame(master=top_frame,corner_radius=0,fg_color="#212121")
            option_title = customtkinter.CTkLabel(master = title_and_date_frame,height=20,text = "Redukce souborů starších než: nastavené datum",justify = "left",font=("Arial",25,"bold"))
            today = Deleting.get_current_date()
            current_date = customtkinter.CTkLabel(master = title_and_date_frame,text = "Dnešní datum: "+today[1],justify = "left",font=("Arial",20,"bold"),bg_color="black")
            option_title.pack(padx=10,pady=10,side="left",anchor="w")
            current_date.pack(padx=5,pady=(0,0),side="left",anchor="e",expand = True,fill="y",ipadx = 10)
            title_and_date_frame.pack(padx=(0,0),pady=(0,0),side="top",anchor="w",fill="both")
            user_input_frame = customtkinter.CTkFrame(master=top_frame,corner_radius=0,fg_color="#212121",border_width=4,border_color="#636363")
            date_input_frame = customtkinter.CTkFrame(master=user_input_frame,corner_radius=0,fg_color="#212121")
            date_label = customtkinter.CTkLabel(master = date_input_frame,text = "‣ budou smazány soubory starší než nastavené datum:",justify = "left",font=("Arial",20))
            set_day     = customtkinter.CTkEntry(master = date_input_frame,width=40,font=("Arial",20), placeholder_text= self.cutoff_date[0])
            sep1        = customtkinter.CTkLabel(master = date_input_frame,width=10,text = ".",font=("Arial",20))
            set_month   = customtkinter.CTkEntry(master = date_input_frame,width=40,font=("Arial",20), placeholder_text= self.cutoff_date[1])
            sep2        = customtkinter.CTkLabel(master = date_input_frame,width=10,text = ".",font=("Arial",20))
            set_year    = customtkinter.CTkEntry(master = date_input_frame,width=60,font=("Arial",20), placeholder_text= self.cutoff_date[2])
            insert_button = customtkinter.CTkButton(master = date_input_frame,width=190, text = "Vložit dnešní datum", command = lambda: insert_current_date(),font=("Arial",20,"bold"))
            date_label. pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            set_day.    pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            sep1.       pack(padx=(5,0),pady=(0,0),side="left",anchor="w")
            set_month.  pack(padx=(5,0),pady=(0,0),side="left",anchor="w")
            sep2.       pack(padx=(5,0),pady=(0,0),side="left",anchor="w")
            set_year.   pack(padx=(5,0),pady=(0,0),side="left",anchor="w")
            insert_button.   pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            date_input_frame.pack(padx=5,pady=(10,0),side="top",anchor="w")
            set_day.bind("<Key>",lambda e: update_entry(e,flag="max_days"))
            set_month.bind("<Key>",lambda e: update_entry(e,flag="max_days"))
            set_year.bind("<Key>",lambda e: update_entry(e,flag="max_days"))

            day_format_input_frame = customtkinter.CTkFrame(master=user_input_frame,corner_radius=0,fg_color="#212121")
            days_label = customtkinter.CTkLabel(master = day_format_input_frame,text = "‣ to znamená starší než:",justify = "left",font=("Arial",20))
            max_days_entry = customtkinter.CTkEntry(master = day_format_input_frame,width=60,font=("Arial",20))
            max_days_entry.insert(0,Deleting.get_max_days(self.cutoff_date))
            days_label2 = customtkinter.CTkLabel(master = day_format_input_frame,text = "dní",justify = "left",font=("Arial",20))
            days_label. pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            max_days_entry. pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            days_label2. pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            day_format_input_frame.pack(padx=5,pady=0,side="top",anchor="w")
            max_days_entry.bind("<Key>",lambda e: update_entry(e,flag="cutoff"))

            ftk_frame = customtkinter.CTkFrame(master=user_input_frame,corner_radius=0,fg_color="#212121")
            ftk_label = customtkinter.CTkLabel(master = ftk_frame,text = "‣ přičemž bude ponecháno:",justify = "left",font=("Arial",20))
            files_to_keep_set = customtkinter.CTkEntry(master = ftk_frame,width=70,font=("Arial",20), placeholder_text= self.files_to_keep)
            ftk_label2 = customtkinter.CTkLabel(master = ftk_frame,text = "souborů, vyhodnocených, jako starších",justify = "left",font=("Arial",20))
            ftk_label. pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            files_to_keep_set. pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            ftk_label2. pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            ftk_frame.pack(padx=5,pady=(0,10),side="top",anchor="w")
            user_input_frame.pack(padx=5,pady=(0,0),side="top",anchor="w",fill="x")
            files_to_keep_set.bind("<Key>",lambda e: update_entry(e,flag="ftk"))

            summary_label = customtkinter.CTkLabel(master = top_frame,text = f"Ponechány tedy budou všechny soubory NOVĚJŠÍ než nastavené datum a současně bude ponecháno: {self.files_to_keep} STARŠÍCH souborů.",justify = "left",font=("Arial",20,"bold"))
            summary_label.pack(padx=10,pady=(10,0),side="top",anchor="w")
            deletable_formats = customtkinter.CTkLabel(master = top_frame,text = f"Smazatelné formáty: {self.supported_formats_deleting}",justify = "left",font=("Arial",20))
            deletable_formats.pack(padx=10,pady=(0,0),side="top",anchor="w")
            top_frame.pack(padx=(0,0),pady=(0),side="top",anchor="w",fill="x")
            top_frame.propagate(False)
            console = tk.Text(self.changable_frame, wrap="none", height=0, width=30,background="black",font=("Arial",22),state=tk.DISABLED)
            console.pack(pady = (10,0),padx =10,side="top",anchor="w",fill="x")

            subfolder_frame = customtkinter.CTkFrame(master=self.changable_frame,corner_radius=0,fg_color="#212121")
            subfolder_checkbox = customtkinter.CTkCheckBox(master = subfolder_frame, text = "Procházet subsložky? (max: 6)",command = lambda: search_subfolders(),font=("Arial",18,"bold"))
            subfolder_warning = customtkinter.CTkLabel(master = subfolder_frame,text = "",font=("Arial",18,"bold"))
            subfolder_checkbox.pack(padx=(10,0),pady=(5,0),side="left",anchor="w")
            subfolder_warning.pack(padx=(10,0),pady=(5,0),side="left",anchor="w")
            subfolder_frame.pack(padx=(0,0),pady=0,side="top",anchor="w")

            self.checkbox_testing = customtkinter.CTkCheckBox(master =self.changable_frame, text = f"Režim TESTOVÁNÍ (Soubory vyhodnocené ke smazání se pouze přesunou do složky s názvem: \"{self.to_delete_folder_name}\")",font=("Arial",18,"bold"),command=lambda: set_testing_mode())
            self.checkbox_testing.pack(pady = (10,0),padx =10,side="top",anchor="w")

            decision_date_frame = customtkinter.CTkFrame(master=self.changable_frame,corner_radius=0,fg_color="#212121")
            decision_date_label = customtkinter.CTkLabel(master = decision_date_frame,text = "Řídit se podle: ",justify = "left",font=("Arial",20,"bold"))
            checkbox_creation_date = customtkinter.CTkCheckBox(master =decision_date_frame, text = "data vytvoření",font=("Arial",18),command=lambda:set_decision_date("creation"))
            checkbox_modification_date = customtkinter.CTkCheckBox(master =decision_date_frame, text = "data poslední změny (doporučeno)",font=("Arial",18),command=lambda:set_decision_date("modification"))
            decision_date_label.pack(pady = (10,0),padx =(10,0),side="left",anchor="w")
            checkbox_creation_date.pack(pady = (10,0),padx =(10,0),side="left",anchor="w")
            checkbox_modification_date.pack(pady = (10,0),padx =(10,0),side="left",anchor="w")
            decision_date_frame.pack(pady = (0,0),padx =0,side="top",anchor="w",fill="x")
            if self.by_creation_date:
                checkbox_creation_date.select()
            else:
                checkbox_modification_date.select()
            if self.testing_mode:
                self.checkbox_testing.select()
            if self.more_dirs:
                subfolder_checkbox.select()
                search_subfolders()

            if self.selected_language == "en":
                option_title.configure(text= "Reducing files older than: set date")
                date_label.configure(text= "‣ files older than the set date will be deleted:")
                insert_button.configure(text= "Insert today's date")
                days_label.configure(text= "‣ it means older than:")
                days_label2.configure(text= "days")
                ftk_label.configure(text= "‣ whereby it will be retained:")
                ftk_label2.configure(text= "files, evaluated as older")
                summary_label.configure(text= f"So all files LATER than the set date will be kept and at the same time: {self.files_to_keep} OLDER files will be kept.")
                deletable_formats.configure(text= f"Deletable formats: {self.supported_formats_deleting}")
                subfolder_checkbox.configure(text= "Browse subfolders? (max: 6)")
                self.checkbox_testing.configure(text= f"TEST mode (Files evaluated for deletion are only moved to a folder named: \"{self.to_delete_folder_name}\")")
                current_date.configure(text = "Current date: "+today[1])
                decision_date_label.configure(text = "To decide by:")
                checkbox_creation_date.configure(text = "date of creation")
                checkbox_modification_date.configure(text = "date of modification (recommended)")

            if option == 2:
                self.selected_option = 2
                self.options1.deselect()
                self.options2.select()
                self.options3.deselect()
                self.options4.deselect()
                if self.selected_language == "en":
                    option_title.configure(text="Reducing newer, deleting files older than: set date")
                    date_label.configure(text= "‣ ALL files older than the set date will be deleted:")
                    ftk_label2.configure(text= "files, evaluated as newer")
                    summary_label.configure(text=f"ALL files OLDER than the set date will be DELETED, while files newer than the set date will be reduced to the number of: {self.files_to_keep} files\n(if all files in the path are older, the deletion will not be performed)")
                else:
                    option_title.configure(text="Redukce novějších, mazání souborů starších než: nastavené datum")
                    date_label.configure(text= "‣ budou smazány VŠECHNY soubory starší než nastavené datum:")
                    ftk_label2.configure(text= "souborů, vyhodnocených, jako novějších")
                    summary_label.configure(text=f"Budou SMAZÁNY VŠECHNY soubory STARŠÍ než nastavené datum, přičemž budou redukovány i soubroy NOVĚJŠÍ na počet: {self.files_to_keep} souborů\n(pokud jsou v dané cestě všechny soubory starší, mazání se neprovede)")
            else:
                self.selected_option = 1
                self.options1.select()
                self.options2.deselect()
                self.options3.deselect()
                self.options4.deselect()
            
            def new_date_enter_btn(e):
                set_cutoff_date()
            set_day.bind("<Return>",new_date_enter_btn)
            set_month.bind("<Return>",new_date_enter_btn)
            set_year.bind("<Return>",new_date_enter_btn)

            def new_FTK_enter_btn(e):
                set_files_to_keep()
            files_to_keep_set.bind("<Return>",new_FTK_enter_btn)
            # self.changable_frame.bind("<Enter>",lambda e: save_before_execution()) # případ, že se nestiskne uložit - aby nedošlo ke ztrátě souborů
            
        def selected3(self,option): # První možnost mazání, od nejstarších
            """
            Budou smazány VŠECHNY adresáře (včetně všech subadresářů), které obsahují v názvu podporovaný formát datumu a jsou vyhodnoceny,jako starší než nastavené datum\n
            - podporované datumové formáty jsou ["YYYYMMDD","DDMMYYYY","YYMMDD"]
            - podporované datumové separátory: [".","/","_"]
            """
            self.clear_frame(self.changable_frame)
            self.more_dirs = False

            def set_cutoff_date():
                # if set_month.get() == self.cutoff_date[1] and set_day.get() == self.cutoff_date[0] and set_day.get() == self.cutoff_date[2]
                input_month = set_month.get()
                if input_month != "":
                    if input_month.isdigit():
                        if int(input_month) < 13 and int(input_month) > 0:
                            self.cutoff_date[1] = int(input_month)
                            max_days_in_month = Deleting.calc_days_in_month(int(self.cutoff_date[1]))
                            if int(self.cutoff_date[0]) > max_days_in_month:
                                self.cutoff_date[0] = str(max_days_in_month)
                            if self.selected_language == "en":
                                Tools.add_colored_line(console,"Date changed to: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green",None,True)
                            else:
                                Tools.add_colored_line(console,"Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green",None,True)
                            max_days_entry.delete(0,"100")
                            max_days_entry.insert(0,Deleting.get_max_days(self.cutoff_date))
                        else:
                            if self.selected_language == "en":
                                Tools.add_colored_line(console,"Month: " + str(input_month) + " is out of range","red",None,True)
                            else:
                                Tools.add_colored_line(console,"Měsíc: " + str(input_month) + " je mimo rozsah","red",None,True)
                    else:
                        if self.selected_language == "en":
                            Tools.add_colored_line(console, "You did not enter a number for the month settings","red",None,True)
                        else:
                            Tools.add_colored_line(console, "U nastavení měsíce jste nezadali číslo","red",None,True)

                input_day = set_day.get()
                max_days_in_month = Deleting.calc_days_in_month(int(self.cutoff_date[1]))

                if input_day != "":
                    if input_day.isdigit():
                        if int(input_day) <= int(max_days_in_month) and int(input_day) > 0:
                            self.cutoff_date[0] = int(input_day)
                            if self.selected_language == "en":
                                Tools.add_colored_line(console, "Date changed to: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green",None,True)
                            else:
                                Tools.add_colored_line(console, "Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green",None,True)
                            max_days_entry.delete(0,"100")
                            max_days_entry.insert(0,Deleting.get_max_days(self.cutoff_date))
                        else:
                            if self.selected_language == "en":
                                Tools.add_colored_line(console, "Day: " + str(input_day) + " is out of range","red",None,True)
                            else:
                                Tools.add_colored_line(console, "Den: " + str(input_day) + " je mimo rozsah","red",None,True)
                    else:
                        if self.selected_language == "en":
                            Tools.add_colored_line(console, "You did not enter a number for the day settings","red",None,True)
                        else:
                            Tools.add_colored_line(console, "U nastavení dne jste nezadali číslo","red",None,True)

                input_year = set_year.get()
                if input_year != "":
                    if input_year.isdigit():
                        if len(str(input_year)) == 2:
                            self.cutoff_date[2] = int(input_year) + 2000
                            if self.selected_language == "en":
                                Tools.add_colored_line(console,  "Date changed to: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green",None,True)
                            else:
                                Tools.add_colored_line(console,  "Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green",None,True)
                            max_days_entry.delete(0,"100")
                            max_days_entry.insert(0,Deleting.get_max_days(self.cutoff_date))
                        elif len(str(input_year)) == 4:
                            self.cutoff_date[2] = int(input_year)
                            if self.selected_language == "en":
                                Tools.add_colored_line(console,  "Date changed to: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green",None,True)
                            else:
                                Tools.add_colored_line(console,  "Datum přenastaveno na: "+ str(self.cutoff_date[0])+ "."+str(self.cutoff_date[1])+"."+ str(self.cutoff_date[2]),"green",None,True)
                            max_days_entry.delete(0,"100")
                            max_days_entry.insert(0,Deleting.get_max_days(self.cutoff_date))
                        else:
                            if self.selected_language == "en":
                                Tools.add_colored_line(console, "Year: " + str(input_year) + " is out of range","red",None,True)
                            else:
                                Tools.add_colored_line(console, "Rok: " + str(input_year) + " je mimo rozsah","red",None,True)
                    else:
                        if self.selected_language == "en":
                            Tools.add_colored_line(console, "You did not enter a number for the year settings","red",None,True)
                        else:
                            Tools.add_colored_line(console, "U nastavení roku jste nezadali číslo","red",None,True)

            def insert_current_date():
                today = Deleting.get_current_date()
                today_split = today[1].split(".")
                i=0
                for items in today_split:
                    i+=1
                    self.cutoff_date[i-1]=items
                set_day.delete(0,"100")
                set_month.delete(0,"100")
                set_year.delete(0,"100")
                set_day.insert(0,self.cutoff_date[0])
                set_month.insert(0,self.cutoff_date[1])
                set_year.insert(0,self.cutoff_date[2])
                max_days_entry.delete(0,"100")
                max_days_entry.insert(0,Deleting.get_max_days(self.cutoff_date))
                if self.selected_language == "en":
                    Tools.add_colored_line(console, "Today's date has been inserted (currently all directories are evaluated as older!)","orange",None,True)
                else:
                    Tools.add_colored_line(console, "Bylo vloženo dnešní datum (Momentálně jsou všechny adresáře vyhodnoceny, jako starší!)","orange",None,True)

            def save_before_execution():
                input_month = set_month.get()
                if input_month != "":
                    if input_month.isdigit():
                        if int(input_month) < 13 and int(input_month) > 0:
                            self.cutoff_date[1] = int(input_month)
                            max_days_in_month = Deleting.calc_days_in_month(int(self.cutoff_date[1]))
                            if int(self.cutoff_date[0]) > max_days_in_month:
                                self.cutoff_date[0] = str(max_days_in_month)

                input_day = set_day.get()
                max_days_in_month = Deleting.calc_days_in_month(int(self.cutoff_date[1]))
                if input_day != "":
                    if input_day.isdigit():
                        if int(input_day) <= int(max_days_in_month) and int(input_day) > 0:
                            self.cutoff_date[0] = int(input_day)

                input_year = set_year.get()
                if input_year != "":
                    if input_year.isdigit():
                        if len(str(input_year)) == 2:
                            self.cutoff_date[2] = int(input_year) + 2000
                        elif len(str(input_year)) == 4:
                            self.cutoff_date[2] = int(input_year)

            def set_max_days(flag=""):
                if flag == "cutoff":
                    new_cutoff = Deleting.get_cutoff_date(int(max_days_entry.get()))
                    set_day.delete(0,"100")
                    set_month.delete(0,"100")
                    set_year.delete(0,"100")
                    set_day.insert(0,new_cutoff[0])
                    set_month.insert(0,new_cutoff[1])
                    set_year.insert(0,new_cutoff[2])
                    set_cutoff_date()
                elif flag == "max_days":
                    set_cutoff_date()
            
            def update_entry(event,flag=""):
                if flag == "cutoff":
                    self.root.after(100, lambda: set_max_days(flag))
                elif flag == "max_days":
                    self.root.after(100, lambda: set_max_days(flag))
                elif flag == "ftk":
                    self.root.after(100, lambda: set_files_to_keep())

            def set_testing_mode():
                if self.checkbox_testing.get() == 1:
                    self.testing_mode = True
                else:
                    self.testing_mode = False

            def set_decision_date(input_arg):
                """
                input_arg:
                - creation
                - modification
                """

                if input_arg == "creation":
                    self.by_creation_date = True
                    checkbox_modification_date.deselect()

                elif input_arg == "modification":
                    self.by_creation_date = False
                    checkbox_creation_date.deselect()

            def set_files_to_keep():
                input_files_to_keep = files_to_keep_set.get()
                if input_files_to_keep.isdigit():
                    if int(input_files_to_keep) >= 0:
                        self.directories_to_keep = int(input_files_to_keep)
                        if self.selected_language == "en":
                            summary_label.configure(text= f"Directories (including all subdirectories) that are evaluated as older than the set date will be deleted\nwhile retaining the minimum number of directories: {input_files_to_keep}")
                            Tools.add_colored_line(console, "Number of older directories left set to: " + str(input_files_to_keep),"green",None,True)
                        else:
                            summary_label.configure(text= f"Budou smazány adresáře (včetně všech subadresářů), které jsou vyhodnoceny jako starší než nastavené datum\npřičemž bude ponechán minimální počet složek: {input_files_to_keep}")
                            Tools.add_colored_line(console, "Počet ponechaných starších adresářů nastaven na: " + str(input_files_to_keep),"green",None,True)
                    else:
                        if self.selected_language == "en":
                            Tools.add_colored_line(console, "Out of range","red",None,True)
                        else:
                            Tools.add_colored_line(console, "Mimo rozsah","red",None,True)
                else:
                    if self.selected_language == "en":
                        Tools.add_colored_line(console, "You didn't enter a number","red",None,True)
                    else:
                        Tools.add_colored_line(console, "Nazadali jste číslo","red",None,True)


            top_frame = customtkinter.CTkFrame(master=self.changable_frame,corner_radius=0,fg_color="#212121",height=240)
            left_side = customtkinter.CTkFrame(master=top_frame,corner_radius=0,fg_color="#212121")
            right_side = customtkinter.CTkFrame(master=top_frame,corner_radius=0,fg_color="#212121")
            header_frame = customtkinter.CTkFrame(master=left_side,corner_radius=0,fg_color="#212121")
            option_title = customtkinter.CTkLabel(master = header_frame,text = "Mazání adresářů podle data v jejich názvu",justify = "left",font=("Arial",25,"bold"))
            today = Deleting.get_current_date()
            current_date = customtkinter.CTkLabel(master = header_frame,text = "Dnešní datum: "+today[1],justify = "left",font=("Arial",20,"bold"),bg_color="black")
            option_title.pack(padx=10,pady=(10),side="left",anchor="w")
            current_date.pack(padx=3,pady=(0,0),side="left",anchor="e",expand = True,fill="y",ipadx = 10)
            header_frame.pack(padx=0,pady=(0,0),side="top",anchor="w",fill="x",expand=False)
            user_input_frame = customtkinter.CTkFrame(master=left_side,corner_radius=0,fg_color="#212121",border_width=4,border_color="#636363")
            date_input_frame = customtkinter.CTkFrame(master=user_input_frame,corner_radius=0,fg_color="#212121")
            date_label = customtkinter.CTkLabel(master = date_input_frame,text = "‣ budou smazány adresáře starší než nastavené datum:",justify = "left",font=("Arial",20))
            set_day     = customtkinter.CTkEntry(master = date_input_frame,width=40,font=("Arial",20), placeholder_text= self.cutoff_date[0])
            sep1        = customtkinter.CTkLabel(master = date_input_frame,width=10,text = ".",font=("Arial",20))
            set_month   = customtkinter.CTkEntry(master = date_input_frame,width=40,font=("Arial",20), placeholder_text= self.cutoff_date[1])
            sep2        = customtkinter.CTkLabel(master = date_input_frame,width=10,text = ".",font=("Arial",20))
            set_year    = customtkinter.CTkEntry(master = date_input_frame,width=60,font=("Arial",20), placeholder_text= self.cutoff_date[2])
            insert_button = customtkinter.CTkButton(master = date_input_frame,width=190, text = "Vložit dnešní datum", command = lambda: insert_current_date(),font=("Arial",20,"bold"))
            date_label. pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            set_day.    pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            sep1.       pack(padx=(5,0),pady=(0,0),side="left",anchor="w")
            set_month.  pack(padx=(5,0),pady=(0,0),side="left",anchor="w")
            sep2.       pack(padx=(5,0),pady=(0,0),side="left",anchor="w")
            set_year.   pack(padx=(5,0),pady=(0,0),side="left",anchor="w")
            insert_button.   pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            date_input_frame.pack(padx=5,pady=(10,0),side="top",anchor="w")
            set_day.bind("<Key>",lambda e: update_entry(e,flag="max_days"))
            set_month.bind("<Key>",lambda e: update_entry(e,flag="max_days"))
            set_year.bind("<Key>",lambda e: update_entry(e,flag="max_days"))

            day_format_input_frame = customtkinter.CTkFrame(master=user_input_frame,corner_radius=0,fg_color="#212121")
            days_label = customtkinter.CTkLabel(master = day_format_input_frame,text = "‣ to znamená starší než:",justify = "left",font=("Arial",20))
            max_days_entry = customtkinter.CTkEntry(master = day_format_input_frame,width=60,font=("Arial",20))
            max_days_entry.insert(0,Deleting.get_max_days(self.cutoff_date))
            days_label2 = customtkinter.CTkLabel(master = day_format_input_frame,text = "dní",justify = "left",font=("Arial",20))
            days_label. pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            max_days_entry. pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            days_label2. pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            day_format_input_frame.pack(padx=5,pady=(0,10),side="top",anchor="w")
            if option == 4:
                day_format_input_frame.pack(padx=5,pady=(0,0),side="top",anchor="w")
            max_days_entry.bind("<Key>",lambda e: update_entry(e,flag="cutoff"))

            ftk_frame = customtkinter.CTkFrame(master=user_input_frame,corner_radius=0,fg_color="#212121")
            ftk_label = customtkinter.CTkLabel(master = ftk_frame,text = "‣ přičemž bude ponecháno:",justify = "left",font=("Arial",20))
            files_to_keep_set = customtkinter.CTkEntry(master = ftk_frame,width=70,font=("Arial",20), placeholder_text= self.directories_to_keep)
            ftk_label2 = customtkinter.CTkLabel(master = ftk_frame,text = "adresářů, vyhodnocených, jako starších",justify = "left",font=("Arial",20))
            ftk_label. pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            files_to_keep_set. pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            ftk_label2. pack(padx=(10,0),pady=(0,0),side="left",anchor="w")
            if option == 4:
                ftk_frame.pack(padx=5,pady=(0,10),side="top",anchor="w")
                files_to_keep_set.bind("<Key>",lambda e: update_entry(e,flag="ftk"))
                files_to_keep_set.insert(0,self.directories_to_keep)

            directories_image = customtkinter.CTkImage(Image.open(Tools.resource_path("images/directories.png")),size=(240, 190))
            image_description = customtkinter.CTkLabel(master = right_side,text = "Ukázka:",font=("Arial",20,"bold"))
            images_label = customtkinter.CTkLabel(master = right_side,text = "",image=directories_image)
            image_description.pack(padx=10,pady=(10),side="top",anchor="w")
            images_label.pack(padx=10,pady=(10),side="top",anchor="w")
            user_input_frame.pack(padx=5,pady=(0,0),side="top",anchor="w",fill="x")
            summary_label = customtkinter.CTkLabel(master = left_side,text = f"Budou smazány jen adresáře (včetně všech subadresářů), které obsahují v názvu podporovaný formát datumu\na jsou vyhodnoceny jako starší než nastavené datum",justify = "left",font=("Arial",20,"bold"))
            summary_label.pack(padx=10,pady=(10,0),side="top",anchor="w")

            deletable_formats = customtkinter.CTkLabel(master = left_side,text = f"Podporované datumové formáty: {Deleting.supported_date_formats}\nPodporované separátory datumu: {Deleting.supported_separators}",justify = "left",font=("Arial",20))
            if option == 3:
                deletable_formats.pack(padx=10,pady=(10,0),side="top",anchor="w")
                left_side.pack(padx=0,pady=(0),side="left",anchor="n",expand=True,fill="x")
                right_side.pack(padx=0,pady=(0),side="left",anchor="w",expand=False)        
            else:
                left_side.pack(padx=0,pady=(0),side="left",anchor="n",expand=True,fill="x")

            top_frame.pack(padx=0,pady=(0),side="top",anchor="w",fill="x")
            top_frame.propagate(False)
            console = tk.Text(self.changable_frame, wrap="none", height=0, width=30,background="black",font=("Arial",22),state=tk.DISABLED)
            console.pack(pady = (10,0),padx =10,side="top",anchor="w",fill="x")

            self.checkbox_testing = customtkinter.CTkCheckBox(master =self.changable_frame, text = f"Režim TESTOVÁNÍ (Soubory vyhodnocené ke smazání se pouze přesunou do složky s názvem: \"{self.to_delete_folder_name}\")",font=("Arial",18,"bold"),command=lambda:set_testing_mode())
            self.checkbox_testing.pack(pady = (10,0),padx =10,side="top",anchor="w")

            decision_date_frame = customtkinter.CTkFrame(master=self.changable_frame,corner_radius=0,fg_color="#212121")
            decision_date_label = customtkinter.CTkLabel(master = decision_date_frame,text = "Řídit se podle: ",justify = "left",font=("Arial",20,"bold"))
            checkbox_creation_date = customtkinter.CTkCheckBox(master =decision_date_frame, text = "data vytvoření",font=("Arial",18),command=lambda:set_decision_date("creation"))
            checkbox_modification_date = customtkinter.CTkCheckBox(master =decision_date_frame, text = "data poslední změny (doporučeno)",font=("Arial",18),command=lambda:set_decision_date("modification"))
            decision_date_label.pack(pady = (10,0),padx =(10,0),side="left",anchor="w")
            checkbox_creation_date.pack(pady = (10,0),padx =(10,0),side="left",anchor="w")
            checkbox_modification_date.pack(pady = (10,0),padx =(10,0),side="left",anchor="w")
            if option == 4:
                decision_date_frame.pack(pady = (0,0),padx =0,side="top",anchor="w",fill="x")
                if self.by_creation_date:
                    checkbox_creation_date.select()
                else:
                    checkbox_modification_date.select()
            if self.testing_mode:
                self.checkbox_testing.select()
        
            if self.selected_language == "en":
                option_title.configure(text= "Delete directories by date in their name")
                date_label.configure(text= "‣ directories older than the set date will be deleted:")
                insert_button.configure(text= "Insert today's date")
                days_label.configure(text= "‣ it means older than:")
                days_label2.configure(text= "days")
                ftk_label.configure(text= "‣ whereby it will be retained:")
                ftk_label2.configure(text= "directories, evaluated as older")
                image_description.configure(text= "Example:")
                summary_label.configure(text= "Only directories (including all subdirectories) that contain a supported date format in their name and are evaluated as older than the set date will be deleted")
                deletable_formats.configure(text= f"Supported date formats: {Deleting.supported_date_formats}\nSupported date separators: {Deleting.supported_separators}")
                self.checkbox_testing.configure(text= f"TEST mode (Files evaluated for deletion are only moved to a folder named: \"{self.to_delete_folder_name}\")")
                current_date.configure(text = "Current date: "+today[1])

            if option == 4:
                self.selected_option =4
                option_title.configure(text = "Mazání adresářů starších než: nastavené datum")
                summary_label.configure(text= f"Budou smazány adresáře (včetně všech subadresářů), které jsou vyhodnoceny jako starší než nastavené datum\npřičemž bude ponechán minimální počet složek: {self.directories_to_keep}")
                if self.selected_language == "en":
                    option_title.configure(text = "Deleting directories older than: set date")
                    summary_label.configure(text= f"Directories (including all subdirectories) that are evaluated as older than the set date will be deleted\nwhile retaining the minimum number of directories: {self.directories_to_keep}")
                    decision_date_label.configure(text = "To decide by:")
                    checkbox_creation_date.configure(text = "date of creation")
                    checkbox_modification_date.configure(text = "date of modification (recommended)")
                self.options1.deselect()
                self.options2.deselect()
                self.options3.deselect()
                self.options4.select()
            else:
                self.selected_option =3
                self.options1.deselect()
                self.options2.deselect()
                self.options3.select()
                self.options4.deselect()
            
            def new_date_enter_btn(e):
                set_cutoff_date()
            set_day.bind("<Return>",new_date_enter_btn)
            set_month.bind("<Return>",new_date_enter_btn)
            set_year.bind("<Return>",new_date_enter_btn)

            # self.changable_frame.bind("<Enter>",lambda e: save_before_execution()) # případ, že se nestiskne uložit - aby nedošlo ke ztrátě souborů

        def create_deleting_option_widgets(self):  # Vytváří veškeré widgets (delete option MAIN)
            def call_path_context_menu(event):
                path_history = Tools.read_json_config()["del_settings"]["path_history_list"]
                def insert_path(path):
                    self.path_set.delete("0","200")
                    self.path_set.insert("0", path)
                if len(path_history) > 0:
                    path_context_menu = tk.Menu(self.root, tearoff=0,fg="white",bg="black")
                    for i in range(0,len(path_history)):
                        path_context_menu.add_command(label=path_history[i], command=lambda row_path = path_history[i]: insert_path(row_path),font=("Arial",22,"bold"))
                        if i < len(path_history)-1:
                            path_context_menu.add_separator()
                            
                    path_context_menu.tk_popup(context_menu_button.winfo_rootx(),context_menu_button.winfo_rooty()+50)

            header_frame =          customtkinter.CTkFrame(master=self.root,corner_radius=0,fg_color="#212121")
            top_frame =             customtkinter.CTkFrame(master=header_frame,corner_radius=0,fg_color="#212121")
            frame_with_cards =      customtkinter.CTkFrame(master=top_frame,corner_radius=0,fg_color="#636363",height=100)

            menu_button =       customtkinter.CTkButton(master = frame_with_cards, width = 250,height=50,text = "MENU",           command = lambda: self.call_extern_function(function="menu"),
                                                        font=("Arial",20,"bold"),corner_radius=0,fg_color="black",hover_color="#212121")
            sorting_button =    customtkinter.CTkButton(master = frame_with_cards, width = 250,height=50,text = "Třídění souborů",command = lambda: self.call_extern_function(function="sorting"),
                                                        font=("Arial",20,"bold"),corner_radius=0,fg_color="black",hover_color="#212121")
            deleting_button =   customtkinter.CTkButton(master = frame_with_cards, width = 250,height=50,text = "Mazání souborů",
                                                        font=("Arial",20,"bold"),corner_radius=0,fg_color="#212121",hover_color="#212121")
            converting_button = customtkinter.CTkButton(master = frame_with_cards, width = 250,height=50,text = "Konvertování souborů",command = lambda: self.call_extern_function(function="converting"),
                                                        font=("Arial",20,"bold"),corner_radius=0,fg_color="black",hover_color="#212121")
            menu_button.        pack(pady = (10,0),padx =(10,0),anchor = "s",side = "left")
            sorting_button.     pack(pady = (10,0),padx =(10,0),anchor = "s",side = "left")
            deleting_button.    pack(pady = (10,0),padx =(10,0),anchor = "s",side = "left")
            converting_button.  pack(pady = (10,0),padx =(10,0),anchor = "s",side = "left")

            frame_with_cards.       pack(pady=0,padx=0,fill="both",expand=True,side = "left",anchor="w")
            frame_with_logo =       customtkinter.CTkFrame(master=top_frame,corner_radius=0)
            logo =                  customtkinter.CTkImage(Image.open(Tools.resource_path("images/jhv_logo.png")),size=(300, 100))
            image_logo =            customtkinter.CTkLabel(master = frame_with_logo,text = "",image =logo)
            frame_with_logo.        pack(pady=0,padx=0,expand=False,side = "left",anchor="e")
            image_logo.             pack(pady = 0,padx =(15,0),ipadx = 20,ipady = 30,expand=False)
            top_frame.              pack(pady=0,padx=0,fill="x",side = "top")

            frame_path_input =      customtkinter.CTkFrame(master=header_frame,corner_radius=0)
            context_menu_button  =  customtkinter.CTkButton(master =frame_path_input, width = 50,height=50, text = "V",font=("Arial",20,"bold"),corner_radius=0,fg_color="#505050")
            self.path_set    =      customtkinter.CTkEntry(master =frame_path_input,height=50,font=("Arial",20),corner_radius=0)
            tree        =           customtkinter.CTkButton(master =frame_path_input,height=50,width = 180,text = "EXPLORER", command = self.call_browseDirectories,font=("Arial",20,"bold"))
            button_save_path =      customtkinter.CTkButton(master =frame_path_input,height=50,text = "Uložit cestu", command = lambda: Tools.save_path(self.console,self.path_set.get(),"del_settings"),font=("Arial",20,"bold"))
            button_open_setting =   customtkinter.CTkButton(master =frame_path_input,height=50,width=50, text = "⚙️", command = lambda: Advanced_option(self.root,windowed=True,spec_location="deleting_option"),font=(None,20))
            context_menu_button.    pack(pady = 10,padx =(10,0),anchor ="w",side = "left")
            self.path_set.          pack(pady = 10,padx =(0,0),anchor ="w",side = "left",fill="both",expand=True)
            tree.                   pack(pady = 10,padx =(10,0),anchor ="w",side = "left")
            button_save_path.       pack(pady = 10,padx =(10,0),anchor ="w",side = "left")
            button_open_setting.    pack(pady = 10,padx =(10,10),anchor = "w",side = "left")
            frame_path_input.       pack(pady=0,padx=0,fill="both",side = "top")
            context_menu_button.bind("<Button-1>", call_path_context_menu)

            double_frame =          customtkinter.CTkFrame(master=header_frame,corner_radius=0,height=400,fg_color="#212121",border_width=2,border_color="#636363")
            option_menu_cards =     customtkinter.CTkFrame(master=double_frame,corner_radius=0,fg_color="#212121",border_width=2,border_color="#636363")
            self.options1 =         customtkinter.CTkCheckBox(master = option_menu_cards,text = "Možnost 1",font=("Arial",20,"bold"),corner_radius=0,command = lambda: self.selected(option=1))
            self.options2 =         customtkinter.CTkCheckBox(master = option_menu_cards,text = "Možnost 2",font=("Arial",20,"bold"),corner_radius=0,command = lambda: self.selected(option=2))
            self.options3 =         customtkinter.CTkCheckBox(master = option_menu_cards,text = "Možnost 3",font=("Arial",20,"bold"),corner_radius=0,command = lambda: self.selected3(option = 3))
            self.options4 =         customtkinter.CTkCheckBox(master = option_menu_cards,text = "Možnost 4",font=("Arial",20,"bold"),corner_radius=0,command = lambda: self.selected3(option = 4))
            self.options1.          pack(pady = (10,0),padx =(10,15),anchor = "w",side = "top")
            self.options2.          pack(pady = (10,0),padx =(10,15),anchor = "w",side = "top")
            self.options3.          pack(pady = (10,0),padx =(10,15),anchor = "w",side = "top")
            self.options4.          pack(pady = (10,0),padx =(10,15),anchor = "w",side = "top")

            self.changable_frame =  customtkinter.CTkFrame(master=double_frame,corner_radius=0,fg_color="#212121")
            option_menu_cards.      pack(pady=0,padx=0,fill="y",side = "left")
            self.changable_frame.   pack(pady=(2,0),padx=(0,2),fill="x",side = "left",expand=True,anchor="n")
            double_frame.           pack(pady=0,padx=0,fill="x",side = "top",anchor="w")
            double_frame.           propagate(False)
            
            def call_start(analyze=False):
                run_background = threading.Thread(target=self.start, args=(analyze,))
                run_background.start()
                # self.start(only_analyze=True)

            bottom_frame =          customtkinter.CTkFrame(master=header_frame,corner_radius=0,fg_color="#212121",border_width=0,border_color="#636363")
            execution_btn_frame =   customtkinter.CTkFrame(master=bottom_frame,corner_radius=0,fg_color="#212121")
            button =                customtkinter.CTkButton(master = execution_btn_frame,width = 300,height = 60,text = "SPUSTIT", command = lambda: call_start(),font=("Arial",20,"bold"))
            create_task_btn =       customtkinter.CTkButton(master = execution_btn_frame,width = 300,height = 60,text = "Nastavit aut. spouštění",
                                                            command = lambda: Subwindows.save_new_task(self.selected_option,
                                                                                                        self.by_creation_date,
                                                                                                        self.path_set.get(),
                                                                                                        self.cutoff_date,
                                                                                                        self.files_to_keep,
                                                                                                        self.directories_to_keep,
                                                                                                        self.more_dirs,
                                                                                                        selected_language=self.selected_language,
                                                                                                        main_root = self.root),font=("Arial",20,"bold"))
            analyze_btn =           customtkinter.CTkButton(master = execution_btn_frame,width = 300,height = 60,text = "Analyzovat cestu",command = lambda: call_start(analyze=True),font=("Arial",20,"bold"))
            button.                 pack(pady=10,padx=(10,0),side="left",anchor="w")
            create_task_btn.        pack(pady=10,padx=(10,0),side="left",anchor="w")
            analyze_btn.            pack(pady=10,padx=(10,0),side="left",anchor="w")
            self.console =          tk.Text(bottom_frame, wrap="word",background="black",font=("Arial",16),state=tk.DISABLED)
            execution_btn_frame.    pack(pady =3,padx=3,side = "top",anchor="n")
            self.console.           pack(pady =0,padx=(10,0),side = "left",fill="both",expand=True)
            bottom_frame .          pack(pady =0,padx=0,side = "top",fill="both",expand=True)
            header_frame.           pack(pady=0,padx=0,fill="both",side = "top",expand=True)
            self.selected(option=1)
            self.options1.select()

            scrollbar = tk.Scrollbar(bottom_frame, command=self.console.yview)
            scrollbar.pack(side="right", fill="y")
            self.console.config(yscrollcommand=scrollbar.set)

            if self.selected_language == "en":
                deleting_button.configure(text = "File deletion")
                button_save_path.configure(text = "Save path")
                self.options1.configure(text = "Option 1")
                self.options2.configure(text = "Option 2")
                self.options3.configure(text = "Option 3")
                self.options4.configure(text = "Option 4")
                # current_date.configure(text = "Current date: "+today[1])
                button.configure(text = "EXECUTE")
                create_task_btn.configure(text = "Set auto. boot")
                analyze_btn.configure(text = "Analyze path")

            if global_recources_load_error:
                create_task_btn.configure(state = "disabled")

            recources_path = self.config_data["app_settings"]["default_path"]
            if len(self.config_data["del_settings"]["path_history_list"]) != 0:
                path_from_history = self.config_data["del_settings"]["path_history_list"][0]
                self.path_set.delete("0","200")
                self.path_set.insert("0", path_from_history)
                Tools.add_colored_line(self.console,"Byla vložena cesta z konfiguračního souboru","white",None,True)
                self.root.update_idletasks()
            elif recources_path != False and recources_path != "/":
                self.path_set.delete("0","200")
                self.path_set.insert("0", str(recources_path))
                if self.selected_language == "en":
                    Tools.add_colored_line(self.console,"The path from the configuration file has been inserted","white")
                else:
                    Tools.add_colored_line(self.console,"Byla vložena cesta z konfiguračního souboru","white")
            else:
                if self.selected_language == "en":
                    Tools.add_colored_line(self.console,"The configuration file contains an invalid file path (you can insert in advanced settings)","orange")
                else:
                    Tools.add_colored_line(self.console,"Konfigurační soubor obsahuje neplatnou cestu k souborům (můžete vložit v pokročilém nastavení)","orange")
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
        def __init__(self,root):
            self.root = root
            self.aut_detect_num_of_pallets = True
            self.by_which_ID_num = ""   
            self.more_dirs = False
            self.unbind_list = []
            self.config_data = Tools.read_json_config()
            self.supported_formats_sorting = self.config_data["sort_conv_settings"]["supported_formats_sorting"]
            self.prefix_func = self.config_data["sort_conv_settings"]["prefix_function"]
            self.prefix_Cam = self.config_data["sort_conv_settings"]["prefix_camera"]
            self.max_num_of_pallets = self.config_data["sort_conv_settings"]["max_pallets"]
            self.safe_mode = self.config_data["sort_conv_settings"]["sorting_safe_mode"]
            self.nok_folder_name = self.config_data["sort_conv_settings"]["temp_dir_name"]
            self.pairs_folder_name = self.config_data["sort_conv_settings"]["pairs_dir_name"]
            self.sort_inside_pair_folder = True
            self.temp_path_for_explorer = None
            self.original_image = Image.open(Tools.resource_path("images/loading3.png"))
            self.original_image = self.original_image.resize((300, 300))
            self.angle = 0

            self.create_sorting_option_widgets()

        def start(self):# Ověřování cesty, init, spuštění
            """
            Ověřování cesty, init, spuštění
            """
            Tools.clear_console(self.console)
            if self.checkbox.get()+self.checkbox2.get()+self.checkbox3.get()+self.checkbox4.get()+self.checkbox5.get() == 0:
                Tools.add_colored_line(self.console,"Nevybrali jste žádný způsob třídění :-)","red")
                nothing = customtkinter.CTkImage(Image.open(Tools.resource_path("images/nothing.png")),size=(1, 1))
                self.images.configure(image = nothing)
                self.name_example.configure(text = "")

            else:
                path = self.path_set.get() 
                if path != "":
                    check = Tools.path_check(path)
                    if check == False:
                        Tools.add_colored_line(self.console,"Zadaná cesta: "+str(path)+" nebyla nalezena","red")
                    else:
                        path = check
                        Tools.add_colored_line(self.console,"- Provádím nastavenou možnost třídění v cestě: "+str(path)+"\n","orange")
                        Tools.add_new_path_to_history(path,which_settings="sort_conv_settings")

                        self.console.update_idletasks()
                        self.root.update_idletasks()
                        self.sort_files(path)
                else:
                    Tools.add_colored_line(self.console,"Nebyla vložena cesta k souborům","red")

        def sort_files(self,path): # Volání externího scriptu
            selected_sort = 0
            self.loading_bar.set(value = 0)
            ignore_pairs = False

            only_one_subfolder = False
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
                if self.one_subfolder.get() == 1:
                    self.more_dirs = True
                    only_one_subfolder = True
            try:
                if self.checkbox_ignore_pairs.get() == 1 and selected_sort == 2:
                    ignore_pairs = True
            except Exception: # the checkbox was not even loaded once...
                pass

            if self.checkbox_safe_mode.get() == 1:
                self.safe_mode = "ne"
            else:
                self.safe_mode = "ano"

            popup = tk.Toplevel(master=root)
            popup.attributes('-topmost', True)
            geometry_string = "1000x1000+" + str(int(root.winfo_screenwidth()/2)-500)+ "+" + str(int(root.winfo_screenheight()/2)-500)
            popup.geometry(str(geometry_string))
            popup.label = tk.Label(popup)
            image_ = ImageTk.PhotoImage(self.original_image)
            popup.label.config(image=image_)  # Update label's image
            popup.label.image = image_  # Keep a reference to the image to prevent garbage collection
            popup.label.place(x=0, y=0, relwidth=1, relheight=1)
            popup.wm_attributes("-transparentcolor","white")# trick to force the bg transparent
            popup.config(bg= 'white')
            popup.label.config(bg= 'white')
            popup.overrideredirect(True)# hide the frame of a window
            popup.update()
            popup.label.update()

            def rotate_image():
                self.angle += 10  # Adjust the rotation speed as needed
                rotated_image = self.original_image.rotate(self.angle)
                image_ = ImageTk.PhotoImage(rotated_image)
                popup.label.config(image=image_)  # Update label's image
                popup.label.image = image_
                popup.update()

            def call_trideni_main(whole_instance):
                whole_instance.main()

            running_program = Trideni.whole_sorting_function(
                path,
                selected_sort,
                self.more_dirs,
                self.max_num_of_pallets,
                self.by_which_ID_num,
                self.prefix_func,
                self.prefix_Cam,
                self.supported_formats_sorting,
                self.aut_detect_num_of_pallets,
                self.nok_folder_name,
                self.pairs_folder_name,
                self.safe_mode,
                self.sort_inside_pair_folder,
                only_one_subfolder,
                ignore_pairs
            )

            run_background = threading.Thread(target=call_trideni_main, args=(running_program,))
            run_background.start()

            output_list_increment = 0
            completed = False
            output_text2 = ""
            previous_console2_text = []
            previous_progres = 0

            while not running_program.finish or completed == False:
                time.sleep(0.05)
                rotate_image()
                #progress bar:
                if running_program.progress != previous_progres:
                    self.loading_bar.set(value = running_program.progress/100)
                    self.root.update_idletasks()
                    root.update_idletasks()
                    self.frame5.update_idletasks()

                if len(running_program.output_list) > output_list_increment:
                    for i in range(0,len(running_program.output_list[output_list_increment])):
                        new_row = str(running_program.output_list[output_list_increment][i])
                        if "bylo dokončeno" in new_row or "byla dokončena" in new_row:
                            Tools.add_colored_line(self.console,str(new_row),"green",("Arial",16,"bold"))
                        elif "Chyba" in new_row or "Třídění ukončeno" in new_row or "Celkový počet duplikátů" in new_row:
                            Tools.add_colored_line(self.console,str(new_row),"red",("Arial",16,"bold"))
                        elif "Nepáry" in new_row:
                            Tools.add_colored_line(self.console,str(new_row),"orange",("Arial",16,"bold"))
                        elif "OK soubory" in new_row:
                            Tools.add_colored_line(self.console,str(new_row),"green",("Arial",16,"bold"))
                        else:
                            Tools.add_colored_line(self.console,str(new_row),"white")
                        self.console.update_idletasks()
                    self.root.update_idletasks()
                    output_list_increment+=1

                if running_program.output_console2 != previous_console2_text and len(running_program.output_console2) != 0:
                    for i in range(0,len(running_program.output_console2)):
                        output_text2 = output_text2 + running_program.output_console2[i] + "\n"
                    if output_text2 != "":
                        if "Chyba" in output_text2:
                            self.console2.configure(text = output_text2,text_color="red")
                        else:
                            self.console2.configure(text = output_text2,text_color="green")
                    self.console2.update_idletasks()
                    previous_console2_text = running_program.output_console2
                    output_text2 = ""

                if running_program.finish and len(running_program.output_list) == output_list_increment and running_program.output_console2 == previous_console2_text and int(self.loading_bar.get())== 1:
                    completed = True
            
            self.console.update_idletasks()
            run_background.join()
            popup.destroy()

        def clear_frame(self,frame): # mazání widgets v daném framu
            for widget in frame.winfo_children():
                widget.destroy()

        def selected(self): #Třídit podle typu souboru
            """
            Nastavení widgets pro třídění podle typu souboru (základní)
            """
            self.clear_frame(self.frame6)
            self.view_image(1)
            #self.console.configure(text = "")
            Tools.clear_console(self.console)
            self.checkbox2.deselect()
            self.checkbox3.deselect()
            self.checkbox4.deselect()
            self.checkbox5.deselect()

            label_fill = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=self.height_of_frame6+15,text = "",justify = "left",font=("Arial",12))
            label_fill.grid(column =0,row=0,pady =0,padx=10)
            
        def selected2(self): #Třídit podle čísla funkce (ID)
            """
            Nastavení widgets pro třídění podle čísla funkce
            """
            self.clear_frame(self.frame6)
            self.view_image(2)
            Tools.clear_console(self.console)
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

            label1          = customtkinter.CTkLabel(master = self.frame6,text = "Nastavte prefix adresářů:",justify = "left",font=("Arial",16))
            prefix_set      = customtkinter.CTkEntry(master = self.frame6,width=150,font=("Arial",16), placeholder_text= self.prefix_func)
            button_save1    = customtkinter.CTkButton(master = self.frame6,width=50, text = "Uložit", command = lambda: set_prefix(),font=("Arial",18,"bold"))
            console_frame6_1 = customtkinter.CTkLabel(master = self.frame6,text = " ",justify = "left",font=("Arial",18))
            label1.grid(column =0,row=0,sticky = tk.W,pady =5,padx=10)
            prefix_set.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)
            button_save1.grid(column =0,row=1,sticky = tk.W,pady =0,padx=160)
            console_frame6_1.grid(column =0,row=2,sticky = tk.W,pady =0,padx=10)
            prefix_set.insert("0", str(self.prefix_func))
            def prefix_enter_btn(e):
                set_prefix()
            prefix_set.bind("<Return>",prefix_enter_btn)
            checkbox_advance = customtkinter.CTkCheckBox(master = self.frame6,font=("Arial",16), text = "Pokročilá nastavení",command = self.selected2_advance)
            label_fill         = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=167,text = "",justify = "left",font=("Arial",16))
            checkbox_advance.grid(column =0,row=4,sticky = tk.W,pady =10,padx=10)
            label_fill.grid(column =0,row=5,sticky = tk.W,pady =0,padx=10)

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

            label1           = customtkinter.CTkLabel(master = self.frame6,height=60,
                                            text = "Podle kterého čísla v ID se řídit:\nvolte první = 1 atd.\nprázdné = celé ID (aut. detekce)",
                                            justify = "left",font=("Arial",16))
            num_set          = customtkinter.CTkEntry(master = self.frame6,height=30,width=150,font=("Arial",16), placeholder_text= self.by_which_ID_num)
            button_save1     = customtkinter.CTkButton(master = self.frame6,height=30,width=50, text = "Uložit", command = lambda: set_which_num_of_ID(),font=("Arial",18,"bold"))
            console_frame6_1 = customtkinter.CTkLabel(master = self.frame6,height=30,text = " ",justify = "left",font=("Arial",18))
            self.checkbox_ignore_pairs = customtkinter.CTkCheckBox(master = self.frame6,height=30,font=("Arial",16), text = "Ignorovat páry (Třídit pouze podle id)")
            button_back      = customtkinter.CTkButton(master = self.frame6,width=100,height=30, text = "Zpět", command = self.selected2,font=("Arial",18,"bold"))
            label_fill          = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=115,text = "",justify = "left",font=("Arial",16))
            label1.grid(column =0,row=0,sticky = tk.W,pady =5,padx=10)
            num_set.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)
            button_save1.grid(column =0,row=1,sticky = tk.W,pady =0,padx=160)
            console_frame6_1.grid(column =0,row=2,sticky = tk.W,pady =5,padx=10)  
            self.checkbox_ignore_pairs.grid(column =0,row=3,sticky = tk.W,pady =(0,10),padx=10)
            button_back.grid(column =0,row=5,sticky = tk.W,pady =10,padx=10)
            label_fill.grid(column =0,row=6,sticky = tk.W,pady =0,padx=10)
            def which_id_num_enter_btn(e):
                set_which_num_of_ID()
            num_set.bind("<Return>",which_id_num_enter_btn)
            
        def selected3(self): #Třídit podle čísla kamery
            """
            Nastavení widgets pro třídění podle čísla kamery
            """
            self.clear_frame(self.frame6)
            Tools.clear_console(self.console)
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

            label1       = customtkinter.CTkLabel(master = self.frame6,height=20,text = "Nastavte prefix adresářů:",justify = "left",font=("Arial",16))
            prefix_set   = customtkinter.CTkEntry(master = self.frame6,height=30,width=150,font=("Arial",16), placeholder_text= self.prefix_Cam)
            button_save1 = customtkinter.CTkButton(master = self.frame6,height=30,width=50, text = "Uložit", command = lambda: set_prefix(),font=("Arial",18,"bold"))
            console_frame6_1 = customtkinter.CTkLabel(master = self.frame6,height=30,text = " ",justify = "left",font=("Arial",18))
            label_fill       = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=205,text = "",justify = "left",font=("Arial",16))
            label1.grid(column =0,row=0,sticky = tk.W,pady =5,padx=10)
            prefix_set.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)
            button_save1.grid(column =0,row=1,sticky = tk.W,pady =0,padx=160)
            console_frame6_1.grid(column =0,row=2,sticky = tk.W,pady =5,padx=10)
            label_fill.grid(column =0,row=3,pady =0,sticky = tk.W,padx=10)
            prefix_set.insert("0", str(self.prefix_Cam))
            def prefix_enter_btn(e):
                set_prefix()
            prefix_set.bind("<Return>",prefix_enter_btn)

        def selected4(self): #Třídit podle obojího (funkce, kamery)
            """
            Nastavení widgets pro třídění podle funkce i čísla kamery
            """
            self.clear_frame(self.frame6)
            #self.console.configure(text = "")
            Tools.clear_console(self.console)
            self.view_image(4)
            self.checkbox.deselect()
            self.checkbox2.deselect()
            self.checkbox3.deselect()
            self.checkbox5.deselect()

            label_fill = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=self.height_of_frame6+15,text = "",justify = "left",font=("Arial",12))
            label_fill.grid(column =0,row=0,pady =0,padx=10)

        def selected5(self): #hledani paru
            """
            Nastavení widgets pro hledání dvakrát vyfocených výrobků za sebou se stejným ID

            - nalezené dvojice nakopíruje do složky
            """
            self.clear_frame(self.frame6)
            Tools.clear_console(self.console)
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
                    console_frame6_1.configure(text = f"Počet palet nastaven na: {input_1}",text_color="green")
                    self.max_num_of_pallets = input_1
                    
            def set_aut_detect():
                if checkbox_aut_detect.get() == 1:
                    self.aut_detect_num_of_pallets = True
                else:
                    self.aut_detect_num_of_pallets = False

            def set_sorting_pair_folder():
                if sort_pair_folder.get() == 1:
                    self.sort_inside_pair_folder = True
                else:
                    self.sort_inside_pair_folder = False

            label1              = customtkinter.CTkLabel(master = self.frame6,height=20,text = "Nastavte počet palet v oběhu:",justify = "left",font=("Arial",16))
            pallets_set         = customtkinter.CTkEntry(master = self.frame6,width=150,height=30, placeholder_text= self.max_num_of_pallets,font=("Arial",16))
            button_save1        = customtkinter.CTkButton(master = self.frame6,width=50,height=30, text = "Uložit", command = lambda: set_max_pallet_num(),font=("Arial",18,"bold"))
            label_aut_detect    = customtkinter.CTkLabel(master = self.frame6,height=60,text = "Možnost aut. detekce:\n(případ, že v cestě nechybí nejvyšší ID)",justify = "left",font=("Arial",16))
            checkbox_aut_detect = customtkinter.CTkCheckBox(master = self.frame6,height=30,font=("Arial",16), text = "Automatická detekce",command=set_aut_detect)
            sort_pair_folder    = customtkinter.CTkCheckBox(master = self.frame6,height=90,font=("Arial",16), text = "Třídit uvnitř složky s páry\npodle typu souboru",command = lambda: set_sorting_pair_folder())
            console_frame6_1    = customtkinter.CTkLabel(master = self.frame6,height=30,text = " ",justify = "left",font=("Arial",18))
            label_fill              = customtkinter.CTkLabel(master = self.frame6,width=self.width_of_frame6,height=0,text = "",justify = "left",font=("Arial",12))
            label1.grid(column =0,row=0,sticky = tk.W,pady =5,padx=10)
            pallets_set.grid(column =0,row=1,sticky = tk.W,pady =0,padx=10)
            button_save1.grid(column =0,row=1,sticky = tk.W,pady =0,padx=160)
            console_frame6_1.grid(column =0,row=2,sticky = tk.W,pady =5,padx=10)
            label_aut_detect.grid(column =0,row=3,sticky = tk.W,pady =5,padx=10)
            checkbox_aut_detect.grid(column =0,row=4,sticky = tk.W,pady =0,padx=10)
            sort_pair_folder.grid(column =0,row=5,sticky = tk.W,pady =0,padx=10)
            label_fill.grid(column =0,row=6,pady =0,padx=10)
            checkbox_aut_detect.select()
            sort_pair_folder.select()
            self.sort_inside_pair_folder = True

            def max_pallets_num_enter_btn(e):
                set_max_pallet_num()
            pallets_set.bind("<Return>",max_pallets_num_enter_btn)

        def one_subfolder_checked(self): # checkbox na přepínání: procházet/ neprocházet 1 subsložku
            self.checkbox6.deselect()
            if self.one_subfolder.get() == 1:
                if self.checkbox_safe_mode.get()==1:
                    dir1sub = customtkinter.CTkImage(Image.open(Tools.resource_path("images/1sub_roz.png")),size=(522, 173))
                    self.images2.configure(image =dir1sub)
                    self.console2.configure(text = "Zadaná cesta/ 1.složka/ složky se soubory",text_color="white")
                else:
                    nodir1sub = customtkinter.CTkImage(Image.open(Tools.resource_path("images/1sub_vol.png")),size=(513, 142))
                    self.images2.configure(image =nodir1sub)
                    self.console2.configure(text = "Zadaná cesta/ 1.složka/ soubory volně, neroztříděné",text_color="white")
            else:
                if self.checkbox_safe_mode.get()==1:
                    dirsnosub = customtkinter.CTkImage(Image.open(Tools.resource_path("images/nosub_roz.png")),size=(432, 133))
                    self.images2.configure(image =dirsnosub)
                    self.console2.configure(text = "Zadaná cesta/ složky se soubory",text_color="white")
                else:
                    nodirsnosub = customtkinter.CTkImage(Image.open(Tools.resource_path("images/nosub_vol.png")),size=(253, 142))
                    self.images2.configure(image =nodirsnosub)
                    self.console2.configure(text = "Zadaná cesta/ soubory volně, neroztříděné",text_color="white")
        
        def two_subfolders_checked(self): # checkbox na přepínání: procházet/ neprocházet 2 subsložky
            self.one_subfolder.deselect()
            if self.checkbox6.get() == 1:
                if self.checkbox_safe_mode.get()==1:
                    dir2sub = customtkinter.CTkImage(Image.open(Tools.resource_path("images/2sub_roz.png")),size=(553, 111))
                    self.images2.configure(image =dir2sub)
                    self.console2.configure(text = "Zadaná cesta/ 1.složka/ 2.složka/ složky se soubory",text_color="white")
                else:
                    nodir2sub = customtkinter.CTkImage(Image.open(Tools.resource_path("images/2sub_vol.png")),size=(553, 111))
                    self.images2.configure(image =nodir2sub)
                    self.console2.configure(text = "Zadaná cesta/ 1.složka/ 2.složka/ soubory volně, neroztříděné",text_color="white")
            else:
                if self.checkbox_safe_mode.get()==1:
                    dirsnosub = customtkinter.CTkImage(Image.open(Tools.resource_path("images/nosub_roz.png")),size=(432, 133))
                    self.images2.configure(image =dirsnosub)
                    self.console2.configure(text = "Zadaná cesta/ složky se soubory",text_color="white")
                else:
                    nodirsnosub = customtkinter.CTkImage(Image.open(Tools.resource_path("images/nosub_vol.png")),size=(253, 142))
                    self.images2.configure(image =nodirsnosub)
                    self.console2.configure(text = "Zadaná cesta/ soubory volně, neroztříděné",text_color="white")
        
        def safe_mode_checked(self):
            if self.one_subfolder.get() == 1:
                self.one_subfolder_checked()
            else:
                self.two_subfolders_checked()
        
        def view_image(self,which_one): # zobrazení ilustračního obrázku
            """
            zobrazení ilustračního obrázku
            """
            if self.checkbox.get()+self.checkbox2.get()+self.checkbox3.get()+self.checkbox4.get()+self.checkbox5.get() == 0:
                nothing = customtkinter.CTkImage(Image.open(Tools.resource_path("images/nothing.png")),size=(1, 1))
                self.images.configure(image = nothing)
                self.name_example.configure(text = "")
            else:
                if which_one == 1:
                    type_24 = customtkinter.CTkImage(Image.open(Tools.resource_path("images/24_type.png")),size=(224, 85))
                    self.images.configure(image =type_24)
                    self.name_example.configure(text = f"221013_092241_0000000842_21_&Cam1Img  => .Height <=  .bmp\n(Podporované formáty:{self.supported_formats_sorting})")
                if which_one == 2:
                    func_24 = customtkinter.CTkImage(Image.open(Tools.resource_path("images/24_func.png")),size=(363, 85))
                    self.images.configure(image =func_24)
                    self.name_example.configure(text = f"221013_092241_0000000842_  => 21 <=  _&Cam1Img.Height.bmp\n(Podporované formáty:{self.supported_formats_sorting})")
                if which_one == 3:
                    cam_24 = customtkinter.CTkImage(Image.open(Tools.resource_path("images/24_cam.png")),size=(437, 85))
                    self.images.configure(image =cam_24)
                    self.name_example.configure(text = f"221013_092241_0000000842_21_&  => Cam1 <=  Img.Height.bmp\n(Podporované formáty:{self.supported_formats_sorting})")
                if which_one == 4:
                    both_24 = customtkinter.CTkImage(Image.open(Tools.resource_path("images/24_both.png")),size=(900, 170))
                    self.images.configure(image =both_24)
                    self.name_example.configure(text = f"221013_092241_0000000842_  => 21 <=  _&  => Cam1 <=  Img.Height.bmp\n(Podporované formáty:{self.supported_formats_sorting})")
                if which_one == 5:
                    PAIRS = customtkinter.CTkImage(Image.open(Tools.resource_path("images/25basic.png")),size=(265, 85))
                    self.images.configure(image =PAIRS)
                    self.name_example.configure(
                        text = f"Nakopíruje nalezené dvojice souborů do složky s názvem PAIRS (např. obsluha vloží dvakrát stejnou paletu po sobě před kameru)\n2023_04_13-07_11_09_xxxx_=> 0020 <=_&Cam2Img.Height.bmp\nFunkce postupuje podle časové známky v názvu souboru, kdy byly soubory pořízeny (podporované formáty:{self.supported_formats_sorting})")
        
        def call_extern_function(self,list_of_frames,function:str): # Tlačítko menu (konec, návrat do menu)
            """
            Funkce čistí všechny zaplněné rámečky a funguje, jako tlačítko zpět do menu\n
            function:
            - menu
            - (sorting)
            - deleting
            - converting
            """
            for frames in list_of_frames:
                frames.pack_forget()
                # frames.grid_forget()
                frames.destroy()
            
            for binds in self.unbind_list:
                self.root.unbind(binds)

            if function == "menu":
                menu.menu()
            elif function == "deleting":
                Deleting_option(self.root)
            elif function == "converting":
                Converting_option(self.root)

        def call_browseDirectories(self): # Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
            """
            Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
            """
            if os.path.exists(self.path_set.get()):
                self.temp_path_for_explorer = self.path_set.get()
            if self.checkbox6.get() == 1 or self.one_subfolder.get() == 1 or self.checkbox_safe_mode.get() == 1: # pokud je zvoleno more_dirs v exploreru pouze slozky...
                output = Tools.browseDirectories("only_dirs",self.temp_path_for_explorer)
            else:
                output = Tools.browseDirectories("all",self.temp_path_for_explorer)

            if str(output[1]) != "/":
                self.path_set.delete("0","200")
                self.path_set.insert("0", output[1])
                Tools.add_new_path_to_history(str(output[1]),which_settings="sort_conv_settings")
                Tools.add_colored_line(self.console,f"Byla vložena cesta: {output[1]}","green")
                self.temp_path_for_explorer = output[1]
            else:
                Tools.add_colored_line(self.console,str(output[0]),"red")

        def create_sorting_option_widgets(self):  # Vytváří veškeré widgets (sorting option MAIN)
            def call_path_context_menu(event):
                path_history = Tools.read_json_config()["sort_conv_settings"]["path_history_list"]
                def insert_path(path):
                    self.path_set.delete("0","200")
                    self.path_set.insert("0", path)
                if len(path_history) > 0:
                    path_context_menu = tk.Menu(self.root, tearoff=0,fg="white",bg="black")
                    for i in range(0,len(path_history)):
                        path_context_menu.add_command(label=path_history[i], command=lambda row_path = path_history[i]: insert_path(row_path),font=("Arial",22,"bold"))
                        if i < len(path_history)-1:
                            path_context_menu.add_separator()
                            
                    path_context_menu.tk_popup(context_menu_button.winfo_rootx(),context_menu_button.winfo_rooty()+50)

            frame_with_logo =       customtkinter.CTkFrame(master=self.root,corner_radius=0)
            logo =                  customtkinter.CTkImage(Image.open(Tools.resource_path("images/logo.png")),size=(1200, 100))
            image_logo =            customtkinter.CTkLabel(master = frame_with_logo,text = "",image =logo)
            frame_with_logo.        pack(pady=0,padx=0,fill="both",expand=False,side = "top")
            image_logo.pack()
            frame_with_cards = customtkinter.CTkFrame(master=self.root,corner_radius=0,fg_color="#636363",height=100)
            frame2 =        customtkinter.CTkFrame(master=self.root,corner_radius=0)
            upper_frame =   customtkinter.CTkFrame(master=self.root,corner_radius=0,fg_color="#636363")
            self.frame3 =   customtkinter.CTkFrame(master=upper_frame,corner_radius=0,width=400,height = 290,fg_color="#212121")
            self.frame4 =   customtkinter.CTkScrollableFrame(master=upper_frame,corner_radius=0,fg_color="#212121")
            self.frame5 =   customtkinter.CTkScrollableFrame(master=self.root,corner_radius=0)
            self.frame6 =   customtkinter.CTkFrame(master=upper_frame,corner_radius=0,fg_color="#212121")


            self.height_of_frame6 = 290
            self.width_of_frame6 = 370
            list_of_frames = [upper_frame,frame2,self.frame3,self.frame4,self.frame5,self.frame6,frame_with_cards,frame_with_logo]
            shift_const = 250
            menu_button =       customtkinter.CTkButton(master = frame_with_cards, width = 250,height=50,text = "MENU",                  command =  lambda: self.call_extern_function(list_of_frames,function="menu"),
                                                        font=("Arial",20,"bold"),corner_radius=0,fg_color="black",hover_color="#212121")
            sorting_button =    customtkinter.CTkButton(master = frame_with_cards, width = 250,height=50,text = "Třídění souborů",
                                                        font=("Arial",20,"bold"),corner_radius=0,fg_color="#212121",hover_color="#212121")
            deleting_button =   customtkinter.CTkButton(master = frame_with_cards, width = 250,height=50,text = "Mazání souborů",        command =  lambda: self.call_extern_function(list_of_frames,function="deleting"),
                                                        font=("Arial",20,"bold"),corner_radius=0,fg_color="black",hover_color="#212121")
            converting_button = customtkinter.CTkButton(master = frame_with_cards, width = 250,height=50,text = "Konvertování souborů",  command =  lambda: self.call_extern_function(list_of_frames,function="converting"),
                                                        font=("Arial",20,"bold"),corner_radius=0,fg_color="black",hover_color="#212121")
            menu_button.        grid(column = 0,row=0,pady = (10,0),padx =260-shift_const,sticky = tk.W)
            sorting_button.     grid(column = 0,row=0,pady = (10,0),padx =520-shift_const,sticky = tk.W)
            deleting_button.    grid(column = 0,row=0,pady = (10,0),padx =780-shift_const,sticky = tk.W)
            converting_button.  grid(column = 0,row=0,pady = (10,0),padx =1040-shift_const,sticky = tk.W)

            context_menu_button  =  customtkinter.CTkButton(master =frame2, width = 50,height=50, text = "V",font=("Arial",20,"bold"),corner_radius=0,fg_color="#505050")
            self.path_set = customtkinter.CTkEntry(master = frame2,height=50,font=("Arial",18),placeholder_text="Zadejte cestu k souborům z kamery (kde se nacházejí složky se soubory nebo soubory přímo)",corner_radius=0)
            tree =          customtkinter.CTkButton(master = frame2,height=50,text = "EXPLORER", command = self.call_browseDirectories,font=("Arial",20,"bold"),corner_radius=0)
            button_save_path = customtkinter.CTkButton(master = frame2,height=50,text = "Uložit cestu", command = lambda: Tools.save_path(self.console,self.path_set.get(),"sort_conv_settings"),font=("Arial",20,"bold"),corner_radius=0)
            button_open_setting = customtkinter.CTkButton(master = frame2,height=50,width=50, text = "⚙️", command = lambda: Advanced_option(self.root,windowed=True,spec_location="sorting_option"),font=(None,20),corner_radius=0)
            context_menu_button.pack(pady = 10,padx =(10,0),anchor ="w",side="left")
            self.path_set.  pack(pady = 10,padx =(0,0),anchor ="w",side="left",fill="x",expand = True)
            tree.           pack(pady = 10,padx =5,anchor ="w",side="left")
            button_save_path.pack(pady = 10,padx =0,anchor ="w",side="left")
            button_open_setting.pack(pady = 10,padx =(5,10),anchor ="w",side="left")
            context_menu_button.bind("<Button-1>", call_path_context_menu)

            self.checkbox =  customtkinter.CTkCheckBox(master = self.frame3,font=("Arial",16), text = "Třídit podle typů souborů",command = self.selected)
            self.checkbox2 = customtkinter.CTkCheckBox(master = self.frame3,font=("Arial",16), text = "Třídit podle čísla funkce (ID)",command = self.selected2)
            self.checkbox3 = customtkinter.CTkCheckBox(master = self.frame3,font=("Arial",16), text = "Třídit podle čísla kamery",command = self.selected3)
            self.checkbox4 = customtkinter.CTkCheckBox(master = self.frame3,font=("Arial",16), text = "Třídit podle čísla funkce i kamery",command = self.selected4)
            self.checkbox5 = customtkinter.CTkCheckBox(master = self.frame3,font=("Arial",16), text = "Najít dvojice (soubory se stejným ID, v řadě za sebou)",command = self.selected5)
            self.checkbox.  pack(pady =12,padx=10,anchor ="w")
            self.checkbox2. pack(pady =12,padx=10,anchor ="w")
            self.checkbox3. pack(pady =12,padx=10,anchor ="w")
            self.checkbox4. pack(pady =12,padx=10,anchor ="w")
            self.checkbox5. pack(pady =12,padx=10,anchor ="w")
            checkboxes =   customtkinter.CTkFrame(master=self.frame4,corner_radius=0,fg_color="#212121")
            self.one_subfolder = customtkinter.CTkCheckBox(master = checkboxes,font=("Arial",16), text = "Projít 1 subsložku?",command = self.one_subfolder_checked)
            self.checkbox6   = customtkinter.CTkCheckBox(master = checkboxes,font=("Arial",16), text = "Projít 2 subsložky?",command = self.two_subfolders_checked)
            self.checkbox_safe_mode = customtkinter.CTkCheckBox(master = checkboxes,font=("Arial",16), text = "Rozbalit poslední složky?",command = self.safe_mode_checked)
            self.images2     = customtkinter.CTkLabel(master = self.frame4,text = "",height=180)
            self.console2    = customtkinter.CTkLabel(master = self.frame4,text = " ",font=("Arial",18,"bold"))
            self.one_subfolder.pack(pady =10,padx=10,anchor="w",side=tk.LEFT)
            self.checkbox6. pack(pady =10,padx=10,anchor="w",side=tk.LEFT)
            self.checkbox_safe_mode.pack(pady =10,padx=10,anchor="w",side=tk.LEFT)
            checkboxes.   pack(side="top",anchor = "w",padx=(10,0))
            self.images2.   pack(side="top",anchor = "w",padx=(10,0),pady = 10)
            self.console2.  pack(pady =5,padx=10,side="top",anchor = "w")
            self.images2.propagate(0)
            self.checkbox_safe_mode.select()
            info_frame =        customtkinter.CTkFrame(master=self.frame5,height=250,corner_radius=0,fg_color="#212121")
            self.name_example = customtkinter.CTkLabel(master = info_frame,height=60,text = "",font=("Arial",18,"bold"))
            self.images =       customtkinter.CTkLabel(master = info_frame,text = "")
            self.name_example.  pack(pady = 12,padx =10,side="top",anchor="n")
            self.name_example.propagate(0)
            self.images.        pack(padx=(30,0),side="top",anchor="n")
            info_frame.         pack(pady=0,padx=5,side = "top",anchor = "n",fill="x",expand=True)
            info_frame.propagate(0)
            button =            customtkinter.CTkButton(master = self.frame5, text = "SPUSTIT", command = self.start,font=("Arial",20,"bold"))
            self.loading_bar =  customtkinter.CTkProgressBar(master = self.frame5, mode='determinate',width = 800,height =20,progress_color="green",corner_radius=0)
            self.console =      tk.Text(self.frame5, wrap="word",background="black",font=("Arial",16),state=tk.DISABLED)

            button.             pack(pady =12,padx=10)
            button.             _set_dimensions(300,60)
            self.loading_bar.   pack(pady = 5,padx = 5)
            self.loading_bar.   set(value = 0)
            self.console.       pack(pady =10,padx=(10,0),side="left",fill="both",expand=True)
            frame_with_cards.pack(pady=0,padx=0,fill="x",expand=False,side = "top")
            frame2.         pack(pady=0,padx=5,fill="both",expand=False,side = "top")
            self.frame3.    pack(pady=5,padx=5,fill="y",expand=False,side="left")
            self.frame6.    pack(pady=5,padx=0,fill="y",expand=False,side="left")
            self.frame4.    pack(pady=5,padx=5,fill="both",expand=True,side="left")
            upper_frame.    pack(pady=0,padx=5,fill="x",expand=False,side="top")

            self.frame5.    pack(pady=0,padx=5,fill="both",expand=True,side = "top")
            scrollbar = tk.Scrollbar(self.frame5, command=self.console.yview)
            scrollbar.pack(pady =10,side="right", fill="y")
            self.console.config(yscrollcommand=scrollbar.set)

            #default nastaveni:
            self.checkbox.select()
            self.selected()
            self.view_image(1)
            self.two_subfolders_checked()
            #predvyplneni cesty pokud je platna v configu
            recources_path = self.config_data["app_settings"]["default_path"]
            if len(self.config_data["sort_conv_settings"]["path_history_list"]) != 0:
                path_from_history = self.config_data["sort_conv_settings"]["path_history_list"][0]
                self.path_set.delete("0","200")
                self.path_set.insert("0", path_from_history)
                Tools.add_colored_line(self.console,"Byla vložena cesta z konfiguračního souboru","white",None,True)
                self.root.update_idletasks()
            elif recources_path != False and recources_path != "/":
                self.path_set.delete("0","200")
                self.path_set.insert("0", str(recources_path))
                Tools.add_colored_line(self.console,"Byla vložena cesta z konfiguračního souboru","white")
            else:
                Tools.add_colored_line(self.console,"Konfigurační soubor obsahuje neplatnou cestu k souborům (můžete vložit v pokročilém nastavení)","orange")

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
                self.root.focus_set()
            self.root.bind("<Escape>",unfocus_widget)
            self.unbind_list.append("<Escape>")
            self.path_set.bind("<Return>",unfocus_widget)

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

    class Catalogue_maker: # Umožňuje nastavit možnosti třídění souborů
        """
        Umožňuje sestavit katalog produktů k projektu
        - ten následné vyexportovat do excelu (.xlm/ .xls)
        - rozpracovaný projekt je možné uložit do souboru .xml
        - databázi produktů stahuje automaticky při spuštění z sharepointu (po restartu celé app)
        """
        def __init__(self,root):
            self.root = root
            self.database_downloaded = menu.database_downloaded
            # automatic download bypass:
            if testing:
                self.database_downloaded = True 
            config_data = Tools.read_json_config()
            self.database_filename = str(config_data["catalogue_settings"]["database_filename"])
            # self.default_excel_filename = config_data["catalogue_settings"]["catalogue_filename"]
            # self.default_xml_file_name = config_data["catalogue_settings"]["metadata_filename"]
            # self.default_subwindow_status = config_data["catalogue_settings"]["subwindow_behav"]
            # self.default_export_extension = config_data["catalogue_settings"]["default_export_suffix"]
            # self.default_path = config_data["catalogue_settings"]["default_path"]
            # self.default_render_mode = config_data["catalogue_settings"]["render_mode"]
            self.create_catalogue_maker_widgets()

        def callback(self):
            # print("received data: ",data_to_save)
            # Tools.save_to_json_config(data_to_save[0],"catalogue_settings","database_filename")
            # Tools.save_to_json_config(data_to_save[1],"catalogue_settings","catalogue_filename")
            # Tools.save_to_json_config(data_to_save[2],"catalogue_settings","metadata_filename")
            # Tools.save_to_json_config(data_to_save[3],"catalogue_settings","subwindow_behav")
            # Tools.save_to_json_config(data_to_save[4],"catalogue_settings","default_export_suffix")
            # Tools.save_to_json_config(data_to_save[5],"catalogue_settings","default_path")
            # Tools.save_to_json_config(data_to_save[6],"catalogue_settings","render_mode")
            menu.menu()

        def create_catalogue_maker_widgets(self):
            if root.wm_state() == "zoomed":
                current_window_size = "max"
            else:
                current_window_size = "min"
            
            if not self.database_downloaded:
                download = download_database.database(self.database_filename)
                input_message = str(download.output)
                menu.database_downloaded = True
            else:
                input_message = "Datábáze se stáhne znovu až po restartu TRIMAZKONU"
            
            Catalogue.Catalogue_gui(self.root,
                                    input_message,
                                    self.callback,
                                    current_window_size,
                                    initial_path)

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
