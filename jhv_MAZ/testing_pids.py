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



msg = "Execute file deleting"
if "Execute file deleting" in msg:
    print("jo")