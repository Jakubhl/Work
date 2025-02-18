import customtkinter
import os
import time
from PIL import Image
import Deleting_option_v2 as Deleting
import trimazkon_tray_MAZ_v2 as trimazkon_tray
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
import struct

def get_all_app_processes():
    pid_list = []
    num_of_apps = 0
    for process in psutil.process_iter(['pid', 'name']):
        # if process.info['name'] == "TRIMAZKON_test.exe":
        if process.info['name'] == "jhv_MAZ.exe":
            print(process.info)
            pid_list.append(process.info['pid'])
            num_of_apps+=1
    
    return [num_of_apps,pid_list]

# print(get_all_app_processes())

# string = "platnost vypršela:"
# print(string.replace("platnost","nic"))

# class WindowsBalloonTip:
#     """
#     Windows system notification (balloon tip).
#     """
#     _class_registered = False  # Ensures window class is registered only once

#     def __init__(self, title, msg, app_icon):
#         message_map = {
#             win32con.WM_DESTROY: self.OnDestroy,
#         }

#         hinst = GetModuleHandle(None)
#         class_name = "PythonTaskbar"
#         try:
#             if not WindowsBalloonTip._class_registered:
#                 # Register the Window class once
#                 wc = WNDCLASS()
#                 wc.hInstance = hinst
#                 wc.lpszClassName = class_name
#                 wc.lpfnWndProc = message_map
#                 RegisterClass(wc)
#                 WindowsBalloonTip._class_registered = True  # Mark as registered
#         except Exception:
#             wc = WNDCLASS()
#             wc.hInstance = hinst
#             wc.lpszClassName = class_name
#             wc.lpfnWndProc = message_map
#             RegisterClass(wc)

#         # Create a new window (without re-registering the class)
#         style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
#         self.hwnd = CreateWindow(class_name, "Taskbar", style, 
#                                  0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, 
#                                  0, 0, hinst, None)

#         UpdateWindow(self.hwnd)

#         # Load icon
#         icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
#         try:
#             hicon = LoadImage(hinst, app_icon, win32con.IMAGE_ICON, 0, 0, icon_flags)
#         except:
#             hicon = LoadIcon(0, win32con.IDI_APPLICATION)

#         # Display notification
#         # flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
#         flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
#         nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
#         Shell_NotifyIcon(NIM_ADD, nid)

#         Shell_NotifyIcon(NIM_MODIFY, 
#                          (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,
#                           hicon, "Balloon tooltip", msg, 200, title))

#         # time.sleep(10)  # Display the notification for 10 seconds
#         # self.cleanup()

#     def cleanup(self):
#         """ Removes the notification icon and destroys the window. """
#         nid = (self.hwnd, 0)
#         Shell_NotifyIcon(NIM_DELETE, nid)
#         DestroyWindow(self.hwnd)

#     def OnDestroy(self, hwnd, msg, wparam, lparam):
#         """ Handles window destruction. """
#         self.cleanup()
#         PostQuitMessage(0)  # Terminate the app.

# app_icon = 'images/logo_TRIMAZKON.ico'
# WindowsBalloonTip("ahoj",
#                     "tohle je na nic",
#                     app_icon)



def check_task_existence_in_TS(taskname):

    # ps_command = f'schtasks /query /tn \"{taskname}\" /v /fo LIST'
    ps_command = f"Get-ScheduledTask -TaskName {taskname}"
    powershell_command = [
        'powershell.exe',
        # '-Command', f'Start-Process powershell -Verb RunAs -ArgumentList \'-Command "{ps_command}"\' -WindowStyle Hidden -PassThru'
        '-Command', ps_command
    ]

    # process = subprocess.Popen(f'schtasks /query /tn \"{taskname}\" /v /fo LIST',
    process = subprocess.Popen(powershell_command,
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
    if "ERROR" in error_data:
        return False
    else:
        return True
    
# check_task_existence_in_TS("jhv_MAZ_startup_tray_setup")


def establish_startup_tray():
    """
    Sets the startup task of switching on the tray application icon
    - if it doesnt exist already
    """

    # path_app_location = str(initial_path + exe_name)
    path_app_location = str(r"C:\Users\jakub.hlavacek.local\AppData\Local\Programs\jhv_MAZ") + str("jhv_MAZ.exe")
    exe_args = "run_tray"
    # task_command = "\"" + path_app_location + " run_tray" + "\" /sc onlogon"
    # ps_command = f"schtasks /Create /TN {cls.task_name} /TR {task_command}"
    ps_command = f"""
    $action = New-ScheduledTaskAction -Execute "{path_app_location}" -Argument "{exe_args}";
    $trigger = New-ScheduledTaskTrigger -AtLogon;
    Register-ScheduledTask -TaskName "jhv_MAZ_startup_tray_setup" -Action $action -Trigger $trigger -User "SYSTEM" -RunLevel Highest
    """
    # powershell_command = [
    #     'powershell.exe',
    #     '-Command', f'Start-Process powershell -Verb RunAs -ArgumentList \'-Command "{ps_command}"\' -WindowStyle Hidden -PassThru'
    # ]

    powershell_command = [
        'powershell.exe',
        '-ExecutionPolicy', 'Bypass',
        '-NoProfile',
        '-Command', f'Start-Process powershell -WindowStyle Hidden -Verb RunAs -ArgumentList "-ExecutionPolicy Bypass -NoProfile -Command \"{ps_command}\""'
    ]
    powershell_command = [
        'powershell.exe',
        '-Command', ps_command
    ]

    try:
        # process = subprocess.Popen(['powershell.exe', '-Command', ps_command],
        process = subprocess.Popen(powershell_command,
        # process = subprocess.Popen(["powershell", "-ExecutionPolicy", "Bypass", "-NoProfile", "-Command", powershell_command],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    creationflags=subprocess.CREATE_NO_WINDOW)

        # process = subprocess.Popen(f"schtasks /Create /TN {cls.task_name} /TR {task_command}",
        #                             stdout=subprocess.PIPE,
        #                             stderr=subprocess.PIPE,
        #                             creationflags=subprocess.CREATE_NO_WINDOW)
        
        stdout, stderr = process.communicate()
        stdout_str = stdout.decode('utf-8').strip()
        stderr_str = stderr.decode('utf-8').strip()
        output_message = "out"+str(stdout_str) +"err"+str(stderr_str)
        print(output_message)

        if "Access is denied" in output_message or "Run as administrator" in output_message:
            return "need_access"
            
    except Exception as e:
        return False

establish_startup_tray()