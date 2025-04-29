import sys
from plyer import notification
import psutil
import subprocess
import os
import shlex
import threading
import time
from multiprocessing import Process
# CREATING TASK:
# name_of_task = "dailyscript_test"
# path_to_app = r"C:\Users\jakub.hlavacek.local\Desktop\JHV\Work\TRIMAZKON\pipe_server\untitled2.py"
# cmd_command = f"schtasks /Create /TN {name_of_task} /TR {path_to_app} /SC DAILY /ST 09:35"
# connection_status = subprocess.call(cmd_command,shell=True,text=True)

#DELETING TASK:
# name_of_task = "dailyscript_test"
# cmd_command = f"schtasks /Delete /TN {name_of_task} /F"
# connection_status = subprocess.call(cmd_command,shell=True,text=True)
# msi_path = f"{initial_path}Installers/{wanted_installer}"
def call_installer(msi_path):
    # os.startfile(msi_path)
    # return
    # subprocess.run(msi_path, shell=True)
    # subprocess.call(msi_path, shell=True,start_new_session=True)

    # p = subprocess.Popen(["cmd.exe", "/c",msi_path],
    #     cwd="/",
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.STDOUT)
    
    # process_handler = subprocess.Popen(["cmd.exe", "/c",msi_path], 
    #                                    creationflags=subprocess.DETACHED_PROCESS)
    cmd = str(msi_path)
    cmds = shlex.split(cmd)
    # p = subprocess.Popen(["cmd.exe", "/c",str(msi_path)], start_new_session=True)
    p = subprocess.Popen(msi_path,shell=True, start_new_session=True)
    # sys.exit(0)

    # subprocess.Popen(
    #     ["cmd.exe", "/c",msi_path],
    #     # start_new_session=True,
    #     creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
    #     close_fds=True,
    #     stdout=subprocess.DEVNULL,
    #     stderr=subprocess.DEVNULL

    # )

def exit_and_launch(msi_path):
    # Wrap the path in quotes to handle spaces and avoid extra escape characters
    cmd = f'timeout /t 3 && {msi_path}'
    
    # Run the command in a new subprocess
    subprocess.Popen(["cmd.exe", "/c", msi_path],
                     creationflags=subprocess.CREATE_BREAKAWAY_FROM_JOB | subprocess.CREATE_NO_WINDOW,
                     )
    
msi_path = "C:/Users/jakub.hlavacek.local/Desktop/JHV/Work/TRIMAZKON/Installers/TRIMAZKON-4.3.3-win64.msi"

exit_and_launch(msi_path)
# childProc = threading.Thread(target=exit_and_launch,args = [msi_path])
# childProc.start()
time.sleep(3)
# childProc.join()
# xx = threading.Thread(target=exit_and_launch,args=[msi_path])
# xx.start()

# k=input("kkt?")

# def call_test():
#     notification.notify(
#             title="Bylo provedeno automatické mazání",
#             message=output_message_clear,
#             app_name="TRIMAZKON", 
#             timeout=5,
#             app_icon = 'images/logo_TRIMAZKON.ico'
#         )
# call_test()
# from plyer.utils import platform
from win32api import *
from win32gui import *
import win32con
import sys, os
import struct
import time
from PIL import Image, ImageDraw
 
class WindowsBalloonTip:
    def __init__(self, title, msg,app_icon_path):
        message_map = {
                win32con.WM_DESTROY: self.OnDestroy,
        }
        # Register the Window class.
        wc = WNDCLASS()
        hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map # could also specify a wndproc.
        classAtom = RegisterClass(wc)
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = CreateWindow( classAtom, "Taskbar", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, hinst, None)
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "images/logo_TRIMAZKON.ico" ))
        # iconPathName = os.path.abspath(os.path.join(sys.path[0], app_icon_path))
        print(iconPathName)
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
            # hicon = LoadIcon(hinst, win32con.IDI_WARNING)
            hicon = LoadImage(0,  # No module instance (use the system instance)
                    win32con.IDI_WARNING,
                    win32con.IMAGE_ICON,
                    0, 0,  # Default size
                    win32con.LR_SHARED
            )
            #    hicon = LoadIcon(0, win32con.IDI_WARNING)
            # hicon = LoadImage(hinst, iconPathName,win32con.IMAGE_ICON, 16, 16, icon_flags)
            #    hicon = Image.open(iconPathName)
           
        except Exception as e:
            print("tady",e)
            hicon = LoadIcon(0, win32con.IDI_WARNING)

        UpdateWindow(self.hwnd)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        UpdateWindow(self.hwnd)
        Shell_NotifyIcon(NIM_MODIFY, \
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Balloon  tooltip",msg,200,title))
        UpdateWindow(self.hwnd)
        # self.show_balloon(title, msg)
        time.sleep(10)
        DestroyWindow(self.hwnd)
    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.

# WindowsBalloonTip("Title for popup", "This is the popup's message",'images/logo_TRIMAZKON.ico')

# for process in psutil.process_iter(['pid', 'name', 'status']):
#     try:
#         print(f"PID: {process.info['pid']}, Name: {process.info['name']}, Status: {process.info['status']}")
#     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#         pass  # Handle cases where processes are inaccessible

# icon_path = Tools.resource_path('images/logo_TRIMAZKON.ico')
# notification.notify(title="Bylo provedeno automatické mazání",
#                     message=str(output_message_clear),
#                     # app_name="TRIMAZKON",
#                     app_icon='images/logo_TRIMAZKON.ico')
# def get_all_app_processes():
#     pid_list = []
#     num_of_apps = 0
#     for process in psutil.process_iter(['pid', 'name']):
#         # if process.info['name'] == "TRIMAZKON_test.exe":
#         if process.info['name'] == "TRIMAZKON.exe" or process.info['name'] == "trimazkon_tray_v2.exe":
            
#             print(process.info['name'])
#             pid_list.append(process.info['pid'])
#             num_of_apps+=1
    
#     return [num_of_apps,pid_list]
# print(get_all_app_processes())
# from win10toast_click import ToastNotifier

# Callback function to handle the click event
# def on_notification_click():
#     print("Notification was clicked!")
#     return True

# # Create a ToastNotifier instance
# toaster = ToastNotifier()

# # Show the notification and set the click callback
# try:
#     toaster.show_toast(
#         "My Application",                    # Notification title
#         output_message_clear,  # Notification message
#         icon='images/logo_TRIMAZKON.ico',
#         duration=10,                         # Duration in seconds
#         threaded=True,                       # Allows the program to keep running
#         callback_on_click=lambda:on_notification_click()  # Function to call on click
#     )
# except Exception as e:
#     pass
