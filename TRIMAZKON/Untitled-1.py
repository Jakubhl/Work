
import customtkinter
import tkinter as tk
from PIL import Image
import psutil
import socket
import threading
import time
import os

def call_subprocess():
    time.sleep(5)
        
run_background = threading.Thread(target=call_subprocess,)
run_background.start()

print("ahaa")
    

print("jo")