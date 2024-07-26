
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
import re


import ctypes
import subprocess
import sys
import time
# customtkinter.set_appearance_mode("dark")
# customtkinter.set_default_color_theme("dark-blue")
# root=customtkinter.CTk()
# root.geometry("1200x900")
# root.state("zoomed")
# root.title("TRIMAZKON v_3.6.2")
# # Configure the column to allow the label to expand horizontally
# project_tree =     customtkinter.CTkScrollableFrame(master=root,corner_radius=0)
# project_tree.      pack(pady=5,padx=5,fill="both",expand=True,side = "top")
# column1 =  customtkinter.CTkLabel(master = project_tree, width = 20,height=30,text = "Projekt: ",font=("Arial",20,"bold"))
# column2 =  customtkinter.CTkLabel(master = project_tree, width = 20,height=30,text = "IPv4 adresa: ",font=("Arial",20,"bold"))
# column3 =  customtkinter.CTkLabel(master = project_tree, width = 20,height=30,text = "Poznámky: ",font=("Arial",20,"bold"))
# column1.pack(pady = 5,padx =10,side = "left",anchor = "n",expand = True)
# column2.pack(pady = 5,padx =10,side = "left",anchor = "n",expand = True)
# column3.pack(pady = 5,padx =10,side = "left",anchor = "n",expand = True)
# column1 =  customtkinter.CTkLabel(master = project_tree, width = 20,height=30,text = "Projekt: ",font=("Arial",20,"bold"))
# column2 =  customtkinter.CTkLabel(master = project_tree, width = 20,height=30,text = "IPv4 adresa: ",font=("Arial",20,"bold"))
# column3 =  customtkinter.CTkLabel(master = project_tree, width = 20,height=30,text = "Poznámky: ",font=("Arial",20,"bold"))
# column1.pack(pady = 5,padx =10,side = "top",anchor = "s",expand = False)
# column2.pack(pady = 5,padx =10,side = "left",anchor = "s",expand = True)
# column3.pack(pady = 5,padx =10,side = "left",anchor = "s",expand = True)

# string = "RESULT: b'\r\nWindows IP Configuration\r\n\r\n\r\nEthernet adapter Ethernet 5:\r\n\r\n   Media State . . . . . . . . . . . : Media disconnected\r\n   Connection-specific DNS Suffix  . : \r\n\r\nWireless LAN adapter P\xfdipojen\xa1 k m\xa1stn\xa1 s\xa1ti* 1:\r\n\r\n   Media State . . . . . . . . . . . : Media disconnected\r\n   Connection-specific DNS Suffix  . : \r\n\r\nWireless LAN adapter P\xfdipojen\xa1 k m\xa1stn\xa1 s\xa1ti* 2:\r\n\r\n   Media State . . . . . . . . . . . : Media disconnected\r\n   Connection-specific DNS Suffix  . : \r\n\r\nEthernet adapter Ethernet 2:\r\n\r\n   Media State . . . . . . . . . . . : Media disconnected\r\n   Connection-specific DNS Suffix  . : \r\n\r\nWireless LAN adapter Wi-Fi:\r\n\r\n   Connection-specific DNS Suffix  . : \r\n   IPv6 Address. . . . . . . . . . . : 2a00:11b1:1080:128d:6697:34a9:cb75:cfcb\r\n   Temporary IPv6 Address. . . . . . : 2a00:11b1:1080:128d:cd97:8ea1:3d4f:3b33\r\n   Link-local IPv6 Address . . . . . : fe80::541d:930c:6cbc:7daf%10\r\n   IPv4 Address. . . . . . . . . . . : 192.168.48.52\r\n   Subnet Mask . . . . . . . . . . . : 255.255.255.0\r\n   Default Gateway . . . . . . . . . : fe80::3c4c:4eff:fe6f:a9d1%10\r\n                                       192.168.48.208\r\n\r\nEthernet adapter Ethernet:\r\n\r\n   Media State . . . . . . . . . . . : Media disconnected\r\n   Connection-specific DNS Suffix  . : \r\n'"
# # root.mainloop()
# ipv4_pattern = re.compile(r'IPv4 Address[.\s]*: ([\d.]+)')
# # Dictionary to store interface names and their IPv4 addresses
# ipv4_addresses = []
# # Split the output by lines
# lines = string.splitlines()
# # lines = result2.splitlines()
# current_interface = None
# # Iterate over each line to find interface names and IPv4 addresses
# for line in lines:
#     if line.strip():
#         # Detect interface name
#         if line[0].isalpha():
#             current_interface = line.strip()
#         else:
#             # Detect IPv4 address for the current interface
#             match = ipv4_pattern.search(line)
#             if match and current_interface:
#                 ipv4_addresses.append(current_interface)
#                 ipv4_addresses.append(match.group(1))
#                 print(current_interface,match.group(1))
#                 #ipv4_addresses[current_interface] = match.group(1)
string = "cpolyoxyethylen"
print(string[1:3])

print(string[3:5])

print(int(string))