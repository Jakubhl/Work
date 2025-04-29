import customtkinter
import os
import time
from PIL import Image
import Deleting_option_v2 as Deleting
import trimazkon_tray_MAZ_v3 as trimazkon_tray
import sharepoint_download as download_database
import string_database_MAZ
import json
from tkinter import filedialog
import tkinter as tk
import threading
import sys
import ctypes
import win32pipe, win32file, pywintypes, psutil
import subprocess
from win32api import *
from win32gui import *
import win32con
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import datetime
import wmi
# import struct
import winreg

testing = False


global_recources_load_error = False
global_licence_load_error = False
exe_path = sys.executable
exe_name = os.path.basename(exe_path)
config_filename = "config_MAZ.json"
app_name = "jhv_MAZ"
app_version = "1.0.6"
trimazkon_version = "4.3.4"
loop_request = False
root = None
print("exe name: ",exe_name)
if testing:
    exe_name = "jhv_MAZ.exe"

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
        prompt_message1 = "Nemáte platnou licenci pro spuštění aplikace jhv_MAZ."
        prompt_message2 = f"Váš HWID:"
        prompt_message3 = f"\n{user_HWID}\n"
        prompt_message4 = "odešlete na email: "
        prompt_message5 = "jakub.hlavacek@jhv.cz "
        prompt_message6 = "s žádostí o licenci."
        title_message = "Upozornění"

        if language_given == "en":
            prompt_message1 = "You do not have a valid license to run the application jhv_MAZ."
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
            if os.path.exists(str(operating_path.get())):
                output = Tools.browseDirectories("only_dirs",start_path=str(operating_path.get()))
            else:
                output = Tools.browseDirectories("only_dirs")
            if str(output[1]) != "/":
                operating_path.delete(0,300)
                operating_path.insert(0, str(output[1]))
                Tools.add_new_path_to_history(str(output[1]))
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
                new_task_name = "jhv_MAZ_task_xx"
                for tasks in current_tasks:
                    names_taken.append(tasks["name"])
                for i in range(1,100):
                    name_suggestion = "jhv_MAZ_task_" + str(i)
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
            path_history = Tools.read_json_config()[10]
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

    @classmethod
    def download_new_version_window(cls,new_version,given_log,language_given="cz"):
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
            
        prompt_message1 = f"Je k dispozici nová verze aplikace: {new_version} !"
        prompt_message2 = f"Upgrade log:"
        title_message = "Upozornění"
        if language_given == "en":
            prompt_message1 = f"New app version available: {new_version} !"
            prompt_message2 = f"Upgrade log:"
            title_message = "Notice"
            
        child_root = customtkinter.CTkToplevel(fg_color="#212121")
        child_root.after(200, lambda: child_root.iconbitmap(app_icon))
        child_root.title(title_message)
        label_frame =       customtkinter.CTkFrame(master = child_root,corner_radius=0)
        proceed_label =     customtkinter.CTkLabel(master = label_frame,text = prompt_message1,font=("Arial",25,"bold"),anchor="w",justify="left")
        proceed_label2 =    customtkinter.CTkLabel(master = label_frame,text = prompt_message2,font=("Arial",20),anchor="w",justify="left")
        proceed_label.      pack(pady=(5,0),padx=10,anchor="w",side = "top")
        proceed_label2.     pack(pady=(5,0),padx=10,anchor="w",side = "top")
        label_frame.        pack(pady=0,padx=0,anchor="w",side = "top",fill="x")
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
        button_close.       pack(pady = 10, padx = (0,10),anchor="e",side="right")
        button_dwnld.       pack(pady = 10, padx = (0,10),anchor="e",side="right")
        button_frame.       pack(pady=0,padx=0,anchor="w",side = "top",fill="x")

        if language_given == "en":
            button_close.configure(text = "Close")
            button_dwnld.configure(text = "Download the new version")
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
    task_name = "jhv_MAZ_startup_tray_setup"
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
    def get_all_app_processes(cls):
        pid_list = []
        num_of_apps = 0
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == exe_name:
                print(process.info)
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
        print("found processes (duplicity): ",found_processes)
        if found_processes[0] > 1:
            return True
        else:
            return False

    @classmethod
    def resource_path(cls,relative_path):
        #PYINSTALLER
        """ Get the absolute path to a resource, works for dev and for PyInstaller """
        # if hasattr(sys, '_MEIPASS'):
        # return os.path.join(os.path.abspath("."), relative_path)
        BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.abspath(".")
        return os.path.join(BASE_DIR, relative_path)
    
    @classmethod
    def create_new_json_config(cls,default_value_list,default_labels):
        updated_settings = [
            {"key": "default_path", "value": default_value_list[0]},
            {"key": "supported_formats_deleting", "value": default_value_list[1]},
            {"key": "default_files_to_keep", "value": default_value_list[2]},
            {"key": "default_cutoff_date", "value": default_value_list[3]},
            {"key": "default_deleting_dir_name", "value": default_value_list[4]},
            {"key": "maximalized", "value": default_value_list[5]},
            {"key": "sorting_safe_mode", "value": default_value_list[6]},
            {"key": "app_zoom", "value": default_value_list[7]},
            {"key": "app_zoom_checkbox", "value": default_value_list[8]},
            {"key": "tray_icon_startup", "value": default_value_list[9]},
            {"key": "path_history_list", "value": [default_value_list[0]]},
            {"key": "default_language", "value": default_value_list[11]},
        ]
        

        with open(initial_path+cls.config_json_filename, "w") as file:
            json.dump({"settings": updated_settings}, file, indent=4)

    @classmethod
    def read_json_config(cls): # Funkce vraci data z configu
        """
        Funkce vrací data z konfiguračního souboru

        data jsou v pořadí:

        0 default_path\n
        1 supported_formats_deleting\n
        2 default_files_to_keep\n
        3 default_cutoff_date\n
        4 default_deleting_dir_name\n
        5 maximalized\n
        6 sorting_safe_mode\n
        7 app_zoom\n
        8 app_zoom_checkbox\n
        9 tray_icon_startup\n
        10 path_history_list\n
        11 default_language\n
        """
        def filter_unwanted_chars(to_filter_data, directory = False,even_space=False):
            unwanted_chars = ["\n","\"","\'","[","]"]
            if directory:
                unwanted_chars = ["\n","\"","\'","[","]","\\","/"]
            if even_space:
                unwanted_chars.append(" ")
            filtered_data = ""
            for letters in to_filter_data:
                if letters not in unwanted_chars:
                    filtered_data += letters
            return filtered_data

        def load_default_values():
            output_array = [default_setting_parameters[0],
                            default_setting_parameters[1],
                            default_setting_parameters[2],
                            default_setting_parameters[3],
                            default_setting_parameters[4],
                            default_setting_parameters[5],
                            default_setting_parameters[6],
                            default_setting_parameters[7],
                            default_setting_parameters[8],
                            default_setting_parameters[9],
                            default_setting_parameters[10],
                            default_setting_parameters[11],
                            ]
            
            print("read intern database (default values)",output_array,len(output_array))
            return output_array

        global global_recources_load_error
        default_setting_parameters = string_database_MAZ.default_setting_database_param
        default_labels = string_database_MAZ.default_setting_database

        if os.path.exists(initial_path+cls.config_json_filename):
            try:
                output_data = []
                with open(initial_path+cls.config_json_filename, "r") as file:
                    data = json.load(file)

                settings = data["settings"]

                # print("config raw data: ", settings)
                for item in settings:
                    output_data.append(item['value'])

                # print("config data: ", output_data, len(output_data))
                return output_data

            except Exception as e:
                print(f"Nejdřív zavřete soubor {cls.config_json_filename} Chyba: {e}")   
                print("Budou načteny defaultní hodnoty")
                global_recources_load_error = True
                output_array = load_default_values()
                return output_array
        else:
            print(f"Chybí konfigurační soubor {cls.config_json_filename}, bude vytvořen")
            Tools.create_new_json_config(default_setting_parameters,default_labels)
            output_array = load_default_values()
            return output_array
        
    @classmethod
    def save_to_json_config(cls,input_data,which_parameter,language_force = "cz"): # Funkce zapisuje data do souboru configu
        """
        Funkce zapisuje data do konfiguračního souboru

        vraci vystupni zpravu: report

        which_parameter je bud: 
        
        1 default_path\n
        2 add_supported_deleting_formats\n
        3 pop_supported_deleting_formats\n
        4 default_files_to_keep\n
        5 default_cutoff_date\n
        6 default_deleting_dir_name\n
        7 maximalized\n
        8 sorting_safe_mode\n
        9 app_zoom\n
        10 app_zoom_checkbox\n
        11 tray_icon_startup\n
        12 path_history_list\n
        13 default_language\n
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
        
        def rewrite_value(key,new_data):
            for item in settings:
                if item["key"] == str(key):
                    item["value"] = new_data  # New value
                    break

        
        if os.path.exists(initial_path + cls.config_json_filename):
            with open(initial_path+cls.config_json_filename, "r") as file:
                data = json.load(file)
            settings = data["settings"]
            try:
                new_tasks = data["task_list"]
            except:
                new_tasks = None
            report = ""

            supported_formats_deleting = next((item["value"] for item in settings if item["key"] == "supported_formats_deleting"), None)
            print("found formats: ", supported_formats_deleting)

            
            if which_parameter == "add_supported_deleting_formats":
                corrected_input = filter_unwanted_chars(str(input_data),formats=True)
                if str(corrected_input) not in supported_formats_deleting:
                    supported_formats_deleting.append(str(corrected_input))
                    report =  (f"Byl přidán formát: \"{corrected_input}\" do podporovaných formátů pro možnosti mazání")
                    if language_force == "en":
                        report =  (f"Added format: \"{corrected_input}\" to supported formats for deletion options")
                    rewrite_value("supported_formats_deleting",supported_formats_deleting)
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
                            rewrite_value("supported_formats_deleting",supported_formats_deleting)
                            break

                if found == False:
                    report =  (f"Formát: \"{input_data}\" nebyl nalezen v podporovaných formátech možností mazání, nemůže tedy být odstraněn")
                    if language_force == "en":
                        report =  (f"The format \".{input_data}\" was not found in the supported delete option formats, so it cannot be deleted")

            elif which_parameter == "default_path":
                report = (f"Základní cesta přenastavena na: {str(input_data)}")
                rewrite_value(which_parameter,str(input_data))
            elif which_parameter == "default_cutoff_date" or which_parameter == "path_history_list":
                rewrite_value(which_parameter,input_data)
            elif which_parameter == "default_files_to_keep" or which_parameter == "app_zoom":
                rewrite_value(which_parameter,int(input_data))
            else:
                rewrite_value(which_parameter,str(input_data))
                              
            with open(initial_path+cls.config_json_filename, "w") as file:
                if new_tasks == None:
                    json.dump({"settings": settings}, file, indent=4)
                else:
                    json.dump({"settings": settings, "task_list": new_tasks}, file, indent=4)

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
        text_file_data = Tools.read_json_config()
        if start_path == None:
            start_path = str(text_file_data[2]) #defaultni cesta
        else: # byla zadana docasna cesta pro explorer
            checked_path = Tools.path_check(start_path)
            if checked_path == False:
                output = "Změněná dočasná základní cesta pro explorer již neexistuje"
                start_path = str(text_file_data[2]) #defaultni cesta
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
    def save_path(cls,console,path_entered):
        path_given = path_entered
        path_checked = Tools.path_check(path_given)
        if path_checked != False and path_checked != "/":
            console_input = Tools.save_to_json_config(path_checked,"default_path")
            Tools.add_new_path_to_history(path_checked)
            Tools.add_colored_line(console,console_input,"green",None,True)
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

        print(data,error_data)
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
    def is_admin(cls):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

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
        if "Access is denied" in output_message or "stup byl odep" in output_message:
            return "need_access"

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

        deleting_path = deleting_path.replace("-|-"," ") #dekodovat mezery v ceste (nemohou byt v task scheduleru)
        cutoff_date = Deleting.get_cutoff_date(days=max_days)
        text_file_data = Tools.read_json_config()
        supported_formats_deleting = text_file_data[1]
        to_delete_folder_name = text_file_data[4]

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

        elif selected_option == 3 or selected_option == 4:
            new_log = {"del_date": output_data[3],
                    "files_checked": output_data[0],
                    "files_older": "",
                    "files_newer": "",
                    "files_deleted": output_data[2],
                    "path_count": "",
                    }
            output_message = f"Provedeno: {output_data[3]}\nZkontrolováno: {output_data[0]} adresářů\nSmazáno: {output_data[2]} adresářů"
            output_message_eng = f"Date of execution: {output_data[3]}\nTotal checked: {output_data[0]} directories\nTotal deleted: {output_data[2]} directories"

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
    def add_new_path_to_history(cls,new_path):
        if new_path == "delete_history":
            Tools.save_to_json_config([],"path_history_list")
            return

        current_paths = Tools.read_json_config()[10]
        if new_path not in current_paths:
            if len(current_paths) > 9:
                current_paths.pop()
            # current_paths.append(str(new_path))
            current_paths.insert(0,str(new_path))
            Tools.save_to_json_config(current_paths,"path_history_list")

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
    def check_for_new_app_version(cls,language_given = "cz"):
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
        version_list_int = []
        for versions in version_list:
            versions = versions.replace(".","")
            version_list_int.append(int(versions))

        print(version_list_int)
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
            Subwindows.download_new_version_window(max_sharepoint_version_str,new_version_log)

initial_path = Tools.get_init_path()
print("init path: ",initial_path)
app_icon = Tools.resource_path('images/logo_TRIMAZKON.ico')
app_licence_validity = Tools.check_licence()

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
            print(f"Waiting for a jhv_MAZ to connect on {pipe_name}...") 
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
            print("jhv_MAZ connected.")

            try:
                while True:
                    hr, data = win32file.ReadFile(pipe, 64 * 1024)
                    received_data = data.decode()
                    print(f"Received: {received_data}")
                    try:
                        global root #pokud existuje
                    except Exception as e:
                        print("root error")

                    if "Establish main menu gui" in received_data:
                        root_existance = self.check_root_existence(root)
                        print("root_status: ",root_existance)
                        if root_existance == True:
                            try:
                                root.deiconify()
                                if Tools.read_json_config()[5] == "ano":
                                    root.after(0, lambda:root.state('zoomed'))
                                root.update_idletasks()
                            except Exception as e:
                                print(e)
                            global menu
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
                        # global root
                        root.destroy()
                        # root.after(100,lambda: root.destroy())

            except pywintypes.error as e:
                if e.args[0] == 109:  # ERROR_BROKEN_PIPE
                    print("jhv_MAZ disconnected.")
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
        
        elif "Open list with del tasks" in str(command):
            message = "Open list with del tasks"
            print("Message sent.",message)
            win32file.WriteFile(handle, message.encode())

        elif "Open list with del logs" in str(command):
            message = "Open list with del logs"
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
        self.pipe_name = f"jhv_MAZ_pipe_{self.current_pid}"
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
                    pipe_name = f"jhv_MAZ_pipe_{pids}"
                    print("calling client",pipe_name,command,parameters)
                    self.client(pipe_name,command,parameters)
                except Exception:
                    pass
        return True
        # else:
            # return False

load_gui=True
print("SYSTEM: ",sys.argv)
if len(sys.argv) > 1 and not global_licence_load_error: # kontrola tady, aby se znovu nedefinovala classa windowsballoontip, řve to...
    print("received: ",sys.argv[1])
    if sys.argv[1] == "deleting":
        del_thread = threading.Thread(target=Tools.deleting_via_cmd,name="Deleting_thread")
        del_thread.start()
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
app_running_status = Tools.check_runing_app_duplicity()
print("already opened app status: ",app_running_status)

if load_gui:
    if not app_running_status: # aplikace ještě neběží -> spustit server
        pipeline_duplex = system_pipeline_communication(exe_name)# Establishment of pipeline server for duplex communication between running applications
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")
        root=customtkinter.CTk(fg_color="#212121")
        root.geometry("1200x900")
        root.title(f"{app_name} v_{app_version}")
        root.wm_iconbitmap(app_icon)
        loop_request=True

    else:# předání parametrů pipeline komunikací PUKUD NEJSOU NA VSTUPU ZADNE SYSTEMOVE PARAMETRY, SPOUSTENO PRES ZÁSTUPCE
        pipeline_duplex_instance = system_pipeline_communication(exe_name,no_server=True) # pokud už je aplikace spuštěná nezapínej server, trvá to...
        pipeline_duplex_instance.call_checking(f"Establish main menu gui",[])

class main_menu:
    def __init__(self,root,new_loop=False):
        self.root = root
        # if not new_loop:
            # pipeline_duplex.root = self.root # předání rootu do pipeline_duplex až ve chvílí, kdy je jasné, že aplikace není vícekrát spuštěná:
        self.data_read_in_txt = Tools.read_json_config()
        self.database_downloaded = False
        self.ib_running = False
        self.run_as_admin = False
        self.TS_tray_taskname = "jhv_MAZ_startup_tray_setup"
        self.selected_language = self.data_read_in_txt[11]
        #init spínání tray podle nastavení
        if self.data_read_in_txt[9] == "ano":
            task_success = Tools.establish_startup_tray()
            if str(task_success) == "need_access":
                self.run_as_admin = True
        else: # když nezaškrtnuto aut. spouštění ujisti se, že není nastavené - potřeba taky admin
            if Tools.check_task_existence_in_TS(self.TS_tray_taskname):
                Tools.remove_task_from_TS(self.TS_tray_taskname)
        
    def clear_frames(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
    def call_deleting_option(self):
        self.clear_frames()
        self.root.unbind("<f>")
        Deleting_option(self.root)

    def call_advanced_option(self,success_message = None):
        self.clear_frames()
        self.root.unbind("<f>")
        Advanced_option(self.root,tray_setting_status_message=success_message)

    def fill_changelog(self,change_log):
        # Iterate through each <string> element and print its text
        for string_element in string_database_MAZ.change_log_list:
            change_log.insert("current lineend",string_element + "\n")
        change_log.see(tk.END)

    def on_closing(self):
        global root
        if Tools.is_admin(): # pokud se vypíná admin app - vypnout i admin tray a zapnout bez práv
            data_read_in_config = Tools.read_json_config()
            if data_read_in_config[9] == "ano":
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

    def is_root_zoomed(self):
        if self.root.state() == "zoomed":
            return True
        else:
            return False
    
    def check_licence(self):
        global app_licence_validity
        app_licence_validity = Tools.check_licence()
        menu.menu(clear_root=True)

    def menu(self,initial=False,zoom_disable = False,clear_root=False): # Funkce spouští základní menu při spuštění aplikace (MAIN)
        """
        Funkce spouští základní menu při spuštění aplikace (MAIN)
        """
        def change_app_language(new_lan,refresh=False):
            if not refresh:
                if Tools.read_json_config()[11] != new_lan:
                    Tools.save_to_json_config(new_lan,"default_language")

            if new_lan == "en":
                new_deleting.configure(text="Set a new delete task")
                task_manager.configure(text="Show set deletion")
                deleting_history.configure(text="View deletion records")
                advanced_button.configure(text="Settings")
                change_log_label.configure(text="List of recently made changes: ")
                resources_load_error.configure(text=f"Failed to load configuration file ({config_filename})")
                pick_language_label.configure(text="Select language:")
                licence_info_label.configure(text="License:")
                if not global_licence_load_error:
                    if "Trial active" in str(app_licence_validity):
                        licence_info_status.configure(text=f"{app_licence_validity}")
                    else:
                        licence_info_status.configure(text=f"valid until {app_licence_validity}")
            else:
                new_deleting.configure(text="Nastavit nové mazání")
                task_manager.configure(text="Zobrazit nastavené mazání")
                deleting_history.configure(text="Zobrazit záznamy o mazání")
                advanced_button.configure(text="Nastavení")
                change_log_label.configure(text="Seznam posledně provedených změn: ")
                resources_load_error.configure(text=f"Nepodařilo se načíst konfigurační soubor ({config_filename})")
                pick_language_label.configure(text="Vybrat jazyk:")
                licence_info_label.configure(text="Licence:")
                if not global_licence_load_error:
                    if "Trial active" in str(app_licence_validity):
                        validity_string = str(app_licence_validity)
                        validity_string = validity_string.replace("Trial active.","Trial verze platná:")
                        validity_string = validity_string.replace("days remaining.","dní")
                        licence_info_status.configure(text=f"{validity_string}")
                    else:
                        licence_info_status.configure(text=f"platná do {app_licence_validity}")

        if clear_root:
            self.clear_frames()
            # self.root.after(0, lambda:self.clear_frames())

        if self.data_read_in_txt[5] == "ano" and initial:
            self.root.after(0, lambda:self.root.state('zoomed')) # max zoom, porad v okne
            
        if self.data_read_in_txt[8] == "ne" and initial: # pokud není využito nastavení windows
            try:
                root.after(0, lambda: Tools.set_zoom(int(self.data_read_in_txt[7]),root))
            except Exception as e:
                print("error with menu scaling")

        frame_with_logo = customtkinter.CTkFrame(master=self.root,corner_radius=0)
        logo = customtkinter.CTkImage(Image.open(Tools.resource_path("images/jhv_logo.png")),size=(300, 100))
        image_logo = customtkinter.CTkLabel(master = frame_with_logo,text = "",image =logo)
        
        menu_upper_frame = customtkinter.CTkFrame(master=self.root,corner_radius=0,fg_color="#212121")
        frame_with_buttons_right = customtkinter.CTkFrame(master=menu_upper_frame,corner_radius=0,fg_color="#212121")
        frame_with_buttons = customtkinter.CTkFrame(master=menu_upper_frame,corner_radius=0,fg_color="#212121")
        frame_with_logo.pack(pady=0,padx=0,fill="x",side = "top")
        image_logo.pack()
        trimazkon_tray_instance = trimazkon_tray.tray_app_service(initial_path,app_icon,exe_name,config_filename)
        new_deleting =         customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Nastavit nové mazání", command = lambda: self.call_deleting_option(),font=("Arial",25,"bold"))
        task_manager =         customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Zobrazit nastavené mazání", command = lambda: trimazkon_tray_instance.show_all_tasks(toplevel=True,maximalized=self.is_root_zoomed()),font=("Arial",25,"bold"))
        deleting_history =      customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Zobrazit záznamy o mazání", command = lambda: trimazkon_tray_instance.show_task_log(toplevel=True,maximalized=self.is_root_zoomed()),font=("Arial",25,"bold"))
        advanced_button =       customtkinter.CTkButton(master = frame_with_buttons, width = 400,height=100, text = "Nastavení", command = lambda: self.call_advanced_option(),font=("Arial",25,"bold"))
        change_log_label =      customtkinter.CTkLabel(master=frame_with_buttons_right, width= 600,height=50,font=("Arial",24,"bold"),text="Seznam posledně provedených změn: ")
        change_log =            customtkinter.CTkTextbox(master=frame_with_buttons_right, width= 600,height=450,fg_color="#212121",font=("Arial",20),border_color="#636363",border_width=3,corner_radius=0)
        resources_load_error =  customtkinter.CTkLabel(master=frame_with_buttons_right, width= 600,height=50,font=("Arial",24,"bold"),text=f"Nepodařilo se načíst konfigurační soubor ({config_filename})",text_color="red")
        new_deleting.           pack(pady =(105,0), padx=20,side="top",anchor="e")
        task_manager.           pack(pady =(10,0), padx=20,side="top",anchor="e")
        deleting_history.       pack(pady =(10,0), padx=20,side="top",anchor="e")
        advanced_button.        pack(pady = (10,0), padx=20,side="top",anchor="e")
        change_log_label.       pack(pady = (50,5), padx=20,side="top",anchor="w")
        change_log.             pack(pady =0,       padx=20,side="top",anchor="w")
        if global_recources_load_error:
            resources_load_error.pack(pady = (5,5), padx=20,side="top",anchor="w")

        frame_with_buttons.pack(pady=0,padx=0,fill="both",expand=True,side = "left")
        frame_with_buttons_right.pack(pady=0,padx=0,fill="both",expand=True,side = "right")
        menu_upper_frame.pack(pady=0,padx=0,fill="both",expand=True,side = "top")
        bottom_ribbon = customtkinter.CTkFrame(master=self.root,corner_radius=0,fg_color="#212121")

        language_frame = customtkinter.CTkFrame(master=bottom_ribbon,corner_radius=0,fg_color="#212121")
        pick_language_label = customtkinter.CTkLabel(master=language_frame,font=("Arial",24,"bold"),text="Vybrat jazyk:")
        czech_button = customtkinter.CTkButton(master = language_frame,text=f"\U0001F1E8\U0001F1FF", width = 50,height=50, command = lambda: change_app_language("cz"),font=(None,25))
        eng_button = customtkinter.CTkButton(master = language_frame,text=f"\U0001F1EC\U0001F1E7", width = 50,height=50, command = lambda: change_app_language("en"),font=(None,25))
        pick_language_label.pack(pady =5,padx=5,side="left",anchor="w")
        czech_button.pack(pady =5,padx=5,side="left",anchor="w")
        eng_button.pack(pady =5,padx=5,side="left",anchor="w")
        language_frame.pack(pady =20,padx=20,side="right",anchor="s")
        # frame_with_buttons_right.pack(pady=0,padx=0,fill="both",expand=True,side = "right")

        licence_info_frame = customtkinter.CTkFrame(master=bottom_ribbon,corner_radius=0,fg_color="#212121")
        licence_info_label = customtkinter.CTkLabel(master=licence_info_frame,font=("Arial",24,"bold"),text="Licence:")
        licence_info_status = customtkinter.CTkLabel(master=licence_info_frame,font=("Arial",24),text="")
        licence_info_label.pack(pady =5,padx=(5,0),side="left",anchor="w")
        licence_info_status.pack(pady =(7,5),padx=(5,0),side="left",anchor="w")
        licence_info_frame.pack(pady =30,padx=20,side="left",anchor="s")
        bottom_ribbon.pack(pady=0,padx=0,fill="both",side = "bottom",expand=True)

        # frame_with_buttons.pack(pady=0,padx=0,fill="both",expand=True,side = "left")
        self.fill_changelog(change_log)
        change_app_language(Tools.read_json_config()[11],refresh = True)

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
            new_deleting.configure(state="disabled")
            task_manager.configure(state="disabled")
            deleting_history.configure(state="disabled")
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

            if self.selected_language == "en":
                licence_info_status.configure(text=app_licence_validity)
                insert_licence_btn.configure(text="Insert license")
                trial_btn.configure(text="Activate trial version (30 days)")
            self.root.after(500, lambda: Subwindows.licence_window(self.selected_language))
        else:
            if initial:
                check_version = threading.Thread(target=Tools.check_for_new_app_version,)
                self.root.after(500,check_version.start)

        # initial promenna aby se to nespoustelo porad do kola pri navratu do menu (system argumenty jsou stále uložené v aplikaci)
        if len(sys.argv) > 1 and initial == True:
            raw_path = str(sys.argv[1])
            #klik na spusteni trimazkonu s admin právy
            # if sys.argv[0] == sys.argv[1]:
            #     self.call_ip_manager()
            if sys.argv[1] == "settings_tray":
                console_message = "Automatické spouštění úspěšně nastaveno"
                if self.selected_language == "en":
                    console_message = "Automatic startup successfully set"
                self.call_advanced_option(success_message=console_message)
            elif sys.argv[1] == "settings_tray_del":
                console_message = "Automatické spouštění úspěšně odstraněno"
                if self.selected_language == "en":
                    console_message = "Automatic startup successfully removed"
                self.call_advanced_option(success_message=console_message)
             
        if self.run_as_admin and not global_licence_load_error:
            require_admin_msg1 = "Upozornění"
            require_admin_msg2 = "Aplikace vyžaduje práva pro nastavení aut. spouštění na pozadí\n     - možné změnit v nastavení\n\nPřejete si znovu spustit aplikaci, jako administrátor?"
            if self.selected_language == "en":
                require_admin_msg1 = "Notice"
                require_admin_msg2 = "The application requires rights to set up automatic startup\n     - can be changed in the settings\n\nWould you like to restart the application as an administrator?"
            self.root.after(1000, lambda: Subwindows.call_again_as_admin("admin_menu",require_admin_msg1,require_admin_msg2,self.selected_language))
        # if initial and len(sys.argv) == 1:
        #     self.root.after(100, lambda: self.call_deleting_option())
        try:
            self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing())
            # self.root.mainloop()
        except Exception as e:
            print("already looped? ",e)

class Advanced_option: # Umožňuje nastavit základní parametry, které ukládá do config souboru
    """
    Umožňuje nastavit základní parametry, které ukládá do config souboru
    """
    def __init__(self,root,windowed=None,spec_location=None,path_to_remember = None,last_params = None,tray_setting_status_message = None):
        self.spec_location = spec_location
        self.path_to_remember = path_to_remember
        self.ib_last_params = last_params
        self.windowed = windowed
        self.root = root
        self.tray_setting_status_message = tray_setting_status_message
        self.unbind_list = []
        self.submenu_option = "default_path"
        self.text_file_data = Tools.read_json_config()
        self.default_dir_name = self.text_file_data[4]
        self.selected_language = self.text_file_data[11]
        
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
            Tools.save_to_json_config("ano","maximalized")
            self.root.after(0, lambda:self.root.state('zoomed'))
        else:
            Tools.save_to_json_config("ne","maximalized")
            self.root.after(0, lambda:self.root.state('normal'))
            self.root.after(10, lambda:self.root.geometry("1200x900"))

    def tray_startup_setup(self,main_console): # Nastavení základního spouštění (v okně/ maximalizované)
        option = self.tray_checkbox.get()
        if option == 1:
            Tools.save_to_json_config("ano","tray_icon_startup")
            new_task_success = Tools.establish_startup_tray()
            if str(new_task_success) == "need_access":
                menu.run_as_admin = True
                require_admin_msg1 = "Upozornění"
                require_admin_msg2 = "Aplikace vyžaduje práva pro nastavení aut. spouštění na pozadí\n\n- přejete si znovu spustit aplikaci, jako administrátor?"
                if self.selected_language == "en":
                    require_admin_msg1 = "Notice"
                    require_admin_msg2 = "The application requires rights to set up automatic startup\n\n- would you like to restart the application as an administrator?"
                Subwindows.call_again_as_admin("settings_tray",require_admin_msg1,require_admin_msg2,self.selected_language)
                main_console.configure(text = "Jsou vyžadována admin práva",text_color="red")
                if self.selected_language == "en":
                    main_console.configure(text = "Admin rights required",text_color="red")
            else:
                # Tools.establish_startup_tray()
                menu.run_as_admin = False
                main_console.configure(text = "Automatické spouštění úspěšně nastaveno",text_color="green")
                if self.selected_language == "en":
                    main_console.configure(text = "Automatic startup successfully set",text_color="green")
        else:
            Tools.save_to_json_config("ne","tray_icon_startup")
            remove_task_success = Tools.remove_task_from_TS("jhv_MAZ_startup_tray_setup")
            if str(remove_task_success) == "need_access":
                menu.run_as_admin = True
                require_admin_msg1 = "Upozornění"
                require_admin_msg2 = "Aplikace vyžaduje práva pro odstranění aut. spouštění na pozadí\n\n- přejete si znovu spustit aplikaci, jako administrátor?"
                if self.selected_language == "en":
                    require_admin_msg1 = "Notice"
                    require_admin_msg2 = "The application requires rights to remove automatic startup\n\n- would you like to restart the application as an administrator?"
                Subwindows.call_again_as_admin("settings_tray_del",require_admin_msg1,require_admin_msg2,self.selected_language)
                main_console.configure(text = "Jsou vyžadována admin práva",text_color="red")
                if self.selected_language == "en":
                    main_console.configure(text = "Admin rights required",text_color="red")
            else:
                menu.run_as_admin = False
                main_console.configure(text = "Automatické spouštění úspěšně odstraněno",text_color="green")
                if self.selected_language == "en":
                    main_console.configure(text = "Automatic startup successfully removed",text_color="green")
    
    def refresh_main_window(self):
        self.clear_frame(self.root)
        self.clear_frame(self.current_root)
        self.current_root.destroy()
        # if self.spec_location == "image_browser":
        #     Image_browser(root=self.root,path_given=self.path_to_remember,params_given=self.ib_last_params)
        # elif self.spec_location == "converting_option":
        #     Converting_option(self.root)
        if self.spec_location == "deleting_option":
            Deleting_option(self.root)
        # elif self.spec_location == "sorting_option":
        #     Sorting_option(self.root)

    def setting_widgets(self,exception=False,main_console_text = "",main_console_text_color = "white",submenu_option = None): # samotné možnosti úprav parametrů uložených v config souboru
        """
        Nabídka možností úprav

        0 = default_path
        1 = set_folder_names
        2 = set_default_parametres
        3 = set_supported_formats

        """

        if self.tray_setting_status_message != None:
            main_console_text = self.tray_setting_status_message
            main_console_text_color = "green"

        self.clear_frame(self.bottom_frame_default_path)
        text_file_data = Tools.read_json_config()
        if exception == False:
            cutoff_date = text_file_data[3]
        else:
            cutoff_date = exception
        
        files_to_keep = text_file_data[2]
        deleting_dir_name = text_file_data[4]
        row_index = 0
        for buttons in self.option_buttons:
            buttons.configure(fg_color = "black")

        def call_browseDirectories(): # Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
            """
            Volání průzkumníka souborů (kliknutí na tlačítko EXPLORER)
            """
            start_path = None
            try:
                start_path = self.path_set.get()
            except Exception:
                start_path = None
                pass
            if select_by_dir.get() == 1:
                output = Tools.browseDirectories("only_dirs",start_path)
            else:
                output = Tools.browseDirectories("all",start_path)
            if str(output[1]) != "/":
                self.path_set.delete("0","200")
                self.path_set.insert("0", output[1])
                console_input = Tools.save_to_json_config(output[1],"default_path") # hlaska o nove vlozene ceste
                default_path_insert_console.configure(text = "Aktuálně nastavená základní cesta k souborům: " + str(output[1]),text_color="white")
                if self.selected_language == "en":
                    default_path_insert_console.configure(text = "The currently set base file path: " + str(output[1]),text_color="white")
                Tools.add_new_path_to_history(str(output[1]))
                if self.selected_language == "en":
                    console_input = f"Base path reconfigured to: {str(output[1])}"
                main_console.configure(text=console_input,text_color="green")
            else:
                main_console.configure(text = str(output[0]),text_color="red")
                if self.selected_language == "en":
                    if str(output[0]) == "Přes explorer nebyla vložena žádná cesta":
                        main_console.configure(text = "No path was inserted via explorer",text_color="red")

        def save_path():
            path_given = str(self.path_set.get())
            path_checked = Tools.path_check(path_given)
            if path_checked != False and path_checked != "/":
                console_input = Tools.save_to_json_config(path_checked,"default_path")
                Tools.add_new_path_to_history(str(path_checked))
                default_path_insert_console.configure(text = "Aktuálně nastavená základní cesta k souborům: " + str(path_checked),text_color="white")
                if self.selected_language == "en":
                    default_path_insert_console.configure(text = "The currently set base file path: " + str(path_checked),text_color="white")
                main_console.configure(text=console_input,text_color="green")
            elif path_checked != "/":
                main_console.configure(text=f"Zadaná cesta: {path_given} nebyla nalezena, nebude tedy uložena",text_color="red")
                if self.selected_language == "en":
                    main_console.configure(text=f"Given path: {path_given} was not found, so it will not be saved",text_color="red")
            elif path_checked == "/":
                main_console.configure(text="Nebyla vložena žádná cesta k souborům",text_color="red")
                if self.selected_language == "en":
                    main_console.configure(text="No file path was inserted",text_color="red")
        
        def select_path_by_file():
            select_by_file.select()
            select_by_dir.deselect()
            # Tools.save_to_json_config("file","explorer_option")

        def select_path_by_dir():
            select_by_dir.select()
            select_by_file.deselect()
            # Tools.save_to_json_config("dir","explorer_option")

        def set_default_cutoff_date():
            input_month = set_month.get()
            if input_month != "":
                if input_month.isdigit():
                    if int(input_month) < 13 and int(input_month) > 0:
                        cutoff_date[1] = int(input_month)
                        max_days_in_month = Deleting.calc_days_in_month(int(cutoff_date[1]))
                        if int(cutoff_date[0]) > max_days_in_month:
                            cutoff_date[0] = str(max_days_in_month)
                        main_console.configure(text="Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2]),text_color="green")
                        if self.selected_language == "en":
                            main_console.configure(text="Date changed to: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2]),text_color="green")
                    else:
                        main_console.configure(text="Měsíc: " + str(input_month) + " je mimo rozsah",text_color="red")
                        if self.selected_language == "en":
                            main_console.configure(text="Month: " + str(input_month) + " is beyond the scope",text_color="red")
                else:
                    main_console.configure(text="U nastavení měsíce jste nezadali číslo",text_color="red")
                    if self.selected_language == "en":
                        main_console.configure(text="You did not enter a number for the month settings",text_color="red")

            input_day = set_day.get()
            max_days_in_month = Deleting.calc_days_in_month(int(cutoff_date[1]))

            if input_day != "":
                if input_day.isdigit():
                    if int(input_day) <= int(max_days_in_month) and int(input_day) > 0:
                        cutoff_date[0] = int(input_day)
                        main_console.configure(text="Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2]),text_color="green")
                        if self.selected_language == "en":
                            main_console.configure(text="Date changed to: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2]),text_color="green")
                    else:
                        main_console.configure(text="Den: " + str(input_day) + " je mimo rozsah",text_color="red")
                        if self.selected_language == "en":
                            main_console.configure(text="Day: " + str(input_day) + " is beyond the scope",text_color="red")
                else:
                    main_console.configure(text="U nastavení dne jste nezadali číslo",text_color="red")
                    if self.selected_language == "en":
                        main_console.configure(text="You did not enter a number for the day settings",text_color="red")

            input_year = set_year.get()
            if input_year != "":
                if input_year.isdigit():
                    if len(str(input_year)) == 2:
                        cutoff_date[2] = int(input_year) + 2000
                        main_console.configure(text="Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2]),text_color="green")
                        if self.selected_language == "en":
                            main_console.configure(text="Date changed to: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2]),text_color="green")
                    elif len(str(input_year)) == 4:
                        cutoff_date[2] = int(input_year)
                        main_console.configure(text="Datum přenastaveno na: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2]),text_color="green")
                        if self.selected_language == "en":
                            main_console.configure(text="Date changed to: "+ str(cutoff_date[0])+ "."+str(cutoff_date[1])+"."+ str(cutoff_date[2]),text_color="green")
                    else:
                        main_console.configure(text="Rok: " + str(input_year) + " je mimo rozsah",text_color="red")
                        if self.selected_language == "en":
                            main_console.configure(text="Year: " + str(input_year) + " is beyond the scope",text_color="red")
                else:
                    main_console.configure(text="U nastavení roku jste nezadali číslo",text_color="red")
                    if self.selected_language == "en":
                        main_console.configure(text="You did not enter a number for the year setting",text_color="red")

            Tools.save_to_json_config(cutoff_date,"default_cutoff_date")
            self.setting_widgets(False, main_console._text,main_console._text_color,submenu_option="set_default_parametres")

        def set_files_to_keep():
            nonlocal main_console
            input_files_to_keep = files_to_keep_set.get()
            if input_files_to_keep.isdigit():
                if int(input_files_to_keep) >= 0:
                    files_to_keep = int(input_files_to_keep)
                    Tools.save_to_json_config(files_to_keep,"default_files_to_keep")
                    main_console.configure(text="Základní počet ponechaných starších souborů nastaven na: " + str(files_to_keep),text_color="green")
                    console_files_to_keep.configure(text = "Aktuálně nastavené minimum: "+str(files_to_keep),text_color="white")
                    if self.selected_language == "en":
                        main_console.configure(text="Base number of older files left set to: " + str(files_to_keep),text_color="green")
                        console_files_to_keep.configure(text = "Currently set minimum: "+str(files_to_keep),text_color="white")
                else:
                    main_console.configure(text="Mimo rozsah",text_color="red")
                    if self.selected_language == "en":
                        main_console.configure(text="Out of range",text_color="red")
            else:
                main_console.configure(text="Nazadali jste číslo",text_color="red")
                if self.selected_language == "en":
                    main_console.configure(text="You didn't enter a number.",text_color="red")

            self.setting_widgets(False,main_console._text,main_console._text_color,submenu_option="set_default_parametres")

        def insert_current_date():
            today = Deleting.get_current_date()
            today_split = today[1].split(".")
            i=0
            for items in today_split:
                i+=1
                cutoff_date[i-1]=items
            main_console.configure(text="Bylo vloženo dnešní datum (Momentálně všechny soubory vyhodnoceny, jako starší!)",text_color="orange")
            if self.selected_language == "en":
                main_console.configure(text="Today's date has been inserted (currently all files are evaluated as older!)",text_color="orange")

            self.setting_widgets(cutoff_date,main_console._text,main_console._text_color,submenu_option="set_default_parametres")

        def add_format(which_operation):
            if which_operation == 1:
                new_format = str(formats_deleting_input.get())
                if new_format !="":
                    main_console_text_add = Tools.save_to_json_config(new_format,"add_supported_deleting_formats",language_force=self.selected_language)
                    main_console.configure(text=main_console_text_add,text_color="white")
            self.setting_widgets(False,main_console._text,main_console._text_color,submenu_option="set_supported_formats")

        def pop_format(which_operation):
            if which_operation == 1:
                format_to_delete = str(formats_deleting_input.get())
                if format_to_delete !="":
                    main_console_text_pop = Tools.save_to_json_config(format_to_delete,"pop_supported_deleting_formats",language_force=self.selected_language)
                    main_console.configure(text=main_console_text_pop,text_color="white")

            self.setting_widgets(False,main_console._text,main_console._text_color,submenu_option="set_supported_formats")
        
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
                Tools.save_to_json_config("ano","app_zoom_checkbox")
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
                Tools.save_to_json_config("ne","app_zoom_checkbox")
                Tools.set_zoom(int(app_zoom_slider.get()),root)

        def call_delete_path_history():
            confirm_window_label1 = "Opravdu si přejete odstranit historii vložených cest?"
            confirm_window_label2 = "Upozornění"
            if self.selected_language == "en":
                confirm_window_label1 = "Are you sure you want to delete the history of embedded paths?"
                confirm_window_label2 = "Notice"
            confirm = Subwindows.confirm_window(confirm_window_label1,confirm_window_label2,self.selected_language)
            if confirm == True:
                Tools.add_new_path_to_history("delete_history")
                main_console.configure(text="Historie vložených cest byla vymazána",text_color="orange")
                if self.selected_language == "en":
                    main_console.configure(text="The history of inserted paths has been deleted",text_color="orange")

        def call_path_context_menu(event):
            path_history = Tools.read_json_config()[10]
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

        if submenu_option == "default_path":
            self.option_buttons[0].configure(fg_color="#212121")
            row_index = 1

            insert_licence_btn =        customtkinter.CTkButton(master = self.bottom_frame_default_path, width = 200,height=40, text = "Otevřít umístění aplikace/ vložit licenci", command = lambda: os.startfile(initial_path),font=("Arial",24,"bold"))
            insert_licence_btn.          pack(pady=(30,0),padx=5,side = "top",anchor = "w")

            first_option_frame =        customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
            self.checkbox_maximalized = customtkinter.CTkCheckBox(master = first_option_frame,height=40,text = "Spouštět v maximalizovaném okně",command = lambda: self.maximalized(),font=("Arial",22,"bold"))
            first_option_frame.         pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")

            tray_option_frame =         customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
            self.tray_checkbox =        customtkinter.CTkCheckBox(master = tray_option_frame,height=40,text = "Spouštět jhv_MAZ na pozadí (v systémové nabídce \"tray_icons\") při zapnutí systému Windows?",command = lambda: self.tray_startup_setup(main_console),font=("Arial",22,"bold"))
            tray_option_frame.          pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")

            current_zoom = self.text_file_data[7]
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
            context_menu_button  =  customtkinter.CTkButton(master = second_option_frame, width = 40,height=40, text = "V",font=("Arial",20,"bold"),corner_radius=0,fg_color="#505050")
            self.path_set =             customtkinter.CTkEntry(     master = second_option_frame,width=805,height=40,font=("Arial",20),placeholder_text="",corner_radius=0)
            button_save5 =              customtkinter.CTkButton(    master = second_option_frame,width=100,height=40, text = "Uložit", command = lambda: save_path(),font=("Arial",22,"bold"))
            button_explorer =           customtkinter.CTkButton(    master = second_option_frame,width=40,height=40, text = "...", command = lambda: call_browseDirectories(),font=("Arial",22,"bold"),corner_radius=0)
            del_path_history =           customtkinter.CTkButton(    master = second_option_frame,height=40, text = "Smazat historii", command = lambda: call_delete_path_history(),font=("Arial",22,"bold"))
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
            if self.selected_language == "en":
                select_by_dir .             grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=200)
            else:
                select_by_dir .             grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=250)
            select_by_file.             grid(column =0,row=row_index+1,sticky = tk.W,pady =0,padx=550)
            context_menu_button.        grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
            self.path_set.              grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=50)
            button_explorer.            grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=855)
            button_save5.               grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=900)
            del_path_history.           grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=1005)
            default_path_insert_console.grid(column =0,row=row_index+3,sticky = tk.W,pady =10,padx=10)
            main_console.               grid(column =0,row=row_index+4,sticky = tk.W,pady =10,padx=10)
            second_option_frame.         pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
            console_frame.              pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
            
            if self.windowed:
                save_changes_button.    pack(pady =5,padx=10,anchor = "e")
                save_frame.             pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top",anchor = "e")
            select_by_dir.select()
            context_menu_button.bind("<Button-1>", call_path_context_menu)

            if self.selected_language == "en":
                insert_licence_btn.configure(text = "Open application root path/ insert license")
                self.checkbox_maximalized.configure(text = "Run in maximized window")
                self.tray_checkbox.configure(text = "Run jhv_MAZ in the background (in the system menu \"tray_icons\") when Windows is turned on?")
                zomm_app_label.configure(text = "Set the overall zoom of the application:")
                checkbox_app_zoom.configure(text = "Use Windows settings")
                label5.configure(text = "Set the base path to the files at startup:")
                explorer_settings_label.configure(text = "Explorer settings:")
                select_by_dir.configure(text = "Select a path by selecting a folder")
                select_by_file.configure(text = "Select a path by selecting a file (they are visible in the search)")
                button_save5.configure(text = "Save")
                del_path_history.configure(text = "Delete history")
                if self.windowed:
                    save_changes_button.configure(text = "Apply/load changes")

            def save_path_enter_btn(e):
                save_path()
                self.current_root.focus_set()
            self.path_set.bind("<Return>",save_path_enter_btn)

            app_zoom_slider.set(self.text_file_data[7])
            if self.text_file_data[8] == "ano":
                checkbox_app_zoom.select()
                windows_zoom_setting()

            def slider_released(e):
                """
                save after the slider is released - it still opening and closing excel otherwise
                """
                if not checkbox_app_zoom.get() == 1:
                    current_zoom = int(app_zoom_slider.get())
                    Tools.save_to_json_config(current_zoom,"app_zoom")
                    Tools.set_zoom(current_zoom,root)

            app_zoom_slider.bind("<ButtonRelease-1>",lambda e: slider_released(e))

            if text_file_data[0] != False and text_file_data[0] != "/":
                default_path_insert_console.configure(text="Aktuálně nastavená základní cesta k souborům: " + str(text_file_data[0]),text_color="white")
                if self.selected_language == "en":
                    default_path_insert_console.configure(text="The currently set base file path: " + str(text_file_data[0]),text_color="white")
                self.path_set.configure(placeholder_text=str(text_file_data[0]))
                self.path_set.delete("0","200")
                self.path_set.insert("0", str(text_file_data[0]))
            else:
                default_path_insert_console.configure(text="Aktuálně nastavená základní cesta k souborům v konfiguračním souboru je neplatná",text_color="red")
                self.path_set.configure(placeholder_text="Není nastavena žádná základní cesta")
                if self.selected_language == "en":
                    default_path_insert_console.configure(text="The currently set base file path in the configuration file is invalid",text_color="red")
                    self.path_set.configure(placeholder_text="No base path is set")
                    
            if text_file_data[5] == "ano":
                self.checkbox_maximalized.select()
            else:
                self.checkbox_maximalized.deselect()

            if text_file_data[9] == "ano":
                self.tray_checkbox.select()
            else:
                self.tray_checkbox.deselect()

        if submenu_option == "set_default_parametres":
            self.option_buttons[1].configure(fg_color="#212121")
            #widgets na nastaveni zakladniho poctu files_to_keep
            files_to_keep_console_text ="Aktuálně nastavené minimum: "+str(files_to_keep)
            second_option_frame =                customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
            second_option_frame.                 pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
            label_files_to_keep =               customtkinter.CTkLabel(master = second_option_frame,height=50,text = "Nastavte základní počet ponechaných souborů:",justify = "left",font=("Arial",22,"bold"))
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
            label_set_default_date =            customtkinter.CTkLabel(master = third_option_frame,height=50,text = "Nastavte základní datum pro vyhodnocení souborů, jako starších:",justify = "left",font=("Arial",22,"bold"))
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

            if self.selected_language == "en":
                label_files_to_keep.configure(text="Set the base number of retained files:")
                button_save2.configure(text="Save")
                label_set_default_date.configure(text="Set the base date for evaluating files as older:")
                button_save_date.configure(text="Save")
                insert_button.configure(text="Insert today's date")
                console_files_to_keep.configure(text=f"Currently set minimum: {files_to_keep}")
                if self.windowed:
                    save_changes_button.configure(text="Apply/ load changes")

            def new_date_enter_btn(e):
                set_default_cutoff_date()
                self.current_root.focus_set()
            set_day.bind("<Return>",new_date_enter_btn)
            set_month.bind("<Return>",new_date_enter_btn)
            set_year.bind("<Return>",new_date_enter_btn)

        if submenu_option == "set_supported_formats":
            self.option_buttons[2].configure(fg_color="#212121")
            #widgets pro nastavovani podporovanych formatu
            supported_formats_deleting = "Aktuálně nastavené podporované formáty pro možnosti mazání: " + str(text_file_data[1])
            first_option_frame =                customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=20,corner_radius=0,border_width=1)
            first_option_frame.                 pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
            label_supported_formats_deleting =  customtkinter.CTkLabel(master = first_option_frame,height=50,text = "Nastavte podporované formáty pro možnosti: MAZÁNÍ:",justify = "left",font=("Arial",22,"bold"))
            formats_deleting_input =            customtkinter.CTkEntry(master = first_option_frame,height=50,font=("Arial",20),width=200)
            button_save4 =                      customtkinter.CTkButton(master = first_option_frame,width=50,height=50, text = "Uložit", command = lambda: add_format(1),font=("Arial",22,"bold"))
            button_pop2 =                       customtkinter.CTkButton(master = first_option_frame,width=70,height=50, text = "Odebrat", command = lambda: pop_format(1),font=("Arial",22,"bold"))
            console_bottom_frame_4=             customtkinter.CTkLabel(master = first_option_frame,height=50,text =supported_formats_deleting,justify = "left",font=("Arial",22))
            label_supported_formats_deleting.   grid(column =0,row=row_index+1,sticky = tk.W,pady =10,padx=10)
            formats_deleting_input.             grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=10)
            button_save4.                       grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=215)
            button_pop2.                        grid(column =0,row=row_index+2,sticky = tk.W,pady =0,padx=290)
            console_bottom_frame_4.             grid(column =0,row=row_index+3,sticky = tk.W,pady =0,padx=10)

            console_frame =                     customtkinter.CTkFrame(master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1,fg_color="black")
            console_frame.                      pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top")
            main_console =                      customtkinter.CTkLabel(master = console_frame,height=20,text = str(main_console_text),text_color=str(main_console_text_color),justify = "left",font=("Arial",22))
            if self.windowed:
                save_frame =                    customtkinter.CTkFrame(     master = self.bottom_frame_default_path,height=50,corner_radius=0,border_width=1)
                save_frame.                     pack(pady=(10,0),padx=5,fill="x",expand=False,side = "top",anchor = "e")
                save_changes_button =               customtkinter.CTkButton(master = save_frame,width=150,height=40, text = "Aplikovat/ načíst změny", command = lambda: self.refresh_main_window(),font=("Arial",22,"bold"))

            main_console.                       grid(column =0,row=row_index+7,sticky = tk.W,pady =10,padx=10)
            if self.windowed:
                save_changes_button.            pack(pady =5,padx=10,anchor = "e")

            if self.selected_language == "en":
                label_supported_formats_deleting.configure(text = "Set supported formats for options: DELETING")
                button_save4.configure(text = "Save")
                button_pop2.configure(text = "Remove")
                console_bottom_frame_4.configure(text = f"Currently set supported formats for deletion options: {text_file_data[1]}")
                save_changes_button.configure(text = "Apply/ load changes")

            def add_or_rem_formats(e):
                self.current_root.focus_set()
            formats_deleting_input.bind("<Return>",add_or_rem_formats)

    def creating_advanced_option_widgets(self): # Vytváří veškeré widgets (advance option MAIN)
        if self.windowed:
            self.current_root=customtkinter.CTkToplevel()
            x = self.root.winfo_rootx()
            y = self.root.winfo_rooty()
            self.current_root.geometry(f"1250x900+{x+200}+{y+200}")
            self.current_root.title("Pokročilá nastavení")
            if self.selected_language == "en":
                self.current_root.title("Advanced option")
            self.current_root.after(200, lambda: self.current_root.iconbitmap(app_icon))
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
        options2 =          customtkinter.CTkButton(master = self.menu_buttons_frame, width = 200,height=50,text = "Počáteční parametry",   command =  lambda: self.setting_widgets(submenu_option="set_default_parametres"),font=("Arial",20,"bold"),corner_radius=0,fg_color="black",hover_color="#212121")
        options3 =          customtkinter.CTkButton(master = self.menu_buttons_frame, width = 200,height=50,text = "Podporované formáty",   command =  lambda: self.setting_widgets(submenu_option="set_supported_formats"),font=("Arial",20,"bold"),corner_radius=0,fg_color="black",hover_color="#212121")
        label0.             grid(column = 0,row=0,sticky = tk.W,pady =10,padx=10)
        shift_const = 210
        if not self.windowed:
            main_menu_button.grid(column = 0,row=0,pady = (10,0),padx =10,sticky = tk.W)
            shift_const = 0
        options0.           grid(column = 0,row=0,pady = (10,0),padx =220-shift_const,sticky = tk.W)
        options2.           grid(column = 0,row=0,pady = (10,0),padx =430-shift_const,sticky = tk.W)
        options3.           grid(column = 0,row=0,pady = (10,0),padx =640-shift_const,sticky = tk.W)
        self.option_buttons = [options0,options2,options3]

        if self.windowed and not global_recources_load_error:
            if self.spec_location == "image_browser":
                self.setting_widgets(submenu_option="set_image_browser_setting")
            else:
                self.setting_widgets(submenu_option="default_path")
        elif not global_recources_load_error:
            self.setting_widgets(submenu_option="default_path")
        elif global_recources_load_error:
            error_label = customtkinter.CTkLabel(master = self.bottom_frame_default_path,height=20,text = "Nepodařilo se načíst konfigurační soubor jhv_MAZ.json (nastavení se nemá kam uložit)",justify = "left",font=("Arial",22,"bold"),text_color="red")
            error_label.grid(column = 0,row=0,pady = (10,0),padx =20,sticky = tk.W)
            options0.configure(state = "disabled")
            options2.configure(state = "disabled")
            options3.configure(state = "disabled")
            if self.selected_language == "en":
                error_label.configure(text = "Failed to load the jhv_MAZ.json configuration file (settings have nowhere to save)")

        if self.selected_language == "en":
            label0.configure(text = "Set the desired parameters (settings will be saved even after the application is shut down): ")
            options0.configure(text = "Basic settings")
            options2.configure(text = "Initial parameters")
            options3.configure(text = "Supported formats")

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

class Deleting_option: # Umožňuje mazat soubory podle nastavených specifikací
    """
    Umožňuje mazat soubory podle nastavených specifikací

    -obsahuje i režim testování, kde soubory pouze přesune do složky ke smazání
    -umožňuje procházet více subsložek
    
    """

    def __init__(self,root):
        self.root = root
        self.unbind_list = []
        self.text_file_data = Tools.read_json_config()
        self.supported_formats_deleting = self.text_file_data[1]
        self.files_to_keep = self.text_file_data[2]
        self.cutoff_date = self.text_file_data[3]
        self.to_delete_folder_name = self.text_file_data[4]
        self.selected_language = self.text_file_data[11]
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
        - (deleting)
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
            Tools.add_new_path_to_history(str(output[1]))
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
            path_history = Tools.read_json_config()[10]
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
        menu_button =           customtkinter.CTkButton(master = frame_with_cards, width = 250,height=50,text = "MENU", command =  lambda: self.call_extern_function(function="menu"),font=("Arial",20,"bold"),corner_radius=0,fg_color="black",hover_color="#212121")
        deleting_button =       customtkinter.CTkButton(master = frame_with_cards, width = 250,height=50,text = "Mazání souborů",font=("Arial",20,"bold"),corner_radius=0,fg_color="#212121",hover_color="#212121")
        menu_button.            pack(pady = (10,0),padx =(10,0),anchor = "s",side = "left")
        deleting_button.        pack(pady = (10,0),padx =(10,0),anchor = "s",side = "left")
        frame_with_cards.       pack(pady=0,padx=0,fill="both",expand=True,side = "left",anchor="w")
        frame_with_logo =       customtkinter.CTkFrame(master=top_frame,corner_radius=0)
        logo =                  customtkinter.CTkImage(Image.open(Tools.resource_path("images/jhv_logo.png")),size=(300, 100))
        image_logo =            customtkinter.CTkLabel(master = frame_with_logo,text = "",image =logo)
        frame_with_logo.        pack(pady=0,padx=0,expand=False,side = "left",anchor="e")
        image_logo.             pack(pady = 0,padx =(15,0),ipadx = 20,ipady = 10,expand=False)
        top_frame.              pack(pady=0,padx=0,fill="x",side = "top")

        frame_path_input =      customtkinter.CTkFrame(master=header_frame,corner_radius=0)
        context_menu_button  =  customtkinter.CTkButton(master =frame_path_input, width = 50,height=50, text = "V",font=("Arial",20,"bold"),corner_radius=0,fg_color="#505050")
        self.path_set    =      customtkinter.CTkEntry(master =frame_path_input,height=50,font=("Arial",20),corner_radius=0)
        tree        =           customtkinter.CTkButton(master =frame_path_input,height=50,width = 180,text = "EXPLORER", command = self.call_browseDirectories,font=("Arial",20,"bold"))
        button_save_path =      customtkinter.CTkButton(master =frame_path_input,height=50,text = "Uložit cestu", command = lambda: Tools.save_path(self.console,self.path_set.get()),font=("Arial",20,"bold"))
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
        bottom_frame .          pack(pady =0,padx=0,side = "top",fill="both",expand=False)
        header_frame.           pack(pady=0,padx=0,fill="x",side = "top")
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

        recources_path = self.text_file_data[0]
        if recources_path != False and recources_path != "/":
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

