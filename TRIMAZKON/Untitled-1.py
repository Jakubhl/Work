
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

interfaces = ['Ethernet 2', 'Ethernet 3', 'Ethernet 5', 'Wi-Fi', 'Ethernet 4', 'Ethernet']
interface_statuses = ['Disconnected', 'Disconnected', 'Disconnected', 'Connected', 'Disconnected', 'Disconnected']
print("status: ", interface_statuses)
connected_interfaces =[]
for items in interface_statuses:
    if (items != "Odpojen") and (items != "Odpojeno") and (items != "Disconnected"):
        print(items)
        connected_interfaces.append(interfaces[interface_statuses.index(items)])
print("online: ", connected_interfaces)