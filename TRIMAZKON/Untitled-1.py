
import customtkinter
import tkinter as tk
from PIL import Image
import psutil
import socket
import threading
import time
import os
import time

def make_sure_ip_changed():
    def call_subprocess():
        time.sleep(5)
        print("what about now")
        
    run_background = threading.Thread(target=call_subprocess,)
    run_background.start()

    return True

make_sure_ip_changed()
print("hurra")