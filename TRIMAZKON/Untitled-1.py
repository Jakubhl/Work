
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

import subprocess
interface_name = "Ethernet 4"
ip = "192.168.18.241"
mask = "255.255.255.0"

import ctypes
import subprocess
import sys
import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Re-run the script with administrative privileges."""
    try:
        params = " ".join([sys.executable] + sys.argv)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    except Exception as e:
        print(f"Failed to elevate privileges: {e}")
    sys.exit()

def enable_interface(interface_name):
    """Enable the network interface."""
    enable_command = f"netsh interface set interface \"{interface_name}\" admin=ENABLED"
    subprocess.run(enable_command, shell=True)

def set_static_ip(interface_name, ip, mask):
    """Set the static IP address of the network interface."""
    netsh_command = f"netsh interface ip set address \"{interface_name}\" static {ip} {mask}"
    subprocess.run(netsh_command, shell=True)

def check_interface_status(interface_name):
    """Check if the interface is connected."""
    check_command = f"netsh interface show interface \"{interface_name}\""
    result = subprocess.run(check_command, capture_output=True, text=True, shell=True)
    return "Connected" in result.stdout

# Define your interface name, IP, and mask
interface_name = "Ethernet 4"
ip = "192.168.1.100"
mask = "255.255.255.0"

# Check for admin rights and run the command
if not is_admin():
    run_as_admin()
else:
    # Ensure the interface is enabled
    enable_interface(interface_name)
    time.sleep(2)  # Wait a moment to allow the interface to enable

    # Check if the interface is connected
    if not check_interface_status(interface_name):
        print(f"The interface '{interface_name}' is not connected. Please connect it and try again.")
        sys.exit(1)

    # Set the static IP address
    set_static_ip(interface_name, ip, mask)
    print(f"IP address set to {ip} with mask {mask} on interface '{interface_name}'")
