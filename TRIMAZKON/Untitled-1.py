import sys
from plyer import notification
import psutil
# CREATING TASK:
# name_of_task = "dailyscript_test"
# path_to_app = r"C:\Users\jakub.hlavacek.local\Desktop\JHV\Work\TRIMAZKON\pipe_server\untitled2.py"
# cmd_command = f"schtasks /Create /TN {name_of_task} /TR {path_to_app} /SC DAILY /ST 09:35"
# connection_status = subprocess.call(cmd_command,shell=True,text=True)

#DELETING TASK:
# name_of_task = "dailyscript_test"
# cmd_command = f"schtasks /Delete /TN {name_of_task} /F"
# connection_status = subprocess.call(cmd_command,shell=True,text=True)

print(len(str("")))
all_string = "|||Datum: 17.12.2024 10:12:26||Zkontrolováno: 161 souborů||Starších: 153 souborů||Smazáno: 0 souborů"
print(all_string.split("|||"))
splitted = all_string.split("|||")
splitted.pop(0)
print(splitted[0].split("||"))
output_data = ["xx","xxf","xxx","sga"]
output_message_clear = f"Provedeno: {output_data[3]}\nZkontrolováno: {output_data[0]} souborů\nStarších: {output_data[1]} souborů\nSmazáno: {output_data[2]} souborů"

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

WindowsBalloonTip("Title for popup", "This is the popup's message",'images/logo_TRIMAZKON.ico')



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
