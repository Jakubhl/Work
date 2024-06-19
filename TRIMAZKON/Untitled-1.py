
import customtkinter
import tkinter as tk
from PIL import Image
import psutil
import socket
import threading
import time
import os
import time
import ctypes
import sys


import ctypes
import subprocess
import sys
import time
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root=customtkinter.CTk()
root.geometry("1200x900")
root.title("TRIMAZKON v_3.6.2")
# Configure the column to allow the label to expand horizontally
root.grid_columnconfigure(0, weight=1)

project_frame =  customtkinter.CTkFrame(master=root,corner_radius=0,fg_color="black",border_width=2,height=50,width=200)
project_frame.grid(row=0,column=0,padx=10,sticky=tk.NSEW)
# project_frame.grid_propagate(1)
# project_frame.grid_configure(sticky="nsew")
# project_frame.grid_propagate()

root.mainloop()